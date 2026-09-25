#!/usr/bin/env python3
"""M4-q4 — one-shot holdout evaluation runs (WORKER-2).

Runs the FROZEN detectors over the HOLDOUT half of tools/HELD-OUT-SPLIT.json and
records raw-signal counts with provenance. This is the "held-out data" step of
LAW §9, with one honest limit stated up front:

  **Raw signal counts are not precision.** Precision/recall need reviewed labels
  (a human STANDARDS pass over the holdout signals); until that exists, this tool
  reports counts and rates only, never a quality score.

Discipline (PATTERNS §5):
  * thresholds are frozen before this run (they live in the detector sources and
    are pinned by sha256 in the provenance);
  * the holdout is reported ONCE; nothing is tuned against it here. Any later
    change informed by these numbers spends the holdout for that detector and
    requires a new split (new salt);
  * `holdout_consumed: true` is stamped in the provenance of every holdout run.

Three subcommands (each a bounded quantum of its own):
  v1      — the inherited v1 detectors A1,A2,B1,B2 from `--v1-tools`
  drop    — C1-drop (tools/det_dropword.py)
  format  — C2-format (tools/det_format.py)

Stdlib only; read-only over the corpus; writes only under --out.
"""
import argparse
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import m5r_reduce as m5r  # noqa: E402

V1_DETECTORS = "A1,A2,B1,B2"


def _utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _holdout(split_path):
    split = json.load(open(split_path, encoding="utf-8"))
    overlap = sorted(set(split["tuning"]) & set(split["holdout"]))
    if overlap:
        raise SystemExit("m4 q4: split integrity violation: %r" % overlap[:3])
    return split, sorted(set(split["holdout"]))


def _prov(out_dir, name, payload):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    return path


def run_v1(v1_tools, corpus, split_path, out_dir):
    sys.path.insert(0, os.path.abspath(v1_tools))
    import run_detectors as rd  # noqa: E402
    import loaders  # noqa: E402

    books = loaders.read_book_store()          # corpus/docdocgo/... via cwd
    dets = rd.select_ids(V1_DETECTORS)
    ctx = rd.book_context(books, dets)
    split, holdout = _holdout(split_path)
    per_file, per_det = {}, {}
    for n in holdout:
        path = os.path.join("corpus", "docdocgo", "overlays", n)
        recs = rd.records(loaders.read_transcript(path), None, None, dets, **ctx)
        per_file[n] = recs
        for r in recs:
            for d in str(r["detector_id"]).split("+"):
                per_det[d] = per_det.get(d, 0) + 1
    out = {"detector_set": V1_DETECTORS, "per_transcript": per_file,
           "signals_total": sum(len(v) for v in per_file.values()),
           "per_detector_signal_instances": per_det}
    _prov(out_dir, "v1-holdout.json", out)
    prov = {
        "run_utc": _utc(), "part": "v1",
        "v1_tools_dir": os.path.abspath(v1_tools),
        "v1_tool_shas": {f: m5r.sha256_file(os.path.join(v1_tools, f))
                         for f in sorted(os.listdir(v1_tools))
                         if f.endswith(".py")},
        "detectors": V1_DETECTORS,
        "split": split_path, "split_salt": split["salt"],
        "split_corpus_files_sha256": split["corpus_files_sha256"],
        "transcripts_read": holdout, "set": "holdout",
        "holdout_reads": holdout, "holdout_consumed": True,
        "thresholds_frozen_before_run": True,
        "signals_total": out["signals_total"],
        "per_detector_signal_instances": per_det,
        "status": "raw signal counts (counts only — NOT precision); PROVISIONAL-UNGATED",
        "note": "no threshold was tuned against the holdout; this report is one-shot "
                "(LAW §9). Any later tuning informed by it requires a new split.",
    }
    _prov(out_dir, "v1-holdout.PROVENANCE.json", prov)
    return out["signals_total"]


def run_drop(corpus, split_path, out_dir, shard=None, shards=None):
    import det_dropword as dd  # noqa: E402
    tag = ("h%d" % shard) if shard else None
    per_file, total = dd.run_tuning(corpus, split_path, out_dir, shard=shard,
                                    shards=shards,
                                    part_tag=("holdout-drop-%s" % shard) if shard
                                    else "holdout-drop", which="holdout")
    return total


def run_format(corpus, split_path, out_dir):
    import det_format as df  # noqa: E402
    per_file, total = df.run_tuning(corpus, split_path, out_dir,
                                    part_tag="holdout-format", which="holdout")
    return total


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("v1")
    v.add_argument("--v1-tools", default="evidence/tools")
    v.add_argument("--corpus", default="corpus")
    v.add_argument("--split", default="tools/HELD-OUT-SPLIT.json")
    v.add_argument("--out", default="runs/m4-q4-holdout")
    d = sub.add_parser("drop")
    d.add_argument("--corpus", default="corpus")
    d.add_argument("--split", default="tools/HELD-OUT-SPLIT.json")
    d.add_argument("--out", default="runs/m4-q4-holdout")
    d.add_argument("--shard", type=int)
    d.add_argument("--shards", type=int)
    f = sub.add_parser("format")
    f.add_argument("--corpus", default="corpus")
    f.add_argument("--split", default="tools/HELD-OUT-SPLIT.json")
    f.add_argument("--out", default="runs/m4-q4-holdout")
    a = ap.parse_args(argv)
    if a.cmd == "v1":
        n = run_v1(a.v1_tools, a.corpus, a.split, a.out)
        print("m4-q4 v1 holdout: %d raw signals (%s)" % (n, V1_DETECTORS))
    elif a.cmd == "drop":
        n = run_drop(a.corpus, a.split, a.out, a.shard, a.shards)
        print("m4-q4 C1-drop holdout%s: %d raw signals"
              % ((" shard %s" % a.shard) if a.shard else "", n))
    else:
        n = run_format(a.corpus, a.split, a.out)
        print("m4-q4 C2-format holdout: %d raw signals" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
