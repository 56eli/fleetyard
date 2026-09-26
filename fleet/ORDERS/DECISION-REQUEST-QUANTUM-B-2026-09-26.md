# DECISION REQUEST — fire quantum b now, or after item v2.e? (owner's call, one-shot cost)

From: ORCHESTRATOR (ORCH-2, A-2026-09-25-002) · lane `arena/01a0d9d0-fleetyard` · 2026-09-26T09:57:29Z
To: OWNER (decision) · BOSS-2 (visibility) · WORKER-2 (do not act on this until the owner rules)
Authority cited: LAW §9 (no certification without held-out evidence) · ERRATA-2026-09-25g §5 (fresh sealed split v2
AUTHORIZED — new salt, sealed before further tuning, **evaluated once**; M6-Final waits for it) · TASK-019 items v2.7/v2.8
(one-shot discipline: frozen thresholds, single run, consumed receipt, **no re-run**).

## Why this is a request and not a gate verdict

Everything ORCH-2 can measure is measured and published: at WORKER-2 `f5e2cf5` the quantum-b **precondition row PASSes with
n=0 open preconditions**, the v2.16 precedent row PASSes (n=521), TASK-015's three named preconditions are all satisfied
(M5-R PASS, TASK-014 q4 PASS, TASK-017 PASS), and the M4 scoreboard is PASS on all five questions. **The run itself has not
happened** — no receipt declares the V2 holdout spent. Firing it is irreversible: one evaluation of a sealed split, and a
second run would be exactly the discipline breach v2.7 exists to prevent. An orchestrator may sequence queue work; it may not
spend a one-shot on its own reading of the moment. So this lane will not fire it, and has told the worker not to either.

## The one fact that makes the sequencing non-obvious

**Item v2.e is still open, and it is a seal-integrity gap, not a documentation gap.** The seal report's citation census does
not name its key: the fixture file mentions the confirmation artefact at **10 paths, of which 5 are artifact+sha pairs**, while
the report carries **1 row / 1 distinct**. The load-bearing half is that the **5 unpaired mentions** — including
`/adjudication_summary_2026_09_25/artifact` — sit **outside** the tool's post-seal void check. So a post-seal confirmation
cited without a paired sha would **not** fire the check that is supposed to detect exactly that. Quantum b is the run whose
whole value depends on the seal holding after it is fired.

The other three open rows do **not** touch the seal: **v2.f** (a header stamp in a prep record), **item 12 / 20.14a** (two
fuzzy stamps in two newly created lane records) and **item 13b** (one clause in a reproducibility note). They are real and they
are mapped, but none of them can invalidate an evaluation.

## The options, with what ORCH-2 will do in each case

- **A — fire now.** Fastest path to the owner's "how bad is it" answer. Cost: the single evaluation is spent while a
  post-seal confirmation could go undetected by the void check. ORCH-2 would gate the receipt (single run, frozen thresholds,
  consumed flag, counts and rates separated, no re-run) and would record the v2.e gap beside the result permanently.
- **B — hold until v2.e closes (ORCH-2's recommendation, as gate, not as owner).** The repair is bounded and already
  specified in `fleet/ORCH-2-REPAIR-MAP.md`: make the census one row per citation, attributable by path, state its key, correct
  the appendix sentence from "all five citations" to 10 mentions / 5 pairs, and either extend the void check to unpaired
  mentions or state as a restriction that it does not. Then fire, once, against a seal whose post-seal detector actually
  covers the artefact. Cost: one worker cycle of delay.
- **C — hold until all four rows close.** No seal benefit over B; it delays the one-shot for documentation-class repairs.
  ORCH-2 does not recommend it and will not require it.

Whichever is chosen, the standing restrictions are unchanged and are not ORCH-2's to lift: no detector is promotable, no
rate or M6 figure may be quoted from the tuning half, the spent v1 holdout is never re-run (its counts stay counts), M6-P
stays owner-accepted PROVISIONAL and is never re-certified, and CANDIDATE never enters a rate.

## What this lane does while the decision is open

It does not idle and it does not guess: cycle L is published (336 rows, FAIL 5, selftest 36/36, suite floor 283), the queue is
re-stated per task, TASK-021's floor is corrected by measurement, and the gate re-runs at whatever head arrives next. This
request is recorded as a document because ERRATA-25g is explicit that status is pushed documents, not chat.
