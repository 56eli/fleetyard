# TASK-020 — M4 shipping-gap repair (q1 + q2 + q3 + q4 + q5): fixtures, clean set, threshold provenance, LAW §8 bindings, stale digest lines

- cut by: ORCH-2 (A-2026-09-25-002), lane `arena/01a0d9d0-fleetyard`, 2026-09-25T20:58Z
- claimant: WORKER-2 (A-2026-09-25-001) — **after TASK-018** (owner ERRATA-25g §5 order), and
  with **TASK-017** landed before item 8 can close
- milestone: **M4** (fleet/PLAN-v2.md) · repairs the FAILED criteria of TASK-014 q1 (`88009d2`
  gate), q3 (`6495a8b` gate), q2 (gate 20:58Z) and q4 (gate 21:09Z) — all four in
  `fleet/GATES.md`
- why one task: the three gates failed on the **same four shapes** — no fixture-recall run, no
  clean-set run, no threshold provenance, incomplete §8 manifests. Cutting three tasks would
  triple the queue for one bundle of work (ERRATA-25f §4: never overfill the queue).
- scope discipline: **append-only** everywhere. No committed artefact is edited in place; a
  correction is a new field, a new file, or a new row with the old one left readable. No
  detector threshold may change in this task (that would re-open tuning and contaminate the
  split-v2 evaluation, TASK-019). Filters in item 5 are **additive and must be reported both
  ways** (raw count and filtered count), never by silently changing the shipped numbers.

## Items

1. **§8 manifest completion (q2.4, q3.5).** For `runs/m4-q2-dropword/` (6 parts + merge) and
   `runs/m4-q3-format/`: publish a supplementary manifest per run directory (new file, e.g.
   `PROVENANCE-SUPPLEMENT.json`) carrying `tool_commit` (a reachable commit sha), `main_head`,
   `policy_sha256` (pin `0fe20a60…`), **book-store digest** (`corpus/docdocgo/html/
   merged-book-texts_json_1.js` = `c0892fcd…`, 24 slugs — required for q2, N/A-for-q3 must be
   *stated* rather than omitted), corpus + split digests at merge level, a **config digest**
   (sha256 over the sorted params), and a **per-part output digest**. Re-pin `detector_sha256`
   to a **committed** blob and state plainly that the original pin (`84e5407f…` for q2,
   `c322e053…` for q3) bound an uncommitted/older working-tree state, with the orchestrator's
   reproduction recorded as the attribution bridge (q2: shards 1 and 3 byte-identical at head,
   `64a97be5…` / `092d6341…`, covering 66/193 transcripts and 93/122 signals; q3: whole run
   byte-identical, `86c8f57d…`).
2. **Fixture-recall results (q2.1b, q3.2).** Run C1-drop and C2-format over
   `evidence/fixtures/confirmed/confirmed.json` (CF-001…CF-016) and publish a per-fixture
   caught/missed table, **labelled IN-SAMPLE / seeded** (the 3 fixture transcripts are
   forced-TUNING; LAW §9 forbids presenting this as recall). CF-015 (class P5) is the named
   target for C1-drop — state explicitly whether it is caught, and if not, why the rule's
   preconditions (≥10 matched words, ratio ≥0.85, flank ≥3, content word, no numeral) miss it.
3. **PATTERNS.md §3 rows (q1.4d, q2.1b, q3.2).** Line 44 (`drop-word — not built`) and line 45
   (`speaker/format — not built`) contradict §5b/§5c and line 179. Update both rows to the
   shipped state with measured cells from item 2, keep every figure **unmeasured/not
   promotable** for precision, and add the ledger binding q1.4d owes: PATTERNS.md must carry
   the M5-R ledger digest it quotes (`d42136c6…`) plus by-transcript (`c1ec4da8…`), the tool
   commit and the policy sha, so the catalogue is attributable without archaeology.
4. **Clean-set runs (q2.1c, q3.3).** `evidence/fixtures/clean/clean.json` = 59 hashed
   known-good Hawkins book passages (integrity verified by ORCH-2: 59/59 sha256 match the frozen
   store). Run both detectors over it and publish the counts. **ORCH-2's gate-side probe is the
   reproduction target: C1-drop 3 signals / 59, C2-format 1 signal / 59.** Report each hit with
   its book citation and its FP shape. Note in the run that v1's `0/59` figure is VOID as
   independent FP evidence (owner ERRATA-2026-09-25 §3) and that a clean-set run is a *misfire*
   check, not a precision measurement.
5. **Two owed filters + the shape defects (q2.6, q2.8).** (a) C1-drop must not report a drop
   when the transcript's own wording (span ±30 chars) occurs verbatim in the book store —
   ORCH-2 measured this shape at 3/59 on clean text and **1/122** in the tuning run
   (`Most_Valuable_Qualities…` @457). (b) C2-format must not report a punctuation/whitespace
   artifact whose bytes are inherited from the matched book span — measured 1/59 on clean text
   (`power_vs_force__the_hidden_de` @236391, `power.When`) and **0/49** in the shipped run.
   Both filters are additive; publish raw **and** filtered counts. (c) Exclude or re-label the
   **9 shape-defective** C1-drop signals ORCH-2 identified (3 where the dropped token already
   occurs in the cited span — `Causality…Part_1 @2574`, `@54983`, `Causality…Part_2 @55220`;
   6 partial-overlap/arithmetic cases, 2 of which are ORCH-2's own hyphen-tokenization artifact
   and must be judged, not assumed). Add the repetition/cross-book FP shapes to the README's
   disclosed FP list, and restate the signal count as **122 raw / ≤113 shape-consistent**, never
   122 omissions.
6. **Threshold provenance (q2.1d, q3.4).** For every threshold in both detectors state what it
   was fitted on and measured on — or state honestly that it was chosen by inspection on the
   tuning set and what that costs. For C2-format, publish the two rejected candidate rules
   **verbatim** (regex + flags + counts) so the camel-glue rejection (35 hits / 18 files) becomes
   reproducible; ORCH-2's probes gave 126/61 (any internal capital) or 6/6 (lowercase-start)
   while double-word 3,436/228 reproduced exactly.
7. **fixtures/v2/dropword.json coherence (q2.7).** Append a note citing the **enacted** leg (d)
   (owner ERRATA-2026-09-25e §2 — omission *within a matched span*; restoring completes the
   match) and record that the file's `proposed_leg_d` wording is superseded; re-adjudicate each
   fixture's `proposed_leg` (currently a/a/b/b) under the enacted text with the clause stated;
   append an exact `generated_utc` (the current value `2026-09-25T19:1xZ` is fuzzy). The four
   fixtures stay **provisional** until TASK-018 adjudicates them individually — detector hits
   never auto-classify (ERRATA-25e §2). ORCH-2 has independently confirmed all four bindings
   byte-exact and none of them a cross-book artifact, so adjudication can proceed on the bytes.
8. **Test-count baseline (q2.5) — blocked on TASK-017.** The lane suite is 26 tests
   (8 dropword + 6 format + 12 m5r, OK, 0 skipped, WITH corpus) against a campaign baseline of
   v1's **115**. After TASK-017 inherits the v1 toolchain, either restore the count or record the
   accepted reduction with reasons and owner visibility. Also fix the dangling instruction in
   `evidence/fixtures/README.md`: `tools/fixtures.py` and `tools/loaders.py` are **absent at
   head**, so `fixtures.py verify` / `build-clean` cannot be run in this lane until TASK-017.

9. **q4 holdout manifests (q4.6).** For all three runs in `runs/m4-q4-holdout/` publish a
   supplement manifest carrying: `corpus_zip_sha256` (`3f36c520…`) and the **book-store digest**
   (`c0892fcd…`) — load-bearing for the v1 leg (B2-misquote produced 8 book-referenced signals)
   and for C1-drop; `tool_commit` + `main_head` + `policy_sha256` (`0fe20a60…`); a config digest;
   and an **output digest for `v1-holdout.json`** (127 KB, currently undigested anywhere). Re-cite
   the v1 toolchain as **lane + commit + blob path** (`origin/arena/01a0d581-fleetyard:tools/<file>`)
   instead of the absolute sandbox path `/home/user/fleetyard/evidence/tools`, and record that
   ORCH-2 verified all 13 pinned shas byte-identical to that archive lane. Add the **explicit zero**
   for `B1-contradiction: 0` to `per_detector_signal_instances` (append a supplement field; never
   edit the original) and state that B1 therefore receives no validation from this run, so v1's B1
   headline hold (TASK-005 FAIL / REDIRECT-005) stands.
10. **Correct the C1-drop gap characterization (q4.8) — append-only.** PATTERNS §5d says the
    5-vs-122 gap is "dominated by sampling noise". ORCH-2's exposure-normalized arithmetic says
    otherwise, and the correction must carry the numbers: holdout transcripts are **14.9% shorter**
    (53,949 vs 63,361 chars mean; holdout = 1,996,122 of 14,224,783 corpus chars), so normalize by
    character exposure, not by file count — **v1: observed 185 vs expected 187.6, P(X≤185) = 0.45**
    (the 5.95-vs-5.00/tx difference is entirely exposure); **C2-format: 12 vs 8.0, P(X≤12) = 0.94**
    (consistent); **C1-drop: 5 vs 19.9, P(X≤5) = 7.7e-05** (5.1e-06 per-file) — a real ~4x deficit,
    not noise. Append the corrected sentence with both candidate causes (parameters fitted to the
    tuning half — untestable while q2.1d's provenance is missing; or a book-exposure difference
    between halves — testable **only** on split v2) and the standing prohibition: **never re-run the
    spent holdout to find out**. Rename the §5d column "rate/tx" to "signals/tx (density, not a
    rate)" so a density is never cited as an error rate.

11. **Stale ledger-digest lines + q5's numbers (q5.7, q5.8).** Three live documents still present
    the q5-era ledger digest `64977c2f…` as current while the ledger at head is **`d42136c6…`**
    (TASK-016's regeneration `a4c6655` rewrote the record shape two minutes after q5):
    `findings/README.md` line 88 ("current ledger sha256 …"), `findings/M4-q5-A1-CLAIM-
    RECONCILIATION.md` ("New ledger sha256 … recorded in findings/PROVENANCE.json") and
    `fleet/branches/WORKER-2-M5R-DELIVERY.md` line 80. Append a dated supersession line to each
    naming `d42136c6…`, the regenerating commit `a4c6655` and the rule "the binding of record is
    `findings/PROVENANCE.json`"; never rewrite the old line, and **leave the worker's
    `fleet/CONTROL.log` occurrence alone** (legitimate append-only history). Then append the
    corrected numbers to the reconciliation doc: ORCH-2's independent re-derivation gives
    **938/938 A1 claims corroborated** (Unicode rule, own code) and a pre-q5 simulation flags
    **97** (9 zero-ASCII-token + 61 over-bound + 27 ASCII-mismatch) against the doc's 98/67;
    claimed unit sizes run to **k=12** (9 claims), not "~11", so `kmax=16` has **4 tokens of
    headroom** — publish the bound *with* the tally and derive it as max-observed-unit + margin;
    and quantify the hyphen labelling nuance: **255 of 938 A1 claims (27%)** change verdict
    depending on whether the tokenizer joins or splits hyphens. The conclusion (no A1 claim-shape
    change required) is ACCEPTED and unchanged by these corrections.

## Acceptance (per-item verdicts will be gated by ORCH-2)

- 20.1 every supplement manifest carries tool_commit (reachable), main_head, policy_sha256,
  corpus + split + **book-store** digests, config digest, per-part output digest, run utc; the
  detector digest re-pin names a committed blob and states the original pin's defect.
- 20.2 a per-fixture table exists for **both** detectors over all 16 CF fixtures, labelled
  in-sample/seeded, with CF-015's outcome and, if missed, the precondition that missed it.
- 20.3 PATTERNS.md §3 rows 44–45 state the shipped detectors with measured cells and no
  precision claim, and PATTERNS.md carries the ledger/by-transcript/tool/policy bindings.
- 20.4 clean-set runs published for both detectors with counts, per-hit citations and FP shapes;
  ORCH-2 can reproduce 3/59 and 1/59 from the committed instructions.
- 20.5 both filters implemented additively with raw **and** filtered counts published; the 9
  shape-defective signals individually adjudicated (excluded or re-labelled with reasons).
- 20.6 threshold provenance stated per threshold; both rejected C2-format rules published
  verbatim and reproducible.
- 20.7 `fixtures/v2/dropword.json` carries the enacted-leg note, re-cut per-fixture legs and an
  exact generated_utc — appended, never edited in place.
- 20.8 test count reconciled against the 115 baseline (or the reduction recorded), and the
  fixture-tooling instruction no longer dangles.
- 20.10 q4 supplement manifests carry corpus + book-store + split digests, tool_commit, main_head,
  policy sha, config digest and an output digest for v1-holdout.json; the v1 toolchain is cited by
  lane + commit + blob path; B1's zero is explicit and its "no validation" consequence stated.
- 20.11 PATTERNS §5d carries the exposure-normalized correction (185/187.6 P=0.45 · 12/8.0 P=0.94 ·
  5/19.9 P=7.7e-05) appended, never rewritten in place, with both candidate causes and the
  never-re-run prohibition; the density column is renamed.
- 20.12 no live document presents a superseded ledger digest as current (the three named lines carry
  append-only supersession naming `d42136c6…` and `a4c6655`); the reconciliation doc carries
  ORCH-2's measured numbers (938/938 · 97 = 9+61+27 · max unit k=12 · kmax headroom 4 · hyphen
  sensitivity 255/938) with the tokenizer and bound published alongside the tally.
- 20.9 global: no threshold changed; no precision/rate/M6 figure claimed; every output stays
  CANDIDATE-class; LAW §8 manifest for every new run; suite green WITH corpus and skip counts
  reported; nothing written outside the claimant's lane; the sealed split v1 stays byte-identical
  (`481d8513…`) and is never used for a precision claim.

## Queue position

TASK-018 (owner-ordered, in force) → **TASK-020 items 1–7** → TASK-017 (v1 toolchain) →
TASK-019a (SEAL split v2) → re-gates of q1/q2/q3 + TASK-020 item 8 → TASK-019b (one-shot
evaluation) → M6 FINAL (TASK-015, still BLOCKED on split v2).
