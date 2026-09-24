"""Tests for tools/loaders.py (TASK-002)."""
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import loaders  # noqa: E402

CORPUS = os.path.join(ROOT, "corpus", "docdocgo")


class ParagraphTest(unittest.TestCase):
    def test_single_line_is_one_paragraph(self):
        ps = loaders.split_paragraphs("Hello there. General Kenobi.")
        self.assertEqual(len(ps), 1)
        self.assertEqual((ps[0].index, ps[0].char_offset, ps[0].byte_offset),
                         (0, 0, 0))

    def test_multi_line_offsets(self):
        text = "caf\u00e9 one\n\n  two\nthree\n"
        ps = loaders.split_paragraphs(text)
        self.assertEqual([p.text for p in ps], ["caf\u00e9 one", "two", "three"])
        for p in ps:
            self.assertEqual(text[p.char_offset:p.char_offset + len(p.text)],
                             p.text)
            self.assertEqual(
                text.encode("utf-8")[p.byte_offset:].decode("utf-8")
                .startswith(p.text), True)
        self.assertEqual(ps[1].byte_offset, ps[1].char_offset + 1)  # é = 2 B

    def test_sentences_offsets(self):
        text = "  One. Two? \"Three!\" four"
        ss = loaders.split_sentences(text)
        self.assertEqual([s.text for s in ss],
                         ["One.", "Two?", "\"Three!\"", "four"])
        for s in ss:
            self.assertEqual(text[s.char_offset:s.char_offset + len(s.text)],
                             s.text)


class TranscriptTest(unittest.TestCase):
    def test_read_and_locate_and_fffd(self):
        with tempfile.NamedTemporaryFile("wb", suffix=".txt",
                                         delete=False) as fh:
            fh.write(b"ab\xffc\nde")
        try:
            t = loaders.read_transcript(fh.name)
        finally:
            os.unlink(fh.name)
        self.assertEqual(t.text, "ab\ufffdc\nde")
        self.assertEqual(t.replacement_offsets, [2])
        self.assertEqual(t.locate(1), (0, 1))
        self.assertEqual(t.locate(6), (1, 1))
        with self.assertRaises(ValueError):
            t.locate(99)


class BookStoreTest(unittest.TestCase):
    def test_parse(self):
        src = ('const x = {\n    "a_b": `line one\nline \\` two`,\n'
               '    "c": `x`\n};\n')
        self.assertEqual(loaders.parse_book_store(src),
                         {"a_b": "line one\nline ` two", "c": "x"})

    def test_rejects_interpolation_and_dupes(self):
        with self.assertRaises(ValueError):
            loaders.parse_book_store('o = { "a": `${x}` };')
        with self.assertRaises(ValueError):
            loaders.parse_book_store('o = { "a": `1`, "a": `2` };')
        with self.assertRaises(ValueError):
            loaders.parse_book_store('o = { "a": `unterminated };')


@unittest.skipUnless(os.path.isdir(CORPUS), "corpus/ not extracted locally")
class RealCorpusTest(unittest.TestCase):
    def test_all_transcripts_load(self):
        paths = loaders.list_transcripts(os.path.join(CORPUS, "overlays"))
        self.assertEqual(len(paths), 230)
        fffd_files = 0
        for p in paths:
            t = loaders.read_transcript(p)
            self.assertEqual(len(t.paragraphs), 1)   # M0: all single-line
            fffd_files += bool(t.replacement_offsets)
        self.assertEqual(fffd_files, 9)             # matches M0 census

    def test_book_store(self):
        books = loaders.read_book_store(
            os.path.join(CORPUS, "html", "merged-book-texts_json_1.js"))
        self.assertEqual(len(books), 24)
        self.assertTrue(loaders.NON_HAWKINS_SLUGS <= set(books))
        self.assertIn("truth_vs_falsehood", books)
        self.assertTrue(all(len(v) > 90000 for v in books.values()))
