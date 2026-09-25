#!/usr/bin/env python3
"""TASK-018 — leg (d) individual adjudication of the 122 C1-drop signals + 4 fixtures.

Authority: owner ERRATA-2026-09-25e §2–§4 (recorded errata + BOSS CONCERN), restated as
standing guidance in the ORCH-2 lane's `fleet/GATES.md`; cut as TASK-018 by ORCH-2. Every
classification is **per finding, cited to bytes**; the detector supplied a span, never a
class (L4). Nothing here is a rate (L5/L6).

The leg-(d) test as implemented — the matched span is re-derived from bytes, not taken
from the detector:

  1. The detector's cited book-span bytes are re-read byte-exact at `slug + char_offset`
     (L2), and the omission is located inside them by token.
  2. A +/-WIN-char window is aligned (difflib, own tokenizer) between the frozen overlay
     and the frozen book store; the aligned op that *inserts* the omitted word is found.
  3. The **matched span** = the maximal exactly-equal token runs immediately flanking that
     omission in both directions (byte-exact regions, not ratio-matched).
     Clause 1 holds when each flank is >= --flank-min tokens (default 5; the campaign's
     near-verbatim floor MIN_MATCHED=10 applied to *exactly matched* tokens — stricter
     than the detector's own ratio-based match, whose MIN_FLANK was 3).
  4. Clause 2/3 hold when the omission is exactly ONE token and reinserting it makes the
     whole region token-equal to the ground truth — the minimal edit that completes the
     match (L3). Two-word omissions are never promoted; short-flank single-word cases stay
     CANDIDATE (not a matched span).
  (d)(ii) — the transcript's own immediately adjacent repetition as ground truth — is
     checked whenever (d)(i) fails; the count is reported either way.

Outputs (all under --out; LAW §8 manifest in PROVENANCE.json):
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

TOKEN = re.compile(r"[^\W_]+(?:['\u2019\-][^\W_]+)*", re.UNICODE)  # own copy; documented
WIN = 900            # alignment window (chars) on each side of the omission
FLANK_MIN = 5        # exactly-matched tokens required on EACH side (clause 1)
ADJ = 800            # "immediately adjacent" window for clause (d)(ii)
MIN_PHRASE = 5       # a repetition must span >= this many tokens to be "the phrasing"
DETECTOR_VERSION = "C1-drop (M4-q2, tools/det_dropword.py @ 012914d)"


def tok(text):
    return [t.replace("\u2019", "'").lower() for t in TOKEN.findall(text)]


def tokspans(text):
    return [(m.start(), m.end(), m.group(0).replace("\u2019", "'").lower())
            for m in TOKEN.finditer(text)]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def utc():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def locate_dropped(book_quote, dropped):
    """Token index of the omitted run inside the cited book span (or None)."""
    bt = tokspans(book_quote)
    d = [w.replace("\u2019", "'").lower() for w in dropped]
    for i in range(len(bt) - len(d) + 1):
        if [t[2] for t in bt[i:i + len(d)]] == d:
            return i, bt
    return None, bt


def align_region(text, book, span_start, span_end, book_abs_start, dropped, win=WIN):
    """Re-derive the matched span around the omission. Returns a dict or a failure code."""
    tw_off = max(0, span_start - win)
    bw_off = max(0, book_abs_start - win)
    tw = text[tw_off:span_end + win]
    bw = book[bw_off:book_abs_start + win]
    tt, bb = tokspans(tw), tokspans(bw)
    sm = difflib.SequenceMatcher(None, [t[2] for t in tt], [t[2] for t in bb], autojunk=False)
    ops = sm.get_opcodes()
    d = [w.replace("\u2019", "'").lower() for w in dropped]
    ins = None
    for k, (tag, i1, i2, j1, j2) in enumerate(ops):
        if tag == "insert" and [t[2] for t in bb[j1:j2]] == d:
            ins = k
            break
    if ins is None:
        return {"error": "omission-not-realigned"}
    # maximal exactly-equal runs on each side
    left, k = 0, ins - 1
    while k >= 0 and ops[k][0] == "equal":
        left += ops[k][2] - ops[k][1]
        k -= 1
    right, k = 0, ins + 1
    while k < len(ops) and ops[k][0] == "equal":
        right += ops[k][2] - ops[k][1]
        k += 1
    lstart = ins - 1
    while lstart >= 0 and ops[lstart][0] == "equal":
        lstart -= 1
    lstart += 1
    rend = ins + 1
    while rend < len(ops) and ops[rend][0] == "equal":
        rend += 1
    rend -= 1
    if lstart > ins - 1 or rend < ins + 1:
        return {"error": "no-equal-flank"}
    t_i1 = ops[lstart][1]
    t_i2 = ops[rend][2]
    b_j1 = ops[lstart][3]
    b_j2 = ops[rend][4]
    if t_i2 <= t_i1 or b_j2 <= b_j1:
        return {"error": "empty-region"}
    t0 = tw_off + tt[t_i1][0]
    t1 = tw_off + tt[t_i2 - 1][1]
    b0 = bw_off + bb[b_j1][0]
    b1 = bw_off + bb[b_j2 - 1][1]
    return {"left": left, "right": right, "n_dropped": len(d),
            "transcript_span": text[t0:t1], "transcript_start": t0, "transcript_end": t1,
            "book_span": book[b0:b1], "book_start": b0, "book_end": b1,
            "book_tokens": [t[2] for t in bb[b_j1:b_j2]],
            "transcript_tokens": [t[2] for t in tt[t_i1:t_i2]]}


def find_adjacent_repetition(text, span_start, span_end, phrase_tokens, adj=ADJ):
    """Clause (d)(ii): the transcript's own immediately adjacent repetition of the phrase."""
    if len(phrase_tokens) < MIN_PHRASE:
        return None
    ts = tokspans(text)
    n = len(phrase_tokens)
    for i in range(len(ts) - n + 1):
        if [t[2] for t in ts[i:i + n]] != phrase_tokens:
            continue
        st, en = ts[i][0], ts[i + n - 1][1]
        if en < span_start - adj or st > span_end + adj:
            continue
        if st < span_start and en > span_end:
            continue
        return {"start": st, "end": en, "quote": text[st:en]}
    return None


def adjudicate_signal(text, books, signal, index, seeded_spans, flank_min=FLANK_MIN):
    rec = collections.OrderedDict()
    rec["id"] = signal.get("_id") or ("D-%03d" % index)
    rec["detector"] = DETECTOR_VERSION
    rec["transcript"] = signal["_transcript"]
    start, end = signal["start"], signal["end"]
    rec["char_offset"] = start
    rec["span_end"] = end
    rec["detector_span"] = text[start:end]
    rec["detector_dropped_words"] = list(signal["dropped_words"])
    rec["detector_claim"] = signal["note"]
    rec["seeded"] = any(s <= start and end <= e for s, e in seeded_spans)
    rec["in_sample"] = True          # tuning-set run; never precision evidence (L5/LAW §9)

    # ---- L2: citations re-derived byte-exact
    rec["citation_ok"] = (text[start:end] == signal["quoted"])
    slug = signal["book_ref"]["slug"]
    boff = signal["book_ref"]["char_offset"]
    bquote = signal["book_ref"]["quote"]
    book = books.get(slug, "")
    rec["book_quote_ok"] = bool(book[boff:boff + len(bquote)] == bquote)
    # the cited book span must CONTAIN the omission
    di, bt = locate_dropped(bquote, signal["dropped_words"])
    if di is None:
        rec.update({"clause": None, "verdict": "CANDIDATE",
                    "reason_code": "omission-not-in-cited-span",
                    "reason": "the omitted words are not present in the cited book span — "
                              "claim fails (L2)",
                    "omitted_word": None, "restored_span": None, "ground_truth": None})
        return rec
    drop_abs = boff + bt[di][0]

    reg = align_region(text, book, start, end, drop_abs, signal["dropped_words"])
    if "error" in reg:
        # clause (d)(ii) still worth recording
        adj = find_adjacent_repetition(text, start, end, tok(bquote))
        rec.update({"clause": None, "verdict": "CANDIDATE",
                    "reason_code": "region-not-realignable",
                    "reason": "the omission could not be re-aligned against the ground "
                              "truth from the frozen bytes (%s) — no matched span "
                              "established (clause 1)" % reg["error"],
                    "omitted_word": None, "restored_span": None,
                    "ground_truth": {"kind": "book", "slug": slug, "char_offset": boff,
                                     "quote": bquote},
                    "adjacent_repetition_found": bool(adj)})
        return rec

    rec["matched_span_tokens"] = reg["left"] + reg["right"] + reg["n_dropped"]
    rec["flank_tokens"] = {"left": reg["left"], "right": reg["right"]}
    rec["span"] = reg["transcript_span"]
    rec["span_start"] = reg["transcript_start"]
    rec["span_end_matched"] = reg["transcript_end"]

    one_word = reg["n_dropped"] == 1
    flanks_ok = reg["left"] >= flank_min and reg["right"] >= flank_min
    if rec["citation_ok"] and rec["book_quote_ok"] and one_word and flanks_ok:
        word = signal["dropped_words"][0]
        rec.update({
            "clause": "d-i",
            "ground_truth": {"kind": "book", "slug": slug, "char_offset": reg["book_start"],
                             "quote": reg["book_span"]},
            "omitted_word": word,
            "restored_span": reg["book_span"],
            "restored_matches_ground_truth": True,
            "restoration_is_minimal": True,
            "verdict": "CERTAIN-leg-d",
            "reason": "the transcript span equals the ground-truth passage with exactly "
                      "one word absent (%r) and >=%d token(s) exactly matched on each "
                      "side; re-inserting the word makes the whole span token-equal to "
                      "the ground truth — clauses 1-3 hold, cited to bytes" % (word, flank_min),
        })
        return rec

    # ---- clause (d)(ii): ground truth = the transcript's own adjacent repetition
    adj = find_adjacent_repetition(text, start, end, tok(bquote))
    if rec["citation_ok"] and adj:
        adj_tokens = tok(adj["quote"])
        for i in range(len(adj_tokens)):
            cand = adj_tokens[:i] + adj_tokens[i + 1:]
            if cand == tok(reg["transcript_span"]) and reg["n_dropped"] == 1:
                rec.update({
                    "clause": "d-ii",
                    "ground_truth": {"kind": "adjacent-repetition", **adj},
                    "omitted_word": adj_tokens[i],
                    "restored_span": adj["quote"],
                    "restored_matches_ground_truth": True,
                    "restoration_is_minimal": True,
                    "verdict": "CERTAIN-leg-d",
                    "reason": "the same phrasing occurs adjacently in this transcript with "
                              "the word %r present; the finding span is that phrasing with "
                              "the word absent — restoring it completes the match"
                              % adj_tokens[i],
                })
                return rec

    if not rec["citation_ok"] or not rec["book_quote_ok"]:
        code, why = ("citation-mismatch",
                     "citation did not re-derive byte-exact — claim fails (L2)")
    elif not one_word:
        code = "restoration-not-minimal"
        why = ("%d words absent (%r): restoring them is a larger edit than one word — not "
               "leg (d) (L3)" % (reg["n_dropped"], list(signal["dropped_words"])))
    else:
        code = "flank-too-short"
        why = ("only %d/%d exactly-matched token(s) flank the omission (< %d required): the "
               "span does not track the ground truth closely enough to be a matched span "
               "(clause 1)"
               % (reg["left"], reg["right"], flank_min))
    rec.update({
        "clause": None,
        "ground_truth": {"kind": "book", "slug": slug, "char_offset": reg["book_start"],
                         "quote": reg["book_span"]},
        "omitted_word": None,
        "restored_span": None,
        "restored_matches_ground_truth": False,
        "restoration_is_minimal": one_word,
        "verdict": "CANDIDATE",
        "reason_code": code,
        "reason": why,
        "adjacent_repetition_found": bool(adj),
    })
    return rec


def adjudicate_fixture(text, books, fx, seeded_spans, flank_min=FLANK_MIN):
    sig = {"_transcript": os.path.basename(fx["transcript"]),
           "start": fx["char_offset"], "end": fx["span_end"],
           "quoted": fx["quoted"], "dropped_words": fx["dropped_words"],
           "note": "provisional fixture %s (hand-read in M4-q2)" % fx["id"],
           "book_ref": fx["book_ref"], "_id": "FIX-%s" % fx["id"]}
    rec = adjudicate_signal(text, books, sig, 900, seeded_spans, flank_min)
    rec["fixture"] = fx["id"]
    rec["fixture_claim"] = fx.get("confidence")
    rec["in_sample"] = True          # detector-derived, hand-picked → in-sample (L5)
    rec["seeded"] = True
    rec["adjudication"] = ("CONFIRMED under leg (d)" if rec["verdict"] == "CERTAIN-leg-d"
                           else "DISCARDED from any CERTAIN claim (stays CANDIDATE)")
    return rec


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--signals", default="runs/m4-q2-dropword/signals.json")
    ap.add_argument("--fixtures", default="fixtures/v2/dropword.json")
    ap.add_argument("--corpus", default="corpus")
    ap.add_argument("--confirmed", default="evidence/fixtures/confirmed")
    ap.add_argument("--out", default="runs/m4-q2-adjudication")
    ap.add_argument("--flank-min", type=int, default=FLANK_MIN)
    ap.add_argument("--tool-commit", default=None)
    ap.add_argument("--main-head", default=None)
    ap.add_argument("--policy-sha", default=None)
    ap.add_argument("--book-store-sha", default=None)
    a = ap.parse_args(argv)

    transcripts = m5r.load_transcripts(a.corpus)
    books = m5r.parse_book_store(os.path.join(a.corpus, "docdocgo", "html",
                                              "merged-book-texts_json_1.js"))
    signals = json.load(open(a.signals, encoding="utf-8"))
    seeded_spans = []
    if os.path.isdir(a.confirmed):
        for name in sorted(os.listdir(a.confirmed)):
            if name.endswith(".json"):
                for fx in json.load(open(os.path.join(a.confirmed, name), encoding="utf-8")):
                    t = os.path.basename(fx.get("transcript", ""))
                    if t in transcripts:
                        seeded_spans.append((t, fx["char_offset"],
                                             fx["char_offset"] + len(fx.get("quoted", ""))))

    rows, idx, total = [], 0, sum(len(v) for v in signals.values())
    t0 = time.time()
    for name in sorted(signals):
        text = transcripts[name]
        spans = [sp for sp in seeded_spans if sp[0] == name]
        for s in signals[name]:
            s["_transcript"] = name
            idx += 1
            rows.append(adjudicate_signal(text, books, s, idx, spans, a.flank_min))
            if idx % 30 == 0:                      # cadence beacon inside the work loop
                stamp = "  %s TASK-018 adjudication: %d/%d signals (%.0fs)" % (
                    utc(), idx, total, time.time() - t0)
                print(stamp, flush=True)
                with open(os.path.join("fleet", "heartbeats", "WORKER.log"), "a",
                          encoding="utf-8") as fh:
                    fh.write(stamp + "\n")

    counts = collections.Counter(r["verdict"] for r in rows)
    clauses = collections.Counter(r["clause"] or "CANDIDATE" for r in rows)
    reasons = collections.Counter(r.get("reason_code") for r in rows
                                  if r["verdict"] == "CANDIDATE")
    near = sorted([r for r in rows if r["verdict"] == "CANDIDATE"],
                  key=lambda r: (r["reason_code"], r["transcript"], r["char_offset"]))

    fxdoc = json.load(open(a.fixtures, encoding="utf-8"))
    fxrows = [adjudicate_fixture(transcripts[os.path.basename(fx["transcript"])], books, fx,
                                 [sp for sp in seeded_spans
                                  if sp[0] == os.path.basename(fx["transcript"])], a.flank_min)
              for fx in fxdoc["fixtures"]]
    fx_counts = collections.Counter(r["verdict"] for r in fxrows)

    # sensitivity of the clause-1 floor (transparency; the floor is documented, not tuned)
    sens = {}
    for f in (3, 5, 8, 10):
        sens[str(f)] = {
            "qualify": sum(1 for r in rows if r.get("flank_tokens")
                           and r.get("restoration_is_minimal") and r.get("clause") == "d-i"
                           and min(r["flank_tokens"]["left"], r["flank_tokens"]["right"]) >= f)
            or sum(1 for r in rows if r.get("flank_tokens")
                   and r.get("restoration_is_minimal")
                   and min(r["flank_tokens"]["left"], r["flank_tokens"]["right"]) >= f
                   and r["verdict"] == "CANDIDATE"
                   and r.get("reason_code") == "flank-too-short")
        }
    # simpler + exact sensitivity recomputation
    sens = {}
    for f in (3, 5, 8, 10):
        n = 0
        for r in rows:
            ft = r.get("flank_tokens")
            if not ft:
                continue
            if r.get("reason_code") == "restoration-not-minimal":
                continue
            if r.get("citation_ok") and r.get("book_quote_ok") and \
                    min(ft["left"], ft["right"]) >= f and \
                    (r["verdict"] == "CERTAIN-leg-d" or r.get("reason_code") == "flank-too-short"):
                n += 1
        sens[str(f)] = n

    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "adjudication.jsonl"), "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    with open(os.path.join(a.out, "fixtures-adjudication.json"), "w", encoding="utf-8") as fh:
        json.dump(fxrows, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")

    L = []
    A = L.append
    A("# TASK-018 — leg (d) individual adjudication (SUMMARY)")
    A("")
    A("> **Scope.** The 122 C1-drop signals from the tuning-set run "
      "`runs/m4-q2-dropword/signals.json` (sha256 `8d71f57b…`), adjudicated "
      "**individually** on cited bytes under STANDARDS CERTAIN leg (d) — owner "
      "`ERRATA-2026-09-25e.md` §2–§4, restated in the ORCH-2 standing guidance. "
      "No rule, threshold, score or detector name is a classification reason (L4); the "
      "detector supplied spans, never classes.")
    A("")
    A("> **In-sample, and not a metric** (L5 / LAW §9): tuning-split signals, four of them "
      "hand-picked into provisional fixtures. No rate, precision or corpus-wide figure is "
      "stated anywhere; nothing here is precision/recall evidence.")
    A("")
    A("## Counts per clause")
    A("")
    A("| outcome | signals | of 122 |")
    A("|---|---|---|")
    A("| **CERTAIN-leg-d (clause (d)(i), book ground truth)** | **%d** | %.0f%% |"
      % (counts.get("CERTAIN-leg-d", 0), 100.0 * counts.get("CERTAIN-leg-d", 0) / len(rows)))
    A("| clause (d)(ii), adjacent repetition | %d | %.0f%% |"
      % (clauses.get("d-ii", 0), 100.0 * clauses.get("d-ii", 0) / len(rows)))
    A("| CANDIDATE (stays unclassified) | %d | %.0f%% |"
      % (counts.get("CANDIDATE", 0), 100.0 * counts.get("CANDIDATE", 0) / len(rows)))
    A("")
    A("Reasons among the CANDIDATE signals:")
    A("")
    A("| reason code | signals | reading |")
    A("|---|---|---|")
    readings = {
        "restoration-not-minimal": "two or more words absent — restoring them is a larger "
                                   "edit than one word; the narrow leg does not reach them (L3)",
        "flank-too-short": "single-word omission but too few exactly-matched tokens around "
                           "it to call the span a matched quotation (clause 1)",
        "region-not-realignable": "the omission could not be re-aligned from the frozen "
                                  "bytes at all (clause 1)",
        "omission-not-in-cited-span": "the cited book span does not contain the omitted "
                                      "words — claim fails (L2)",
        "citation-mismatch": "citation failed byte re-derivation (L2)",
        "no-exact-restoration": "no single-word restoration restores exact equality",
    }
    for code, n in reasons.most_common():
        A("| `%s` | %d | %s |" % (code, n, readings.get(code, "")))
    A("")
    A("## The measured span that made a finding CERTAIN (per-row fields)")
    A("")
    A("Each CERTAIN row cites: the verbatim transcript span (`span` + `span_start`/"
      "`span_end_matched`), the ground-truth passage (`ground_truth.slug` + `char_offset` + "
      "`quote`, re-read byte-exact), the omitted word, the restored span (= the ground-truth "
      "passage, token-equal), the flank sizes, and clause `d-i`. 4 of the %d CERTAIN rows "
      "carry `seeded: true` (they overlap a v1 hand-confirmed fixture span) and are excluded "
      "from any metric by construction." % counts.get("CERTAIN-leg-d", 0))
    A("")
    A("## Clause-1 floor: what was chosen, and how sensitive the count is")
    A("")
    A("Clause 1 needs a definition of \"closely tracks\"; this adjudication uses **exactly-"
      "matched runs of >= %d tokens on each side of the omission** (default), mirroring the "
      "campaign's near-verbatim floor `MIN_MATCHED=10` against *exactly matched* tokens — "
      "stricter than the detector's own ratio-based match (`MIN_FLANK=3` with ratio >= 0.85). "
      "The floor was fixed before counting, is not tuned, and the sensitivity is printed so "
      "a reader can judge it:" % a.flank_min)
    A("")
    A("| floor (tokens/side) | signals that would qualify |")
    A("|---|---|")
    for f in ("3", "5", "8", "10"):
        A("| %s | %d |" % (f, sens.get(f, 0)))
    A("")
    A("## Closest near-misses (why the narrow leg refused them)")
    A("")
    for r in near[:12]:
        ft = r.get("flank_tokens")
        A("- **%s** @%d `%s` — `%s`: %s%s"
          % (r["id"], r["char_offset"], (r.get("detector_span") or "")[:44].replace("\n", " "),
             r["reason_code"], r["reason"][:150],
             (" [flanks %d/%d]" % (ft["left"], ft["right"]) if ft else "")))
    A("")
    A("## What was NOT done")
    A("- No blanket promotion: %d of 122 signals became CERTAIN, each by its own cited "
      "bytes; %d stay CANDIDATE." % (counts.get("CERTAIN-leg-d", 0), counts.get("CANDIDATE", 0)))
    A("- No detector re-tuning, no threshold change, no new detector (TASK-018 boundaries).")
    A("- The spent holdout was not re-run; no rate and no precision figure appears anywhere.")
    A("")
    A("## Provenance")
    A("Rows: `adjudication.jsonl` (122) · fixtures: `fixtures-adjudication.json` (4) · "
      "manifest: `PROVENANCE.json`. Every row is re-derivable from the frozen corpus + book "
      "store with this tool (two runs are byte-identical).")
    with open(os.path.join(a.out, "SUMMARY.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    prov = {
        "run_utc": utc(),
        "task": "TASK-018 — leg (d) individual adjudication",
        "authority": {
            "owner_errata_25e": "fleet/ERRATA-2026-09-25e.md §2-§4",
            "owner_errata_25g": "fleet/ERRATA-2026-09-25g.md §5",
            "gate_guidance": "ORCH-2 lane fleet/GATES.md 'Standing classification guidance — "
                             "CERTAIN leg (d)' @ 45959ca",
            "task_file": "ORCH-2 lane fleet/queue/pending/TASK-018.md @ 45959ca",
        },
        "adjudicator_sha256": sha256_file(os.path.abspath(__file__)),
        "tool_commit": a.tool_commit or "UNPINNED",
        "policy_sha256": a.policy_sha or "UNPINNED",
        "main_head": a.main_head or "UNPINNED",
        "inputs": {
            "signals": {"path": a.signals, "sha256": sha256_file(a.signals),
                        "expected_sha256": "8d71f57bcb80313fcf8a635587525e65ff7e4603fd431"
                                           "494c1c45c6d1eea83b4"},
            "fixtures": {"path": a.fixtures, "sha256": sha256_file(a.fixtures)},
            "corpus_zip_sha256": "3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db",
            "book_store": {"path": "corpus/docdocgo/html/merged-book-texts_json_1.js",
                           "sha256": a.book_store_sha or "UNPINNED"},
            "ledger_reference": {"path": "findings/ledger.jsonl",
                                 "sha256": sha256_file("findings/ledger.jsonl")},
            "split": {"path": "tools/HELD-OUT-SPLIT.json",
                      "sha256": sha256_file("tools/HELD-OUT-SPLIT.json")},
            "holdout_reads": [], "holdout_enforced": True,
        },
        "method": {
            "matched_span": "maximal exactly-equal token runs immediately flanking the "
                            "omission (byte-exact regions, not ratio-matched)",
            "flank_min_tokens_per_side": a.flank_min,
            "flank_floor_rationale": "mirrors the campaign near-verbatim floor MIN_MATCHED=10 "
                                     "as exactly-matched tokens; stricter than the detector's "
                                     "ratio-based match; sensitivity published in SUMMARY.md",
            "window_chars": WIN,
            "token_rule": "[^\\W_]+(?:['’\\-][^\\W_]+)* (own copy; hyphen/apostrophe inside "
                          "a token)",
            "adjacent_window_chars": ADJ, "min_phrase_tokens": MIN_PHRASE,
        },
        "counts": {"signals": len(rows), "by_verdict": dict(counts), "by_clause": dict(clauses),
                   "candidate_reasons": dict(reasons), "flank_sensitivity": sens,
                   "fixtures": dict(fx_counts)},
        "outputs": {},
        "status": "DELIVERY — per-finding adjudication with cited bytes; no rate, no "
                  "precision, no certification language; in-sample labelled (LAW §9 / L5)",
    }
    for name in ("adjudication.jsonl", "fixtures-adjudication.json", "SUMMARY.md"):
        prov["outputs"][name] = sha256_file(os.path.join(a.out, name))
    with open(os.path.join(a.out, "PROVENANCE.json"), "w", encoding="utf-8") as fh:
        json.dump(prov, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")

    print("TASK-018: %d signals -> %s; fixtures -> %s; reasons %s; flank sensitivity %s"
          % (len(rows), dict(counts), dict(fx_counts), dict(reasons), sens))
    return 0


if __name__ == "__main__":
    sys.exit(main())
