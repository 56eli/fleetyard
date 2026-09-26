# WORKER-2 — TASK-019b preparation: the one-shot harness (built, NOT run)

lane `arena/01a0d9ce-fleetyard` · worker `A-2026-09-25-001` · 2026-09-26T00:32:03Z (src 72104a5; read `21:5xZ`)
task: TASK-019 quantum b (holdout evaluation), preparation only — **no holdout has been read**

## Why this exists

TASK-019b is one-shot by construction: thresholds frozen and recorded **before** the single
run, the receipt stamped `holdout_consumed` with the full read list, the split salt/digest
and the tool commit, and **never re-run** (a re-run needs a new split with a new salt). That
discipline cannot be remembered into existence at the moment of the run — it has to be in the
tooling, so this harness was built and tested now, while the run is still blocked.

## What was built

| artefact | what it is |
|---|---|
| `tools/m4_one_shot_v2.py` | `freeze` / `run` / `score` / `verify` for the holdout evaluation |
| `tools/c2_detectors.py` | the registry bridging the harness to `tools/det_dropword.py` and `tools/det_format.py` — each detector's canonical `which="holdout"` path, its frozen parameters, and its file digest |
| `tests/test_m4_one_shot_v2.py` | 10 tests, all on a toy corpus + toy split in a temp dir |
| `tools/m4_seal_audit.py`, `tests/test_m4_seal_audit.py` | the post-seal integrity check (7 tests) with its report in `runs/m4-q2-adjudication/` — see that report and the seal appendix |

## The refusals (the point of the harness)

`run` refuses, with the rule named in the message, when:

1. **no freeze exists** — "thresholds must be recorded before the run";
2. **a receipt already exists** in the out dir — the holdout is spent for those detector
   versions; "a second run needs a NEW SPLIT (new salt) in a new --out dir, plus a dated
   record";
3. **a detector file or its parameters changed after the freeze** — a post-freeze edit
   invalidates the run rather than riding along;
4. **the split file no longer matches the frozen split digest**;
5. the detector's evaluated transcript set is not exactly the frozen holdout set (a partial
   read is refused, not scored).

`score` refuses any verdict other than `confirmed` / `discarded` and any label without a
reason ("the cited bytes read"). It computes precision **only** over hand-labelled signals,
publishes label coverage (`labelled/total`), separates `seeded` from `independent`
(LAW §9 — seeded never counts toward the rate), keeps unlabelled signals as
`candidate_unlabelled` (never blended into any figure) and carries the protocol text into
the score file. Label keys are detector-qualified (`"C1-drop/<transcript>#<n>"`), because the
same transcript index occurs under both detectors.

`verify` re-checks the receipt without touching the corpus: thresholds digest, signals
digest, `holdout_consumed`, first attempt, freeze-vs-receipt split agreement, the live split
file, and that neither detector has changed since the run.

## What the freeze will record (at run time, not now)

`THRESHOLDS.json` binds: the split file + its sha256, the salt, the split counts and corpus
digest, each detector's module sha256 and frozen parameters (C1-drop:
window 24 / stride 12 / min_score 0.20 / top_k 3 / min_matched 10 / min_ratio 0.85 /
max_drop 2 / min_flank 3; C2-format: the seven rule ids and excerpt 60), the adjudication
protocol, and the statement that the freeze precedes any read of that split's holdout. The
freeze command requires `--utc`, `--tool-commit`, `--main-head`, `--policy-sha`, so the
record cannot be written without naming its provenance. The receipt then carries the
thresholds digest, so a later freeze cannot be substituted for the one that was used.

## State

* The harness is **built and tested**; it has **not been run** against split v2.
* The v2 holdout has **not** been opened by anything in this work — every test uses a toy
  corpus, toy book and toy split in a temp dir; the audit reads git objects and committed
  files only.
* Still required before the single run: ORCH-2's re-gates (q1/q2/q3 + item 8) and the queue
  turn for quantum b. Thresholds are frozen by `freeze` **at that point**, in one commit, so
  the freeze cannot be stale or back-dated.
* Probe results that are part of the record, not the run: `runs/m4-q2-adjudication/SEAL-AUDIT.json`
  + `runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md` (split v2 stands; the fixture-file
  digest moved by an append-only edit, no fixture was added, the confirmation artefact
  predates the seal).

## Suite

`python3 -m unittest discover -s tests` → **244 tests, OK, 1 skipped** (227 before + 10
harness tests + 7 audit tests), run **with** the corpus present, so the skip is unchanged and
no test was dropped.

No threshold was changed, no detector edited, no rate or precision stated, no M6 figure, and
the holdout stays sealed.

## Addendum (2026-09-26) — pre-registration recorded: 29 of 33 holdout transcripts

ORCH-2's GATE CYCLE H routed item **v2.b (criterion v2.11)** to TASK-019 and required the
quantum-b consequence to be decided **in the pre-registration, not afterwards**. It is decided
and recorded here, before any run:

**The four label-tainted holdout transcripts are excluded from the reported denominator; the
evaluated holdout is 29 of 33 transcripts.** The four (with their seven signals) are named in
`tools/HELD-OUT-SPLIT-V2-NOTE-2026-09-26.md` and machine-readably in
`tools/HELD-OUT-SPLIT-V2-EXCLUSIONS.json`. The harness now:

* binds the exclusions into `THRESHOLDS.json` (`holdout_exclusions` + digest) at freeze time;
* refuses at run time if the exclusion file changed after the freeze, or if an exclusion is not
  a holdout member;
* evaluates exactly `holdout − exclusions`, drops the excluded transcripts' signals
  **unexamined** (they never enter the signals artefact, a denominator or the review queue);
* records `holdout_evaluated`, `holdout_excluded` and `excluded_signals_dropped_unexamined` in
  the receipt.

The standing caveat travels with any resulting figure: *"a first figure under v2 is an estimate
under this split, not a pristine out-of-sample number"* (all 33 holdout transcripts were read by
the pre-seal v1-era run — the seal's own disclosure). Still required before the single run:
ORCH-2's re-gates and the queue turn; thresholds are frozen in one commit at that point (with
the exclusions already fixed in the file above).

---

# ADDENDUM — cycle-I/cycle-J repairs landed in the harness (2026-09-26T02:2xZ, append-only)

Items **v2.g** and **§G2** were the two worker-side conditions the gate kept open in this file's
own subject matter, and both are now in the tooling rather than in prose.

**§G2 — the freeze binds the notes that make the seal readable.** `freeze` writes a
`companion_notes` list, one entry per dated note: `path` + `sha256` + `commit` (the commit that
**added** the note, so a later digest-only re-pin cannot be mistaken for authorship) +
`commit_utc` (that commit's committer time, exact to the second) + the **source** of both. The
defaults are the seal appendix, the seal audit report and the dated seal note; a missing note is
refused at freeze time, an uncommitted note is refused (its commit cannot be derived), and `run`
**refuses** when a bound note's live digest has moved or the note is gone — the same refusal shape
as a changed detector or a changed split. `verify` re-checks the bound digests and fails a freeze
that binds no companion at all. So the run cannot proceed on the seal alone (O-5/A1 as amended).

**v2.g — the refusal surface is now 12/12 asserted, 4 of them added here.** The four refusals the
gate found unasserted now each have a toy test, and each test asserts the message fragment:

| refusal | test |
|---|---|
| detector **parameters** changed after the freeze | `test_run_refuses_when_the_frozen_parameters_changed` (edits the freeze record; the module file is untouched, so the assertion cannot be satisfied by the file-digest branch) |
| **evaluated set ≠ frozen holdout** (partial read) | `test_run_refuses_a_partial_holdout_read` (a frozen holdout of two, a detector that reads one) |
| exclusions **not holdout members** | `test_run_refuses_exclusions_that_are_not_holdout_members` |
| **score-side** partial/substituted read | `test_score_refuses_a_partial_or_substituted_read` (a shortened signals file, a substituted one, and labels naming no signal of this run — plus the unmodified pair still scoring, so the refusal is not spurious) |

`score` gained the two denominator guards this required: it refuses when the signals file covers
fewer transcripts than the receipt evaluated, when its bytes are not the ones the receipt bound,
and when the labels name signals this run never produced. Partial **labelling** remains a
disclosure, not a refusal — unlabelled signals stay `CANDIDATE` with `label_coverage` published,
because refusing them would forbid the protocol's own shape; what must never happen is scoring a
*smaller read*, and that is now refused three ways. §H's sentence (29 primary + 33 pre-registered
sensitivity from the same run) is in `tools/HELD-OUT-SPLIT-V2-NOTE-2026-09-26.md`.

Test count in this file's subject matter: `tests/test_m4_seal_audit.py` **12** (was 7),
`tests/test_m4_one_shot_v2.py` **18** (was 10), `tests/test_m4_t18_dispositions.py` **7** (was 6).
The harness is still **NOT RUN** and the v2 holdout has not been opened.
