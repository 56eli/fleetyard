#!/usr/bin/env python3
"""Append ONE row to `fleet/CONTROL.log` under an exclusive lock — the lane's cadence signal.

Why a tool: ORCH-2 reported (cycle J, re-reported in the repair map) that this lane's `CONTROL.log`
utc column had minute-precision rows, two forward stamps, a backward jump, and **seq values used
twice** — so a cadence reader must not treat `seq` as a unique key. Part of that was two writers
(hand-written rows and the cadence watcher's auto-rows) interleaving: both computed `seq = max + 1`
from a file the other was changing.

This tool makes the row-writing atomic and the invariants checkable:

  * exclusive `flock` on the log for the read-modify-append, so two writers cannot pick one seq;
  * `seq` = max(existing) + 1, computed inside the lock — unique by construction;
  * the row's stamp defaults to `date -u` and is refused if it would go **backwards** (an
    append-only signal log must be orderable), unless `--allow-backward` states why;
  * exact-to-the-second stamps only (a minute-precision stamp is refused: it is the defect the
    gate ruled on, and the column is the boss's liveness input under ERRATA-25f);
  * the note is single-line (a row is one line) and is written verbatim.

Usage:
  python3 tools/control_row.py --commit <sha> --status OK --note "…"
  python3 tools/control_row.py --commit <sha> --status ERRATA --note-file /tmp/note.txt
  python3 tools/control_row.py --check           # report the invariants for the whole file
"""
import argparse
import datetime
import fcntl
import hashlib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTROL = os.path.join(ROOT, "fleet", "CONTROL.log")
REGISTRY = os.path.join(ROOT, "fleet2", "activations", "REGISTRY.md")
WORKER = "A-2026-09-25-001"
EXACT = re.compile(r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def registry_sha():
    """The canonical registry digest: the copy at origin/main when it can be read."""
    out = subprocess.run(("git", "-C", ROOT, "show", "origin/main:fleet2/activations/REGISTRY.md"),
                         capture_output=True)
    blob = out.stdout if out.returncode == 0 else None
    if blob is None and os.path.exists(REGISTRY):
        with open(REGISTRY, "rb") as fh:
            blob = fh.read()
    return hashlib.sha256(blob or b"").hexdigest()


def parse(lines):
    rows = []
    for n, line in enumerate(lines, 1):
        f = line.rstrip("\n").split("|")
        if len(f) < 6:
            continue
        rows.append({"line": n, "utc": f[0], "commit": f[1], "worker": f[2], "registry": f[3],
                     "seq": f[4], "status": f[5], "note": "|".join(f[6:])})
    return rows


def check(verbose=True):
    with open(CONTROL, encoding="utf-8") as fh:
        rows = parse(fh.readlines())
    problems = []
    seen = {}
    for r in rows:
        if not EXACT.match(r["utc"]):
            problems.append("line %d: stamp %r is not exact to the second" % (r["line"], r["utc"]))
        if r["seq"] in seen:
            problems.append("line %d: seq %s already used at line %d"
                            % (r["line"], r["seq"], seen[r["seq"]]))
        seen[r["seq"]] = r["line"]
    for a, b in zip(rows, rows[1:]):
        if b["utc"] < a["utc"]:
            problems.append("line %d: stamp %s goes backwards after %s"
                            % (b["line"], b["utc"], a["utc"]))
    if verbose:
        for p in problems:
            print("FAIL: %s" % p)
        if not problems:
            print("control log: OK (%d rows, exact stamps, unique seqs, non-decreasing)"
                  % len(rows))
    return problems


def append(commit, status, note, utc=None, allow_backward=None):
    if "\n" in note or "\r" in note:
        raise SystemExit("control_row: a row is one line; the note contains a newline")
    stamp = utc or utc_now()
    if not EXACT.match(stamp):
        raise SystemExit("control_row: %r is not exact to the second (use date -u)" % stamp)
    os.makedirs(os.path.dirname(CONTROL), exist_ok=True)
    with open(CONTROL, "a+", encoding="utf-8") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        fh.seek(0)
        rows = parse(fh.readlines())
        seqs = [int(r["seq"]) for r in rows if r["seq"].isdigit()]
        seq = (max(seqs) + 1) if seqs else 1
        if rows and stamp < rows[-1]["utc"]:
            if not allow_backward:
                raise SystemExit("control_row: refusing a backward stamp (%s after %s) without "
                                 "--allow-backward stating why" % (stamp, rows[-1]["utc"]))
        fh.seek(0, os.SEEK_END)
        fh.write("%s|%s|%s|%s|%d|%s|%s\n"
                 % (stamp, commit or "UNPINNED", WORKER, registry_sha(), seq, status, note))
        fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
    print("control_row: seq %d appended (%s, %s)" % (seq, stamp, status))
    return seq


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--commit", default=None)
    ap.add_argument("--status", default="OK")
    ap.add_argument("--note", default=None)
    ap.add_argument("--note-file", default=None)
    ap.add_argument("--utc", default=None)
    ap.add_argument("--allow-backward", default=None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return 1 if check() else 0
    note = a.note
    if a.note_file:
        with open(a.note_file, encoding="utf-8") as fh:
            note = fh.read().strip()
    if not note:
        raise SystemExit("control_row: --note or --note-file is required")
    append(a.commit, a.status, note.replace("\n", " "), a.utc, a.allow_backward)
    return 1 if check() else 0


if __name__ == "__main__":
    sys.exit(main())
