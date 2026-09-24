#!/usr/bin/env python3
"""B1-contradiction — transcript claims vs book tables (TASK-005 / M3).

All reference values are PARSED FROM THE BOOK STORE at run time (anchored
on the table headers), never typed in by hand; each signal carries the book
slug + char offset + verbatim book quote it relies on.

Rules:
  happiness-percent : "<level> ... N% ... happy" where N differs from the
                      book table "Correlation of Levels of Consciousness and
                      the Rate of Happiness" (Reality, Spirituality and
                      Modern Man). Level named by word ("courage") or by log
                      ("level 500").
  polarity          : "above (200 | which) ... negative" or "below ...
                      positive" in a sentence about the 200 line — the books
                      state that energy goes positive at 200.
  level-log         : "<Level> [calibrates] [at] N" where N is not a log the
                      books give that level in either Map table.

Self-test: python3 tools/det_contradiction.py --self-test
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loaders  # noqa: E402

DETECTOR_ID = "B1-contradiction"

LEVEL_NAMES = ["Enlightenment", "Peace", "Joy", "Unconditional Love", "Love",
               "Reason", "Acceptance", "Willingness", "Neutrality", "Courage",
               "Pride", "Anger", "Desire", "Fear", "Grief", "Apathy", "Guilt",
               "Shame"]
_NAME_RX = "|".join(n.replace(" ", r"\s+") for n in LEVEL_NAMES)

HAPPY_SLUG, HAPPY_ANCHOR = "reality_spirituality_and_mode", "LEVEL LOG PERCENT"
MAP_SLUG, MAP_ANCHOR = "discovery_of_the_presence_of_g", "Level Log Emotion Process"
POLARITY_SLUG = "healing_and_recovery"
POLARITY_RX = r"At level 200, energy goes positive"


def _canon(name):
    return re.sub(r"\s+", " ", name).title()


def parse_tables(books):
    """Book-derived reference: happiness %, level logs, polarity quote."""
    ref = {"happy": {}, "happy_log": {}, "logs": {}, "cites": {}}
    text = books[HAPPY_SLUG]
    a = text.index(HAPPY_ANCHOR)
    seg = text[a:a + 900]
    for m in re.finditer(r"(%s)(?:,\s*hatred)?\s+([\d,]+(?:-[\d,]+)?)\s+(\d+)"
                         % _NAME_RX, seg):
        name = _canon(m.group(1))
        ref["happy"][name] = int(m.group(3))
        lo = int(m.group(2).split("-")[0].replace(",", ""))
        ref["happy_log"][lo] = name
        ref["logs"].setdefault(name, set()).add(lo)
        ref["cites"][("happy", name)] = {
            "slug": HAPPY_SLUG, "char_offset": a + m.start(),
            "quote": m.group(0)}
    text = books[MAP_SLUG]
    a = text.index(MAP_ANCHOR)
    seg = text[a:a + 2500]
    for m in re.finditer(r"\b(%s)\s+([\d,]+)(?:-[\d,]+)?\b" % _NAME_RX, seg):
        name = _canon(m.group(1))
        ref["logs"].setdefault(name, set()).add(int(m.group(2).replace(",", "")))
        ref["cites"].setdefault(("map", name), {
            "slug": MAP_SLUG, "char_offset": a + m.start(), "quote": m.group(0)})
    # Prose statements anywhere in the Hawkins books ("Enlightenment
    # calibrates at 600", "Acceptance calibrates at 380") are also accepted:
    # the books are the ground truth, even where they vary.
    for slug, text in books.items():
        if slug in loaders.NON_HAWKINS_SLUGS:
            continue
        for m in _BOOK_LOG.finditer(text):
            name = _canon(m.group(1) or m.group(3))
            n = int(m.group(2) or m.group(4))
            if n not in ref["logs"].setdefault(name, set()):
                ref["logs"][name].add(n)
                ref["cites"].setdefault(("prose", name, n), {
                    "slug": slug, "char_offset": m.start(),
                    "quote": m.group(0)})
    m = re.search(POLARITY_RX, books[POLARITY_SLUG])
    ref["cites"]["polarity"] = {"slug": POLARITY_SLUG,
                                "char_offset": m.start(), "quote": m.group(0)}
    return ref


NEAR = 60
_ABOVE_NEG = re.compile(r"\babove\s+(?:which|200|level\s+200|that)\b"
                        r"[^.?!]{0,60}?\bnegative\b", re.I)
_BELOW_POS = re.compile(r"\bbelow\s+(?:which|200|level\s+200|that)\b"
                        r"[^.?!]{0,60}?\bpositive\b", re.I)
_PCT = re.compile(r"(?<![\d.])(\d{1,3}(?:\.\d+)?)\s?(?:%|percent\b)")
_LEVEL_WORD = re.compile(r"\b(%s)\b" % _NAME_RX, re.I)
_LEVEL_NUM = re.compile(r"\blevel\s+(\d{2,4})\b", re.I)
_LEVEL_LOG = re.compile(r"\b(%s)[ \t]+(?:(?:calibrates|calibrated|is)[ \t]+)?"
                        r"(?:at[ \t]+)?(?:level[ \t]+)?(\d{1,4})\b"
                        r"(?![,.]?\d|\s*(?:%%|percent|-|\u2013|to\b))"
                        % _NAME_RX, re.I)
_BOOK_LOG = re.compile(r"\b(%s)\s+(?:(?:calibrates|calibrated|is)\s+)?at\s+"
                       r"(?:level\s+)?(\d{2,4})\b|\b(%s)\s+calibrates\s+"
                       r"(\d{2,4})\b" % (_NAME_RX, _NAME_RX), re.I)


def _signal(start, end, text, sug, note, cite):
    return {"detector": DETECTOR_ID, "start": start, "end": end,
            "quoted": text[start:end], "suspected": sug, "note": note,
            "book_ref": cite}


def detect(text, reference=None, **_ctx):
    if reference is None:
        return []
    ref = reference
    out = []
    sents = loaders.split_sentences(text)
    for i, s in enumerate(sents):
        prev = sents[i - 1] if i else None
        window_start = prev.char_offset if prev else s.char_offset
        window = text[window_start:s.char_offset + len(s.text)]
        low = s.text.lower()
        # happiness-percent: level named <= NEAR chars before the percent,
        # "happ" in the percent's own sentence
        if "happ" in low:
            for m in _PCT.finditer(s.text):
                near = s.text[max(0, m.start() - 40):m.end() + 40].lower()
                if "happ" not in near:
                    continue
                pos = s.char_offset + m.start() - window_start
                before = window[max(0, pos - NEAR):pos]
                names = [(x.end(), _canon(x.group(1)))
                         for x in _LEVEL_WORD.finditer(before)]
                names += [(x.end(), ref["happy_log"].get(int(x.group(1))))
                          for x in _LEVEL_NUM.finditer(before)]
                names = [n for n in names if n[1] in ref["happy"]]
                if not names:
                    continue
                name = max(names)[1]
                want = ref["happy"][name]
                if abs(float(m.group(1)) - want) > 0.5:
                    st = s.char_offset + m.start()
                    out.append(_signal(
                        st, s.char_offset + m.end(), text, "%d%%" % want,
                        "happiness-percent: book table gives %s = %d%%, "
                        "transcript says %s" % (name, want, m.group(0)),
                        ref["cites"][("happy", name)]))
        # polarity: "above which/200 ... negative" (or below ... positive)
        # with 200 in this or the two previous sentences
        ctx = " ".join(x.text for x in sents[max(0, i - 2):i + 1])
        if "200" in ctx:
            for rx, a, b in ((_ABOVE_NEG, "negative", "positive"),
                             (_BELOW_POS, "positive", "negative")):
                other = "below" if a == "negative" else "above"
                if rx.search(s.text) and not re.search(
                        r"\b%s\b" % other, low) and b not in low:
                    out.append(_signal(
                        s.char_offset, s.char_offset + len(s.text), text,
                        s.text.replace(a, b),
                        "polarity: the side %s the 200 line stated as %s; "
                        "books: energy goes positive at 200" % (
                            "above" if a == "negative" else "below", a),
                        ref["cites"]["polarity"]))
        # level-log
        for m in _LEVEL_LOG.finditer(s.text):
            name = _canon(m.group(1))
            n = int(m.group(2))
            pre = s.text[max(0, m.start() - 14):m.start()].lower()
            if re.search(r"\b(of|for)\s+$", pre):
                continue    # "Teacher of Enlightenment", "Prize for Peace"
            if name == "Love" and ("unconditional" in pre or
                                   re.search(r"\b(i|we|you|they)\s+$", pre)):
                continue
            if re.match(r"\s*(years?|percent|times)\b",
                        s.text[m.end():m.end() + 10], re.I):
                continue
            logs = ref["logs"].get(name)
            if not logs or n in logs or n < 10:
                continue
            want = sorted(logs)
            cite = ref["cites"].get(("map", name)) or \
                ref["cites"].get(("happy", name))
            st = s.char_offset + m.start()
            out.append(_signal(st, s.char_offset + m.end(), text,
                               "%s %s" % (name, "/".join(map(str, want))),
                               "level-log: books give %s = %s, transcript "
                               "says %d" % (name, want, n), cite))
    out.sort(key=lambda x: x["start"])
    return out


def _toy_reference():
    books = {
        HAPPY_SLUG: "x " + HAPPY_ANCHOR + " Peace 600 100 Joy 570 99 "
                    "Unconditional Love 540 96 Love 500 89 Acceptance 350 71 "
                    "Courage 200 55 Shame 20 1 end",
        MAP_SLUG: MAP_ANCHOR + " Peace 600 Bliss Joy 540 Serenity Love 500 "
                  "Courage 200 Shame 20",
        POLARITY_SLUG: "At level 200, energy goes positive, so the field.",
    }
    return parse_tables(books)


SELF_TEST = [
    ("By the level courage. 255% of people are happy.", 1),
    ("At level 500. 89% are happy. By the level courage. 55% are happy.", 0),
    ("Integrity at 200. Below which all the energies are negative. And above "
     "which all the energies are negative.", 1),
    ("Above 200 the energies are positive.", 0),
    ("Courage calibrates at 250.", 1),
    ("Joy 540. Joy 570. Unconditional love 540. Love 500.", 0),
]


def self_test():
    ok = True
    ref = _toy_reference()
    for text, want in SELF_TEST:
        got = len(detect(text, reference=ref))
        if got != want:
            print("FAIL: %r -> %d (want %d)" % (text[:40], got, want))
            ok = False
    print("%s self-test %s" % (DETECTOR_ID, "OK" if ok else "FAIL"))
    return ok


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(0 if self_test() else 1)
    print(__doc__)
