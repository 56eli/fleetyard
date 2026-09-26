# ORCH-2 VERIFICATION LEDGER — every figure ORCH-2 has re-derived independently

**Purpose.** One place, per check: the exact method, the expected value and its source, the observed value, and the
verdict — so that any successor orchestrator, the boss, or the owner can re-establish trust in this lane's numbers
without reading 28 CONTROL cycles, and so that no figure quoted anywhere in the lane rests on assertion alone.
Written 2026-09-25T23:06:23Z by ORCH-2 (activation A-2026-09-25-002) at lane head `b112b56`.

**Where the checks ran.** Gate-side worktree `/home/user/gate-scratch/w-4fc` at WORKER-2 head `4fc40c8`, with the
corpus re-materialized read-only by `sh tools/m5r_inputs.sh` (corpus zip `3f36c520…`, 230 overlays, 230 inherited
census record files under `evidence/runs/m5-raw/records/`). Nothing in this document was produced by running a
detector over the corpus; every row is a digest, a re-read, a count or a closed-form probability.

**Suite at this head, my own run:** 227 tests, **OK**, skipped=1 (the M6-report skip).

---

## 1. Bindings and digests (all re-derived at `4fc40c8`)

| # | Check | Method (literal) | Expected (source) | Observed | Verdict |
|---|---|---|---|---|---|
| 1.1 | corpus zip | `sha256sum docdocgo-fixes.zip` | `3f36c520…` (`findings/PROVENANCE.json`) | `3f36c520…` | **MATCH** |
| 1.2 | **book store — path now identified** | `sha256` of `corpus/docdocgo/html/merged-book-texts_json_1.js` | `c0892fcd…` (`findings/PROVENANCE.json` → `book_store.path`) | `c0892fcd…` | **MATCH** |
| 1.3 | **policy — path now identified** | `sha256` of `fleet2/POLICY-MANIFEST.sha256` | `0fe20a60…` (q4 supplement; `findings/PROVENANCE.json`) | `0fe20a60…` | **MATCH** |
| 1.4 | ledger | `sha256sum findings/ledger.jsonl` | `d42136c6…` (manifest `outputs.ledger.jsonl`) | `d42136c6…`, **1334** lines | **MATCH** |
| 1.5 | by-transcript | `sha256` over sorted lines `"<sha256(bytes)>  <relpath>\n"` for every file under `findings/by-transcript/` | `c1ec4da8…` (manifest `outputs.by_transcript_digest`) | `c1ec4da8…`, **230** files | **MATCH** |
| 1.6 | inherited census records | same construction over `evidence/runs/m5-raw/records/*.json` | `d8c93536…` (manifest `inputs.records_digest_sha256`) | `d8c93536…`, **230** files | **MATCH** |
| 1.7 | overlays | `sha256(concat over basenames sorted of "<sha256(text)>  <basename>\n")`, text decoded utf-8/errors=replace | `027f82a0…` (manifest `inputs.overlays_digest`) | `027f82a0…` | **MATCH** |
| 1.8 | overlays **wrong variant** (manifest warns "do not") | `sha256("\n".join(sorted(lines_without_trailing_newline)))` | `58274f46…` (manifest warning) | `58274f46…` | **MATCH — the warning is accurate**; the manifest does not state the join, and eight other plausible variants give eight different values (`837e4bb3…`, `5b09dbac…`, `8cc3ddd4…`, `49252338…`, `b16f9b4f…`, `a363846a…`, `50aca054…`) → **item 13** |
| 1.9 | fixtures binding | same construction, **keyed by basename**, over the two files in `fixtures/confirmed/` (`confirmed.json`, `corrections.json`) | `c5d8f6f3…` (manifest `inputs.fixtures_digest_sha256`, `fixtures_files: 2`) | `c5d8f6f3…` | **MATCH — but only with basename keys**; the manifest's `derivations` says "same construction as records_digest", which uses relpaths and does **not** reproduce it → **item 13** |
| 1.10 | q4 supplement artefacts | `sha256` of each of the three signal files and three provenance files in `runs/m4-q4-holdout/` | `cf8e7a7a…` (127 733 B), `7ffa7a77…` (4 611 B), `a837ab32…` (6 630 B), `1aa37a60…`, `3d2ec2ce…`, `5d935515…` | identical, byte counts identical | **6/6 MATCH** |
| 1.11 | q4 per-leg config digests | `sha256(json.dumps(config, sort_keys=True, separators=(',',':')))` | `19353270…`, `40945872…`, `805241dd…` | identical | **3/3 MATCH** (compact form; indent-2 gives different values — the form must be stated) |
| 1.12 | v1 toolchain pins | for each of 13 files: supplement value vs `sha256(git show bf97d85:tools/<f>)` vs `sha256(tools/<f>)` at head | 13 shas (`census.py 74afce41…`, `det_confusion 8fec0338…`, `det_contradiction 641c8719…`, `det_misquote 3b8d1cd4…`, `det_nonsense 63028d77…`, `det_repetition f1af20a9…`, `fixtures efaf85f6…`, `loaders 3452c95d…`, `report_m6 c7c4288c…`, `retrieval f36f3a6b…`, `run_detectors d7d109c5…`, `sweep_m5 9df1816e…`, `tokenizer 3f9ce9f7…`) | identical on all three legs | **13/13 three-way MATCH** |
| 1.13 | split v1 | `sha256sum tools/HELD-OUT-SPLIT.json` + salt/mod/bucket counts + `corpus_files_sha256` | `481d8513…`, salt `fleetyard-m4-holdout-2026-09-25`, mod 5, 193/37, `9ae90185…` | identical; 193 tuning / 37 holdout re-counted | **MATCH** |
| 1.14 | split v2 | `sha256sum tools/HELD-OUT-SPLIT-V2.json`; my own independent draw | `73d86f0d…`; 33 holdout / 197 tuning, set-equal to my draw | identical | **MATCH** (TASK-019a) |
| 1.15 | reducer | `sha256(tools/m5r_reduce.py)` at `219075a`, `ffb8811`, `4fc40c8` and in the worktree | `6d4bb9ce…` | identical at all four points | **MATCH → the M5-R PASS stands** |
| 1.16 | q4 `tool_commit` attributability | `git cat-file -e ffb8811:tools/m4_q4_supplement.py` | the pin must contain the generator | **exit ≠ 0 — absent** (added by `d7fee6e`) | **FAIL → criterion 20.10, item 8a** |
| 1.17 | other head artefacts | `sha256` of `signals.json`, `adjudication.jsonl`, `SUMMARY.md`, `fixtures-adjudication.json`, `signals-v2tuning.json`, `det_dropword.py`, `det_format.py` | `8d71f57b…`, `82863ab9…`, `0a37118e…`, `61568a9e…`, `b25651e4…`, `a0236325…`, `ef9ff4f2…` | identical | **7/7 unchanged** |

| 1.18 | **config comparability across the tuning and holdout runs** | compare the config objects published by the q2/q3 supplements with those published by the q4 holdout supplement, and re-read the parameters baked into the pinned detectors | **drop leg: `40945872…` == `40945872…`** (q2 tuning vs q4 holdout, identical digest over all eight parameters). **format leg: digests differ (`8e7e35a2…` vs `805241dd…`) because the q4 supplement published a *subset*** — the seven-rule list is byte-identical in both, and the two omitted fields live in the pinned detector: `ABBREV` = **38** entries, **set-equal** to q3's published `abbreviations`, and `EXCERPT = 60` == q3's `excerpt_chars: 60`, both in `det_format.py` = `ef9ff4f2…` | **COMPARABILITY ESTABLISHED FROM THE PINNED SOURCE**, not from the digests → **item 14 / criterion 20.16**: a published config digest must cover the whole configuration in force, or state the subset relation and where the remainder lives |

## 2. M5-R manifest stats re-derived from the ledger itself

| # | Check | Method | Expected (manifest) | Observed | Verdict |
|---|---|---|---|---|---|
| 2.1 | findings | `wc -l findings/ledger.jsonl` | 1334 | 1334 | **MATCH** |
| 2.2 | raw signals | `sum(len(claim_checks) for row in ledger)` | 1336 | **1336** | **MATCH** — the 2-row gap vs 1334 is exactly `M5R-0460` and `M5R-0461`, the only rows carrying **two** claim_checks |
| 2.3 | per-detector claims | count `claim_checks` by `detector` | A1 938, A2 158, B1 12, B2 228 | identical | **MATCH** |
| 2.4 | claims corroborated | count `claim_ok == true` by detector | A1 938/938, A2 158/158, B1 12/12, B2 228/228, 0 failed, 0 not_checked | identical | **MATCH** — **A1 corroboration 938/938 re-derived a third time** |
| 2.5 | coverage | distinct transcripts in ledger | 206 with findings, 24 zero-finding | 206 + 24 = 230 | **MATCH** |
| 2.6 | seeded | rows with `seeded` truthy | 3 | **3** — `M5R-0078`, `M5R-0460`, `M5R-0461`, all in the three fixture-bearing transcripts | **MATCH**, and see §5.3: this is the **M5-R reducer's fixture seeding**, a different mechanism from the TASK-018 adjudication `seeded` flag |
| 2.7 | book refs | count claim_checks whose serialized form mentions `book` | 242 refs, 242 ok, 0 bad, 0 citation_failures | **240** by this crude proxy | **NOT AN EQUIVALENT RE-DERIVATION** — the manifest's counter is not reproducible from the ledger by substring proxy; recorded as a proxy, not as a mismatch |
| 2.8 | A1 unit sizes | regex `claim (\d+)-token` over the 938 A1 claim notes | k=1 248 · 2 179 · 3 92 · 4 124 · 5 84 · 6 63 · 7 57 · 8 30 · 9 21 · 10 20 · 11 11 · 12 9 | **identical, term for term**; sum 938, max k=12 with exactly 9 claims | **MATCH** → `kmax=16` is max-observed **+ 4 tokens headroom**, not "≈11 + margin" |

## 3. Inherited census, exposure and the three Poisson rows

| # | Check | Method | Observed | Verdict |
|---|---|---|---|---|
| 3.1 | census tallies | flatten the 230 per-transcript record lists, bucket by `detector_id`, key transcripts by **extension-stripped basename** against `tools/HELD-OUT-SPLIT.json` | **tuning 1149** (A1 775, B2 220, A2 142, B1 10, `A1+B1` 1, `A2+B1` 1) · **holdout 185** (A1 162, A2 15, B2 8, **B1 0**) · 1149 + 185 = **1334** = ledger rows | **MATCH** with the q4 receipt and with the supplement's `original_values` |
| 3.2 | exposure | total characters of the 193 tuning transcripts vs the 37 holdout transcripts | **12 228 661** vs **1 996 122** → ratio **0.16323** | **MATCH** with PATTERNS §5d |
| 3.3 | v1 leg | Poisson, λ = 1149 × ratio; CDF in log space (`lgamma`) | expected **187.5548**, observed 185, **P(X ≤ 185) = 0.445075** | **MATCH with my q4 gate figure (187.6 / 0.45)**; the worker's published **187.9 / 0.44 does not reproduce** from these inputs → **item 11a** |
| 3.4 | C2-format | λ = 49 × ratio | expected **7.9984**, observed 12, **P(X ≤ 12) = 0.936279** | **MATCH** (published 8.0 / 0.94) |
| 3.5 | C1-drop | λ = 122 × ratio | expected **19.9144**, observed 5, **P(X ≤ 5) = 7.67659e-05** | **MATCH** (published 19.9 / 7.7e-05) — a real ~4× deficit; the §5d claim that the gaps are "dominated by sampling noise" is **wrong for C1-drop** and is now contradicted in place |

| 3.6 | comparability premise of §3.3–§3.5 | the exposure-normalized comparison assumes the **same** configuration on the tuning and holdout sides | **verified** — drop leg by digest equality (1.18), format leg by re-reading the pinned detector (seven rules identical, 38 abbreviations set-equal, excerpt 60) | **PREMISE HOLDS** |

## 4. TASK-018 adjudication set — re-derived byte-exactly at `4fc40c8`

| # | Check | Method | Observed | Verdict |
|---|---|---|---|---|
| 4.1 | rows and verdicts | count `adjudication.jsonl` | **122** rows: **57 CERTAIN-leg-d**, 65 CANDIDATE | **MATCH** |
| 4.2 | span re-read | `corpus_text[span_start : span_end_matched] == span` for every row carrying both keys | **120/120 exact**, of which **57/57 CERTAIN-leg-d** | **MATCH** |
| 4.3 | the two rows without those keys | `D-027`, `D-117` (both CANDIDATE, `span: null`): `corpus_text[char_offset : char_offset+len(detector_span)] == detector_span` | **2/2 exact** (`'mystic the'`, `'make sudden'`) | **MATCH** → **all 122 rows are byte-verifiable**; §4.2's 120/120 must not be padded to 122/122 by comparing `null == null` |
| 4.4 | ground-truth quotes | re-read `ground_truth.quote` from the book store at `ground_truth.char_offset` (fallback: substring search) | **57/57 exact** | **MATCH** |
| 4.5 | restoration | `restored_span` token-equal to `ground_truth.quote` under the stated token rule (alnum plus apostrophe/hyphen inside tokens; everything else a separator) | **57/122** — exactly the CERTAIN rows | **MATCH** (CANDIDATE rows legitimately differ) |
| 4.6 | v1 fixture spans | for each of the 16 `fixtures/confirmed/confirmed.json` entries: `corpus_text[char_offset : char_offset+len(quoted)] == quoted`, cross-checked by `find()` | **16/16 offset-exact**, `find()` agrees on all 16 | **MATCH** — the v1 confirmed fixtures are independently located |
| 4.7 | **fixture overlap — decisive form** | count adjudicated rows living in a fixture-bearing transcript, then interval-intersect | the 16 fixtures live in **3** transcripts (`A_Unique_Sedona_Seminar_Dec_2008_Part_2`, `Love_Sep_2011_Part_1`, `Satsang_Series_Volume_IX_Part_6`); **0 of the 122 rows are in any of them**, so overlaps = **0/122** | **MATCH, and stronger than an interval test** |
| 4.8 | `seeded` on the adjudication rows | count `seeded is True`; count key presence | **0 of 122** true; the key is **present on all 122** with value **`false`**; `in_sample: true` on all 122 | **MATCH** → `SUMMARY.md`'s *"4 of the 57 CERTAIN rows carry `seeded: true`"* is **false**, and so is the same sentence in `PATTERNS.md §5b-bis` → **TASK-018 item 0d** |
| 4.9 | the real seeded rows | `fixtures-adjudication.json` | **4** rows `FIX-D2-001…004`, all `seeded: true` (2 CERTAIN-leg-d, 2 CANDIDATE), in a **separate file** | **MATCH** — the source of the false sentence: the four exist, but not among the 57 |

## 5. Two ORCH-2 instrument defects found and fixed in this pass (recorded so nobody repeats them)

**5.1 — a vacuous overlap test.** My first fixture-overlap test read `fixture['span_end']`, a key that **does not
exist** in `confirmed.json` (its keys are `book_ref, char_offset, confidence, detector, evidence, evidence_class, id,
paragraph, quoted, status, status_by, suspected, transcript`). Every pair hit `continue`, so the test returned
**0/122 for the wrong reason**. An interval test over absent keys cannot fail. Fixed by deriving each fixture span as
`[char_offset, char_offset + len(quoted))` and verifying that derivation byte-exactly first (§4.6), then by the
stronger transcript-level test (§4.7). **The published conclusion did not change, but it now rests on a real test.**
Rule adopted: *any set-level or interval check must print how many comparisons it actually performed; a zero from zero
comparisons is not a result.*

**5.2 — `null == null` counted as a match.** My first span re-read used `.get()` fallbacks, so the two rows with no
matched span compared `None == None` and were counted exact, inflating the result to 122/122. Corrected to **120/120**
plus a separate, differently-keyed check for the two exceptions (§4.3). Rule adopted: *a byte-exactness count must
report the denominator of rows for which the comparison was defined.*

**5.3 — two different `seeded` mechanisms, easily conflated.** The **ledger** carries `seeded` on **3** rows
(`M5R-0078`, `M5R-0460`, `M5R-0461`) — the M5-R reducer's fixture-seeding recall check. The **adjudication** carries
`seeded` on **all 122** rows, `false` on every one, and the **4** `seeded: true` rows live in a different file
(`fixtures-adjudication.json`, FIX-D2). Any statement about "the seeded rows" must say which of the three it means.

## 6. What this ledger does **not** establish

- **No precision, no rate, no recall, no M6 figure.** Nothing here measures a detector against held-out ground truth;
  the 185 / 5 / 12 counts are a **receipt**, and precision is gated behind **TASK-019 quantum b** under the
  pre-registration protocol annexed to `TASK-019.md`.
- **No detector is promotable.** C1-drop and C2-format remain not promotable; the 122 drop-word and 48 format signals
  remain **CANDIDATE / PROVISIONAL-UNGATED**; the 57 CERTAIN-leg-d rows remain **restricted** (band 71/57/33/22,
  strata, site count 55, notation class, D-002/D-039 dispositions — TASK-018 items 0d–0g).
- **§3.6 is a premise check, not a measurement.** Establishing that both sides ran the same configuration makes the
  exposure comparison meaningful; it does not make 5 or 12 a precision figure.
- **§2.7 is a proxy**, not a re-derivation. **§1.8 and §1.9 expose two derivation notes in `findings/PROVENANCE.json`
  that do not reproduce as literally written** — the primary digests do, and that manifest remains the binding of
  record, but its `derivations` block must state the join and the key convention exactly (**TASK-020 item 13,
  criterion 20.15**).
- **B1-contradiction receives no validation** from the spent-holdout receipt (0 rows on the holdout side); v1's B1
  headline hold (TASK-005 FAIL / REDIRECT-005) stands.
- **M6-P** remains owner-accepted and is **not** re-certified here.

---

## 7. The instrument that produces this ledger — `fleet/gate-tools/orch2_verify.py`

Sections 1–5 are now **mechanical**, not prose. `python3 fleet/gate-tools/orch2_verify.py <worktree> --head <sha>`
re-runs every row read-only over a gate-side worktree (corpus materialized by `sh tools/m5r_inputs.sh`) and prints, per
row: expected with its source, observed, verdict, and **`n` = the number of comparisons actually performed**. Run at
WORKER-2 head `4fc40c8` on 2026-09-25T23:15:45Z:

```
== summary: 107 rows · FAIL 7 · INFO 2 · PASS 97 · PROXY 1
```

Full output committed at `fleet/gate-tools/orch2_verify_output_4fc40c8.txt`.

**Rules built in (both were broken by ORCH-2 once — see §5):**
- **R1** — every set-level or interval check reports `n`; a zero produced by zero comparisons is reported as
  **VACUOUS**, never as PASS. The fixture-overlap row demonstrates it: `n=0` interval comparisons were *possible*
  (no adjudicated row shares a transcript with any fixture), so the row is INFO/VACUOUS-by-data and points at the
  decisive membership test (`0 of 122`, `n=122`).
- **R2** — every byte-exactness count reports the denominator over which the comparison was **defined**. Rows lacking
  `span_start`/`span_end_matched` are counted separately and verified by a *different* key
  (`char_offset` + `detector_span`); `None == None` is never a match.

**The invariant that makes this useful: the instrument's FAIL set is exactly the open-item set — no more, no less.**

| FAIL row | Open item |
|---|---|
| `criterion 20.10: tool_commit contains the generator` — ABSENT at `ffb8811` | **TASK-020 item 8a** (extended to all six supplement artefacts) |
| `worker's published v1 row vs the census` — census gives 187.5548 / 0.4451, not 187.9 / 0.44 | **TASK-020 item 11a** |
| `q4 format config digest covers a SUBSET` — `8e7e35a2…` vs `805241dd…` | **TASK-020 item 14 / criterion 20.16** |
| `PATTERNS §5e carries '98'` (unannotated) | **TASK-020 item 11b** |
| `PATTERNS §5e carries 'up to 11'` (unannotated) | **TASK-020 item 11b** |
| `PATTERNS §5b-bis fuzzy timestamp` — `21:5xZ` | **TASK-020 item 12 / criterion 20.14** |
| `PATTERNS §5b-bis repeats the false seeded sentence` | **TASK-018 item 0d** |

INFO rows: split v2's fixtures-adjacent binding (**item v2.a** owed, criterion v2.5) and the vacuous-by-data interval
row. PROXY row: the manifest's `book_refs 242`, which is not re-derivable from the ledger by substring proxy (mine gives
240) and is therefore never reported as a mismatch. **Item 13** produces no FAIL because both derivations *do*
reproduce once the exact construction is known — the instrument records them as PASS **with the note** that the manifest
does not state the join (`"\n".join(sorted(lines_without_trailing_newline))` → `58274f46…`) or the key convention
(basename over `fixtures/confirmed/`), which is precisely what criterion 20.15 asks to be fixed.

**Consequence for the re-gates.** When WORKER-2 lands item 8a the instrument's first FAIL clears and the **q3 re-gate**
is a single run plus invariance check; when items 0d–0g land, the last FAIL clears and the **q2 re-gate** follows the
same way. Any **new** FAIL on a later head is by construction a new finding, not a re-litigation.

### 7.1 Four defects the instrument found **in itself** on its first run (recorded, not quietly fixed)

Two of the four produced **false PASSes** — the dangerous direction, and the reason R1/R2 exist.

1. **Wrong artefact path** → false FAIL: `signals-v2tuning.json` is under `runs/m4-q3-format/`, not
   `runs/m4-q2-dropword/`; the instrument reported ABSENT for a file that is present and unchanged (`b25651e4…`).
2. **Sloppy section slice** → **false PASS**: §5e was sliced as "from the first occurrence of the label to end of
   file", so wording from *later* sections (which do carry supersession language) satisfied §5e's check. Fixed by
   `slice_section()`, which cuts from the heading to the next heading of the same or higher level and reports the slice
   length so an empty slice is VACUOUS, not PASS.
3. **Word-count heuristic** → three false FAILs: comparing the count of `supersed*` mentions to the count of stale
   digest occurrences is meaningless — a correction block quotes the stale digest itself. Replaced by a
   document-level test (every stale line either sits inside a SUPERSESSION block or has one later in the same
   document; the current digest appears; the manifest is named as the binding of record), with the distance reported
   rather than required, because under append-only discipline an inline marker would rewrite history.
4. **Case-insensitive marker matching** → mis-classification that happened to yield the right verdict: lower-case
   "supersedes" from an *older errata about a different subject* sits three lines above an original stale line in
   `WORKER-2-M5R-DELIVERY.md`, so that line was classified as "quoted by the correction". Fixed by requiring the
   uppercase `SUPERSESSION` token for block detection.

**Standing rule adopted from this:** a gate instrument is run against a head whose answer ORCH-2 already knows before
its output is trusted. This one was — every row reproduced the figures in §1–§5, and the four defects above surfaced as
disagreements with results ORCH-2 had already derived by hand.

---

## 8. Instrument v2 — read-scope, signal evidence and LAW §8 completeness (2026-09-25T23:27:53Z)

Three sections were added so that the **q2 and q3 re-gates are also a single run**: §6 read-scope and one-shot
discipline, §7 drop-word signal evidence, §8 LAW §8 manifest completeness. At `4fc40c8`:

```
== summary: 172 rows · FAIL 14 · INFO 11 · PASS 145 · PROXY 2
```

**§6 — the holdout was never read by a tuning-side run, and the spent-holdout run read exactly the 37.**
- q2 supplement: `holdout_reads == []`, `holdout_enforced == true`, `split_counts` == split v2 (197/33/230);
  `signals.json` keys **set-equal to the v1 TUNING 193** (n=193) with **∩ v1 holdout == 0**; `merge.signals_total`
  122 == actual; `merge.signals_sha256` == actual; all **6** part digests match and every part manifest declares
  `holdout_reads == []`.
- q2 filter arithmetic closes exactly: raw **122** − source_inherited **1** = **121**; 121 − deferred_holdout **7** =
  **114**. The 7 deferred are the v2-holdout signals of TASK-019 item v2.b.
- q3 v2 run: `transcripts_read_count` **197** == split v2 tuning; `holdout_reads == []`; `holdout_enforced` true.
- q4: all three provenance files declare `transcripts_read` **set-equal to the 37 spent-holdout transcripts**
  (n=37 each) with **∩ v1 tuning == 0**, and `v1-holdout.PROVENANCE.json` carries `holdout_consumed: true` plus
  `thresholds_frozen_before_run` and the `v1_tool_shas` block.

**§7 — the 122 drop-word signals are byte-verifiable evidence.** Transcript spans re-read byte-exactly **122/122**;
book citations found in the book store **122/122**; `dropped_words` present and contained in the suspected span
**122/122** (after defect #5 below was fixed — it was 114/122 before). The drop-consistency row is reported as
**PROXY, not FAIL**: the mechanical rule encoded here (remove every occurrence of each dropped word, compare token
lists) is *not* the procedure the q2.6 gate used to separate 3 repetition artifacts from 6 partial overlaps, and until
that procedure is encoded this row may not serve as a criterion.

**§8 — LAW §8 completeness.** All three supplements carry the six required keys, an exact-to-the-second `run_utc`, a
book-store binding **or an explicit stated N/A** (the q3 supplement does the latter correctly: *"N/A for this detector
— C2-format never reads the book store (stated, not omitted)"*), status language forbidding promotion and rate, a
**complete `detector_pin_defect` disclosure** (`original_pin` + `defect` + `attribution_bridge`, the bridge naming my
own byte-identical reproductions), and `detector_sha256_at_head` equal to the actual tool digest at head. The q2
README's threshold-provenance section names all eight C1-drop parameters; the q3 README's states the correct answer for
C2-format — **no numeric thresholds, seven shape predicates**.

**FAIL set (14 rows) still maps exactly onto open items:** 20.10 generator pin + three per-manifest generator rows →
**item 8a**; published v1 row → **item 11a**; format config subset + two missing `config_digest_note` rows → **item 14**;
PATTERNS §5e ×2 → **item 11b**; §5b-bis false seeded sentence → **TASK-018 item 0d**; and the two timestamp rows →
**item 12**, now quantified below.

### 8.1 The timestamp census (criterion 20.14), mechanically enumerated

| Row | Result |
|---|---|
| **20.14a** fuzzy timestamps **asserted** in the worker tree | **26 instances** across 10 files — `fleet/LOG.md` (11), `tools/PATTERNS.md` (4: 20:1xZ, 21:2xZ, 21:3xZ, 21:5xZ), `fleet/branches/WORKER-2-M5R-DELIVERY.md` (4), `findings/M4-q5-A1-CLAIM-RECONCILIATION.md` (2), `findings/README.md`, `fleet/branches/WORKER-2-TASK-019a-DELIVERY.md`, `fleet/branches/WORKER-2-TASK-020-DELIVERY.md`, `runs/m4-q4-holdout/README.md`, `tools/INHERITED-V1-MANIFEST.json`, `fixtures/v2/dropword.json` |
| fuzzy values **quoted in order to report or supersede** them | 4 sites — **not instances** |
| **20.14b** an artefact's **own** time field not exact to the second | **1 offender**: `tools/INHERITED-V1-MANIFEST.json` → `materialised_utc` (**TASK-017 item 17.a**) |
| own time field fuzzy but **superseded in-file by an exact sibling** | 1 site: `fixtures/v2/dropword.json` `generated_utc` beside `generated_utc_exact` — **the compliant repair pattern**, reported as INFO, never flagged |
| **20.14c** exact-to-the-second timestamps present | 38 sites |
| **20.14d** minute-precision elsewhere (citations, prose, headers) | 43 sites |
| **§9 SELF-AUDIT of ORCH-2's own lane** | 52 files: **11 fuzzy instances asserted** (`fleet/CONTROL.log` ×3, `fleet/GATES.md` ×6, `fleet/queue/pending/TASK-020.md`, `fleet/queue/status.md`), 19 fuzzy values quoted as citations, **0** own-time offenders, 171 exact-to-second, 66 minute-precision |

**Ruling recorded for item 12.** Exactness is required where a timestamp is **evidence** — a run, generation,
materialisation or appended correction that must be ordered against a commit (minute precision cannot settle whether
the q2 parts ran before their delivery commit at 19:06:53Z; only seconds can). Where a timestamp is **narrative**, a
date plus minute is acceptable **if the commit sha is cited beside it**. **ORCH-2 is an instance of its own criterion**
(11 asserted fuzzy values in this lane's records); they are historical and will not be rewritten, and from this cycle
ORCH-2 (i) stamps its own headers exact to the second and (ii) **backticks every fuzzy value it quotes**, so that an
audit distinguishes asserting a fuzzy timestamp from reporting one.

### 8.2 Five more defects this instrument found in itself (defects #5–#9; #1–#4 are in §7.1)

5. **Curly apostrophes — include is not enough, normalise.** Adding `’` (U+2019) to the in-token character class still
   failed 8 of 122 rows, because the *data* uses `’` while `dropped_words` uses `'`: `tokens("that’s")` → `["that’s"]`
   never equals `"that's"`. Fixed by **normalising** `’`/`ʼ` → `'` before tokenising; the row went 114/122 → **122/122**.
   This is the known "curly-vs-straight apostrophe" gate-instrument defect class, reproduced in my own tool.
6. **Run-level field demanded at part level.** `holdout_consumed` is a property of the **run**; requiring it in each
   `part-holdout-*.PROVENANCE.json` produced two false FAILs. Fixed by reading it where it is declared and reporting
   the part level as INFO — and, in the same pass, by digging into the parts' nested `inputs` block, which turned two
   *unverified* read sets into two **verified** ones (37/37, ∩ tuning 0).
7. **Every generator checked against every manifest.** Looping all `*supplement*.py` tools over all three supplements
   produced meaningless rows (q2's `tool_commit` "lacking" `m4_q4_supplement.py`). Fixed by pairing each manifest with
   its own generator: q2/q3 → `m4_t20_supplement.py`, q4 → `m4_q4_supplement.py`.
8. **A regex that matched the suffix of a correct value.** `"...\d2:\d2Z(?!:)"` matches `38:04Z` inside
   `2026-09-25T20:38:04Z`, reporting **19 false offenders** for own-time fields that are all exact to the second.
   Fixed by `fullmatch` on the value. Rule: *a pattern that classifies a whole value must match the whole value.*
9. **An audit that could not tell asserting from quoting.** The first self-audit reported ORCH-2's own lane as the
   worst offender in the fleet, because gate records **quote** fuzzy timestamps in order to report them. Fixed by
   classifying each hit as `instance` or `citation` from its immediate wrapping and the preceding 60 characters, and
   reporting both. Rule: *a defect census must exclude citations of the defect, and say how it decided.*

Also recorded: the instrument crashed once on a duplicated `note=` keyword argument while these rows were being added —
a reminder that the instrument is code and is subject to the same review as any delivery.

---

## 10. ORCH-2 SELF-ITEM O-1 — a gate figure of mine is WITHDRAWN and restated with its rule (2026-09-25T23:32:36Z)

My q2 gate (criterion q2.6) published the caveat **"113/122 fully consistent drops, 9/122 shape-defective — 3
repetition artifacts, 6 partial-overlap of which 2 are my own hyphen tokenization."** Mechanising it showed that
**no natural rule reproduces 113/9**, so the figure is **withdrawn** and replaced by a rule-stated one. This is the
same standard I applied to WORKER-2's exposure-normalized v1 row (item 11a: *"187.9 does not reproduce from the stated
inputs"*); it applies to my own numbers first.

**Five natural consistency rules over the same 122 signals** (apostrophes — straight *and* curly — normalised, hyphens
inside tokens, every other character a separator):

| Rule | Consistent | Shape-defective |
|---|---|---|
| A — remove **every** occurrence of each dropped word from `tokens(suspected)`, compare with `tokens(quoted)` | **114/122** | **8** |
| B — remove the **first** occurrence of each dropped word | **122/122** | 0 |
| C — `quoted` is a subsequence of `suspected` and the token-count difference equals the number of dropped words | **122/122** | 0 |
| D — `tokens(suspected) − tokens(quoted) == dropped_words` | **114/122** | 8 |
| E — `quoted` appears contiguously inside `suspected` | 8/122 | 114 |
| A again, under a **hyphen-splitting** token rule | 67/122 | 55 |

**The restatement now binding (encoded in the instrument as a PASS row):** under **rule A** with the token rule above,
**8 of 122** signals are shape-defective and **every one of the 8 is a repetition artifact** — the dropped word occurs
more than once in the book-side span, so removing *every* occurrence over-deletes. Examples: `['evidence']` against
`"evidence; evidence of"` → `"evidence of"`; `['staggering']` against `"staggering, staggering. This"` →
`"Staggering. This"`; `['sudden','jumps']` against `"make sudden jumps, sudden"` → `"make sudden"`. Under rule B (remove
the first occurrence) **all 122 are consistent**, which is the semantically right model: the book side repeats, the
transcript drops one copy.

**Two consequences.** (1) The **3 + 6 decomposition is withdrawn** — the defective rows are 8 repetition artifacts, not
3 repetition + 6 partial-overlap; the "partial-overlap" class disappears once apostrophes are normalised (defect #5).
(2) **The token rule is load-bearing and must always travel with the number**: hyphen-splitting turns 114/8 into 67/55.
Any future quotation of this caveat must name rule A, the token rule, and the count 8 — or quote rule B's 122/122 and
say why.

**Effect on the q2 re-gate: none on the verdict** (q2 stays FAIL/INCOMPLETE pending item 8a and TASK-018 items 0d–0g),
but the q2.6 caveat is now precise, mechanised and reproducible instead of a hand count that could not be re-derived.

---

## 11. INSTRUMENT v3 — split v2 and the inherited toolchain mechanized (CONTROL seq 34)

Sections added so that the two remaining re-gates are a single run rather than ad-hoc reasoning. Row count
**174 → 206 · PASS 175 · FAIL 15 · INFO 14 · PROXY 2**. Fresh output at
`fleet/gate-tools/orch2_verify_output_4fc40c8.txt`.

**§10 — TASK-019a split v2 (criteria v2.1–v2.6, items v2.a/v2.b).**

| check | result |
|---|---|
| `corpus_files_sha256` recomputed from the stated derivation | **PASS** — it is a LIST digest (`sha256_text("\n".join(sorted basenames) + "\n")`), not a content digest; my earlier gate note now carries the derivation |
| independent re-draw under `int(full hexdigest) % 5 == 0` | **PASS** — 33 holdout / 197 tuning, SET-EQUAL in both buckets; the alternative reading (`int(first 8 hex)`) gives 28/2 and does not reproduce, so the method statement is executable only under the full-digest reading |
| bucket counts, holdout ∩ tuning | 33/197/230 · intersection 0 |
| zero fixture contamination in the v2 holdout | **PASS** (0 of 6 fixture transcripts) |
| zero spent-v1-holdout transcripts in the v2 holdout | **PASS** (0 of 37) |
| every forced transcript in v2 tuning, each with a stated reason | **PASS** (43/43; `forced_not_by_fixture` empty) |
| criterion v2.5 — seal binds the ACTUAL fixtures | confirmed.json **PASS** (`f2c15869…`); `fixtures/v2/dropword.json` **FAIL** (seal `c8e96319…`, actual `c40d272f…`) → **ITEM v2.a** |
| seal manifest: `tool_sha256` == actual generator, `tool_commit f4ab7bb6b121` contains `tools/m4_split_v2.py`, `run_utc` exact | all **PASS** (attributability here is sound, unlike criterion 20.10) |
| re-seal rule + contamination disclosure present | **PASS** |
| guard is code | `tools/m4_split_v2.py` present; `tests/test_m4_split_v2.py` present with **10 test functions** |
| criterion v2.b | **INFO** — three committed files mention deferral (`EVAL.json`, `PROVENANCE-SUPPLEMENT.json`, `README.md`) and the supplement records `deferred_holdout: 7`, but none enumerates the four transcripts or which three were promoted to D-092/093/094 → **ITEM v2.b stands** |

**§11 — TASK-017 inherited v1 toolchain.** All three legs of the three-way now run over the full manifest, not a
sample: `archive blob == in_archive_sha256` **266/266**, `file at head == sha256` **266/266**, and the manifest's
two per-file claims agree (unmodified) **266/266**; `file_count` 33 + 233 = `file_count_total` 266; `unmodified:
true`; archive lane cited read-only and never re-stamped. **TASK-017 remains PASS all six, item 17.a
(`materialised_utc` own-time) unchanged.**

**Standing caveat carried into v3.** The re-draw reads the *seal's own* method statement; because only one of two
plausible readings reproduces it, a repair that changes the wording must re-run §10 rather than assume the draw
still holds. The contamination and forcing checks are independent of the hash reading.

### 11.1 INSTRUMENT v3.1 — §10 now closes every quantum-a criterion, and found four defects in itself

Row count **206 → 222 · PASS 186 · FAIL 16 · INFO 18 · PROXY 2**. The FAIL set maps one-to-one onto the open
items and nothing else: item 8a (4 rows), 11a, 11b (2), item 12 / 20.14 (2), 20.16 config notes (2), item 14,
TASK-018 item 0d, 20.14b = item 17.a, **v2.5 = item v2.a**, **the v2.b note = item v2.b**.

**Quantum-a criteria now mechanized (v2.1–v2.6, v2.9):**

| criterion | verdict | the evidence the instrument recomputes |
|---|---|---|
| v2.1 | **PASS** | salt differs from the spent v1 salt; `mod 5` / `holdout_bucket 0` / method statement published; my independent re-draw is **set-equal in both buckets** (33 / 197) under `int(full hexdigest) % 5`. The rival reading `int(first 8 hex) % 5` yields 28 / 2 and does **not** reproduce — recorded as a caveat, because it means the method statement is executable under exactly one of two plausible readings |
| v2.2 | **PASS** | `corpus_files_sha256 = 9ae90185…` reproduced from the **written** derivation; it is a LIST digest over sorted basenames, content being pinned separately by the corpus zip |
| v2.3 | **PASS** | 43/43 forced transcripts (6 fixture-bearing ∪ 37 spent v1 holdout) are in v2 TUNING, each with a stated reason; `forced_not_by_fixture` empty; 0 fixture transcripts and 0 spent-holdout transcripts in the v2 holdout |
| v2.4 | **PASS** | seal `293b29c` (20:50:46Z) precedes the commit that **introduced** the split-v2 reference in all 5 declaring artefacts (q3 `1cd5d44` 21:06:12Z; q2 `a5dec38` 21:21:03Z); the TASK-018 adjudication set pre-dates the seal by 12 minutes, so its labels are v1-era |
| v2.5 | **FAIL → item v2.a** | seal binds `c8e96319…` for `fixtures/v2/dropword.json`, actual `c40d272f…`; `fixtures/confirmed/confirmed.json` binds correctly (`f2c15869…`); the fixture entered at `012914d` pre-seal and was modified afterwards |
| v2.6 | **PASS** | `HoldoutGuard` raises `SystemExit` on a holdout name and is instantiated in three tuning-side tools; `det_dropword.py` carries all three named integrity protections, `det_format.py` both of its two; the post-seal v2 tuning run is keyed 197/197 ⊆ tuning with ∩ holdout = 0 |
| v2.9 | **PASS** | the TASK-019a artefact is labelled DELIVERY and promotes nothing |
| v2.b note | **FAIL → item v2.b** | the seal's own text does not state the holdout taint |

**The taint, now DERIVED rather than asserted (item v2.b's expected content).** Reading
`runs/m4-q2-dropword/signals.json` against the v2 holdout and `runs/m4-q2-adjudication/adjudication.jsonl`:

- the pre-seal q2 run was keyed by the **v1 tuning 193**, and **all 33** v2-holdout transcripts sit inside it —
  so every one of the 33 was read before the seal. This is **not** a v2.6 violation (the run pre-dates the seal) and
  the seal's `disclosure` covers it in terms: *"v1 detectors were shaped with corpus-wide knowledge … a first figure
  under v2 is an estimate under this split, not a pristine out-of-sample number."* That sentence must ride along with
  every quantum-b figure.
- **7 signals in 4 holdout transcripts** were deferred by the shipped source-inheritance filter (122 − 1 − 7 = 114):
  `Radical_Subjectivity_The_I_of_Self_Feb_2002_Part_2` ×4, `Realization_of_the_Self_as_the_I_Nov_2003_Part_1` ×1,
  `Spiritual_Traps_Oct_2005_Part_2` ×1, `Witnessing_and_Observing_Oct_2004_Part_1` ×1.
- those same 7 carry **hand labels** from TASK-018: **3 CERTAIN-leg-d** (`D-092`, `D-093`, `D-094`, all in the
  Radical_Subjectivity file) and **4 CANDIDATE** (`D-095`, `D-107`, `D-108`, `D-122`). So 4 of the 33 holdout
  transcripts are already signal-bearing **and labelled**.
- consequence for quantum b, which the pre-registration must decide **in advance**: either a per-file breakdown
  disclosing those 4, or their exclusion with the denominator change stated up front. The instrument now emits both
  facts as rows, so whichever way WORKER-2 decides, the landing check is mechanical.

**Four more instrument defects, published (defects #21–#24; cumulative 24).** Two produced results in the
**dangerous direction** — a false FAIL against a criterion that is in fact sound:

- **#21 — variable shadowing crashed the run.** `seal_t` held the v2 tuning name-set and was later rebound to the
  seal's commit timestamp, giving `TypeError: unsupported operand type(s) for -: 'set' and 'int'`. Renamed to
  `seal_tn` / `seal_ct`. Rule: a name bound to a set is never rebound to a scalar in the same scope.
- **#22 — a file's ADD time is not when a statement entered it.** Testing criterion v2.4 with
  `git log --diff-filter=A` reported `runs/m4-q3-format/README.md` as predating the seal and so **failed a sound
  criterion**: the README was added v1-era at 19:08Z but its split-v2 reference was introduced by `1cd5d44` at
  21:06Z, after the seal. Ordering evidence about a *reference* must use `git log -S <needle>` (pickaxe), which is
  what the row now does.
- **#23 — counting occurrences of one pattern is not counting protections.** Requiring three hits of
  `split integrity violation|not in corpus` falsely failed `det_format.py`, which has both protections it needs but
  words the overlap check differently. The row now checks three **named** protections (both-buckets overlap, tuning
  names in corpus, duplicates across parts) and requires the ones each detector actually owes.
- **#24 — a function assumed the shape of a parameter it never loaded.** `sup['source_inheritance_filter']` raised
  `KeyError` because the caller's `sup` was not the q2 supplement. The deferred count is now read from
  `runs/m4-q2-dropword/PROVENANCE-SUPPLEMENT.json` by the function that reports it.

**SELF-ITEM O-2 (ORCH-2's own lane, owed).** Three of those four defects were a crash or a false FAIL caught only
because I read the output line by line. The instrument has **no smoke test**: nothing asserts that a known tree
yields known verdicts. Owed by me: a `--selftest` mode over a small fixture tree with expected row verdicts, so a
refactor that breaks a section fails loudly instead of silently changing a gate result. Until it exists, every
instrument change must be diffed against the previous committed output — which is why
`fleet/gate-tools/orch2_verify_output_4fc40c8.txt` is committed beside the tool.

---

## 12. QUANTUM-B READINESS — ANNEX amendment §F and instrument §12 (CONTROL seq 36)

Instrument v3.2: **231 rows · PASS 192 · FAIL 17 · INFO 20 · PROXY 2**. The 17 FAIL rows cover **16 distinct open
items** — item v2.a appears twice, once as the criterion-v2.5 row and once as the §12 blocker row, deliberately, so
that the thing standing between the fleet and TASK-015 is visible in the readiness section and not only inside the
split criteria.

**§12 rows (all new).** Frozen-input drift against ANNEX B1/B4: **6/6 match at the worker head** (`det_dropword.py
a0236325…`, `det_format.py ef9ff4f2…`, `m5r_reduce.py 6d4bb9ce…`, ledger `d42136c6…`, policy manifest `0fe20a60…`,
corpus zip `3f36c520…`) plus the book store `c0892fcd…` at its manifest path
(`corpus/docdocgo/html/merged-book-texts_json_1.js`). Holdout 33 as the pre-registration will bind it. The four
label-tainted transcripts **4/4 present by name**; denominators primary 33 / sensitivity 29 pre-declared. Split-v2
file digest at this head `73d86f0d…` (expected to change exactly once, when item v2.a lands). No pre-registration
artefact exists — **the correct state** while v2.a/v2.b are open. No receipt consumes the v2 holdout.

**ANNEX amendment §F (append-only, in `fleet/queue/pending/TASK-019.md`).** Deriving the taint instead of restating
it corrected the ANNEX's own wording: A4 called the four excluded transcripts "fixture-adjacent", but the holdout
contains **zero** fixture transcripts (verified in §10) — what those four carry is **prior hand labels** from the
pre-seal TASK-018 adjudication. §F therefore: names the four and their seven prior verdicts (F1); fixes **primary 33
/ sensitivity 29** from a single run with no third denominator permitted (F2); requires the seven signals to be
**re-adjudicated blind** and a prior-vs-new comparison published, disagreements reported and never silently
reconciled — which turns a disclosure into a measurement (F3, new requirement D3-bis); forbids presenting the seven
as discoveries (F4); restates ERRATA-25e §2 for holdout rows — no auto-promotion, individual reasons and citations,
CANDIDATE never blended, the restricted 57 not a floor (F5); binds the **two caveat sentences** that must ride with
every quantum-b figure, the seal's "estimate under this split, not a pristine out-of-sample number" and the
drop-consistency token rule from self-item O-1 (F6); and makes frozen-input drift machine-checked, with a drift
voiding the pre-registration (F7).

**Instrument defect #25 (cumulative 25), a false FAIL in the dangerous direction.** My first readiness row reported
that two receipts already declared the holdout spent and therefore that the quantum-b run had happened. Both receipts
bind `split_file: tools/HELD-OUT-SPLIT.json` and `split_salt: fleetyard-m4-holdout-2026-09-25` — the **v1** split.
The row now classifies a receipt by the split it actually consumes (v2 split file or v2 salt) and reports the two v1
receipts as expected. Rule: **a consumption claim is only about the artefact it names**; testing "did anyone consume
a holdout" when the criterion is "did anyone consume *this* holdout" produces exactly the false alarm that would have
blocked a legitimate run.

**State after this cycle.** Quantum b remains **HELD** and correctly so: no pre-registration commit exists, item v2.a
is open (so v2.7's frozen inputs are not yet frozen), and item v2.b's note is unpublished. Nothing in §12 indicates
drift or a premature run. TASK-015 M6-FINAL stays blocked behind quantum b; no detector is promotable; no rate, no
precision, no M6 figure; M6-P owner-accepted and not re-certified.

---

## 13. SELF-ITEM O-2 CLOSED — the instrument now has a smoke test, and the smoke test was mutation-tested

`fleet/gate-tools/orch2_verify.py --selftest` needs no worktree and asserts **18 cases**, each named after the defect
or self-item it guards. Output committed at `fleet/gate-tools/orch2_verify_selftest.txt`. The section output is
**byte-identical** before and after the refactor that made this possible, verified by diff against the committed
golden file — that diff is the discipline O-2 asks for, and it is now automated in case T16, which re-counts the
golden file's verdict rows and compares them with the golden's own `== summary:` line.

**Helpers extracted so the tests exercise the real code paths, not copies** (two copies of a rule is how defect #8
happened): `ts_class`, `draw_holdout(names, salt, mod, bucket, reading)`, `drop_rules`, `rule_a_defect`. §7, §10 and
the run-utc row now call them.

| case | what it pins |
|---|---|
| T1 | curly apostrophes are **normalised**, not merely added to the in-token class (defects #5/#19) |
| T2 | em/en dashes are **separators**; gluing them merges two tokens (defect #2) |
| T3, T7 | hyphens stay **inside** tokens — the load-bearing rule of self-item O-1, and dropping a hyphenated token's *half* fails rule A |
| T4 | empty/None inputs tokenize to nothing instead of crashing |
| T5, T6 | a repetition artifact fails rule A and passes rule B; a clean single drop satisfies A–D but not E |
| T8, T8b | a pattern classifying a whole value must **fullmatch** it, and a value that merely *contains* a timestamp is not that timestamp (defect #8's actual mechanism) |
| T9 | a census must tell **asserting** from **quoting** (defect #18) |
| T10 | fixtures store paths, splits store basenames (defect #4) |
| T11, T12 | the draw is deterministic, partitions the corpus, and the two integer readings **disagree** — the mechanical basis of the v2.1 caveat |
| T13–T15 | sha256 known-answer, Poisson CDF known value + monotonicity, `dir_digest` order-independence |
| T16 | the committed golden output agrees with its own summary line |
| T17 | two ABSENT values compare equal, so a `check()` over `.get()` results needs an explicit sentinel (defect #5-class trap, stated so callers guard it) |

**The selftest was itself tested, by mutation.** Five regressions were injected into the helper code and every one
was caught:

| mutation | result |
|---|---|
| revert the curly-apostrophe normalisation | exit 1, **T1** fails |
| `ts_class` uses `search` instead of `fullmatch` | exit 1, **T8b** fails (T8 alone would NOT have caught it — which is why T8b exists) |
| hyphen becomes a separator | exit 1, **T3 + T7** fail |
| `rule_a_defect` stops reporting repetition artifacts | exit 1, **T5** fails |
| the draw defaults to the `hex8` reading | exit 1, **T11** fails |

Honest note on method: my first hyphen mutation produced a **syntax error**, so the mutant exited non-zero for the
wrong reason and proved nothing. It was re-run with a syntactically valid mutation before the row above was written.
A mutation test that crashes is not a mutation test.

**Standing rule from this cycle:** any change to the instrument must (i) pass `--selftest`, and (ii) be diffed against
the committed golden output, with any row movement explained in the ledger before the new output is committed.

---

## 14. SELF-CORRECTION O-3 (the q2.6 figure `113/9` restored), item 13 / criterion 20.15 mechanized, and two new coherence defects

Instrument v3.3: **256 rows · PASS 205 · FAIL 27 · INFO 22 · PROXY 2**, `--selftest` 18/18 before and after. Full
narrative in `fleet/GATES.md` self-correction #3; this section carries the derivation.

### 14.1 O-3 — why O-1's withdrawal was wrong, and what replaces it

O-1 withdrew `113/9` because none of five token-set rules reproduced it. The figure is not a token-set result: it is
the tally of WORKER-2's published per-signal **shape adjudication** (`runs/m4-q2-dropword/EVAL.json` →
`shape_adjudication.signals[*].shape`), whose categories include *"RE-LABELLED — excluded from any count until a
human read"* — a judgement class no token arithmetic can produce. Recomputed from the 122 rows:

```
kind tally      consistent 113 · partial-overlap 5 · dropped-token-not-missing 3 · gate-boundary-excluded 1   (== published counts)
reconciliation  raw 122 = countable 113 + excluded_dropped_token_not_missing 3 + re_labelled_needs_human_read 6
                gate_figure 113 ; 6 = 5 partial-overlap + 1 gate-boundary
deletion_closes True for ALL 122 — so the note's "114 deletion-closing" is a different test: 122 − 8 = 114, then −1 = 113
```

The decisive cross-check: **ORCH-2's rule-A failure set and the worker's 8 shape exclusions are SET-IDENTICAL in both
directions (8 = 8, A−W = ∅, W−A = ∅)**. The ninth row is
`('Positionality_and_Duality_Transcending_the_Opposites_Apr_2002_Part_2', 40831, 40841, ('one-third', 'of'))`, which
passes rule A under the stated token rule and fails under hyphen-splitting — the exact sensitivity O-1 documented, and
the reason the worker excludes it pending a human read instead of calling it consistent.

So `113/9` **is reproducible**, its decomposition is **3 + 5 + 1** (= the worker's `excluded 3` + `re_labelled 6`), and
O-1's claim that the "3 + 6" arithmetic was my own artifact is withdrawn. What O-1 keeps: the token rule is
load-bearing, and the number must never be quoted without its rule. What O-1 additionally got wrong: the caveat's
labels — the six rows needing a human read are five of WORKER-2's partial-overlap rows plus one hyphen row of mine,
not "6 partial overlaps of which 2 are my own hyphen tokenization".

**Method lesson, recorded because it generalizes:** a self-audit must search the *artefact* space, not only the
*rule* space. I looked for a procedure inside my own five rules and concluded the published figure was
unreproducible, when the procedure was published beside the data all along — and my own cycle-F gate record already
quoted it. Corollary now in force: before withdrawing a figure, grep the lane's own prior gate records for it.

### 14.2 Item 13 / criterion 20.15 now has FAIL rows of its own (§14 of the instrument)

Until this cycle item 13 appeared only in the *notes* of two PASS rows in §1, so the standing claim "the FAIL set
equals the open items" was **incomplete** — corrected here and in `GATES.md`. §14 tests each of the seven
`derivations` entries in `findings/PROVENANCE.json` (the binding of record) two ways:

- **20.15a — does the stated method reproduce the published value when followed literally? 6/7.** The failure is
  `fixtures_digest_sha256`: "same construction over the fixtures dir" (relpath keys) gives `ee56250d001f…`, while the
  published `c5d8f6f3db3b…` reproduces only with **basename** keys over the **2** files in `fixtures/confirmed/`.
  Reproduced literally: `by_transcript_digest`, `records_digest_sha256`, `overlays_digest`, `corpus_zip_sha256`,
  `outputs.ledger.jsonl`, `tool_sha256`.
- **20.15b — does each derivation state its canonicalization (key convention, join, sort)? 5/7.** Unstated:
  `fixtures_digest_sha256` (no key convention, no input set) and `overlays_digest`'s warned-against variant — the
  `58274f46…` warning is reproducible exactly as `sha256("\n".join(sorted(lines_without_trailing_newline)))`, but the
  manifest does not say so, which makes the warning uncheckable as written. Eight other plausible variants give eight
  other values, so "sorting the lines instead (do not)" is not a specification.

### 14.3 Two new coherence defects — TASK-020 item 15 (criterion 20.13 / L10)

- **15a.** `EVAL.json`'s `count_reconciliation.note` attributes the hyphen-tokenization case to
  `A_Review_of_the_Work_Sep_2007_Part_1_enxautogen_html.txt` @40831. That transcript carries **zero** q2 signals; the
  row is in `Positionality_and_Duality_Transcending_the_Opposites_Apr_2002_Part_2` @40831–40841 (book side
  `the_evolution_of_consciousness` @307559, `"States. One-third of the"`). A note that misnames the row it explains is
  the same defect class as a digest that binds the wrong file (item v2.a).
- **15b.** Two different sets of 114 signals are published under the same number: filter-side `filtered: 114`
  (122 − 1 source-inherited `quite` @457 − 7 deferred v2-holdout) and shape-side *"114 deletion-closing"*
  (122 − 3 − 5). **Intersection 106; 8 differ in each direction; the two exclusion sets are disjoint (0 overlap).**
  No committed document says so. Any future quotation of `114` must name which set it means.

### 14.4 Items 0e / 0f / 0g derived (§13), so the repairs are checkable

- **0e — the dedupe key is the missing datum.** Over the 57 CERTAIN-leg-d rows: distinct `(transcript, char_offset)`
  = **57**; distinct `(transcript, span text)` = **55**. The published 55 is therefore a **span-text** dedupe, and the
  two collisions are distinct sites at different offsets: **D-097/D-098** (`percent`,
  `Radical_Subjectivity…Feb_2002_Part_2` @838 span-end 852 and @1132 span-end 1141) and **D-120/D-121** (`see`,
  `The_Levels_of_Consciousness…Mar_2002_Part_2` @60506 and @61014). Publishing "55" without its key is a
  criterion-20.15 defect, not a counting error.
- **0f — the strata reproduce exactly under an explicit word list.** ORCH-2's reconstruction over the 32 distinct
  omitted words gives **27 / 6 / 11 / 13 = 57**: interjections/fillers {huh 7, yeah 6, see 6, right 3, really, heh,
  haha, um, well} = 27; notation {percent 6} = 6; function words {it's 3, that's, there's, he'd, may, since, however,
  including, already} = 11; content {bonaparte, earphones, evidence, go, high, lincoln, man, osama, otherwise, quite,
  realms, things, undoubtedly} = 13. This is a **reconstruction, not their classification** — the binding requirement
  is that WORKER-2 publishes its own per-word list, plus the notation-class ruling (ERRATA-25e §2 treats notation
  variants as transcriber formatting conventions) and the statement that speaker-side filler presence is unknowable
  without audio. All three are still ABSENT (three FAIL rows).
- **0g — verified as still open, and its arithmetic verified as right.** `adjudication.jsonl` has **no** disposition,
  ruling or note key in its schema (25 keys, none of them append-only), so neither D-002 (CERTAIN-leg-d while
  `shape_adjudication` excludes that very site as `dropped-token-not-missing`) nor D-039 (CERTAIN-leg-d while the
  source-inheritance filter suppresses exactly that signal as its own published example — confirmed: the filter's
  example IS the D-039 site, `quite` @457) carries a written ruling, and the **7** rows on v2-holdout transcripts
  (D-092, D-093, D-094, D-095, D-107, D-108, D-122) are **0/7** marked as holdout members in the record. If D-002 and
  D-039 are demoted the count becomes **55 rows / 53 span-text sites** — recomputed and confirmed, so the arithmetic
  in the item may be published as stated.
- **20.13 field completeness, adjudicated per row class.** All 122 rows carry verdict, reason, `seeded`, `in_sample`,
  transcript and char_offset; `clause` appears on 57/57 CERTAIN-leg-d rows and on 0/65 CANDIDATE rows, correctly,
  because it is the leg-(d) clause; and D-027 and D-117 have no rebuilt `span` because their own reason states the
  omission is not re-alignable from the frozen bytes, each still carrying `detector_span` + `char_offset` +
  `span_end`. **Instrument defect #26 (cumulative 26):** my first version of that row demanded `clause` on every row
  and `span` on every row, producing 67 false "missing" fields — the same class as defect #6/#12 (a field demanded of
  rows to which it does not apply). Rule: state the row class a field is owed by.

### 14.5 Where this leaves the FAIL set

27 FAIL rows over the open items: item 8a ×4 · 11a · 11b ×2 · item 12/20.14 ×2 · 20.16 config notes ×2 · item 14 ·
TASK-018 item 0d · item 17.a · v2.a ×2 (criterion row + §12 blocker) · v2.b · item 0f ×3 · item 0g ×2 ·
criterion 20.13 ×3 (items 15a, 15b, the unqualified `57/122` in PATTERNS §3) · criterion 20.15 ×2 (item 13).
No verdict moves: q1 PASS · q2 FAIL · q3 FAIL on item 8a alone · q4 PASS · q5 PASS; TASK-017 PASS with 17.a;
TASK-018 FAIL/INCOMPLETE; TASK-019a FAIL on v2.5 + the v2.b note with quantum b HELD; TASK-020 FAIL/INCOMPLETE.


---

## 15. SELF-ITEM O-4 (forward-stamped headers) and §15 of the instrument (quantum-b criteria v2.12–v2.16)

Instrument v3.4: **261 rows without `--self-audit` · PASS 207 · FAIL 27 · INFO 25 · PROXY 2**; `--selftest` 18/18
before and after. Narrative in `fleet/GATES.md` self-correction #4, stamped 2026-09-26T00:20:51Z.

### 15.1 O-4 — ORCH-2 inside its own criterion again

Ten header stamps were written from an estimate rather than from `date -u`; **eight are forward-stamped** relative to
the lane clock (`2026-09-26T00:22:41Z` in five places and `2026-09-26T00:26:04Z` in three, against CONTROL seq 38's
real `2026-09-26T00:16:59Z`), and `2026-09-25T23:58:12Z` in two places was 9 s behind seq 36's real
`2026-09-25T23:58:21Z`. Not cosmetic: commit-order criteria v2.4 and v2.12 are decided on timestamps, and a gate
authority whose headers claim times that had not happened cannot require sourced timestamps of a worker. Disclosed
verbatim and left in place (append-only), with the authoritative CONTROL stamps published beside them. Standing rule:
**the CONTROL.log line is written first and its stamp copied into every header of the cycle.**

Mechanized in `--self-audit`: every exact stamp in the lane's `.md` files is compared against the newest CONTROL.log
entry, and a forward stamp FAILs unless it is disclosed inside the correction section. **Defect #28**: the first
version tested whether the stamp appears anywhere in `GATES.md`, which the offending header itself satisfied — a
disclosure check must look inside the disclosure, not inside the file containing it.

### 15.2 §15 — the quantum-b criteria are pre-registered as rows, so the eventual gate is one run

Three HELD rows state exactly what will be checked when the artefacts exist: **v2.12** pre-registration commit before
the run commit, by add-time and — where a *reference* is concerned — by `git log -S` introduction time (defect #22's
lesson), with both stamps exact and sourced; **v2.13** a receipt that declares the v2 holdout spent with
`holdout_reads` **equal** to the pre-registered eval set, which is the 33 holdout transcripts or the 29 sensitivity
set if ANNEX §F2's exclusion is chosen — whichever is named, no more and no less; **v2.14** eval-directory purity from
that path's own commit history, not from a manifest claim.

Two **precedent** rows PASS today and pin the tests v2.15/v2.16 will apply: on the existing adjudication set the
`seeded` / `in_sample` flags are present on **122/122** rows and `seeded: true` on **0** (an absent flag is as much a
defect as a wrong one — and this is the row TASK-018 item 0d's false sentence contradicts), and
`tools/m4_q4_supplement.py` carries **0** references to the tuning-side readers (`overlays`, `parse_book_store`,
`run_tuning`), which is the source read v2.16 demands of the quantum-b tool: it must not be *able* to reach the tuning
path, and `HoldoutGuard` must be instantiated rather than merely importable.


---

## 16. CRITERION-TO-SECTION MAP — the authoritative coverage claim (CONTROL seq 40, 2026-09-26T00:25:11Z)

Instrument v3.5: **271 rows · PASS 210 · FAIL 27 · INFO 25 · PROXY 9**; `--selftest` 18/18. §16 of the instrument now
asks two questions the gate had never asked of itself: which criteria does it actually mechanize, and does it cite any
criterion that exists in no queue file. Because counting ids in the source is a **proxy** — a section can mechanize a
criterion without printing its id — this map is the coverage claim of record, and the PROXY rows point at it.

| section | what it mechanizes | criteria / items served |
|---|---|---|
| §1 bindings & digests | corpus zip, book store, policy, ledger + line count, by-transcript, inherited census records, overlays (stated method **and** the warned-against variant), fixtures binding, q4 artefact + config digests | TASK-013 C1/C2 lineage · 20.2 / 20.3 / 20.4 · q4.4 / q4.5 · item 14 and criterion 20.16 (config canonicalization) |
| §2 pins | the 13 tool pins to the archive lane; generator attributability | 20.1 · **20.10 = item 8a** |
| §3 manifest stats | corroboration classes 938 / 158 / 228 / 12, k-tally, census rows | q5.1 / q5.2 · q3 census claims |
| §4 census & exposure | exposure-normalized expectation and Poisson tail | q5.3 / q5.4 · **item 11a** (`187.9 / 0.44` vs the census's `187.5548 / 0.4451`) |
| §5 adjudication | the 57 CERTAIN-leg-d rows re-derived byte-exact; the floor sensitivity band 71 / 57 / 33 / 22 | TASK-018 substance · q2.5 |
| §6 read scope + timestamp census | `holdout_reads`, one-shot declarations, part-level read sets; fuzzy / exact / minute census with asserting-vs-quoting classification | q2.7 · q3.8 · **20.14a–d = item 12 and item 17.a** |
| §7 signal evidence | 122/122 transcript spans and book citations byte-exact, dropped words contained; the five-rule sensitivity, the stated rule-A criterion, and the O-3 reconciliation | **q2.6** (substance, though the id is not printed in the row names) |
| §8 LAW §8 completeness | the six required keys, exact run stamps, book-store binding or stated N/A, promotion-forbidding status, the pin-defect disclosure, `detector_sha256_at_head` | q2.8 · q3.9 · q4.6 / q4.8 · **20.16** · **item 8a** |
| §9 self-audit | the same timestamp criteria over ORCH-2's own lane, plus the forward-stamp detector | 20.14 applied to me · **self-item O-4** |
| §10 split v2 | re-draw, contamination, forcing, commit order by pickaxe, guard-is-code, the derived v2.b enumeration and its landing check | **v2.1–v2.6, v2.9** · **items v2.a / v2.b** |
| §11 inherited toolchain | three-way equality over all 266 files, counts, `unmodified`, archive lane read-only | **TASK-017's six criteria** · **item 17.a** |
| §12 quantum-b readiness | frozen-input drift against ANNEX B1/B4, the four tainted transcripts by name, denominators, blocker state, no v2 receipt | ANNEX A/B · **v2.10** |
| §13 coherence | the shape adjudication tally and reconciliation, rule-A set-identity, the two 114s, site dedupe, strata, dispositions | **20.13 / L10** · **items 0e / 0f / 0g / 8b / 15a / 15b** · the O-3 restoration |
| §14 derivations | each of the seven stated derivations, literally, and their canonicalization | **20.15 = item 13** |
| §15 quantum-b criteria | v2.12–v2.14 as HELD rows stating the exact future test; v2.15 / v2.16 precedents that PASS today | **v2.12–v2.16** |
| §16 coverage | per-task id citations (PROXY), the ghost check, and the open-item coverage row | LAW §9's per-criterion requirement, applied to the gate itself |

**The row that matters operationally** is §16's last: **every open item in the queue — 8a, 8b, 11a, 11b, 12, 13, 14,
15a, 15b, 0d, 0e, 0f, 0g, 17.a, v2.a, v2.b — is cited by a row that flips when it is repaired: 16/16.** Two ids had
to be added to reach it: `item 17.a` is now named in the 20.14b row that reports it, and `item 8b` is named in the §13
disposition row it shares with item 0g. So every re-gate the fleet is waiting on is now one instrument run.

**Ghost check: 0.** A row that cites a criterion outside the ruleset invents authority, so every id the instrument
names was checked against the queue files. Two corrections were needed to make the check itself sound: the sub-letters
I coined (`20.14a`–`d`, `20.15a`/`b`) are traced to their **parent** criterion, which must exist; and **defect #29** —
my first id extractor matched the word `closure` inside my own comment, so an extractor must require an id *shape*, not
just a preceding keyword.

**Honest gaps this map names.** (i) **TASK-021's criteria 21.1–21.8 are not mechanized** — the task has not started and
is queued last; mechanization is owed by me when it lands, and until then its gate is by hand. (ii) The `C`-series ids
of TASK-013 / TASK-016 and `L1`–`L9` of TASK-018 are cited only where a row needed them: those tasks are **gated PASS
by hand and recorded in `GATES.md`**, with no re-gate pending, so mechanizing them now would buy nothing. (iii) The
`q`-ids of TASK-014 are mostly uncited because q1 / q4 / q5 are closed and q2 / q3 are open **only** through items that
are mechanized — the scoreboard verdicts live in `GATES.md`, the item rows live here.

## 17. TASK-021 PRE-MECHANIZED BEFORE IT IS CLAIMED — and criterion 21.8's floor corrected by measurement (CONTROL seq 41, 2026-09-26T00:36:26Z)

Instrument v3.6: **282 rows · PASS 217 · FAIL 27 · INFO 30 · PROXY 8**; `--selftest` 18/18; golden refreshed. §16
published one honest gap — *TASK-021's criteria 21.1–21.8 are not mechanized, owed by me when it lands* — and §17
closes it **before the task is claimed**, in §15's pre-registration pattern: whatever can be checked now is a PASS
row, and whatever needs the artefact is a HELD row that states the exact test it will get. The FAIL set is unchanged
at 27: §17 asserts no verdict, it only pre-registers.

### 17.1 What is pinned now, from bytes rather than prose

| fact | value | why it is load-bearing |
|---|---|---|
| the shipped operating point, read from `tools/det_dropword.py` module constants | **8/8** — `window 24`, `stride 12`, `min_score 0.20`, `top_k 3`, `min_matched 10`, `min_ratio 0.85`, `max_drop 2`, `min_flank 3` | criterion 21.2's anchor row is now checkable against source, not against the q2 README's table. The file is byte-identical (`a0236325…`) at both `4fc40c8` and `72104a5` |
| each grid axis contains its own anchor | `min_flank 3 ∈ {2,3,5,8}` · `min_ratio 0.85 ∈ {0.80,0.85,0.90}` · `min_matched 10 ∈ {8,10,14}` | if an axis did not contain the shipped value, "one at a time from the shipped point" would be undefined on that axis |
| the table's expected size | **8 distinct settings** (anchor + 3 + 2 + 2), or **11 rows** if the anchor is repeated per axis | a delivered table of any other size is a deviation the worker must explain, and the gate can say so without judgement |
| both denominators, derived from the split files | v1 tuning **193** / v2 tuning **197**; 33 of the 193 are v2-holdout members | criterion 21.3 requires them beside *every* comparison to the shipped 122 — the failure mode is a bare "122 → N" |

### 17.2 What is held, with the test stated

| criterion | the test §17 will apply |
|---|---|
| 21.1 | `runs/m4-t21-sensitivity/` exists; the HoldoutGuard refusal is in code (not a comment); `holdout_reads: []`; `holdout_enforced: true` |
| 21.4 | the stability set sums coherently with the anchor row: `stable + shipped-only + setting-specific = anchor count` |
| 21.5 | no threshold chosen or recommended; no precision / recall / rate / M6 figure anywhere in the artefacts; every output labelled CANDIDATE-class / PROVISIONAL-UNGATED (grep, not reading) |
| 21.6 | the §8 manifest carries a `tool_commit` that **contains** the generating tool — the exact failure of **item 8a** at `ffb8811…` and `71c37cf…` |
| 21.7 | the dedupe rule **names its key**. Lesson of item 0e, restated as a number: over the 57 CERTAIN-leg-d rows there are **57 distinct `(transcript, char_offset)` sites but only 55 distinct span texts** (`D-097`/`D-098` and `D-120`/`D-121` collide), so "site count" is ambiguous until the key is named |
| 21.8 | the suite stays green **with the corpus present** and the test count does not drop |

### 17.3 A measurement that corrects the queue file

Criterion 21.8 publishes a floor of **217** tests. That is **stale**. Re-run in the `w-4fc` worktree with the corpus
materialised: **`Ran 227 tests in 208.391s` → `OK (skipped=1)`**. So the binding floor at `4fc40c8` is **227 with one
skip reported**, not 217; BOSS-2's cycle 50 reports **244 OK** at WORKER-2's new head `72104a5`, which cycle I will
verify itself. The correction is recorded here rather than edited into the queue file: the queue file is the worker's
specification and the floor it states was true when written — the gate publishes the current number and the derivation.

### 17.4 The coverage meta-gate measured its own gap closing

§16's per-task citation rows are **PROXY** because counting ids in the source does not prove a criterion is ungated.
The TASK-021 row was PROXY at seq 40 (zero ids cited) and is **PASS at seq 41** (all eight cited), so PROXY fell 9 → 8.
That is the confirmation §16 was not decorative: it named a gap, the gap was closed in the next cycle, and the
instrument itself reported the change.


---

## 18. GATE CYCLE I — the worker's seal audit re-derived from git bytes (CONTROL seq 42, 2026-09-26T00:52:53Z)

Instrument v3.7: **306 rows at `72104a5`** (PASS 235 / FAIL 33 / INFO 30 / PROXY 8) · **283 rows at `4fc40c8`** (FAIL 27,
unchanged) · `--selftest` 18/18 · both goldens committed. Full gate record in `GATES.md` ("GATE CYCLE I"), including the
16-claim re-derivation table (13 OK / 3 MISMATCH) and self-corrections **O-5** and **O-6**.

### 18.1 The ruling and why it needed re-derivation

WORKER-2 delivered a tool that audits **its own** seal (`tools/m4_seal_audit.py`, `eb4e4ec7…`) and a verdict of
**STANDING (appendix owed)**. A self-audit is a claim, not evidence, so §18 recomputes every load-bearing number from git
objects. The verdict **survives**: the seal file is byte-identical since `79eb401` (`73d86f0d…`), 6 of its 7 bound digests
recompute MATCH at head, the fixture move `c8e96319… → c40d272f…` is **append-only** (0 keys changed, 0 removed, 63 added;
ids `{D2-001..D2-004}` identical), the single confirmation artefact is **pre-seal by 13m36s** (`1fb524e` @ `20:38:18Z`,
whole history one commit), membership holds (197/33/43, `forced ∩ holdout = ∅`), the draw still reproduces set-equal, and the
tool opens **no transcript bytes**.

Two numbers the worker's artefacts do not contain, derived here: the seal's **`book_store_sha256` binding has no named file**
— identified from `tools/census.py`'s `book_store_bytes` (14,634,979) as `corpus/docdocgo/html/merged-book-texts_json_1.js`
and confirmed by digest `c0892fcd…`; and the fixture file mentions the confirmation artefact at **10 paths**, of which only
**5** are `artifact`+`artifact_sha256` pairs — the tool's unstated key.

### 18.2 What cycle I opened

| | |
|---|---|
| **items v2.c / v2.d / v2.e / v2.f** | forward-stamped + self-contradicting `audit_utc`; missing `tool_commit`; a 5-row citation census against 10 mentions with the key unnamed **and the 5 unpaired mentions outside the void check**; a fuzzy prep-record header taking item 12's census **26 → 27** |
| **item v2.a** | clause (i) substance and clause (ii) **landed and verified**; clause (iii) **half-landed** (the `re_seal_rule` evaluation is there, the *"one draw, not two"* statement is absent everywhere) |
| **item v2.b** | **unlanded** — 0 mentions of the taint in all three new artefacts |
| **quantum b** | **still blocked**, now on four named conditions: v2.b · v2.a (iii) 2nd half · the freeze binding the companion note · ANNEX A2 |
| **O-5** | ANNEX A1 was **unsatisfiable** (it demanded an edit to a file whose digest the appendix and v2.10 both bind) → amended in the open; v2.5 / v2.10 / the BLOCKER row re-worded with their tests. Instrument defect **#30**: expectation text and test must be amended in the same edit |
| **O-6** | my heartbeat file was **1h21m stale** while CONTROL.log ran to seq 41 → mechanized as a `--self-audit` row failing on a >20 min lag (25f's own Class-2 threshold); closed by a disclosing line, not by back-dating |
| **suite floor** | `4fc40c8`: 227 OK (skipped=1) · `72104a5`: **244 OK (skipped=1)** = 227 + 10 + 7. TASK-021's published 217 is doubly stale |
| **ops** | GitHub auth failed mid-cycle (`GH_TOKEN` invalid) → CONTROL 41's `b81e86d` and this cycle are **local-only** until restored; both goldens make every figure reproducible offline. This clone's fetch refspec is **main-only**, so fleet tips are read with `ls-remote` and fetched by explicit refspec |


---

## 19. ANNEX A2 decided before any run, and the "one draw" substance verified (CONTROL seq 43, 2026-09-26T01:00:20Z)

Instrument v3.8: **308 rows at `72104a5`** (PASS 237 / FAIL 33 / INFO 30 / PROXY 8) · **284 rows at `4fc40c8`**
(PASS 218 / FAIL 27 / INFO 31 / PROXY 8) · `--selftest` 18/18 · both goldens refreshed.

### 19.1 The A2 decision (`TASK-019.md` ANNEX §G, binding, recorded with no freeze written and the holdout unopened)

**The v1-era adjudication set is EXCLUDED from the quantum-b evaluation.** No label, denominator or sanity figure may come
from `adjudication.jsonl` (122 rows), `fixtures/confirmed`, `fixtures/v2/dropword` or `PATTERNS.md`; holdout signals are
labelled **fresh and blind** for the run; `seeded` stays separated from `independent` and never counts toward the rate;
unlabelled signals stay `candidate_unlabelled`; and if items **0d–0g** land before the freeze the exclusion is **not** lifted
automatically — lifting needs an amendment to §G **before the freeze**, and after it nothing changes, because the freeze
carries the protocol text into the score file.

Why: 0d–0g are open defects in exactly the artefacts a label-reuse path would read, and quantum b is **one-shot**, so a
known-defective input would enter a figure that cannot be re-run. The exclusion costs nothing measurable — the 33
v2-holdout transcripts have never been adjudicated, so fresh labels are required on either branch of A2.

**Effect:** the BLOCKER row drops from four open conditions to **three** — item **v2.b**, item **v2.a(iii) 2nd half**, and the
**§G2 freeze binding**. All three are worker-side and none is substantive, so quantum b is one delivery away from issuable,
with TASK-015 M6 FINAL behind it.

### 19.2 §G2 — the freeze binding, specified so the repair is one diff

`THRESHOLDS.json` must carry a `companion_notes` list binding `path` + `sha256` + `commit` + `commit_utc` for
`SEAL-APPENDIX-2026-09-25.md` and `SEAL-AUDIT.json`, and `run` must refuse when a bound companion note's live digest no
longer matches — the same refusal shape the harness already raises for a changed detector or a changed split. The seal stays
byte-identical (O-5), so the disclosure that makes it readable lives beside it, and the run must not proceed on the seal alone.

### 19.3 §G3 — "one draw, not two" verified from the two seal blobs

| | `293b29c` (20:50:46Z) | `79eb401` (20:51:54Z) |
|---|---|---|
| keys added / removed | — | **0 / 0** |
| keys whose value differs | — | **`manifest` only** |
| `holdout` / `tuning` / `salt` | 33 / 197 / `fleetyard-m4-holdout-v2-2026-09-25` | **identical** |

So the split was drawn **once**; `79eb401` re-manifested it (binding `tool_sha256` to the tool's head revision). §18 now
derives this comparison as a row (**PASS on substance**), while the **STATEMENT** row stays **FAIL** — item v2.a(iii)'s
second half is therefore **documentation-only**, and the reason it matters is on the record: `79eb401`'s own commit subject
says **"re-seal"**, which reads as a second draw to anyone who has not compared the blobs.

### 19.4 Instrument defect #31 — the position of a check is part of its correctness

The lane-side A2 row was first placed inside §18 **after** the early return that fires when the worker's audit artefacts are
absent, so it silently vanished at `4fc40c8` (283 rows instead of 284). **A check that only runs at some heads is not a
check.** Moved before the guard; both goldens now carry it. Same family as defect **#28** (a disclosure check must slice the
disclosure, not the file containing it).


---

## 20. The harness's refusals mapped to their tests — item v2.g (CONTROL seq 44, 2026-09-26T01:04:16Z)

Instrument v3.9: **311 rows at `72104a5`** (PASS 239 / FAIL 34 / INFO 30 / PROXY 8) · **284 rows at `4fc40c8`** (FAIL 27,
unchanged) · `--selftest` 18/18 · both goldens refreshed. FAIL 34 = 33 + **v2.g**.

Cycle I credited the harness with "capability evidence" on the strength of its refusal **code**. Code-present is not
code-proven, so §18 now requires each refusal to be **asserted by a test**: the fragment must appear in the harness's message
*and* in an `assertIn` in `tests/test_m4_one_shot_v2.py`.

| refusal | asserted? |
|---|---|
| freeze overwrite (`refusing to overwrite`) | **yes** |
| no freeze before run (`thresholds must be recorded before the run`) | **yes** |
| receipt exists → holdout spent (`already holds a consumption receipt`, `NEW SPLIT`) | **yes** |
| detector **file** changed after freeze (`changed after the freeze`) | **yes** |
| detector **parameters** changed after freeze | **NO** — the tested assertion is ambiguous between the two branches |
| split digest no longer matches the freeze (`does not match the frozen record`) | **yes** |
| **evaluated set ≠ frozen holdout (partial read)** | **NO** — and this is the refusal that protects the denominator |
| score: verdict outside `confirmed`/`discarded` (`allowed:`) | **yes** |
| score: label without a reason (`carries no reason`) | **yes** |

**7/9.** The two gaps are item **v2.g** (repair: two toy tests, no corpus). The partial-read refusal is the one that matters:
quantum b is one-shot, so a silently smaller denominator could never be re-run.

**Two properties verified because the refusal is only usable if it cannot fire spuriously:**
* both detectors assign `per_file[n] = sigs` **unconditionally** inside the read loop, so a **zero-signal** holdout transcript
  still counts as read — otherwise the refusal would fire on every real run and quantum b could never be scored;
* both detectors write `holdout_reads` / `holdout_consumed` **themselves** in holdout mode, so the receipt's read list is not
  reconstructed after the fact (v2.12's precedent; the run-level test stays HELD — the receipt's `holdout_reads` must be
  set-equal to the pre-registered **33**, or the §F2 sensitivity **29**).

**Corroboration of §18 from the worker's own suite.** The two new modules run **17 tests in 0.354 s → OK**, and the audit
tool's tests exercise its VOID logic in all five directions — patched sealed content
(`verdict: VOID — fixtures/toy.json: sealed content was patched after the seal (1 changed path(s), first:
/fixtures[0]/verdict: 'CERTAIN-leg-d' -> 'CANDIDATE')`), a post-seal confirmation artefact, a new fixture after the seal, a
fixture transcript inside the holdout, and an internally inconsistent seal — plus the two STANDING cases. The mutation case is
the one my append-only ruling rests on, so the classification I re-derived from the real blobs is also proven on a toy
mutation by the tool's own tests.


---

## 21. Recreation #3 recovered; CONTROL 41–44 re-published (CONTROL seq 45, 2026-09-26T01:21:34Z)

The owner restored GitHub auth at ~01:19Z. The push was rejected non-fast-forward and `git log` showed a **single commit at
the branch base `2ed0b9b`**: the third workspace recreation of this campaign. `.git` had been re-created (01:18:47Z) while the
**working tree survived**, so the four unpushed commits — `b81e86d` (CONTROL 41), `29bfded` (42), `be2fff0` (43), `e0eebbf`
(44) — are **gone as objects** while everything they carried is **present as files** and is re-committed in one recovery
commit.

**Recovery, in the order the cursor prescribes:** live tips by `git ls-remote` (this clone's fetch refspec is main-only) →
fetch by explicit refspec → **registry check first**: `fleet2/activations/REGISTRY.md` hashes to `a86115d2667e7d54…` and
equals `origin/main`'s copy byte-for-byte, so the frozen-registry FAIL-CLOSED gate **passes** → `git reset --mixed` to
`92c80b3` (**never `--hard`, never force-push**) → exactly **14 changed paths, all mine** → `--selftest` **18/18**.

**What survived** (all of it): instrument **v3.9** with §17 and §18 · ledger §17–§20 · GATES cycle I + self-corrections #5
(O-5) and #6 (O-6) · **ANNEX §G** (A2 decided pre-run) with §G2/§G3 · items **v2.c–v2.g** · both goldens (**311 rows at
`72104a5`**, **284 at `4fc40c8`**) · CONTROL.log seq 41–44 and their heartbeat lines · the cursor.
**What was lost:** the two gate worktrees (`w-4fc`, `w-721`), rebuildable in ~2 min each from the cursor recipe.

**What the outage cost.** For ~45 minutes this lane published nothing, so BOSS-2's cycles 51–58 all witnessed *"ORCH-2 @
92c80b3"*, and my cycle-I items **v2.c–v2.g were invisible to WORKER-2**. Its seven deliveries in that window therefore
cannot have answered them — which is why cycle J re-checks them at the new head instead of assuming them closed. No order,
CONCERN or REDIRECT was issued (ERRATA-25f's commit-quiet rule held).

**Lesson extended.** Commit-quiet is fine; **push-quiet is not**. The fleet reads the lane HEAD, so an unpushed lane looks
idle however much work is local. On push failure: say so in that cycle's CONTROL note, retry every cycle, and treat the
working tree as the authoritative record until the push lands — the reason this recreation cost time and nothing else.

## 22. GATE CYCLE J — the 7-delivery batch adjudicated, and a new defect class: exact but IMPOSSIBLE stamps (CONTROL seq 46, 2026-09-26T01:59:14Z)

Bound head **`1c8a287`** · worktree `/home/user/gate-scratch/w-1c8` · zip `3f36c520391049a4…` ✓ · 230 transcripts / 230
records ✓ · range `72104a5..1c8a287` = 41 files, +2095/−81 · registry `a86115d2667e7d54…` == `origin/main` byte-for-byte ·
main unmoved `7d033ab` · instrument v4.0 **322 rows (PASS 267 · FAIL 16 · INFO 31 · PROXY 8)**, golden
`orch2_verify_output_1c8a287.txt`, `--selftest` 20/20 · suite **Ran 257 in 217.2s, OK (skipped=1)**.

### 22.1 The dispositions, re-derived rather than read (method + expected + observed)

| derivation | method | result |
|---|---|---|
| append-only integrity | `git show 72104a5:runs/m4-q2-adjudication/adjudication.jsonl` vs `head -122` at head | **byte-identical, same order** — the 15 appended rows come after ✓ |
| disposition schema | key sets over the 15 appended rows | all carry `by/id/record/ruling/reason/task/utc/utc_source`; 8 also carry `new_verdict` + `prev_verdict`; every id ∈ the 122 ✓ |
| key discipline | `Counter(id)` over the 15 rows | **15 rows / 14 distinct ids** — D-092 carries two rulings (`refused-notation` + `holdout-member-note`), so any figure over the append must name its key (item 0e's lesson, applied to the append itself) |
| effective split | apply the 8 verdict-changing rows to the frozen 122 | **57/65 as adjudicated (frozen) → 49 CERTAIN-leg-d / 73 CANDIDATE effective**; 2 demotions (D-002, D-039) + 6 notation refusals (D-041/042/087/092/097/098) = 8 ✓ |
| strata vs effective | 27 fillers + 11 function + (13 − 2) content, notation 6 refused | **49** ✓ — the published strata close on the effective count, not only on 57 |
| distinct sites | `(transcript, restored_span)` over the 49 | **48** (only the D-120/D-121 `see` pair collapses; D-097/D-098 collapsed at 57 and are both refused now) — matches PATTERNS' published "49 promoted rows / 48 distinct sites" ✓ |
| holdout taint | dispositions with `ruling == holdout-member-note` | **7/7**: D-092, D-093, D-094, D-095, D-107, D-108, D-122 ✓ |
| pinned artefacts | sha256 at `72104a5` vs `1c8a287` | `signals.json`, `fixtures-adjudication.json`, `signals-v2tuning.json`, `det_dropword.py`, `det_format.py`, `m5r_reduce.py` all **UNCHANGED** ✓ (so TASK-013's M5-R PASS stands at this head) |

### 22.2 Item 8a verified by content, not by field presence

`generator_pins` on all six supplements. Checked against git: **`a5dec38` contains `tools/m4_t20_supplement.py` and that
blob hashes to `f73f6914…` == the pinned `generator_tool_sha256`**; **`d7fee6e` contains `tools/m4_q4_supplement.py` at
`fc0065ef…` == pinned**. Both tools differ at head (`7249c24d…`, `fb72269d…`) because this very delivery changed them
(+4, +3 lines) — which is the point of the pin: it names the bytes that produced the artefact, not the bytes that happen to
be head. `runs/m4-pin-repair-2026-09-26.json` records the repair and `tests/test_m4_pin_repair.py` (5 tests) covers it.
This closes item 8a and **unblocks the q3 re-gate** BOSS-2's cycle 51 named; q3's only remaining gap is `config_digest_note`
(criterion 20.15b, re-cited from 20.16 by defect #37).

### 22.3 NEW DEFECT CLASS — criterion 20.14c: exact to the second, impossible all the same

**19 own-time stamps in 5 changed files POST-DATE the commit that contains them**: `01:12:00Z` ×16 (the 15 dispositions +
`RECOUNT-2026-09-26.json`) against `7d14685` @ `00:39:44Z` (**+32.3 min**); `01:14:30Z` ×2 (the seal note + the exclusions
file) and `01:22:00Z` ×1 (the regenerated `SEAL-AUDIT.json`) against `c5b5b25` @ `00:41:22Z` (**+33.1 / +40.6 min**).
Author and committer dates agree on every commit in the range, and none of these files was touched after those commits, so
the bytes cannot have been written when they say they were. The seal note compounds it by attributing `01:14:30Z` to
`CONTROL seq 43` and commit `7d14685` — whose committer time is `00:39:44Z`.

**The control that makes the ruling non-spurious** (a forward-stamp claim is only as good as its alternative explanation):
`fleet/TIMESTAMP-CENSUS-2026-09-26.md` stamps itself **`2026-09-26T01:00:55Z`** "from `date -u` on the lane clock" and was
committed at `01:04:41Z` — a plausible **3.8-minute** write-then-commit gap in the *same lane, same hour, same toolchain*.
Git's clock and the lane's clock therefore agree to within minutes; +32/+41 min is not skew. Every offending value is also
`:00`- or cadence-shaped, i.e. **projected from the CONTROL grid rather than read** — and CONTROL rows 43/44
(`01:14:30Z`/`01:26:40Z`) are themselves forward-stamped against a lane whose last commit is `01:04:46Z`, which is where the
projected values came from.

Two independent verifications of the honest pattern in the same delivery: the census's own header (above), and the repaired
prep header `2026-09-26T00:32:03Z (src 72104a5; read `21:5xZ`)` — `00:32:03Z` **is** `72104a5`'s committer time, and
`materialised_utc = 2026-09-25T20:48:00Z` **is** `b2e0761`'s (which closes TASK-017 item 17.a). So the lane knows the rule
and applies it where it derived values from commits; the failures are all where a value was taken from the cadence grid.

**Fleet-signal side, REPORTED to BOSS-2 (not adjudicated here — the boss owns fleet signals):** WORKER-2's `fleet/CONTROL.log`
utc column has **9 of 56 rows at minute precision** (`18:26Z`, `18:27Z`, `18:34Z`, `18:41Z`…), **2 rows forward-stamped**,
**one backward jump** (`01:26:40Z` → `00:57:47Z`), and **seq values 10–15, 38, 39, 45 each used twice** — so seq is not a
unique key in that log and a cadence reader must not treat it as one (ORCH-2's own log is rendered by `fleet2check
control-render`, which enforces uniqueness and monotonicity). ERRATA-25f makes this column a liveness SIGNAL, which is why it
is reported rather than noted.

### 22.4 ANNEX §H — A4 amended: the denominator swap adopted, both numbers kept

WORKER-2's note excludes the four label-tainted transcripts **before any run**: 29 of 33 evaluated, machine-readable,
digest-bound into the freeze, enforced in `m4_one_shot_v2.py`, covered by two tests. Verified preconditions: **no receipt,
score, threshold record or quantum-b output exists at this head** (which is what separates a pre-registration from a
post-hoc choice); all four excluded transcripts are holdout members; `29 = 33 − 4`; the rationale is §F2's own ground
(D-093/D-094 are CERTAIN rows whose spans the campaign has read and annotated).

**Ruling:** A4's *structure* survives with the roles swapped — **primary 29, sensitivity 33 from the same run** (no second
spend: the four were already read), each reported with the four named, neither number chosen or dropped after the run, the
sensitivity never a certification figure. **Owed:** one sentence committing to the 33 sensitivity, because the note
currently forbids the excluded four from re-entering *any* denominator. Quantum b stays **BLOCKED** on §G2 (the freeze binds
no companion digest — 0 mentions in the harness), §H's sentence, v2.a(iii) 2nd half, v2.g's four untested refusals, and the
v2.c/v2.d/v2.e/v2.h hygiene set.

### 22.5 Refusal surface grew: v2.g is now 8/12, not 7/9

The exclusions added two refusals (`are not holdout members`, `changed after the freeze`), one of which is asserted
(`test_exclusions_changed_after_the_freeze_are_refused`) and one of which is not. **Untested: 4** — the parameters-changed
branch, the evaluated-set (**partial read**) refusal, exclusions-not-holdout-members, and the score-side partial read. The
two that guard the denominator are the load-bearing ones: a partial or wrongly-scoped holdout read must be **refused, not
scored**, because the figure is one-shot. Verified alongside (unchanged): both detectors emit an entry per transcript read,
so a zero-signal transcript cannot look like a partial read — the refusal is non-spurious.

### 22.6 Self-corrections O-7 and O-8, and defects #32–#38

Recorded in full in `fleet/GATES.md` (cycle J + O-7 + O-8). Summary of the effect on the verdict: **13 rows flipped from
FAIL to PASS on amendment** (34 → 16 across the cycle, of which 5 were landed repairs my rows mis-tested and 8 were genuine
worker repairs), and **2 rows flipped the other way** on tightened tests (v2.a(iii) 2nd half, by defect #38). Every amendment
is disclosed with its reason in the row text and in the golden, so a reader can see which PASSes are new and why.


---

## 23. GATE CYCLE K — TASK-013 RE-GATED because the reducer moved: **PASS HOLDS on a re-run, not on a byte-identity proxy** (CONTROL seq 47, 2026-09-26T02:17:07Z)

Bound head **`34db0b0`** · worktree `/home/user/gate-scratch/w-34d` · zip `3f36c520391049a4…` ✓ · book store
`corpus/docdocgo/html/merged-book-texts_json_1.js` `c0892fcd…` ✓ · range `1c8a287..34db0b0` = 6 files
(`findings/PROVENANCE.json`, `tools/m5r_reduce.py` +46, `tools/m4_prov_check.py` new 149 ln, `tools/m4_q4_supplement.py`,
`runs/m4-q4-holdout/PROVENANCE-SUPPLEMENT.json`, + tests) · registry `a86115d2667e7d54…` == `origin/main` at last successful
read · instrument **324 rows (PASS 271 · FAIL 13 · INFO 32 · PROXY 8)**, golden `orch2_verify_output_34db0b0.txt` (569 ln),
`--selftest` 20/20 · suite **Ran 263 in 199.3s, OK (skipped=1)**.

### 23.1 The re-gate: method, then bytes

TASK-013's PASS had been quoted on *"the reducer's bytes are identical across `219075a`/`ffb8811`/`4fc40c8`/`72104a5`/
`1c8a287`"*. Item 13 (a repair **this queue required**) moved those bytes, so the milestone was re-gated on the substance.

| output | published at `34db0b0` | re-run of the tool AT HEAD, published pins | verdict |
|---|---|---|---|
| `ledger.jsonl` | `d42136c673188f9e…` | `d42136c673188f9e…` | **BYTE-IDENTICAL** |
| `by_transcript_digest` | `c1ec4da86a6ce4f4…` | `c1ec4da86a6ce4f4…` | **IDENTICAL** (230 files) |
| findings / files | 1334 / 230 | 1334 / 230 | identical |
| book refs | 242 ok / 0 bad | 242 ok / 0 bad | identical |
| citation failures | 0 | 0 | identical |
| regenerated manifest | — | differs in **`tool_sha256` only**: `6d4bb9ce…` → `a89ff189…` | as the artefact's own `derivations_revision` states |

Invocation that reproduces (from `tools/m5r_inputs.sh`'s recipe, in the gate worktree):

```
python3 tools/m5r_reduce.py --records evidence/runs/m5-raw/records --fixtures evidence/fixtures/confirmed \
  --corpus corpus --utc 2026-09-25T19:55:24Z --tool-commit dada3e602689cb900971fda0dccce8267f31a2b2 \
  --main-head 77f1d6de80ec0ae77d7ca06fdfd581671cea7cae --policy-sha 0fe20a6057ec9fa26fdc2184f84352185f8278fb346bc9d9de14927819ffdc85 \
  --book-store-sha c0892fcd20502d49b99fffe87a4ec4b3b5ecc94a1f98606aab7909127934a4a8 --detector-tool-commit 7b8863d
```

**Ruling: TASK-013 M5-R remains PASS.**

### 23.2 The diagnosis that made the ruling safe (and produced item 13b)

The first re-run passed only `--utc` and produced a **different** ledger digest. A field-by-field diff over all **1334 rows**
localised the difference to exactly one field, `status_by`: `tools/m5r_reduce.py@dada3e6…` published vs
`tools/m5r_reduce.py@UNPINNED` re-run. Every row embeds the `--tool-commit` pin, so:

- with the full pin set the outputs are byte-identical (§23.1) — the tool's behaviour is unchanged;
- **without** the original pin the content is identical and the digest is `c94cce40…`.

Hence **item 13b**: the artefact's `reproducibility_note` ("a rebuild with this revision emits these exact derivations and a
byte-identical ledger/by-transcript") must name the pin its claim depends on. One clause closes it. This is criterion 20.15a's
discipline applied to a claim *about* reproduction: a stated derivation must reproduce when followed **literally**.

### 23.3 Items closed, opened, and still owed at `34db0b0`

| item | criterion | verdict at `34db0b0` | evidence |
|---|---|---|---|
| **13** | 20.15a / 20.15b | **CLOSED — 7/7** | `fixtures_digest_sha256` recomputed under the NEW stated construction (basename keys over the 2 `.json` in `fixtures/confirmed/`, lines carrying `\n`) = `c5d8f6f3db3b0d01…` == published; `overlays_digest` states the warned-against variant's construction → `58274f46…` reproducible as written; `tool_sha256` = `6d4bb9ce…` at the stated `tool_commit dada3e6`; `json_canonicalization` added |
| **14** | 20.16 | **CLOSED** | q4's format leg publishes the COMPLETE config; digest **`8e7e35a2…` == q3's** (no subset remains); `config_digest_note` on all three run objects |
| **13b** | 20.15a | **OPEN (new)** | the `reproducibility_note` does not name the `--tool-commit` dependency (§23.2) |
| q3 note | 20.15b | **OPEN** | `runs/m4-q3-format/PROVENANCE-SUPPLEMENT.json` publishes `8e7e35a2…` with no `config_digest_note` anywhere in the file, while q2 and all three q4 legs carry one |
| 0h / v2.h / 12c | 20.14c | **OPEN, unchanged** | whole-tree census: **19 forward stamps of 61 own-time stamps**, all `:00`- or cadence-shaped; **none new** in `1c8a287..34db0b0` — the files carrying them were not touched |
| quantum b | v2.7 | **BLOCKED** | §G2, the §H sentence, v2.a(iii)-2nd-half, v2.g's four untested refusals, v2.c/v2.d/v2.e/v2.h |

### 23.4 ANNEX §F7 amended and §F8 recorded (self-correction O-10)

§F7 as drafted voided a pre-registration on **any** post-freeze change to a bound input — which, applied literally at this
head, would have voided quantum b's freeze over +46 lines of derivations prose that this queue required, the lane disclosed,
and the gate verified neutral. Amended: drift voids **unless** (i) disclosed in the artefact with old/new digest and its
effect on outputs, (ii) verified behaviour-neutral by re-running the changed tool with the published pins and comparing output
bytes, (iii) re-pinned in the ANNEX **before the bound run starts**. §F8 records this instance: **B1/B4
`tools/m5r_reduce.py` `6d4bb9ce…` → `a89ff189…`**, no other frozen value moved, quantum b's freeze **stands** on the amended
pin. The instrument's §12 tuple was re-pinned in the same act, with the disclosure comment attached (§12: 6/6 match).

### 23.5 Instrument defects #39–#41 and self-corrections O-9/O-10

**#39** `tool_sha256` resolved at head instead of at the manifest's stated `tool_commit` — FAIL against a derivation that
reproduces exactly. **#40** `fixtures_digest_sha256` recomputed with the OLD literal reading after item 13 rewrote the
derivation — a row must re-read the published text each run, never a copy taken at cut time. **#41** (build discipline) a new
row anchored on a string that also occurs in the **module docstring** landed inside the docstring and never executed (the run
silently reported one row fewer), and the same slice deleted §19's control-block initialisation → `NameError: ctrl`. Amended
rule: after any multi-anchor edit, run `--selftest` **and** a full run, and compare the **row count** to the previous golden
before publishing a verdict — a missing row is a silent PASS.

**O-9** (proxy vs substance): where a criterion is "figure X reproduces", the gate RE-RUNS the producing tool at head with
the published pins and compares output bytes; a byte-identity row over the tool may survive as HISTORY, never as the verdict.
Corollary: when a re-run disagrees with a published digest, **diff the rows before diffing the claim** — one field, one
argument, two minutes. **O-10** (my own over-broad rule): every absolute pre-registration rule needs its escape hatch written
at drafting time, with the evidence the hatch requires; an unwritten hatch gets improvised under pressure, which is how
pre-registrations die. Full text in `fleet/GATES.md`.

### 23.6 Platform

GitHub auth died mid-cycle (`gh auth status` → *"the github.com token in GH_TOKEN is no longer valid"*; `git fetch` /
`ls-remote` → *"could not read Username"*). Fleet heads could not be re-read after ~02:1xZ; last successful read: main
`7d033ab`, BOSS-2 `1723564`, WORKER-2 `34db0b0`. Cycle K is committed locally at this head; the push is retried on cadence.
CONTROL.log and the heartbeat continue at cadence **inside** the work loop, so the lane's signals stay live while its push
channel is down — push-quiet here is an outage, not a dark lane (ERRATA-25f).

### 23.7 The worker's own checker verified by RUNNING it — item 13 now rests on two independent implementations (2026-09-26T02:34:11Z)

`tools/m4_prov_check.py` (149 ln, new at `fa71443`) claims to recompute every published derivation **by following the text
now in the manifest**. ORCH-2 ran it in the gate worktree with its **default paths** (the corpus zip is materialised at the
repo root, `fixtures/confirmed/` is tracked and byte-identical to the archived copy under `evidence/`):

```
$ python3 tools/m4_prov_check.py
PASS inputs.corpus_zip_sha256 3f36c520391049a4 · PASS inputs.records_digest_sha256 d8c935367c8d0ab8
PASS inputs.fixtures_digest_sha256 c5d8f6f3db3b0d01 · PASS inputs.overlays_digest 027f82a0d2522f3e
PASS derivations.overlays_digest warned variant 58274f468fe2db53 · PASS outputs.ledger.jsonl d42136c673188f9e
PASS outputs.by_transcript_digest c1ec4da86a6ce4f4 · PASS book_store.sha256 c0892fcd20502d49
PASS tool_sha256 (blob at tool_commit) 6d4bb9ce78f2964e
prov check: OK (manifest dce2eb3a0ff89ada)   [exit 0, 9/9]
```

Every value equals ORCH-2's own recomputation (§23.3), and the tool resolves `tool_sha256` **at the manifest's own
`tool_commit`** — the same literal reading that corrected instrument defect #39. It is **independent**: its own
`dir_digest`/`overlays_digest`, no import from `m5r_reduce.py`.

**Mutation controls (a check that cannot fail is not a check):**

| mutation | expected | observed |
|---|---|---|
| `inputs.fixtures_digest_sha256` → `0`×64 in a sibling temp manifest | exit 1, that field named | **exit 1**, `FAIL inputs.fixtures_digest_sha256` ✓ |
| `inputs.overlays_digest` → the WARNED variant's value | exit 1 (the value row **and** the "must differ" row fire) | **exit 1**, `FAIL inputs.overlays_digest` ✓ |
| `--manifest` pointing at a nonexistent file | exit 2, fail-closed | **exit 2**, `inputs missing:` ✓ |

Two rows were added to the instrument so this is mechanical rather than a note: §14 *"item 13's own tool … run with its
DEFAULT paths"* (exit 0 and 9/9) and §14 *"item 13's tool is NOT vacuous — mutation control"* (tamper a published digest in a
temp manifest, require exit 1 with the field named, clean up the temp file). **Instrument now 326 rows.**

**One latent coupling recorded, not charged as a defect:** the tool calls `dir_digest(--fixtures, "relpath")` while the
manifest's derivation names **basename** keys. The derivation forecloses the divergence in its own text — *"the directory is
flat, so the keys ARE basenames"* — and both copies of the directory are flat with 2 files, so the values agree. If a
subdirectory is ever added under `fixtures/confirmed/`, the tool would silently follow a different convention from the text
it claims to follow literally. Either `key="basename"` in the tool or one more sentence in the derivation closes it; it is
recorded here so the next reader does not have to re-derive the equivalence.

### 23.8 Instrument defect **#42** — an R1 sweep: nine rows reported `n=0`, and five of them were PASSes (2026-09-26T02:34:11Z)

R1 (built into the instrument after ORCH-2 broke it once) says *every set-level check reports n = the number of comparisons
performed, and a zero produced by zero comparisons is VACUOUS, not PASS*. Auditing the cycle-K golden for `\[n=0\]` found
nine rows where `n` counted **defects found** or **matches** instead of comparisons — so a clean artefact reported
`PASS [n=0]`, indistinguishable from a row that did no work at all:

| row | n was | n is now |
|---|---|---|
| §4 interval overlaps with any fixture span | 0 (INFO) | **VACUOUS** — 0 interval comparisons were genuinely possible, and the label now says so |
| §12 a committed pre-registration artefact exists | matches (0) | filenames compared under `runs/` (INFO/HELD retained) |
| §12 no receipt declares the V2 holdout SPENT | offending receipts (0) → **PASS [n=0]** | JSON artefacts examined for a spend declaration |
| §13 the rebuilt EVAL drops no field a derivation reads | dropped keys (0) → **PASS [n=0]** | 3 (two key-presence tests + the closure test) |
| §15 v2.16 PRECEDENT — one-shot discipline in the tool's source | hits (0) → **PASS [n=0]** | source lines scanned |
| §18 the audit tool opens no transcript content | matching lines (0) → **PASS [n=0]** | source lines scanned |
| §18 item v2.a(iii) 2nd half — the STATEMENT | artefacts carrying it (0) → FAIL [n=0] | companion artefacts **searched** (the FAIL was real but looked like zero work) |
| §18 v2.16 precedent — quantum-b tool/registry | matches (0) → **PASS [n=0]** | source lines scanned |
| §15 criterion v2.12 — pre-registration commit before the run commit | candidate run dirs (0), INFO/HELD | **left as is** — reviewed: it claims no PASS, and its observed text says "HELD — no quantum-b run directory exists yet" |

Post-sweep: **326 rows — PASS 273 · FAIL 13 · INFO 31 · PROXY 8 · VACUOUS 1**, `--selftest` 20/20, golden refreshed
(`orch2_verify_output_34db0b0.txt`, 573 ln). The FAIL set is unchanged by the sweep — **an n fix must never move a verdict,
and none did**; that is itself the check on the sweep.

Rule added to the instrument's own discipline: *`n` counts comparisons performed. If the natural count is "how many defects
did I find", the row is reporting the wrong number — report the population searched and put the defect count in the observed
text.*

### 23.9 Three rows judged wording instead of substance, the golden stopped clipping evidence, and the 13 FAILs got a repair map (2026-09-26T02:37:06Z)

**Defect #44 (O-8's lineage, found by review — no verdict moved).** Three FAIL rows tested the shape ORCH-2 predicted rather
than the criterion's substance, so a legitimate repair could have been failed:

| row | was | now |
|---|---|---|
| §8 config canonicalization stated (20.15b) | demanded the literal key `config_digest_note` | **any key whose value states the construction** (`sort_keys` / `separators` / `canonical` / `sha256 of` / `json.dumps`), judged at every level where a `config_sha256` is published |
| §18 v2.a(iii) 2nd half — the STATEMENT | 5 accepted phrasings | **13** (`one draw`, `same draw`, `single draw`, `re-manifest`, `manifest-only`, `not a second draw`, `no re-draw`, `not re-drawn`, `was not redrawn`, `without re-draw`, `identical partition`, `same partition`, `same salt`, `partition unchanged`, `only the manifest`) — defect #38's rule still holds: a bare citation is not a statement |
| §18 ANNEX §H (A4 amended) | `sensitivit` anywhere + a `33` in the note (a hollow sentence could PASS) | the **conjunction** A4-as-amended actually requires: both denominators stated (29 and 33, with `sensitivity`/`primary`), a same-run / no-second-spend phrase, and the four named or bound by reference to `holdout_exclusions` |

Post-amendment the FAIL set is unchanged (**13**), which is the check on the amendment: a substance fix must not move a
verdict at a head where nothing was repaired. `n` on the §H row is now 4 (its four conditions), on the STATEMENT row 6
(companion artefacts searched).

**Defect #43 — the golden clipped its own evidence.** `Report.add` printed `observed[:400]`, so the 20.14c row's
**19-offender list reached the published record unreadable**: a worker told "19 forward stamps in 5 files" cannot repair
without re-deriving the list. Fixed by wrapping instead of clipping (`textwrap.fill`, 140 cols, continuations indented so
§16's row-parser regex cannot mistake them for rows). The golden grows 573 → **668 lines** and now carries the full list:
`adjudication.jsonl` **15** (the appended dispositions) + `RECOUNT-2026-09-26.json` 1 + `SEAL-AUDIT.json` 1 +
`HELD-OUT-SPLIT-V2-EXCLUSIONS.json` 1 + `HELD-OUT-SPLIT-V2-NOTE-2026-09-26.md` 1 = **19** over **4 distinct values**
(`01:12:00Z` ×16, `01:14:30Z` ×2, `01:22:00Z` ×1) against commits at `00:39:44Z` / `00:41:22Z`. **The byte-frozen seal
`tools/HELD-OUT-SPLIT-V2.json` carries no forward stamp**, so the repair never has to touch it.

Rule added: *evidence a repair depends on must survive into the published record — wrap, never clip.* A row whose observed
text is truncated is a row whose FAIL cannot be acted on.

**`fleet/ORCH-2-REPAIR-MAP.md` published.** One entry per FAIL row at `34db0b0`: the row name, the criterion, the owning
task/item, **the artefact change that flips it**, and the evidence the gate will re-derive. Ordered so the two one-sentence
repairs (item 13b; q3's config note) come first, then the stamp family (3 rows, one root cause), then provenance completeness
(v2.c/v2.d/v2.e), then quantum b's blockers (v2.a(iii)-statement, O-5's freeze binding, §H's sentence, v2.g's four untested
refusals, v2.b), and finally the one entry ORCH-2 does **not** rule (the WORKER lane's `CONTROL.log` utc column — evidenced,
REPORTED to BOSS-2). It also states what is already settled and not re-openable by repair: TASK-013 M5-R **PASS**, q1/q4/q5
**PASS**, TASK-017 **PASS**, the v2 seal **STANDS**.

### 23.10 Defect **#45** — the coverage claim was CURATED, and the curated list was three cycles stale; §20 now derives it (2026-09-26T02:41:41Z)

§16's load-bearing row — *"every OPEN item in the queue has a row in this instrument that flips when it is repaired"* — read
its open-item list from a **hardcoded tuple** frozen at cycle F/G:

```python
OPEN = ("8a", "8b", "11a", "11b", "12", "13", "14", "15a", "15b", "0d", "0e", "0f", "0g", "17.a", "v2.a", "v2.b")
```

Ten of those sixteen were **closed cycles ago** (8a, 11a/11b, 12, 13, 14, 15a/15b, 0d–0g), and every item opened since was
**absent** (13b, 0h, 12c, v2.c, v2.d, v2.e, v2.g, v2.h, 20.14c, 20.15b). The row PASSed — on a list that no longer described
the queue. This is the row the instrument's own note calls *"the coverage claim that matters, because these are the items
whose re-gate must be a single run"*, so a stale list here is worse than a missing row: it asserts completeness that does not
exist. Same family as O-9 (a proxy standing in for the substance) and #42 (a number that means something other than what the
reader takes from it).

**Fix, in two parts.** (i) The tuple is refreshed to the cycle-K open set
`("0h", "12c", "13b", "v2.a", "v2.b", "v2.c", "v2.d", "v2.e", "v2.g", "v2.h", "20.14c", "20.15b")` and demoted to a
cross-check; `criterion 20.14c`'s row now also names **TASK-020 item 12c**, which it enforces but did not cite. (ii) A new
**§20 derives the claim** from the published repair map instead of curating it:

| §20 row | test | at `34db0b0` |
|---|---|---|
| every FAIL row is mapped to a repair, quoted **VERBATIM** | each of the 13 FAIL row names appears in `fleet/ORCH-2-REPAIR-MAP.md` as `- **Row (verbatim):** \`…\`` | **PASS 13/13** |
| the map carries no entry for a row that no longer FAILs | every quoted name is still a FAIL | **PASS**, 0 stale |
| VACUOUS rows owe no repair | reported as vacuous-by-data, neither PASS nor FAIL (R1) | **PASS**, 1 row |

Both directions matter: an unmapped FAIL is a FAIL nobody can act on, and a stale map entry is a promise a landed repair
already kept — the map is append-only per cycle, so a repair forces a **new** map for the new head rather than an edit.

**Defect #46 (found by §20's own first run).** The verbatim-quote regex was `` `([^`]+)` ``, which stops at the **first inner
backtick** — and four row names contain one (`derivations_revision`, `audit_utc`, `tool_commit`, `utc_source`). The coverage
row therefore reported 9/13 mapped and 4 "stale" entries that were its own truncated quotations. Fixed to match greedily to
the closing backtick at end of line (a name may contain backticks; it may not end with one). The lesson is the mutation-test
lesson again: **a new mechanical check must be run against the artefact it checks before its verdict is believed** — §20's
first FAIL was §20's own bug, and it was only readable because the row printed the names it failed to match.

**Instrument after §20: 329 rows — PASS 276 · FAIL 13 · INFO 31 · PROXY 8 · VACUOUS 1**, `--selftest` 20/20, golden refreshed
(676 ln). The FAIL set is the same 13 the repair map lists — which is now a **mechanical** agreement, not an assertion.

### 23.11 The cycle-K amendments are now mutation-tested, and §20 knows which head its map binds (2026-09-26T02:46:02Z)

**(a) Four predicates lifted to module level so `--selftest` can attack them.** The §8/§18/§19 amendments (defect #44) and
§20's quote parser (defect #46) were inline expressions — correct today, invisible to the selftest, and one refactor away from
silently changing a gate result (self-item O-2's whole reason for existing). They are now `states_construction()`,
`one_draw_statement()`, `h_denominator_commitment()` and `verbatim_row_quotes()`, each documented with the defect it guards,
and **seven new selftest cases** pin both directions:

| case | guard | positive | negative |
|---|---|---|---|
| T21 | #44 §8 | a key named `config_canonicalization` whose value states `sort_keys`/`separators` **counts** | the literal `config_digest_note` also counts; an unrelated `note` key does **not** |
| T22/T23 | #44 §18 vs #38 §18 | *"the partition was not redrawn, same salt, manifest only"* with both commits **is** the statement | a bare `(src 293b29c)` timestamp citation is **not** |
| T24/T25 | #44 §19 | 29 + 33 + `holdout_exclusions` + *"SAME run, no second spend"* satisfies amended A4 | *"a sensitivity figure over 33 transcripts"* alone does **not** (the hollow sentence the old row PASSed) |
| T26/T27 | #46 §20 | a quoted row name **containing inner backticks** parses whole | a line that is not a `**Row (verbatim):**` quote yields nothing (no phantom coverage) |

`--selftest` is now **27/27 ok**. The full run is **verdict-neutral**: 329 rows, FAIL 13, and the FAIL set is byte-for-byte
the same 13 names as before the refactor (compared mechanically, not by eye). Golden refreshed (676 ln).

**(b) §20 is bound to the head its map was published for.** Running the amended instrument at the *previous* gated head
`1c8a287` exposed the flaw: that head has **17** FAILs, the `34db0b0` map quotes **13**, so §20 reported a FAIL — against the
worker, for a mismatch that is the gate's own bookkeeping. A repair map is head-specific by design (append-only per cycle), so
§20 now reads the head from the map's title and, when it differs from the head being gated, reports **INFO — "coverage NOT
claimed for this head"** instead of failing anybody. Verified at both heads:

| head | rows | FAIL | §20 |
|---|---|---|---|
| `34db0b0` (map's head) | 329 | **13** | mapped 13/13 PASS · 0 stale PASS · VACUOUS 1 PASS |
| `1c8a287` (previous) | 327 | **17** | INFO — map binds `34db0b0`, coverage not claimed; VACUOUS 1 PASS |

The row keeps its teeth where it matters: at the map's own head, an unmapped FAIL or a stale entry fails the run.

### 23.12 Why the re-gate transfers **all thirteen** M5-R criteria, criterion by criterion (2026-09-26T02:48:44Z)

Byte-identity of the outputs is not automatically byte-identity of the *verdict*: TASK-013's thirteen criteria are not all
properties of the same thing. Some are properties of the artefact bytes, some of the tool's behaviour, some of the process
around it. Classified and evidenced:

| criterion | property of | cycle-K evidence at `34db0b0` | status |
|---|---|---|---|
| **C1** completeness (every record → exactly one finding) | artefact bytes | `ledger.jsonl` + `by-transcript` byte-identical; 1334 findings / 230 files | **transferred** |
| **C2** dedupe + cross-detector merge performed and reported | artefact bytes | identical manifest `stats` (1336 detector instances → 1334 findings, seeded 3) | **transferred** |
| **C3** adjudication against cited bytes (transcript + book quotes byte-exact) | artefact bytes, re-tested | the re-run itself reports **0 citation failures, 242 ok / 0 bad book refs** | **re-verified at head** |
| **C4** classification per STANDARDS; the tool never invents CERTAIN | tool behaviour + bytes | identical class distribution inside identical bytes; the diff touches **no logic** (below) | **transferred** |
| **C5** seeded vs independent reported separately | artefact bytes | identical; seeded = 3 reported apart | **transferred** |
| **C6** finding-record shape complete | artefact bytes | field-level diff over all **1334 rows**: the only field that can differ is `status_by`, and only when the `--tool-commit` pin is omitted (§23.2) | **transferred** |
| **C7** coverage truth in the ledger's own summary | artefact bytes | identical summary text | **transferred** |
| **C8** provenance manifest binds all inputs, every derivation recomputable | artefact + tool | manifest identical **except `tool_sha256`**, which re-derives at its own stated `tool_commit`; derivations now **7/7** literal (§14) and independently confirmed by the worker's own checker **9/9** (§23.7) | **strengthened** |
| **C9** determinism: a fresh independent replay at a pinned utc reproduces every output byte | process | **cycle K's re-run IS that replay** — different head, different worktree, corpus re-materialised from the zip, pins from the manifest | **re-verified at head** |
| **C10** suite green WITH corpus, skip counts reported, count never drops | process | `Ran 263 tests in 199.3s — OK (skipped=1)`; floor 257 → **263**, no drop, no errata needed | **re-verified at head** |
| **C11** stdlib only, no network, declared read/write scope, no evidence executed as instructions | tool source | imports at head: `argparse, datetime, difflib, hashlib, io, json, os, re, sys, unicodedata` — all stdlib; **no** `urllib`/`socket`/`requests`/`subprocess`/`os.system`; **one** write site (`ledger_path`); the diff changes **no import, I/O or network line** | **re-verified at head** |
| **C12** no error rate, no precision/recall, no completion language | artefact bytes | identical text | **transferred** |
| **C13** limits disclosed | artefact bytes | identical text | **transferred** |

**8 transferred by byte-identity · 4 re-verified at head (C3, C9, C10, C11) · 1 strengthened (C8).** No criterion rests on the
reducer's bytes being unchanged, which is why the PASS survives their change.

**The diff, precisely (and a correction to this ledger's own earlier wording).** `git diff --numstat 1c8a287 34db0b0 --
tools/m5r_reduce.py` = **+42 / −4** (46 changed lines, net +38) — earlier entries in this cycle said "+46 lines", which reads
as 46 *added*; the correct figure is 46 *changed*. Every one of them is inside the manifest's `derivations` dict literal:
three derivation strings rewritten (`fixtures_digest_sha256`, `overlays_digest`, plus a new `json_canonicalization`) and the
new `derivations_revision` record. **No control flow, no import, no I/O, no constant that feeds a computation.** That is what
makes "documentation-only" a verified statement rather than a characterisation — and it is why C4 and C11 transfer instead of
needing a fresh adjudication.

**One artefact sentence worth quoting, because it is honest and it is also why item 13b exists:**
`derivations_revision.effect_on_run_outputs` names the run's untouched values (ledger `d42136c6…`, by-transcript `c1ec4da8…`,
1334 findings, `tool_sha256 6d4bb9ce…` at `tool_commit dada3e6…`) and says *"only this manifest's derivations prose changed"*;
`reproducibility_note` says *"a rebuild with this revision emits these exact derivations and a byte-identical
ledger/by-transcript; tool_sha256 necessarily differs, because it hashes the running file."* The first half is exactly right
and ORCH-2 reproduced it. The second half is the one that omits the `--tool-commit` dependency (§23.2) — item **13b**, one
clause.

### 23.13 Two more criteria mechanized — the field-level diff and C11's source scan — and defect **#47** (2026-09-26T02:52:34Z)

**(a) The cycle-K diagnosis is now a row.** §1 *"criterion C6 / item 13b — the re-run's ledger rows are FIELD-IDENTICAL to the
published ones, and any differing field is NAMED"* aligns the published and re-run ledgers by `id` and reports every field
whose value differs: **1334/1334 aligned, differing fields: NONE** (PASS, n=1334). This is the analysis that settled the
re-gate — run without `--tool-commit`, the only differing field is `status_by` — mechanized so the next cycle inherits the
answer instead of re-deriving it, and so a future tool change that moves a **real** field is named rather than hidden behind a
digest mismatch. A field name is worth more than a digest: it says *what* moved.

**(b) C11 is now read from the tool's source every run.** §1 *"criterion C11 — the reducer is stdlib-only, opens no network or
subprocess, and every write goes under `--out`"* (PASS, n=18 = 10 imports + 6 write sites + 2 derivation checks): imports are
`argparse, datetime, difflib, hashlib, io, json, os, re, sys, unicodedata` — all in `sys.stdlib_module_names`; no
`urllib`/`socket`/`requests`/`http`/`subprocess`; all six write-mode `open(` sites target `args.out`, `ledger_path` or `bt`,
and both of those are assigned from `args.out`. So C11 stops being a cycle-K assertion and becomes a standing check: a future
edit that adds a network import or writes outside `--out` flips the row.

**(c) Defect #47 — a row that under-counted the population it polices.** The first version of (b) captured write sites with
`open\(([^,]+),\s*["\']w`, which stops at the **first comma**: `open(os.path.join(args.out, "SUMMARY.md"), "w"` never
matched, so the row reported **ONE** write site where the tool has **SIX** — and still PASSed. That is worse than no row: it
reads as a clean bill of health over a population of one. The derivation regexes were also anchored `^ledger_path` and so
missed both indented assignments inside `main()`, which is what made the row FAIL loudly enough to be caught. Fixed by
scanning **lines** that contain both an `open(` and a write mode, then judging each line's target, and by anchoring `^\s*`.
Rule: **when a row counts a population, verify the count against the source by hand at least once** — an under-count is
invisible in the verdict and only visible in the number.

**(d) §20 earned its keep in the same act.** Adding the C11 row made the run FAIL **15**: the new row was not in the repair
map, and §20 reported *"13/14 mapped; UNMAPPED: criterion C11 — …"*. That is the coverage check doing exactly what defect #45
said it must — no FAIL may exist that nobody has mapped to a repair — and it fired on the gate's own new row before it fired
on anybody else's. Once C11's own regex was fixed the row PASSed and the FAIL set returned to the mapped 13.

**Instrument: 331 rows — PASS 278 · FAIL 13 · INFO 31 · PROXY 8 · VACUOUS 1**, `--selftest` 27/27, golden refreshed (680 ln).

### 23.14 The gate turned its timestamp census on its own lane and found two classifier defects — and confirmed it had NOT over-charged the worker (2026-09-26T03:00:26Z)

`--self-audit` runs the same census over ORCH-2's own tree. Two defects fell out, both in the classifier that separates
*a fuzzy stamp this lane asserts* from *a fuzzy stamp this lane quotes in order to report it* — the distinction the whole
criterion 20.14a charge rests on.

**Defect #48 — the self-audit reported the count and never verdicted it.** It printed `FUZZY asserted 26` beside two PASS
rows (O-4, O-6) and drew no conclusion, so this lane could accumulate the exact defect it charges WORKER-2 with while its
self-audit looked clean. A row now judges it: asserted-fuzzy stamps in **amendable** docs FAIL; those inside append-only
records (`CONTROL.log`, the heartbeat log, the ledger, `GATES.md`, `LOG.md`, the cursor, and `status.md`'s log, which
declares itself append-only) are reported as history, because repairing them means rewriting a record.

**Defect #49 — the citation classifier tested the wrong character.** `FUZZY_TS` matches only the **time fragment**, so the
"immediate wrapping" test inspected the character beside `21:5xZ` *inside* `` `2026-09-25T21:5xZ` `` — a digit, not a
delimiter — and classified a fully backticked quotation as an **asserted instance**. Backticking the whole stamp is the
normal way this lane quotes one. Two fixes: look outward across timestamp characters for the delimiter, and treat a
delimited span that also carries a full ISO stamp or a `(src ` annotation as **quoted artefact content** (an author's own
stamp is never written that way). Four selftest cases pin it (T28–T31), including the negative that keeps it honest: a
nearby backticked **digest** does not pardon a fuzzy stamp in the author's own sentence. `--selftest` is now **31/31**.

**The charge against WORKER-2 was NOT overstated — verified, not assumed.** The classifier bug inflated *instance* counts, so
the first question was whether the published worker figures were wrong. Re-run at **both** gated heads:

| head | 20.14a asserted instances | quoted sites | verdict |
|---|---|---|---|
| `1c8a287` (cycle J golden, pre-fix) | 0 | 29 | PASS |
| `1c8a287` (post-fix) | **0** | **29** | PASS |
| `34db0b0` (pre-fix) | 0 | 29 | PASS |
| `34db0b0` (post-fix) | **0** | **29** | PASS |

No worker-side figure moved, because the worker's own quotations were already caught by the 60-character context rule; the
bug only bit on spans the context window could not reach. The historical "26 instances across 10 files" at `4fc40c8` (ledger
§20.14a) was computed with the old classifier and is therefore an **upper bound** — but item 12 repaired those sites and the
row has PASSed at every head since, so nothing owed to WORKER-2 changes. Recording it anyway: a figure computed with a
buggy classifier stays in the record labelled with that fact.

**ORCH-2's own lane, corrected.** Asserted-fuzzy stamps fell 26 → **17**, citations rose 24 → **27**, and the amendable count
is **0**. Three of the repairs were substantive, not cosmetic: the GitHub-outage time this lane had written as `~02:1xZ` is
now a **bounded window with its bounds and their sources** — *between 02:01:46Z (CONTROL seq 46) and 02:17:07Z (the first
cycle-K document stamp); the exact second is not recoverable because the credential died between two calls in that window* —
in `status.md`, `ORCH-2-HEARTBEAT.md` and `ORCH-STATE.md`. That is criterion 20.14's own discipline applied to an
approximation: state the bound and its source instead of a fuzzy token. The remaining 17 sit in append-only records,
including CONTROL seq 47's `~02:1xZ`, which is corrected here rather than edited there.

Instrument **331 rows — PASS 278 · FAIL 13 · INFO 31 · PROXY 8 · VACUOUS 1** (unchanged), golden unchanged, `--selftest`
**31/31**.
