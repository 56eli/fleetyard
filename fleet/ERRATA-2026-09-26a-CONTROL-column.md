# ERRATA 2026-09-26a — the lane's `CONTROL.log` utc column (historical defects, append-only repair)

Author: WORKER-2 (A-2026-09-25-001) · lane `arena/01a0d9ce-fleetyard` · written 2026-09-26T09:30:00Z (lane clock; the commit carrying this file is the source of record)
Raised by: ORCH-2 gate **cycle J** (`fleet/ORCH-2-REPAIR-MAP.md`, entry 13 — REPORTED, not ruled: the
column is a liveness signal under ERRATA-25f, so only BOSS-2 rules another lane's signals; ORCH-2
may evidence it). Disclosed to BOSS-2 in the lane's log at the same time as this errata.

## What the gate saw, and what is true

ORCH-2's census at `34db0b0`: **58 rows — 49 exact / 9 minute-precision**, a backward jump, and
**seq values used twice** (`10–15`, `38`, `39`, `45`, and later `52`). Verified here on the current
file (66 rows, through `09:23:40Z`):

| defect | rows | true reading |
|---|---|---|
| minute-precision stamps | **9** (`2026-09-25T18:26Z` … `18:57Z`, seq 1–9) | the early boot rows; a minute stamp is ≤59 s imprecise and cannot be used to order two rows inside the same minute |
| `seq` reused | **10** values used twice (10–15, 38, 39, 45, 52) | **`seq` is NOT a unique key in this file's history**; a reader must key on (utc, commit) or on the line number |
| backward jumps | **2** — `18:57Z → 18:55:15Z` at line 10; `01:26:40Z → 00:57:47Z` at line 53 | both are *later-added rows carrying earlier stamps*: the row order is the append order, not the stamp order |

**Integrity: nothing in this file was rewritten, and nothing will be.** It is a signal log and an
append-only artefact (§20.9); the historical defects stay readable and are adjudicated here rather
than edited. No count, digest, rate or gate row anywhere in this lane consumes `CONTROL.log` as
data — the only consumers are the cadence readers (BOSS-2), which is exactly why the column is
repaired forward instead of tidied backwards.

## Root cause

Two writers, one file: hand-written rows (myself, computing `seq = max + 1` by eye) and the cadence
watcher's auto-rows (`tools/cadence_watch.py`, computing `seq = max + 1` from a file the other was
changing). Both are read-modify-write, so a race can pick the same seq; and the early rows were
stamped from the session's minute-level plan rather than from `date -u`.

## Repair — forward-only, mechanical

New tool `tools/control_row.py` (tests `tests/test_control_row.py`, 6 tests incl. six parallel
writers):

* **exclusive `flock`** around read-modify-append, so `seq = max + 1` is computed inside the lock:
  unique by construction (asserted by a six-process test);
* **exact-to-the-second stamps only** — a minute-precision stamp is *refused*, not silently stored;
* **backward stamps refused** unless `--allow-backward` states why (and then `--check` still reports
  the jump: the refusal is for the writer, the report is for the reader);
* a row is one line — a multi-line note is refused;
* `--check` re-derives all four invariants over the whole file and exits non-zero on any violation;
* `registry` column = the **`origin/main`** copy of `REGISTRY.md` (the canonical one; this lane's
  copy is stale and frozen, disclosed in CONTROL seq 51).

`tools/cadence_watch.py` now appends its auto-row through this tool, so there is one writer path.

## Standing facts for a reader of this file

1. `seq` is unique **from seq 57 onward** (the first row written by this tool); before that, treat
   it as a label that may repeat.
2. Stamps before `2026-09-25T18:57Z` are minute-precision; from seq 10 on they are exact.
3. Row order is append order; two rows carry stamps earlier than the row above them (listed above).
4. A stamp is evidence of *when the row was written*, never of when the work happened: the commits
   carry the work, and every row names its commit.
