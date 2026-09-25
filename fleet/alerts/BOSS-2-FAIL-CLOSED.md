# ALERT — BOSS-2 boot FAIL-CLOSED · activation record does not verify (A-2026-09-25-003)

**Headline:** (JJJ voice lives in the commit headline per LAW §10; this file is
the sober payload.)

**Class:** activation / registry integrity (LAW §1A, §1.3) + nonce custody (§1A)
+ MAIN-MOVED (§1A).
**Severity:** blocking for anything that certifies, gates or declares. Advisory
only for ordinary D-tier record-keeping, which the owner has directed to continue.
**Non-suppressible:** yes — §1A chain-break / MAIN-MOVED alarm and §6.
**Filed:** 2026-09-25T18:32Z by BOSS-2, activation A-2026-09-25-003, lane
`arena/01a0d9d1-fleetyard`.
**Measurement time:** 2026-09-25T18:32Z (fetch re-taken immediately before
commit, so a reader can price staleness — the v1 boss's own recorded lesson).

## Sober payload

1. **Record mismatch — 5 of 6 lines byte-exact, 1 differs.** Registry
   `fleet2/activations/REGISTRY.md` at `origin/main`
   (`ca03d711a33d2b8d2cb6aa7265a4854df731b918`), git blob
   `2812d3fc62e8a84db30de79fed29ddb1aa14810e`, file bytes sha256
   `758c65cf9baa14d30f3b6b509c374702385eadd7317d169642bba8f27967a154`.
   Block `## A-2026-09-25-003` sha256
   `1707015e35872d87df999baad39daeb29106cd5679135dba4dbdfbcee0c4e672`.
   Lines 1–3 and 5–6 are byte-identical to the boot instrument. **Line 4
   `nonce_hash` differs**: the boot instrument says `UNHASHED-OWNER-CHAT-ONLY`;
   main carries a 16-character nonce-shaped literal. Under the boot prompt's own
   rule ("verify BYTE-EXACT … mismatch/absent = FAIL-CLOSED") this is a FAIL.
   The literal is deliberately **not** reprinted in this lane and its digest is
   deliberately **not** computed by BOSS — reprinting or hashing it into a
   committed artifact would repeat and widen the exposure described in (2).
2. **URGENT — nonce custody: three activation nonces appear to be published in
   clear on a PUBLIC repository.** `gh api repos/56eli/fleetyard` returns
   `private: false, visibility: public`. §1A requires the registry to carry
   `sha256(nonce)` and states the nonce is "never stored on main in clear". The
   deployed line-4 values for **all three** FLEET2 activations
   (A-2026-09-25-001 WORKER-2, -002 ORCH-2, -003 BOSS-2) are 16-character
   nonce-shaped literals, not 64-hex digests, and they are world-readable at the
   raw file URL. If any of them is a live activation nonce, that nonce is
   compromised by the deployment and must be **retired and re-issued** — a
   holder of it can forge a boot stub for that activation. BOSS cannot confirm
   or deny that they are live without hashing its own nonce, which it will not
   do; the owner can settle it in one look. This is the finding that should be
   actioned first.
3. **No anchor, no chain.** §1A requires append-only records carrying
   `prev-hash` plus a boot ANCHOR (sha256 of the registry record). The deployed
   file has no per-record `hash:` line, no `prev`, no `seq`, and the boot
   instrument carries no ANCHOR. The file's entire history is one owner commit
   ("Update nonce_hash values in REGISTRY.md") that created and wrote it in the
   same act, against §1A's "append-only; never rewrite".
4. **The fleet's own validator rejects the registry.** Preflight satisfied
   first: `fleet2check/fleet2check.py selftest` → **30/30 tests OK** (the §11
   deployment preflight). Run against the fetched registry:
   `verify-activation`, `active-role` and `controls` each return
   `CHAIN-BREAK content outside a record block: '# FLEET2 ACTIVATION REGISTRY — …'`
   with rc=1. The deployed file uses `## A-…` free-text records; §11/§1A require
   governed `### <id>` blocks with `seq`/`prev`/`kind`/`issuer`/`issued_utc`/
   `policy_sha256`/`nonce_sha256`/`fences` and a `hash:` line. **No activation in
   this registry can be verified by the shipped checker — not BOSS-2, not
   WORKER-2, not ORCH-2.** This is independent of the line-4 diff.
5. **MAIN-MOVED — main advanced during this boot.** First fetch
   (18:29Z) read `origin/main` = `2ed0b9b`; the current head is
   `ca03d711a33d2b8d2cb6aa7265a4854df731b918` (owner `56eli`, 18:29:30Z,
   "Clarify owner hash documentation update"). Diff is exactly one added file,
   `fleet/controls/owner-hash-clarification`; registry blob, policy manifest and
   all eight deployed policy files are byte-unchanged. The move is therefore
   explained by a genuine owner commit and is **not** itself the alarm — the
   chain-break limb of §1A is.
6. **The owner's clarification, as adjudicated.** The new file reads:
   "I only dropped WORKER, ORCHESTRATOR and BOSS hashes into
   fleet2/43-BOOT-STUBS.md, not into your initialization prompts. That was an
   accident. Continue work as planned anyway." BOSS's adjudication:
   - It is owner-authored on main, so it is an owner record under §1.4 (it is
     not an agent-authored owner-named artifact). BOSS honours it.
   - "Continue work as planned anyway" is **D-tier direction**: it directs
     ordinary work inside the running activation's scope. BOSS has therefore
     performed the cycle-1 record-keeping duties (baseline LOG, completion-manifest
     tracking, stall-watch arming, drill witnessing as observation).
   - It **cannot repair the G-tier defect**. §1B: D "can never change ends,
     scopes, policy, or activations"; a grant that cannot verify is void and
     work does not start. The activation stays **UNVERIFIED** and BOSS certifies,
     gates and declares nothing.
   - Its factual claim does not check out. `fleet2/43-BOOT-STUBS.md` **does not
     exist** anywhere on main — the full `fleet2/` tree is 8 files
     (`POLICY-MANIFEST.sha256`, `activations/REGISTRY.md`, `design/40-DEPLOY.md`,
     `design/41-HALT-STUBS.md`, `design/42-NEXT-STEPS.md`,
     `design/CROSS-REFERENCE.md`, `fleet2check/fleet2check.py`,
     `fleet2check/test_fleet2check.py`). And what it calls "hashes" are not
     digests — see (2).
   - It is not a well-formed control either: it sits in `fleet/controls/`
     without the `target + date + reason` that §4.3 requires, and it is a
     relaxation with no `nonce_sha256`, which the shipped checker requires for
     relaxing controls. BOSS treats it as an owner note, which is how BOSS has
     used it, and records the shape defect without contesting the instruction.
7. **ORCH-2 has no lane at all.** Activation A-2026-09-25-002 (ORCH-2) is live
   in the registry with `lane: TBD`. No lane for it exists on `origin`
   (`git ls-remote` shows only `56eli-patch-1`, the five v1 archive lanes,
   WORKER-2's `arena/01a0d9ce-fleetyard`, and `main`). Consequences: no
   heartbeat, no queue, no gates, and **cycle-1 drill witnessing for the
   orchestrator has no subject** — see the stall-watch table in §9 of the
   verification record. Also noted: LAW §2A's `END.md` marker does not exist on
   any lane, so D-7 has no `END.md` to reject; the v1 lanes ended by halt
   commits instead.
8. **Policy manifest: 8 of 9 files verify.** Manifest sha256
   `0fe20a6057ec9fa26fdc2184f84352185f8278fb346bc9d9de14927819ffdc85` matches
   the pinned `0fe20a6057ec9fa2` prefix. Deployed files matching their pinned
   digest: `fleet/LAW.md`, `fleet/CANON.md`, `fleet/roles/WORKER.md`,
   `fleet/roles/ORCHESTRATOR.md`, `fleet/roles/BOSS.md`, `fleet/PLAN-v2.md`,
   `fleet2/design/40-DEPLOY.md`, `fleet2/design/CROSS-REFERENCE.md`. The ninth
   entry, `30-INSTRUMENT-FIXES.md` = `4b65145dbb8e9849…`, has **no deployed
   file**: the closest candidate `fleet/ERRATA-2026-09-25c.md` hashes to
   `7384a60878a2185f…` and does not match. So the enacted instrument-fixes text
   is not bound by the manifest it is supposed to be pinned by.
9. **Independent corroboration.** WORKER-2, booting separately on lane
   `arena/01a0d9ce-fleetyard`, reached the identical verdict on its own record
   A-2026-09-25-001 at main `2ed0b9b` and filed
   `fleet/alerts/WORKER-2-FAIL-CLOSED.md`. Two independent agents, same defect:
   this is systemic to the instrument, not a per-role misreading.
10. **One piece of good news, verified.** The §1A / 40-DEPLOY Phase D-a T2 layer
    is in place: ruleset `fleet2-policy` (id 24011125) is `active` on the
    default branch with `deletion`, `non_fast_forward` and `pull_request` rules.
    Force-push to main is blocked and main cannot be deleted. That protection is
    real and working.
11. **Effects.** LAW §1.3 fail-closed: no new mission work, **nothing
    certified**, no gate verdicts, no completion language, no REDIRECT issued
    with an acknowledgement deadline, no M-item statuses changed by BOSS.
    Read-only diagnosis and durable recovery performed and recorded in
    `fleet/branches/BOSS-2-BOOT-VERIFICATION.md`. Heartbeat
    "fail-closed: registry unavailable" logged in `fleet/heartbeats/BOSS.log`;
    control checks in `fleet/CONTROL.log`.
12. **Ask (owner's choice; BOSS takes none of these unilaterally).**
    - **(a) Retire and re-issue the three nonces**, and replace the line-4
      literals with real `sha256(nonce)` values. Highest priority — the repo is
      public. Do not paste new nonces into any file that lands on main.
    - **(b) Append governed records** to `fleet2/activations/REGISTRY.md` in the
      §1A/§11 shape (`seq`/`prev`/`kind: ACT`/`issuer`/`issued_utc`/
      `policy_sha256`/`nonce_sha256`/`role`/`lane`/`incarnation`/`fences` +
      `hash:`), so the shipped checker can return `VERDICT: OK`. BOSS has drafted
      the exact text for A-2026-09-25-003 in §11 of the verification record for
      the owner to paste; BOSS does not write main.
    - **(c) Boot or retire ORCH-2** — it is activated on paper with no lane, no
      heartbeat and no queue, which stalls M6-P/M5-R tasking behind it.
    - **(d) Deploy `30-INSTRUMENT-FIXES.md`** byte-exact, or correct the manifest.
    BOSS stays fail-closed at 300 s control cadence and 900 s cycle cadence, and
    will re-verify on every fetch. Absent all of the above, BOSS continues
    owner-directed D-tier record-keeping only.

No webhook credentials are held by BOSS; this alert publishes as a lane commit
and the owner's repo-level GitHub→Discord relay delivers it (LAW §10).

---

## Resolution — 2026-09-25T18:48Z (Owner Ruling ERRATA-2026-09-25d)

Resolved by owner commit `25bdab98200074ea89c22944188e948d8b748be2` enacting `fleet/ERRATA-2026-09-25d.md`:
1. Main churn 20:12–20:33Z confirmed as disclosed owner acts (§1).
2. Registry rewrite confirmed as disclosed owner exception; registry frozen until 2.0.1 (§6).
3. Verification standard defined as normalized equality (§3); 6/6 record lines match.
4. Activations confirmed in force (§5); mission resume ordered (§7).
5. WORKER-2 delivered M5-R at `8011439` and re-grounded at `341ee2e`; ORCH-2 registered `arena/01a0d9d0-fleetyard` at `574f499`.
6. BOSS-2 active, tracking PLAN-v2 completion manifest, stall-watch classes 1–6 armed.
