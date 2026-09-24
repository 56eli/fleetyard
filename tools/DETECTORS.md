# DETECTORS — family A (language integrity), TASK-004 / M2

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

## Fixture + clean-set results (verbatim output of `python3 tools/run_detectors.py --eval`)

| detector | fixture hits (independent) | fixture hits (seeded from that fixture) | clean-set false positives |
|---|---|---|---|
| A1-repetition | 2/18 CF-005,CF-006 | 0  | 0/59 passages |
| A2-nonsense | 1/18 CF-003 | 0  | 0/59 passages |
| A4-confusion | 0/18  | 8 CF-001,CF-002,CF-004,CF-010,CF-011,CF-012,CF-013,CF-017 | 0/59 passages |

"Fixture hits" = a signal overlaps the fixture's quoted span (recall on the
18 CERTAIN fixtures). **Precision is not measured yet**: that needs a finding
pass over flagged spans (no reviewed sample exists). Clean-set FPs use a
held-out lexicon (the passage's own book removed from A4's lexicon).

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
