#!/usr/bin/env python3
"""M4 — sealed holdout split **v2** (TASK-019 quantum a), owner-authorized.

Why v2 exists: the q1 split's 37-transcript holdout was evaluated once (M4-q4) and is
SPENT. LAW §9 requires held-out data fixed before tuning, so a fresh split is sealed here
with a new salt, published method, and the in-sample exclusions forced to TUNING — the
seal is committed **before** any further tuning of any detector.

Method (published; the verifier re-derives the sets from it):

    bucket(basename) = int(sha256(SALT_V2 + basename), 16) mod 5
    bucket == 0  -> HOLDOUT ; otherwise TUNING
    transcripts carrying any hand-confirmed or provisional fixture -> FORCED to TUNING
    transcripts read in the SPENT v1 holdout (M4-q4, counts only)  -> FORCED to TUNING

Corpus file-list digest, derivation written down (v2.2):

    files = sorted(basename for basename in corpus/docdocgo/overlays/*.txt)
    corpus_files_sha256 = sha256_text("\\n".join(files) + "\\n")
        where sha256_text(t) = sha256(t.encode("utf-8")).hexdigest()

That is a digest of the **file list** (names, sorted, newline-joined, trailing newline), not
of file contents; content identity is pinned separately by the frozen corpus zip sha256
recorded in the manifest block. The v1 split used the identical construction, so the two
are directly comparable.

Re-seal rule (binding): if any fixture is confirmed after this seal, the split is VOID and
must be re-sealed with a new salt + a dated record. Never silently reused, never patched.

Usage:
  python3 tools/m4_split_v2.py build  --corpus corpus --out tools/HELD-OUT-SPLIT-V2.json \
      [--tool-commit SHA --main-head SHA --policy-sha SHA --book-store-sha SHA]
  python3 tools/m4_split_v2.py verify --split tools/HELD-OUT-SPLIT-V2.json --corpus corpus
"""
import argparse
import hashlib
import json
import os
import re
import sys

SALT_V2 = "fleetyard-m4-holdout-v2-2026-09-25"
MOD = 5
HOLDOUT_BUCKET = 0
V1_SPLIT = "tools/HELD-OUT-SPLIT.json"   # the spent v1 split (its holdout was read once)
FIXTURE_FILES = [
    ("fixtures/confirmed/confirmed.json", "v1 hand-confirmed fixtures (TASK-002/006)"),
    ("fixtures/v2/dropword.json", "TASK-018 leg-(d) adjudicated drop-word fixtures "
                                 "(in-sample by construction; D2-001..D2-004)"),
]


def sha256_text(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def corpus_files(corpus_dir):
    d = os.path.join(corpus_dir, "docdocgo", "overlays")
    return sorted(n for n in os.listdir(d) if n.endswith(".txt"))


def forced_map():
    """basename -> list of reasons (fixture sources that force it to TUNING)."""
    out = {}
    for path, reason in FIXTURE_FILES:
        if not os.path.exists(path):
            continue
        for fx in json.load(open(path, encoding="utf-8"))["fixtures"] \
                if path.endswith("dropword.json") else json.load(open(path, encoding="utf-8")):
            name = os.path.basename(fx["transcript"])
            out.setdefault(name, []).append(reason)
    return out


def v1_holdout():
    """Transcripts read in the spent v1 holdout (M4-q4). Disclosed exclusion: the v2 holdout
    must be entirely unseen, so these are forced to TUNING even when their v2 bucket says
    holdout."""
    if not os.path.exists(V1_SPLIT):
        return set()
    return set(json.load(open(V1_SPLIT, encoding="utf-8"))["holdout"])


def bucket(name):
    return int(hashlib.sha256((SALT_V2 + name).encode("utf-8")).hexdigest(), 16) % MOD


def build(corpus_dir, tool_commit=None, main_head=None, policy_sha=None, book_store_sha=None):
    files = corpus_files(corpus_dir)
    forced = forced_map()
    for n in v1_holdout():
        forced.setdefault(n, []).append("read in the spent v1 holdout (M4-q4) — v2 holdout "
                                        "must be entirely unseen")
    tuning, holdout = [], []
    for n in files:
        if n in forced or bucket(n) != HOLDOUT_BUCKET:
            tuning.append(n)
        else:
            holdout.append(n)
    years = {}
    for n in files:
        m = re.search(r"_(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)_(\d{4})_", n)
        y = m.group(2) if m else "unknown"
        row = years.setdefault(y, {"tuning": 0, "holdout": 0})
        row["holdout" if n in holdout else "tuning"] += 1
    return {
        "milestone": "M4",
        "task": "TASK-019 quantum a (fresh sealed split v2) — ORCH-2 queue @ owner "
                "ERRATA-2026-09-25g §5",
        "purpose": "held-out data fixed before tuning (LAW §9); replaces the spent v1 split",
        "version": 2,
        "method": "sha256(SALT+basename) mod 5 == 0 -> HOLDOUT; fixture transcripts forced "
                  "to TUNING",
        "salt": SALT_V2, "mod": MOD, "holdout_bucket": HOLDOUT_BUCKET,
        "corpus_files_sha256": sha256_text("\n".join(files) + "\n"),
        "corpus_files": len(files),
        "derivations": {
            "corpus_files_sha256": 'sha256_text("\\n".join(sorted basenames*) + "\\n") where '
                                   'sha256_text(t)=sha256(t.encode("utf-8")).hexdigest(); '
                                   'basenames* = every *.txt directly under '
                                   'corpus/docdocgo/overlays (list digest, not content '
                                   'digest — content is pinned by the corpus zip sha256)',
            "holdout_set": "basenames whose sha256(SALT+basename) mod 5 == 0",
            "tuning_set": "the complement within the corpus file list, plus every forced "
                          "transcript",
            "forced_transcripts": "union of os.path.basename(fx['transcript']) over "
                                  "fixtures/confirmed/confirmed.json and "
                                  "fixtures/v2/dropword.json, PLUS every transcript listed "
                                  "in tools/HELD-OUT-SPLIT.json['holdout'] (the spent v1 "
                                  "holdout, read once at M4-q4 as counts only) — a "
                                  "disclosed contamination-avoidance rule so the v2 holdout "
                                  "is entirely unseen",
        },
        "fixture_sources": {
            "fixtures/confirmed/confirmed.json": sha256_file("fixtures/confirmed/confirmed.json")
            if os.path.exists("fixtures/confirmed/confirmed.json") else "MISSING",
            "fixtures/v2/dropword.json": sha256_file("fixtures/v2/dropword.json")
            if os.path.exists("fixtures/v2/dropword.json") else "MISSING",
        },
        "fixture_transcripts_forced_tuning": sorted(forced),
        "forced_with_reasons": {k: v for k, v in sorted(forced.items())},
        "forced_not_by_fixture": sorted(n for n in files
                                        if n in forced and not forced[n]),
        "v1_holdout_forced_tuning": sorted(v1_holdout()),
        "tuning": tuning, "holdout": holdout,
        "counts": {"tuning": len(tuning), "holdout": len(holdout), "total": len(files)},
        "by_year": years,
        "re_seal_rule": "if any fixture is confirmed after this seal, the split is VOID and "
                        "must be re-sealed with a new salt + a dated record; never silently "
                        "reused, never patched",
        "disclosure": (
            "v1 detectors were shaped with corpus-wide knowledge, and the drop-word and "
            "format rules were shaped on the v1 tuning set; a first figure under v2 is an "
            "estimate under this split, not a pristine out-of-sample number. What the split "
            "guarantees is that FUTURE tuning cannot silently consume the transcripts it is "
            "later measured on: no tuning run may read the v2 holdout, and the one-shot "
            "evaluation (TASK-019 quantum b) reads the holdout only, once, with thresholds "
            "frozen in advance."),
        "manifest": {
            "run_utc": _utc(),
            "sealed_by": "WORKER-2 (A-2026-09-25-001), lane arena/01a0d9ce-fleetyard",
            "tool": "tools/m4_split_v2.py",
            "tool_sha256": sha256_file(os.path.abspath(__file__)),
            "tool_commit": tool_commit or "UNPINNED",
            "main_head": main_head or "UNPINNED",
            "policy_sha256": policy_sha or "UNPINNED",
            "corpus_zip_sha256": _zip_sha(),
            "book_store_sha256": book_store_sha or "UNPINNED",
            "output_digest_note": "the digest of this seal file is recorded in the TASK-019a "
                                  "delivery record and in the commit that seals it (a file "
                                  "cannot contain its own hash)",
        },
    }


def _zip_sha():
    for p in ("docdocgo-fixes.zip",):
        if os.path.exists(p):
            return sha256_file(p)
    return "MISSING"


def _utc():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def verify(split_path, corpus_dir):
    saved = json.load(open(split_path, encoding="utf-8"))
    problems = []
    files = corpus_files(corpus_dir)
    if saved.get("salt") == "fleetyard-m4-holdout-2026-09-25":
        problems.append("salt is not fresh (v1 salt reused)")
    if saved["corpus_files_sha256"] != sha256_text("\n".join(files) + "\n"):
        problems.append("corpus file list changed since the split was fixed")
    tun, hol = set(saved["tuning"]), set(saved["holdout"])
    if tun & hol:
        problems.append("tuning/holdout overlap: %s" % sorted(tun & hol)[:3])
    if tun | hol != set(files):
        problems.append("split does not cover the corpus exactly")
    expect_forced = set(forced_map()) | set(v1_holdout())
    force = set(saved.get("fixture_transcripts_forced_tuning", []))
    if force != expect_forced:
        problems.append("forced set does not match the fixture files + spent v1 holdout on "
                        "disk (missing %s)" % sorted(expect_forced - force)[:3])
    for n in files:
        want_hold = (n not in force) and bucket(n) == HOLDOUT_BUCKET
        if want_hold != (n in hol):
            problems.append("bucket mismatch for %s" % n)
    if hol & force:
        problems.append("a fixture transcript landed in holdout: %s" % sorted(hol & force)[:3])
    if set(saved.get("fixture_transcripts_forced_tuning", [])) - set(saved["tuning"]):
        problems.append("a forced transcript is not in the tuning set")
    return (not problems), problems


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--corpus", default="corpus")
    b.add_argument("--out", required=True)
    b.add_argument("--tool-commit")
    b.add_argument("--main-head")
    b.add_argument("--policy-sha")
    b.add_argument("--book-store-sha")
    v = sub.add_parser("verify")
    v.add_argument("--split", required=True)
    v.add_argument("--corpus", default="corpus")
    a = ap.parse_args(argv)
    if a.cmd == "build":
        data = build(a.corpus, a.tool_commit, a.main_head, a.policy_sha, a.book_store_sha)
        with open(a.out, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=1, sort_keys=True)
            fh.write("\n")
        print("split v2 sealed: %s (tuning=%d holdout=%d; forced=%d)"
              % (a.out, data["counts"]["tuning"], data["counts"]["holdout"],
                 len(data["fixture_transcripts_forced_tuning"])))
        print("seal sha256: %s" % sha256_file(a.out))
        return 0
    ok, problems = verify(a.split, a.corpus)
    print("split v2 verify: %s" % ("OK" if ok else "PROBLEMS"))
    for p in problems:
        print("  - %s" % p)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
