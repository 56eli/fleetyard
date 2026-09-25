# M4-q3 — C2-format run (tuning set) — PROVISIONAL-UNGATED

Detector `C2-format` (speaker/format artifacts, mechanically checkable half),
first run over the **tuning** half of `tools/HELD-OUT-SPLIT.json`. Holdout never
opened (`holdout_reads: []` in the provenance).

## What was run

| field | value |
|---|---|
| detector | `tools/det_format.py` (self-test green; sha pinned in provenance) |
| rules | R1 glued period (abbrev-filtered) · R2 repeated punctuation · R3 4+ dot run · R4 underscore run · R5 space-before-comma · R6 spaced period · R7 glued comma |
| inputs | `corpus` (zip `3f36c5203910…`), `tools/HELD-OUT-SPLIT.json` |
| result | **193/193 tuning transcripts, 49 raw signals in 32 transcripts** |
| by rule | R1 22 · R2 3 · R3 5 · R4 1 · R5 15 · R6 2 · R7 1 |
| provenance | `PROVENANCE.json` (inputs, rules, per-rule counts, detector sha) |

All signals are **CANDIDATE-class raw format artifacts**: the artifact itself is
mechanically demonstrable; whether it changed meaning is a reading question and is
not claimed. Precision/recall: **unmeasured** (holdout run + review = q4).

## The scope census behind the "speaker/format" claim (grounded, not asserted)

Corpus-wide census over all 230 transcripts (frozen bytes):

| probe | hits | reading |
|---|---|---|
| speaker labels (`Q:` `A:` `Speaker 1` `Questioner:` `Student:`…) | **0** | the corpus format encodes no speaker turns |
| bracketed stage directions (`[laughter]`, `(inaudible)`, `[music]`…) | **0** | none present to audit |
| HTML entities / tags / JS residue / control chars / tabs / nbsp | **0** | the corpus is clean of parser residue |
| double spaces / spaces before `;` | **0** | no whitespace drift |
| camel-glue (`veryCapitalist`) | 35 hits / 18 files | **not a rule**: dominated by legitimate proper nouns (`MacArthur`, `YouTube`) — recorded, not shipped |
| double word (`that that`) | 3,436 hits / 228 files | **not an artifact**: ordinary spoken repetition (A1-repetition's domain) |

Consequence, stated plainly: **speaker attribution is out of mechanical scope in
this corpus** — there are no speaker turns to check, and deciding that a passage is
wrongly attributed to the speaker rather than a questioner is a human reading
judgment. The M2 remainder "speaker/format" is therefore resolved as:
*format artifacts → measurable and measured here; speaker attribution → unmeasured,
recorded as an explicit M6 limitation*. That limitation is a finding about the
instrument, not a silence.

## Sample signals (verbatim, for the reader to judge)

- `R1` `people.You` (missing space after a sentence period — grammar/sense intact)
- `R2` `soul****` (censor-style asterisk run) · `, ,` doubled comma
- `R3` `.....` (5-dot run, adjacent to mixed-script garbage)
- `R5` `you , propensity` · `thank you , thank you again` (spurious space before comma)
- `R6` `Laugh . bacteria` (spaced sentence period mid-stream)
- `R7` `cure,lly` (missing space after comma)

## Limits

No audio; no human review of the 49 signals; no ORCH-2 gate (PROVISIONAL-UNGATED).
Rules are deliberately conservative — the census entries that were *rejected* as
rules (camel-glue, double word) are recorded above so the rejection is auditable.
