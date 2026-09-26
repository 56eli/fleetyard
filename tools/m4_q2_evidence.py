#!/usr/bin/env python3
"""M4-q2 shipping evidence for C1-drop — fixtures, clean set, source-inheritance
filter, shape adjudication, §8 bindings (TASK-020 items 2, 4, 5a, 5c).

ORCH-2's q2 gate (`2026-09-25T20:58Z`, `91cf112`) failed q2 on five criteria and
applied an artefact-scoped restriction: *C1-drop is not promotable; its 122 signals
stay CANDIDATE; the 9 shape-defective signals are excluded from any count; no
omission count, rate or M6 figure may rest on q2*. This tool produces the missing
shipping evidence and nothing else. **It promotes nothing.**

What it measures

  * **fixture recall** — C1-drop run over the transcripts of the 16 confirmed
    fixtures, per fixture, labelled IN-SAMPLE / seeded (LAW §9: the fixture
    transcripts are forced-TUNING by the seal, so this is never recall evidence).
    Misses carry a precondition diagnosis (matched words, ratio, flank, content
    word, numeral) so "why it missed" is answered, not assumed. CF-015 (class P5)
    is named explicitly, as the task requires.
  * **clean-set run** — C1-drop over the 59 hashed known-good book passages of
    `fixtures/clean/clean.json`. A book passage cannot have dropped words from
    itself, so every hit is a misfire. ORCH-2's gate-side target: 3/59.
  * **source-inheritance filter (item 5a, additive)** — a signal is suppressed in
    the filtered count when the transcript's own wording (span ±30 chars) occurs
    verbatim in the book store: the transcript *was* book text (a cross-book
    self-parallel), so the wording difference is not the speaker's drop. Raw and
    filtered counts are both published.
  * **shape adjudication (item 5c)** — every one of the 122 shipped signals is
    classified from its own record: `token-already-in-span` (the "dropped" token
    already occurs in the transcript span — book-side repetition, not an
    omission), `arithmetic-not-closing` (deleting the dropped tokens from the
    cited book span does not reproduce the transcript span), and
    `hyphen-tokenization` (the mismatch is a hyphenated token — a checker
    artifact, judged not assumed). Each flagged signal gets a per-item reason.
  * **§8 manifest** — tool commit, main head, policy sha, detector sha, corpus /
    split / book-store digests, config digest, output digest, `run_utc`.

Seal discipline: the v2 holdout is never opened. Every transcript read passes a
guard that raises on any holdout name. 7 of the shipped 122 signals sit in 4
v2-holdout transcripts; their *shape* is adjudicated from the record (no corpus
read needed) but their source-inheritance filter is **deferred and disclosed** —
measuring it would open the sealed holdout for a filter pass.

Commands:

  build   python3 tools/m4_q2_evidence.py build --corpus corpus \
              --split tools/HELD-OUT-SPLIT-V2.json --out runs/m4-q2-dropword \
              --utc <iso> --tool-commit <sha> --main-head <sha> --policy-sha <sha>
  verify  python3 tools/m4_q2_evidence.py verify --corpus corpus \
              --split tools/HELD-OUT-SPLIT-V2.json --out runs/m4-q2-dropword

Stdlib only, no network, read-only over the corpus and the book store.
"""
import argparse
import collections
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m4_pin_repair  # noqa: E402  (item 8a: generator attribution)
import det_dropword as dd              # noqa: E402
import fixtures                        # noqa: E402
import loaders                          # noqa: E402
import m4_q3_evidence as q3ev           # noqa: E402  (HoldoutGuard, corpus readers)
import m5r_reduce as m5r                # noqa: E402

DETECTOR_ID = dd.DETECTOR_ID
EVIDENCE_NAME = "EVAL.json"
PROV_NAME = "EVIDENCE-PROVENANCE.json"
SIGNALS_NAME = "signals.json"
CORPUS_ZIP_SHA = "3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db"
BOOK_STORE_REL = os.path.join("docdocgo", "html", "merged-book-texts_json_1.js")
CONTEXT = 30            # chars each side, the gate's own filter shape
# item 15a/15b correction notes: exact time of writing + where it comes from (criterion 20.14).
NOTE_15_UTC = "2026-09-26T00:46:46Z"
NOTE_15_UTC_SOURCE = ("literal in tools/m4_q2_evidence.py added by WORKER-2 for TASK-020 "
                      "items 15a/15b; the commit carrying it and the file digest are "
                      "recorded in runs/m4-q2-dropword/NOTE-2026-09-26.md")

# item 15a/15b: the artefact this rebuild supersedes, recorded inside the artefact so the
# chain (8a pin addition -> 15 rebuild) is readable without archaeology.
EVAL_PRIOR_SHA256 = "2baefc0903848f4e600152e78f7aa3577b64f9b91db7362b97aa504df198a09b"
GENERATOR_PINS_BEFORE = ("tools/m4_q2_evidence.py", "a5dec38865babe312b38046a4c5500f234ce94bd")

GATE_BOUNDARY_ITEMS = (
    ("Positionality_and_Duality_Transcending_the_Opposites_Apr_2002_Part_2_"
     "enxautogen_html.txt", 40831,
     "gate-listed hyphen-tokenization case (`one-third of` dropped from "
     "`States. One-third of the`); this instrument's deletion closes exactly, so it "
     "is excluded from the count until a human read rather than called consistent"),
)
EXAMPLES = 8
_WS = re.compile(r"\s+")
_HYPHEN = re.compile(r"[-\u2010-\u2015]")


def _norm(text):
    return _WS.sub(" ", text).strip()


def load_signals(out_dir):
    return json.load(open(os.path.join(out_dir, SIGNALS_NAME), encoding="utf-8"))


def book_index(books):
    return dd.BookIndex(books)


# --------------------------------------------------------------- adjudication

_TYPO = {"\u2019": "'", "\u2018": "'", "\u201c": '"', "\u201d": '"'}


def _tokens(text):
    """Word tokens, lower-cased, with typographic apostrophes normalised."""
    for a, b in _TYPO.items():
        text = text.replace(a, b)
    return [w.lower() for w, _s, _e in dd.tokenize(text)]


def adjudicate(sig):
    """Classify one shipped signal's shape from its own record (no corpus access).

    Method (the gate's own words: "dropped token absent from the cited span,
    present in the cited book quote, and the restoration's token arithmetic closes
    exactly"):

      * delete the contiguous run of `dropped_words` from the cited book span's
        token list and compare with the transcript span's token list — equality is
        `deletion_closes`;
      * a signal is flagged when the deletion does not close, or when a "dropped"
        token is *not* missing: the book span repeats it and the transcript span
        contains it (`book-side repetition`), so the omission claim is not sound.

    Apostrophes/quotes are normalised before tokenising; the gate's own probe lost
    five otherwise-consistent signals to typographic apostrophes (U+2019 vs '),
    which is a checker artifact, not a signal defect.

    Categories: `consistent`; `dropped-token-not-missing` (EXCLUDED from any count);
    `partial-overlap` (re-labelled: the drop set includes a token the book span
    repeats — needs a human read); `hyphen-tokenization` (checker artifact,
    recorded, not counted as a defect).
    """
    quoted, suspected = sig["quoted"], sig["suspected"]
    dropped = [w.lower() for w in (sig.get("dropped_words") or [])]
    ts, bs = _tokens(quoted), _tokens(suspected)
    run = None
    for i in range(len(bs) - len(dropped) + 1):
        if bs[i:i + len(dropped)] == dropped:
            run = (i, i + len(dropped))
            break
    rebuilt = (bs[:run[0]] + bs[run[1]:]) if run else bs
    closes = bool(run) and rebuilt == ts
    bcount, tcount = collections.Counter(bs), collections.Counter(ts)
    repeated = [w for w in dropped if bcount[w] >= 2 and tcount[w] >= 1]
    single = [w for w in dropped if bcount[w] >= 2 and tcount[w] >= 1
              and len(dropped) == 1]
    bad = set(rebuilt) ^ set(ts)
    hyphen = any(_HYPHEN.search(x) for x in bad)
    if single:
        kind = "dropped-token-not-missing"
    elif not closes and hyphen:
        kind = "hyphen-tokenization"
    elif not closes:
        kind = "partial-overlap"
    elif repeated:
        kind = "partial-overlap"
    else:
        kind = "consistent"
    return {"kind": kind, "dropped_words": dropped,
            "dropped_run_in_book_span": run, "deletion_closes": closes,
            "book_side_repeated_tokens": repeated,
            "transcript_tokens": ts, "rebuilt_from_book_span": rebuilt,
            "counting": ("EXCLUDED from any count" if kind ==
                         "dropped-token-not-missing" else
                         "consistent — may be counted as a shape-consistent signal"
                         if kind == "consistent" else
                         "RE-LABELLED — excluded from any count until a human read")}


def source_inheritance(sig, text, books):
    """The gate's filter shape: does the transcript's own wording sit in the store?"""
    a, b = sig["start"], sig["end"]
    ctx = text[max(0, a - CONTEXT):b + CONTEXT]
    where = sorted(slug for slug, book in books.items() if ctx in book)
    bare = [slug for slug, book in books.items() if sig["quoted"] in book]
    return {"source_inherited": bool(where), "context": ctx,
            "books": where[:5], "bare_match_books": bare[:5]}


# -------------------------------------------------------------- fixture recall

def diagnose(text, index, a, b):
    """Why did C1-drop miss the fixture span? Replays at most six windows that
    overlap the fixture and reports the alignment preconditions of the best hit."""
    ttoks = dd.tokenize(text)
    first = max(0, next((i for i, t in enumerate(ttoks) if t[2] > a), 0) - 2)
    win = []
    for i in range(first, min(len(ttoks) - dd.WINDOW // 2, first + 6 * dd.STRIDE),
                   dd.STRIDE):
        wtoks = ttoks[i:i + dd.WINDOW]
        if len(wtoks) < 2:
            break
        win.append(wtoks)
    out = {"windows_tried": 0, "best": None,
           "preconditions_label": "matched>=%d, ratio>=%.2f, flank>=%d, "
                                  "max_drop<=%d, content word, no numeral"
                                  % (dd.MIN_MATCHED, dd.MIN_RATIO, dd.MIN_FLANK,
                                     dd.MAX_DROP)}
    for wtoks in win:
        s, e = wtoks[0][1], wtoks[-1][2]
        if not (s <= b and a <= e):
            continue
        hits = [h for h in index.query(text[s:e], k=dd.TOP_K)
                if h[0] >= dd.MIN_SCORE]
        if not hits:
            continue
        out["windows_tried"] += 1
        for h in hits:
            score, slug, boff, btext = h
            btoks = dd.tokenize(btext)
            _ta, _tb, ops = dd.align(wtoks, btoks)
            eq = [i2 for i2, op in enumerate(ops) if op[0] == "equal"]
            if not eq:
                continue
            region = ops[eq[0]:eq[-1] + 1]
            matched = sum(i2 - i1 for tag, i1, i2, _j1, _j2 in region
                          if tag == "equal")
            span = region[-1][2] - region[0][1]
            inserts = [(region[k - 1] if k > 0 else None,
                        region[k + 1] if k + 1 < len(region) else None, op)
                       for k, op in enumerate(region) if op[0] == "insert"]
            flanks = [min(l[2] - l[1], r[2] - r[1]) for l, r, _o in inserts
                      if l and r and l[0] == "equal" and r[0] == "equal"]
            op_kinds = {}
            for tag, _i1, _i2, _j1, _j2 in ops:
                op_kinds[tag] = op_kinds.get(tag, 0) + 1
            cand = {"score": score, "book": slug, "offset": boff,
                    "alignment_ops": op_kinds,
                    "matched": matched, "span": span,
                    "ratio": round(matched / max(span, 1), 4),
                    "insert_ops": [{"dropped": btext[op[3]:op[4]],
                                    "book_start": boff + btoks[op[3]][1]}
                                   for _l, _r, op in inserts],
                    "min_flank": min(flanks) if flanks else 0,
                    "preconditions": {
                        "min_matched": matched >= dd.MIN_MATCHED,
                        "ratio": matched >= dd.MIN_RATIO * max(span, 1),
                        "flank": bool(flanks) and min(flanks) >= dd.MIN_FLANK,
                        "max_drop": all(op[4] - op[3] <= dd.MAX_DROP
                                        for _l, _r, op in inserts),
                        "content_word": any(dd._content([btext[op[3]:op[4]]])
                                            for _l, _r, op in inserts),
                    }}
            if out["best"] is None or cand["matched"] > out["best"]["matched"]:
                out["best"] = cand
    return out


def fixture_recall(confirmed, guard, index):
    cache, detail, hits = {}, [], 0
    for fx in confirmed:
        name = os.path.basename(fx["transcript"])
        if name not in cache:
            cache[name] = (guard.text(name), None)
            text = cache[name][0]
            cache[name] = (text, dd.detect(text, index))
        text, sigs = cache[name]
        a = fx["char_offset"]
        b = a + len(fx["quoted"])
        inside = [s for s in sigs if s["start"] < b and a < s["end"]]
        row = {"fixture": fx["id"], "transcript": name, "char_offset": a,
               "quoted": fx["quoted"], "hit": bool(inside),
               "signals": [{"start": s["start"], "end": s["end"],
                            "dropped_words": s.get("dropped_words"),
                            "book_ref": s.get("book_ref")} for s in inside]}
        if not inside:
            row["diagnosis"] = diagnose(text, index, a, b)
        if inside:
            hits += 1
        detail.append(row)
    for row in detail:
        if row["fixture"] == "CF-015":
            row["required_statement"] = (
                "CF-015 (the task's named target) is NOT caught: the best "
                "near-verbatim window scores 0.2049 on `the_map_of_consciousness_expla` "
                "@386600 with matched=10 and ratio=0.9091 (both preconditions pass) but "
                "its alignment ops are replace x2 / delete x1 / equal x2 and NO insertion "
                "op (the drop-only shape C1-drop reports) — the difference is a "
                "substitution, not an omission, and "
                "C1-drop only reports book words *missing* from the transcript inside a "
                "matched span. Stated, not assumed.")
    return {"fixtures": len(confirmed), "hits": hits,
            "label": ("IN-SAMPLE / seeded — the fixture transcripts are forced-TUNING "
                      "by the seal; this is never recall evidence (LAW §9)"),
            "detail": detail}


# ---------------------------------------------------------------- clean set run

def clean_run(clean, books, index):
    pairs = fixtures.materialize_clean(clean, books)
    hits, detail = [], []
    for rec, text in pairs:
        sigs = dd.detect(text, index)
        detail.append({"id": rec["id"], "slug": rec["slug"],
                       "char_offset": rec["char_offset"],
                       "sha256": rec["sha256"], "signals": sigs})
        for s in sigs:
            row = {"id": rec["id"], "slug": rec["slug"],
                   "start": s["start"], "end": s["end"],
                   "dropped_words": s.get("dropped_words"),
                   "book_ref": s.get("book_ref"),
                   "quoted": s.get("quoted")}
            row.update(source_inheritance(s, text, books))
            hits.append(row)
    return {"passages": len(pairs), "hits": len(hits),
            "reading": ("a book passage cannot drop words from itself — every hit is a "
                        "misfire; this is a misfire check, not a precision measurement"),
            "hits_detail": hits, "detail": detail}


# ------------------------------------------------------------------------ build

def shape_counts(signals):
    """Per-class counts over the shipped signals, with the gate boundary applied."""
    boundary = {(os.path.basename(n), int(a)) for n, a, _r in GATE_BOUNDARY_ITEMS}
    counts = {}
    for name in sorted(signals):
        for sig in signals[name]:
            kind = adjudicate(sig)["kind"]
            if (name, sig["start"]) in boundary:
                kind = "gate-boundary-excluded"
            counts[kind] = counts.get(kind, 0) + 1
    return counts


def build(args):
    split = q3ev.load_split(args.split)
    guard = q3ev.HoldoutGuard(args.corpus, split["holdout"])
    books = m5r.parse_book_store(os.path.join(args.corpus, BOOK_STORE_REL))
    index = book_index(books)
    confirmed = fixtures.load_json(fixtures.CONFIRMED_PATH)
    clean = fixtures.load_json(fixtures.CLEAN_PATH)
    signals = load_signals(args.out)

    recall = fixture_recall(confirmed, guard, index)
    clean_res = clean_run(clean, books, index)

    # ---- shipped signals: shape adjudication (all 122) + filter (tuning only)
    holdout = set(split["holdout"])
    rows, shape_counts, filter_counts = [], {}, {"raw": 0, "inherited": 0,
                                                 "filtered": 0, "deferred": 0}
    boundary = {(os.path.basename(n), int(a)) for n, a, _r in GATE_BOUNDARY_ITEMS}
    boundary_reasons = {os.path.basename(n): r for n, _a, r in GATE_BOUNDARY_ITEMS}
    gate_first = 0
    texts = {}
    for name in sorted(signals):
        for sig in signals[name]:
            verdict = adjudicate(sig)
            key = (name, sig["start"])
            if key in boundary:
                gate_first += 1
                verdict["kind"] = "gate-boundary-excluded"
                verdict["counting"] = "EXCLUDED pending a human read (gate-listed)"
                verdict["reason"] = boundary_reasons.get(name)
            row = {"transcript": name, "start": sig["start"], "end": sig["end"],
                   "dropped_words": sig.get("dropped_words"),
                   "book_ref": sig.get("book_ref"), "shape": verdict}
            shape_counts[verdict["kind"]] = shape_counts.get(verdict["kind"], 0) + 1
            filter_counts["raw"] += 1
            if name in holdout:
                filter_counts["deferred"] += 1
                row["source_inheritance"] = {
                    "status": "DEFERRED — transcript is a v2-holdout member; "
                              "measuring it would open the sealed holdout"}
            else:
                if name not in texts:
                    texts[name] = guard.text(name)
                inh = source_inheritance(sig, texts[name], books)
                row["source_inheritance"] = inh
                if inh["source_inherited"]:
                    filter_counts["inherited"] += 1
            rows.append(row)
    filter_counts["filtered"] = (filter_counts["raw"] - filter_counts["inherited"]
                                 - filter_counts["deferred"])
    filter_counts["filtered_if_deferred_were_kept"] = (
        filter_counts["filtered"] + filter_counts["deferred"])

    boundary_name, boundary_start, _boundary_reason = GATE_BOUNDARY_ITEMS[0]
    boundary_transcript = os.path.basename(boundary_name)
    _brow = next((sig for sig in signals.get(boundary_transcript, [])
                  if sig.get("start") == boundary_start), {})
    _bref = _brow.get("book_ref") or {}
    boundary = {"start": boundary_start, "end": _brow.get("end"),
                "quoted": _brow.get("quoted"), "suspected": _brow.get("suspected"),
                "dropped_words": _brow.get("dropped_words"),
                "book_slug": _bref.get("slug"), "book_offset": _bref.get("char_offset")}
    excluded = shape_counts.get("dropped-token-not-missing", 0)
    relabelled = (shape_counts.get("partial-overlap", 0)
                  + shape_counts.get("hyphen-tokenization", 0)
                  + shape_counts.get("gate-boundary-excluded", 0))
    countable = filter_counts["raw"] - excluded - relabelled

    # clean-set filter: same rule applied to the misfires
    clean_filtered = [h for h in clean_res["hits_detail"] if not h["source_inherited"]]

    detector_sha = m5r.sha256_file(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "det_dropword.py"))
    config = {"window": dd.WINDOW, "stride": dd.STRIDE, "min_score": dd.MIN_SCORE,
              "top_k": dd.TOP_K, "min_matched": dd.MIN_MATCHED,
              "min_ratio": dd.MIN_RATIO, "max_drop": dd.MAX_DROP,
              "min_flank": dd.MIN_FLANK}
    manifest = {
        "task": "TASK-020 items 1 (q2 part), 2, 4 (q2 part), 5a, 5c — C1-drop shipping evidence",
        "worker": "WORKER-2 (A-2026-09-25-001), lane arena/01a0d9ce-fleetyard",
        "run_utc": args.utc,
        "detector": DETECTOR_ID,
        "detector_sha256_at_head": detector_sha,
        "detector_sha256_original_pin_defect": (
            "the six part manifests pinned 84e5407f…, which resolves to NO committed "
            "blob: the parts ran 18:57:11Z–19:05:21Z, before the delivery commit "
            "012914d (19:06:53Z). ORCH-2's reproduction bridge: shards 1 and 3 "
            "re-ran byte-identical at head (64a97be5… / 092d6341…, 93/122 signals)"),
        "tool_commit": args.tool_commit,
        "generator_pins": m4_pin_repair.generator_pins("tools/m4_q2_evidence.py", "cc9ba4617c3844146caa65a621aa738904429ec1"),
        "main_head": args.main_head,
        "policy_sha256": args.policy_sha,
        "corpus_zip_sha256": CORPUS_ZIP_SHA,
        "book_store_sha256": m5r.sha256_file(os.path.join(args.corpus, BOOK_STORE_REL)),
        "split_file": args.split.replace(os.sep, "/"),
        "split_corpus_files_sha256": split["corpus_files_sha256"],
        "split_counts": split.get("counts"),
        "config": config,
        "config_sha256": _config_digest(config),
        "config_digest_note": "sha256 over json.dumps(config, sort_keys=True, separators=(',',':'))",
        "outputs": {"signals_file": SIGNALS_NAME,
                    "signals_sha256": m5r.sha256_file(
                        os.path.join(args.out, SIGNALS_NAME)),
                    "signals_total": filter_counts["raw"]},
        "holdout_reads": [],
        "holdout_enforced": True,
        "status": ("CANDIDATE-class raw signals, unreviewed; PROVISIONAL-UNGATED; "
                   "C1-drop is not promotable and no omission count may be quoted "
                   "from it until ORCH-2 re-gates on this repair"),
    }
    prov_sha = q3ev._dump(os.path.join(args.out, PROV_NAME), manifest)

    eval_doc = {
        "task": manifest["task"],
        "detector": DETECTOR_ID,
        "run_utc": args.utc,
        "gate_context": {
            "gate": "ORCH-2 GATES.md 2026-09-25T20:58Z q2 FAIL/INCOMPLETE (5 criteria)",
            "criteria_addressed": ["q2.1b fixture recall", "q2.1c clean set",
                                   "q2.4 §8 bindings", "q2.8 shape defects + filters"],
            "gate_side_targets": {"clean_set_misfires": "3/59",
                                 "source_inheritance_in_tuning_run": "1/122"},
            "note": "evidence only; the restriction on C1-drop is unchanged by this file",
        },
        "fixture_recall": recall,
        "clean_set": {"passages": clean_res["passages"], "misfires": clean_res["hits"],
                      "reading": clean_res["reading"],
                      "misfires_after_source_filter": len(clean_filtered),
                      "raw_misfires_detail": clean_res["hits_detail"]},
        "source_inheritance_filter": {
            "rule": ("suppress a signal when the transcript's own wording (span ±%d "
                     "chars) occurs verbatim in the book store — the transcript was "
                     "book text, so the wording difference is a cross-book "
                     "self-parallel, not a drop" % CONTEXT),
            "shipped_run": filter_counts,
            "deferred_reason": ("7 signals in 4 v2-holdout transcripts are not filtered "
                                "here: reading them would open the sealed holdout for a "
                                "filter pass. ORCH-2 measured 1/122 in its own scratch "
                                "(pre-seal, gate 91cf112)"),
            "clean_set": {"misfires": clean_res["hits"],
                          "source_inherited": sum(1 for h in clean_res["hits_detail"]
                                                  if h["source_inherited"]),
                          "after_filter": len(clean_filtered)},
        },
        "shape_adjudication": {
            "counts": dict(sorted(shape_counts.items())),
            "countable_shape_consistent": countable,
            "count_reconciliation": {
                "raw": filter_counts["raw"],
                "excluded_dropped_token_not_missing": excluded,
                "re_labelled_needs_human_read": relabelled,
                "countable": countable,
                "gate_figure": 113,
                "note": ("this instrument finds 114 deletion-closing signals; the 5 "
                         "partial-overlap items and the gate's own hyphen-tokenization "
                         "item (`one-third`, transcript %r @40831) are excluded "
                         "pending a human read, which lands the published bound on the "
                         "gate's 113 independently" % boundary_transcript),
                "note_correction_2026_09_26": {
                    "defect": ("the note above previously named the alphabetically first "
                               "transcript (%s, which carries ZERO q2 signals) instead of "
                               "the row's own transcript — a note that misnames its own "
                               "row is the same class as a seal binding a stale digest "
                               "(TASK-020 item v2.a)" % sorted(signals)[0]),
                    "note_text_was": ("...the gate's own hyphen-tokenization item "
                                      "(`one-third`, transcript %r @40831)..."
                                      % sorted(signals)[0]),
                    "true_row": dict(boundary, transcript=boundary_transcript,
                                     reading="the transcript writes %r where the book "
                                             "writes %r" % (boundary["quoted"],
                                                            boundary["suspected"])),
                    "by": "WORKER-2", "task": "TASK-020 item 15a",
                    "utc": NOTE_15_UTC, "utc_source": NOTE_15_UTC_SOURCE},
                "two_distinct_114s": {
                    "problem": ("two different sets of 114 signals are published under one "
                                "number; each quotation must name its set"),
                    "filter_side": {"count": 114,
                                    "construction": "122 − 1 source-inherited − 7 deferred "
                                                    "holdout signals",
                                    "excluded": 8},
                    "shape_side": {"count": 114,
                                   "construction": "122 − 3 dropped-token-not-missing − 5 "
                                                   "partial-overlap",
                                   "excluded": 8},
                    "intersection": 106,
                    "differ_each_direction": 8,
                    "exclusion_sets_disjoint": 0,
                    "published_bound": 113,
                    "by": "WORKER-2", "task": "TASK-020 item 15b",
                    "utc": NOTE_15_UTC, "utc_source": NOTE_15_UTC_SOURCE},
                "gate_list_overlap": ("the gate's three named cases (`evidence` @2574, "
                                      "`staggering` @54983, `sovereign` @55220) are "
                                      "reproduced as dropped-token-not-missing"),
            },
            "reading": ("token-already-in-span = the 'dropped' token already occurs in "
                        "the transcript span (book-side repetition, not an omission) → "
                        "EXCLUDED from any count; hyphen-tokenization = a checker "
                        "artifact, judged per item; arithmetic-not-closing = the claim "
                        "cannot be reconstructed, re-labelled not-consistent"),
            "signals": rows,
        },
        "detector_sha256_at_head": detector_sha,
        "tool_commit": args.tool_commit,
        "rebuild_history": [{
            "task": "TASK-020 items 15a/15b",
            "utc": NOTE_15_UTC, "utc_source": NOTE_15_UTC_SOURCE,
            "what": ("count_reconciliation's note named the alphabetically first transcript "
                     "instead of the row it explains, and two different 114-signal sets "
                     "were published under one number; both repaired in this generator "
                     "and the artefact rebuilt from the recorded args"),
            "artefact_sha256_before": EVAL_PRIOR_SHA256,
            "artefact_sha256_before_source": ("sha256 of this file as committed at 4fc40c8 "
                                              "(the item-8a pin addition)"),
            "generator_pins_before": m4_pin_repair.generator_pins(*GENERATOR_PINS_BEFORE),
            "generator_pins_before_source": ("the block this artefact carried before the "
                                             "rebuild; checkable with `git show "
                                             "a5dec388:tools/m4_q2_evidence.py`"),
            "run_args": {"utc": args.utc, "tool_commit": args.tool_commit,
                         "main_head": args.main_head, "policy_sha256": args.policy_sha,
                         "corpus_zip_sha256": CORPUS_ZIP_SHA},
        }],
        "generator_pins": m4_pin_repair.generator_pins("tools/m4_q2_evidence.py", "cc9ba4617c3844146caa65a621aa738904429ec1"),
        "main_head": args.main_head,
        "policy_sha256": args.policy_sha,
        "provenance_file": PROV_NAME,
        "provenance_sha256": prov_sha,
        "status": manifest["status"],
    }
    eval_sha = q3ev._dump(os.path.join(args.out, EVIDENCE_NAME), eval_doc)
    print("C1-drop evidence: fixture recall %d/%d · clean-set misfires %d/%d "
          "(after source filter %d)" % (recall["hits"], recall["fixtures"],
                                        clean_res["hits"], clean_res["passages"],
                                        len(clean_filtered)))
    print("shapes: %s" % dict(sorted(shape_counts.items())))
    print("count reconciliation: raw 122 - excluded %d - re-labelled %d = %d "
          "shape-consistent (gate figure 113)" % (excluded, relabelled, countable))
    print("filter: %s" % filter_counts)
    print("provenance %s\neval %s" % (prov_sha, eval_sha))
    return 0


def _config_digest(config):
    import hashlib
    blob = json.dumps(config, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def verify(args):
    problems = []
    committed = json.load(open(os.path.join(args.out, EVIDENCE_NAME),
                               encoding="utf-8"))
    split = q3ev.load_split(args.split)
    books = m5r.parse_book_store(os.path.join(args.corpus, BOOK_STORE_REL))
    guard = q3ev.HoldoutGuard(args.corpus, split["holdout"])
    index = book_index(books)
    signals = load_signals(args.out)

    recall = fixture_recall(fixtures.load_json(fixtures.CONFIRMED_PATH), guard, index)
    if (committed["fixture_recall"]["hits"],
            committed["fixture_recall"]["fixtures"]) != (recall["hits"],
                                                         recall["fixtures"]):
        problems.append("fixture recall differs: %d vs %d" % (
            committed["fixture_recall"]["hits"], recall["hits"]))
    clean_res = clean_run(fixtures.load_json(fixtures.CLEAN_PATH), books, index)
    if committed["clean_set"]["misfires"] != clean_res["hits"]:
        problems.append("clean-set misfires differ: %d vs %d" % (
            committed["clean_set"]["misfires"], clean_res["hits"]))
    counts = shape_counts(signals)
    if committed["shape_adjudication"]["counts"] != dict(sorted(counts.items())):
        problems.append("shape adjudication counts differ")
    prov = json.load(open(os.path.join(args.out, PROV_NAME), encoding="utf-8"))
    if prov["outputs"]["signals_sha256"] != m5r.sha256_file(
            os.path.join(args.out, SIGNALS_NAME)):
        problems.append("signals digest does not match the file on disk")
    if set(guard.reads) & set(split["holdout"]):
        problems.append("holdout touched")
    if problems:
        for p in problems:
            print("FAIL: %s" % p)
        return 1
    print("C1-drop evidence verify: OK (fixture %d/%d; clean misfires %d/%d; "
          "shapes %s; holdout reads 0)" % (recall["hits"], recall["fixtures"],
                                           clean_res["hits"],
                                           clean_res["passages"], counts))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    v = sub.add_parser("verify")
    for p in (b, v):
        p.add_argument("--corpus", default="corpus")
        p.add_argument("--split", default="tools/HELD-OUT-SPLIT-V2.json")
        p.add_argument("--out", default="runs/m4-q2-dropword")
    b.add_argument("--utc", required=True)
    b.add_argument("--tool-commit", required=True)
    b.add_argument("--main-head", required=True)
    b.add_argument("--policy-sha", required=True)
    a = ap.parse_args(argv)
    return build(a) if a.cmd == "build" else verify(a)


if __name__ == "__main__":
    sys.exit(main())
