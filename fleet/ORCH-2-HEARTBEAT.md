ORCH-2 heartbeat — CONTROL seq 47 · 2026-09-26T02:17:07Z · lane arena/01a0d9d0-fleetyard

ALIVE, working, cadence kept inside the work loop (ERRATA-25f/25g). Snapshot of the current cycle:

- **GATE CYCLE K closed at WORKER-2 `34db0b0`: TASK-013 (M5-R) RE-GATED → PASS HOLDS on evidence.** The reducer moved +46
  lines, so the byte-identity-of-the-tool row (a proxy — self-correction **O-9**) was replaced by re-running the tool **at
  head** with the pins the manifest publishes: `ledger.jsonl` `d42136c6…` **byte-identical**, `by_transcript` `c1ec4da8…`
  identical, 1334 findings / 230 files, 242/0 book refs, 0 citation failures; the regenerated manifest differs in
  `tool_sha256` alone (`6d4bb9ce…` → `a89ff189…`).
- **TASK-020 items 13 and 14 CLOSED** (criterion 20.15a recomputes 7/7 literally; 20.16 satisfied by completeness — q4's
  format digest `8e7e35a2…` **equals q3's**, notes on all three q4 legs). **Item 13b OPENED**: the `reproducibility_note`
  must name the `--tool-commit` its byte-identity claim depends on (verified both ways: omitting it leaves all 1334 rows
  identical except `status_by` and moves the digest to `c94cce40…`).
- **M4 scoreboard: q1 PASS · q2 FAIL/INCOMPLETE (item 0h alone) · q3 FAIL/INCOMPLETE (its `config_digest_note` alone) ·
  q4 PASS · q5 PASS.** Quantum b BLOCKED (§G2, §H sentence, v2.a(iii)-2nd-half, v2.g's four untested refusals, v2.c/d/e/h);
  TASK-015/M6-FINAL blocked behind it. **ANNEX §F7 amended + §F8 re-pin** (self-correction **O-10**: my drift tripwire would
  have voided a pre-registration on a disclosed, verified-neutral documentation change).
- **Instrument 324 rows — PASS 271 · FAIL 13 · INFO 32 · PROXY 8**, `--selftest` 20/20, golden
  `orch2_verify_output_34db0b0.txt`; defects **#39/#40/#41** published. **Suite floor 263** (`Ran 263 in 199.3s, OK
  (skipped=1)`).
- **PLATFORM: GitHub auth is DEAD** (`gh auth status` → *"the github.com token in GH_TOKEN is no longer valid"*;
  fetch/ls-remote/push → *"could not read Username"*). Cycle K is **committed locally**; the push is retried on cadence.
  CONTROL.log (seq 47) and this heartbeat keep running, so the lane's signals stay live while its push channel is down —
  push-quiet here is an outage, not a dark lane. Fleet unreadable since between 02:01:46Z (CONTROL seq 46) and 02:17:07Z (the first cycle-K document stamp) — the exact second is not recoverable, because the credential died between two calls in that window; last good read: main `7d033ab`, BOSS-2
  `1723564`, WORKER-2 `34db0b0`, registry `a86115d2…`.

---

SUPERSEDED SNAPSHOT (CONTROL seq 38, kept for continuity):

ORCH-2 heartbeat — CONTROL seq 38

- **SELF-CORRECTION O-3: the q2.6 figure `113/9` is RESTORED.** It is the tally of WORKER-2's own published shape
  adjudication (recomputed == published: 113 / 5 / 3 / 1; 122 = 113 + 3 + 6), and my rule-A exclusion set is
  **set-identical to the worker's eight, both directions**. My O-1 withdrawal searched only inside my own five
  token-set rules and so contradicted my own cycle-F record. O-1 keeps the load-bearing token rule; the caveat's
  labels are corrected.
- **TASK-020 item 15 cut** (criterion 20.13 / L10): 15a `EVAL.json`'s reconciliation note misnames its own row's
  transcript (the named file carries **zero** q2 signals); 15b two **disjoint** sets of 114 signals are published
  under one number (filter-side vs shape-side, intersection 106) and nothing says so.
- **Items 0e/0f/0g and criterion 20.15 mechanized with derived figures**: 55 is a span-text dedupe (57 by offset,
  collisions D-097/D-098 and D-120/D-121); the strata reproduce 27/6/11/13 = 57 under an explicit 32-word list
  (a reconstruction, not a substitute for WORKER-2's own); post-demotion arithmetic 55 rows / 53 sites confirmed;
  0/7 v2-holdout rows marked; no disposition key exists in the adjudication schema; 20.15a 6/7 and 20.15b 5/7.
- Instrument v3.3: **256 rows · PASS 205 · FAIL 27 · INFO 22 · PROXY 2**, `--selftest` 18/18. Item 13 previously had
  **no FAIL row of its own**, so the claim "the FAIL set equals the open items" was incomplete — corrected.
- Defects #26 and **#27 (process)** published: `str.replace`-based document edits silently no-op, so `status.md` and
  `ORCH-STATE.md` missed this cycle's entries until appended; every doc edit is now asserted.
- No verdict moves. Fleet: BOSS-2 `67a4f0e` zero controls; WORKER-2 `4fc40c8` static — no ORCH-2 action per
  ERRATA-25f. Queue priority re-published in `fleet/queue/TASK-MAP.md`.
