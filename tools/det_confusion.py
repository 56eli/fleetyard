#!/usr/bin/env python3
"""A4-confusion — acoustic-confusion candidates (TASK-004 / M2, family A).

Two paths:
  list   : a hand-built confusion list (CONFUSIONS). Each entry records its
           provenance: "seed:CF-xxx" = learned from a hand-found fixture
           (so fixture hits on these are NOT independent evidence of recall),
           "general" = written from domain knowledge, not from a fixture.
  lexicon: difflib near-form of a PROPER NAME. A capitalized transcript
           token that never occurs in the Hawkins books and is rare in the
           transcripts (<= MAX_TRANSCRIPT_FREQ corpus-wide, when counts are
           given) but is a close difflib match (>= CUTOFF, not a mere
           prefix/suffix variant) to a book word that is >= 90% capitalized
           and occurs >= 3 times (a name/term: "Balsakar" -> "Balsekar").

Stdlib only. The lexicon is built from the book store by the caller
(build_lexicon) so evaluation can hold a book out.
Self-test: python3 tools/det_confusion.py --self-test
"""
import collections
import difflib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokenizer  # noqa: E402

DETECTOR_ID = "A4-confusion"
CUTOFF = 0.82
MAX_TRANSCRIPT_FREQ = 3

# (regex, suggestion, provenance, note). Regexes are case-insensitive.
CONFUSIONS = [
    (r"\bDilgo\W+Quince\b", "Dilgo Khyentse", "seed:CF-001",
     "Tibetan name heard as English 'quince'"),
    (r"\bJempolski\b", "Jampolsky", "seed:CF-002", "author name near-form"),
    (r"\bunquestionable love\b", "unconditional love", "seed:CF-004",
     "Hawkins term 'unconditional love' (cal. 540)"),
    (r"\bGiven to Caesar\b", "Give unto Caesar", "seed:CF-010",
     "scripture quote; 'unto' heard as 'to'"),
    (r"(?:^|(?<=[.!?]\s))Except that God\b", "Accept that God", "seed:CF-011",
     "homophone accept/except"),
    (r"(?<!Gloria )(?<!Gloria, )\b(?:We are |We're )?in excelsis\b",
     "Gloria in excelsis", "seed:CF-012", "closing prayer 'Gloria in "
     "excelsis Deo' with 'Gloria' lost"),
    (r"\bcustody bills?\b", "custody battle", "seed:CF-013",
     "near-form bill/battle"),
    (r"\bintegrus\b", "integrous", "seed:CF-017", "Hawkins term 'integrous'"),
    (r"\bexelsis\b|\bexcelsior Deo\b", "excelsis", "general",
     "Latin prayer word near-form"),
    (r"\bkinesiologi\b|\bkinesthesiology\b", "kinesiology", "general",
     "Hawkins term"),
    (r"\bKrillian\b", "Kirlian", "general", "Kirlian photography"),
    (r"\bBals[ai]kar\b|\bBhalsikar\b|\bBalasikar\b", "Balsekar", "general",
     "Ramesh Balsekar"),
    (r"\bMut?kananda\b|\bMatkananda\b", "Muktananda", "general",
     "Swami Muktananda"),
]
_COMPILED = [(re.compile(p, re.I), s, prov, note)
             for p, s, prov, note in CONFUSIONS]


def book_counts(books):
    """Per-book (lower-case counts, capitalized counts) for build_lexicon."""
    out = {}
    for slug, text in books.items():
        low = collections.Counter()
        cap = collections.Counter()
        for t in tokenizer.tokenize(text):
            w = t.text.replace("\u2019", "'")
            lw = w.lower()
            low[lw] += 1
            if w[0].isupper():
                cap[lw] += 1
        out[slug] = (low, cap)
    return out


def build_lexicon(books=None, exclude=(), counts=None):
    """Proper-name lexicon: {"words": all book words, "proper": by initial}.

    Pass `books` (slug -> text) or precomputed `counts` (book_counts()).
    Books whose slug is in `exclude` are left out (held-out evaluation).
    """
    if counts is None:
        counts = book_counts(books)
    low = collections.Counter()
    cap = collections.Counter()
    for slug, (lo, ca) in counts.items():
        if slug in exclude:
            continue
        low.update(lo)
        cap.update(ca)
    proper = collections.defaultdict(list)
    for w, c in low.items():
        if c >= 3 and len(w) >= 4 and w.isalpha() and cap[w] >= 0.9 * c:
            proper[w[0]].append(w)
    return {"words": low, "proper": dict(proper)}


def detect(text, lexicon=None, transcript_freq=None, **_ctx):
    out = []
    taken = []
    for rx, sug, prov, note in _COMPILED:
        for m in rx.finditer(text):
            out.append({"detector": DETECTOR_ID, "start": m.start(),
                        "end": m.end(), "quoted": m.group(0),
                        "suspected": sug,
                        "note": "list (%s): %s" % (prov, note)})
            taken.append((m.start(), m.end()))
    if lexicon is not None:
        words, proper = lexicon["words"], lexicon["proper"]
        for t in tokenizer.tokenize(text):
            w = t.text
            if len(w) < 4 or not w.isalpha() or not w[0].isupper():
                continue
            lw = w.lower()
            if lw in words:
                continue
            if transcript_freq is not None and \
                    transcript_freq.get(lw, 0) > MAX_TRANSCRIPT_FREQ:
                continue
            if any(s <= t.start < e for s, e in taken):
                continue
            cands = [c for c in proper.get(lw[0], ())
                     if abs(len(c) - len(lw)) <= 2]
            m = difflib.get_close_matches(lw, cands, n=1, cutoff=CUTOFF)
            if not m or m[0].startswith(lw) or lw.startswith(m[0]):
                continue
            sug = m[0].capitalize()
            ratio = difflib.SequenceMatcher(None, lw, m[0]).ratio()
            out.append({"detector": DETECTOR_ID, "start": t.start,
                        "end": t.end, "quoted": w, "suspected": sug,
                        "note": "lexicon: not in Hawkins books; near-form "
                                "of book name '%s' (difflib %.2f)" %
                                (sug, ratio)})
    out.sort(key=lambda s: s["start"])
    return out


def _toy_lexicon():
    books = {"b": "Ramesh Balsekar taught. Balsekar wrote. Balsekar spoke. "
                  "Unconditional love is the goal of the teaching."}
    return build_lexicon(books)


SELF_TEST = [
    ("Rumi. Dilgo. Quince. 570.", None, 1),
    ("God loves you. Accept that. Except that God loves you.", None, 1),
    ("We are in excelsis Deo.", None, 1),
    ("Gloria in excelsis Deo.", None, 0),
    ("I met Balsekor yesterday.", "toy", 1),   # lexicon path (not in list)
    ("I met Balsekar yesterday.", "toy", 0),
    ("Except that it rained, all was well.", None, 0),
]


def self_test():
    ok = True
    toy = _toy_lexicon()
    for text, lex, want in SELF_TEST:
        got = len(detect(text, lexicon=toy if lex else None))
        if got != want:
            print("FAIL: %r -> %d (want %d)" % (text[:40], got, want))
            ok = False
    print("%s self-test %s" % (DETECTOR_ID, "OK" if ok else "FAIL"))
    return ok


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print(__doc__)
