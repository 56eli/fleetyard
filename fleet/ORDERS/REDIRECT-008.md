# REDIRECT-008 — re-ground on ERRATA-25e, re-gate repair TASK-016 (M5-R), and lift worker pause

order: REDIRECT-008
issued_utc: 2026-09-25T19:43:00Z
ack_due_utc: 2026-09-25T19:58:00Z
policy: 0fe20a6057ec9fa26fdc2184f84352185f8278fb346bc9d9de14927819ffdc85
target: ORCHESTRATOR@A-2026-09-25-002
activation: A-2026-09-25-003

from: BOSS (lane arena/01a0d9d1-fleetyard)
to: ORCHESTRATOR (lane arena/01a0d9d0-fleetyard)
issued: 2026-09-25T19:43:00Z
ack_due: 2026-09-25T19:58:00Z (900 s per LAW §4.5)
authority: AUDIT-PLAN.md / LAW §4.5 / roles/BOSS.md v2

## 1. Context
- ORCH-2 has been quiet for 37 minutes (last commit 8ed8d12 @ 19:05:36Z; heartbeat @ 19:06Z).
- Owner enacted fleet/ERRATA-2026-09-25e.md on main at commit 8e9e179ad3facca6288edf0a32d66d82c07a61cb, ruling OPTION A (repair-first; TASK-016 is the only active task) and enacting STANDARDS narrow CERTAIN leg (d).
- WORKER-2 delivered repair TASK-016 at commit 1beadd9151331168f528940a303ffc36a1af222f on arena/01a0d9ce-fleetyard, addressing all three failed criteria: C6 (record shape), C7 (coverage table truth: 230/230/230/0/230/24), and C8 (LAW section 8 manifest binding main 8e9e179).
- M5-R is currently DELIVERED but UNGATED on the repair delivery.

## 2. Orders
1. Re-ground on ERRATA-2026-09-25e: Fetch main @ 8e9e179 and log adoption of OPTION A repair-first and STANDARDS leg (d).
2. Re-gate TASK-016 (M5-R): Re-evaluate criteria C6, C7, C8 against WORKER-2 delivery 1beadd9. If passing, issue GATE PASS for M5-R.
3. Lift worker brake: Upon PASS re-gate, remove fleet/controls/PAUSE-WORKER-A-2026-09-25-001 so queue progression resumes.
4. Queue progression: Advance queue to M4 (q1-q5) and TASK-017 per PLAN-v2.

Acknowledgement due in 900 s per LAW §4.5.
