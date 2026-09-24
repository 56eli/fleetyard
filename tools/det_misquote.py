#!/usr/bin/env python3
"""B2-misquote — near-verbatim book quotes with altered words (TASK-005/M3).

Lectures quote the books constantly (slides are read aloud from them). A
transcript window that aligns with a Hawkins book passage almost word for
word, except for a few changed words, is a misquotation candidate: either
the ASR garbled the quote or the speaker altered it. The signal carries the
book slug + char offset + verbatim book text of the aligned region.

Algorithm: slide a WINDOW-token window (stride STRIDE) over the transcript;
retrieve the top book passage (tools/retrieval.py TF-IDF); word-align with
difflib.SequenceMatcher; within the aligned region require >= MIN_MATCHED
matched words and a match ratio >= MIN_RATIO; report each replace/delete/
insert op of <= MAX_OP words that is flanked by matched words on both sides
(>= MIN_FLANK words in total) and changes at least one content word.

Scope: slides and quotes of Hawkins' OWN books (non-Hawkins entries are
excluded from the index). Explicit "as it says in <book>" attribution is not
parsed — any near-verbatim match counts (disclosed in DETECTORS.md).
Self-test: python3 tools/det_misquote.py --self-test
"""
import difflib
import re
import unicodedata
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import retrieval  # noqa: E402
import tokenizer  # noqa: E402

DETECTOR_ID = "B2-misquote"
WINDOW, STRIDE = 24, 12
MIN_SCORE = 0.20
TOP_K = 3
MIN_MATCHED, MIN_RATIO = 10, 0.85
MAX_OP, MIN_FLANK = 2, 3        # MIN_FLANK: matched words on EACH side
MAX_DELETE = 1                  # one spurious transcript word
SPELLING = 0.9                  # >= this char ratio = spelling variant
NEAR_FORM = 0.5                 # difflib char ratio for a replaced pair
_NUMBER_WORDS = frozenset("zero one two three four five six seven eight nine "
                          "ten eleven twelve twenty thirty forty fifty hundred "
                          "thousand".split())
FILLERS = frozenset("uh um uh-huh yeah okay ok so well like you know "
                    "and but oh huh hmm see right anyway quote".split())


def _norm(tok):
    return tok.lower().replace("\u2019", "'")


def _variant(ts, bs):
    """True for hyphenation, inflection and spelling variants."""
    def fold(w):
        w = unicodedata.normalize("NFKD", w)
        return re.sub(r"[^a-z]", "", w)
    x, y = fold(ts), fold(bs)
    if x == y:
        return True
    n = 0
    for c1, c2 in zip(x, y):
        if c1 != c2:
            break
        n += 1
    if n >= 4 and n >= 0.7 * min(len(x), len(y)):
        return True                   # capacity/capacities, realizing/realize
    return difflib.SequenceMatcher(None, x, y).ratio() >= SPELLING


def _content(words):
    return [w for w in words if w not in retrieval.STOPWORDS
            and w not in FILLERS]


def align(wtoks, ptoks):
    """Opcode list on normalized words, plus matched count / region."""
    a = [_norm(t.text) for t in wtoks]
    b = [_norm(t.text) for t in ptoks]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return a, b, sm.get_opcodes()


def _matched(wtoks, hit):
    a, b, ops = align(wtoks, tokenizer.tokenize(hit.text))
    return sum(i2 - i1 for tag, i1, i2, _j1, _j2 in ops if tag == "equal")


def _signals_for_window(text, wtoks, hit):
    ptoks = tokenizer.tokenize(hit.text)
    a, b, ops = align(wtoks, ptoks)
    eq = [op for op in ops if op[0] == "equal"]
    if not eq:
        return []
    first, last = ops.index(eq[0]), ops.index(eq[-1])
    region = ops[first:last + 1]
    matched = sum(i2 - i1 for tag, i1, i2, _j1, _j2 in region if tag == "equal")
    span = region[-1][2] - region[0][1]
    if matched < MIN_MATCHED or matched < MIN_RATIO * max(span, 1):
        return []
    out = []
    for k, (tag, i1, i2, j1, j2) in enumerate(region):
        if tag == "equal":
            continue
        if max(i2 - i1, j2 - j1) > MAX_OP:
            continue
        left = region[k - 1] if k > 0 else None
        right = region[k + 1] if k + 1 < len(region) else None
        if not (left and right and left[0] == "equal" and right[0] == "equal"):
            continue
        if min(left[2] - left[1], right[2] - right[1]) < MIN_FLANK:
            continue
        tw, bw = a[i1:i2], b[j1:j2]
        if any(w.isdigit() or w in _NUMBER_WORDS for w in tw + bw):
            continue                  # numeral formatting, not wording
        if tag == "insert":
            continue                  # speaker skipped book words: paraphrase
        if any("'" in w for w in tw + bw):
            continue                  # contractions / tense of auxiliaries
        if tag == "delete":
            if len(tw) > MAX_DELETE or not _content(tw):
                continue              # extra transcript filler
            gap = hit.text[ptoks[j1 - 1].end:ptoks[j1].start]
            if gap.strip():
                continue              # book has punctuation there: the
                                      # speaker added a word at a boundary
            why = "extra transcript word(s) inside a book quote"
        else:
            ts, bs = " ".join(tw), " ".join(bw)
            if not _content(tw + bw) or min(len(ts), len(bs)) < 4:
                continue
            if difflib.SequenceMatcher(None, ts, bs).ratio() < NEAR_FORM:
                continue              # different word, not a near-form
            if _variant(ts, bs) or _variant(" ".join(_content(tw)),
                                            " ".join(_content(bw))):
                continue              # hyphenation / inflection / spelling
            why = "near-form substitution inside a book quote"
        # spans: replace = the op itself; delete (extra transcript word) =
        # widened by one flanking word each side so the suggestion reads
        # as a correction ("no influence interest" -> "no interest")
        if tag == "delete":
            ti1, ti2, bj1, bj2 = i1 - 1, i2 + 1, j1 - 1, j1 + 1
        else:
            ti1, ti2, bj1, bj2 = i1, i2, j1, j2
        st, en = wtoks[ti1].start, wtoks[ti2 - 1].end
        sug = hit.text[ptoks[bj1].start:ptoks[bj2 - 1].end]
        # verbatim book context = the aligned book region
        rb1 = region[0][3]
        rb2 = region[-1][4]
        bstart = ptoks[rb1].start
        bend = ptoks[rb2 - 1].end
        out.append({
            "detector": DETECTOR_ID, "start": st, "end": en,
            "quoted": text[st:en], "suspected": sug,
            "note": "%s: transcript %r vs book %r inside a %d/%d-word "
                    "near-verbatim match (tf-idf %.2f)" % (
                        why, " ".join(a[i1:i2]), " ".join(b[j1:j2]),
                        matched, span, hit.score),
            "book_ref": {"slug": hit.slug,
                         "char_offset": hit.char_offset + bstart,
                         "quote": hit.text[bstart:bend]},
        })
    return out


def detect(text, index=None, exclude_slugs=(), **_ctx):
    if index is None:
        return []
    toks = tokenizer.tokenize(text)
    seen = set()
    out = []
    for i in range(0, max(len(toks) - WINDOW // 2, 1), STRIDE):
        wtoks = toks[i:i + WINDOW]
        if len(_content([_norm(t.text) for t in wtoks])) < 6:
            continue
        s, e = wtoks[0].start, wtoks[-1].end
        hits = [h for h in index.query(text[s:e], k=TOP_K + len(exclude_slugs) * 3)
                if h.score >= MIN_SCORE and h.slug not in exclude_slugs][:TOP_K]
        if not hits:
            continue
        # the passage the window aligns with best (most matched words)
        best = max(hits, key=lambda h: (_matched(wtoks, h), h.score))
        for sig in _signals_for_window(text, wtoks, best):
            key = (sig["start"], sig["end"])
            if key not in seen:
                seen.add(key)
                out.append(sig)
    out.sort(key=lambda x: x["start"])
    return out


_TOY_BOOKS = {
    "book_a": ("Noncontrolling: Spiritual purity has no interest in the "
               "personal lives of aspirants, or in clothing, dress, style, "
               "sex lives, economics, family patterns, lifestyles, or dietary "
               "habits.\n\nFree of force or intimidation: There is no "
               "brainwashing, adulation of leaders, training rituals."),
    "book_b": "Courage is the critical point of integrity at 200.\n\n" * 2,
    "book_c": ("The goal of his teaching was for his followers to reach "
               "Unconditional Love, and once it was reached the soul was "
               "safe forever."),
}


def toy_index():
    return retrieval.BookIndex(_TOY_BOOKS)


SELF_TEST = [
    ("So the teacher is non-controlling. Spiritual purity has no influence "
     "interest in the personal lives of aspirants, or in clothing, dress, "
     "style, sex lives, economics, family patterns.", 1),
    ("Okay. The goal of his teaching was for his followers to reach "
     "unquestionable love, and once it was reached the soul was safe.", 1),
    ("So the teacher is non-controlling. Spiritual purity has no interest "
     "in the personal lives of aspirants, or in clothing, dress, style, sex "
     "lives, economics, family patterns.", 0),
    ("We went to the store and bought some bread and milk and eggs for the "
     "breakfast tomorrow morning with the kids.", 0),
]


def self_test():
    ok = True
    idx = toy_index()
    for text, want in SELF_TEST:
        got = len(detect(text, index=idx))
        if got != want:
            print("FAIL: %r -> %d (want %d)" % (text[:40], got, want))
            ok = False
    print("%s self-test %s" % (DETECTOR_ID, "OK" if ok else "FAIL"))
    return ok


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print(__doc__)
