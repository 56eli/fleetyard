#!/usr/bin/env python3
"""TASK-011: M5 exploratory full-corpus RAW signal census (NOT audited findings).

    python3 tools/sweep_m5.py [--out runs/m5-raw] [--limit N] [--fresh]

Runs exactly A1-repetition, A2-nonsense, B1-contradiction and B2-misquote
(A4-confusion EXCLUDED: independent fixture recall 0/16 and its in-sample
clean FP figure is void, owner ERRATA-2026-09-25 section 3) over every
corpus/docdocgo/overlays/*.txt in sorted order (manifest.json excluded).

Output (the only files written), under --out:
  records/<transcript stem>.json   raw signal records for one transcript,
                                   written per transcript, so an interrupted
                                   sweep resumes where it stopped
  index.json                       machine-readable manifest + totals
  INDEX.md                         human-readable manifest + totals

Every record carries review_status "unreviewed" and reporting_class
"CANDIDATE-class raw signal, unreviewed". The runner's own label is kept as
raw_runner_confidence; a runner "HIGH CONFIDENCE" is NOT a reviewed HIGH
finding and must never enter a headline rate (STANDARDS). No transcript is
"audited" by this tool: audited = detectors ran AND a finding pass reviewed
the emitted records; this tool does only the first half.

Reads only corpus/** . Stdlib only, no network.
"""
import argparse
import collections
import hashlib
import json
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loaders  # noqa: E402
import run_detectors as rd  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUT = os.path.join("runs", "m5-raw")
ZIP = "docdocgo-fixes.zip"
REVIEW_STATUS = "unreviewed"
REPORTING_CLASS = "CANDIDATE-class raw signal, unreviewed"
YEAR_RE = re.compile(r"_((?:19|20)\d\d)(?:_|$)")
EXCLUDED = {
    "A4-confusion": "no independent held-out FP rate; fixture recall 0/16 "
                    "independent (TASK-007 pending)",
    "drop-word": "detector never built (M2 accepted incomplete); unmeasured, "
                 "NOT zero",
    "speaker/format": "detector never built (M2 accepted incomplete); "
                      "unmeasured, NOT zero",
}


def year_of(path):
    m = YEAR_RE.search(os.path.basename(path).replace(".txt", ""))
    return m.group(1) if m else "unknown"


def stem(path):
    return os.path.basename(path)[:-len(".txt")]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_head():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                       stderr=subprocess.DEVNULL,
                                       text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def raw_records(transcript, dets, ctx):
    out = []
    for r in rd.records(transcript, None, None, dets, **ctx):
        r["raw_runner_confidence"] = r.pop("confidence")
        r["reporting_class"] = REPORTING_CLASS
        r["review_status"] = REVIEW_STATUS
        out.append(r)
    return out


def split_ids(detector_id):
    return detector_id.split("+")


def summarise(paths, per_file, failures, meta):
    det_totals = collections.Counter()
    combos = collections.Counter()
    raw_conf = collections.Counter()
    by_year = collections.defaultdict(lambda: {"transcripts": 0,
                                               "processed": 0, "records": 0})
    zero = []
    rows = []
    for p in paths:
        y = year_of(p)
        by_year[y]["transcripts"] += 1
        s = stem(p)
        if s not in per_file:
            continue
        recs = per_file[s]
        by_year[y]["processed"] += 1
        by_year[y]["records"] += len(recs)
        c = collections.Counter()
        for r in recs:
            combos[r["detector_id"]] += 1
            raw_conf[r["raw_runner_confidence"]] += 1
            for d in split_ids(r["detector_id"]):
                c[d] += 1
                det_totals[d] += 1
        if not recs:
            zero.append(s)
        rows.append({"transcript": s, "year": y, "records": len(recs),
                     "per_detector": dict(sorted(c.items()))})
    n_proc = len(per_file)
    pending = [stem(p) for p in paths if stem(p) not in per_file]
    return dict(meta, **{
        "transcripts_total": len(paths),
        "processed": n_proc,
        "pending_detector_run": len(pending),
        "next_pending": pending[0] if pending else None,
        "failed_reads": failures,
        "finding_pass_audited": 0,
        "pending_review": n_proc,
        "records_total": sum(len(v) for v in per_file.values()),
        "records_per_detector_signal": dict(sorted(det_totals.items())),
        "records_per_detector_combination": dict(sorted(combos.items())),
        "raw_runner_confidence": dict(sorted(raw_conf.items())),
        "by_year": dict(sorted(by_year.items())),
        "zero_hit_transcripts": zero,
        "per_transcript": rows,
    })


def render_md(ix):
    L = []
    w = L.append
    w("# M5 raw signal census — PROVISIONAL, UNREVIEWED (TASK-011)")
    w("")
    w("**This is not an audited-findings release.** Every record below is a "
      "*CANDIDATE-class raw signal, unreviewed*, including records the runner "
      "labelled `HIGH CONFIDENCE`. No detector precision has been measured. "
      "Clean-set checks (0/59) are in-sample only, invalid as an independent "
      "false-positive estimate. A transcript with zero raw hits is NOT shown "
      "to be error-free.")
    w("")
    w("## Provenance")
    w("")
    for k in ("generated_utc", "corpus_zip_sha256", "overlays_sha256",
              "tool_commit", "detectors", "command"):
        w("- %s: `%s`" % (k, ix[k]))
    w("- excluded:")
    for k, v in ix["excluded"].items():
        w("  - %s — %s" % (k, v))
    w("")
    w("## Coverage truth")
    w("")
    w("| transcripts (.txt) | detector-run | pending detector run | "
      "finding-pass audited | pending review | failed reads |")
    w("|---|---|---|---|---|---|")
    w("| %d | %d | %d | %d | %d | %d |" % (
        ix["transcripts_total"], ix["processed"], ix["pending_detector_run"],
        ix["finding_pass_audited"], ix["pending_review"],
        len(ix["failed_reads"])))
    if ix["next_pending"]:
        w("")
        w("Next pending file: `%s`" % ix["next_pending"])
    w("")
    w("## Raw unreviewed signal totals (CANDIDATE-class, not error counts)")
    w("")
    w("Records: **%d**. A record is one merged span; a span flagged by two "
      "detectors counts once in the record total and once per detector "
      "below." % ix["records_total"])
    w("")
    w("| detector | records carrying its signal |")
    w("|---|---|")
    for d, n in ix["records_per_detector_signal"].items():
        w("| %s | %d |" % (d, n))
    w("")
    w("| detector combination | records |")
    w("|---|---|")
    for d, n in ix["records_per_detector_combination"].items():
        w("| %s | %d |" % (d, n))
    w("")
    w("Raw runner label (NOT a reviewed class): " + ", ".join(
        "%s %d" % kv for kv in ix["raw_runner_confidence"].items()))
    w("")
    w("## By year (from file name; `unknown` kept separate)")
    w("")
    w("| year | transcripts | detector-run | raw records |")
    w("|---|---|---|---|")
    for y, v in ix["by_year"].items():
        w("| %s | %d | %d | %d |" % (y, v["transcripts"], v["processed"],
                                     v["records"]))
    w("")
    w("## Re-review candidates (most raw records; NOT proven hotspots)")
    w("")
    w("| transcript | year | raw records | per detector |")
    w("|---|---|---|---|")
    top = sorted(ix["per_transcript"], key=lambda r: (-r["records"],
                                                       r["transcript"]))[:20]
    for r in top:
        w("| %s | %s | %d | %s |" % (r["transcript"], r["year"], r["records"],
                                     ", ".join("%s %d" % kv for kv in
                                               r["per_detector"].items())))
    w("")
    w("## Zero-raw-hit transcripts (%d; not evidence of zero errors)" %
      len(ix["zero_hit_transcripts"]))
    w("")
    for s in ix["zero_hit_transcripts"]:
        w("- %s" % s)
    w("")
    w("Per-transcript counts: `index.json` → `per_transcript`; records: "
      "`records/<transcript>.json`.")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--limit", type=int, help="process at most N new files")
    ap.add_argument("--fresh", action="store_true",
                    help="ignore existing per-transcript outputs")
    a = ap.parse_args(argv)
    dets = rd.select_ids(rd.M5_SELECTION)
    assert all(d.DETECTOR_ID != "A4-confusion" for d in dets)
    paths = loaders.list_transcripts()
    recdir = os.path.join(a.out, "records")
    os.makedirs(recdir, exist_ok=True)
    books = loaders.read_book_store()
    ctx = rd.book_context(books, dets)
    per_file, failures, done_new = {}, [], 0
    t0 = time.time()
    for p in paths:
        s = stem(p)
        fp = os.path.join(recdir, s + ".json")
        if not a.fresh and os.path.exists(fp):
            with open(fp, encoding="utf-8") as fh:
                per_file[s] = json.load(fh)
            continue
        if a.limit is not None and done_new >= a.limit:
            continue
        try:
            recs = raw_records(loaders.read_transcript(p), dets, ctx)
        except (OSError, ValueError) as e:
            failures.append({"transcript": s, "error": repr(e)})
            continue
        tmp = fp + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(recs, ensure_ascii=False, indent=1) + "\n")
        os.replace(tmp, fp)
        per_file[s] = recs
        done_new += 1
        print("[%3d/%d] %6.0fs %4d rec  %s" % (len(per_file), len(paths),
                                               time.time() - t0, len(recs), s),
              file=sys.stderr, flush=True)
    overlays = hashlib.sha256()
    for p in paths:
        overlays.update(stem(p).encode("utf-8") + b"\0" +
                        sha256_file(p).encode() + b"\n")
    meta = {
        "task": "TASK-011",
        "status": "PROVISIONAL raw census, unreviewed; M5 NOT certified",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "corpus_zip_sha256": sha256_file(os.path.join(ROOT, ZIP))
        if os.path.exists(os.path.join(ROOT, ZIP)) else "missing",
        "overlays_sha256": overlays.hexdigest(),
        "tool_commit": git_head(),
        "detectors": [d.DETECTOR_ID for d in dets],
        "excluded": EXCLUDED,
        "command": "python3 tools/sweep_m5.py --out %s" % a.out,
        "precision": "UNMEASURED",
        "clean_set": "0/59 in-sample only, invalid as independent FP estimate",
    }
    ix = summarise(paths, per_file, failures, meta)
    with open(os.path.join(a.out, "index.json"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(ix, ensure_ascii=False, indent=1) + "\n")
    with open(os.path.join(a.out, "INDEX.md"), "w", encoding="utf-8") as fh:
        fh.write(render_md(ix))
    print("processed %d/%d, records %d, failures %d" % (
        ix["processed"], ix["transcripts_total"], ix["records_total"],
        len(failures)), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
