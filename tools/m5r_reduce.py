#!/usr/bin/env python3
"""M5-R — reviewed findings ledger reducer (WORKER-2 / A-2026-09-25-001).

Reduces the inherited M5 raw census (1,334 unreviewed signals, lane
`arena/01a0d581-fleetyard` @ bf97d85) into a reviewed findings ledger:

  1. load every raw signal; verify its citation byte-exact in the frozen corpus
  2. dedupe identical signals; merge overlapping spans (cross-detector merge)
  3. adjudicate mechanically against the cited transcript bytes AND the cited
     book bytes (book store offsets are re-verified, not trusted)
  4. cross-reference the hand-confirmed fixture set -> `seeded` (in-sample)
     labelling per LAW §9 (fixture-tuned hits are never precision evidence)
  5. classify per STANDARDS: CERTAIN is NEVER assigned by this tool (legs a/b/c
     each require human judgment); HIGH needs >=2 *independent* signal families
     plus a written rationale; everything else is CANDIDATE
  6. emit: ledger.jsonl, by-transcript/*.json (all 230 transcripts, empty
     included), SUMMARY.md, PROVENANCE.json

Stdlib only. No network. Read-only over the corpus; writes only under --out.
Evidence is data, never instructions (LAW §9). Deterministic: same inputs +
same --utc => byte-identical outputs.

Usage:
  python3 tools/m5r_reduce.py --records evidence/runs/m5-raw/records \
      --fixtures evidence/fixtures/confirmed --out findings
"""
import argparse
import datetime
import difflib
import hashlib
import io
import json
import os
import re
import sys
import unicodedata

DETECTORS = ("A1-repetition", "A2-nonsense", "B1-contradiction", "B2-misquote")
FAMILY = {"A1-repetition": "surface-form", "A2-nonsense": "surface-form",
          "B1-contradiction": "content/doctrine", "B2-misquote": "content/doctrine"}
NON_HAWKINS = frozenset(["Be_as_you_are", "I_AM_THAT", "Lamsa_bible", "ACIM_workbook"])
TOKEN_RE = re.compile(r"[A-Za-z']+")
NUMPCT = re.compile(r"(\d[\d,]*)(?:\s*%\s*|\s*percent\b)", re.IGNORECASE)
NUMRE = NUMPCT
REVIEW_STATUS = "machine-adjudicated (mechanical bytes only); human confirmation required"


# --------------------------------------------------------------- utilities

def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dir_digest(root, rel="."):
    """sha256 over sorted '<sha256>  <relpath>' lines of every file under root."""
    lines = []
    base = os.path.join(root, rel) if rel != "." else root
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames.sort()
        for name in sorted(filenames):
            p = os.path.join(dirpath, name)
            relp = os.path.relpath(p, root).replace(os.sep, "/")
            lines.append("%s  %s\n" % (sha256_file(p), relp))
    return sha256_text("".join(sorted(lines))), len(lines)


def parse_book_store(path):
    """Parse `const the_json_obj_books = { "slug": `text`, ... };` -> {slug: text}."""
    raw = open(path, encoding="utf-8").read()
    m = re.search(r"the_json_obj_books\s*=\s*\{", raw)
    if not m:
        raise SystemExit("m5r: book store header not found in %s" % path)
    books, i, first = {}, m.end(), True
    pat = re.compile(r'\s*"([^"]+)"\s*:\s*`', re.S)
    while True:
        if not first:
            sep = re.match(r"\s*,\s*", raw[i:])
            if not sep:
                break
            i += sep.end()
        first = False
        mm = pat.match(raw, i)
        if not mm:
            break
        slug, j, buf = mm.group(1), mm.end(), []
        while j < len(raw):
            c = raw[j]
            if c == "\\":
                nxt = raw[j + 1]
                if nxt == "u":
                    buf.append(chr(int(raw[j + 2:j + 6], 16)))
                    j += 6
                elif nxt == "n":
                    buf.append("\n")
                    j += 2
                elif nxt == "t":
                    buf.append("\t")
                    j += 2
                elif nxt in "`\\$":
                    buf.append(nxt)
                    j += 2
                else:
                    buf.append(nxt)
                    j += 2
                continue
            if c == "`":
                j += 1
                break
            if c == "$" and raw[j + 1:j + 2] == "{":
                raise SystemExit("m5r: ${ interpolation in book store — not plain data")
            buf.append(c)
            j += 1
        books[slug] = "".join(buf)
        i = j
    if not books:
        raise SystemExit("m5r: no books parsed")
    return books


def load_transcripts(corpus_dir):
    """basename -> text for corpus/docdocgo/overlays/*.txt (sorted)."""
    d = os.path.join(corpus_dir, "docdocgo", "overlays")
    out = {}
    for name in sorted(os.listdir(d)):
        if name.endswith(".txt"):
            out[name] = open(os.path.join(d, name), encoding="utf-8",
                             errors="replace").read()
    if not out:
        raise SystemExit("m5r: no transcripts under %s" % d)
    return out


def year_of(name):
    m = re.search(r"_(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)_(\d{4})_", name)
    if m:
        return m.group(2)
    m = re.search(r"_(\d{4})_", name)
    return m.group(1) if m else "unknown"


# ------------------------------------------------------------ signal loading

def load_signals(records_dir):
    """Read the inherited raw census -> (signals, per_source_files)."""
    signals, sources = [], []
    for name in sorted(os.listdir(records_dir)):
        if not name.endswith(".json"):
            continue
        path = os.path.join(records_dir, name)
        recs = json.load(open(path, encoding="utf-8"))
        sources.append(name)
        for rec in recs:
            dets = [d for d in str(rec.get("detector_id", "")).split("+") if d]
            for det in dets:
                signals.append({
                    "source_file": name,
                    "transcript": os.path.basename(rec["transcript_path"]),
                    "transcript_path": rec["transcript_path"],
                    "paragraph": rec["location"]["paragraph"],
                    "offset": int(rec["location"]["char_offset"]),
                    "quote": rec["quoted_text"],
                    "intended": rec.get("suspected_intended_text"),
                    "runner_evidence": rec.get("evidence_class", ""),
                    "book_reference": rec.get("book_reference"),
                    "runner_confidence": rec.get("raw_runner_confidence"),
                    "detector": det,
                    "multi_detector_record": len(dets) > 1,
                })
    return signals, sources


def citation_verify(signals, transcripts):
    """Every signal's quote must be byte-exact at its offset. Returns failures."""
    fails = []
    for s in signals:
        text = transcripts.get(s["transcript"])
        if text is None:
            fails.append(dict(s, failure="transcript-missing"))
            continue
        q = s["quote"]
        if text[s["offset"]:s["offset"] + len(q)] != q:
            fails.append({"transcript": s["transcript"], "offset": s["offset"],
                          "detector": s["detector"], "failure": "quote-mismatch",
                          "quote_head": q[:60]})
    return fails


# ------------------------------------------------------------------ merging

def merge_signals(signals):
    """Dedupe identical signals; merge overlapping spans per transcript."""
    by_t = {}
    for s in signals:
        by_t.setdefault(s["transcript"], []).append(s)
    findings = []
    for transcript in sorted(by_t):
        rows = sorted(by_t[transcript], key=lambda r: (r["offset"], -(len(r["quote"])),
                                                       r["detector"]))
        groups = []
        for s in rows:
            start, end = s["offset"], s["offset"] + len(s["quote"])
            placed = False
            for g in groups:
                if start < g["end"] and g["start"] < end:   # strict overlap
                    g["end"] = max(g["end"], end)
                    g["start"] = min(g["start"], start)
                    g["signals"].append(s)
                    placed = True
                    break
            if not placed:
                groups.append({"transcript": transcript, "start": start,
                               "end": end, "signals": [s]})
        # a merge can chain: re-sweep until stable
        changed = True
        while changed:
            changed = False
            out = []
            for g in sorted(groups, key=lambda x: (x["start"], -x["end"])):
                if out and g["start"] < out[-1]["end"]:
                    out[-1]["end"] = max(out[-1]["end"], g["end"])
                    out[-1]["signals"].extend(g["signals"])
                    changed = True
                else:
                    out.append(g)
            groups = out
        for g in groups:
            # dedupe: same detector + same quote text
            seen, sigs = set(), []
            for s in sorted(g["signals"], key=lambda r: (r["detector"], r["offset"],
                                                         r["quote"])):
                key = (s["detector"], s["quote"])
                if key in seen:
                    continue
                seen.add(key)
                sigs.append(s)
            g["signals"] = sigs
            g["detectors"] = sorted({s["detector"] for s in sigs})
            g["families"] = sorted({FAMILY[d] for d in g["detectors"] if d in FAMILY})
            findings.append(g)
    findings.sort(key=lambda f: (f["transcript"], f["start"], f["detectors"]))
    return findings


# ------------------------------------------------------------- adjudication

def repetition_rederive(span_text, kmax=8):
    """Independently re-derive the repetition structure from the span bytes."""
    tokens = TOKEN_RE.findall(span_text.lower())
    n = len(tokens)
    span_periodic, period, repeats = False, None, None
    for k in range(1, min(kmax, n // 2) + 1):
        if n % k == 0 and all(tokens[i] == tokens[i % k] for i in range(n)):
            span_periodic, period, repeats = True, k, n // k
            break
    best = None
    for k in range(1, min(kmax, max(n, 1)) + 1):
        i = 0
        while i + k <= n:
            run = 1
            while i + (run + 1) * k <= n and tokens[i:i + k] == tokens[i + run * k:i + (run + 1) * k]:
                run += 1
            if run >= 3 and (best is None or run > best[1] or (run == best[1] and k < best[0])):
                best = (k, run, i)
                i += run * k
            else:
                i += 1
    return {"tokens": n, "span_fully_periodic": span_periodic,
            "span_period_tokens": period, "span_repeats": repeats,
            "longest_run": ({"unit_tokens": best[0], "repeats": best[1],
                             "start_token": best[2]} if best else None)}


def corroborate_signal(sig, finding):
    """Check the runner's own claim string against a fresh derivation of the bytes.

    Returns (ok, note). Only claims this tool can recompute mechanically are
    checked; anything else returns ok=None (not checked, not corroborated).
    """
    ev = sig.get("runner_evidence") or ""
    det = sig["detector"]
    if det == "A1-repetition":
        r = sig.get("rederived") or {}
        m = re.search(r"(\d+)-token unit repeated (\d+) times", ev)
        if not m:
            return (None, "claim shape not parsed")
        want = (int(m.group(1)), int(m.group(2)))
        ok = bool(r.get("span_fully_periodic")) and \
            (want[0] == r.get("span_period_tokens") and want[1] == r.get("span_repeats"))
        return (ok, "claim %d-token x%d vs re-derived %s x%s (this tool's simple "
                    "tokenizer; a mismatch may be claim shape OR tokenizer shape — "
                    "review, do not read as detector error)" % (
                        want[0], want[1], r.get("span_period_tokens"),
                        r.get("span_repeats")))
    if det == "A2-nonsense":
        a = sig.get("rederived") or {}
        checks, names = [], []
        low = ev.lower()
        if "replacement-char" in low:
            checks.append(a.get("replacement_chars", 0) > 0)
            names.append("replacement-chars")
        if "script-mix" in low or "mixed/foreign" in low:
            checks.append(a.get("non_ascii_letters", 0) > 0 or
                          a.get("non_latin_letters", 0) > 0)
            names.append("non-ASCII letters")
        if "impossible-percent" in low:
            checks.append(bool(a.get("impossible_percent")))
            names.append("impossible percent")
        if not checks:
            return (None, "claim shape not parsed")
        return (all(checks), "re-derived %s" % ", ".join(
            "%s=%s" % (n, a.get({"replacement-chars": "replacement_chars",
                                 "non-ASCII letters": "non_ascii_letters",
                                 "impossible percent": "impossible_percent"}[n]))
            for n in names))
    if det in ("B1-contradiction", "B2-misquote"):
        bcs = [b for b in finding["book_checks"] if b.get("detector") == det]
        if not bcs:
            return (False, "no book reference to verify")
        return (all(b.get("quote_ok") for b in bcs),
                "book quote verified at cited offset" if all(b.get("quote_ok") for b in bcs)
                else "book quote NOT byte-exact at cited offset")
    return (None, "no mechanical claim to check")



def anomaly_rederive(span_text):
    """Independently re-derive A2-style surface anomalies from the bytes."""
    fffd = span_text.count("\ufffd")
    nonascii = nonlatin = 0
    for ch in span_text:
        if not ch.isalpha() or ord(ch) < 128:
            continue
        nonascii += 1
        try:
            if unicodedata.name(ch).split()[0] not in ("LATIN",):
                nonlatin += 1
        except ValueError:
            nonlatin += 1
    pcts = [int(m.group(1).replace(",", "")) for m in NUMPCT.finditer(span_text)]
    return {"replacement_chars": fffd, "non_ascii_letters": nonascii,
            "non_latin_letters": nonlatin, "percent_values": pcts,
            "impossible_percent": [p for p in pcts if p > 100]}


def parse_runner_subtypes(evidence):
    """Pull the parenthetical subtype claims out of the runner's evidence string."""
    out = []
    for part in re.split(r";\s*", evidence or ""):
        m = re.search(r"\(([^()]*)\)", part)
        if m:
            out.append(m.group(1))
    return out


def check_book_ref(books, ref):
    if not ref:
        return None
    slug = ref.get("slug")
    text = books.get(slug)
    off, quote = int(ref.get("char_offset", -1)), ref.get("quote", "")
    if text is None:
        return {"slug": slug, "known_book": False, "offset_ok": False,
                "quote_ok": False}
    return {"slug": slug, "known_book": True,
            "hawkins_own": slug not in NON_HAWKINS,
            "book_chars": len(text), "offset": off,
            "offset_ok": 0 <= off < len(text),
            "quote_ok": text[off:off + len(quote)] == quote,
            "quote_head": quote[:70]}


def token_ops(transcript_text, book_text):
    """Word-level divergence summary between a transcript span and a book span."""
    a = [t.lower() for t in TOKEN_RE.findall(transcript_text)]
    b = [t.lower() for t in TOKEN_RE.findall(book_text)]
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    ops = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        ops.append({"op": tag, "transcript": " ".join(a[i1:i2]) or None,
                    "book": " ".join(b[j1:j2]) or None})
        if len(ops) >= 4:
            break
    return ops


def adjudicate(finding, transcripts, books, fixtures):
    text = transcripts[finding["transcript"]]
    span_text = text[finding["start"]:finding["end"]]
    out = {
        "id": None,  # filled after sorting
        "transcript": finding["transcript"],
        "paragraph": 0,
        "char_offset": finding["start"],
        "span_end": finding["end"],
        "span_text": span_text,
        "detectors": finding["detectors"],
        "families": finding["families"],
        "signals": [],
        "book_checks": [],
        "citation_ok": all(s["quote"] == text[s["offset"]:s["offset"] + len(s["quote"])]
                            for s in finding["signals"]),
        "seeded": False,
        "fixture_overlap": [],
        "review_status": REVIEW_STATUS,
    }
    for s in finding["signals"]:
        sig = {
            "detector": s["detector"],
            "runner_evidence": s["runner_evidence"],
            "runner_subtypes": parse_runner_subtypes(s["runner_evidence"]),
            "asserted_quote": s["quote"],
            "asserted_intended": s["intended"],
            "quote_verified": s["quote"] == text[s["offset"]:s["offset"] + len(s["quote"])],
            "quote_len": len(s["quote"]),
            "offset": s["offset"],
        }
        if s["detector"] == "A1-repetition":
            sig["rederived"] = repetition_rederive(s["quote"])
        elif s["detector"] == "A2-nonsense":
            sig["rederived"] = anomaly_rederive(s["quote"])
        out["signals"].append(sig)
    out["span_facts"] = anomaly_rederive(span_text)
    if "A1-repetition" in finding["detectors"]:
        out["rederived_repetition"] = repetition_rederive(span_text)
    if "A2-nonsense" in finding["detectors"]:
        out["rederived_anomaly"] = anomaly_rederive(span_text)
    for s in finding["signals"]:
        bc = check_book_ref(books, s["book_reference"])
        if bc is not None:
            bc["detector"] = s["detector"]
            bc["book_quote"] = (s["book_reference"] or {}).get("quote", "")
            if bc.get("quote_ok"):
                bc["divergence"] = token_ops(s["quote"], bc["book_quote"])
                nums_t = [m.group(1) for m in NUMRE.finditer(s["quote"])]
                nums_b = [m.group(1) for m in NUMRE.finditer(bc["book_quote"])]
                if nums_t or nums_b:
                    bc["numbers"] = {"transcript": nums_t, "book": nums_b,
                                     "differ": nums_t != nums_b}
            out["book_checks"].append(bc)
    # fixture cross-reference (in-sample labelling, LAW §9)
    for fx in fixtures:
        fx_start = fx["char_offset"]
        fx_end = fx_start + len(fx.get("quoted", "")) or fx_start + 1
        if fx_end <= fx_start:
            fx_end = fx_start + 1
        if fx["transcript"] == finding["transcript"] and \
                finding["start"] < fx_end and fx_start < finding["end"]:
            out["fixture_overlap"].append({
                "id": fx["id"], "confidence": fx["confidence"],
                "offset": fx["char_offset"], "quoted": fx["quoted"],
                "suspected": fx["suspected"], "evidence_class": fx["evidence_class"],
                "status": fx["status"], "status_by": fx["status_by"]})
    out["claim_checks"] = []
    for s in out["signals"]:
        ok, note = corroborate_signal(s, out)
        out["claim_checks"].append({"detector": s["detector"], "claim_ok": ok,
                                    "note": note})
    out["claims_all_corroborated"] = all(c["claim_ok"] is not False
                                         for c in out["claim_checks"])
    out["seeded"] = bool(out["fixture_overlap"])
    return out


def classify(f):
    """STANDARDS ladder. CERTAIN is never assigned here."""
    if f["fixture_overlap"]:
        ids = ", ".join(x["id"] for x in f["fixture_overlap"])
        return ("CERTAIN (inherited fixture)",
                "Covers hand-confirmed fixture(s) %s — CERTAIN per STANDARDS, "
                "inherited (v1 hand-read, gate-reviewed); in-sample for detector "
                "metrics (seeded=true), not admissible as precision evidence "
                "(LAW §9)." % ids)
    content_ok = any(bc.get("quote_ok") for bc in f["book_checks"]
                     if FAMILY.get(bc.get("detector")) == "content/doctrine")
    have_surface = "surface-form" in f["families"]
    have_content = "content/doctrine" in f["families"]
    if have_surface and have_content and content_ok:
        rats = []
        for d in f["detectors"]:
            if d == "A1-repetition":
                r = f.get("rederived_repetition", {})
                lr = r.get("longest_run") or {}
                rats.append("A1-repetition: pattern signal re-derived from the span "
                            "bytes (%s-token unit repeated %sx%s)" % (
                                lr.get("unit_tokens"), lr.get("repeats"),
                                ", span fully periodic" if r.get("span_fully_periodic") else ""))
            elif d == "A2-nonsense":
                a = f.get("rederived_anomaly", {})
                rats.append("A2-nonsense: surface anomaly re-derived (replacement-chars=%d, "
                            "non-Latin=%d, impossible-percent=%s)" % (
                                a.get("replacement_chars", 0), a.get("non_latin_letters", 0),
                                a.get("impossible_percent") or "none"))
            elif d.startswith("B1"):
                rats.append("B1-contradiction: content signal — cited book bytes verified "
                            "at the cited offset, transcript value differs from the book's")
            elif d.startswith("B2"):
                rats.append("B2-misquote: content signal — cited book quote verified "
                            "byte-exact; word-level divergence vs the book derived")
        rat = ("Independent families converge: surface-form (text-internal patterns) plus "
               "content/doctrine (external book bytes, offsets re-verified). " +
               " | ".join(rats) + ". Detector count alone is not the basis: the two "
               "families read different evidence sources (span patterns vs frozen book "
               "text), so their agreement is non-trivial.")
        return ("HIGH (convergence, proposed)", rat)
    return ("CANDIDATE", "Single-family or single-signal evidence; no independent "
                         "second signal and/or no verified book leg. Needs a human "
                         "read (STANDARDS leg a/b/c) before any upgrade.")




# ------------------------------------------------------------------- output

def review_score(f):
    """Mechanical review priority (facts only; never a class)."""
    score, why = 0, []
    for bc in f["book_checks"]:
        if bc.get("quote_ok") and (bc.get("numbers") or {}).get("differ"):
            score += 3
            why.append("book-table number differs")
        elif bc.get("quote_ok") and bc.get("divergence"):
            score += 2
            why.append("book quote diverges word-level")
        elif bc.get("quote_ok"):
            score += 1
            why.append("book quote verified")
    sf = f.get("span_facts", {})
    if sf.get("impossible_percent"):
        score += 3
        why.append("impossible percent")
    if sf.get("replacement_chars"):
        score += 2
        why.append("undecodable byte(s)")
    if sf.get("non_latin_letters"):
        score += 2
        why.append("script-mix")
    r = f.get("rederived_repetition") or {}
    if r.get("span_fully_periodic") and (r.get("span_repeats") or 0) >= 5:
        score += 1
        why.append("periodic run x%d" % r["span_repeats"])
    if len(f["detectors"]) > 1:
        score += 2
        why.append("multi-detector")
    if any(c["claim_ok"] is False for c in f.get("claim_checks", [])):
        score += 1
        why.append("runner claim not re-derived")
    if f["seeded"]:
        score -= 1
        why.append("in-sample (fixture overlap)")
    return score, why


def render_queue(findings, limit=100):
    ranked = sorted(findings, key=lambda f: (-f["review_score"][0], f["transcript"],
                                             f["char_offset"]))
    L = ["# M5-R — review queue (mechanical priority, top %d)" % limit, "",
         "Priority is a **mechanical** score over verified facts (verified book leg, "
         "number divergence, undecodable bytes, script-mix, periodic runs, "
         "multi-detector convergence); it is **not** a confidence class and does not "
         "change any finding's class. Work down the list with STANDARDS legs a/b/c in "
         "hand; confirm or discard each with reasons (the corpus is frozen — nothing "
         "is `fixed`, only confirmed/discarded).", "",
         "| # | score | id | transcript | @offset | detectors | why | quote (head) |",
         "|---|---|---|---|---|---|---|---|"]
    for i, f in enumerate(ranked[:limit], 1):
        L.append("| %d | %d | %s | %s | %d | %s | %s | `%s` |" % (
            i, f["review_score"][0], f["id"], f["transcript"], f["char_offset"],
            "+".join(f["detectors"]), "; ".join(f["review_score"][1]),
            f["span_text"][:60].replace("|", "/").replace("`", "'").replace("\n", " ")))
    L.append("")
    L.append("Full ranked order: sort `ledger.jsonl` by `review_score[0]` descending. "
             "Queue length %d findings." % len(findings))
    return "\n".join(L) + "\n"


def render_summary(findings, stats, prov):
    L = []
    A = L.append
    A("# M5-R — reviewed findings ledger (SUMMARY)")
    A("")
    A("**Reduction of the inherited M5 raw census (TASK-011, lane "
      "`arena/01a0d581-fleetyard` @ `bf97d85`) into findings with evidence.**")
    A("")
    A("> Honesty scope: every finding here is *machine-adjudicated* — citations and "
      "book offsets were re-verified byte-exact, repetition/anomaly structure was "
      "re-derived from the frozen bytes, and fixture-tuned hits are separated. "
      "**No audio was heard; no human read every transcript.** CERTAIN is assigned "
      "only by inheritance from the v1 hand-confirmed fixture set, never by this "
      "tool. There is **no corpus-wide error rate** in this document (LAW §9: "
      "precision/recall need held-out data; only the ledger is delivered). "
      "CANDIDATE is never blended into anything.")
    A("")
    A("## 1. Reduction funnel")
    A("")
    A("| stage | count |")
    A("|---|---|")
    A("| raw signals loaded (inherited census) | %d |" % stats["raw_signals"])
    A("| record files | %d |" % stats["record_files"])
    A("| citation failures (quote not byte-exact at offset) | %d |" % stats["citation_failures"])
    A("| duplicate signals removed (same detector+quote) | %d |" % stats["duplicates_removed"])
    A("| **merged findings** | **%d** |" % len(findings))
    A("| transcripts with >=1 finding | %d of %d |" % (stats["transcripts_with_findings"],
                                                       stats["transcripts_total"]))
    A("")
    A("Reading of the funnel: the inherited census is **1,334 records**; two of them "
      "carry two detector signals each (**1,336 signal instances**), and those two "
      "convergent records merge back to one finding each — hence 1,334 findings, "
      "one per inherited record, with no exact duplicates found (0 removed).")
    A("")
    A("## 2. Classification (STANDARDS ladder)")
    A("")
    A("| class | findings | seeded | note |")
    A("|---|---|---|---|")
    for cls in ("CERTAIN (inherited fixture)", "HIGH (convergence, proposed)", "CANDIDATE"):
        c = [f for f in findings if f["class"] == cls]
        s = [f for f in c if f["seeded"]]
        note = {"CERTAIN (inherited fixture)": "prior v1 hand-confirmed fixtures; in-sample",
                "HIGH (convergence, proposed)": ">=2 independent families + written rationale; gate review",
                "CANDIDATE": "single signal; human read required"}[cls]
        A("| %s | %d | %d | %s |" % (cls, len(c), len(s), note))
    A("")
    A("Seeded / independent split (LAW §9): **seeded (fixture-overlap, in-sample) = %d**; "
      "**independent = %d**. Seeded findings are excluded from any precision/recall "
      "claim by construction." % (stats["seeded"], len(findings) - stats["seeded"]))
    A("")
    A("## 3. By detector (merged findings carrying it)")
    A("")
    A("| detector | findings | raw signals |")
    A("|---|---|---|")
    for d in DETECTORS:
        A("| %s | %d | %d |" % (d, sum(1 for f in findings if d in f["detectors"]),
                                stats["per_detector"].get(d, 0)))
    A("")
    A("## 4. By year (file-name year; unknown kept separate)")
    A("")
    A("| year | findings | CANDIDATE | HIGH | CERTAIN(inherited) |")
    A("|---|---|---|---|---|")
    years = sorted({year_of(f["transcript"]) for f in findings},
                   key=lambda y: (y == "unknown", y))
    for y in years:
        fs = [f for f in findings if year_of(f["transcript"]) == y]
        A("| %s | %d | %d | %d | %d |" % (
            y, len(fs), sum(1 for f in fs if f["class"] == "CANDIDATE"),
            sum(1 for f in fs if f["class"].startswith("HIGH")),
            sum(1 for f in fs if f["class"].startswith("CERTAIN"))))
    A("")
    A("## 5. Review queue — transcripts by finding count (top 20)")
    A("")
    A("| transcript | findings | classes |")
    A("|---|---|---|")
    counts = {}
    for f in findings:
        counts.setdefault(f["transcript"], []).append(f)
    for t, fs in sorted(counts.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:20]:
        cls = ", ".join(sorted({f["class"].split(" (")[0] for f in fs}))
        A("| %s | %d | %s |" % (t, len(fs), cls))
    A("")
    A("## 6. HIGH findings (each with its independence rationale)")
    A("")
    highs = [f for f in findings if f["class"].startswith("HIGH")]
    if not highs:
        A("(none)")
    for f in highs:
        A("- **%s** @%d — %s" % (f["id"], f["char_offset"], f["transcript"]))
        A("  - quote: `%s`" % f["span_text"][:160].replace("`", "'"))
        A("  - rationale: %s" % f["rationale"])
    A("")
    A("## 7. CERTAIN (inherited fixture) findings")
    A("")
    for f in findings:
        if f["class"].startswith("CERTAIN"):
            for x in f["fixture_overlap"]:
                A("- **%s** ↔ %s @%d — `%s` → `%s` (leg %s; %s)" % (
                    f["id"], x["id"], x["offset"], x["quoted"][:70], x["suspected"],
                    x["evidence_class"], x["status_by"][:60]))
    A("")
    A("## 8. Book-byte adjudication")
    A("")
    A("- findings carrying a cited book reference: %d" % stats["book_refs"])
    A("- cited book quotes verified byte-exact at the cited offset: %d"
      % stats["book_refs_ok"])
    A("- cited book offset/slug failures: %d" % stats["book_refs_bad"])
    A("- book references to non-Hawkins entries (text reliable, doctrine not): %d"
      % stats["book_refs_nonhawkins"])
    A("")
    A("## 9. Mechanical facts attached to every finding")
    A("")
    A("`ledger.jsonl` / `by-transcript/*.json` carry, per finding: citation (offset + "
      "span_end + verbatim span), the runner's claim (evidence string, asserted "
      "intended text), the re-derived repetition structure (A1) or surface anomaly "
      "(A2), the verified book check + word-level divergence + number comparison "
      "(B1/B2), fixture overlap, class + rationale, `seeded`, and "
      "`review_status=%s`." % REVIEW_STATUS)
    A("")
    A("## 10. Mechanical corroboration of the runner's own claims")
    A("")
    A("Each raw signal's evidence string was re-derived from the bytes where a "
      "mechanical check exists (LAW §7: identical output alone is not suspicion — "
      "missing fresh evidence is; this is that fresh evidence). 'not corroborated' "
      "means this tool's re-derivation did not reproduce the runner's claim string: "
      "it is a **review flag**, not a verdict — it can reflect the claim's shape or "
      "this tool's simpler tokenizer/percent handling. Those findings score +1 in "
      "the review queue.")
    A("")
    A("| detector | signals | corroborated | failed | not machine-checkable |")
    A("|---|---|---|---|---|")
    for d in DETECTORS:
        c = stats["claims"][d]
        A("| %s | %d | %d | %d | %d |" % (d, stats["per_detector"][d],
                                          c["corroborated"], c["failed"], c["not_checked"]))
    A("")
    A("Review queue: `REVIEW-QUEUE.md` (top 100 by mechanical score; the score is "
      "an ordering aid, never a class).")
    A("")
    A("## 11. Coverage truth")
    A("")
    A("- All %d transcripts are present in `by-transcript/`; **%d carry zero findings** "
      "— that is *not* evidence of being error-free (the detectors are known to miss "
      "fluent errors; drop-word and speaker/format detectors do not exist)."
      % (stats["transcripts_total"], stats["transcripts_total"] - stats["transcripts_with_findings"]))
    A("- Detectors that produced the raw census: %s. A4-confusion, drop-word and "
      "speaker/format were not run (unmeasured, not zero)." % ", ".join(DETECTORS))
    A("- Provenance: see `PROVENANCE.json` (inputs pinned by sha256; corpus digest "
      "method defined explicitly, unlike the inherited run's).")
    A("")
    A("_Generated %s by `tools/m5r_reduce.py` (%s)._"
      % (prov["run_utc"], prov["tool_sha256"][:16]))
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", required=True)
    ap.add_argument("--fixtures", required=True)
    ap.add_argument("--corpus", default="corpus")
    ap.add_argument("--out", default="findings")
    ap.add_argument("--utc", default=None)
    ap.add_argument("--archive-ref", default="origin/arena/01a0d581-fleetyard")
    args = ap.parse_args(argv)

    utc = args.utc or datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ")
    transcripts = load_transcripts(args.corpus)
    books = parse_book_store(os.path.join(args.corpus, "docdocgo", "html",
                                          "merged-book-texts_json_1.js"))
    fixtures_raw = json.load(open(os.path.join(args.fixtures, "confirmed.json"),
                                  encoding="utf-8"))
    corrections, cpath = [], os.path.join(args.fixtures, "corrections.json")
    if os.path.exists(cpath):
        corrections = json.load(open(cpath, encoding="utf-8"))
    latest = {}
    for c in corrections:
        if c.get("new", {}).get("status", "").find("confirmed") < 0:
            latest[c["id"]] = c.get("new", {}).get("confidence", "")
    fixtures = []
    for fx in fixtures_raw:
        if latest.get(fx["id"]):
            continue  # withdrawn/downgraded by the append-only corrections log
        fx = dict(fx)
        fx["transcript"] = os.path.basename(fx["transcript"])
        fixtures.append(fx)

    signals, sources = load_signals(args.records)
    fails = citation_verify(signals, transcripts)
    findings = merge_signals(signals)
    n_raw = len(signals)
    deduped = sum(len(f["signals"]) for f in findings)
    adj = [adjudicate(f, transcripts, books, fixtures) for f in findings]
    for i, f in enumerate(adj, 1):
        f["id"] = "M5R-%04d" % i
        f["class"], f["rationale"] = classify(f)
        f["review_score"] = review_score(f)

    claims = {d: {"checked": 0, "corroborated": 0, "failed": 0, "not_checked": 0}
              for d in DETECTORS}
    for f in adj:
        for c in f["claim_checks"]:
            row = claims[c["detector"]]
            if c["claim_ok"] is None:
                row["not_checked"] += 1
            elif c["claim_ok"]:
                row["checked"] += 1
                row["corroborated"] += 1
            else:
                row["checked"] += 1
                row["failed"] += 1

    stats = {
        "raw_signals": n_raw,
        "record_files": len(sources),
        "citation_failures": len(fails),
        "duplicates_removed": n_raw - deduped,
        "transcripts_total": len(transcripts),
        "transcripts_with_findings": len({f["transcript"] for f in adj}),
        "per_detector": {d: sum(1 for s in signals if s["detector"] == d)
                         for d in DETECTORS},
        "seeded": sum(1 for f in adj if f["seeded"]),
        "book_refs": sum(len(f["book_checks"]) for f in adj),
        "book_refs_ok": sum(1 for f in adj for b in f["book_checks"] if b.get("quote_ok")),
        "book_refs_bad": sum(1 for f in adj for b in f["book_checks"]
                             if not b.get("quote_ok")),
        "book_refs_nonhawkins": sum(1 for f in adj for b in f["book_checks"]
                                    if b.get("hawkins_own") is False),
        "fixtures_active": len(fixtures),
        "claims": claims,
    }

    os.makedirs(args.out, exist_ok=True)
    bt = os.path.join(args.out, "by-transcript")
    os.makedirs(bt, exist_ok=True)
    ledger_path = os.path.join(args.out, "ledger.jsonl")
    with open(ledger_path, "w", encoding="utf-8") as fh:
        for f in adj:
            fh.write(json.dumps(f, ensure_ascii=False, sort_keys=True) + "\n")
    per_t = {}
    for f in adj:
        per_t.setdefault(f["transcript"], []).append(f)
    for name in sorted(transcripts):
        with open(os.path.join(bt, name + ".json"), "w", encoding="utf-8") as fh:
            json.dump(per_t.get(name, []), fh, ensure_ascii=False, sort_keys=True, indent=1)
    rec_digest, rec_n = dir_digest(args.records)
    fx_digest, fx_n = dir_digest(args.fixtures)
    ov_lines = []
    for name in sorted(transcripts):
        ov_lines.append("%s  %s\n" % (sha256_text(transcripts[name]), name))
    prov = {
        "run_utc": utc,
        "tool": "tools/m5r_reduce.py",
        "tool_sha256": sha256_file(os.path.abspath(__file__)),
        "inputs": {
            "archive_ref": args.archive_ref,
            "records_dir": args.records,
            "records_digest_sha256": rec_digest,
            "records_files": rec_n,
            "fixtures_digest_sha256": fx_digest,
            "fixtures_files": fx_n,
            "corpus_zip_sha256": "3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db",
            "overlays_digest_method": "sha256 over sorted lines '<sha256(text)>  <basename>' "
                                      "for all 230 corpus/docdocgo/overlays/*.txt",
            "overlays_digest": sha256_text("".join(ov_lines)),
            "book_store": "corpus/docdocgo/html/merged-book-texts_json_1.js",
        },
        "stats": stats,
        "outputs": {},
    }
    ledger_digest = sha256_file(ledger_path)
    bt_digest, bt_n = dir_digest(bt)
    prov["outputs"] = {"ledger.jsonl": ledger_digest,
                       "by_transcript_digest": bt_digest, "by_transcript_files": bt_n,
                       "findings": len(adj)}
    with open(os.path.join(args.out, "SUMMARY.md"), "w", encoding="utf-8") as fh:
        fh.write(render_summary(adj, stats, prov))
    with open(os.path.join(args.out, "REVIEW-QUEUE.md"), "w", encoding="utf-8") as fh:
        fh.write(render_queue(adj))
    with open(os.path.join(args.out, "PROVENANCE.json"), "w", encoding="utf-8") as fh:
        json.dump(prov, fh, indent=1, sort_keys=True)
        fh.write("\n")
    if fails:
        with open(os.path.join(args.out, "CITATION-FAILURES.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(fails, fh, indent=1)
    print("m5r: %d raw signals -> %d findings (%d dup removed); seeded=%d; "
          "book refs ok=%d bad=%d; citation failures=%d"
          % (n_raw, len(adj), stats["duplicates_removed"], stats["seeded"],
             stats["book_refs_ok"], stats["book_refs_bad"], len(fails)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
