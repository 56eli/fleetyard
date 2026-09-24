"""Tests for the fixture sets and tools/fixtures.py (TASK-002)."""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import fixtures  # noqa: E402
import loaders  # noqa: E402

CORPUS = os.path.join(ROOT, "corpus", "docdocgo")
CONFIRMED = os.path.join(ROOT, fixtures.CONFIRMED_PATH)
CLEAN = os.path.join(ROOT, fixtures.CLEAN_PATH)


class ConfirmedShapeTest(unittest.TestCase):
    """Corpus-free checks of the confirmed set's shape (STANDARDS record)."""

    @classmethod
    def setUpClass(cls):
        cls.recs = fixtures.load_json(CONFIRMED)

    def test_count_and_spread(self):
        self.assertGreaterEqual(len(self.recs), 15)
        self.assertGreaterEqual(len({r["transcript"] for r in self.recs}), 3)

    def test_fields_and_taxonomy(self):
        ids = set()
        for r in self.recs:
            for f in fixtures.REQUIRED_FIELDS:
                self.assertIn(f, r, r.get("id"))
            self.assertNotIn(r["id"], ids)
            ids.add(r["id"])
            self.assertEqual(r["confidence"], "CERTAIN")
            self.assertIn(r["evidence_class"], ("a", "b", "c"))
            self.assertTrue(r["transcript"].startswith(
                "corpus/docdocgo/overlays/"))
            self.assertNotEqual(r["quoted"], r["suspected"])
            if r["evidence_class"] == "b":
                self.assertIsNotNone(r["book_ref"])


class CleanShapeTest(unittest.TestCase):
    def test_pointers_only(self):
        recs = fixtures.load_json(CLEAN)
        self.assertGreaterEqual(len(recs), 40)
        for r in recs:
            self.assertEqual(set(r), {"id", "slug", "char_offset", "length",
                                      "sha256"})
            self.assertNotIn(r["slug"], loaders.NON_HAWKINS_SLUGS)

    def test_pick_passage_rejects_tables(self):
        table = "Rumi 550. Plato 485. Buddha 1000. Zen 540. " * 40
        self.assertIsNone(fixtures.pick_passage(table, 0))
        prose = "This is a clean sentence about the Self. " * 40
        got = fixtures.pick_passage("x. " + prose, 0)
        self.assertIsNotNone(got)
        self.assertGreaterEqual(len(got[1]), fixtures.CLEAN_MIN)


@unittest.skipUnless(os.path.isdir(CORPUS), "corpus/ not extracted locally")
class AgainstCorpusTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.books = loaders.read_book_store(
            os.path.join(CORPUS, "html", "merged-book-texts_json_1.js"))

    def test_confirmed_quotes_verbatim(self):
        cwd = os.getcwd()
        os.chdir(ROOT)
        try:
            probs = fixtures.verify_confirmed(fixtures.load_json(CONFIRMED),
                                              self.books)
        finally:
            os.chdir(cwd)
        self.assertEqual(probs, [])

    def test_clean_materializes_and_is_reproducible(self):
        recs = fixtures.load_json(CLEAN)
        self.assertEqual(len(fixtures.materialize_clean(recs, self.books)),
                         len(recs))
        self.assertEqual(fixtures.build_clean(self.books), recs)
