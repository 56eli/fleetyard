# TASK-001: Corpus inventory (M0)
milestone: M0 — Corpus inventory (baseline)
status: OPEN
cut: 2026-09-24
cut-by: orchestrator (arena/01a0d582-fleetyard)

## deliverable
- `tools/CORPUS.md` committed on the worker lane
- Per-file list: path, bytes, year, title parse
- Totals cross-checked against the bootstrap battery
- Anomalies noted: empty files, duplicates, encoding issues

## acceptance criteria
1. Every file under `corpus/docdocgo/overlays/` listed with path, byte size, parsed year (from filename or content), and title
2. Book store file listed separately with its size
3. Extra sources listed if present
4. File count totals match actual `find corpus/docdocgo/overlays/ -name '*.txt' | wc -l` (currently 230)
5. Encoding anomalies flagged (files not valid UTF-8)
6. Empty or near-empty files (< 100 bytes) flagged
7. Duplicate-content detection (hash comparison)
8. The census is committed as a readable markdown table

## notes
- Bootstrap letter expected 231 overlays; actual count is 230 — the worker should document this discrepancy
- The worker must run `python3 -m unittest discover -s tests` before pushing (even if tests are minimal at this stage)