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
