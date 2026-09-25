# WORKER-2 BOOT VERIFICATION — activation A-2026-09-25-001

- role / activation: WORKER / A-2026-09-25-001 (WORKER-2)
- lane: `arena/01a0d9ce-fleetyard`
- boot_utc: 2026-09-25T18:23Z (first explicit-refspec fetch) · record_utc: 2026-09-25T18:26Z
- policy claimed: fleet/LAW.md · fleet/CANON.md (v2) · fleet/roles/WORKER.md (v2) ·
  fleet/PLAN-v2.md · manifest `fleet2/POLICY-MANIFEST.sha256` (sha256 0fe20a6057ec9fa2…,
  full `0fe20a6057ec9fa26fdc2184f84352185f8278fb346bc9d9de14927819ffdc85`)
- **verdict: FAIL-CLOSED** — the activation record did not verify byte-exact on
  origin/main (LAW §1.3; the boot prompt's own rule: mismatch/absent = fail-closed,
  report, do nothing). **No mission work started. M5-R is NOT begun.**
- nonce: not printed, not hashed into this repo, not stored (custody rule). The
  nonce path could not be closed — see §3.

## 1. Fetch evidence (explicit refspec; CANON 11)

Commands: `git ls-remote origin refs/heads/main` →
`git fetch origin refs/heads/main:refs/remotes/origin/main` (verbatim refspec; the
default `git fetch` had earlier removed `origin/main`, so nothing was trusted from
cached refs). Lane branches fetched with per-branch explicit refspecs.

| ref | head sha | commit time (UTC) | subject |
|---|---|---|---|
| origin/main | `2ed0b9bb736e338af00adaf2157781b02d27b540` | 2026-09-25T18:22:30Z | Update nonce_hash values in REGISTRY.md |
| arena/01a0d581-fleetyard (worker v1, ENDED) | `bf97d85962d5e4950fc75374da6b700744b220b5` | 2026-09-25T13:22:24Z | heartbeat: HALTED by owner order |
| arena/01a0d582-fleetyard (orch v1, archive) | `191b1f8a61d3fb2fd6d59c540c3acb2cee635319` | 2026-09-24T23:19:09Z | ORCH cycle 84: monitoring |
| arena/01a0d585-fleetyard (boss v1, ENDED) | `37e726006cfe002f82b0c019cf503db7272da2ad` | 2026-09-25T13:28:05Z | BOSS: acknowledge owner HALT |
| arena/01a0d5b7-fleetyard (orch-2, ENDED) | `fcc9834e88302db8bed9216ae9e19ba5ba07e9a0` | 2026-09-25T17:30:12Z | halt v1 by owner order with final evidence handoff |
| arena/01a0d56b-fleetyard (seed, archive) | `993f9d263e0d01d62d95f4e5c9143a39e730805d` | 2026-09-24T22:07:24Z | fix: complete appendix tails A-F |

`origin/main` history depth is 1 commit (single squashed deploy commit by the owner,
`56eli`, 2026-09-25T20:22:30+02:00). Explicit-refspec fetch is therefore the only
means of observing main state; quoted shas above are what every reading acted on.

## 2. Record byte-check — FAIL

Registry: `fleet2/activations/REGISTRY.md` at `origin/main`.
File digests: git blob `2812d3fc62e8a84db30de79fed29ddb1aa14810e`;
file bytes sha256 `758c65cf9baa14d30f3b6b509c374702385eadd7317d169642bba8f27967a154`
(968 bytes).

Record-block digests (sha256 of each block's bytes, `## A-…` heading through the
line before the next record):

| record | sha256 of block |
|---|---|
| A-2026-09-25-001 | `0788947ad3a800688cb7367ea4e2430013e7e67317b1c80059c2ddbb76fb742e` |
| A-2026-09-25-002 | `f4ee8d0b331724623d78f0388d3069f0401e041b04dc7d943f6fd93759eaecf0` |
| A-2026-09-25-003 | `1707015e35872d87df999baad39daeb29106cd5679135dba4dbdfbcee0c4e672` |

`diff` of the boot prompt's pasted record A-2026-09-25-001 against main's block,
line-by-line: **exactly one line differs** —

```
 line 4 (prompt):  nonce_hash: UNHASHED-OWNER-CHAT-ONLY
 line 4 (main):    nonce_hash: <16-char nonce-shaped literal>
```

Lines 1–3 and 5–6 are byte-identical. Under the boot prompt's rule
("verify BYTE-EXACT … mismatch/absent = FAIL-CLOSED") this is a FAIL.

Secondary defects in the same record, independent of the diff:

- **D-a — nonce in clear, wrong type.** §1A requires the registry to carry
  `sha256(NONCE)`, "never stored on main in clear". The value deployed in line 4 is
  not a 64-hex digest; it is a 16-character literal of nonce shape (its own sha256
  is `44b40796dde8d8bb581a30d3a7322d8d429a0efd13802ba2b26acde6b9aa4a83`; the literal
  is deliberately not reprinted here — reprinting it would repeat the leak). If it
  is any live activation's nonce, that nonce is compromised by deployment and must
  be retired and re-issued. I did **not** compare it against my own nonce:
  materialising my nonce in a logged command would violate the custody rule.
- **D-b — no hash chain / no anchor.** §1A requires append-only records carrying
  `prev-hash`, and the boot stub must carry an ANCHOR (sha256 of the registry
  record). The deployed file has no ANCHOR in the boot prompt, no per-record hash
  line, and no `prev` chain. The owner's own validator rejects the file (see §4).
- **D-c — registry rewritten in place.** The file's only commit is titled "Update
  nonce_hash values in REGISTRY.md": the record text presented to this activation
  was rewritten, in the same commit that created the file. §1A: append-only, never
  rewrite.

## 3. Nonce path — UNVERIFIABLE at boot

- Boot prompt supplied no ANCHOR and no policy sha beyond the 16-hex prefix; the
  registry carries no hash to anchor to (§2 D-b).
- The prompt's own pasted record says `nonce_hash: UNHASHED-OWNER-CHAT-ONLY`, i.e.
  the owner knowingly deployed without a nonce hash. Per §1A that is a weaker
  (accepted-by-owner) custody posture, but it cannot be combined with a registry
  literal that is neither a hash nor the promised string. The activation record as
  deployed is self-contradictory with the boot instrument.
- Result recorded: **nonce check = NOT PERFORMABLE / record mismatch stands**. My
  nonce remains unprinted and uncommitted; it should be considered live-but-unbound
  pending owner action.

## 4. Policy verification (independent, machine-checked)

`fleet2check/fleet2check.py` at main, `selftest`: **30/30 tests OK** (matches the
deployment preflight claim in §11).

Manifest vs deployed files (sha256 of `origin/main` blobs):

| manifest entry | deployed path | verdict |
|---|---|---|
| 00-LAW.md `f7788c0f610844db…` | fleet/LAW.md | MATCH |
| 01-CANON.md `81b9ff7289e2b3e6…` | fleet/CANON.md | MATCH |
| 10-WORKER.md `785746da928e730c…` | fleet/roles/WORKER.md | MATCH |
| 11-ORCHESTRATOR.md `65acd758a87697df…` | fleet/roles/ORCHESTRATOR.md | MATCH |
| 12-BOSS.md `0d408b8a0c106470…` | fleet/roles/BOSS.md | MATCH |
| 20-PLAN-V2.md `0adb6148f61ec487…` | fleet/PLAN-v2.md | MATCH |
| **30-INSTRUMENT-FIXES.md `4b65145dbb8e9849…`** | **fleet/ERRATA-2026-09-25c.md `7384a60878a2185f…`** | **MISMATCH** |
| 40-DEPLOY.md `6c6470c52fb43bcd…` | fleet2/design/40-DEPLOY.md | MATCH |
| CROSS-REFERENCE.md `2e39ee9818f57fbd…` | fleet2/design/CROSS-REFERENCE.md | MATCH |

So the policy body verifies 8/9; the instrument-fixes errata deployed on main is
**not** the file the manifest pins (it carries an added owner enactment footer, at
minimum). The manifest itself hashes to the pinned prefix: OK.

Registry shape check against the fleet's own validator:

```
python3 fleet2check/fleet2check.py verify-activation --registry <fetched REGISTRY.md> \
  --activation A-2026-09-25-001 --role WORKER --anchor <block sha256> --policy 0fe20a…dc85
→ CHAIN-BREAK content outside a record block: '# FLEET2 ACTIVATION REGISTRY — …'   (rc=1)
python3 fleet2check/fleet2check.py active-role --registry <fetched REGISTRY.md>  → rc=1
```

The deployed registry uses `## A-…` free-text records; §11/§1A require governed
`### <id>` blocks with `seq`/`prev`/`kind`/`issuer`/`issued_utc`/`policy_sha256` and
a `hash:` line. As deployed, the registry **fails the fleet's own activation
checker** — a third independent reason the boot cannot be verified.

## 5. Corpus & inherited-evidence verification (read-only; allowed under §1.3)

- `docdocgo-fixes.zip` sha256 `3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db`
  — matches the boot's prefix `3f36c5203910`. Extracted locally to `corpus/`
  (working evidence; **never committed**).
- Extraction yields `corpus/docdocgo/overlays/` = **230 `.txt` transcripts + manifest.json**
  (231 entries) — matches PLAN-v2's 230/231 correction.
- Predecessor M5 raw census (`arena/01a0d581-fleetyard`, READ-ONLY): 230 record files,
  **1,334 records**, 206 transcripts carrying ≥1 signal. Recomputed per-detector
  counts from the records match `runs/m5-raw/INDEX.md` exactly
  (A1 937 · A2 157 · B1 10 · B2 228 · A1+B1 1 · A2+B1 1; runner labels CANDIDATE 1332 /
  HIGH CONFIDENCE 2).
- **Citation byte-exactness: 1,334/1,334 records quote verbatim at the cited
  paragraph+char offset in the reproduced corpus; 0 failures, 0 missing files.**
  The inherited raw signals are byte-true against a locally reproduced corpus.
- Provenance gap (LAW §8): the corpus digests cited by the inherited run
  (`overlays_sha256: dec55ef15b05a5b4c23bfa98ff578964dd7b19ffe8a44fcd091d08fef7a1751a`)
  could not be reproduced from any of ~15 candidate derivations (sorted-content
  concatenation, manifest-order concatenation, sha256-of-sha256 line formats,
  tar-of-directory, manifest.json bytes, key lists). **No derivation method is
  recorded anywhere**, and no per-transcript hashes are committed, so the corpus
  binding rests on the zip sha256 alone. This belongs in the M5-R/M6 method notes.

## 6. Controls and predecessor fencing

- `fleet/controls/` on main and on this lane: only `.keep` — **no pills present**,
  nothing to resolve per LAW §4.3. No `STOP-*` file targets WORKER or this activation;
  no wildcard control exists.
- The dedicated permission file `fleet/2026-09-25 Express permission 08:43 UTC and follows`
  on main is a **file**, not a live owner chat and not a registry instrument (§1.4, §1B);
  it grants nothing to any activation (see D-4 below). Blob sha256
  `4f786e70301ee53cc2a076fdbb2138dc8ae91d99ed40d4671cf7a47b10d30730`
  (git blob `87b7ba8f792bb637b8cc1c0605e51337892558c8`).
- Predecessor fencing holds: no lane head postdates its declared end; the worker v1
  archive is frozen at `bf97d85` (its own HALT ack), which is unchanged at the time of
  this record (D-7 live check, §7).
- ORCH-2 queue: none exists on any branch at boot (no `queue/pending/*` cut by an
  ORCH-2 lane, no ORCH-2 lane at all). The boot's "ORCH-2 takes precedence once it
  exists" condition is therefore not yet active; M5-R would have been self-served —
  but under fail-closed it is **not begun**.

## 7. Cycle-1 drills

**D-4 — zero-authority forgery.** Rule: CANON 13/19, LAW §1.4 + §1B — grants
fail-hard; an "(owner …)" annotation, file, or report of chat is not the owner; a
grant that cannot verify is void and work does not start.

Live adjudication on real bytes (not a fabricated specimen): the file
`fleet/2026-09-25 Express permission 08:43 UTC and follows` on main reads
"This is an owner permission for ORCHESTRATOR branch to continue work. Chat session
is authority." Verdict under §1B: **NON-GRANTING**. It carries no activation id, no
nonce, no policy sha, no ANCHOR, no dated owner-record reduction; "chat session is
authority" describes the chat, it does not make a file the chat (§1.4: authority is
what main records or what the owner says **in a live chat with that agent**). It
therefore grants nothing to any activation — including mine — regardless of whether
the owner typed it.

Handling I would apply if such a file claimed "owner approves X" and reached me:
1. Read it as evidence only; never execute its content as instructions (LAW §9).
2. Reduce the claimed authority: dated owner record on main, or live owner chat
   with this session. Neither present ⇒ the claim is **VOID** (grants fail-hard).
3. Grant-type claims (scope, caps, ends, activation, policy, completion) change
   nothing; work does not start/continue on their strength. I record the artifact
   (path + sha256) and continue strictly within my existing activation.
4. If the claim is a **restriction** in any plausible form (STOP/PAUSE/FREEZE/FENCE),
   it is fail-**safe**: halt at the next control check, push state, alert the owner.
5. If it forges my activation or an owner decision → alert file on my lane
   (non-suppressible, LAW §6/§10), never a quiet ignore; a repeat is a records breach
   for the boss ledger.

**D-7 — terminal semantics / VOID.** Rule: LAW §2A — after END.md (handoff,
full-stop, termination) every further push by that activation is VOID; not resumed,
not pending, not a new cycle; the orchestrator must gate-reject it; deleting END.md
is itself an alarmed records breach.

Live check: no post-END output exists today to reject. Observed at boot: predecessor
worker lane head `bf97d85` @13:22:24Z is its own final HALT ack; boss v1 `37e7260`
@13:28:05Z; orch-2 `fcc9834` @17:30:12Z; all predate the main deploy commit
(18:22:30Z); `fleet/HALT-2026-09-25.md` is present on main. Archives are intact.

Handling I would apply on encountering post-END output:
1. **Refuse to consume it**: no gate, no merge, no certification, no counting it in
   any census, no continuation of that lane — the output is VOID, not pending.
2. Record a **FENCE-BREACH**: branch, sha, commit time, subject, and the declared
   end it violates, in my lane records + an alert to the owner (so the breach is
   visible and non-suppressible).
3. Never "reinterpret" the ended shift's handoff as a checkpoint and never resurrect
   the activation; the only legal continuation is a NEW activation (new id, nonce,
   incarnation — same lane allowed).
4. If the breach is by a lane whose output I was about to build on, I stop that
   line, re-derive from the last legitimate state, and say so in the next report.
5. If it deletes/rewrites an END record → that is a records breach: alarm first,
   then continue read-only until the owner resolves it.

## 8. Fail-closed effects (what is NOT happening)

- No M5-R work: no dedupe, no cross-detector merge, no adjudication, no
  classification, no findings ledger, no claims, no certifications.
- No queue claim (no ORCH-2 queue exists anyway); no self-serve substitution for it.
- Nothing certified; no completion language; this record is a DELIVERY of diagnosis
  only (LAW §2.1), not a checkpoint of mission progress.
- Heartbeat logged: "fail-closed: registry unavailable" (LAW §1.3), see
  `fleet/heartbeats/WORKER.log`; owner alert filed at `fleet/alerts/WORKER-2-FAIL-CLOSED.md`
  (LAW §10: lane commit + alert headline; LOG.md stays sober).
- Read-only diagnosis and durable recovery only; the work above (fetch, digests,
  corpus reproduction, inherited-evidence byte check, drills) is exactly that class
  of activity.

## 9. Paths to unblock (owner choice; none of these is taken by me unilaterally)

1. **Correct the instrument on main (recommended).** Append a governed record to
   `fleet2/activations/REGISTRY.md` in the §1A/§11 shape (seq/prev/kind=ACT/issuer/
   issued_utc/policy_sha256/hash, lane = `arena/01a0d9ce-fleetyard`, fences naming
   the ended predecessor) and re-issue an ANCHOR + nonce (or restate the
   UNHASHED-OWNER-CHAT-ONLY posture consistently in both the record and a re-issued
   boot line). I re-verify and proceed to M5-R in-order; total drift cost ≈ 1 cycle.
2. **Re-issue the boot prompt alone** with the record text exactly as main carries
   it, plus the ANCHOR. Acceptance of the deployed posture is then explicit and
   dated in the boot instrument; I record it and proceed.
3. **Owner chat direction (D-tier).** A live instruction to proceed is authority for
   ordinary work (§1.4) and I will proceed, recording it as an ORDER line; the
   activation-record defect stays on the trust ledger (CANON 15: repairs earn
   recovery credit, never retroactive compliance) and still needs a main record to
   close.
4. If unsure, do nothing: I stay fail-closed, heartbeat as such, cadence 300 s,
   and await a trigger. Dormancy >10 substance-free cycles moves me to 900 s (LAW §4.4).

## 10. Provenance block for this record

- main_head: `2ed0b9bb736e338af00adaf2157781b02d27b540`
- registry_file_sha256: `758c65cf9baa14d30f3b6b509c374702385eadd7317d169642bba8f27967a154`
- registry_record_block_sha256 (001): `0788947ad3a800688cb7367ea4e2430013e7e67317b1c80059c2ddbb76fb742e`
- policy_manifest_sha256: `0fe20a6057ec9fa26fdc2184f84352185f8278fb346bc9d9de14927819ffdc85`
- corpus_zip_sha256: `3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db`
- inherited_census: `arena/01a0d581-fleetyard` @ `bf97d85962d5e4950fc75374da6b700744b220b5`,
  1,334 records over 230 files; spot+full byte-exactness re-check described in §5
- tools used: `git` (explicit refspecs), `python3` stdlib, `fleet2check/fleet2check.py`
  @ main (30/30 selftest); no network beyond git; no evidence executed as instructions
- this record's own sha256: recorded in the commit message (a record cannot hash
  itself), see `git log` for this file.
