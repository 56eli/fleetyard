"""Self-test + fixture/clean checks for tools/det_nonsense.py (TASK-004)."""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import det_nonsense as det  # noqa: E402


class SelfTest(unittest.TestCase):
    def test_builtin_self_test(self):
        self.assertTrue(det.self_test())

    def test_signal_shape(self):
        for text, _want in [(t[0], t[-1]) for t in det.SELF_TEST]:
            for s in det.detect(text):
                self.assertEqual(s["detector"], det.DETECTOR_ID)
                self.assertEqual(text[s["start"]:s["end"]], s["quoted"])
                self.assertTrue(s["note"])


class NonsenseDetails(unittest.TestCase):
    def test_percent_forms(self):
        self.assertEqual(len(det.detect("a 150 percent rise")), 1)
        self.assertEqual(det.detect("100% and 99.5 percent and 1,000 people"),
                         [])
        self.assertEqual(len(det.detect("rose 1,200% overnight")), 1)

    def test_long_korean_run_is_not_garble(self):
        run = " ".join(["\uc9c4\uc2e4\uc740"] * det.MIN_FOREIGN_RUN)
        self.assertEqual(det.detect("Truth. " + run + ". Next."), [])
        short = " ".join(["\uc9c4\uc2e4\uc740"] * (det.MIN_FOREIGN_RUN - 1))
        self.assertEqual(len(det.detect("Truth. " + short + ". Next.")), 1)
