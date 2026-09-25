# ALERTS — sober ledger (append-only)

Per owner ruling 2026-09-25: the alert **headline** carries the Jameson voice and is the text
delivered to the owner's Discord by the repo-level GitHub→Discord webhook. This file and the
commit **body** carry the sober payload: class, minutes, shas, next action. `fleet/LOG.md`
stays sober. Worker and orchestrator work commits stay dry.

Dedup rule in force: max one alert per class per 20 minutes.

---

## 2026-09-25T08:45Z — CLASS 1 — WORKER STALLED

- class: (1) worker stalled
- quiet: **488 minutes** (8 h 08 m)
- worker lane: `arena/01a0d581-fleetyard`
- worker head: `5ea8de8b8eb5ceb1b1aa6d0e9360c8d10b79478b` @ 2026-09-25T00:36:28Z
- last heartbeat line: 2026-09-25T00:32:27Z "cycle 13 TASK-010 PASS @ c833bee seen ... claim
  TASK-011 @ arena/01a0d581-fleetyard c833bee (97 tests OK, 16 findings)" — a **claim**, not a
  handoff and not capability-lost, so the class fires on its literal terms
- threshold: heartbeat age AND worker-head age both >20 min → 488 min and ~492 min
- task in flight: **TASK-011** (M5 raw census) CLAIMED at 00:32:27Z, **never delivered**
- committed M5 artefacts: `tools/sweep_m5.py`, `tests/test_sweep_m5.py` only — no sweep output,
  no findings ledger, no `reports/` on any lane
- possible causes: worker session ended / capability cut / sandbox teardown mid-task. Not
  determinable from the lane: no handoff line and no insanity pill
  (`fleet/alerts/worker-insanity` absent), and `fleet/controls/PAUSE-WORKER` is absent on the
  orchestrator lane, so no brake was holding it
- next action: boot a successor worker lane; per `fleet/roles/WORKER.md` it CONTINUES from the
  worker lane's state at `5ea8de8` and must **not** restart TASK-011 — `tools/sweep_m5.py` is
  resumable by design, so the existing progress carries forward
- delivered by: BOSS commit headline (repo-level GitHub→Discord webhook)

## 2026-09-25T08:45Z — CLASS 2 — ORCHESTRATOR SILENT

- class: (2) orchestrator silent
- quiet: **440 minutes** (7 h 20 m)
- orchestrator lane: `arena/01a0d5b7-fleetyard` (the active successor)
- orchestrator head: `e4fa5b9` @ 2026-09-25T01:24:53Z
- last heartbeat line: 2026-09-25T01:24:53Z "CYCLE 16/40 SCHEDULE WATCH ... then sleep 300s
  before cycle 17" — **cycle 17 never ran**, so it stopped mid-shift without a handoff line
- threshold: heartbeat age >20 min → 440 min
- consequence, per the role definition: **gates, queue, and pause-removal are down.** Nothing
  can be gated, no task can be cut or re-opened, and no certification can be issued
- its own caps at stop: 16/40 cycles, ~123/240 min wall — it did **not** exhaust either, so
  this is a crash or teardown, not a lawful exit
- blocked behind it: **TASK-011** CLAIMED and ungated; **TASK-012** (M6 provisional report)
  still BLOCKED and never started
- next action: boot a successor orchestrator lane. Per owner ERRATA-2026-09-25 §2 it must
  re-gate standing state before certifying anything, and per REDIRECT-007's served priority it
  must keep the order TASK-011 → TASK-012 → TASK-007 → TASK-009 → TASK-008
- delivered by: BOSS commit headline (repo-level GitHub→Discord webhook)

## Classes considered and NOT fired at 2026-09-25T08:45Z

- class (3) queue starved — does not fire: TASK-011 is CLAIMED, so the queue is not empty
- class (4) post-handoff with no successor — does not fire on its literal terms, because
  neither lane's last line is a handoff. Both stopped mid-shift. Reported as worse than a
  clean end rather than being forced into a class it does not match
- predecessor `arena/01a0d582-fleetyard` @ `191b1f8` (stopped at cycle 84, superseded,
  read-only) — silence expected and NOT alertable

## Retired channel

The direct Discord webhook given at boot never delivered: HTTP 000, `SSL_ERROR_SYSCALL` to
`discord.com:443`, on every attempt across cycles 2, 3 and 4 — 0 of 4 composed alerts
delivered. Its four composed texts are preserved verbatim in `fleet/LOG.md`. Superseded by the
repo-level GitHub→Discord webhook as of the owner ruling of 2026-09-25.

---

## 2026-09-25T10:23:05Z — class 2 timer tripped, ALERT NOT POSTED (reasoning on the record)

| field | value |
|---|---|
| class | (2) orchestrator silent — TIMER ONLY |
| measured_at | 2026-09-25T10:23:05Z (fresh fetch, verified) |
| orchestrator lane | `arena/01a0d5b7-fleetyard` @ `577c9c5`, committed 2026-09-25T09:46:36Z |
| quiet | 34.7 min (timer threshold 20 min) |
| worker lane | `arena/01a0d581-fleetyard` @ `663d05a`, 3.9 min — healthy |
| posted to Discord | **NO** |
| next action | re-measure next cycle; fire class (2) properly if head is still `577c9c5` |

**Why no alarm.** The class-2 template asserts a consequence — "gates, queue, and pause-removal
are down" — that is false at this timestamp. The orchestrator gated TASK-011 at 09:31:52Z and
published the interim answer at 09:46:36Z; its cadence is 300s and owner ERRATA-2026-09-25 §4
permits pushing only on substance or roughly every 20 minutes for liveness. Posting an alarm
whose stated consequence BOSS knows to be untrue would breach CANON §5 worse than withholding
the ping. BOSS had already had to correct one stale alarm earlier this shift (see LOG
self-correction) and will not compound it. This entry exists so the decision is auditable
rather than silent.

**Trip-wire:** if the orchestrator head is unchanged at the next cycle, class (2) fires with the
Jameson headline, the key number and the sha.
