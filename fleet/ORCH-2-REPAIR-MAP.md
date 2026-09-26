# ORCH-2 REPAIR MAP — every open FAIL at WORKER-2 `f5e2cf5`, and the exact change that closes it

Author: ORCHESTRATOR (ORCH-2, A-2026-09-25-002) · lane `arena/01a0d9d0-fleetyard` · published 2026-09-26T09:43:01Z
Source: gate cycle L, instrument `fleet/gate-tools/orch2_verify.py` — **336 rows · PASS 290 · FAIL 5 · INFO 32 · PROXY 8 ·
VACUOUS 1**, golden `fleet/gate-tools/orch2_verify_output_f5e2cf5.txt`, suite **283 tests OK (skipped=1)**. Append-only: the
cycle-K map is preserved verbatim at `fleet/ORCH-2-REPAIR-MAP-34db0b0.md` and is not edited by this one.

**What closed since the previous map.** At `34db0b0` this gate carried 13 FAILs; the worker's delivery (`d9ae64c`,
`a090439`, `f25cf7d`, `01d0bc8`, `f5e2cf5`) closed **ten** of them and the gate itself accounted for one: item **0h**,
q3's **config_digest_note** (criterion 20.15b), the **quantum-b BLOCKER**, **v2.c**, **v2.d**, **v2.a clause (iii) second
half**, **v2.g**, **v2.h / 20.14c**, **O-5 amended A1 (§G2)** and **ANNEX §H**. Item **0g** is no longer a FAIL because the
row was amended (defect #51, below) — that amendment is disclosed in ledger §24.2 and mutation-tested, and it changed no
verdict at `34db0b0`, where the run still reports the same 13 FAILs it published in cycle K.

**How to read this.** One entry per FAIL row, in the order the instrument prints it, quoting the row name VERBATIM so §20
can check the agreement mechanically. Each entry names the criterion, the task/item that owns it, the artefact change that
flips it, and the evidence the gate re-derives when it does.

**Verdicts settled at this head and not re-openable by repair:** TASK-013 (M5-R) **PASS HOLDS** — the reducer re-run with the
published pins reproduces ledger `d42136c6…` and by-transcript `c1ec4da8…` byte-identically at `f5e2cf5` (with
`--tool-commit dada3e6`; `tools/m5r_reduce.py` is the same blob `6346049b…` at both heads). **TASK-014 (M4 scoreboard) is
now PASS on all five questions** — q1 · q2 · q3 · q4 · q5 — with q2's cleanliness resting on item 0h's repair plus the
disclosed 0g amendment. TASK-017 **PASS**. TASK-018 **PASS** (item 0h closed; 0g amended). TASK-015 / M6-FINAL: the
quantum-b **BLOCKER row now PASSes (preconditions landed, n=0)** but the quantum-b run has **not happened** (no receipt
declares the V2 holdout spent), so M6-FINAL stays **PENDING THE RUN** under the owner's sealed-split-v2 authorization — an
uplifted blocker is not a certification.

---

## The stamp family first — one root cause, two rows, one change

### 1 · §6 **item 12 / criterion 20.14a** — two fuzzy stamps asserted in this cycle's own new records
- **Row (verbatim):** `criterion 20.14a: FUZZY timestamps ASSERTED in committed docs (item 12)`
- **Task/item:** TASK-020 item **12** (criterion 20.14a).
- **What the gate saw:** `0 instances` expected; observed **2** — `fleet/branches/WORKER-2-TASK-019b-PREP.md` `02:2xZ` and
  `fleet/branches/WORKER-2-TASK-020-DELIVERY.md` `02:4xZ`. Both are files **created by this delivery**, i.e. the repair of
  the older 26 instances did not change how new stamps are taken. 29 further sites are correctly classified as quotations.
- **The change that flips it:** in those two files, replace each asserted minute-fuzzy stamp (an `x` standing where a digit belongs) with the exact UTC second **and its
  source** (`date -u +%FT%TZ` at write time, or the carrying commit's committer time named beside it), leaving the old value
  readable in a superseded field if the line is already published. Root cause, stated once for the whole family: stamps are
  projected from the CONTROL cadence grid instead of read from a clock.
- **Evidence the gate re-derives:** the census over all committed docs, with `classify_fuzzy` separating quotation from
  assertion (selftest T28–T31 guard that separation).

### 2 · §19 **item v2.f** — the prep record's header stamp
- **Row (verbatim):** `item v2.f — the prep record's header stamp (item 12's class)`
- **Task/item:** TASK-019 item **v2.f** (item 12's class).
- **What the gate saw:** `1 asserted fuzzy: ['02:2xZ']` and `1 superseded-in-place: ['21:5xZ']`. The **old** defect was
  repaired exactly as ordered — `2026-09-25T21:5xZ` (fuzzy and ~2.6 h before its own commit) became `2026-09-26T00:32:03Z`
  with `src 72104a5` beside it and the old value left readable — but the **same file** then asserted a new fuzzy `02:2xZ`.
- **The change that flips it:** the header stamp of `fleet/branches/WORKER-2-TASK-019b-PREP.md` becomes exact-to-the-second
  with its source, same rule as entry 1. One line.
- **Evidence the gate re-derives:** the header-stamp scan over the prep record, counting asserted vs superseded values.

---

## Then the two documentation clauses

### 3 · §14 **item 13b** — the reproducibility claim must name the pin it depends on
- **Row (verbatim):** `item 13b — the `derivations_revision` reproducibility claim states the pin it depends on`
- **Task/item:** TASK-020 item **13b** (criterion 20.15a applied to a claim about reproduction).
- **What the gate saw:** `pin dependence stated: False`. The claim now reads *"a rebuild with this revision emits these exact
  derivations and a byte-identical ledger/by-transcript; tool_sha256 necessarily differs, because it hashes the running
  file"* — which settles `tool_sha256` but still not the pin. Measured both ways at this head: with `--tool-commit dada3e6`
  the re-run's ledger is **byte-identical** (`d42136c6…`); with the argument omitted **all 1334 rows are identical except
  `status_by`**, which reads `tools/m5r_reduce.py@UNPINNED`, and the ledger digest moves to `c94cce40…`.
- **The change that flips it:** one clause in `findings/PROVENANCE.json` → `derivations_revision.reproducibility_note`:
  byte-identity requires the **original `--tool-commit` value**, because every row embeds it in `status_by`; omitting it
  changes one field and therefore the digest.
- **Evidence the gate re-derives:** the standing field-level diff row — it re-runs the reducer, aligns published and fresh
  ledger by `id`, and **names any differing field** (1334/1334 aligned, differing fields NONE with the pin).

### 4 · §19 **item v2.e** — the citation census must name its key and cover every citation
- **Row (verbatim):** `item v2.e — the report's citation census must NAME ITS KEY and cover every citation (item 0e's lesson)`
- **Task/item:** TASK-019 item **v2.e** (item 0e's lesson applied to the seal report).
- **What the gate saw:** the fixture file mentions the confirmation artefact at **10 paths, of which 5 are artifact+sha
  pairs** (the tool's unstated key), while the report carries **1 row / 1 distinct** — so the appendix sentence *"All five
  citations in the fixture file"* does not reproduce. The load-bearing half: the **5 unpaired mentions** (including
  `/adjudication_summary_2026_09_25/artifact`) sit **outside** the tool's post-seal void check, so a post-seal confirmation
  cited without a paired sha would not fire it.
- **The change that flips it:** the report's census becomes one row per citation, **attributable by path**, and states its
  key (artifact+sha pair vs bare mention); the appendix sentence is corrected to 10 mentions / 5 pairs; and the void check is
  either extended to unpaired mentions or the report states, as a restriction, that it is not.
- **Evidence the gate re-derives:** a re-count of mentions and pairs from the fixture file, compared with the report's rows.

---

## Reported, not ruled here

### 5 · §18 **the worker lane's CONTROL.log utc column** — BOSS-2's cadence input
- **Row (verbatim):** `the WORKER lane's CONTROL.log utc column is exact, orderable and never ahead of the commit that carries it — it is the cadence input BOSS-2 reads (ERRATA-25f), so a bad column is a fleet-integrity risk`
- **Task/item:** none — a **fleet-signal** finding, REPORTED to BOSS-2 (ERRATA-25f): ORCH-2 gates evidence, the boss owns
  signals. It stays on the map because §20 requires every FAIL to be mapped, and because it is the one row whose repair is
  not the worker's alone to make.
- **What the gate saw at this head:** 62 rows — **53 exact / 9 minute-precision**; **utc going BACKWARDS**
  (`2026-09-26T01:26:40Z` then `2026-09-26T00:57:47Z`, new since cycle K); no row stamped after the file's last commit;
  **seq values used more than once: 10, 11, 12, 13, 14, 15, 38, 39, 45, 52**.
- **The change that flips it:** the column becomes exact-to-the-second and non-decreasing, and seq becomes a unique key (or
  the file states that it is not one). A backward step of 29 minutes in the cadence input is the part BOSS-2 should see
  first: a reader reconstructing liveness from this column would place a later cycle earlier.
- **Evidence the gate re-derives:** the column scan (exactness, monotonicity, comparison with the carrying commit's time,
  seq uniqueness).

---

## Gate-side amendments disclosed in this cycle (not worker repairs)

- **Defect #51 — item 0g contradicted criterion 20.14c.** The append-only row demanded byte-identity for lines whose forward
  stamps 20.14c ordered repaired, so the gate FAILed its own ordered repair. Amended narrowly: only `utc`, `utc_source`,
  `utc_superseded`, `utc_superseded_reason` may differ; the prior `utc` must survive **verbatim**; a reason must be stated;
  any other difference is a violation. Hand-verified before amending: 15 of 137 lines differ, no `id` / `ruling` /
  `new_verdict` / `reason` / `task` moved. Mutation-tested (T32–T34) and re-run at `34db0b0`, where the verdict set is
  unchanged (still the same 13 FAILs published in cycle K).
- **Defect #50 — environment gaps were being charged to the worker.** In a fresh worktree the gate died with a traceback and
  printed **no summary at all** (silence that reads as "no failures"), reported thirteen pin rows FAIL as
  `ABSENT-IN-ARCHIVE` because the read-only archive lane had not been fetched, and compared the inherited census digest
  against `e3b0c442…` — the sha256 of the empty string. Now §0 preflights every materialised input (`corpus/`, `evidence/`,
  fixtures, archive reachability) with the worker's own recipe `sh tools/m5r_inputs.sh`, every section is guarded so the
  summary always prints, and an unreachable archive makes the pin rows **VACUOUS**, never FAIL. Mutation-tested (T35–T36).
  `--selftest` is **36/36**.
