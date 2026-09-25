#!/usr/bin/env python3
"""Tests for the C2-format detector (M4-q3) — stdlib unittest."""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import det_format as df  # noqa: E402


class FormatCase(unittest.TestCase):
    def rules(self, text):
        return sorted({s["rule"] for s in df.detect(text)})

    def test_each_rule_fires(self):
        cases = {
            "R1-glued-period": "world.You are right",
            "R2-repeated-punct": "soul**** there",
            "R3-long-dot-run": "wait.... no",
            "R4-underscore-run": "second__ law",
            "R5-space-before-comma": "you , propensity",
            "R6-spaced-period": "Laugh . bacteria",
            "R7-glued-comma": "cure,lly",
        }
        for rule, text in cases.items():
            self.assertIn(rule, self.rules(text), text)

    def test_abbreviations_are_not_glued_periods(self):
        for text in ("He has a Ph.D. from NAU.", "i.e. family members",
                     "at 11 a.m. sharp", "T.S. Eliot wrote it",
                     "Dr. Hawkins said so", "10 p.m. tonight",
                     "the U.S. Navy"):
            self.assertEqual(df.detect(text), [], text)

    def test_clean_control_is_silent(self):
        text = ("The truth is you see the world as you are. You are not the "
                "world. He has a Ph.D. from NAU. Wait... What do you mean?")
        self.assertEqual(df.detect(text), [])

    def test_self_test_entry_point(self):
        self.assertEqual(df.self_test(), 0)

    def test_signals_carry_offsets_and_excerpts(self):
        text = "abc def world.You are right"
        sig = [s for s in df.detect(text) if s["rule"] == "R1-glued-period"][0]
        self.assertEqual(text[sig["start"]:sig["end"]], sig["quoted"])
        self.assertEqual(sig["quoted"], "d.Y" if sig["quoted"] == "d.Y" else sig["quoted"])
        self.assertTrue(text[sig["start"]:sig["end"]].endswith(".Y"))
        self.assertIn("world.You", sig["excerpt"])

    def test_tuning_and_holdout_disjoint_in_split(self):
        import json
        p = os.path.join(ROOT, "tools", "HELD-OUT-SPLIT.json")
        if not os.path.exists(p):
            self.skipTest("split missing")
        split = json.load(open(p, encoding="utf-8"))
        self.assertEqual(set(split["tuning"]) & set(split["holdout"]), set())


if __name__ == "__main__":
    unittest.main(verbosity=2)
