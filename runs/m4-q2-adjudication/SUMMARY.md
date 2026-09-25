# TASK-018 — leg (d) individual adjudication (SUMMARY)

> **Scope.** The 122 C1-drop signals from the tuning-set run `runs/m4-q2-dropword/signals.json` (sha256 `8d71f57b…`), adjudicated **individually** on cited bytes under STANDARDS CERTAIN leg (d) — owner `ERRATA-2026-09-25e.md` §2–§4, restated in the ORCH-2 standing guidance. No rule, threshold, score or detector name is a classification reason (L4); the detector supplied spans, never classes.

> **In-sample, and not a metric** (L5 / LAW §9): tuning-split signals, four of them hand-picked into provisional fixtures. No rate, precision or corpus-wide figure is stated anywhere; nothing here is precision/recall evidence.

## Counts per clause

| outcome | signals | of 122 |
|---|---|---|
| **CERTAIN-leg-d (clause (d)(i), book ground truth)** | **57** | 47% |
| clause (d)(ii), adjacent repetition | 0 | 0% |
| CANDIDATE (stays unclassified) | 65 | 53% |

Reasons among the CANDIDATE signals:

| reason code | signals | reading |
|---|---|---|
| `restoration-not-minimal` | 48 | two or more words absent — restoring them is a larger edit than one word; the narrow leg does not reach them (L3) |
| `flank-too-short` | 15 | single-word omission but too few exactly-matched tokens around it to call the span a matched quotation (clause 1) |
| `region-not-realignable` | 2 | the omission could not be re-aligned from the frozen bytes at all (clause 1) |

## The measured span that made a finding CERTAIN (per-row fields)

Each CERTAIN row cites: the verbatim transcript span (`span` + `span_start`/`span_end_matched`), the ground-truth passage (`ground_truth.slug` + `char_offset` + `quote`, re-read byte-exact), the omitted word, the restored span (= the ground-truth passage, token-equal), the flank sizes, and clause `d-i`. 4 of the 57 CERTAIN rows carry `seeded: true` (they overlap a v1 hand-confirmed fixture span) and are excluded from any metric by construction.

## Clause-1 floor: what was chosen, and how sensitive the count is

Clause 1 needs a definition of "closely tracks"; this adjudication uses **exactly-matched runs of >= 5 tokens on each side of the omission** (default), mirroring the campaign's near-verbatim floor `MIN_MATCHED=10` against *exactly matched* tokens — stricter than the detector's own ratio-based match (`MIN_FLANK=3` with ratio >= 0.85). The floor was fixed before counting, is not tuned, and the sensitivity is printed so a reader can judge it:

| floor (tokens/side) | signals that would qualify |
|---|---|
| 3 | 71 |
| 5 | 57 |
| 8 | 33 |
| 10 | 22 |

## Closest near-misses (why the narrow leg refused them)

- **D-006** @54983 `Staggering. This` — `flank-too-short`: only 23/4 exactly-matched token(s) flank the omission (< 5 required): the span does not track the ground truth closely enough to be a matched span (cl [flanks 23/4]
- **D-012** @55220 `be sovereign` — `flank-too-short`: only 3/12 exactly-matched token(s) flank the omission (< 5 required): the span does not track the ground truth closely enough to be a matched span (cl [flanks 3/12]
- **D-017** @48990 `around, has` — `flank-too-short`: only 3/10 exactly-matched token(s) flank the omission (< 5 required): the span does not track the ground truth closely enough to be a matched span (cl [flanks 3/10]
- **D-026** @21147 `earth, ruler` — `flank-too-short`: only 3/2 exactly-matched token(s) flank the omission (< 5 required): the span does not track the ground truth closely enough to be a matched span (cla [flanks 3/2]
- **D-029** @40792 `that will` — `flank-too-short`: only 10/4 exactly-matched token(s) flank the omission (< 5 required): the span does not track the ground truth closely enough to be a matched span (cl [flanks 10/4]
- **D-033** @32450 `the nature` — `flank-too-short`: only 6/4 exactly-matched token(s) flank the omission (< 5 required): the span does not track the ground truth closely enough to be a matched span (cla [flanks 6/4]
- **D-034** @49903 `cholesterol, hypoglycemia` — `flank-too-short`: only 4/7 exactly-matched token(s) flank the omission (< 5 required): the span does not track the ground truth closely enough to be a matched span (cla [flanks 4/7]
- **D-036** @9688 `to the` — `flank-too-short`: only 3/5 exactly-matched token(s) flank the omission (< 5 required): the span does not track the ground truth closely enough to be a matched span (cla [flanks 3/5]
- **D-057** @39896 `universe it` — `flank-too-short`: only 3/10 exactly-matched token(s) flank the omission (< 5 required): the span does not track the ground truth closely enough to be a matched span (cl [flanks 3/10]
- **D-068** @51758 `78% it` — `flank-too-short`: only 10/4 exactly-matched token(s) flank the omission (< 5 required): the span does not track the ground truth closely enough to be a matched span (cl [flanks 10/4]
- **D-100** @38342 `Muhammad repeatedly` — `flank-too-short`: only 3/29 exactly-matched token(s) flank the omission (< 5 required): the span does not track the ground truth closely enough to be a matched span (cl [flanks 3/29]
- **D-101** @39331 `the collective` — `flank-too-short`: only 4/73 exactly-matched token(s) flank the omission (< 5 required): the span does not track the ground truth closely enough to be a matched span (cl [flanks 4/73]

## What was NOT done
- No blanket promotion: 57 of 122 signals became CERTAIN, each by its own cited bytes; 65 stay CANDIDATE.
- No detector re-tuning, no threshold change, no new detector (TASK-018 boundaries).
- The spent holdout was not re-run; no rate and no precision figure appears anywhere.

## Provenance
Rows: `adjudication.jsonl` (122) · fixtures: `fixtures-adjudication.json` (4) · manifest: `PROVENANCE.json`. Every row is re-derivable from the frozen corpus + book store with this tool (two runs are byte-identical).
