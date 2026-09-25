# M5-R — reviewed findings ledger (README)

Deliverable of milestone **M5-R** (fleet/PLAN-v2.md), produced by WORKER-2 on lane
`arena/01a0d9ce-fleetyard`, under main `5fdd00e` and policy `0fe20a6057ec9fa2…`.

It reduces the inherited M5 raw census (`arena/01a0d581-fleetyard` @ `bf97d85`,
READ-ONLY archive) — **1,334 unreviewed records / 1,336 detector-signal instances**
over 230 transcripts — into findings with their evidence attached.

## Files

| file | what it is |
|---|---|
| `ledger.jsonl` | one JSON object per finding, deterministic order (transcript, offset, detectors) |
| `by-transcript/<name>.json` | all findings for that transcript — **all 230 transcripts present**, empty arrays included (coverage truth) |
| `SUMMARY.md` | funnel, class distribution, by detector/year, hotspots, HIGH rationales, book-byte adjudication, corroboration table |
| `REVIEW-QUEUE.md` | top 100 by a **mechanical** review score (ordering aid only — never a class) |
| `PROVENANCE.json` | LAW §8 run manifest: every input pinned by sha256, tool sha, output digests, stats |

## Coverage truth (STANDARDS honesty rule; the campaign row since v1)

`transcripts 230 | detector-run 230 | machine-adjudicated 230 | human finding-pass
audited 0 | pending human review 230 | zero-finding transcripts 24 (not shown clean)`

“Reviewed” in this ledger means **machine-adjudicated against cited bytes** — a
machine-adjudicated reduction of the raw census, not a human finding pass. No human
has yet read all 1,334 findings, and the 24 zero-finding transcripts are not “clean”,
they are unmeasured by several detectors.

## What “reviewed” means here — and what it does not

Every finding is **machine-adjudicated against cited bytes**:

1. **Citation verified** — the quoted text is byte-exact at the cited paragraph +
   char offset in the locally reproduced corpus (0 failures of 1,336).
2. **Claim re-derived** — where a mechanical check exists, the runner's own
   evidence string was recomputed from the bytes: A1 repetition structure
   (period × repeats), A2 anomalies (U+FFFD bytes, non-ASCII/script-mix letters,
   impossible percentages incl. `6,000%` / `590 percent` forms), B1/B2 book
   references (quote byte-exact at the cited slug + book offset; word-level
   divergence and number comparison computed where the quote verifies).
3. **Seeded vs independent separated** (LAW §9) — findings whose span is covered by
   the v1 hand-confirmed fixture set are marked `seeded=true` (in-sample for
   detector metrics; never precision/recall evidence). Independent = everything
   else.
4. **Classified per STANDARDS** — with one hard rule: **this tool never assigns
   CERTAIN**. Legs a/b/c each require human judgment (near-form sense restoration,
   same-teaching book contradiction, self-contradiction), so:
   - `CERTAIN (inherited fixture)` — only where a prior hand-confirmed v1 fixture
     covers the span (cited by id); inherited, not re-certified here;
   - `HIGH (convergence, proposed)` — ≥2 *independent* signal families
     (surface-form = A1/A2 vs content/doctrine = B1/B2 with a verified book leg)
     plus a written independence rationale; proposed for gate review;
   - `CANDIDATE` — everything else; human read required before any upgrade.

**It does not:** hear audio, replace the human read, produce an error rate, or claim
that zero-hit transcripts are clean. Drop-word / speaker-format / A4-confusion were
never run (unmeasured ≠ zero).

## Headline numbers (this run)

- 1,334 findings from 1,334 records; 0 citation failures; 0 exact duplicates.
- Classes: **CERTAIN (inherited fixture) 2** (CF-003, CF-006) · **HIGH 0** ·
  **CANDIDATE 1,332**. Seeded 2 / independent 1,332.
- Claim corroboration (after M4-q5 errata #2): **A1 938/938 · A2 158/158 · B1 12/12
  · B2 228/228 — 0 flagged.** The earlier 98 A1 "not re-derived" flags were defects
  in this tool (ASCII-only tokenizer; 8-token search bound), fixed and documented in
  `findings/M4-q5-A1-CLAIM-RECONCILIATION.md`.
- Book-byte adjudication: 242 cited book references, **242 verified byte-exact at
  the cited slug + offset**, 0 failures, 0 non-Hawkins citations.
- `HIGH 0` is a real result, not a gap: the only two cross-family convergences in
  the whole census are exactly the two fixture-overlapping spans (in-sample), so
  there is no *independent* convergence to propose today.

## Reproduce

```sh
sh tools/m5r_inputs.sh evidence          # archive inputs (READ-ONLY lane) + corpus
python3 tools/m5r_reduce.py \
    --records evidence/runs/m5-raw/records \
    --fixtures evidence/fixtures/confirmed \
    --corpus corpus --out findings --utc <ISO8601Z>
python3 -m unittest tests.test_m5r        # 6 tests; determinism asserted
```

Determinism: two runs with the same `--utc` produce byte-identical
`ledger.jsonl`, `by-transcript/*`, `SUMMARY.md`, `REVIEW-QUEUE.md` (verified on the
real inputs; current ledger sha256 `64977c2fed5be3f5814cf0bf6099d5565d51497572ed6cd559d0554fb72e5e04`).

Corpus identity: `docdocgo-fixes.zip` sha256 `3f36c5203910…`; overlays digest
`027f82a0d2522f3e0f9403c7d0f787a67e30560e941b29fa4ee813f6dbb5dd6e` computed by a
**defined, documented method** (sha256 over sorted `"<sha256(text)>  <basename>"`
lines — the inherited run cited a digest with no recorded method; this tool fixes
that for M5-R and later work).

## Interface to the rest of the campaign

- **M6 (final report):** per-class counts by year/detector/transcript, hotspots and
  the queue come from here; rates still need human review + held-out data.
- **M4 (self-improvement loop):** the corroboration table and the 98 A1 claim
  mismatches are direct detector-quality inputs (over-wide spans, tokenizer-shape
  differences); CERTAIN findings inherited from the fixtures remain the rule-source.
- **Gating:** this is a DELIVERY, not a certification (LAW §2.1); ORCH-2 gates it
  per LAW §9 when that activation exists. Nothing here is a rate, a pass, or a
  completion.

> **SUPERSESSION (appended 2026-09-25T21:4xZ, TASK-020 item 11 — q5.7):** the ledger digest
> quoted above (`64977c2f…`) is **no longer current**. TASK-016's regeneration (`a4c6655`)
> rewrote the record shape two minutes after the q5 run, and the ledger at head is
> **`d42136c673188f9e091526083b95941cabc5822a8b5cffeb8913b942cb658a32`** (1,334 findings).
> The old line is left readable, not rewritten — it was true when written. **The binding of
> record is `findings/PROVENANCE.json`** (its `outputs.ledger.jsonl` field), not any digest
> quoted inside prose: any figure on this page is void unless that manifest agrees.
