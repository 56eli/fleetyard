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
## Successor addendum — 2026-09-24T23:27:14Z (append-only)
Worker claimed this task @ 90080502f9b065be7e70addf121b425690e21359 (2026-09-24T23:06:07Z). Existing `status: OPEN` at top is historical, **not** a second unclaimed task. SELF-M3a retrieval was delivered and successor re-gated PASS (6/10 cited book refs @5), but contradiction/misquotation/terminology remain, no M3 certification. Factual correction to the old notes: there are **10 fixtures with book_refs, of which 5 are class b**, not "10 class-b fixtures". PAUSE-WORKER now names TASK-006 exclusively; after its PASS the worker CONTINUES this claimed M3 task from its current lane progress, never restarts. M2 is ACCEPTED INCOMPLETE per owner errata; M5 must not ingest A4 in-sample FP or unreviewed signals as rates. For next gates, detector fixture overlap is recall, *not precision*, and clean evaluation must be independent.

## Successor gate addendum — 2026-09-24T23:46Z (append-only)
Worker delivered TASK-005 @ 1e1c57b9b1a61eaf81c1419a6e4755c7e3b76f68 (pushed after reconnect; heartbeat d70d4b9). Independent successor gate at f165889: suite 78 tests OK, B1 2/18 and B2 1/18 independent fixture overlap, exact book refs, self-tests and runner present. These implementation checks PASS, but criterion 3's independent clean-set FP evidence FAILS: disclosures 7–8 explicitly describe tuning B1/B2 rules on the same 59 scored clean passages/book store; their 0/59 is in-sample. Precision unmeasured. Full-task certification is HELD, with focused TASK-009 repair using new holdout after TASK-007; the worker must not repeat TASK-005 from scratch. M3 also lacks terminology drift and explicit attribution, so no M3 milestone certification.
