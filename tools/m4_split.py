#!/usr/bin/env python3
"""M4 — fixed held-out split, generated BEFORE any tuning (PLAN-v2 / LAW §9).

LAW §9: "Precision/recall claims require held-out data fixed before tuning."
This tool fixes that data now, deterministically, so every later detector change
is measured against a split that predates it.

Method (fixed, published):
  bucket(name) = int(sha256(SALT + basename), 16) % 5
  bucket 0 -> HOLDOUT; else TUNING.
  Transcripts that carry v1 hand-confirmed fixtures are FORCED into TUNING
  (they are in-sample by construction and may never be holdout).

Disclosure (honesty): the v1 detectors were written with corpus-wide knowledge,
so a first holdout measurement is an estimate under this split, not a pristine
out-of-sample one. What the split guarantees is that *future* tuning cannot
silently consume the same transcripts it is later measured on.

Usage:
  python3 tools/m4_split.py build  --corpus corpus --fixtures evidence/fixtures/confirmed \
      --out tools/HELD-OUT-SPLIT.json
  python3 tools/m4_split.py verify --split tools/HELD-OUT-SPLIT.json --corpus corpus
"""
import argparse
import hashlib
import json
import os
import re
import sys

SALT = "fleetyard-m4-holdout-2026-09-25"
MOD = 5
HOLDOUT_BUCKET = 0


def sha256_text(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def corpus_files(corpus_dir):
    d = os.path.join(corpus_dir, "docdocgo", "overlays")
    return sorted(n for n in os.listdir(d) if n.endswith(".txt"))


def fixture_transcripts(fixtures_dir):
    p = os.path.join(fixtures_dir, "confirmed.json")
    out = set()
    if os.path.exists(p):
        for fx in json.load(open(p, encoding="utf-8")):
            out.add(os.path.basename(fx["transcript"]))
    return sorted(out)


def bucket(name):
    return int(hashlib.sha256((SALT + name).encode("utf-8")).hexdigest(), 16) % MOD


def build(corpus_dir, fixtures_dir):
    files = corpus_files(corpus_dir)
    forced = set(fixture_transcripts(fixtures_dir))
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
        "purpose": "held-out split fixed before tuning (LAW §9)",
        "method": "sha256(SALT+basename) mod 5 == 0 -> HOLDOUT; fixture transcripts forced to TUNING",
        "salt": SALT, "mod": MOD, "holdout_bucket": HOLDOUT_BUCKET,
        "corpus_files_sha256": sha256_text("\n".join(files) + "\n"),
        "corpus_files": len(files),
        "fixture_transcripts_forced_tuning": sorted(forced),
        "tuning": tuning, "holdout": holdout,
        "counts": {"tuning": len(tuning), "holdout": len(holdout), "total": len(files)},
        "by_year": years,
        "disclosure": ("v1 detectors were shaped with corpus-wide knowledge; a first "
                       "holdout measurement under this split is an estimate, not a "
                       "pristine out-of-sample figure. The split binds FUTURE tuning: "
                       "no tuning run may read the holdout set; promotion runs must "
                       "read the holdout only."),
    }


def verify(split_path, corpus_dir):
    """Return (ok, problems); recompute the split and compare with the file."""
    saved = json.load(open(split_path, encoding="utf-8"))
    force = set(saved.get("fixture_transcripts_forced_tuning", []))
    files = corpus_files(corpus_dir)
    problems = []
    if saved["corpus_files_sha256"] != sha256_text("\n".join(files) + "\n"):
        problems.append("corpus file list changed since the split was fixed")
    tun, hol = set(saved["tuning"]), set(saved["holdout"])
    if tun & hol:
        problems.append("tuning/holdout overlap: %s" % sorted(tun & hol)[:3])
    if tun | hol != set(files):
        problems.append("split does not cover the corpus exactly")
    for n in files:
        want_hold = (n not in force) and bucket(n) == HOLDOUT_BUCKET
        if want_hold != (n in hol):
            problems.append("bucket mismatch for %s" % n)
    if hol & force:
        problems.append("a fixture transcript landed in holdout")
    return (not problems), problems


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--corpus", default="corpus")
    b.add_argument("--fixtures", required=True)
    b.add_argument("--out", required=True)
    v = sub.add_parser("verify")
    v.add_argument("--split", required=True)
    v.add_argument("--corpus", default="corpus")
    a = ap.parse_args(argv)
    if a.cmd == "build":
        data = build(a.corpus, a.fixtures)
        with open(a.out, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=1, sort_keys=True)
            fh.write("\n")
        print("split written: %s (tuning=%d holdout=%d)"
              % (a.out, data["counts"]["tuning"], data["counts"]["holdout"]))
        return 0
    ok, problems = verify(a.split, a.corpus)
    for p in problems:
        print("SPLIT-PROBLEM %s" % p)
    print("split verify: %s" % ("OK" if ok else "FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
