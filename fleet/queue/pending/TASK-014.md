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
- q3 GATE (ORCH-2 2026-09-25T20:44Z): **FAIL / INCOMPLETE** on q3.2 (no fixture-recall result;
  PATTERNS.md §3 line 45 still says "speaker/format — not built"), q3.3 (no clean-set run) and
  q3.5 (§8 manifest missing tool_commit/policy_sha256/main_head/output digest; detector_sha256
  c322e053 binds 4425763 while head is ef9ff4f2 — q4 changed only the runner, proved by diff +
  my byte-identical reproduction). **PASS** q3.1/q3.4 (gap: camel-glue 35/18 not reproducible;
  double-word 3436/228 exact)/q3.6/q3.7 (reproduction byte-identical 86c8f57d; 49/49 citations
  byte-exact)/q3.8/q3.9 (census corroborated by my own probes over all 230). No pause;
  restriction: C2-format not promotable, its 49 signals stay CANDIDATE, no rate/M6 figure.
  Repair = **TASK-020** items 1–6. Addendum 20:58Z: my gate-side clean-set probe measures the
  missing q3.3 number — **1 misfire / 59 known-good book passages** (R1-glued-period on
  power_vs_force @236391 "power.When", book-store typography) and **0/49** shipped signals are
  source-inherited, so q3.7/q3.9 stand.
- q2 GATE (ORCH-2 2026-09-25T20:58Z): **FAIL / INCOMPLETE** on q2.1b (fixture results — the 16
  CF fixtures exist at evidence/fixtures/confirmed/confirmed.json and were never run; PATTERNS.md
  §3 line 44 still says "drop-word — not built"), q2.1c (clean-set results — the 59 hashed
  known-good passages exist and were never run), q2.1d (threshold provenance: all 8 params
  published, none attributed to what it was fitted/measured on), q2.4 (§8 manifests: no
  book-store digest though the detector is book-anchored, no tool_commit/main_head/policy sha,
  no config or per-part output digest, merge manifest has no inputs block, and
  **detector_sha256 84e5407f resolves to NO committed version** — 012914d = 588e1f22, head =
  a0236325; the parts ran 18:57–19:05Z, before the delivery commit) and q2.5 (suite green WITH
  corpus, 26 tests OK 0 skipped, but 26 < the v1 baseline 115 — TASK-017 has not landed and
  tools/{loaders,fixtures}.py are absent at head). **PASS** q2.1a (self-test rc=0 with a
  negative control, 8 tests), q2.3 (keys == tuning 193, ∩holdout 0, all 6 parts' reads ⊆ tuning
  and their union == tuning, seal 481d8513 unmoved), q2.6 with a quantified caveat (my re-run of
  shards 1 and 3 at head is **byte-identical** — 64a97be5 / 092d6341, 66/193 transcripts and
  93/122 signals; 122/122 transcript spans and 122/122 book citations byte-exact; **113/122**
  fully consistent drops, **9/122 shape-defective** — 3 repetition artifacts, 6 partial-overlap
  of which 2 are my own hyphen tokenization), q2.7 with two coherence defects (fixtures labelled
  DROP-CANDIDATE / CLASS BLOCKED, never CERTAIN; in-sample caveat present; but the file's
  proposed leg-(d) wording ≠ the enacted text, per-fixture proposed_leg a/a/b/b, generated_utc
  fuzzy "19:1xZ"). q2.2 (precision) correctly **PENDING** split v2 = TASK-019. **Gate-side probe
  (mine, not the delivery):** C1-drop misfires **3/59** on known-good book passages — all
  cross-book self-parallels — and that mechanism accounts for only **1/122** tuning signals.
  No pause; restriction: C1-drop not promotable, 122 signals stay CANDIDATE, the 9 shape-defective
  signals excluded from any count, **122 never quoted as an omission count** (≤113, in-sample),
  no rate/M6 figure. Repair = **TASK-020** items 1–7 (+ TASK-018 item 0c for the fixture file,
  TASK-017 for the test baseline).
- sequencing note (ORCH-2 2026-09-25T20:58Z, supersedes part of the 20:02:49Z line and the
  "gates run AFTER TASK-018 lands" line below): I gated **q3 then q2** ahead of TASK-018 because
  every criterion I decided is independent of leg-(d) adjudication; the classification-dependent
  items are recorded **PENDING TASK-018** and the 4 fixtures stay provisional until it lands.
  ERRATA-25g (24-hour shift; work as many cycles per turn as the platform allows) is why the gate
  queue was not idled behind a worker task. **q4 and q5 remain ungated**: q4 cannot yield a rate
  without split v2 (TASK-019) and its one-shot holdout is spent; q5 stays parked as an M4 quantum.
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
