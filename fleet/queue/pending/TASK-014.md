# TASK-014 — M4: formal self-improvement loop (PATTERNS.md + detectors + held-out validation)

- q1 GATE (ORCH-2 2026-09-25T20:08:32Z): **FAIL / INCOMPLETE** on q1.4d only (PATTERNS.md quotes the M5-R
  ledger's figures with no binding to its digest); q1.1/q1.2/q1.3/q1.4a-c **PASS** — the
  split is verified clean, deterministic, reproducible by me byte-for-byte (holdout 37 /
  tuning 193; corpus_files_sha256 9ae90185… reproduced; fixtures forced TUNING; seal
  unmoved since 593cad3), all 16 fixtures wired, every precision cell unmeasured.
  Repair = TASK-018 item 0b (append-only binding + pause-removal line). **No activation
  pause issued** — artefact-scoped restriction instead, reasons in fleet/GATES.md 20:08Z:
  q1 may not be cited as passed, no M4 promotion or q2-q5 gate credit, no M6 figure may
  rest on PATTERNS.md until the binding lands.
- status (ORCH-2 2026-09-25T20:02:49Z): q1 gate **OPEN** (mine, in progress); q2 **PARKED** by owner
  ERRATA-25e §1 (DELIVERED-PROVISIONAL-UNGATED @ `012914d`, not gated, not certified);
  q3 `4425763`, q4 `4e114f1`, q5 `2f55b0c` delivered 19:08-19:16Z, **UNGATED**, parked
  with q2 and now resumable after the M5-R PASS — gating order is q1 → q2 → q3 → q4 → q5.
  Leg (d) (ERRATA-25e §2) governs q2's classification claims; adjudication itself is
  TASK-018, and q4 now owes a FRESH sealed split (the one-shot holdout is spent).
- milestone: **M4** (fleet/PLAN-v2.md) · cut by ORCH-2 (A-2026-09-25-002) 2026-09-25T19:01Z
- claimant: WORKER-2 (A-2026-09-25-001) — actionable only after TASK-016 re-gates PASS
  (PAUSE in force). q1 was delivered before this task existed (commit `593cad3`); it is
  ratified as TASK-014 q1 and gated against the criteria below, not against criteria
  invented after the fact where the delivery is already stronger.
- prerequisites: **TASK-017** (v1 toolchain inherited with provenance) for q2–q4.

## q1 — rule catalog + held-out split (DELIVERED `593cad3`; GATE OPEN, no verdict yet)
Acceptance:
- q1.1 `tools/PATTERNS.md`: every CERTAIN fixture mapped to a pattern + a rule sketch +
  whether a current detector catches it; coverage truth re-derived from the ledger, not
  asserted. (Observed: P1–P7 over the 16 fixtures; 3/16 covered — CF-003, CF-006, CF-015;
  13 invisible. Matches my own re-derivation.)
- q1.2 held-out split **fixed before any tuning** (LAW §9), deterministic, published,
  sealed (method + salt + mod + bucket + corpus digest), with in-sample fixture transcripts
  forced into TUNING and an honesty disclosure about v1's corpus-wide knowledge.
  (Observed: holdout 37 / tuning 193 / 230; `m4_split.py verify` → OK rc=0.)
- q1.3 per-detector status table with precision **unmeasured** and promotable **no** until
  q4; seeded/in-sample figures never presented as precision (LAW §9).
- q1.4 open items I will gate: rule→fixture wiring for all 16; `corpus_files_sha256`
  derivation documented; tuning code demonstrably unable to read the holdout list;
  PATTERNS.md bound to the M5-R ledger digest it quotes.

## q2 — drop-word detector (M2 remainder, never built)
- Ships WITH: self-test, fixture results (which of the 16 confirmed fixtures it catches —
  CF-015 class P5 is the target), clean-set results on genuinely held-out passages, and a
  disclosed threshold-provenance (fitted on what, measured on what).
- Precision/recall only against the q1 holdout (37 transcripts), fixed before tuning;
  tuning runs must not read the holdout; the split's seal must not change.
- LAW §8 manifest for every cache/run: corpus + book-store + split digests, detector and
  config digest, tool commit, policy sha, output digest, run utc.
- Suite green WITH corpus, skip counts reported, test count never drops (campaign baseline
  is v1's 115 — see TASK-017).

## q3 — speaker/format detector (M2 remainder, never built)
- Same shipping requirements as q2, plus an explicit statement of what "speaker/format
  error" means mechanically (speaker label drift, merged/split turns, attribution mismatch)
  and what it cannot see. Unmeasured ≠ zero until it ships.

## q4 — held-out validation of B1/B2 (and the A4 decision) BEFORE any headline rate
- B1-contradiction and B2-misquote validated on the q1 holdout: v1's gate hold stands
  (TASK-005 FAIL / REDIRECT-005 — B1 thresholds were calibrated on the clean set, B2
  filters fitted), so **no headline rate for B1/B2 until this passes on data fixed before
  tuning**.
- A4-confusion: re-admission only with independent fixture recall (v1: 0/16 independent,
  8 seeded) and a genuinely held-out clean-FP measurement; v1's 0/59 is VOID as independent
  FP evidence (owner ERRATA-2026-09-25 §3). Otherwise A4 stays excluded and says so.
- Output: per-detector precision + FP counts on holdout, seeded vs independent reported
  separately, promotion decisions recorded with their evidence; detector promotion requires
  held-out validation + provenance-manifested caches (PLAN-v2 M4).

## q2-q4 precision criteria RE-CUT (ORCH-2 %s) — the one-shot holdout is spent
The q1 holdout (37 transcripts, salt `fleetyard-m4-holdout-2026-09-25`) was **evaluated once**
at 19:12-19:14Z (`runs/m4-q4-holdout/`, `holdout_consumed: true`, counts only, no rate) and is
**spent**: LAW §9 requires held-out data *fixed before tuning*, and both the reducer (errata #2)
and the detector set have moved since. Therefore, for q2, q3 and q4:
- any precision/recall or promotion criterion is evaluated against **TASK-019's fresh sealed
  split v2** (owner-AUTHORIZED, ERRATA-25g §5 @ main 7d033ab; cut 20:35Z) — a **fresh sealed split v2**
  (new salt, dated record, sealed BEFORE any further tuning, evaluated exactly once) — not
  against the spent split, and not against the tuning set;
- **do not re-run the spent split**; it stays on the lane as a receipt, and its counts
  (v1 185 / C1-drop 5 / C2-format 12) remain counts, never rates;
- until split v2 exists and has been evaluated once, every precision cell stays **unmeasured**
  and every detector stays **not promotable** — that is a correct state, not a defect;
- q2's classification claims are gated under the leg-(d) standing guidance in fleet/GATES.md
  and depend on **TASK-018**'s per-finding adjudications (the 122 signals and 4 provisional
  fixtures are signals/provisional until then; detector hits never auto-classify).
Gate sequencing (recorded so it is not read as idleness): **q2 → q3 → q4 → q5 gates run AFTER
TASK-018 lands**, because TASK-018 changes q2's fixture classes and because q4 cannot yield a
rate without split v2. Gating now would produce verdicts on artefacts that are about to move.

## Global boundaries
Frozen corpus · stdlib only · no network · finding = citation · CANDIDATE never in a rate ·
CERTAIN and HIGH reported separately · every CERTAIN becomes a rule + fixture · no
certification language (milestone certification is ORCH-2's, completion is the owner's).
