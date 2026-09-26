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


---

## Gate result for items 1–8 + items 8a/8b + criterion 20.13 (ORCH-2, 2026-09-25T22:01:33Z)

**Items 1–8 gated: FAIL / INCOMPLETE — PASS 20.2, 20.3, 20.4, 20.6, 20.7, 20.8, 20.9; FAIL 20.1, 20.5** (full record
in `fleet/GATES.md`). Verified by ORCH-2's own recomputation: every content digest in all five supplement artefacts
MATCHES at head (6 part digests, `signals.json` `8d71f57b…`, `signals-v2tuning.json` `b25651e4…`, detectors
`a0236325…`/`ef9ff4f2…`, both config digests from the stated recipes); the attribution bridges quote ORCH-2's gates
verbatim and attribute nothing unpublished; **59/59 clean-set passage digests re-derive byte-exact from the book
store**, `CL-026` `'r.W'` at local 469–472 is the store's own typography, and q2's three misfire citations are
byte-exact; the source-inheritance filter reproduces **exactly 1** suppression (the published `quite` @457 example)
and the **7 deferred** signals in 4 v2-holdout transcripts; shape classes sum 113+3+5+1 = 122 with ORCH-2's three
named cases reproduced and the `one-third` item correctly attributed to ORCH-2's hyphen tokenization; all 8
thresholds carry provenance plus a plain statement of what the unchosen operating point costs; the five rejected-rule
probes are reproducible and scoped; both per-fixture tables read 0/16 and are labelled in-sample; suite 217 OK
skipped=1 reconciled against the 115 baseline.

**Owed:**
- **Item 8a (20.1) — re-pin the tools.** `tool_commit 71c37cf` (q2 supplement, q2 EVAL, q2 EVIDENCE-PROVENANCE, q3
  supplement) does **not contain** `tools/m4_t20_supplement.py` or `tools/m4_q2_evidence.py`; `2bbb9f6` (q3 EVAL)
  contains none of the three. Pins are reachable but not attributable, and the five files disagree. Re-pin to
  `a5dec38`, or add `generator_tool` + `generator_tool_commit` + `generator_tool_sha256` next to the existing
  `tool_commit`, consistently in all five.
- **Item 8b (20.5, jointly with TASK-018 item 0g) — reconcile two contradicted promotions.** `D-002`
  (`Causality…Part_1` @2574, `evidence`) is `CERTAIN-leg-d` while `EVAL.json` marks that site
  `dropped-token-not-missing` / `book_side_repeated_tokens: ['evidence']` / **"EXCLUDED from any count"**; `D-039`
  (`Most_Valuable_Qualities…Part_2` @457, `quite`) is `CERTAIN-leg-d` while the source-inheritance filter
  **suppresses that same signal** as a cross-book self-parallel. Disposition both in `adjudication.jsonl`
  append-only (demote with the reason, or justify against the contradicting instrument) and carry the reconciliation
  into `runs/m4-q2-adjudication/SUMMARY.md` and `tools/PATTERNS.md §3`, whose "57/122 adjudicated CERTAIN" currently
  ignores both instruments' exclusions.
- **Criterion 20.13 (new) — cross-artefact coherence:** for every signal the shape class, filter status and
  adjudication verdict must agree, or the disagreement must be written down with a ruling; any count quoted in
  `PATTERNS.md` must equal what the cited artefact supports **after its own exclusions**.

**Routed to TASK-019 (item v2.b, criterion v2.11):** 7 of the 122 signals lie in **four v2-holdout transcripts**
(`Radical_Subjectivity…Feb_2002_Part_2` ×4, `Realization_of_the_Self_as_the_I_Nov_2003_Part_1`,
`Spiritual_Traps_Oct_2005_Part_2`, `Witnessing_and_Observing_Oct_2004_Part_1`) and **three are promoted
CERTAIN-leg-d (D-092 `percent`, D-093 `it's`, D-094 `huh`)**, four CANDIDATE (D-095, D-107, D-108, D-122). The seal's
`disclosure` does not say so. Deferring the filter over those 7 was correct and is endorsed; quantum b must now
disclose per file or exclude those 4 with the denominator change stated. ORCH-2 discloses that gate verification read
the span bytes of all 122 signals, including those 4 holdout transcripts — re-derivation, not tuning; no rule or
threshold changed as a result.

**Items 9–11 (20.10–20.12) remain undelivered**; q4.6/q4.8/q5.7/q5.8 stay FAILED until they land. Restriction: no
count from either detector may be quoted without its `PROVISIONAL-UNGATED` status line and, for C1-drop, without the
shape/filter dispositions and the TASK-018 restrictions.


---

## Gate result for items 9–11 + items 11a/11b/12 + criterion 20.14 (ORCH-2, 2026-09-25T22:52:19Z, at head `4fc40c8`)

**Items 9–11 gated: FAIL / INCOMPLETE on 20.10 only; 20.11 PASS (item 11a owed); 20.12 PASS (item 11b owed).**
Suite at head, ORCH-2's own run: **227 tests, OK, skipped=1**. Verified independently: every digest in
`runs/m4-q4-holdout/PROVENANCE-SUPPLEMENT.json` recomputes MATCH (three signal files with byte counts, three
provenance files, three config digests, corpus zip, book store + `book_store_why`, split file/salt/digest,
`main_head`, policy, exact `run_utc`); **the 13 v1 toolchain pins are byte-identical to `bf97d85` by ORCH-2's own
check, 13/13**, now cited lane+commit+blob instead of a sandbox path; the **B1 zero is explicit** with its
consequence (B1 gets no validation; v1's B1 hold stands) and ORCH-2 reproduced the holdout side from the inherited
census as **185 = A1 162 + A2 15 + B2 8 + B1 0**; **one-shot discipline verified in code** (`m4_q4_supplement.py`
has 0 references to `overlays`, `parse_book_store` or `run_tuning` — it cannot read the corpus); PATTERNS §5d's
wrong "dominated by sampling noise" claim is **left readable and contradicted in place**, with ORCH-2's own
arithmetic confirming ratio **0.16323**, C2-format **8.0 / P=0.9363**, C1-drop **19.9 / P=7.677e-05** and the v1 leg
**1149 × ratio = 187.6 / P=0.4451**; all three stale ledger-digest lines carry appended SUPERSESSION blocks naming
`findings/PROVENANCE.json` as the binding of record (verified `outputs.ledger.jsonl` = `d42136c6…` = the ledger at
head); and q5's numbers are corrected append-only, including the unit-size tally that **ORCH-2 re-derived exactly
from the ledger's 938 A1 claim notes** (k=1 248 · 2 179 · 3 92 · 4 124 · 5 84 · 6 63 · 7 57 · 8 30 · 9 21 · 10 20 ·
11 11 · **12 9**; sum 938; max 12 with 9 claims → `kmax=16` is max-observed + 4 tokens headroom).

**Owed:**
- **Item 8a (extended):** the q4 supplement's `tool_commit ffb8811` does not contain `tools/m4_q4_supplement.py`
  (introduced by `d7fee6e`). Item 8a now covers **all six supplement artefacts** (q2 ×3, q3 ×2, q4 ×1). Convention:
  `tool_commit` = lane head at run time is acceptable **only** alongside `generator_tool` +
  `generator_tool_commit` + `generator_tool_sha256`.
- **Item 11a (20.11 precision):** publish the tuning-side count per row (**1149 / 49 / 122**) so all three rows of
  the §5d table recompute, and reconcile the published **187.9 / 0.44** with the census-supported **187.6 / 0.4451**.
  The conclusion is unaffected: v1 consistent, C2-format consistent, C1-drop a real ~4× deficit at P ≈ 7.7e-05.
- **Item 11b (20.12 residual):** `tools/PATTERNS.md §5e` still reads "All **98** … units **up to 11**" with no
  supersession note. Append the same treatment (98 → **97 = 9 + 61 + 27**; max unit **12** with 9 claims; cite the
  reconciliation doc). **Restriction until then: §5e may not be quoted for those two numbers.**
- **Item 12 + criterion 20.14 (recurring defect):** four appended notes carry fuzzy timestamps — the three
  SUPERSESSION blocks (`21:4xZ`), PATTERNS §5b-bis (`21:5xZ`) and TASK-017's `materialised_utc` (`20:5xZ`, item
  17.a). Apply the pattern this lane already owns in `fixtures/v2/dropword.json`: an exact value **plus its source**
  (the committer timestamps of `d7fee6e` / `4fc40c8` / `b2e0761` recover them), the fuzzy value superseded and left
  readable. **Criterion 20.14: every appended note and every manifest timestamp is exact to the second and carries
  its source.**

**TASK-020 overall stays FAIL/INCOMPLETE** — outstanding: 8a, 8b, 11a, 11b, 12, criterion 20.13.
**Consequence of this gate: q1, q4 and q5 RE-GATE PASS** (see `fleet/GATES.md`); **q3 is unblocked by item 8a alone**;
q2 waits on 8a/8b plus TASK-018 items 0d–0g.


---

## Items 13 and 14 + criteria 20.15 and 20.16 (ORCH-2, 2026-09-25T23:09:35Z) — cut from the verification ledger, not from a delivery

Both items come from `fleet/ORCH-2-VERIFICATION-LEDGER.md` §1.8, §1.9 and §1.18. Neither is a comparability failure —
ORCH-2 established comparability independently — but both are cases where **a published number does not reproduce when
the published method is followed literally**, which is the same defect class as q5.8 and item 11a. Since
`findings/PROVENANCE.json` was designated the **binding of record** by the item-11 repair, its derivation notes must be
literally executable.

### Item 13 — `findings/PROVENANCE.json` `derivations` must reproduce as written (criterion **20.15**)
- **`fixtures_digest_sha256` (`c5d8f6f3…`)**: the note says *"same construction as records_digest over the fixtures
  dir"*, but `records_digest` keys lines by **path relative to the records dir** and that construction does **not**
  reproduce `c5d8f6f3…`. ORCH-2 reproduced it **only with basename keys over the two files in `fixtures/confirmed/`**
  (`confirmed.json`, `corrections.json`) — consistent with `fixtures_files: 2`. State the key convention (**basename**)
  and the exact input set, and note that `fixtures/clean/`, `fixtures/negative/` and `fixtures/v2/` are **outside** this
  binding (so the later addition of `fixtures/v2/dropword.json` did not silently alter the M5-R binding — worth saying
  explicitly, because it is a virtue of the current state that the digest does not prove).
- **`overlays_digest` wrong-variant warning (`58274f46…`)**: ORCH-2 reproduced it **exactly** as
  `sha256("\n".join(sorted(lines_without_trailing_newline)))`. The manifest says only *"sorting the resulting lines
  instead gives 58274f46… (do not)"* — eight other plausible variants give eight different values (`837e4bb3…`,
  `5b09dbac…`, `8cc3ddd4…`, `49252338…`, `b16f9b4f…`, `a363846a…`, `50aca054…`, plus the correct `027f82a0…`). State
  the join exactly so the warning is checkable.
- **Criterion 20.15:** *every derivation method stated in a manifest reproduces the published value when followed
  literally; where a wrong variant is warned against, its exact construction is stated; and every digest publication
  states its canonicalization (JSON `sort_keys`/`separators`, key convention, join).* The good pattern already exists
  in this lane: `runs/m4-q2-dropword/PROVENANCE-SUPPLEMENT.json` publishes
  `config_digest_note: "sha256 over json.dumps(params, sort_keys=True, separators=(',',':'))"`.

### Item 14 — the q4 supplement's config digests publish a subset (criterion **20.16**)
- The q4 holdout supplement's **format-leg** `config` object contains **only** `rules` (digest `805241dd…`), while the
  q3 tuning supplement publishes `abbreviations` (38 entries) + `excerpt_chars` (60) + `rules` (digest `8e7e35a2…`).
  A reader comparing the two digests would conclude the configurations differ. **They do not:** ORCH-2 re-read the
  pinned detector `tools/det_format.py` (`ef9ff4f2…`, byte-identical at head) and found `ABBREV` = **38** entries
  **set-equal** to q3's published list, and `EXCERPT = 60` == q3's `excerpt_chars`. The seven-rule list is identical in
  both supplements. **The exposure comparison in PATTERNS §5d therefore stands** (ledger §3.6).
- The **drop leg** needs nothing: `40945872…` is published identically by the q2 and q4 supplements over all eight
  parameters — comparability by digest.
- **Repair:** publish the complete configuration in force for the format leg (or state the subset relation and that the
  remainder is baked into `det_format.py` at its pinned sha), and adopt the q2 supplement's `config_digest_note`
  pattern in the q4 supplement for all three legs.
- **Criterion 20.16:** *a published config digest covers the complete configuration in force for the run; if a subset is
  published, the subset relation and the location of the remainder (file + pinned sha) are stated in the same object.*

**Priority unchanged:** these are hygiene items — queue position **4**, after 8a, TASK-018 0d–0g and TASK-019 v2.a/v2.b.


---

## Item 12 EXTENDED — the timestamp census is now mechanical and complete (2026-09-25T23:27:53Z)

`fleet/gate-tools/orch2_verify.py` §6 enumerates every timestamp site under criterion 20.14 (details and the full site
list in `fleet/ORCH-2-VERIFICATION-LEDGER.md` §8.1). The scope of item 12 is therefore **larger than first cut**:

- **26 fuzzy timestamps asserted** across 10 files of the worker tree — `fleet/LOG.md` (11), `tools/PATTERNS.md` (4),
  `fleet/branches/WORKER-2-M5R-DELIVERY.md` (4), `findings/M4-q5-A1-CLAIM-RECONCILIATION.md` (2), `findings/README.md`,
  `fleet/branches/WORKER-2-TASK-019a-DELIVERY.md`, `fleet/branches/WORKER-2-TASK-020-DELIVERY.md`,
  `runs/m4-q4-holdout/README.md` (`21:3xZ`, a site not previously catalogued), `tools/INHERITED-V1-MANIFEST.json`,
  `fixtures/v2/dropword.json`. Plus **4 sites that quote a fuzzy value in order to supersede it — not instances**.
- **1 own-time-field offender**: `tools/INHERITED-V1-MANIFEST.json` → `materialised_utc` (**TASK-017 item 17.a**).
  `fixtures/v2/dropword.json`'s fuzzy `generated_utc` is **compliant**, because the same object carries
  `generated_utc_exact` + `generated_utc_exact_source` — that is the repair pattern, and the instrument reports it as
  INFO rather than flagging it.

**Proportionate repair, in this order.** (1) **Load-bearing** timestamps — anything that identifies a run, a
generation, a materialisation or an appended correction, and so must be orderable against a commit — become exact to
the second with their source: the three SUPERSESSION blocks, PATTERNS §5b-bis and §5d/§5e correction notes,
`runs/m4-q4-holdout/README.md`'s item-10 correction, and `tools/INHERITED-V1-MANIFEST.json`. Committer timestamps of
`d7fee6e` / `4fc40c8` / `b2e0761` recover them. (2) **Narrative** timestamps (`fleet/LOG.md`, delivery-note prose) may
stay date-plus-minute **provided the commit sha is cited beside them**. (3) Everywhere a fuzzy value is *quoted*, put
it in backticks so an audit can tell citation from assertion — ORCH-2 has adopted the same rule for its own records,
which the self-audit shows carry **11 asserted fuzzy values** of their own.


---

## Item 15 (NEW) + criteria 20.13 / 20.15 mechanized (ORCH-2, 2026-09-26T00:22:41Z, at head `4fc40c8`)

Both defects were found while restoring the q2.6 figure `113/9` (see `fleet/GATES.md` self-correction #3 and
`fleet/ORCH-2-VERIFICATION-LEDGER.md` §14). They are coherence defects, not comparability failures, and both are now
FAIL rows in `fleet/gate-tools/orch2_verify.py` §13, so each repair flips a row.

### Item 15a — `EVAL.json`'s reconciliation note misnames the row it explains
`runs/m4-q2-dropword/EVAL.json` → `shape_adjudication.count_reconciliation.note` attributes the gate-listed
hyphen-tokenization case to `A_Review_of_the_Work_Sep_2007_Part_1_enxautogen_html.txt` @40831. That transcript
carries **zero** q2 signals. The row is
`Positionality_and_Duality_Transcending_the_Opposites_Apr_2002_Part_2_enxautogen_html.txt` @40831–40841, book side
`the_evolution_of_consciousness` @307559 (`"States. One-third of the"` → `"states the"`, dropped
`['one-third','of']`). **Repair:** correct the transcript append-only, or state why two files are in play. A note that
misnames its own row is the same class as a seal that binds a stale digest (item v2.a).

### Item 15b — two different sets of 114 signals are published under one number
- **filter-side** `filtered: 114` (`PROVENANCE-SUPPLEMENT.json`, `EVAL.json`) = 122 − 1 source-inherited
  (`quite` @457, D-039) − 7 deferred v2-holdout signals.
- **shape-side** *"this instrument finds 114 deletion-closing signals"* (`count_reconciliation.note`) = 122 − 3
  `dropped-token-not-missing` − 5 `partial-overlap`; the published bound then removes the ninth row (the gate-listed
  hyphen case) to reach **113**.
- **Intersection 106 · 8 differ in each direction · the two exclusion sets are disjoint (0 overlap).**
`runs/m4-q2-dropword/README.md` explains 113 vs 114 on the shape side; nothing states that the filter-side 114 is a
*different set*. **Repair:** wherever either figure is quoted, name which set it is (one sentence in the supplement
and one in `README.md` is enough). Same rule as the token convention travelling with `8/122`.

### Criterion 20.15 / item 13 now has its own FAIL rows (§14 of the instrument)
`findings/PROVENANCE.json` publishes seven `derivations`. Followed **literally**, **6/7** reproduce; the failure is
`fixtures_digest_sha256` — "same construction over the fixtures dir" gives `ee56250d001f…`, while the published
`c5d8f6f3db3b…` needs **basename** keys over the **2** files in `fixtures/confirmed/`. **5/7** state their
canonicalization; unstated are `fixtures_digest_sha256` and the `overlays_digest` warning variant, which reproduces
exactly as `sha256("\n".join(sorted(lines_without_trailing_newline)))` = `58274f46…` but is not specified, so the
warning is uncheckable as written. **Repair (item 13, unchanged in substance):** state the key convention and input
set for the fixtures digest — and say explicitly that `fixtures/clean/`, `fixtures/negative/` and `fixtures/v2/` are
outside that binding, which is why adding `fixtures/v2/dropword.json` did not silently alter the M5-R binding — and
state the join for the warned-against overlays variant.

### Criterion 20.13 / L10 status
Coherence is now measured rather than asserted: the shape tally recomputes to the published counts (113/5/3/1), the
reconciliation arithmetic closes (122 = 113 + 3 + 6), ORCH-2's rule-A exclusions are set-identical to the worker's
eight (8 = 8, both directions), every adjudication row carries the fields its class owes (item 0g's schema gap is a
separate row), and `PATTERNS.md §3`'s `57/122` is still quoted **without** the exclusions behind it — three FAIL rows
in total (15a, 15b, the unqualified count). **TASK-020 overall stays FAIL/INCOMPLETE**; outstanding: 8a, 8b, 11a,
11b, 12, 13, 14, **15a, 15b**, plus criteria 20.13 / 20.15 / 20.16, and TASK-018's 0d–0g.


---

### Item 12 census at WORKER-2 `72104a5` (ORCH-2, 2026-09-26T00:52:53Z) — **26 → 27 asserted fuzzy instances**

The mechanical census of asserted fuzzy timestamps grows by one at this head: `fleet/branches/WORKER-2-TASK-019b-PREP.md`
carries the header **`2026-09-25T21:5xZ`** — fuzzy, and ~2.6 h **before its own commit** (`14255bd`, `2026-09-26T00:31:39Z`).
It is recorded as **item v2.f** in `TASK-019.md` because it arrived with the seal-audit delivery, but it is item 12's class
and is repaired by item 12's rule (exact UTC + its source; load-bearing sites first).

Two related instances in the same delivery are **not** fuzzy-timestamp cases but the same family, and are tracked there:
`SEAL-AUDIT.json.audit_utc` is exact-shaped but **forward-stamped** and **contradicted** by the appendix's own citation of it
(item **v2.c**). Item 12's census row (criterion 20.14a) reports **27** at `72104a5`; criterion 20.14b's own-time offender
list is unchanged at 1 (`tools/INHERITED-V1-MANIFEST.json`), because `audit_utc` is shaped to the second — which is exactly
why v2.c is its own item rather than a census entry.
