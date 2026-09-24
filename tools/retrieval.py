#!/usr/bin/env python3
"""Book-passage retrieval — stdlib TF-IDF over the book store (SELF-M3a, M3).

    idx = BookIndex(books)                 # Hawkins books only by default
    idx.query("spiritual purity has no interest ...", k=5)
      -> [Hit(score, slug, char_offset, text), ...]

Passages: book text split on blank lines, merged into chunks of
MIN_CHARS..MAX_CHARS characters; each keeps its exact char offset in the
book (so a finding can cite slug + offset + verbatim quote). Scoring:
cosine similarity of sublinear-tf x smoothed-idf vectors, stopwords removed.
Non-Hawkins book-store entries (loaders.NON_HAWKINS_SLUGS) are excluded
unless include_non_hawkins=True — they are not Hawkins doctrine.

CLI: python3 tools/retrieval.py "query text" [k]
     python3 tools/retrieval.py --eval   # fixture book_ref recall
Stdlib only, no network, read-only.
"""
import collections
import math
import os
import re
import sys
from collections import namedtuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loaders  # noqa: E402
import tokenizer  # noqa: E402

MIN_CHARS, MAX_CHARS = 400, 1200
Hit = namedtuple("Hit", "score slug char_offset text")

STOPWORDS = frozenset("""
a about above after again all also am an and any are as at be because been
before being below between both but by can could did do does doing down
during each few for from further had has have having he her here hers him
his how i if in into is it its itself just me more most my no nor not now
of off on once only or other our ours out over own same she should so some
such than that the their theirs them then there these they this those
through to too under until up very was we were what when where which while
who whom why will with would you your yours
""".split())


def terms(text):
    return [w for w in tokenizer.words(text)
            if w not in STOPWORDS and not w.isdigit() and len(w) > 1]


def split_passages(text):
    """[(char_offset, passage_text)] — blank-line blocks merged to size."""
    blocks = []
    for m in re.finditer(r"\S(?:.*?\S)?(?=\s*\n\s*\n|\s*\Z)", text, re.S):
        blocks.append((m.start(), m.end()))
    out = []
    cur = None
    for s, e in blocks:
        if cur is None:
            cur = [s, e]
        elif cur[1] - cur[0] < MIN_CHARS and e - cur[0] <= MAX_CHARS:
            cur[1] = e
        else:
            out.append(tuple(cur))
            cur = [s, e]
    if cur is not None:
        out.append(tuple(cur))
    return [(s, text[s:e]) for s, e in out]


class BookIndex(object):
    def __init__(self, books, include_non_hawkins=False):
        self.passages = []          # (slug, offset, text)
        vecs = []
        df = collections.Counter()
        for slug in sorted(books):
            if slug in loaders.NON_HAWKINS_SLUGS and not include_non_hawkins:
                continue
            for off, ptext in split_passages(books[slug]):
                tf = collections.Counter(terms(ptext))
                if not tf:
                    continue
                self.passages.append((slug, off, ptext))
                vecs.append(tf)
                df.update(tf.keys())
        n = len(vecs)
        self.idf = {t: math.log((1 + n) / (1 + c)) + 1.0 for t, c in df.items()}
        self.postings = collections.defaultdict(list)
        self.norms = []
        for i, tf in enumerate(vecs):
            w = {t: (1 + math.log(c)) * self.idf[t] for t, c in tf.items()}
            norm = math.sqrt(sum(x * x for x in w.values()))
            self.norms.append(norm)
            for t, x in w.items():
                self.postings[t].append((i, x / norm))

    def query(self, text, k=5):
        tf = collections.Counter(t for t in terms(text) if t in self.idf)
        if not tf:
            return []
        q = {t: (1 + math.log(c)) * self.idf[t] for t, c in tf.items()}
        qn = math.sqrt(sum(x * x for x in q.values()))
        scores = collections.defaultdict(float)
        for t, x in q.items():
            for i, y in self.postings[t]:
                scores[i] += (x / qn) * y
        best = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
        return [Hit(round(s, 4), self.passages[i][0], self.passages[i][1],
                    self.passages[i][2]) for i, s in best]


def _norm_ws(s):
    return re.sub(r"\s+", " ", s).strip()


def eval_fixtures(index, confirmed, k=5):
    """For fixtures with a book_ref: is the cited quote inside a top-k hit
    when querying with the transcript's context (the quoted span plus the
    surrounding 300 chars)? Returns list of (fixture id, rank or None)."""
    out = []
    cache = {}
    for fx in confirmed:
        b = fx.get("book_ref")
        if not b:
            continue
        if fx["transcript"] not in cache:
            cache[fx["transcript"]] = loaders.read_transcript(fx["transcript"])
        t = cache[fx["transcript"]].text
        a = fx["char_offset"]
        ctx = t[max(0, a - 150):a + len(fx["quoted"]) + 150]
        quote = _norm_ws(b["quote"])
        rank = None
        for r, h in enumerate(index.query(ctx, k=k), 1):
            if quote in _norm_ws(h.text):
                rank = r
                break
        out.append((fx["id"], rank))
    return out


def main(argv):
    books = loaders.read_book_store()
    idx = BookIndex(books)
    if len(argv) > 1 and argv[1] == "--eval":
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import fixtures
        res = eval_fixtures(idx, fixtures.load_json(fixtures.CONFIRMED_PATH))
        for fid, rank in res:
            print("%s rank %s" % (fid, rank if rank else "miss (not in top 5)"))
        print("book_ref recall@5: %d/%d" % (sum(1 for _f, r in res if r),
                                            len(res)))
        return 0
    k = int(argv[2]) if len(argv) > 2 else 5
    for h in idx.query(argv[1], k=k):
        print("%.4f %s @%d | %s" % (h.score, h.slug, h.char_offset,
                                     _norm_ws(h.text)[:160]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
