"""Tests for tools/det_misquote.py (TASK-005, B2)."""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import det_misquote as dm  # noqa: E402
import fixtures  # noqa: E402
import loaders  # noqa: E402
import retrieval  # noqa: E402

CORPUS = os.path.join(ROOT, "corpus", "docdocgo")
CF015 = ("So the teacher is non-controlling. Spiritual purity has no "
         "influence interest in the personal lives of aspirants, or in "
         "clothing, dress, style, sex lives, economics, family patterns.")


class ToyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.idx = dm.toy_index()

    def test_self_test(self):
        self.assertTrue(dm.self_test())

    def test_no_index_no_signals(self):
        self.assertEqual(dm.detect(CF015), [])

    def test_extra_word_signal(self):
        (s,) = dm.detect(CF015, index=self.idx)
        self.assertEqual(s["quoted"], "no influence interest")
        self.assertEqual(s["suspected"], "no interest")
        self.assertEqual(CF015[s["start"]:s["end"]], s["quoted"])
        b = s["book_ref"]
        book = dm._TOY_BOOKS[b["slug"]]
        self.assertEqual(book[b["char_offset"]:b["char_offset"] +
                              len(b["quote"])], b["quote"])
        self.assertIn("has no interest in the personal lives", b["quote"])

    def test_near_form_substitution(self):
        (s,) = dm.detect("Okay. The goal of his teaching was for his "
                         "followers to reach unquestionable love, and once it "
                         "was reached the soul was safe.", index=self.idx)
        self.assertEqual(s["quoted"], "unquestionable")
        self.assertEqual(s["suspected"], "Unconditional")

    def test_variants_are_not_misquotes(self):
        for a, b in [("all encompassing", "all-encompassing"),
                     ("capacity", "capacities"), ("realizing", "realize"),
                     ("milosevic", "milošević")]:
            self.assertTrue(dm._variant(a, b), (a, b))
        self.assertFalse(dm._variant("unquestionable", "unconditional"))

    def test_exclude_own_book(self):
        text = dm._TOY_BOOKS["book_a"].replace("no interest",
                                               "no influence interest")
        self.assertTrue(dm.detect(text, index=self.idx))
        self.assertEqual(dm.detect(text, index=self.idx,
                                   exclude_slugs=("book_a",)), [])


@unittest.skipUnless(os.path.isdir(CORPUS), "corpus/ not extracted locally")
class CorpusTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cwd = os.getcwd()
        os.chdir(ROOT)
        try:
            cls.books = loaders.read_book_store()
            cls.idx = retrieval.BookIndex(cls.books)
            cls.conf = fixtures.load_json(fixtures.CONFIRMED_PATH)
            cls.clean = fixtures.load_json(fixtures.CLEAN_PATH)
        finally:
            os.chdir(cwd)

    def test_cf015_hit_with_book_ref(self):
        fx = [c for c in self.conf if c["id"] == "CF-015"][0]
        text = loaders.read_transcript(os.path.join(ROOT, fx["transcript"])).text
        a, b = fx["char_offset"], fx["char_offset"] + len(fx["quoted"])
        sigs = [s for s in dm.detect(text, index=self.idx)
                if s["start"] < b and a < s["end"]]
        self.assertEqual(len(sigs), 1)
        self.assertEqual(sigs[0]["suspected"], "no interest")
        ref = sigs[0]["book_ref"]
        # the passage is reprinted in several books; any verbatim copy of
        # the fixture's book sentence is an acceptable reference
        self.assertIn("Spiritual purity has no interest in the personal lives",
                      ref["quote"])
        self.assertIn("has no interest in the personal lives",
                      fx["book_ref"]["quote"])
        book = self.books[ref["slug"]]
        self.assertEqual(book[ref["char_offset"]:ref["char_offset"] +
                              len(ref["quote"])], ref["quote"])

    def test_zero_clean_false_positives_held_out(self):
        fps = [(r["id"], s["quoted"]) for r, t in
               fixtures.materialize_clean(self.clean, self.books)
               for s in dm.detect(t, index=self.idx,
                                  exclude_slugs=(r["slug"],))]
        self.assertEqual(fps, [])


if __name__ == "__main__":
    unittest.main()
