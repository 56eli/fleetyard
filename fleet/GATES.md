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
