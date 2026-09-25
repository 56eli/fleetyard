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
                       Korean code-switch (TASK-010): an English word with a
                       Korean case particle attached ("yes나", "no를",
                       "archangel이") INSIDE Korean text is normal Korean
                       grammar, not garble, and is not flagged. The same
                       token shape in English context ("My hand은 You saw")
                       is still flagged.
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
# Korean particles that attach to a (loan)word: case/topic/conjunctive
KO_PARTICLES = frozenset(
    "이 가 은 는 을 를 의 에 와 과 도 나 로 만 랑 이나 으로 에서 에게 "
    "한테 까지 부터 처럼 보다 이랑 이라고 라고 라는".split())
KO_CONTEXT = 3          # tokens each side inspected
KO_CONTEXT_MIN = 2      # Hangul tokens needed among them
_LATIN_HANGUL = re.compile(r"^([A-Za-z][A-Za-z'\-]*)([\uac00-\ud7a3]{1,3})$")


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


def _hangul(tok):
    return any(0xAC00 <= ord(ch) <= 0xD7A3 for ch in tok)


def is_korean_codeswitch(toks, i):
    """English word + Korean particle, embedded in Korean text."""
    m = _LATIN_HANGUL.match(toks[i].text)
    if not m or m.group(2) not in KO_PARTICLES:
        return False
    near = toks[max(0, i - KO_CONTEXT):i] + toks[i + 1:i + 1 + KO_CONTEXT]
    return sum(1 for t in near if _hangul(t.text)) >= KO_CONTEXT_MIN


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
    for i in range(len(toks)):
        if kinds[i] == "M" and is_korean_codeswitch(toks, i):
            kinds[i] = "O"      # part of the surrounding Korean run
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
    # TASK-010 negative: Sedona Dec 2008 Part 2 @9671 interpreter Korean
    ("\uadf8\ub798\uc11c \uc9c4\uc815\ud55c \uc2a4\uc2b9\uc740 \uc790\uc720\ub97c "
     "\ud5c8\ub77d\ud558\uace0, \uadf8\uc5d0\uac8c yes\ub098 no\ub97c \uc120\ud0dd\ud560 "
     "\uae30\ud68c\ub97c \uc8fc\uace0,", 0),
    # same token shape in English context is still garble
    ("didn't answer. No, never. My hand\uc740 You saw stop complaining", 1),
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
