# WORKER-2 — TASK-014 q3 shipping-evidence rebuild (C2-format) — lane delivery

**Worker:** WORKER-2 (`A-2026-09-25-001`), lane `arena/01a0d9ce-fleetyard`
**Trigger:** ORCH-2 gate `2026-09-25T20:44Z` (head `6495a8b`): *TASK-014 q3 = FAIL / INCOMPLETE*
on three shipping criteria — q3.2 (no fixture recall anywhere), q3.3 (no clean-set run), q3.5
(§8 manifest lacking `tool_commit` / `policy_sha256` / `main_head` / output digest, and a
`detector_sha256` binding an older commit). The gate found the detector's **substance clean**
and applied an artefact-scoped restriction: *C2-format is not promotable, its 49 signals stay
CANDIDATE, no M6 figure may quote them*.
**This delivery is evidence, not a gate.** The restriction stands until ORCH-2 re-gates.

## What was produced

| artefact | content |
|---|---|
| `tools/m4_q3_evidence.py` | build/verify instrument (stdlib only, read-only over corpus + book store) + holdout guard |
| `tests/test_m4_q3_evidence.py` | 19 tests (guard, split integrity, determinism, tamper detection, findings) |
| `runs/m4-q3-format/EVAL.json` | fixture recall, clean-set run, rejected-rule probes (verbatim), book-store confound probe **and its control** |
| `runs/m4-q3-format/PROVENANCE-V2.json` | LAW §8 manifest of the new run with every binding the gate asked for |
| `runs/m4-q3-format/signals-v2tuning.json` | the run: **197 v2-tuning transcripts → 48 signals** `{R1 25, R2 2, R3 5, R5 12, R6 3, R7 1}`, sha256 `b25651e4cbb5670e2685fef450b039ae42b175832c01d9bdf0a6606efc60f1c2` |
| `runs/m4-q3-format/README.md`, `tools/PATTERNS.md` §3/§5c | the record and the catalogue fix for the §3 "not built" contradiction the gate flagged |

## Results (measured, nothing here is a rate)

* **q3.2 fixture recall = 0/16.** C2-format fires inside none of the 16 confirmed fixtures.
  Format artifacts are not what those fixtures encode — the answer the gate predicted, now
  **measured and stated** rather than left blank.
* **q3.3 clean set = 1/59 misfire** (in-sample tune passages; an FP count, **not** an
  independent FP rate). The single misfire is `R1` `r.W` in `power.When` (CL-026,
  `power_vs_force__the_hidden_de…`) — and that same glue occurs **verbatim in the book store**
  at that passage. The clean passages are known-good but **not certified artifact-free** with
  respect to R1; recorded, not hidden.
* **q3.4 documentation gap closed.** Both rejected-rule probes are republished with regex +
  flags, re-measured on the v2 tuning half: double-word `\b(\w+)\s+\1\b` (re.IGNORECASE)
  **2,876 / 195 files**; camel probes **104 / 53** (any internal capital), **6 / 6**
  (lowercase-start), **3 / 3** (classic), **2 / 2** (lower-upper run). The historic
  "35 hits / 18 files" census figure is marked **superseded** — its exact pattern was never
  recorded, which was the gap. The *decision* to reject camel-glue stands: the examples are
  dominated by proper nouns.
* **q3.5 §8 bindings present**: `tool_commit`, `main_head` (`7d033ab`), `policy_sha256`
  (`0fe20a60…`), `detector_sha256` at head (`ef9ff4f2…`), `corpus_zip_sha256` (`3f36c520…`),
  `split_corpus_files_sha256`, output digest, `run_utc`, `holdout_reads: []`,
  `holdout_enforced: true`. The historic run is **cited by digest** (`86c8f57d…`), not
  replayed.

## Discipline recorded

* **The v2 holdout was never opened.** Every transcript read goes through a guard that raises
  on any holdout name; fixture transcripts are forced-to-tuning by the seal, so reading them is
  tuning work. `verify` asserts `holdout_reads: []`.
* **The historic 193-transcript run was not replayed** — 33 of its files are v2-holdout members;
  replaying it would have opened the sealed holdout. The new run is over the v2 tuning half.
* **The confound probe is reported as UNINFORMATIVE, because its control failed.** A nested
  window probe (bare glue / ±10 / ±25 chars vs every book) returned 0/48 on both window tiers —
  which would *look* like "transcripts do not inherit book text". The control over the 15
  fixtures that carry a book reference returns **15/15 on the bare quote but 0/15 on the same
  windows**: transcripts and the book store are normalised differently, so the window tiers
  cannot detect book-derived text on this corpus. The negative result is **not** evidence of
  independence and is not reported as such. (Instrument lesson, recorded as the gate's own
  probes were: calibrate a probe before believing its negative.)
* **Determinism**: build with a fixed `--utc` reproduces byte-identical outputs (test-covered);
  `verify` rebuilds from the corpus and fails on any tampering (test-covered).
* No corpus or evidence file is committed; no detector logic was modified; no thresholds were
  set; no rate is claimed; the 48 new signals are CANDIDATE-class and **receive no promotion
  from this delivery**.

## Suite

`python3 -m unittest discover -s tests` → **Ran 183 tests, OK (skipped=1)** — up from 164
(19 added); no test was removed or weakened. `tools/m4_q3_evidence.py verify` → OK, holdout
reads 0.

## Open for ORCH-2

1. Re-gate q3 on these artefacts (`EVAL.json` + `PROVENANCE-V2.json` + `signals-v2tuning.json`).
2. q3.4's remaining half is a **doc** judgement (whether the §3/§5c catalogue text is now
   consistent); q3.2/q3.3/q3.5 are measurements above.
3. The q2+q3 repair task ORCH-2 said it would cut may fold this in or supersede it; this file
   claims no criterion as passed.
