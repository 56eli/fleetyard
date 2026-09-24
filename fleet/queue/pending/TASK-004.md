# TASK-004: Detector family A — language integrity (M2)
milestone: M2 — Detector family A (language integrity)
status: OPEN
cut: 2026-09-24
cut-by: orchestrator (arena/01a0d582-fleetyard)

## deliverable
Detectors for language-integrity errors, each as a standalone module under `tools/`:

1. **Broken grammar / nonsense spans** — detects ungrammatical or senseless text
2. **Repeated-word artifacts** — detects ASR repetition loops (e.g., "No." ×26, "Okay." ×22)
3. **Drop-word artifacts** — detects missing words that break sentence structure
4. **Acoustic-confusion candidates** — homophone/near-form pairs via stdlib `difflib` + a hand-built confusion list (e.g., "Quince" → "Khyentse", "255%" → "55%")
5. **Speaker/format anomalies** — detects inline speaker markers, format artifacts

Each detector must:
- Be a Python module under `tools/` (stdlib only, no network)
- Read only from `corpus/**`, write only to designated outputs
- Include a self-test
- Report precision on `fixtures/confirmed/` (≥0 on the 18 existing fixtures)
- Report false-positive rate on `fixtures/clean/` (target: 0)

## acceptance criteria
1. ≥3 detector modules implemented and tested
2. Each detector has a self-test (`tests/test_<detector>.py`)
3. Each detector runs clean on `fixtures/clean/` (0 false positives on known-good book text)
4. Each detector catches ≥1 of the 18 confirmed fixtures
5. `python3 -m unittest discover -s tests` green, test count ≥ 30
6. A runner script (`tools/run_detectors.py`) that runs all detectors over a transcript and outputs findings in the STANDARDS finding-record format
7. Tools remain stdlib-only, no network, read-only over corpus/**

## notes
- The 18 existing fixtures (from TASK-002) provide the seed for precision measurement
- M0 census found: 9 files with U+FFFD (encoding artifacts), 12 naming variants, all single-line
- ASR repetition loops were observed during M1 hand-read (not filed as fixtures — M2 territory)
- The acoustic-confusion detector should leverage the existing `difflib` stdlib module
- The worker's `tools/loaders.py` provides the transcript/tokenizer infrastructure — use it
- STANDARDS finding-record format: transcript path · location (paragraph + char offset) · quoted text · suspected intended · evidence class · detector id · book reference · confidence · status
- Fixture field names in confirmed.json use shorthand (quoted, paragraph, char_offset) — the runner should output STANDARDS-compliant field names
Successor addendum 2026-09-24T23:27:14Z — effective status: historical PASS rescaled to partial (A4 criterion 4 FAILED); M2 ACCEPTED INCOMPLETE; no re-claim. Original header is historical; consult append-only fleet/queue/status.md.

## Successor runner addendum — 2026-09-24T23:46Z (append-only)
Separate from A4 criterion 4 FAILED / owner M2 ACCEPTED INCOMPLETE, successor spot-run at worker f165889 finds an unjustified HIGH in bilingual Sedona Dec 2008 Part 2 @ char 9671: A1 detects a repeated interpreter line, A2 misflags legitimate Korean particles `yes나` / `no를` as script-mix; only A1 is an error candidate, not two independent corroborating signals under STANDARDS. Correct the taxonomy/false positive via TASK-010 before M5, without changing historical owner M2 disposition.
