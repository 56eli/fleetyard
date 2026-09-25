#!/usr/bin/env python3
"""C2-format — speaker/format artifacts (M4-q3, WORKER-2).

The M2 disposition carried two unbuilt classes: "drop-word" and "speaker/format".
M4-q2 built the drop-word rule for book-anchored drops. This tool covers the
mechanically checkable half of speaker/format: **format/parsing artifacts** in
the frozen transcripts.

What this tool DOES claim (all rules mechanical, byte-checkable):
  R1 glued period    — "word.Next" (missing space after a sentence period),
                       excluding abbreviations (Ph.D, i.e, a.m, Dr., initials…)
  R2 repeated punct  — runs of 2+ identical [!?*;,] marks ("****", ",,")
  R3 long dot run    — 4+ consecutive dots (malformed ellipsis)
  R4 underscore run  — literal "_" runs in running text
  R5 space before ,  — "word ," (spurious space before a comma)
  R6 spaced period   — "word . word" (spurious space around a sentence period)
  R7 glued comma     — "word,Word" (missing space after a comma)

What this tool does NOT claim (measured, then disclosed — see the census in
runs/m4-q3-format/README.md):
  * **Speaker attribution is out of mechanical scope.** A corpus census found
    zero speaker labels ("Q:", "A:", "Speaker 1"), zero bracketed stage
    directions, zero HTML/JS residue and zero control characters across all 230
    transcripts: the corpus format encodes no speaker turns at all. Whether a
    passage is mis-attributed to the speaker rather than a questioner is a
    *reading* judgment; it stays unmeasured here and is recorded as an explicit
    M6 limitation.
  * Camel-glue ("veryCapitalist") was measured (35 hits / 18 files) but is
    dominated by legitimate proper nouns (MacArthur, YouTube), so it is NOT a
    rule; the census is recorded instead of a noisy detector.

Outputs are CANDIDATE-class raw signals (each with its rule id, byte offsets and
the verbatim excerpt). A format artifact is mechanically demonstrable; whether
it *changed meaning* is not, and is not claimed.

Tuning discipline: `--tuning` reads only tools/HELD-OUT-SPLIT.json tuning
transcripts and refuses a split whose tuning/holdout overlap.

Self-test: python3 tools/det_format.py --self-test
Run:       python3 tools/det_format.py --tuning --split tools/HELD-OUT-SPLIT.json \
                --corpus corpus --out runs/m4-q3-format
Stdlib only, no network, read-only over the corpus.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m5r_reduce as m5r  # noqa: E402

DETECTOR_ID = "C2-format"
EXCERPT = 60            # chars of context on each side in the signal excerpt

# abbreviations whose internal period is legitimate (lower-cased, no trailing dot)
ABBREV = frozenset("""
ph.d m.d b.a m.a d.d.s r.n l.p.n d.o jr sr st mr mrs ms dr vs etc no inc ltd
co corp dept est fig vol pp ed eds al i.e e.g a.m p.m u.s u.k n.y n.j
""".split())


def _signals_for_rule(rule, text, start, end, note, suggested=None):
    s = max(0, start - EXCERPT)
    e = min(len(text), end + EXCERPT)
    return {"detector": DETECTOR_ID, "rule": rule, "start": start, "end": end,
            "quoted": text[start:end], "excerpt": text[s:e],
            "note": note, "suggested": suggested}


ABBREV_FLAT = frozenset(x.replace(".", "") for x in ABBREV)


def _abbrev_before(text, dot):
    """Is the period at index `dot` part of an abbreviation/initial/acronym?

    The whole letter/dot token containing the period is examined, so "Ph.D"
    (dot inside the abbreviation) is recognised, while "world.Next" is not.
    """
    i = dot
    while i - 1 >= 0 and (text[i - 1].isalpha() or text[i - 1] == "."):
        i -= 1
    j = dot + 1
    while j < len(text) and (text[j].isalpha() or text[j] == "."):
        j += 1
    token = text[i:j]
    parts = [p for p in token.split(".") if p]
    core = token.replace(".", "").lower()
    if core in ABBREV_FLAT:
        return True                      # phd, md, ie, eg, am, pm, us, dr, vs, etc
    if parts and all(len(p) == 1 for p in parts):
        return True                      # initials: "T.S", "J"
    if len(core) <= 3 and core.isupper():
        return True                      # short acronyms: "US", "MD", "NY"
    if nx_isdigit(text, dot + 1):
        return True                      # numbered abbreviations
    return False


def nx_isdigit(text, i):
    return i < len(text) and text[i].isdigit()


def detect(text):
    out = []
    # R1 glued period: letter . letter  with no space after the period
    for m in re.finditer(r"[A-Za-z]\.[A-Za-z]", text):
        if _abbrev_before(text, m.start() + 1):
            continue
        out.append(_signals_for_rule(
            "R1-glued-period", text, m.start(), m.end(),
            "missing space after a sentence period: %r" % m.group(0),
            suggested=m.group(0)[:1] + ". " + m.group(0)[2:]))
    # R2 repeated punctuation runs
    for m in re.finditer(r"([!?*;,])\1+", text):
        out.append(_signals_for_rule(
            "R2-repeated-punct", text, m.start(), m.end(),
            "repeated punctuation run (%d x %r)" % (len(m.group(0)), m.group(1)[0]),
            suggested="" if m.group(1) == "*" else m.group(1)))
    # R3 4+ dots
    for m in re.finditer(r"\.{4,}", text):
        out.append(_signals_for_rule(
            "R3-long-dot-run", text, m.start(), m.end(),
            "dot run of %d (malformed ellipsis)" % len(m.group(0)),
            suggested="..."))
    # R4 underscore runs
    for m in re.finditer(r"_{1,}", text):
        out.append(_signals_for_rule(
            "R4-underscore-run", text, m.start(), m.end(),
            "underscore run in running text", suggested=""))
    # R5 space before comma
    for m in re.finditer(r"\w\s+,", text):
        out.append(_signals_for_rule(
            "R5-space-before-comma", text, m.start(), m.end(),
            "space before a comma", suggested=m.group(0)[0] + ","))
    # R6 spaced period between words: "word . word"
    for m in re.finditer(r"[a-z]\s+\.\s+(?=[a-z])", text):
        out.append(_signals_for_rule(
            "R6-spaced-period", text, m.start(), m.end(),
            "space around a sentence period"))
    # R7 glued comma: letter , letter
    for m in re.finditer(r"[a-z],[A-Za-z]", text):
        out.append(_signals_for_rule(
            "R7-glued-comma", text, m.start(), m.end(),
            "missing space after a comma", suggested=m.group(0)[0] + ", " + m.group(0)[2]))
    out.sort(key=lambda s: (s["start"], s["rule"]))
    return out


# ------------------------------------------------------------------ self-test

_TOY = ("The truth is you see the world as you are.You are not the world. "
        "It is very**** simple , indeed. He has a Ph.D. from NAU and lives "
        "on i.e. Wall Street. Wait....._What do you mean? ")
_TOY_CLEAN = ("The truth is you see the world as you are. You are not the world. "
              "He has a Ph.D. from NAU. Wait... What do you mean? ")


def self_test():
    hits = detect(_TOY)
    rules = {h["rule"] for h in hits}
    for want in ("R1-glued-period", "R2-repeated-punct", "R3-long-dot-run",
                 "R4-underscore-run", "R5-space-before-comma"):
        assert want in rules, "rule %s did not fire: %r" % (want, sorted(rules))
    assert not [h for h in hits if h["rule"] == "R1-glued-period"
                and "Ph.D" in h["quoted"]], "abbreviation Ph.D wrongly flagged"
    clean = detect(_TOY_CLEAN)
    assert not clean, "clean control produced signals: %r" % clean
    print("C2-format self-test OK (%d signals on the toy, 0 on the clean control)"
          % len(hits))
    return 0


# -------------------------------------------------------------------- runner

def run_tuning(corpus_dir, split_path, out_dir, part_tag=None, which="tuning"):
    """Run over the split's tuning set (default) or its holdout set (one-shot)."""
    split = json.load(open(split_path, encoding="utf-8"))
    overlap = sorted(set(split["tuning"]) & set(split["holdout"]))
    if overlap:
        raise SystemExit("C2-format: split integrity violation: %r" % overlap[:3])
    if which == "holdout":
        tuning = sorted(set(split["holdout"]))
    else:
        tuning = [n for n in split["tuning"] if n not in set(split["holdout"])]
    transcripts = m5r.load_transcripts(corpus_dir)
    missing = [n for n in tuning if n not in transcripts]
    if missing:
        raise SystemExit("C2-format: tuning names not in corpus: %r" % missing[:3])
    per_file, total = {}, 0
    for n in tuning:
        sigs = detect(transcripts[n])
        per_file[n] = sigs
        total += len(sigs)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        target = ("part-%s.json" % part_tag) if part_tag else "signals.json"
        with open(os.path.join(out_dir, target), "w", encoding="utf-8") as fh:
            json.dump(per_file, fh, ensure_ascii=False, sort_keys=True, indent=1)
        prov = {
            "run_utc": _utc(),
            "detector": DETECTOR_ID,
            "detector_sha256": m5r.sha256_file(os.path.abspath(__file__)),
            "rules": ["R1-glued-period", "R2-repeated-punct", "R3-long-dot-run",
                      "R4-underscore-run", "R5-space-before-comma",
                      "R6-spaced-period", "R7-glued-comma"],
            "inputs": {"corpus_dir": corpus_dir,
                       "corpus_zip_sha256": "3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db",
                       "split_file": split_path,
                       "split_corpus_files_sha256": split["corpus_files_sha256"],
                       "transcripts_read": tuning, "set": which,
                       "holdout_reads": tuning if which == "holdout" else [],
                       "holdout_enforced": which != "holdout",
                       "holdout_consumed": which == "holdout"},
            "outputs": {"signals_file": target, "signals_total": total,
                        "per_rule": _per_rule(per_file),
                        "transcripts": len(tuning)},
            "status": "CANDIDATE-class raw signals, unreviewed; PROVISIONAL-UNGATED",
            "not_claimed": "speaker attribution (no speaker labels exist in this corpus "
                           "format) and meaning impact — see runs/m4-q3-format/README.md",
        }
        pname = ("part-%s.PROVENANCE.json" % part_tag) if part_tag else "PROVENANCE.json"
        with open(os.path.join(out_dir, pname), "w", encoding="utf-8") as fh:
            json.dump(prov, fh, indent=1, sort_keys=True)
            fh.write("\n")
    return per_file, total


def _per_rule(per_file):
    counts = {}
    for sigs in per_file.values():
        for s in sigs:
            counts[s["rule"]] = counts.get(s["rule"], 0) + 1
    return dict(sorted(counts.items()))


def _utc():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tuning", action="store_true")
    ap.add_argument("--split", default="tools/HELD-OUT-SPLIT.json")
    ap.add_argument("--corpus", default="corpus")
    ap.add_argument("--out")
    ap.add_argument("--part-tag")
    ap.add_argument("--set", choices=("tuning", "holdout"), default="tuning")
    ap.add_argument("--transcript")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if a.transcript:
        text = m5r.load_transcripts(a.corpus)[os.path.basename(a.transcript)]
        for s in detect(text):
            print(json.dumps(s, ensure_ascii=False))
        return 0
    if a.tuning:
        per_file, total = run_tuning(a.corpus, a.split, a.out, part_tag=a.part_tag,
                                     which=a.set)
        print("C2-format %s run: %d transcripts, %d signals %s"
              % (a.set, len(per_file), total, _per_rule(per_file)))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
