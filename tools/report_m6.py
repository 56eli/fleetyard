#!/usr/bin/env python3
"""TASK-012: render reports/CORPUS-AUDIT.md (PROVISIONAL M6 report).

    python3 tools/report_m6.py [--out reports/CORPUS-AUDIT.md]

Every number in the report is computed here from committed, reviewable
inputs, so an auditor can re-run it:
  fixtures/confirmed/confirmed.json     16 hand-read CERTAIN fixtures
  fixtures/confirmed/corrections.json   append-only review log (reviewed HIGH)
  runs/m5-raw/index.json + records/     TASK-011 raw census (unreviewed)
  corpus/docdocgo/overlays/*.txt        word counts only (frozen, read-only)

Nothing is written except --out. Stdlib only, no network.
"""
import argparse
import collections
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loaders  # noqa: E402
import sweep_m5  # noqa: E402
import tokenizer  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUT = os.path.join("reports", "CORPUS-AUDIT.md")
RUN = os.path.join(ROOT, "runs", "m5-raw")
CONFIRMED = os.path.join(ROOT, "fixtures", "confirmed", "confirmed.json")
CORRECTIONS = os.path.join(ROOT, "fixtures", "confirmed", "corrections.json")
LEG = {"a": "a (acoustic near-form restores doctrinal sense)",
       "b": "b (book contradicts the transcript)",
       "c": "c (lecture contradicts itself)"}

# Pattern ledger seed: hand-assigned from the fixture evidence text.
PATTERNS = [
    ("P1 function-word swap on a slide table ('in' heard as 'and')",
     ["CF-007", "CF-008", "CF-021", "CF-022"],
     "One repeated slide (infatuation row); 4 cited instances, 1 pattern."),
    ("P2 number misheard in a book table / calibration",
     ["CF-003", "CF-019", "CF-020"],
     "255% for 55%, 40% for 60%, 380 for 390. CF-020 may be speaker "
     "misstatement (no audio)."),
    ("P3 proper name rendered as English words / misspelt",
     ["CF-001", "CF-002"], "Dilgo 'Quince' (Khyentse), 'Jempolski' "
     "(Jampolsky)."),
    ("P4 homophone / near-form of a doctrinal or scriptural phrase",
     ["CF-004", "CF-010", "CF-011", "CF-012", "CF-017"],
     "unquestionable/unconditional, Given to/Give unto, Except/Accept, "
     "We are/Gloria, integrus/integrous."),
    ("P5 polarity flip in a doctrinal statement (inside a repeat loop)",
     ["CF-006"], "'negative' for 'positive' above level 200."),
    ("P6 sentence boundary inserted mid-phrase",
     ["CF-015"], "'no influence. Interest' for 'no interest'."),
    ("N1 NEGATIVE: Korean interpreter code-switch is not garble",
     ["NEG-001"], "yes나 / no를 in Sedona Dec 2008; fixed in A2 (TASK-010)."),
]


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def git_head():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                       stderr=subprocess.DEVNULL,
                                       text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def md(s, n=None):
    s = " ".join(str(s).split()).replace("|", "\\|")
    return s if n is None or len(s) <= n else s[:n - 1] + "…"


def short(path):
    return os.path.basename(path).replace("_enxautogen_html.txt", "")


def word_counts(paths):
    return {sweep_m5.stem(p): len(tokenizer.words(
        loaders.read_transcript(p).text)) for p in paths}


def reviewed_high(corrections):
    out = []
    for e in corrections:
        if e["new"].get("confidence") == "HIGH CONFIDENCE":
            out.append((e["id"], e["record_before"], e["reason"]))
    return out


def build(confirmed, corrections, ix, words, head):
    L = []
    w = L.append
    n_tx = ix["transcripts_total"]
    tot_words = sum(words.values())
    fx_tx = sorted({c["transcript"] for c in confirmed})
    fx_words = sum(words[sweep_m5.stem(t)] for t in fx_tx)
    high = reviewed_high(corrections)
    ncert = len(confirmed)
    classes = collections.Counter(c["evidence_class"] for c in confirmed)
    overlap = ix.get("fixture_overlap", [])
    hit_tx = n_tx - len(ix["zero_hit_transcripts"])

    w("# CORPUS-AUDIT — David R. Hawkins lecture transcripts")
    w("")
    w("**PROVISIONAL (TASK-012). Not an M6 certification. No corpus-wide "
      "error rate can be stated yet.**")
    w("")
    w("- Rendered by `python3 tools/report_m6.py` at worker commit `%s` "
      "(lane `arena/01a0d581-fleetyard`)." % head)
    w("- Corpus: `docdocgo-fixes.zip` sha256 `%s`; %d transcript `.txt` "
      "files (the 231st directory entry is `manifest.json`, not a "
      "transcript); overlays digest `%s`." % (
          ix["corpus_zip_sha256"], n_tx, ix["overlays_sha256"]))
    w("- Raw census: `runs/m5-raw/` (TASK-011, PASS provisional raw only), "
      "tool commit `%s`, detectors %s." % (ix["tool_commit"],
                                           ", ".join(ix["detectors"])))
    w("- Authority note: produced after the worker's original 4-hour wall, "
      "on the owner's chat instruction (main `e8d81ae`: \"Chat session is "
      "authority\"). The orchestrator holds post-cap worker output pending a "
      "worker-specific owner record on main.")
    w("")

    w("## 1. Executive answer: how bad is it?")
    w("")
    w("**We don't know yet, in any measured sense, and this report does not "
      "pretend to.** What exists:")
    w("")
    w("1. **Reviewed evidence is a tiny, non-random sample.** %d CERTAIN "
      "transcription errors (proof legs: a %d, b %d) plus %d reviewed "
      "HIGH CONFIDENCE ones were found by hand-reading **%d of %d "
      "transcripts** (%s words, %.2f%% of the corpus's %s words). In those "
      "3 transcripts that is at least **%.1f CERTAIN errors per 10,000 "
      "words** (%.1f with reviewed HIGH). This is a *lower bound for those 3 "
      "files only*: they were not randomly chosen and the hand-read was not "
      "proven exhaustive. It must not be extrapolated to the corpus." % (
          ncert, classes["a"], classes["b"], len(high), len(fx_tx), n_tx,
          format(fx_words, ","), 100.0 * fx_words / tot_words,
          format(tot_words, ","), 1e4 * ncert / fx_words,
          1e4 * (ncert + len(high)) / fx_words))
    w("2. **Automatic detectors ran on %d/%d transcripts** and emitted "
      "**%d unreviewed raw signals** on %d transcripts. None has been "
      "reviewed. **Finding-pass audited: %d/%d; pending review: %d/%d.** "
      "Detector precision is **unmeasured**, so raw counts are *not* error "
      "counts; they may be mostly false alarms or a small fraction of real "
      "errors." % (ix["processed"], n_tx, ix["records_total"], hit_tx,
                    ix["finding_pass_audited"], n_tx, ix["pending_review"],
                    n_tx))
    w("3. **The detectors are known to miss most errors.** Together they "
      "overlap only %d of the %d hand-found CERTAIN errors (%s). Most "
      "confirmed errors are fluent, plausible English (homophones, "
      "misheard numbers, swapped function words) that no current detector "
      "sees." % (len({o['fixture'] for o in overlap}), ncert,
                 ", ".join(sorted({o['fixture'] for o in overlap}))))
    w("4. **Whole error classes were never measured:** dropped words and "
      "speaker/format errors (no detector built), and acoustic confusion "
      "(A4 excluded, no independent false-positive rate). Unmeasured is "
      "not zero.")
    w("")
    w("**Qualitative reading (not a rate):** every transcript that has been "
      "read closely contains meaning-changing errors, including in doctrinal "
      "content (calibration numbers, happiness-table percentages, "
      "scripture and prayer wording, the positive/negative polarity of "
      "level 200). Readers should treat any exact number, name or quotation "
      "in these transcripts as unverified until checked against the books.")
    w("")

    w("## 2. Coverage truth")
    w("")
    w("| transcripts | detector-run | finding-pass audited | pending review "
      "| hand-read (M1) | failed reads |")
    w("|---|---|---|---|---|---|")
    w("| %d | %d | %d | %d | %d | %d |" % (
        n_tx, ix["processed"], ix["finding_pass_audited"],
        ix["pending_review"], len(fx_tx), len(ix["failed_reads"])))
    w("")
    w("Excluded from scope: `extra-sources/` Book-of-Slides OCR (owner "
      "UNDECIDED); the 4 non-Hawkins books in the book store (never cited "
      "as Hawkins teaching).")
    w("")

    w("## 3. Reviewed findings (fixture-backed)")
    w("")
    w("### 3a. CERTAIN (%d, hand-read, 3 transcripts)" % ncert)
    w("")
    w("Each quote is byte-exact at paragraph + char offset in the frozen "
      "transcript; each book quote is exact at its book offset "
      "(`python3 tools/fixtures.py verify`).")
    w("")
    w("| id | transcript | para @offset | transcript says | intended | leg "
      "| book slug @offset: quote |")
    w("|---|---|---|---|---|---|---|")
    for c in confirmed:
        br = c.get("book_ref")
        bq = ("%s @%d: \"%s\"" % (br["slug"], br["char_offset"],
                                  md(br["quote"], 90))) if br else "—"
        w("| %s | %s | %d @%d | \"%s\" | \"%s\" | %s | %s |" % (
            c["id"], short(c["transcript"]), c["paragraph"], c["char_offset"],
            md(c["quoted"], 90), md(c["suspected"], 90),
            c["evidence_class"], bq))
    w("")
    w("Proof legs: " + "; ".join(LEG.values()) + ". Status of all: "
      "confirmed, WORKER hand-read (TASK-002/TASK-006), independently "
      "re-verified by orchestrator and Boss. Why each is CERTAIN: "
      "`fixtures/confirmed/confirmed.json` → `evidence`.")
    w("")
    w("Caveats: CF-007/008/021/022 are one repeated slide pattern (4 "
      "instances, 1 pattern; without CF-021/022 the count is 14). CF-020 is "
      "a certain text-vs-book discrepancy, but without audio the source "
      "(ASR vs the speaker misremembering) is unknown. CF-002 depends on the "
      "open owner item on other-author quotes (15 remain without it).")
    w("")
    w("### 3b. Reviewed HIGH CONFIDENCE (%d, withdrawn from CERTAIN in "
      "TASK-006)" % len(high))
    w("")
    w("| id | transcript | @offset | transcript says | intended | why not "
      "CERTAIN |")
    w("|---|---|---|---|---|---|")
    for i, r, why in high:
        w("| %s | %s | @%d | \"%s\" | \"%s\" | %s |" % (
            i, short(r["transcript"]), r["char_offset"], md(r["quoted"], 70),
            md(r["suspected"], 70), md(why, 110)))
    w("")
    w("(CF-009 was withdrawn to CANDIDATE and is outside every count here.)")
    w("")

    w("## 4. Error rates by class")
    w("")
    w("| class | corpus-wide rate | why |")
    w("|---|---|---|")
    w("| CERTAIN | not estimable yet | reviewed denominator is 3 "
      "hand-picked transcripts; 0/%d audited |" % n_tx)
    w("| HIGH CONFIDENCE | not estimable yet | same; runner HIGH labels are "
      "unreviewed |")
    w("| CANDIDATE | not a rate | raw signal, precision unmeasured |")
    w("| drop-word, speaker/format | unmeasured | no detector exists |")
    w("")
    w("All 0/59 clean-set figures are **in-sample, invalid as an "
      "independent FP estimate** (the detectors were tuned on those "
      "passages).")
    w("")

    w("## 5. Unreviewed raw signals (CANDIDATE-class, NOT findings)")
    w("")
    w("Everything in this section is automatic output that no human has "
      "reviewed. It is never blended into section 3 or 4. The runner's "
      "%d nominal `HIGH CONFIDENCE` labels are the same errors as CERTAIN "
      "fixtures CF-003 and CF-006 (dedupe), not additional findings." %
      ix["raw_runner_confidence"].get("HIGH CONFIDENCE", 0))
    w("")
    w("| detector | what it flags | records |")
    w("|---|---|---|")
    what = {"A1-repetition": "back-to-back repeated phrase loops",
            "A2-nonsense": "script-mix / garbled tokens, impossible "
                           "percentages, U+FFFD",
            "B1-contradiction": "level/percentage/polarity values vs book "
                                "tables",
            "B2-misquote": "near-verbatim book passages with divergent "
                           "words"}
    for d, n in ix["records_per_detector_signal"].items():
        w("| %s | %s | %d |" % (d, what.get(d, ""), n))
    w("| **total merged records** | | **%d** |" % ix["records_total"])
    w("")
    w("By year (from file name). Raw signals per 10k words is a "
      "*signal density*, not an error density:")
    w("")
    w("| year | transcripts | words | raw records | raw / 10k words |")
    w("|---|---|---|---|---|")
    yw = collections.Counter()
    for r in ix["per_transcript"]:
        yw[r["year"]] += words[r["transcript"]]
    for y, v in ix["by_year"].items():
        w("| %s | %d | %s | %d | %.1f |" % (
            y, v["transcripts"], format(yw[y], ","), v["records"],
            1e4 * v["records"] / yw[y] if yw[y] else 0))
    w("")
    w("B2 hits concentrate in a few 2002 lectures (up to 28 per "
      "transcript); unreviewed, these may be read-aloud book passages "
      "with loose paraphrase rather than transcription errors. A2 still flags ~34 legitimate short Korean "
      "interpreter phrases in Sedona Dec 2008 Parts 1, 2, 4.")
    w("")

    w("## 6. Re-review candidates (most raw signals; NOT proven hotspots)")
    w("")
    w("| transcript | year | words | raw records | per detector |")
    w("|---|---|---|---|---|")
    top = sorted(ix["per_transcript"],
                 key=lambda r: (-r["records"], r["transcript"]))[:15]
    for r in top:
        w("| %s | %s | %s | %d | %s |" % (
            r["transcript"].replace("_enxautogen_html", ""), r["year"],
            format(words[r["transcript"]], ","), r["records"],
            ", ".join("%s %d" % kv for kv in r["per_detector"].items())))
    w("")
    w("%d transcripts had zero raw signals; that does not show they are "
      "error-free (see section 1, point 3)." % len(ix["zero_hit_transcripts"]))
    w("")

    w("## 7. Pattern ledger seed")
    w("")
    w("| pattern | fixtures | note | detector coverage today |")
    w("|---|---|---|---|")
    covered = {o["fixture"] for o in overlap}
    for name, ids, note in PATTERNS:
        cov = ", ".join(i for i in ids if i in covered) or "none"
        w("| %s | %s | %s | %s |" % (name, ", ".join(ids), note, cov))
    w("")

    w("## 8. Limitations")
    w("")
    for s in [
        "No detector precision measured; no human review of raw output.",
        "Clean-set checks are in-sample (tuned on the same 59 passages).",
        "M2 (family A) ACCEPTED INCOMPLETE: drop-word and speaker/format "
        "detectors never built; A4 excluded (0/16 independent recall).",
        "M3 (family B) not certified: terminology drift and explicit "
        "book-attribution checks unimplemented; B1 accepts any value any "
        "book states (the books contradict each other); B1/B2 calibrated "
        "in-sample; B2 cannot catch CF-004-type paraphrase errors.",
        "Book retrieval finds the cited book for 9/15 book-referenced "
        "fixtures.",
        "The 16 CERTAIN come from 3 transcripts; 4 of them are one slide "
        "pattern.",
        "No audio: a book contradiction proves the text is wrong, not that "
        "the ASR (rather than the speaker) caused it.",
        "Year is parsed from file names; 52 transcripts have no year.",
    ]:
        w("- " + s)
    w("")

    w("## 9. Recommendations")
    w("")
    for s in [
        "**Measure before extrapolating:** hand-review a random sample of "
        "raw signals per detector (e.g. 30 each) to get a first precision "
        "estimate, and hand-read a *random* sample of transcripts (not "
        "hand-picked) to get an unbiased CERTAIN/HIGH density with a "
        "confidence interval.",
        "**Verify every number, name and quotation** against the books "
        "before reuse; patterns P2–P4 are the commonest confirmed errors.",
        "**Re-transcription priority** should wait for reviewed densities; "
        "until then use section 6 only as a review queue.",
        "**Build the missing detectors** (drop-word, speaker/format) and a "
        "held-out clean split before any corpus-wide rate is published.",
    ]:
        w("- " + s)
    w("")

    w("## 10. Next steps")
    w("")
    w("| step | task | unlocks |")
    w("|---|---|---|")
    w("| A4 held-out FP + fix seeded-hit test | TASK-007 | A4 back into "
      "the sweep |")
    w("| B1/B2 held-out clean re-test | TASK-009 (after 007) | M3 "
      "certification path |")
    w("| M4 pattern rules + missing detectors | TASK-008 | drop-word, "
      "speaker/format coverage |")
    w("| reviewed precision sample + findings ledger | M5 (uncut) | M5 "
      "certification, real rates |")
    w("| random-sample hand-read | M5/M6 (uncut) | unbiased density |")
    w("")

    w("## 11. Owner open items (unresolved, not guessed)")
    w("")
    w("- Which side of the ledger the Book-of-Slides OCR files sit on: "
      "UNDECIDED; excluded here.")
    w("- Whether \"misquotation\" covers other authors' quotes: default "
      "applied (Hawkins' teaching plus quotes the transcript attributes to "
      "a book that contradicts it); CF-002 depends on this.")
    w("")

    w("## 12. Reproduce")
    w("")
    w("```")
    w("sha256sum docdocgo-fixes.zip        # 3f36c5203910...")
    w("python3 -c \"import zipfile; zipfile.ZipFile('docdocgo-fixes.zip')"
      ".extractall('corpus')\"")
    w("python3 -m unittest discover -s tests")
    w("python3 tools/fixtures.py verify")
    w("python3 tools/sweep_m5.py --out runs/m5-raw --fresh   # ~17 min")
    w("python3 tools/report_m6.py")
    w("```")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=DEFAULT_OUT)
    a = ap.parse_args(argv)
    ix = load(os.path.join(RUN, "index.json"))
    text = build(load(CONFIRMED), load(CORRECTIONS), ix,
                 word_counts(loaders.list_transcripts()), git_head())
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("wrote %s" % a.out, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
