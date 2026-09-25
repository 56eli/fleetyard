#!/usr/bin/env python3
"""Tests for the TASK-018 leg-(d) adjudicator (stdlib unittest, synthetic where possible)."""
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import m4_q2_adjudicate as adj  # noqa: E402

BOOK = ("Spiritual purity has no interest in the personal lives of aspirants, or in "
        "clothing, dress, style, sex lives, economics, family patterns, and dietary "
        "habits of the sincere student of truth.\n")
BOOKS = {"toy": BOOK}
BOOKWORD = "aspirants"
PHRASE = "the personal lives of aspirants, or in clothing, dress, style"
BOFF = BOOK.index(PHRASE)                 # cited ground-truth span contains the word


def signal(text, span_text, dropped, book_quote=None, boff=None, start=None):
    s = text.index(span_text) if start is None else start
    return {"_transcript": "toy.txt", "start": s, "end": s + len(span_text),
            "quoted": span_text, "dropped_words": dropped,
            "note": "synthetic", "_id": "D-TEST",
            "book_ref": {"slug": "toy", "char_offset": boff if boff is not None else BOFF,
                         "quote": book_quote if book_quote else PHRASE}}


class LegDCase(unittest.TestCase):
    def test_single_word_omission_is_promoted_with_cited_bytes(self):
        t = BOOK.replace("aspirants, ", ", ")        # drops exactly the one word
        rec = adj.adjudicate_signal(t, BOOKS,
                                    signal(t, "lives of , or in clothing", ["aspirants"]), 1, [])
        self.assertEqual(rec["verdict"], "CERTAIN-leg-d")
        self.assertEqual(rec["clause"], "d-i")
        self.assertTrue(rec["citation_ok"] and rec["book_quote_ok"])
        self.assertTrue(rec["restored_matches_ground_truth"])
        self.assertTrue(rec["restoration_is_minimal"])
        self.assertEqual(rec["omitted_word"], "aspirants")
        self.assertGreaterEqual(min(rec["flank_tokens"].values()), adj.FLANK_MIN)
        # the cited ground truth re-derives from the book bytes
        gt = rec["ground_truth"]
        self.assertEqual(BOOK[gt["char_offset"]:gt["char_offset"] + len(gt["quote"])],
                         gt["quote"])

    def test_faithful_span_stays_candidate(self):
        rec = adj.adjudicate_signal(BOOK, BOOKS,
                                    signal(BOOK, "lives of aspirants, or", ["aspirants"]),
                                    1, [])
        self.assertEqual(rec["verdict"], "CANDIDATE")

    def test_two_word_omission_is_never_promoted(self):
        t = BOOK.replace(" of aspirants,", ",")           # drops "of" + "aspirants"
        rec = adj.adjudicate_signal(t, BOOKS,
                                    signal(t, "lives, or in", ["of", "aspirants"]), 1, [])
        self.assertEqual(rec["verdict"], "CANDIDATE")
        self.assertIn(rec["reason_code"], ("restoration-not-minimal", "region-not-realignable"))

    def test_short_flank_single_word_stays_candidate(self):
        t = BOOK.replace("aspirants", "seekers")               # a substitution, not a drop
        rec = adj.adjudicate_signal(t, BOOKS, signal(t, "lives of seekers, or", ["aspirants"]),
                                    1, [])
        self.assertEqual(rec["verdict"], "CANDIDATE")

    def test_flank_floor_is_parameterised_and_reported(self):
        t = BOOK.replace("aspirants,", ",")
        strict = adj.adjudicate_signal(t, BOOKS,
                                       signal(t, "lives of , or in clothing", ["aspirants"]),
                                       1, [], flank_min=99)
        self.assertEqual(strict["verdict"], "CANDIDATE")
        self.assertEqual(strict["reason_code"], "flank-too-short")
        self.assertTrue(strict["restoration_is_minimal"])

    def test_hyphenated_words_are_one_token(self):
        self.assertEqual(adj.tok("Mm-hmm. Mm-hmm."), ["mm-hmm", "mm-hmm"])

    def test_citation_mismatch_fails_l2(self):
        t = BOOK.replace("aspirants,", ",")
        sig = signal(t, "lives of , or in clothing", ["aspirants"])
        sig["quoted"] = "not what is in the file"
        rec = adj.adjudicate_signal(t, BOOKS, sig, 1, [])
        self.assertEqual(rec["verdict"], "CANDIDATE")
        self.assertFalse(rec["citation_ok"])


class ArtifactCase(unittest.TestCase):
    """Checks on the delivered artifacts (skipped when they are absent)."""

    ADJ = os.path.join(ROOT, "runs", "m4-q2-adjudication", "adjudication.jsonl")
    FXR = os.path.join(ROOT, "runs", "m4-q2-adjudication", "fixtures-adjudication.json")
    FIX = os.path.join(ROOT, "fixtures", "v2", "dropword.json")
    SIGNALS = os.path.join(ROOT, "runs", "m4-q2-dropword", "signals.json")

    def rows(self):
        if not os.path.exists(self.ADJ):
            self.skipTest("adjudication artifact absent")
        with open(self.ADJ, encoding="utf-8") as fh:
            return [json.loads(l) for l in fh]

    def test_every_signal_has_a_record(self):
        rows = self.rows()
        self.assertEqual(len(rows), 122)
        with open(self.SIGNALS, encoding="utf-8") as fh:
            n = sum(len(v) for v in json.load(fh).values())
        self.assertEqual(len(rows), n)

    def test_records_carry_the_l1_fields(self):
        for r in self.rows():
            for key in ("id", "transcript", "char_offset", "detector_dropped_words",
                        "verdict", "clause", "reason"):
                self.assertIn(key, r, key)
            if r["verdict"] == "CERTAIN-leg-d":
                for key in ("span", "span_start", "span_end_matched", "ground_truth",
                            "omitted_word", "restored_span", "flank_tokens"):
                    self.assertIn(key, r, (r["id"], key))
                self.assertEqual(r["clause"], "d-i" if r["ground_truth"]["kind"] == "book"
                                 else "d-ii")
                self.assertTrue(r["citation_ok"] and r["book_quote_ok"])
                self.assertTrue(r["restoration_is_minimal"])
                self.assertGreaterEqual(min(r["flank_tokens"].values()), 5)

    def test_no_blanket_promotion_and_counts_match_summary(self):
        rows = self.rows()
        promoted = [r for r in rows if r["verdict"] == "CERTAIN-leg-d"]
        self.assertTrue(all(r.get("reason") for r in rows))
        self.assertTrue(all(r.get("omitted_word") for r in promoted))
        with open(os.path.join(os.path.dirname(self.ADJ), "PROVENANCE.json"),
                  encoding="utf-8") as fh:
            prov = json.load(fh)
        self.assertEqual(prov["counts"]["by_verdict"].get("CERTAIN-leg-d", 0), len(promoted))
        self.assertEqual(prov["counts"]["signals"], len(rows))

    def test_fixtures_adjudicated_with_reasons(self):
        if not os.path.exists(self.FXR):
            self.skipTest("fixture adjudication absent")
        with open(self.FXR, encoding="utf-8") as fh:
            fx = json.load(fh)
        self.assertEqual(len(fx), 4)
        for r in fx:
            self.assertIn(r["verdict"], ("CERTAIN-leg-d", "CANDIDATE"))
            self.assertTrue(r["reason"])
            self.assertTrue(r["in_sample"] and r["seeded"])
            self.assertIn("adjudication", r)

    def test_fixture_file_annotated_append_only(self):
        if not os.path.exists(self.FIX):
            self.skipTest("fixture file absent")
        with open(self.FIX, encoding="utf-8") as fh:
            doc = json.load(fh)
        self.assertIn("adjudication_summary_2026_09_25", doc)
        for f in doc["fixtures"]:
            self.assertIn("adjudication_2026_09_25", f)
            self.assertTrue(f["suspected"] and f["quoted"])   # original claim intact

    def test_determinism_two_runs_byte_identical(self):
        rows = self.rows()
        with tempfile.TemporaryDirectory() as d:
            rc = adj.main(["--out", d, "--flank-min", "5", "--tool-commit", "X",
                           "--main-head", "X", "--policy-sha", "X", "--book-store-sha", "X"])
            self.assertEqual(rc, 0)
            with open(self.ADJ, encoding="utf-8") as fh:
                a = fh.read()
            with open(os.path.join(d, "adjudication.jsonl"), encoding="utf-8") as fh:
                b = fh.read()
            # provenance carries run_utc/mains; the rows must be identical
            self.assertEqual(a, b)
            shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
