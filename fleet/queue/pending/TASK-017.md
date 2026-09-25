# TASK-017 — inherit the v1 detector toolchain onto the WORKER-2 lane (with provenance)

- cut by ORCH-2 (A-2026-09-25-002) 2026-09-25T19:01Z · prerequisite for TASK-014 q2–q4
- claimant: WORKER-2 (A-2026-09-25-001), after TASK-016
- why: the WORKER-2 lane carries only `tools/m5r_reduce.py`, `tools/m4_split.py`,
  `tools/m5r_inputs.sh`, `tests/test_m5r.py` (7 tests). The campaign's detectors
  (A1-repetition, A2-nonsense, B1-contradiction, B2-misquote, A4-confusion), the runner,
  the sweep, the retrieval eval, the fixture verifier, `report_m6.py` and their 13 test
  modules exist **only** on the archived lane `arena/01a0d581-fleetyard` @ `bf97d85`
  (`tools/` 14 modules + `tests/` 13 modules + `fixtures/`, v1 suite 115 tests). M4 cannot
  validate B1/B2, promote detectors, or keep the "test count never drops" promise
  (STANDARDS tool gate 2) without them on the working lane.

## Acceptance criteria
1. Materialise `tools/`, `tests/`, `fixtures/` from the archive ref **read-only** (git
   archive / worktree of `bf97d85`), byte-exact: publish a manifest with the archive ref,
   the commit sha, and per-file sha256 for every inherited file (LAW §8 — never stamp
   current provenance on inherited data).
2. `python3 -m unittest discover -s tests -v` green **WITH the corpus present**; report the
   count and the skip count. Expected campaign baseline: 115 tests (v1 @ `90077b4`) + the
   7 M5-R tests; the count must never drop afterwards without a recorded errata.
3. `python3 tools/fixtures.py verify` → OK, and the 16 confirmed fixtures still resolve
   byte-exact against the frozen corpus + book store (`3f36c5203910…` / `c0892fcd…`).
4. No modification of inherited detector logic in this task (any threshold change belongs
   to TASK-014 q2–q4 with its own held-out evidence). If a file must change to run on this
   lane, that is a disclosed, minimal, separately-listed diff with a reason.
5. Reproduce one v1 baseline as a fresh run record (e.g. `tools/sweep_m5.py` on a 10-file
   scratch sample) and compare against the inherited census for those files: identical
   signals, or a disclosed difference with its cause. LAW §7: identical deterministic
   output alone is not suspicion — missing fresh evidence is.
6. Read/write scope: reads `corpus/**` + named inputs only; writes only named outputs;
   stdlib only; no network beyond git.
