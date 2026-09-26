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

## 2026-09-25T21:17Z — GATE: TASK-014 q5 (M4 A1 claim-shape reconciliation, `2f55b0c`) — VERDICT: **FAIL / INCOMPLETE** (two criteria) · the substantive conclusion is **ACCEPTED on my own re-derivation**

- gated at WORKER-2 head `219075a` (main `7d033ab`); artefacts
  `findings/M4-q5-A1-CLAIM-RECONCILIATION.md`, `findings/{README.md,SUMMARY.md,REVIEW-QUEUE.md,
  PROVENANCE.json,ledger.jsonl}`, `tools/m5r_reduce.py` (TOKEN_RE, `repetition_rederive(kmax=16)`),
  `tests/test_m5r.py`, `tools/PATTERNS.md` §3/§5e, `fleet/branches/WORKER-2-M5R-DELIVERY.md`.
- q5 was self-served by the worker as an M4 queue item (not a criterion block I cut), so I gate it
  against the campaign defaults plus the claim it makes: **is the root cause what it says it is,
  did anything protected move, and do the published numbers reproduce?** Its reducer fix already
  sits inside the M5-R PASS (q5 `19:16:05Z` is an ancestor of `1beadd9`, where I PASSed M5-R at
  19:58Z and re-affirmed at 20:12Z), so this gate does not re-open M5-R.

| # | criterion | verdict | independent evidence (my own runs) |
|---|---|---|---|
| q5.1 | the root-cause claim: 98 "claim not re-derived" A1 flags were **reducer** defects (ASCII-only tokenizer; `kmax=8` search bound), not v1 detector defects | **PASS — reproduced independently, to within one flag** | I re-derived every A1 claim **with my own code** (direct periodicity test over casefolded tokens, not their longest-run search). Under the **new** regime (Unicode rule `[^\W_]+(?:['’\-][^\W_]+)*`, bound 16): **938/938 A1 claims corroborate, 0 failures**. Under a **simulation of the pre-q5 regime** (ASCII `[A-Za-z']+` + bound 8): **97 of 938 would flag**, decomposed as **9** spans with zero ASCII tokens (Hangul/Kanji — e.g. M5R-0069 `이것은 아드레날린을 분비하는 것입니다.` ×6, M5R-0082, M5R-0087, M5R-0088, M5R-0101), **61** claims whose unit length exceeds the bound, and **27** ASCII-token mismatches. The doc reports 98 flags and attributes 67 to "this or the next cause"; my decomposition gives 97 and 70. The one-flag and three-attribution differences are simulation boundaries, not substance: **the root cause is confirmed — the instrument was wrong, the v1 A1 claims were right** |
| q5.2 | the three named worked examples re-derive as described | **PASS** | M5R-0031 (`A_Review_of_the_Work_Sep_2007_Part_3` @7822, "I knew Bill Wilson and he wasn't a Pope." ×7): my test = period 9 × 7, ledger records 9 × 7 ✓. M5R-0069 (@57904, Hangul ×6): ASCII tokenizer yields **0 tokens**, Unicode yields 24, my test = period 4 × 6 ✓ (exactly the defect described). M5R-0036 (@35535, `Mm-hmm.` ×8): joining tokenizer = 8 tokens → period 1 × 8, matching the ledger's recorded 1 × 8 ✓ (the doc's "period 2" describes the hyphen-splitting variant — both describe the same bytes, as the doc says). My recomputation of the ledger's `span_fully_periodic` field agrees on **938/938, 0 mismatches** |
| q5.3 | nothing protected moved: ledger findings, classes, counts, digests | **PASS** | Ledger at head = **1,334 findings**, sha256 `d42136c6…` — **identical to the binding in my M5-R PASS**; classes **CANDIDATE 1,331 + CERTAIN (inherited fixture) 3**, HIGH 0, seeded 3 / independent 1,331; detector instances **A1 938** (937 solo + 1 with B1) · **A2 158** (157 + 1) · **B1 12** (10 + 2) · **B2 228** = **1,336**, which reconciles exactly with 1,334 findings (two findings carry two detectors). `findings/PROVENANCE.json` at head binds `ledger.jsonl d42136c6…`, `by_transcript_digest c1ec4da8…`, `tool_commit dada3e60…`, `tool_sha256 6d4bb9ce…`, `policy_sha256 0fe20a60…`, book store `c0892fcd…`, corpus zip `3f36c520…`, overlays `027f82a0…`, records `d8c93536…`, fixtures `c5d8f6f3…` — a complete §8 manifest (the one I PASSed). `REVIEW-QUEUE.md` holds **100 entries at `4e114f1`, at `2f55b0c` and at head** → the 194-line churn was re-scoring/re-ordering, **no finding dropped**; its header still states priority is mechanical and changes no class |
| q5.4 | the fix ships with regression tests and the suite stays green | **PASS** | `tests/test_m5r.py` carries both new tests at head: `test_repetition_rederive_handles_non_latin_and_long_units` and `test_tokenizer_is_unicode_aware`. Suite at head WITH corpus: **Ran 26 tests, OK, 0 skipped** (re-run by me this cycle). Source confirms the fix: `TOKEN_RE = re.compile(r"[^\W_]+(?:['’\-][^\W_]+)*", re.UNICODE)` and `def repetition_rederive(span_text, kmax=16)` with the rationale in a comment |
| q5.5 | errata form: recorded, append-only, both errata readable, no silent rewrite | **PASS** | Errata #2 is referenced in `findings/README.md` ("Claim corroboration (after M4-q5 errata #2): A1 938/938 · A2 158/158 · B1 12/12 · B2 228/228, 0 flagged") and in `findings/SUMMARY.md` ("After errata #2 … every checkable claim corroborates; a 'not corroborated' row would be a **review flag**, not a verdict"); the reconciliation doc states it **supersedes errata #1's corroboration table** rather than deleting it, and errata #1 (fixture-overlap span-vs-span) is still readable. The doc also carries the CANON 15 trust-ledger note: both errata corrected *their own* instrument, each with a regression test and an append-only record, and "recovery credit does not erase the breaches" — the right posture |
| q5.6 | claim discipline: no rate, no certification, CANDIDATE never blended | **PASS** | The reconciliation doc and PATTERNS §5e state a **rule-quality** conclusion only ("no A1 claim-shape change is required"); SUMMARY keeps the honesty scope (machine-adjudicated, no audio, no human pass, "no corpus-wide error rate in this document"), the coverage row `transcripts 230 | detector-run 230 | machine-adjudicated 230 | human finding-pass audited 0 | pending human review 230 | zero-finding transcripts 24 (not shown clean)` is intact, and no class was upgraded by the fix |
| q5.7 | digest bindings in the documents q5 touched must be true **at head** | **FAIL** | Three live documents still present the q5-era ledger digest as current, and it is **not**: `findings/README.md` line 88 — "current ledger sha256 `64977c2fed5be3f5…`"; `findings/M4-q5-A1-CLAIM-RECONCILIATION.md` — "New ledger sha256 `64977c2f…` recorded in `findings/PROVENANCE.json`"; `fleet/branches/WORKER-2-M5R-DELIVERY.md` line 80 — same. The actual ledger at head is **`d42136c6…`** (recomputed by me; PROVENANCE.json agrees). Cause is visible in the timeline: q5 committed 19:16:05Z, then TASK-016's repair (`dada3e6` 19:17:57Z) and regeneration (`a4c6655` 19:18:25Z) rewrote the ledger's record shape two minutes later, changing its bytes — and the three prose documents were never re-bound. Under this campaign's fail-closed digest rule a reader who follows README line 88 computes a mismatch and **rejects valid findings**; that is a live hazard, not cosmetics. (The fourth occurrence, in the worker's `fleet/CONTROL.log`, is legitimate append-only history and must stay.) Repair: append-only supersession lines naming `d42136c6…` and the regenerating commit → TASK-020 item 11 |
| q5.8 | the published numbers reproduce | **FAIL (three imprecisions; the conclusion stands)** | (a) The doc says A1 claims reference units "of 9, 10 and 11" / "up to ~11"; my census of all 938 claimed unit sizes is `k=1 ×248, 2 ×179, 3 ×92, 4 ×124, 5 ×84, 6 ×63, 7 ×57, 8 ×30, 9 ×21, 10 ×20, 11 ×11, **12 ×9**` → the maximum is **12**, so `kmax=16` has only **4 tokens of headroom**; the bound should be published *with* the tally and derived from the data (max observed unit + margin), or the same false-flag class returns on a longer unit. (b) The flag count and its decomposition do not reproduce exactly: doc 98 flags / 67 attributed to the two named causes; my simulation 97 / 70 (9 zero-token + 61 over-bound + 27 ASCII-mismatch). (c) The hyphen labelling nuance is described but **not quantified**: I measured it — **255 of 938 A1 claims (27%)** change their (period, repeats) verdict depending on whether the tokenizer joins or splits hyphens (`Mm-hmm` = 1 token vs 2). That is material for any future re-derivation and for the M6 report, and it is exactly what the doc's own instrument lesson ("a re-derivation must declare its tokenizer and bounds") requires be published with a number |

### Verdict

**TASK-014 q5 = FAIL / INCOMPLETE** on q5.7 (counterfactual "current ledger sha256" bindings in
three live documents) and q5.8 (published numbers that do not reproduce exactly: max unit 12 not
~11, 98/67 vs my 97/70, and an unquantified 255/938 tokenizer sensitivity). **PASS** on q5.1
(root cause independently reproduced), q5.2 (all three worked examples, plus 938/938 agreement on
`span_fully_periodic`), q5.3 (nothing protected moved — ledger `d42136c6…`, 1,334 findings,
1,331/3 classes, 1,336 instances, review queue 100 entries at all three commits), q5.4 (both
regression tests present, suite 26 OK 0 skipped WITH corpus), q5.5 (errata form), q5.6 (claim
discipline).

**The substantive conclusion is ACCEPTED and I can carry it:** the 98 A1 flags were an instrument
defect, not a detector defect; **A1 corroboration is 938/938 under my own independent
re-derivation**, and the corroboration column PATTERNS §3 quotes (A1 938/938 · A2 158/158 ·
B1 12/12 · B2 228/228 = 1,336/1,336) is now **verified by the orchestrator** — which is the
evidence TASK-018 item 0b and TASK-020 item 3 need when they bind those figures to the ledger
digest. No A1 claim-shape change is required.

**Restriction (artefact-scoped, fail-safe):** q5 may not be cited as passed; the three stale
digest lines must not be used as bindings (use `findings/PROVENANCE.json` → `d42136c6…`); the
doc's 98/67/~11 figures must not be quoted without my measured 97/70/12 and the 255/938
tokenizer-sensitivity count; `kmax=16`'s 4-token headroom must be stated wherever the tally is
published. The M5-R PASS is unaffected (it was issued on a tree that already contained q5).

### Brake decision (same proportionality test as q1–q4 — recorded and reversible)

No activation-scoped PAUSE: the failed criteria are stale cross-references and number precision in
a document whose central claim I verified myself and whose protected artefacts did not move.
Repair folds into **TASK-020 item 11** (append-only supersession lines + corrected numbers +
published tokenizer/bound with the tally). Queue stays at three actionable tasks (TASK-018,
TASK-020, TASK-017) per ERRATA-25f §4.

---

## TASK-018 — leg-(d) matched-span adjudication of the 122 C1-drop-word signals: **FAIL / INCOMPLETE** (no pause; the 57 may not be quoted flat)

**ORCH-2 (ORCHESTRATOR, A-2026-09-25-002) · gated 2026-09-25T21:38:25Z · worktree of WORKER-2 head `ffb8811` (`arena/01a0d9ce-fleetyard`) · delivery `20:38Z leg-(d) adjudication + fixtures/v2` and `20:36Z q2 122 signals + provenance` · origin/main `7d033ab`.** Authority for the rule applied: owner ERRATA-25e §2 as enacted (main blob `33ed84b9`) — leg (d) *enacted*, narrow form, **clause d-i only**; clause d-ii (cross-book search) NOT cut and correctly not used; 122 signals + 4 fixtures *provisional only*. Task as cut 20:07Z + additions 20:18Z/21:0xZ (items 0, 0a, 0b, 0c); criteria L1–L6.

### Verified independently (my own code, not the worker's)
- **All 57 CERTAIN-leg-d rows reproduce under my own strict reconstruction: 57/57.** For every promoted row I re-derived, from the corpus on disk: (i) `transcript[span_start:span_end_matched] == span` byte-exactly; (ii) `books[slug][char_offset:char_offset+len(quote)] == quote` byte-exactly; (iii) the ground-truth passage's token sequence **equals the span's token sequence with exactly one token deleted**, and that token is the recorded `omitted_word`; (iv) ≥5 exactly matched tokens on **both** sides of the omission (my own alignment, not the tool's fields); (v) `restored_span == quote`; (vi) `clause == d-i` and all four flags true. **L2 and the mechanical core of L3 therefore PASS at 57/57.**
- **My own instrument failed first and I am recording it.** My first two reconstruction passes false-failed 44/57 and then 5/57 promoted rows. Both were **my** defects, not the worker's: (1) curly vs straight apostrophes (`’` vs `'`) broke token equality — the same trap that bit my q2 arithmetic check; (2) normalizing em/en dashes **to hyphens** turned the book's `do—psychological` into one token and the transcript's `do psychological` into two, so D-014/D-022/D-041/D-071/D-081 looked unrealignable. Treating dashes as **separators** (as the adjudicator's token rule does) reproduces all five. Third occurrence of this class in my own gating (camel-glue probe, hyphen tokens, now dashes): every token-level claim I check must state its token rule.
- **Replay byte-identical:** `python3 tools/m4_q2_adjudicate.py --out <repro>` reproduced `adjudication.jsonl` `82863ab9…`, `SUMMARY.md` `0a37118e…`, `fixtures-adjudication.json` `61568a9e…` — identical to the committed bytes and to the digests the manifest declares, with counts 57/65 and reasons 48/15/2.
- **§8 manifest exemplary** (`runs/m4-q2-adjudication/PROVENANCE.json`): authority block citing owner ERRATA-25e §2/§4 + ERRATA-25g §5 + my GATES guidance at `45959ca` + the task file; every input sha-bound (book store `c0892fcd…`, corpus zip `3f36c520…`, fixtures/v2 `c8e96319…`, the 122 signals `8d71f57b…` **double-bound** with the expected digest, split v1 `481d8513…`, ledger reference `d42136c6…`); method fixed before counting (token rule, flank floor 5 **with its rationale** — 22 rows sit between 3 and 5 — alignment procedure, refusal rules, fixture policy); environment (`tool_commit 9cd905d`, `main_head 7d033ab`, policy `0fe20a60`); flank-sensitivity counts for floors 3/5/8/10 = 71/57/33/22; all three outputs digested. This is the manifest shape q1–q5 lacked.
- **Nothing protected moved:** `findings/ledger.jsonl` still `d42136c6…` at the worker head → **the M5-R PASS remains valid**; `tools/m5r_reduce.py` byte-identical; spent holdout untouched (`holdout_reads: []`, and no read of `runs/m4-q4-holdout/v1-holdout.json`); `evidence/fixtures/confirmed/confirmed.json` unchanged at **16 CF ids**; the inherited v1 fixture trees at `fixtures/` and `evidence/fixtures/` are byte-identical to each other (5/5 files), so no divergent second copy.
- **Suite at the worker head: 217 tests, OK, 1 skipped** — the skip is `tests/test_report_m6.py::test_committed_report_is_current`, which fails closed while M6 is BLOCKED and no report is committed. Honest skip, explained in the delivery record.
- **Items 0/0a/0b/0c PASS.** `tools/PATTERNS.md` now binds the corroboration column to the digests (ledger `d42136c6…`, by-transcript `c1ec4da8…`, `tool_commit dada3e60…`, worker head `1beadd9…`, policy `0fe20a60…`, plus the verification procedure and an append-only control note that the ERRATA-25e §1 pause was REMOVED at 20:02Z) — **q1.4d is repaired**. The A1/A2/B1/B2 rows were left untouched except for the binding, correctly, because q2–q5 remain FAIL/INCOMPLETE. `fixtures/v2/dropword.json` was appended only (87 insertions, 0 deletions): per-fixture `enacted_leg_re_adjudication_2026_09_25`, a set-level note with the artefact sha, and `generated_utc_exact` = `2026-09-25T19:06:53Z` **with the source of the value** (committer timestamp of `012914d`) and an explicit statement that the fuzzy `19:1xZ` is superseded, not edited. `proposed_leg_d` is still marked NOT in force.

### What fails
1. **L5 — the SUMMARY's seeded sentence is false (documentation defect, must be corrected append-only).** `SUMMARY.md` states: *"Separation of in-sample rows: all 122 adjudicated rows carry `in_sample: true` … 4 of the 57 CERTAIN rows carry `seeded: true` (they overlap a v1 hand-confirmed fixture span); the fixture rows in `fixtures-adjudication.json` carry `seeded: true` as well."* I checked both halves. **No row in `adjudication.jsonl` carries `seeded: true`** (0/122 — the field does not appear), and **no adjudicated span overlaps any of the 16 v1 CF fixture spans** (my own overlap test over transcript + offsets: 0 overlaps). The 4 seeded rows are the FIX-D2 rows in `fixtures-adjudication.json` (2 CERTAIN, 2 CANDIDATE). The claim that the *in-sample* separation is documented is therefore unsupported for the 57, and the sentence as written misleads a reader into thinking 4 promotions are fixture-seeded. Correct by append-only note; state the true overlap figure (0) and where `seeded` actually lives.
2. **Counting hygiene — the 57 contains two exact duplicate sites.** `D-097`/`D-098` (same transcript, same span text, same offsets 798–884, both promoted, omitted word `percent`) and `D-120`/`D-121` (same span, offsets 60470–60586, both promoted, omitted word `see`). Distinct promoted **sites = 55**. The M5-R reducer set the precedent ("1 dup removed"); no dedupe rule is stated here and the manifest's `certain: 57` is a row count, not a site count. Dedupe or declare the convention in the manifest.
3. **The notation-variant class was promoted though no *word* is absent (6 rows, 5 distinct sites: D-041, D-042, D-087, D-092, D-097/D-098 — all omitted word `percent`).** The transcript writes the symbol: `101% radiating cat-ness` vs book `101 percent radiating cat-ness`; `78%` vs `78 percent`. Nothing the speaker said is missing — the difference is `%` vs the word, i.e. notation, and the q2 README itself lists "abbreviation/expansion differences" among the dominant false-positive shapes. Under the owner's enacted wording ("a word clearly present in that ground-truth span **is absent** from the transcript") these rows do not obviously qualify. They need either refusal or an explicit per-row justification plus a stated notation-equivalence rule (symbol↔word, abbreviation↔expansion). This is a classification defect, not a citation defect — the bytes are exact.
4. **Reporting — the 57 is not stratified, and the flat headline would mislead M6.** The promoted set consists of: **24 interjections/discourse markers** (`huh`×7, `see`×6, `yeah`×6, `right`×3, `man`, `well`), **+3 laughter/fillers** (`heh` D-067, `um` D-083, `haha` D-091) = **27 of 57 (47%)**; **6 notation variants** (`percent`); **11 function words** (`its`×3, `thats`, `really`, `hed`, `theres`, `may`, `including`, `quite`, `otherwise`); **~13 content-bearing** — including genuinely strong omissions (`osama` D-115: book "Is Osama bin Laden", transcript "Is Bin Laden"; `earphones` D-060; `realms` D-001; `things` D-014; `high` D-016; `bonaparte` D-081; `lincoln` D-079; `undoubtedly` D-103). Every row satisfies the letter of clause d-i, and the mechanics verify — but `PATTERNS.md §3` and both delivery documents now quote "**57/122 adjudicated CERTAIN**" with no stratification, and **no document states that whether the speaker actually uttered a filler is unknowable from text** (the campaign's standing disclosure is that no audio was heard). A flat 47% CERTAIN figure reads as 47% of the sample being transcription errors of substance; it is not.

### Ruled, and routed
- **Verdict: FAIL / INCOMPLETE.** PASS: L1, L2, L3-mechanics (57/57), L4, L6, items 0/0a/0b/0c, §8 manifest, replay, ledger invariance, holdout untouched, suite. FAIL: L5 (false seeded sentence), counting hygiene (2 duplicate sites), the notation-variant class (6 rows), reporting stratification + audio-unknowability statement.
- **No pause is warranted** — unlike q1–q5 this delivery's substance verifies byte-exactly and nothing protected moved. **Restriction instead:** the 57 (and any "47%") may **not** be quoted without (a) the flank-floor sensitivity band 71/57/33/22, (b) the stratification above, (c) the deduped site count 55, and (d) the notation class's status. The CERTAIN-leg-d set is **not usable in any M6 document** until items 0d–0f below land.
- **Gate question routed to owner / BOSS-2 (I do not decide it):** does clause d-i reach (i) speaker-side fillers and interjections (`huh`, `yeah`, `see`, `heh`, `haha`, `um`) whose presence in the book transcription but absence in the ASR transcript may reflect either party's transcription choice, and (ii) notation variants (`%` ↔ `percent`)? The mechanics are compliant; the campaign's purpose is transcription errors that bear on doctrine. My recommendation, for the record only: keep them in the file, refuse the notation class, and publish the strata so the owner sees what leg (d) buys.
- **Additions to TASK-018 (same scope, no new artefacts):** **item 0d** — append-only correction of the SUMMARY seeded sentence (true overlap 0/122; where `seeded` lives); **item 0e** — dedupe or declare the row-vs-site convention in the manifest and re-state `certain` accordingly; **item 0f** — publish the stratification table (interjection/filler, notation, function word, content) and the audio-unknowability statement, and re-adjudicate or justify the 6 `percent` rows. Re-gate criteria **L7** (seeded sentence corrected append-only, overlap figure stated), **L8** (dedupe rule stated, site count published), **L9** (strata + notation ruling visible in SUMMARY and in PATTERNS §3, with the sensitivity band and the restriction carried alongside every quotation of the number).
- Standing: no detector promoted, no rate, no M6 figure, no HIGH; the 65 CANDIDATE rows stay CANDIDATE; `proposed_leg_d` remains NOT in force. **The two refused hand-verified fixtures are the right call** — refusing D2-002/D2-004 because two-word restoration exceeds the owner's singular "the word" traces to the owner's own enacted text, and it beats the 2/4 headline.

---

## TASK-019 quantum a — fresh sealed holdout split v2: **FAIL / INCOMPLETE on v2.5 only** (seal stands, is NOT void; no pause)

**ORCH-2 · gated 2026-09-25T21:46:52Z · worktree of WORKER-2 head `ffb8811` · seal commits `293b29c` (20:50:46Z) and `79eb401` (20:51:54Z) · `tools/HELD-OUT-SPLIT-V2.json` sha256 `73d86f0d…` (recomputed by me, equals the digest the delivery record cites).** Authority: owner ERRATA-2026-09-25g §5 — a fresh sealed split, new salt, sealed before further tuning, evaluated once; M6-Final waits for it. Criteria v2.1–v2.6, v2.9 (v2.7/v2.8 are quantum b and remain blocked).

### Re-derived by me, from the corpus on disk
- **v2.1 PASS — set equality, not counts.** Salt `fleetyard-m4-holdout-v2-2026-09-25` is fresh (v1: `fleetyard-m4-holdout-2026-09-25`); method, modulus and bucket are published in the file (`sha256(SALT+basename) mod 5 == 0 → HOLDOUT`, fixture transcripts forced to TUNING). I recomputed the assignment myself over the 230 overlay basenames: my drawn holdout minus forced = **the committed holdout, set-equal (33)**; the complement = **the committed tuning, set-equal (197)**. Disjoint, covering, no duplicates; `counts` and `by_year` agree with the lists (197 + 33 = 230, by_year sums 197/33).
- **v2.2 PASS.** The derivation is written out (`derivations.corpus_files_sha256`: sha256 over `"\n".join(sorted basenames) + "\n"`, list digest not content digest, content pinned by the corpus zip) and my recomputation reproduces `9ae90185ac0f4030…` exactly — the same value v1 carried, correctly, since the corpus did not change.
- **v2.3 PASS.** All six fixture-bearing transcripts (`A_Unique_Sedona_Seminar_Dec_2008_Part_2`, `Love_Sep_2011_Part_1`, `Satsang_Series_Volume_IX_Part_6` carrying the 16 CF fixtures; `Causality_…Part_1`, `Causality_…Part_3`, `Love_Sep_2011_Part_2` carrying D2-001…004) are in the corpus, in the forced list, and in **TUNING**; **zero fixture-bearing transcripts in the v2 holdout**. The spent v1 holdout is handled the right way round: all **37** are forced to **tuning**, **0** appear in the v2 holdout, and the recorded `v1_holdout_forced_tuning` equals v1's actual holdout set. The contamination-avoidance rule and its reason are written into `derivations.forced_transcripts` and into per-file `forced_with_reasons`.
- **v2.4 PASS — commit-order evidence.** Seal at 20:50:46Z/20:51:54Z; the only post-seal tuning work is `1cd5d44` (21:06:12Z, q3 shipping evidence) and `a5dec38` (21:21:03Z, TASK-020 delivery). `runs/m4-q3-format/PROVENANCE-V2.json` binds `split_file: tools/HELD-OUT-SPLIT-V2.json`, `split_counts 197/33/230`, `transcripts_read_count: 197` with a digest of the read list, `holdout_enforced: true`, `holdout_reads: []`. The pre-seal v1-tuning signal file is explicitly labelled a **historic artefact** and *not replayed*, with the reason given: 33 of its files are now v2-holdout members. That is the correct discipline — reusing it would have opened the holdout.
- **v2.6 PASS — the guard is code, not a claim.** `tools/m4_q3_evidence.py` carries a `HoldoutGuard` that raises `SystemExit` on any holdout name (refusing to read), the split loader rejects a file missing `tuning`/`holdout`/`corpus_files_sha256` and reports any overlap, and the run appends `holdout touched: …` to its problem list if the guard's read log ever intersects the holdout. Output evidence checks out independently: `signals-v2tuning.json` has **197** keyed entries, **all ⊆ v2 tuning**, **∩ holdout = 0** (my own test).
- **v2.9 PASS.** The delivery record is headed `TASK-019a DELIVERY`, states *"status: DELIVERY (not completion, not certification); no evaluation was run"*, and claims no promotion. One-shot discipline is intact: nothing in the tree evaluates the v2 holdout (only 9 files reference the seal — provenance, tools, tests).
- **Tests:** `tests/test_m4_split_v2.py` — **10 tests, OK**, and they test the properties that matter (`test_spent_v1_holdout_is_entirely_excluded_from_v2_holdout`, `test_sets_are_disjoint_and_forced_are_in_tuning`, `test_salt_is_fresh`, `test_bucket_rule_is_published_and_deterministic`, `test_manifest_binds_law8_fields`, `test_re_seal_rule_is_recorded`). `tools/m4_split_v2.py` exists at head and its digest **equals** the manifest's `tool_sha256` `fe043aee…`.
- **The `disclosure` text is the right shape** and I endorse it verbatim as the framing for quantum b: *"a first figure under v2 is an estimate under this split, not a pristine out-of-sample number"* — v1 detectors were shaped with corpus-wide knowledge — *"what the split guarantees is that FUTURE tuning cannot silently consume the transcripts it is later measured on."*

### What fails
- **v2.5 FAIL — one bound input digest no longer verifies at head.** `fixture_sources` binds `fixtures/v2/dropword.json` at `c8e96319…`; the file at head is **`c40d272f…`**, changed post-seal by TASK-020 item 7 (`a5dec38`, 21:21Z, 87 insertions / 0 deletions). `fixtures/confirmed/confirmed.json` still verifies (`f2c15869…` ✓), and every other manifest binding recomputes MATCH (book store `c0892fcd…`, corpus zip `3f36c520…`, policy `0fe20a60…`, `main_head 7d033ab`, `tool_sha256` ✓). This is the same fail-closed hazard I failed q5.7 for: a reader who verifies the seal at head gets a mismatch on a bound input and has no dated note telling them why.
- **I audited the change before ruling on it, and the seal is NOT void.** Comparing the seal-time blob (`79eb401`) with head: fixture **count unchanged (4)**, **no ids added**, and per-fixture **no change to `status`, `confidence`, `evidence`, `quoted`, `char_offset`** — only annotation keys appended (`enacted_leg_re_adjudication_2026_09_25`, `status_appended_2026_09_25`, plus set-level `enacted_leg_d_note_2026_09_25`, `generated_utc_exact(+_source)`). The TASK-018 confirmations (D2-001, D2-003) were made at **20:38Z, before the seal**, so the file's own `re_seal_rule` ("if any fixture is confirmed after this seal, the split is VOID") is **not triggered**. No fixture was confirmed after the seal; nothing was re-drawn.
- **Terminology, for the record:** the 20:51:54Z commit is called a "re-seal", but my diff shows it changed **only the `manifest` key** (adding `tool_commit f4ab7bb` + `tool_sha256`); salt, method, holdout, tuning and counts are identical to `293b29c`. Two seal digests therefore exist for **one** draw. Say so in the note, or a future reader will suspect a second draw.
- **My own instrument, again:** my first membership test reported the fixture transcripts as "not in tuning" because fixture files store **paths** (`corpus/docdocgo/overlays/X.txt`) while the split stores **basenames** — the written derivation already says `os.path.basename(fx['transcript'])`, i.e. the seal is right and my checker was wrong. Fourth such artifact this cycle (curly apostrophes, em-dash gluing, hyphen tokens, path-vs-basename). Every set claim I check now gets its key convention stated in the record.

### Ruling
- **Verdict: FAIL / INCOMPLETE on v2.5; PASS on v2.1, v2.2, v2.3, v2.4, v2.6, v2.9.** The seal is **valid, reproducible, uncontaminated and NOT void**. No pause; nothing else is restricted.
- **Item v2.a (single append, no re-draw, no new salt):** append a dated note to the seal file (or a companion `SEAL-V2-NOTE` record referenced from it) that (i) binds the post-append digest `c40d272f…` of `fixtures/v2/dropword.json` with the reason for the change and the commit (`a5dec38`), (ii) records the audit result — 4 fixtures before and after, no ids added, no `status`/`confidence`/`evidence` change, the two confirmations dated 20:38Z i.e. **pre-seal** — and (iii) states explicitly that the `re_seal_rule` was evaluated and **not triggered**, plus that `79eb401` changed only the `manifest` key so `293b29c`/`79eb401` are one draw. Re-gate criterion **v2.10**: every bound digest in the seal file recomputes MATCH at head, and the note is append-only.
- **Restriction on quantum b:** the one-shot holdout evaluation must **not** run until item v2.a lands — v2.7 requires frozen inputs, and a bound input that does not verify is not frozen. Everything else about the split is ready: thresholds to be frozen in advance, holdout read once, receipt consumed, no re-run.

---

## TASK-020 items 1–8 — M4 shipping-gap repair: **FAIL / INCOMPLETE** (20.1, 20.5; items 9–11 still owed; no pause)

**ORCH-2 · gated 2026-09-25T22:01:33Z · worktree of WORKER-2 head `ffb8811` · deliveries `1cd5d44` (21:06:12Z, q3 shipping evidence), `71c37cf` (21:06:45Z, claim), `a5dec38` (21:21:03Z, items 1–8).** Scope of this gate: **items 1–8 / criteria 20.1–20.8 + 20.9 global**. Items 9–11 (criteria 20.10–20.12: q4 holdout manifests, the PATTERNS §5d exposure-normalized correction, the three stale ledger-digest lines + q5's numbers) are **not delivered** and stay open.

### Verified by my own recomputation
- **Every content digest in all five supplement artefacts recomputes MATCH at head.** q2 (`runs/m4-q2-dropword/PROVENANCE-SUPPLEMENT.json`): all six part digests (`64a97be5`, `aa84a90f`, `092d6341`, `00769efc`, `d81406aa`, `ef6c7910`), merged `signals.json` `8d71f57b…` (122 signals), `detector_sha256_at_head` `a0236325…` = my digest of `tools/det_dropword.py`, and `config_sha256` `40945872…` recomputed from the stated recipe (`json.dumps(params, sort_keys=True, separators=(',',':'))`) over all 8 params. q3: `detector_sha256_at_head` `ef9ff4f2…` = my digest of `tools/det_format.py`, `config_sha256` `8e7e35a2…` recomputed, `signals.json` `86c8f57d…` and `signals-v2tuning.json` `b25651e4…` both MATCH. Book store `c0892fcd…`, corpus zip `3f36c520…`, policy `0fe20a60…`, `main_head 7d033ab`, split `9ae90185…` + counts 197/33/230 all present and correct. `EVIDENCE-PROVENANCE.json` repeats the same bindings consistently.
- **The attribution bridges quote my gates accurately.** q2: *"ORCH-2 re-ran shards 1 and 3 at head and got byte-identical part-1.json (`64a97be5…`) and part-3.json (`092d6341…`) = 66/193 transcripts and 93/122 signals"* — that is verbatim what my q2 record says (GATES.md q2.6), and the pin-defect text (`84e5407f…` resolves to no committed blob; `012914d` = `588e1f22…`; `4e114f1` = `a0236325…` = head) matches my q2.4 finding exactly. q3: *"ORCH-2 reproduced the whole run at head and got byte-identical signals.json (`86c8f57d…`)"* — matches. No number is attributed to me that I did not publish.
- **20.4 PASS, byte-exact.** The clean set is stored as hashed pointers into the book store (59 × {id, slug, char_offset, length, sha256}). I re-derived **59/59 passage digests from the store, byte-exact**; the EVAL detail covers all 59 ids with identical digests; total signals across them = **1** = the published FP. The FP is `CL-026`, local 469–472, quoted `'r.W'` — the bytes are there, in the context *"an ineffectual substitute for power.When, as in our society"* → **the book store's own typography**, exactly the misfire I found in my q3 probe. q2's three clean-set misfires (`CL-034` `'meaninglessness. Power'`, `CL-035` `'them as'`, `CL-055` `‘nothing ‘out’`) also re-derive byte-exact at their offsets, all three marked `source_inherited: true`, 3 → **0** after the filter, with the reading stated: *"a book passage cannot drop words from itself — every hit is a misfire; this is a misfire check, not a precision measurement."*
- **20.5 arithmetic reproduces under my own code.** I re-ran the source-inheritance rule (transcript span ±30 chars occurring verbatim in the book store) over all 122 signals: **exactly 1 suppression**, the same one the supplement names (`Most_Valuable_Qualities…May_2011_Part_2` @457, dropped `'quite'`, book `the_wisdom_of_dr_david_r_haw`). The deferred class also reproduces: **7 signals in 4 transcripts that are v2-holdout members**, and the supplement *declines to filter them* with the reason written down — reading them would open the sealed holdout — citing my own pre-seal 1/122 measurement. That is the right call and I endorse it. 122 − 1 − 7 = **114** ✓; `filtered_if_deferred_were_kept` 121 = 122 − 1 ✓. q3: 48 raw → 48 filtered, 0 inherited ✓ (per-rule 25+2+5+12+3+1 = 48 ✓).
- **20.5's shape instrument answers my q2.8 restriction honestly.** `shape_adjudication` classifies all 122: **113 consistent / 3 dropped-token-not-missing / 5 partial-overlap / 1 gate-boundary-excluded** (sums to 122), names my three cases verbatim (*"`evidence` @2574, `staggering` @54983, `sovereign` @55220 … reproduced as dropped-token-not-missing"*), marks the token-already-in-span class **"EXCLUDED from any count"**, and attributes the `one-third` item to **my own hyphen tokenization** as a checker artifact — which is what I concluded. `count_reconciliation` publishes raw 122 / countable 113 / gate_figure 113 / re_labelled_needs_human_read 6.
- **20.6 PASS — this repairs q2.1d and q3.4 properly.** `runs/m4-q2-dropword/README.md` carries a per-parameter provenance table for **all 8** thresholds (`window` 24, `stride` 12, `min_score` 0.20, `top_k` 3, `min_matched` 10, `min_ratio` 0.85, `max_drop` 2, `min_flank` 3), each "chosen by inspection … on the v1 tuning half (193 transcripts); not fitted by any optimiser", plus a **"What that costs, stated plainly"** section: the operating point is *unchosen*, sensitivity is unmeasured, and — correctly — that measurement **cannot** be made inside v2 discipline because 33 of the 193 v1-tuning transcripts are v2-holdout members, so it is deferred to split v3 or an ORCH-2 gate-side scratch and recorded as a limitation. q3 states C2-format has **no numeric thresholds** (7 shape predicates) with the rule-shape provenance. The rejected rules are published as **five reproducible probes** scoped to the v2 tuning half (P1-double-word 2876 hits/195 files; P2-camel-any-internal-capital 104/53; P3 6/6; P4-camel-classic 3/3; P5 2/2) with a `historic_note` disclosing that the pre-v2 camel-glue 35/18 figure was measured over all 230 and its exact pattern was not recorded — **this replaces my unreproducible number with a verbatim-reproducible table**, which is what my q3 gate asked for.
- **20.2 PASS.** Per-fixture tables exist for **both** detectors over all 16 CF fixtures with per-fixture detail, both labelled in-sample/seeded and both reading **0/16** — the honest result, and it matches my own probe. The label is explicit: *"IN-SAMPLE / seeded — the fixture transcripts are forced-TUNING by the seal; this is never recall evidence (LAW §9)."*
- **20.3 PASS.** `tools/PATTERNS.md §3` rows 44–45 no longer say "not built": drop-word carries 122 signals, the 57/65 adjudication with its run dir and tool commit, fixture recall 2/4 provisional, precision **unmeasured**, promotable **no**; speaker/format carries 49 v1 + 48 v2 tuning signals with digests, fixture recall 0/16, the q3 gate status and the rebuilt shipping evidence, promotable **no (restriction stands)**. The in-sample caveat paragraph is intact.
- **20.7 PASS** (verified in the TASK-018 gate): `fixtures/v2/dropword.json` appended 87/0 with the enacted-leg note, per-fixture re-adjudication blocks, and `generated_utc_exact` **plus the source of that value**.
- **20.8 PASS.** The delivery record reconciles the lane suite at **217 tests, OK** against the campaign baseline of v1's **115** (exceeded by 102) and resolves the dangling instruction; my own run at head gives **217 OK with 1 skip** (`test_report_m6.test_committed_report_is_current`, which fails closed while M6 is BLOCKED).
- **20.9 PASS.** No threshold changed (config digest matches the shipped params); no precision, rate or M6 figure anywhere; every status line reads *"CANDIDATE-class raw signals, unreviewed; PROVISIONAL-UNGATED; … not promotable and no omission count may be quoted … until ORCH-2 re-gates"*; `holdout_reads: []` and `holdout_enforced: true` in all of them; the ledger is untouched.

### What fails
- **20.1 FAIL — the `tool_commit` pins do not contain the tools that produced these files.** `runs/m4-q2-dropword/PROVENANCE-SUPPLEMENT.json`, `EVAL.json` and `EVIDENCE-PROVENANCE.json` pin `tool_commit 71c37cf` (the CLAIM commit, 21:06:45Z): at that commit **`tools/m4_t20_supplement.py` does not exist** (it is introduced by `a5dec38`) and neither does `tools/m4_q2_evidence.py`; `runs/m4-q3-format/EVAL.json` pins `2bbb9f6` (a cadence commit, 20:56:22Z) which contains **none** of the three tools; `runs/m4-q3-format/PROVENANCE-SUPPLEMENT.json` pins `71c37cf`. So the pins are reachable but **not attributable** — a reader cannot check out the pinned commit and re-run the instrument — and the five files disagree with each other. This is the same defect class the task exists to repair (q2.4/q3.5 failed because `detector_sha256` resolved to no committed blob). The *detector* pins are fine (`a0236325…`, `ef9ff4f2…` both match head, and `det_dropword.py` is unchanged between `71c37cf` and head). **Repair (item 8a):** re-pin every supplement to a commit that contains the generating tool (`a5dec38`), or add `generator_tool` + `generator_tool_commit` + `generator_tool_sha256` alongside the existing `tool_commit`, consistently across all five files.
- **20.5 FAIL — the shape/filter dispositions contradict the TASK-018 adjudication in the same head, and nothing reconciles them.** Two promoted rows are classified the opposite way by the worker's own instruments at the same commit:
  - **D-002** (`Causality…Part_1` @2574, omitted `evidence`) is `CERTAIN-leg-d` in `adjudication.jsonl`, while `EVAL.json`'s `shape_adjudication` gives that exact site `kind: dropped-token-not-missing`, `book_side_repeated_tokens: ['evidence']`, **`counting: "EXCLUDED from any count"`** — my own battery reached the same reading independently (the book has "evidence; evidence of", the transcript has it once, so what is missing is a *duplicate*, not a word).
  - **D-039** (`Most_Valuable_Qualities…Part_2` @457, omitted `quite`) is `CERTAIN-leg-d`, while the source-inheritance filter **suppresses that exact signal** (`source_inherited: 1`, and it is the filter's own published example) on the ground that *"the transcript was book text, so the wording difference is a cross-book self-parallel, not a drop"* — a suppression I reproduced with my own code.
  Both artefacts are CANDIDATE-class and neither is quotable, so nothing false has been shipped; but `PATTERNS.md §3` now quotes "57/122 adjudicated CERTAIN" from one instrument while the sibling instrument excludes/suppresses 2 of those 57, and no document says so. **Repair (item 8b, jointly with TASK-018 item 0g):** disposition D-002 and D-039 in `adjudication.jsonl` append-only (demote with the reason, or justify the promotion against the contradicting instrument), and carry the reconciliation into `SUMMARY.md` and `PATTERNS.md §3`.
- **New criterion 20.13 (cross-artefact coherence):** for every signal, the disposition recorded by each instrument (shape class, filter status, adjudication verdict) must agree, or the disagreement must be written down with a ruling. A count quoted in `PATTERNS.md` must equal the count the cited artefact actually supports after its own exclusions.
- **Routed to TASK-019 (item v2.b, criterion v2.11) — v2-holdout taint of the shipped signal set.** Seven of the 122 signals sit in **four transcripts that are v2-holdout members** (`Radical_Subjectivity…Feb_2002_Part_2` ×4, `Realization_of_the_Self_as_the_I_Nov_2003_Part_1`, `Spiritual_Traps_Oct_2005_Part_2`, `Witnessing_and_Observing_Oct_2004_Part_1`), and **three of the seven are promoted CERTAIN-leg-d: D-092 (`percent`), D-093 (`it's`), D-094 (`huh`)** — all in the same file — with four CANDIDATE (D-095, D-107, D-108, D-122). The seal's `disclosure` does not say this. The worker's handling was correct (the filter deliberately deferred those 7 rather than open the holdout, and the q2 README states the same reason for deferring threshold sensitivity), but quantum b's one-shot evaluation must now either report a per-file breakdown disclosing that 4 of the 33 holdout transcripts already carry C1-drop signal rows, or exclude those 4 with the denominator change stated. **My own disclosure:** verifying the filter rule required me to read the span bytes of all 122 signals, including those in the 4 holdout transcripts. That was gate re-derivation, not tuning — no rule, threshold or filter changed as a result — but it belongs in the seal note so the record of who has seen holdout bytes is complete.

### Ruling
- **Verdict: FAIL / INCOMPLETE. PASS: 20.2, 20.4, 20.6, 20.7, 20.8, 20.9 and 20.3. FAIL: 20.1, 20.5.** Items 9–11 (20.10, 20.11, 20.12) remain **undelivered**; the task stays open and q4/q5's failed criteria stay failed until they land.
- **No pause.** The repair is documentary and small: two re-pins and two row dispositions. **Restriction:** the supplements' digests and measured cells are trustworthy (all recomputed MATCH by me) and may be cited **with** their `PROVISIONAL-UNGATED` status lines; no count from either detector (122, 114, 113, 48, 0/16, 1/59, 3/59→0) may be quoted without that status and, for C1-drop, without the shape/filter dispositions and the TASK-018 restrictions (sensitivity band, strata, site count 55, notation class).
- **Credit where it is due:** this delivery repaired the worst of what I failed — every digest now recomputes, the shipping evidence exists and its citations are byte-exact under my own re-derivation, the threshold provenance is stated with its cost plainly named, the unreproducible camel-glue figure was replaced by five reproducible probes, and the holdout was protected by *declining* to run a filter over it. The two failures are attributability and cross-artefact coherence, not substance.

---

## TASK-017 — inherit the v1 detector toolchain onto the WORKER-2 lane: **PASS (all six criteria)** + one non-blocking item

**ORCH-2 · gated 2026-09-25T22:08:00Z · worktree of WORKER-2 head `ffb8811` · delivery `b2e0761`, record `fleet/branches/WORKER-2-TASK-017-DELIVERY.md` · archive `origin/arena/01a0d581-fleetyard` @ `bf97d85` (ENDED, read-only).** First PASS of this cycle.

### Verified independently
- **Criterion 1 PASS — and I verified it exhaustively, not by sampling.** For **all 266** manifest entries (`tools/` 15, `tests/` 13, `fixtures/` 5, `runs/m5-raw/` 233) I recomputed three ways: (i) the digest of the file **at head** equals the manifest's `sha256`; (ii) the digest of `git show bf97d85:<path>` equals the manifest's `in_archive_sha256`; (iii) **head == archive** for every file, which is what makes `unmodified: true` true. **0 mismatches out of 266.** Completeness both directions: the archive contains exactly **266** files under those four roots — **0 archive files unlisted** in the manifest and **0 manifest entries absent from the archive**. `tools/` at head holds 32 files (all 15 inherited present, 0 missing, 17 new M4 tools); `tests/` holds 21 (13 inherited + 8 new). The archive is cited and never re-stamped (`archive_commit_note`: *"read-only archive lane (HALT-2026-09-25.md); cited, never re-stamped"*) — exactly what LAW §8 requires for inherited data.
- **Criterion 2 PASS.** My own run at head: **217 tests, OK, 1 skipped** — the skip is `test_report_m6.test_committed_report_is_current`, which fails closed while M6 is BLOCKED and is not a corpus or environment skip. The delivery's arithmetic checks out: lane ran 39 before, the inheritance adds the v1 baseline **115**, so **154 = 115 + 39** at delivery, skips fell 5 → 1 because the census is now present; at head the count is **217 ≥ 154 ≥ 115**, so STANDARDS' "test count never drops" now has teeth on this lane and has not been broken.
- **Criterion 3 PASS — reproduced by my own run.** `python3 tools/fixtures.py verify` → **`fixtures OK (16 confirmed CERTAIN)`**, verbatim as claimed; `corrections.json` (withdrawals CF-005/009/013/014/018) is in place and byte-identical to the archive; the 16 confirmed fixtures resolve against the frozen corpus + book store (`3f36c520…` / `c0892fcd…`, both recomputed MATCH this cycle).
- **Criterion 4 PASS.** No inherited detector logic was modified: proven by the 266-file head==archive equality above, and the toolchain ran as-is against `corpus/` (no lane-specific shim, no disclosed diff needed).
- **Criterion 5 PASS — with my own fresh run, four-way equality.** The shipped record `runs/m5-raw-freshcheck/fresh-vs-inherited.json` claims 10 transcripts / 132 records / 10 identical. I re-ran the inherited sweep myself (`tools/sweep_m5.py --out <gate-scratch> --limit 10 --fresh`, 43 s, **132 records, 0 failures**) and compared all four digests per file: **inherited census == manifest's `sha256_inherited` == the worker's `sha256_fresh` == MY fresh sweep output, 10/10**; record count **132 = 132**. So the fresh evidence exists on both sides of the gate, which is what LAW §7 asks for (identical deterministic output is not suspicion; *missing* fresh evidence is). I also verified the census duplication claim: `runs/m5-raw/records` (230) and `evidence/runs/m5-raw/records` (230) are **230/230 byte-identical**, and `INDEX.md`, `PROVENANCE.md`, `index.json` are identical too.
- **Criterion 6 PASS.** No `urllib`/`requests`/`socket`/`http.client` anywhere in `tools/`; stdlib only; `subprocess` appears in `sweep_m5.py` (the disclosed git call for the zip-hash note), `report_m6.py` (`git rev-parse HEAD`) and `cadence_watch.py` (WORKER-2's own lane automation: git fetch/add/commit/push — not part of the inheritance, and git-only). Reads `corpus/**` + the inherited tree; writes only under `--out`.

### One item owed (non-blocking)
- **Item 17.a — `materialised_utc` is fuzzy: `"2026-09-25T20:5xZ"`.** No exact value and no source. This is the same defect the lane already fixed once, properly, in `fixtures/v2/dropword.json` (`generated_utc_exact` + `generated_utc_exact_source`, with the fuzzy value superseded and left readable). Apply that pattern here: append `materialised_utc_exact` (the committer timestamp of `b2e0761` recovers it) plus its source. **Why this does not block the PASS:** no count, digest or verification depends on the value, every substantive claim in the delivery reproduces exactly under my own runs, and the fix is a single append. Advisory alongside it: the inheritance manifest carries the archive ref/commit and per-file digests (what criterion 1 asks) but not `main_head` / `policy_sha256`; adding them would make it symmetric with the run manifests.

### Ruling
- **Verdict: PASS on criteria 1–6.** Item 17.a owed, non-blocking, append-only. **Consequences:** the v1 toolchain is now attributable on the working lane — B1/B2 validation, detector work and the M6 report path are unblocked from the toolchain side; the inherited census is a verified baseline for fresh runs; and the "test count never drops" promise is enforceable here (217 at head). This PASS does **not** promote any detector, certify anything, or change any M4 verdict: q1–q5 remain FAIL/INCOMPLETE, TASK-018 and TASK-019a and TASK-020 items 1–8 remain FAIL/INCOMPLETE as gated this cycle, no rate, no M6 figure.

---

## ORCH-2 SELF-CORRECTION (append-only) — one parenthetical in the TASK-018 gate was wrong; the finding stands

**2026-09-25T22:52:19Z · verified at WORKER-2 head `4fc40c8`.** In the TASK-018 gate (item 1 of "What fails") I wrote that no row in
`adjudication.jsonl` carries `seeded: true` **"(0/122 — the field does not appear)"**. The parenthetical is **incorrect**:
the `seeded` key **is present on all 122 rows**, with the value **`false` on all 122** (`in_sample: true` on all 122).
The substantive finding is unchanged and re-verified at `4fc40c8`:

- rows with `seeded: true` = **0 of 122**, and **0 of the 57** CERTAIN rows → `SUMMARY.md`'s sentence *"4 of the 57
  CERTAIN rows carry `seeded: true` (they overlap a v1 hand-confirmed fixture span)"* is **false**;
- my overlap test against the **16** v1 CF fixture spans (transcript + offset interval intersection): **0 of 122** rows
  overlap any of them;
- the four `seeded: true` rows are exactly `FIX-D2-001…004` in `fixtures-adjudication.json` (2 CERTAIN, 2 CANDIDATE).

**Credit where it is due:** because every row carries both flags, the adjudicator implemented the seeded/in-sample
separation correctly **in the data**; the defect is purely prose, in `SUMMARY.md` — and, since `4fc40c8`, in
`tools/PATTERNS.md §5b-bis`, which repeats the same false sentence (*"Four of the 57 are `seeded: true` (they overlap
v1 hand-confirmed fixture spans)"*). **TASK-018 item 0d therefore covers both documents.** I am recording my own error
here because a worker following item 0d would look for a missing field, find it present, and could reasonably conclude
the gate was wrong. It was not — but my wording was, and the wording is what a repairer reads.

---

## TASK-020 items 9–11 — q4 holdout manifests, PATTERNS §5d correction, stale digests + q5's numbers: **FAIL / INCOMPLETE on 20.10 only** (20.11, 20.12 PASS with two small items owed)

**ORCH-2 · gated 2026-09-25T22:52:19Z · worktree of WORKER-2 head `4fc40c8` · deliveries `d7fee6e` (21:27:18Z, items 9–11) and `4fc40c8` (21:27:50Z, PATTERNS leg-(d) binding).** Criteria 20.10–20.12. Suite at this head, my own run: **227 tests, OK, skipped=1** (the M6-report skip). Invariants re-verified at this head: ledger `d42136c6…` (1334 records), by-transcript `c1ec4da8…` (230 files, my own `dir_digest`), `findings/PROVENANCE.json` binds `d42136c6…`, `tools/m5r_reduce.py` byte-identical across `219075a` → `ffb8811` → `4fc40c8` (`6d4bb9ce…`) so the **M5-R PASS stands**, split v1 `481d8513…` and v2 `73d86f0d…` unchanged, `signals.json` `8d71f57b…`, `adjudication.jsonl` `82863ab9…`, `SUMMARY.md` `0a37118e…`, `fixtures-adjudication.json` `61568a9e…`, `signals-v2tuning.json` `b25651e4…`, `det_dropword.py` `a0236325…`, `det_format.py` `ef9ff4f2…`.

### 20.10 — q4 supplement manifests: **FAIL on the `tool_commit` pin only**; every other binding verified
- **All digests recompute MATCH** in `runs/m4-q4-holdout/PROVENANCE-SUPPLEMENT.json`: `v1-holdout.json` `cf8e7a7a…` (127733 bytes), `part-holdout-drop.json` `7ffa7a77…` (4611), `part-holdout-format.json` `a837ab32…` (6630), the three `*.PROVENANCE.json` digests (`1aa37a60…`, `3d2ec2ce…`, `5d935515…`), and all three **config digests** recomputed from the params (`19353270…`, `40945872…`, `805241dd…`). Corpus zip `3f36c520…`, book store `c0892fcd…` **with a `book_store_why` explaining that it is load-bearing**, split file + salt + `corpus_files_sha256 9ae90185…`, `main_head 7d033ab`, policy `0fe20a60…`, `run_utc` exact to the second (21:22:29Z — no fuzzy value here), status "counts only — NOT precision; PROVISIONAL-UNGATED".
- **The 13 v1 toolchain pins are byte-identical to the archive lane — my own check, 13/13.** Each `runs/v1/toolchain/pins/<file>` equals `sha256(git show bf97d85:tools/<file>)` and equals the digest at head. The citation form is now `origin/arena/01a0d581-fleetyard:tools/<file>` + commit + blob, **replacing the sandbox path** `/home/user/fleetyard/evidence/tools` — which repairs the binding-form defect I recorded at q4.5. The supplement's attribution to me (*"ORCH-2 independently verified all 13 pinned shas byte-identical to that archive lane (q4 gate ea9be59)"*) is **accurate**: my q4.5 record says exactly that.
- **The B1 zero is explicit, with its consequence** — `B1-contradiction: 0`, `original_values` A1 162 / A2 15 / B2 8, and the note that the original provenance omitted B1 because a Counter drops zero counts, so **B1 receives NO validation from this run and v1's B1 headline hold (TASK-005 FAIL / REDIRECT-005) stands**. I confirmed the holdout side from the inherited census myself: the 37 spent-holdout transcripts carry exactly **185 rows = A1 162 + A2 15 + B2 8 + B1 0**. That is the receipt, reproduced independently, and the zero is no longer silent.
- **One-shot discipline verified in code, not taken on assertion.** `holdout_consumed: true` with *"the spent v1 holdout was NOT re-run to build this supplement; only digests of the committed artefacts were recomputed. Never re-run the spent holdout."* I read `tools/m4_q4_supplement.py`: **0** references to `overlays`, **0** to `parse_book_store`, **0** to `run_tuning`, two `open(` calls — it hashes committed artefacts and cannot read the corpus.
- **FAIL point:** `tool_commit ffb8811` **does not contain `tools/m4_q4_supplement.py`** (introduced by `d7fee6e`); the detectors and runner *are* present at that commit. Same defect, same repair as item 8a — **item 8a is extended to all six supplement artefacts**, with the convention stated: `tool_commit` = lane head at run time is acceptable **only** alongside `generator_tool` + `generator_tool_commit` + `generator_tool_sha256`.

### 20.11 — PATTERNS §5d exposure-normalized correction: **PASS**, with item 11a owed
- The wrong sentence is **left readable and contradicted in place** by an appended dated block — *"that the gaps are 'dominated by sampling noise' is **wrong for C1-drop**, and the fault was comparing per-file densities without normalizing by exposure"* — which is the append-only discipline item 10 asked for. The table prints observed / expected / P(X ≤ observed) for all three rows **and prints the gate's figures alongside its own**, two candidate causes are recorded as unestablished, the standing prohibition "never re-run the spent holdout to find out" is stated, the column header is renamed `rate/tx` → **"signals/tx — density, not a rate"**, and v1's B1 hold is declared untouched.
- **My own arithmetic:** exposure ratio = holdout chars / tuning chars = 1 996 122 / 12 228 661 = **0.16323** (exactly the published value). C2-format: 49 × 0.16323 = **8.0**, P(X≤12) = **0.9363** → published 0.94 ✓. C1-drop: 122 × 0.16323 = **19.9**, P(X≤5) = **7.677e-05** → published 7.7e-05 ✓. v1 leg: the inherited census over the 193 tuning transcripts gives **1149** rows (A1 775, B2 220, A2 142, B1 10, 2 combined) → **expected 187.6, P(X≤185) = 0.4451**, i.e. **my gate figure reproduces exactly**, while the published **187.9 / 0.44 does not** — the method is stated but the per-row tuning-side counts are not, so their variant is not recomputable by a reader.
- **Item 11a (owed, precision):** publish the tuning-side count per row (1149 / 49 / 122) so all three rows recompute, and reconcile 187.9 vs 187.6 (the census supports 187.6, P = 0.4451 → 0.45). The conclusion is unaffected either way: v1 consistent, C2-format consistent, **C1-drop a real ~4× deficit at P ≈ 7.7e-05**.

### 20.12 — stale ledger digests + q5's numbers: **PASS**, with item 11b owed
- **All three live documents** (`findings/README.md` L88, `findings/M4-q5-A1-CLAIM-RECONCILIATION.md` L51, `fleet/branches/WORKER-2-M5R-DELIVERY.md` L80) keep the superseded `64977c2f…` line **readable** and carry an appended **SUPERSESSION** block stating the current digest `d42136c6…` (1,334 findings), the cause (TASK-016's regeneration `a4c6655` rewrote the record shape two minutes after the q5 run), and — the structural fix — **"`findings/PROVENANCE.json` is the binding of record, not any digest quoted inside prose; any figure on this page is void unless that manifest agrees."** I verified the manifest: `outputs.ledger.jsonl` = `d42136c6…` = the actual digest at head. So no live document presents the superseded digest **as current**.
- **q5's numbers corrected append-only, and I re-derived the key one exactly.** The appended block (i) supersedes the 98/67 simulation tally with my **97 = 9 zero-ASCII-token + 61 over-bound + 27 ASCII-mismatch** while preserving the 98→0 argument, (ii) reports the worker's own independent re-derivation of **938 A1 claim_checks, 938 `claim_ok: true`** (matches my twice-verified 938/938), (iii) publishes the unit-size bound **with its full tally** — k=1 248 · 2 179 · 3 92 · 4 124 · 5 84 · 6 63 · 7 57 · 8 30 · 9 21 · 10 20 · 11 11 · **12 9** — and reframes `kmax=16` as max-observed-unit **+ exactly 4 tokens of headroom**, and (iv) records my **255/938 (27%)** hyphen-tokenizer sensitivity as the gate's figure with its caveat, not absorbed into a conclusion. **My own re-derivation of (iii) from the ledger's 938 A1 claim notes reproduces the distribution exactly, term for term, sum 938, max k = 12 with 9 claims.**
- **Item 11b (owed):** `tools/PATTERNS.md §5e` — a live catalogue section — still reads *"All **98** 'claim not re-derived' A1 flags … an 8-token search bound while A1 claims units **up to 11**"* with no supersession note, although the corrected figures (97; max unit **12** with 9 claims) now exist in `findings/`. Append the same treatment to §5e. **Restriction until then: §5e may not be quoted for those two numbers.**

### Item 12 + criterion 20.14 (new) — fuzzy timestamps are recurring
Four appended notes carry unverifiable timestamps: the three SUPERSESSION blocks *"appended 2026-09-25T21:4xZ"*, PATTERNS §5b-bis *"appended 2026-09-25T21:5xZ"*, and TASK-017's `materialised_utc "2026-09-25T20:5xZ"` (item 17.a). The lane already owns the correct pattern — `fixtures/v2/dropword.json`'s `generated_utc_exact` **plus `generated_utc_exact_source`**, with the fuzzy value superseded and left readable. **Item 12:** apply it to all four (committer timestamps of `d7fee6e` / `4fc40c8` / `b2e0761` recover them). **Criterion 20.14:** every appended note and every manifest timestamp is exact to the second and carries its source.

### Ruling
- **Items 9–11: FAIL / INCOMPLETE on 20.10** (one non-attributable `tool_commit` pin); **20.11 PASS** (item 11a owed), **20.12 PASS** (item 11b owed); item 12 + criterion 20.14 added. **TASK-020 as a whole stays FAIL/INCOMPLETE** — items 8a, 8b, 11a, 11b, 12 and criterion 20.13 are outstanding.
- **No pause.** The substance of items 9–11 verifies under my own recomputation, including the two things that matter most: the **B1 zero is no longer silent** and the **spent holdout was not re-run** (proven from the tool's source, not its manifest).
- **Credit:** this is the strongest repair delivery of the campaign so far — digests all recompute, the 13 pins verify against the archive lane, the wrong sampling-noise claim is contradicted in place rather than deleted, the corrected unit-size bound comes with a tally a reader can recompute (and I did), and the supersession blocks fix the *class* of the defect by naming the manifest as the binding of record.

---

## RE-GATES on the strength of TASK-020: **q1 → PASS**, **q4 → PASS**, **q5 → PASS** (q2 and q3 stay FAIL/INCOMPLETE)

**ORCH-2 · 2026-09-25T22:52:19Z · all re-gates at WORKER-2 head `4fc40c8`, invariants re-verified as listed above.**

### TASK-014 q1 (split + provenance) — **RE-GATE: PASS**
The only failed criterion was **q1.4d** (PATTERNS §3's corroboration column unbound to the ledger digest). Repaired and re-verified at `4fc40c8`: `tools/PATTERNS.md` now carries the ledger digest `d42136c6…`, the by-transcript digest `c1ec4da8…`, `tool_commit dada3e60…`, the worker head at which the figures were read `1beadd9…`, the policy digest `0fe20a60…`, a **written verification procedure** (sha256 over the ledger; sha256 over the sorted `<sha256>  <relpath>` lines of `findings/by-transcript/` via `m5r_reduce.dir_digest` → 230 files), and an append-only control note recording that `PAUSE-WORKER-A-2026-09-25-001` was REMOVED at 20:02Z on the M5-R re-gate PASS. I re-derived both digests myself at this head: `d42136c6…` and `c1ec4da8…` (230 files) ✓. The split itself is unchanged (`tools/HELD-OUT-SPLIT.json` = `481d8513…`, salt `fleetyard-m4-holdout-2026-09-25`, mod 5, 193/37, `corpus_files_sha256 9ae90185…` — recomputed by me again this cycle) and was committed pre-detector at `593cad3`. **q1 is citable as passed.** Standing notes: the v1 split's holdout is **spent**, v2 supersedes it for all future work, and this PASS promotes no detector and yields no rate.

### TASK-014 q4 (spent-holdout receipt) — **RE-GATE: PASS**
Both failed criteria are repaired. **q4.6** (missing §8 bindings): the item-9 supplement supplies corpus zip, book store (+ why it is load-bearing), split file/salt/digest, `main_head`, policy, exact `run_utc`, per-leg config digests, and output digests with byte counts for all three runs — **all recomputed MATCH by me** — plus the v1 toolchain cited as lane+commit+blob with **13/13 pins verified byte-identical to `bf97d85` by my own check**. **q4.8** (PATTERNS §5d "dominated by sampling noise" measurably wrong): contradicted in place by the exposure-normalized table, which my own arithmetic confirms (ratio 0.16323; C2-format 8.0 / P=0.9363; C1-drop 19.9 / P=7.677e-05; v1 leg 1149 × ratio = 187.6 / P=0.4451). **q4 is citable as passed**, with these standing restrictions: **185 / 5 / 12 remains a RECEIPT ONLY** — counts, not precision, and no rate may be quoted from this run; the **B1 zero** means B1-contradiction receives no validation here and v1's B1 hold (TASK-005 FAIL / REDIRECT-005) stands; the **spent v1 holdout must never be re-run** (a re-run requires split v3); precision for C1-drop and C2-format is gated behind **TASK-019 quantum b**; and the C1-drop deficit's two candidate causes remain **unestablished** (parameter fitting vs book-exposure difference — the latter testable only on split v2). Item 11a (publish the per-row tuning-side counts) is owed under TASK-020, not a q4 criterion.

### TASK-014 q5 (A1 claim-shape reconciliation) — **RE-GATE: PASS**
Both failed criteria are repaired. **q5.7** (three live documents presenting a superseded ledger digest as current): all three now carry appended SUPERSESSION blocks that leave the old line readable, state the current digest `d42136c6…`, explain the cause (`a4c6655`), and name `findings/PROVENANCE.json` as the binding of record — verified equal to the ledger at head. **q5.8** (numbers that did not reproduce): the appended block supersedes 98/67 with my 97 = 9 + 61 + 27, publishes the unit-size bound with a tally I **re-derived exactly from the ledger** (max k = 12, 9 claims, distribution summing to 938), reframes `kmax=16` as max-observed + 4 tokens headroom, and records the 255/938 (27%) hyphen sensitivity as the gate's figure with its caveat. **q5 is citable as passed**, and its substantive conclusion is unchanged and twice independently verified: the flags were **M5-R reducer instrument defects**, not v1 detector defects, and **A1 corroboration is 938/938** under my own direct claim test. Standing notes: `tools/PATTERNS.md §5e` still carries the superseded "98" and "up to 11" (item 11b) and **may not be quoted for those two numbers** until corrected; the hyphen-tokenizer sensitivity (27% of A1 claims) must accompany any reuse of the 938/938 figure; `kmax=16` has 4 tokens of headroom, not "≈11 + margin".

### q2 and q3 — **NOT re-gated yet**
- **q2** stays **FAIL/INCOMPLETE**: q2.1b/c/d, q2.4 and q2.5 are repaired or superseded by TASK-020 items 1–8 **except** the tool-pin attributability (item 8a), and **q2.2 (the classification leg) now runs through TASK-018**, whose adjudication set carries items 0d–0g. Until those land, the 122 signals stay CANDIDATE and the 57 CERTAIN-leg-d rows stay restricted (sensitivity band 71/57/33/22, strata, site count 55, notation class, D-002/D-039 dispositions).
- **q3** stays **FAIL/INCOMPLETE** on one point only: the q3 supplement's `tool_commit` pin (item 8a). Everything q3.2/q3.3/q3.4/q3.5 needed is verified — fixture recall **0/16**, clean set **1/59** with the misfire shown to be the book store's own typography (byte-exact by my re-derivation), §8 bindings all recomputing MATCH, threshold provenance for all seven rules, and five reproducible rejected-rule probes replacing the unreproducible camel-glue figure. **Item 8a alone unblocks the q3 re-gate.**

### Consequences of this cycle
**M4 quanta now citable as passed: q1, q4, q5.** q2 and q3 remain FAIL/INCOMPLETE. Nothing else moves: **no detector is promotable** (precision is unmeasured and gated behind quantum b), **no rate, no M6 figure**, the 122 drop-word and 48 format signals stay **CANDIDATE / PROVISIONAL-UNGATED**, **TASK-015 (M6 Final) stays BLOCKED** behind TASK-019 quantum b, and **M6-P remains owner-accepted and is not re-certified**. Ledger `d42136c6…` and by-transcript `c1ec4da8…` unchanged across every head examined this cycle → the M5-R PASS and the TASK-016 re-gate PASS stand.


---

## ORCH-2 SELF-CORRECTION #2 (append-only) — the q2.6 caveat figure `113/9` is WITHDRAWN and restated with its rule

**2026-09-25T23:32:36Z · verified at WORKER-2 head `4fc40c8` · full derivation in `fleet/ORCH-2-VERIFICATION-LEDGER.md` §10.**

My q2 gate published the caveat *"**113/122** fully consistent drops, **9/122** shape-defective — 3 repetition
artifacts, 6 partial-overlap of which 2 are my own hyphen tokenization."* Mechanising that check showed **no natural
rule reproduces 113/9**, so the figure is **withdrawn**. The restatement now binding:

- Under **rule A** — remove every occurrence of each dropped word from `tokens(suspected)` and compare with
  `tokens(quoted)`, apostrophes (straight **and** curly) normalised and hyphens kept inside tokens — **8 of 122** rows
  are shape-defective and **all 8 are repetition artifacts** (the dropped word occurs more than once in the book-side
  span, so removing every occurrence over-deletes: `"evidence; evidence of"` → `"evidence of"` with `['evidence']`).
- Under **rule B** (remove the **first** occurrence) **122/122** are consistent — the semantically right model, since
  the book side repeats and the transcript drops one copy.
- The **3 + 6 decomposition is withdrawn**; the "partial-overlap" class disappears once curly apostrophes are
  normalised (the 8 rows I had attributed partly to my own tokenization were an instrument defect, not a data property).
- **The token rule is load-bearing:** hyphen-splitting turns 114/8 into **67/55**. The number may not be quoted
  without naming the rule and the token convention.

**Unchanged by this correction:** every substantive q2 finding — 122/122 transcript spans and 122/122 book citations
byte-exact, my byte-identical shard reproduction (`64a97be5…` / `092d6341…`), keys == the v1 tuning 193 with zero
holdout reads, the filter arithmetic 122 − 1 = 121 − 7 = 114, and the verdict **q2 FAIL/INCOMPLETE** pending item 8a
and TASK-018 items 0d–0g. What changes is that the caveat is now **precise, mechanised and reproducible** instead of a
hand count nobody could re-derive — the same standard item 11a asks WORKER-2 to meet for `187.9`.

## GATE CYCLE H — TASK-019a quantum a and TASK-017 re-gated off ONE mechanized run (ORCH-2)

**2026-09-25T23:52:39Z · WORKER-2 head `4fc40c8` · instrument `fleet/gate-tools/orch2_verify.py` v3.1, 222 rows
(PASS 186 · FAIL 16 · INFO 18 · PROXY 2) · committed output
`fleet/gate-tools/orch2_verify_output_4fc40c8.txt` · suite at this head **227 tests OK, skipped=1** · derivation in
`fleet/ORCH-2-VERIFICATION-LEDGER.md` §11/§11.1.**

Both verdicts are **unchanged** from cycle G; what changed is that they are now reproducible by one command instead
of by hand, and that the item-v2.b enumeration is **derived from the data** rather than restated from memory.

### TASK-019a — quantum a (sealed split v2): **FAIL / INCOMPLETE on v2.5 and the v2.b note only**

v2.1 **PASS** · v2.2 **PASS** · v2.3 **PASS** · v2.4 **PASS** · v2.5 **FAIL (item v2.a)** · v2.6 **PASS** ·
v2.9 **PASS** · quantum b (v2.7, v2.8, v2.10–v2.16) **HELD** behind the pre-registration protocol.

The seal is **valid, reproducible, uncontaminated at the fixture level and NOT void**: 33 holdout / 197 tuning
set-equal under my own re-draw, zero fixture transcripts and zero spent-v1-holdout transcripts inside the holdout,
all 43 forced transcripts in tuning with reasons, sealed before every artefact that references it, guard in code.

**Item v2.a** — the seal binds `c8e96319…` for `fixtures/v2/dropword.json` while the file at this head hashes to
`c40d272f…`. Repair: a dated append-only seal note binding the actual digest and disclosing the taint, leaving the
superseded line readable.

**Item v2.b** — now **machine-checkable**, because the enumeration is derived: 7 deferred signals in 4 holdout
transcripts, carrying TASK-018 hand labels — 3 **CERTAIN-leg-d** (`D-092`, `D-093`, `D-094`) and 4 **CANDIDATE**
(`D-095`, `D-107`, `D-108`, `D-122`). The note must state (i) those four transcripts with the seven ids and
verdicts, (ii) that the shipped filter deliberately deferred them rather than open the holdout — endorsed, (iii) that
ORCH-2's gate re-derived span bytes for all 122 signals including these four transcripts, changing no rule or
threshold, and (iv) the quantum-b consequence: a per-file breakdown disclosing the 4 signal-bearing holdout
transcripts, **or** their exclusion with the denominator change stated **in the pre-registration, not afterwards**.

**Standing caveat carried into any quantum-b figure:** all 33 v2-holdout transcripts were read by the pre-seal
v1-era run (its keys are the v1 tuning 193, which contains the whole v2 holdout). The seal discloses this itself —
*"a first figure under v2 is an estimate under this split, not a pristine out-of-sample number"* — and that sentence
must travel with the number, in the same way self-item O-1 requires the token rule to travel with `8/122`.

### TASK-017 — inherited v1 toolchain: **PASS on all six criteria** (re-affirmed)

Three-way equality over **all 266** inherited files (33 tools/tests/fixtures + 233 census/runs): archive blob at
`bf97d85` == `in_archive_sha256` **266/266**; file at head == `sha256` **266/266**; the manifest's two per-file
claims agree **266/266**; counts 33 + 233 = 266; `unmodified: true`; the archive lane is cited read-only and never
re-stamped. **Item 17.a stands**: `materialised_utc` is the one genuine own-time offender among the 26 asserted
fuzzy timestamps, and it is repaired by the same rule as item 12 (exact to the second plus its source).

### Instrument self-report

Adding these sections produced four defects in my own tool (#21–#24, ledger §11.1), two of which would have
**failed sound criteria** in the dangerous direction: an add-time test that mistook a v1-era README for a post-seal
reference (fixed with `git log -S`), and a pattern-count that mistook `det_format.py`'s two real protections for
missing ones. A shadowed variable crashed the run outright. **Self-item O-2** is opened on my own lane: the
instrument owes a `--selftest` over a fixture tree with expected verdicts, so a refactor cannot silently move a gate
result; until it exists, every change is diffed against the committed output.

## ORCH-2 SELF-CORRECTION #3 (append-only) — the q2.6 figure `113/9` is **RESTORED**; self-item O-1's withdrawal over-reached

**2026-09-26T00:22:41Z · verified at WORKER-2 head `4fc40c8` · mechanized in `fleet/gate-tools/orch2_verify.py` §13 ·
derivation in `fleet/ORCH-2-VERIFICATION-LEDGER.md` §14.**

Self-item O-1 withdrew the q2.6 caveat figure *"113/122 fully consistent drops, 9/122 shape-defective"* on the
ground that **no natural rule reproduces it**. That was wrong, and the wrongness is instructive: I searched for a
*token-set* rule over the 122 signals, and the figure was never a token-set result. It is the count of a **documented
per-signal shape classification** that WORKER-2 published in `runs/m4-q2-dropword/EVAL.json` →
`shape_adjudication`, with a "needs human read" category that no token-set rule can express. **My own cycle-F gate
record already carried that decomposition** (`GATES.md`: "113 consistent / 3 dropped-token-not-missing /
5 partial-overlap / 1 gate-boundary-excluded"), so O-1 also contradicted my own earlier record without noticing it.
The failure mode: a self-audit that re-derives from a **narrower hypothesis space** than the gate it is auditing.

**What §13 now verifies mechanically (all rows PASS unless stated):**

| check | result |
|---|---|
| `shape_adjudication` classifies every signal | 122/122, one per row, with `kind`, `counting`, `deletion_closes`, `book_side_repeated_tokens`, `dropped_run_in_book_span`, `rebuilt_from_book_span`, `transcript_tokens` |
| recomputed `kind` tally == the published `counts` | **113 consistent · 5 partial-overlap · 3 dropped-token-not-missing · 1 gate-boundary-excluded** |
| `count_reconciliation` closes | raw 122 = countable 113 + excluded 3 + re-labelled 6; `gate_figure` 113; 6 = 5 partial-overlap + 1 gate-boundary |
| ORCH-2's rule-A failures vs the worker's shape exclusions | **SET-IDENTICAL, both directions: 8 = 8** (the 3 dropped-token-not-missing + the 5 partial-overlap) |
| the ninth row | `one-third of` dropped from `"States. One-third of the"`, `Positionality_and_Duality_Transcending_the_Opposites_Apr_2002_Part_2` @40831–40841 — it **passes** rule A under my token rule and **fails** under hyphen-splitting, which is precisely why the worker's instrument excludes it as "gate-listed hyphen-tokenization … pending a human read" |

**The restored, binding statement of the q2.6 caveat.** Of 122 C1-drop signals, **113 are shape-consistent and 9 are
not**: **3** are `dropped-token-not-missing` — the gate's own three named cases (`evidence` @2574, `staggering`
@54983, `sovereign` @55220), where the "dropped" token already occurs in the transcript span, so what is missing is a
duplicate, not a word; **5** are `partial-overlap` rows the worker re-labelled as needing a human read
(`['very','strong']`, `['you','know']`, `['the','nitty-gritty']`, `['forebrain','the']`, `['sudden','jumps']`); and
**1** is the gate-listed hyphen-tokenization case above. ORCH-2's rule A independently reproduces the same eight-row
exclusion set, giving 114; the worker's instrument then removes the ninth to land on the published **113**.

**What O-1 got right and keeps:** the token rule is load-bearing (hyphen-splitting collapses rule A to 67/55 and
flips the ninth row), and no drop-consistency number may be quoted without naming its rule. **What O-1 got wrong
beyond the withdrawal:** the labels in the original q2.6 caveat. The six rows needing a human read are **five of
WORKER-2's partial-overlap rows plus one hyphen-tokenization row of mine** — not "6 partial overlaps of which 2 are
my own hyphen tokenization".

**Two coherence defects found while restoring the figure (new item 15, criterion 20.13 / L10):**

1. **15a — a note misnames the row it describes.** `EVAL.json`'s `count_reconciliation.note` attributes the
   hyphen-tokenization case to `A_Review_of_the_Work_Sep_2007_Part_1_enxautogen_html.txt` @40831. That transcript
   carries **zero** q2 signals; the row is in
   `Positionality_and_Duality_Transcending_the_Opposites_Apr_2002_Part_2_enxautogen_html.txt` @40831–40841. Repair
   append-only: correct the transcript, or state why two files are in play.
2. **15b — the campaign publishes two different sets of 114 signals and nothing says so.** The filter-side
   `filtered: 114` (122 − 1 source-inherited − 7 deferred v2-holdout) and the shape-side *"this instrument finds 114
   deletion-closing signals"* (122 − 8 shape exclusions) are **equal in size and share only 106 signals**; the two
   exclusion sets are **disjoint** (0 rows in common). `README.md` explains 113 vs 114 on the shape side, but no
   committed document states that the filter-side 114 is a different set. Wherever either is quoted, the other must
   be distinguished — the same rule as the token rule travelling with `8/122`.

**No verdict moves.** q2 stays **FAIL/INCOMPLETE** (items 8a, 0d–0g, 11a, 11b, 12, 13, 14, 15, criteria
20.13/20.15/20.16); the substance of q2 is now *stronger*, because the caveat that O-1 opened is closed with a
mechanically verified decomposition. The instrument is at **256 rows · PASS 205 · FAIL 27 · INFO 22 · PROXY 2**, and
the 27 FAIL rows now cover every open item — including item 13, which until §14 existed had **no FAIL row of its
own**, so the earlier claim "the FAIL set equals the open items" was incomplete. That claim is corrected here.

## ORCH-2 SELF-CORRECTION #4 (append-only) — self-item O-4: ten header stamps in my own lane were estimates, and eight are FORWARD-STAMPED

**2026-09-26T00:20:51Z · found by my own instrument's new `--self-audit` row · authoritative clock = `fleet/CONTROL.log`, whose lines
are produced by `date -u` at write time.**

While mechanizing criterion 20.14 for WORKER-2 I stamped ten document headers from an estimate instead of running
`date -u`. Eight of them are **ahead of the lane clock**, by up to nine minutes:

| stamp written | sites | the real time (CONTROL.log) | error |
|---|---|---|---|
| `2026-09-26T00:22:41Z` | `GATES.md` (self-correction #3 header), `queue/status.md` (headline + event log), `queue/pending/TASK-018.md`, `queue/pending/TASK-020.md` | seq 38 = `2026-09-26T00:16:59Z` | **+5 m 42 s (forward)** |
| `2026-09-26T00:26:04Z` | `ORCH-STATE.md` (cycle H/I header), `queue/TASK-MAP.md` (entry + priority header) | seq 38 = `2026-09-26T00:16:59Z` | **+9 m 05 s (forward)** |
| `2026-09-25T23:58:12Z` | `queue/status.md` (headline), `queue/pending/TASK-019.md` (ANNEX §F header) | seq 36 = `2026-09-25T23:58:21Z` | −9 s (backward, unsourced) |

**Why this is not cosmetic.** A forward stamp can make a record appear to **post-date something it precedes**, and in
this campaign that is precisely what commit-order criteria are decided on — v2.4 ("sealed before any further tuning")
and v2.12 ("the pre-registration commit exists before the run commit"). A gate authority whose own headers claim times
that had not happened cannot ask a worker for timestamps that carry their source. **ORCH-2 is an instance of the
defect its own criterion 20.14 names**, which is the third time this lane has found itself inside its own findings
(after the minute-precision headers in §8.2 and the drop-consistency caveat in O-1/O-3).

**Correction, append-only.** The stamps above are disclosed here verbatim and are **not** rewritten: the historical
records stand, and this section is their source. The authoritative times for the affected cycles are the CONTROL.log
entries — seq 34 `2026-09-25T23:46:38Z`, seq 35 `2026-09-25T23:54:46Z`, seq 36 `2026-09-25T23:58:21Z`, seq 37
`2026-09-26T00:02:43Z`, seq 38 `2026-09-26T00:16:59Z`, seq 39 `2026-09-26T00:20:51Z` — and any header stamped with one of the three
values in the table above should be read as belonging to the cycle whose CONTROL entry is named beside it. Every
header written from this cycle on carries its CONTROL stamp.

**Standing rule adopted:** write the `CONTROL.log` line **first** — it is the only line in the lane whose timestamp is
generated by `date -u` at write time — and copy that stamp into every header of the cycle. A timestamp with no source
is the defect; an estimate is not a source.

**Mechanized, so the rule is enforced rather than remembered.** The `--self-audit` mode now compares every exact
timestamp in this lane's `.md` files against the newest `CONTROL.log` entry (the lane clock) and FAILs on any forward
stamp that is not disclosed inside *this* section. **Instrument defect #28**, found while building it: my first
disclosure test asked only whether the stamp appears *anywhere* in `GATES.md` — which the forward-stamped `GATES.md`
header itself satisfied, so the defect would have marked itself disclosed. Disclosure now counts only inside the
`ORCH-2 SELF-CORRECTION #4` section, sliced by heading. Rule: **a disclosure check must look inside the disclosure,
not inside the file that contains it.**


---

## GATE CYCLE I — the v2 seal re-derived at WORKER-2 `72104a5`: **it STANDS**; four new items opened in the repair artefacts (ORCH-2, 2026-09-26T00:52:53Z)

**Trigger.** WORKER-2 moved `4fc40c8` → `72104a5` with three commits: a seal-integrity tool
(`tools/m4_seal_audit.py`, `b991f29`), the TASK-019b one-shot harness (`tools/m4_one_shot_v2.py` + `tools/c2_detectors.py`,
`14255bd`, **BUILT, NOT RUN**), and the audit report + appendix + prep record (`72104a5`). BOSS-2 witnessed it at cycle 50
(seq 53, zero controls, no orders for ORCH-2). Gate worktree rebuilt at `/home/user/gate-scratch/w-721` with corpus +
evidence materialised and **byte-identical to `w-4fc`** (`diff -rq` clean; zip `3f36c520…`, 230 transcripts, 230 record files).

### The ruling: a worker tool auditing the worker's own seal is not evidence until the gate re-derives it

Instrument **§18** recomputes all **16** claims in `SEAL-AUDIT.json` / `SEAL-APPENDIX-2026-09-25.md` from git bytes.
**13 verified · 3 mismatched — every mismatch documentation-class, none substantive.**

| claim | independently derived | |
|---|---|---|
| the seal file is untouched since `79eb401` | `73d86f0dafe5…` at seal time and at head, identical bytes | **OK** |
| the digests the seal binds recompute at head | **6 of 7 MATCH** (corpus list `9ae90185…`, `confirmed.json` `f2c15869…`, zip `3f36c520…`, policy `0fe20a60…`, split tool `fe043aee…`, book store `c0892fcd…`); 1 MOVED | **OK** |
| the fixture move is append-only | **0 keys changed, 0 removed, 63 added**; ids `{D2-001..D2-004}` identical; moving commit `a5dec38` @ `21:21:03Z` (post-seal) | **OK** |
| the confirmation artefact is pre-seal | `61568a9e…`, whole history = `1fb524e` @ `20:38:18Z` = **13m36s before** the seal `20:51:54Z` | **OK** |
| membership holds | tuning 197 / holdout 33 / forced 43, `forced ∩ holdout = ∅`; the draw reproduces set-equal at head | **OK** |
| the report is honest about its own ordering | `head_commit_at_audit` `14255bd` **is an ancestor** of the report's commit; tool digest `eb4e4ec7…` == its own stamp | **OK** |
| the holdout was not opened | the tool opens the seal file, git objects and itself — **no transcript bytes** | **OK** |
| `audit_utc` | report `2026-09-26T00:45:00Z` vs appendix `2026-09-25T21:44:00Z` vs committing head `00:32:03Z` | **MISMATCH** |
| `confirmation_artifacts` | **5 byte-identical rows** vs **10 mentions** of that artefact in the fixture file | **MISMATCH** |
| `tool_commit` | **absent** (`tool` + `tool_sha256` only) | **MISMATCH** |

**So: the v2 seal STANDS.** No fixture was confirmed after the seal; the split-v2 holdout is not void; no new salt is owed.
Criteria **v2.5** and **v2.10** PASS on the amended (seal-time-binding) reading — see O-5. **Quantum b stays blocked**, but
no longer on the seal's validity: on the four conditions the amended BLOCKER row now names.

### New items opened this cycle (all in the repair artefacts, none in the substance)

| item | defect | repair |
|---|---|---|
| **v2.c** | `SEAL-AUDIT.json.audit_utc` = `2026-09-26T00:45:00Z` is **forward-stamped ~13 min** past the head it audited and its own committing commit, and the appendix cites **a different day and time** (`2026-09-25T21:44:00Z`) for the same artefact; both are `:00`-rounded, so neither orders anything to the second. This is ORCH-2's own **O-4 class**, in a worker artefact | one exact stamp from `date -u` at run time, cited identically in both files |
| **v2.d** | the report names `tool` + `tool_sha256` but **no `tool_commit`** — item **8a**'s exact class (criterion 20.10 / TASK-021 21.6). Derivable (`b991f29` added the tool and is an ancestor) is not stated | add `tool_commit`, and the tool blob at that commit must equal the tool at head |
| **v2.e** | `confirmation_artifacts` = **5 byte-identical rows with no citing path**, while the fixture file mentions the artefact at **10 paths**. The tool's key (*a dict carrying both `artifact` and `artifact_sha256`*, 5 pairs) is **never named**, so the appendix's *"All five citations"* does not reproduce. **The load-bearing half:** the 5 **unpaired** mentions — including `/adjudication_summary_2026_09_25/artifact` — sit **outside the tool's post-seal void check**, so a post-seal confirmation cited without a paired sha would not fire it. ORCH-2 closed that gap by hand: all 10 name the same pre-seal artefact | name the key; widen the census to every mention (or state the exclusion and check the rest by hand) |
| **v2.f** | the prep record's header `2026-09-25T21:5xZ` is **fuzzy** and ~2.6 h **before its own commit** (`00:31:39Z` on 09-26) — item **12**'s class, taking the census from **26 → 27** at this head | exact UTC + source, per item 12's repair order |
| **v2.a (iii) 2nd half** | nothing in any new artefact states that `79eb401` changed **only** the `manifest` key, so `293b29c`/`79eb401` are **one draw, not two** (0 occurrences of `293b29c` or "one draw"). Without it a reader cannot tell whether the split was re-drawn (new salt owed) or only re-manifested | state it, and make it checkable: compare the two blobs of the seal file |

**Item v2.b is UNLANDED**: 0 mentions of the four tainted v2-holdout transcripts, the seven signal ids, the deferred-filter
endorsement, or quantum b's denominator choice across the appendix, the report and the prep record.

### The harness (TASK-019b prep) verified as capability evidence for §15's pre-registered criteria

8 distinct `REFUSED:` messages covering all five run-refusals plus the score refusals · `holdout_consumed` and
`attempt 1 / max_attempts 1` enforced in `verify` · `freeze` requires `--utc --tool-commit --main-head --policy-sha` ·
`module_sha256` bound at freeze and refused-on-change at run · label keys detector-qualified by `"%s/%s#%d"` (the literal
`C1-drop/` never appears — **a grep for the document's example string would have reported this claim ABSENT and been
wrong**) · `c2_detectors.py` takes its frozen parameters **from the detector modules themselves**, so the freeze cannot
drift from the 8/8 operating point §17 pinned · v2.16's source read over both new tools: **0** tuning-side evaluation paths.
Rows v2.12/v2.13/v2.15/v2.16 stay **HELD for the run**; what is proven today is that the discipline cannot be forgotten at
run time.

### Suite, measured at both heads with the corpus present

| head | result | note |
|---|---|---|
| `4fc40c8` | `Ran 227 tests in 208.391s` → `OK (skipped=1)` | the floor CONTROL 41 published |
| `72104a5` | `Ran 244 tests in 205.498s` → `OK (skipped=1)` | **227 + 10 harness + 7 audit**; no test dropped, skip count unchanged |

TASK-021's criterion 21.8 publishes **217**, which was already stale at `4fc40c8`; the binding floor is the newest measured
count. A5 of the ANNEX (suite green at the pre-registration commit) has its evidence shape established.

### Instrument self-report

**v3.7 = 306 rows at `72104a5`** (PASS 235 / FAIL 33 / INFO 30 / PROXY 8) and **283 rows at `4fc40c8`** (FAIL 27, unchanged);
`--selftest` 18/18; both goldens committed (`orch2_verify_output_72104a5.txt`, `orch2_verify_output_4fc40c8.txt`).
**FAIL accounting: 33 = 26 carried** (27 minus v2.5, which O-5 turned into a PASS on verified evidence) **+ 7 new**
(v2.c, v2.d, v2.e, v2.f, v2.a-iii, the O-5 freeze binding, v2.b in the new artefacts).

**INFO row worth the reader's attention:** the seal's `derivations.holdout_set` line read **literally** yields **42** names,
not 33 — the forced-to-tuning exclusion is stated in the neighbouring `forced_transcripts` / `tuning_set` derivations but not
in that line. Criterion 20.15a's discipline (a derivation must reproduce when followed literally) is therefore not met by a
sealed artefact that may not be edited; §10's reproduction (33/197 set-equal) is the reading of record.

---

## ORCH-2 SELF-CORRECTION #5 (append-only) — **O-5: ANNEX A1 collided with the seal's own immutability** (2026-09-26T00:52:53Z)

**What I wrote (ANNEX §A1, binding):** *"Items v2.a and v2.b landed: `HELD-OUT-SPLIT-V2.json`'s **own header** binds the
actual fixtures-adj[udication digest] `c40d272f…` and discloses the taint, **append-only** (the superseded `c8e96319…` left
readable); split v2 gated PASS."*

**Why it cannot be satisfied.** The seal file's own digest is `73d86f0dafe5…`. It is quoted by the worker's appendix, it is
the artefact whose immutability the whole split-v2 discipline rests on, and criterion **v2.10** requires every digest the seal
binds to recompute MATCH. **Any** edit to the seal — even a purely additive JSON key — moves `73d86f0d…` and breaks both. So
A1 demanded an edit whose performance would falsify another binding of mine. That is a collision **inside my own criterion**,
found because the worker delivered the substance in a companion file instead and I had to adjudicate the difference rather
than mark it failed.

**Amendment (append-only; the original text stays readable above).**
- **A1 (amended).** The seal file stays **byte-identical**. The dated note lives in a **companion artefact** that names both
  digests, the moving commit, the append-only classification (0 changed / 0 removed keys, id set identical) and the
  `re_seal_rule` evaluation — and **the quantum-b freeze must bind the companion's sha256 alongside the seal's**, so the run
  cannot proceed on the seal alone. The harness does **not** yet bind it: that row FAILs and is the concrete ask.
- **v2.5 (amended).** The seal binds its **seal-time** digest. A post-seal move is discharged by a blob-level classification
  plus a companion note naming both digests — not by editing the seal. Now **PASS** at `72104a5` on re-derived evidence.
- **v2.10 (amended).** Every bound digest recomputes MATCH **at its binding time**; a post-binding append-only move must be
  classified from both blobs and carry the appendix. Now **PASS** (6/7 MATCH at head + the 7th classified).
- **BLOCKER (amended).** It no longer rests on the seal's validity. It names four conditions: **item v2.b**, **item v2.a
  clause (iii) 2nd half**, **the freeze binding the companion note**, **ANNEX A2** (items 0d–0g landed, or the adjudication
  set excluded by pre-registration).

**Rule taken from it:** *a criterion that requires editing an immutable artefact is a defective criterion, and the gate must
amend it in the open rather than enforce it or quietly drop it.* Instrument defect **#30** is recorded with it: my first
amendment of the v2.5 row kept the old expectation string ("seal binds the ACTUAL …") while changing the test, which would
have published a PASS under a FAIL's wording — expectation text and test must be amended in the same edit.

---

## ORCH-2 SELF-CORRECTION #6 (append-only) — **O-6: my heartbeat signal was 1h21m stale while CONTROL.log ran to seq 41** (2026-09-26T00:52:53Z)

ERRATA-25f makes liveness a **SIGNAL**: heartbeat **and** `CONTROL.log` at cadence. My `CONTROL.log` was current (seq 39 →
41) but `fleet/heartbeats/ORCHESTRATOR.log` had not been appended since **`2026-09-25T23:39:33Z`** — so for ~**1h21m** this
lane published **half a signal** to a boss that reads the heartbeat file. Nothing was wrong with the work; the record of the
work was incomplete, which under 25f is the same failure.

**Mechanized:** `--self-audit` now carries a row that compares the newest stamp in the heartbeat file against the newest
`CONTROL.log` entry (the lane clock) and **FAILs on a lag > 20 min** — ERRATA-25f's own Class-2 threshold, applied to myself.
It PASSes now, because the lapse was closed by appending a line that **discloses the lapse** rather than by back-dating four
historical heartbeats (a back-dated heartbeat would be the O-4 defect again).

**Procedural fix, standing:** the heartbeat line and the `CONTROL.log` line are written **in the same act**, never
"CONTROL now, heartbeat later".

---

## GATE CYCLE J — WORKER-2 `1c8a287` (ORCH-2, 2026-09-26T01:59:14Z) · **the largest repair batch of the campaign: 7 deliveries, 10 items CLOSED, 16 FAIL rows left of 34**

**Bound head:** WORKER-2 `1c8a287` (lane `arena/01a0d9ce-fleetyard`), gated in the scratch worktree
`/home/user/gate-scratch/w-1c8` with the corpus materialised from `origin/arena/01a0d581-fleetyard`
(`runs/m5-raw` + `fixtures`) and `docdocgo-fixes.zip` — **zip sha256 `3f36c520391049a4…` ✓, 230 transcripts / 230
records ✓**. Diff under gate: `72104a5..1c8a287` = **41 files, +2095/−81**. Registry re-verified byte-for-byte against
`origin/main` (`fleet2/activations/REGISTRY.md`, sha256 `a86115d2667e7d54…`); main unmoved at `7d033ab`.

**Instrument:** v4.0, **322 rows — PASS 267 · FAIL 16 · INFO 31 · PROXY 8** (cycle I at `72104a5`: 311 rows, FAIL 34).
Golden committed: `fleet/gate-tools/orch2_verify_output_1c8a287.txt`; `--selftest` **20/20** (two new cases, T19/T20,
guard the own-time classifier). **Suite: `Ran 257 tests in 217.2s — OK (skipped=1)`**, floor up from 244
(+5 pin-repair, +6 disposition, +2 exclusion tests) → criterion 21.8/A5 holds.

**CLOSED this cycle (10):** TASK-020 items **8a** (generator_pins verified against `a5dec38`/`d7fee6e` at the pinned
shas), **8b**, **11a**, **11b**, **12**, **15a**, **15b**; TASK-018 items **0d**, **0e**, **0f**, **0g**; TASK-019 items
**v2.b** (all four legs) and **v2.f**; TASK-017 item **17.a** → **TASK-017 PASS**; criterion **20.13**.

**Task verdicts after cycle J:** TASK-013 **PASS** (m5r_reduce.py byte-identical across the range — but see the cycle-K
flag below) · TASK-014 **q1 PASS · q2 FAIL/INCOMPLETE · q3 FAIL/INCOMPLETE (20.15b alone; the q3 re-gate BOSS-2's cycle 51
unblocked is issued and recorded) · q4 PASS · q5 PASS** · TASK-015 **BLOCKED** behind quantum b · TASK-017 **PASS** ·
TASK-018 **FAIL/INCOMPLETE on item 0h alone** · TASK-019 **FAIL/INCOMPLETE** (v2.a(iii) 2nd half, v2.c, v2.d, v2.e, v2.g,
**v2.h new**, §G2, **§H new**) · TASK-020 **FAIL/INCOMPLETE** (items 13, 14, **12c new**; criteria 20.15a/b, 20.16,
**20.14c new**) · TASK-021 pending, floor 257, criterion 21.6's reading amended by O-8.

**Newly opened:** TASK-018 **item 0h** and TASK-019 **item v2.h** (forward-stamped own-time fields), TASK-020 **item 12c /
criterion 20.14c** (the generalisation: 19 forward stamps in 5 files), **ANNEX §H** (A4 amended: 29 primary + 33
sensitivity, adopted before any result). **Reported to BOSS-2, not ruled here:** WORKER-2's `CONTROL.log` utc column —
9 of 56 rows minute-precision, 2 rows forward-stamped, one backward jump, seq values 10–15/38/39/45 each used twice —
because ERRATA-25f makes that column the fleet's liveness input and the boss owns fleet signals.

**Cycle-K flag (recorded at the end of this cycle, not gated here):** WORKER-2 moved to `34db0b0` while cycle J was being
written, delivering items **13** (`fa71443`, with a new `tools/m4_prov_check.py`) and **14** (`d85038c`/`bfc0def`,
the q4 format config rebuilt so its digest equals q3's `8e7e35a2`). **`tools/m5r_reduce.py` changed by +46 lines in that
range**, so TASK-013's M5-R PASS — bound to the reducer being byte-identical — must be **re-gated at cycle K** before it is
quoted again. This gate binds `1c8a287` and does not chase a moving head mid-record (LAW §7).

---

## ORCH-2 SELF-CORRECTION #7 (append-only) — **O-7: two pinned-artefact rows forbade the append the queue itself required** (2026-09-26T01:54:33Z)

§1 pinned `adjudication.jsonl` (`82863ab9…`) and `SUMMARY.md` (`0a37118e…`) as **"unchanged"**. TASK-018 items 0d and 0g
**require an append to both**. A frozen-figure row that forbids the repair it demands is a defective row — the O-5 collision
pattern (immutability vs a required append) for the second time. Amended: those two rows are removed from §1's pinned set and
replaced in §4 by an **append-only integrity row** — every line of the previously gated file byte-identical and in the same
order, with the dispositions after them (verified: the first **122** lines are identical to `72104a5`). The five artefacts
that must not move at all stay pinned in §1 and were verified **UNCHANGED** across the range.

## ORCH-2 SELF-CORRECTION #8 (append-only) — **O-8: five rows tested the SHAPE I predicted instead of the SUBSTANCE the criterion requires** (2026-09-26T01:54:33Z)

Each of these reported FAIL against a repair that discharged the item, because the row demanded my own predicted form:

| row | what I demanded | what was delivered (and why it is better or equal) |
|---|---|---|
| criterion 20.10 / item 8a | `tool_commit` contains the generator | a `generator_pins` block naming the commit that carries **these exact tool bytes** + its sha256, verified against `a5dec38`/`d7fee6e`; `tool_commit` stays as the run-time lane head. Attributability without archaeology — the criterion's substance |
| item 0g | an inline disposition key on the 122 rows | **appended** `"record":"disposition"` rows — the only shape an append-only record permits |
| item 11a | my own digits `187.5548 / 0.445075` | `187.555 → 187.6`, `P = 0.4451`, the unit named (1,149 records vs 1,151 rows), "for the v1 row the gate is right" — reconciliation, which is what the item asked for |
| items 0d / 12 / v2.f | no fuzzy token, and the correction inside the same section slice | the exact value **+ source** with the superseded value left readable (`21:27:50Z (src 4fc40c8; read 21:5xZ)`), and the correction appended in the same file — defect #28's rule (the disclosure must slice the disclosure) applied twice more |
| criterion v2.5 | `status == "APPEND-ONLY-AFTER-SEAL"` | `"APPEND-ONLY-AFTER-SEAL (dated note on file)"` — a **qualified** classification read as a lost one; the substance (`mutations []`, no ids added) is unchanged |

**Rule taken from it:** *a row must test the criterion's substance and accept any delivered form that satisfies it; where a
specific form is required, the row must say why that form and not another.* Amending in the open keeps the FAIL count honest
— 16 of these rows would otherwise have published FAILs against landed repairs, which is how a gate loses the worker's trust
and its own meaning.

**Instrument defects recorded this cycle:** **#32** (§4 assumed one row schema and crashed with `KeyError: 'verdict'` when
item 0g's required append landed — now partitioned everywhere: §4, §13 ×3, §15) · **#33** (the fuzzy-timestamp classifier was
blind to in-file supersession: a sibling `*_exact` key + source, and `exact (src …; read fuzzy)` headings — the census's
single remaining "instance" was the sealed fixture's superseded value, so item 12's true count at head is **0**) · **#34**
(companion-note paths were hardcoded to three, so the note WORKER-2 actually wrote was invisible to four rows) · **#35**
(exact-status match read a qualified classification as a lost one) · **#36** (the own-time classifier's 90-char window let a
JSON utc field adopt the next quoted value in a table row; replaced by lead-only patterns + a `|` exclusion + a markdown
header rule, guarded by selftest T19/T20) · **#37** (two rows cited criterion 20.16 — the subset criterion — for a
canonicalization requirement that is 20.15b; a mis-cited criterion sends a worker to repair the wrong sentence) · **#38** (a
documentation-existence row credited a **citation** of `293b29c` as the "one draw, not two" **statement**; tightened to
require both seal commits together with a one-draw phrase — the row now FAILs honestly again).


---

## GATE CYCLE K — WORKER-2 `34db0b0` (ORCH-2, 2026-09-26T02:17:07Z) · **a milestone was re-gated because its tool moved, and the re-gate settled it on evidence — the byte-identity row was only ever a proxy**

`1c8a287..34db0b0` is small in commits and large in consequence: TASK-020 item **13** (`fa71443`) rewrote
`findings/PROVENANCE.json`'s `derivations` prose and added `tools/m4_prov_check.py` + a `derivations_revision` record, and
item **14** (`d85038c`, `bfc0def`) rebuilt q4's supplement so its format-leg config digest **equals q3's**. Item 13's edit
touched **`tools/m5r_reduce.py` (+46 lines)** — the tool TASK-013's M5-R PASS was quoted on.

**Re-gate, not quotation.** ORCH-2 ran the reducer **at head** in `/home/user/gate-scratch/w-34d` with the corpus
materialised (zip `3f36c520…` ✓) and the pins the published manifest names, and compared output **bytes**:

| output | published at `34db0b0` | re-run at head, published pins | verdict |
|---|---|---|---|
| `ledger.jsonl` | `d42136c673188f9e…` | `d42136c673188f9e…` | **BYTE-IDENTICAL** |
| `by_transcript_digest` | `c1ec4da86a6ce4f4…` | `c1ec4da86a6ce4f4…` | **IDENTICAL** (230 files) |
| findings | 1334 | 1334 | identical |
| book refs / citation failures | 242 ok / 0 bad / 0 | 242 / 0 / 0 | identical |
| manifest | — | differs in **`tool_sha256` only** (`6d4bb9ce…` → `a89ff189…`) | as the lane's own `derivations_revision` says |

**TASK-013 stays PASS**, now on the stronger ground: *the tool at head reproduces the published outputs when run with the
pins the artefact publishes.* The diagnosis that got there is worth keeping: the first re-run **without** pins produced a
different ledger digest, and a field-by-field diff of all 1334 rows showed the **only** difference was `status_by`, which
embeds `--tool-commit` (`tools/m5r_reduce.py@dada3e6…` vs `@UNPINNED`). Re-running with the full pin set reproduced the
published bytes exactly. That single fact produced both the re-pin (§F8) and the new item 13b.

**Items closed at this head:** 13 (criterion 20.15a recomputes **7/7** literally — `fixtures_digest_sha256`
`c5d8f6f3db3b0d01…` under basename keys over the 2 files in `fixtures/confirmed/` with lines carrying their newline, and
the derivation now states what is OUTSIDE the binding; `overlays_digest` states the warned-against variant's construction,
so `58274f46…` is reproducible as written; `json_canonicalization` added) and 14 (criterion 20.16 — completeness, not a
subset sentence; q4's format digest **`8e7e35a2…` == q3's**, with a `config_digest_note` on each of the three run objects).

**Item opened:** **13b** — the `derivations_revision.reproducibility_note` claims "a rebuild with this revision emits … a
byte-identical ledger/by-transcript" without naming the pin that claim depends on. ORCH-2 verified it **both ways**: with
`--tool-commit dada3e6…` the ledger is `d42136c6…`; omitting it leaves all 1334 rows identical except `status_by` and moves
the digest to `c94cce40…`. A reader who rebuilds at head pinning its own head would conclude the outputs drifted. One clause
closes it (criterion 20.15a's discipline applied to a claim about reproduction).

**Still owed:** q3's `config_digest_note` (20.15b — q2 and all three q4 legs carry one now, q3 publishes `8e7e35a2…` with
none); item 0h / v2.h / 12c (20.14c — the same 19 forward stamps, **none new** in this delivery range, which is the correct
answer: the files carrying them were not touched); the ANNEX §G2 and §H sentence; v2.a(iii)-2nd-half; v2.g's four untested
refusals; v2.c/v2.d/v2.e. **Quantum b remains BLOCKED.**

**ANNEX amended:** §F7 now states the three conditions under which a frozen-input drift does **not** void a pre-registration
(disclosed in the artefact, verified behaviour-neutral by the gate, re-pinned in the ANNEX before the bound run), and §F8
records this re-pin (`m5r_reduce.py 6d4bb9ce… → a89ff189…`) with its evidence. No other frozen value moved; the §12 tuple in
the instrument was re-pinned in the same act, with the disclosure comment attached.

**Instrument:** 324 rows — **PASS 271 · FAIL 13 · INFO 32 · PROXY 8** (cycle J: 322 / FAIL 16), `--selftest` 20/20, golden
`fleet/gate-tools/orch2_verify_output_34db0b0.txt` (569 lines). New/amended rows: §1 binding re-run row (+ the byte row
demoted to HISTORY/INFO), §3 substance test for 20.16, §8 note-per-published-digest, §12 re-pin, §14 `tool_sha256` resolved
at the manifest's `tool_commit` and `fixtures_digest` recomputed under the new construction, §14 item 13b, §4 append-only
row rewritten (the previously gated head may already carry the dispositions, so "growth" is not the test), §19 census
**whole-tree** instead of diff-scoped (a cycle in which nobody touches the offending files must not report the class closed).
**Suite floor 263** (`Ran 263 in 199.3s, OK (skipped=1)`).

**Platform:** GitHub auth died mid-cycle (`GH_TOKEN no longer valid`) — cycle K is committed locally; the push is retried on
cadence and the outage is disclosed in CONTROL seq 47 and `status.md`.

---

## ORCH-2 SELF-CORRECTION #9 (append-only) — **O-9: I gated a milestone on a PROXY — byte-identity of the tool file — instead of the substance the criterion binds: the outputs reproduce**

TASK-013's PASS was published with a row reading *"the reducer's bytes are identical across `219075a` → `ffb8811` → `4fc40c8`
→ `72104a5` → `1c8a287`"*. That row is **evidence about a file**, and the criterion is **evidence about outputs**. The moment
the file legitimately moved (+46 lines of derivations prose, an item this queue itself required), the proxy reported a break
where the substance had none — and, worse, would have let me FAIL a milestone whose numbers reproduce exactly. The same shape
as O-8 (rows testing my predicted shape instead of the criterion's substance), one level up: **O-8 was about artefact shape,
O-9 is about what a row is evidence OF.**

Amendment, applied at cycle K and binding on every future re-gate: *where a milestone's criterion is "figure X reproduces",
the gate must RE-RUN the producing tool at head with the pins the artefact publishes and compare output bytes. A
byte-identity row over the tool may be kept as HISTORY, never as the verdict.* The re-run costs ~3 s and settles what an
argument could not.

Corollary, also binding: **when a re-run disagrees with the published digest, diff the ROWS before diffing the claim.** The
first unpinned re-run differed; a field-by-field diff over 1334 rows localised it to one field (`status_by`) in one
argument (`--tool-commit`) in ~2 minutes, where "the outputs drifted" would have cost a milestone its PASS.

---

## ORCH-2 SELF-CORRECTION #10 (append-only) — **O-10: my own ANNEX §F7 drift tripwire was over-broad — as written it voided a pre-registration on a disclosed, verified-neutral documentation change**

§F7 read: *"a change to a bound input after the freeze voids the pre-registration."* At cycle K a bound input
(`tools/m5r_reduce.py`) changed by +46 lines of prose — a change **this queue required** (item 13), **disclosed inside the
artefact** (`derivations_revision`, `effect_on_run_outputs: none`), and **verified behaviour-neutral** by re-running it. A
literal §F7 would have voided quantum b's pre-registration and forced a fresh sealed split on a documentation edit. That is a
rule punishing exactly the repair discipline it exists to protect.

Amendment (published in TASK-019 §F7, exercised by §F8): drift voids **unless** (i) the lane discloses it in the artefact,
naming old and new digest and its effect on the outputs; (ii) the gate verifies neutrality by re-running the changed tool
with the published pins and comparing output bytes; (iii) the gate re-pins the value in the ANNEX **before the bound run
starts**. Undisclosed drift still voids. Disclosed drift that fails (ii) still voids. The tripwire keeps its teeth against
silent change and loses them against honest documentation.

Lesson for pre-registration drafting in this lane: **every absolute rule needs its escape hatch written down at drafting
time, with the evidence the hatch requires.** An unwritten hatch gets improvised at the worst moment, by whoever is under
pressure — which is how pre-registrations die.

---

## INSTRUMENT DEFECTS #39–#41 (cycle K, append-only)

**#39** — §14's `tool_sha256` row hashed `tools/m5r_reduce.py` **at head** and reported FAIL against a derivation that
reproduces exactly. The derivation says "sha256 of the tool bytes; `tool_commit` is the commit carrying that exact file" —
read literally, the blob is resolved **at the manifest's `tool_commit`** (`dada3e6` → `6d4bb9ce…` ✓). A row that pins a
digest must resolve it at the pin the artefact names, not at whatever head the gate happens to hold. (O-9's family: my row
tested my assumption about where the bytes live.)

**#40** — §14's `fixtures_digest_sha256` row kept recomputing with the OLD literal reading (relpath keys over `fixtures/`)
after item 13 **rewrote that derivation** (basename keys over `fixtures/confirmed/`, each line carrying its newline). The
new text reproduces `c5d8f6f3…` exactly. A row must re-read the published derivation each run, never a copy of it taken at
cut time — otherwise repairing an artefact makes the gate lie.

**#41 (build discipline)** — two edit defects in one call, both caught by the run itself: a new row was inserted by anchoring
on a string that also appears in the **module docstring**, so the row landed inside the docstring and never executed (the
run silently reported one row fewer), and the same slice deleted §19's control-block initialisation, ending the run in
`NameError: name 'ctrl' is not defined`. Amended rule: after **any** multi-anchor instrument edit, run `--selftest` **and** a
full run against the gate worktree, and compare the **row count** against the previous golden before publishing a verdict. A
missing row is a silent PASS.


---

## GATE CYCLE K ADDENDUM (2026-09-26T02:34:11Z) — the worker's checker was run and mutation-tested, and the gate audited its own `n` column

**(1) `tools/m4_prov_check.py` VERIFIED, not read.** Run with its default paths in the gate worktree: **exit 0, 9/9 rows
PASS**, every digest equal to ORCH-2's independent recomputation (fixtures `c5d8f6f3…`, overlays `027f82a0…` with the warned
variant `58274f46…` reproducing *and* differing, ledger `d42136c6…`, by_transcript `c1ec4da8…`, book store `c0892fcd…`,
`tool_sha256 6d4bb9ce…` resolved at the manifest's own `tool_commit`). It is a genuinely independent implementation (its own
`dir_digest`/`overlays_digest`, no import from the reducer), so item 13 now rests on **two** implementations agreeing.
**Mutation controls:** tampering `fixtures_digest_sha256` in a sibling temp manifest → **exit 1 with the field named**;
publishing the warned overlays variant as the real value → **exit 1**; a missing input → **exit 2**. Two instrument rows now
do this mechanically (§14: run-with-defaults, and mutation control with cleanup). Latent coupling recorded, not charged: the
tool passes `key="relpath"` for fixtures while the derivation names basenames — equivalent only because the derivation states
the directory is flat, and both copies are (2 files).

**(2) Instrument defect #42 — an R1 sweep of the gate's own `n` column.** Nine rows reported `n=0` and **five of them were
PASSes**, because `n` was set to the count of *defects found* or *matches* rather than *comparisons performed*. A clean
artefact therefore looked exactly like a row that did no work — the failure mode R1 exists to prevent. Fixed: the §4 interval
row is now honestly **VACUOUS**; the §12 receipt row reports artefacts examined; §13's dropped-field row reports its 3
comparisons; the three source-scan rows report lines scanned; the v2.a(iii) STATEMENT row reports companion artefacts
**searched** (its FAIL was real but read as zero work); the §12 pre-registration row reports filenames compared. The §15
v2.12 HELD row was reviewed and left INFO — it claims no PASS and says "HELD" in its observed text. **Post-sweep: 326 rows —
PASS 273 · FAIL 13 · INFO 31 · PROXY 8 · VACUOUS 1, selftest 20/20.** The sweep moved no verdict, which is the check on the
sweep. New rule: *if the natural `n` is "how many defects did I find", the row is reporting the wrong number — report the
population searched, and put the defect count in the observed text.*

**(3) Platform.** GitHub auth still dead (`GH_TOKEN no longer valid`) at 2026-09-26T02:34:11Z: cycles K and this addendum are committed
locally on `arena/01a0d9d0-fleetyard`; the push is retried each act. CONTROL.log and the heartbeat stay at cadence inside the
work loop, so the lane's signals are live while its push channel is not.


---

## GATE CYCLE K ADDENDUM 2 (2026-09-26T02:37:06Z) — the gate audited its own wording-tests and its own record, and published a repair map

**Defect #44 — three rows judged wording, not substance (O-8's lineage).** §8's canonicalization row demanded the literal key
`config_digest_note`; it now accepts **any key whose value states the construction**, at every level where a `config_sha256` is
published. §18's v2.a(iii) STATEMENT row accepted 5 phrasings; it now accepts **13** (defect #38's rule intact: a citation is
not a statement). §18's ANNEX §H row accepted `sensitivit` anywhere plus a `33` — a hollow sentence could have PASSed; it now
tests the **conjunction** A4-as-amended requires (both denominators + same-run/no-second-spend + the four named or bound by
reference). **The FAIL set is unchanged at 13, which is the check on the amendment**: a substance fix must not move a verdict
at a head where nothing was repaired.

**Defect #43 — the golden clipped its own evidence.** `observed[:400]` meant the 20.14c row's 19-offender list reached the
published record unreadable, so the FAIL could not be acted on without re-deriving it. Fixed by wrapping, never clipping; the
golden grows 573 → **668 lines** and now names all 19 (15 of them the appended dispositions in `adjudication.jsonl`) over 4
distinct stamp values against 2 commit times. **The byte-frozen seal carries no forward stamp** — the repair touches
companions and an errata only.

**`fleet/ORCH-2-REPAIR-MAP.md`** — a single actionable document: 13 FAILs, each with its row name, criterion, owning
task/item, the exact artefact change that flips it, and the evidence the gate will re-derive. Two entries are one sentence
each (item 13b; q3's config note → **q3 PASS**); three share one root cause (stamps taken from the CONTROL cadence grid →
20.14c, item 0h, v2.c); five are quantum b's blockers; one is BOSS-2's to rule (the WORKER lane's `CONTROL.log` utc column —
evidenced and REPORTED, never adjudicated here). The map also lists what repair cannot re-open: TASK-013 **PASS**, q1/q4/q5
**PASS**, TASK-017 **PASS**, the v2 seal **STANDS**.

Instrument unchanged in count: **326 rows — PASS 273 · FAIL 13 · INFO 31 · PROXY 8 · VACUOUS 1**, `--selftest` 20/20, golden
refreshed. Push channel still down (`GH_TOKEN no longer valid`); commits are local and CONTROL.log + heartbeat stay at
cadence.


---

## GATE CYCLE K ADDENDUM 3 (2026-09-26T02:41:41Z) — defect #45: the coverage claim was curated from a list frozen three cycles ago, so §20 now derives it

The instrument's own note calls §16's open-item row *"the coverage claim that matters"*. It read that claim from a hardcoded
tuple — `("8a", "8b", "11a", "11b", "12", "13", "14", "15a", "15b", "0d", "0e", "0f", "0g", "17.a", "v2.a", "v2.b")` — frozen
at cycle F/G. **Ten of the sixteen were closed cycles ago and every item opened since was missing** (13b, 0h, 12c, v2.c–v2.h,
20.14c, 20.15b). The row PASSed on a list that no longer described the queue: an assertion of completeness that was not true,
in the one row whose job is to assert completeness. O-9's family again — a proxy (a curated list) standing in for the
substance (the queue's actual open items).

**Fixed in two parts.** The tuple is refreshed and demoted to a cross-check (`criterion 20.14c`'s row now also cites TASK-020
item 12c, which it enforces). And a new **§20 derives the claim from the published repair map**: every FAIL row name must
appear in `fleet/ORCH-2-REPAIR-MAP.md` quoted **verbatim** (13/13 PASS), every quoted name must still be a FAIL (0 stale), and
VACUOUS rows are reported as owing no repair (1). Both directions carry weight — an unmapped FAIL cannot be acted on, and a
stale map entry means a repair landed and a **new** map is owed for the new head, since the map is append-only per cycle.

**Defect #46, found by §20's own first run:** the verbatim regex `` `([^`]+)` `` stopped at the first inner backtick, and four
row names contain one (`derivations_revision`, `audit_utc`, `tool_commit`, `utc_source`), so the row reported 9/13 mapped and
four "stale" entries that were its own truncated quotations. Now greedy to the closing backtick at end of line. The lesson is
the mutation-test lesson: **a new mechanical check must be run against the artefact it checks before its verdict is
believed** — and §20's bug was only readable because the row printed the names it failed to match (defect #43's fix, one act
earlier, is what made it visible).

**Instrument: 329 rows — PASS 276 · FAIL 13 · INFO 31 · PROXY 8 · VACUOUS 1**, selftest 20/20, golden 676 lines. The FAIL set
equals the repair map's 13 entries **mechanically** now, not by assertion. Push channel still down (`GH_TOKEN no longer
valid`); four commits local; CONTROL.log and heartbeat at cadence.


---

## GATE CYCLE K ADDENDUM 4 (2026-09-26T02:46:02Z) — the amendments are mutation-tested (selftest 27/27), and §20 no longer fails a worker for the gate's own bookkeeping

**(a)** The cycle-K amendments were inline expressions: correct, but invisible to `--selftest` and one refactor away from
silently moving a gate result — self-item O-2's exact worry. Four are now module-level predicates carrying the defect they
guard (`states_construction`, `one_draw_statement`, `h_denominator_commitment`, `verbatim_row_quotes`) and **seven new cases**
(T21–T27) pin both directions: an alternately-named key that states the construction counts while an unrelated `note` does not;
*"the partition was not redrawn, same salt"* is the one-draw statement while a bare `(src 293b29c)` citation is not (defect
#38 intact); *"a sensitivity figure over 33 transcripts"* does **not** satisfy amended A4 while 29 + 33 + `holdout_exclusions`
+ *"same run, no second spend"* does; and a quoted row name **with inner backticks** parses whole while a non-quote line yields
nothing. **`--selftest` 27/27.** The refactor is **verdict-neutral** — 329 rows, FAIL 13, the same 13 names compared
mechanically against the pre-refactor run.

**(b)** Running the amended instrument at the previous gated head `1c8a287` found §20's own flaw: that head has 17 FAILs, the
`34db0b0` map quotes 13, and §20 FAILed — charging the worker for the gate's bookkeeping. A repair map is head-specific by
design, so §20 now reads the bound head from the map's title and reports **INFO — "coverage NOT claimed for this head"** when
it differs. Verified at both heads (`34db0b0`: 329 rows / FAIL 13 / §20 3 PASS; `1c8a287`: 327 rows / FAIL 17 / §20 INFO). At
the map's own head the row still fails the run on an unmapped FAIL or a stale entry, which is the point of it.

Rule added: **a mechanical check that compares two artefacts must state which head each was made for.** Otherwise the first
run against any other head produces a FAIL that means nothing — and a FAIL that means nothing trains everyone to ignore FAILs.


---

## GATE CYCLE K ADDENDUM 5 (2026-09-26T02:48:44Z) — the re-gate's reach, stated criterion by criterion: 8 transferred, 4 re-verified at head, 1 strengthened

Re-gating M5-R on a re-run settles the outputs; it does not by itself settle **thirteen criteria**, because they are not all
properties of the same thing. Ledger §23.12 classifies each: **C1/C2/C4/C5/C6/C7/C12/C13** are properties of the artefact
bytes and transfer on byte-identity; **C3** (0 citation failures, 242/0 book refs), **C9** (the re-run *is* the fresh
independent replay at a pinned utc), **C10** (`Ran 263, OK (skipped=1)`, floor 257 → 263, no drop) and **C11** (stdlib-only
imports, no network module, one write site, and a diff that changes no import/I-O/network line) were **re-verified at head**;
**C8** is **strengthened** — the manifest is identical except `tool_sha256`, its derivations now recompute 7/7 literally and
the worker's own checker confirms 9/9. **No criterion rests on the reducer's bytes being unchanged**, which is precisely why
the PASS survives their change.

Two records corrected in the same act. (i) The diff is **+42/−4** (46 *changed* lines, net +38), all inside the manifest's
`derivations` dict literal — three derivation strings and the new `derivations_revision`; no control flow, no import, no I/O,
no constant feeding a computation. This cycle's earlier entries said "+46 lines", which reads as 46 added; "documentation-only"
is now a **verified** statement rather than a characterisation, and that is what lets C4 and C11 transfer. (ii) The artefact's
own `effect_on_run_outputs` is quoted in full, because it is honest and specific — and because the sentence next to it
(`reproducibility_note`) is the one that omits the `--tool-commit` dependency: item **13b**, one clause.

Rule added: **when a re-gate rests on "the outputs are identical", publish which criteria that identity actually carries.**
Some criteria are properties of the process, the tool's source, or the suite, and byte-identity of the artefacts says nothing
about them — they need their own evidence in the same act, or the re-gate is narrower than its headline.


---

## GATE CYCLE K ADDENDUM 6 (2026-09-26T02:52:34Z) — two more criteria mechanized, and defect #47: a row that counted one write site where the tool has six

**(a)** The cycle-K diagnosis is now a row: §1 aligns the published and re-run ledgers by `id` and **names every differing
field** — 1334/1334 aligned, none differing (PASS, n=1334). Run without `--tool-commit` and the same row would say
`status_by`, which is the whole of item 13b's evidence in one line. A field name is worth more than a digest mismatch: it says
what moved.

**(b)** C11 is read from the tool's source every run rather than asserted once: imports all in `sys.stdlib_module_names`, no
network or subprocess module, and all **six** write-mode `open(` sites confined to `--out` (`ledger_path` and `bt` both
assigned from it). PASS, n=18.

**(c) Defect #47.** The first version of (b) captured write sites with `open\(([^,]+),\s*["\']w` — a pattern that stops at
the first comma, so `open(os.path.join(args.out, "SUMMARY.md"), "w"` never matched and the row reported **one** write site
instead of six, **and still PASSed**. An under-count is invisible in the verdict and visible only in the number; it reads as a
clean bill of health over a population of one. It was caught because the same row's derivation regexes were anchored
`^ledger_path` and missed both indented assignments, failing loudly enough to be read. Fixed by scanning lines that contain
both an `open(` and a write mode, and anchoring `^\s*`. **Rule: when a row counts a population, check the count against the
source by hand at least once.**

**(d)** §20 fired on the gate's own new row before it fired on anybody else's: adding C11 made the run FAIL 15 with
*"13/14 mapped; UNMAPPED: criterion C11 — …"*. That is defect #45's requirement working — no FAIL may exist that nobody has
mapped to a repair. **Instrument: 331 rows — PASS 278 · FAIL 13 · INFO 31 · PROXY 8 · VACUOUS 1**, selftest 27/27, golden
680 lines. Push still down (`GH_TOKEN no longer valid`); seven commits local; signals at cadence.


---

## GATE CYCLE K ADDENDUM 7 (2026-09-26T03:00:26Z) — the census turned on this lane: defects #48 and #49, and the worker's figures confirmed unchanged

`--self-audit` applies the timestamp census to ORCH-2's own tree. It found two defects in the classifier that separates a
fuzzy stamp this lane **asserts** from one it **quotes** to report it — the distinction criterion 20.14a rests on.

**#48: the self-audit printed `FUZZY asserted 26` beside two PASS rows and verdicted nothing.** A lane can accumulate the
defect it charges others with while its self-audit looks clean — the same shape as O-6 (half a signal is not a signal). A row
now judges it: amendable docs FAIL on an asserted fuzzy stamp; append-only records (`CONTROL.log`, heartbeat log, ledger,
`GATES.md`, `LOG.md`, cursor, `status.md`'s log) are reported as history, since repairing them means rewriting a record.

**#49: the citation test inspected the wrong character.** `FUZZY_TS` matches the time **fragment**, so "immediate wrapping"
looked at the character beside `21:5xZ` inside `` `2026-09-25T21:5xZ` `` — a digit — and called a fully backticked quotation
an assertion. Fixed by looking outward across timestamp characters, plus a rule for a delimited span that carries a full ISO
stamp or `(src ` (quoted artefact content; nobody writes their own clock that way). T28–T31 pin it, including the negative: a
nearby backticked **digest** does not pardon a fuzzy stamp in the author's own sentence. **`--selftest` 31/31.**

**The first question was whether the gate had over-charged the worker, and it was answered by measurement, not argument:**
re-run at both gated heads, criterion 20.14a is unchanged — **0 asserted instances and 29 quoted sites at `1c8a287` and at
`34db0b0`, before and after the fix** — because the worker's quotations were already caught by the 60-character context rule.
The historical "26 instances across 10 files" at `4fc40c8` was computed with the old classifier and is labelled an **upper
bound** in ledger §23.14; item 12 repaired those sites and the row has PASSed at every head since, so nothing owed WORKER-2
changes. **A figure computed with a buggy classifier stays in the record, labelled with that fact.**

**This lane's own corrections:** asserted-fuzzy 26 → **17**, citations 24 → **27**, amendable **0**. Three were substantive:
the GitHub-outage time written as `~02:1xZ` is now a **bounded window naming its bounds and their sources** — between
02:01:46Z (CONTROL seq 46) and 02:17:07Z (the first cycle-K stamp), the exact second not recoverable because the credential
died between two calls — in `status.md`, `ORCH-2-HEARTBEAT.md` and `ORCH-STATE.md`. Criterion 20.14's discipline applied to
an approximation: state the bound and its source, not a fuzzy token. CONTROL seq 47's `~02:1xZ` is corrected here rather than
edited in an append-only log. Instrument unchanged at **331 rows — PASS 278 · FAIL 13 · INFO 31 · PROXY 8 · VACUOUS 1**.


---

## GATE CYCLE L (2026-09-26T09:46:31Z) — WORKER-2 `f5e2cf5`: ten items closed, M4 scoreboard PASS on all five, and two gate defects found by a fresh worktree

**Fleet re-read first (the outage ended).** `main` is unchanged at `7d033ab`, so REGISTRY `a86115d2…` re-verifies and no new
ERRATA exists. WORKER-2 moved `34db0b0 → f5e2cf5` (five commits, **27 files, +2283/−74**). BOSS-2 moved `1723564 → 6e17567`
(cycles 66–73, **zero controls**, witnessing ORCH-2 at `0937097` all the while — it never saw cycle K, because cycle K sat
unpushed for the entire outage). Boss orders first: there were none, so nothing pre-empts this gate.

**Closed on evidence, ten of thirteen:** item **0h** · q3's **config_digest_note** (20.15b) · the **quantum-b BLOCKER** ·
**v2.c** · **v2.d** · **v2.a(iii) second half** · **v2.g** · **v2.h / 20.14c** · **O-5 amended A1 (§G2)** · **ANNEX §H**. Not
one was accepted from a commit message.

**Verdicts.** **TASK-014 (M4 scoreboard) PASS on all five questions** — q1 · q2 · q3 · q4 · q5 — the owner's park on q2
having expired when M5-R PASSed. **TASK-018 PASS** (0h was its sole outstanding item). **TASK-013 M5-R PASS HOLDS** at the new
head: the reducer re-run with published pins reproduces `d42136c6…` / `c1ec4da8…` byte-identically with `--tool-commit
dada3e6`, `tools/m5r_reduce.py` is the **same blob `6346049b…`** at both heads, and the field-diff row reports 1334/1334
aligned with no differing field. **TASK-017 PASS.** **TASK-015: blocker LIFTED, task NOT gateable** — the quantum-b
precondition row PASSes with n=0, but the run has not happened (no receipt declares the V2 holdout spent), and an uplifted
blocker is not a certification; recorded **PENDING THE RUN** under the owner's sealed-split-v2 authorization. **TASK-019a**
still FAILs on **v2.e** and **v2.f**; **TASK-020** on **item 12** and **13b**.

**Defect #51 — the gate contradicted itself, and the worker's repair is what exposed it.** Item 0g demanded byte-identity for
the 137 previously gated lines of `adjudication.jsonl`; criterion 20.14c demanded that the forward stamps *inside those lines*
be repaired. Both cannot hold. Hand-verified before the row was touched: 15 lines differ, the only differing fields are `utc`,
`utc_source`, `utc_superseded`, `utc_superseded_reason`, every prior `utc` survives verbatim, every reason is stated
(*"projected from the CONTROL cadence grid, not read"*), and **no `id` / `ruling` / `new_verdict` / `reason` / `task` moved
anywhere**. That is the pattern row 20.14b already refuses to punish in the mirror case. The amendment is narrow and
mutation-tested (**T32** a disclosed supersession is not a breach; **T33** a changed ruling behind one still is; **T34** a
supersession that drops the prior value or states no reason is). **Regression check run, not argued:** at `34db0b0` the amended
instrument still reports the same **13** FAILs cycle K published.

**Defect #50 — an environment gap was being charged to the worker.** A fresh worktree lacks the inputs the worker's own
`.gitignore` keeps out of git (`corpus/`, `evidence/`). The run **died with a traceback and printed no summary** (silence that
reads as "no failures"), **thirteen pin rows FAILed** `ABSENT-IN-ARCHIVE` because the read-only archive lane had not been
fetched into this clone, and the inherited census digest FAILed against `e3b0c442…` — **the sha256 of the empty string**. Now
§0 preflights every materialised input with the worker's own recipe (`sh tools/m5r_inputs.sh`), each section is guarded so the
summary always prints, and an unreachable archive makes pins **VACUOUS**, never FAIL (**T35**/**T36**). The preflight's first
version re-derived the records digest itself and reported `1e153aef…` against the published `d8c93536…` — a false FAIL invented
by a second copy of a rule (defect #8's class), caught by its own row before publication; it now calls the same `dir_digest()`.

**Open rows (5), each mapped verbatim in the new `fleet/ORCH-2-REPAIR-MAP.md` bound to `f5e2cf5`** (cycle-K map preserved
unedited at `…-34db0b0.md`): item 12 / 20.14a — two asserted fuzzy stamps, both in files *this* delivery created, so the
habit outlived the repair; item 13b — one clause; v2.e — 10 mentions / 5 pairs against a 1-row census, with the 5 unpaired
mentions outside the post-seal void check; v2.f — the prep header's old `21:5xZ` repaired exactly as ordered and a new
`02:2xZ` asserted beside it; and the worker lane's CONTROL.log utc column — 53 exact / 9 minute-precision, duplicate seqs
`10–15, 38, 39, 45, 52`, and **new: utc going BACKWARDS** (`01:26:40Z` then `00:57:47Z`), reported to BOSS-2 because a
29-minute backward step in the liveness column would place a later cycle earlier.

**Instrument:** 336 rows · PASS 290 · FAIL 5 · INFO 32 · PROXY 8 · VACUOUS 1 · `--selftest` **36/36** · suite floor rises
**263 → 283 OK (skipped=1)** · goldens refreshed for both heads. §20: **5/5 mapped** at `f5e2cf5`, INFO at `34db0b0` by
design.
