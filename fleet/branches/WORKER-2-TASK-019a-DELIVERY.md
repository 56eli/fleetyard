# WORKER-2 — TASK-019a DELIVERY (fresh sealed split v2)

- task: **TASK-019 quantum a** (ORCH-2 queue `fleet/queue/pending/TASK-019.md` @ `6495a8b`)
- authority: owner `fleet/ERRATA-2026-09-25g.md` §5 (fresh sealed split v2 AUTHORIZED)
- claimant: WORKER-2 (A-2026-09-25-001), lane `arena/01a0d9ce-fleetyard`
- status: **DELIVERY** (not completion, not certification); **no evaluation was run** in this
  quantum (that is 019b, gated on ORCH-2's q2/q3 gates and frozen thresholds)

## The seal

`tools/HELD-OUT-SPLIT-V2.json` — **sha256 `73d86f0dafe5e51162723bd92121021a099a5c6b5b89fc5386421c496ced5d8a`**
(committed *before* any further tuning; commit order is the evidence, v2.4).

| field | value |
|---|---|
| salt (fresh, dated) | `fleetyard-m4-holdout-v2-2026-09-25` |
| rule | `bucket(basename) = int(sha256(SALT+basename),16) mod 5`; bucket 0 → HOLDOUT; else TUNING |
| counts | **tuning 197 / holdout 33 / total 230** |
| forced to TUNING | **43** — the 6 fixture-bearing transcripts (3 v1 hand-confirmed + all 3 carrying TASK-018 drop-word fixtures, whether adjudicated CONFIRMED or refused) **plus the 37 transcripts of the spent v1 holdout** |
| v1-holdout ∩ v2-holdout | **0** (disclosed contamination-avoidance rule: the v2 holdout is entirely unseen; the 37 read-once v1-holdout transcripts are forced into tuning) |
| corpus file-list digest | `sha256_text("\n".join(sorted basenames) + "\n")`, derivation written into the seal file itself (v2.2) |
| per-year table | inside the seal (`by_year`) |
| generator/verifier | `tools/m4_split_v2.py` (`build` / `verify`), stdlib only — the seal's `manifest.tool_sha256` binds the head revision of that file |

`python3 tools/m4_split_v2.py verify --split tools/HELD-OUT-SPLIT-V2.json --corpus corpus`
→ **OK** (run_utc `2026-09-25T20:50:46Z (src 293b29c; read `20:5xZ`)`). Independent re-derivation from the published rule is
the gate: anyone with the salt, the modulus and bucket number, and the corpus file list can
reproduce both sets exactly (set equality, not counts).

## Criterion evidence

- **v2.1** fresh salt + published method/modulus/bucket; the verifier recomputes the sets
  from the rule and compares as sets; a tamper test (swap one name between the sets) is
  refused with `bucket mismatch`.
- **v2.2** `corpus_files_sha256` is the file-list digest with its construction written into
  the seal (same construction as v1, so the two are comparable); the *content* pin remains
  the frozen corpus zip sha256 `3f36c520…` in the manifest block. Regression test
  re-derives the digest from the corpus directory independently.
- **v2.3** every in-sample transcript is forced to tuning: the 3 v1 fixture transcripts
  (`A_Unique_Sedona_Seminar_Dec_2008_Part_2`, `Love_Sep_2011_Part_1`,
  `Satsang_Series_Volume_IX_Part_6`) and the 3 transcripts carrying TASK-018's drop-word
  fixtures (`Causality_The_Ego_s_Foundation_Jan_2002_Part_1` and `_Part_3`,
  `Love_Sep_2011_Part_2`). Verified by set membership (`holdout ∩ forced = ∅`); the seal was
  cut **after** TASK-018's fixture decisions landed, so the forced set is complete.
- **v2.4** sealed before any further tuning — no detector, threshold or fixture was touched
  in this task; this delivery is the sealing commit's record.
- **v2.5** LAW §8 manifest block inside the seal: run utc, tool + tool sha256, tool commit,
  main head, policy sha, corpus zip sha, book store sha, and the derivation block; the seal's
  own digest is recorded here (a file cannot contain its own hash).
- **v2.6** tuning path cannot read the v2 holdout — `tools/det_dropword.py`,
  `tools/det_format.py` and `tools/m4_q4_holdout.py` take `--set tuning|holdout` and stamp
  `holdout_reads`/`holdout_enforced` in their provenance; the v2 evaluation runner (quantum b)
  will take the v2 split explicitly. Tests assert the split's disjointness and the forced-set
  membership so a later edit cannot silently break it.
- **v2.9** no promotion, no rate, no precision claim anywhere in this delivery.

## Disclosure carried into the seal (honesty, v2.6/§5.6)

v1 detectors were shaped with corpus-wide knowledge, and the drop-word/format rules were
shaped on the v1 tuning set. A first figure under v2 is therefore **an estimate under this
split**, not a pristine out-of-sample number. What the split guarantees is that *future*
tuning cannot silently consume the transcripts it will later be measured on: the one-shot
evaluation reads the v2 holdout only, once, with thresholds frozen in advance, and a second
run requires split v3.

## Re-seal rule (binding)

If any fixture is confirmed **after** this seal, the split is **VOID** and must be re-sealed
with a new salt and a dated record. Never silently reused, never patched.

## Suite

`python3 -m unittest discover -s tests` → **164 tests, OK, 1 skipped** (154 before this task
+ 10 new split-v2 tests; the single skip is the not-yet-committed M6 report).

## Next

**TASK-019b is blocked** until ORCH-2 gates q2/q3 and the thresholds are frozen. Meanwhile:
cadence continues (heartbeat + CONTROL.log ≤300 s; controls and the orchestrator lane read
every cycle); nothing else in the queue is claimable by me.

## Addendum (2026-09-26, append-only) — post-seal fixture-digest audit

A pass over the seal's own tripwire (`fixture_sources`) found that
`fixtures/v2/dropword.json` no longer hashes to the digest recorded at seal time
(`c8e963199a1e…` → `c40d272f30d0…`, last touched by `a5dec38`). That is exactly the class of
event the re-seal rule above is about, so it was adjudicated from git bytes rather than
assumed benign:

* `tools/m4_seal_audit.py` (+7 tests) recovers the seal-time blob
  (`git show 79eb401:fixtures/v2/dropword.json`) and diffs it against HEAD. Result: the change
  is **append-only** — no `fixtures[]` entry was added, no key present at seal time changed
  value (`mutations` empty). The added blocks are TASK-020 item 7's enacted-leg annotation and
  the exact-utc keys.
* The only confirmation artefact cited there, `runs/m4-q2-adjudication/fixtures-adjudication.json`
  (`61568a9e…`), belongs to commit `1fb524e` at 2026-09-25T20:38:18Z — **13 minutes before** the
  seal commit `79eb401`. No fixture was confirmed after the seal.
* Membership still holds: the 43 forced-to-tuning names do not intersect the 33 holdout
  names; `tools/m4_split_v2.py verify` passes.
* Report: `runs/m4-q2-adjudication/SEAL-AUDIT.json` — verdict **STANDING (appendix owed)**,
  written at head `14255bd`. Appendix (owed): `runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md`,
  naming both digests.

**Verdict: the v2 seal STANDS; no new salt is owed; the split-v2 holdout is not void.** The
seal file itself is untouched (`73d86f0d…`, `79eb401`). The defect this exposes — a
seal-time digest of a file that later appends will invalidate, producing a benign tripwire
rather than a confirmation signal — is stated in the appendix, with the recommendation that a
future seal bind either an append-only-free fixture source or the seal-time blob's own sha
(the audit already compares those two numbers).

## Addendum 2 (2026-09-26) — GATE CYCLE H items v2.a and v2.b discharged

ORCH-2's GATE CYCLE H failed quantum a on **v2.5 (item v2.a)** and the **v2.b note** only
(v2.1–v2.4, v2.6, v2.9 PASS; seal valid, reproducible, NOT void). Both are now discharged by a
**new dated file**, `tools/HELD-OUT-SPLIT-V2-NOTE-2026-09-26.md`, written next to the seal so
that a reader who verifies the seal and finds the digest mismatch is led straight to it:

* **v2.a** — the note binds the actual digest (`c40d272f…` vs the sealed `c8e96319…`), leaves
  the superseded `fixture_sources` line readable (the seal file is untouched at `73d86f0d…`),
  states the append-only adjudication (no fixture added, no sealed value mutated, the one
  confirmation artefact `61568a9e…` is commit `1fb524e` — 13 minutes *before* the seal) and
  names the defect class (a seal-time digest over a file later amended by design is a benign
  tripwire, not a confirmation signal) with a build-time recommendation for future seals.
* **v2.b** — the note states the taint (four holdout transcripts, seven signals: `D-092`
  percent, `D-093` it's, `D-094` huh promoted; `D-095`, `D-107`, `D-108`, `D-122` CANDIDATE),
  records that the shipped filter deliberately deferred them rather than open the holdout
  (ORCH-2 endorsed), records ORCH-2's gate re-derivation of all 122 span bytes including those
  four transcripts as re-derivation and not tuning (no rule or threshold changed), and carries
  the seal's standing caveat verbatim — *"a first figure under v2 is an estimate under this
  split, not a pristine out-of-sample number"*.

**Quantum-b consequence, pre-registered before the run (item v2.b iv):** the four label-tainted
transcripts are **excluded from the reported denominator** — evaluated holdout **29 of 33**.
Machine-readable: `tools/HELD-OUT-SPLIT-V2-EXCLUSIONS.json`; bound into the freeze and enforced
by `tools/m4_one_shot_v2.py` (`run` evaluates exactly `holdout − exclusions`, refuses exclusions
that are not holdout members, refuses a post-freeze change to the exclusion set, drops the
excluded signals unexamined — they enter no artefact, denominator or review queue — and the
receipt lists evaluated and excluded transcripts separately). The choice is recorded **now** so
it cannot be made after the numbers appear.

`tools/m4_seal_audit.py` now looks for a dated note naming both digests and reports the
discharged state (`SEAL-AUDIT.json`: **STANDING — dated note on file**). No threshold, detector,
split, salt or membership changed; no rate or M6 figure.
