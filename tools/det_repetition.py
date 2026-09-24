#!/usr/bin/env python3
"""A1-repetition — ASR repetition-loop detector (TASK-004 / M2, family A).

Flags a word sequence of k tokens (k = 1..MAX_K) repeated back-to-back:
  k == 1      : >= 8 repeats   ("No. No. No. ..." x26)
  k in 2..3   : >= 5 repeats
  k >= 4      : >= 3 repeats   ("It is discovered that to be loved." x5)
Case and punctuation are ignored when comparing, so both sentence loops and
unpunctuated loops ("you take it back upon yourself you take it ...") are
caught. The span runs from the first repeat to the end of the last; the
suspected intended text is a single occurrence.

Stdlib only, no I/O beyond what the caller passes in.
Self-test: python3 tools/det_repetition.py --self-test
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokenizer  # noqa: E402

DETECTOR_ID = "A1-repetition"
MAX_K = 12


def min_repeats(k):
    if k == 1:
        return 8
    if k <= 3:
        return 5
    return 3


def detect(text, **_ctx):
    toks = tokenizer.tokenize(text)
    norm = [t.text.lower().replace("\u2019", "'") for t in toks]
    n = len(norm)
    out = []
    i = 0
    while i < n:
        best = None
        for k in range(1, MAX_K + 1):
            if i + 2 * k > n:
                break
            unit = norm[i:i + k]
            reps = 1
            while norm[i + reps * k:i + (reps + 1) * k] == unit:
                reps += 1
            if reps >= min_repeats(k):
                cover = reps * k
                if best is None or cover > best[0]:
                    best = (cover, k, reps)
        if best is None:
            i += 1
            continue
        cover, k, reps = best
        start, end = toks[i].start, toks[i + cover - 1].end
        # keep trailing sentence punctuation of the last repeat in the quote
        while end < len(text) and text[end] in ".!?,":
            end += 1
        one_end = toks[i + k - 1].end
        while one_end < len(text) and text[one_end] in ".!?,":
            one_end += 1
        out.append({
            "detector": DETECTOR_ID, "start": start, "end": end,
            "quoted": text[start:end],
            "suspected": text[start:one_end],
            "note": "%d-token unit repeated %d times back-to-back" % (k, reps),
        })
        i += cover
    return out


SELF_TEST = [
    ("Yes. " + "No. " * 26 + "Accusations.", 1),
    ("It is discovered that to be loved. " * 5 + "It is discovered.", 1),
    ("you take it back upon yourself " * 22, 1),
    ("Okay. Okay. Okay. Purr, purr, purr, purr, purr, purr.", 0),
    ("Where the 15% calibrate. Where the 15% calibrate. Over 200.", 0),
]


def self_test():
    ok = True
    for text, want in SELF_TEST:
        got = len(detect(text))
        if got != want:
            print("FAIL: %r -> %d (want %d)" % (text[:40], got, want))
            ok = False
    print("%s self-test %s" % (DETECTOR_ID, "OK" if ok else "FAIL"))
    return ok


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print(__doc__)
