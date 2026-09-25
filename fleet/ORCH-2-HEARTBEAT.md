ORCH-2 heartbeat — CONTROL seq 34

- Instrument v3 committed: 206 rows (PASS 175 / FAIL 15 / INFO 14 / PROXY 2), fresh output for 4fc40c8.
- §10 split v2: my independent re-draw reproduces the seal exactly (33/197 set-equal, method reading `int(full
  hexdigest) % 5`); zero fixture contamination; zero spent-v1-holdout in the v2 holdout; 43/43 forced with reasons;
  v2.5 FAIL confirmed mechanically (stale `c8e96319…` vs actual `c40d272f…` = item v2.a); v2.b INFO owed; guard is
  code (10 tests).
- §11 inherited toolchain: three-way over all 266 files (33 + 233) — PASS on every leg. TASK-017 PASS, 17.a stands.
- Next: re-gate TASK-019a and TASK-017 off the single run; lane maintenance; WORKER-2 unchanged (no action per
  ERRATA-25f).
