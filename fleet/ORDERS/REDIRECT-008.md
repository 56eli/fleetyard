# REDIRECT-008 — re-ground on ERRATA-25e/f, re-gate repair TASK-016 (M5-R), and lift worker pause

> **STATUS NOTE (Owner Ruling ERRATA-2026-09-25f §5):** URGENCY FRAMING RETIRED.
> Deep review quiet is normal under the new liveness doctrine; no 900 s acknowledgement
> deadline is in force. The re-gate substance stands as ordinary queue law — ORCH-2
> re-gates when its review of TASK-016 completes.

order: REDIRECT-008
issued_utc: 2026-09-25T19:43:00Z
ack_due_utc: 2026-09-25T19:58:00Z
policy: 0fe20a6057ec9fa26fdc2184f84352185f8278fb346bc9d9de14927819ffdc85
target: ORCHESTRATOR@A-2026-09-25-002
activation: A-2026-09-25-003

from: BOSS (lane arena/01a0d9d1-fleetyard)
to: ORCHESTRATOR (lane arena/01a0d9d0-fleetyard)
issued: 2026-09-25T19:43:00Z
authority: AUDIT-PLAN.md / roles/BOSS.md v2 / ERRATA-2026-09-25f

## 1. Context
- Owner enacted `fleet/ERRATA-2026-09-25e.md` (OPTION A repair-first + STANDARDS leg d) and `fleet/ERRATA-2026-09-25f.md` (liveness doctrine).
- WORKER-2 delivered repair TASK-016 at commit `1beadd9151331168f528940a303ffc36a1af222f` on `arena/01a0d9ce-fleetyard`, addressing all three failed criteria: C6 (record shape), C7 (coverage table truth: 230/230/230/0/230/24), and C8 (LAW §8 manifest binding main `8e9e179`).
- M5-R is currently DELIVERED on the repair delivery and undergoing ORCH-2 review.

## 2. Queue Law Substance
1. **Re-ground on ERRATA-2026-09-25e and 25f:** Adopt OPTION A repair-first, STANDARDS leg (d), and liveness-as-signals doctrine.
2. **Re-gate TASK-016 (M5-R):** Re-evaluate criteria C6, C7, C8 against WORKER-2 delivery `1beadd9` at normal review depth. When review completes, issue GATE verdict for M5-R.
3. **Lift worker brake:** Upon PASS re-gate, remove `fleet/controls/PAUSE-WORKER-A-2026-09-25-001` so queue progression resumes.
4. **Queue progression:** Advance queue to M4 (q1-q5) and TASK-017 per PLAN-v2.
