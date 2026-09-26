#!/usr/bin/env python3
"""Tests for `tools/m4_t18_dispositions.py` (TASK-018 items 0d–0g).

The committed artefacts are read (never written); the append/refuse behaviour is exercised
on a copy in a temp dir.
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import m4_t18_dispositions as disp  # noqa: E402

ADJ = os.path.join(ROOT, "runs", "m4-q2-adjudication", "adjudication.jsonl")
REC = os.path.join(ROOT, "runs", "m4-q2-adjudication", "RECOUNT-2026-09-26.json")


def rows():
    with open(ADJ, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


class Dispositions(unittest.TestCase):
    def test_committed_file_has_122_signal_rows_and_the_dispositions(self):
        signal = disp.signal_rows(rows())
        ruled = [r for r in rows() if r.get("record") == "disposition"]
        self.assertEqual(len(signal), 122)
        self.assertEqual({r["id"] for r in ruled},
                         set(disp.DEMOTIONS) | set(disp.NOTATION_IDS) | set(disp.HOLDOUT_IDS))

    def test_base_lines_match_the_recorded_digest(self):
        prov = json.load(open(os.path.join(ROOT, "runs", "m4-q2-adjudication",
                                           "PROVENANCE.json"), encoding="utf-8"))
        blob = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n"
                       for r in disp.signal_rows(rows()))
        # PROVENANCE records the tool's own serialisation of the same rows; both digests are
        # published in the recount so the base is provably unedited
        rec = json.load(open(REC, encoding="utf-8"))
        self.assertEqual(rec["base_122_lines_sha256_before_append"],
                         prov["outputs"]["adjudication.jsonl"])
        self.assertEqual(rec["base_lines_reconstructed_digest"],
                         hashlib.sha256(blob.encode("utf-8")).hexdigest())

    def test_dispositions_carry_reasons_and_exact_utc(self):
        for r in [x for x in rows() if x.get("record") == "disposition"]:
            self.assertTrue(r.get("reason"))
            self.assertRegex(r.get("utc", ""), r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
            self.assertIn("utc_source", r)

    def test_recount_arithmetic_and_strata(self):
        rec = json.load(open(REC, encoding="utf-8"))
        counts = rec["facts"]["omitted_word_counts"]
        self.assertEqual(sum(counts.values()), 57)
        self.assertEqual(rec["facts"]["seeded_true_rows"], 0)
        self.assertEqual(rec["facts"]["fixture_span_overlaps"], 0)
        self.assertEqual(rec["counts_after_exclusions"]["rows"], 49)
        self.assertEqual(rec["counts_after_exclusions"]["sites"], 48)
        self.assertEqual(rec["stratification"]["after_exclusions"]["sum"], 49)
        self.assertEqual(rec["standing_statements"]["band"]["floors"]["3"], 71)

    def test_build_refuses_a_second_append(self):
        tmp = tempfile.mkdtemp(prefix="t18disp-")
        self.addCleanup(shutil.rmtree, tmp, True)
        out = os.path.join(tmp, "run")
        shutil.copytree(os.path.join(ROOT, "runs", "m4-q2-adjudication"), out)
        os.remove(os.path.join(out, "adjudication.jsonl"))
        shutil.copy(ADJ, os.path.join(out, "adjudication.jsonl"))
        with self.assertRaises(SystemExit) as ctx:
            disp.main(["build", "--out", out, "--utc", "2026-09-26T01:20:00Z"])
        self.assertIn("already present", str(ctx.exception))

    def test_corrections_prose_carries_the_required_qualifiers(self):
        summary = open(os.path.join(ROOT, "runs", "m4-q2-adjudication", "SUMMARY.md"),
                       encoding="utf-8").read()
        patterns = open(os.path.join(ROOT, "tools", "PATTERNS.md"), encoding="utf-8").read()
        for needle in ("0 of 122", "55 distinct sites", "71/57/33/22", "unknowable"):
            self.assertIn(needle, summary)
            self.assertIn(needle, patterns)


if __name__ == "__main__":
    unittest.main()
