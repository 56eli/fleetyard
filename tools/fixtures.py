#!/usr/bin/env python3
"""Fixture sets (TASK-002 / M1). Stdlib only, no network, read-only corpus.

fixtures/confirmed/confirmed.json
    Hand-found CERTAIN transcript errors (STANDARDS finding records).
fixtures/clean/clean.json
    Clean-set sample from the book store, stored as POINTERS
    (slug, char_offset, length, sha256) — not as copied text. corpus/ is
    deliberately not in git (ERRATA-2026-09-24 §2) and this repo is public,
    so book text is materialized locally from the frozen corpus and verified
    by sha256 at load time.

Usage:
    python3 tools/fixtures.py build-clean   # (re)writes fixtures/clean/clean.json
    python3 tools/fixtures.py verify        # checks both sets against corpus/
"""
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loaders  # noqa: E402

CONFIRMED_PATH = os.path.join("fixtures", "confirmed", "confirmed.json")
CLEAN_PATH = os.path.join("fixtures", "clean", "clean.json")

REQUIRED_FIELDS = ("id", "transcript", "paragraph", "char_offset", "quoted",
                   "suspected", "evidence_class", "evidence", "detector",
                   "book_ref", "confidence", "status", "status_by")

CLEAN_FRACTIONS = (0.3, 0.5, 0.7)
CLEAN_MIN, CLEAN_MAX = 600, 1500
_SENT_START = re.compile(r"[.!?][\"'\u201d\u2019)]?\s+(?=[A-Z\u201c\"])")


def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _acceptable(passage):
    if "\n\n\n" in passage:            # layout gaps: headings / tables
        return False
    digits = sum(ch.isdigit() for ch in passage)
    if digits > 0.01 * len(passage):   # calibration lists, indices
        return False
    return len(loaders.split_sentences(passage)) >= 4


def pick_passage(text, start):
    """First acceptable sentence-aligned passage at/after `start`, or None."""
    pos = start
    while pos < len(text) - CLEAN_MIN:
        m = _SENT_START.search(text, pos)
        if not m:
            return None
        begin = m.end()
        end = begin
        for s in _SENT_START.finditer(text, begin):
            end = s.start() + 1
            if end - begin >= CLEAN_MIN:
                break
        passage = text[begin:end]
        if CLEAN_MIN <= len(passage) <= CLEAN_MAX and _acceptable(passage):
            return begin, passage
        pos = begin + 2000
    return None


def build_clean(books):
    """Deterministic clean-set pointers: 3 passages per Hawkins book."""
    records = []
    for slug in sorted(books):
        if slug in loaders.NON_HAWKINS_SLUGS:
            continue
        text = books[slug]
        seen = set()
        for frac in CLEAN_FRACTIONS:
            got = pick_passage(text, int(len(text) * frac))
            if not got or got[0] in seen:
                continue
            seen.add(got[0])
            begin, passage = got
            records.append({"id": "CL-%03d" % (len(records) + 1),
                            "slug": slug, "char_offset": begin,
                            "length": len(passage), "sha256": _sha(passage)})
    return records


def materialize_clean(records, books):
    """Pointer records -> list of (record, text); raises on sha mismatch."""
    out = []
    for r in records:
        text = books[r["slug"]][r["char_offset"]:r["char_offset"] + r["length"]]
        if _sha(text) != r["sha256"]:
            raise ValueError("clean fixture %s does not match corpus" % r["id"])
        out.append((r, text))
    return out


def verify_confirmed(records, books):
    """List of problems (empty = every record checks out against corpus)."""
    problems = []
    cache = {}
    for r in records:
        missing = [f for f in REQUIRED_FIELDS if f not in r]
        if missing:
            problems.append("%s: missing %s" % (r.get("id"), missing))
            continue
        if r["transcript"] not in cache:
            cache[r["transcript"]] = loaders.read_transcript(r["transcript"])
        t = cache[r["transcript"]]
        off = r["char_offset"]
        if t.text[off:off + len(r["quoted"])] != r["quoted"]:
            problems.append("%s: quote not at offset" % r["id"])
        if t.locate(off)[0] != r["paragraph"]:
            problems.append("%s: paragraph mismatch" % r["id"])
        b = r["book_ref"]
        if b is not None:
            src = books.get(b["slug"], "")
            if src[b["char_offset"]:b["char_offset"] + len(b["quote"])] != b["quote"]:
                problems.append("%s: book quote not at offset" % r["id"])
            if b["slug"] in loaders.NON_HAWKINS_SLUGS:
                problems.append("%s: book ref is not Hawkins" % r["id"])
        if r["evidence_class"] in ("b",) and b is None:
            problems.append("%s: class b needs a book_ref" % r["id"])
    return problems


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "verify"
    books = loaders.read_book_store()
    if cmd == "build-clean":
        recs = build_clean(books)
        os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)
        with open(CLEAN_PATH, "w", encoding="utf-8") as fh:
            json.dump(recs, fh, indent=1)
            fh.write("\n")
        print("wrote %s (%d passages)" % (CLEAN_PATH, len(recs)))
        return 0
    probs = verify_confirmed(load_json(CONFIRMED_PATH), books)
    materialize_clean(load_json(CLEAN_PATH), books)
    for p in probs:
        print(p)
    print("fixtures %s" % ("OK" if not probs else "FAIL"))
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
