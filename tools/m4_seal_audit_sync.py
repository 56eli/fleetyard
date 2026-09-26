#!/usr/bin/env python3
"""Re-run the seal audit and keep the companion appendix's citations in step — one command.

The audit report's digest and its exact `audit_utc` are cited by
`runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md`, and the audit itself checks that citation
(item v2.c). So the two have to be written in a fixed order, or each write stales the other:

  1. run    -> the report carries the new stamp (the appendix still cites the old one -> owed)
  2. sync   -> the appendix cites the new stamp as live and the old one as superseded history
  3. run    -> the report now sees a single live citation and no unmarked conflict
  4. sync   -> the appendix's cited report digest follows that second report's bytes
  5. run    -> must reproduce step 4's report byte-for-byte (nothing left to chase)

This is a maintenance helper for THIS lane's artefacts, not a gate instrument. It refuses to run
if the working tool differs from the committed blob (so a report is never attributed to bytes that
were never committed), and it stops at the first step that does not behave as described.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = "runs/m4-q2-adjudication/SEAL-AUDIT.json"
APPENDIX = "runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md"
TOOL = "tools/m4_seal_audit.py"
SEAL = "tools/HELD-OUT-SPLIT-V2.json"


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run_audit(stamp, out):
    p = subprocess.run([sys.executable, os.path.join(ROOT, TOOL), "--seal", SEAL, "--out", out,
                        "--utc", stamp], cwd=ROOT, capture_output=True, text=True)
    if p.returncode not in (0, 1):
        raise SystemExit("seal audit failed: %s" % (p.stderr or p.stdout))
    return p.stdout.strip().splitlines()[-1]


def sync_appendix(stamp, digest):
    path = os.path.join(ROOT, APPENDIX)
    text = open(path, encoding="utf-8").read()
    live = re.search(r"audit utc ([0-9TZ:-]+)\*\*, sha256 `([0-9a-f]{64})`", text)
    if not live:
        raise SystemExit("appendix: live citation row not found")
    old_stamp, old_digest = live.group(1), live.group(2)
    if old_stamp != stamp:
        text = text.replace(old_stamp, stamp)
        if "`%s`" % old_stamp in text:
            text = text.replace("and `%s` stay readable above" % old_stamp,
                                "and `%s` stay readable above" % old_stamp)
        else:
            text = text.replace("stay readable above",
                                "and `%s` stay readable above" % old_stamp, 1)
    text = text.replace(old_digest, digest)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return old_stamp, old_digest


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--utc", required=True, help="date -u at run time, exact to the second")
    a = ap.parse_args()
    tool_running = sha(os.path.join(ROOT, TOOL))
    tool_committed = hashlib.sha256(subprocess.run(
        ["git", "-C", ROOT, "show", "HEAD:%s" % TOOL], capture_output=True).stdout).hexdigest()
    if tool_running != tool_committed:
        raise SystemExit("refusing: the working %s differs from the committed blob — commit the "
                         "tool first, so the report is attributed to bytes that exist" % TOOL)

    print("1/5 run  ->", run_audit(a.utc, os.path.join(ROOT, REPORT)))
    old_stamp, old_digest = sync_appendix(a.utc, sha(os.path.join(ROOT, REPORT)))
    print("2/5 sync -> appendix live stamp %s (was %s); digest -> %s"
          % (a.utc, old_stamp, sha(os.path.join(ROOT, REPORT))[:12]))
    print("3/5 run  ->", run_audit(a.utc, os.path.join(ROOT, REPORT)))
    second = sha(os.path.join(ROOT, REPORT))
    sync_appendix(a.utc, second)
    print("4/5 sync -> appendix cites report digest %s" % second[:12])
    print("5/5 run  ->", run_audit(a.utc, os.path.join(ROOT, REPORT)))
    if sha(os.path.join(ROOT, REPORT)) != second:
        raise SystemExit("the third run does not reproduce the second — something is still "
                         "chasing, so the pair is NOT in step")
    import json
    rep = json.load(open(os.path.join(ROOT, REPORT), encoding="utf-8"))
    print("\nverdict: %s" % rep["verdict"]["one_line"])
    print("outstanding: %s | void: %s" % (rep["outstanding"], rep["void_reasons"]))
    print("appendix cited identically: %s"
          % rep["appendix_audit_utc_check"]["cited_identically"])
    print("report sha256 %s | stamps %s" % (second, a.utc))
    return 0 if not rep["outstanding"] and not rep["void_reasons"] else 1


if __name__ == "__main__":
    sys.exit(main())
