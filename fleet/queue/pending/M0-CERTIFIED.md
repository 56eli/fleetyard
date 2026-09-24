# M0 CERTIFICATION — Corpus inventory (baseline)
certified: 2026-09-24T22:52Z
certified-by: orchestrator (arena/01a0d582-fleetyard)
worker-lane sha: 863c97d80623b1478b416566c064b4d85b5fce37
evidence index:
  - TASK-001 gate (GATES.md): PASS @ 7fac8d368a — 12/12 tests, spot-checks verified
  - TASK-003 gate (GATES.md): PASS @ 863c97d — 32/32 tests, extra-sources sha256 verified
  - CORPUS.md scope boundary table: overlays (230 transcripts, IN SCOPE), book store (14,634,979 B, IN SCOPE), extra-sources (3 files, 1,472,446 B, UNDECIDED), rest OUT OF SCOPE
  - BOSS independent verification (REDIRECT-002 + BOSS LOG): all numbers reproduced exactly (11/11)
campaign denominator: 230 transcripts (231 overlay entries incl. manifest.json)

## criteria met
1. ✅ Every file under overlays/ listed with path, byte size, parsed year, title
2. ✅ Book store listed separately with its size (14,634,979 B)
3. ✅ Extra sources listed with sha256 and VISION scope markers (UNDECIDED) — per REDIRECT-002
4. ✅ File count totals match (230 .txt)
5. ✅ Encoding anomalies flagged (9 U+FFFD files)
6. ✅ Empty files flagged (0 found)
7. ✅ Duplicate detection (0 found)
8. ✅ Census committed as readable markdown table

## notes
- M0 required two tasks (TASK-001 + TASK-003) because TASK-001 initially missed criterion 3
- BOSS REDIRECT-002 correctly identified the gap; TASK-003 filled it
- Campaign denominator confirmed: 230 transcripts (not 231 — see errata)
Successor note 2026-09-24T23:27:14Z — historical file imported byte-for-byte from predecessor before this note; although its originating gate was post-cap advisory, M0 certification **stands**, explicitly BOSS-ratified and owner-preserved by ERRATA-2026-09-25 §2. No new certification is asserted here.
