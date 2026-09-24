"""Tests for tools/retrieval.py (SELF-M3a)."""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import fixtures  # noqa: E402
import loaders  # noqa: E402
import retrieval  # noqa: E402

CORPUS = os.path.join(ROOT, "corpus", "docdocgo")

TOY = {
    "book_a": ("Unconditional love calibrates at 540 and heals.\n\n"
               "The ego is not the real you.\n\n" + "Filler text. " * 40),
    "book_b": "Courage is the critical point of integrity at 200.\n\n" * 3,
    "I_AM_THAT": "Unconditional love unconditional love 540.",
}


class PassageTest(unittest.TestCase):
    def test_offsets_exact_and_sized(self):
        text = TOY["book_a"]
        ps = retrieval.split_passages(text)
        for off, p in ps:
            self.assertEqual(text[off:off + len(p)], p)
            self.assertLessEqual(len(p), retrieval.MAX_CHARS)
        self.assertEqual(ps[0][0], 0)

    def test_terms_drop_stopwords_and_digits(self):
        self.assertEqual(retrieval.terms("The ego is at 200 and it"), ["ego"])


class ToyIndexTest(unittest.TestCase):
    def setUp(self):
        self.idx = retrieval.BookIndex(TOY)

    def test_ranking(self):
        top = self.idx.query("love that is unconditional", k=1)[0]
        self.assertEqual(top.slug, "book_a")
        self.assertEqual(TOY["book_a"][top.char_offset:].split("\n")[0],
                         "Unconditional love calibrates at 540 and heals.")
        self.assertEqual(self.idx.query("courage integrity")[0].slug, "book_b")

    def test_non_hawkins_excluded_by_default(self):
        self.assertNotIn("I_AM_THAT", {p[0] for p in self.idx.passages})
        full = retrieval.BookIndex(TOY, include_non_hawkins=True)
        self.assertIn("I_AM_THAT", {p[0] for p in full.passages})

    def test_empty_query(self):
        self.assertEqual(self.idx.query("the and of"), [])


@unittest.skipUnless(os.path.isdir(CORPUS), "corpus/ not extracted locally")
class FixtureRecallTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cwd = os.getcwd()
        os.chdir(ROOT)
        try:
            cls.idx = retrieval.BookIndex(loaders.read_book_store())
            cls.res = dict(retrieval.eval_fixtures(
                cls.idx, fixtures.load_json(fixtures.CONFIRMED_PATH)))
        finally:
            os.chdir(cwd)

    def test_recall_floor(self):
        # measured 6/10 at SELF-M3a; a drop is a regression
        self.assertEqual(len(self.res), 10)
        self.assertGreaterEqual(sum(1 for r in self.res.values() if r), 6)

    def test_known_hits(self):
        self.assertLessEqual(self.res["CF-015"], 3)
        self.assertLessEqual(self.res["CF-012"], 3)
