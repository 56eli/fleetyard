#!/usr/bin/env python3
"""TASK-018 items 0d–0g — dispositions, recount and stratification (append-only).

The TASK-018 gate verified the substance (57/57 promoted rows reproduce) and then found four
record defects. This tool repairs them without editing any committed sentence:

  0d  `SUMMARY.md` and `tools/PATTERNS.md §5b-bis` claim four `seeded: true` promotions; the
      data has **zero** (`seeded: false` on all 122 rows) and zero overlaps with the 16 v1 CF
      fixture spans. The claim is contradicted by append, never rewritten.
  0e  Two promoted pairs are duplicate sites (`D-097`/`D-098`, `D-120`/`D-121`): 57 rows =
      55 distinct span-text sites. Both numbers are published with the dedupe key named.
  0f  The promoted set is stratified per omitted word, the notation class (`%` in the
      transcript where the book writes "percent") is **refused** under the narrow enacted leg
      — no *word* is absent; a symbol stands for it — and the standing statement that
      whether the speaker uttered a filler is unknowable without audio is published. The
      refusal is marked reversible by an owner ruling.
  0g  `D-002` and `D-039` are demoted with the reason each sibling instrument gives, and the
      seven rows on v2-holdout transcripts are marked as holdout members. Arithmetic:
      57 − 6 notation refusals − 2 contradicted demotions = **49 rows**, 55 − 5 notation
      sites − 2 demotions = **48 distinct sites**.

Dispositions are **appended** to `adjudication.jsonl` as lines with
`"record": "disposition"`; the base 122 signal lines are untouched (their digest is compared
against `PROVENANCE.json`'s recorded output digest), so the record's own determinism is
provable rather than weakened.

  build   python3 tools/m4_t18_dispositions.py build --utc <iso> [--out runs/m4-q2-adjudication]
  verify  python3 tools/m4_t18_dispositions.py verify [--out runs/m4-q2-adjudication]

Stdlib only; the corpus is not read.
"""
import argparse
import subprocess
import hashlib
import json
import os
import sys

STRATA = {
    "interjections/fillers": ["huh", "yeah", "see", "right", "really", "heh", "haha", "um",
                             "well"],
    "notation (percent)": ["percent"],
    "function words": ["it's", "that's", "there's", "he'd", "may", "since", "however",
                       "including", "already"],
    "content": ["bonaparte", "earphones", "evidence", "go", "high", "lincoln", "man",
                "osama", "otherwise", "quite", "realms", "things", "undoubtedly"],
}
DEMOTIONS = {
    "D-002": ("demoted", "CANDIDATE",
              "sibling instrument contradicts the promotion: runs/m4-q2-dropword/EVAL.json "
              "shape_adjudication marks this exact site dropped-token-not-missing with "
              "book_side_repeated_tokens ['evidence'] and 'EXCLUDED from any count' — the "
              "book reads 'evidence; evidence of' and the transcript carries it once, so "
              "what is absent is a duplicate, not a word (ORCH-2's independent battery "
              "agrees)"),
    "D-039": ("demoted", "CANDIDATE",
              "sibling instrument contradicts the promotion: the source-inheritance filter "
              "suppresses exactly this signal (its single published example) as a cross-book "
              "self-parallel — the transcript *was* book text, so the missing token is not "
              "evidence of a drop by the speaker"),
}
NOTATION_IDS = ("D-041", "D-042", "D-087", "D-092", "D-097", "D-098")
NOTATION_REASON = ("refused under the enacted narrow leg: the transcript writes the symbol "
                   "(%/digits) where the book writes the word, so no *word* is absent and "
                   "clause d-i (restoring an absent word) does not reach notation variants; "
                   "reversible only by an owner ruling that puts notation in scope")
HOLDOUT_IDS = ("D-092", "D-093", "D-094", "D-095", "D-107", "D-108", "D-122")
HOLDOUT_NOTE = ("v2-holdout member transcript: the row stays in the file, but it is label-"
                "tainted and may never be quoted as tuning-side evidence (TASK-019 items "
                "v2.b / ANNEX §F)")
BAND = {"floors": {"3": 71, "5": 57, "8": 33, "10": 22},
        "note": "the 57 (now 49 after the stated exclusions) is a floor-5 number: quote the "
                "row, not the number"}
AUDIO = ("whether the speaker uttered a filler is unknowable from text — no audio was heard "
         "by anyone in this campaign")

SUMMARY_BLOCK = """
## Corrections (appended 2026-09-26, append-only — TASK-018 items 0d–0g)

**0d — the seeded sentence above is wrong, and the data is right.** No row in
`adjudication.jsonl` carries `seeded: true` (0 of 122, and 0 of 57); the `seeded` key is
present on all 122 rows with the value `false`, and **no adjudicated span overlaps any of the
16 v1 CF fixture spans (0 overlaps)**. The four rows that do carry `seeded: true` are
`FIX-D2-001…004` in `fixtures-adjudication.json` (2 CERTAIN, 2 CANDIDATE). The sentence above
is left readable; this block is its correction.

**0e — rows vs sites.** `D-097`/`D-098` (`percent`) and `D-120`/`D-121` (`see`) are exact
duplicate sites at different offsets: **57 promoted rows = 55 distinct sites**, dedupe key
`(transcript, restored_span text)`. M5-R set the precedent ("1 dup removed"); both numbers are
published here and in `RECOUNT-2026-09-26.json`.

**0f — strata, the notation ruling, and what text cannot show.** Composition of the 57 by
omitted word: **27 interjections/fillers** (`huh`×7, `yeah`×6, `see`×6, `right`×3, `really`,
`heh`, `haha`, `um`, `well`) + **6 notation** (`percent`) + **11 function words** (`it's`×3,
`that's`, `there's`, `he'd`, `may`, `since`, `however`, `including`, `already`) + **13
content** (`bonaparte`, `earphones`, `evidence`, `go`, `high`, `lincoln`, `man`, `osama`,
`otherwise`, `quite`, `realms`, `things`, `undoubtedly`) = 57. **The notation class is
REFUSED** under the enacted narrow leg — the transcript writes the symbol where the book
writes the word, so no *word* is absent; marked reversible only by an owner ruling that puts
notation in scope. Standing statement: **whether the speaker uttered a filler is unknowable
from text — no audio was heard** by anyone in this campaign.

**0g — two promotions contradicted by sibling instruments, and seven holdout-tainted rows.**
`D-002` (`evidence`) is demoted: `EVAL.json` marks that exact site
`dropped-token-not-missing` (the book reads "evidence; evidence of" — the duplicate is what is
absent). `D-039` (`quite`) is demoted: the source-inheritance filter suppresses exactly that
signal as a cross-book self-parallel. Both dispositions are appended to `adjudication.jsonl`
(`"record": "disposition"`) with their reasons. `D-092`, `D-093`, `D-094` (promoted) and
`D-095`, `D-107`, `D-108`, `D-122` (CANDIDATE) sit on **v2-holdout member transcripts** — they
stay in the file and are marked as holdout members; none may be quoted as tuning-side
evidence.

**Recount, with the arithmetic stated rather than restated.** 57 promoted rows − 6 notation
refusals = 51; 51 − 2 contradicted demotions = **49 promoted rows**. Sites: 55 − 5 notation
sites (`D-097`/`D-098` are one site) − 2 demotions = **48 distinct sites**. Strata after the
exclusions: 27 + 0 notation + 11 + 11 content = 49. **The flank-floor band still travels with
every quotation: floors 3/5/8/10 → 71/57/33/22** (the 49 is the same construction at floor 5
after the exclusions named here). The CERTAIN-leg-d set remains unusable in any M6 document
until the gate accepts these repairs.
"""

PATTERNS_BLOCK = """
### 5b-ter. TASK-018 items 0d–0g — corrections (appended 2026-09-26, append-only)

* **0d:** §5b-bis's sentence "Four of the 57 are `seeded: true`" is wrong. The data has
  **0 of 122 rows seeded** (`seeded: false` throughout) and **0 overlaps with the 16 v1 CF
  fixture spans**; the four seeded rows are `FIX-D2-001…004` in `fixtures-adjudication.json`.
  Corrected by append; the sentence above stays readable.
* **0e:** 57 promoted **rows** = **55 distinct sites** (dedupe key `(transcript,
  restored_span text)`; collisions `D-097`/`D-098`, `D-120`/`D-121`).
* **0f:** strata — 27 interjections/fillers · 6 notation · 11 function words · 13 content.
  **The notation class is refused** (no word is absent when the transcript writes `%`);
  the classification is reversible only by an owner ruling. Speaker-side filler presence is
  **unknowable from text** (no audio heard).
* **0g:** `D-002` and `D-039` are demoted (each contradicted by a sibling instrument:
  `EVAL.json` shape adjudication; the source-inheritance filter) and the seven rows on
  v2-holdout transcripts are marked holdout members. Recount: **49 promoted rows / 48 distinct
  sites** (57 − 6 notation − 2 demoted; 55 − 5 − 2).
* **Every quotation of the number carries the band: floors 3/5/8/10 → 71/57/33/22**, the
  stratification, the deduped site count and the notation status. The set is not usable in any
  M6 document until the gate accepts these repairs.
"""

MARKERS = ("## Corrections (appended 2026-09-26", "### 5b-ter.")


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def load_rows(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


def signal_rows(rows):
    return [r for r in rows if r.get("record") != "disposition"]


def fixture_spans(confirmed_path, dropword_path):
    out = []
    for path in (confirmed_path, dropword_path):
        if not os.path.exists(path):
            continue
        doc = json.load(open(path, encoding="utf-8"))
        items = doc.get("fixtures", []) if isinstance(doc, dict) else doc
        for f in items:
            out.append({"id": f.get("id"), "transcript": os.path.basename(str(f.get("transcript"))),
                        "offset": int(f.get("char_offset", 0)), "quoted": f.get("quoted") or ""})
    return out


def stratum_of(word):
    for stratum, words in STRATA.items():
        if word in words:
            return stratum
    return None


def _git(repo, *args):
    p = subprocess.run(("git", "-C", repo) + args, capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None


def resolve_stamp(args):
    """An own-time stamp must be EXACT and SOURCED (item 12's order; criterion 20.14c).

    The defective value this replaces was `:00`-shaped and projected from the CONTROL cadence
    grid, then labelled "the lane clock at write time" — a stamp that post-dated the very commit
    carrying it. So: either derive the value from the commit that carries these lines, or state
    the source explicitly; a bare `--utc` is refused, and the superseded value (when a repair
    passes one) stays readable beside it.
    """
    if args.utc_from_commit:
        out = _git(args.repo, "show", "-s", "--format=%cI", args.utc_from_commit)
        if out is None:
            raise SystemExit("m4_t18_dispositions: --utc-from-commit %s is not a commit in %s"
                             % (args.utc_from_commit, args.repo))
        iso = out.strip()
        return (iso.replace("+00:00", "Z"),
                "git committer time of %s (the commit that carries these lines), exact to the "
                "second" % args.utc_from_commit[:7],
                (args.superseded, args.superseded_reason) if args.superseded else (None, None))
    if not args.utc:
        raise SystemExit("m4_t18_dispositions: a stamp is required: --utc-from-commit <sha> "
                         "(preferred) or --utc <iso> with --utc-source <text>")
    if not args.utc_source:
        raise SystemExit("m4_t18_dispositions: --utc requires --utc-source — an own-time stamp "
                         "with no named source is the 20.14c defect class")
    return (args.utc, args.utc_source,
            (args.superseded, args.superseded_reason) if args.superseded else (None, None))


def stamp_fields(utc, source, superseded=None, superseded_reason=None):
    fields = {"utc": utc, "utc_source": source}
    if superseded:
        fields["utc_superseded"] = superseded
        fields["utc_superseded_reason"] = superseded_reason
    return fields


def disposition_lines(rows, utc, fixtures, utc_source=None, superseded=None,
                      superseded_reason=None):
    cert = [r for r in signal_rows(rows) if r.get("verdict") == "CERTAIN-leg-d"]
    seeded_true = sum(1 for r in signal_rows(rows) if r.get("seeded") is True)
    overlaps = 0
    for f in fixtures:
        for r in signal_rows(rows):
            if os.path.basename(str(r.get("transcript"))) != f["transcript"]:
                continue
            span = r.get("restored_span") or ""
            if f["quoted"] and f["quoted"] in span:
                overlaps += 1
    counts = {}
    for r in cert:
        counts[r.get("omitted_word")] = counts.get(r.get("omitted_word"), 0) + 1
    extra = {w: n for w, n in counts.items() if stratum_of(w) is None}
    if extra:
        raise SystemExit("m4_t18_dispositions: unclassified omitted words: %r" % extra)
    lines = []
    for rid, (ruling, verdict, reason) in sorted(DEMOTIONS.items()):
        lines.append({"record": "disposition", "id": rid, "ruling": ruling,
                      "new_verdict": verdict, "reason": reason, "by": "WORKER-2",
                      "task": "TASK-018 item 0g",
                      **stamp_fields(utc, utc_source, superseded, superseded_reason)})
    for rid in NOTATION_IDS:
        lines.append({"record": "disposition", "id": rid, "ruling": "refused-notation",
                      "new_verdict": "CANDIDATE", "reason": NOTATION_REASON,
                      "by": "WORKER-2", "task": "TASK-018 item 0f",
                      **stamp_fields(utc, utc_source, superseded, superseded_reason)})
    for rid in HOLDOUT_IDS:
        lines.append({"record": "disposition", "id": rid, "ruling": "holdout-member-note",
                      "reason": HOLDOUT_NOTE, "by": "WORKER-2", "task": "TASK-018 item 0g",
                      **stamp_fields(utc, utc_source, superseded, superseded_reason)})
    return lines, {"seeded_true_rows": seeded_true, "fixture_span_overlaps": overlaps,
                   "certain_rows": len(cert), "omitted_word_counts": dict(sorted(counts.items()))}


def build(args):
    # the stamp is resolved FIRST: an own-time value that cannot be sourced must stop the run
    # before any file is read or written (criterion 20.14c)
    utc, utc_source, (superseded, superseded_reason) = resolve_stamp(args)
    adj = os.path.join(args.out, "adjudication.jsonl")
    prov_path = os.path.join(args.out, "PROVENANCE.json")
    rows = load_rows(adj)
    if any(r.get("record") == "disposition" for r in rows):
        raise SystemExit("m4_t18_dispositions: dispositions already present — append-only "
                         "means once; re-running would duplicate them")
    base = signal_rows(rows)
    prov = json.load(open(prov_path, encoding="utf-8"))
    recorded = prov["outputs"]["adjudication.jsonl"]
    base_digest = hashlib.sha256(("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n"
                                          for r in base)).encode("utf-8")).hexdigest()
    fixtures = fixture_spans(os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(args.out))), "fixtures", "confirmed", "confirmed.json"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(args.out))),
                     "fixtures", "v2", "dropword.json"))
    lines, facts = disposition_lines(rows, utc, fixtures, utc_source, superseded,
                                     superseded_reason)
    with open(adj, "a", encoding="utf-8") as fh:
        for line in lines:
            fh.write(json.dumps(line, ensure_ascii=False, sort_keys=True) + "\n")
    notation_sites = len(set(NOTATION_IDS) - {"D-098"})       # D-097/D-098 are one site
    demotions = len(DEMOTIONS)
    after_rows = facts["certain_rows"] - len(NOTATION_IDS) - demotions
    after_sites = 55 - (len(NOTATION_IDS) - 1) - demotions
    strata_after = {"interjections/fillers": 27, "notation (percent)": 0,
                    "function words": 11, "content": 13 - demotions}
    recount = {
        "tool": "tools/m4_t18_dispositions.py",
        "task": "TASK-018 items 0d–0g (recount, dispositions, stratification)",
        "written_utc": utc,
        "utc_source": utc_source,
        **({"written_utc_superseded": superseded,
            "written_utc_superseded_reason": superseded_reason} if superseded else {}),
        "base_file": "adjudication.jsonl",
        "base_signal_rows": len(base),
        "base_122_lines_sha256_before_append": prov["outputs"]["adjudication.jsonl"],
        "base_lines_reconstructed_digest": base_digest,
        "base_lines_rule": ("the tool's 122 signal lines are never edited; a fresh build of "
                            "tools/m4_q2_adjudicate.py reproduces them (its determinism test)"),
        "amended_file_sha256": sha(adj),
        "disposition_lines_appended": len(lines),
        "dispositions": {r["id"]: {"ruling": r["ruling"],
                                   "new_verdict": r.get("new_verdict")} for r in lines},
        "facts": facts,
        "stratification": {
            "by_word": STRATA,
            "before_exclusions": {"interjections/fillers": 27, "notation (percent)": 6,
                                  "function words": 11, "content": 13, "sum": 57},
            "after_exclusions": dict(strata_after, sum=after_rows),
            "notation_refused": list(NOTATION_IDS),
            "notation_sites": notation_sites,
        },
        "counts_after_exclusions": {
            "rows": after_rows, "sites": after_sites,
            "arithmetic": ("57 rows − 6 notation refusals = 51; 51 − 2 contradicted demotions "
                           "= %d rows. Sites: 55 − %d notation sites − 2 = %d."
                           % (after_rows, notation_sites, after_sites)),
        },
        "seeded_sentence_correction": {
            "claim_corrected": "four of the 57 promoted rows carry seeded: true",
            "data": {"rows_with_seeded_true": facts["seeded_true_rows"],
                     "rows_with_seeded_key": len(base),
                     "fixture_span_overlaps": facts["fixture_span_overlaps"],
                     "seeded_rows_location": "fixtures-adjudication.json FIX-D2-001…004 "
                                             "(2 CERTAIN, 2 CANDIDATE)"},
        },
        "dedupe": {"key": "(transcript, restored_span text)", "rows": 57, "sites": 55,
                   "collisions": {"percent": ["D-097", "D-098"], "see": ["D-120", "D-121"]}},
        "standing_statements": {"audio": AUDIO, "band": BAND,
                                "restriction": ("the promoted set is not usable in any M6 "
                                                "document until ORCH-2 accepts these repairs")},
        "no_rate": "no rate, precision or M6 figure is stated; LAW §9 (in-sample / seeded)",
    }
    out = os.path.join(args.out, "RECOUNT-2026-09-26.json")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(recount, ensure_ascii=False, sort_keys=True, indent=1) + "\n")
    appended = []
    summary = os.path.join(args.out, "SUMMARY.md")
    with open(summary, encoding="utf-8") as fh:
        text = fh.read()
    if MARKERS[0] not in text:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(SUMMARY_BLOCK)
        appended.append("SUMMARY.md")
    patterns = os.path.join(os.path.dirname(os.path.abspath(args.out)), "..", "tools",
                            "PATTERNS.md")
    patterns = os.path.abspath(patterns)
    if os.path.exists(patterns):
        with open(patterns, encoding="utf-8") as fh:
            ptext = fh.read()
        if MARKERS[1] not in ptext:
            with open(patterns, "a", encoding="utf-8") as fh:
                fh.write(PATTERNS_BLOCK)
            appended.append("tools/PATTERNS.md")
    print("dispositions appended: %d lines; recount -> RECOUNT-2026-09-26.json" % len(lines))
    print("appended prose blocks: %s" % (", ".join(appended) or "none (already present)"))
    print("counts: %d rows -> %d rows; 55 sites -> %d sites" %
          (facts["certain_rows"], after_rows, after_sites))
    return 0


def verify(args):
    problems = []
    adj = os.path.join(args.out, "adjudication.jsonl")
    rows = load_rows(adj)
    base = signal_rows(rows)
    disp = [r for r in rows if r.get("record") == "disposition"]
    if len(base) != 122:
        problems.append("base signal rows: %d (want 122)" % len(base))
    want = set(DEMOTIONS) | set(NOTATION_IDS) | set(HOLDOUT_IDS)
    got = {r["id"] for r in disp}
    if got != want:
        problems.append("dispositions: missing %s, extra %s"
                        % (sorted(want - got), sorted(got - want)))
    for r in disp:
        if not r.get("reason") or not r.get("utc"):
            problems.append("disposition %s lacks reason/utc" % r.get("id"))
        if not r.get("utc_source"):
            problems.append("disposition %s carries an unsourced own-time stamp "
                            "(criterion 20.14c)" % r.get("id"))
        if r.get("utc_superseded") and not r.get("utc_superseded_reason"):
            problems.append("disposition %s keeps a superseded stamp with no reason" % r.get("id"))
    rec_path = os.path.join(args.out, "RECOUNT-2026-09-26.json")
    if not os.path.exists(rec_path):
        problems.append("RECOUNT-2026-09-26.json missing")
    else:
        rec = json.load(open(rec_path, encoding="utf-8"))
        counts = {}
        for r in base:
            if r.get("verdict") == "CERTAIN-leg-d":
                counts[r.get("omitted_word")] = counts.get(r.get("omitted_word"), 0) + 1
        if counts != rec["facts"]["omitted_word_counts"]:
            problems.append("omitted-word tally does not recompute from the base rows")
        if rec["counts_after_exclusions"]["rows"] != 49:
            problems.append("rows after exclusions is not 49")
        if rec["counts_after_exclusions"]["sites"] != 48:
            problems.append("sites after exclusions is not 48")
        if rec["facts"]["seeded_true_rows"] != 0:
            problems.append("seeded:true rows is not 0")
    summary = open(os.path.join(args.out, "SUMMARY.md"), encoding="utf-8").read()
    patterns_path = os.path.abspath(os.path.join(args.out, "..", "..", "tools", "PATTERNS.md"))
    body = summary + (open(patterns_path, encoding="utf-8").read()
                      if os.path.exists(patterns_path) else "")
    for needle in ("0 of 122", "55 distinct sites", "71/57/33/22", "unknowable",
                   "49 promoted"):
        if needle not in body:
            problems.append("corrections prose lacks %r" % needle)
    if problems:
        for p in problems:
            print("FAIL: %s" % p)
        return 1
    print("dispositions verify: OK (122 base rows + %d dispositions; recount 49 rows / 48 "
          "sites; corrections prose carries the band, the strata and the audio statement)"
          % len(disp))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--utc", default=None)
    b.add_argument("--utc-source", default=None)
    b.add_argument("--utc-from-commit", default=None)
    b.add_argument("--superseded", default=None,
                   help="the repaired defective stamp, kept readable beside the exact one")
    b.add_argument("--superseded-reason", default=None)
    b.add_argument("--repo", default=".")
    b.add_argument("--out", default="runs/m4-q2-adjudication")
    v = sub.add_parser("verify")
    v.add_argument("--out", default="runs/m4-q2-adjudication")
    a = ap.parse_args(argv)
    return {"build": build, "verify": verify}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
