"""tests for tools/m4_coherence_check.py — criterion 20.13 made mechanical (TASK-020 item 8b)."""
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import m4_coherence_check as coh  # noqa: E402

ADJ = os.path.join(ROOT, "runs", "m4-q2-adjudication", "adjudication.jsonl")


def have_inputs():
    return os.path.exists(ADJ) and os.path.exists(os.path.join(ROOT, "runs", "m4-q2-dropword",
                                                               "EVAL.json"))


@unittest.skipUnless(have_inputs(), "adjudication artefacts absent")
class CoherenceCase(unittest.TestCase):
    def setUp(self):
        self.res = coh.build(ROOT)

    def test_the_join_is_complete_over_all_122_signals(self):
        self.assertEqual(self.res["counts"]["raw"], 122)
        self.assertEqual([r for r in self.res["table"] if r.get("missing_shape_row")], [])

    def test_no_promotion_survives_an_instrument_exclusion(self):
        self.assertEqual(self.res["problems"], [])
        self.assertEqual(self.res["counts"]["final_certain"], 49)
        self.assertEqual(self.res["counts"]["final_candidate"] + 49, 122)

    def test_counts_reconcile_with_the_recount_and_the_two_114s_block(self):
        self.assertEqual(self.res["count_problems"], [])
        self.assertEqual(self.res["counts"]["counted_by_both"], 106)
        self.assertEqual(self.res["counts"]["filter_source_inherited"]
                         + self.res["counts"]["filter_deferred"], 8)
        self.assertEqual(self.res["counts"]["shape_dropped_token_not_missing"]
                         + self.res["counts"]["shape_partial_overlap"], 8)

    def test_a_second_disposition_on_one_id_is_accumulated_not_replaced(self):
        """D-092 carries a notation refusal AND a holdout note; keeping only the last line
        silently restored its promotion (49 -> 50) during development. Pin that behaviour."""
        d = self.res["dispositions"]["D-092"]
        self.assertEqual(len(d), 2)
        self.assertIn("refused-notation", [x["ruling"] for x in d])
        self.assertIn("holdout-member-note", [x["ruling"] for x in d])
        row = [r for r in self.res["table"] if r["id"] == "D-092"][0]
        self.assertEqual(row["verdict_final"], "CANDIDATE")

    def test_patterns_quotes_the_number_with_its_qualifier(self):
        self.assertTrue(all(self.res["patterns"].values()), self.res["patterns"])

    def test_main_reports_failure_when_a_ruling_is_deleted(self):
        tmp = tempfile.mkdtemp(prefix="coh-")
        try:
            shutil.copytree(os.path.join(ROOT, "runs", "m4-q2-adjudication"),
                            os.path.join(tmp, "runs", "m4-q2-adjudication"))
            shutil.copytree(os.path.join(ROOT, "runs", "m4-q2-dropword"),
                            os.path.join(tmp, "runs", "m4-q2-dropword"))
            os.makedirs(os.path.join(tmp, "tools"))
            shutil.copy(os.path.join(ROOT, "tools", "PATTERNS.md"),
                        os.path.join(tmp, "tools", "PATTERNS.md"))
            path = os.path.join(tmp, "runs", "m4-q2-adjudication", "adjudication.jsonl")
            with open(path, encoding="utf-8") as fh:
                lines = fh.readlines()
            # drop the DISPOSITION line only - the signal row stays, so its original promotion
            # comes back and the checker must flag it (do not remove both: that is a different
            # defect, a shorter base)
            keep = [ln for ln in lines
                    if not ('"D-039"' in ln and '"disposition"' in ln)]
            self.assertEqual(len(keep), len(lines) - 1)
            with open(path, "w", encoding="utf-8") as fh:
                fh.writelines(keep)
            res = coh.build(tmp)                     # build() takes the root, so no monkeypatching
            self.assertEqual(res["counts"]["raw"], 122)
            self.assertTrue(any("D-039" in p for p in res["problems"]), res["problems"])
            self.assertEqual(res["counts"]["final_certain"], 50)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
