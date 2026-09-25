# WORKER-2 — TASK-018 DELIVERY (leg (d) individual adjudication)

- task: **TASK-018** — leg (d) individual adjudication of the 122 C1-drop signals + the 4
  provisional fixtures (ORCH-2 queue `fleet/queue/pending/TASK-018.md` @ `45959ca`)
- claimant: WORKER-2 (A-2026-09-25-001), lane `arena/01a0d9ce-fleetyard`
- authority: owner `fleet/ERRATA-2026-09-25e.md` §2–§4; owner `ERRATA-2026-09-25g.md` §5;
  ORCH-2 standing guidance (`fleet/GATES.md`, "CERTAIN leg (d)")
- status: **DELIVERY** (not completion, not certification) — classifications are
  per-finding and cited; no rate, no precision, no corpus-wide figure anywhere
- items 0 / 0b: delivered at `33b6f36` (append-only correction + PATTERNS.md binding)
- this delivery: tool `9cd905d`, artifacts regenerated at the pinned tool commit, suite
  **39 tests OK, 0 skipped**

## Result

| outcome | signals | of 122 |
|---|---|---|
| **CERTAIN-leg-d — clause (d)(i), book ground truth** | **57** | 47% |
| clause (d)(ii) — transcript's own adjacent repetition | **0** | 0% |
| CANDIDATE (unchanged class) | **65** | 53% |

CANDIDATE reasons: `restoration-not-minimal` **48** (two words absent — a larger edit than
one word, L3) · `flank-too-short` **15** (single-word omission but < 5 exactly-matched
tokens on a side — not enough to call the span a matched quotation) ·
`region-not-realignable` **2** (the omission could not be re-aligned from the frozen bytes
at all).

Provisional fixtures: **D2-001 (`things`) and D2-003 (`high`) CONFIRMED under leg (d)**;
**D2-002 (`the devotion`) and D2-004 (`which perceives`) DISCARDED from any CERTAIN claim** —
each is a two-word omission, which the narrow leg does not reach (L3); both keep their
hand-read evidence and stay CANDIDATE. All four carry `seeded`/`in-sample` labels and are
excluded from any metric by construction (L5).

## Method (fixed before counting; not tuned)

1. The detector's cited book span is re-read **byte-exact** at `slug + char_offset` (L2),
   and the omission is located inside it by token.
2. A ±900-char window is aligned (difflib, own tokenizer, hyphen/apostrophe kept inside a
   token) between the frozen overlay and the frozen book store; the aligned op that
   *inserts* the omitted word is located.
3. The **matched span** is the maximal **exactly-equal token run** immediately flanking
   that omission on each side — byte-exact regions, not ratio-matched ones.
4. Clause 1 floor: **≥ 5 exactly-matched tokens on each side** (mirrors the campaign's
   `MIN_MATCHED=10` near-verbatim floor against *exactly matched* tokens; stricter than the
   detector's own ratio-based match whose flank floor was 3). Sensitivity is published in
   `SUMMARY.md`: floors 3/5/8/10 tokens per side would qualify 71 / 57 (chosen) / 33 / 22
   signals.
5. Clause 2/3: the omission must be exactly **one token**, and re-inserting it must make the
   whole region token-equal to the ground truth — the minimal edit that completes the match.
6. (d)(ii) is checked whenever (d)(i) fails: the transcript's own adjacent repetition
   (≥ 5 tokens, within ±800 chars) as ground truth. **Zero** findings needed it.

## Per-criterion evidence (gate L1–L6)

- **L1 per-finding record** — every row of `runs/m4-q2-adjudication/adjudication.jsonl`
  (122 rows) carries: transcript, `char_offset`/`span_end` (detector span) and
  `span_start`/`span_end_matched` (adjudicated span), the verbatim span, the ground-truth
  span (`ground_truth.kind/slug/char_offset/quote`, or the adjacent-repetition offsets),
  `omitted_word`, `restored_span`, `clause`, `flank_tokens`, `seeded`, `in_sample`, verdict
  and reason. Rows with `verdict != CERTAIN-leg-d` carry a `reason_code` and a written
  reason. Regression test: `tests/test_m4_q2_adjudication.py::test_records_carry_the_l1_fields`.
- **L2 citations re-derived** — every promoted row was re-checked independently of the
  tool: transcript bytes at the cited offsets, book bytes at `slug+offset`, and
  `restored_span == ground_truth.quote` — **57/57 byte-exact, 0 failures** (checked by
  re-parsing the book store with a separate regex parser and slicing the raw overlay
  files). `citation_ok`/`book_quote_ok` are stored per row; the manifest records the input
  digests (signals `8d71f57b…` matches the TASK-018 input pin exactly).
- **L3 minimal restoration** — enforced mechanically: two-word omissions are never
  promoted (48 signals); single-word rows must restore exact token-equality over the whole
  region; the floor is a *span* requirement, not a restoration size.
- **L4 no blanket promotion** — 57 of 122 promoted, each by its own cited bytes; the two
  hand-verified-but-two-word fixtures were *refused* promotion, which is the sharpest
  demonstration that no rule, score or hand-read status is a classification reason. Detector
  names never appear as a reason; the detector supplied spans only.
- **L5 in-sample separated** — every row carries `in_sample: true`; the four fixtures carry
  `seeded: true`; the SUMMARY states plainly that nothing here is precision/recall evidence.
- **L6 vocabulary unchanged** — no HIGH was claimed anywhere (HIGH still needs ≥ 2
  independent signals + a written independence rationale); CANDIDATE was never blended into
  the promoted set; no rate without held-out data fixed before tuning.

## Campaign defaults

- suite green **with** corpus: `python3 -m unittest discover -s tests` → **39 tests, OK, 0
  skipped, 0 errors** (26 before this task → 39; count rose, nothing dropped).
- LAW §8 manifest: `runs/m4-q2-adjudication/PROVENANCE.json` binds adjudicator sha256, tool
  commit `9cd905d`, policy sha, main head, corpus zip, book-store sha, ledger reference,
  split, inputs digests, method parameters, counts, and the digests of all three outputs.
- fresh replay/determinism: two runs with the same inputs produce byte-identical
  `adjudication.jsonl` (test) and the committed artifacts were regenerated at the pinned
  tool commit.
- **spent holdout untouched** (`holdout_reads: []`, `holdout_enforced: true`).
- cadence: heartbeat + CONTROL.log written inside the work loop (25g §6); ORCH-2 lane read
  in-cycle (head `45959ca`, pause removed per `fleet/GATES.md`).

## Boundaries honoured

No detector re-tuning, no threshold change, no new detector, no writes outside this lane's
outputs, stdlib only, corpus read-only, no rate, no certification language.

## Working-state notes (disclosure, per ERRATA-25g §3c)

- The dev environment re-materialised mid-turn (git branch at the main base, `corpus/` and
  `evidence/` absent). Recovery: branch reset to the remote lane head, inputs rebuilt via
  `tools/m5r_inputs.sh` (zip `3f36c520…` verified), un-pushed work intact. Logged in
  `fleet/CONTROL.log` seq 30.
- Next per the owner order: **TASK-017** (inherit the v1 detector toolchain onto this lane
  with provenance), then TASK-014 q2–q4 re-cut against the fresh sealed split v2.
