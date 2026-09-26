# TASK-021 — C1-drop threshold sensitivity over the **v2 tuning half only** (the measurement the q2 README deferred)

- cut by ORCH-2 (A-2026-09-25-002) 2026-09-25T22:08:00Z · claimant: WORKER-2 · prerequisite: none (TASK-017 PASSed, toolchain inherited)
- why: `runs/m4-q2-dropword/README.md` (TASK-020 item 6) states the operating point is **unchosen** and its
  sensitivity **unmeasured**, and correctly declines to measure it inside split v2 discipline because 33 of the 193
  v1-tuning transcripts are **v2-holdout members** — recomputing the shipped run at other thresholds would open the
  seal. It defers the measurement "to split v3 or to an ORCH-2 gate-side scratch". This task cuts it properly, on the
  side of the seal that may be read.
- authority: LAW §9 (no certification without held-out evidence; in-sample never quoted as precision), STANDARDS tool
  gate, owner ERRATA-2026-09-25e §4 (detector hits never auto-classify) and §2 (leg (d) narrow), ERRATA-2026-09-25g §5
  (fresh sealed split v2, evaluated once).

## Scope — what may and may not be read
1. **Read the v2 tuning half only**: the 197 transcripts in `tools/HELD-OUT-SPLIT-V2.json['tuning']`. The 33 holdout
   transcripts must not be opened by this task, directly or through any cache. Reuse the `HoldoutGuard` pattern
   (`tools/m4_q3_evidence.py`) so the refusal is in code, and publish `holdout_reads: []` + `holdout_enforced: true`.
2. **No threshold may be chosen, fitted or recommended.** This is a sensitivity *map*, not a tuning run: publish
   counts, never an operating point, and never a precision or rate figure.
3. **Never compare to 122 without stating the denominator change.** The shipped 122 signals came from the **v1**
   tuning half (193 files, of which 33 are now v2-holdout members). A v2-tuning run has a different denominator
   (197 files) and a different membership; any table must carry both denominators and say so in the same line.

## Items
1. Run the inherited/unmodified C1-drop detector (`tools/det_dropword.py` @ `a0236325…`) over the v2 tuning half at
   the shipped settings, then at a published grid: `min_flank` ∈ {2, 3, 5, 8}, `min_ratio` ∈ {0.80, 0.85, 0.90},
   `min_matched` ∈ {8, 10, 14} — one parameter at a time from the shipped point (no full cross-product needed), plus
   the shipped point itself as the anchor row.
2. Publish per setting: raw signal count, count after the source-inheritance filter, count after the shape
   exclusions (`dropped-token-not-missing`), and the count of distinct sites (dedupe identical transcript+offset
   spans — TASK-018 item 0e found two duplicate sites inside the 57).
3. Publish the **stability set**: signals present at every setting in the grid, and signals present only at the
   shipped point. Those two numbers bound how much of any future figure is threshold-driven.
4. LAW §8 manifest for the run: detector digest at head, config digest per setting (state the recipe), corpus +
   book-store + corpus-zip digests, split file digest + counts, `tool_commit` **that contains the generating tool**
   (TASK-020 item 8a failed on exactly this), `main_head`, `policy_sha256`, `run_utc` exact to the second with its
   source, `holdout_reads`, and per-output digests.
5. One artefact directory (`runs/m4-t21-sensitivity/`) with `EVAL.json` + `README.md`; tests in `tests/` covering the
   holdout refusal, the grid arithmetic and the dedupe rule.

## Acceptance criteria
- 21.1 the v2 holdout is provably unread: guard in code, `holdout_reads: []`, and ORCH-2 can re-run the whole grid
  byte-identically from the published manifest.
- 21.2 every count in the table reproduces under ORCH-2's own re-run of at least two settings (anchor + one variant).
- 21.3 both denominators (v1 193 / v2 197) are stated with every comparison to the shipped 122; no line implies the
  numbers are interchangeable.
- 21.4 the stability set is published (present-at-every-setting vs shipped-point-only) and the two counts sum
  coherently with the anchor row.
- 21.5 no threshold is chosen or recommended; no precision, rate, recall or M6 figure appears anywhere in the
  artefacts; every output is labelled CANDIDATE-class / PROVISIONAL-UNGATED.
- 21.6 §8 manifest complete, every digest recomputes MATCH at head, and `tool_commit` contains the generating tool.
- 21.7 site-level dedupe rule stated and applied; duplicate sites counted separately from rows.
- 21.8 the suite stays green with the corpus present and the test count does not drop from 217.

---

## Cycle-J updates (ORCH-2, 2026-09-26T01:54:33Z)

**Criterion 21.8 / A5 — the binding suite floor is now 257.** Measured in the scratch worktree at `1c8a287` with the corpus
materialised (`python3 -m unittest discover -s tests -t tests`): **Ran 257 tests in 217.2s, OK (skipped=1)**. History:
217 published in this file (stale since `4fc40c8`) → 227 at `4fc40c8` → 244 at `72104a5` → **257 at `1c8a287`** (+5
`test_m4_pin_repair`, +6 `test_m4_t18_dispositions`, +2 pre-registered-exclusion harness tests). The skip count travels with
the count; a future delivery that lands below 257 fails 21.8 whatever its own test count says.

**Criterion 21.6's reading, amended by O-8 (stated in advance so no delivery is ambushed).** 21.6 asks for a `tool_commit`
containing the generator. TASK-020 item 8a landed a better shape, and 21.6 accepts **either** form, provided the delivery
says which it uses:

1. `tool_commit` contains the generating tool at the pinned sha (the original reading); **or**
2. a `generator_pins` block naming `generator_tool`, `generator_tool_commit` (a reachable commit whose blob of that tool
   hashes to `generator_tool_sha256`) and `generator_tool_note` explaining that `tool_commit` is the lane head at run time —
   the form all six supplements now carry, verified by ORCH-2 against `a5dec38` and `d7fee6e`.

Form 2 is preferred where the tool moved after the run, because it pins the bytes that produced the artefact rather than a
commit that happens to be head.


---

## STATUS UPDATE (ORCH-2 2026-09-26T09:55:22Z) — the binding suite floor is now **283**, not 257 and not 263

Measured at WORKER-2 `f5e2cf5` in a scratch worktree with the corpus and evidence materialised (`sh tools/m5r_inputs.sh`):
`python3 -m unittest discover -s tests -t tests` → **Ran 283 tests in 215.316s — OK (skipped=1)**, 29 test files. The rise from
263 is the worker's own twenty new tests in this delivery (`tests/test_m4_coherence_check.py` new, plus growth in the
seal-audit, one-shot-v2, t18-dispositions and t20-supplement suites). Criterion 21.8 / A5 binds **283** from this cycle: a
claimant whose run reports fewer tests has not run the suite at this head. Note for the claimant: the suite needs the
materialised inputs, and a fresh worktree without them fails in ways that look like test failures — §0 of the gate instrument
now preflights them (ledger §24.5).
