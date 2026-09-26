# M4-q4 — holdout runs (one-shot) — PROVISIONAL-UNGATED

Frozen detectors over the **holdout** half of `tools/HELD-OUT-SPLIT.json`
(37 of 230 transcripts). Thresholds were frozen before the run; nothing was tuned
against the holdout; every provenance file carries `holdout_consumed: true`.

## What was run (three bounded quanta)

| part | detector(s) | transcripts | raw signals | wall | provenance |
|---|---|---|---|---|---|
| v1 | A1,A2,B1,B2 (inherited v1 tools, sha-pinned) | 37/37 | **185** | 103 s | `v1-holdout.PROVENANCE.json` |
| drop | C1-drop (M4-q2) | 37/37 | **5** | 97 s | `part-holdout-drop.PROVENANCE.json` |
| format | C2-format (M4-q3) | 37/37 | **12** | <1 s | `part-holdout-format.PROVENANCE.json` |

Per-detector signal instances (v1): A1-repetition 162 · A2-nonsense 15 ·
B2-misquote 8 · B1-contradiction 0.

## The one thing this run does prove: reproduction

The independent re-run of the v1 detectors on the holdout transcripts reproduces
the inherited M5 census **exactly** — 185/185 signals, **0 per-transcript count
mismatches** across all 37 files (check performed against
`evidence/runs/m5-raw/records/*`). That is a reproduction receipt for the inherited
census under a fresh process, fresh index build, and a different code path.

## What this run does NOT prove (stated, not glossed)

- **Counts are not precision.** Precision/recall need reviewed labels — a human
  STANDARDS pass over the holdout signals. No such pass exists; no rate is claimed.
  Raw signal counts can be mostly false alarms or mostly real errors; this run does
  not distinguish.
- **Densities, for context only (not rates):** signals per transcript — v1 tuning
  5.95 vs holdout 5.00; C1-drop tuning 0.63 vs holdout 0.14; C2-format tuning 0.25 vs
  holdout 0.32. The dimension is called *density*, not a rate: a signal count is not an
  error count.
- **CORRECTION (appended 2026-09-25T21:27:18Z (src d7fee6e; read `21:3xZ`), TASK-020 item 10):** the earlier statement
  here that these differences are "dominated by sampling noise" is **wrong for C1-drop**.
  Normalized by character exposure (holdout transcripts are 14.9% shorter; the holdout is
  1,996,122 of 14,224,783 corpus chars), v1 is 185 observed vs **187.9 expected**
  (P(X≤185) = 0.44) and C2-format 12 vs **8.0** (P = 0.94) — both consistent — while
  C1-drop is 5 vs **19.9** (P(X≤5) = **7.7e-05**): a real ~4x deficit, not noise. Causes
  recorded, neither established: parameters fitted to the tuning half (now partly testable
  via TASK-020 item 6 provenance) or a book-exposure difference between halves (testable
  only on split v2, TASK-019b). **Never re-run the spent holdout to find out.** See
  PATTERNS §5d for the table and the derivation.
- **The holdout is now spent for these detectors and versions** (one-shot discipline,
  LAW §9 / PATTERNS §5). Any later tuning informed by these counts invalidates this
  evaluation for that detector; a new split (new salt) is then owed.
- No ORCH-2 gate exists: PROVISIONAL-UNGATED.

## Files

- `v1-holdout.json` — per-transcript records (v1 shape) for the 37 holdout files
- `v1-holdout.PROVENANCE.json` — detector shas, split binding, counts, one-shot stamp
- `part-holdout-drop.json` / `.PROVENANCE.json` — C1-drop holdout signals (5)
- `part-holdout-format.json` / `.PROVENANCE.json` — C2-format holdout signals (12)

Runner: `tools/m4_q4_holdout.py` (`v1` | `drop` | `format`), committed on this lane.

## Correction-2 (appended 2026-09-26, TASK-020 item 11a)

The item-10 correction above gives the v1 expectation as **187.9 / P = 0.44**; the gate's q4
result gives **187.6 / 0.4451**, and the gate is right for this row. Both numbers come from the
same census at two counting units: the 193 tuning transcripts hold **1,149 v1 records** but
**1,151 detector rows** — two records in `Love_Sep_2011_Part_1_enxautogen_html` carry two v1
families each (`A1+B1`, `A2+B1`). The exposure expectation must use **records**:
1,149 × 0.1632327 = 187.555 → **187.6** (P = **0.4451**); 1,151 × 0.1632327 = 187.88 → 187.9
(P = 0.4357) — the value this file previously carried, from rows. Conclusion unchanged: v1 is
consistent with tuning exposure. Tuning-side counts per row, re-derived at head: **1,149** v1
records (A1 776 · A2 143 · B2 220 · B1 12 rows) · C1-drop **122** · C2-format **49**. The C1/C2
rows are unaffected (single-family runs; 8.0 / P 0.94 and 19.9 / P 7.7e-05 as published).
See `tools/PATTERNS.md` §5d.
