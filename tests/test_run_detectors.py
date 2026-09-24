"""Tests for tools/run_detectors.py (TASK-004)."""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import fixtures  # noqa: E402
import loaders  # noqa: E402
import run_detectors as rd  # noqa: E402

CORPUS = os.path.join(ROOT, "corpus", "docdocgo")
STANDARDS_FIELDS = {"transcript_path", "location", "quoted_text",
                    "suspected_intended_text", "evidence_class",
                    "detector_id", "book_reference", "confidence", "status",
                    "status_by"}


class MergeAndRecordTest(unittest.TestCase):
    def test_merge_overlaps(self):
        sigs = [{"start": 0, "end": 5}, {"start": 3, "end": 9},
                {"start": 9, "end": 12}]
        self.assertEqual([(g["start"], g["end"]) for g in rd.merge(sigs)],
                         [(0, 9), (9, 12)])

    def test_records_taxonomy(self):
        t = loaders.Transcript("x.txt", "Hi. " + "No. " * 9 +
                               "Then 255% of people. " +
                               "Given to Caesar that which is Caesar's.")
        recs = rd.records(t)
        self.assertEqual(len(recs), 3)
        for r in recs:
            self.assertEqual(set(r), STANDARDS_FIELDS)
            self.assertEqual(r["status"], "open")
            self.assertIn(r["confidence"], ("CANDIDATE", "HIGH CONFIDENCE"))
            off = r["location"]["char_offset"]
            self.assertEqual(t.text[off:off + len(r["quoted_text"])],
                             r["quoted_text"])
        self.assertEqual(recs[2]["suspected_intended_text"],
                         "Give unto Caesar")

    def test_converging_signals_are_high(self):
        # a repetition loop made of an impossible percentage: two detectors
        t = loaders.Transcript("x.txt", "It was 300% " * 5)
        recs = rd.records(t)
        self.assertTrue(any(r["confidence"] == "HIGH CONFIDENCE"
                            for r in recs))
        self.assertFalse(any(r["confidence"] == "CERTAIN" for r in recs))


@unittest.skipUnless(os.path.isdir(CORPUS), "corpus/ not extracted locally")
class EvalTest(unittest.TestCase):
    """TASK-004 criteria 3 + 4 measured on the real fixture sets."""

    @classmethod
    def setUpClass(cls):
        cwd = os.getcwd()
        os.chdir(ROOT)
        try:
            books = loaders.read_book_store()
            cls.conf = fixtures.load_json(fixtures.CONFIRMED_PATH)
            clean = fixtures.load_json(fixtures.CLEAN_PATH)
            cls.res = rd.evaluate(books, cls.conf, clean)
        finally:
            os.chdir(cwd)

    def test_zero_clean_false_positives(self):
        for det, r in self.res.items():
            self.assertEqual(r["clean_fp"], [], det)

    def test_each_detector_hits_a_fixture(self):
        for det, r in self.res.items():
            self.assertGreaterEqual(len(r["hits"]) + len(r["seeded_hits"]),
                                    1, det)

    def test_measured_hits(self):
        self.assertEqual(sorted(self.res["A1-repetition"]["hits"]),
                         ["CF-005", "CF-006"])
        self.assertEqual(self.res["A2-nonsense"]["hits"], ["CF-003"])
        self.assertEqual(len(self.res["A4-confusion"]["seeded_hits"]), 8)
