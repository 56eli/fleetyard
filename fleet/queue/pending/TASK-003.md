# TASK-003: Extra-sources census (M0 supplement)
milestone: M0 — Corpus inventory (supplement for criterion 3)
status: OPEN
cut: 2026-09-24
cut-by: orchestrator (arena/01a0d582-fleetyard) per REDIRECT-002

## context
REDIRECT-002 (boss lane arena/01a0d585-fleetyard) found that TASK-001 acceptance criterion 3
("Extra sources listed if present") is unmet. `corpus/docdocgo/extra-sources/` holds 3 files
(1,472,446 B) whose trust level VISION marks "side UNDECIDED ... treat as suspect until ruled".
The census must record them so M5's full-corpus sweep has a documented boundary.

## deliverable
- Extend `tools/census.py` (or `tools/CORPUS.md`) to also census `corpus/docdocgo/extra-sources/`
- Per-file: path, bytes, sha256
- Explicit in-scope / out-of-scope / UNDECIDED marker per VISION
- Book store (`corpus/docdocgo/html/merged-book-texts_json_1.js`) listed separately with its size
- Regenerate via `tools/census.py`, do not hand-edit

## acceptance criteria
1. `corpus/docdocgo/extra-sources/` listed in CORPUS.md with per-file path, byte size, sha256
2. Each file has an explicit scope marker: UNDECIDED (per VISION)
3. Book store listed separately (14,634,979 B)
4. `python3 -m unittest discover -s tests` green, test count ≥ current count
5. Tools remain stdlib-only, read-only over corpus/**

## BOSS evidence (from REDIRECT-002)
```
Book_of_Slides_Barret_notes.txt             159279  sha256:eff8b8b1c99f
Book_of_Slides_discord_ocr.txt               52450  sha256:0ad660acfbab
Book_of_Slides_phone_ocr.txt               1260717  sha256:655a84b26136
TOTAL 1472446 bytes (3 files)
```

## notes
- This is NOT a criticism of the worker's M0 work (BOSS LOG: "the worker's M0 work is in-bounds and its numbers are exact")
- VISION open item: owner must decide which side of the ledger Book-of-Slides OCR sits on
- Until owner rules, UNDECIDED is the correct classification
Successor addendum 2026-09-24T23:27:14Z — effective status: GATED for M0; owner/BOSS-ratified M0 CERTIFIED; not a new OPEN task. Original header is historical; consult append-only fleet/queue/status.md.
