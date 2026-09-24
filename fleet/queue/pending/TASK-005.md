# TASK-005: Detector family B — doctrinal consistency (M3)
milestone: M3 — Detector family B (doctrinal consistency)
status: OPEN
cut: 2026-09-24
cut-by: orchestrator (arena/01a0d582-fleetyard)

## deliverable
Detectors for doctrinal-consistency errors, building on M1's book-store reader and M2's detector framework:

1. **Book-passage retrieval** — stdlib TF-IDF (or similar) over the book store; given a transcript span, find the most relevant book passage(s)
2. **Contradiction/garble detection** — transcript claims vs retrieved book passages: detect when the transcript states something the book contradicts
3. **Terminology drift** — Hawkins-specific terms (calibrate/calibration, levels of consciousness, ego vs Self, etc.) used inconsistently or incorrectly
4. **Misquotation detection** — when a transcript attributes a quote to a specific book, check if the book text matches

Each detector must meet the same gates as M2: self-test, fixtures precision, clean-set FPs.

## acceptance criteria
1. ≥2 detector modules implemented and tested (contradiction + misquotation minimum)
2. Book-passage retrieval implemented (stdlib TF-IDF or equivalent, no external libs)
3. Each detector has self-test + clean-set FP check (target: 0)
4. Each detector catches ≥1 of the existing 18 fixtures (or new fixtures from doctrinal reading)
5. `python3 -m unittest discover -s tests` green, test count ≥ 50
6. A runner extension or `tools/run_detectors.py` integration for B-family detectors
7. Tools remain stdlib-only, no network, read-only over corpus/**

## notes
- NON_HAWKINS_SLUGS (Be_as_you_are, I_AM_THAT, Lamsa_bible, ACIM_workbook) must NOT be cited as Hawkins doctrine — M3 detectors should exclude them from doctrinal comparison
- The 10 class-b fixtures with book refs provide seed evidence for doctrinal detectors
- VISION open item: "misquotation" scope — does it include other-author quotes? Default: only Hawkins' teaching + any quote attributed to a book that the book contradicts
- VISION open item: Book-of-Slides OCR is UNDECIDED — treat as suspect until ruled
- Book store has 20 Hawkins books (24 total minus 4 non-Hawkins) — the retrieval index covers these
- TF-IDF can be implemented with collections.Counter and math.log — stdlib only
- The clean set (59 passages from 20 books) serves as the negative set for doctrinal detectors too