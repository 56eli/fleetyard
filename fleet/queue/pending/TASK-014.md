# TASK-014 — M4: formal self-improvement loop (PATTERNS.md + detectors + held-out validation)

**STATUS UPDATE (ORCH-2 2026-09-26T09:55:22Z, gate cycle L at WORKER-2 `f5e2cf5`) — TASK-014 is PASS on all five questions.**
q1 **PASS** · q2 **PASS** · q3 **PASS** · q4 **PASS** · q5 **PASS**. q2 closed on item **0h** (a disposition's utc may not
post-date its carrying commit, and its `utc_source` must be true) plus the disclosed amendment of item 0g (ledger §24.4:
the row had demanded byte-identity for lines criterion 20.14c ordered repaired; 15 of 137 lines differ, only the four stamp
fields, every prior `utc` preserved verbatim with a reason, **no substance field moved**; mutation-tested T32–T34 and
regression-checked at `34db0b0`, where the same 13 FAILs still report). q3 closed on its published `config_digest_note`
(criterion 20.15b), which the row re-derives rather than trusts. The owner's park on q2 ("do NOT gate before M5-R PASS")
expired when M5-R PASSed in cycle K, so gating q2/q3 now is inside the standing order. **What PASS does not mean:** every
precision cell stays **unmeasured** and every detector stays **not promotable** until sealed split v2 has been evaluated once
(quantum b) — that is a correct state, not a defect, and it is TASK-015's remaining gate.

- q1 GATE (ORCH-2 2026-09-25T20:08:32Z): **FAIL / INCOMPLETE** on q1.4d only (PATTERNS.md quotes the M5-R
  ledger's figures with no binding to its digest); q1.1/q1.2/q1.3/q1.4a-c **PASS** — the
  split is verified clean, deterministic, reproducible by me byte-for-byte (holdout 37 /
  tuning 193; corpus_files_sha256 9ae90185… reproduced; fixtures forced TUNING; seal
  unmoved since 593cad3), all 16 fixtures wired, every precision cell unmeasured.
  Repair = TASK-018 item 0b (append-only binding + pause-removal line). **No activation
  pause issued** — artefact-scoped restriction instead, reasons in fleet/GATES.md 20:08Z:
  q1 may not be cited as passed, no M4 promotion or q2-q5 gate credit, no M6 figure may
  rest on PATTERNS.md until the binding lands.
- q3 GATE (ORCH-2 2026-09-25T20:44Z): **FAIL / INCOMPLETE** on q3.2 (no fixture-recall result;
  PATTERNS.md §3 line 45 still says "speaker/format — not built"), q3.3 (no clean-set run) and
  q3.5 (§8 manifest missing tool_commit/policy_sha256/main_head/output digest; detector_sha256
  c322e053 binds 4425763 while head is ef9ff4f2 — q4 changed only the runner, proved by diff +
  my byte-identical reproduction). **PASS** q3.1/q3.4 (gap: camel-glue 35/18 not reproducible;
  double-word 3436/228 exact)/q3.6/q3.7 (reproduction byte-identical 86c8f57d; 49/49 citations
  byte-exact)/q3.8/q3.9 (census corroborated by my own probes over all 230). No pause;
  restriction: C2-format not promotable, its 49 signals stay CANDIDATE, no rate/M6 figure.
  Repair = **TASK-020** items 1–6. Addendum 20:58Z: my gate-side clean-set probe measures the
  missing q3.3 number — **1 misfire / 59 known-good book passages** (R1-glued-period on
  power_vs_force @236391 "power.When", book-store typography) and **0/49** shipped signals are
  source-inherited, so q3.7/q3.9 stand.
- q2 GATE (ORCH-2 2026-09-25T20:58Z): **FAIL / INCOMPLETE** on q2.1b (fixture results — the 16
  CF fixtures exist at evidence/fixtures/confirmed/confirmed.json and were never run; PATTERNS.md
  §3 line 44 still says "drop-word — not built"), q2.1c (clean-set results — the 59 hashed
  known-good passages exist and were never run), q2.1d (threshold provenance: all 8 params
  published, none attributed to what it was fitted/measured on), q2.4 (§8 manifests: no
  book-store digest though the detector is book-anchored, no tool_commit/main_head/policy sha,
  no config or per-part output digest, merge manifest has no inputs block, and
  **detector_sha256 84e5407f resolves to NO committed version** — 012914d = 588e1f22, head =
  a0236325; the parts ran 18:57–19:05Z, before the delivery commit) and q2.5 (suite green WITH
  corpus, 26 tests OK 0 skipped, but 26 < the v1 baseline 115 — TASK-017 has not landed and
  tools/{loaders,fixtures}.py are absent at head). **PASS** q2.1a (self-test rc=0 with a
  negative control, 8 tests), q2.3 (keys == tuning 193, ∩holdout 0, all 6 parts' reads ⊆ tuning
  and their union == tuning, seal 481d8513 unmoved), q2.6 with a quantified caveat (my re-run of
  shards 1 and 3 at head is **byte-identical** — 64a97be5 / 092d6341, 66/193 transcripts and
  93/122 signals; 122/122 transcript spans and 122/122 book citations byte-exact; **113/122**
  fully consistent drops, **9/122 shape-defective** — 3 repetition artifacts, 6 partial-overlap
  of which 2 are my own hyphen tokenization), q2.7 with two coherence defects (fixtures labelled
  DROP-CANDIDATE / CLASS BLOCKED, never CERTAIN; in-sample caveat present; but the file's
  proposed leg-(d) wording ≠ the enacted text, per-fixture proposed_leg a/a/b/b, generated_utc
  fuzzy "19:1xZ"). q2.2 (precision) correctly **PENDING** split v2 = TASK-019. **Gate-side probe
  (mine, not the delivery):** C1-drop misfires **3/59** on known-good book passages — all
  cross-book self-parallels — and that mechanism accounts for only **1/122** tuning signals.
  No pause; restriction: C1-drop not promotable, 122 signals stay CANDIDATE, the 9 shape-defective
  signals excluded from any count, **122 never quoted as an omission count** (≤113, in-sample),
  no rate/M6 figure. Repair = **TASK-020** items 1–7 (+ TASK-018 item 0c for the fixture file,
  TASK-017 for the test baseline).
- q4 GATE (ORCH-2 2026-09-25T21:09Z): **FAIL / INCOMPLETE** on q4.6 (§8 manifests: no book-store
  digest on two book-anchored detector sets, no corpus binding and no output digest at all on the
  v1 leg — v1-holdout.json is 127 KB undigested, no tool_commit/main_head/policy sha anywhere) and
  q4.8 (PATTERNS §5d calls the C1-drop 5-vs-122 gap "dominated by sampling noise"; exposure-
  normalized arithmetic says P(X<=5) = 7.7e-05 — a real ~4x deficit — while v1 fits at P=0.45 and
  C2-format at P=0.94). **PASS** q4.1 (thresholds provably frozen before the run: the q2 tuning and
  q4 holdout params blocks are identical, the rules list is identical, and no commit after the run
  touched either detector), q4.2 (one run per detector set, single run_utc, holdout_consumed true
  in all three manifests), q4.3 (inverse isolation airtight: holdout_reads == the 37 holdout names,
  transcripts_read ∩ tuning = 0), q4.4 (counts only, no precision/rate/promotion, A4 correctly NOT
  run; defect: the manifest omits the explicit zero for B1-contradiction), q4.5 (all 13 pinned v1
  tool shas are byte-identical to origin/arena/01a0d581-fleetyard:tools/*.py — attributable;
  defect: cited by absolute sandbox path and evidence/tools/ is not in the committed tree, so the
  v1 leg cannot be re-run from this checkout until TASK-017 inherits it), q4.7 (**the reproduction
  receipt verifies on my own arithmetic**: recount = 185 signals, A1 162 / A2 15 / B2 8 / B1 0, and
  per-transcript counts match the committed m5-raw records for all 37 holdout files with 0
  mismatches). q4.9 (precision/recall/FP counts/promotion decisions) = **NOT GATEABLE**, transferred
  to TASK-019b on split v2. **I did not re-run the spent holdout** — every check was arithmetic over
  committed artefacts or a blob comparison against the read-only archive lane. No pause;
  restriction: 185/5/12 are a receipt only (never a rate, never precision, never an M6 figure),
  C1-drop's exposure-normalized deficit blocks its promotion and must be characterized on split v2,
  B1 stays unvalidated so v1's B1 headline hold stands. Repair = **TASK-020** items 9-10.
- q5 GATE (ORCH-2 2026-09-25T21:17Z): **FAIL / INCOMPLETE** on q5.7 (three live documents still
  present the q5-era ledger digest 64977c2f as CURRENT while the ledger at head is d42136c6 —
  findings/README.md line 88, findings/M4-q5-A1-CLAIM-RECONCILIATION.md, fleet/branches/
  WORKER-2-M5R-DELIVERY.md line 80; cause: TASK-016's regeneration a4c6655 rewrote the record
  shape two minutes after q5; under the fail-closed digest rule a reader following those lines
  rejects valid findings) and q5.8 (published numbers do not reproduce exactly: claimed unit sizes
  run to k=12 not "~11" so kmax=16 has 4 tokens of headroom; my pre-q5 simulation flags 97 =
  9 zero-ASCII-token + 61 over-bound + 27 ASCII-mismatch against the doc's 98/67; and the hyphen
  labelling nuance is unquantified — I measured **255/938 A1 claims (27%)** as
  tokenizer-sensitive). **PASS** q5.1 (root cause reproduced independently: with my own code and
  the Unicode rule, **938/938 A1 claims corroborate, 0 failures** — the instrument was wrong, the
  v1 claims were right), q5.2 (all three worked examples re-derive as described: M5R-0031 9x7,
  M5R-0069 Hangul 4x6 with 0 ASCII tokens, M5R-0036 Mm-hmm 1x8; my recomputation of the ledger's
  span_fully_periodic agrees 938/938), q5.3 (nothing protected moved: ledger d42136c6 = my M5-R
  PASS binding, 1,334 findings, CANDIDATE 1,331 + CERTAIN-inherited 3, detector instances
  A1 938 / A2 158 / B1 12 / B2 228 = 1,336 reconciling with 1,334 findings via two dual-detector
  findings, REVIEW-QUEUE 100 entries at 4e114f1, 2f55b0c and head so nothing was dropped), q5.4
  (both regression tests present at head — test_repetition_rederive_handles_non_latin_and_long_units,
  test_tokenizer_is_unicode_aware; suite Ran 26 OK 0 skipped WITH corpus), q5.5 (errata #2 recorded
  in README + SUMMARY, supersedes errata #1's table without deleting it, CANON 15 trust-ledger note
  present), q5.6 (rule-quality conclusion only; no rate, no certification, coverage row intact, no
  class upgraded). **ACCEPTED and carried by me:** the corroboration column PATTERNS §3 quotes
  (938/938 · 158/158 · 12/12 · 228/228 = 1,336/1,336) is now ORCH-2-VERIFIED, which is the receipt
  TASK-018 item 0b and TASK-020 item 3 need when binding those figures. The M5-R PASS is unaffected
  (q5 is an ancestor of 1beadd9 where I issued it). No pause; restriction: q5 not citable as passed,
  the three stale digest lines are not bindings (use findings/PROVENANCE.json), and the doc's
  98/67/~11 figures must not be quoted without my 97/70/12 + 255/938. Repair = **TASK-020** item 11.
- M4 GATE SWEEP COMPLETE (ORCH-2 2026-09-25T21:17Z): q1 FAIL(1 criterion) · q2 FAIL(5) ·
  q3 FAIL(3) · q4 FAIL(2, precision NOT GATEABLE -> TASK-019b) · q5 FAIL(2). **No M4 quantum is
  citable as passed; no detector is promotable; no rate exists.** One recurring shape across all
  five: LAW §8 bindings that do not resolve (detector digests pinning uncommitted or older blobs,
  missing book-store/tool_commit/policy/output digests, one counterfactual "current ledger" line)
  plus shipping evidence that was available and unrun (16 CF fixtures, 59 hashed clean passages).
  Substance, where I could test it, held: reproductions byte-identical (q3 whole run, q2 shards
  1+3 = 93/122 signals), citations byte-exact (49/49 and 122/122 + 122/122 book refs), isolation
  airtight both directions, the q4 one-shot discipline provable, the q4 reproduction receipt true
  (185/185, 0 mismatches) and the q5 root cause reproduced (938/938). Repair is ONE task
  (TASK-020, items 1-11) behind TASK-018, then TASK-017, then split v2 (TASK-019a seal /
  TASK-019b one-shot evaluation), then M6 FINAL (TASK-015, still BLOCKED).
- sequencing note (ORCH-2 2026-09-25T20:58Z, supersedes part of the 20:02:49Z line and the
  "gates run AFTER TASK-018 lands" line below): I gated **q3 then q2** ahead of TASK-018 because
  every criterion I decided is independent of leg-(d) adjudication; the classification-dependent
  items are recorded **PENDING TASK-018** and the 4 fixtures stay provisional until it lands.
  ERRATA-25g (24-hour shift; work as many cycles per turn as the platform allows) is why the gate
  queue was not idled behind a worker task. **q4 and q5 remain ungated**: q4 cannot yield a rate
  without split v2 (TASK-019) and its one-shot holdout is spent; q5 stays parked as an M4 quantum.
- status (ORCH-2 2026-09-25T20:02:49Z): q1 gate **OPEN** (mine, in progress); q2 **PARKED** by owner
  ERRATA-25e §1 (DELIVERED-PROVISIONAL-UNGATED @ `012914d`, not gated, not certified);
  q3 `4425763`, q4 `4e114f1`, q5 `2f55b0c` delivered 19:08-19:16Z, **UNGATED**, parked
  with q2 and now resumable after the M5-R PASS — gating order is q1 → q2 → q3 → q4 → q5.
  Leg (d) (ERRATA-25e §2) governs q2's classification claims; adjudication itself is
  TASK-018, and q4 now owes a FRESH sealed split (the one-shot holdout is spent).
- milestone: **M4** (fleet/PLAN-v2.md) · cut by ORCH-2 (A-2026-09-25-002) 2026-09-25T19:01Z
- claimant: WORKER-2 (A-2026-09-25-001) — actionable only after TASK-016 re-gates PASS
  (PAUSE in force). q1 was delivered before this task existed (commit `593cad3`); it is
  ratified as TASK-014 q1 and gated against the criteria below, not against criteria
  invented after the fact where the delivery is already stronger.
- prerequisites: **TASK-017** (v1 toolchain inherited with provenance) for q2–q4.

## q1 — rule catalog + held-out split (DELIVERED `593cad3`; GATE OPEN, no verdict yet)
Acceptance:
- q1.1 `tools/PATTERNS.md`: every CERTAIN fixture mapped to a pattern + a rule sketch +
  whether a current detector catches it; coverage truth re-derived from the ledger, not
  asserted. (Observed: P1–P7 over the 16 fixtures; 3/16 covered — CF-003, CF-006, CF-015;
  13 invisible. Matches my own re-derivation.)
- q1.2 held-out split **fixed before any tuning** (LAW §9), deterministic, published,
  sealed (method + salt + mod + bucket + corpus digest), with in-sample fixture transcripts
  forced into TUNING and an honesty disclosure about v1's corpus-wide knowledge.
  (Observed: holdout 37 / tuning 193 / 230; `m4_split.py verify` → OK rc=0.)
- q1.3 per-detector status table with precision **unmeasured** and promotable **no** until
  q4; seeded/in-sample figures never presented as precision (LAW §9).
- q1.4 open items I will gate: rule→fixture wiring for all 16; `corpus_files_sha256`
  derivation documented; tuning code demonstrably unable to read the holdout list;
  PATTERNS.md bound to the M5-R ledger digest it quotes.

## q2 — drop-word detector (M2 remainder, never built)
- Ships WITH: self-test, fixture results (which of the 16 confirmed fixtures it catches —
  CF-015 class P5 is the target), clean-set results on genuinely held-out passages, and a
  disclosed threshold-provenance (fitted on what, measured on what).
- Precision/recall only against the q1 holdout (37 transcripts), fixed before tuning;
  tuning runs must not read the holdout; the split's seal must not change.
- LAW §8 manifest for every cache/run: corpus + book-store + split digests, detector and
  config digest, tool commit, policy sha, output digest, run utc.
- Suite green WITH corpus, skip counts reported, test count never drops (campaign baseline
  is v1's 115 — see TASK-017).

## q3 — speaker/format detector (M2 remainder, never built)
- Same shipping requirements as q2, plus an explicit statement of what "speaker/format
  error" means mechanically (speaker label drift, merged/split turns, attribution mismatch)
  and what it cannot see. Unmeasured ≠ zero until it ships.

## q4 — held-out validation of B1/B2 (and the A4 decision) BEFORE any headline rate
- B1-contradiction and B2-misquote validated on the q1 holdout: v1's gate hold stands
  (TASK-005 FAIL / REDIRECT-005 — B1 thresholds were calibrated on the clean set, B2
  filters fitted), so **no headline rate for B1/B2 until this passes on data fixed before
  tuning**.
- A4-confusion: re-admission only with independent fixture recall (v1: 0/16 independent,
  8 seeded) and a genuinely held-out clean-FP measurement; v1's 0/59 is VOID as independent
  FP evidence (owner ERRATA-2026-09-25 §3). Otherwise A4 stays excluded and says so.
- Output: per-detector precision + FP counts on holdout, seeded vs independent reported
  separately, promotion decisions recorded with their evidence; detector promotion requires
  held-out validation + provenance-manifested caches (PLAN-v2 M4).

## q2-q4 precision criteria RE-CUT (ORCH-2 %s) — the one-shot holdout is spent
The q1 holdout (37 transcripts, salt `fleetyard-m4-holdout-2026-09-25`) was **evaluated once**
at 19:12-19:14Z (`runs/m4-q4-holdout/`, `holdout_consumed: true`, counts only, no rate) and is
**spent**: LAW §9 requires held-out data *fixed before tuning*, and both the reducer (errata #2)
and the detector set have moved since. Therefore, for q2, q3 and q4:
- any precision/recall or promotion criterion is evaluated against **TASK-019's fresh sealed
  split v2** (owner-AUTHORIZED, ERRATA-25g §5 @ main 7d033ab; cut 20:35Z) — a **fresh sealed split v2**
  (new salt, dated record, sealed BEFORE any further tuning, evaluated exactly once) — not
  against the spent split, and not against the tuning set;
- **do not re-run the spent split**; it stays on the lane as a receipt, and its counts
  (v1 185 / C1-drop 5 / C2-format 12) remain counts, never rates;
- until split v2 exists and has been evaluated once, every precision cell stays **unmeasured**
  and every detector stays **not promotable** — that is a correct state, not a defect;
- q2's classification claims are gated under the leg-(d) standing guidance in fleet/GATES.md
  and depend on **TASK-018**'s per-finding adjudications (the 122 signals and 4 provisional
  fixtures are signals/provisional until then; detector hits never auto-classify).
Gate sequencing (recorded so it is not read as idleness): **q2 → q3 → q4 → q5 gates run AFTER
TASK-018 lands**, because TASK-018 changes q2's fixture classes and because q4 cannot yield a
rate without split v2. Gating now would produce verdicts on artefacts that are about to move.

## Global boundaries
Frozen corpus · stdlib only · no network · finding = citation · CANDIDATE never in a rate ·
CERTAIN and HIGH reported separately · every CERTAIN becomes a rule + fixture · no
certification language (milestone certification is ORCH-2's, completion is the owner's).


---

## RE-GATES (2026-09-25T22:52:19Z, ORCH-2, at WORKER-2 head `4fc40c8`): q1 **PASS** · q4 **PASS** · q5 **PASS** · q2 and q3 unchanged

Full records in `fleet/GATES.md`. Repaired by TASK-020 (items 1–11) and TASK-018 item 0b, all re-verified at this head
with the invariants intact (ledger `d42136c6…` 1334 records, by-transcript `c1ec4da8…` 230 files, `m5r_reduce.py`
byte-identical `219075a`→`ffb8811`→`4fc40c8`, split v1 `481d8513…`, split v2 `73d86f0d…`, suite **227 OK skipped=1**):

- **q1 → PASS.** q1.4d repaired: PATTERNS binds ledger + by-transcript + `tool_commit dada3e60…` + the worker head the
  figures were read at (`1beadd9…`) + policy, with a written verification procedure and an append-only control note.
  Both digests re-derived by ORCH-2 at this head. Standing notes: the v1 holdout is **spent**, v2 supersedes it, and
  this PASS promotes nothing.
- **q4 → PASS.** q4.6 repaired by the item-9 supplement (all bindings recompute MATCH; **13/13** toolchain pins
  byte-identical to `bf97d85` by ORCH-2's own check; lane+commit+blob replacing the sandbox path). q4.8 repaired by the
  exposure-normalized correction, confirmed by ORCH-2's own arithmetic (ratio 0.16323; 8.0/P=0.9363; 19.9/P=7.677e-05;
  1149 × ratio = 187.6/P=0.4451). **Restrictions: 185/5/12 is a RECEIPT ONLY** — counts, not precision, no rate;
  the **B1 zero** means B1 gets no validation and v1's B1 hold stands; the **spent holdout is never re-run**;
  precision waits on **TASK-019 quantum b**; the C1-drop deficit's two candidate causes stay unestablished.
- **q5 → PASS.** q5.7 repaired (three SUPERSESSION blocks, old lines readable, `findings/PROVENANCE.json` named as the
  binding of record and verified equal to the ledger at head). q5.8 repaired (98/67 superseded by 97 = 9 + 61 + 27;
  unit-size bound published **with a tally ORCH-2 re-derived exactly from the ledger**: max k = 12, 9 claims, sum 938;
  `kmax=16` reframed as max-observed + 4 tokens headroom; 255/938 = 27% hyphen sensitivity recorded as the gate's
  figure with its caveat). Substantive conclusion unchanged and twice independently verified: the flags were **reducer
  instrument defects**, and **A1 corroboration is 938/938**. **Restriction:** PATTERNS §5e still carries "98" and "up
  to 11" (TASK-020 item 11b) and may not be quoted for those numbers until corrected; the 27% hyphen sensitivity must
  accompany any reuse of 938/938.
- **q2 → still FAIL/INCOMPLETE.** Items 1–8 repaired q2.1b/c/d, q2.4 and q2.5 in substance, but item 8a (tool-pin
  attributability) is outstanding and **q2.2 now runs through TASK-018**, whose adjudication set carries items 0d–0g.
  The 122 signals stay CANDIDATE; the 57 stay restricted.
- **q3 → still FAIL/INCOMPLETE on one point only: item 8a.** q3.2/q3.3/q3.4/q3.5 are verified repaired (fixture recall
  0/16, clean set 1/59 with the misfire shown to be the book store's own typography byte-exact, §8 bindings all
  recomputing MATCH, threshold provenance for all seven rules, five reproducible rejected-rule probes). **Item 8a alone
  unblocks the q3 re-gate.**

**M4 scoreboard after this cycle: q1 PASS · q2 FAIL/INCOMPLETE · q3 FAIL/INCOMPLETE (one item) · q4 PASS · q5 PASS.**
Unchanged: no detector promotable, no precision, no rate, no M6 figure; TASK-015 (M6 Final) BLOCKED behind TASK-019
quantum b; M6-P owner-accepted and not re-certified.

---

## M4 SCOREBOARD after GATE CYCLE J at WORKER-2 `1c8a287` (ORCH-2, 2026-09-26T01:54:33Z)

**q1 PASS · q2 FAIL/INCOMPLETE · q3 FAIL/INCOMPLETE · q4 PASS · q5 PASS** — and the q3 re-gate BOSS-2's cycle 51 unblocked
(item 8a) is hereby **issued and recorded**: 8a is CLOSED, and q3's only remaining gap is one field.

| leg | verdict at `1c8a287` | what is outstanding |
|---|---|---|
| q1 | **PASS** (unchanged since cycle G) | — |
| q2 | **FAIL / INCOMPLETE** | TASK-018 **item 0h** (the 15 dispositions' forward-stamped `utc`), TASK-020 **item 13** / criteria **20.15a-b** (`fixtures_digest_sha256`, `overlays_digest`). Items 0d–0g, 8b, 12, 15a, 15b and criterion 20.13 all CLOSED this cycle; the effective split is **49 CERTAIN-leg-d / 73 CANDIDATE** over 48 sites, with 57/65 frozen as adjudicated |
| q3 | **FAIL / INCOMPLETE** | criterion **20.15b** on `runs/m4-q3-format/PROVENANCE-SUPPLEMENT.json`: no `config_digest_note` (the q2 supplement has one). **Item 8a CLOSED** — `generator_pins` verified against `a5dec38`. Its config object is complete (38 abbreviations + `excerpt_chars` 60 + rules), so criterion 20.16's subset clause does not apply to q3 |
| q4 | **PASS** (unchanged) | TASK-020 **item 14** / criterion **20.16** (the format leg's subset) and **20.15b** (`config_digest_note`) are tracked under TASK-020, as at cycle G |
| q5 | **PASS** (unchanged) | item **11b** CLOSED this cycle: §5e's superseded figures stay readable with 97 = 9 + 61 + 27, max unit 12 over 9 claims, delta stated |

Suite floor at this head: **Ran 257 tests, OK (skipped=1)** — up from 244 at `72104a5` (+5 pin-repair, +6 disposition, +2
pre-registered-exclusion tests), so criterion 21.8/A5's "count never drops" holds. Six pinned artefacts are byte-identical
across `72104a5..1c8a287` (`signals.json`, `fixtures-adjudication.json`, `signals-v2tuning.json`, `det_dropword.py`,
`det_format.py`, `m5r_reduce.py`), so **TASK-013's M5-R PASS stands unchanged** and no M4 leg was re-certified.

---

## M4 SCOREBOARD after GATE CYCLE K at WORKER-2 `34db0b0` (ORCH-2, 2026-09-26T02:17:07Z)

**q1 PASS · q2 FAIL/INCOMPLETE · q3 FAIL/INCOMPLETE · q4 PASS · q5 PASS** — q4's remaining item closed, q2 and q3 each owe
one thing.

| leg | verdict | outstanding |
|---|---|---|
| q1 | **PASS** | — |
| q2 | **FAIL / INCOMPLETE** | **TASK-018 item 0h** only (the 15 dispositions' forward-stamped `utc`, criterion 20.14c). Items 13 and 15a/15b closed; `EVAL.json`'s classification still closes over all 122 signals (113 + 3 + 5 + 1) and the effective split is **49 / 73 over 48 sites** |
| q3 | **FAIL / INCOMPLETE** | **criterion 20.15b** only: `runs/m4-q3-format/PROVENANCE-SUPPLEMENT.json` publishes `config_sha256 8e7e35a2…` with no `config_digest_note`. Item 8a closed at cycle J |
| q4 | **PASS** | item **14** CLOSED at this head: the format leg publishes the complete config and its digest equals q3's; all three run objects carry `config_digest_note`. The M5-R reducer change touched q4's generator, and the q4 supplement was rebuilt with its pin refreshed (`9cfd82fa` artefact, pin `d85038c8`) |
| q5 | **PASS** | — |

**TASK-013 (M5-R) was re-gated at this head because `tools/m5r_reduce.py` changed: PASS HOLDS** — the tool at head, run with
the published pins, reproduces `ledger.jsonl` `d42136c6…` and `by_transcript` `c1ec4da8…` **byte-for-byte**, 1334 findings,
242/0 book refs, 0 citation failures, and the regenerated manifest differs only in `tool_sha256`. See TASK-013.md and
self-correction **O-9**. Suite floor **263**.
