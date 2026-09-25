"""Tests for tools/det_contradiction.py (TASK-005, B1)."""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import det_contradiction as dc  # noqa: E402
import fixtures  # noqa: E402
import loaders  # noqa: E402

CORPUS = os.path.join(ROOT, "corpus", "docdocgo")


class ToyTest(unittest.TestCase):
    def setUp(self):
        self.ref = dc._toy_reference()

    def test_self_test(self):
        self.assertTrue(dc.self_test())

    def test_no_reference_no_signals(self):
        self.assertEqual(dc.detect("By courage 255% are happy."), [])

    def test_happiness_signal_fields(self):
        text = "By the level courage. 255% of people are happy."
        (s,) = dc.detect(text, reference=self.ref)
        self.assertEqual(s["detector"], dc.DETECTOR_ID)
        self.assertEqual(text[s["start"]:s["end"]], s["quoted"])
        self.assertEqual(s["quoted"], "255%")
        self.assertEqual(s["suspected"], "55%")
        ref = s["book_ref"]
        self.assertEqual(ref["slug"], dc.HAPPY_SLUG)

    def test_book_ref_quote_is_verbatim(self):
        books = {dc.HAPPY_SLUG: "x " + dc.HAPPY_ANCHOR + " Courage 200 55 z",
                 dc.MAP_SLUG: dc.MAP_ANCHOR + " Courage 200",
                 dc.POLARITY_SLUG: "At level 200, energy goes positive."}
        ref = dc.parse_tables(books)
        (s,) = dc.detect("Courage. 12% are happy.", reference=ref)
        b = s["book_ref"]
        q = books[b["slug"]][b["char_offset"]:b["char_offset"] + len(b["quote"])]
        self.assertEqual(q, b["quote"])

    def test_layout_newline_is_not_a_claim(self):
        # table/title layout ("ENLIGHTENMENT\n\n365") must not read as a log
        self.assertEqual(dc.detect("ENLIGHTENMENT\n\n\n365 days",
                                   reference=self.ref), [])
        self.assertEqual(dc.detect("A Teacher of Enlightenment 800 pages.",
                                   reference=self.ref), [])


@unittest.skipUnless(os.path.isdir(CORPUS), "corpus/ not extracted locally")
class CorpusTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cwd = os.getcwd()
        os.chdir(ROOT)
        try:
            cls.books = loaders.read_book_store()
            cls.ref = dc.parse_tables(cls.books)
            cls.conf = fixtures.load_json(fixtures.CONFIRMED_PATH)
            cls.clean = fixtures.load_json(fixtures.CLEAN_PATH)
            cls.texts = {p: loaders.read_transcript(p).text
                         for p in {c["transcript"] for c in cls.conf}}
        finally:
            os.chdir(cwd)

    def test_reference_parsed_from_books(self):
        self.assertEqual(self.ref["happy"]["Courage"], 55)
        self.assertEqual(self.ref["happy"]["Love"], 89)
        self.assertEqual(len(self.ref["happy"]), 18)
        # prose values the books themselves give are accepted
        self.assertTrue({600, 700} <= self.ref["logs"]["Enlightenment"])

    def test_fixture_hits(self):
        hits = set()
        for fx in self.conf:
            a, b = fx["char_offset"], fx["char_offset"] + len(fx["quoted"])
            for s in dc.detect(self.texts[fx["transcript"]], reference=self.ref):
                if s["start"] < b and a < s["end"]:
                    hits.add(fx["id"])
        self.assertEqual(hits, {"CF-003", "CF-006"})

    def test_zero_clean_false_positives(self):
        fps = [(r["id"], s["quoted"]) for r, t in
               fixtures.materialize_clean(self.clean, self.books)
               for s in dc.detect(t, reference=self.ref)]
        self.assertEqual(fps, [])

    def test_books_do_not_contradict_themselves(self):
        # the whole Hawkins book store as a clean set: 0 signals
        fps = [(slug, s["quoted"]) for slug, t in self.books.items()
               if slug not in loaders.NON_HAWKINS_SLUGS
               for s in dc.detect(t, reference=self.ref)]
        self.assertEqual(fps, [])


if __name__ == "__main__":
    unittest.main()
