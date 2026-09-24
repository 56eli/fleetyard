# TASK-001: Corpus inventory (M0)
milestone: M0 — Corpus inventory (baseline)
status: GATE-OPEN (numbers PASS, criterion 3 pending per REDIRECT-002)
cut: 2026-09-24
cut-by: orchestrator (arena/01a0d582-fleetyard)
claimed: 2026-09-24T22:23Z (self-serve by worker, no queue at boot)
delivered: 52dce65 on worker lane
gate: numbers PASS @ 7fac8d368a (12/12 tests, spot-checks verified), NOT CERTIFIED (criterion 3)

## deliverable
- `tools/CORPUS.md` committed on the worker lane (`tools/census.py` + `tests/test_census.py`)
- Per-file list (path, bytes, year, title parse), totals cross-checked against the bootstrap battery
- Anomalies noted (empty files, duplicates, encoding)
- **CORRECTION (REDIRECT-002):** criterion 3 "Extra sources listed if present" is UNMET.
  `corpus/docdocgo/extra-sources/` (3 files, 1,472,446 B) is not censused.
  TASK-003 supplements M0 with the extra-sources census.

## acceptance criteria
1. ✅ Every file under `corpus/docdocgo/overlays/` listed with path, byte size, parsed year, title
2. ✅ Book store file listed separately with its size
3. ❌ Extra sources listed if present — NOT MET (per REDIRECT-002)
4. ✅ File count totals match actual find (230 .txt)
5. ✅ Encoding anomalies flagged (9 files with U+FFFD)
6. ✅ Empty or near-empty files flagged (0 found)
7. ✅ Duplicate-content detection (0 found)
8. ✅ The census is committed as a readable markdown table

## notes
- Bootstrap letter's "231" = directory entries (230 .txt + manifest.json). Campaign denominator = 230 transcripts.
- Thought_and_Ideation_Feb_2004_Part_1 is a part-number gap, not a missing file (manifest never listed it).
- Worker self-served M0 before orchestrator lane existed — legitimate per role spec.