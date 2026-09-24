# fixtures (TASK-002 / M1)

- `confirmed/confirmed.json` — 18 CERTAIN transcript errors hand-found by
  reading three full transcripts end to end (no detectors):
  `Love_Sep_2011_Part_1` (9), `Satsang_Series_Volume_IX_Part_6` (5),
  `A_Unique_Sedona_Seminar_Dec_2008_Part_2` (4). Each record carries the
  STANDARDS finding fields: transcript path, paragraph + char offset,
  verbatim quote, suspected intended text, evidence class (a/b/c) with the
  evidence chain, detector id, book reference (slug + char offset + verbatim
  book quote) where doctrinal, confidence, status (+ who).
  Offsets are Python `str` indices into the UTF-8-decoded file
  (`tools/loaders.py`). Every transcript is a single line, so paragraph = 0.
- `clean/clean.json` — 59 clean-set passages from the 20 Hawkins books in
  the book store, stored as pointers (slug, char offset, length, sha256),
  materialized from the local frozen corpus by `tools/fixtures.py`. The four
  non-Hawkins book-store entries (`loaders.NON_HAWKINS_SLUGS`) are excluded.

`python3 tools/fixtures.py verify` re-checks every quote, offset and hash
against `corpus/`. `python3 tools/fixtures.py build-clean` regenerates the
clean set deterministically.
