# DETECTORS — family A (TASK-004 / M2) and family B (TASK-005 / M3)

Stdlib only, no network, read-only over `corpus/**`. Each detector is a
standalone module with `detect(text, **ctx) -> [signal]` and `--self-test`.
`tools/run_detectors.py` merges overlapping signals into STANDARDS finding
records (>= 2 distinct detectors = HIGH CONFIDENCE, else CANDIDATE; CERTAIN
is never assigned automatically; status always `open`).

| id | module | catches |
|---|---|---|
| A1-repetition | `tools/det_repetition.py` | ASR repetition loops (k-token unit repeated back-to-back; k=1 >= 8x, k=2-3 >= 5x, k>=4 >= 3x) |
| A2-nonsense | `tools/det_nonsense.py` | impossible percentages (> 100), script-mix garble (mixed-script tokens, Vietnamese-only letters, short non-Latin runs in English), U+FFFD |
| A4-confusion | `tools/det_confusion.py` | hand-built confusion list (provenance per entry) + difflib near-forms of Hawkins-book proper names |
| B1-contradiction | `tools/det_contradiction.py` | claims that contradict book tables: happiness % per level (Reality, Spirituality and Modern Man table), "<Level> [calibrates at] N" logs not given anywhere in the Hawkins books, polarity inversions of the 200 line ("above which ... negative") |
| B2-misquote | `tools/det_misquote.py` | near-verbatim quotes of a Hawkins book with a near-form word substitution or one spurious extra word (TF-IDF retrieval via `tools/retrieval.py` + word-level difflib alignment) |

Family B signals carry `book_ref` = {slug, char_offset, quote} (verbatim book
text), which `run_detectors.py` copies into the record's `book_reference`.
`--family A|B|AB` (default AB) selects detectors; the book index and B1's
reference tables are built once per run. Runtime: family A ~seconds for the
whole corpus; B2 ~2-4 s per transcript (~10-15 min for `--all`).

## Fixture + clean-set results (verbatim output of `python3 tools/run_detectors.py --eval`)

| detector | fixture hits (independent) | fixture hits (seeded from that fixture) | clean-set false positives |
|---|---|---|---|
| A1-repetition | 2/18 CF-005,CF-006 | 0  | 0/59 passages |
| A2-nonsense | 1/18 CF-003 | 0  | 0/59 passages |
| A4-confusion | 0/18  | 8 CF-001,CF-002,CF-004,CF-010,CF-011,CF-012,CF-013,CF-017 | 0/59 passages |
| B1-contradiction | 2/18 CF-003,CF-006 | 0  | 0/59 passages |
| B2-misquote | 1/18 CF-015 | 0  | 0/59 passages |

"Fixture hits" = a signal overlaps the fixture's quoted span (recall on the
18 CERTAIN fixtures). **Precision is not measured yet**: that needs a finding
pass over flagged spans (no reviewed sample exists). Clean-set FPs use a
held-out lexicon (the passage's own book removed from A4's lexicon); B2's
clean-set check likewise excludes the passage's own book from retrieval
(`exclude_slugs`). B1 was additionally run over the whole Hawkins book store
as a clean set: 0 signals (test-enforced).

## Disclosures
1. A4's 8 fixture hits all come from list entries SEEDED from those same
   fixtures (provenance `seed:CF-xxx`), so they are not independent recall
   evidence; A4's independent fixture recall is 0/18. Its generic paths
   (`general` list entries, difflib lexicon) are untested against fixtures.
2. A4's difflib cutoff was raised 0.80 -> 0.82 after the first held-out eval
   gave 2 clean-set FPs (`Lenny`->`Lenin`, `Llamas`->`Lama`, both ratio
   0.80). The cutoff is therefore calibrated on the clean set.
3. Not delivered in this task (TASK-004 asks >= 3 modules): drop-word and
   speaker/format detectors. Neither could meet criterion 4 (catch >= 1
   fixture) with the current fixture set, so none shipped.
4. Long non-Latin runs (the inline Korean interpretation in
   `A_Unique_Sedona_Seminar_Dec_2008_*`) are deliberately NOT flagged by A2.
5. Informational dry run over all 230 transcripts (not committed, not a
   findings ledger; M5 owns the sweep): 1264 records in 210 transcripts —
   A1 937, A2 171, A4 155, A1+A2 1 (the only HIGH). All unreviewed.

### Family B (TASK-005)
6. B1 reference values are parsed from the books at run time, never typed
   in. The books themselves are not consistent (e.g. Enlightenment at 600
   and 700, Acceptance 350 and 380, Pride 175 and 190, Joy 540 and 570), so
   B1 accepts ANY value a Hawkins book states in prose ("<Level> calibrates
   at N" / "<Level> at N") or in the Map / happiness tables. A single
   canonical table would flag the books against themselves.
7. B1 calibration history (all on the clean set + book store, so partly
   fitted): first draft gave 147 transcript hits, mostly index/page-number
   and loose-window FPs; tightened to level-within-60-chars + "happ" within
   40 chars for percentages, no comma form for logs, same-line whitespace
   only (book table layout "ENLIGHTENMENT\n\n365" was a FP), and no match
   after "of"/"for" ("Teacher of Enlightenment 800"). Corpus-wide B1: 12
   signals (level-log 6, happiness 5, polarity 1). Plausible: CF-003
   (255%), CF-006 (polarity), "joy at 400", "neutrality at 200". Known weak /
   likely FP: "unlimited love at 540" and "five hundred is love 540 is
   unconditional" (Love vs Unconditional Love parse), "money trumps peace
   calibrates at 375" (not about the level Peace), two Witnessing_and_
   Observing hits that quote a different (city/society) table with its own
   happiness column, and "90%" for level 500 (book 89%, likely rounding).
   Unreviewed.
8. B2 calibration history: the first (loose) version flagged ~50 signals in
   one transcript — lecture slides paraphrase the books, so most diffs were
   editorial, not errors. Shipped rules: region >= 10 matched words at
   ratio >= 0.85; op <= 2 words flanked by >= 3 matched words on each side;
   substitutions only when char-similar (difflib >= 0.5) and not a
   hyphenation/inflection/spelling/diacritic variant (>= 0.9 or shared
   stem); deletions = one extra content word inside an UNPUNCTUATED book
   phrase; book-side omissions (speaker skipped words) are ignored; numbers
   and contractions ignored. Each filter was added after seeing clean-set or
   fixture-transcript output, so the rules are fitted to what we have.
9. B2 recall is narrow: 1/18 (CF-015). CF-004 ("unquestionable love") is a
   near-form substitution B2 is designed for, but the transcript sentence is
   surrounded by a repetition loop and chat, so no window retrieves the book
   passage. Explicit attribution ("as it says in <book>") is not parsed.
   Retrieval picks the best-aligned of the top 3 passages; reprinted
   passages may cite a different book than the fixture (CF-015 cites
   the_map_of_consciousness_expla; fixture cites discovery_of_the_presence_of_g,
   same sentence).
10. B2 sample (informational, every 10th transcript = 23 files, 88 s): 29
    signals, concentrated in audiobook-style readings (Radical_Subjectivity,
    The_Levels_of_Consciousness). Plausible ASR errors among them:
    imminent->immanent, ascent->assent, community->committee, Wang->Huang,
    Farms->Firearms, litter->later, "an integrist"->integrous; also noise
    such as till->until, "Who says"->"We say". Unreviewed; precision
    unmeasured.
11. Contradiction/misquote are the only B modules; no numeric-claim or
    date detector shipped.
