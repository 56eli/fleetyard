#!/usr/bin/env python3
"""C1-drop — dropped words against a book source (M4-q2, WORKER-2).

The M2/M5 audit named "drop-word" as a whole unmeasured error class: the v1
B2-misquote detector *skips* the alignment case where the BOOK has words the
transcript lacks (its source comment: "speaker skipped book words: paraphrase").
C1-drop is the inverse rule: inside an aligned near-verbatim book quote, report
the book words the transcript is missing, with the book citation that supplies
them. It is the drop-word detector for source-anchored text (slides/quotes).

Scope and honesty (disclosed, not hidden):
  * Only BOOK-ANCHORED drops are detected. A dropped word in ordinary
    conversation away from any quoted passage is invisible to this rule and
    stays unmeasured — the class is *narrowed*, not closed.
  * The rule never assigns CERTAIN; every output is a CANDIDATE-class raw
    signal carrying its own evidence (transcript span + book span + offsets).
  * Tuning discipline (LAW §9 / tools/HELD-OUT-SPLIT.json): `--tuning` mode
    may only read the TUNING transcripts; it refuses to run if a holdout
    transcript would be opened. Promotion runs are separate and read the
    holdout only.

Algorithm: slide WINDOW tokens (STRIDE) over the transcript, retrieve top-k
book passages (stdlib TF-IDF, Hawkins books only), align with
difflib.SequenceMatcher, keep the aligned region (first..last equal op) when
matched >= MIN_MATCHED and matched/span >= MIN_RATIO; report each `insert` op
(book words absent from the transcript) of <= MAX_DROP tokens flanked by
>= MIN_FLANK matched words on both sides, provided at least one dropped token
is a content word and none is a numeral.

Inputs come from the same frozen corpus loaders as the M5-R reducer
(`tools/m5r_reduce.py`: `load_transcripts`, `parse_book_store`) — lane-local
reuse, one implementation of the corpus identity.

Self-test:  python3 tools/det_dropword.py --self-test
Tuning run: python3 tools/det_dropword.py --tuning --split tools/HELD-OUT-SPLIT.json \
                --corpus corpus --out runs/m4-q2-dropword
Stdlib only, no network, read-only over the corpus.
"""
import argparse
import collections
import difflib
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m5r_reduce as m5r  # noqa: E402  (corpus loaders: transcripts + book store)

DETECTOR_ID = "C1-drop"
WINDOW, STRIDE = 24, 12
MIN_SCORE = 0.20
TOP_K = 3
MIN_MATCHED, MIN_RATIO = 10, 0.85
MAX_DROP = 2            # book words the transcript may be missing per op
MIN_FLANK = 3           # matched words required on EACH side of the drop
NUM_WORDS = frozenset("zero one two three four five six seven eight nine ten "
                      "eleven twelve twenty thirty forty fifty hundred thousand"
                      .split())
STOP = frozenset("""
a about above after again all also am an and any are as at be because been
before being below between both but by can could did do does doing down
during each few for from further had has have having he her here hers him
his how i if in into is it its itself just me more most my no nor not now
of off on once only or other our ours out over own same she should so some
such than that the their theirs them then there these they this those
through to too under until up very was we were what when where which while
who whom why will with would you your yours
""".split())

_WORD = re.compile(r"[^\W_]+(?:['\u2019\-][^\W_]+)*", re.UNICODE)


def tokenize(text):
    """[(text, start, end)] — same shape as the v1 tokenizer."""
    return [(m.group(0), m.start(), m.end()) for m in _WORD.finditer(text)]


def words(text):
    return [t[0].replace("\u2019", "'").lower() for t in tokenize(text)]


def terms(text):
    return [w for w in words(text) if w not in STOP and not w.isdigit() and len(w) > 1]


def split_passages(text):
    blocks = []
    for m in re.finditer(r"\S(?:.*?\S)?(?=\s*\n\s*\n|\s*\Z)", text, re.S):
        blocks.append((m.start(), m.end()))
    out, cur = [], None
    for s, e in blocks:
        if cur is None:
            cur = [s, e]
        elif cur[1] - cur[0] < 400 and e - cur[0] <= 1200:
            cur[1] = e
        else:
            out.append(tuple(cur))
            cur = [s, e]
    if cur is not None:
        out.append(tuple(cur))
    return [(s, text[s:e]) for s, e in out]


class BookIndex(object):
    """TF-IDF over Hawkins book passages (port of the v1 retrieval index)."""

    def __init__(self, books, non_hawkins=frozenset(["Be_as_you_are", "I_AM_THAT",
                                                     "Lamsa_bible", "ACIM_workbook"])):
        self.passages, vecs, df = [], [], collections.Counter()
        for slug in sorted(books):
            if slug in non_hawkins:
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
        for i, tf in enumerate(vecs):
            w = {t: (1 + math.log(c)) * self.idf[t] for t, c in tf.items()}
            norm = math.sqrt(sum(x * x for x in w.values())) or 1.0
            for t, x in w.items():
                self.postings[t].append((i, x / norm))

    def query(self, text, k=5):
        tf = collections.Counter(t for t in terms(text) if t in self.idf)
        if not tf:
            return []
        q = {t: (1 + math.log(c)) * self.idf[t] for t, c in tf.items()}
        qn = math.sqrt(sum(x * x for x in q.values())) or 1.0
        scores = collections.defaultdict(float)
        for t, x in q.items():
            for i, y in self.postings[t]:
                scores[i] += (x / qn) * y
        best = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
        return [(round(s, 4), self.passages[i][0], self.passages[i][1],
                 self.passages[i][2]) for i, s in best]


def _norm(w):
    return w.lower().replace("\u2019", "'")


def _content(ws):
    return [w for w in ws if w not in STOP and not w.isdigit()]


def _inside_book_quote(btext, pos):
    """True when pos falls inside an unbalanced opening curly quote (“ … ”)."""
    seg = btext[:pos]
    return seg.count("\u201c") > seg.count("\u201d")


def align(ttoks, btoks):
    a = [_norm(t[0]) for t in ttoks]
    b = [_norm(t[0]) for t in btoks]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return a, b, sm.get_opcodes()


def signals_for_window(text, ttoks, hit):
    """Report book words missing from the transcript (insert ops, a=transcript)."""
    score, slug, boff, btext = hit
    btoks = tokenize(btext)
    a, b, ops = align(ttoks, btoks)
    eq = [i for i, op in enumerate(ops) if op[0] == "equal"]
    if not eq:
        return []
    region = ops[eq[0]:eq[-1] + 1]
    matched = sum(i2 - i1 for tag, i1, i2, _j1, _j2 in region if tag == "equal")
    span = region[-1][2] - region[0][1]
    if matched < MIN_MATCHED or matched < MIN_RATIO * max(span, 1):
        return []
    out = []
    for k, (tag, i1, i2, j1, j2) in enumerate(region):
        if tag != "insert":              # a=transcript: insert = book words missing
            continue
        if (j2 - j1) > MAX_DROP or (j2 - j1) < 1:
            continue
        left = region[k - 1] if k > 0 else None
        right = region[k + 1] if k + 1 < len(region) else None
        if not (left and right and left[0] == "equal" and right[0] == "equal"):
            continue
        if min(left[2] - left[1], right[2] - right[1]) < MIN_FLANK:
            continue
        dropped = b[j1:j2]
        if not _content(dropped):
            continue                      # dropping "the" is not evidence
        if any(w.isdigit() or w in NUM_WORDS for w in dropped):
            continue                      # numeral formatting
        # transcript span = one flanking token each side, so the suggestion reads
        # as a correction; book span = the same window in book coordinates.
        ti1, ti2 = max(i1 - 1, 0), min(i2 + 1, len(a))
        bj1, bj2 = max(j1 - 1, 0), min(j2 + 1, len(b))
        if ti2 <= ti1 or bj2 <= bj1:
            continue
        if _inside_book_quote(btext, btoks[bj1][1]):
            continue                      # book dialogue the speaker need not read
        book_slice = btext[btoks[bj1][1]:btoks[bj2 - 1][2]]
        if any(c in book_slice for c in "()\u201c\u201d"):
            continue                      # editorial marks, not wording
        st = ttoks[ti1][1]
        en = ttoks[ti2 - 1][2]
        bstart = btoks[bj1][1]
        bend = btoks[bj2 - 1][2]
        out.append({
            "detector": DETECTOR_ID,
            "start": st, "end": en,
            "quoted": text[st:en],
            "suspected": btext[bstart:bend],
            "dropped_words": dropped,
            "note": "transcript is missing %r inside a %d/%d-word near-verbatim "
                    "book match (tf-idf %.2f)" % (" ".join(dropped), matched, span, score),
            "book_ref": {"slug": slug, "char_offset": boff + bstart,
                         "quote": btext[bstart:bend]},
        })
    return out


def detect(text, index, window=WINDOW, stride=STRIDE, min_score=MIN_SCORE, top_k=TOP_K):
    ttoks = tokenize(text)
    seen, out = set(), []
    for i in range(0, max(len(ttoks) - window // 2, 1), stride):
        wtoks = ttoks[i:i + window]
        if len(_content([_norm(t[0]) for t in wtoks])) < 6:
            continue
        s, e = wtoks[0][1], wtoks[-1][2]
        hits = [h for h in index.query(text[s:e], k=top_k) if h[0] >= min_score]
        if not hits:
            continue
        best = max(hits, key=lambda h: (sum(1 for x in align(wtoks, tokenize(h[3]))[2]
                                              if x[0] == "equal"), h[0]))
        for sig in signals_for_window(text, wtoks, best):
            key = (sig["start"], sig["end"])
            if key not in seen:
                seen.add(key)
                out.append(sig)
    out.sort(key=lambda x: (x["start"], x["end"]))
    return out


# ------------------------------------------------------------------ self-test

_TOY_BOOKS = {
    "book_drop": ("Spiritual purity has no interest in the personal lives of "
                  "aspirants, or in clothing, dress, style, sex lives, economics, "
                  "family patterns, lifestyles, or dietary habits.\n\n"
                  "Courage is the critical point of integrity at 200."),
    "book_other": "Nothing in this passage overlaps the toy transcript at all.\n\n",
}
_TOY_BAD = ("Spiritual purity has no interest in the personal lives, or in "
            "clothing, dress, style, sex lives, economics.")   # drops "of aspirants"
_TOY_GOOD = ("Spiritual purity has no interest in the personal lives of aspirants, "
             "or in clothing, dress, style, sex lives, economics.")


def self_test():
    idx = BookIndex(_TOY_BOOKS)
    assert detect(_TOY_BAD, idx), "a dropped word was not detected"
    hits = detect(_TOY_GOOD, idx)
    assert not hits, "a faithful quote produced a drop signal: %r" % hits
    sig = detect(_TOY_BAD, idx)[0]
    assert "aspirants" in sig["dropped_words"], sig["dropped_words"]
    assert sig["quoted"] and sig["suspected"] and sig["book_ref"]["quote"]
    assert sig["book_ref"]["slug"] == "book_drop"
    print("C1-drop self-test OK (detects a drop, ignores the faithful quote)")
    return 0


# ----------------------------------------------------------------- runner

def load_split(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def run_tuning(corpus_dir, split_path, out_dir, limit=None, quiet=False,
               offset=0, shard=None, shards=None, part_tag=None, which="tuning"):
    """Run the detector over the split's TUNING set (default) or its HOLDOUT set.

    `which="holdout"` is the one-shot evaluation mode (LAW §9 / PATTERNS §5):
    thresholds must already be frozen, the result is reported once, and any
    later tuning informed by it spends the holdout (a new split is then owed).

    Sharding exists because LAW §4A bounds a work quantum to <=240 s wall:
    `--shards N --shard i` runs one bounded part; parts merge at the end.
    """
    split = load_split(split_path)
    holdout = set(split["holdout"])
    overlap = sorted(set(split["tuning"]) & holdout)
    if overlap:
        raise SystemExit("C1-drop: split integrity violation — transcripts in both "
                         "tuning and holdout: %r" % overlap[:3])
    if which == "holdout":
        tuning = sorted(holdout)
    else:
        tuning = [n for n in split["tuning"] if n not in holdout]
    if shards:
        if not (1 <= shard <= shards):
            raise SystemExit("C1-drop: --shard must be within 1..--shards")
        chunk = len(tuning) // shards + (1 if len(tuning) % shards else 0)
        tuning = tuning[(shard - 1) * chunk: shard * chunk]
    if offset:
        tuning = tuning[offset:]
    if limit:
        tuning = tuning[:limit]
    if which != "holdout":
        assert not (set(tuning) & holdout), "holdout transcript in the tuning run"
    transcripts = m5r.load_transcripts(corpus_dir)
    missing = [n for n in tuning if n not in transcripts]
    if missing:
        raise SystemExit("C1-drop: tuning names not in corpus: %r" % missing[:3])
    books = m5r.parse_book_store(os.path.join(corpus_dir, "docdocgo", "html",
                                              "merged-book-texts_json_1.js"))
    index = BookIndex(books)
    per_file, total = {}, 0
    for n in tuning:
        sigs = detect(transcripts[n], index)
        per_file[n] = sigs
        total += len(sigs)
        if not quiet and (len(per_file) % 25 == 0):
            print("  … %d/%d transcripts, %d signals" % (len(per_file), len(tuning), total))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        target = ("part-%s.json" % part_tag) if part_tag else "signals.json"
        with open(os.path.join(out_dir, target), "w", encoding="utf-8") as fh:
            json.dump(per_file, fh, ensure_ascii=False, sort_keys=True, indent=1)
        prov = {
            "run_utc": _utc(),
            "detector": DETECTOR_ID,
            "detector_sha256": m5r.sha256_file(os.path.abspath(__file__)),
            "params": {"window": WINDOW, "stride": STRIDE, "min_score": MIN_SCORE,
                       "top_k": TOP_K, "min_matched": MIN_MATCHED,
                       "min_ratio": MIN_RATIO, "max_drop": MAX_DROP,
                       "min_flank": MIN_FLANK},
            "inputs": {
                "corpus_dir": corpus_dir,
                "corpus_zip_sha256": "3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db",
                "split_file": split_path,
                "split_corpus_files_sha256": split["corpus_files_sha256"],
                "split_salt": split["salt"],
                "transcripts_read": tuning,
                "set": which,
                "holdout_reads": tuning if which == "holdout" else [],
                "holdout_enforced": which != "holdout",
                "holdout_consumed": which == "holdout",
                "shard": ({"shard": shard, "shards": shards} if shards else None),
            },
            "outputs": {"signals_per_transcript": {n: len(v) for n, v in sorted(per_file.items())},
                        "signals_total": total,
                        "transcripts": len(tuning)},
            "status": "CANDIDATE-class raw signals, unreviewed; PROVISIONAL-UNGATED "
                      "(no ORCH-2). Not a rate: precision unmeasured (holdout run pending).",
        }
        pname = ("part-%s.PROVENANCE.json" % part_tag) if part_tag else "PROVENANCE.json"
        prov["outputs"]["signals_file"] = target
        with open(os.path.join(out_dir, pname), "w", encoding="utf-8") as fh:
            json.dump(prov, fh, indent=1, sort_keys=True)
            fh.write("\n")
    return per_file, total


def merge_parts(out_dir):
    """Merge shard parts -> signals.json + MERGE-PROVENANCE.json (deterministic)."""
    parts = sorted(f for f in os.listdir(out_dir)
                   if f.startswith("part-") and f.endswith(".json")
                   and "PROVENANCE" not in f)
    merged, per_part = {}, []
    for f in parts:
        data = json.load(open(os.path.join(out_dir, f), encoding="utf-8"))
        dupes = sorted(set(data) & set(merged))
        if dupes:
            raise SystemExit("C1-drop: transcripts in two parts: %r" % dupes[:3])
        merged.update(data)
        per_part.append({"part": f, "transcripts": len(data),
                         "signals": sum(len(v) for v in data.values()),
                         "sha256": m5r.sha256_file(os.path.join(out_dir, f))})
    with open(os.path.join(out_dir, "signals.json"), "w", encoding="utf-8") as fh:
        json.dump(merged, fh, ensure_ascii=False, sort_keys=True, indent=1)
    meta = {"parts": per_part, "transcripts": len(merged),
            "signals_total": sum(len(v) for v in merged.values()),
            "signals_json_sha256": m5r.sha256_file(os.path.join(out_dir, "signals.json")),
            "merge_utc": _utc(),
            "status": "CANDIDATE-class raw signals, unreviewed; PROVISIONAL-UNGATED"}
    with open(os.path.join(out_dir, "MERGE-PROVENANCE.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return meta


def _utc():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tuning", action="store_true")
    ap.add_argument("--split", default="tools/HELD-OUT-SPLIT.json")
    ap.add_argument("--corpus", default="corpus")
    ap.add_argument("--out")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--shard", type=int)
    ap.add_argument("--shards", type=int)
    ap.add_argument("--part-tag")
    ap.add_argument("--set", choices=("tuning", "holdout"), default="tuning")
    ap.add_argument("--merge", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--transcript")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if a.transcript:
        books = m5r.parse_book_store(os.path.join(a.corpus, "docdocgo", "html",
                                                  "merged-book-texts_json_1.js"))
        text = m5r.load_transcripts(a.corpus)[os.path.basename(a.transcript)]
        for s in detect(text, BookIndex(books)):
            print(json.dumps(s, ensure_ascii=False))
        return 0
    if a.merge:
        meta = merge_parts(a.out)
        print("C1-drop merge: %d parts, %d transcripts, %d signals"
              % (len(meta["parts"]), meta["transcripts"], meta["signals_total"]))
        return 0
    if a.tuning:
        per_file, total = run_tuning(a.corpus, a.split, a.out, limit=a.limit,
                                     offset=a.offset, shard=a.shard, shards=a.shards,
                                     part_tag=a.part_tag, which=a.set)
        print("C1-drop %s run: %d transcripts, %d signals" % (a.set, len(per_file), total))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
