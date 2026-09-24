#!/usr/bin/env python3
"""A2-nonsense — senseless-span detector (TASK-004 / M2, family A).

Rules (each yields one signal):
  impossible-percent : a percentage above 100 ("255% of people are happy").
  script-mix         : a token mixing Latin letters with another script
                       ("spirit持"), a Latin token carrying Vietnamese-only
                       letters, or a SHORT non-Latin run (< MIN_FOREIGN_RUN
                       tokens) wedged in English text — ASR hallucination.
                       Long non-Latin runs (e.g. the inline Korean
                       interpretation in Sedona Dec 2008) are NOT flagged
                       here: they are a real second language, not garble.
  replacement-char   : U+FFFD (undecodable bytes in the source file).

Stdlib only. Self-test: python3 tools/det_nonsense.py --self-test
"""
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokenizer  # noqa: E402

DETECTOR_ID = "A2-nonsense"
MIN_FOREIGN_RUN = 4
_PCT = re.compile(r"(?<![\d.])(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s?(%|percent\b)")
_VIET = set("ăâđêôơưĂÂĐÊÔƠƯ")


def _script(ch):
    """'L' Latin letter, 'O' other-script letter, None for non-letters."""
    if not ch.isalpha():
        return None
    if ord(ch) < 0x250:
        return "L"
    name = unicodedata.name(ch, "")
    if name.startswith("LATIN"):
        return "L"
    return "O"


def _is_viet(tok):
    return any(ch in _VIET for ch in tok) or any(
        0x1EA0 <= ord(ch) <= 0x1EF9 for ch in tok)


def detect(text, **_ctx):
    out = []
    for m in _PCT.finditer(text):
        val = float(m.group(1).replace(",", ""))
        if val > 100:
            out.append({"detector": DETECTOR_ID, "start": m.start(),
                        "end": m.end(), "quoted": m.group(0),
                        "suspected": None,
                        "note": "impossible-percent: %s > 100" % m.group(1)})
    toks = tokenizer.tokenize(text)
    kinds = []
    for t in toks:
        s = {_script(ch) for ch in t.text} - {None}
        kinds.append("M" if s == {"L", "O"} else ("O" if s == {"O"} else "L"))
    i = 0
    while i < len(toks):
        t = toks[i]
        if kinds[i] == "M" or (kinds[i] == "L" and _is_viet(t.text)):
            out.append({"detector": DETECTOR_ID, "start": t.start,
                        "end": t.end, "quoted": t.text, "suspected": None,
                        "note": "script-mix: mixed/foreign letters in token"})
            i += 1
            continue
        if kinds[i] == "O":
            j = i
            while j < len(toks) and kinds[j] == "O":
                j += 1
            if j - i < MIN_FOREIGN_RUN:
                s, e = toks[i].start, toks[j - 1].end
                out.append({"detector": DETECTOR_ID, "start": s, "end": e,
                            "quoted": text[s:e], "suspected": None,
                            "note": "script-mix: short non-Latin run (%d "
                                    "tokens) inside English" % (j - i)})
            i = j
            continue
        i += 1
    for m in re.finditer("\ufffd+", text):
        out.append({"detector": DETECTOR_ID, "start": m.start(),
                    "end": m.end(), "quoted": m.group(0), "suspected": None,
                    "note": "replacement-char: undecodable source bytes"})
    out.sort(key=lambda s: s["start"])
    return out


SELF_TEST = [
    ("By the level courage. 255% of people are happy.", 1),
    ("At level 500, 89% are happy; 100 percent at 600.", 0),
    ("are met. kennt \u0111\u1ed9ng ether ..... ani , ting \u6743 ... are", 2),
    ("spirit\u6301 is here", 1),
    ("Truth. \uc9c4\uc2e4\uc740 \uc0ac\ubb3c\uc758 \ubcf8\uc9c8\uacfc "
     "\uad00\uacc4\ud558\uace0 \uac70\uc9d3\uc740 \ud604\uc0c1\uc785\ub2c8\ub2e4.", 0),
    ("caf\u00e9 na\u00efve r\u00e9sum\u00e9", 0),
    ("bad \ufffd byte", 1),
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
