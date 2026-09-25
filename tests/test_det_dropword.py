#!/usr/bin/env python3
"""Tests for the C1-drop detector (M4-q2) — stdlib unittest.

Covers: the drop rule on toy books, the faithful-quote negative control, the
book-dialogue filter, tuning/holdout discipline (holdout never read, overlap
refused), shard merge determinism, and — when the local corpus is present —
byte-exact binding of fixtures/v2/dropword.json to transcript and book bytes.
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import det_dropword as dd  # noqa: E402

CORPUS = os.path.join(ROOT, "corpus")
FIXTURES = os.path.join(ROOT, "fixtures", "v2", "dropword.json")

BOOKS = {
    "toy": ("Spiritual purity has no interest in the personal lives of aspirants, "
            "or in clothing, dress, style, sex lives, economics.\n\n"
            "\u201cYou will see,\u201d she said, and then she said some thing, "
            "and the people laughed at her.\n\n"
            "Courage is the critical point of integrity at 200."),
}
T_DROP = ("Spiritual purity has no interest in the personal lives, or in clothing, "
          "dress, style, sex lives, economics.")
T_FAITHFUL = ("Spiritual purity has no interest in the personal lives of aspirants, "
              "or in clothing, dress, style, sex lives, economics.")


class DropWordCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = dd.BookIndex(BOOKS)

    def test_detects_a_dropped_content_word(self):
        sigs = dd.detect(T_DROP, self.index)
        self.assertTrue(sigs, "no drop detected")
        self.assertIn("aspirants", sigs[0]["dropped_words"])
        self.assertEqual(sigs[0]["book_ref"]["slug"], "toy")
        self.assertTrue(sigs[0]["quoted"] and sigs[0]["suspected"])

    def test_faithful_quote_produces_no_signal(self):
        self.assertEqual(dd.detect(T_FAITHFUL, self.index), [])

    def test_book_dialogue_filter(self):
        # a drop that sits inside the book's own quoted dialogue is skipped
        t = ("You will see, she said, and then she said some thing, and the "
             "people laughed at her.")
        hits = [s for s in dd.detect(t, self.index)
                if dd._inside_book_quote(BOOKS["toy"], s["book_ref"]["char_offset"])]
        self.assertEqual(hits, [])

    def test_self_test_entry_point(self):
        self.assertEqual(dd.self_test(), 0)

    def test_tuning_run_never_reads_holdout(self):
        with tempfile.TemporaryDirectory() as d:
            split = {"salt": "test", "corpus_files_sha256": "x",
                     "tuning": ["a.txt", "b.txt"], "holdout": ["h.txt"]}
            sp = os.path.join(d, "split.json")
            json.dump(split, open(sp, "w"))
            corpus = os.path.join(d, "corpus")
            os.makedirs(os.path.join(corpus, "docdocgo", "overlays"))
            os.makedirs(os.path.join(corpus, "docdocgo", "html"))
            for n in ("a.txt", "b.txt"):
                open(os.path.join(corpus, "docdocgo", "overlays", n), "w", encoding="utf-8").write(
                    "Short text with no book match at all.")
            open(os.path.join(corpus, "docdocgo", "html", "merged-book-texts_json_1.js"),
                 "w", encoding="utf-8").write(
                'const the_json_obj_books = {\n "toy": `Spiritual purity has no '
                'interest in the personal lives of aspirants, or in clothing, '
                'dress, style, sex lives.`,\n};\n')
            per_file, _ = dd.run_tuning(corpus, sp, os.path.join(d, "out"), quiet=True)
            self.assertEqual(sorted(per_file), ["a.txt", "b.txt"])
            self.assertNotIn("h.txt", per_file)
            # an overlapping split is refused outright
            bad = dict(split, tuning=["a.txt", "h.txt"])
            json.dump(bad, open(sp, "w"))
            with self.assertRaises(SystemExit):
                dd.run_tuning(corpus, sp, os.path.join(d, "out"), quiet=True)

    def test_merge_is_deterministic_and_rejects_duplicates(self):
        with tempfile.TemporaryDirectory() as d:
            for tag, data in (("1", {"a.txt": [{"x": 1}]}),
                              ("2", {"b.txt": [{"x": 2}]})):
                json.dump(data, open(os.path.join(d, "part-%s.json" % tag), "w"))
            m1 = dd.merge_parts(d)
            m2 = dd.merge_parts(d)
            self.assertEqual(m1["signals_total"], 2)
            self.assertEqual(m1["signals_json_sha256"], m2["signals_json_sha256"])
            json.dump({"a.txt": []}, open(os.path.join(d, "part-3.json"), "w"))
            with self.assertRaises(SystemExit):
                dd.merge_parts(d)


class FixtureBindingCase(unittest.TestCase):
    @unittest.skipUnless(os.path.isdir(CORPUS), "local corpus not extracted")
    def test_v2_fixtures_bind_to_transcript_and_book_bytes(self):
        doc = json.load(open(FIXTURES, encoding="utf-8"))
        transcripts = None
        books = None
        for f in doc["fixtures"]:
            name = os.path.basename(f["transcript"])
            if transcripts is None:
                sys.path.insert(0, os.path.join(ROOT, "tools"))
                import m5r_reduce as m5r
                transcripts = m5r.load_transcripts(CORPUS)
                books = m5r.parse_book_store(os.path.join(
                    CORPUS, "docdocgo", "html", "merged-book-texts_json_1.js"))
            text = transcripts[name]
            self.assertEqual(text[f["char_offset"]:f["char_offset"] + len(f["quoted"])],
                             f["quoted"], f["id"])
            b = books[f["book_ref"]["slug"]]
            off = f["book_ref"]["char_offset"]
            self.assertEqual(b[off:off + len(f["book_ref"]["quote"])],
                             f["book_ref"]["quote"], f["id"])
            self.assertNotEqual(f["suspected"], f["quoted"], f["id"])

    def test_holdout_split_excludes_every_fixture_transcript(self):
        split_path = os.path.join(ROOT, "tools", "HELD-OUT-SPLIT.json")
        if not os.path.exists(split_path):
            self.skipTest("split file missing")
        split = json.load(open(split_path, encoding="utf-8"))
        self.assertTrue(set(split["tuning"]) & set(split["holdout"]) == set())
        self.assertEqual(len(split["tuning"]) + len(split["holdout"]),
                         split["counts"]["total"])
        if os.path.exists(FIXTURES):
            doc = json.load(open(FIXTURES, encoding="utf-8"))
            for f in doc["fixtures"]:
                self.assertIn(os.path.basename(f["transcript"]), split["tuning"])
                self.assertNotIn(os.path.basename(f["transcript"]), split["holdout"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
