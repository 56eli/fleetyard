# ALERTS — sober ledger (append-only)

Per owner ruling 2026-09-25: the alert **headline** carries the Jameson voice and is the text
delivered to the owner's Discord by the repo-level GitHub→Discord webhook. This file and the
commit **body** carry the sober payload: class, minutes, shas, next action. `fleet/LOG.md`
stays sober. Worker and orchestrator work commits stay dry.

Dedup rule in force: max one alert per class per 20 minutes.

---

## 2026-09-25T18:32Z — CLASS ACTIVATION / REGISTRY INTEGRITY + NONCE CUSTODY + MAIN-MOVED

- class: activation / registry integrity (LAW §1A, §1.3) + nonce custody (§1A) + MAIN-MOVED (§1A)
- role / activation: BOSS / A-2026-09-25-003 (BOSS-2)
- lane: `arena/01a0d9d1-fleetyard`
- head at alert: `ca03d711a33d2b8d2cb6aa7265a4854df731b918`
- severity: blocking for gating/certification/declarations; advisory for D-tier record-keeping
- non-suppressible: yes (LAW §1A chain-break / MAIN-MOVED alarm, LAW §6)
- measurement timestamp: 2026-09-25T18:32Z

### Sober payload summary
1. **Record mismatch.** Line 4 of 6 in `fleet2/activations/REGISTRY.md` block `## A-2026-09-25-003` differs from the boot instrument (`nonce_hash: UNHASHED-OWNER-CHAT-ONLY` vs a 16-character nonce-shaped literal on main). Lines 1–3 and 5–6 are byte-identical. Fails the byte-exact check (LAW §1.3).
2. **URGENT — Public nonce exposure.** Repo is public (`gh api repos/56eli/fleetyard` -> `private: false, visibility: public`). Three 16-character nonce-shaped literals are world-readable on main in `fleet2/activations/REGISTRY.md`. §1A requires `sha256(nonce)` on main, never cleartext. If these are live nonces, they are compromised and must be retired and re-issued immediately.
3. **No anchor / no chain.** Registry lacks `seq`, `prev-hash`, and per-record `hash:` lines required by §1A. Boot prompt lacked an ANCHOR.
4. **Checker failure.** Shipped validator `fleet2check/fleet2check.py` (30/30 selftest green) rejects the registry with `CHAIN-BREAK` (rc=1) for all subcommands.
5. **MAIN-MOVED.** Main advanced during boot from `2ed0b9b` to `ca03d71` (+ `fleet/controls/owner-hash-clarification`). Adjudicated as genuine owner D-tier direction ("Continue work as planned anyway"), but cannot cure the G-tier verification defect (§1B).
6. **ORCH-2 missing.** Activation A-2026-09-25-002 exists on paper with `lane: TBD`, but has no remote branch on origin. Cycle-1 drills for ORCH-2 cannot be witnessed.
7. **Manifest gap.** 8 of 9 files match `fleet2/POLICY-MANIFEST.sha256`; `30-INSTRUMENT-FIXES.md` does not match deployed `fleet/ERRATA-2026-09-25c.md`.
8. **Corroboration.** WORKER-2 on `arena/01a0d9ce-fleetyard` reached the identical FAIL-CLOSED verdict on A-2026-09-25-001 and filed `fleet/alerts/WORKER-2-FAIL-CLOSED.md`.
9. **Next action:** Owner retires and re-issues nonces, appends governed §1A records to REGISTRY.md, and boots ORCH-2. BOSS-2 operates fail-closed: records kept, nothing certified.

---

## 2026-09-25T18:48Z — RESOLUTION — OWNER RULING 25d RE-GROUNDED

- class: activation / registry integrity (RESOLUTION)
- role / activation: BOSS / A-2026-09-25-003 (BOSS-2)
- lane: `arena/01a0d9d1-fleetyard`
- head at resolution: `25bdab98200074ea89c22944188e948d8b748be2`
- status: RESOLVED by owner commit `fleet/ERRATA-2026-09-25d.md` on main.
- payload:
  1. Main churn 20:12–20:33Z confirmed as disclosed owner acts (§1).
  2. Registry rewrite confirmed as disclosed owner exception; registry frozen until 2.0.1 (§6).
  3. Verification standard defined as normalized equality (§3); 6/6 record lines match.
  4. Activations confirmed in force (§5); mission resume ordered (§7).
  5. Sibling status: WORKER-2 delivered M5-R at 8011439 and re-grounded on 25d at 341ee2e; ORCH-2 lane registered at 574f499.
  6. BOSS-2 active, tracking PLAN-v2 manifest, stall-watch classes 1–6 armed.

---

## 2026-09-25T19:43Z — CLASS 2 — ORCHESTRATOR SILENT

- class: (2) orchestrator silent
- quiet: **37 minutes** (threshold: 20 min)
- orchestrator lane: `arena/01a0d9d0-fleetyard`
- orchestrator head: `8ed8d122cd8ee32f9bbeb426c4d377d03653382d` @ 2026-09-25T19:05:36Z
- last heartbeat line: 2026-09-25T19:06Z
- measurement timestamp: 2026-09-25T19:43:00Z
- status: FIRED. WORKER-2 delivered repair TASK-016 at `1beadd9` while held under scoped brake `PAUSE-WORKER-A-2026-09-25-001`. Gates, queue, and pause-removal are DOWN.
- action: Order `fleet/ORDERS/REDIRECT-008.md` issued targeting `ORCHESTRATOR@A-2026-09-25-002`; ack due in 900 s (by 2026-09-25T19:58:00Z).
