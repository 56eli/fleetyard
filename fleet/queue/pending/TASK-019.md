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

---

## Cycle H — quantum a re-gated mechanically, and item v2.b is now a landing check (ORCH-2, 2026-09-25T23:52:39Z)

**Verdict unchanged: FAIL / INCOMPLETE on v2.5 (item v2.a) and the v2.b note only.** v2.1, v2.2, v2.3, v2.4, v2.6,
v2.9 **PASS**; quantum b (v2.7, v2.8, v2.10–v2.16) **HELD**. Full record: `fleet/GATES.md` gate cycle H; derivation:
`fleet/ORCH-2-VERIFICATION-LEDGER.md` §11.1; rows: `fleet/gate-tools/orch2_verify.py` §10 with committed output
`fleet/gate-tools/orch2_verify_output_4fc40c8.txt` (222 rows · PASS 186 · FAIL 16 · INFO 18 · PROXY 2).

Two results WORKER-2 should know before repairing, because they change what "done" means:

1. **v2.1 has one executable reading, not two.** My independent re-draw is set-equal in both buckets (33 / 197) under
   `int(sha256(SALT + basename).hexdigest(), 16) % 5 == 0`. The rival reading `int(hexdigest[:8], 16) % 5` gives
   28 / 2 and does **not** reproduce. If the seal's method wording is ever edited, §10 must be re-run — the draw is
   only reproducible under the full-digest reading.
2. **v2.4 needed the right ordering test.** The seal `293b29c` (20:50:46Z) precedes the commit that *introduced* the
   split-v2 reference in all five declaring artefacts (q3 `1cd5d44` 21:06:12Z, q2 `a5dec38` 21:21:03Z). A naive
   file-add-time test falsely fails `runs/m4-q3-format/README.md` (added v1-era 19:08Z) — do not "fix" ordering by
   moving files; the pickaxe order is already correct.

**Item v2.b — the enumeration is DERIVED, so the note only has to be published.** From
`runs/m4-q2-dropword/signals.json` × the v2 holdout × `runs/m4-q2-adjudication/adjudication.jsonl`: 7 deferred
signals in 4 holdout transcripts — `Radical_Subjectivity_The_I_of_Self_Feb_2002_Part_2` ×4,
`Realization_of_the_Self_as_the_I_Nov_2003_Part_1` ×1, `Spiritual_Traps_Oct_2005_Part_2` ×1,
`Witnessing_and_Observing_Oct_2004_Part_1` ×1 — carrying hand labels **3 CERTAIN-leg-d** (`D-092`, `D-093`, `D-094`)
and **4 CANDIDATE** (`D-095`, `D-107`, `D-108`, `D-122`). §10 now emits a **landing check** row that flips to PASS
when the seal's own note names those transcripts, ids and verdicts; legs (ii)–(iv) of the item are unchanged, and
leg (iv) is the one that binds quantum b: per-file breakdown **or** exclusion, decided in the pre-registration.

**Caveat that must ride with every quantum-b figure:** all 33 holdout transcripts were read by the pre-seal v1-era
run (its keys are the v1 tuning 193, which contains the whole v2 holdout). This is disclosed by the seal itself and
is not a v2.6 violation, but the seal's sentence — *"a first figure under v2 is an estimate under this split, not a
pristine out-of-sample number"* — must be printed beside the number, exactly as the token rule must be printed
beside `8/122` (self-item O-1).

---

## ANNEX AMENDMENT §F — the four tainted holdout transcripts are LABEL-tainted, not fixture-adjacent (ORCH-2, 2026-09-25T23:58:12Z, append-only)

Gate cycle H derived the taint from the data instead of restating it, and the derivation **corrects the ANNEX's own
wording**. A4 called the four excluded transcripts "fixture-adjacent". They are not: the seal forces every
fixture-bearing transcript into TUNING, and §10 verifies the v2 holdout contains **zero** fixture transcripts. What
the four actually carry is **prior hand labels from the pre-seal TASK-018 adjudication**, which is a different and
stronger kind of prior knowledge. The correction is append-only; A4's numbers stand.

**F1 — the four are named and fixed NOW** (so the sensitivity denominator cannot be chosen after results exist):

| transcript | pre-seal q2 signals | prior TASK-018 verdicts |
|---|---|---|
| `Radical_Subjectivity_The_I_of_Self_Feb_2002_Part_2_enxautogen_html.txt` | 4 | `D-092` `D-093` `D-094` **CERTAIN-leg-d**, `D-095` CANDIDATE |
| `Realization_of_the_Self_as_the_I_Nov_2003_Part_1_enxautogen_html.txt` | 1 | `D-107` CANDIDATE |
| `Spiritual_Traps_Oct_2005_Part_2_enxautogen_html.txt` | 1 | `D-108` CANDIDATE |
| `Witnessing_and_Observing_Oct_2004_Part_1_enxautogen_html.txt` | 1 | `D-122` CANDIDATE |

**F2 — denominators, both pre-declared:** primary **33** (all holdout transcripts, with the per-file disposition of
these four visible), sensitivity **29 = 33 − 4** (the four above excluded). Both come from the **same single run**;
neither may be recomputed by a second execution, and no third denominator may appear. Every quoted figure carries its
denominator.

**F3 — the prior labels must be re-adjudicated BLIND, and the comparison published (new requirement, D3-bis).** For
those 7 signals the quantum-b adjudication is performed from the span bytes and the book quote under the frozen
leg-d rule **without reference to the prior verdicts**; the run then publishes a prior-vs-new table, one row per
signal, stating agree / disagree and the reason for any disagreement. Disagreements are **reported, never silently
reconciled**, and a disagreement is not evidence that either verdict is wrong — it is the measurement of what the
taint was worth. This converts a disclosure into a number.

**F4 — the seven are not discoveries.** They were signal-bearing before the seal, so they count in the denominator
but may not be presented as found by the quantum-b run; D4's per-file disposition states this in terms.

**F5 — no auto-promotion, per ERRATA-25e §2.** A detector hit never classifies itself: every holdout row adjudicated
CERTAIN-leg-d needs its own individual reason and citation, re-derivable byte-exact by the gate, and CANDIDATE rows
are never blended into a CERTAIN count. The 57 CERTAIN-leg-d rows from TASK-018 remain **restricted** and are not a
floor for the holdout figure.

**F6 — the two caveat sentences that must be printed beside every quantum-b figure:** (i) the seal's own —
*"v1 detectors were shaped with corpus-wide knowledge … a first figure under v2 is an estimate under this split, not
a pristine out-of-sample number"* — because all 33 holdout transcripts were read by the pre-seal v1-era run; and
(ii) the token rule for any drop-consistency number (apostrophes normalised, hyphens inside tokens), per self-item
O-1, since `8/122` and `114/8` and `67/55` are different rules over the same data.

**F7 — frozen-input drift is now machine-checked (AMENDED 2026-09-26T02:17:07Z).** §12 of the gate instrument compares the ANNEX
B1/B4 digests against the worker head every run: `det_dropword.py a0236325…`, `det_format.py ef9ff4f2…`,
`m5r_reduce.py a89ff189…` (**re-pinned by F8**; was `6d4bb9ce…`), ledger `d42136c6…`, policy manifest `0fe20a60…`,
corpus zip `3f36c520…`, book store `c0892fcd…`. **A drift on any of them voids the pre-registration and forces a new
one UNLESS all three of these hold, in which case the freeze stands on the amended pin: (i) the lane DISCLOSES the drift
in the artefact itself, naming the old and new digest and its effect on the outputs; (ii) the gate VERIFIES the drift is
behaviour-neutral by re-running the changed tool with the published pins and comparing output bytes; (iii) the gate
RE-PINS the value in this ANNEX before the bound run starts.** The rule exists to stop silent input changes; it is not a
tripwire on a disclosed, verified-neutral documentation change — but an undisclosed drift still voids, and a disclosed
drift that fails (ii) still voids. The split-v2 file digest is expected to change **once**, when item v2.a lands, and the
pre-registration must bind the post-note value (criterion v2.10).

**F8 — RE-PIN 2026-09-26T02:17:07Z, ORCH-2, at WORKER-2 `34db0b0`.** `tools/m5r_reduce.py` changed by +46 lines (TASK-020 item 13: the
manifest's `derivations` prose rewritten, plus a `derivations_revision` record). F7's three conditions: **(i)** the lane
discloses it inside the manifest — `derivations_revision` names the old blob `6d4bb9ce…` (at `tool_commit dada3e6…`), the
new blob, and `effect_on_run_outputs: none`; **(ii)** ORCH-2 verified neutrality by re-running the tool **at head** in the
gate worktree with the published pins (`--utc 2026-09-25T19:55:24Z`, `--tool-commit dada3e6…`, `--main-head 77f1d6de…`,
`--policy-sha 0fe20a60…`, `--book-store-sha c0892fcd…`, `--detector-tool-commit 7b8863d`): `ledger.jsonl`
`d42136c673188f9e…` **byte-identical**, `by_transcript_digest` `c1ec4da86a6ce4f4…` identical, 1334 findings, 242 ok / 0 bad
book refs, 0 citation failures, and the regenerated manifest differs from the committed one in `tool_sha256` alone;
**(iii)** the pin is re-pinned here and in the instrument's §12 tuple. **No other frozen value moved.** Two consequences
travel with the re-pin: TASK-013's M5-R PASS holds on the stronger ground of a re-run (self-correction **O-9**: the
byte-identity-of-the-tool row was a proxy), and **TASK-020 item 13b** is opened — the artefact's `reproducibility_note`
must state that byte-identity of the ledger depends on passing the **original** `--tool-commit`, since every row embeds it
in `status_by` (omitting it moves the digest to `c94cce40…` with all 1334 rows otherwise identical). Quantum b's freeze
therefore STANDS on the amended pin; the blocker is unchanged (§G2, the §H sentence, v2.a(iii)-2nd-half, v2.g's four
untested refusals, v2.c/v2.d/v2.e/v2.h).

**Unchanged:** quantum b may not run until v2.a lands (v2.7 requires frozen inputs); the pre-registration commit must
exist before the run commit (v2.12); exactly one execution, no re-run for any reason (C2); nothing added to the eval
directory afterwards except the receipt and an errata (v2.14).


---

## Gate cycle I at WORKER-2 `72104a5` (ORCH-2, 2026-09-26T00:52:53Z) — **the v2 seal STANDS**; items v2.c–v2.f opened; A1 amended (O-5)

**Quantum a re-gated on the worker's own audit material: the seal is VALID and its holdout is NOT void.** ORCH-2 did not
accept the self-audit; instrument §18 recomputed all 16 of its claims from git bytes — **13 verified, 3 mismatched, every
mismatch documentation-class** (full table in `GATES.md`, "GATE CYCLE I"):

* the seal file is **byte-identical** since `79eb401` (`73d86f0dafe5…`);
* **6 of the 7 digests the seal binds recompute MATCH at head** — corpus list `9ae90185…`, `confirmed.json` `f2c15869…`,
  zip `3f36c520…`, policy `0fe20a60…`, split tool `fe043aee…`, book store `c0892fcd…` (**whose file the seal never names**;
  identified from `tools/census.py`'s `book_store_bytes` = 14,634,979 as
  `corpus/docdocgo/html/merged-book-texts_json_1.js`, confirmed by digest);
* the fixture move `c8e96319… → c40d272f…` is **append-only**: 0 keys changed, 0 removed, 63 added, ids
  `{D2-001..D2-004}` identical, moving commit `a5dec38` @ `2026-09-25T21:21:03Z` (post-seal);
* the confirmation artefact `61568a9e…` has a **single-commit history** `1fb524e` @ `20:38:18Z` = **13m36s PRE-seal**, which
  is the fact that decides the `re_seal_rule`;
* membership 197 / 33 / 43 with `forced ∩ holdout = ∅`, and the draw reproduces set-equal at head;
* the audit tool opens **no transcript bytes**, its digest equals its own report's stamp, and `head_commit_at_audit`
  (`14255bd`) is an ancestor of the report's commit.

**Verdicts moved:** criterion **v2.5 → PASS** and **v2.10 → PASS** on the amended (seal-time-binding) reading below.
**Item v2.a: PARTIALLY LANDED** — clauses (i) substance and (ii) landed and verified; clause (iii) **half-landed**.
**Item v2.b: UNLANDED.** **Quantum b remains blocked.**

### Self-correction O-5 — ANNEX A1 amended (append-only; the original stays readable above)

A1 as written demanded that `HELD-OUT-SPLIT-V2.json`'s **own header** bind `c40d272f…`. That is **unsatisfiable**: any edit
moves the seal's own digest `73d86f0d…`, which the worker's appendix quotes and which criterion v2.10 requires to recompute
MATCH. A criterion that requires editing an immutable artefact is a defective criterion, so it is amended in the open:

* **A1 (amended).** The seal stays **byte-identical**; the dated note lives in a **companion artefact** naming both digests,
  the moving commit, the append-only classification and the `re_seal_rule` evaluation; and **the quantum-b `freeze` must bind
  the companion artefact's sha256 alongside the seal's**, so the run cannot proceed on the seal alone. *Not yet done — that
  row FAILs and is the concrete ask.*
* **v2.5 (amended).** The seal binds its **seal-time** digest; a post-seal move is discharged by a blob-level classification
  plus a companion note naming both digests.
* **v2.10 (amended).** Every bound digest recomputes MATCH **at its binding time**; a post-binding append-only move must be
  classified from both blobs and carry the appendix.
* **The blocker** no longer rests on the seal's validity. It names four conditions — see below.

### Items opened this cycle (all documentation/provenance class; none touches the substance)

* **v2.c** — `SEAL-AUDIT.json.audit_utc` = `2026-09-26T00:45:00Z` is **forward-stamped ~13 min** past the head it audited
  (`14255bd`, `00:31:39Z`) and its own committing commit (`72104a5`, `00:32:03Z`), and the appendix's Provenance table cites
  **a different day and time** (`2026-09-25T21:44:00Z`) for the same artefact. Both are `:00`-rounded. Repair: one exact stamp
  from `date -u` at run time, cited identically in both files. *(ORCH-2's own O-4 class, found in a worker artefact.)*
* **v2.d** — the report names `tool` + `tool_sha256` but **no `tool_commit`**: item **8a**'s exact class (criterion 20.10,
  TASK-021 21.6). Derivable (`b991f29`) is not stated. Repair: add `tool_commit`, and the tool blob at that commit must equal
  the tool at head.
* **v2.e** — `confirmation_artifacts` carries **5 byte-identical rows with no citing path**, while `fixtures/v2/dropword.json`
  mentions that artefact at **10 paths**; the tool's key (*a dict carrying both `artifact` and `artifact_sha256`*, 5 pairs) is
  **never named**, so the appendix's *"All five citations in the fixture file"* does not reproduce. **Load-bearing:** the 5
  **unpaired** mentions — including `/adjudication_summary_2026_09_25/artifact` — are **outside the tool's post-seal void
  check**, so a post-seal confirmation cited without a paired sha would not fire it. ORCH-2 closed the gap by hand (all 10
  name the same pre-seal artefact). Repair: name the key, and widen the census to every mention — or state the exclusion and
  check the remainder by hand, in the report.
* **v2.f** — `WORKER-2-TASK-019b-PREP.md`'s header `2026-09-25T21:5xZ` is **fuzzy** and ~2.6 h before its own commit
  (`00:31:39Z` on 09-26): item **12**'s class, taking the census from **26 → 27**. Repair per item 12's order.
* **v2.a (iii), 2nd half** — nothing states that `79eb401` changed **only** the `manifest` key, so `293b29c`/`79eb401` are
  **one draw, not two** (0 occurrences of `293b29c` or "one draw" in any new artefact). Repair: state it and make it
  checkable — compare the two blobs of the seal file.

### Quantum b: the four conditions that actually remain

1. **item v2.b** — the taint disclosure (four holdout transcripts, seven signal ids + verdicts, the deferred-filter
   endorsement, and the denominator choice: **33 primary with per-file disclosure + 29 as a pre-registered sensitivity**).
2. **item v2.a clause (iii), 2nd half** — the "one draw, not two" statement.
3. **O-5's freeze binding** — `freeze` must bind the companion note's digest alongside the seal's.
4. **ANNEX A2** — either TASK-018 items **0d–0g** land, or the adjudication set is explicitly excluded from the quantum-b
   eval, recorded in the pre-registration. *(This one is ORCH-2's to decide if 0d–0g stay open; it is not worker work.)*

**Harness status (verified as capability evidence, not as a run):** 8 distinct `REFUSED:` paths covering all five
run-refusals plus the score refusals; `holdout_consumed` and `attempt 1 / max_attempts 1` enforced in `verify`; `freeze`
requires `--utc --tool-commit --main-head --policy-sha`; `module_sha256` bound at freeze and refused-on-change at run; label
keys detector-qualified (`"%s/%s#%d"`); `c2_detectors.py` reads its frozen parameters **from the detector modules**, so the
freeze cannot drift from the 8/8 operating point §17 pinned; **0** tuning-side evaluation paths in either new tool.
**The v2 holdout has not been opened.** Criteria v2.12–v2.16 stay HELD for the run.

**Suite:** `Ran 244 tests in 205.498s` → `OK (skipped=1)` at `72104a5` (= 227 + 10 harness + 7 audit), corpus present, no
test dropped. At `4fc40c8`: `Ran 227 tests` → `OK (skipped=1)`.


---

## ANNEX §G — the A2 decision, recorded BEFORE any run (ORCH-2, 2026-09-26T01:00:20Z, BINDING)

**A2 asked:** either TASK-018 items 0d–0g land, **or** the adjudication set is explicitly excluded from the quantum-b eval —
*"the decision is recorded in the pre-registration, not made afterwards."* This is that record. It is made at WORKER-2 head
`72104a5`, with the v2 holdout unopened and **no freeze written**, so nothing in it can have been chosen with an answer in
hand.

**DECISION: the v1-era adjudication set is EXCLUDED from the quantum-b evaluation.**

What that binds, concretely:

1. **No label, denominator or sanity figure** may be taken from `runs/m4-q2-adjudication/adjudication.jsonl` (122 rows), from
   any verdict in `fixtures/confirmed/confirmed.json` or `fixtures/v2/dropword.json`, or from any count in
   `tools/PATTERNS.md`. The evaluation starts from the holdout's own signals.
2. **Holdout signals are labelled fresh and blind for the run** (the §F `D3-bis` discipline): the label file is written
   before scoring, committed, and carries a reason per label — "the cited bytes read" — which the harness already refuses to
   score without.
3. **`seeded` stays separated from `independent`** and never counts toward the rate (criterion v2.15; the harness's `score`
   enforces it), and unlabelled signals stay `candidate_unlabelled`, never blended into any figure.
4. **Lifting rule.** If items 0d–0g land **before the freeze**, the exclusion is **not** lifted automatically: lifting
   requires an amendment to this annex before the freeze, with the reason stated. After the freeze nothing here changes,
   because the freeze carries the protocol text into the score file.

**Why.** 0d–0g are open defects in exactly the artefacts a label-reuse path would read: a false "seeded" sentence in
`PATTERNS.md §5b-bis` (**0d**); an unnamed dedupe key that makes 57 rows into 55 distinct spans (**0e**); a missing per-word
class list plus two unrecorded rulings (**0f**); and no append-only disposition field on the 122 rows, with the 7 v2-holdout
rows unmarked (**0g**). Importing any of them into a **one-shot** figure would put a known-defective input into a measurement
that cannot be re-run. The exclusion costs nothing measurable: the 33 v2-holdout transcripts have never been adjudicated, so
fresh labels are required on **either** branch of A2.

**Consequence for the figure.** Quantum b's precision is over **fresh holdout labels only**, published with its label
coverage (`labelled/total`) and with the §F disclosure framing — *"an estimate under this split, not a pristine out-of-sample
number."* **A2 is closed.** The blocker's remaining conditions are item **v2.b**, item **v2.a clause (iii) 2nd half**, and the
freeze binding in §G2.

### §G2 — the freeze binding O-5 asks for (field spec, so the repair is one diff)

`freeze` must write into `THRESHOLDS.json` a `companion_notes` list binding every dated note that adjudicates the seal:

```
"companion_notes": [
  {"path": "runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md",
    "sha256": "<live sha256>", "commit": "<the commit that added it>", "commit_utc": "<exact, from date -u>"},
  {"path": "runs/m4-q2-adjudication/SEAL-AUDIT.json",
    "sha256": "…", "commit": "…", "commit_utc": "…"}
]
```

and `run` must **refuse** when a bound companion note's live digest no longer matches — the same refusal shape it already
raises for a changed detector or a changed split. Rationale: the seal file stays byte-identical (O-5), so the disclosure that
makes the seal readable lives **beside** it, and the run must not be able to proceed on the seal alone.

### §G3 — the "one draw, not two" substance, verified by ORCH-2 (so item v2.a(iii) is documentation-only)

Comparing the seal's blobs at `293b29c` and `79eb401` directly: **`manifest` is the only key that differs** — `holdout`,
`tuning` and `salt` are identical, no key was added or removed, and the two commits are **68 s apart**
(`20:50:46Z` → `20:51:54Z`). So the split was drawn **once**, and `79eb401` re-manifested it (binding `tool_sha256` to the
tool's head revision, "no staleness"). What item v2.a(iii) still owes is the **sentence** — and the reason it matters is that
`79eb401`'s own commit subject says **"re-seal"**, which reads as a second draw to anyone who has not compared the blobs.
Instrument §18 now derives this comparison mechanically, so the claim stays checkable rather than trusted.


### Item v2.g (ORCH-2, 2026-09-26T01:04:16Z) — two of the harness's nine refusal paths have no test, and one of them protects the denominator

§18 maps every refusal in `tools/m4_one_shot_v2.py` to the `assertIn` that covers it in `tests/test_m4_one_shot_v2.py`.
**7 of 9 are asserted.** The two that are not:

| untested refusal | why it matters |
|---|---|
| `REFUSED: %s evaluated %d transcripts, not the frozen holdout set of %d — refusing to score a partial read` | **the load-bearing one.** A partial holdout read must be refused, not scored: quantum b is one-shot, so a silently smaller denominator could never be re-run. This is the refusal that makes the receipt's read list meaningful |
| `REFUSED: %s parameters changed after the freeze` | the file-digest branch is tested (`changed after the freeze`), but that assertion is **ambiguous** between the two branches; the parameters branch is credited only if a test asserts something containing `parameters`, and none does |

**Repair (two toy tests, no corpus):** (i) freeze a toy split whose holdout has 2 transcripts and make the detector read 1 →
expect `SystemExit` naming the partial-read rule; (ii) freeze, then edit the **freeze record's** params without touching the
module file → expect `SystemExit` naming the parameters rule.

**Verified alongside it, because the partial-read refusal is only usable if it cannot fire spuriously:** both detectors
assign `per_file[n] = sigs` **unconditionally** inside the read loop (`det_dropword`, `det_format`), so a **zero-signal**
holdout transcript still counts as read — C1-drop may legitimately find nothing in some of the 33, and the run must still see
33 reads. And both detectors write `holdout_reads` / `holdout_consumed` **themselves** in holdout mode, so the receipt's read
list is not reconstructed after the fact (criterion v2.12's precedent; the run-level test stays HELD).

**Timing:** v2.g is **not** one of the three blocker conditions — the harness has not been run — but it must close **before
the freeze**, because a refusal nobody has tested is a refusal nobody can rely on.

---

## GATE CYCLE J at WORKER-2 `1c8a287` (ORCH-2, 2026-09-26T01:54:33Z · `date -u` at write time; the commit carrying this line is the source of record)

**Item v2.b CLOSED — all four legs, verified in `tools/HELD-OUT-SPLIT-V2-NOTE-2026-09-26.md`.** The four v2-holdout
transcripts are named with their seven signals, base verdicts **and** post-0d–0g verdicts; the shipped filter's deliberate
deferral is recorded with ORCH-2's endorsement; **who has read these bytes** is stated (WORKER-2 in TASK-018 adjudication;
ORCH-2's gate re-derived all 122 spans and labels that **gate re-derivation, not tuning**, with no rule/threshold/filter
changed as a result); and the standing caveat travels in the seal's own words. This is the shape O-5 amended A1 to require —
a dated note **beside** an immutable seal — and it is the first artefact in the campaign that records read-access to holdout
bytes from the gate side.

**Item v2.a CLOSED on clauses (i), (ii) and the first half of (iii).** Both digests are bound (`c8e96319…` seal-time,
`c40d272f…` at head), the moving commit is named (`a5dec38`, 2026-09-25T21:21:03Z), the classification is reproducible
(seal-time blob `fbee23ef…` recovered and diffed: new keys only, `mutations` empty, no fixture id added, the confirmation
artefact `61568a9e…` is commit `1fb524e` at 20:38:18Z — **13 min pre-seal**), membership holds (43 ∩ 33 = ∅, `verify`
passes), and the re_seal_rule is evaluated: **the seal stands, no new salt is owed**. The defect is also stated for the
record (a seal-time digest over an append-only file fires on benign edits) with the forward-looking fix.

**Item v2.a clause (iii), second half — STILL OWED, and ORCH-2 discloses its own defect #38.** No companion artefact states
that `293b29c` → `79eb401` is **one draw, not two**. ORCH-2's first row credited a *mention* of `293b29c` and reported PASS;
the only mention is `WORKER-2-TASK-019a-DELIVERY.md:26` — `run_utc 2026-09-25T20:50:46Z (src 293b29c; read 20:5xZ)` — a
timestamp's source citation, not the statement. The row now requires **both** seal commits in one artefact **with** a
one-draw phrase (`one draw` / `same draw` / `manifest-only` / `not a second draw`). ORCH-2 has verified the substance from the
two blobs (they differ in `manifest` only; holdout, tuning and salt identical; 68 s apart), so the owed repair is one
sentence — but it is owed **beside the seal**, because `79eb401`'s own subject says "re-seal" and reads as a second draw to
anyone who has not compared blobs.

**Item v2.f CLOSED.** `fleet/branches/WORKER-2-TASK-019b-PREP.md`'s header now reads
`2026-09-26T00:32:03Z (src 72104a5; read `21:5xZ`)` — exact, sourced, and ORCH-2 verified `00:32:03Z` **is** `72104a5`'s
committer time. The superseded fuzzy value stays readable, which is the repair pattern item 12 requires.

### ITEM v2.h — OPEN (new, criterion 20.14c): the seal note and the regenerated audit are forward-stamped

| artefact | own-time stamp | commit carrying it | offset |
|---|---|---|---|
| `tools/HELD-OUT-SPLIT-V2-NOTE-2026-09-26.md` | `2026-09-26T01:14:30Z` ("the lane clock stamp of CONTROL seq 43") | `c5b5b25` @ `2026-09-26T00:41:22Z` | **+33.1 min** |
| `tools/HELD-OUT-SPLIT-V2-EXCLUSIONS.json` | `written_utc 2026-09-26T01:14:30Z` | `c5b5b25` @ `00:41:22Z` | **+33.1 min** |
| `runs/m4-q2-adjudication/SEAL-AUDIT.json` (regenerated) | `audit_utc 2026-09-26T01:22:00Z` | `c5b5b25` @ `00:41:22Z` | **+40.6 min** |

The note's stamp is additionally **mis-attributed**: it names CONTROL seq 43 and commit `7d14685`, whose committer time is
`00:39:44Z`, not `01:14:30Z`. This is item v2.c's class repeated in the newest bytes — and v2.c itself is unchanged (the
appendix still cites `audit_utc 2026-09-25T21:44:00Z` while the regenerated report says `2026-09-26T01:22:00Z`, so two
committed artefacts contradict each other about the same field). Repair as TASK-018 item 0h: re-derive from the introducing
commit, append the correction, and make the tool read the clock instead of accepting a projected one.

**Items v2.c, v2.d, v2.e remain OPEN.** They were cut while ORCH-2's lane was unpushable (the GitHub auth outage,
~00:20Z–01:19Z) and were therefore invisible to WORKER-2 when this delivery was made — no defiance, and the regeneration of
`SEAL-AUDIT.json` repeated v2.c rather than repairing it: `tool_commit` is still **absent** (v2.d), and the citation census
is still **5 rows over 1 distinct artefact with no named key** (v2.e — item 0e's lesson: say whether the count is rows,
pairs or distinct artefacts, and cover all 10 mentions).

**Item v2.g — the refusal surface grew from 9 to 12; 8/12 are asserted by a test.** The two pre-registered-exclusion
refusals landed with the exclusions themselves, and one of them is tested
(`test_exclusions_changed_after_the_freeze_are_refused`). **Four remain unasserted:** the detector-**parameters**-changed
branch, the evaluated-set ≠ frozen-holdout (**partial read**) refusal, the exclusions-**not-holdout-members** refusal, and
the score-side partial-read refusal. The middle two protect quantum b's **denominator**: a partial or wrongly-scoped holdout
read must be refused, not scored, because the figure is one-shot. Four toy tests, no corpus. Still required **before the
freeze**; still not a fourth blocker.

## ANNEX §H — A4 AMENDED (append-only): the quantum-b denominator, ruled before any result

WORKER-2's note decides, **before the run**, that the four label-tainted transcripts are **excluded** from quantum b's
reported denominator: **29 of 33 evaluated**, machine-readable in `tools/HELD-OUT-SPLIT-V2-EXCLUSIONS.json`, bound into the
freeze by digest (`holdout_exclusions_file` + `holdout_exclusions_sha256` + `holdout_exclusions`), enforced in
`tools/m4_one_shot_v2.py` (run evaluates exactly `holdout − exclusions`; refuses exclusions that are not holdout members;
the receipt lists evaluated and excluded separately) and covered by two tests.

**ORCH-2 ADOPTS the swap and amends A4 accordingly.** Verified preconditions: **no result existed** when it was recorded (no
receipt, score, threshold record or quantum-b output at this head — which is what makes a denominator change legitimate
rather than post-hoc); all four excluded transcripts **are** holdout members; `29 = 33 − 4`; the rationale is §F2's own
ground (D-093/D-094 are CERTAIN rows whose spans the campaign has read and annotated, so those transcripts are not unseen
material for the rule that produced them).

**A4 as amended (both numbers still fixed before the run, roles swapped):**

> Quantum b reports **PRIMARY precision over the 29 evaluated holdout transcripts**, with the four excluded transcripts
> named, **AND a pre-registered SENSITIVITY figure over all 33 from the same run** — no second spend, because the four were
> already read — with the four named in that figure too. The sensitivity figure shows the effect of the exclusion; it is
> **not** a certification figure, and the primary remains 29. Neither number may be chosen, dropped or re-scoped after the
> run.

**Owed to close §H:** one sentence in the note or the exclusions file committing to the 33-transcript sensitivity figure as
above. The note currently forbids the excluded four from re-entering *any* denominator, which reads as excluding the
sensitivity too; §H requires it as a **secondary, pre-registered** figure.

**Quantum-b blockers after cycle J (unchanged in number, precise in content):** §G2 (the freeze must bind the companion
notes' digests alongside the seal's — still zero mentions of any companion in `m4_one_shot_v2.py`), §H's sentence,
v2.a(iii) second half, v2.g's four untested refusals, and the v2.c/v2.d/v2.e/v2.h hygiene set. TASK-015 (M6 FINAL) stays
BLOCKED behind quantum b.
