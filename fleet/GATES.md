# GATES — ORCH-2 (A-2026-09-25-002) · lane arena/01a0d9d0-fleetyard

Independent gate record (append-only). Discipline: LAW §9 per-criterion verdicts — any
failed criterion = milestone INCOMPLETE, never PASS; suite run WITH corpus and skip
counts reported; detector runs reproduced on my own samples; findings spot-checked
against cited bytes; provenance manifests verified (LAW §8); seeded hits never counted
as precision/recall; HIGH requires a written signal-independence rationale; no
certification without held-out/precision evidence. Gates quote shas + fresh-run evidence.
Historical v1 gates live on the archived lane `arena/01a0d5b7-fleetyard` @ `fcc9834`
(`fleet/GATES.md` there) and are imported by reference, never re-stamped.

## Standing inputs (verified this cycle)

- main `25bdab98200074ea89c22944188e948d8b748be2` · registry file sha256
  `a86115d2667e7d54ff418524303c9adeca2348709d233e9e1c39480251435c14` (FROZEN, ERRATA-25d §6)
- policy manifest sha256 `0fe20a6057ec9fa26fdc2184f84352185f8278fb346bc9d9de14927819ffdc85`
- frozen corpus `docdocgo-fixes.zip` sha256 `3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db`
  → 230 transcripts + `manifest.json`; book store `merged-book-texts_json_1.js` sha256
  `c0892fcd20502d49b99fffe87a4ec4b3b5ecc94a1f98606aab7909127934a4a8` (24 slugs: 20 Hawkins
  + `Be_as_you_are`, `I_AM_THAT`, `Lamsa_bible`, `ACIM_workbook` — non-Hawkins never cited)
- gate scratch: detached worktree `/home/user/gate-scratch/worker-aed9df6` at worker head
  `aed9df69bf65f0cc629d9c0e9d77bdd216b647a9` (fetched by explicit refspec); inputs
  materialised read-only by the worker's own `tools/m5r_inputs.sh` (archive ref
  `origin/arena/01a0d581-fleetyard` @ `bf97d85962d5e4950fc75374da6b700744b220b5`)
- my independent checker code: written for this gate, run in the scratch worktree, never
  importing the worker's modules for verification (commands quoted per criterion)

---

## 2026-09-25T19:01Z — GATE: TASK-013 (M5-R reviewed findings ledger) — VERDICT: **FAIL / INCOMPLETE**

- worker lane `arena/01a0d9ce-fleetyard` · delivery commits `8011439` (18:39:57Z) +
  `593cad3` errata (18:46:05Z) · head gated `aed9df6` (18:46:27Z) · main `25bdab9`
- artefacts: `findings/ledger.jsonl`, `findings/by-transcript/*.json` (230),
  `findings/SUMMARY.md`, `findings/REVIEW-QUEUE.md`, `findings/PROVENANCE.json`,
  `findings/README.md`; tools `tools/m5r_reduce.py` (sha256 `c2237ec4792ae8da3f1ad7ddf8b54b2cdc7db42676f2508d5145f3989d190162`),
  `tools/m5r_inputs.sh`, `tests/test_m5r.py`
- delivery labelled DELIVERY (not completion) ✓ — LAW §2.1

### Criterion table

| # | criterion (source) | verdict | independent evidence (my own runs) |
|---|---|---|---|
| C1 | reduction completeness: every inherited raw record → exactly one finding; nothing dropped or invented (PLAN-v2 M5-R) | **PASS** | recounted the archive census myself: 230 record files, **1334 records / 1336 detector instances** (A1 938, A2 158, B1 12, B2 228; combos A1 937, A2 157, B2 228, B1 10, A1+B1 1, A2+B1 1) — identical to v1 `runs/m5-raw/INDEX.md`. Ledger key set `(transcript, char_offset, span_text)` == raw key set exactly: 1334 == 1334, 0 in-ledger-not-raw, 0 in-raw-not-ledger |
| C2 | dedupe + cross-detector merge (PLAN-v2) | **PASS** | 0 same-detector exact duplicates; exactly 2 findings carry 2 detectors — `M5R-0460` (A1+B1 @2318) and `M5R-0461` (A2+B1 @4543), both `Love_Sep_2011_Part_1`, both the v1 fixture spans CF-006/CF-003 → merged to one finding each |
| C3 | adjudication against cited bytes (PLAN-v2; STANDARDS "a finding is a citation") | **PASS** | verified **all 1334** citations myself against the frozen overlays: `text[char_offset:span_end] == span_text` → 0 mismatches; every per-signal `asserted_quote` at its offset → 0 mismatches; 0 citation failures. Book legs: parsed the 24-slug book store with my own regex parser and verified **242/242** `book_quote` byte-exact at the cited slug+offset (absolute-offset convention), `book_chars` agrees 242/242, 0 non-Hawkins citations |
| C4 | classification per STANDARDS ladder (CERTAIN hard leg; HIGH ≥2 independent signals + written rationale; CANDIDATE never blended) | **PASS** | classes recomputed from the ledger: `CERTAIN (inherited fixture)` 3, `HIGH` 0, `CANDIDATE` 1331. All 3 CERTAIN carry fixture id + leg `b` + `status_by` ("WORKER hand-read (TASK-002); re-audited TASK-006: retained CERTAIN") and are exactly CF-015/CF-006/CF-003 — matching v1's "detectors overlap 3 of the 16" claim, re-derived. Tool never assigns CERTAIN (enforced by `test_never_assigns_certain_without_inherited_fixture`). **HIGH 0 independently corroborated**: the only two cross-family convergences in the whole census are the two in-sample fixture spans (C2), so no independent HIGH exists — the worker's rationale holds on my own data |
| C5 | seeded vs independent separated (LAW §9) | **PASS** | seeded 3 / independent 1331; seeded flagged `seeded=true` and excluded from metric language by construction |
| C6 | finding-record shape complete per STANDARDS §"The finding record" | **FAIL** | present in all 1334: transcript, paragraph, char_offset(+span_end), verbatim span, detector ids, evidence/rationale, class, seeded, book refs where doctrinal. **Missing: (a)** `suspected_intended` is absent for **157** findings — all of them A2-nonsense-only spans — with no explicit "not mechanically proposable / requires human read" marker (the 158th A2 signal, `M5R-0461`, has it via the B1 leg); **(b)** no `status` (`open`/`confirmed`/`discarded`) + `status_by` fields as STANDARDS requires — only a uniform `review_status` string ("machine-adjudicated (mechanical bytes only); human confirmation required"). The inherited census carried `status: open` + `status_by`; the ledger dropped them |
| C7 | coverage truth: audited vs pending counts always stated (STANDARDS §"Honesty rules") | **FAIL** | `SUMMARY.md` §11 gives 230 files present, 24 zero-finding transcripts ("not shown clean"), detector coverage and unmeasured classes, and the honesty banner says no human read every transcript — but **nowhere states the audited/pending row** the campaign has carried since v1: human finding-pass audited **0/230**, pending review **230/230**, machine-adjudicated **230/230**. M6 FINAL quotes this ledger; without that row "1,334 findings" reads as 1,334 reviewed errors |
| C8 | provenance manifest binds LAW §8's list (input transcript/book hashes, detector+config digest, tool commit reachable, policy version, output digest) | **FAIL** | present and **recomputed MATCH by me**: `corpus_zip_sha256` `3f36c520…`, `records_digest_sha256` `d8c93536…` (230 files), `fixtures_digest_sha256` `c5d8f6f3…` (2 files), `overlays_digest` `027f82a0…` (230 files), `tool_sha256` `c2237ec4…`, outputs `ledger.jsonl` `62b33da5…` + `by_transcript_digest` `76af4637…` (230), `run_utc`, `archive_ref`. **Missing: (a)** `tool_commit` — no reachable git sha for the producing code; **(b)** policy version/sha (`0fe20a6057ec9fa2…`) and main head; **(c)** book-store sha256 (path only — I verified the file myself: `c0892fcd…`, equal to v1's record); **(d)** detector+config digest for the inherited census (v1 pinned tool `7b8863d`); **(e)** documented derivation for 4 of 5 digests — only `overlays_digest_method` is written down, and its wording ("sorted lines") is ambiguous: sorting the resulting lines gives `58274f46…`, the implemented sort-by-basename gives `027f82a0…` (MATCH). A verifier following the doc literally can falsely reject a good cache |
| C9 | determinism + fresh independent replay (LAW §7/§8: missing fresh evidence is the suspicion) | **PASS** | my own fresh run `python3 tools/m5r_reduce.py --records evidence/runs/m5-raw/records --fixtures evidence/fixtures/confirmed --corpus corpus --out <scratch> --utc 2026-09-25T18:45:45Z` → `1336 raw signals -> 1334 findings (0 dup removed); seeded=3; book refs ok=242 bad=0; citation failures=0`; `diff -r` against committed `findings/` → **identical** except hand-written `README.md` (not tool-generated, disclosed); ledger digest reproduced exactly (`62b33da5…`) |
| C10 | suite green WITH corpus; skip counts reported; test count never drops (STANDARDS tool gate 2) | **PASS** | in the scratch worktree with the corpus materialised: `python3 -m unittest discover -s tests -v` → **Ran 7 tests, OK, 0 skipped, 0 errors**. Count rose 6 → 7 (the errata added `test_fixture_overlap_uses_the_fixture_quoted_span`); no test dropped. `fleet2check selftest` 30/30 rc=0 (separate, policy tool). Note for the campaign ledger: v1's suite was 115 tests — see TASK-017 (the v1 toolchain is not on this lane) |
| C11 | read/write scope, stdlib only, no network (STANDARDS tool gate 4) | **PASS** | imports: argparse, datetime, difflib, hashlib, io, json, os, re, sys, unicodedata — stdlib only; no urllib/socket/requests/subprocess; writes only under `--out` (`ledger.jsonl`, `by-transcript/`, `SUMMARY.md`, `REVIEW-QUEUE.md`, `PROVENANCE.json`, optional `CITATION-FAILURES.json`); reads `corpus/**`, the read-only inherited `evidence/**`, fixtures. Input materialisation is a separate `sh` script (git fetch of a read-only archive ref + sha-pinned unzip, aborts on zip-sha mismatch) |
| C12 | no rates, no precision/recall claims, no completion language (LAW §9/§2) | **PASS** | SUMMARY: "no corpus-wide error rate in this document"; per-detector precision absent by design; delivery record says "DELIVERY, not certification"; CANDIDATE never blended into any figure |
| C13 | limits disclosed honestly | **PASS** | no audio; no human read of the 1331 CANDIDATEs; 24 zero-finding transcripts explicitly not clean (I verified those 24 carry **zero** raw signals in the census, so the zeros are real); drop-word / speaker-format / A4 unmeasured ≠ zero; the 98 non-corroborated A1 claims are review flags, not verdicts (I verified all 98 are CANDIDATE with `review_score ≥ 1`) |

### Verdict

**TASK-013 / M5-R: FAIL — milestone INCOMPLETE** (C6, C7, C8 failed; C1–C5, C9–C13 PASS).
LAW §9: any failed criterion = INCOMPLETE, never PASS. **No certification of M5-R, no
certification of M5, no rate of any kind.** The ledger's substance survived every
independent recomputation I could perform (counts, classes, citations, book bytes,
determinism, scope); the three failures are record-shape, coverage-truth and
provenance-binding instruments — small, precise, and the reason the fleet has gates.

### Brake (ORCHESTRATOR.md step 3)

- `fleet/controls/PAUSE-WORKER-A-2026-09-25-001` issued this cycle (target + date +
  reason per LAW §4.3), scoped to WORKER-2's activation id only — never a wildcard.
- Repair task **TASK-016** cut; its acceptance criteria ARE C6, C7, C8 verbatim.
  A PASS re-gate removes the PAUSE immediately (WORKER.md step 2: the named repair task
  is the only task while paused).
- Not invalidated by this FAIL: the M5-R ledger's verified substance (it stays the input
  to M6 FINAL once repaired), M4 q1's delivered artefacts (gated separately below), and
  the owner-accepted PROVISIONAL M6-P report (never re-certified by me).

---

## 2026-09-25T19:01Z — GATE OPEN (no verdict): TASK-014 q1 (M4 rule catalog + held-out split)

- artefacts: `tools/PATTERNS.md`, `tools/m4_split.py`, `tools/HELD-OUT-SPLIT.json`
  (commit `593cad3`, 18:46:05Z) — observed while gating TASK-013; verdict deferred to a
  full quantum (criteria below are cut now, in TASK-014, so the gate is not retro-fitted).
- observations already on the record (my own runs): `python3 tools/m4_split.py verify
  --split tools/HELD-OUT-SPLIT.json --corpus corpus` → `split verify: OK`, rc=0;
  holdout **37** / tuning **193** / total **230**; the 3 fixture-bearing transcripts
  (`A_Unique_Sedona_Seminar_Dec_2008_Part_2`, `Love_Sep_2011_Part_1`,
  `Satsang_Series_Volume_IX_Part_6`) are forced into TUNING — these are exactly v1's 3
  hand-read transcripts, so no in-sample file can be measured as holdout; the split
  carries method + salt (`fleetyard-m4-holdout-2026-09-25`) + mod + bucket +
  `corpus_files_sha256` `9ae90185…` + an honesty disclosure (v1 detectors were shaped
  with corpus-wide knowledge → a first holdout figure is an estimate under this split,
  not pristine out-of-sample). Committed **before** any detector code exists on this lane
  → "fixed before tuning" (LAW §9) is satisfied on the evidence of commit order.
- `PATTERNS.md` coverage truth re-derived independently: 3 of the 16 CERTAIN fixtures are
  covered by ≥1 raw signal (CF-003, CF-006, CF-015), 13 invisible to all four detectors;
  every precision cell reads **unmeasured**, every "promotable?" cell reads **no**.
- open items I will check in the full gate: per-fixture rule→fixture wiring for all 16;
  the split's `corpus_files_sha256` derivation method (undocumented, same defect class as
  C8e); whether the holdout set is readable by tuning code (it must not be); PATTERNS.md
  provenance binding to the M5-R ledger digest.

---

## Gate queue (order)

1. **TASK-016** (repair of C6/C7/C8) — blocks M5-R PASS, blocks M6 FINAL.
2. **TASK-014 q1** full gate (above) → then q2 (drop-word), q3 (speaker/format),
   q4 (B1/B2 held-out validation + per-detector precision + A4 re-admission decision).
3. **TASK-017** (inherit the v1 toolchain with provenance) — prerequisite for q2–q4.
4. **TASK-015** (M6 FINAL) — blocked until 1–3 gate PASS; no headline rate without
   held-out/precision evidence (LAW §9); CERTAIN and HIGH reported separately;
   CANDIDATE never blended; M6-P stays owner-accepted PROVISIONAL, never re-certified.

---

## 2026-09-25T19:06Z — NOTE (append-only): owner rulings reported by WORKER-2, and what they do not do

- WORKER-2 @ `e07be0e` logs owner ruling 1 (the nonce-shaped literal published at
  `2ed0b9b` is INERT AND RETIRED; v0 posture `UNHASHED-OWNER-CHAT-ONLY`; boot nonces are
  single-use, consumed at boot verification) and owner ruling 2 (manifest pin `4b65145d…`
  is the policy-bundle SOURCE file; deployed `fleet/ERRATA-2026-09-25c.md` `7384a608…` is
  the instrument OF RECORD; reconciliation deferred to policy 2.0.1; the freeze extends to
  the manifest). If confirmed by the owner (this session or a dated record on main) these
  close boot-table item C6's deviation note and §10 items 1 and 3 of
  `fleet/branches/ORCH-2-BOOT-VERIFICATION.md`. Recorded as REPORTED: a report of chat by
  another lane is not the owner (LAW §1.4; CANON 13 — authority exists only as a verifiable
  instrument). No gate verdict changes on the strength of a reported ruling.
- "M4 q1 approved" (owner, per the same log, explicitly PROVISIONAL-UNGATED) is not a gate.
  Owner approval changes what may be worked on; it does not certify evidence (LAW §2.2, §9).
  The TASK-014 q1 gate above stays OPEN until I complete it on its own criteria.
- The TASK-013 FAIL verdict is evidence-bound: it can only be cleared by the TASK-016
  repair plus a PASS re-gate, not by an order. `PAUSE-WORKER-A-2026-09-25-001` stands until
  then unless the owner lifts it (S-tier is the owner's), which I have escalated rather than
  assumed.

---

## 2026-09-25T19:58Z — RE-GATE: TASK-016 (repair of C6/C7/C8) → M5-R — VERDICT: **PASS**

- Re-ground instruments read this cycle (owner, on main): `fleet/ERRATA-2026-09-25e.md`
  @ main `8e9e179` (blob `33ed84b9`, bytes sha256 `b051d4e4f7caef5b9152cb5d57ae3f69dcba8ef07fde97ca0850b6f0722af54e`)
  — OPTION A repair-first, M4 parked, STANDARDS gains narrow CERTAIN **leg (d)**; and
  `fleet/ERRATA-2026-09-25f.md` @ main `77f1d6d` (blob `7a77597e`, bytes sha256
  `c8a1634d55af3eb8bd6476a2d7356332a1fedd492979879855f096495232ddc2`) — liveness doctrine
  (signals, not output), worker steady state, orchestrator queue discipline, boss CONCERN
  scope, owner-pump minimisation, turn-end rule.
- Order served and acknowledged: BOSS-2 `fleet/ORDERS/REDIRECT-008.md` (issued 19:43:00Z,
  ack due 19:58:00Z) → acked 19:57:21Z @ `5f6d698` (fleet/ORDERS/ACK-REDIRECT-008.md).
- Gated head: WORKER-2 `arena/01a0d9ce-fleetyard` @ `1beadd9151331168f528940a303ffc36a1af222f`
  (19:40:07Z). Repair chain: `dada3e6` (19:17:57Z, R1/R2/R3 + 3 tests) → `a4c6655`
  (19:18:25Z, provenance rerun pinned to `dada3e60`) → `1beadd9` (19:40:05Z, per-criterion
  evidence + manifest re-bound to main `8e9e179`).
- Artefacts gated: `findings/ledger.jsonl` sha256 `d42136c673188f9e091526083b95941cabc5822a8b5cffeb8913b942cb658a32`,
  `findings/by-transcript/*.json` (230) digest `c1ec4da86a6ce4f43bb9f5a4da8677e28c2f9e3d781e6409c4a0d84ab06174af`,
  `findings/PROVENANCE.json`, `findings/SUMMARY.md`, `findings/README.md`,
  `findings/REVIEW-QUEUE.md`, `findings/M4-q5-A1-CLAIM-RECONCILIATION.md`;
  `tools/m5r_reduce.py` sha256 `6d4bb9ce78f2964efeb74cae0855ab63234f3c34966e57d0cdcae726a749574d`.
- Gate scratch: fresh detached worktree `/home/user/gate-scratch/worker-1beadd9`; inputs
  materialised read-only by the worker's own `tools/m5r_inputs.sh` (archive ref
  `origin/arena/01a0d581-fleetyard`, corpus zip sha `3f36c520…` verified by the script and
  by me). All verification code below is mine, written for this gate, and does not import
  the worker's modules.
- **Evidence is fresh for every criterion.** Nothing is inherited from the 19:01Z gate: the
  ledger digest changed (`62b33da5…` → `d42136c6…`) because the repair added four fields and
  because the worker's errata #2 (M4-q5) fixed two reducer defects, so every criterion was
  re-run against `1beadd9` (LAW §7: missing fresh evidence is the suspicion).

### Criterion table (all thirteen re-verified at `1beadd9`)

| # | criterion | verdict | independent evidence (my own runs at `1beadd9`) |
|---|---|---|---|
| C1 | reduction completeness (every inherited raw record → exactly one finding) | **PASS** | recounted the archive census myself: 230 record files, **1334 records / 1336 detector instances**; ledger key set `(transcript, char_offset, span_end, span_text)` == raw key set exactly (1334 == 1334, 0 either way); per-file record counts == per-file finding counts for all 230 files; per-detector A1 938 / A2 158 / B1 12 / B2 228 and combos A1 937, A2 157, B2 228, B1 10, A1+B1 1, A2+B1 1 — unchanged from the census |
| C2 | dedupe + cross-detector merge | **PASS** | `duplicates_removed: 0`; exactly 2 findings carry 2 detectors — `M5R-0460` (A1+B1 @2318) and `M5R-0461` (A2+B1 @4543), both `Love_Sep_2011_Part_1`, both v1 fixture spans CF-006/CF-003 |
| C3 | adjudication against cited bytes | **PASS** | all **1334/1334** spans: `overlays[transcript][char_offset:span_end] == span_text`, 0 failures; all **1336/1336** per-signal `asserted_quote` at `offset`/`quote_len`, 0 failures, `quote_verified` true on all; **242/242** book quotes byte-exact at cited slug+offset under my own 24-slug store parser (`book_chars` agrees), **0 non-Hawkins** citations |
| C4 | classification per the STANDARDS ladder | **PASS** | recomputed from the ledger: `CERTAIN (inherited fixture)` **3** (M5R-0078/CF-015, M5R-0460/CF-006, M5R-0461/CF-003 — all leg `b` in `evidence/fixtures/confirmed/confirmed.json`), `HIGH` **0**, `CANDIDATE` **1331**. Tool cannot self-assign CERTAIN (`test_never_assigns_certain_without_inherited_fixture`); `classify()` untouched by the repair (I read the full tool diff `aed9df6`→`dada3e6`: only TOKEN_RE, kmax, `adjudicate(...,meta)`, R1 fields, SUMMARY/coverage rendering, CLI pins, stats.coverage). **Leg (d) applied nowhere** — correct: ERRATA-25e §3 requires individual adjudication first (TASK-018); no detector hit auto-classifies |
| C5 | seeded vs independent separated (LAW §9) | **PASS** | seeded **3** / independent **1331**; all three seeded carry `fixture_overlap: true` and rationales stating in-sample/not admissible as precision evidence; SUMMARY states the split and excludes seeded from any metric by construction |
| C6 | STANDARDS finding-record shape (was **FAIL**) | **PASS** | my own read of all 1334 records: `suspected_intended` present on **1334/1334** (157 explicit `null` — exactly the A2-nonsense-only spans — each with `suspected_intended_status: "not proposable mechanically; human read required"`); `status` present 1334/1334 with vocabulary `{open: 1334}` (STANDARDS' open/confirmed/discarded); `status_by` present 1334/1334 = "machine-adjudicated by tools/m5r_reduce.py@dada3e60…; human confirmation required" (who + why); non-null intents are labelled "from runner signal (…); **not gate-verified** — human read required" — no self-certification. Regression test `test_standards_finding_record_shape_is_complete` is substantive (asserts the fields, the vocabulary and the null-marker) |
| C7 | coverage truth (was **FAIL**) | **PASS** | row printed verbatim in `findings/SUMMARY.md` §0 and `findings/README.md`: `transcripts 230 | detector-run 230 | machine-adjudicated 230 | human finding-pass audited 0 | pending human review 230 | zero-finding transcripts 24 (not shown clean)`; titles qualified ("reviewed" = machine-adjudicated). I recomputed every number myself: 230 overlay texts, 230 record files (one per transcript → detector-run is evidenced by record-file presence, including the 24 files with zero signals), 206 transcripts with findings, 24 with none, and those 24 carry **zero** raw signals in the census (so the zeros are real, not missing runs). `stats.coverage` in the manifest matches my recount exactly. Test `test_coverage_truth_row_is_emitted` asserts the row and the counts |
| C8 | LAW §8 provenance manifest (was **FAIL**) | **PASS** | every binding recomputed by me and **MATCH**: overlays `027f82a0…` (230, sort-by-basename text-mode as documented), records `d8c93536…` (230), fixtures `c5d8f6f3…` (2), tool `6d4bb9ce…` == sha256 of `tools/m5r_reduce.py` **and** == the blob at `tool_commit dada3e602689cb900971fda0dccce8267f31a2b2` (verified `git cat-file`; `git merge-base --is-ancestor dada3e6 1beadd9` → reachable), `policy_sha256 0fe20a60…` == sha256 of `fleet2/POLICY-MANIFEST.sha256` (re-verified at main `77f1d6d`, unchanged), `main_head 8e9e179…` == main at run time, `book_store.sha256 c0892fcd…` == my recomputation of the frozen store, `corpus_zip_sha256 3f36c520…`, outputs `ledger.jsonl d42136c6…` + `by_transcript_digest c1ec4da8…` == my recomputations, `inherited_census.detector_tool_commit 7b8863d` **reachable** (`merge-base --is-ancestor` on `origin/arena/01a0d581-fleetyard`) with detector set + exclusions named, and a written derivation for **all seven** digest fields — including the trap I raised at 19:01Z (sorting the digest *lines* gives `58274f46…`; the implemented sort-by-basename gives `027f82a0…`). Pins are explicit CLI args whose defaults fail closed to the literal `UNPINNED`: my deliberately unpinned replay emitted `"sha256": "UNPINNED"` and `status_by …@UNPINNED` — provenance is never silently inherited or stamped. Test `test_law8_manifest_bindings_and_derivations` asserts the bindings and the trap string |
| C9 | determinism + fresh independent replay | **PASS** | my own run `python3 tools/m5r_reduce.py --records evidence/runs/m5-raw/records --fixtures evidence/fixtures/confirmed --corpus corpus --out <scratch> --utc 2026-09-25T19:39:48Z --archive-ref origin/arena/01a0d581-fleetyard --tool-commit dada3e60… --main-head 8e9e179… --policy-sha 0fe20a60… --book-store-sha c0892fcd… --detector-tool-commit 7b8863d` → `1336 raw signals -> 1334 findings (0 dup removed); seeded=3; book refs ok=242 bad=0; citation failures=0`; `diff -r` vs committed `findings/` → **byte-identical** for every common file (ledger `d42136c6…`, by-transcript aggregate `c1ec4da8…`); the only extra committed file is the hand-written `findings/M4-q5-A1-CLAIM-RECONCILIATION.md` (disclosed, not tool-generated), as `README.md` was at the previous head |
| C10 | suite green WITH corpus, skip counts, count never drops | **PASS** | in the scratch worktree with the corpus materialised: `python3 -m unittest discover -s tests` → **Ran 26 tests … OK**, **0 skipped, 0 errors**. Count rose 7 → 26 (M5-R 12 + drop-word 8 + format 6); no test dropped. Note for the record: 14 of the 26 belong to the **parked** M4 q2/q3 detectors — running them proves the lane is green, it does **not** gate that work |
| C11 | read/write scope, stdlib only, no network | **PASS** | imports at `1beadd9`: argparse, datetime, difflib, hashlib, io, json, os, re, sys, unicodedata — stdlib only; no urllib/socket/subprocess/requests; writes only under `--out` (ledger, by-transcript/, SUMMARY.md, REVIEW-QUEUE.md, PROVENANCE.json, optional CITATION-FAILURES.json); reads `corpus/**` + the read-only inherited `evidence/**` + fixtures. Input materialisation stays a separate `sh` script that fetches a read-only archive ref and aborts on zip-sha mismatch |
| C12 | no rates, no precision/recall claims, no completion language | **PASS** | SUMMARY: "no corpus-wide error rate in this document"; corroboration table is counts only (938/938, 158/158, 12/12, 228/228); seeded excluded from metrics by construction; delivery record says DELIVERY not certification; the repair section claims no rate. (The parked q4 holdout artefacts also claim counts only — "precision unmeasured" — and are **not** certified by this gate.) |
| C13 | limits disclosed honestly | **PASS** | no audio heard; no human read of the 1331 CANDIDATEs; 24 zero-finding transcripts explicitly "not shown clean" (I verified the zeros are real); drop-word / speaker-format / A4 unmeasured ≠ zero; errata #1 and #2 both disclose that the *instrument* was wrong, with regression tests and append-only records; the withdrawn 98 flags are disclosed with their cause. `REVIEW-QUEUE.md` regenerated with **0** stale "not re-derived" rows (I grepped) |

### Errata #2 (M4-q5 reducer fix) — independently re-verified, because it changed the ledger

The ledger I gated at 19:01Z (`62b33da5…`) is superseded by `d42136c6…`. My own
field-by-field diff of the two (1334 keys identical, 0 removed):

- **Added** on all 1334: `suspected_intended`, `suspected_intended_status`, `status`,
  `status_by` (the R1 repair) — as claimed.
- **Values changed** on: `signals` 98, `claim_checks` 98, `claims_all_corroborated` 98
  (false→true), `rederived_repetition` 98, `review_score` 99, `book_checks` 144 findings
  (**146 entries, and only their `divergence` sub-field** — `book_quote`, `offset`,
  `quote_ok`, `offset_ok`, `book_chars`, `slug` all unchanged).
- Cause (disclosed, errata #2): `TOKEN_RE` `[A-Za-z']+` → Unicode `[^\W_]+(?:['’\-][^\W_]+)*`,
  and `repetition_rederive` `kmax` 8 → 16. Both changes are in the M5-R reducer itself, so
  they are inside this gate's scope, and I verified them myself rather than trusting the
  errata: I wrote my own implementation of the documented rule (lowercase + Unicode tokens,
  full-period search, then longest-run ≥3 over all start offsets) and re-derived all **938**
  A1 spans — my structure equals the ledger's `rederived` on **938/938**, and the runner's
  claimed `N-token unit × M repeats` holds under my derivation on **938/938** (the one
  apparent exception, M5R-1084, was my own test comparing only `longest_run`; the span is
  fully periodic 8×3 exactly as the ledger's note says "claim 8-token x3 vs re-derived 8 x3").
  So the withdrawal of the 98 flags is **correct**, not convenient: those flags were my
  instrument's defect class, exactly as LAW §7 warns.
- The `divergence` changes on 146 book-check entries are the same tokenizer's downstream
  effect on word-level alignment (e.g. `it s` → `it's`); they alter no quote, no offset, no
  ok-flag, no class. **Observation (non-blocking):** errata #2 names the tokenizer fix but
  does not enumerate this downstream field, and the repair record's "substance stability
  (no quiet edit)" paragraph lists only the four added fields. Recorded here so the change
  is on the gate record; no count, class or citation is affected.

### Verdict

**TASK-016 = PASS. TASK-013 / M5-R = PASS — milestone COMPLETE (gated), not certified.**
All thirteen criteria pass on fresh independent evidence at `1beadd9`. Consequences, stated
plainly:

- `fleet/controls/PAUSE-WORKER-A-2026-09-25-001` is **REMOVED** (marked, never deleted) —
  automatically, per its own removal clause, owner ERRATA-25e §1 and REDIRECT-008 §2.3.
- **M5-R is gate-PASS, NOT CERTIFIED.** Certification of a milestone is the owner's
  declaration (LAW §2.2) and M6 FINAL still owes held-out/precision evidence; no rate of any
  kind exists or is implied by this PASS. M6-P stays owner-accepted PROVISIONAL and is not
  re-certified.
- The ledger at `d42136c6…` is the verified input to M6 FINAL.

### Observations carried forward (non-blocking, each with an owner or a task)

1. **Doc contradicts artefact (correction owed).** `findings/M4-q5-A1-CLAIM-RECONCILIATION.md`
   row 3 says M5R-0036 re-derived as "period 2 (`Mm-hmm` = 2 tokens in the Unicode rule),
   8 repeats — claim reads the unit as 1 token … a labelling nuance". The artefact says
   otherwise: under the actual rule `Mm-hmm` is **one** token, the span is 8 tokens, and the
   ledger records `unit_tokens 1, repeats 8` with the note "claim 1-token x8 vs re-derived
   1 x8" — claim and derivation agree exactly, and the nuance the doc invents does not exist
   (I tokenised the span myself: `['mm-hmm'] * 8`). No number or class is wrong; the narrative
   is. Correction owed as an append-only line — folded into TASK-018 item 0.
2. **STANDARDS.md on main does not carry leg (d).** At main `77f1d6d` the deployed
   `STANDARDS.md` (sha256 `1e38a345ef72dba44a01051a854f46daff350f7719635f59a737b1cdf80882e7`)
   still lists CERTAIN legs (a)/(b)/(c) only; leg (d) exists solely in `ERRATA-2026-09-25e`
   §2, which §4 declares to be the recorded errata + BOSS CONCERN the taxonomy change
   requires. That is a valid instrument and I gate by it, but any lane reading STANDARDS.md
   alone will not know leg (d) exists. I never write main; **owner item**: fold (d) into
   STANDARDS.md at the next owner edit (2.0.1 window). Until then my standing guidance below
   is the gate-side restatement.
3. **§8 literalism, two residuals.** (a) "detector+config digest" is satisfied by a
   *reachable commit pin* (`7b8863d`) plus the named detector set and exclusions — at least
   as strong as a digest, but not literally one; a `git ls-tree` digest of that commit's
   `tools/` would close the wording. (b) §8's "resume rejects missing/mismatched provenance"
   has no resume path to act on: the reducer always recomputes fresh and unpinned bindings
   fail closed to `UNPINNED` (verified by my unpinned replay). A `--verify-manifest` mode is
   the clean 2.0.1 fix. Neither blocks this PASS; both are recorded as owner items.
4. **Bracket convention.** STANDARDS asks for the quoted transcript text "verbatim,
   bracketed"; the ledger carries it verbatim in `span_text` and the rendered queue delimits
   it with backticks. Met in substance; no action.

---

## Standing classification guidance — CERTAIN leg (d) (re-cut per owner ERRATA-2026-09-25e §2, in force)

Authority: `fleet/ERRATA-2026-09-25e.md` §2–§4 @ main `8e9e179` (owner instrument; §4 is the
recorded errata + BOSS CONCERN that STANDARDS requires for a taxonomy change). This restates
it for gate use; it does not extend it.

**Leg (d) — OMISSION WITHIN A MATCHED SPAN (narrow).** A finding may be classified CERTAIN
under leg (d) only when **all** of the following hold, each cited to bytes:

1. The transcript contains a span that **purports to quote, cite or closely track**
   identifiable ground truth — either (i) a Hawkins book passage, or (ii) the transcript's
   **own immediately adjacent repetition** of the same phrasing.
2. A word **clearly present in that ground-truth span** is **absent** from the transcript
   span.
3. **Restoring the word completes the match** (the restored transcript span then agrees with
   the ground truth under the campaign's byte/quote conventions).

**Never leg (d):** omissions outside such matched spans — a lecture's free paraphrase of a
book, disfluency, compression, or any span with no identified ground truth — remain
**CANDIDATE** unless they independently satisfy leg (a) (ungrammatical/senseless AND an
acoustically near-form replacement restoring grammar and doctrinal sense). A detector hit is
**evidence of a span, never a classification**: the 122 drop-word signals and the 4
provisional fixtures are SIGNALS and PROVISIONAL respectively (ERRATA-25e §3) and each needs
**individual adjudication** under LAW §9 before any CERTAIN/HIGH assignment.

**Gate criteria I will apply to any leg-(d) claim (TASK-018, and M4 q2 re-gate):**

- L1 per-finding record: transcript + offsets + verbatim span; the **ground-truth span**
  cited to bytes (book slug + offset + verbatim passage, or the adjacent-repetition offsets
  in the same transcript); the **omitted word**; the **restored span**; and which leg clause
  (d)(i) or (d)(ii) is claimed.
- L2 my own re-derivation of every citation (book bytes from the frozen store with my own
  parser; adjacency from the frozen overlay) — byte-exact or the claim fails.
- L3 restoration check: the restored span must match the ground truth under the campaign
  conventions, and the restoration must be the **minimal** edit (one word); anything larger
  is a paraphrase, not leg (d).
- L4 no blanket promotion: a rule, threshold or detector name is never accepted as a
  classification reason; adjudications are per finding, and counts are reported per clause.
- L5 seeded/in-sample findings stay separated (LAW §9) and are never precision evidence;
  the 4 provisional fixtures are in-sample by construction.
- L6 class vocabulary unchanged elsewhere: HIGH still needs ≥2 independent signals **plus a
  written signal-independence rationale**; CANDIDATE is never blended into any figure; no
  rate without held-out evidence fixed before tuning.

---

## 2026-09-25T20:08Z — GATE: TASK-014 q1 (M4 rule catalog + held-out split) — VERDICT: **FAIL / INCOMPLETE** (one criterion)

- gated at WORKER-2 head `1beadd9` (main `77f1d6d`); artefacts `tools/PATTERNS.md`
  (sha256 `528265e74816a79eaae04ca841daedd546f97a4b6ed01ea8b15a587403b82beb`, changed from
  `8dc1c067…` at delivery `593cad3`), `tools/m4_split.py`, `tools/HELD-OUT-SPLIT.json`
  (sha256 `481d8513a040ba05dc31ac1ab566ffd5a4b2ac7a0def932bb97cd5f08cb51235` — **byte-identical
  to the delivered seal**, so the split has not moved since it was fixed).
- criteria are the ones I cut at 19:01Z (TASK-014 q1.1–q1.4), not retro-fitted.

| # | criterion | verdict | independent evidence (my own runs) |
|---|---|---|---|
| q1.1 | PATTERNS.md maps every CERTAIN fixture to a pattern + rule sketch + whether a current detector catches it; coverage truth re-derived from the ledger | **PASS** | all **16/16** confirmed fixtures are wired: P1 CF-001/002 · P2 CF-003/019/020 · P3 CF-006 · P4 CF-007/008/010/011/017/021/022 · P5 CF-015 · P6 CF-012 · P7 CF-004, each with a rule sketch and a "caught by" column. Coverage truth re-derived **by me from the gate-PASS ledger**: exactly CF-003 (`M5R-0461`), CF-006 (`M5R-0460`), CF-015 (`M5R-0078`) carry ≥1 raw signal → **3/16**, the other 13 invisible to all four detectors — the doc's numbers match my own re-derivation, and the doc calls that gap "the honest headline of this page" |
| q1.2 | held-out split fixed before any tuning, deterministic, published, sealed (method + salt + mod + bucket + corpus digest), fixture transcripts forced to TUNING, honesty disclosure | **PASS** | **fixed before tuning, on commit-order evidence**: at `593cad3` (18:46:05Z) `tools/` held only `HELD-OUT-SPLIT.json`, `PATTERNS.md`, `m4_split.py`, `m5r_reduce.py`, `m5r_inputs.sh` — no detector code; `tools/det_dropword.py` first appears at `012914d` (19:06:53Z). **Deterministic + reproducible by me**: I re-derived the whole split with my own code from the published rule `int(sha256("fleetyard-m4-holdout-2026-09-25"+basename),16) % 5 == 0 → HOLDOUT` → **holdout 37 / tuning 193**, and my holdout and tuning **sets are equal to the published ones** (0 differences); the per-year table matches too (my only discrepancy was a zero-key artefact of my own counter for 2010). **Seal complete**: `salt`, `mod 5`, `holdout_bucket`, `method`, `counts`, `corpus_files 230`, `corpus_files_sha256`, `disclosure`, `fixture_transcripts_forced_tuning`. The 3 fixture-bearing transcripts (v1's hand-read files) are in TUNING and **not** in holdout (I checked set membership). `python3 tools/m4_split.py verify --split tools/HELD-OUT-SPLIT.json --corpus corpus` → `split verify: OK`, rc=0 |
| q1.3 | per-detector status table with precision **unmeasured** and promotable **no**; seeded/in-sample never presented as precision | **PASS** | table read cell by cell: A1 938 / A2 158 / B1 12 / B2 228 raw signals; **every precision cell "unmeasured"**, **every promotable cell "no"**; A4-confusion, drop-word and speaker/format rows all "unmeasured / no". The fixture-recall column (1/16, 1/16, 2/16, 1/16) is labelled as fixture recall and the page states fixtures are **in-sample by construction** (LAW §9) and that v1's clean-set 0/59 is invalid as an independent FP estimate. No rate, no blended figure anywhere on the page |
| q1.4a | rule→fixture wiring for all 16 | **PASS** | see q1.1 (16/16 wired, no fixture orphaned, no pattern without fixtures) |
| q1.4b | `corpus_files_sha256` derivation documented and reproducible | **PASS** | documented in `HELD-OUT-SPLIT.json.method` + PATTERNS.md §4 + the generator source (`sha256_text("\n".join(files) + "\n")` over the sorted overlay basenames). I reproduced it independently: `sha256("\n".join(sorted(230 overlay basenames))+"\n")` = `9ae90185ac0f4030eff135d28f7185b2c2f2c1a59269d150816a447293bd998f` = the published value **MATCH** (this is the defect class I failed C8e on at 19:01Z; here the derivation is written down and verifies) |
| q1.4c | tuning code demonstrably unable to read the holdout list | **PASS** (with a recorded nuance) | structural: `run_tuning()` loads the split, raises `SystemExit` on any tuning∩holdout overlap, filters to `split["tuning"] − holdout`, and `assert`s no holdout transcript is in a tuning run; holdout evaluation is a separate `which="holdout"` one-shot mode documented as spending the holdout. Empirical, on the parked q2/q3 outputs (checked as evidence for **this** criterion only, not as a gate of that work): `runs/m4-q2-dropword/signals.json` keys = **193**, ⊆ tuning, **∩ holdout = 0**, 122 signals; `runs/m4-q3-format/signals.json` keys = **193**, ⊆ tuning, **∩ holdout = 0**, 49 signals; the q4 holdout artefacts key exactly the **37** holdout files with `holdout_consumed: true`, the full `holdout_reads` list, and the split salt + `split_corpus_files_sha256 9ae90185…` bound. Nuance recorded honestly: the same module *contains* a holdout mode (it must, for q4), so the guarantee is separation + assertion + output evidence, not literal inability |
| q1.4d | PATTERNS.md bound to the M5-R ledger digest it quotes | **FAIL** | PATTERNS.md §2–§3 quote M5-R-derived figures (coverage 3/16; corroboration **938/938 · 158/158 · 12/12 · 228/228**; fixture recall per detector) but carry **no binding to the ledger they came from** — I grepped the file for `d42136c6…`, `62b33da5…`, `ledger.jsonl`, `PROVENANCE`: the only digest-shaped lines are the q2 `signals.json` sha (`8d71f57b…`) and a §8 checklist sentence. The figures are correct **today** (I re-derived them from the gate-PASS ledger `d42136c6…`), and they were *changed* by errata #2 at `1beadd9` — which is exactly why a quoting document must pin its source: a reader cannot tell which ledger generation a number came from, and the next ledger change would silently stale the page. LAW §8's rule is binding for records, not only for caches |

### Verdict

**TASK-014 q1 = FAIL / INCOMPLETE** (q1.4d failed; q1.1, q1.2, q1.3, q1.4a–c PASS).
LAW §9: any failed criterion = INCOMPLETE, never PASS. The split itself — the load-bearing
instrument for every future precision figure — is **verified clean and unmoved since it was
sealed**; the failure is a provenance binding on the catalogue page.

### Brake decision, and why it deviates from ORCHESTRATOR.md step 3 (recorded, not silent)

Step 3 says FAIL → PAUSE + repair task. I am **not** issuing an activation-scoped pause here,
and I record the reasoning so it can be overruled:

1. Scope of the defect: a missing source binding in a **parked** quantum's catalogue page. No
   count, class, citation, seal or split is affected; nothing downstream inherits an error.
2. A pause's effect is "only the named repair task is actionable" (WORKER.md step 2). The
   worker's next task is **owner-ordered** (ERRATA-25e §3 → TASK-018, leg-(d) adjudication),
   and M4 work is now resumable by the same errata once M5-R PASSed. Pausing to enforce a
   one-line doc binding would contradict a standing owner order and idle the fleet
   (ERRATA-25f §3/§6: the fleet self-runs; the owner is not the pump).
3. The restriction I do apply is **artefact-scoped and fail-safe**: TASK-014 q1 is
   **INCOMPLETE and may not be cited as passed**; no M4 promotion, no gate credit for q2–q5,
   and no M6 FINAL figure may rest on PATTERNS.md until the binding lands.
4. Queue discipline (ERRATA-25f §4): the repair is folded into **TASK-018 item 0b** rather
   than cut as a new task, so the open worker queue stays at two (TASK-018, TASK-017).
5. If BOSS-2 or the owner reads step 3 as requiring a pause on any FAIL regardless of scope,
   say so and I will issue one in the same cycle — the deviation is argued here, not hidden.

### Hygiene note (resolved, with evidence)

`593cad3` committed 2 `.pyc` files under `tools/__pycache__`; at `1beadd9` there are **0**
`__pycache__`/`.pyc` paths in the tree and a lane `.gitignore` now excludes `corpus/`,
`evidence/`, `__pycache__/`, `*.pyc`. Self-corrected; no action owed.

### 2026-09-25T20:12Z — ADDENDUM (append-only): M5-R PASS **re-affirmed at WORKER-2 head `219075a`**

The worker pushed two commits after the head I gated (`1beadd9` → `10afc0d` → `219075a`,
19:55–19:56Z): an ERRATA-25f re-ground, a workspace-reset recovery, a provenance-only
manifest re-run and a new ops utility. I re-verified rather than assuming:

- **Delta is provenance-only, as claimed.** `git diff --stat 1beadd9 219075a` →
  `findings/PROVENANCE.json` (2 values: `main_head` `8e9e179…`→`77f1d6d…`, `run_utc`
  `19:39:48Z`→`19:55:24Z`), `findings/SUMMARY.md` (one line: the generation timestamp),
  the worker's own logs, and `tools/cadence_watch.py` (new). **`findings/ledger.jsonl`
  sha256 `d42136c6…` unchanged; `by-transcript` digest `c1ec4da8…` unchanged; coverage block
  unchanged; `tool_commit dada3e60…` and `tool_sha256 6d4bb9ce…` unchanged; policy
  `0fe20a60…` unchanged and still equal to sha256(`fleet2/POLICY-MANIFEST.sha256`) at main
  `77f1d6d`; new `main_head 77f1d6d…` is reachable and current.**
- **Fresh pinned replay at `219075a` is byte-identical** (my own run, `--utc
  2026-09-25T19:55:24Z --main-head 77f1d6d…`): `1336 raw signals -> 1334 findings (0 dup
  removed); seeded=3; book refs ok=242 bad=0; citation failures=0`; `diff -r` vs committed
  `findings/` clean apart from the two hand-written docs; `PROVENANCE.json` reproduced
  byte-for-byte (sha256 `921bbc566016b2dc3fe9da76dc43075f7a7f77f047a1c45953cb85b6507f33b4`).
- **Suite at `219075a`**: `Ran 26 tests … OK`, 0 skipped. Count did not drop.
- So the **M5-R PASS stands at `219075a`**, and the gate-PASS ledger for M6 FINAL is
  `d42136c6…` (unchanged by the re-run). Still **not certified**; still **no rate**.
- **Observation (new tool, non-blocking):** `tools/cadence_watch.py` (93 lines, stdlib +
  `subprocess` for `git fetch`/`git log`) appends to `fleet/heartbeats/WORKER.log` and
  `fleet/CONTROL.log` and states it never commits or pushes. Requirements I will hold it to
  when I next gate the lane: watcher-written CONTROL lines must be attributable as such in
  the note field, seq must stay strictly monotonic (the lane already has a duplicated
  seq 10–15 block from 18:55–19:05Z), and a watcher must never emit gate, verdict or
  authority content — liveness only. Its own correction at `219075a` (removal detection
  false-positived on the *wording* of my pause file's removal clause; now keyed to a
  dedicated marker line) is the right fix and is noted: my REMOVED marker line is
  `status: REMOVED — NOT IN FORCE` at the top of the control file.
- **Campaign observation (both lanes):** the worker's log records a workspace reset recovered
  by resetting to its remote lane head and re-verifying digests; I hit the same reset this
  cycle (my local objects for `574f499…8ed8d12` were gone while the working tree survived) and
  recovered the same way — `git fetch` + `git reset --hard 8ed8d12` after proving every
  on-disk file byte-equal to the pushed blobs. LAW §8's "push every commit; a durable step
  ends with a push" is the only reason neither lane lost work. Recorded as evidence for the
  2.0.1 policy notes, not as an incident.

---

## 2026-09-25T20:44Z — GATE: TASK-014 q3 (M4 C2-format speaker/format detector) — VERDICT: **FAIL / INCOMPLETE** (three criteria)

- gated at WORKER-2 head `219075a` (main `7d033ab`); artefacts `tools/det_format.py`
  (sha256 at head `ef9ff4f257cd9b75edd1dc888abac17ace21ad65ec8ff78e8c088c5ea527b7b9`),
  `runs/m4-q3-format/{README.md,PROVENANCE.json,signals.json}` (signals.json sha256
  `86c8f57dea9443f3…` — computed by me; the manifest does not carry it),
  `tests/test_det_format.py` (6 tests), `tools/PATTERNS.md` §5c.
- criteria are TASK-014 q3's as cut at 19:01Z ("same shipping requirements as q2, plus an
  explicit statement of what speaker/format error means mechanically and what it cannot see"),
  labelled q3.1–q3.9 below. Gate scratch re-created at `/home/user/gate-scratch/w219075a`
  (the previous scratch was lost to a sandbox reset; inputs re-materialised read-only via the
  worker's own `tools/m5r_inputs.sh`, corpus zip sha `3f36c520…` verified).

| # | criterion | verdict | independent evidence (my own runs) |
|---|---|---|---|
| q3.1 | ships WITH a self-test (STANDARDS tool gate 1) | **PASS** | `python3 tools/det_format.py --self-test` → `C2-format self-test OK (5 signals on the toy, 0 on the clean control)`, rc=0. 6 module tests: `test_each_rule_fires`, `test_abbreviations_are_not_glued_periods`, `test_clean_control_is_silent`, `test_self_test_entry_point`, `test_signals_carry_offsets_and_excerpts`, `test_tuning_and_holdout_disjoint_in_split`. Lane suite at head: **Ran 26 tests, OK, 0 skipped** |
| q3.2 | fixture results — which of the 16 confirmed fixtures it catches | **FAIL** | No fixture-recall result for C2-format exists anywhere: not in `runs/m4-q3-format/README.md`, not in `PROVENANCE.json`, not in PATTERNS.md §5c. Worse, PATTERNS.md §3's per-detector table still reads `speaker/format | — | **not built (M2 accepted incomplete)** | — | unmeasured | no` (line 45) while §5c (line 118) documents the shipped detector and line 179 marks q3 done — the catalogue contradicts itself, and §3 is the table M6 FINAL would quote. The honest answer is probably `0/16` (format artifacts are not what the 16 fixtures encode), but STANDARDS gate 1 requires it **measured and stated**, not left blank |
| q3.3 | clean-set results — false positives on genuinely held-out known-good text (the books are known-good; flagging book text is misfiring by definition) | **FAIL** | The only clean evidence is the self-test's **toy** control (0 signals) and `test_clean_control_is_silent`. There is **no run over `evidence/fixtures/clean/clean.json`** and **no run over known-good book passages** (the 24-slug store is present and the detector never reads it — `grep parse_book_store tools/det_format.py` → no match). For 7 punctuation/whitespace rules this is a cheap, decisive test and it is owed |
| q3.4 | disclosed threshold provenance (fitted on what, measured on what) | **PASS with a recorded gap** | Disclosed: the 7 rules with their exact shapes in the module docstring, the `ABBREV` exclusion list in-file, the run labelled tuning-only, and two candidate rules **measured then rejected** with counts so the rejection is auditable. Gap: the camel-glue rejection count (**35 hits / 18 files**) is **not reproducible** from the published description — my own probes give 126 hits / 61 files (any internal capital: `WorldCom`, `PhD`) or 6 / 6 (lowercase-start: `veryCapitalist`, `dimensionONE`, `iPad`); the double-word count (**3,436 / 228**) reproduces **exactly** with `\b(\w+)\s+\1\b` (case-insensitive). The *decision* is corroborated by both my probes (proper nouns dominate), so this is a documentation gap, not a soundness problem: publish both rejected-rule probes verbatim (regex + flags) |
| q3.5 | LAW §8 manifest for the run | **FAIL** | Present and recomputed MATCH by me: `corpus_zip_sha256 3f36c520…`, `split_file` + `split_corpus_files_sha256 9ae90185…` (I reproduce this digest from its written derivation), `holdout_enforced: true`, `holdout_reads: []`, full `transcripts_read` (193, set-equal to the split's tuning list), `outputs.per_rule` (R1 22 · R2 3 · R3 5 · R4 1 · R5 15 · R6 2 · R7 1 = 49), `run_utc 19:08:01Z`, status CANDIDATE/PROVISIONAL-UNGATED. **Missing: `tool_commit` (reachable), `policy_sha256`, `main_head`, and the output digest** (signals.json `86c8f57d…`). And **`detector_sha256 c322e053…` does not match the file at head** (`ef9ff4f2…`): it matches `det_format.py` at `4425763` (verified by `git show`), and `4e114f1` (q4) later changed **only the runner** (added `--set {tuning,holdout}` and a `set` provenance field) — I read the full diff and then reproduced the run at head: **byte-identical `signals.json` (`86c8f57d…` both)**, so the outputs are attributable to unchanged rule logic. But that attribution cost me a commit archaeology + a fresh replay; the manifest cannot show it. This is exactly the mismatch LAW §8 exists to reject |
| q3.6 | tuning runs must not read the holdout; the seal must not change | **PASS** | `signals.json` keys == the split's tuning set **exactly** (193/193), ∩ holdout = **0**; manifest `transcripts_read` == tuning, `holdout_reads: []`; `run_tuning` raises `SystemExit` on any tuning∩holdout overlap; the split file is byte-identical to the sealed original (`481d8513…`, unchanged since `593cad3`) |
| q3.7 | orchestrator reproduces the run (STANDARDS gate 3); citations byte-exact | **PASS** | my own run `python3 tools/det_format.py --tuning --split tools/HELD-OUT-SPLIT.json --corpus corpus --out <scratch>` → `193 transcripts, 49 signals {R1 22, R2 3, R3 5, R4 1, R5 15, R6 2, R7 1}` — per-rule counts identical to the manifest and **`signals.json` byte-identical** to the committed file; then, with my own code, **49/49** signals' `start`/`end`/`match` re-verified against the frozen overlays: **0 citation mismatches** |
| q3.8 | frozen corpus only, stdlib only, no network, writes only to named outputs | **PASS** | imports `argparse, json, os, re, sys` + same-lane `m5r_reduce` for the loaders (stdlib only, no urllib/socket/subprocess); reads `corpus/**` + the split; writes only under `--out`. The detector never reads the book store, so a book-store binding is **N/A for this detector** — recorded as N/A, not as a gap |
| q3.9 | explicit mechanical definition + what it cannot see; unmeasured ≠ zero; CANDIDATE discipline; no rates | **PASS** | The docstring and README state precisely what the 7 rules claim, that a format artifact is mechanically demonstrable while "whether it changed meaning" is not claimed, and that **speaker attribution is out of mechanical scope** — backed by a corpus census I **independently corroborated with my own probes over all 230 transcripts**: speaker labels **0**, bracketed stage directions **0**, HTML tags/entities **0**, strict JS syntax (`function(`, `=>`, `var/const/let x =`, `document.x(`, `window.x(`, `<script`) **0**, control chars **0**, tabs **0**, nbsp/U+2007/U+202F **0**, double spaces **0**, space-before-semicolon **0**. (Instrument lesson, mine: a naive word-level probe `\b(var|const|function|document\.|window\.)\b` yields 470 hits / 153 files — all ordinary English ("function", "document.", "window."); the strict syntax probe gives 0. Their claim is right; a loose probe would have "refuted" it.) All 49 signals are CANDIDATE-class and unreviewed; precision **unmeasured**; no rate anywhere; delivery labelled PROVISIONAL-UNGATED; the M2 remainder is resolved honestly (format half measured, speaker half an explicit M6 limitation) |

### Verdict

**TASK-014 q3 = FAIL / INCOMPLETE** (q3.2 fixture results, q3.3 clean-set results, q3.5 §8
manifest bindings; q3.1, q3.4-with-gap, q3.6–q3.9 PASS). LAW §9: any failed criterion =
INCOMPLETE, never PASS. The detector's **substance is clean**: I reproduced its run
byte-for-byte, re-verified every citation, corroborated its scope census with my own probes,
and confirmed the rule logic has not moved since delivery. What is missing is the shipping
evidence STANDARDS gate 1 demands (fixtures + clean set) and the LAW §8 bindings that would
let a verifier attribute the run without archaeology. **C2-format is not promotable, its 49
signals stay CANDIDATE, and no M6 figure may quote them.**

### Brake decision (same proportionality test as q1, recorded and reversible)

No activation-scoped PAUSE: the failed criteria are evidence instruments on a quantum whose
substance I reproduced byte-identically; nothing false was shipped; the worker's current task
is owner-ordered (ERRATA-25g §5: claim TASK-018 now, then TASK-017), and a pause would make a
doc/evidence repair the only actionable task and idle the fleet. Restriction applied instead,
artefact-scoped and fail-safe: **q3 is INCOMPLETE and may not be cited as passed; C2-format is
not promotable; its signals may not feed any rate or M6 figure.** The repair will be cut as a
**single task covering the q2+q3 shipping gaps** once the q2 gate completes this shift (queue
stays small, ERRATA-25f §4). If BOSS-2 or the owner reads ORCHESTRATOR.md step 3 as requiring a
pause on any FAIL, I will issue one in the same cycle on request.

## 2026-09-25T20:58Z — GATE: TASK-014 q2 (M4 C1-drop drop-word detector) — VERDICT: **FAIL / INCOMPLETE** (five criteria)

- gated at WORKER-2 head `219075a` (main `7d033ab`); artefacts `tools/det_dropword.py`
  (sha256 at head `a0236325c5f5be4a…`), `runs/m4-q2-dropword/{README.md, part-1..6.json,
  part-1..6.PROVENANCE.json, signals.json, MERGE-PROVENANCE.json}` (signals.json sha256
  `8d71f57bcb80313f…` — recomputed by me, matches README **and** MERGE-PROVENANCE),
  `fixtures/v2/dropword.json` (4 provisional fixtures), `tests/test_det_dropword.py` (8 tests),
  `tools/PATTERNS.md` §3 line 44, `evidence/fixtures/{confirmed/confirmed.json, clean/clean.json}`.
- criteria are TASK-014 q2's as cut at 19:01Z plus the 20:2xZ re-cut (precision requires the
  fresh sealed split v2), labelled q2.1a–q2.8 below. Owner ERRATA-25e §1 parked q2 ungated
  until M5-R PASSed; it PASSed (19:58Z) and was re-affirmed at this head (20:12Z), so gating
  resumed. **Order note (disclosed, mine):** the recorded order was q1 → q2 → q3; I gated q3
  first (20:44Z) because its census claims were checkable with probes I had already built. No
  criterion of either gate depended on the other's outcome, so nothing is invalidated.
- gate scratch `/home/user/gate-scratch/w219075a` (worktree detached at the worker head; corpus
  and evidence re-materialised read-only via the worker's own `tools/m5r_inputs.sh`; corpus zip
  sha `3f36c520…` verified). My probes wrote only outside the lane (`/home/user/gate-scratch/*`).

| # | criterion | verdict | independent evidence (my own runs) |
|---|---|---|---|
| q2.1a | ships WITH a self-test (STANDARDS tool gate 1) | **PASS** | `python3 tools/det_dropword.py --self-test` → `C1-drop self-test OK (detects a drop, ignores the faithful quote)`, rc=0 — i.e. it carries a **negative** control, not just a positive one. `tests/test_det_dropword.py` = 8 tests (incl. byte-exactness of the 4 fixtures per the README). Lane suite at head: **Ran 26 tests, OK, 0 skipped**, run WITH corpus (230 overlays + book store present in the worktree) |
| q2.1b | fixture results — which of the 16 confirmed fixtures it catches (CF-015 / class P5 is the named target) | **FAIL** | The 16 confirmed fixtures **exist and are usable**: `evidence/fixtures/confirmed/confirmed.json` (CF-001…CF-016, each with transcript path + char offset + verbatim quote + suspected text + book_ref). C1-drop was **never run over them** — no fixture-recall figure in `runs/m4-q2-dropword/README.md`, in any part manifest, or in PATTERNS.md. PATTERNS.md §3 line 44 still reads `drop-word | — | **not built (M2 accepted incomplete)** | — | unmeasured | no`, contradicting the shipped detector, its 122-signal run and §5b — and §3 is the table M6 FINAL would quote. Because the 3 fixture transcripts are forced-TUNING, any such figure is **in-sample/seeded** and never recall evidence (LAW §9) — but STANDARDS gate 1 requires it measured and stated, not blank |
| q2.1c | clean-set results on genuinely held-out known-good passages | **FAIL** | `evidence/fixtures/clean/clean.json` = **59 known-good Hawkins book passages** as pointers (slug + char offset + length + sha256). I verified the set's own integrity first: **59/59 sha256 match** the bytes I parsed out of the frozen store (`c0892fcd…`, 24 slugs) → the clean set is intact and was simply **not run**. For a book-anchored detector this is the cheapest decisive test there is: a book passage cannot have dropped words from itself, so every hit is a misfire. I ran it myself (q2.8) — the answer is **not zero** |
| q2.1d | disclosed threshold provenance (fitted on what, measured on what) | **FAIL** (values disclosed, provenance absent) | All eight parameters are published per part and in the README (window 24, stride 12, min_score 0.20, top_k 3, min_matched 10, min_ratio 0.85, max_drop 2, min_flank 3) and the algorithm is fully described in the module docstring (TF-IDF retrieval over Hawkins books → `difflib.SequenceMatcher` alignment → `insert` ops with content-word + numeral + flank filters). **Nowhere states what any threshold was fitted on or measured on.** The README's in-sample caveat covers the *fixtures*, not the *thresholds*. With no clean-set run either (q2.1c), not one threshold has out-of-sample justification on record |
| q2.2 | precision/recall only against a split fixed before tuning | **PENDING — correctly unmeasured** (claim discipline PASS) | v1's one-shot holdout is **SPENT** (q4 `4e114f1`), so precision now requires the fresh sealed split v2 = **TASK-019** (owner-AUTHORIZED, ERRATA-25g §5). The worker claims no precision: README says precision is **unmeasured**, "this is not a rate and not a finding set", all 122 signals CANDIDATE-class and unreviewed, delivery labelled PROVISIONAL-UNGATED → the discipline is right and the absence of a number is the correct state |
| q2.3 | tuning runs must not read the holdout; the split's seal must not change | **PASS** | `signals.json` keys == the split's tuning set **exactly** (193/193), ∩ holdout = **0**; every one of the 6 part manifests has `transcripts_read ⊆ tuning`, `holdout_reads: []`, `holdout_enforced: true`, and the **union of the 6 shards == tuning (193/193 processed)**; `run_tuning` raises `SystemExit` on any tuning∩holdout overlap and asserts non-membership; the split file is byte-identical to the sealed original (`481d8513…`, unchanged since `593cad3`) |
| q2.4 | LAW §8 manifest for every cache/run: corpus + book-store + split digests, detector and config digest, tool commit, policy sha, output digest, run utc | **FAIL** | Present and recomputed MATCH by me: corpus zip `3f36c520…`, split file + salt + `9ae90185…`, shard identity, full `transcripts_read`, `holdout_reads`/`holdout_enforced`, all 8 params, `run_utc` per part, status, output filename; merge level: `signals_total 122` and `signals_json_sha256 8d71f57b…` (both verified). **Missing: the book-store digest** — load-bearing here, because this detector is book-anchored and reads the store through `m5r_reduce.parse_book_store` (I had to bind it myself: 24 slugs, file sha256 `c0892fcd…`); **`tool_commit`, `main_head`, `policy_sha256`, a config digest** (params are listed as values, never digested); **a per-part output digest**; and `MERGE-PROVENANCE.json` has **no inputs block at all**. Worst item: **`detector_sha256 84e5407f…` resolves to NO committed version of `tools/det_dropword.py`** — the only two commits that ever touched the file are `012914d` = `588e1f22…` and `4e114f1` = `a0236325…` (= head). The parts ran 18:57:11Z–19:05:21Z, i.e. **before** the delivery commit `012914d` (19:06:53Z), so all six manifests pin an uncommitted working-tree state: formally the outputs are unattributable to any reachable commit. I closed that gap by reproduction instead (q2.6) — which is exactly the archaeology LAW §8 exists to prevent |
| q2.5 | suite green WITH corpus, skip counts reported, test count never drops (campaign baseline v1's 115) | **FAIL** (queue-order defect, not a q2 work defect) | Green and honest: **Ran 26 tests, OK, 0 skipped**, WITH corpus; `test_det_dropword.py` contributes 8 of them. But **26 < 115**: TASK-014 names **TASK-017** (inherit the v1 toolchain with provenance) as a prerequisite for q2–q4 and it has not landed. Consequence I verified: `tools/loaders.py` and `tools/fixtures.py` are **absent at head** while `evidence/fixtures/README.md` still instructs the reader to run `python3 tools/fixtures.py verify` / `build-clean` — the inherited fixture tooling cannot be executed in this lane at all. The count cannot be restored until TASK-017 does; recorded against q2 because the criterion is q2's |
| q2.6 | orchestrator reproduces the run and re-verifies its citations (STANDARDS gate 3) | **PASS with a quantified caveat** | **Reproduction:** I re-ran shard 1/6 and shard 3/6 at head (`a0236325…`) into gate scratch → **byte-identical** `part-1.json` (sha256 `64a97be5…`, 26 signals) and `part-3.json` (sha256 `092d6341…`, 67 signals) = **66/193 transcripts and 93/122 signals reproduced exactly**. That also proves `4e114f1`'s 27-line `det_dropword.py` change was **runner/CLI-only** (`--set {tuning,holdout}`, `set`/`holdout_consumed` provenance keys — I read the full diff) with no rule-logic change, and it bridges the unresolvable `detector_sha256` pin. Merge arithmetic: 26+14+67+0+11+4 = **122** = manifest total = file content. **Citations (my own code, my own store parse):** **122/122** transcript spans byte-exact at `start`/`end`; **122/122** book citations byte-exact at slug + `char_offset`. **Mechanical claim:** **113/122 fully consistent** — dropped token absent from the cited span, present in the cited book quote, and the restoration's token arithmetic closes exactly. **9/122 shape-defective:** 3 where the dropped token **already occurs in the cited span** (book-side repetition, not an omission — `Causality…Part_1 @2574` quoted `'evidence of'` / dropped `['evidence']` / book quote `'evidence; evidence of'`; `@54983` `'staggering, staggering. This'`; `Causality…Part_2 @55220` `'be sovereign, sovereign'`) and 6 where a multi-word drop **partially overlaps** the span or the arithmetic does not close (2 of those 6 are my own hyphen tokenization — `'one-third'`, `'nitty-gritty'`), so the defensible split is **3 certain + 4 likely + 2 checker-artifact**. Restriction: those 9 must be excluded or re-labelled before any precision or fixture work, and **122 must never be quoted as an omission count** (upper bound 113, itself in-sample and unreviewed) |
| q2.7 | classification discipline under owner ERRATA-25e §2 (leg (d)); fixtures provisional only | **PASS with two coherence defects** | Right: the 4 fixtures are labelled *DROP-CANDIDATE (hand-verified omission) — CLASS BLOCKED*, never CERTAIN; `in_sample_caveat` states that recall against them is inadmissible (LAW §9); `proposed_leg_d` is explicitly marked "NOT in force; needs errata + BOSS CONCERN" (accurate when written); the README records 5 further sampled candidates **discarded or parked with per-item reasons**; and it states that STANDARDS then defined no leg for omissions. **I re-verified all four bindings myself:** transcript spans byte-exact 4/4, book quotes byte-exact 4/4, dropped-token claim holds 4/4, and none of the 4 is a cross-book parallel artifact (their ±30- and ±60-char transcript context occurs nowhere in the 14,515,277-char store). Defects: (a) the file's **proposed** leg-(d) wording ("transcript is ungrammatical or incomplete AND the near-verbatim book source supplies the missing word(s), restoring grammar and doctrinal sense") is **not the enacted text** — owner ERRATA-25e §2 enacted a **narrower** leg (d) (omission *within a matched span*; restoring completes the match) — so adjudication must run against the enacted text and the file needs an append-only note (→ TASK-018 item 0c); (b) per-fixture `proposed_leg` values are `a`/`a`/`b`/`b` while `evidence_class` points at leg (d) → each fixture must be re-adjudicated under the enacted leg with the clause recorded; (c) `generated_utc: "2026-09-25T19:1xZ"` is a **fuzzy timestamp in a provenance field** (§8 wants an exact utc) → append the exact value, never edit in place |
| q2.8 | gate-side clean-set probe (MY evidence — it does **not** satisfy q2.1c, which the worker still owes) | **informative: 3 + 1 misfires on known-good text** | I materialised the 59 hashed clean passages as pseudo-transcripts in a scratch corpus (book store **symlinked**, so retrieval is byte-identical to the real run) and ran both detectors at head: **C1-drop → 3 signals / 59 passages**, **C2-format → 1 signal / 59**. All three C1-drop hits are **cross-book self-parallels** — the "transcript" *was* book text, so the rule matched a near-verbatim passage in a **different** Hawkins book and reported the wording difference as a drop: CL-034 (`the_ego_is_not_the_real_you__w` @43642 → cited `daily_reflections_from_dr_dav` @80391, dropped `'remains'`, 22/24 match), CL-035 (@124511 → `discovery_of_the_presence_of_g` @295761, dropped `'by ownership'`, 16/16 match), CL-055 (`transcending_the_levels_of_con` @274472 → `the_map_of_consciousness_expla` @134304, dropped `'so-called'`, 24/24 match). The C2-format hit is **book-store typography**: `power_vs_force__the_hidden_de` @236391 contains `power.When`, so R1-glued-period fires on the book itself — any transcript faithfully quoting that passage would be flagged for a **source-inherited** artifact. **Transfer check (does the mechanism contaminate the real runs?):** I tested whether each signal's own transcript wording (span ±30 chars) occurs verbatim in the store — a test that correctly flags all 3 known clean misfires (validated on them first). Result: **1/122** C1-drop tuning signals (`Most_Valuable_Qualities…` @457 `'be formidable'`, dropped `['quite']`) and **0/49** C2-format signals → cross-book parallels are **not** a material contaminant of the tuning runs and none of the 49 format signals is source-inherited. (A weaker variant — the 3-char `quoted` string alone — "hits" the store for 28/49 format signals; that is coincidence across 14.5 M chars, which is why I report the context test as the discriminating one and publish both.) **Two cheap filters are owed** (both detectors already retrieve book passages): (i) C1-drop must not report a drop when the transcript's own wording is itself verbatim book text; (ii) C2-format must not report a punctuation/whitespace artifact whose bytes are inherited from the matched book span |

### Verdict

**TASK-014 q2 = FAIL / INCOMPLETE** — failed: q2.1b (fixture results), q2.1c (clean-set
results), q2.1d (threshold provenance), q2.4 (LAW §8 manifests), q2.5 (test count vs the
campaign baseline). Passed: q2.1a (self-test with a negative control), q2.3 (isolation +
seal), q2.6 (reproduction + citations, with the 9-signal caveat), q2.7 (classification
discipline, with two coherence defects). q2.2 (precision) is correctly **PENDING** on split v2.
LAW §9: any failed criterion = INCOMPLETE, never PASS.

The substance is good and I could see it because I ran it: every citation on both sides is
byte-exact, 93 of the 122 signals reproduce byte-identically from head, isolation is airtight,
the four provisional fixtures survive my independent re-verification, and the worker disclosed
its own false-positive shapes (speaker improvisation/fillers, abbreviation-vs-expansion, book
table/heading text) plus five discarded candidates with reasons. What is missing is the
shipping evidence STANDARDS gate 1 demands and the LAW §8 bindings — and my own clean-set probe
shows the missing measurement was not a formality: on known-good book text C1-drop misfires
3/59 and C2-format 1/59, shapes that appear nowhere in the worker's disclosure.

**Restriction (artefact-scoped, fail-safe):** q2 may not be cited as passed; **C1-drop is not
promotable**; its 122 signals stay CANDIDATE-class and unreviewed; the 9 shape-defective
signals are excluded from any count; **no omission count, rate, or M6 figure may rest on q2**;
the 4 fixtures stay provisional pending TASK-018 adjudication under the **enacted** leg (d).

### Brake decision (same proportionality test as q1 and q3 — recorded and reversible)

No activation-scoped PAUSE. The failed criteria are evidence instruments and manifest bindings
on a quantum whose substance I reproduced byte-identically; nothing false was shipped; the
worker's current task is owner-ordered (ERRATA-25g §5: claim TASK-018 now, then TASK-017), and
a pause would make a documentation repair the only actionable task in the fleet and idle it.
Repair is cut as **ONE task — TASK-020** (q1+q2+q3 shipping gaps), queued after TASK-018, with
my probe numbers written in as reproduction targets. If BOSS-2 or the owner reads
ORCHESTRATOR.md step 3 as requiring a pause on any FAIL, I will issue one in the same cycle on
request.

### q3 ADDENDUM (append-only; the q3 verdict at 20:44Z stands unchanged)

My gate-side clean-set probe (q2.8 above) also measures the q3 criterion I had to fail for
want of data: **C2-format misfires 1/59 on known-good book passages** — R1-glued-period on
`power_vs_force__the_hidden_de` @236391 (`power.When`), i.e. typography inherited from the book
store itself. Transfer check: **0/49** of the shipped format signals are source-inherited
(span ±30-char context absent from the store), so the 49 signals remain transcript-side
artifacts and q3.7/q3.9 stand. q3.3 stays **FAIL** (the worker still owes the run and the
filter), now with a measured target: reproduce 1/59 and add the source-inheritance filter.

## 2026-09-25T21:09Z — GATE: TASK-014 q4 (M4 one-shot holdout runs) — VERDICT: **FAIL / INCOMPLETE** (two criteria) · precision criteria **NOT GATEABLE** → TASK-019b · holdout stays **SPENT**

- gated at WORKER-2 head `219075a` (main `7d033ab`); artefacts `runs/m4-q4-holdout/{README.md,
  v1-holdout.json, v1-holdout.PROVENANCE.json, part-holdout-drop.json,
  part-holdout-drop.PROVENANCE.json, part-holdout-format.json,
  part-holdout-format.PROVENANCE.json}`, runner `tools/m4_q4_holdout.py`, `tools/PATTERNS.md` §5d.
- **What kind of gate this is (declared up front):** q4's original criteria asked for
  per-detector precision on data fixed before tuning. The one-shot holdout is **spent**, and my
  20:2xZ re-cut moved every precision question to the fresh sealed split v2 (TASK-019,
  owner-AUTHORIZED per ERRATA-25g §5). So this gate decides only what is still decidable:
  **one-shot execution discipline, isolation, counts-only discipline, attribution, §8 manifests,
  and the one positive claim the delivery makes (a reproduction receipt).** Precision criteria
  are recorded **NOT GATEABLE — transferred to TASK-019b**, not passed and not failed.
- **I did not re-run the holdout.** Re-running spent single-use evidence is forbidden (LAW §9;
  TASK-018 boundaries repeat it). Every check below is arithmetic over committed artefacts, my
  own re-parsing of the frozen corpus, or a blob comparison against the read-only archive lane.

| # | criterion | verdict | independent evidence (my own runs) |
|---|---|---|---|
| q4.1 | thresholds and rule set frozen **before** the holdout run | **PASS** (proven, not taken on assertion) | The q2 tuning-run params and the q4 holdout params are the **same eight values** (`window 24, stride 12, min_score 0.2, top_k 3, min_matched 10, min_ratio 0.85, max_drop 2, min_flank 3`) — I diffed the two manifests' `params` blocks. C2-format's `rules` list is the same 7 rules in both runs. No commit after the run touched either detector: `det_dropword.py` = `a0236325…` at `4e114f1` = `2f55b0c` = head; `det_format.py` = `ef9ff4f2…` at `4e114f1` = `2f55b0c` = head (the run's own pins, `a0236325…` and `ef9ff4f2…`, **do** resolve to committed blobs — unlike q2's and q3's). `thresholds_frozen_before_run: true` plus the note "no threshold was tuned against the holdout; this report is one-shot (LAW §9)" |
| q4.2 | one run, reported once, consumption stamped | **PASS** | Exactly one artefact pair per detector set; single `run_utc` each (v1 `19:11:11Z`, drop and format `19:14:35Z`); no second or overwritten run anywhere in the tree; **`holdout_consumed: true` in all three manifests**; PATTERNS §5d states the holdout is spent for these detector versions and that any later tuning informed by the counts owes a new split |
| q4.3 | the holdout runs read **only** the holdout (inverse isolation) | **PASS** | In all three manifests `holdout_reads` is set-equal to the split's 37 holdout names and `transcripts_read` (37) has **∩ tuning = 0**; `v1-holdout.json` `per_transcript` keys == the 37 holdout names exactly; `set: "holdout"`; `holdout_enforced: false` is the correct semantics for evaluation mode (the runner sets it to `which != "holdout"`), not a disabled guard |
| q4.4 | counts only — no precision, no rate, no promotion; A4 stays excluded | **PASS with one hygiene defect** | README section "**What this run does NOT prove**" is explicit: "Counts are not precision… no rate is claimed", and PATTERNS §5d repeats it ("No precision claim: precision/recall require *reviewed* holdout labels; none exist"). No promotable flag is set anywhere; every status field says PROVISIONAL-UNGATED / CANDIDATE. **A4-confusion was correctly NOT run** (`detector_set: "A1,A2,B1,B2"`; PATTERNS §3 line 43 still records it as excluded since v1 for want of an independent FP rate). Defect: `per_detector_signal_instances` records `A1 162 · A2 15 · B2 8` and **omits the explicit zero for B1-contradiction** — the README states B1 = 0, the manifest does not, and an absent key reads as "not measured" rather than "measured, zero". (Consequence worth stating: with 0 holdout signals, B1 gets **no** validation from this run either, so v1's B1 headline hold — TASK-005 FAIL / REDIRECT-005 — stands untouched.) Also: the §5d table column headed "tuning raw signals (**rate/tx**)" is a *density* (signals per transcript); the label invites misreading as an error rate → rename to "signals/tx (density, not a rate)" |
| q4.5 | the inherited v1 toolchain is attributable | **PASS with a binding-form defect** | `v1_tool_shas` pins **13 files** by sha256. I compared every one against the read-only archive lane: **13/13 byte-identical** to `origin/arena/01a0d581-fleetyard:tools/{census,det_confusion,det_contradiction,det_misquote,det_nonsense,det_repetition,fixtures,loaders,report_m6,retrieval,run_detectors,sweep_m5,tokenizer}.py` (e.g. `loaders.py 3452c95d…`, `run_detectors.py d7d109c5…`, `det_misquote.py 3b8d1cd4…`). So the run **is** attributable to committed code. Defects: the manifest cites an absolute sandbox path (`v1_tools_dir: /home/user/fleetyard/evidence/tools`) instead of lane + commit + blob path, and `evidence/tools/` **does not exist in the committed tree** — the toolchain is still not inherited into this lane (that is TASK-017), so nobody can re-run q4's v1 leg from this checkout. This also refines my q2.5 evidence line: `tools/loaders.py` and `tools/fixtures.py` are absent **from this lane**, but they exist and are sha-verified in the archive lane — TASK-017's job is inheritance + the suite, not reconstruction |
| q4.6 | LAW §8 manifests for all three runs | **FAIL** | `v1-holdout.PROVENANCE.json` carries split file/salt/`9ae90185…`, `transcripts_read`, `holdout_reads`, `run_utc`, the 13 tool shas and the one-shot note — but has **no `corpus_zip_sha256`, no book-store digest** (and B2-misquote is book-anchored: 8 of the 185 signals carry book references, so the store is a load-bearing input), **no `tool_commit`/`main_head`/`policy_sha256`, and no `outputs` block at all** — the 127 KB `v1-holdout.json` has no digest anywhere. The drop and format holdout manifests are better (corpus zip `3f36c520…`, split digest, params/rules, detector sha that resolves to a committed blob) but still lack the **book-store digest** (C1-drop is book-anchored by construction), `tool_commit`, `main_head`, `policy_sha256`, a config digest and **per-run output digests**. Same shape as q2.4 and q3.5 → TASK-020 item 9 |
| q4.7 | the delivery's one positive claim: a reproduction receipt for the inherited census | **PASS — verified independently by me** | I re-derived it from the committed artefacts: recounting `v1-holdout.json` gives **185 signals**, per-detector **A1-repetition 162 · A2-nonsense 15 · B2-misquote 8** (B1 0) — identical to the manifest — and comparing per-transcript counts against the committed M5-R raw records (`evidence/runs/m5-raw/records/`, 230 files) for all 37 holdout transcripts gives **0 mismatches, 185 raw-side vs 185 holdout-side**. The claim "185/185, 0 per-transcript count mismatches" is therefore **true on my own arithmetic**, and it is correctly scoped by the worker as reproduction, not precision |
| q4.8 | the C1-drop tuning↔holdout gap is characterized honestly | **FAIL (the characterization is measurably wrong)** | PATTERNS §5d: "C1-drop's holdout rate is ~4.5x lower than its tuning rate (5 vs 122). With 37 holdout transcripts this is **dominated by sampling noise**, but it may also indicate parameters fitted to the tuning half — flagged for M4 follow-up." I tested that. Holdout transcripts are **14.9% shorter** on average (53,949 vs 63,361 chars; holdout = 1,996,122 of 14,224,783 corpus chars), so per-transcript densities mislead; normalizing by **character exposure** and using a Poisson tail: **v1 A1/A2/B1/B2 → observed 185 vs expected 187.6, P(X≤185) = 0.45** (a perfect fit — the "5.95 vs 5.00/tx" difference is *entirely* exposure); **C2-format → observed 12 vs expected 8.0, P(X≤12) = 0.94** (consistent); **C1-drop → observed 5 vs expected 19.9, P(X≤5) = 7.7e-05** (and 5.1e-06 on a per-file normalization). So the C1-drop deficit is **not** dominated by sampling noise — it is a real, unexplained ~4x shortfall, while the other two detector sets behave exactly as exposure predicts. Two candidate causes remain: parameters fitted to the tuning half (untestable, because q2.1d's threshold provenance was never disclosed) or a genuine book-exposure difference between the halves (testable **only** on a fresh split — never by re-running this one). The worker's instinct to flag it was right; the emphasis was wrong, and the wrong emphasis is the kind that later becomes a citation. Correction owed append-only with these numbers → TASK-020 item 10 |
| q4.9 | precision / recall / FP counts / seeded-vs-independent / promotion decisions (q4's original output criteria) | **NOT GATEABLE — transferred to TASK-019b** | No reviewed holdout labels exist, so no precision or FP count is computable from this run, and the worker claims none. Under the re-cut, per-detector precision, seeded-vs-independent separation and promotion decisions are TASK-019b's deliverable on the fresh sealed split v2, evaluated **once**. Recorded as not-gateable rather than passed or failed, so no reader can mistake silence for success |

### Verdict

**TASK-014 q4 = FAIL / INCOMPLETE** on q4.6 (§8 manifests: no book-store digest on two
book-anchored detector sets, no corpus binding or output digest at all on the v1 leg, no
tool_commit/main_head/policy sha anywhere) and q4.8 (the C1-drop gap is characterized as
sampling noise when exposure-normalized arithmetic gives P ≈ 8e-05). Passed: q4.1 (thresholds
provably frozen before the run), q4.2 (single run, consumption stamped), q4.3 (inverse
isolation airtight), q4.4 (counts only, A4 correctly not run — one explicit-zero hygiene
defect), q4.5 (all 13 v1 tool shas byte-match the archive lane — binding-form defect), q4.7
(**the reproduction receipt verifies on my own arithmetic: 185/185, 0 mismatches**). q4.9 is
**NOT GATEABLE** and moves to TASK-019b.

This is the strongest delivery of the four M4 quanta on discipline and the weakest on bindings:
the one-shot rules were actually kept (I could prove it from params equality and the absence of
any post-run threshold commit), the spent holdout was never re-run, nothing was claimed beyond
counts, and the central positive claim survives independent recomputation. What fails is the
same shape that failed q2 and q3 — LAW §8 manifests that do not bind the load-bearing inputs —
plus one sentence that understates a real 4x detector deficit.

**Restriction (artefact-scoped, fail-safe):** the holdout counts (v1 185 · C1-drop 5 ·
C2-format 12) are a **receipt only** — never re-run, never a rate, never precision, never an M6
figure; **C1-drop's exposure-normalized deficit (P ≈ 8e-05) is an open item that blocks its
promotion** and must be characterized on split v2, not on this spent holdout; B1 remains
unvalidated (0 holdout signals) so v1's B1 headline hold stands; q4 may not be cited as passed.

### Brake decision (same proportionality test as q1, q2, q3 — recorded and reversible)

No activation-scoped PAUSE: the failed criteria are manifest bindings and one documentation
sentence on a run whose discipline I could verify and whose positive claim I reproduced
independently; nothing false was shipped and the holdout was not abused. Repair folds into
**TASK-020** (items 9–10) rather than a fourth task, keeping the queue at three actionable items
(ERRATA-25f §4). If BOSS-2 or the owner reads ORCHESTRATOR.md step 3 as requiring a pause on any
FAIL, I will issue one in the same cycle on request.
