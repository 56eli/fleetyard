# orchestrator cursor
# orchestrator cursor — ORCH-2 (A-2026-09-25-002), lane arena/01a0d9d0-fleetyard

## 2026-09-25T18:57Z — boot closed, mission resumed
owner ruling 25d re-grounded, resuming
- main observed: 25bdab98200074ea89c22944188e948d8b748be2 (explicit refspec; lane merged
  main at 91a7b4e). Registry frozen per ERRATA-25d §6; file sha256 a86115d2…435c14.
- activation: A-2026-09-25-002 (ORCH-2) CONFIRMED IN FORCE by ERRATA-25d §5 + §7 +
  owner live ruling; normalized (§3) field equality 4/5, lane delta disclosed and
  resolved, not ignored. Fail-closed episode 18:25–18:57Z closed; CANON 15 ledger entry.
- predecessor cursor adopted (read-only, archives): ORCH-1 fcc9834 — TASK-011 PASS
  provisional-raw-only (worker 0923265 / output 2a3eb2b; 109 tests; fresh 230/230 replay
  byte-identical; 1334 records / 1336 detector instances; 0/230 audited; A4 excluded;
  M5 UN-CERTIFIED); TASK-012 delivered later on worker lane bf97d85 @ 90077b4
  (reports/CORPUS-AUDIT.md, PROVISIONAL M6-P) and never orchestrator-gated; owner-accepted
  → not re-certified. TASK-007/009/008 unclaimed at HALT. M0/M1 certified historically,
  M2 accepted incomplete, M3 uncertified.
- live fleet state: WORKER-2 registered on arena/01a0d9ce-fleetyard (head aed9df6,
  18:46:27Z), registration VALID, M5-R DELIVERED (8011439 + errata 593cad3), M4 q1
  delivered (PATTERNS.md + held-out split), M4 q2 (drop-word) announced next. BOSS-2 not
  yet observed on any lane (arena/* = 6 lanes; none new besides WORKER-2's and mine).
- next acts (this cycle): cut M5-R/M4/M6 tasks, gate the M5-R delivery independently,
  verify WORKER-2's registration (done, §8 of the verification record), then gate M4 q1.

## 2026-09-25T19:01Z — cycle 1 (mission): queue cut + first independent gate
- Queue (order): TASK-016 (repair M5-R) -> TASK-017 (inherit v1 toolchain) -> TASK-014
  q2-q4 (drop-word, speaker/format, B1/B2 held-out + precision, A4 decision) -> TASK-015
  (M6 FINAL). TASK-013 gated FAIL/INCOMPLETE; TASK-014 q1 gate OPEN (no verdict).
- Gate verdict TASK-013 (M5-R) = **FAIL / INCOMPLETE**: C6 finding-record shape (157
  findings without a suspected-intended field; no STANDARDS status/status_by), C7 coverage
  truth (no audited 0/230 vs pending 230/230 row), C8 LAW §8 manifest (no tool_commit, no
  policy sha, no book-store sha256, no detector+config digest, 4/5 digest methods
  undocumented). All other criteria PASS under my own independent reproduction — the
  ledger's numbers, citations, book bytes, determinism, scope and honesty all held.
- Brake: PAUSE-WORKER-A-2026-09-25-001 (scoped, dated, reasoned; removable by PASS).
- Certifications outstanding: none granted. M0/M1 historical, M2 accepted incomplete,
  M3 uncertified, M5-R incomplete, M4 in flight, M6-P owner-accepted PROVISIONAL (never
  re-certified by me), M6 blocked. No rate exists anywhere in my records.

## 2026-09-25T19:06Z — fleet coherence + two escalations to the owner
- Fleet is 3-up: WORKER-2 `arena/01a0d9ce` @ `e07be0e` (18:52:41Z) · BOSS-2
  `arena/01a0d9d1` @ `bb2eabb` (18:59:53Z) · ORCH-2 `arena/01a0d9d0` @ this head.
  BOSS-2 fail-closed at 18:29Z on the same registry defect and resumed at 18:48Z on
  ERRATA-25d; it witnessed my cycle-1 drills D-4/D-7 as PASS @ `f2da67a` and is tracking
  the M5-R scoreboard (3 CERTAIN-inherited / 0 HIGH / 1331 CANDIDATE) — matching my own
  re-derivation exactly.
- WORKER-2 @ `e07be0e` logs two owner chat rulings: (1) the nonce-shaped literal on main is
  INERT AND RETIRED (v0 posture; boot nonces single-use, consumed at boot verification);
  (2) manifest pin `4b65145d…` is the policy-bundle SOURCE file while deployed
  `fleet/ERRATA-2026-09-25c.md` (`7384a608…`) is the instrument OF RECORD, reconciliation
  deferred to 2.0.1, freeze extends to the manifest. Both would close items 1 and 3 of my
  boot record §10 — but a report of chat by another lane is not the owner (LAW §1.4,
  CANON 13), so I record them as REPORTED and asked the owner to confirm them here or on
  main. Until then my §10 items stand as open, not as accusations.
- "M4 q1 approved" (owner, per WORKER-2's log, labelled PROVISIONAL-UNGATED) does not
  replace my gate: certification is evidence-bound and mine, completion is the owner's
  (LAW §2.2, §9). My TASK-014 q1 gate stays OPEN and will be completed on its criteria.
- Collision escalated: my `PAUSE-WORKER-A-2026-09-25-001` (19:01Z, brake on a FAIL per
  ORCHESTRATOR.md step 3) postdates the owner's M4 approval given to WORKER-2 (~18:52Z).
  The PAUSE stands (restrictions are fail-safe) and I asked the owner to choose:
  (A) repair-first as cut, (B) run TASK-016 and M4 q2 in parallel on an owner ORDER line,
  or (C) lift the PAUSE — noting that in every case the M5-R FAIL verdict is evidence-bound
  and only a repair + re-gate clears it, and M6 FINAL stays blocked until it does.

## 2026-09-25T20:04:10Z — M5-R gate-PASS, PAUSE removed, queue kept small
- main observed `77f1d6de80ec0ae77d7ca06fdfd581671cea7cae` (merged into this lane @
  44139d7): ERRATA-25e (OPTION A; M4 parked; CERTAIN leg (d)) + ERRATA-25f (liveness =
  signals not output; worker idle-cycles are correct; orchestrator review takes the time it
  takes but never overfills the queue; boss CONCERN scope narrowed, REDIRECT-008's urgency
  framing retired with its re-gate substance standing; owner is not the cycle pump; never
  end a turn for idleness). Registry frozen and unchanged; policy manifest unchanged.
- REDIRECT-008 (boss, 19:43Z, ack due 19:58Z) ACKED 19:57:21Z @ 5f6d698: all four orders
  accepted and executed this cycle. The Class-2 fire was correct on the facts (my signals
  stale 19:06Z→19:56Z mid-review) — defect owned, cadence now written inside the loop.
- **GATE: TASK-016 = PASS → TASK-013 / M5-R = PASS** at WORKER-2 `1beadd9` (fleet/GATES.md
  19:58Z). All thirteen criteria re-run with fresh evidence, nothing inherited from the
  19:01Z gate: ledger `d42136c6…`, by-transcript `c1ec4da8…`, tool `6d4bb9ce…` ==
  blob at `tool_commit dada3e60` (reachable), pinned replay byte-identical, unpinned replay
  proves pins fail closed to `UNPINNED`, 1334/1334 spans + 1336/1336 signal quotes +
  242/242 book bytes re-verified with my own parsers, all seven §8 digests recomputed MATCH
  (incl. inherited detector commit `7b8863d` reachable), coverage row recomputed
  230/230/230/0/230/24 (+206 with findings, 24 zero-signal), record shape 1334/1334 with
  157 explicit nulls, classes CERTAIN-inherited 3 / HIGH 0 / CANDIDATE 1331, seeded 3/1331,
  suite **26 tests OK, 0 skipped, WITH corpus**.
- Errata #2 (M4-q5's reducer fix) changed the ledger, so I re-derived it myself: my own
  implementation of the documented token/period rule matches the ledger's `rederived` on
  **938/938** A1 spans and every runner claim holds → the 98 withdrawn flags were correctly
  withdrawn. Field-level diff vs the gated `62b33da5…`: 4 fields added on 1334; values
  changed on signals/claim_checks/claims_all_corroborated/rederived_repetition (98),
  review_score (99), and book_checks (144 findings / 146 entries, **`divergence` only**).
  No class, count, citation or book quote moved.
- **PAUSE-WORKER-A-2026-09-25-001 REMOVED** (marked, never deleted) per its own removal
  clause + ERRATA-25e §1 + REDIRECT-008 §2.3. TASK-013/TASK-016 CLOSED (files kept with
  CLOSED status lines). Not certified: milestone certification is the owner's (LAW §2.2);
  no rate exists; M6-P untouched.
- Queue (deliberately small, ERRATA-25f §4): **TASK-018** cut — owner-ordered leg-(d)
  individual adjudication of the 122 drop-word signals + 4 provisional fixtures under the
  standing guidance L1–L6 in fleet/GATES.md, item 0 = one append-only correction to
  findings/M4-q5-A1-CLAIM-RECONCILIATION.md (its M5R-0036 row contradicts the artefact:
  `Mm-hmm` is ONE token under the Unicode rule; the ledger says 1×8 and the claim agrees).
  Then **TASK-017** (v1 toolchain inheritance). M4 q2–q5 stay DELIVERED-PROVISIONAL-UNGATED
  (resumable, ungated, uncertified); gating order q1 → q2 → q3 → q4 → q5. TASK-015 (M6
  FINAL) still BLOCKED: M4 gates + a **fresh sealed holdout** (the one-shot split was spent
  19:12–19:14Z, counts only) + TASK-017 + TASK-018.
- Coherence facts handed to BOSS-2 + owner without inventing verdicts:
  fleet/alerts/ORCH-2-COHERENCE-2026-09-25-001.md (post-PAUSE q3/q4/q5 timeline and the
  worker's duplicated seq 10–15 / missing control-check lines; holdout spent; STANDARDS.md
  still lacks leg (d); §8 literalism residuals; my boot §10 items still REPORTED).
- Next this cycle: complete the TASK-014 q1 full gate (PATTERNS.md + held-out split) —
  including whether PATTERNS.md still binds the superseded ledger digest; control check
  ≤300 s; cadence lines inside the work, not after it.

## 2026-09-25T20:08:32Z — TASK-014 q1 gated: FAIL / INCOMPLETE on one criterion
- q1.1/q1.2/q1.3/q1.4a-c **PASS** on my own re-derivation at `1beadd9`: all 16 CERTAIN
  fixtures wired to P1-P7; coverage truth 3/16 (CF-003/006/015) reproduced from the
  gate-PASS ledger; the split was fixed **before** any detector existed (commit order at
  `593cad3`), is deterministic and reproducible by me exactly (holdout 37 / tuning 193, sets
  equal, per-year table equal), its seal `481d8513…` is byte-identical to the delivered one,
  `corpus_files_sha256 9ae90185…` reproduces from the documented derivation, fixture
  transcripts are forced TUNING, every precision cell reads unmeasured and every promotable
  cell no, and the tuning path filters + asserts + SystemExits on holdout overlap while the
  parked q2/q3 outputs key exactly the 193 tuning files (0 holdout).
- **q1.4d FAIL**: `tools/PATTERNS.md` (`528265e7…`) quotes M5-R figures (938/938 · 158/158 ·
  12/12 · 228/228, coverage 3/16) with no binding to the ledger digest they came from — and
  those very figures were changed by errata #2 at this head, which is the point of a binding.
- Brake: **no activation-scoped PAUSE** (deviation from ORCHESTRATOR.md step 3, argued and
  reversible in fleet/GATES.md 20:08Z); artefact-scoped restriction instead — q1 may not be
  cited as passed, no M4 promotion, no q2-q5 gate credit, no M6 figure may rest on
  PATTERNS.md. Repair folded into **TASK-018 item 0b** (queue stays at two tasks).
- Hygiene: 2 `.pyc` files were committed at `593cad3`; at `1beadd9` there are 0 and a lane
  `.gitignore` excludes corpus/, evidence/, __pycache__/, *.pyc — self-corrected.
- Next: M4 q2-q5 gates are resumable and ungated (order q2 → q3 → q4 → q5); they will be
  gated against TASK-014's criteria plus the leg-(d) standing guidance, and q4 cannot yield a
  rate until a fresh sealed split exists (the one-shot holdout is spent).

## 2026-09-25T20:10:48Z — cycle close: gates current, queue small, handoffs outstanding
- **M5-R: gate PASS, re-affirmed at WORKER-2 head `219075a`** (provenance-only delta
  re-verified; ledger `d42136c6…` and by-transcript `c1ec4da8…` unchanged; fresh pinned
  replay byte-identical incl. `PROVENANCE.json` `921bbc56…`; suite 26 OK 0 skipped). PAUSE
  REMOVED. Not certified, no rate, M6-P untouched.
- **TASK-014 q1: FAIL / INCOMPLETE** on q1.4d only (PATTERNS.md quotes the ledger's figures
  with no digest binding). Split itself verified clean, deterministic, sealed before any
  detector existed, and reproduced by me exactly. No activation pause (deviation argued and
  reversible in GATES.md 20:08Z); artefact-scoped restriction in force.
- **Criteria re-cut**: q2-q4 precision now requires a **fresh sealed split v2** (the q1
  holdout was spent 19:12-19:14Z and is a receipt only); until then every precision cell
  stays unmeasured and nothing is promotable.
- **Handoffs outstanding**: WORKER-2 → TASK-018 (item 0 doc correction, item 0b PATTERNS.md
  binding, then the owner-ordered per-finding leg-(d) adjudication of 122 signals + 4
  provisional fixtures under L1-L6), then TASK-017. BOSS-2 + owner →
  fleet/alerts/ORCH-2-COHERENCE-2026-09-25-001.md (post-PAUSE q3/q4/q5 timeline and the
  duplicated worker seq 10-15; holdout spent; STANDARDS.md still lacks leg (d) text; LAW §8
  literalism residuals; my boot §10 items still REPORTED; my own 50-min signal stall owned).
- **Mine next cycle**: gate M4 q2 → q3 → q4 → q5 after TASK-018 lands; keep cadence lines
  inside the review loop (ERRATA-25f §4); control check ≤300 s; never write main; never
  re-certify M6-P; no rate anywhere without split v2 evaluated once.

## 2026-09-25T20:36:36Z — 25g re-ground, TASK-019 cut, and a workspace-reset recovery (recorded, nothing lost)
- Owner ERRATA-2026-09-25g @ main `7d033ab` (blob `84d3019f`, bytes `d0191e6d…`) read and
  adopted: a shift spans ~24 h; a turn ends ONLY for platform necessity, a genuinely blocking
  FAIL, or shift handoff — never for status; status is pushed documents; work as many cycles
  per turn as the platform allows; push state + a cursor line before any turn end.
  **My previous turn-end (a chat status essay after ~2 h) is owned as a FAILED STATE.** The
  shift now continues inside the turn.
- **TASK-019 cut** (owner-AUTHORIZED): fresh sealed holdout split **v2** — quantum a seals
  (new salt; published, written-down, independently reproducible method; v1 fixture
  transcripts **and TASK-018's confirmations** forced to TUNING; sealed before any further
  tuning on commit-order evidence; re-seal rule if a fixture is confirmed later; LAW §8
  manifest), quantum b evaluates **once** after I gate q2/q3 and thresholds are frozen
  (per-detector precision + FP counts, seeded vs independent separate, hand adjudications with
  reasons I re-derive byte-exact, CANDIDATE never blended, B1/B2 headline hold until it
  passes). Criteria v2.1–v2.9 in the task file. Worker order: **TASK-018 → 019a → 017 →
  [my q2/q3 gates] → 019b**.
- **Infrastructure event (second this shift):** the sandbox reset the local repo to the branch
  point `2ed0b9b` while my pushed head was `45959ca`; my cycle-A commit landed on `2ed0b9b`
  and was correctly rejected by the remote. Recovered with `git fetch` + `git reset --mixed
  45959ca` (working tree preserved, so this cycle's writes survived) + `git merge origin/main`
  = `7ae4032`; registry file sha `a86115d2…435c14` unchanged; no pushed history rewritten;
  correction logged as CONTROL seq 12 rather than editing seq 11. WORKER-2 logged the same
  reset at `10afc0d` — LAW §8's push-every-commit rule is why neither lane lost work.
  Standing fix in my pre-push check: assert `git rev-parse HEAD` is a descendant of the
  remote lane head before committing after any reset.
- Next in this turn: M4 **q3** gate (independent of leg (d)), then **q2** (determinable
  criteria; leg-(d) classification items PENDING TASK-018), then q4 execution discipline and
  q5 residuals; TASK-018/019/017 gates as they land.

## Cycle C (2026-09-25T21:02:05Z) — M4-q2 gate FAIL/INCOMPLETE + gate-side clean-set probe + TASK-020 cut
- **q2 (C1-drop, 012914d) GATE = FAIL / INCOMPLETE** on five criteria (q2.1b fixture results,
  q2.1c clean-set results, q2.1d threshold provenance, q2.4 §8 manifests, q2.5 test count vs
  the v1 baseline 115). PASS on q2.1a self-test, q2.3 isolation, q2.6 reproduction+citations
  (with a 9/122 shape caveat), q2.7 classification discipline (with two coherence defects);
  q2.2 precision correctly PENDING split v2. Full table: fleet/GATES.md 20:58Z.
- **Worst provenance item:** all six part manifests pin detector_sha256 84e5407f, which matches
  **no committed version** of tools/det_dropword.py (012914d = 588e1f22, head = a0236325) — the
  run predates its own delivery commit by ~10 minutes. I closed the attribution gap by
  reproduction instead: shards 1/6 and 3/6 re-run at head are **byte-identical** (64a97be5,
  092d6341) = 66/193 transcripts, 93/122 signals, and 4e114f1's change to the file is
  runner-only. This is the second gate in a row where a §8 digest did not resolve (q3: c322e053
  bound 4425763) → TASK-020 item 1 makes committed-blob re-pins explicit.
- **I ran the clean set the worker did not** (gate-side, labelled as mine): 59 hashed known-good
  Hawkins passages, integrity verified 59/59 against store c0892fcd, materialised as
  pseudo-transcripts with the store symlinked → **C1-drop 3 misfires, C2-format 1 misfire**. All
  three drop misfires are cross-book self-parallels; the format misfire is book-store typography
  ("power.When" in power_vs_force @236391). Transfer test (validated on the 3 known misfires):
  1/122 drop signals and 0/49 format signals carry that shape → the tuning runs are not
  materially contaminated, but both detectors owe an additive source-inheritance filter, and the
  worker's disclosed FP list omits both shapes. Numbers are written into TASK-020 as
  reproduction targets so the repair is checkable, not descriptive.
- **Fixture file coherence:** all 4 provisional dropword fixtures re-verified byte-exact by me
  (spans, book quotes, dropped-token claims) and none is a cross-book artifact, so TASK-018 can
  adjudicate on bytes. But the file's proposed leg-(d) wording is **not** the enacted text
  (ERRATA-25e §2 is narrower), per-fixture proposed_leg says a/a/b/b, and generated_utc is fuzzy
  → TASK-018 item 0c (shared with TASK-020 item 7, single edit, cross-referenced).
- **Sequencing disclosed:** I gated q3 then q2 ahead of TASK-018, superseding my own 20:02Z
  "gates run after TASK-018" line, because no criterion I decided depends on leg-(d)
  adjudication; classification items are recorded PENDING and the fixtures stay provisional.
- No pause issued (proportionality test recorded in GATES.md, reversible on request); artefact
  restrictions applied instead. Queue held at three actionable tasks (018, 020, 017) per
  ERRATA-25f §4. Next in this turn: q4 execution-discipline gate (holdout SPENT — receipt only,
  never re-run) and q5 residuals, then TASK-018/019/020 gates as they land.
- **Disclosure (my scripting error, same cycle, repaired):** the first write of CONTROL seq 14
  left the registry field EMPTY (I hashed a non-existent `fleet/REGISTRY.md`), and my first
  repair hashed the wrong path (`REGISTRY.md` instead of `fleet2/activations/REGISTRY.md`),
  which produced the empty-input digest `e3b0c442…`. Both were corrected in-cycle: seq 14 now
  carries `a86115d2…435c14`, re-derived from `origin/main:fleet2/activations/REGISTRY.md` and
  equal to the FROZEN registry digest (ERRATA-25d §6). No verdict or note text was rewritten;
  the field fill is disclosed here and in CONTROL seq 15. Standing fix: the pre-push check now
  asserts the registry field of the newest CONTROL line is 64 hex chars and equals the frozen
  digest.

## Cycle D (2026-09-25T21:10:55Z) — M4-q4 gate FAIL/INCOMPLETE on 2 criteria; the one-shot discipline HELD and I could prove it
- **q4 GATE = FAIL / INCOMPLETE** on q4.6 (§8 manifests: the v1 leg has no corpus binding, no
  book-store digest, no tool_commit/main_head/policy sha and no output digest for a 127 KB file;
  drop/format legs lack the book-store digest and output digests) and q4.8 (the C1-drop gap is
  called sampling noise). PASS on q4.1/q4.2/q4.3/q4.4/q4.5/q4.7; q4.9 **NOT GATEABLE** → TASK-019b.
  Table: fleet/GATES.md 21:09Z.
- **The discipline checks are the ones that matter here and they pass on evidence, not assertion:**
  the q2 tuning params block and the q4 holdout params block are identical value-for-value, the
  C2-format rules list is identical, neither detector file changed in any commit after the run
  (det_dropword a0236325, det_format ef9ff4f2 from 4e114f1 through head), and unlike q2/q3 the q4
  detector pins **do** resolve to committed blobs. Inverse isolation is airtight (holdout_reads ==
  the 37 names, transcripts_read ∩ tuning = 0, in all three manifests) and holdout_consumed is
  stamped everywhere. **I did not re-run the spent holdout** — arithmetic over committed artefacts
  and blob comparisons only.
- **I verified the delivery's one positive claim myself:** recounting v1-holdout.json gives 185
  signals (A1 162 / A2 15 / B2 8 / B1 0, exactly as manifested) and per-transcript counts match the
  committed M5-R raw records for all 37 holdout transcripts with **0 mismatches**. The reproduction
  receipt is real.
- **Attribution surprise, in the worker's favour:** all 13 v1 tool shas pinned by the q4 manifest are
  **byte-identical to the archived v1 lane** origin/arena/01a0d581-fleetyard:tools/*.py, so the v1
  leg is attributable to committed code even though evidence/tools/ (the directory the manifest
  cites) is not in this tree at all. That
  refines my q2.5 evidence line (the v1 files are absent from THIS lane, not lost) and sharpens
  TASK-017: inherit 13 named files + the v1 suite, cite lane+commit+blob.
- **New analysis contributed by this gate (exposure normalization):** holdout transcripts are 14.9%
  shorter, so per-transcript densities mislead. Normalized by character exposure with a Poisson
  tail: v1 185 vs 187.6 expected (P=0.45 — the 5.95-vs-5.00/tx difference is entirely exposure),
  C2-format 12 vs 8.0 (P=0.94 — consistent), **C1-drop 5 vs 19.9 (P=7.7e-05)** — a real ~4x deficit.
  So PATTERNS §5d's "dominated by sampling noise" is wrong for the one detector where it matters,
  and right-by-accident for the other two. Two live causes: thresholds fitted to the tuning half
  (untestable while q2.1d's provenance is missing) or a book-exposure difference between halves
  (testable only on split v2). Either way: C1-drop stays not-promotable and TASK-019's
  seal-before-tuning rule is exactly the control that would have prevented the ambiguity.
- Repair folded into **TASK-020** (now items 1-10, criteria 20.1-20.11) rather than a fourth task;
  queue still three actionable items (018, 020, 017). Next in this turn: **q5** (2f55b0c — A1 claim
  reconciliation, reducer Unicode tokenizer + kmax 16, errata #2) as the last ungated M4 quantum.

## Cycle E (2026-09-25T21:17Z) — M4-q5 gate FAIL/INCOMPLETE on 2 criteria, substance ACCEPTED on my own re-derivation; **M4 gate sweep complete (q1–q5)**
- **q5 GATE = FAIL / INCOMPLETE** on q5.7 (three live documents present the superseded ledger digest
  `64977c2f…` as *current*; the ledger at head is `d42136c6…` because TASK-016's regeneration
  `a4c6655` rewrote the record shape two minutes after q5) and q5.8 (its numbers do not reproduce
  exactly: claimed units run to **k=12**, not "~11", leaving `kmax=16` four tokens of headroom; my
  pre-q5 simulation flags **97** = 9 zero-ASCII-token + 61 over-bound + 27 ASCII-mismatch vs the
  doc's 98/67; and the hyphen nuance is unquantified — **255/938 A1 claims, 27%, are
  tokenizer-sensitive**). PASS on q5.1–q5.6. Table: fleet/GATES.md 21:17Z.
- **What I could carry forward (the useful part):** with my own direct periodicity test over
  casefolded Unicode tokens — an independent implementation, not their longest-run search — **938/938
  A1 claims corroborate, 0 failures**, and my recomputation of the ledger's `span_fully_periodic`
  agrees on **938/938**. So the corroboration column PATTERNS §3 quotes (938/938 · 158/158 · 12/12 ·
  228/228 = 1,336/1,336) is now **ORCH-2-VERIFIED**: that is exactly the receipt TASK-018 item 0b and
  TASK-020 item 3 need when they bind those figures to the ledger digest, and it closes the q1.4d
  story from the evidence side.
- **Nothing protected moved:** ledger `d42136c6…` (= my M5-R PASS binding), 1,334 findings,
  CANDIDATE 1,331 + CERTAIN-inherited 3, instances 938/158/12/228 = 1,336 reconciling with 1,334 via
  two dual-detector findings, `REVIEW-QUEUE.md` 100 entries at `4e114f1`, `2f55b0c` and head (the
  194-line churn dropped nothing), both q5 regression tests present, suite 26 OK 0 skipped WITH
  corpus. The M5-R PASS is unaffected — q5 is an ancestor of `1beadd9` where I issued it.
- **M4 gate sweep complete:** q1 FAIL(1) · q2 FAIL(5) · q3 FAIL(3) · q4 FAIL(2 + precision NOT
  GATEABLE → TASK-019b) · q5 FAIL(2). Standing consequences: no M4 quantum citable as passed, no
  detector promotable, no rate exists, TASK-015 (M6 FINAL) stays BLOCKED on split v2. The five gates
  share ONE shape — §8 bindings that do not resolve plus shipping evidence that existed and was never
  run — which is why the repair is a single task (TASK-020, items 1–11, criteria 20.1–20.12) rather
  than five, and why every substance test I could run (byte-identical reproductions, 100% citation
  exactness both directions, isolation both directions, one-shot discipline, the 185/185 receipt, the
  938/938 re-derivation) came back clean. That contrast is the honest headline for the owner: the
  work is sound and the paperwork is not, and the paperwork is what makes sound work unverifiable.
- Next in this turn: fleet re-check cycle (boss lane for orders/CONCERNs, worker lane for a TASK-018
  claim, main for new errata), then idle-with-cadence — heartbeat + CONTROL.log at ≤300 s — while the
  worker's owner-ordered tasks run. Turn does not end for status or idleness (ERRATA-25g).

### Cursor at turn end (platform necessity — push and fetch dead since 21:38Z)

Cycle F gate queue **exhausted**: TASK-018 **FAIL/INCOMPLETE** · TASK-019a **FAIL on v2.5 only** (seal valid, NOT
void; quantum b held) · TASK-020 items 1–8 **FAIL** (items 9–11 undelivered) · TASK-017 **PASS all six**. TASK-021
cut. Nothing further is gateable until repairs land, and no delivery can be read while fetch is dead. Local commits
awaiting push, in order: `8cd2f5c` → `cba2550` → `3dd0b45` → `1ca3941` → `430706b` → the cycle-F summary commit.
Consolidated record: `fleet/ORCH-2-CYCLE-F-GATE-SUMMARY.md`. Owner action required: **reconnect GitHub in Arena**;
the reconnect runbook is at the end of that summary.


## Cycle G (2026-09-25T22:33:26Z) — reconnect, workspace-reset recovery, backlog push

- **Credentials restored by the owner.** git fetch/push work; `gh api user` → 403 scope limit (not auth) — no
  gh-API-only step may be relied on here.
- **Second platform event:** the workspace had been **recreated** — fresh clone at `7d033ab`, my lane at its base
  `2ed0b9b`, the six cycle-F commits **absent as objects**, `/home/user/gate-scratch` **wiped**. The **documents
  survived** (snapshot). Recovered with `git fetch origin '+refs/heads/*:refs/remotes/origin/*'` +
  **`git reset --mixed origin/arena/01a0d9d0-fleetyard`** (never `--hard`) → HEAD on the pushed head `31ce8dd`,
  working tree intact, clean fast-forward. **Frozen registry verified intact** (`a86115d2667e7d54…` both from
  `origin/main` and in my tree; nothing under `fleet2/` modified). `origin/main` still `7d033ab`.
- **Disclosure:** the lost shas (`8cd2f5c`, `cba2550`, `3dd0b45`, `1ca3941`, `430706b`, `4d297d0`) were local-only;
  their **content** is pushed now, re-committed on `31ce8dd`. Verdicts/criteria/items/restrictions/digests unchanged;
  only container commits lost. Recorded in the alert §6.
- **Fleet while blind:** BOSS-2 cycles 20–31, **zero controls, no CONCERN against ORCH-2**, reconnect noted at cycle
  24; my silence read correctly as a gating battery. WORKER-2 `ffb8811` → **`4fc40c8`**: `d7fee6e` = **TASK-020 items
  9–11 delivered** (q4 LAW §8 supplement, PATTERNS §5d exposure-normalized correction, the three stale ledger-digest
  lines, q5's numbers; suite 227 OK per BOSS-2), `4fc40c8` = leg-(d) outcome bound into PATTERNS **with the floor-5
  sensitivity row 71/57/33/22 attached** (my beacon seq 18 rule, adopted independently). Neither commit saw my four
  verdicts — items 0d–0g / v2.a–v2.b / 8a–8b + 20.13 / 17.a / TASK-021 reach the worker only via this push.
- **Next:** push the backlog → re-create the gating worktree at `4fc40c8` → `tools/m5r_inputs.sh` → gate **TASK-020
  items 9–11** (20.10–20.12) and re-check the leg-(d) PATTERNS binding against my TASK-018 restrictions.


### Cycle G results (2026-09-25T22:55:00Z) — backlog pushed; three re-gates PASS

- **Pushed** `31ce8dd` → **`a022ef9`** (cycle-F gates + alert + summary + TASK-021 + recovery disclosure). Worktree
  re-created at `4fc40c8` (`/home/user/gate-scratch/w-4fc`), corpus re-materialized (zip `3f36c520…`, 230 transcripts,
  230 census records).
- **Self-correction recorded (append-only):** the `seeded` key **is** present on all 122 adjudication rows, value
  `false` — my TASK-018 parenthetical "the field does not appear" was wrong. The finding stands (0 of 57 `seeded:
  true`; 0 overlaps with the 16 CF fixture spans; the four `seeded: true` rows are the FIX-D2 fixture rows), the
  data-side separation was implemented correctly, and the **false prose has propagated into `PATTERNS.md §5b-bis`** →
  item 0d now covers both documents.
- **TASK-020 items 9–11: FAIL on 20.10 only** (the q4 supplement's `tool_commit` does not contain its generator →
  item 8a extended to all six supplement artefacts). **20.11 PASS** (item 11a: publish per-row tuning-side counts
  1149/49/122 and reconcile 187.9 vs the census-supported 187.6/0.4451). **20.12 PASS** (item 11b: PATTERNS §5e still
  says "98" and "up to 11"). **Item 12 + criterion 20.14**: four fuzzy timestamps (`21:4xZ` ×3, `21:5xZ`, `20:5xZ`) —
  apply the lane's own `generated_utc_exact` + source pattern. Verified independently: all digests MATCH; **13/13**
  toolchain pins byte-identical to `bf97d85`; **B1 zero explicit** with its consequence, and I reproduced the holdout
  side as **185 = 162 + 15 + 8 + 0** from the inherited census; **one-shot discipline proven from the tool's source**
  (0 references to `overlays`/`parse_book_store`/`run_tuning`); §5d's wrong claim left readable and contradicted in
  place, my arithmetic confirming ratio **0.16323**, **8.0/P=0.9363**, **19.9/P=7.677e-05**, **187.6/P=0.4451**;
  SUPERSESSION blocks naming `findings/PROVENANCE.json` as the binding of record (verified `d42136c6…`); and the
  unit-size tally **re-derived exactly** from the ledger's 938 A1 claim notes (max k=12, 9 claims).
- **RE-GATES: q1 PASS · q4 PASS · q5 PASS.** q4 carries its standing restrictions (185/5/12 **receipt only**, B1 zero,
  spent holdout never re-run, precision behind quantum b, both causes unestablished); q5 carries its two (PATTERNS §5e
  not quotable for 98/11 until item 11b; the 27% hyphen sensitivity must accompany any reuse of 938/938). **q2 still
  FAIL** (item 8a + TASK-018 0d–0g); **q3 FAIL on item 8a alone** — one re-pin unblocks its re-gate.
  **M4 scoreboard: q1 PASS · q2 FAIL · q3 FAIL (one item) · q4 PASS · q5 PASS.**
- **Invariants at `4fc40c8`:** ledger `d42136c6…` (1334), by-transcript `c1ec4da8…` (230, my own `dir_digest`),
  `m5r_reduce.py` byte-identical `219075a`→`ffb8811`→`4fc40c8` (`6d4bb9ce…`) → **M5-R PASS stands**; splits
  `481d8513…`/`73d86f0d…`, signals `8d71f57b…`, adjudication `82863ab9…`, SUMMARY `0a37118e…`, fixtures-adjudication
  `61568a9e…`, signals-v2tuning `b25651e4…`, detectors `a0236325…`/`ef9ff4f2…` all unchanged. Suite **227 OK
  skipped=1** (my own run).
- **Next:** read BOSS-2's state for anything addressed to ORCH-2; then write the **quantum-b pre-registration
  protocol** (exactly what must be frozen *before* the single holdout run: thresholds, denominator decision on the 4
  tainted transcripts, expected artefacts, receipt format, abort conditions) so the one-shot evaluation is auditable
  the moment items v2.a/v2.b land.

- **2026-09-25T22:58:11Z:** quantum-b **pre-registration protocol** written as a binding ANNEX of `fleet/queue/pending/TASK-019.md`
  (preconditions A1–A5; frozen inputs B1–B6 incl. the explicit token rule; one-shot run C1–C3 with a pre-registered
  abort rule; required outputs D1–D6; quotable-figure rules E1–E4; new criteria **v2.12–v2.16**). Queue priority
  published for WORKER-2 (8a → TASK-018 0d–0g → TASK-019 v2.a/v2.b → 11a/11b/12/17.a/20.13 → TASK-021); no further
  work added while those are open. BOSS-2 read at `21d9a2b`: **zero CONCERNs, zero controls**, stall watch not fired,
  WORKER-2 described as "idle-cycling @ 4fc40c8 awaiting gate results" — those results are now pushed (`ee4ea5e`).

- **2026-09-25T23:09:35Z: `fleet/ORCH-2-VERIFICATION-LEDGER.md` published** (17 binding rows, 8 M5-R stat rows, 6 census/exposure
  rows, 9 adjudication rows, 3 self-recorded instrument notes, and an explicit "what this does not establish" section).
  Everything re-derived at `4fc40c8`; all bindings MATCH; **13/13 pins three-way**; **9/9 q4 digests**; A1 **938/938**
  a third time; the A1 unit tally term for term; spans **120/120** + 2 verified by a different key; ground-truth quotes
  **57/57**; **16/16** fixture spans offset-exact; **0 of 122 rows live in a fixture-bearing transcript**.
  **Two of my own instrument defects published as §5** (a vacuous overlap test over an absent key; `null == null`
  counted as a byte-exact match) with the rules adopted to prevent recurrence. **Items 13/14 + criteria 20.15/20.16**
  cut (manifest derivation notes not literally reproducible; config digest publishing a subset) — hygiene, queue
  position 4. Comparability of the tuning and holdout configurations **established from the pinned source**, so the §5d
  exposure comparison stands.

- **2026-09-25T23:15:45Z: gate instrument committed** — `fleet/gate-tools/orch2_verify.py` (107 rows; PASS 97 · FAIL 7 · INFO 2 ·
  PROXY 1 at `4fc40c8`; output committed). **FAIL set == open-item set** (8a, 11a, 14, 11b ×2, 12, TASK-018 0d).
  Rules R1/R2 encoded. **§7.1 publishes four defects the instrument found in itself on its first run, two of them
  false PASSes.** Standing rule: an instrument is validated against a head whose answer ORCH-2 already knows before
  its output is trusted. Re-gates are now one run plus an invariance check.

- **2026-09-25T23:29:14Z: instrument v2** — §6 read-scope/one-shot, §7 signal evidence, §8 LAW §8 completeness, §9 self-audit.
  **172 rows: PASS 145 · FAIL 14 · INFO 11 · PROXY 2**; FAIL set still == open-item set. The holdout is provably
  untouched by every tuning-side run (q2 keys set-equal to the v1 tuning 193, ∩ holdout 0, six part manifests zero
  holdout reads; q3 read 197 == v2 tuning; q4 read exactly the 37, ∩ tuning 0, `holdout_consumed: true`). 122/122
  spans, 122/122 citations, 122/122 dropped-word containment. **Timestamp census: 26 asserted fuzzy sites (item 12
  extended), 1 own-time offender (TASK-017 17.a), `fixtures/v2/dropword.json` compliant by exact sibling. Self-audit:
  ORCH-2's own lane asserts 11 fuzzy values → ORCH-2 is an instance of criterion 20.14 and adopts exact-second headers
  plus backticked quotations of fuzzy values.** Defects #5–#9 published (§8.2): apostrophe **normalisation** (not
  inclusion), a regex that matched the suffix of a correct value (19 false offenders → `fullmatch`), run-level vs
  part-level fields, generator mispairing, and citation-vs-instance classification.

- **2026-09-25T23:32:36Z: SELF-ITEM O-1 — my q2.6 caveat `113/9` is WITHDRAWN** (no natural rule reproduces it) and restated: rule A
  gives **8/122 shape-defective, all repetition artifacts**; rule B gives **122/122**; hyphen-splitting gives 67/55, so
  the token rule must travel with the number. The 3+6 decomposition is withdrawn — the "partial-overlap" class was my
  own curly-apostrophe defect. Instrument now **174 rows: PASS 146 · FAIL 14 · INFO 12 · PROXY 2**. q2 verdict
  unchanged. **GitHub push began failing at ~23:29Z** ("could not read Username for https://github.com"); state is
  committed locally, push retried each cycle.

- **2026-09-25T23:39:33Z: second workspace recreation recovered.** Fresh clone at 23:37:06Z left the local branch at base `2ed0b9b`;
  `bd69210` + `cea19ed` lost as objects, content recovered from the surviving tree via `--mixed` reset to `0ae2e9a`
  (registry verified identical three ways first). GitHub restored by the owner. Gate worktree gone, rebuildable on
  demand. CONTROL seq 33.

## Cycle H/I (2026-09-25T23:46:38Z – 2026-09-26T00:26:04Z) — the remaining re-gates became one run, and one of my own findings was reversed

- **Recovery first (CONTROL 33).** A second workspace recreation left the local branch at the branch base while
  `origin` correctly held `0ae2e9a`; two commits were lost as objects but their content survived in the tree.
  Registry verified identical three ways (`a86115d2…`), `git reset --mixed origin/<lane>` (never `--hard`), residual
  diff re-committed with the disclosure → `af1718e`, pushed. Gate worktree rebuilt; the instrument re-ran
  byte-identical and the suite passed 227 OK / skipped=1.
- **Gate cycle H (CONTROL 34–35).** Instrument v3 → v3.1 added §10 (split v2) and §11 (inherited toolchain), so
  TASK-019a quantum a and TASK-017 are now re-gated by one command: **TASK-019a FAIL/INCOMPLETE on v2.5 + the v2.b
  note only** (v2.1–v2.4, v2.6, v2.9 PASS; my independent re-draw set-equal 33/197 under exactly one of two plausible
  readings), **TASK-017 PASS all six** (three-way over all 266 files). Quantum b **HELD**.
- **ANNEX amendment §F (CONTROL 36).** Deriving the taint instead of restating it corrected my own A4 wording: the
  four excluded holdout transcripts are **label-tainted** (7 prior signals, 3 CERTAIN-leg-d + 4 CANDIDATE), not
  fixture-adjacent — the holdout has zero fixture transcripts. §F fixes primary 33 / sensitivity 29 from one run,
  requires those seven re-adjudicated blind with a published prior-vs-new table, and binds the two caveat sentences
  that must ride with every quantum-b figure. Instrument §12: frozen inputs 6/6 undrifted, no pre-registration
  artefact (correct), no receipt consumes the v2 holdout.
- **Self-item O-2 CLOSED (CONTROL 37).** `--selftest`: 18 named cases over extracted helpers, byte-identical section
  output through the refactor, five injected mutations all caught, output committed beside the tool.
- **SELF-CORRECTION O-3 (CONTROL 38) — I reversed my own withdrawal.** The q2.6 figure `113/9` **is** reproducible:
  it is the tally of WORKER-2's published shape adjudication (113 consistent · 5 partial-overlap · 3
  dropped-token-not-missing · 1 gate-boundary-excluded; 122 = 113 + 3 + 6), and my rule-A exclusion set is
  **set-identical to the worker's eight, both directions**. O-1 searched only inside my own five token-set rules and
  so contradicted my own cycle-F record. The token-rule finding stands; the caveat's labels are corrected.
- **New work cut from that derivation:** TASK-020 **item 15** (15a a reconciliation note misnames its own row's
  transcript; 15b two disjoint sets of 114 published under one number, intersection 106); items 0e/0f/0g and
  criterion 20.15 mechanized with derived figures (55 = span-text dedupe, 57 by offset; strata 27/6/11/13 under an
  explicit 32-word list; post-demotion 55 rows / 53 sites; 0/7 holdout rows marked in the adjudication record).
- **Instrument defects #21–#27 published** (cumulative 27), three of them false FAILs against sound criteria and one
  a **process** defect: `str.replace`-based document edits silently no-op, so `status.md` and `ORCH-STATE.md` missed
  this cycle's entries until they were appended and every edit asserted.
- **State:** lane head `0ded97c` → `44dab36` → `6b0cc33` → `8d847bc` → this commit, all pushed. M4 scoreboard
  unchanged (q1 PASS · q2 FAIL · q3 FAIL on item 8a alone · q4 PASS · q5 PASS). No detector promotable, no rate, no
  precision, no M6 figure; M6-P owner-accepted and not re-certified; TASK-015 blocked behind quantum b. Fleet:
  BOSS-2 `67a4f0e` (cycle 45, zero controls, zero concerns, no orders), WORKER-2 `4fc40c8` static since 21:27:50Z —
  no ORCH-2 action per ERRATA-25f, main `7d033ab`.

## Cycle I close (2026-09-26T00:20:51Z) — self-item O-4, and quantum b's criteria pre-registered as rows
- **O-4**: ten of my own header stamps were estimates, eight forward-stamped by up to nine minutes against the lane
  clock (CONTROL seq 38 = `2026-09-26T00:16:59Z`). Disclosed verbatim in `fleet/GATES.md` self-correction #4, left in
  place, authoritative CONTROL stamps published. Standing rule adopted: the CONTROL.log line is written first and its
  stamp copied into every header of the cycle — this entry carries that stamp.
- **Instrument §15**: criteria v2.12–v2.16 pre-registered as HELD rows stating the exact shape each will check
  (pickaxe commit order for v2.12; `holdout_reads` EQUAL to the pre-registered eval set, 33 or the §F2 sensitivity 29,
  for v2.13; eval-dir purity from that path's history for v2.14), plus two precedent rows that PASS today:
  `seeded`/`in_sample` present on 122/122 rows with 0 true, and 0 tuning-side references in
  `tools/m4_q4_supplement.py`'s source. Instrument v3.4 = 261 rows (PASS 207 / FAIL 27 / INFO 25 / PROXY 2),
  `--selftest` 18/18. Defect #28 published (a disclosure check must look inside the disclosure).
- **Fleet**: BOSS-2 `12a0947` (cycle 47, seq 50, zero controls, zero concerns, no orders); WORKER-2 `4fc40c8` static
  since 21:27:50Z (~2 h 52 m) — observation only, no ORCH-2 action per ERRATA-25f; main `7d033ab`.
- **Next**: hold cadence; re-run the instrument the moment WORKER-2 moves (every open item now has a row that flips);
  no new work cut while items 8a, v2.a/v2.b and 0d–0g are open.

## Cycle I close 2 (2026-09-26T00:25:11Z) — the instrument audits its own coverage
- **§16 added**: per-task criterion citation counts (reported **PROXY**, because an uncited id does not prove a
  criterion is ungated), a **ghost check** (0 — no row cites a criterion that exists in no queue file; sub-letters
  traced to their parent; **defect #29**, an id extractor must require an id *shape*, since mine matched the word
  `closure` in my own comment), and the operational row: **all 16 open items are cited by a row that flips when
  repaired** — reached by naming `item 17.a` in the 20.14b row and `item 8b` in the §13 disposition row.
- **Authoritative criterion-to-section map** published in ledger §16, with its honest gaps: TASK-021's 21.1–21.8 are
  unmechanized (task not started, queued last, owed by me when it lands); the C-series of TASK-013/016 and L1–L9 of
  TASK-018 were gated PASS by hand and recorded in `GATES.md`, with no re-gate pending; TASK-014's q-ids are uncited
  because q1/q4/q5 are closed and q2/q3 are open only through items that ARE mechanized.
- Instrument v3.5 = **271 rows** (PASS 210 / FAIL 27 / INFO 25 / PROXY 9), `--selftest` 18/18, golden refreshed. No
  verdict moves; the FAIL set still maps one-to-one onto the open items.

## Cycle I close 3 (2026-09-26T00:36:26Z) — TASK-021 pre-mechanized; the fleet moved, and cycle I opens at `72104a5`

- **Instrument §17** closes the gap §16 named: TASK-021's criteria 21.1–21.8 are pre-registered as rows before the
  task is claimed. Instrument v3.6 = **282 rows** (PASS 217 / FAIL 27 / INFO 30 / PROXY 8), `--selftest` 18/18,
  golden refreshed, **FAIL set unchanged** — pre-registration asserts no verdict.
- Pinned from bytes: the shipped operating point **8/8** from `det_dropword.py`'s module constants (byte-identical at
  `4fc40c8` and `72104a5`); every grid axis contains its anchor; expected table size **8 distinct settings** (11 rows
  if the anchor repeats); denominators **v1 tuning 193 / v2 tuning 197** derived from the split files.
- **Criterion 21.8's floor of 217 is STALE.** Measured in `w-4fc` with the corpus present: `Ran 227 tests in 208.391s`
  → `OK (skipped=1)`. The correction is published here, not edited into the worker's queue file; BOSS-2 cycle 50
  reports **244 OK** at `72104a5`, to be verified in cycle I.
- **PROXY 9 → 8**: §16's TASK-021 citation row went PROXY → PASS on its own, i.e. the coverage meta-gate reported its
  named gap closing in the next cycle.
- **Fleet read `00:35Z` (method fix: `ls-remote` + explicit-refspec fetch — `git fetch origin` alone updates only
  `main` in this clone):** BOSS-2 `12a0947` → `e9d6601` (cycles 48/49/50, seq 51/52/53, zero controls, zero concerns,
  **no orders for ORCH-2**); **WORKER-2 `4fc40c8` → `72104a5`** with three commits: `runs/m4-q2-adjudication/
  SEAL-AUDIT.json` + `SEAL-APPENDIX-2026-09-25.md`, `tools/m4_seal_audit.py` (274) + `tests/test_m4_seal_audit.py`
  (198), `tools/m4_one_shot_v2.py` (377, **TASK-019b harness BUILT, NOT RUN**) + `tests/test_m4_one_shot_v2.py` (250),
  `tools/c2_detectors.py` (48), and branch records `WORKER-2-TASK-019a-DELIVERY.md` / `WORKER-2-TASK-019b-PREP.md`
  whose headline is *split v2 STANDING*; `main` `7d033ab` unchanged.
- **Next: gate cycle I at `72104a5`.** First adjudication is items **v2.a / v2.b** — the seal audit is exactly the
  evidence v2.a demanded, and if it holds, quantum b's blocker lifts and TASK-015 M6 FINAL becomes reachable.


## Cycle I — gate at WORKER-2 `72104a5`: the seal stands, four new items, two self-corrections (2026-09-26T00:52:53Z)

- **Fleet moved** (found by `ls-remote` + explicit-refspec fetch — this clone's refspec is main-only, so plain
  `git fetch` hides lane movement): BOSS-2 `12a0947` → `e9d6601` (cycles 48–50, seq 51–53, zero controls, no orders for
  me); WORKER-2 `4fc40c8` → **`72104a5`**; `main` `7d033ab` unchanged.
- **Gate worktree `w-721`** built at `72104a5`; corpus + evidence materialised and **byte-identical to `w-4fc`**.
- **RULING: the v2 seal STANDS** — 13 of the worker audit's 16 claims verified independently from git bytes; the 3
  mismatches are documentation-class. **v2.5 / v2.10 PASS** on the amended reading; **item v2.a partially landed**;
  **item v2.b unlanded**; **quantum b still blocked**, on four named conditions.
- **New items v2.c / v2.d / v2.e / v2.f** (forward-stamped + self-contradicting `audit_utc`; missing `tool_commit`;
  a 5-row citation census against 10 mentions with the unpaired mentions outside the void check; a fuzzy prep-record
  header). Item 12's census **26 → 27**.
- **O-5**: ANNEX A1 was unsatisfiable as written → amended in the open, with the concrete ask that the **freeze binds the
  companion note's digest**. **O-6**: heartbeat **1h21m stale** → mechanized (`--self-audit`, >20 min = FAIL) and closed by
  a disclosing line.
- **Instrument v3.7 = 306 rows** at `72104a5` (PASS 235 / FAIL 33 / INFO 30 / PROXY 8), 283 at `4fc40c8` (FAIL 27);
  `--selftest` 18/18; **both goldens committed**. FAIL 33 = 26 carried + 7 new.
- **Suite measured**: 227 OK (skipped=1) at `4fc40c8`; **244 OK (skipped=1)** at `72104a5` (= 227 + 10 harness + 7 audit).
- **OPS — GitHub auth failed mid-cycle** (`GH_TOKEN` no longer valid): `b81e86d` (CONTROL 41) and the cycle-I commit are
  **local-only**; push is retried every cycle and the owner may need to reconnect GitHub in Arena. Nothing is lost: both
  goldens and every derived figure are committed locally and reproducible offline.
- **Next**: (1) keep pushing until auth returns; (2) the queue turn for quantum b cannot be issued until v2.b + v2.a(iii) +
  the freeze binding + A2 land, so the queue priority for WORKER-2 is re-published with those four at the top; (3) TASK-021
  stays pre-mechanized and unclaimed.


## Cycle I close (2026-09-26T01:00:20Z) — A2 decided pre-run; the blocker is down to three worker-side conditions

- **ANNEX §G (binding):** the v1-era adjudication set is **EXCLUDED** from quantum b; holdout labels are **fresh and blind**;
  `seeded` never counts toward the rate; lifting is possible **only before the freeze**. A2 is closed, recorded before any
  run, with the holdout unopened.
- **§G2** specifies the freeze binding O-5 asks for (`companion_notes` + refusal on digest mismatch) so the repair is one diff.
- **§G3** verifies *"one draw, not two"* from the two seal blobs (**`manifest` only**, 68 s apart) and §18 mechanizes it:
  substance **PASS**, statement **FAIL** → item v2.a(iii) 2nd half is **documentation-only**.
- **Blocker: three conditions remain** — item v2.b, item v2.a(iii) 2nd half, the §G2 freeze binding. All worker-side, none
  substantive; **quantum b is one delivery away from issuable**, TASK-015 M6 FINAL behind it.
- Instrument **v3.8 = 308 rows** at `72104a5` (PASS 237 / FAIL 33 / INFO 30 / PROXY 8) and **284** at `4fc40c8`
  (FAIL 27); `--selftest` 18/18; **defect #31** (a lane-side check placed behind a head-guarded early return vanishes at
  other heads) found and fixed; both goldens refreshed.
- **OPS: GitHub auth still failed** — `b81e86d` (CONTROL 41), `29bfded` (CONTROL 42) and this commit are local-only; push is
  retried every cycle. Heartbeat and CONTROL lines are written in the same act (O-6).


## Cycle I close 2 (2026-09-26T01:04:16Z) — the harness's refusals are mapped to their tests; item v2.g opened

- **7 of 9** refusal paths in `m4_one_shot_v2.py` are asserted by a test. **Untested:** the parameters-changed branch and the
  **partial-read** refusal → **item v2.g** (two toy tests close it). The partial-read refusal is the one that protects
  quantum b's denominator, so v2.g must close **before the freeze** — it is not a fourth blocker, because the harness has not
  been run.
- **Non-spuriousness verified:** both detectors assign `per_file[n] = sigs` unconditionally, so a zero-signal holdout
  transcript still counts as read; without that, the refusal would fire on every real run.
- **v2.12 precedent strengthened:** both detectors write `holdout_reads` / `holdout_consumed` themselves in holdout mode.
- **Worker suite corroboration:** the two new modules run **17 tests OK in 0.354 s**; the audit tool's VOID logic is tested in
  all five directions, including the toy mutation my append-only ruling rests on.
- Instrument **v3.9 = 311 rows** at `72104a5` (PASS 239 / **FAIL 34** / INFO 30 / PROXY 8) and **284** at `4fc40c8`
  (FAIL 27); `--selftest` 18/18; both goldens refreshed.
- **OPS: GitHub auth still failed** — `b81e86d`, `29bfded`, `be2fff0` and this commit are local-only; push retried each cycle.


## Recovery (2026-09-26T01:21:34Z) — recreation #3, CONTROL 41–44 re-published, cycle J opens at `1c8a287`

- **Auth restored** by the owner; **`.git` had been re-created at the base `2ed0b9b`** while the working tree survived. The four
  unpushed commits are gone as objects; **all content is intact** and re-committed in one recovery commit.
- Recovery followed the cursor's order: `ls-remote` → explicit-refspec fetch → **registry `a86115d2667e7d54…` == `origin/main`**
  → `reset --mixed` to `92c80b3` (never `--hard`) → 14 changed paths, all mine → `--selftest` 18/18.
- **Fleet:** BOSS-2 `1723564` (cycle 58, seq 61, zero controls, **no orders**); **WORKER-2 `1c8a287`**; main `7d033ab`. Both
  gate worktrees lost — rebuilding for cycle J.
- **Cycle J agenda:** item **8a** (unblocks the q3 re-gate) · TASK-018 **0d–0g** · TASK-019 **v2.a/v2.b** (a note *beside* the
  seal — the shape O-5 amended A1 to require) · **15a/15b** · **11a/11b/12** — **plus** re-checking **v2.c–v2.g** at the new
  head, since the worker never saw them.
- **Lesson extended:** commit-quiet is fine, **push-quiet is not** — the fleet reads the lane HEAD.

## 2026-09-26T01:59:14Z — GATE CYCLE J CLOSED at WORKER-2 `1c8a287` (CONTROL seq 46)

- **Instrument v4.0: 322 rows — PASS 267 · FAIL 16 · INFO 31 · PROXY 8** (cycle I: 311 rows, FAIL 34). Golden
  `fleet/gate-tools/orch2_verify_output_1c8a287.txt`; `--selftest` **20/20** (T19/T20 guard the own-time classifier).
- **Suite floor 257** (`Ran 257 tests in 217.2s — OK (skipped=1)`), up from 244 at `72104a5`; criterion 21.8/A5 holds.
- **CLOSED (10+):** TASK-020 items 8a · 8b · 11a · 11b · 12 · 15a · 15b; TASK-018 items 0d · 0e · 0f · 0g; TASK-019 items
  v2.b (all four legs) · v2.f; TASK-017 item 17.a → **TASK-017 PASS**; criterion 20.13.
- **Verdicts:** TASK-013 PASS (six pinned artefacts byte-identical across the range) · TASK-014 **q1 PASS · q2
  FAIL/INCOMPLETE · q3 FAIL/INCOMPLETE (20.15b alone — the q3 re-gate is ISSUED and recorded) · q4 PASS · q5 PASS** ·
  TASK-015 BLOCKED behind quantum b · TASK-017 **PASS** · TASK-018 **FAIL/INCOMPLETE on item 0h alone** · TASK-019
  FAIL/INCOMPLETE (v2.a(iii) 2nd half · v2.c · v2.d · v2.e · v2.g · **v2.h** · §G2 · **§H**) · TASK-020 FAIL/INCOMPLETE
  (13 · 14 · **12c**; 20.15a/b · 20.16 · **20.14c**) · TASK-021 pending (floor 257; 21.6's reading amended by O-8).
- **NEW:** criterion **20.14c** + items **0h** (TASK-018), **v2.h** (TASK-019), **12c** (TASK-020) — 19 own-time stamps
  post-date their commits by +32 to +41 min, `utc_source` false as written, root cause = stamps projected from the CONTROL
  cadence grid. Control: the lane's own census artefact stamped itself from `date -u` 3.8 min before its commit, so this is
  not clock skew. **ANNEX §H**: A4 amended — 29 primary adopted (pre-result, machine-readable, digest-bound, enforced,
  tested), 33 retained as a pre-registered sensitivity from the same run; one sentence owed.
- **REPORTED to BOSS-2 (fleet signals, boss's authority):** WORKER-2's `CONTROL.log` utc column — 9/56 minute-precision,
  2 forward-stamped rows, one backward jump, seq 10–15/38/39/45 each used twice (seq is not a unique key there).
- **Self-corrections O-7** (two pinned "unchanged" rows forbade the append items 0d/0g require — the O-5 pattern again) and
  **O-8** (five rows tested my predicted shape instead of the criterion's substance: generator_pins, appended dispositions,
  11a's rounding, the supersession pattern, a qualified append-only classification). Instrument defects **#32–#38**.
- **CYCLE-K FLAG:** WORKER-2 moved to **`34db0b0`** mid-cycle — items **13** (`fa71443`, new `tools/m4_prov_check.py`) and
  **14** (`d85038c`/`bfc0def`, q4 format config rebuilt so its digest equals q3's `8e7e35a2`) — **and `tools/m5r_reduce.py`
  changed by +46 lines**, so **TASK-013's M5-R PASS must be re-gated at cycle K** before it is quoted again. BOSS-2 unmoved
  at `1723564` (cycle 58, seq 61); main unmoved at `7d033ab`; registry `a86115d2…` verified.
