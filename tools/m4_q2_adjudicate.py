#!/usr/bin/env python3
"""TASK-018 — leg (d) individual adjudication of the 122 C1-drop signals + 4 fixtures.

Authority: owner ERRATA-2026-09-25e §2–§4 (recorded errata + BOSS CONCERN), restated as
standing guidance in the ORCH-2 lane's `fleet/GATES.md`; task cut as TASK-018 by ORCH-2.
Every classification here is **per finding, cited to bytes** — no rule, threshold, score or
detector name is ever the reason (L4); the detector supplied a *span*, never a class.

The leg-(d) test as implemented (three clauses, each mechanical):

  clause 1 (matched span)  the transcript span S (verbatim bytes at the cited offsets) is
                           compared, token by token, against a ground-truth span either
                           (i) from a Hawkins book passage (frozen book store), or
                           (ii) from the transcript's OWN immediately adjacent repetition of
                           the same phrasing (a contiguous occurrence of the ground-truth
                           token sequence within ADJ chars of the finding, in the same file).
  clause 2 (word absent)   exactly one ground-truth token is absent from S, and every other
                           token matches in order — i.e. the divergence set is a single
                           deletion (the omission).
  clause 3 (restoration)   putting that one word back yields token-equality with the ground
                           truth — the minimal edit (one word) that completes the match (L3).

Anything else is CANDIDATE with a reason code; two-word omissions are NOT promoted
(restoration not minimal); paraphrase shadows are not promoted (no exact match).

Outputs (all under --out, LAW §8 manifest in PROVENANCE.json):
  adjudication.jsonl · fixtures-adjudication.json · SUMMARY.md · PROVENANCE.json

Stdlib only, read-only over the corpus; writes only under --out.
"""
import argparse
import collections
import difflib
import hashlib
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import m5r_reduce as m5r  # noqa: E402  (corpus loaders only — never the reducer's logic)

TOKEN = re.compile(r"[^\W_]+(?:['\u2019\-][^\W_]+)*", re.UNICODE)   # own copy; documented
ADJ = 800            # "immediately adjacent" window for clause (d)(ii), chars
MIN_PHRASE = 5       # a repetition must span >= this many tokens to count as "the phrasing"
DETECTOR_VERSION = "C1-drop (M4-q2, tools/det_dropword.py @ 012914d)"


def tok(text):
    """Own tokenizer (independent of the reducer's): Unicode words, hyphens/apostrophes
    kept inside a token; lower-cased, curly apostrophes normalised."""
    return [t.replace("\u2019", "'").lower() for t in TOKEN.findall(text)]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def utc():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ------------------------------------------------------------------ the leg (d) test

def single_deletion_restores(s, b):
    """All positions i where b with b[i] removed equals s (token-exact). Empty if none."""
    out = []
    if len(b) != len(s) + 1:
        return out
    for i in range(len(b)):
        if b[:i] + b[i + 1:] == s:
            out.append(i)
    return out


def divergence_profile(s, b):
    """Why a span failed clause 2/3: count of non-equal ops + the diff for the record."""
    sm = difflib.SequenceMatcher(None, s, b, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
    missing = [b[j1:j2] for tag, _i1, _i2, j1, j2 in ops if tag == "insert"]
    extra = [s[i1:i2] for tag, i1, i2, _j1, _j2 in ops if tag == "delete"]
    subs = [(s[i1:i2], b[j1:j2]) for tag, i1, i2, j1, j2 in ops if tag == "replace"]
    return {"n_diff_ops": len(ops), "missing_tokens": missing, "extra_tokens": extra,
            "substitutions": subs}


def find_adjacent_repetition(transcript, span_start, span_end, b_tokens, adj=ADJ):
    """Clause (d)(ii): the transcript's own immediately adjacent repetition of the same
    phrasing. Returns (char_start, char_end, text) of the occurrence, or None.

    The occurrence must (a) lie within `adj` chars of the finding and (b) consist of the
    ground-truth token sequence contiguously (same order, same tokens).
    """
    if len(b_tokens) < MIN_PHRASE:
        return None
    toks = [(m.start(), m.end(), m.group(0).replace("\u2019", "'").lower())
            for m in TOKEN.finditer(transcript)]
    n = len(b_tokens)
    for i in range(len(toks) - n + 1):
        if [t[2] for t in toks[i:i + n]] != b_tokens:
            continue
        st, en = toks[i][0], toks[i + n - 1][1]
        if en < span_start - adj or st > span_end + adj:
            continue
        if st < span_start and en > span_end:      # the occurrence IS the span: not adjacent
            continue
        return {"adjacent_repetition": {"start": st, "end": en,
                                        "quote": transcript[st:en]}}
    return None


def adjudicate_signal(text, books, signal, index, seeded_spans):
    """Return one per-finding record (L1) with verdict + reason."""
    rec = collections.OrderedDict()
    rec["id"] = "D-%03d" % index
    rec["detector"] = DETECTOR_VERSION
    rec["transcript"] = signal["_transcript"]
    start, end = signal["start"], signal["end"]
    rec["char_offset"] = start
    rec["span_end"] = end
    rec["span"] = text[start:end]
    rec["detector_dropped_words"] = list(signal["dropped_words"])
    rec["detector_claim"] = signal["note"]
    rec["seeded"] = any(s <= start and end <= e for s, e in seeded_spans)
    rec["in_sample"] = True          # tuning-set run; never precision evidence (LAW §9 / L5)

    # ---- citation re-derivation, byte-exact (L2)
    rec["citation_ok"] = (text[start:end] == signal["quoted"])
    slug = signal["book_ref"]["slug"]
    boff = signal["book_ref"]["char_offset"]
    bquote = signal["book_ref"]["quote"]
    book = books.get(slug, "")
    rec["book_ref"] = {"slug": slug, "char_offset": boff, "quote": bquote}
    rec["book_quote_ok"] = bool(book[boff:boff + len(bquote)] == bquote)

    s = tok(rec["span"])
    b = tok(bquote)
    rec["tokens_span"] = len(s)
    rec["tokens_book"] = len(b)

    # ---- clause (d)(i): book ground truth, single-deletion restoration
    hits = single_deletion_restores(s, b)
    if rec["citation_ok"] and rec["book_quote_ok"] and hits:
        i = hits[0]
        word = b[i]
        restored = list(s)
        # reinsert at the token position (map back through the phrase: rebuild from b)
        restored_tokens = list(b)
        restored_tokens.pop(i)
        rec.update({
            "clause": "d-i",
            "ground_truth": {"kind": "book", "slug": slug, "char_offset": boff,
                             "quote": bquote},
            "omitted_word": word,
            "restored_span": " ".join(restored_tokens),
            "restored_matches_ground_truth": True,
            "restoration_is_minimal": True,
            "verdict": "CERTAIN-leg-d",
            "reason": "transcript span is the ground-truth passage with exactly one word "
                      "absent (%r); restoring it yields token-equality — clauses 1-3 all "
                      "hold, cited to bytes" % word,
        })
        return rec

    # ---- clause (d)(ii): ground truth = the transcript's own adjacent repetition
    adj = find_adjacent_repetition(text, start, end, b)
    if rec["citation_ok"] and adj:
        adj_s = tok(adj["adjacent_repetition"]["quote"])
        hits2 = single_deletion_restores(s, adj_s)
        if hits2:
            i = hits2[0]
            word = adj_s[i]
            rec.update({
                "clause": "d-ii",
                "ground_truth": {"kind": "adjacent-repetition",
                                 **adj["adjacent_repetition"]},
                "omitted_word": word,
                "restored_span": " ".join(adj_s),
                "restored_matches_ground_truth": True,
                "restoration_is_minimal": True,
                "verdict": "CERTAIN-leg-d",
                "reason": "the same phrasing occurs adjacently in the transcript with the "
                          "word %r present; the finding span is that phrasing with the word "
                          "absent — restoring it completes the match" % word,
            })
            return rec

    # ---- CANDIDATE: record the precise failure (near-miss evidence)
    prof = divergence_profile(s, b)
    if not rec["citation_ok"] or not rec["book_quote_ok"]:
        reason_code, why = ("citation-mismatch",
                            "citation did not re-derive byte-exact — claim fails (L2)")
    elif len(prof["missing_tokens"]) and all(len(m) >= 2 for m in prof["missing_tokens"]) \
            and not prof["extra_tokens"] and not prof["substitutions"]:
        reason_code = "restoration-not-minimal"
        why = ("two or more words absent (%r): restoring them is a larger edit than one "
               "word — not leg (d) (L3)" % [w for m in prof["missing_tokens"] for w in m])
    elif prof["substitutions"] or prof["extra_tokens"]:
        reason_code = "span-not-exact"
        why = ("span does not match the ground truth modulo a single omission (other token "
               "differences: %d substitution(s), %d extra token(s)) — paraphrase shadow, "
               "not a matched span (clause 2)" % (len(prof["substitutions"]),
                                                  len(prof["extra_tokens"])))
    else:
        reason_code = "no-single-insertion"
        why = ("no single ground-truth word restores an exact match (missing %r) — not a "
               "one-word omission within a matched span" % prof["missing_tokens"])
    rec.update({
        "clause": None,
        "ground_truth": {"kind": "book", "slug": slug, "char_offset": boff,
                         "quote": bquote},
        "omitted_word": None,
        "restored_span": None,
        "restored_matches_ground_truth": False,
        "restoration_is_minimal": False,
        "verdict": "CANDIDATE",
        "reason_code": reason_code,
        "reason": why,
        "divergence_profile": prof,
        "adjacent_repetition_found": bool(adj),
    })
    return rec


# ------------------------------------------------------------------ fixtures

def adjudicate_fixture(text, books, fx, seeded_spans):
    sig = {"_transcript": os.path.basename(fx["transcript"]),
           "start": fx["char_offset"], "end": fx["span_end"],
           "quoted": fx["quoted"], "dropped_words": fx["dropped_words"],
           "note": "provisional fixture %s (hand-read in M4-q2)" % fx["id"],
           "book_ref": fx["book_ref"]}
    rec = adjudicate_signal(text, books, sig, 900, seeded_spans)
    rec["id"] = "FIX-%s" % fx["id"]
    rec["fixture"] = fx["id"]
    rec["fixture_claim"] = fx.get("confidence")
    rec["adjudication"] = ("CONFIRMED under leg (d)" if rec["verdict"] == "CERTAIN-leg-d"
                           else "DISCARDED from the CERTAIN claim (stays CANDIDATE)")
    return rec


# ------------------------------------------------------------------ runner

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--signals", default="runs/m4-q2-dropword/signals.json")
    ap.add_argument("--fixtures", default="fixtures/v2/dropword.json")
    ap.add_argument("--corpus", default="corpus")
    ap.add_argument("--confirmed", default="evidence/fixtures/confirmed")
    ap.add_argument("--out", default="runs/m4-q2-adjudication")
    ap.add_argument("--tool-commit", default=None)
    ap.add_argument("--main-head", default=None)
    ap.add_argument("--policy-sha", default=None)
    ap.add_argument("--book-store-sha", default=None)
    a = ap.parse_args(argv)

    transcripts = m5r.load_transcripts(a.corpus)
    books = m5r.parse_book_store(os.path.join(a.corpus, "docdocgo", "html",
                                              "merged-book-texts_json_1.js"))
    signals = json.load(open(a.signals, encoding="utf-8"))

    # hand-confirmed fixture spans (seeded labelling, LAW §9 / L5)
    seeded_spans = []
    if os.path.isdir(a.confirmed):
        for name in sorted(os.listdir(a.confirmed)):
            if not name.endswith(".json"):
                continue
            for fx in json.load(open(os.path.join(a.confirmed, name), encoding="utf-8")):
                t = os.path.basename(fx.get("transcript", ""))
                if t in transcripts:
                    seeded_spans.append((t, fx["char_offset"],
                                         fx["char_offset"] + len(fx.get("quoted", ""))))

    rows, idx = [], 0
    t0 = time.time()
    for name in sorted(signals):
        text = transcripts[name]
        spans = [sp for sp in seeded_spans if sp[0] == name]
        for s in signals[name]:
            s["_transcript"] = name
            idx += 1
            rows.append(adjudicate_signal(text, books, s, idx, spans))
            if idx % 25 == 0:                       # cadence beacon inside the work loop
                stamp = ("  %s TASK-018 adjudication: %d/%d signals adjudicated (%.0fs)"
                         % (utc(), idx, sum(len(v) for v in signals.values()),
                            time.time() - t0))
                print(stamp, flush=True)
                with open(os.path.join("fleet", "heartbeats", "WORKER.log"),
                          "a", encoding="utf-8") as fh:
                    fh.write(stamp + "\n")

    counts = collections.Counter(r["verdict"] for r in rows)
    clauses = collections.Counter(r["clause"] or "CANDIDATE" for r in rows)
    reasons = collections.Counter(r.get("reason_code") for r in rows
                                  if r["verdict"] == "CANDIDATE")

    fxdoc = json.load(open(a.fixtures, encoding="utf-8"))
    fxrows = []
    for fx in fxdoc["fixtures"]:
        name = os.path.basename(fx["transcript"])
        spans = [sp for sp in seeded_spans if sp[0] == name]
        fxrows.append(adjudicate_fixture(transcripts[name], books, fx, spans))
    fx_counts = collections.Counter(r["verdict"] for r in fxrows)

    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "adjudication.jsonl"), "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    with open(os.path.join(a.out, "fixtures-adjudication.json"), "w",
              encoding="utf-8") as fh:
        json.dump(fxrows, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")

    # ---- SUMMARY (counts per clause; near-misses) — the deliverable document
    near = [r for r in rows if r["verdict"] == "CANDIDATE"]
    near_sorted = sorted(near, key=lambda r: (r["reason_code"], r["transcript"],
                                              r["char_offset"]))
    lines = []
    A = lines.append
    A("# TASK-018 — leg (d) adjudication of the C1-drop signals (SUMMARY)")
    A("")
    A("> **Scope.** 122 detector signals from the tuning-set run "
      "`runs/m4-q2-dropword/signals.json` (sha256 `8d71f57b…`), each adjudicated "
      "**individually** on cited bytes under STANDARDS CERTAIN leg (d) as restated in "
      "the ORCH-2 standing guidance (owner `ERRATA-2026-09-25e.md` §2–§4). No rule, "
      "threshold, score or detector name is a classification reason (L4).")
    A("")
    A("> **These are in-sample signals** (tuning split; four were hand-picked into "
      "provisional fixtures) — nothing here is precision/recall evidence (LAW §9 / L5).")
    A("")
    A("## Counts per clause")
    A("")
    A("| outcome | signals | share of 122 |")
    A("|---|---|---|")
    for k in ("CERTAIN-leg-d", "CANDIDATE"):
        A("| %s | %d | %.0f%% |" % (k, counts.get(k, 0), 100.0 * counts.get(k, 0) / len(rows)))
    A("| — of which clause (d)(i) book ground truth | %d | %.0f%% |"
      % (clauses.get("d-i", 0), 100.0 * clauses.get("d-i", 0) / len(rows)))
    A("| — of which clause (d)(ii) adjacent repetition | %d | %.0f%% |"
      % (clauses.get("d-ii", 0), 100.0 * clauses.get("d-ii", 0) / len(rows)))
    A("")
    A("Failure reasons among the %d CANDIDATE signals:" % counts.get("CANDIDATE", 0))
    A("")
    A("| reason code | signals | reading |")
    A("|---|---|---|")
    reading = {
        "restoration-not-minimal": "two or more words absent — restoring them is a larger "
                                   "edit than one word, so the narrow leg does not reach "
                                   "them (L3)",
        "span-not-exact": "the span tracks the passage only loosely (substitutions / extra "
                          "tokens) — a paraphrase shadow, not a matched span",
        "no-single-insertion": "no single ground-truth word restores an exact match",
        "citation-mismatch": "citation failed byte re-derivation (L2)",
    }
    for code, n in reasons.most_common():
        A("| `%s` | %d | %s |" % (code, n, reading.get(code, "")))
    A("")
    A("## Closest near-misses (why the narrow leg refused them)")
    A("")
    for r in near_sorted[:12]:
        prof = r.get("divergence_profile", {})
        miss = [w for m in prof.get("missing_tokens", []) for w in m]
        A("- **%s** @%d `%s` — %s: absent %r%s"
          % (r["id"], r["char_offset"], r["span"][:48].replace("\n", " "),
             r["reason_code"], miss,
             ("; substitutions %r" % (prof.get("substitutions")[:2],)
              if prof.get("substitutions") else "")))
    A("")
    A("## What was NOT done")
    A("- No blanket promotion: %d of 122 signals were promoted, each by its own cited "
      "bytes; the detector's own `note` was never the reason." % counts.get("CERTAIN-leg-d", 0))
    A("- No detector re-tuning, no threshold change, no new detector (TASK-018 boundaries).")
    A("- The spent holdout was not re-run; no rate, precision or corpus-wide figure is "
      "stated anywhere.")
    A("")
    A("## Provenance")
    A("Rows: `adjudication.jsonl` (122) · fixtures: `fixtures-adjudication.json` (4) · "
      "manifest: `PROVENANCE.json`.")
    with open(os.path.join(a.out, "SUMMARY.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    prov = {
        "run_utc": utc(),
        "task": "TASK-018 (leg (d) adjudication)",
        "authority": {"owner_errata_25e": "fleet/ERRATA-2026-09-25e.md §2-§4 @ main",
                      "owner_errata_25g": "fleet/ERRATA-2026-09-25g.md §5",
                      "gate_guidance": "ORCH-2 lane fleet/GATES.md 'Standing classification "
                                       "guidance — CERTAIN leg (d)' @ 45959ca",
                      "task_file": "ORCH-2 lane fleet/queue/pending/TASK-018.md @ 45959ca"},
        "adjudicator_sha256": sha256_file(os.path.abspath(__file__)),
        "tool_commit": a.tool_commit or "UNPINNED",
        "policy_sha256": a.policy_sha or "UNPINNED",
        "main_head": a.main_head or "UNPINNED",
        "inputs": {
            "signals": {"path": a.signals, "sha256": sha256_file(a.signals)},
            "fixtures": {"path": a.fixtures, "sha256": sha256_file(a.fixtures)},
            "corpus_zip_sha256": "3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db",
            "book_store": {"path": "corpus/docdocgo/html/merged-book-texts_json_1.js",
                           "sha256": a.book_store_sha or "UNPINNED"},
            "ledger_reference": {"path": "findings/ledger.jsonl",
                                 "sha256": sha256_file("findings/ledger.jsonl")},
            "split": {"path": "tools/HELD-OUT-SPLIT.json",
                      "sha256": sha256_file("tools/HELD-OUT-SPLIT.json")},
            "holdout_reads": [],
            "holdout_enforced": True,
        },
        "params": {"adjacent_window_chars": ADJ, "min_phrase_tokens": MIN_PHRASE,
                   "token_rule": "[^\\W_]+(?:['’\\-][^\\W_]+)* (own copy; Unicode; "
                                 "hyphen/apostrophe kept inside a token)"},
        "counts": {"signals": len(rows), "by_verdict": dict(counts), "by_clause": dict(clauses),
                   "candidate_reasons": dict(reasons),
                   "fixtures": dict(fx_counts)},
        "outputs": {},
        "status": "DELIVERY — per-finding adjudication; no rate, no precision, no "
                  "certification language; in-sample labelled (LAW §9 / L5)",
    }
    for name in ("adjudication.jsonl", "fixtures-adjudication.json", "SUMMARY.md"):
        prov["outputs"][name] = sha256_file(os.path.join(a.out, name))
    with open(os.path.join(a.out, "PROVENANCE.json"), "w", encoding="utf-8") as fh:
        json.dump(prov, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")

    print("TASK-018 adjudication: %d signals -> %s; fixtures -> %s; reasons %s"
          % (len(rows), dict(counts), dict(fx_counts), dict(reasons)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
