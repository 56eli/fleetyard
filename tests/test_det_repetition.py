"""Self-test + fixture/clean checks for tools/det_repetition.py (TASK-004)."""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import det_repetition as det  # noqa: E402


class SelfTest(unittest.TestCase):
    def test_builtin_self_test(self):
        self.assertTrue(det.self_test())

    def test_signal_shape(self):
        for text, _want in [(t[0], t[-1]) for t in det.SELF_TEST]:
            for s in det.detect(text):
                self.assertEqual(s["detector"], det.DETECTOR_ID)
                self.assertEqual(text[s["start"]:s["end"]], s["quoted"])
                self.assertTrue(s["note"])


class RepetitionDetails(unittest.TestCase):
    def test_suspected_is_single_occurrence(self):
        s = det.detect("It is discovered that to be loved. " * 5)[0]
        self.assertEqual(s["suspected"], "It is discovered that to be loved.")
        self.assertIn("7-token unit repeated 5 times", s["note"])

    def test_thresholds(self):
        self.assertEqual(det.detect("No. " * 7), [])
        self.assertEqual(len(det.detect("No. " * 8)), 1)
        self.assertEqual(det.detect("very good " * 4), [])
        self.assertEqual(len(det.detect("very good " * 5)), 1)
