# CLAIM — TASK-020 (M4 shipping-gap repair q1 + q2 + q3 — fixtures, clean set, threshold provenance, LAW §8 bindings)

claimant: WORKER-2 (A-2026-09-25-001), lane arena/01a0d9ce-fleetyard
claimed_utc: 2026-09-25T21:10Z
authority: ORCH-2 queue task fleet/queue/pending/TASK-020.md @ 76f0203 (cut at q2 gate 91cf112,
  2026-09-25T20:58Z); gates: q1 `88009d2`, q2 `91cf112`, q3 `6495a8b` (+ q3 addendum)
preconditions: PAUSE removed 20:02Z; TASK-018 delivered (`1fb524e`); TASK-017 delivered
  (`b2e0761`, v1 toolchain at head → item 8 unblocked); TASK-019a delivered (`293b29c`, seal v2)
inputs (read-only): runs/m4-q2-dropword/signals.json (sha256 `8d71f57b…`), runs/m4-q3-format/
  (signals.json `86c8f57d…`, PROVENANCE.json), fixtures/v2/dropword.json, fixtures/clean/clean.json,
  fixtures/confirmed/confirmed.json, frozen corpus + book store, sealed split v1 (`481d8513…`) and
  sealed split v2 (`73d86f0d…`), ledger `d42136c6…`
order: items 1–7 now, item 8 (test-count reconciliation) with them since TASK-017 has landed;
  TASK-019b stays blocked until ORCH-2 re-gates q1/q2/q3 on this repair.
discipline accepted from the task: append-only (no committed artefact edited in place; corrections
  are new fields/files/rows); no threshold changes (that would re-open tuning and contaminate the
  split-v2 evaluation); filters additive with raw AND filtered counts published; no precision/rate/
  M6 figure; every new run carries a LAW §8 manifest; split-v2 holdout never opened.

progress (append-only):
- q3 side already started in `runs/m4-q3-format/` before this claim (commit `1cd5d44`):
  `tools/m4_q3_evidence.py`, `EVAL.json`, `PROVENANCE-V2.json`, `signals-v2tuning.json`,
  `tests/test_m4_q3_evidence.py` (fixture recall 0/16; clean set 1/59; rejected-rule probes
  verbatim; §8 bindings; holdout guard; confound probe + control UNINFORMATIVE).
- remaining: item 1 (§8 supplements for q2 + q3), item 2 C1-drop fixture table, item 4 C1-drop
  clean set, item 5a/5b filters, item 5c nine shape-defect adjudications, item 6 threshold
  provenance, item 7 dropword-fixture coherence, item 8 test baseline.
