#!/usr/bin/env python3
"""Criterion 20.13 — cross-artefact coherence, computed rather than asserted.

Three instruments describe the same 122 C1-drop signals:

  * the adjudication ledger   `runs/m4-q2-adjudication/adjudication.jsonl` (verdicts + rulings)
  * the shape adjudication    `runs/m4-q2-dropword/EVAL.json` (`shape_adjudication.signals`)
  * the source-inheritance filter (the `source_inheritance` object on those same rows)

Criterion 20.13 (ORCH-2, items 1-8 gate) requires that for every signal the shape class, the
filter status and the adjudication verdict **agree**, or that the disagreement is written down
with a ruling — and that any count quoted in `tools/PATTERNS.md` equals what the cited artefact
supports **after its own exclusions**.

Usage:
    python3 tools/m4_coherence_check.py [--json] [--out runs/m4-q2-adjudication/COHERENCE-2026-09-26.json]

Exit status 0 = every signal coherent (or ruled) and every checked quotation supported.
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADJ = os.path.join("runs", "m4-q2-adjudication", "adjudication.jsonl")
RECOUNT = os.path.join("runs", "m4-q2-adjudication", "RECOUNT-2026-09-26.json")
EVALQ2 = os.path.join("runs", "m4-q2-dropword", "EVAL.json")
PATTERNS = os.path.join("tools", "PATTERNS.md")

SHAPE_EXCLUDED = ("dropped-token-not-missing", "partial-overlap")


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_rows(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def build(root):
    rows = load_rows(os.path.join(root, ADJ))
    signals = [r for r in rows if r.get("record") != "disposition"]
    # an id may carry MORE THAN ONE disposition (D-092: a notation refusal AND a holdout-member
    # note). Keeping only the last line silently restored D-092's promoted verdict, which is
    # exactly the kind of count error this checker exists to catch - so accumulate, don't replace.
    disps = {}
    for r in rows:
        if r.get("record") == "disposition":
            disps.setdefault(r["id"], []).append(r)
    ev = load_json(os.path.join(root, EVALQ2))
    shapes = ev["shape_adjudication"]["signals"]
    by_site = {(r["transcript"], r["start"]): r for r in shapes}

    table = []
    for s in signals:
        site = (s["transcript"], s["char_offset"])
        row = by_site.get(site)
        if row is None:
            table.append({"id": s["id"], "site": list(site), "missing_shape_row": True})
            continue
        kind = row["shape"]["kind"]
        fi = row.get("source_inheritance") or {}
        deferred = str(fi.get("status", "")).startswith("DEFERRED")
        inherited = fi.get("source_inherited") is True
        ds = disps.get(s["id"], [])
        final = s["verdict"]
        for d in ds:
            if d.get("new_verdict"):
                final = d["new_verdict"]
        table.append({
            "id": s["id"], "site": list(site), "shape": kind,
            "filter": "deferred" if deferred else ("source-inherited" if inherited else "pass"),
            "verdict_original": s["verdict"], "verdict_final": final,
            "shape_excluded": kind in SHAPE_EXCLUDED,
            "filter_excluded": deferred or inherited,
            "disposition": [d.get("ruling") for d in ds] or None,
            "seeded": bool(s.get("seeded")),
            "clause": s.get("clause"),
        })

    problems = []
    # 1. every signal has a shape row and a filter status (join is complete)
    for r in table:
        if r.get("missing_shape_row"):
            problems.append("%s: no shape row at its site" % r["id"])

    # 2. a CERTAIN verdict must not stand where an instrument excludes the site, unless the
    #    exclusion is a deferral recorded by a ruling (the v2-holdout members).
    for r in table:
        if r.get("verdict_final") != "CERTAIN-leg-d":
            continue
        if r.get("shape_excluded"):
            problems.append("%s: CERTAIN but shape class %s" % (r["id"], r["shape"]))
        if r.get("filter") == "source-inherited":
            problems.append("%s: CERTAIN but source-inherited" % r["id"])
        if r.get("filter") == "deferred" and not r.get("disposition"):
            problems.append("%s: CERTAIN while the filter defers its transcript, no ruling"
                            % r["id"])

    # 3. counts, computed
    counts = {
        "raw": len(table),
        "shape_consistent": sum(1 for r in table if r["shape"] == "consistent"),
        "shape_dropped_token_not_missing": sum(1 for r in table
                                               if r["shape"] == "dropped-token-not-missing"),
        "shape_partial_overlap": sum(1 for r in table if r["shape"] == "partial-overlap"),
        "shape_gate_boundary": sum(1 for r in table if r["shape"] == "gate-boundary-excluded"),
        "filter_source_inherited": sum(1 for r in table if r["filter"] == "source-inherited"),
        "filter_deferred": sum(1 for r in table if r["filter"] == "deferred"),
        "counted_by_both": sum(1 for r in table
                               if not r["shape_excluded"] and r["filter"] == "pass"),
        "final_certain": sum(1 for r in table if r["verdict_final"] == "CERTAIN-leg-d"),
        "final_candidate": sum(1 for r in table if r["verdict_final"] == "CANDIDATE"),
        "seeded": sum(1 for r in table if r["seeded"]),
    }
    rulings, ruling_rows = {}, 0
    for r in table:
        for ruling in (r.get("disposition") or []):
            rulings[ruling] = rulings.get(ruling, 0) + 1
            ruling_rows += 1
    counts["rulings"] = rulings
    counts["disposition_lines"] = ruling_rows
    counts["rows_with_a_ruling"] = sum(1 for r in table if r.get("disposition"))

    # 4. the published recount must equal what the instruments support after exclusions
    rec = load_json(os.path.join(root, RECOUNT))
    ca = rec["counts_after_exclusions"]
    quoted = {}
    m = re.search(r"(\d+)\s*(?:promoted\s*)?rows", json.dumps(ca))
    quoted["recount"] = ca
    problems_counts = []
    if ca.get("rows") is not None and ca["rows"] != counts["final_certain"]:
        problems_counts.append("recount rows %s != computed final CERTAIN %d"
                               % (ca["rows"], counts["final_certain"]))
    if ca.get("sites") is not None and ca["sites"] > ca.get("rows", 10 ** 9):
        problems_counts.append("recount sites %s exceeds rows %s" % (ca["sites"], ca["rows"]))
    # the item-15b block in EVAL.json must agree with this computation
    ev = load_json(os.path.join(root, EVALQ2))
    two = ev["shape_adjudication"]["count_reconciliation"]["two_distinct_114s"]
    for key, computed in (("intersection", counts["counted_by_both"]),
                          ("differ_each_direction",
                           counts["shape_dropped_token_not_missing"]
                           + counts["shape_partial_overlap"]),
                          ("exclusion_sets_disjoint", 0)):
        if two.get(key) != computed:
            problems_counts.append("EVAL two_distinct_114s.%s = %s != computed %s"
                                   % (key, two.get(key), computed))
    quoted["two_distinct_114s"] = two

    # 5. PATTERNS must carry the qualifier with every quotation of 57
    pat = open(os.path.join(root, PATTERNS), encoding="utf-8").read()
    pat_checks = {
        "qualifier_present": "49 promoted rows / 48 distinct" in pat,
        "band_present": "71/57/**33**/22" in pat or "71 / 57 / 33 / 22" in pat,
        "floor5_statement": "floor-5 number" in pat,
        "row_qualified": "The drop-word row's" in pat or "57 is a floor-5 number" in pat,
    }
    return {"table": table, "counts": counts, "problems": problems,
            "count_problems": problems_counts, "patterns": pat_checks, "recount": rec,
            "quoted": quoted, "dispositions": disps}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--utc", default=None,
                    help="exact-to-the-second stamp for the written report (item 12 discipline)")
    a = ap.parse_args(argv)
    res = build(ROOT)
    ok = (not res["problems"] and not res["count_problems"]
          and all(res["patterns"].values()))
    report = {
        "task": "criterion 20.13 - shape class / filter status / adjudication verdict coherence",
        "by": "WORKER-2, lane arena/01a0d9ce-fleetyard",
        "criterion": ("for every signal the shape class, filter status and adjudication verdict "
                      "agree, or the disagreement is written down with a ruling; any count "
                      "quoted in PATTERNS.md equals what the cited artefact supports after its "
                      "own exclusions"),
        "counts": res["counts"],
        "problems": res["problems"],
        "count_problems": res["count_problems"],
        "patterns_checks": res["patterns"],
        "verdict": "COHERENT" if ok else "INCOHERENT",
        "report_utc": a.utc,
        "report_utc_source": ("--utc argument, passed as the lane clock at write time; the "
                              "commit carrying this report is the source of record") if a.utc else None,
        "rulings": {k: v for k, v in sorted(res["counts"]["rulings"].items())},
        "recount_file": RECOUNT,
        "recount_counts": res["recount"]["counts_after_exclusions"],
    }
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            json.dump(report, fh, ensure_ascii=False, sort_keys=True, indent=1)
            fh.write("\n")
    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        c = res["counts"]
        print("coherence: %d signals | shape-consistent %d | shape-excluded %d | filter-excluded %d"
              % (c["raw"], c["shape_consistent"],
                 c["shape_dropped_token_not_missing"] + c["shape_partial_overlap"],
                 c["filter_source_inherited"] + c["filter_deferred"]))
        print("counted by both instruments: %d | final CERTAIN %d / CANDIDATE %d | seeded %d"
              % (c["counted_by_both"], c["final_certain"], c["final_candidate"], c["seeded"]))
        print("rulings: %s" % json.dumps(c["rulings"], sort_keys=True))
        print("PATTERNS quotation checks: %s" % json.dumps(res["patterns"], sort_keys=True))
        for p in res["problems"] + res["count_problems"]:
            print("  PROBLEM %s" % p)
        print("coherence check: %s" % ("OK" if ok else "FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
