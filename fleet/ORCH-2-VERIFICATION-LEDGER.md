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
