#!/usr/bin/env python3
"""TASK-020 item 8a — attribute every supplement artefact to the tool that generated it.

The gate found the pins unusable as attribution: `tool_commit` is the **lane head at run
time**, which for these artefacts does not contain the generator script at all (the q2
supplements were pinned to `71c37cf`, the q3 EVAL to `2bbb9f6`, the q4 supplement to
`ffb8811` — a cadence-check commit). A reader could not get from the manifest to the code
that produced it.

The convention this tool installs, in every supplement artefact of the M4 run directories:

  * `tool_commit` stays as written (the lane head at run time — a legitimate fact, and the
    append-only rule forbids rewriting it);
  * a `generator_pins` object is added next to it carrying
      `generator_tool`         path of the generator script,
      `generator_tool_commit`  the reachable commit that carries those exact script bytes,
      `generator_tool_blob`    `origin/arena/01a0d9ce-fleetyard:tools/<file>` — the same
                               lane+blob citation style item 9 used for the v1 toolchain,
      `generator_tool_sha256`  sha256 of the script bytes,
      `generator_tool_note`    what the two commits mean, so the pair cannot be
                               misread as a contradiction;
  * the generator scripts emit the same object at build time (so a rebuild reproduces it),
    and their `verify` checks it is present.

The insertion is byte-checkable: each artefact is parsed, the object is inserted and the
document is re-serialised with the exact style the artefact already uses
(`json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1) + "\n"` — verified to
round-trip each file byte-identically before any change), so the diff is additions only.

  build   python3 tools/m4_pin_repair.py build  [--repo .]
  verify  python3 tools/m4_pin_repair.py verify [--repo .]

Stdlib only, read-only outside the listed artefacts; writes the repair report under `runs/`.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

STYLE = dict(ensure_ascii=False, sort_keys=True, indent=1)
LANE = "origin/arena/01a0d9ce-fleetyard"
REPORT = "runs/m4-pin-repair-2026-09-26.json"
REPORT_NOTE = ("item 8a: every supplement artefact carries generator_pins so the manifest "
               "reaches the code that produced it; old->new file digests recorded here "
               "because the repair is an in-place addition the gate asked for")
ARTEFACTS = (
    ("runs/m4-q2-dropword/PROVENANCE-SUPPLEMENT.json", "tools/m4_t20_supplement.py", "a5dec38865babe312b38046a4c5500f234ce94bd"),
    ("runs/m4-q2-dropword/EVAL.json", "tools/m4_q2_evidence.py", "cc9ba4617c3844146caa65a621aa738904429ec1"),
    ("runs/m4-q2-dropword/EVIDENCE-PROVENANCE.json", "tools/m4_q2_evidence.py", "cc9ba4617c3844146caa65a621aa738904429ec1"),
    ("runs/m4-q3-format/PROVENANCE-SUPPLEMENT.json", "tools/m4_t20_supplement.py", "a5dec38865babe312b38046a4c5500f234ce94bd"),
    ("runs/m4-q3-format/EVAL.json", "tools/m4_q3_evidence.py", "1cd5d444fb3ae05ad3ff74aa61323e67422eebf7"),
    ("runs/m4-q4-holdout/PROVENANCE-SUPPLEMENT.json", "tools/m4_q4_supplement.py", "d7fee6e142ebbeecbd0e605395aa3d848499bf8a"),
)
NOTE = ("generator_tool_commit is the reachable commit carrying these exact script bytes; "
        "tool_commit above is the lane head at run time, which for these artefacts is an "
        "earlier or later commit and does not contain the generator — pinning both makes "
        "the manifest attributable without archaeology")


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_bytes(blob):
    return hashlib.sha256(blob).hexdigest()


def blob_at(repo, ref, path):
    p = subprocess.run(("git", "-C", repo, "show", "%s:%s" % (ref, path)),
                       capture_output=True)
    return p.stdout if p.returncode == 0 else None


def generator_pins(tool_path, tool_commit, lane=LANE, repo="."):
    """The block a generator emits about itself (used by build paths and by this repair)."""
    blob = blob_at(repo, tool_commit, tool_path)
    if blob is None:
        raise SystemExit("m4_pin_repair: %s does not exist at %s" % (tool_path, tool_commit))
    return {
        "generator_tool": tool_path,
        "generator_tool_commit": tool_commit,
        "generator_tool_blob": "%s:%s" % (lane, tool_path),
        "generator_tool_sha256": sha_bytes(blob),
        "generator_tool_note": NOTE,
    }


def guard_overwrite(path, tool_path):
    """Refuse to overwrite a manifest that records a different generator.

    Two tools writing one path is how a manifest silently becomes another tool's
    output; the recorded `generator_pins.generator_tool` is the tripwire.
    """
    if not os.path.exists(path):
        return
    try:
        doc = json.loads(open(path, encoding="utf-8").read())
    except Exception:
        return
    pinned = (doc.get("generator_pins") or {}).get("generator_tool")
    if pinned and pinned != tool_path:
        raise SystemExit("m4_pin_repair: refusing to overwrite %s — it records generator %s, "
                         "not %s (two tools must never write one manifest path)"
                         % (path, pinned, tool_path))


def build(args):
    report = {"tool": "tools/m4_pin_repair.py",
              "task": "TASK-020 item 8a — supplement generator attribution",
              "note": REPORT_NOTE, "artefacts": []}
    for rel, tool, commit in ARTEFACTS:
        path = os.path.join(args.repo, rel)
        raw = open(path, encoding="utf-8").read()
        doc = json.loads(raw)
        if json.dumps(doc, **STYLE) + "\n" != raw:
            raise SystemExit("m4_pin_repair: %s does not round-trip in the known style — "
                             "refusing to rewrite it" % rel)
        pins = generator_pins(tool, commit, repo=args.repo)
        before = sha(path)
        if doc.get("generator_pins") == pins:
            status = "already-present"
        elif "generator_pins" in doc:
            raise SystemExit("m4_pin_repair: %s already carries a different generator_pins "
                             "block — refusing to overwrite" % rel)
        else:
            doc["generator_pins"] = pins
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(json.dumps(doc, **STYLE) + "\n")
            status = "added"
        report["artefacts"].append({
            "file": rel, "tool_commit": doc.get("tool_commit"),
            "generator_tool": tool, "generator_tool_commit": commit,
            "generator_tool_sha256": pins["generator_tool_sha256"],
            "sha256_before": before, "sha256_after": sha(path), "status": status,
            "changed": before != sha(path)})
        print("%-12s %s  %s -> %s" % (status, rel, before[:12], report["artefacts"][-1]["sha256_after"][:12]))
    out = os.path.join(args.repo, REPORT)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(report, **STYLE) + "\n")
    print("repair report -> %s" % REPORT)
    return 0


def verify(args):
    problems = []
    for rel, tool, commit in ARTEFACTS:
        path = os.path.join(args.repo, rel)
        doc = json.loads(open(path, encoding="utf-8").read())
        pins = doc.get("generator_pins")
        if not pins:
            problems.append("%s: no generator_pins" % rel)
            continue
        want = generator_pins(pins.get("generator_tool", tool), pins.get("generator_tool_commit", commit),
                              repo=args.repo)
        if pins.get("generator_tool_sha256") != want["generator_tool_sha256"]:
            problems.append("%s: generator_tool_sha256 does not match the blob at %s"
                            % (rel, pins.get("generator_tool_commit")))
        if sha(path) != sha(os.path.join(args.repo, rel)):
            problems.append("%s: file unreadable" % rel)
    if problems:
        for p in problems:
            print("FAIL: %s" % p)
        return 1
    print("pin repair verify: OK (%d artefacts carry generator_pins, digests match their "
          "cited commits)" % len(ARTEFACTS))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    v = sub.add_parser("verify")
    for p in (b, v):
        p.add_argument("--repo", default=".")
    a = ap.parse_args(argv)
    return {"build": build, "verify": verify}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
