# M4-q3 — C2-format run (tuning set) — PROVISIONAL-UNGATED

Detector `C2-format` (speaker/format artifacts, mechanically checkable half),
first run over the **tuning** half of `tools/HELD-OUT-SPLIT.json`. Holdout never
opened (`holdout_reads: []` in the provenance).

## What was run

| field | value |
|---|---|
| detector | `tools/det_format.py` (self-test green; sha pinned in provenance) |
| rules | R1 glued period (abbrev-filtered) · R2 repeated punctuation · R3 4+ dot run · R4 underscore run · R5 space-before-comma · R6 spaced period · R7 glued comma |
| inputs | `corpus` (zip `3f36c5203910…`), `tools/HELD-OUT-SPLIT.json` |
| result | **193/193 tuning transcripts, 49 raw signals in 32 transcripts** |
| by rule | R1 22 · R2 3 · R3 5 · R4 1 · R5 15 · R6 2 · R7 1 |
| provenance | `PROVENANCE.json` (inputs, rules, per-rule counts, detector sha) |

All signals are **CANDIDATE-class raw format artifacts**: the artifact itself is
mechanically demonstrable; whether it changed meaning is a reading question and is
not claimed. Precision/recall: **unmeasured** (holdout run + review = q4).

## The scope census behind the "speaker/format" claim (grounded, not asserted)

Corpus-wide census over all 230 transcripts (frozen bytes):

| probe | hits | reading |
|---|---|---|
| speaker labels (`Q:` `A:` `Speaker 1` `Questioner:` `Student:`…) | **0** | the corpus format encodes no speaker turns |
| bracketed stage directions (`[laughter]`, `(inaudible)`, `[music]`…) | **0** | none present to audit |
| HTML entities / tags / JS residue / control chars / tabs / nbsp | **0** | the corpus is clean of parser residue |
| double spaces / spaces before `;` | **0** | no whitespace drift |
| camel-glue (`veryCapitalist`) | 35 hits / 18 files | **not a rule**: dominated by legitimate proper nouns (`MacArthur`, `YouTube`) — recorded, not shipped |
| double word (`that that`) | 3,436 hits / 228 files | **not an artifact**: ordinary spoken repetition (A1-repetition's domain) |

Consequence, stated plainly: **speaker attribution is out of mechanical scope in
this corpus** — there are no speaker turns to check, and deciding that a passage is
wrongly attributed to the speaker rather than a questioner is a human reading
judgment. The M2 remainder "speaker/format" is therefore resolved as:
*format artifacts → measurable and measured here; speaker attribution → unmeasured,
recorded as an explicit M6 limitation*. That limitation is a finding about the
instrument, not a silence.

## Sample signals (verbatim, for the reader to judge)

- `R1` `people.You` (missing space after a sentence period — grammar/sense intact)
- `R2` `soul****` (censor-style asterisk run) · `, ,` doubled comma
- `R3` `.....` (5-dot run, adjacent to mixed-script garbage)
- `R5` `you , propensity` · `thank you , thank you again` (spurious space before comma)
- `R6` `Laugh . bacteria` (spaced sentence period mid-stream)
- `R7` `cure,lly` (missing space after comma)

## Limits

No audio; no human review of the 49 signals; no ORCH-2 gate (PROVISIONAL-UNGATED).
Rules are deliberately conservative — the census entries that were *rejected* as
rules (camel-glue, double word) are recorded above so the rejection is auditable.

## Shipping-evidence rebuild (2026-09-25, after ORCH-2's q3 gate 20:44Z)

ORCH-2 gated q3 INCOMPLETE on three shipping criteria (no fixture recall, no clean-set
run, §8 bindings absent; C2-format not promotable, its signals stay CANDIDATE). The
missing measurements were then produced by `tools/m4_q3_evidence.py` (build/verify) —
**evidence only**: the restriction stands until ORCH-2 re-gates.

| artefact | what it is |
|---|---|
| `EVAL.json` | fixture recall, clean-set run, rejected-rule probes (verbatim), book-store confound probe + control |
| `PROVENANCE-V2.json` | §8 manifest for the new run: `tool_commit`, `main_head`, `policy_sha256`, `detector_sha256`, `corpus_zip_sha256`, `split_corpus_files_sha256`, output digest, `holdout_reads: []` |
| `signals-v2tuning.json` | the run itself, over the **v2 tuning half** (197 transcripts) |
| `PROVENANCE.json`, `signals.json` (unchanged, 2026-09-25T20:33Z) | the **historic** run over the v1 tuning half (193 → 49 signals); kept and cited by digest `86c8f57d…`, **not replayed** because 33 of its files are v2-holdout members |

Results, as measured (nothing here is a rate):

* **Fixture recall 0/16** — C2-format fires inside none of the 16 confirmed fixtures.
  Format artifacts are not what those fixtures encode; measured and stated, per gate 1.
* **Clean set 1/59** — one misfire, `R1` `r.W` in `power.When` inside CL-026
  (`power_vs_force__the_hidden_de…`). That same glue sits in the **book store** verbatim:
  the "known-good" passage is not artifact-free with respect to R1. Clean-set figure is
  in-sample tune data — an FP count, **not** an independent FP rate.
* **Rejected-rule probes republished** (pattern + flags, v2 tuning half): double-word
  `\b(\w+)\s+\1\b` (re.IGNORECASE) **2,876 hits / 195 files**; camel probes
  104/53 (any internal capital), 6/6 (lowercase-start), 3/3 (classic), 2/2 (lower-upper
  run). The historic census figure (35 / 18 files over all 230) is marked **superseded**:
  its exact pattern was not recorded, which was the documentation gap the gate found.
* **Book-store confound probe — UNINFORMATIVE, recorded as such.** A nested-window probe
  (bare glue / ±10 chars / ±25 chars versus every book) returned 0/48 on both window
  tiers, but the **control** over the 15 fixtures that carry a book reference returned
  15/15 on the bare quote and **0/15** on the same windows: transcripts and the book store
  are normalised differently, so the window tiers cannot detect book-derived text here and
  the negative result is *not* evidence that the transcripts are book-independent.

`python3 tools/m4_q3_evidence.py verify --corpus corpus --split tools/HELD-OUT-SPLIT-V2.json \
    --out runs/m4-q3-format` → OK (holdout reads 0; 19 module tests).

## Threshold provenance (TASK-020 item 6, append-only)

C2-format has **no numeric decision thresholds**: the seven rules are shape predicates
(`word.Next` without an abbreviation before it; 2+ identical punctuation marks; 4+ dots; a
`_` run; `word ,`; `word . word`; `word,Word`), and the only numbers in the module are
`EXCERPT = 60` (a display window, not a decision) and the hand-assembled `ABBREV` exclusion
list. Their provenance:

* the rule shapes were chosen by inspection of the corpus's artifact shapes during the
  M4-q3 build and are enumerated in the module docstring;
* the `ABBREV` list was hand-assembled from the abbreviations actually seen in the tuning
  half; it is **not exhaustive by construction** — an abbreviation outside the list fires
  R1. The clean-set misfire is the mirror image of that cost: `power.When` in the book
  store is not an abbreviation at all but the book's own typography, and R1 cannot tell the
  two apart without a book-side anchor;
* two candidate rules were measured and **rejected**, and their probes are now published
  verbatim (pattern + flags + counts) in `EVAL.json`: double-word `\b(\w+)\s+\1\b`
  (re.IGNORECASE) 2,876 hits / 195 files; camel-glue probes 104 / 53 (any internal
  capital), 6 / 6 (lowercase-start), 3 / 3 (classic), 2 / 2 (lower-upper run). The
  historic census figure (35 / 18 files, all 230 transcripts) is **superseded**: its exact
  pattern was never recorded, which was the documentation gap the q3 gate found.

**What that costs.** The rules are conservative and mechanically demonstrable; what is
unmeasured is their *operating point* — no sensitivity study exists (how many signals at a
tighter dot run, a stricter abbreviation list), and no numeric threshold can be tuned
because none exists to tune. See `EVAL.json` for the measurements that do exist
(fixture recall 0/16, clean set 1/59, source-inheritance filter 48 → 48 raw/filtered on the
run and 1 → 0 on the clean set).
