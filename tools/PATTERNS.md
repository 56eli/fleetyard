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
| A1-repetition | 938 | 840/938 re-derived; 98 flagged (claim or tokenizer shape) | 1/16 (CF-006) | **unmeasured** | no |
| A2-nonsense | 158 | 158/158 | 1/16 (CF-003) | **unmeasured** | no |
| B1-contradiction | 12 | 12/12 (book quotes byte-exact) | 2/16 (CF-003, CF-006) | **unmeasured** | no |
| B2-misquote | 228 | 228/228 (book quotes byte-exact) | 1/16 (CF-015) | **unmeasured** | no |
| A4-confusion | — | excluded since v1 (no independent FP rate) | — | unmeasured | no |
| drop-word | — | not built (M2 accepted incomplete) | — | unmeasured | no |
| speaker/format | — | not built (M2 accepted incomplete) | — | unmeasured | no |

Fixtures are **in-sample** by construction (LAW §9: seeded hits are never
precision/recall evidence). Clean-set figures from v1 (0/59) were tuned on those
passages — invalid as an independent false-positive estimate.

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

## 6. Next quanta (M4 work queue, in order)

1. **M4-q2 — drop-word detector** (largest unmeasured class): rule = word-level
   alignment of transcript spans against book/slide sources, flagging missing
   function/content words that restore grammar **and** doctrine; fixtures: CF-015
   (in-sample) + new hand-reads from the *tuning* set; holdout untouched.
2. **M4-q3 — speaker/format detector**: structural anomalies (missing speaker
   tags / merged turns / format drift), fixtures from M1 notes + tuning set.
3. **M4-q4 — per-detector precision runs** on the holdout split with frozen
   thresholds; publish provenance manifests; feed M6.
4. **M4-q5 — A1 claim-shape reconciliation**: resolve the 98 "not re-derived" A1
   claims (over-wide spans vs tokenizer shape) and record the outcome in
   `corrections.json`-style append-only notes for the detector rules.

Every step: suite green before push, control line per quantum, commit + push,
heartbeat with task id + sha.
