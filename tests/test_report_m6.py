"""TASK-012: provisional M6 report renderer (tools/report_m6.py)."""
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import report_m6  # noqa: E402

CORPUS = os.path.join(ROOT, "corpus", "docdocgo")
INDEX = os.path.join(ROOT, "runs", "m5-raw", "index.json")


class PatternTest(unittest.TestCase):
    def test_patterns_cover_all_confirmed_fixtures(self):
        conf = {c["id"] for c in report_m6.load(report_m6.CONFIRMED)}
        seeded = {i for _n, ids, _t in report_m6.PATTERNS for i in ids}
        self.assertEqual(conf - seeded, set())
        self.assertEqual(seeded - conf, {"NEG-001"})

    def test_reviewed_high_is_the_five_withdrawn(self):
        high = report_m6.reviewed_high(report_m6.load(report_m6.CORRECTIONS))
        self.assertEqual([h[0] for h in high],
                         ["CF-005", "CF-013", "CF-014", "CF-016", "CF-018"])


@unittest.skipUnless(os.path.isdir(CORPUS) and os.path.isfile(INDEX),
                     "corpus/ or runs/m5-raw missing")
class RenderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import loaders
        cls.ix = report_m6.load(INDEX)
        cls.words = report_m6.word_counts(loaders.list_transcripts())
        cls.text = report_m6.build(report_m6.load(report_m6.CONFIRMED),
                                   report_m6.load(report_m6.CORRECTIONS),
                                   cls.ix, cls.words, "HEAD")

    def test_honesty_markers(self):
        t = self.text
        for s in ["PROVISIONAL", "No corpus-wide error rate",
                  "Finding-pass audited: 0/230", "pending review: 230/230",
                  "unmeasured", "in-sample, invalid as an independent FP",
                  "Unmeasured is not zero", "not estimable yet",
                  "NOT proven hotspots", "UNDECIDED"]:
            self.assertIn(s, t)

    def test_numbers_match_index(self):
        t = self.text
        self.assertIn("**%d unreviewed raw signals**" %
                      self.ix["records_total"], t)
        for d, n in self.ix["records_per_detector_signal"].items():
            self.assertIn("| %s |" % d, t)
            self.assertIn("| %d |" % n, t)
        self.assertEqual(len(self.words), 230)

    def test_raw_section_is_separate_from_reviewed(self):
        t = self.text
        reviewed = t[t.index("## 3."):t.index("## 5.")]
        self.assertNotIn(str(self.ix["records_total"]), reviewed)

    def test_committed_report_is_current(self):
        path = os.path.join(ROOT, report_m6.DEFAULT_OUT)
        if not os.path.isfile(path):
            self.skipTest("report not committed yet")
        with open(path, encoding="utf-8") as fh:
            committed = fh.read()
        # identical apart from the rendering-commit line
        strip = lambda s: [ln for ln in s.splitlines()
                           if not ln.startswith("- Rendered by")]
        self.assertEqual(strip(committed), strip(self.text))


if __name__ == "__main__":
    unittest.main()
