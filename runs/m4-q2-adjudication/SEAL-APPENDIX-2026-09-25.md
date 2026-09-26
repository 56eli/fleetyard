# SEAL APPENDIX — split v2, fixture-file digest (append-only; new file, 2026-09-25)

This is the appendix the seal rule owes. It is a **new file**: no committed artefact was
edited to produce it, and `tools/HELD-OUT-SPLIT-V2.json` remains byte-identical at
sha256 `73d86f0dafe5e51162723bd92121021a099a5c6b5b89fc5386421c496ced5d8a`
(commit `79eb401`, sealed 2026-09-25T20:51:54+00:00).

## The finding

The seal records, as the digest of its second fixture source
(`fixture_sources` in the seal file):

| | sha256 | commit | utc |
|---|---|---|---|
| `fixtures/v2/dropword.json` **at seal time** (blob `79eb401:fixtures/v2/dropword.json`, `fbee23ef…`) | `c8e963199a1ec5ee1b658c16bdc0dcab634a751199f6b3e00081efce4d97fd52` | `79eb401` | 2026-09-25T20:51:54Z |
| `fixtures/v2/dropword.json` **at HEAD** | `c40d272f30d0bbd5955a9e6da20e7a4ede691a11f99b70005227a6ac75629b95` | `a5dec38` | 2026-09-25T21:21:03Z |
| `fixtures/confirmed/confirmed.json` | `f2c15869d6cfc3529246a114bbc72a7c86a6c5d4b6d70968af22412b5ac61582` | `b2e0761` (pre-seal) | unchanged |

The v2 seal's own rule reads: *"if any fixture is confirmed after this seal, the split is
VOID and must be re-sealed with a new salt + a dated record; never silently reused, never
patched."* The digest move above therefore had to be adjudicated rather than left implicit.

## The adjudication (mechanical, reproducible)

`tools/m4_seal_audit.py` re-derives the answer from git bytes, not from prose. For each
fixture source it recovers the seal-time blob (`git show <seal-commit>:<file>`), diffs it
against HEAD, and classifies the change. Report: `runs/m4-q2-adjudication/SEAL-AUDIT.json`
(verdict at the time of writing: **STANDING — appendix owed**). The result:

* **No fixture was added after the seal.** The fixture id set is `{D2-001…D2-004}` at seal
  time and at HEAD; no `fixtures[]` entry was appended (this is the check that would have
  fired on a post-seal confirmation).
* **No sealed value was mutated.** The diff between seal-time and HEAD blobs contains only
  *additions* (the TASK-020 item-7 `enacted_leg_d_note_2026_09_25` block, the
  `generated_utc_exact*` keys, and per-fixture `enacted_leg_re_adjudication_2026_09_25`
  blocks). Every key present at seal time holds the same value at HEAD — the audit's
  `mutations` list is empty.
* **The one confirmation artefact is pre-seal.** All five citations in the fixture file
  point at `runs/m4-q2-adjudication/fixtures-adjudication.json`, sha
  `61568a9ede89d700d00a40a47d79ca7ab50834cc3358ebfbaa1bccd339ba3451`, whose content — and
  whole history — is commit `1fb524e` (2026-09-25T20:38:18Z), **13 minutes before** the
  seal commit `79eb401`. The adjudication that confirmed D2-001/D2-003 and refused
  D2-002/D2-004 was thus complete before the seal; the later edit only recorded it.
* **Membership holds.** `fixture_transcripts_forced_tuning` (43 names) does not intersect
  the holdout (33 names); `tools/m4_split_v2.py verify` passes, including the check that
  the forced set still equals the fixture files on disk + the spent v1 holdout.

Verdict: **the v2 seal STANDS.** No fixture was confirmed after the seal; the split-v2
holdout is not void; no new salt is owed. The rule was written for confirmations, and a
confirmation is a dated act (`1fb524e`), not a file digest — which is exactly why the audit
places the confirmation artefact in time rather than comparing digests alone.

## The defect, stated plainly

`fixture_sources` recorded a **digest at seal time that any later append to the same file
invalidates**, and TASK-020 item 7 (append-only by design) did exactly that — so a live,
tripwire-style re-check of the seal digest would now fire on a benign append and could be
mistaken for a confirmation after the seal. Two consequences, recorded rather than fixed
(no committed artefact may be edited):

1. **Read `fixture_sources` as a seal-time binding, not as a standing tripwire.** A digest
   mismatch means "compare blobs", and `tools/m4_seal_audit.py` does that comparison. The
   distinction it draws — append-only vs mutation vs new confirmation — is the load-bearing
   one.
2. **Future seals should bind fixture sources that are not also append-only annotation
   targets**, or bind the seal-time blob's own sha (the audit's internal-consistency check
   already compares these two numbers, so a future seal can catch this at build time).

Same failure mode as the defect already recorded for `tools/m4_q2_evidence.py` re-pins: a
digest-staleness class, not a substance change. It is named here so the 019b receipt carries
a crisp answer to "was the split touched after the seal?".

## Provenance

| artefact | sha256 / ref |
|---|---|
| `tools/m4_seal_audit.py` | tool digest stamped in the report (`tool_sha256`) |
| `runs/m4-q2-adjudication/SEAL-AUDIT.json` | see the file (audit utc `2026-09-25T21:44:00Z`) |
| seal file (unchanged) | `73d86f0d…`, commit `79eb401` |
| re-seal rule | quoted in this file from `tools/HELD-OUT-SPLIT-V2.json:re_seal_rule` |

No threshold, detector, split, salt, membership or fixture verdict was changed by this
appendix. No rate, precision or M6 figure is stated. The split-v2 holdout was **not** opened:
the audit reads git objects and committed files only.
