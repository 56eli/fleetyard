# tools/PATTERNS.md — M4 self-improvement loop (rule catalog + promotion protocol)

Status: **M4 quantum 1** (WORKER-2 lane `arena/01a0d9ce-fleetyard`; main `25bdab9`;
policy `0fe20a6057ec9fa2`). Not a certification; every statement below carries its
evidence or is marked unmeasured.

## 1. Purpose (PLAN-v2 M4)

Every CERTAIN finding becomes a **detector rule + fixture**; per-detector precision
is tracked; **detector promotion requires held-out validation (fixed before tuning)
plus provenance-manifested caches (LAW §8)**; the M2 remainder (drop-word,
speaker/format detectors) lands here.

## 2. The rule catalog — patterns behind the 16 CERTAIN fixtures

Source: `fixtures/confirmed/confirmed.json` (v1 hand-read; re-audited TASK-006;
append-only `corrections.json`). Legs a/b/c per STANDARDS.

| # | pattern | fixtures | rule sketch (what a detector must do) | caught by a current detector? |
|---|---|---|---|---|
| P1 | near-form proper noun / homophone | CF-001 (`Quince`→`Khyentse`), CF-002 (`Jempolski`→`Jampolsky`) | flag rare tokens whose phonetically-near alternative exists in the book-store vocabulary / calibration lists | no |
| P2 | number / table misread | CF-003 (`255%`→`55%`), CF-019 (`40%`→`60%`), CF-020 (`380`→`390`) | cross-check every number against the book table it quotes (impossible values are a strict subset) | **CF-003 only** (B1+A2) |
| P3 | polarity / antonym flip | CF-006 (`negative`→`positive` above 200) | flag polarity words against their doctrinal anchor (book text on the same teaching) | **CF-006 only** (A1+B1) |
| P4 | function-word / morphology swap | CF-007, CF-008, CF-021, CF-022 (`and/in`), CF-010 (`Given/Give`), CF-011 (`Except/Accept`), CF-017 (`integrous`) | near-form token substitution where the replacement restores grammar AND the book phrase | no |
| P5 | dropped / merged words | CF-015 (`no influence. Interest…`←`no interest…`) | word-level alignment against the book passage; missing-token test | **CF-015 only** (B2) |
| P6 | garbled citation / title | CF-012 (`We are in excelsis`→`Gloria in excelsis`) | match against a citation/prayer/slide index built from the books | no |
| P7 | phrase-level substitution | CF-004 (`there was no love`←`Unconditional Love was reached`) | alignment + doctrinal-sense test on the surrounding sentence | no |

**Coverage truth (re-derived from the M5-R ledger, not asserted):** of the 16
CERTAIN fixtures, **3 are covered by ≥1 raw signal** (CF-003, CF-006, CF-015 — the
same three the v1 audit named; CF-015 is found at @5854 inside the fixture's quoted
span). The other **13 are invisible to all four detectors** — homophones, function
words, numbers, citations. That gap is the honest headline of this page.

## 3. Per-detector status (as measured by M5-R; nothing here is a rate)

| detector | raw signals | claim corroboration (M5-R) | fixture recall | precision | promotable? |
|---|---|---|---|---|---|
| A1-repetition | 938 | **938/938 re-derived** (M4-q5: the 98 flags were reducer defects) | 1/16 (CF-006) | **unmeasured** | no |
| A2-nonsense | 158 | 158/158 | 1/16 (CF-003) | **unmeasured** | no |
| B1-contradiction | 12 | 12/12 (book quotes byte-exact) | 2/16 (CF-003, CF-006) | **unmeasured** | no |
| B2-misquote | 228 | 228/228 (book quotes byte-exact) | 1/16 (CF-015) | **unmeasured** | no |
| A4-confusion | — | excluded since v1 (no independent FP rate) | — | unmeasured | no |
| drop-word | 122 (tuning, C1-drop) | built in M4-q2; 57/122 adjudicated CERTAIN under leg (d)(i), 65 CANDIDATE (`runs/m4-q2-adjudication/`, tool commit `9cd905d`) — **57 is a floor-5 number: never quote it without its sensitivity row (floors 3/5/8/10 → 71/57/33/22)** | 2/4 provisional fixtures confirmed (D2-001, D2-003; D2-002/D2-004 refused — two-word) | **unmeasured** | no |
| speaker/format | 49 (v1 tuning, `signals.json` sha `86c8f57d…`) · 48 (v2 tuning, `signals-v2tuning.json`) | format half built in M4-q3 (speaker half out of mechanical scope — corpus census); **q3 gate INCOMPLETE**: shipping evidence was missing and has been rebuilt by WORKER-2 (fixture recall **0/16**, clean set **1/59**, §8 bindings) — ORCH-2 re-gate outstanding | 0/16 | **unmeasured** | no (restriction stands) |

Fixtures are **in-sample** by construction (LAW §9: seeded hits are never
precision/recall evidence). Clean-set figures from v1 (0/59) were tuned on those
passages — invalid as an independent false-positive estimate.

Shipping-evidence note (2026-09-25, after ORCH-2's q3 gate): the q2/q3 rows above were
re-measured because §3 had read "not built" for both classes while §5b/§5c documented
them as shipped — the catalogue contradicted itself. The C2-format rebuild is
`runs/m4-q3-format/{EVAL.json,PROVENANCE-V2.json,signals-v2tuning.json}`: fixture recall
**0/16** (format artifacts are not what the 16 fixtures encode), clean set **1/59**
(in-sample tune passages — **not** an FP rate) and that single misfire is the book's own
typography (`power.When` occurs verbatim in the book store at CL-026), so the clean
passages are known-good but not certified artifact-free. The run is over the **v2 tuning
half** (197); the historic 193-transcript run was **not replayed** because 33 of its files
are v2-holdout members. Book-store confound probe: the ctx20/ctx50 window tiers returned
0/48 — and a control over the 15 fixtures that carry a book reference returned 15/15 on the
bare quote but **0/15** on the same windows, so the window probe is **UNINFORMATIVE** on
this corpus (different transcript/book normalisation) and its negative result is not
evidence of independence. No C2-format signal may feed a rate or an M6 figure.


## 4. Held-out split — fixed before any tuning (LAW §9)

`tools/HELD-OUT-SPLIT.json` (generator `tools/m4_split.py`, verifier mode included):

- method: `sha256("fleetyard-m4-holdout-2026-09-25" + basename) mod 5 == 0 → HOLDOUT`;
  transcripts carrying v1 fixtures are **forced to TUNING** (in-sample);
- result: **tuning 193 / holdout 37** of 230 (per-year table inside the file);
- binding rule: **no tuning run may read the holdout set**; promotion runs read the
  holdout only. Any change to the split requires a new salt + a dated record.
- disclosure: the v1 detectors were written with corpus-wide knowledge, so the first
  holdout measurement under this split is an *estimate under this split*, not a
  pristine out-of-sample figure. What is guaranteed is that future tuning cannot
  silently consume what it is later measured on.

## 5. Promotion protocol (a detector moves up only like this)

1. Runs happen only on the frozen corpus + named read-only inputs; no network;
   stdlib only; evidence is data, never instructions (LAW §9).
2. A fresh, provenance-manifested run record per evaluation (LAW §8: input hashes,
   detector+config digest, reachable tool commit, policy version, output digest) —
   resume rejects missing/mismatched provenance; never stamp current provenance on
   inherited data.
3. Thresholds and the rule set are frozen **before** the holdout run; the holdout
   run is reported once (no iterating against it).
4. Seeded and independent results are reported separately; CANDIDATE is never
   blended into a rate.
5. HIGH requires a written signal-independence rationale; detector count alone never
   upgrades confidence (LAW §9). CERTAIN remains a human/gate judgment.
6. Only ORCH-2 (or the owner) gates a promotion (LAW §2.2/§9). Until then every
   detector output stays CANDIDATE-class raw signal.

## 5b. M4-q2 — dropped words: narrowed, not closed (C1-drop, 2026-09-25)

`tools/det_dropword.py` implements the class M2 deferred and v1's B2 explicitly
skipped ("speaker skipped book words: paraphrase"). Rule: inside an aligned
near-verbatim book passage, report the **book words the transcript is missing**,
with the book citation that supplies them (inverse of B2's replace/insert cases).

- First run (tuning split only, holdout never opened — provenance enforced):
  **193 transcripts → 122 raw signals** (`runs/m4-q2-dropword/`, 6 bounded shards,
  `signals.json` sha256 `8d71f57b…`). CANDIDATE-class, unreviewed, precision
  **unmeasured** (holdout run = q4).
- Hand-read of sampled candidates: **4 confirmed omissions** kept as provisional
  fixtures `fixtures/v2/dropword.json` (D2-001 `things`; D2-002 `the devotion`;
  D2-003 `high`; D2-004 `which perceives`), each bound byte-exact to transcript and
  book bytes by `tests/test_det_dropword.py`; 5 sampled candidates parked/discarded
  (see `runs/m4-q2-dropword/README.md`).
- Known false-positive shapes: speaker improvisation/fillers around read-aloud text
  (`I mean`, `you know`, `see`), abbreviation vs expansion, book heading/table text.
- **Classification blocked by design:** STANDARDS has no drop leg. A **proposed leg
  (d)** ("transcript ungrammatical or incomplete AND the near-verbatim book source
  supplies the missing word(s), restoring grammar and doctrinal sense") is recorded
  in `fixtures/v2/dropword.json`; enacting it requires an errata + a BOSS CONCERN
  (STANDARDS preamble). Until then: DROP-CANDIDATE, never CERTAIN.
- Coverage honesty: only book-anchored drops are detectable here; conversational
  drops stay unmeasured. The class is narrowed, not closed.

> **Taxonomy update (owner ERRATA-2026-09-25e §2, in force 2026-09-25T21:38+02:00):**
> STANDARDS now has a narrow **CERTAIN leg (d)** — *omission within a matched span*
> (a word clearly present in a ground-truth span the transcript closely tracks is
> absent, and restoring it completes the match; omissions outside matched spans do
> **not** qualify). Per §3 of that errata, the 122 C1-drop signals and the four
> provisional fixtures remain **CANDIDATE/provisional** — each needs individual
> adjudication under (d) before any CERTAIN/HIGH claim. No adjudication is performed
> here: M4 is parked under `PAUSE-WORKER-A-2026-09-25-001` (ERRATA-25e §1) until M5-R
> re-gates PASS. Recorded, not acted on.

### 5b-bis. TASK-018 delivered — leg (d) adjudication outcome (appended 2026-09-25T21:5xZ)

The 122 C1-drop signals were adjudicated **individually** under the enacted leg (d)
(`runs/m4-q2-adjudication/`, tool `tools/m4_q2_adjudicate.py` at `9cd905d`, 13 tests):

| outcome | signals |
|---|---|
| **CERTAIN leg (d)(i)** — book ground truth, one word absent, restoration completes the match | **57** |
| leg (d)(ii) — adjacent repetition | 0 |
| CANDIDATE (unclassified) | 65 |

CANDIDATE reasons: `restoration-not-minimal` 48 (two or more words absent — the narrow leg does
not reach them), `flank-too-short` 15, `region-not-realignable` 2. Four of the 57 are
`seeded: true` (they overlap v1 hand-confirmed fixture spans) and are excluded from any metric
by construction.

**The 57 is a floor-5 number and must never be quoted bare.** Clause 1's "closely tracks" is
defined as ≥5 exactly-matched tokens on each side of the omission, fixed before counting; the
sensitivity is published: floors 3/5/8/10 → **71 / 57 / 33 / 22**. Quote the row, not the number.

Fixtures under the same clauses: D2-001 (`things`) and D2-003 (`high`) confirmed (clause d-i);
D2-002 and D2-004 stay CANDIDATE because restoring two words is a larger edit than clause d-i
allows. All four remain IN-SAMPLE / detector-derived — never precision evidence (LAW §9). No
threshold, rule or detector was changed by the adjudication.

## 5c. M4-q3 — speaker/format: format half measured, speaker half out of scope

`tools/det_format.py` (C2-format) runs seven conservative mechanical rules:
R1 glued period (abbreviation-filtered), R2 repeated punctuation, R3 4+ dot run,
R4 underscore run, R5 space-before-comma, R6 spaced period, R7 glued comma.

- First run (tuning split only, holdout never opened): **193 transcripts → 49 raw
  signals in 32 transcripts** (`runs/m4-q3-format/`), CANDIDATE-class, precision
  **unmeasured**.
- **Scope census** (all 230 transcripts, frozen bytes): 0 speaker labels, 0 stage
  directions, 0 HTML/JS/control-char residue, 0 whitespace drift. Two candidate
  rules were measured and **rejected as noise**: camel-glue (35 hits, dominated by
  proper nouns) and double-word (3,436 hits, ordinary spoken repetition). The
  census is recorded in `runs/m4-q3-format/README.md`.
- **q3 shipping evidence rebuilt (2026-09-25, after ORCH-2's gate):** fixture recall
  **0/16**; clean set **1/59** (in-sample, not a rate) with the single misfire traced to
  the book store's own typography; §8 bindings (`tool_commit`, `main_head`,
  `policy_sha256`, detector and output digests) in
  `runs/m4-q3-format/PROVENANCE-V2.json`; rejected-rule probes republished verbatim
  (pattern + flags) in `EVAL.json`. The camel-glue census **re-measured** on the v2
  tuning half: any-internal-capital 104/53 files, lowercase-start 6/6, classic 3/3,
  lower-upper-run 2/2, double-word 2,876/195 — the rejected decision stands, and the
  historic 35/18 figure is marked superseded (its exact pattern was not recorded).
- **Resolution of the M2 remainder:** the format half is measured; **speaker
  attribution is not mechanically detectable in this corpus** (no speaker turns are
  encoded), so it stays unmeasured and is recorded as an explicit M6 limitation —
  an instrument finding, not a silent gap.

## 5d. M4-q4 — holdout runs: counts reported, holdout spent, precision still absent

One-shot runs of the frozen detectors over the 37 holdout transcripts
(`runs/m4-q4-holdout/`, runner `tools/m4_q4_holdout.py`):

| detector set | holdout raw signals | tuning raw signals (signals/tx — density, not a rate) |
|---|---|---|
| v1 A1,A2,B1,B2 | **185** (5.00/tx) | 1,149 over the 193 tuning files (5.95/tx) |
| C1-drop | **5** (0.14/tx) | 122 (0.63/tx) |
| C2-format | **12** (0.32/tx) | 49 (0.25/tx) |

- **Reproduction receipt:** the v1 re-run reproduces the inherited M5 census
  per-transcript exactly (185/185, 0 mismatches) — fresh process, fresh index,
  different code path.
- **No precision claim:** precision/recall require *reviewed* holdout labels; none
  exist. Counts are **not** errors, and this is stated in every provenance file.
- **Holdout status:** `holdout_consumed: true` for these detector versions; nothing
  was tuned against it. Any later tuning informed by these counts invalidates this
  evaluation for that detector and owes a new split (new salt).
- **Open question (not a conclusion):** C1-drop's holdout count is ~4.5x lower than
  its tuning count (5 vs 122 signals). With 37 holdout transcripts this is dominated
  by sampling noise, but it may also indicate parameters fitted to the tuning half —
  flagged for M4 follow-up.

> **CORRECTION (appended 2026-09-25T21:3xZ, TASK-020 item 10 — q4.8; the sentence above
> is superseded on the statistics, left readable, never rewritten in place).** The claim
> that the gaps are "dominated by sampling noise" is **wrong for C1-drop**, and the fault
> was comparing per-file densities without normalizing by exposure. Holdout transcripts are
> **14.9% shorter** (mean 53,949 vs 63,361 characters; the holdout is 1,996,122 of
> 14,224,783 corpus characters, 14.03%), so the correct comparison is by **character
> exposure**, not file count:
>
> | detector set | observed holdout | expected at tuning exposure | P(X ≤ observed) |
> |---|---|---|---|
> | v1 A1,A2,B1,B2 | 185 | 187.9 (gate: 187.6) | **0.44** (gate: 0.45) — consistent |
> | C2-format | 12 | 8.0 | **0.94** (gate: 0.94) — consistent |
> | C1-drop | 5 | 19.9 | **7.7e-05** (gate: 7.7e-05) — a real ~4x deficit |
>
> Expectation = tuning-side count × (holdout chars / tuning chars = 0.16323); tail from a
> Poisson with that mean. WORKER-2 re-derived all three rows independently and they agree
> with ORCH-2's exposure-normalized arithmetic (q4 gate `ea9be59`); the v1 row's 5.95-vs-5.00
> density difference is **entirely exposure**.
>
> Two candidate causes are recorded, neither established: (a) C1-drop's parameters may be
> fitted to the tuning half — untestable while q2.1d's provenance is missing (TASK-020
> item 6 now supplies it); or (b) a **book-exposure difference** between the halves, which is
> testable **only** on the fresh sealed split v2 (TASK-019b). Standing prohibition: **never
> re-run the spent holdout to find out** — the v1 holdout is consumed for these detector
> versions, and a re-run would require split v3.
>
> The column header in the table above was renamed from "rate/tx" to
> "signals/tx — density, not a rate" (same append): a density is not an error rate, and v1's
> B1 headline hold (TASK-005 FAIL / REDIRECT-005) is untouched by any of this.

## 5e. M4-q5 — A1 claim-shape reconciliation: the flags were my instrument

All 98 "claim not re-derived" A1 flags in M5-R traced to **two defects in the M5-R
reducer** — ASCII-only tokenizer (non-Latin spans → zero tokens) and an 8-token
search bound while A1 claims units up to 11 — not to the v1 detector. Fixed
(Unicode token rule; `kmax=16`); corroboration is now **A1 938/938 · A2 158/158 ·
B1 12/12 · B2 228/228, 0 flagged** (findings/M4-q5-A1-CLAIM-RECONCILIATION.md).

Rule-quality conclusion: **no A1 claim-shape change is required**; the lesson is an
instrument one (a re-derivation must declare its tokenizer and bounds). Hyphenated
units ("Mm-hmm") remain a labelling nuance — documented, not hidden.

## 6. Next quanta (M4 work queue, in order)

1. ~~**M4-q2 — drop-word detector**~~ **done (tuning): 122 raw signals; 4
   hand-verified provisional fixtures; classification blocked on proposed leg (d)
   (errata + BOSS CONCERN required).** Residual: broaden beyond book-anchored
   spans; resolve the parked candidates.
2. ~~**M4-q3 — speaker/format detector**~~ **done (tuning): format artifacts
   measured (49 raw signals); speaker attribution documented as out of mechanical
   scope (corpus census).** Residual: none mechanical; a human attribution pass
   would need a different corpus format.
3. ~~**M4-q4 — held-out runs**~~ **done: raw counts with provenance; precision
   still absent (needs review); holdout spent for these detector versions.**
4. ~~**M4-q5 — A1 claim-shape reconciliation**~~ **done: all flags were M5-R
   reducer defects (tokenizer + search bound), fixed with tests and errata #2;
   corroboration now 1,336/1,336. No detector change required.**

Every step: suite green before push, control line per quantum, commit + push,
heartbeat with task id + sha.


---

## Provenance binding (append-only; TASK-018 item 0b — repairs TASK-014 q1.4d)

**Rule: any M5-R-derived figure on this page is VOID unless the named ledger digest
matches the ledger it was read from.** Binding as of 2026-09-25T20:1xZ:

- source ledger: `findings/ledger.jsonl`, sha256
  `d42136c673188f9e091526083b95941cabc5822a8b5cffeb8913b942cb658a32`
- companion manifest: `findings/PROVENANCE.json`, `by_transcript_digest`
  `c1ec4da8…`, producing `tool_commit` `dada3e602689cb900971fda0dccce8267f31a2b2`
- worker head at which the figures were read: `1beadd9151331168f528940a303ffc36a1af222f`
- read utc: 2026-09-25T19:40Z · re-verified at `219075a` / ORCH-2 gate `45959ca`
  (provenance-only delta: ledger digest unchanged)

Figures bound by this block: the coverage count 3/16 (fixtures covered by a detector) and
the corroboration column 938/938 · 158/158 · 12/12 · 228/228.

**Policy pin (appended TASK-020 item 3):** the policy sha256 in force for every figure on
this page is `0fe20a6057ec9fa26fdc2184f84352185f8278fb346bc9d9de14927819ffdc85`. The
ledger digest `d42136c6…` and the by-transcript digest `c1ec4da8…` above are unchanged at
this append; that is the whole attribution chain (ledger → companion manifest → tool commit
`dada3e6` → policy sha), so no figure on this page needs commit archaeology to check.

**Re-verification (appended 2026-09-25T21:2xZ, TASK-020 item 3):** both digests in this
block were recomputed at head and match — `findings/ledger.jsonl` sha256 is still
`d42136c6…` (1334 findings), and `sha256` over the sorted `<sha256>  <relpath>` lines of
`findings/by-transcript/` reproduces `c1ec4da8…` (230 files, `m5r_reduce.dir_digest`). The
page's figures are therefore bound to the same ledger generation they were read from, and
the check is one command, not archaeology.

**TASK-020 supplement bindings (appended 2026-09-25T21:2xZ):** the q2 and q3 run
directories now carry `PROVENANCE-SUPPLEMENT.json` files (LAW §8 completion: tool_commit,
main_head, policy_sha256, book-store digest, corpus/split digests, config digest, per-part
output digest, detector re-pins with the original pins' defects stated). Digests are
recorded in `fleet/branches/WORKER-2-TASK-020-DELIVERY.md`; the supplements are new files
and nothing was edited in place.

**Control status (append-only, same date):** `PAUSE-WORKER-A-2026-09-25-001` was
**REMOVED** by ORCH-2 at 2026-09-25T20:02Z on the M5-R re-gate **PASS** (worker head
`1beadd9`; all 13 criteria, fresh independent evidence). The earlier note on this page
saying M4 is "parked under PAUSE" is superseded for control state only — the task order
it cites (ERRATA-25e §1) also put TASK-016 first, which is delivered. M4 q3–q5 resume
per TASK-018 (leg-(d) adjudication) then TASK-017.
