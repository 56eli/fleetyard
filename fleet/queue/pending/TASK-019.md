# TASK-019 — fresh sealed holdout split **v2** (+ its one-shot evaluation), owner-AUTHORIZED

- cut by ORCH-2 (A-2026-09-25-002) 2026-09-25T20:35Z · milestone **M4 → M6 FINAL**
- authority: owner `fleet/ERRATA-2026-09-25g.md` §5 @ main `7d033ab` (blob `84d3019f`,
  bytes sha256 `d0191e6d65d3eeb6969629678f54ec5ba1aa03f3d37dbaf896fa13feed405e6a`):
  "Fresh sealed split v2 is AUTHORIZED: cut it as a queue task (new salt, sealed before
  further tuning, evaluated once); M6-Final headline waits for it."
- why it exists: the q1 split's 37-transcript holdout was **evaluated once and is SPENT**
  (`runs/m4-q4-holdout/`, `holdout_consumed: true`, 19:12–19:14Z, counts only). LAW §9
  requires held-out data **fixed before tuning**; the reducer (errata #2) and the detector
  set have moved since, so no precision figure may rest on the spent split.
- claimant: WORKER-2 (A-2026-09-25-001) · order: **TASK-018 → TASK-019a → TASK-017 →
  (ORCH-2 gates q2/q3) → TASK-019b**

## Quantum a — SEAL split v2 (no evaluation in this quantum)
1. **New salt**, dated and distinct from `fleetyard-m4-holdout-2026-09-25`; publish the
   method (rule, modulus, bucket), the salt, the counts, the per-year table, the corpus
   file-set digest **with its derivation written down** (q1's `corpus_files_sha256`
   derivation reproduced cleanly — do the same, and say so in the file, not only in source).
2. Deterministic and independently reproducible: I must be able to re-derive the exact
   holdout/tuning sets from the published rule with my own code (this is the gate).
3. **In-sample exclusions forced to TUNING:** the 3 v1 fixture-bearing transcripts
   (`A_Unique_Sedona_Seminar_Dec_2008_Part_2`, `Love_Sep_2011_Part_1`,
   `Satsang_Series_Volume_IX_Part_6`) **plus every transcript carrying a fixture confirmed
   by TASK-018** (the 4 provisional dropword fixtures D2-001..D2-004 and anything else the
   leg-(d) adjudication confirms). Seal **after** TASK-018's fixture decisions land, so the
   forced set is complete.
4. **Re-seal rule:** if any fixture is confirmed *after* the seal, the split is void and must
   be re-sealed with a new salt + dated record. Never silently reused, never patched.
5. Seal = a committed file (e.g. `tools/HELD-OUT-SPLIT-V2.json`) + generator/verifier mode,
   committed **before** any further tuning of any detector (commit order is the evidence).
6. Repeat the honesty disclosure: v1 detectors were shaped with corpus-wide knowledge, and
   the drop-word/format rules were shaped on the tuning set — a first figure under v2 is an
   estimate under this split, not pristine out-of-sample.
7. LAW §8 manifest on the run that produces it (corpus + book-store digests, tool commit
   reachable, policy sha, main head, output digest, run utc, derivations).

## Quantum b — ONE-SHOT evaluation (only after ORCH-2 has gated q2/q3 and thresholds are frozen)
1. Thresholds frozen and recorded **before** the run; the run happens **once**; the receipt
   stamps `holdout_consumed`, the full read list, the split salt + digest, and the tool
   commit. Never re-run: a second run needs split v3 and a dated record.
2. Output: per-detector **precision + false-positive counts on the holdout**, with
   **seeded vs independent reported separately** (LAW §9), and per-signal adjudication
   records (each holdout signal confirmed/discarded **with reasons**, cited to bytes) —
   labels are hand reads, not detector agreement.
3. CANDIDATE is never blended into a rate; CERTAIN and HIGH are reported separately; no
   corpus-wide extrapolation beyond what the holdout supports; A4-confusion stays excluded
   unless this run supplies independent fixture recall + a genuinely held-out clean-FP
   measurement (v1's 0/59 is VOID as independent FP evidence — owner ERRATA-2026-09-25 §3).
4. B1/B2 headline gate: v1's hold stands (TASK-005 FAIL / REDIRECT-005 — B1 thresholds
   calibrated on the clean set, B2 filters fitted), so **no headline rate for B1/B2 until
   this quantum passes**.
5. Suite green WITH corpus, skip counts reported, test count never drops (campaign baseline
   v1's 115 tests — TASK-017); stdlib only, no network, corpus read-only, writes only to the
   named outputs.

## Gate (ORCH-2, LAW §9 — any failed criterion = INCOMPLETE)
v2.1 new salt + published method/modulus/bucket, deterministic, **re-derived by me exactly**
(set equality, not counts) · v2.2 corpus file-set digest reproduced from a **written**
derivation · v2.3 all in-sample transcripts (v1 fixtures + TASK-018 confirmations) forced to
TUNING, verified by set membership · v2.4 sealed before any further tuning, on commit-order
evidence · v2.5 §8 manifest complete and recomputed MATCH by me · v2.6 tuning path cannot
read the v2 holdout (filter + assertion + output evidence: keyed transcripts ⊆ tuning,
∩ holdout = 0) · v2.7 (quantum b) one-shot discipline: frozen thresholds, single run,
consumed receipt, no re-run · v2.8 (quantum b) labels are hand adjudications with reasons
and citations I re-derive byte-exact; seeded/independent separated; CANDIDATE never blended;
no rate beyond the holdout · v2.9 no promotion without this evidence; delivery labelled
DELIVERY, never completion or certification.


---

## Quantum a gate result + item v2.a (ORCH-2, 2026-09-25T21:46:52Z)

**Quantum a (sealed split v2) gated: FAIL / INCOMPLETE on v2.5 only; PASS v2.1, v2.2, v2.3, v2.4, v2.6, v2.9**
(full record in `fleet/GATES.md`). The seal is valid, reproduces exactly under ORCH-2's own re-derivation
(holdout set-equal 33, tuning set-equal 197, corpus digest `9ae90185…` recomputed), has zero fixture contamination
(all six fixture-bearing transcripts forced to TUNING; all 37 spent v1 holdout files forced to TUNING, 0 in the v2
holdout), is sealed before all further tuning on commit-order evidence, and its tuning path **refuses holdout reads
in code** (`HoldoutGuard` → `SystemExit`; `signals-v2tuning.json` = 197 entries, all ⊆ tuning, ∩ holdout = 0).
10 tests OK. Delivery correctly labelled DELIVERY, no evaluation run.

**Owed — item v2.a (one append; no re-draw, no new salt):** the seal's `fixture_sources` binding for
`fixtures/v2/dropword.json` is **stale** (`c8e96319…` recorded; `c40d272f…` at head after the post-seal append-only
annotation in `a5dec38`). Append a dated note that (i) binds `c40d272f…` with the reason and commit, (ii) records
ORCH-2's audit — 4 fixtures before and after, no ids added, no `status`/`confidence`/`evidence`/`quoted`/`char_offset`
change, and the two confirmations (D2-001, D2-003) dated **20:38Z, pre-seal** — and (iii) states that the
`re_seal_rule` was evaluated and **NOT triggered**, and that `79eb401` changed **only** the `manifest` key so
`293b29c`/`79eb401` are one draw, not two.

**New criterion v2.10:** every bound digest in the seal file recomputes MATCH at head, and the note is append-only.

**Restriction:** quantum b (the one-shot holdout evaluation) must **not** run until v2.a lands — v2.7 requires frozen
inputs. Then: thresholds frozen in advance, holdout read once, receipt consumed, no re-run, and the `disclosure`
framing carried into every figure ("an estimate under this split, not a pristine out-of-sample number").


---

## Item v2.b + criterion v2.11 (ORCH-2, 2026-09-25T22:01:33Z) — v2-holdout taint disclosure, found while gating TASK-020

Seven of the 122 pre-seal C1-drop signals lie in **four transcripts that are v2-holdout members**
(`Radical_Subjectivity_The_I_of_Self_Feb_2002_Part_2` ×4, `Realization_of_the_Self_as_the_I_Nov_2003_Part_1`,
`Spiritual_Traps_Oct_2005_Part_2`, `Witnessing_and_Observing_Oct_2004_Part_1`). Three of the seven were promoted
**CERTAIN-leg-d** by TASK-018 (`D-092` `percent`, `D-093` `it's`, `D-094` `huh`, all in the same file); four are
CANDIDATE (`D-095`, `D-107`, `D-108`, `D-122`). The seal's `disclosure` field does not state this.

**Item v2.b:** fold into the same dated append-only note as item v2.a: (i) the four holdout transcripts that already
carry C1-drop signal rows from the pre-seal v1-era run, with the seven signal ids and their verdicts; (ii) that the
shipped source-inheritance filter **deliberately deferred** those seven rather than open the holdout (endorsed);
(iii) that ORCH-2's gate verification read the span bytes of all 122 signals, including those four transcripts —
re-derivation, not tuning, with no rule or threshold changed; (iv) the consequence for quantum b: the one-shot
evaluation must either report a **per-file breakdown** disclosing that 4 of 33 holdout transcripts are already
signal-bearing, or **exclude those 4** with the denominator change stated in advance.

**Criterion v2.11:** the seal note discloses every pre-seal artefact that has touched a v2-holdout transcript, and
quantum b's plan states which of the two options above it takes **before** the single run.


---

# ANNEX — Quantum-b pre-registration protocol (ORCH-2, 2026-09-25T22:58:11Z, BINDING)

**Why this exists.** Quantum b is the **only** path to a precision figure for the C1-drop and C2-format rules, and it is
a **one-shot** run over a 33-transcript sealed holdout that cannot be replaced without a fresh salt. A one-shot
measurement is only worth anything if everything that could be chosen *after* seeing the result is fixed *before* the
run. This annex is that list. It is written now, while the holdout is still untouched, so that neither the worker nor
the gate can be accused of picking the denominator, the floor or the thresholds with the answer in hand.

**A. Preconditions (all gate-checked before the run may start)**
- **A1.** Items v2.a and v2.b landed: `HELD-OUT-SPLIT-V2.json`'s **own header** binds the actual fixtures-adj
  `c40d272f…` and discloses the taint, **append-only** (the superseded `c8e96319…` left readable); split v2 gated PASS.
- **A2.** Either TASK-018 items 0d–0g landed, **or** the adjudication set is explicitly excluded from the quantum-b
  eval — the decision is recorded in the pre-registration, not made afterwards.
- **A3.** Criterion **v2.10**: every digest bound by the seal recomputes MATCH at the pre-registration commit
  (detector shas, corpus files, fixtures, ledger, split v1), and the recomputation output is committed.
- **A4.** **Denominator decided in advance.** Recommended: **33 primary** with per-file disclosure of the four
  fixture-adjacent transcripts, **plus 29 as a pre-registered sensitivity** — both numbers fixed now, the primary
  chosen now.
- **A5.** The suite passes at the pre-registration commit, with corpus and skip counts recorded.

**B. Frozen inputs (digests recorded in the pre-registration commit; no change permitted until after the gate)**
- **B1.** Detectors: `det_dropword.py a0236325…`, `det_format.py ef9ff4f2…`; for the v1 leg the **13 pins** at
  `bf97d85…`, already materialized under `runs/v1/toolchain/pins/`.
- **B2.** Thresholds: the eight C1-drop parameters at their shipped values (**122 / 113 / 311 / 48 / 173 / 8 / 118 /
  110**), the seven C2-format rules with their provenance, the v1 configs (`a4b5b0c7…`, `324e22b9…`, `8823094b…`,
  `d4115b7c…`).
- **B3.** Adjudication rule: clause **d-i**, flank floor **5** (this is what makes the count "57"-shaped), with the
  **sensitivity band 71 / 57 / 33 / 22 pre-registered as a report, not a choice**. The gate will not accept a
  post-run change of floor.
- **B4.** Data: corpus zip `3f36c520…` (+ the 230 overlays, or re-materialized and re-digested), book store
  `c0892fcd…`, split v2 file digest (post-note), ledger `d42136c6…` (invariant), policy `0fe20a60…`, `main_head` at
  run time.
- **B5.** **The token rule stated explicitly** (a documented gate-instrument defect class in this campaign):
  apostrophes and hyphens **inside** tokens, em/en dashes as **separators**, and the key convention (transcript
  sha256, basename) used for every set-level comparison.
- **B6.** Classification vocabulary: **CERTAIN-leg-d / CANDIDATE** with reason codes. **No new label may be introduced
  after the run.**

**C. The single run**
- **C1.** Exactly one execution over the pre-registered holdout set. The run publishes `holdout_reads` — the list of
  holdout transcripts actually read — and the gate verifies it **equals** the eval set: no more, no less.
- **C2.** **No re-run for any reason.** Pre-registered abort rule: a crash **before any holdout byte is read** (proved
  by an empty read log) may be retried **once**; any crash after the first read **consumes the holdout**.
- **C3.** No threshold, detector, token rule or denominator may change between the pre-registration commit and the run
  commit.

**D. Outputs that must exist in the run commit** (nothing added afterwards except the receipt and an errata)
- **D1.** Raw per-detector signal counts for the holdout set.
- **D2.** Per-signal citations — transcript span bytes **and** book quote bytes — sufficient for independent
  re-derivation: the gate's own 938/938-style claim test must be reproducible on the holdout rows.
- **D3.** Per-signal adjudication under leg d-i with per-row reasons, `seeded` / `in_sample` flags, and the
  fixture-overlap test result. Expected: **no `seeded: true`** on any holdout row, because holdout transcripts carry
  no fixtures — this must be **verified and published**, not assumed (the prose in TASK-018 item 0d is exactly the
  failure this guards against).
- **D4.** The denominator used, with the four tainted files' disposition visible **per file**.
- **D5.** A **consumed receipt**: run digests, exact UTC **plus its source**, the statement that split v2's holdout is
  now **spent**, and a `holdout_consumed`-style note of the kind the q4 supplement used.
- **D6.** `one_shot_discipline` attested **and verifiable from the tool's source** — the gate reads the source, as it
  did for `tools/m4_q4_supplement.py` (0 references to `overlays`, `parse_book_store`, `run_tuning`).

**E. What may be quoted after the gate PASSes**
- **E1.** precision = CERTAIN-leg-d rows / signals, **with** denominator, flank floor, strata, site count,
  notation-class disposition, and the taint disclosure for the four files.
- **E2.** **No extrapolation** to the corpus; **no rate per transcript** unless exposure-normalized with the ratio
  stated (the §5d correction is the binding pattern).
- **E3.** The C1-drop expectation for the holdout may be compared (19.9 at v1 exposure), but the deficit's **cause
  remains unestablished**.
- **E4.** Every figure carries: split v2 · one-shot · in-sample-free · the **27% hyphen-tokenizer sensitivity** caveat
  wherever A1 claims are involved · PROVISIONAL until the gate PASSes.

**F. New gate criteria for quantum b (v2.7/v2.8 stand; these are added)**
- **v2.12** — the pre-registration commit exists **before** the run commit, verified by commit order and by exact
  timestamps carrying their source (per criterion 20.14).
- **v2.13** — the receipt exists, declares the holdout spent, and `holdout_reads` equals the pre-registered eval set.
- **v2.14** — nothing was added to the eval directory after the run except the receipt and an errata, verified from
  that path's commit history.
- **v2.15** — the `seeded` / `in_sample` separation is verified on the holdout rows (0 `seeded: true` expected; any
  deviation is a FAIL, and the field must be **present** on every row — an absent flag is as much a defect as a wrong
  one).
- **v2.16** — one-shot discipline verified from the tool's **source**, not only from its manifest.

**G. Prohibitions.** Never re-run the spent v1 holdout. Never re-certify M6-P. No detector is promotable on a receipt.
No M6 figure until this gate PASSes. **TASK-015 (M6 Final) stays BLOCKED until then.**
