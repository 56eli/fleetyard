#!/usr/bin/env python3
"""Run family-A detectors and emit STANDARDS finding records (TASK-004).

    python3 tools/run_detectors.py corpus/docdocgo/overlays/X.txt [...]
    python3 tools/run_detectors.py --all [--out findings.json]
    python3 tools/run_detectors.py --eval

Findings go to stdout, or to --out (the only file this tool writes).
Reads only corpus/** (plus the fixtures for --eval). Stdlib only.

Confidence assignment (STANDARDS): signals from different detectors whose
spans overlap are merged; >= 2 distinct detectors = HIGH CONFIDENCE, one =
CANDIDATE. CERTAIN is never assigned automatically — it needs a proof leg
(a/b/c) checked by a finding pass. Every record is status "open".

--eval prints, per detector: fixture recall on fixtures/confirmed (a fixture
is hit when a signal overlaps its quoted span; hits on confusion-list
entries seeded FROM that fixture are counted separately, because they are
not independent evidence), and false positives on fixtures/clean (the
confusion lexicon is rebuilt WITHOUT the passage's own book, so a clean
passage cannot vouch for itself).
"""
import argparse
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import det_confusion  # noqa: E402
import det_nonsense  # noqa: E402
import det_repetition  # noqa: E402
import fixtures  # noqa: E402
import loaders  # noqa: E402
import tokenizer  # noqa: E402

DETECTORS = [det_repetition, det_nonsense, det_confusion]


def hawkins_books(books):
    return {k: v for k, v in books.items()
            if k not in loaders.NON_HAWKINS_SLUGS}


def transcript_frequencies(paths):
    freq = collections.Counter()
    for p in paths:
        freq.update(tokenizer.words(loaders.read_transcript(p).text))
    return freq


def signals(text, lexicon=None, transcript_freq=None, detectors=DETECTORS):
    out = []
    for d in detectors:
        out.extend(d.detect(text, lexicon=lexicon,
                            transcript_freq=transcript_freq))
    out.sort(key=lambda s: (s["start"], s["end"]))
    return out


def merge(sigs):
    """Group signals with overlapping spans."""
    groups = []
    for s in sigs:
        if groups and s["start"] < groups[-1]["end"]:
            g = groups[-1]
            g["end"] = max(g["end"], s["end"])
            g["signals"].append(s)
        else:
            groups.append({"start": s["start"], "end": s["end"],
                           "signals": [s]})
    return groups


def records(transcript, lexicon=None, transcript_freq=None):
    text = transcript.text
    out = []
    for g in merge(signals(text, lexicon, transcript_freq)):
        dets = sorted({s["detector"] for s in g["signals"]})
        para, _ = transcript.locate(g["start"])
        sugg = [s["suspected"] for s in g["signals"] if s["suspected"]]
        out.append({
            "transcript_path": transcript.path.replace(os.sep, "/"),
            "location": {"paragraph": para, "char_offset": g["start"]},
            "quoted_text": text[g["start"]:g["end"]],
            "suspected_intended_text": sugg[0] if sugg else None,
            "evidence_class": "signals: " + "; ".join(
                "%s (%s)" % (s["detector"], s["note"]) for s in g["signals"]),
            "detector_id": "+".join(dets),
            "book_reference": None,
            "confidence": "HIGH CONFIDENCE" if len(dets) >= 2 else "CANDIDATE",
            "status": "open",
            "status_by": "run_detectors (automatic, unreviewed)",
        })
    return out


def evaluate(books, confirmed, clean):
    """Per-detector fixture recall + clean-set false positives."""
    hb = hawkins_books(books)
    counts = det_confusion.book_counts(hb)
    full_lex = det_confusion.build_lexicon(counts=counts)
    tpaths = loaders.list_transcripts()
    tfreq = transcript_frequencies(tpaths)
    res = {d.DETECTOR_ID: {"hits": [], "seeded_hits": [], "clean_fp": [],
                           "clean_n": len(clean)} for d in DETECTORS}
    cache = {}
    for fx in confirmed:
        if fx["transcript"] not in cache:
            cache[fx["transcript"]] = loaders.read_transcript(fx["transcript"])
        text = cache[fx["transcript"]].text
        a = fx["char_offset"]
        b = a + len(fx["quoted"])
        for d in DETECTORS:
            for s in d.detect(text, lexicon=full_lex, transcript_freq=tfreq):
                if s["start"] < b and a < s["end"]:
                    seeded = ("seed:%s)" % fx["id"]) in s["note"]
                    key = "seeded_hits" if seeded else "hits"
                    res[d.DETECTOR_ID][key].append(fx["id"])
                    break
    held = {}
    for rec, text in fixtures.materialize_clean(clean, books):
        slug = rec["slug"]
        if slug not in held:
            held[slug] = det_confusion.build_lexicon(counts=counts,
                                                     exclude=(slug,))
        for d in DETECTORS:
            for s in d.detect(text, lexicon=held[slug], transcript_freq=None):
                res[d.DETECTOR_ID]["clean_fp"].append(
                    (rec["id"], s["quoted"], s["note"]))
    return res


def format_eval(res, n_fixtures):
    lines = ["| detector | fixture hits (independent) | fixture hits "
             "(seeded from that fixture) | clean-set false positives |",
             "|---|---|---|---|"]
    for det, r in res.items():
        lines.append("| %s | %d/%d %s | %d %s | %d/%d passages |" % (
            det, len(r["hits"]), n_fixtures, ",".join(r["hits"]),
            len(r["seeded_hits"]), ",".join(r["seeded_hits"]),
            len({x[0] for x in r["clean_fp"]}), r["clean_n"]))
        for fp in r["clean_fp"]:
            lines.append("|  | FP %s: %r — %s | | |" % fp)
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--eval", action="store_true")
    a = ap.parse_args(argv)
    books = loaders.read_book_store()
    if a.eval:
        conf = fixtures.load_json(fixtures.CONFIRMED_PATH)
        clean = fixtures.load_json(fixtures.CLEAN_PATH)
        print(format_eval(evaluate(books, conf, clean), len(conf)))
        return 0
    paths = loaders.list_transcripts() if a.all else a.paths
    if not paths:
        ap.error("give transcript paths or --all")
    lex = det_confusion.build_lexicon(hawkins_books(books))
    tfreq = transcript_frequencies(loaders.list_transcripts())
    out = []
    for p in paths:
        out.extend(records(loaders.read_transcript(p), lex, tfreq))
    blob = json.dumps(out, ensure_ascii=False, indent=1) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(blob)
        print("wrote %s (%d findings)" % (a.out, len(out)), file=sys.stderr)
    else:
        sys.stdout.write(blob)
    return 0


if __name__ == "__main__":
    sys.exit(main())
