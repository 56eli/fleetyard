# ORCH-2 BOOT VERIFICATION — activation A-2026-09-25-002 (ORCHESTRATOR)

- lane: `arena/01a0d9d0-fleetyard` · role file `fleet/roles/ORCHESTRATOR.md` (v2)
- policy: `fleet/LAW.md` · `fleet/CANON.md` (v2) · `fleet/PLAN-v2.md` · manifest
  `fleet2/POLICY-MANIFEST.sha256` sha256 `0fe20a6057ec9fa26fdc2184f84352185f8278fb346bc9d9de14927819ffdc85`
  (stub quoted the prefix `0fe20a6057ec9fa2` — MATCH)
- **VERDICT: ACTIVATION IN FORCE — RESUMED** (2026-09-25T18:57Z) after an initial
  **FAIL-CLOSED** episode (18:40Z) that the owner repaired on main and ruled on live.
- nonce custody: the boot prompt carried the literal placeholder `<NONCE-2>` — no nonce
  value was ever delivered to this session. Nothing was printed, hashed or committed.
  Posture on main is `UNHASHED-OWNER-CHAT-ONLY` (owner-held nonce, chat-delivered).

## 1. Timeline (explicit-refspec observations; CANON 11)

| utc | main head | event (observed) |
|---|---|---|
| 18:25Z | `2ed0b9bb736e338af00adaf2157781b02d27b540` | session start; lane created at this base |
| 18:26–18:35Z | `2ed0b9b` | boot reads: registry, LAW/CANON/roles/PLAN-v2, manifest, fleet2check, HALT, archives (read-only API), sibling lane |
| 18:29:30Z | `ca03d71` | owner web commit: `fleet/controls/owner-hash-clarification` added |
| 18:33:45Z | `5fdd00e` | owner web commit: registry `nonce_hash` standardised to `UNHASHED-OWNER-CHAT-ONLY`, FORMAT v0 owner note added, lane lines standardised |
| 18:40Z | `5fdd00e` | ORCH-2 registration pushed (`574f499993ff1b6914693096fee1069b3aba8ff7`) with verdict FAIL-CLOSED |
| 18:44:14Z | `25bdab98200074ea89c22944188e948d8b748be2` | owner web commit: `fleet/ERRATA-2026-09-25d.md` |
| 18:57Z | `25bdab9` | owner live-chat ruling: re-ground on ERRATA-25d, activation confirmed in force, resume. Lane merged main (`91a7b4e…`), re-verified, RESUMED |

All four main commits in this window carry committer `GitHub <noreply@github.com>`
(web-UI edits under the owner account) and author `56eli`; agent lane commits on this
repo carry committer `56eli`. `ERRATA-2026-09-25d` §1 discloses all main commits
20:12–20:33Z (+02:00) as OWNER ACTS, states no force-push occurred and answers
MAIN-MOVED alarms for them; §2 discloses the registry rewrite as an owner exception.
Independent check of that claim: `git log origin/main` is linear (no merge/force
artefacts in the fetched depth-80 window) and `git merge-base --is-ancestor c29d8a9
origin/main` = YES. Accepted; no investigation owed (§1).

## 2. First verdict — FAIL-CLOSED at main `2ed0b9b` (18:40Z)

Boot-stub record A-2026-09-25-002 vs the deployed record: 6 lines, 5 identical, **1
differs** — line 4 `nonce_hash`: stub `UNHASHED-OWNER-CHAT-ONLY`, main carried a
16-character nonce-shaped literal (not reprinted here; not a 64-hex digest, so not a
sha256). Digests: stub record `edf5fbb3e5a43ba9a855dbd109d8428d8b8e49fbe927c29368ee283638734a97`;
main record block `f4ee8d0b331724623d78f0388d3069f0401e041b04dc7d943f6fd93759eaecf0`;
registry file `758c65cf9baa14d30f3b6b509c374702385eadd7317d169642bba8f27967a154`.
Triggers: the boot prompt's own rule (mismatch = FAIL-CLOSED) · LAW §1.3 (registry
conflict → no new work) · LAW §1B (activation is a Grant; grants fail-hard).
The stub's record text was byte-identical to main's record 002 at `0eda002`
(18:13:17Z) — i.e. the stub was composed against that state and main moved after.
Effects honoured: no tasks cut, no gates, no certifications, no controls, no queue
writes; read-only diagnosis + durable records only; owner alerted on push (§1.3).

## 3. Second verdict — still not byte-exact at main `5fdd00e` (18:35–18:40Z)

`nonce_hash` was restored to `UNHASHED-OWNER-CHAT-ONLY` (matching the stub) but the
lane line was standardised, so record 002 differed in **line 6**: stub `lane: TBD`,
main `lane: TBD (agent registers at boot)`. Digests: main record block
`2917dcee286035a5e265aad7d2ebd007fd80c0465b973ab0f99fde46a386c190`; registry file
`a86115d2667e7d54ff418524303c9adeca2348709d233e9e1c39480251435c14`. Sibling WORKER-2
(record 001, whose stub quoted the parenthetical) verified byte-exact PASS at this
head — the asymmetry is recorded in §8, not assumed.

## 4. Re-ground on `fleet/ERRATA-2026-09-25d.md` (main `25bdab9`) — RESUME

Errata file: git blob `834d2ea8bfec5543b81b2e3a606df29166a74f7d`, bytes sha256
`d2b75b8c1f287b09e33d4593aaec59e0f0a2a2e300876b9c6ab781418c25dc50`, 28 lines,
"Signed: owner (this commit is the signature)." Registry bytes unchanged between
`5fdd00e` and `25bdab9` (`git diff --stat` empty; file sha256 `a86115d2…` both).

**§3 NORMALIZED EQUALITY applied** (trim trailing whitespace, normalize line endings,
compare the five record fields). ORCH-2's own recomputation:

| field | stub vs main@`25bdab9` |
|---|---|
| `issued_utc` (incl. role + activation) | EQUAL |
| `policy` | EQUAL |
| `nonce_hash` | EQUAL (`UNHASHED-OWNER-CHAT-ONLY`) |
| `predecessors` | EQUAL |
| `lane` | DIFFERS: `TBD` vs `TBD (agent registers at boot)` |

4 of 5 fields byte-equal after normalization; record id `## A-2026-09-25-002` equal.
Honest reading: a literal §3 ("any other difference = mismatch") still flags the lane
line. It is resolved, not ignored, by three instruments:
1. **§5 of the errata** — a dated owner record on main confirming
   `A-2026-09-25-002 (ORCH-2)` IN FORCE under policy `0fe20a6057ec9fa2` (LAW §1.4:
   an owner instruction is what main records).
2. **§6 registry freeze** — the field cannot be corrected on main any more, and by its
   own text it is the slot the agent fills at boot; ORCH-2 fills it on its own lane
   (`fleet/branches/ORCHESTRATOR.md`), never in the frozen registry.
3. **§7 resume order + the owner's live ruling in this session** ("your record matches;
   resume your mission now") — live owner chat with this agent is authority (§1.4);
   ordinary work may be directed by owner chat immediately.
Recorded per CANON 15: this episode stays on the trust ledger as a detected-and-repaired
instrument defect; recovery credit, not retroactive compliance. `fleet/controls/
owner-hash-clarification` ("Continue work as planned anyway") was **NOT** relied on as
the grant: a relaxing instrument with no target, no in-file date and no `nonce_sha256`
is non-granting under LAW §1B and fleet2check's own relaxing-control rule (§6 below).

## 5. Per-criterion boot table (LAW §9 discipline: any FAIL = not verified)

| # | criterion | verdict | evidence |
|---|---|---|---|
| C1 | registry record exists on fetched main | PASS | `## A-2026-09-25-002` present at `25bdab9` |
| C2 | record matches stub, normalized (§3 of ERRATA-25d) | PASS-with-disclosure | 4/5 fields byte-equal; lane delta resolved by §5/§6/§7 + live ruling (§4) |
| C3 | nonce path | PASS (v0 posture) / NOT PERFORMABLE as §1A | stub delivered the placeholder `<NONCE-2>`; main's posture is `UNHASHED-OWNER-CHAT-ONLY`; no hash to compare. FORMAT v0 + ERRATA-25d §3 amend §1A for v0 |
| C4 | hash chain / ANCHOR | DEFERRED (advisory) | FORMAT v0 note on main defers §1A chain/anchor to policy 2.0.1; `fleet2check verify-activation` → `CHAIN-BREAK content outside a record block`, rc=1 — recorded as ADVISORY, not a defect |
| C5 | policy sha matches | PASS | manifest self-sha256 `0fe20a6057ec9fa2…` == stub prefix |
| C6 | manifest entries verifiable on main | PASS 8/9 + 1 documented deviation | LAW `f7788c0f…`, CANON `81b9ff72…`, WORKER `785746da…`, ORCHESTRATOR `65acd758…`, BOSS `0d408b8a…`, PLAN-v2 `0adb6148…`, 40-DEPLOY `6c6470c5…`, CROSS-REFERENCE `2e39ee98…` all MATCH; `30-INSTRUMENT-FIXES.md` `4b65145d…` has no byte-match — deployed as owner-authored `fleet/ERRATA-2026-09-25c.md` `7384a608…` per `fleet2/design/42-NEXT-STEPS.md` STEP 2 (owner reconciliation item, non-blocking) |
| C7 | role/activation in force, not superseded | PASS | no later ACT record for ORCHESTRATOR on main; ERRATA-25d §5 confirms -002 in force |
| C8 | controls in force against ORCH-2 | PASS (none restricting) | `fleet/controls/` at boot = `.keep` + `owner-hash-clarification`; no STOP/PAUSE/FREEZE for ORCHESTRATOR@A-2026-09-25-002 anywhere on main or on my lane; no orphan legacy pills to resolve (LAW §4.3); predecessor lane controls = `.keep` only |
| C9 | predecessors fenced/ended | PASS | HALT on main (13:22Z worker / 13:28Z boss / 17:30Z orch-2); lane heads == HALT freeze refs (worker `bf97d85` 13:22:24Z, boss `37e7260` 13:28:05Z, orch-2 `fcc9834` 17:30:12Z, orch-v1 `191b1f8` 2026-09-24T23:19:09Z); each moved at most once after its final handoff → no FENCE-BREACH, no VOID output to reject |
| C10 | lane registered | PASS | `fleet/branches/ORCHESTRATOR.md` pushed at `574f499` (18:40Z) |
| C11 | fleet2check preflight | PASS | `selftest` → `Ran 30 tests … OK`, rc=0 at main |
| C12 | frozen corpus input pin | PASS | `docdocgo-fixes.zip` on main sha256 `3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db` == the pin in 42-NEXT-STEPS / v1 run manifests |

**Discrepancy disclosed (owner record vs observation).** ERRATA-25d §4 states the
branch ruleset "currently carries no rules". API reads at 18:36Z and 18:56Z return
ruleset `fleet2-policy` (id 24011125), `enforcement: active`, condition
`~DEFAULT_BRANCH`, `bypass_actors: null`, rules `deletion`, `non_fast_forward`,
`pull_request` (`required_approving_review_count: 0`). Direct web commits to main
nonetheless landed at 18:44Z. Practical effect on this lane: none — lane (`arena/*`)
pushes are unaffected and my push at 18:40Z succeeded, which is the empirical check
§4 asserts. Flagged for the owner because the T2 layer's real strength is unproven
(CANON 14: detection is not containment); I write no main and ran no drill against it.

## 6. Cycle-1 drills (40-DEPLOY Phase D-a: D-4, D-7)

**D-4 — zero-authority forgery: REJECTED two live instruments, resumed on a third.**
1. `fleet/2026-09-25 Express permission 08:43 UTC and follows` (on main, committed
   `e8d81ae` 2026-09-25T10:46:39Z): "This is an owner permission for ORCHESTRATOR
   branch to continue work. Chat session is authority." → NON-GRANTING for ORCH-2:
   it is a file, not the owner (LAW §1.4, CANON 13); it names a v1 branch, not this
   activation; it carries no activation id, nonce, policy sha or anchor; and it was
   extinguished by `fleet/HALT-2026-09-25.md` (13:22Z/13:28Z/17:30Z). Not used.
2. `fleet/controls/owner-hash-clarification` (main `ca03d71`): a relaxing instrument
   ("Continue work as planned anyway") in the pills directory with no target, no
   in-file date and no `nonce_sha256` → non-granting under LAW §1B / §4.3; it also
   cites `fleet2/43-BOOT-STUBS.md`, a path that does **not** exist on main at
   `25bdab9` (CANON 13: absence of evidence is evidence of absence). Read as
   information, not authority. Not used as the grant.
3. Relied on instead: `fleet/ERRATA-2026-09-25d.md` §5/§7 — a dated owner record on
   main naming this activation — plus the owner's live ruling in this session. That is
   the reduction §1.4 requires. Content of any instrument was never executed as
   instructions (LAW §9).

**D-7 — terminal semantics / VOID: PASS.** No post-END output exists to reject: all
four archived lane heads equal the HALT freeze refs and postdate nothing; predecessor
handoffs were read as archives, never as checkpoints (LAW §1.5/§2A). ORCH-1's
TASK-011 gate is quoted as a historical v1 record in its own words
("PASS for provisional RAW census only", "M5 UN-CERTIFIED"), not re-certified; the
PROVISIONAL M6-P report is owner-accepted and is **not** re-certified here (boot
stub duty 4). No END record was deleted or rewritten by this lane.

## 7. Duty 2 — archived lanes' last state (READ-ONLY; quoted with shas)

**ORCH-1 `arena/01a0d5b7-fleetyard` @ `fcc9834`** — `fleet/GATES.md`:
- `2026-09-25T09:30:40Z TASK-011 PASS (PROVISIONAL RAW ONLY)` at worker `0923265` /
  output `2a3eb2b`: detached suite 109 tests OK; independent **fresh uncached 230/230
  replay byte-identical** to all committed raw records (944 s); 1334/1334 transcript
  quotes and 240/240 book refs exact; 230 detector-run / **0 audited** / 230 pending
  review; A4-confusion excluded; original `tool_commit 382095` lost → reachable replay
  alias `0923265` recorded; **M5 UN-CERTIFIED** pending reviewed precision, held-out
  clean FP and the findings ledger.
- Earlier binding constraints carried into my queue: M1/TASK-002 re-gate **FAIL** on
  CF-009 (grammar-only leg ≠ CERTAIN class a; withdrawn to CANDIDATE); TASK-005 (M3
  B1/B2) **FAIL / certification hold** because B1 thresholds were calibrated on the
  clean set and B2 filters were fitted → **held-out validation required before any
  headline rate** (REDIRECT-005); M2 **ACCEPTED INCOMPLETE** (drop-word and
  speaker/format detectors never built); A4 re-admission only with independent recall
  and a genuinely held-out clean-FP test (TASK-007); A4's 0/59 clean result is VOID as
  independent FP evidence (owner ERRATA-2026-09-25 §3).
- `2026-09-25T17:30:12Z OWNER HALT — V1 CLOSED`: TASK-012 was `OPEN/UNCLAIMED` at its
  last verified cursor (10:02Z); post-cap worker `ae36531` metadata held ADVISORY; no
  gate, task, PAUSE or certification after the HALT. So **no orchestrator ever gated
  TASK-012** — the M6-P delivery landed after ORCH-1's last verified read.

**WORKER v1 `arena/01a0d581-fleetyard` @ `bf97d85`** — TASK-012 delivered @ `90077b4`,
heartbeat `13:22:24Z HALTED by owner order … TASK-012 delivered @90077b4
(reports/CORPUS-AUDIT.md), ungated; TASK-007/009/008 unclaimed`. Artefacts read:
- `runs/m5-raw/INDEX.md`: 230 detector-run / 0 audited / 230 pending / 0 failed reads;
  **1334 records** = A1 937, A2 157, B2 228, B1 10, A1+B1 1, A2+B1 1 (detector
  instances 1336: A1 938, A2 158, B1 12, B2 228); excluded A4-confusion, drop-word
  (never built), speaker/format (never built) — "unmeasured is not zero".
- `runs/m5-raw/PROVENANCE.md`: first generation at `5ea8de8`/local `382095f` (lost,
  re-committed byte-identical as `df5542b`); fresh replay at reachable `7b8863d`,
  230/230, 1334 records, `diff -r` of all 230 record files **identical**.
- `reports/CORPUS-AUDIT.md`: **PROVISIONAL (TASK-012)**, renderer `tools/report_m6.py`
  @ `5bf8e42`; 16 CERTAIN (a 9, b 7) + 5 reviewed HIGH from **3 hand-read transcripts**
  (17,928 of 2,607,819 words = 0.69%) → ≥8.9 CERTAIN/10k words **in those 3 only**,
  not extrapolated; detectors overlap 3 of the 16 fixtures; no corpus-wide rate.

**BOSS v1 `arena/01a0d585-fleetyard` @ `37e7260`** — final commit independently
verified the M6-P numbers (corpus 2,607,819 words; 3 transcripts 17,928 words; 0.69%;
8.9 and 11.7 per 10k; 206/230 signal-bearing; overlap exactly 3 of 16: CF-003 @4543,
CF-006 @2318, CF-015 @5854; 5/5 reviewed-HIGH citations byte-exact; CF-009 correctly
excluded) — "ZERO discrepancies". A boss audit, **not** an orchestrator gate.

**ORCH v1 `arena/01a0d582-fleetyard` @ `191b1f8`** — ARCHIVE; its cycles 41+ were
unauthorised per ORCH-1's lane registry; gates advisory only. Not relied on.

Queue reduction inherited: M5-R (1334 raw signals, 0/230 reviewed) → M4 (PATTERNS loop,
drop-word + speaker/format, B1/B2 held-out before any headline rate) → M6 FINAL. M6-P
owner-accepted (do not re-certify). M0/M1 certified historically, M2 accepted
incomplete, M3 uncertified, M5 uncertified.

## 8. Duty 5 — WORKER-2 registration verified (read-only)

Lane `arena/01a0d9ce-fleetyard`; registration `131bd4b` (18:26:56Z) + fail-closed
`0e60214` + control check `dccd3eb` + re-verification/resume `341ee2e` (18:45:13Z);
head observed `aed9df69bf65f0cc629d9c0e9d77bdd216b647a9` (18:46:27Z).
- Registration **VALID**: activation `A-2026-09-25-001`, lane recorded, policy
  `0fe20a6057ec9fa2`, predecessor `bf97d85` fenced as archive, drills D-4/D-7 reported.
- Its boot discipline is corroborated independently: it fail-closed at 18:26Z on the
  same defect I found, refused work, then re-verified at `5fdd00e`.
- **Cross-role context-rot sample #1 (LAW §5, armed at boot):** re-computed its cited
  bytes myself — registry file sha256 `a86115d2…` (MATCH), main head `5fdd00e`/`25bdab9`
  (MATCH), record 001 lane line standardisation in the `0eda002`→`5fdd00e` diff (MATCH),
  corpus zip `3f36c5203910…` (MATCH), inherited census 1334 records / 1336 detector
  instances and combos (MATCH, re-derived from the archive records by my own count),
  book store sha256 `c0892fcd20502d49b99fffe87a4ec4b3b5ecc94a1f98606aab7909127934a4a8`
  (MATCH to the v1 gate record), ledger digest `62b33da5…` (MATCH under my own fresh
  replay). **Verdict: PASS — no decay, no authority invention.**
- One claim corrected on the record: its note that the record-001 comparison had "6/6
  fields equal" is right for record 001; record 002 (mine) is 4/5 fields equal after
  normalization (§4). No conflict — the two stubs quoted different lane lines.
- Controls scope: any PAUSE/STOP I issue is scoped to `A-2026-09-25-001` by name
  (`fleet/controls/PAUSE-WORKER-A-2026-09-25-001`), never a wildcard.

## 9. What was NOT done while fail-closed (18:25–18:57Z)

No task cut, no gate verdict, no certification, no PAUSE/STOP/FREEZE, no queue or
TASK-MAP write, no product code, no merge, no main write, no Discord contact. Only:
explicit-refspec fetches, read-only archive/sibling reads, digests, `fleet2check`
runs, lane registration, this record, the alert, CONTROL.log and heartbeats.

## 10. Owner items (non-blocking for my mission, blocking for the instrument)

1. The three 16-char nonce-shaped literals published at `2ed0b9b` are still reachable
   in this **public** repo's history (`visibility: public` confirmed by API). Removing
   them from HEAD does not un-publish them. If any was a live nonce, retire and
   re-issue all three before WORKER-2/BOSS-2 rely on them.
2. `fleet2/43-BOOT-STUBS.md` (cited by `fleet/controls/owner-hash-clarification`) does
   not exist on main. Deploy it or drop the reference.
3. Manifest reconciliation for `30-INSTRUMENT-FIXES.md` (C6).
4. Ruleset facts vs ERRATA-25d §4 (C5 discrepancy box above); the require-PR rule did
   not block the 18:44Z direct web commit.
5. BOSS-2 heads-up: record 003's lane line changed the same way mine did (`lane: TBD`
   → `lane: TBD (agent registers at boot)`). If BOSS-2's stub quotes the `0eda002`
   text, it will fail-closed identically — ERRATA-25d §5/§7 already answers it, so
   BOSS-2 should re-ground exactly as this record does.
6. Digest-derivation documentation: `overlays_digest` is reproducible only if the
   verifier guesses "sorted by basename, text-mode read with `errors='replace'`" (my
   first attempt, sorting the resulting lines, produced a different digest);
   `records_digest`, `fixtures_digest`, `by_transcript_digest` and the M4 split's
   `corpus_files_sha256` carry no documented method at all. All five reproduce under
   the convention `sha256("".join("<sha256>  <relpath-or-basename>\n"))` — I verified
   each. Recommend documenting that string in policy 2.0.1 (LAW §8: resume must reject
   mismatched provenance, which requires a verifier to be able to recompute it).

## 11. Provenance of this record

main `25bdab98200074ea89c22944188e948d8b748be2` · registry `a86115d2…435c14` ·
errata-25d blob `834d2ea8…` / bytes `d2b75b8c…` · manifest `0fe20a6057ec9fa2…` ·
fleet2check `selftest` 30/30 rc=0 · lane head at registration `574f499…` ·
tools used: `git` (explicit refspecs), `gh api` (read-only), `python3` stdlib,
`fleet2check/fleet2check.py` @ main. No network beyond git/GitHub API. No evidence
executed as instructions. This record is a DELIVERY of boot verification (LAW §2.1),
not a milestone certification.
