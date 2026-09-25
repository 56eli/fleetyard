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
- **cross-book self-parallel** (added TASK-020 item 5c): the "transcript" *was* book
  text, so the rule matched a near-verbatim passage in a **different** Hawkins book and
  reported that book's wording as a drop. Measured on the clean set: CL-034
  (`the_ego_is_not_the_real_you__w` → `daily_reflections_from_dr_dav` @80391, `remains`),
  CL-035 (→ `discovery_of_the_presence_of_g` @295761, `by ownership`), CL-055
  (`transcending_the_levels_of_con` → `the_map_of_consciousness_expla` @134304,
  `so-called`) — 3/59 misfires, all cleared by the source-inheritance filter.
- **book-side repetition** (added TASK-020 item 5c): the cited book span repeats the
  token the rule calls missing (`evidence; evidence of`, `staggering, staggering. This`,
  `be sovereign, sovereign`) — the omission claim is not sound for that token. 3 signals,
  excluded from every count.

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

## Threshold provenance (TASK-020 item 6, append-only)

Every C1-drop parameter, with what it was fitted on and measured on:

| parameter | value | provenance |
|---|---|---|
| `window` | 24 tokens | chosen by inspection while building the rule on the **v1 tuning half (193 transcripts)** in M4-q2; not fitted by any optimiser |
| `stride` | 12 tokens | same — half the window, so consecutive windows overlap and a drop cannot fall between them |
| `min_score` | 0.20 | same — a retrieval floor set low on purpose: the alignment filters, not the TF-IDF score, do the deciding |
| `top_k` | 3 | same — three candidate book passages per window, best-by-matched-words wins |
| `min_matched` | 10 | same — a drop is only reported inside a ≥10-word match |
| `min_ratio` | 0.85 | same — ≥85% of the matched region must be equal tokens |
| `max_drop` | 2 | same — at most two book words may be missing per operation |
| `min_flank` | 3 | same — ≥3 matched words on each side of the drop |

**What that costs, stated plainly.** No threshold was fitted on held-out data; none was
tuned against the v1 holdout (never opened) or against the clean set (which had never been
run before this repair). The consequence is that the operating point is *unchosen*: the
thresholds are conservative by construction (few, high-support signals), but their
**sensitivity is unmeasured** — nobody has measured how many signals appear or vanish at
`min_ratio` 0.80, `min_flank` 2, `min_matched` 8, and so on. That measurement cannot be
made inside split v2 discipline: 33 of the 193 v1-tuning transcripts are members of the
**v2 holdout**, so recomputing the shipped run at other thresholds would open the sealed
holdout. It is therefore deferred to split v3 or to an ORCH-2 gate-side scratch, and
recorded here as a limitation rather than papered over.

What *was* measured against the shipped thresholds: the fixture recall (0/16, in-sample)
and the clean-set misfire count (3/59 → 0/59 after the source-inheritance filter) — see
`EVAL.json`.

## Shipping-evidence rebuild (TASK-020 items 1/2/4/5a/5c, append-only)

The q2 gate (`91cf112`, 20:58Z) failed q2 on five criteria and restricted C1-drop. The
missing evidence now exists, produced by `tools/m4_q2_evidence.py` +
`tools/m4_t20_supplement.py`:

| artefact | content |
|---|---|
| `EVAL.json` | fixture recall **0/16** (per-fixture table + a precondition diagnosis for every miss, including CF-015), clean-set run **3/59** misfires with per-hit citations, the source-inheritance filter (raw **122** → filtered **114**, 7 deferred), and the per-signal shape adjudication |
| `EVIDENCE-PROVENANCE.json` | §8 manifest for the TASK-020-era measurements |
| `PROVENANCE-SUPPLEMENT.json` | §8 completion for the **original** run: part digests (part-1 `64a97be5…`, part-3 `092d6341…` — the two ORCH-2 reproduced), merge digest, book-store digest `c0892fcd…`, config digest over the 8 params, tool commit / main head / policy sha, and the detector re-pin with the `84e5407f…` defect stated |

Results, as measured:

* **CF-015 (the named target) is NOT caught**: the best near-verbatim window scores 0.2049
  on `the_map_of_consciousness_expla` @386600, matched 10, ratio 0.9091 — both
  preconditions pass — but the alignment carries **no insertion op** (replace×2, delete×1,
  equal×2). The difference is a *substitution*, and C1-drop reports only book words
  **missing** from the transcript inside a matched span.
* **Clean set 3/59 → 0/59 after the filter.** All three misfires are cross-book
  self-parallels (the "transcript" *was* book text): CL-034 → `daily_reflections_from_dr_dav`
  @80391 (`remains`), CL-035 → `discovery_of_the_presence_of_g` @295761 (`by ownership`),
  CL-055 → `the_map_of_consciousness_expla` @134304 (`so-called`). Each hit's own wording is
  verbatim in the store, which is exactly what the filter detects.
* **Shape adjudication reconciles to the gate's 113**: raw 122 − 3 `dropped-token-not-missing`
  (the gate's own three: `evidence` @2574, `staggering` @54983, `sovereign` @55220) −
  5 `partial-overlap` − 1 gate-listed hyphen case (`one-third`, deferred to a human read) =
  **113 countable**. This instrument finds 114 deletion-closing signals; the difference is
  the gate's own tokenizer artifact and is disclosed rather than absorbed.
* **Source-inheritance filter on the shipped run: 1/122** (reproducing the gate-side figure);
  7 signals sit in v2-holdout transcripts and are **deferred** — filtering them would open
  the sealed holdout.

**122 must never be quoted as an omission count**; the defensible upper bound is 113,
in-sample and unreviewed.
