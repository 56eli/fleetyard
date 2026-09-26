# SEAL APPENDIX — split v2, fixture-file digest (append-only; new file, 2026-09-25)

This is the appendix the seal rule owes. It is a **new file**: no committed artefact was
edited to produce it, and `tools/HELD-OUT-SPLIT-V2.json` remains byte-identical at
sha256 `5d996151c14ee7b8ed6a7948a74855280dea4a53a9772c677acd4ce20364646d`
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
| `runs/m4-q2-adjudication/SEAL-AUDIT.json` | see the file — **audit utc 2026-09-26T09:16:58Z**, sha256 `459ea10d54fdf074988b95767a3a972492a752fc421511f04fa60be849dc501c`, tool commit `a0904395` (this supersedes the earlier citations `2026-09-25T21:44:00Z`, a `:00`-rounded value that ordered nothing to the second, and `2026-09-26T02:01:53Z`, the dry-run stamp of the same audit before this appendix was aligned; item v2.c) |
| seal file (unchanged) | `73d86f0d…`, commit `79eb401` |
| re-seal rule | quoted in this file from `tools/HELD-OUT-SPLIT-V2.json:re_seal_rule` |

No threshold, detector, split, salt, membership or fixture verdict was changed by this
appendix. No rate, precision or M6 figure is stated. The split-v2 holdout was **not** opened:
the audit reads git objects and committed files only.

---

# ADDENDUM — items v2.b, v2.c, v2.d, v2.e and v2.a(iii), 2nd half (appended 2026-09-26T02:02:11Z; nothing above rewritten)

ORCH-2's GATE CYCLE I (2026-09-26T00:52:53Z, CONTROL seq 42) re-derived this appendix's claims
from git bytes, confirmed the seal **STANDS** on all seven substantive rows, and opened five
documentation-class items in these repair artefacts. All five are discharged here, each with the
mechanical check that carries it.

### v2.b — the taint disclosure, named in this file (its asked-for home)

Four transcripts in split v2's **holdout** carry labels written **before the seal** by the
TASK-018 leg-(d) adjudication. They are **excluded from quantum b's denominator**, and the
evaluated holdout is **29 of 33** transcripts. The full list, with every affected signal id:

| holdout transcript (excluded) | pre-seal signals on it | verdicts at the exclusion date |
|---|---|---|
| `Radical_Subjectivity_The_I_of_Self_Feb_2002_Part_2_enxautogen_html.txt` | **D-092**, **D-093**, **D-094**, **D-095** | D-092 refused-notation (notation refusal, TASK-018 item 0f) · D-093·D-094 CERTAIN-leg-d · D-095 CANDIDATE |
| `Realization_of_the_Self_as_the_I_Nov_2003_Part_1_enxautogen_html.txt` | **D-107** | CANDIDATE |
| `Spiritual_Traps_Oct_2005_Part_2_enxautogen_html.txt` | **D-108** | CANDIDATE |
| `Witnessing_and_Observing_Oct_2004_Part_1_enxautogen_html.txt` | **D-122** | CANDIDATE |

Seven signals over four transcripts. The deferral of the source-inheritance filter over exactly
these seven was **correct and is endorsed** (ORCH-2, items 1–8 gate); what was missing was the
disclosure, not the decision. Machine-readable: `tools/HELD-OUT-SPLIT-V2-EXCLUSIONS.json`
(sha256 in the audit report's `taint_disclosure.source_sha256`), bound into the quantum-b freeze
and enforced by `tools/m4_one_shot_v2.py` — the excluded transcripts' signals are dropped
**unexamined** and never enter a denominator or a review queue. The audit report now carries a
`taint_disclosure` block and **fails** if this file or the dated note stops naming the
transcripts, the signal ids or the 29/33 denominator.

### v2.c — one exact audit stamp, cited identically in both files

This appendix's provenance row and `SEAL-AUDIT.json` now carry the same stamp, taken from
`date -u` at run time and never rounded:

**audit utc 2026-09-26T09:16:58Z** — cited above in the provenance row, and carried identically by
`SEAL-AUDIT.json` (sha256 `5d996151c14ee7b8ed6a7948a74855280dea4a53a9772c677acd4ce20364646d`), which was generated from the tool at commit `a0904395` (the commit whose blob equals the tool at head; its origin is `b991f29`). The
superseded earlier values `2026-09-25T21:44:00Z`, `2026-09-26T02:01:53Z` and `2026-09-26T02:07:06Z` and `2026-09-26T09:16:19Z` stay readable above
and here marked as superseded (the first was `:00`-rounded and named a different day and
time from the report's own field — ORCH-2's O-4 class, in this artefact; item v2.c). The audit
tool now reads this file and **fails** if its live audit-stamp citation disagrees with the
report's.

### v2.d — `tool_commit` for the audit tool

`SEAL-AUDIT.json` now carries `tool_commit` (the reachable commit whose blob **equals the tool at
head**, checked as `tool_unchanged_since_tool_commit`), `tool_commit_utc`, and
`tool_origin_commit` (the commit that first added the tool, `b991f294`). A reader no longer has
to derive the attribution from history: it is stated, and the equality is asserted in the report.

### v2.e — the citation census now covers every mention, and names the key

The previous census saw only objects carrying **both** `artifact` and `artifact_sha256` (5
pairs) while the fixture file cites the artefact at **6** paths; the sixth,
`/adjudication_summary_2026_09_25/artifact`, had **no paired digest** and so sat **outside** the
post-seal void check. The audit report now keeps `artifact_mentions` — **one row per citation
key**, naming the key (`json_path`, `keys_citing`), the artefact, the digest and its
`digest_source` — and puts **every** mention through the post-seal check, resolving an unpaired
mention's digest from the file at HEAD. `confirmation_artifacts` is now the artefact-level view
with the citing paths listed. **Result: 1 unpaired mention found and resolved; every one of the
six citations names the same pre-seal artefact — so the gap is closed by check, not by hand.**

### v2.a (iii), 2nd half — "one draw, not two", stated and checkable

`79eb401`'s commit subject says *re-seal*, which reads as a second draw to anyone who has not
compared the blobs. It was not one. The seal file has **two revisions**, and comparing them
mechanically (`seal_history` in the audit report, computed from `git show`):

| | `293b29c` (20:50:46Z) | `79eb401` (20:51:54Z) |
|---|---|---|
| keys added / removed | — | **0 / 0** |
| keys whose value differs | — | **`manifest` only** |
| `holdout` / `tuning` / `salt` | 33 / 197 / `fleetyard-m4-holdout-v2-2026-09-25` | **identical** |

So the split was drawn **once**; the second commit re-manifested the same draw. **No new salt is
owed**, and the audit report states this as `seal_history.one_draw` with its construction — a
future reader who sees the word "re-seal" in the log can check it in one command instead of
re-drawing the split.

No threshold, detector, split, salt, membership or fixture verdict was changed by this addendum.
No rate, precision or M6 figure is stated. The split-v2 holdout was **not** opened.
