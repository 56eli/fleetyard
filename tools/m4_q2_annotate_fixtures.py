#!/usr/bin/env python3
"""TASK-018 item 2 — append the leg-(d) adjudication outcome to the provisional fixtures.

Append-only by construction: the existing fixture fields (claims, spans, offsets,
`confidence`, `status`) are never rewritten. Each fixture gains one new object,
`adjudication_2026_09_25`, naming the verdict, the reason, and the artifact that carries
the cited bytes. Deterministic: re-running with the same adjudication file produces the
same bytes (the field is replaced by an identical value).

Usage: python3 tools/m4_q2_annotate_fixtures.py \
           --fixtures fixtures/v2/dropword.json \
           --adjudication runs/m4-q2-adjudication/fixtures-adjudication.json
"""
import argparse
import collections
import json
import os
import sys


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", default="fixtures/v2/dropword.json")
    ap.add_argument("--adjudication", default="runs/m4-q2-adjudication/"
                                              "fixtures-adjudication.json")
    a = ap.parse_args(argv)
    fx = json.load(open(a.fixtures, encoding="utf-8"))
    adj = json.load(open(a.adjudication, encoding="utf-8"))
    by_id = {r["fixture"]: r for r in adj}
    counts = collections.Counter()
    for f in fx["fixtures"]:
        r = by_id.get(f["id"])
        if not r:
            continue
        counts[r["verdict"]] += 1
        f["adjudication_2026_09_25"] = {
            "verdict": r["verdict"],
            "adjudication": r["adjudication"],
            "clause": r.get("clause"),
            "omitted_word": r.get("omitted_word"),
            "reason_code": r.get("reason_code"),
            "reason": r["reason"],
            "cited_bytes": "runs/m4-q2-adjudication/fixtures-adjudication.json "
                           "(transcript span + book slug/offset/quote, re-derived)",
            "in_sample": True,
            "note": "leg (d) per owner ERRATA-2026-09-25e §2; the narrow leg reaches "
                    "single-word omissions only — a two-word omission is NOT promoted "
                    "(L3), whatever its hand-read status",
        }
    fx["adjudication_summary_2026_09_25"] = {
        "confirmed_leg_d": counts.get("CERTAIN-leg-d", 0),
        "discarded_from_certain_claim": counts.get("CANDIDATE", 0),
        "artifact": "runs/m4-q2-adjudication/fixtures-adjudication.json",
        "task": "TASK-018 (ORCH-2 queue @ 45959ca)",
        "in_sample": "these four fixtures are detector-derived and hand-picked: in-sample, "
                     "never precision evidence (LAW §9 / L5)",
    }
    with open(a.fixtures, "w", encoding="utf-8") as fh:
        json.dump(fx, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    print("annotated %d fixtures: %s" % (len(fx["fixtures"]), dict(counts)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
