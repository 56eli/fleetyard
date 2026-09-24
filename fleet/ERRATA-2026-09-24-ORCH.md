# ERRATA — 2026-09-24 (orchestrator)

## E1: Owner ruling on 230/231 count
The seed docs' "231" = directory ENTRIES under `overlays/` (230 transcripts + manifest.json).
230 is the transcript count. AUDIT-PLAN M5 "all 231 transcripts" reads 230.
The sweep covers all 230. TASK-001 gate (M0 corpus inventory) stands on its numbers.

## E2: Owner ruling on Thought_and_Ideation Part 1
`Thought_and_Ideation_Feb_2004_Part_1` missing from the zip: corpus anomaly, correctly
recorded in M0 census (part-number gap). Not a Hawkins error; out of audit scope. No action.

## E3: Correction from REDIRECT-001 — no missing file
The orchestrator's earlier claim of a "missing file" was incorrect. The battery expects 231
directory entries under `overlays/` including `manifest.json`. Nothing is missing. The
campaign denominator is **230 transcripts** (231 overlay entries).

## E4: AUDIT-PLAN M5 reads "231 transcripts"
AUDIT-PLAN.md M5 still reads "all 231 transcripts" — should read 230. The file is
byte-identical (blob 0684af57) on main, worker, and orchestrator lanes. Per CANON §4 /
VISION §3, agents never write main; raised as CONCERN for owner action.