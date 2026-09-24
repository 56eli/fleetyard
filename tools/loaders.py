"""Corpus loaders (TASK-002 / M1). Stdlib only, no network, read-only.

Transcript reader
    read_transcript(path) -> Transcript
    Paragraphs are newline-delimited blocks. Every transcript in the current
    corpus is a single line (M0 census), so it yields ONE paragraph (index 0)
    whose char offset is 0; finding locations are then (paragraph 0, global
    char offset). If a future file carries newlines, each non-blank line
    becomes its own paragraph with its own offsets. `sentences()` gives a
    finer, offset-preserving split for detectors that need it.

Book-store reader
    read_book_store(path) -> dict slug -> text
    Parses `const the_json_obj_books = { "slug": `...`, ... };` (JS template
    literals). Escapes \\` \\\\ \\$ are decoded; `${` interpolation is refused
    (would mean the file is not plain data).
"""
import os
import re
from collections import namedtuple

DEFAULT_CORPUS = os.path.join("corpus", "docdocgo")
OVERLAYS_DIR = os.path.join(DEFAULT_CORPUS, "overlays")
BOOK_STORE_PATH = os.path.join(DEFAULT_CORPUS, "html",
                               "merged-book-texts_json_1.js")

# Book-store entries that are NOT Hawkins' own writing (found at TASK-002:
# Ramana Maharshi "Be As You Are", Nisargadatta "I Am That", the Lamsa Bible,
# the ACIM workbook). They are reliable TEXT but not Hawkins DOCTRINE, so
# doctrinal checks (M3) must not cite them as Hawkins' teaching.
NON_HAWKINS_SLUGS = frozenset(["Be_as_you_are", "I_AM_THAT", "Lamsa_bible",
                               "ACIM_workbook"])

Paragraph = namedtuple("Paragraph", "index text char_offset byte_offset")
Sentence = namedtuple("Sentence", "text char_offset")


class Transcript(object):
    """A loaded transcript: raw text, paragraphs, U+FFFD positions."""

    def __init__(self, path, text):
        self.path = path
        self.text = text
        self.paragraphs = split_paragraphs(text)
        self.replacement_offsets = [i for i, ch in enumerate(text)
                                    if ch == "\ufffd"]

    def locate(self, char_offset):
        """Global char offset -> (paragraph index, offset within paragraph)."""
        if not 0 <= char_offset <= len(self.text):
            raise ValueError("offset out of range: %d" % char_offset)
        for p in reversed(self.paragraphs):
            if p.char_offset <= char_offset:
                return p.index, char_offset - p.char_offset
        return 0, char_offset

    def sentences(self):
        return split_sentences(self.text)


def split_paragraphs(text):
    """Non-blank newline-delimited blocks with char and UTF-8 byte offsets."""
    paras = []
    pos = 0
    for line in text.split("\n"):
        start = pos
        pos += len(line) + 1
        stripped = line.strip()
        if not stripped:
            continue
        lead = len(line) - len(line.lstrip())
        cstart = start + lead
        paras.append(Paragraph(len(paras), stripped, cstart,
                               len(text[:cstart].encode("utf-8"))))
    return paras


_SENT_END = re.compile(r"[.!?]+[\"'\u201d\u2019)]*(?=\s+|$)")


def split_sentences(text):
    """Sentences with char offsets (split after . ! ? followed by space)."""
    out = []
    start = 0
    n = len(text)
    while start < n and text[start].isspace():
        start += 1
    for m in _SENT_END.finditer(text):
        end = m.end()
        if end <= start:
            continue
        out.append(Sentence(text[start:end], start))
        start = end
        while start < n and text[start].isspace():
            start += 1
    if start < n and text[start:].strip():
        out.append(Sentence(text[start:].rstrip(), start))
    return out


def read_transcript(path):
    """Read an overlay transcript (UTF-8; undecodable bytes -> U+FFFD)."""
    with open(path, "rb") as fh:
        data = fh.read()
    return Transcript(path, data.decode("utf-8", errors="replace"))


def list_transcripts(overlays_dir=OVERLAYS_DIR):
    """Sorted paths of every transcript (*.txt; manifest.json excluded)."""
    return [os.path.join(overlays_dir, n) for n in sorted(os.listdir(overlays_dir))
            if n.endswith(".txt")]


_KEY = re.compile(r'"((?:[^"\\]|\\.)*)"\s*:\s*`')


def parse_book_store(src):
    """Parse the JS book-store source text into an ordered dict slug->text."""
    books = {}
    pos = src.find("{")
    if pos < 0:
        raise ValueError("no object literal found")
    while True:
        m = _KEY.search(src, pos)
        if not m:
            break
        slug = m.group(1)
        i = m.end()
        buf = []
        while True:
            if i >= len(src):
                raise ValueError("unterminated template literal for %r" % slug)
            ch = src[i]
            if ch == "\\" and i + 1 < len(src):
                buf.append(src[i + 1])
                i += 2
                continue
            if ch == "$" and src.startswith("${", i):
                raise ValueError("template interpolation in %r" % slug)
            if ch == "`":
                break
            buf.append(ch)
            i += 1
        if slug in books:
            raise ValueError("duplicate slug %r" % slug)
        books[slug] = "".join(buf)
        pos = i + 1
    if not books:
        raise ValueError("no books parsed")
    return books


def read_book_store(path=BOOK_STORE_PATH):
    with open(path, encoding="utf-8") as fh:
        return parse_book_store(fh.read())
