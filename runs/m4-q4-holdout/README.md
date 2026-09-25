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
- **Rates, for context only:** signals per transcript — v1 tuning 5.95 vs holdout
  5.00; C1-drop tuning 0.63 vs holdout 0.14; C2-format tuning 0.25 vs holdout 0.32.
  With 37 holdout transcripts these differences are dominated by sampling noise; the
  C1-drop gap is flagged as an **open question** (possible parameter fit to the
  tuning half) for M4 follow-up, not a conclusion.
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
