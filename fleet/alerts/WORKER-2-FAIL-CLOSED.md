# ALERT — WORKER-2 boot FAIL-CLOSED · registry record does not verify (A-2026-09-25-001)

**Headline:** WORKER-2 boot FAIL-CLOSED — `fleet2/activations/REGISTRY.md` @ main
`2ed0b9b` (`758c65cf`sha) fails the byte-exact record check: line 4 `nonce_hash`
differs from the boot prompt's text; no anchor, no hash chain; owner's own
`fleet2check verify-activation` rejects the registry (CHAIN-BREAK, rc=1). No mission
work started; M5-R not begun.

**Class:** activation/registry integrity (LAW §1A, §1.3) + nonce custody (§1A).
**Severity:** blocking (mission cannot start under this instrument).
**Non-suppressible:** yes (LAW §6 — worker may raise directly to owner).
**Filed:** 2026-09-25T18:26Z by WORKER-2 on lane `arena/01a0d9ce-fleetyard`.

## Sober payload

1. **Record mismatch.** Verified at main `2ed0b9bb736e338af00adaf2157781b02d27b540`,
   registry file bytes sha256 `758c65cf9baa14d30f3b6b509c374702385eadd7317d169642bba8f27967a154`.
   Boot prompt record A-2026-09-25-001 vs main: **6 lines, 5 identical, 1 differs** —
   line 4, `nonce_hash`: prompt says `UNHASHED-OWNER-CHAT-ONLY`; main carries a
   16-character nonce-shaped literal (its sha256 begins `44b40796dde8d8bb…` — the
   literal is not reprinted here to avoid repeating the leak).
2. **Nonce in clear / wrong type.** §1A: the registry carries `sha256(nonce)`, never
   the nonce in clear. A 16-char literal is not a sha256. If it is a live nonce, it
   is compromised by the deployment and must be retired and re-issued. I did not
   compare it to my own nonce (custody: no printing, no hashing at boot).
3. **No anchor / no chain.** §1A requires records with `prev-hash` and a boot ANCHOR
   (sha256 of the record). Neither exists in the deployed file or the boot prompt.
   The file was also rewritten in place by an owner commit titled "Update nonce_hash
   values…", against "append-only, never rewrite".
4. **Fleet's own checker rejects it.** `fleet2check/fleet2check.py` (30/30 selftest
   green) run against the fetched registry: `verify-activation` → CHAIN-BREAK
   (`content outside a record block`), rc=1; `active-role` → rc=1. The deployed
   registry is not in the §11 governed-record shape at all.
5. **Manifest gap.** Policy files verify 8/9 against `fleet2/POLICY-MANIFEST.sha256`
   (manifest itself hashes to the pinned `0fe20a6057ec9fa2…`). The one mismatch:
   manifest `30-INSTRUMENT-FIXES.md` = `4b65145dbb8e9849…` vs deployed
   `fleet/ERRATA-2026-09-25c.md` = `7384a60878a2185f…`.
6. **Effects.** LAW §1.3 fail-closed: no new work, nothing certified, heartbeat
   "fail-closed: registry unavailable". Read-only diagnosis and durable recovery were
   performed and are reported in `fleet/branches/WORKER-2-BOOT-VERIFICATION.md`
   (fetch shas, digests, corpus reproduction, inherited-evidence byte check
   1,334/1,334, D-4/D-7 drills).
7. **Ask.** Owner: correct the instrument on main per §1A/§11 (or re-issue the boot
   with the exact main text + ANCHOR), or direct ordinary work by live chat
   (D-tier) — I then proceed to M5-R. Absent any of these I stay fail-closed at
   300 s cadence. Full options: §9 of the verification record.

No webhook credentials held; this alert publishes as a lane commit (LAW §10).
