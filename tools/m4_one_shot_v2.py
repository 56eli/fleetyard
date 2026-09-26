#!/usr/bin/env python3
"""TASK-019b harness — one-shot evaluation of the M4 detectors on a sealed split.

Quantum b of TASK-019, in code and in refusals. The evaluation it performs is
**not run** by building or testing this tool: `freeze` records the thresholds,
`run` is the single execution, `score` turns hand adjudications into counts, and
`verify` re-checks the receipt without touching the corpus.

Discipline the tool enforces (LAW §9 / TASK-019 quantum b):

  * **thresholds frozen and recorded before the run** — `freeze` writes
    `THRESHOLDS.json` bound to the split digest, the salt and every detector's
    file sha; `run` refuses if the freeze is missing, stale, or made after the
    receipt (it checks the receipt's `thresholds_sha256`);
  * **the run happens once** — `run` refuses outright when a receipt already
    exists for the out dir, and the receipt records `holdout_consumed: true`,
    the full read list, the split salt + digest, the tool commit and the run utc;
    a second run needs a **new split** (new salt) in a new out dir, and the
    refusal message says so;
  * **no tuning after the freeze** — `run` refuses if any detector file's sha
    differs from the frozen value, so a post-freeze edit cannot quietly ride along;
  * **labels are hand reads, not detector agreement** — `score` takes a labels
    file, computes precision only over hand-labelled signals, reports the
    labelled/total coverage, separates **seeded** from **independent** (LAW §9),
    keeps **CANDIDATE** out of every rate and reports it separately, and never
    emits a bare percentage without its counts;
  * **provenance** — every artefact the tool writes carries the §8 bindings and
    the harness stamps the thresholds digest into the receipt.

Commands:

  freeze  python3 tools/m4_one_shot_v2.py freeze --split tools/HELD-OUT-SPLIT-V2.json \
              --out runs/m4-q2-q3-v2-holdout --utc <iso> --tool-commit <sha> \
              --main-head <sha> --policy-sha <sha> [--corpus corpus]
  run     python3 tools/m4_one_shot_v2.py run --split ... --out ... --corpus corpus \
              --tool-commit <sha> [--detectors C1-drop,C2-format]
  score   python3 tools/m4_one_shot_v2.py score --out ... --labels labels.json
  verify  python3 tools/m4_one_shot_v2.py verify --out ... [--split ...]

Stdlib only, no network, corpus read-only, writes only under `--out`.
"""
import argparse
import collections
import datetime
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c2_detectors  # noqa: E402  (registry mirroring the detector modules)
import m5r_reduce as m5r  # noqa: E402

THRESHOLDS = "THRESHOLDS.json"
EXCLUSIONS = "tools/HELD-OUT-SPLIT-V2-EXCLUSIONS.json"
RECEIPT = "RECEIPT.json"
REVIEW = "REVIEW-QUEUE.md"
SIGNALS = "signals-holdout.json"
SCORE = "SCORE.json"
DETECTORS = ("C1-drop", "C2-format")
LABEL_VERDICTS = ("confirmed", "discarded")
ADJUDICATION_PROTOCOL = {
    "labels_are": "hand reads of each holdout signal against cited bytes; never detector agreement",
    "verdicts": list(LABEL_VERDICTS),
    "rate": ("precision = confirmed / (confirmed + discarded) over hand-labelled signals "
             "only; CANDIDATE/unlabelled signals are reported separately and never blended"),
    "separation": ("signals overlapping a confirmed fixture span are seeded and are "
                   "excluded from the independent rate (LAW §9)"),
    "reporting": ("every rate is published with both counts and the labelled/total "
                  "coverage; no corpus-wide extrapolation beyond the holdout"),
}


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha(path):
    return m5r.sha256_file(path)


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def dump(path, obj):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    blob = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(blob)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def detector_state(name):
    """Current file sha + frozen parameters for one detector."""
    module = c2_detectors.MODULES[name]
    return {"module": os.path.basename(module.__file__),
            "module_sha256": sha(os.path.abspath(module.__file__)),
            "params": c2_detectors.params(name)}


def freeze(args):
    split = load(args.split)
    doc = {
        "task": "TASK-019b (quantum b) — thresholds frozen before the one-shot run",
        "frozen_utc": args.utc,
        "tool_commit": args.tool_commit,
        "main_head": args.main_head,
        "policy_sha256": args.policy_sha,
        "split_file": args.split.replace(os.sep, "/"),
        "split_sha256": sha(args.split),
        "split_salt": split.get("salt"),
        "split_counts": split.get("counts"),
        "split_corpus_files_sha256": split.get("corpus_files_sha256"),
        "holdout_exclusions_file": args.exclusions.replace(os.sep, "/"),
        "holdout_exclusions_sha256": sha(args.exclusions),
        "holdout_exclusions": exclusion_set(args.exclusions),
        "detectors": {name: detector_state(name) for name in DETECTORS},
        "adjudication_protocol": ADJUDICATION_PROTOCOL,
        "freeze_precedes_holdout_read": (
            "committed before any read of this split's holdout; every v2-era manifest "
            "records holdout_reads: []"),
        "supersedes": None,
        "note": ("a later freeze must be a NEW dated record naming what it supersedes; "
                 "no detector file may change after this record without invalidating the "
                 "run (enforced in run(): module_sha256 mismatch = refusal)"),
    }
    path = os.path.join(args.out, THRESHOLDS)
    if os.path.exists(path):
        raise SystemExit("refusing to overwrite an existing freeze: %s (a new freeze "
                         "must name what it supersedes)" % path)
    digest = dump(path, doc)
    print("thresholds frozen: %s\nsha256 %s" % (path, digest))
    return 0


def exclusion_set(path=EXCLUSIONS):
    """The pre-registered exclusions (item v2.b iv): transcripts excluded from the denominator."""
    if not os.path.exists(path):
        return []
    doc = load(path)
    out = []
    for e in doc.get("excluded_transcripts", []):
        out.append(e["transcript"] if isinstance(e, dict) else str(e))
    return sorted(out)


def _guard_run(args):
    """Every refusal that protects the one-shot discipline, in one place."""
    th_path = os.path.join(args.out, THRESHOLDS)
    if not os.path.exists(th_path):
        raise SystemExit("REFUSED: no frozen threshold record at %s — run `freeze` first "
                         "(thresholds must be recorded before the run)" % th_path)
    receipt_path = os.path.join(args.out, RECEIPT)
    if os.path.exists(receipt_path):
        receipt = load(receipt_path)
        raise SystemExit(
            "REFUSED: this out dir already holds a consumption receipt "
            "(split salt %r, run %s, holdout_consumed=%s). The holdout is SPENT for "
            "these detector versions: a second run needs a NEW SPLIT (new salt) in a "
            "new --out dir, plus a dated record. Never re-run."
            % (receipt.get("split_salt"), receipt.get("run_utc"),
               receipt.get("holdout_consumed")))
    frozen = load(th_path)
    if sha(args.exclusions) != frozen.get("holdout_exclusions_sha256"):
        raise SystemExit("REFUSED: the pre-registered exclusions changed after the freeze "
                         "(%s) — an exclusion may not be changed after the freeze, only "
                         "before the run" % args.exclusions)
    if frozen["split_sha256"] != sha(args.split):
        raise SystemExit("REFUSED: the split file's sha256 does not match the frozen "
                         "record (%s vs %s) — the freeze binds a different split"
                         % (sha(args.split)[:12], frozen["split_sha256"][:12]))
    for name in args.detectors:
        now = detector_state(name)
        was = frozen["detectors"].get(name)
        if not was or was["module_sha256"] != now["module_sha256"]:
            raise SystemExit("REFUSED: %s changed after the freeze (%s -> %s) — a "
                             "post-freeze detector edit invalidates the run"
                             % (name, (was or {}).get("module_sha256", "ABSENT")[:12],
                                now["module_sha256"][:12]))
        if was["params"] != now["params"]:
            raise SystemExit("REFUSED: %s parameters changed after the freeze" % name)
    return frozen


def run(args):
    frozen = _guard_run(args)
    split = load(args.split)
    excluded = exclusion_set(args.exclusions)
    unknown = [t for t in excluded if t not in set(split["holdout"])]
    if unknown:
        raise SystemExit("REFUSED: pre-registered exclusions are not holdout members: %r"
                         % unknown[:3])
    holdout = sorted(set(split["holdout"]) - set(excluded))
    reads, per_detector, dropped_total = [], {}, []
    for name in args.detectors:
        signals, read = c2_detectors.evaluate(name, args.corpus, args.split)
        # the pre-registered exclusions are dropped here, unexamined: their signals never
        # enter the artefact, a denominator or a review queue
        dropped = sorted(set(signals) & set(excluded))
        signals = {t: v for t, v in signals.items() if t not in set(excluded)}
        if sorted(signals) != holdout:
            raise SystemExit("REFUSED: %s evaluated %d transcripts, not the frozen holdout "
                             "set of %d — refusing to score a partial read"
                             % (name, len(signals), len(holdout)))
        per_detector[name] = signals
        reads.extend(t for t in read if t not in set(excluded))
        dropped_total.extend(dropped)
    signals_path = os.path.join(args.out, SIGNALS)
    signals_sha = dump(signals_path, per_detector)
    receipt = {
        "task": "TASK-019b (quantum b) — one-shot holdout evaluation receipt",
        "run_utc": args.utc or utc_now(),
        "tool_commit": args.tool_commit,
        "main_head": frozen["main_head"],
        "policy_sha256": frozen["policy_sha256"],
        "split_file": frozen["split_file"],
        "split_sha256": frozen["split_sha256"],
        "split_salt": frozen["split_salt"],
        "thresholds_file": THRESHOLDS,
        "thresholds_sha256": sha(os.path.join(args.out, THRESHOLDS)),
        "holdout_consumed": True,
        "one_shot": {"attempt": 1, "max_attempts": 1,
                     "rule": "a second run needs a new split (new salt) + dated record"},
        "holdout_reads": sorted(set(reads)),
        "holdout_transcripts": len(holdout),
        "holdout_excluded": excluded,
        "holdout_evaluated": len(holdout),
        "excluded_signals_dropped_unexamined": sorted(set(dropped_total)),
        "exclusion_rule": ("excluded transcripts contribute no signals, no denominator and "
                           "no review queue entries; the exclusion was fixed before the run"),
        "holdout_exclusions_file": args.exclusions.replace(os.sep, "/"),
        "holdout_exclusions_sha256": sha(args.exclusions),
        "detectors": {name: {
            "signals_total": sum(len(v) for v in per_detector[name].values()),
            "transcripts_with_signals": sum(1 for v in per_detector[name].values() if v),
            "module_sha256": frozen["detectors"][name]["module_sha256"],
        } for name in args.detectors},
        "signals_file": SIGNALS,
        "signals_sha256": signals_sha,
        "status": ("raw CANDIDATE-class signals over the sealed holdout, unreviewed; "
                   "labels are hand reads (score step); no rate exists until then"),
    }
    receipt_sha = dump(os.path.join(args.out, RECEIPT), receipt)
    _review(args, receipt, per_detector)
    print("one-shot run complete: %d transcripts, %s"
          % (len(holdout), {k: v["signals_total"] for k, v in receipt["detectors"].items()}))
    print("receipt sha256 %s\nsignals sha256 %s" % (receipt_sha, signals_sha))
    return 0


def _review(args, receipt, per_detector):
    lines = ["# TASK-019b — holdout review queue (hand adjudication required)", "",
             "The receipt below is one-shot: **never re-run**. Every signal needs a hand",
             "read against cited bytes, with a verdict of `confirmed` or `discarded` and a",
             "reason; `score` refuses any other verdict.", "",
             "Label keys are detector-qualified — `\"<detector>/<transcript>#<n>\": {\"verdict\":",
             "\"confirmed\"|\"discarded\", \"reason\": \"<the cited bytes read>\"}` — because the same",
             "transcript index occurs under more than one detector.", "",
             "| field | value |", "|---|---|",
             "| run utc | %s |" % receipt["run_utc"],
             "| split salt | `%s` |" % receipt["split_salt"],
             "| split sha256 | `%s` |" % receipt["split_sha256"],
             "| holdout transcripts | %d |" % receipt["holdout_transcripts"],
             "| signals | %s |" % ", ".join("%s %d" % (k, v["signals_total"])
                                            for k, v in sorted(receipt["detectors"].items())),
             "", "## Signals", ""]
    for name in sorted(per_detector):
        lines.append("### %s" % name)
        lines.append("")
        for transcript in sorted(per_detector[name]):
            for i, sig in enumerate(per_detector[name][transcript], 1):
                lines.append("- [ ] `%s/%s#%d` %s @%d-%d `%s`  → verdict: ____ reason: ____"
                             % (name, transcript, i,
                                sig.get("rule") or sig.get("detector"),
                                sig.get("start", -1), sig.get("end", -1),
                                (sig.get("quoted") or "")[:80].replace("\n", " ")))
        lines.append("")
    with open(os.path.join(args.out, REVIEW), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def score(args):
    labels = load(args.labels)
    signals = load(os.path.join(args.out, SIGNALS))
    receipt = load(os.path.join(args.out, RECEIPT))
    result = {"task": "TASK-019b — scored hand adjudications", "run_utc": utc_now(),
              "scored_utc": args.utc or utc_now(),
              "receipt_sha256": sha(os.path.join(args.out, RECEIPT)),
              "signals_sha256": sha(os.path.join(args.out, SIGNALS)),
              "split_salt": receipt["split_salt"],
              "protocol": ADJUDICATION_PROTOCOL, "detectors": {}}
    for name in sorted(signals):
        rows = [(t, i, sig) for t in sorted(signals[name])
                for i, sig in enumerate(signals[name][t], 1)]  # 1-based: matches REVIEW-QUEUE.md
        counts = collections.Counter()
        examples = []
        for transcript, idx, sig in rows:
            key = "%s/%s#%d" % (name, transcript, idx)
            label = labels.get(key)
            if label is None:
                counts["unlabelled"] += 1
                continue
            verdict = label.get("verdict")
            if verdict not in LABEL_VERDICTS:
                raise SystemExit("REFUSED: label %r has verdict %r; allowed: %s"
                                 % (key, verdict, list(LABEL_VERDICTS)))
            if not label.get("reason"):
                raise SystemExit("REFUSED: label %r carries no reason" % key)
            seeded = bool(sig.get("seeded") or label.get("seeded"))
            bucket = "seeded" if seeded else "independent"
            counts[verdict] += 1
            counts["%s_%s" % (bucket, verdict)] += 1
            if verdict == "discarded" and len(examples) < 10:
                examples.append({"key": key, "reason": label.get("reason"),
                                 "citation": label.get("citation")})
        ind_c = counts.get("independent_confirmed", 0)
        ind_d = counts.get("independent_discarded", 0)
        seeded_c = counts.get("seeded_confirmed", 0)
        seeded_d = counts.get("seeded_discarded", 0)
        labelled = ind_c + ind_d + seeded_c + seeded_d
        result["detectors"][name] = {
            "signals_total": len(rows),
            "labelled": labelled,
            "label_coverage": ("%d/%d" % (labelled, len(rows))),
            "independent": {"confirmed": ind_c, "discarded": ind_d,
                            "precision": (("%d/%d" % (ind_c, ind_c + ind_d))
                                          if (ind_c + ind_d) else None)},
            "seeded_excluded": {"confirmed": seeded_c, "discarded": seeded_d},
            "candidate_unlabelled": counts.get("unlabelled", 0),
            "fp_examples": examples,
            "reading": ("precision is stated as counts over hand-labelled independent "
                        "signals only; seeded signals are excluded from it; unlabelled "
                        "signals stay CANDIDATE and are never blended"),
        }
    dump(os.path.join(args.out, SCORE), result)
    print(json.dumps({k: v["independent"] for k, v in result["detectors"].items()},
                     indent=1))
    print("scored → %s" % os.path.join(args.out, SCORE))
    return 0


def verify(args):
    problems = []
    out = args.out
    for name in (THRESHOLDS, RECEIPT, SIGNALS):
        if not os.path.exists(os.path.join(out, name)):
            problems.append("%s missing" % name)
    if problems:
        for p in problems:
            print("FAIL: %s" % p)
        return 1
    receipt = load(os.path.join(out, RECEIPT))
    frozen = load(os.path.join(out, THRESHOLDS))
    if receipt["thresholds_sha256"] != sha(os.path.join(out, THRESHOLDS)):
        problems.append("receipt's thresholds digest does not match the frozen record")
    if receipt["signals_sha256"] != sha(os.path.join(out, SIGNALS)):
        problems.append("receipt's signals digest does not match the signals file")
    if not receipt.get("holdout_consumed"):
        problems.append("receipt does not stamp holdout_consumed")
    if receipt["one_shot"]["attempt"] != 1:
        problems.append("receipt is not a first attempt")
    if frozen["split_sha256"] != receipt["split_sha256"]:
        problems.append("freeze and receipt disagree on the split digest")
    if receipt.get("holdout_exclusions_sha256") != frozen.get("holdout_exclusions_sha256"):
        problems.append("freeze and receipt disagree on the exclusions digest")
    if len(set(receipt.get("holdout_excluded", [])) & set(receipt.get("holdout_reads", []))):
        problems.append("a pre-registered exclusion was read anyway")
    if args.split and os.path.exists(args.split):
        if sha(args.split) != frozen["split_sha256"]:
            problems.append("the live split file no longer matches the freeze")
    for name in sorted(receipt["detectors"]):
        now = detector_state(name)["module_sha256"]
        if now != receipt["detectors"][name]["module_sha256"]:
            problems.append("%s changed after the run — the receipt is for another "
                            "detector version" % name)
    if problems:
        for p in problems:
            print("FAIL: %s" % p)
        return 1
    print("one-shot receipt verify: OK (%s; %d holdout transcripts read; detectors %s; "
          "signals digest %s…)" % (receipt["run_utc"], receipt["holdout_transcripts"],
                                   ",".join(sorted(receipt["detectors"])),
                                   receipt["signals_sha256"][:12]))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("freeze")
    r = sub.add_parser("run")
    s = sub.add_parser("score")
    v = sub.add_parser("verify")
    for p in (f, r, s, v):
        p.add_argument("--out", default="runs/m4-q2-q3-v2-holdout")
    for p in (f, r, v):
        p.add_argument("--split", default="tools/HELD-OUT-SPLIT-V2.json")
        p.add_argument("--exclusions", default=EXCLUSIONS)
    f.add_argument("--utc", required=True)
    f.add_argument("--tool-commit", required=True)
    f.add_argument("--main-head", required=True)
    f.add_argument("--policy-sha", required=True)
    r.add_argument("--corpus", default="corpus")
    r.add_argument("--tool-commit", required=True)
    r.add_argument("--utc", default=None)
    r.add_argument("--detectors", default=",".join(DETECTORS))
    s.add_argument("--labels", required=True)
    s.add_argument("--utc", default=None)
    a = ap.parse_args(argv)
    if a.cmd == "run":
        a.detectors = tuple(x.strip() for x in a.detectors.split(",") if x.strip())
    return {"freeze": freeze, "run": run, "score": score, "verify": verify}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
