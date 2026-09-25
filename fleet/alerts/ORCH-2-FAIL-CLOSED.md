# ALERT — ORCH-2 boot FAIL-CLOSED · registry record did not verify (A-2026-09-25-002) — CLOSED by owner repair

**Headline (JJJ, for the relay):** ONE LINE OFF, PARKER! ORCH-2 cold at the gate —
main's record 002 didn't match my stub (`nonce_hash` at `2ed0b9b`, then `lane:` at
`5fdd00e`; anchors `edf5fbb3` ≠ `f4ee8d0b` ≠ `2917dcee`), 0 tasks cut, 0 gates, 0
certifications, and three nonce-shaped literals sat naked in a PUBLIC repo's history —
owner repaired main (`5fdd00e`, `25bdab9` + ERRATA-25d), ORCH-2 re-verified and resumed.

- class: activation/registry integrity (LAW §1A, §1.3, §1B) + nonce custody (§1A)
- severity: was blocking (no work authority); **CLOSED 2026-09-25T18:57Z**
- non-suppressible: yes (LAW §6 — raised directly to the owner)
- filed: 2026-09-25T18:40Z by ORCH-2 on lane `arena/01a0d9d0-fleetyard`; closed 18:57Z

## Sober payload

1. **Record mismatch #1 (18:40Z, main `2ed0b9b`).** Boot-stub record A-2026-09-25-002
   vs deployed record: 6 lines, 5 identical, line 4 `nonce_hash` differs — stub
   `UNHASHED-OWNER-CHAT-ONLY`, main a 16-char nonce-shaped literal (not 64-hex, so not
   a sha256; literal not reprinted). Registry file sha256 `758c65cf…a154`; main record
   block `f4ee8d0b…ecf0`; stub record `edf5fbb3…4a97` (== main's record 002 at
   `0eda002`, 18:13:17Z — main moved after the stub was composed).
2. **Record mismatch #2 (main `5fdd00e`, 18:33:45Z).** `nonce_hash` restored to
   `UNHASHED-OWNER-CHAT-ONLY`, but line 6 was standardised: stub `lane: TBD` vs main
   `lane: TBD (agent registers at boot)`. Record block `2917dcee…c190`; registry file
   `a86115d2…5c14`. Sibling WORKER-2 (record 001) verified byte-exact PASS at this head.
3. **Nonce/anchor path not closable at boot.** The stub delivered the placeholder
   `<NONCE-2>` (no nonce value) and no ANCHOR; the deployed registry carries no
   per-record hash and no `prev` chain. `fleet2check verify-activation` → CHAIN-BREAK,
   rc=1 (`selftest` 30/30 OK).
4. **Nonce custody exposure.** The three literals published at `2ed0b9b` remain
   reachable in this public repo's history. If any was a live nonce it is burned:
   retire and re-issue before WORKER-2/BOSS-2 rely on it. Owner's
   `fleet/controls/owner-hash-clarification` says they were meant for
   `fleet2/43-BOOT-STUBS.md` — a path that does not exist on main.
5. **Effects honoured while fail-closed (LAW §1.3):** no tasks, no gates, no
   certifications, no controls, no queue writes; read-only diagnosis + durable records;
   owner alerted on push (lane commit `574f499`).

## Resolution (owner acts — accepted, not assumed)

- `ca03d71` (18:29:30Z) `fleet/controls/owner-hash-clarification`; `5fdd00e`
  (18:33:45Z) registry standardised + FORMAT v0 owner note (chain/ANCHOR mechanics
  deferred to policy 2.0.1; fleet2check chain output ADVISORY); `25bdab9` (18:44:14Z)
  `fleet/ERRATA-2026-09-25d.md` — §1 main-churn disclosure (owner acts, no force-push),
  §2 registry-rewrite exception, §3 NORMALIZED EQUALITY verification standard,
  §5 activations confirmed in force (incl. **-002 ORCH-2**), §6 registry freeze,
  §7 resume order.
- Owner live ruling in this session (18:56Z): re-ground on ERRATA-25d, activation
  confirmed in force, resume.
- ORCH-2 re-verification under §3: 4 of 5 record fields byte-equal after
  normalization; the `lane` delta resolved by §5 + §6 + §7 + live ruling (§1.4), and
  recorded — not silently absorbed. **Verdict: IN FORCE, RESUMED 18:57Z.**
- CANON 15: the episode stays on the trust ledger as a detected-and-repaired instrument
  defect. Recovery credit, never retroactive compliance.
- Full record: `fleet/branches/ORCH-2-BOOT-VERIFICATION.md`.

No webhook credentials held; this alert publishes as a lane commit (LAW §10).
