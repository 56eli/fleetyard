# TASK-002: Tooling foundation (M1)
milestone: M1 — Tooling foundation
status: OPEN
cut: 2026-09-24
cut-by: orchestrator (arena/01a0d582-fleetyard)

## deliverable
- `tools/loaders.py`: transcript reader (plain text → paragraphs with char offsets), book-store reader (parses JS-embedded book JSON into slug→text)
- `tools/tokenizer.py`: tokenizer (stdlib)
- `fixtures/confirmed/`: ≥15 CONFIRMED errors hand-found by reading 3 full transcripts, each with full evidence chain
- `fixtures/clean/`: clean-set sample from the book store
- Tests for all of the above

## acceptance criteria
1. Transcript reader: reads a .txt file from overlays/, returns list of paragraphs with (text, char_offset, byte_offset). Note: per M0 census, all transcripts are single-line (no newline-delimited paragraphs) — the reader must handle this correctly (single paragraph or split by sentence/punctuation).
2. Book-store reader: parses `corpus/docdocgo/html/merged-book-texts_json_1.js` → dict of slug→text. Must handle the JS variable assignment prefix.
3. Tokenizer: splits text into tokens (words). Stdlib only.
4. Fixture set `fixtures/confirmed/`: ≥15 CONFIRMED errors from 3 different transcripts. Each error has: transcript path, location (paragraph + char offset), quoted transcript text (verbatim), suspected intended text, evidence class (a/b/c per STANDARDS), book reference if doctrinal.
5. Clean set `fixtures/clean/`: sample passages from the book store (known-good text). Used to verify detectors don't false-positive on clean text.
6. All tests green: `python3 -m unittest discover -s tests`. Test count ≥ current count (do not drop tests).
7. Tools are stdlib only, no network, read-only over corpus/**.

## notes
- The 9 files with U+FFFD replacement chars may affect text processing — loaders should handle or flag these.
- The 12 naming variants (no _enxautogen_html suffix) and 52 undated filenames should be handled by the reader.
- Fixture errors must be hand-found by READING transcripts, not by running detectors (detectors come in M2).