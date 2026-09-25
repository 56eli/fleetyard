#!/usr/bin/env python3
"""M4-q3 shipping evidence for C2-format — fixture recall, clean-set run, §8 bindings.

ORCH-2's q3 gate (2026-09-25T20:44Z, `6495a8b`) found the C2-format detector's
*substance* clean (its run reproduced byte-for-byte, all 49 citations exact) but
the *shipping evidence* missing:

  q3.2 no fixture-recall result existed anywhere;
  q3.3 no clean-set run over `fixtures/clean/clean.json` (the known-good book
       passages) and no run over known-good book text;
  q3.4 a documentation gap: the two rejected-rule probes were not published
       verbatim (regex + flags), so "camel-glue 35 hits / 18 files" was not
       reproducible;
  q3.5 the LAW §8 manifest lacked `tool_commit`, `policy_sha256`, `main_head`
       and an output digest, and its `detector_sha256` bound a commit older
       than head.

This tool produces those measurements as one deterministic artefact and nothing
else. It does NOT promote C2-format: the gate's restriction stands (C2-format is
not promotable, its signals stay CANDIDATE, no M6 figure may quote them) until
ORCH-2 re-gates on this evidence.

Discipline built in:

  * **The v2 holdout is never opened.** The sealed split
    `tools/HELD-OUT-SPLIT-V2.json` (sha256 f357ed21… → re-sealed 73d86f0d…)
    is loaded for its *tuning* list only; every transcript read goes through a
    guard that raises `SystemExit` on any holdout name, and the manifest records
    `holdout_reads: []`. Fixture transcripts are forced-to-tuning by the seal, so
    reading them is tuning, not holdout, work.
  * **The historic 193-transcript run is NOT replayed.** 33 of its tuning files
    are members of the v2 holdout; replaying it would open the holdout. The new
    run is over the v2 tuning half (197) and is labelled as such; the historic
    `runs/m4-q3-format/signals.json` (sha256 86c8f57d…) stays as the artefact
    ORCH-2 itself reproduced, cited by digest only.
  * **Outputs are deterministic** given `--utc` (the only volatile input), so a
    verifier can rebuild and compare digests.

Commands:

  build   python3 tools/m4_q3_evidence.py build --corpus corpus \
              --split tools/HELD-OUT-SPLIT-V2.json --out runs/m4-q3-format
  verify  python3 tools/m4_q3_evidence.py verify --corpus corpus \
              --split tools/HELD-OUT-SPLIT-V2.json --out runs/m4-q3-format

Stdlib only, no network, read-only over the corpus and the book store.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import det_format                      # noqa: E402
import fixtures                        # noqa: E402
import loaders                          # noqa: E402
import m5r_reduce as m5r                # noqa: E402

DETECTOR_ID = det_format.DETECTOR_ID
SIGNALS_NAME = "signals-v2tuning.json"
PROV_NAME = "PROVENANCE-V2.json"
EVAL_NAME = "EVAL.json"
CORPUS_ZIP_SHA = "3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db"

# Rejected-rule probes, published verbatim (q3.4's documentation gap). The
# historic census figure ("camel-glue 35 hits / 18 files") was measured over the
# full 230-transcript corpus *before* split v2 and its exact pattern was not
# recorded; it is superseded by this table, recomputed on the v2 tuning half.
PROBES = (
    ("P1-double-word", r"\b(\w+)\s+\1\b", re.IGNORECASE,
     "ordinary spoken repetition (A1-repetition's domain), not an artifact"),
    ("P2-camel-any-internal-capital", r"[a-z][A-Z]", 0,
     "any lowercase directly followed by an uppercase anywhere in the text"),
    ("P3-camel-lowercase-start-word", r"\b[a-z][a-z]*[A-Z]", 0,
     "word starting lowercase that contains an uppercase later"),
    ("P4-camel-classic", r"\b[a-z]+[A-Z][a-z]+\b", 0,
     "lowercase on both sides of the capital (true camel case)"),
    ("P5-camel-lower-upper-run", r"\b[a-z]{2,}[A-Z]{2,}", 0,
     "lowercase run then an uppercase run (dimensionONE-style)"),
)
EXAMPLES_PER_PROBE = 8


class HoldoutGuard:
    """Reads corpus transcripts, refusing any name in the sealed holdout."""

    def __init__(self, corpus_dir, holdout):
        self._texts = m5r.load_transcripts(corpus_dir)
        self.holdout = frozenset(holdout)
        self.reads = []

    def text(self, name):
        # fixture records carry corpus-relative paths; the split carries basenames
        name = os.path.basename(str(name).replace("\\", "/"))
        if name in self.holdout:
            raise SystemExit("C2-format evidence: refusing to read holdout "
                             "transcript %r" % name)
        if name not in self._texts:
            raise SystemExit("C2-format evidence: %r not in corpus" % name)
        self.reads.append(name)
        return self._texts[name]


def load_split(path):
    split = json.load(open(path, encoding="utf-8"))
    missing = [k for k in ("tuning", "holdout", "corpus_files_sha256")
               if k not in split]
    if missing:
        raise SystemExit("C2-format evidence: split lacks %r" % missing)
    overlap = sorted(set(split["tuning"]) & set(split["holdout"]))
    if overlap:
        raise SystemExit("C2-format evidence: split integrity violation %r"
                         % overlap[:3])
    return split


def fixture_recall(confirmed, guard):
    """Which of the confirmed fixtures C2-format fires inside, per fixture.

    Same overlap rule as tools/run_detectors.py:evaluate(): a hit is any signal
    whose byte span intersects the fixture's quoted span. C2-format has no
    seeding mechanism, so every hit is independent by construction.
    """
    out, hits = [], 0
    for fx in confirmed:
        text = guard.text(fx["transcript"])
        a = fx["char_offset"]
        b = a + len(fx["quoted"])
        sigs = [s for s in det_format.detect(text) if s["start"] < b and a < s["end"]]
        if sigs:
            hits += 1
        out.append({
            "fixture": fx["id"],
            "transcript": fx["transcript"],
            "char_offset": a,
            "quoted_len": len(fx["quoted"]),
            "hit": bool(sigs),
            "signals": [{"rule": s["rule"], "start": s["start"],
                         "end": s["end"], "quoted": s["quoted"]}
                        for s in sigs],
        })
    return {"fixtures": len(confirmed), "hits": hits, "detail": out}


def clean_run(clean, books):
    """C2-format over the known-good passages of fixtures/clean/clean.json.

    The clean passages are known-good book text: flagging one is misfiring by
    definition. `materialize_clean` re-verifies each passage's sha256 against the
    book store before it is scored, so a drift in the corpus fails loudly.
    """
    pairs = fixtures.materialize_clean(clean, books)
    fps, detail = [], []
    for rec, text in pairs:
        sigs = det_format.detect(text)
        detail.append({"id": rec["id"], "slug": rec["slug"],
                       "char_offset": rec["char_offset"],
                       "length": rec["length"], "sha256": rec["sha256"],
                       "signals": [{"rule": s["rule"], "start": s["start"],
                                    "end": s["end"], "quoted": s["quoted"]}
                                   for s in sigs]})
        for s in sigs:
            fps.append({"id": rec["id"], "rule": s["rule"],
                        "quoted": s["quoted"], "note": s["note"]})
    return {"passages": len(pairs), "false_positives": len(fps),
            "fp_detail": fps, "detail": detail}


def probe_table(names, guard):
    """Rejected-rule probes, recomputed with the exact pattern + flags on view."""
    texts = {n: guard.text(n) for n in names}
    out = []
    for pid, pattern, flags, note in PROBES:
        rx = re.compile(pattern, flags)
        total, files, examples = 0, 0, []
        for name in sorted(texts):
            found = [m.group(0) for m in rx.finditer(texts[name])]
            if found:
                files += 1
                total += len(found)
                for val in found:
                    if len(examples) < EXAMPLES_PER_PROBE:
                        examples.append(val)
        out.append({"probe": pid, "pattern": pattern,
                    "flags": "re.IGNORECASE" if flags & re.IGNORECASE else "0",
                    "hits": total, "files": files, "note": note,
                    "examples": examples})
    return out


def tuning_run(split, guard):
    per_file, texts, total = {}, {}, 0
    for name in split["tuning"]:
        text = guard.text(name)
        texts[name] = text
        sigs = det_format.detect(text)
        per_file[name] = sigs
        total += len(sigs)
    per_rule = {}
    for sigs in per_file.values():
        for s in sigs:
            per_rule[s["rule"]] = per_rule.get(s["rule"], 0) + 1
    return per_file, total, dict(sorted(per_rule.items())), texts


def book_confound(per_file, texts, books, window=25):
    """Is a signal's surrounding text *the same text* as in the book store?

    The clean-set run raised this question: its single R1 misfire is `power.When`
    inside `power_vs_force__the_hidden_de…`, and that exact glue also exists in
    the book store — the book's own typography. So for every signal of the run
    this compares three nested windows against every book:

      bare    the matched glue itself (short patterns match by chance — a bound,
              not evidence on its own);
      ctx20   the 20 characters around the glue;
      ctx50   the 2x25 characters around the glue (near-verbatim passage share).

    A ctx50 match means the transcript carries the book's text verbatim across
    the artifact, so the transcript cannot be said to have introduced it. This
    restricts what C2-format's signals can be read as; it does not refute that
    the text is glued.
    """
    tiers = ("bare", "ctx20", "ctx50")
    per_rule = {}
    examples = []
    for name in sorted(per_file):
        text = texts[name]
        for sig in per_file[name]:
            a, b = sig["start"], sig["end"]
            probes = {"bare": sig["quoted"],
                      "ctx20": text[max(0, a - 10):b + 10],
                      "ctx50": text[max(0, a - window):b + window]}
            found = {}
            for tier in tiers:
                need = probes[tier]
                if not need:
                    continue
                where = [slug for slug, book in books.items() if need in book]
                if where:
                    found[tier] = where
            if not found:
                continue
            slot = per_rule.setdefault(sig["rule"], {
                "signals": 0, "tiers": {t: 0 for t in tiers}, "books": []})
            slot["signals"] += 1
            for tier in found:
                slot["tiers"][tier] += 1
            slot["books"] = sorted(set(slot["books"]) | {b for v in
                                                         found.values() for b in v})
            if found.get("ctx50") and len(examples) < EXAMPLES_PER_PROBE:
                examples.append({"transcript": name, "rule": sig["rule"],
                                 "quoted": sig["quoted"],
                                 "window": probes["ctx50"],
                                 "books": found["ctx50"][:3]})
    for slot in per_rule.values():
        slot["book_count"] = len(slot["books"])
        slot["books"] = slot["books"][:5]
    total = sum(len(v) for v in per_file.values())
    return {
        "signals_total": total,
        "window_chars": window,
        "per_rule": dict(sorted(per_rule.items())),
        "signals_matching_any_tier": sum(v["signals"] for v in per_rule.values()),
        "signals_ctx50": sum(v["tiers"]["ctx50"] for v in per_rule.values()),
        "signals_ctx20": sum(v["tiers"]["ctx20"] for v in per_rule.values()),
        "examples": examples,
        "reading": ("ctx50 = the transcript carries the book's text verbatim "
                    "across the artifact, so the transcript did not introduce "
                    "it (a restriction on the signal's reading, not a refutation "
                    "that the text is glued); bare matches are shown as an upper "
                    "bound because short patterns match by chance"),
    }


def confound_control(confirmed, books, guard):
    """Calibration for `book_confound`: does the window probe even work?

    Run the same windows over the 15 confirmed fixtures that carry a book
    reference — passages that ARE book text, verified by
    `fixtures.verify_confirmed`. If their windows do not match the book store
    either, the window tiers cannot separate book-derived text from
    transcript-local text on this corpus, and `book_confound`'s negative result
    must be read as UNINFORMATIVE rather than as evidence of independence.
    """
    rows = {"with_book_ref": 0, "quote_in_book": 0, "ctx20_in_book": 0,
            "ctx50_in_book": 0}
    for fx in confirmed:
        br = fx.get("book_ref")
        if not br:
            continue
        rows["with_book_ref"] += 1
        text = guard.text(fx["transcript"])
        book = books.get(br["slug"], "")
        a, b = fx["char_offset"], fx["char_offset"] + len(fx["quoted"])
        if br["quote"] in book:
            rows["quote_in_book"] += 1
        if text[max(0, a - 10):b + 10] in book:
            rows["ctx20_in_book"] += 1
        if text[max(0, a - 25):b + 25] in book:
            rows["ctx50_in_book"] += 1
    rows["verdict"] = ("UNINFORMATIVE" if rows["with_book_ref"] and
                       rows["ctx50_in_book"] == 0 else "informative")
    rows["reading"] = ("known book quotes score 15/15 on the bare tier but 0 on "
                       "the window tiers: transcripts and the book store are "
                       "normalised differently, so ctx20/ctx50 cannot detect "
                       "book-derived text here")
    return rows


def _dump(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    blob = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(blob)
    return m5r.sha256_file(path)


def build(args):
    split = load_split(args.split)
    guard = HoldoutGuard(args.corpus, split["holdout"])
    books = loaders.read_book_store()
    confirmed = fixtures.load_json(fixtures.CONFIRMED_PATH)
    clean = fixtures.load_json(fixtures.CLEAN_PATH)

    per_file, total, per_rule, texts = tuning_run(split, guard)
    signals_path = os.path.join(args.out, SIGNALS_NAME)
    signals_sha = _dump(signals_path, per_file)

    recall = fixture_recall(confirmed, guard)
    clean_res = clean_run(clean, books)
    probes = probe_table(split["tuning"], guard)
    confound = book_confound(per_file, texts, books)
    confound["control"] = confound_control(confirmed, books, guard)

    detector_sha = m5r.sha256_file(os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "det_format.py")))
    tuning_reads = sorted(set(guard.reads) & set(split["tuning"]))

    manifest = {
        "task": "TASK-014 q3 (M4 C2-format) — shipping evidence rebuild",
        "worker": "WORKER-2 (A-2026-09-25-001), lane arena/01a0d9ce-fleetyard",
        "run_utc": args.utc,
        "detector": DETECTOR_ID,
        "detector_sha256": detector_sha,
        "tool_commit": args.tool_commit,
        "main_head": args.main_head,
        "policy_sha256": args.policy_sha,
        "split_file": args.split.replace(os.sep, "/"),
        "split_corpus_files_sha256": split["corpus_files_sha256"],
        "split_counts": split.get("counts"),
        "corpus_dir": args.corpus.replace(os.sep, "/"),
        "corpus_zip_sha256": CORPUS_ZIP_SHA,
        "book_store_sha256": m5r.sha256_file(os.path.join(
            args.corpus, "docdocgo", "html", "merged-book-texts_json_1.js")),
        "transcripts_read_count": len(tuning_reads),
        "transcripts_read_sha256": _list_digest(tuning_reads),
        "holdout_reads": [],
        "holdout_enforced": True,
        "outputs": {"signals_file": SIGNALS_NAME, "signals_sha256": signals_sha,
                    "signals_total": total, "per_rule": per_rule},
        "historic_artefact": {
            "path": "runs/m4-q3-format/signals.json",
            "sha256": "86c8f57dea9443f3b9758add19dbfe01e75b1369b144c74a58d1735b5a8c15ee",
            "note": ("run over the v1 tuning half (193) before split v2; not "
                     "replayed here because 33 of its files are v2-holdout "
                     "members"),
        },
        "status": ("CANDIDATE-class raw signals, unreviewed; PROVISIONAL-UNGATED; "
                   "C2-format is not promotable and these signals may not feed "
                   "any rate or M6 figure until ORCH-2 re-gates"),
    }
    prov_sha = _dump(os.path.join(args.out, PROV_NAME), manifest)

    eval_doc = {
        "task": manifest["task"],
        "detector": DETECTOR_ID,
        "run_utc": args.utc,
        "gate_context": {
            "gate": "ORCH-2 GATES.md 2026-09-25T20:44Z q3 INCOMPLETE",
            "criteria_addressed": ["q3.2 fixture recall", "q3.3 clean set",
                                   "q3.4 rejected-rule probes verbatim",
                                   "q3.5 §8 manifest bindings"],
            "note": ("evidence only; the gate is ORCH-2's to re-run — the "
                     "restriction on C2-format is unchanged by this file"),
        },
        "fixture_recall": recall,
        "clean_set": {"passages": clean_res["passages"],
                      "false_positives": clean_res["false_positives"],
                      "fp_detail": clean_res["fp_detail"],
                      "reading": ("tune-set known-good book passages, in-sample; "
                                  "NOT an independent FP rate (LAW §9)"),
                      "detail": clean_res["detail"]},
        "book_store_confound": confound,
        "rejected_rule_probes": {
            "scope": "v2 tuning half only (%d transcripts)" % len(split["tuning"]),
            "historic_note": ("the pre-v2 census figure (camel-glue 35 / 18 files) "
                              "was measured over all 230 before the v2 seal and its "
                              "exact pattern was not recorded; this table replaces "
                              "it — every probe below is reproducible verbatim"),
            "probes": probes,
        },
        "detector_sha256": detector_sha,
        "tool_commit": args.tool_commit,
        "main_head": args.main_head,
        "policy_sha256": args.policy_sha,
        "signals_file": SIGNALS_NAME,
        "signals_sha256": signals_sha,
        "signals_total": total,
        "per_rule": per_rule,
        "provenance_file": PROV_NAME,
        "provenance_sha256": prov_sha,
        "historic_signals_sha256": _historic_signals_sha(args.out),
        "status": manifest["status"],
    }
    eval_sha = _dump(os.path.join(args.out, EVAL_NAME), eval_doc)
    print("C2-format evidence: %d tuning transcripts, %d signals %s"
          % (len(split["tuning"]), total, per_rule))
    print("fixture recall %d/%d · clean-set FP %d/%d"
          % (recall["hits"], recall["fixtures"],
             clean_res["false_positives"], clean_res["passages"]))
    for p in probes:
        print("probe %-32s %6d hits / %3d files" % (p["probe"], p["hits"],
                                                    p["files"]))
    print("book-store confound: ctx50 %d/%d · ctx20 %d/%d · any %d/%d %s"
          % (confound["signals_ctx50"], confound["signals_total"],
             confound["signals_ctx20"], confound["signals_total"],
             confound["signals_matching_any_tier"], confound["signals_total"],
             confound["per_rule"]))
    print("confound control: %s (book quotes %d/%d in store, window tiers %d/%d)"
          % (confound["control"]["verdict"], confound["control"]["quote_in_book"],
             confound["control"]["with_book_ref"],
             confound["control"]["ctx50_in_book"],
             confound["control"]["with_book_ref"]))
    print("signals %s\nprovenance %s\neval %s" % (signals_sha, prov_sha, eval_sha))
    return 0


def _historic_signals_sha(out_dir):
    path = os.path.join(out_dir, "signals.json")
    return m5r.sha256_file(path) if os.path.exists(path) else None


def _list_digest(names):
    import hashlib
    h = hashlib.sha256()
    for n in names:
        h.update(n.encode("utf-8") + b"\n")
    return h.hexdigest()


def verify(args):
    """Rebuild from the corpus and compare against the committed artefacts."""
    problems = []
    split = load_split(args.split)
    guard = HoldoutGuard(args.corpus, split["holdout"])
    books = loaders.read_book_store()
    committed = json.load(open(os.path.join(args.out, EVAL_NAME),
                               encoding="utf-8"))
    per_file, total, per_rule, texts = tuning_run(split, guard)
    committed_signals = json.load(open(os.path.join(args.out, SIGNALS_NAME),
                                       encoding="utf-8"))
    if committed_signals != per_file:
        problems.append("signals content differs from a fresh run")
    if committed["signals_total"] != total or committed["per_rule"] != per_rule:
        problems.append("signal totals differ: %r vs %r"
                        % (committed["per_rule"], per_rule))
    recall = fixture_recall(fixtures.load_json(fixtures.CONFIRMED_PATH), guard)
    if (committed["fixture_recall"]["hits"],
            committed["fixture_recall"]["fixtures"]) != (recall["hits"],
                                                         recall["fixtures"]):
        problems.append("fixture recall differs")
    clean_res = clean_run(fixtures.load_json(fixtures.CLEAN_PATH), books)
    if (committed["clean_set"]["false_positives"],
            committed["clean_set"]["passages"]) != (clean_res["false_positives"],
                                                    clean_res["passages"]):
        problems.append("clean-set false positives differ")
    probes = probe_table(split["tuning"], guard)
    if committed["rejected_rule_probes"]["probes"] != probes:
        problems.append("rejected-rule probe table differs")
    confound = book_confound(per_file, texts, books)
    confound["control"] = confound_control(
        fixtures.load_json(fixtures.CONFIRMED_PATH), books, guard)
    if (committed["book_store_confound"]["signals_ctx50"],
            committed["book_store_confound"]["signals_ctx20"],
            committed["book_store_confound"]["per_rule"]) != (
            confound["signals_ctx50"], confound["signals_ctx20"],
            confound["per_rule"]):
        problems.append("book-store confound result differs")
    if committed["book_store_confound"]["control"] != confound["control"]:
        problems.append("confound control result differs")
    holdout_touched = sorted(set(guard.reads) & set(split["holdout"]))
    if holdout_touched:
        problems.append("holdout touched: %r" % holdout_touched[:3])
    if os.path.basename(args.split) == "HELD-OUT-SPLIT-V2.json":
        if committed["signals_sha256"] != m5r.sha256_file(
                os.path.join(args.out, SIGNALS_NAME)):
            problems.append("signals digest does not match the file on disk")
    if problems:
        for p in problems:
            print("FAIL: %s" % p)
        return 1
    print("C2-format evidence verify: OK (%d transcripts, %d signals %s; "
          "fixture %d/%d; clean FP %d/%d; holdout reads 0)"
          % (len(set(guard.reads)), total, per_rule, recall["hits"],
             recall["fixtures"], clean_res["false_positives"],
             clean_res["passages"]))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    v = sub.add_parser("verify")
    for p in (b, v):
        p.add_argument("--corpus", default="corpus")
        p.add_argument("--split", default="tools/HELD-OUT-SPLIT-V2.json")
        p.add_argument("--out", default="runs/m4-q3-format")
    b.add_argument("--utc", required=True)
    b.add_argument("--tool-commit", required=True)
    b.add_argument("--main-head", required=True)
    b.add_argument("--policy-sha", required=True)
    a = ap.parse_args(argv)
    return build(a) if a.cmd == "build" else verify(a)


if __name__ == "__main__":
    sys.exit(main())
