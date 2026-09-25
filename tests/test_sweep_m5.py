"""TASK-011: detector selector + M5 raw census wrapper (tools/sweep_m5.py)."""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import run_detectors as rd  # noqa: E402
import sweep_m5  # noqa: E402

CORPUS = os.path.join(ROOT, "corpus", "docdocgo")
SEDONA2 = ("corpus/docdocgo/overlays/"
           "A_Unique_Sedona_Seminar_Dec_2008_Part_2_enxautogen_html.txt")


class SelectorTest(unittest.TestCase):
    def test_m5_selection_is_four_detectors_without_a4(self):
        ids = [d.DETECTOR_ID for d in rd.select_ids(rd.M5_SELECTION)]
        self.assertEqual(ids, ["A1-repetition", "A2-nonsense",
                               "B1-contradiction", "B2-misquote"])
        self.assertNotIn("A4-confusion", ids)

    def test_order_and_case_insensitive(self):
        ids = [d.DETECTOR_ID for d in rd.select_ids(" b2, a1 ")]
        self.assertEqual(ids, ["A1-repetition", "B2-misquote"])

    def test_unknown_id_rejected(self):
        with self.assertRaises(ValueError):
            rd.select_ids("A1,A3")
        with self.assertRaises(ValueError):
            rd.select_ids(" , ")

    def test_cli_rejects_bad_selection(self):
        with self.assertRaises(SystemExit), \
                redirect_stdout(io.StringIO()), \
                open(os.devnull, "w") as null:
            old, sys.stderr = sys.stderr, null
            try:
                rd.main(["--detectors", "A9", "x.txt"])
            finally:
                sys.stderr = old


class SummaryTest(unittest.TestCase):
    def test_year_of(self):
        self.assertEqual(sweep_m5.year_of("x/Love_Sep_2011_Part_1_enx.txt"),
                         "2011")
        self.assertEqual(sweep_m5.year_of("x/Satsang_Series_Volume_IX.txt"),
                         "unknown")

    def test_summary_counts_and_coverage_truth(self):
        paths = ["o/A_2004_x.txt", "o/B_2004_y.txt", "o/C_z.txt"]
        rec = lambda d, c: {"detector_id": d, "raw_runner_confidence": c}
        per = {"A_2004_x": [rec("A1-repetition", "CANDIDATE"),
                            rec("A1-repetition+A2-nonsense", "HIGH CONFIDENCE")],
               "C_z": []}
        ix = sweep_m5.summarise(paths, per, [], {"m": 1})
        self.assertEqual((ix["processed"], ix["pending_detector_run"],
                          ix["finding_pass_audited"], ix["pending_review"]),
                         (2, 1, 0, 2))
        self.assertEqual(ix["next_pending"], "B_2004_y")
        self.assertEqual(ix["records_total"], 2)
        self.assertEqual(ix["records_per_detector_signal"],
                         {"A1-repetition": 2, "A2-nonsense": 1})
        self.assertEqual(ix["zero_hit_transcripts"], ["C_z"])
        self.assertEqual(ix["by_year"]["2004"],
                         {"transcripts": 2, "processed": 1, "records": 2})
        self.assertEqual(ix["by_year"]["unknown"]["processed"], 1)
        md = sweep_m5.render_md(dict(ix, generated_utc="t",
                                     corpus_zip_sha256="z", overlays_sha256="o",
                                     tool_commit="c", detectors=[], command="x",
                                     excluded=sweep_m5.EXCLUDED))
        self.assertIn("PROVISIONAL, UNREVIEWED", md)
        self.assertIn("NOT zero", md)
        self.assertIn("| 3 | 2 | 1 | 0 | 2 | 0 |", md)


@unittest.skipUnless(os.path.isdir(CORPUS), "corpus/ not extracted locally")
class SmokeCorpusTest(unittest.TestCase):
    """Book-referenced B result + repetition sample on Sedona Dec 2008 P2,
    re-read against the frozen transcript/book bytes."""

    @classmethod
    def setUpClass(cls):
        import loaders
        cls.loaders = loaders
        cls.books = loaders.read_book_store()
        dets = rd.select_ids(rd.M5_SELECTION)
        cls.t = loaders.read_transcript(os.path.join(ROOT, SEDONA2))
        cls.recs = sweep_m5.raw_records(cls.t, dets,
                                        rd.book_context(cls.books, dets))

    def test_every_record_is_unreviewed_and_offsets_exact(self):
        self.assertTrue(self.recs)
        for r in self.recs:
            self.assertEqual(r["review_status"], "unreviewed")
            self.assertEqual(r["reporting_class"], sweep_m5.REPORTING_CLASS)
            self.assertNotIn("confidence", r)
            self.assertNotIn("A4", r["detector_id"])
            o = r["location"]["char_offset"]
            self.assertEqual(self.t.text[o:o + len(r["quoted_text"])],
                             r["quoted_text"])
            self.assertEqual(self.t.locate(o)[0], r["location"]["paragraph"])

    def test_book_referenced_b2_result(self):
        # CF-015 (hand-read, @5833): B2 must fire with an exact book quote
        a, b = 5833, 5833 + len("Spiritual purity has no influence. "
                                "Interest in the personal lives of students.")
        b2 = [r for r in self.recs if "B2-misquote" in r["detector_id"]
              and r["location"]["char_offset"] < b
              and a < r["location"]["char_offset"] + len(r["quoted_text"])]
        self.assertTrue(b2)
        ref = b2[0]["book_reference"]
        text = self.books[ref["slug"]]
        self.assertNotIn(ref["slug"], self.loaders.NON_HAWKINS_SLUGS)
        o = ref["char_offset"]
        self.assertEqual(text[o:o + len(ref["quote"])], ref["quote"])
        self.assertIn("interest in the personal lives", ref["quote"])

    def test_repetition_sample_candidate_only(self):
        hit = [r for r in self.recs if r["location"]["char_offset"] == 9671]
        self.assertEqual([(r["detector_id"], r["raw_runner_confidence"])
                          for r in hit], [("A1-repetition", "CANDIDATE")])

    def test_sweep_writes_resumable_outputs(self):
        with tempfile.TemporaryDirectory() as d, \
                open(os.devnull, "w") as null:
            old, sys.stderr = sys.stderr, null
            try:
                sweep_m5.main(["--out", d, "--limit", "1"])
                sweep_m5.main(["--out", d, "--limit", "0"])   # resume only
            finally:
                sys.stderr = old
            with open(os.path.join(d, "index.json"), encoding="utf-8") as fh:
                ix = json.load(fh)
            self.assertEqual(ix["processed"], 1)
            self.assertEqual(ix["transcripts_total"], 230)
            self.assertEqual(ix["finding_pass_audited"], 0)
            self.assertNotIn("A4-confusion", ix["detectors"])
            self.assertTrue(ix["corpus_zip_sha256"].startswith("3f36c5203910"))
            self.assertEqual(len(os.listdir(os.path.join(d, "records"))), 1)


if __name__ == "__main__":
    unittest.main()
