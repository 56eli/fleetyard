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

## Addendum — items 9, 10, 11 (q4 + q5 gate extensions), appended after delivery

**Item 9 — q4 holdout §8 supplement (`runs/m4-q4-holdout/PROVENANCE-SUPPLEMENT.json`,
sha256 `0a1fd43c9e1fbff4ea530636dbca3edaf6f97e7212da95e8461361c588c38907`; tool
`tools/m4_q4_supplement.py` + 10 tests).** Written fresh; all three run artefacts and their
original provenance files are untouched. It carries `corpus_zip_sha256` (`3f36c520…`), the
**book-store digest** (`c0892fcd…`, with the load-bearing reason stated: the v1 leg's
B2-misquote produced 8 book-referenced signals and C1-drop is book-anchored), `tool_commit`,
`main_head`, `policy_sha256` (`0fe20a60…`), a **config digest** per part (v1
`193532701167…`, drop `409458723e16…`, format `805241dd0930…`), and an **output digest for
every part file**, including the previously undigested `v1-holdout.json`: **sha256
`cf8e7a7a4f2c07300832a11a900375a1787acc0a0ed5cd31cce4018649d83536`** (127,733 bytes).
The v1 toolchain is re-cited as **lane + commit + blob path**
(`origin/arena/01a0d581-fleetyard:tools/<file>`), replacing the sandbox path
`/home/user/fleetyard/evidence/tools`, and the supplement records that all **13 pins are
byte-identical to that lane's blobs — verified independently by WORKER-2 at build time
(`git show <ref>:tools/<file>` → sha256, 13/13) and by ORCH-2** (q4 gate `ea9be59`).
`B1-contradiction: 0` is now an **explicit** supplement field with its consequence stated:
B1 receives **no validation** from this run, so v1's B1 headline hold (TASK-005 FAIL /
REDIRECT-005) stands. `verify` re-checks every digest, the pins against the archive lane,
and the B1 zero (tamper-tested). The spent holdout was **not re-run** to produce this file.

**Item 10 — the "sampling noise" correction (`tools/PATTERNS.md` §5d + `runs/m4-q4-holdout/
README.md`, appended, never rewritten).** WORKER-2 re-derived ORCH-2's exposure arithmetic
independently and reproduces it: holdout transcripts are **14.9% shorter** (mean 53,949 vs
63,361 chars; holdout = 1,996,122 of 14,224,783 corpus chars = 14.03%); expectation =
tuning-side count × 0.16323; Poisson tails — **v1 185 vs 187.9 expected, P(X≤185) = 0.44**
(gate 187.6 / 0.45), **C2-format 12 vs 8.0, P = 0.94** (gate 0.94), **C1-drop 5 vs 19.9,
P(X≤5) = 7.7e-05** (gate 7.7e-05) → a real ~4x deficit, **not** noise. Both candidate causes
are recorded (parameters fitted to the tuning half — now partly testable via item 6's
provenance; or a book-exposure difference between halves — testable only on split v2), with
the standing prohibition **never re-run the spent holdout to find out**. The §5d column was
renamed from "rate/tx" to **"signals/tx — density, not a rate"** as required.

**Item 11 — stale ledger digests and q5's numbers (all append-only; old lines left
readable).** Supersession notes now sit in `findings/README.md`,
`fleet/branches/WORKER-2-M5R-DELIVERY.md` and `findings/M4-q5-A1-CLAIM-RECONCILIATION.md`
naming the current ledger **`d42136c673188f9e091526083b95941cabc5822a8b5cffeb8913b942cb658a32`**
(recomputed at head), the regenerating commit **`a4c6655`**, and the rule that **the binding
of record is `findings/PROVENANCE.json`**. `fleet/CONTROL.log`'s occurrence was deliberately
left alone (legitimate append-only history). The reconciliation doc additionally carries the
corrected numbers: **938 A1 claim_checks, 938 `claim_ok: true`** (WORKER-2's own recount at
head); ORCH-2's pre-q5 simulation tally **97 = 9 zero-ASCII-token + 61 over-bound + 27
ASCII-mismatch** (superseding the doc's 98/67, cited as the gate's measurement); claimed unit
sizes **run to k = 12 with exactly 9 claims at k = 12** (WORKER-2's tally: k=1 248 · k=2 179 ·
k=3 92 · k=4 124 · k=5 84 · k=6 63 · k=7 57 · k=8 30 · k=9 21 · k=10 20 · k=11 11 · k=12 9),
so `kmax = 16` is **max-observed-unit + margin with 4 tokens of headroom**, published with
the tally; and the hyphen labelling nuance is quantified as **255/938 (27%)** (ORCH-2's
figure, cited with the tokenizer caveat; WORKER-2 separately re-verified the `M5R-0036`
instance). The rule-quality conclusion — no v1 A1 claim-shape change required — is untouched.

**Suite after this addendum: 227 tests, OK, 1 skipped, WITH corpus** (baseline 115; 10 of the
new tests cover the q4 supplement). All original files remain byte-identical: only appends and
new files, `git diff` clean for `tools/det_dropword.py`, `tools/det_format.py` and every
`runs/m4-q4-holdout/` artefact.

## Addendum — item 8a: generator attribution for all six supplement artefacts (2026-09-26)

**Owed by the gate:** `tool_commit` alone did not reach the code that produced the artefacts
(q2 pins `71c37cf`, q3 EVAL `2bbb9f6`, q4 `ffb8811` — a cadence commit; none contains the
generator). Repair, per the gate's convention: keep `tool_commit` as written (the lane head at
run time) and add a `generator_pins` object next to it.

| artefact | generator | generator commit | sha256 before → after |
|---|---|---|---|
| `runs/m4-q2-dropword/PROVENANCE-SUPPLEMENT.json` | `tools/m4_t20_supplement.py` | `a5dec388…` | `70ec0da9…` → `6c0fcb20…` |
| `runs/m4-q2-dropword/EVAL.json` | `tools/m4_q2_evidence.py` | `a5dec388…` | `b56f4bdb…` → `2baefc09…` |
| `runs/m4-q2-dropword/EVIDENCE-PROVENANCE.json` | `tools/m4_q2_evidence.py` | `a5dec388…` | `605a6495…` → `c1285e01…` |
| `runs/m4-q3-format/PROVENANCE-SUPPLEMENT.json` | `tools/m4_t20_supplement.py` | `a5dec388…` | `c1ed8e9b…` → `cf68ee05…` |
| `runs/m4-q3-format/EVAL.json` | `tools/m4_q3_evidence.py` | `1cd5d444…` | `513c2826…` → `eb6a0a22…` |
| `runs/m4-q4-holdout/PROVENANCE-SUPPLEMENT.json` | `tools/m4_q4_supplement.py` | `d7fee6e1…` | `0a1fd43c…` → `af6af1b8…` |

Each block carries `generator_tool`, `generator_tool_commit` (full sha), `generator_tool_blob`
(`origin/arena/01a0d9ce-fleetyard:tools/<file>` — the same citation style item 9 used for the
v1 toolchain), `generator_tool_sha256` and a note distinguishing the two commits. Report:
`runs/m4-pin-repair-2026-09-26.json`; tool `tools/m4_pin_repair.py` + `tests/test_m4_pin_repair.py`
(5 tests); the four generators now emit the block at build time and two of them
(`m4_t20_supplement`, `m4_q4_supplement`) refuse to overwrite a manifest that records a
different generator, so a future collision fails loudly.

**Rebuild proof:** every artefact was regenerated with its own generator and the recorded run
args and is **byte-identical** to the committed file (q2 supplement, q3 supplement, q4
supplement, q2 evidence pair, q3 EVAL), so the addition is reproducible rather than
hand-applied. Two stale cross-references were corrected by that same rebuild: q2 `EVAL.json`
`provenance_sha256` `605a6495…` → `c1285e01…` and q3 `EVAL.json` `provenance_sha256`
`afeb5306…` → `b2bf6ad7…` (both pointed at their supplement's pre-repair digest — the same
staleness class as item v2.a, caught by the rebuild rather than by a reader).

**Disclosed consequence:** the six digests above are cited in `fleet/LOG.md` and earlier text
of this file as the pre-repair values (append-only: left readable). The current values are the
ones in this table.
