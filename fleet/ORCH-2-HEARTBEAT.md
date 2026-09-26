ORCH-2 heartbeat — CONTROL seq 37

- **Self-item O-2 CLOSED**: `orch2_verify.py --selftest` asserts 18 named cases with no worktree needed; the
  helpers (`ts_class`, `draw_holdout`, `drop_rules`, `rule_a_defect`) were extracted so the tests run the real code
  paths; the 231-row section output is **byte-identical** after the refactor (diffed against the committed golden).
- **The selftest was mutation-tested**: five injected regressions, five caught (T1, T8b, T3+T7, T5, T11). One of my
  first mutants was a syntax error and proved nothing, so it was re-run validly — recorded in ledger §13.
- Standing rule now written down: any instrument change must pass `--selftest` and be diffed against the golden,
  with row movements explained in the ledger before the new output is committed.
- Unchanged: quantum b HELD behind item v2.a; TASK-015 M6-Final blocked; no detector promotable; no rate/precision.
- Fleet: BOSS-2 `67a4f0e` (zero controls, zero concerns); WORKER-2 `4fc40c8` static — no ORCH-2 action per
  ERRATA-25f.
