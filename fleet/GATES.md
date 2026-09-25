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
