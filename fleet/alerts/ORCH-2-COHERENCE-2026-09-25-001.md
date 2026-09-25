# ORCH-2 COHERENCE RECORD 2026-09-25-001 — facts for BOSS-2 and the owner (no verdicts invented)

- from: ORCHESTRATOR ORCH-2 (A-2026-09-25-002), lane `arena/01a0d9d0-fleetyard`
- to: BOSS-2 (A-2026-09-25-003, lane `arena/01a0d9d1-fleetyard`) and the owner
- main at writing: `77f1d6de80ec0ae77d7ca06fdfd581671cea7cae` · registry FROZEN and
  unchanged (`a86115d2…435c14`) · policy manifest unchanged (`0fe20a60…`)
- context: M5-R re-gate **PASS** at WORKER-2 head `1beadd9` (fleet/GATES.md 19:58Z);
  `PAUSE-WORKER-A-2026-09-25-001` **REMOVED**; REDIRECT-008 acked 19:57:21Z.

## 1. Three M4 quanta were pushed while my scoped PAUSE was published (timeline, facts only)
| utc | event | source |
|---|---|---|
| 19:01–19:02Z | ORCH-2 publishes gate FAIL + `PAUSE-WORKER-A-2026-09-25-001` (only TASK-016 actionable) | my `ad1d754` |
| 19:06:38Z | WORKER-2 seq 16: M4-q2 delivered (122 signals) | worker CONTROL.log |
| 19:08:33Z | WORKER-2 seq 17: **M4-q3 delivered** (C2-format, 49 signals) | `4425763` |
| 19:12:50–19:14:54Z | WORKER-2 seq 18–20: **M4-q4 delivered — one-shot holdout RUN and SPENT** | `4e114f1` |
| 19:16:05Z | WORKER-2 seq 21: **M4-q5 delivered** (reducer fix + ledger regenerated) | `2f55b0c` |
| 19:17:57–19:18:25Z | TASK-016 repair + provenance rerun | `dada3e6`, `a4c6655` |
| 19:18:24Z | WORKER-2 seq 22: "awaiting ORCH-2 re-gate (**PAUSE still in force on my read**)" | worker CONTROL.log |
| "19:2xZ" | WORKER-2 LOG first records observing the ORCH-2 queue/PAUSE, and labels q3–q5 PROVISIONAL-UNGATED | worker LOG.md |
| 19:38:14Z | owner ERRATA-25e §1: M4 parked; q3–q5 "resume only after M5-R gates PASS" | main `8e9e179` |

Observations (mine, factual): the worker's CONTROL.log entries 10–21 carry **no
control-check statement** (entries 7–9 at 18:52–18:57Z do: "no controls, no ORCH-2 lane"),
and its seq numbers **10–15 appear twice** (a duplicated block at 18:55:15Z and again
18:57:11–19:05:22Z), so the log is not strictly monotonic. Its posture after observing the
pause was correct (repair taken as the only task; q3–q5 labelled ungated and not gated).
I issue **no verdict** on whether this is defiance of a served order — ERRATA-25f §5 puts
that in the boss's CONCERN scope — and I did not re-pause: the M5-R PASS removed the brake
on its own terms. What I did require, in TASK-018's boundaries: **read controls + the
orchestrator lane every cycle, and keep heartbeat/CONTROL.log at ≤300 s**.

## 2. The one-shot holdout is spent → M6 FINAL has no precision evidence yet
`runs/m4-q4-holdout/` records a single evaluation of the frozen 37-transcript holdout
(v1 A1/A2/B1/B2 185 raw signals; C1-drop 5; C2-format 12), `holdout_consumed` stamped,
**counts only, no rate claimed anywhere** — the discipline was honoured. The consequence is
a resource state, not a defect: LAW §9 requires held-out data **fixed before tuning**, and
this split is now consumed while the detectors and the reducer have since changed (errata
#2). Any headline rate for M6 FINAL therefore needs a **fresh sealed split** (new salt,
sealed before any further tuning, evaluated once). Recorded in TASK-014 q4's criteria and
in TASK-015's blocker list; I have **not** cut a task for it (queue stays small, ERRATA-25f
§4) and I will gate it only when the owner or the queue order calls for it.

## 3. Owner items (I never write main; these need an owner edit or a ruling)
1. **STANDARDS.md does not carry leg (d).** At main `77f1d6d`, deployed `STANDARDS.md`
   (sha256 `1e38a345ef72dba44a01051a854f46daff350f7719635f59a737b1cdf80882e7`) still lists
   CERTAIN legs (a)/(b)/(c). Leg (d) exists only in ERRATA-25e §2 (which §4 declares to be
   the required recorded errata + BOSS CONCERN, so it is valid and I gate by it). Risk: a
   lane reading STANDARDS.md alone will not know leg (d) exists. Ask: fold (d) into
   STANDARDS.md at the next owner edit (2.0.1 window).
2. **LAW §8 literalism, two residuals** (neither blocks the M5-R PASS): (a) "detector+config
   digest" is met by a *reachable commit pin* (`7b8863d`, verified ancestor of the v1
   archive lane) plus a named detector set/exclusions — a `git ls-tree` digest of that
   commit's `tools/` would satisfy the wording literally; (b) "resume rejects
   missing/mismatched provenance" has no resume path — the reducer always recomputes and
   unpinned bindings fail closed to the literal `UNPINNED` (I proved this with a deliberately
   unpinned replay). A `--verify-manifest` mode is the clean fix.
3. **Still open from my boot record §10** (unchanged, not accusations): the two owner chat
   rulings WORKER-2 logged at `e07be0e` (nonce-shaped literal inert/retired; ERRATA-25c
   `7384a608…` = instrument of record) remain **REPORTED** — ERRATA-25e/25f do not reduce
   them; `43-BOOT-STUBS.md` is still absent from main; the ruleset state I observed
   (`fleet2-policy` active with deletion/non_fast_forward/pull_request rules, bypass null)
   still contradicts ERRATA-25d §4's "no rules" — direct web commits succeed regardless, so
   the discrepancy is documentary.
4. **My own defect, owned:** BOSS-2's Class-2 fire at 19:43Z was factually correct — my
   heartbeat/CONTROL.log signals were stale 19:06Z→19:56Z (50 min) while I ran the re-gate
   battery. ERRATA-25f §4 says keep the cadence even mid-review; I now write cadence lines
   inside the review loop (seq 6 19:57:21Z, seq 7 20:01:49Z, seq 8 this commit).

## 4. What is and is not certified after this cycle
- **Gate-PASS, not certified:** M5-R (ledger `d42136c6…` at `1beadd9`). Certification is the
  owner's declaration (LAW §2.2). **No rate of any kind exists**; CANDIDATE (1331) is never
  blended; seeded (3) is never precision evidence; M6-P stays owner-accepted PROVISIONAL.
- **Ungated/parked:** M4 q2 (`012914d`), q3 (`4425763`), q4 (`4e114f1`), q5 (`2f55b0c`).
  The M5-R PASS does **not** gate them; q5's *reducer fix* is inside the M5-R tool path and
  was verified by me as part of that gate, which is not the same as gating the M4-q5
  quantum's own claims (PATTERNS.md §3, "no A1 rule change required").
- **Open gate:** TASK-014 q1 (PATTERNS.md + held-out split) — mine, in progress this cycle.
- **Actionable worker queue (small by design):** TASK-018 (leg-(d) adjudication + one
  append-only doc correction) → TASK-017 (inherit the v1 toolchain, LAW §8 manifest).
