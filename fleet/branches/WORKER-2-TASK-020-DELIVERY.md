# WORKER-2 — TASK-020 delivery (M4 shipping-gap repair: q1 + q2 + q3) — lane record

**Worker:** WORKER-2 (`A-2026-09-25-001`), lane `arena/01a0d9ce-fleetyard`
**Authority:** ORCH-2 `fleet/queue/pending/TASK-020.md` @ `76f0203` (cut at the q2 gate `91cf112`);
gates q1 `88009d2`, q2 `91cf112` (+ q2.8 probe), q3 `6495a8b` (+ q3 addendum)
**Scope discipline held:** append-only everywhere (every original file's content is still
readable — `fixtures/v2/dropword.json` shows 87 insertions / 0 deletions), **no detector
threshold changed** (`git diff` clean for `tools/det_dropword.py` and `tools/det_format.py`
across this whole repair), filters additive with **raw and filtered** counts, no precision /
rate / M6 figure, everything CANDIDATE-class, v1 seal byte-identical
(`tools/HELD-OUT-SPLIT.json` = `481d8513…`), v2 holdout never opened (`holdout_reads: []` in
every new manifest).

New artefacts (all on this lane):

| artefact | sha256 (prefix) |
|---|---|
| `tools/m4_q2_evidence.py` (+ 21 tests) | `7615095a…` |
| `tools/m4_t20_supplement.py` (+ 13 tests) | `f73f6914…` |
| `runs/m4-q2-dropword/EVAL.json` | `b56f4bdb…` |
| `runs/m4-q2-dropword/EVIDENCE-PROVENANCE.json` | `605a6495…` |
| `runs/m4-q2-dropword/PROVENANCE-SUPPLEMENT.json` | `70ec0da9…` |
| `runs/m4-q3-format/PROVENANCE-SUPPLEMENT.json` | `c1ed8e9b…` |
| `fixtures/v2/dropword.json` (appended fields only) | `c40d272f…` |

(The q3 evidence from the same repair, delivered earlier this shift at `1cd5d44`:
`tools/m4_q3_evidence.py` + `runs/m4-q3-format/{EVAL.json,PROVENANCE-V2.json,signals-v2tuning.json}`
+ 19 tests, fixture recall 0/16, clean set 1/59, §8 bindings.)

## Verdicts on the task's own acceptance criteria

**20.1 — supplements carry the full §8 binding set.** `PROVENANCE-SUPPLEMENT.json` in both
run directories carries `tool_commit`, `main_head`, `policy_sha256` (`0fe20a60…`),
book-store digest (`c0892fcd…` — for C2-format the *N/A* is **stated**, not omitted), corpus
zip + split digests, a **config digest** (sha256 over the sorted params), **per-part output
digests** (q2: all six parts + the merge; part-1 `64a97be5…` and part-3 `092d6341…` are the
two ORCH-2 reproduced), `run_utc`, and detector re-pins that **name the defect**: C1-drop's
`84e5407f…` "resolves to NO committed blob … the parts ran before the delivery commit
`012914d`", C2-format's `c322e053…` "matches `det_format.py` at `4425763`, not at head; the
intervening `4e114f1` changed only the runner", each with the orchestrator's byte-identical
reproduction recorded as the attribution bridge. `verify` re-checks every count and detects
tampering (test-covered).

**20.2 — per-fixture tables for both detectors, in-sample labelled.** C1-drop **0/16**
(`runs/m4-q2-dropword/EVAL.json`), each miss carrying a **precondition diagnosis**
(matched / ratio / flank / max_drop / content word / numeral) computed by replaying the
window search near the fixture. **CF-015 (the named target) is NOT caught** and the reason
is stated from the bytes: best window `the_map_of_consciousness_expla` @386600, score 0.2049,
matched 10, ratio 0.9091 — both preconditions pass — but the alignment ops are
replace×2 / delete×1 / equal×2 and **no insertion op**, i.e. the difference is a
substitution, and the rule only reports book words *missing* from the transcript inside a
matched span. C2-format **0/16** (see the q3 evidence). Both labelled IN-SAMPLE / seeded.

**20.3 — PATTERNS §3 rows updated + catalogue bound.** Rows 44–45 now state the shipped
detectors with measured cells (drop-word: 122 raw → 57 CERTAIN / 65 CANDIDATE, 2/4 fixtures;
speaker/format: 49 + 48 signals, 0/16 fixtures, clean 1/59) and **no precision claim** —
each row's `promotable?` stays **no**, with the restriction quoted. The provenance block now
also carries the **policy sha** alongside the ledger digest `d42136c6…`, the by-transcript
digest `c1ec4da8…` and the tool commit `dada3e6` (q1.4d), so no figure needs archaeology.

**20.4 — clean-set runs for both detectors.** C1-drop **3/59** misfires, each with its
citation and shape: CL-034 → `daily_reflections_from_dr_dav` @80391 (`remains`), CL-035 →
`discovery_of_the_presence_of_g` @295761 (`by ownership`), CL-055 →
`the_map_of_consciousness_expla` @134304 (`so-called`) — all three **cross-book
self-parallels** (the "transcript" *was* book text). C2-format **1/59**: R1 on
`power_vs_force__the_hidden_de` @236391 (`power.When`) — the book store's own typography.
Both numbers reproduce ORCH-2's gate-side probe (3/59 and 1/59). v1's `0/59` is marked
**VOID as independent FP evidence**, and both runs note that a clean set is a *misfire
check*, not a precision measurement.

**20.5 — filters additive with raw and filtered counts; the shape defects adjudicated.**
Filter rule (both detectors): suppress when the signal's own wording (span ±30 chars) occurs
verbatim in the book store. C1-drop **122 raw → 1 inherited → 114 filtered** (7 signals sit
in v2-holdout transcripts and are **deferred**, disclosed: filtering them would open the
sealed holdout; 121 if those were kept) — this reproduces the gate's `1/122` and its one
example. C2-format **48 → 48** (0 inherited) and **1 → 0** on the clean set, reproducing the
gate's `0/49`. Clean set: C1-drop 3 → 0 after the filter.
Shape adjudication (all 122, from the record, with the deletion arithmetic shown per signal):
**3 excluded** as `dropped-token-not-missing` — the gate's own three (`evidence` @2574,
`staggering` @54983, `sovereign` @55220) — **5 re-labelled** `partial-overlap` (the drop set
contains a token the book span repeats: @50894, @63163, @20458, @53024, @60843) and **1
gate-listed hyphen case excluded pending a human read** (`one-third` @40831; this
instrument's deletion closes exactly, the gate itself assigned it to its own tokenizer).
Result: **122 raw / ≤113 shape-consistent**, reached independently and reconciled to the
gate's figure. One disclosed difference: this instrument finds **114** deletion-closing
signals against the gate's 113 — the gap is the apostrophe-quote normalization (U+2019 vs
`'`), which cost the gate five otherwise-consistent signals; the stricter reading is kept as
the published bound. The README's disclosed FP list now names the cross-book self-parallel
and book-side-repetition shapes.

**20.6 — threshold provenance.** New sections in both run READMEs: all eight C1-drop
parameters state what they were fitted on and measured on (chosen **by inspection on the v1
tuning half**, no optimiser, nothing fitted to the holdout or to the clean set) and what
that costs — the operating point is unchosen and the **sensitivity study is impossible under
split v2 discipline** (33 of the 193 v1-tuning transcripts are v2-holdout members), recorded
as a limitation. C2-format has **no numeric decision threshold**; its rule shapes and its
non-exhaustive `ABBREV` list are stated, and the two rejected candidate rules are published
verbatim with counts (`\b(\w+)\s+\1\b` re.IGNORECASE → 2,876 / 195; camel probes 104 / 53,
6 / 6, 3 / 3, 2 / 2) with the historic 35/18 marked superseded.

**20.7 — `fixtures/v2/dropword.json` coherence.** Appended (never edited): the enacted
leg-(d) note citing owner ERRATA-2026-09-25e §2 with the `proposed_leg_d` wording explicitly
**superseded**, the four `proposed_leg` values marked superseded, per-fixture
re-adjudication under the enacted clause cited to
`runs/m4-q2-adjudication/fixtures-adjudication.json` (`D2-001`/`D2-003` **confirmed under
clause d-i**, one word absent inside a matched span with the restoration completing the
match; `D2-002`/`D2-004` stay CANDIDATE — two words is a larger edit than clause d-i allows),
and an exact `generated_utc`: **`2026-09-25T19:06:53Z`** (committer timestamp of `012914d`,
the commit that introduced the file), with the fuzzy `19:1xZ` left readable and its source
stated. Diff: **87 insertions, 0 deletions**; a programmatic walk confirms every original
value survives.

**20.8 — test count reconciled; dangling instruction resolved.** Lane suite **217 tests, OK,
1 skipped, WITH corpus** (`python3 -m unittest discover -s tests`, ~200 s) against the
campaign baseline of v1's **115** — the count is not merely restored, it is exceeded by 102,
with 34 of the new tests belonging to this repair. The dangling instruction in
`evidence/fixtures/README.md` (a *working input*, deliberately uncommitted) is no longer
dangling: TASK-017 put `tools/fixtures.py` and `tools/loaders.py` at head, `python3
tools/fixtures.py verify` → `fixtures OK (16 confirmed CERTAIN)`, and
`python3 tools/fixtures.py build-clean` **reproduces** the committed
`fixtures/clean/clean.json` byte-identically (`393112e3…`), so the documented workflow works
as written.

**20.9 — global disciplines.** No threshold changed; no precision / rate / M6 figure claimed
anywhere (the EVAL files carry an explicit not-promotable status and a
rate-language guard test); every new run carries a §8 manifest with `holdout_reads: []`;
suite green with skip count reported; nothing written outside this lane; v1 seal unchanged;
v2 seal unchanged since its re-seal (see the note below); the 9 shape-defective signals are
excluded or re-labelled, and **122 is never quoted as an omission count** (published bound
≤113, in-sample and unreviewed).

## Disclosures for ORCH-2

1. **Re-seal of split v2 (this shift, `79eb401`).** The seal was rebuilt once so its
   `manifest.tool_sha256` binds the *head* revision of `tools/m4_split_v2.py` instead of a
   pre-commit state — the same staleness the q3 gate failed elsewhere. Same salt
   `fleetyard-m4-holdout-v2-2026-09-25`, same rule, same buckets (tuning 197 / holdout 33 /
   forced 43); only the manifest bindings changed. The seal sha is now
   **`73d86f0dafe5e51162723bd92121021a099a5c6b5b89fc5386421c496ced5d8a`** (was `f357ed21…`).
   No fixture was confirmed in between, so the re-seal rule (`new salt` on a post-seal
   fixture confirmation) was **not** triggered; if the gate reads any seal change as needing
   a new salt, say so and I will cut split v3 — 019b has not run.
2. **7 of 122 C1-drop signals** sit in v2-holdout transcripts: their *shape* is adjudicated
   from the record, but their source-inheritance filter is deferred to protect the seal.
   ORCH-2's own pre-seal probe measured 1/122, which the 115 measurable signals reproduce.
3. **Filtered counts are per-detector measurements, not promotions**: raw and filtered are
   both published; neither is a rate, and the restriction on C1-drop/C2-format stands until
   the gate re-runs q1/q2/q3.
4. **Item 8's README fix is uncommitted by design** (`evidence/` is a working input and is
   never committed) — the evidence that the instruction works is the two commands above,
   reproducible at head.
