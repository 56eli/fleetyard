# fixtures (TASK-002 / M1)

- `confirmed/confirmed.json` — the CURRENT confirmed denominator: 16 CERTAIN
  transcript errors hand-found by reading three full transcripts end to end
  (no detectors): `Love_Sep_2011_Part_1` (10),
  `Satsang_Series_Volume_IX_Part_6` (4),
  `A_Unique_Sedona_Seminar_Dec_2008_Part_2` (2). (TASK-002 filed 18; the
  TASK-006 re-audit withdrew 6 and added 4 — see below.) Each record carries the
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

## TASK-006 re-audit (fixture taxonomy repair, 2026-09-24)

All 18 TASK-002 records were re-read against the exact transcript bytes, the
book quotes and STANDARDS legs a/b/c. Reading applied: leg (a) needs BOTH
halves — grammar/sense AND doctrinal sense (the restored text states Hawkins'
teaching, a scripture/prayer he cites, a teacher/author/term from the books);
leg (c) needs the lecture to actually contradict itself, not merely use a
different word elsewhere. Every change is in the append-only
`confirmed/corrections.json` (seq, date, reviewer, action, former/new
status, reason, full `record_before` snapshot for withdrawals).

| id | before | after | why (short) |
|---|---|---|---|
| CF-005 | CERTAIN b | HIGH CONFIDENCE (withdrawn) | truncation/repetition, not a near-form; fragment states no claim to contradict |
| CF-009 | CERTAIN a | CANDIDATE (withdrawn) | non-doctrinal announcement, grammar-only repair (successor finding upheld) |
| CF-013 | CERTAIN a | HIGH CONFIDENCE (withdrawn) | non-doctrinal Q&A; context corroborates, no contradiction |
| CF-014 | CERTAIN a | HIGH CONFIDENCE (withdrawn) | non-doctrinal Q&A; restatement corroborates, no contradiction |
| CF-016 | CERTAIN a | HIGH CONFIDENCE (withdrawn) | anecdote (eagle), not doctrine |
| CF-018 | CERTAIN a | HIGH CONFIDENCE (withdrawn) | non-doctrinal; interpreter rendering corroborates |
| CF-002 | CERTAIN a | CERTAIN b (retained) | examined: book attributes 'Love is Letting Go of Fear' verbatim to Jerry Jampolsky; transcript names 'Jempolski' |
| CF-007, CF-008 | CERTAIN a | CERTAIN a (retained, book leg added) | infatuation (cal. 145) vs Love (cal. 500) teaching, verbatim book passage |
| CF-001/003/004/006/010/011/012/015/017 | CERTAIN | CERTAIN (retained) | reviewed, legs stand |
| CF-019 | — | CERTAIN b (new) | '40% happiness' at level 200; book table row 200–300 '8% 1.5% 60% 9.0%' (3 of 4 values match) |
| CF-020 | — | CERTAIN b (new) | 'Truth vs. Falsehood ... calibrating at 380'; the book lists 'Enneagrams 390' |
| CF-021, CF-022 | — | CERTAIN a (new) | 'Perception/Productivity and infatuation is ...' — same slide pattern as CF-007/008 |

Honest limits:
- The floor (>= 15 CERTAIN from 3 fully read transcripts) is met at 16, but
  thinly: 10 of 16 are from one transcript, and 4 of 16 (CF-007/008/021/022)
  are ONE repeated ASR pattern on one slide (distinct instances, not distinct
  patterns). Without CF-021/022 the set would be 14 (floor FAILED).
- CF-020's error source (ASR "ninety"->"eighty" vs the questioner
  misremembering) cannot be told from text; it is in scope under the VISION
  default ("any quote the transcript attributes to a book that the book
  contradicts"). If the owner narrows scope to ASR-only, CF-020 goes and the
  floor is 15.
- New fixtures were found by re-reading the transcripts by hand. One more
  plausible error ('Lotus Land Buddhism' -> 'Pure Land Buddhism',
  Love_Sep_2011 @31465) was deliberately NOT added: the worker had seen it
  earlier in a B2 detector dump, so it is not independent of detector output.
- Withdrawn records are excluded from every evaluation denominator
  (`run_detectors.py --eval`, retrieval `--eval`); they are not deleted.

## negative/negative.json (TASK-010)

Negative regression examples: spans where detectors must NOT produce an
error signal (or must not reach HIGH CONFIDENCE). Stored as pointers
(transcript, offset, length, sha256) plus a short quote and the expected
outputs. NEG-001: Sedona Dec 2008 Part 2 @9671, the Korean interpreter's
legitimate `yes나` / `no를` code-switch; expected A2 = 0 signals, max
confidence CANDIDATE (A1's repeat may stand). Negatives are never counted as
recall or precision.
