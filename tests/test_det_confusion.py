"""Self-test + fixture/clean checks for tools/det_confusion.py (TASK-004)."""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import det_confusion as det  # noqa: E402


class SelfTest(unittest.TestCase):
    def test_builtin_self_test(self):
        self.assertTrue(det.self_test())

    def test_signal_shape(self):
        for text, _want in [(t[0], t[-1]) for t in det.SELF_TEST]:
            for s in det.detect(text):
                self.assertEqual(s["detector"], det.DETECTOR_ID)
                self.assertEqual(text[s["start"]:s["end"]], s["quoted"])
                self.assertTrue(s["note"])


class ConfusionDetails(unittest.TestCase):
    def test_list_provenance_recorded(self):
        for _p, _s, prov, _n in det.CONFUSIONS:
            self.assertTrue(prov == "general" or prov.startswith("seed:CF-"))
        s = det.detect("Dilgo. Quince. 575.")[0]
        self.assertEqual(s["suspected"], "Dilgo Khyentse")
        self.assertIn("seed:CF-001", s["note"])

    def test_lexicon_rules(self):
        lex = det._toy_lexicon()
        # lower-case, prefix variants and known words are not flagged
        self.assertEqual(det.detect("balsekor spoke", lexicon=lex), [])
        self.assertEqual(det.detect("Balsekars spoke", lexicon=lex), [])
        # corpus frequency gate
        self.assertEqual(det.detect("Balsekor spoke", lexicon=lex,
                                    transcript_freq={"balsekor": 9}), [])
        # held-out lexicon: excluding the only book removes the name
        held = det.build_lexicon({"b": "Balsekar x"}, exclude=("b",))
        self.assertEqual(held["proper"], {})
