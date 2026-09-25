# M4-q2 — C1-drop run (tuning set) — PROVISIONAL-UNGATED

Detector `C1-drop` (dropped words against a book source), first run over the
**tuning** half of `tools/HELD-OUT-SPLIT.json`. The holdout half was never opened
(`holdout_reads: []` in every part provenance; the split's shards assert it).

## What was run

| field | value |
|---|---|
| detector | `tools/det_dropword.py` (self-test green; sha pinned per part) |
| params | window 24 / stride 12; tf-idf ≥ 0.20; top-3 passages; ≥ 10 matched words, ratio ≥ 0.85; drop ≤ 2 tokens; flank ≥ 3 matched words/side; content-word required; numerals, book-dialogue and editorial marks filtered |
| inputs | `corpus` (zip `3f36c5203910…`), `tools/HELD-OUT-SPLIT.json` (salt `fleetyard-m4-holdout-2026-09-25`) |
| shards | 6 bounded runs (73–112 s each, LAW §4A quanta), each with its own provenance |
| result | **193/193 tuning transcripts processed, 122 raw signals** |
| outputs | `part-<i>.json` + `part-<i>.PROVENANCE.json` (6), `signals.json`, `MERGE-PROVENANCE.json` |

`signals.json` sha256 `8d71f57bcb80313fcf8a635587525e65ff7e4603fd431494c1c45c6d1eea83b4`.

## Status of the 122 signals

**CANDIDATE-class raw signals, unreviewed.** This is not a rate and not a
finding set: precision is **unmeasured** (that requires the q4 holdout run with
frozen thresholds — not yet done). Dominant false-positive shapes seen while
hand-sampling the tuning output (recorded, not hidden):

- speaker improvisation around a read-aloud passage (drop of fillers such as
  `I mean`, `you know`, `see`, `however` — arguably speech, not transcription);
- abbreviation/expansion differences (book `Osama bin` vs transcript `Bin`);
- book table/heading text (`Earth  Infinity  Ruler`) picked up by retrieval.

## Review of the top candidates (hand-read, tuning set)

4 of the sampled candidates were hand-verified as real transcript omissions and
kept as provisional fixtures in `fixtures/v2/dropword.json` (D2-001…D2-004), each
with transcript span + book citation re-verified byte-exact (see
`tests/test_det_dropword.py`). Five further sampled candidates were **discarded or
parked**: `Illness_and_SelfHealing @32450` (`inherent` — doctrinal nuance kept as a
near-miss), `@5013` (`or resistant` — meaning preserved), `Causality…Part_1 @48990`
(`probably` — hedge loss, kept as a near-miss), `Experiential…Mystic @40792`
(`study` — transcript remains grammatical, paraphrase), `Intention…Part_3 @9688`
(`identify` — different construction, paraphrase).

**Classification is blocked, deliberately:** STANDARDS defines no leg for
omissions. `fixtures/v2/dropword.json` carries a **proposed leg (d)** wording; per
the STANDARDS preamble a taxonomy change needs a recorded errata **and** a BOSS
CONCERN, neither of which exists (BOSS-2 not booted). Until then the four fixtures
are labelled *DROP-CANDIDATE (hand-verified omission) — CLASS BLOCKED*, never
CERTAIN.

## Honest limits

- Only book-anchored drops are detectable by this rule; drops in ordinary
  conversation remain **unmeasured** — the class is narrowed, not closed.
- Tuning-set fixtures are detector-derived and therefore **in-sample**; recall
  computed against them is not admissible evidence (LAW §9).
- No audio was heard; no independent review; no ORCH-2 gate exists
  (PROVISIONAL-UNGATED).
