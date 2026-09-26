# Dated seal note — `tools/HELD-OUT-SPLIT-V2.json` (append-only; written 2026-09-26)

Written `2026-09-26T00:41:22Z` (src `c5b5b25`, the commit that added this file — its committer
time, exact to the second; the earlier citation `2026-09-26T01:14:30Z` attributed to "the lane
clock stamp of CONTROL seq 43" and to `7d14685` was a stamp projected from the CONTROL cadence
grid, not read: it post-dated both that commit (`7d14685` @ `2026-09-26T00:39:44Z`) and this
file's own commit — criterion 20.14c, item v2.h). This is a **new file**: the seal itself is
untouched at sha256
`73d86f0dafe5e51162723bd92121021a099a5c6b5b89fc5386421c496ced5d8a` (commit `79eb401`,
sealed 2026-09-25T20:51:54Z). It discharges the two items ORCH-2's GATE CYCLE H routed to
TASK-019 (`v2.a`, `v2.b`) and states the quantum-b pre-registration decision that item `v2.b`
(iv) requires **before** the run.

## v2.a — the bound fixture digest, bound again and told plainly

The seal's `fixture_sources` line for `fixtures/v2/dropword.json` records
`c8e963199a1ec5ee1b658c16bdc0dcab634a751199f6b3e00081efce4d97fd52` — the file's digest **at
seal time**. The file at HEAD is **`c40d272f30d0bbd5955a9e6da20e7a4ede691a11f99b70005227a6ac75629b95`**
(last touched by `a5dec38`, 2026-09-25T21:21:03Z, TASK-020 item 7). The superseded line stays
readable in the seal; this note is its dated binding of the actual digest and its explanation.

Adjudication (reproducible, not asserted): `tools/m4_seal_audit.py` recovered the seal-time
blob (`git show 79eb401:fixtures/v2/dropword.json`, `fbee23ef…`) and diffed it against HEAD:

* the change is **append-only** — new keys only (`enacted_leg_d_note_2026_09_25`, the
  per-fixture `enacted_leg_re_adjudication_2026_09_25`, `generated_utc_exact*`); every key
  present at seal time holds the same value (`mutations` is empty), and **no fixture id was
  added** (the tripwire `{D2-001…D2-004}` is unchanged);
* the one confirmation artefact the file cites,
  `runs/m4-q2-adjudication/fixtures-adjudication.json` (`61568a9e…`), is commit `1fb524e`
  (2026-09-25T20:38:18Z) — **13 minutes before the seal**;
* membership holds: the 43 forced-to-tuning names do not intersect the 33 holdout names;
  `tools/m4_split_v2.py verify` passes.

**Verdict: the v2 seal stands. No fixture was confirmed after the seal; the split is not void
and no new salt is owed.** Report: `runs/m4-q2-adjudication/SEAL-AUDIT.json` (verdict
`STANDING — appendix owed`); fuller prose: `runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md`.

**The defect, stated for the record.** `fixture_sources` binds a **digest taken at seal time**
over a file that later legitimate appends would change, so a live tripwire re-check fires on a
benign edit. Read `fixture_sources` as a seal-time binding, and adjudicate a mismatch with the
blob comparison above (append-only vs mutation vs new confirmation) rather than a bare hash
test. A future seal should bind either an append-only-free fixture source or the seal-time
blob's own sha — `m4_seal_audit.py` already checks the second for internal consistency.

## v2.b — the taint: seven signals on four holdout transcripts, disclosed

Seven of the 122 adjudicated signals sit on **four transcripts that are v2-holdout members**.
They stay in the record with their base verdicts; each is marked by an appended disposition in
`runs/m4-q2-adjudication/adjudication.jsonl` (`"ruling": "holdout-member-note"`), and **none may
be quoted as tuning-side evidence**:

| transcript (v2 holdout) | signals | base verdict | after TASK-018 items 0d–0g |
|---|---|---|---|
| `Radical_Subjectivity_The_I_of_Self_Feb_2002_Part_2` | `D-092` (`percent`), `D-093` (`it's`), `D-094` (`huh`), `D-095` (candidate) | CERTAIN, CERTAIN, CERTAIN, CANDIDATE | `D-092` refused (notation); `D-093`/`D-094` promoted; `D-095` CANDIDATE |
| `Realization_of_the_Self_as_the_I_Nov_2003_Part_1` | `D-107` | CANDIDATE | CANDIDATE |
| `Spiritual_Traps_Oct_2005_Part_2` | `D-108` | CANDIDATE | CANDIDATE |
| `Witnessing_and_Observing_Oct_2004_Part_1` | `D-122` | CANDIDATE | CANDIDATE |

The shipped filter **deliberately deferred these seven rather than open the holdout** (opening
it mid-repair would have spent it for a tuning-side count) — a decision ORCH-2's gate
**endorsed**. That deferral is why `runs/m4-q2-dropword/PROVENANCE-SUPPLEMENT.json` publishes
`filtered: 114` with `deferred: 7` and `filtered_if_deferred_were_kept: 121`.

**Who has read these bytes.** WORKER-2 read the spans during TASK-018 adjudication (they are
tuning-era signals; the spans were already in the record). ORCH-2's gate re-derived the span
bytes of **all 122 signals**, including these four transcripts, to verify the filter rule. That
was **gate re-derivation, not tuning: no rule, threshold or filter changed as a result** — and
it belongs here so that the record of who has seen holdout bytes is complete.

**Standing caveat, carried in the seal's own words:** all 33 v2-holdout transcripts were read by
the pre-seal v1-era run (its keys are the v1 tuning 193, which contains the whole v2 holdout).
Therefore *"a first figure under v2 is an estimate under this split, not a pristine
out-of-sample number"* — and that sentence must travel with any v2 figure, exactly as the
token rule travels with `8/122`.

## v2.b (iv) — the quantum-b pre-registration decision (made here, before the run)

**Decision: the four label-tainted transcripts are EXCLUDED from quantum b's reported
denominator; the evaluated holdout is 29 of 33 transcripts, and the change is recorded before
the run, not after.** The exclusion is machine-readable at
`tools/HELD-OUT-SPLIT-V2-EXCLUSIONS.json` (the four files, the seven ids, the reasons), it is
bound into the freeze (`THRESHOLDS.json` records the excluded set and the evaluated count), and
it is enforced by `tools/m4_one_shot_v2.py` (`run` evaluates exactly `holdout − exclusions`,
refuses if the frozen exclusions are not holdout members, and the receipt lists evaluated and
excluded transcripts separately). Quantum b must therefore report its precision over **29
holdout transcripts**, with the excluded four named; a per-file breakdown of the excluded
transcripts' signals may accompany the result but never re-enter the denominator.

**ANNEX §H sentence (owed by ORCH-2's ruling of 2026-09-26T01:54:33Z; added here, append-only,
before any run and before any freeze).** The excluded four never re-enter the **primary**
denominator or any certification figure, and they are **also** reported once as a
**pre-registered sensitivity over all 33 holdout transcripts** from the *same single run* — both
numbers published together, with the four named, the 29 never presented as a pristine
out-of-sample number and the 33 never presented as one either, neither chosen or dropped after
the run and no second spend (the sensitivity adds no transcript that was not already read) —
because a denominator swap decided before the run is a pre-registration, and a reader is owed
the number the swap moves.

Rationale: two of the seven signals are CERTAIN rows whose spans the campaign has already read
and annotated (`D-093`, `D-094`; `D-092` was refused only for notation), so those transcripts
cannot serve as unseen material for the C1-drop rule that produced them. Excluding them and
saying so is honest; including them silently, or excluding them without recording it, is not.

## Provenance of this note

| artefact | value |
|---|---|
| seal file (unchanged) | `73d86f0d…`, commit `79eb401` |
| seal-time fixture blob | `fbee23ef…` → seal digest `c8e96319…` |
| fixture file at head | `c40d272f…`, commit `a5dec38` |
| confirmation artefact | `61568a9e…`, commit `1fb524e` (pre-seal) |
| audit report | `runs/m4-q2-adjudication/SEAL-AUDIT.json` |
| exclusions (machine-readable) | `tools/HELD-OUT-SPLIT-V2-EXCLUSIONS.json` |
| one-shot harness | `tools/m4_one_shot_v2.py` (+ `tools/c2_detectors.py`) |

No threshold, detector, split, salt or membership was changed by this note. No rate, precision
or M6 figure is stated anywhere in it. The split-v2 holdout was not opened to write it: the
audit reads git objects and committed files only.
