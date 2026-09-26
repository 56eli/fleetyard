# boss cursor

updated: 2026-09-26T09:35Z
boss lane: arena/01a0d9d1-fleetyard
activation: A-2026-09-25-003 (BOSS-2)
status: **ACTIVE / IN FORCE** — owner rulings `fleet/ERRATA-2026-09-25d.md`, `25e.md`,
  `25f.md`, and `25g.md` on main @ `7d033abd3f52d0cb8a3a3b0c61881bdef5fad95a` re-grounded.
  24h shift expectation in effect; continuous cadence cycling within turns; tracker published
  as pushed documentation; zero reporting stops.
cadence: 300 s control check (even while dormant) / 900 s cycle sleep.

## milestone state (the campaign scoreboard — PLAN-v2)
- M0 corpus inventory — **CERTIFIED ✓** @ 863c97d (preserved from v1)
- M1 tooling foundation — **CERTIFIED ✓** @ 9f56f3e (repaired set; preserved from v1; full v1 toolchain inherited and **GATED PASS on all 6 criteria** by ORCH-2 @ `a022ef9`)
- M2 detector family A — **ACCEPTED INCOMPLETE ✓** (owner §3; drop-word + speaker/format deferred to M4)
- M6-P provisional report — **ACCEPTED PROVISIONAL ✓** @ 90077b4 (`reports/CORPUS-AUDIT.md`, 187 lines, worker v1 lane `bf97d85`, verified by v1 boss; accepted as v1 deliverable per HALT notice)
- M5-R reviewed findings ledger — **GATED PASS on all 13 criteria** by ORCH-2 at `5f6d698` / `9989249`,
  re-affirmed @ `45959ca`. C6, C7, C8 repaired by WORKER-2 at `1beadd9`.
  Findings ledger: `findings/ledger.jsonl` with 1,334 findings: **3 CERTAIN-inherited**
  [CF-003, CF-006, CF-015] / **0 HIGH** / **1,331 CANDIDATE**; 242/242 book refs byte-exact;
  deterministic; 26 tests green. Scoreboard: **3 / 0 / 1,331**. Milestone **CLEARED**.
- M4 self-improvement loop — **IN PROGRESS** on worker lane (Scoreboard: **q1 PASS, q2 INCOMPLETE, q3 INCOMPLETE [1 item], q4 PASS, q5 PASS**):
  - q1 catalog + split: **RE-GATED PASS ✓** by ORCH-2 @ `ee4ea5e` (repaired by TASK-020 item 0b; PATTERNS binds ledger, by-transcript, tool_commit dada3e60, worker head 1beadd9, policy 0fe20a60).
  - q4 one-shot holdout run: **RE-GATED PASS ✓** by ORCH-2 @ `ee4ea5e` (repaired by TASK-020 item 9; holdout receipt verified 185/185; 13/13 tool pins verified to archive lane; exposure-normalized Poisson deficit P=7.7e-05 published; receipt only, no rates, spent holdout never re-run).
  - q5 residuals: **RE-GATED PASS ✓** by ORCH-2 @ `ee4ea5e` (repaired by TASK-020 item 11; supersession blocks name findings/PROVENANCE.json as binding of record; A1 corroboration verified 938/938 under direct claim test).
  - q3 C2-format: NEAR-PASS (substance verified 0/16 fixture recall, 1/59 clean set traced to book store, LAW §8 bindings recompute MATCH; pending 1 item: item 8a tool re-pin).
  - q2 C1-drop: INCOMPLETE (substance reproduced 93/122 byte-identical; pending item 8a tool pin + TASK-018 items 0d-0g).
  - Toolchain foundation: TASK-017 **GATED PASS ON ALL SIX CRITERIA** by ORCH-2 @ `a022ef9` (266 manifest entries verified three ways head == archive, suite 217 OK / 1 skip, 16 fixtures verified, fresh sweep 10/10 four-way equality; item 17.a owed non-blocking).
  - Leg-(d) individual adjudication: TASK-018 GATED FAIL / INCOMPLETE (no pause) by ORCH-2 @ `a022ef9`. Substance verified 57/57 byte-exact under strict reconstruction; 4 repairs owed: 0d (false seeded sentence in SUMMARY and PATTERNS 5b-bis), 0e (dedupe 2 duplicate sites, 55 distinct sites), 0f (stratification table: 27/57 fillers/interjections, 6 notation variants, 11 function words, ~13 content; audio-unknowability disclosure), 0g (reconcile D-002/D-039 contradictions). Restriction: 57 never quoted without sensitivity table 71/57/33/22, strata, 55 sites, notation status.
  - Fresh split v2: TASK-019a GATED FAIL / INCOMPLETE on v2.5 only by ORCH-2 @ `a022ef9`. Seal is VALID, reproducible, uncontaminated, NOT void (197 tuning / 33 holdout). Defect: post-seal dropword fixture append changed digest c8e96319 -> c40d272f. Item v2.a (dated append-only note) and v2.b cut. Quantum b held pending v2.a.
  - Consolidated repair: TASK-020 items 1-8 gated @ `a022ef9` (fails 20.1 tool pins, 20.5 D-002/039 contradictions); items 9-11 gated @ `ee4ea5e` (20.11 PASS, 20.12 PASS, 20.10 FAIL on tool pin only). Item 8a extended to 6 supplement files. Item 11a, 11b, item 12 (exact timestamps) cut.
  - C1-drop sensitivity: TASK-021 CUT by ORCH-2 @ `a022ef9` (grid over v2 tuning half 197 files; min_flank 2/3/5/8, min_ratio 0.80/0.85/0.90, min_matched 8/10/14; HoldoutGuard in code; criteria 21.1-21.8).
  - BOSS Guidance on clause d-i: Per ERRATA-25e §2 text ("not accounted for by ... transcriber formatting convention"), notation variants (% vs percent) are transcriber formatting conventions and excluded from omission counts. Fillers/interjections must be stratified with audio-unknowability disclosure and sensitivity table 71/57/33/22.
  - Actionable queue: WORKER-2 to claim repair items (0d-0g, v2.a-v2.b, 8a-8b, 11a-11b, 12, 17.a) and TASK-021; ORCH-2 drafting quantum-b pre-registration protocol.
- M6 final audit report — **BLOCKED on fresh sealed holdout split v2 repair v2.a + M4 completion**
  (TASK-017 passed; q1, q4, q5 passed; awaiting quantum b one-shot evaluation).
- **Completion:** DECLARED BY THE OWNER ONLY on main against the completion manifest (LAW §2.2). BOSS tracks and advises.

## lanes (verified by explicit-refspec fetch 2026-09-25T22:56Z)
- main: `7d033abd3f52d0cb8a3a3b0c61881bdef5fad95a` (owner commit, `fleet/ERRATA-2026-09-25g.md`)
- worker (WORKER-2): `arena/01a0d9ce-fleetyard` @ `15d5c3c4975595422d1684c37460a3ccce72d6cd` (ALIVE; full test suite 302 OK / 1 skip, floor 257, +45; TASK-021 sensitivity grid running over tuning partition; holdout untouched)
- orchestrator (ORCH-2): `arena/01a0d9d0-fleetyard` @ `af8444d61e3e608306365b23ae4b42e0393c2037` (ALIVE; Gate Cycle K completed at `34db0b0`: M5-R PASS re-gated, instrument 331 rows, 31/31 selftest)
- boss (BOSS-2): `arena/01a0d9d1-fleetyard` — ALIVE, ACTIVE / RESUMED
- predecessor archives (frozen, read-only):
  - worker v1: `arena/01a0d581-fleetyard` @ `bf97d85` (HALT ack)
  - orch-2 v1: `arena/01a0d5b7-fleetyard` @ `fcc9834` (HALT ack)
  - boss v1: `arena/01a0d585-fleetyard` @ `37e7260` (HALT ack)
  - orch v1: `arena/01a0d582-fleetyard` @ `191b1f8` (superseded)
  - seed: `arena/01a0d56b-fleetyard` @ `993f9d2`

## brakes & controls
- `fleet/controls/PAUSE-WORKER-A-2026-09-25-001`: **LIFTED / REMOVED** by ORCH-2 at `5f6d698` / `9989249`.
- `STOP-BOSS` / `STOP-BOSS-2`: ABSENT.
- `STOP-WORKER` / `STOP-WORKER-2`: ABSENT.
- Zero active brakes across the fleet.

## orders in flight
- `fleet/ORDERS/REDIRECT-008.md`: **ACKNOWLEDGED & COMPLETED** by ORCH-2 (`fleet/ORDERS/ACK-REDIRECT-008.md` @ `5f6d698`).

## stall watch (re-armed per ERRATA-25f §2: signals only)
- Class 1 (worker stalled): NOT FIRED (WORKER-2 active @ `4fc40c8`).
- Class 2 (orchestrator silent): NOT FIRED (ORCH-2 active @ `ee4ea5e`).
- Class 3 (starvation): NOT FIRED (M4 re-gates delivering passes; repairs and protocol in flight).
- Class 4 (post-handoff): NOT FIRED (all v1 archives verified frozen).
- Class 5 (LOUD ZOMBIE): ARMED.
- Class 6 (context-rot support): ARMED.

## CONCERN criteria (narrowed per ERRATA-25f §5)
- (1) Liveness-signal staleness (>20 min without heartbeat/CONTROL.log)
- (2) Authority invention
- (3) Product-integrity risk
- (4) Defiance of a served order
- Current status: **ZERO CONCERNS ACTIVE**; all roles aligned with ERRATA-25d/e/f/g.
