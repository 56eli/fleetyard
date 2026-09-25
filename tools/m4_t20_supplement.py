#!/usr/bin/env python3
"""TASK-020 item 1 (LAW §8 supplements for the q2 and q3 run directories) and
item 5b (the C2-format source-inheritance filter, additive).

Item 1 — the gates found the §8 manifests incomplete: no `tool_commit`, no
`main_head`, no `policy_sha256`, no book-store digest (load-bearing for the
book-anchored C1-drop), no config digest, no per-part output digest, and a
`detector_sha256` that resolved to an uncommitted working-tree state
(`84e5407f…` for C1-drop) or to an older commit (`c322e053…` for C2-format).
This tool writes **new** files — `PROVENANCE-SUPPLEMENT.json` in each run
directory — and edits nothing: the original manifests stay byte-identical and
readable, and the supplement states plainly what the original pin bound.

Item 5b — the gate's filter for C2-format: *a punctuation/whitespace artifact
whose bytes are inherited from the matched book span must not be reported*. The
format detector has no book anchor, so the filter is applied as the gate applied
it: suppress a signal when the transcript's own wording (span ±30 chars) occurs
verbatim in the book store. Raw and filtered counts are both published. C1-drop's
variant of the same filter (item 5a) lives in `tools/m4_q2_evidence.py` and its
counts are re-measured here for the supplement.

Commands:

  build   python3 tools/m4_t20_supplement.py build --corpus corpus \
              --split tools/HELD-OUT-SPLIT-V2.json --q2 runs/m4-q2-dropword \
              --q3 runs/m4-q3-format --utc <iso> --tool-commit <sha> \
              --main-head <sha> --policy-sha <sha>
  verify  python3 tools/m4_t20_supplement.py verify --corpus corpus \
              --split tools/HELD-OUT-SPLIT-V2.json --q2 runs/m4-q2-dropword \
              --q3 runs/m4-q3-format

Stdlib only, no network, read-only over the corpus and the book store. The v2
holdout is never opened (every transcript read passes the guard).
"""
import argparse
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import det_dropword as dd              # noqa: E402
import det_format as df                # noqa: E402
import fixtures                        # noqa: E402
import m4_q3_evidence as q3ev           # noqa: E402
import m5r_reduce as m5r                # noqa: E402

SUPPLEMENT = "PROVENANCE-SUPPLEMENT.json"
CONTEXT = 30
CORPUS_ZIP_SHA = "3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db"
BOOK_STORE_REL = os.path.join("docdocgo", "html", "merged-book-texts_json_1.js")
Q2_PARAMS = {"window": dd.WINDOW, "stride": dd.STRIDE, "min_score": dd.MIN_SCORE,
             "top_k": dd.TOP_K, "min_matched": dd.MIN_MATCHED,
             "min_ratio": dd.MIN_RATIO, "max_drop": dd.MAX_DROP,
             "min_flank": dd.MIN_FLANK}
Q3_RULES = ["R1-glued-period", "R2-repeated-punct", "R3-long-dot-run",
            "R4-underscore-run", "R5-space-before-comma", "R6-spaced-period",
            "R7-glued-comma"]


def digest_config(params):
    return hashlib.sha256(json.dumps(params, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def sha(path):
    return m5r.sha256_file(path) if os.path.exists(path) else None


def source_inheritance(sig, text, books):
    """Item 5a/5b rule: the signal's own wording verbatim in the book store."""
    a, b = sig["start"], sig["end"]
    ctx = text[max(0, a - CONTEXT):b + CONTEXT]
    books_hit = sorted(slug for slug, book in books.items() if ctx in book)
    return {"source_inherited": bool(books_hit), "context": ctx,
            "books": books_hit[:5],
            "bare_quoted_match": sorted(slug for slug, book in books.items()
                                        if sig["quoted"] in book)[:5]}


def q3_filter(args, books, guard, split):
    """Item 5b: raw vs filtered over the v2-tuning run and the clean misfire."""
    signals = json.load(open(os.path.join(args.q3, "signals-v2tuning.json"),
                             encoding="utf-8"))
    rows, inherited = [], 0
    for name in sorted(signals):
        if not signals[name]:
            continue                       # nothing to filter; never read the file
        text = guard.text(name)
        for sig in signals[name]:
            info = source_inheritance(sig, text, books)
            if info["source_inherited"]:
                inherited += 1
            rows.append({"transcript": name, "start": sig["start"],
                         "rule": sig["rule"], **info})
    clean = fixtures.load_json(fixtures.CLEAN_PATH)
    clean_rows = []
    for rec, text in fixtures.materialize_clean(clean, books):
        for sig in df.detect(text):
            clean_rows.append({"id": rec["id"], "slug": rec["slug"],
                               "rule": sig["rule"], "quoted": sig["quoted"],
                               **source_inheritance(sig, text, books)})
    return {"rule": ("suppress a signal when the transcript's own wording "
                     "(span ±%d chars) occurs verbatim in the book store; the format "
                     "detector has no book anchor, so this is the gate's own shape "
                     "applied without a matched span" % CONTEXT),
            "run": {"raw": len(rows), "source_inherited": inherited,
                    "filtered": len(rows) - inherited,
                    "signals": rows},
            "clean_set": {"misfires_raw": len(clean_rows),
                          "source_inherited": sum(1 for r in clean_rows
                                                  if r["source_inherited"]),
                          "misfires_after_filter": sum(1 for r in clean_rows
                                                       if not r["source_inherited"]),
                          "signals": clean_rows}}


def q2_filter_counts(args, books, guard, split):
    """Item 5a: C1-drop's filter, re-measured for the supplement."""
    signals = json.load(open(os.path.join(args.q2, "signals.json"), encoding="utf-8"))
    holdout = set(split["holdout"])
    raw = inherited = deferred = 0
    examples = []
    texts = {}
    for name in sorted(signals):
        for sig in signals[name]:
            raw += 1
            if name in holdout:
                deferred += 1
                continue
            if name not in texts:
                texts[name] = guard.text(name)
            info = source_inheritance(sig, texts[name], books)
            if info["source_inherited"]:
                inherited += 1
                if len(examples) < 8:
                    examples.append({"transcript": name, "start": sig["start"],
                                     "dropped_words": sig.get("dropped_words"),
                                     "books": info["books"]})
    return {"rule": ("suppress a drop when the transcript's own wording (span ±%d "
                     "chars) occurs verbatim in the book store — the transcript *was* "
                     "book text (cross-book self-parallel)" % CONTEXT),
            "raw": raw, "source_inherited": inherited,
            "filtered": raw - inherited - deferred, "deferred_holdout": deferred,
            "filtered_if_deferred_were_kept": raw - inherited,
            "examples": examples}


def supplement_common(args, split, books):
    return {
        "run_utc": args.utc,
        "tool_commit": args.tool_commit,
        "main_head": args.main_head,
        "policy_sha256": args.policy_sha,
        "corpus_zip_sha256": CORPUS_ZIP_SHA,
        "book_store_sha256": m5r.sha256_file(os.path.join(args.corpus, BOOK_STORE_REL)),
        "split_file": args.split.replace(os.sep, "/"),
        "split_corpus_files_sha256": split["corpus_files_sha256"],
        "split_counts": split.get("counts"),
        "holdout_reads": [],
        "holdout_enforced": True,
        "why_this_file_exists": (
            "ORCH-2's q2/q3 gates failed the LAW §8 criteria: the original manifests "
            "carried no tool_commit / main_head / policy_sha256 / book-store digest / "
            "config digest / per-part output digest, and their detector pins resolved "
            "to uncommitted or older states. This supplement is new (nothing was "
            "edited in place); the originals stay readable and unchanged."),
    }


def build(args):
    split = q3ev.load_split(args.split)
    guard = q3ev.HoldoutGuard(args.corpus, split["holdout"])
    books = m5r.parse_book_store(os.path.join(args.corpus, BOOK_STORE_REL))

    # ---- q2 supplement
    q2 = supplement_common(args, split, books)
    q2.update({
        "task": "TASK-020 item 1 (q2 part) — LAW §8 supplement for runs/m4-q2-dropword",
        "detector": dd.DETECTOR_ID,
        "detector_sha256_at_head": sha(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "det_dropword.py")),
        "detector_pin_defect": {
            "original_pin": "84e5407f…",
            "defect": ("resolves to NO committed blob: the six parts ran "
                       "18:57:11Z–19:05:21Z, before the delivery commit 012914d "
                       "(19:06:53Z), so every part manifest pinned an uncommitted "
                       "working-tree state"),
            "committed_versions": {"012914d": "588e1f22… (= head of det_dropword.py)"},
            "attribution_bridge": ("ORCH-2 re-ran shards 1 and 3 at head and got "
                                   "byte-identical part-1.json (64a97be5…) and "
                                   "part-3.json (092d6341…) = 66/193 transcripts and "
                                   "93/122 signals; the 4e114f1 change was "
                                   "runner/CLI-only (--set {tuning,holdout}, provenance "
                                   "keys), read in full by the gate"),
        },
        "config": Q2_PARAMS,
        "config_sha256": digest_config(Q2_PARAMS),
        "config_digest_note": ("sha256 over json.dumps(params, sort_keys=True, "
                               "separators=(',',':'))"),
        "parts": {("part-%d.json" % i): sha(os.path.join(args.q2, "part-%d.json" % i))
                  for i in range(1, 7)},
        "merge": {"signals_file": "signals.json",
                  "signals_sha256": sha(os.path.join(args.q2, "signals.json")),
                  "signals_total": sum(len(v) for v in json.load(open(
                      os.path.join(args.q2, "signals.json"),
                      encoding="utf-8")).values())},
        "source_inheritance_filter": q2_filter_counts(args, books, guard, split),
        "status": ("CANDIDATE-class raw signals, unreviewed; C1-drop is not promotable "
                   "and no omission count may be quoted from it until ORCH-2 re-gates "
                   "on the TASK-020 repair"),
    })

    # ---- q3 supplement
    q3 = supplement_common(args, split, books)
    q3.update({
        "task": "TASK-020 item 1+5b (q3 part) — LAW §8 supplement for runs/m4-q3-format",
        "detector": df.DETECTOR_ID,
        "detector_sha256_at_head": sha(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "det_format.py")),
        "book_store_digest_status": ("N/A for this detector — C2-format never reads the "
                                     "book store (state, not an omission). The store "
                                     "digest above is recorded for the run directory's "
                                     "completeness only."),
        "detector_pin_defect": {
            "original_pin": "c322e053…",
            "defect": ("matches det_format.py at 4425763, not at head; the intervening "
                       "4e114f1 changed only the runner (--set {tuning,holdout} + a "
                       "`set` provenance field)"),
            "attribution_bridge": ("ORCH-2 reproduced the whole run at head and got "
                                   "byte-identical signals.json (86c8f57d…), so the "
                                   "outputs are attributable to unchanged rule logic"),
        },
        "rules": Q3_RULES,
        "config": {"rules": Q3_RULES, "excerpt_chars": df.EXCERPT,
                   "abbreviations": sorted(df.ABBREV)},
        "config_sha256": digest_config({"rules": Q3_RULES, "excerpt_chars": df.EXCERPT,
                                        "abbreviations": sorted(df.ABBREV)}),
        "outputs": {"signals_v1tuning.json": sha(os.path.join(args.q3, "signals.json")),
                    "signals_v2tuning.json": sha(os.path.join(
                        args.q3, "signals-v2tuning.json")),
                    "notes": ("signals.json is the historic v1-tuning run (193 → 49), "
                              "cited by digest only; signals-v2tuning.json is the "
                              "TASK-020-era run over the v2 tuning half (197 → 48)")},
        "source_inheritance_filter": q3_filter(args, books, guard, split),
        "status": ("CANDIDATE-class raw signals, unreviewed; C2-format is not "
                   "promotable and no M6 figure may quote it until ORCH-2 re-gates "
                   "on the TASK-020 repair"),
    })

    q2_sha = q3ev._dump(os.path.join(args.q2, SUPPLEMENT), q2)
    q3_sha = q3ev._dump(os.path.join(args.q3, SUPPLEMENT), q3)
    print("q2 supplement %s (parts %s; filter raw %d → %d, deferred %d)"
          % (q2_sha, {k: v[:8] for k, v in q2["parts"].items()},
             q2["source_inheritance_filter"]["raw"],
             q2["source_inheritance_filter"]["filtered"],
             q2["source_inheritance_filter"]["deferred_holdout"]))
    print("q3 supplement %s (filter raw %d → %d; clean %d → %d)"
          % (q3_sha, q3["source_inheritance_filter"]["run"]["raw"],
             q3["source_inheritance_filter"]["run"]["filtered"],
             q3["source_inheritance_filter"]["clean_set"]["misfires_raw"],
             q3["source_inheritance_filter"]["clean_set"]["misfires_after_filter"]))
    return 0


def verify(args):
    problems = []
    split = q3ev.load_split(args.split)
    books = m5r.parse_book_store(os.path.join(args.corpus, BOOK_STORE_REL))
    guard = q3ev.HoldoutGuard(args.corpus, split["holdout"])
    for path, checker in ((os.path.join(args.q2, SUPPLEMENT),
                           lambda d: q2_filter_counts(args, books, guard, split)),
                          (os.path.join(args.q3, SUPPLEMENT),
                           lambda d: q3_filter(args, books, guard, split))):
        if not os.path.exists(path):
            problems.append("%s missing" % path)
            continue
        doc = json.load(open(path, encoding="utf-8"))
        for key in ("tool_commit", "main_head", "policy_sha256", "book_store_sha256",
                    "corpus_zip_sha256", "config_sha256", "run_utc"):
            if not doc.get(key):
                problems.append("%s lacks %s" % (os.path.basename(path), key))
        if doc["detector_sha256_at_head"] != sha(os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "det_dropword.py" if "q2" in path else "det_format.py")):
            problems.append("%s detector pin stale" % os.path.basename(path))
        fresh = checker(doc)
        committed = doc["source_inheritance_filter"]
        if path.endswith("m4-q2-dropword/" + SUPPLEMENT):
            keys = ("raw", "source_inherited", "filtered", "deferred_holdout")
            if any(committed[k] != fresh[k] for k in keys):
                problems.append("q2 filter counts differ")
        else:
            if (committed["run"]["raw"], committed["run"]["source_inherited"],
                    committed["run"]["filtered"],
                    committed["clean_set"]["misfires_raw"],
                    committed["clean_set"]["source_inherited"],
                    committed["clean_set"]["misfires_after_filter"]) != (
                    fresh["run"]["raw"], fresh["run"]["source_inherited"],
                    fresh["run"]["filtered"],
                    fresh["clean_set"]["misfires_raw"],
                    fresh["clean_set"]["source_inherited"],
                    fresh["clean_set"]["misfires_after_filter"]):
                problems.append("q3 filter counts differ")
    if set(guard.reads) & set(split["holdout"]):
        problems.append("holdout touched")
    if problems:
        for p in problems:
            print("FAIL: %s" % p)
        return 1
    print("TASK-020 supplements verify: OK (both supplements carry the §8 bindings; "
          "filters reproduce; holdout reads 0)")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    v = sub.add_parser("verify")
    for p in (b, v):
        p.add_argument("--corpus", default="corpus")
        p.add_argument("--split", default="tools/HELD-OUT-SPLIT-V2.json")
        p.add_argument("--q2", default="runs/m4-q2-dropword")
        p.add_argument("--q3", default="runs/m4-q3-format")
    b.add_argument("--utc", required=True)
    b.add_argument("--tool-commit", required=True)
    b.add_argument("--main-head", required=True)
    b.add_argument("--policy-sha", required=True)
    a = ap.parse_args(argv)
    return build(a) if a.cmd == "build" else verify(a)


if __name__ == "__main__":
    sys.exit(main())
