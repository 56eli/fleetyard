# GATES — orchestrator gate log (append-only)

2026-09-24 CYCLE 1 — no gate needed: worker lane (7c4ae48) has no production commits beyond registration.
observed: overlay count 230 (not 231); missing file = Thought_and_Ideation_Feb_2004_Part_1; manifest.json internally consistent at 230.

2026-09-24 CYCLE 3 — GATE: TASK-001 (M0 corpus inventory) — worker sha 7fac8d368a
verdict: PASS
suite: 12 tests OK (10 pass, 2 skipped — corpus-dependent tests skipped in scratch worktree, expected)
spot-checks:
  - file sizes: Advaita Part 1 (58888=58888), Love Sep 2011 Part 1 (33343=33343), Ego and Self Part 1 (120213=120213) ✓
  - U+FFFD anomaly: Sedona Part 4 count (3=3) ✓
  - book store: 14634979=14634979 ✓
  - total overlay .txt bytes: 14240774=14240774 ✓
  - Thought_and_Ideation Part 1 missing confirmed (only Parts 2,3 exist) ✓
  - 230 transcripts + manifest.json = 231 entries; worker correctly disclosed ✓
taxonomy: N/A (no findings in M0 — census task only)
tool gates: census.py stdlib-only, read-only over corpus/**, no network ✓
notes: worker self-served M0 (no orchestrator queue at boot time — acceptable per role spec). Clean delivery.

CORRECTION (2026-09-24, per REDIRECT-001): cycle-1 observation "missing file = Thought_and_Ideation_Feb_2004_Part_1" was wrong. Battery's 231 counts overlay/ directory entries (230 .txt + manifest.json). Nothing is missing — Part 1 is a part-number gap, not a lost file. Manifest never listed it. Campaign denominator = 230 transcripts. See fleet/ERRATA-2026-09-24-ORCH.md E3.

CORRECTION (2026-09-24, per REDIRECT-002): the CYCLE 3 PASS verdict must NOT be taken as M0 certification. TASK-001 acceptance criterion 3 ("Extra sources listed if present") is unmet — tools/CORPUS.md does not census corpus/docdocgo/extra-sources/ (3 files, 1,472,446 B, UNDECIDED per VISION). M0 gate remains OPEN pending criterion 3 via TASK-003. The PASS numbers (test suite, spot-checks, battery) stand on their merits.

2026-09-24 CYCLE 9 — GATE: TASK-002 (M1 tooling foundation) — worker sha 2f14b03
verdict: PASS
suite: 30 tests OK (24 pass, 6 skipped — corpus-dependent tests in scratch worktree, expected)
test count: 30 (up from 12 — no tests dropped) ✓
spot-checks:
  - fixture CF-001: "Dilgo. Quince." @ Love Sep 2011 P1 offset 5292 — verified against corpus bytes ✓
  - fixture CF-003: "255% of people are happy" @ Love Sep 2011 P1 offset 4543 — verified (should be 55%) ✓
  - clean set: 59 sha256 pointers, 5/5 verified against book store via loaders ✓
  - book store: 24 entries parsed by read_book_store() ✓
  - NON_HAWKINS_SLUGS: 4 entries (Be_as_you_are, I_AM_THAT, Lamsa_bible, ACIM_workbook) — correctly identified and disclosed ✓
  - U+FFFD handling: Sedona Part 4 has 3 replacement chars at positions [15362, 15376, 15377] — matches M0 census ✓
  - transcript loader: single-paragraph mode for single-line transcripts, locate() correct, sentences() works ✓
  - tokenizer: "Dilgo. Quince. 570." → 3 tokens with correct offsets ✓
taxonomy: 18 fixtures, all CERTAIN (a:13, b:5), 10 with book refs, 3 transcripts hand-read. Classes applied correctly. No CANDIDATE in rates.
tool gates: all 4 tools stdlib-only (loaders, tokenizer, fixtures, census). fixtures.py imports loaders (local module, not third-party). No network. Read-only over corpus/**. ✓
disclosures noted:
  - Book store contains 4 non-Hawkins books (worker disclosed) — M3 must not cite these as doctrine
  - Clean set stored as sha256 pointers (not copied text) — correct for public repo
  - Sedona Dec 2008 P2 is bilingual (Korean interpreter) — language detectors must expect non-English
  - ASR repetition loops observed (No.×26, Okay.×22) — M2 candidates, not filed as fixtures
  - Worker erratum: class split is a:13 b:5 (corrected from a:12 b:6)
minor notes:
  - Fixture field names use shorthand (quoted, paragraph, char_offset) vs STANDARDS spec (quoted_text, location). Content is semantically equivalent; tests pass. Not a gate failure but noted for taxonomy discipline.
  - M1 delivered as 3 focused commits (loaders+tokenizer, fixtures+clean set, hand-found fixtures) — clean task boundary.

2026-09-24 CYCLE 41 — GATE: TASK-003 (M0 supplement: extra-sources census) — worker sha 863c97d
verdict: PASS
suite: 32 tests OK (25 pass, 7 skipped — corpus-dependent in scratch worktree)
test count: 32 (up from 30 — no tests dropped) ✓
spot-checks:
  - extra-sources sha256: Barret (eff8b8b1c99f), discord (0ad660acfbab), phone (655a84b26136) — all match corpus ✓
  - extra-sources sizes: 159279 + 52450 + 1260717 = 1472446 B — matches table ✓
  - book store listed separately: 14634979 B, sha256 c0892fcd2050… ✓
  - scope markers: all 3 files marked UNDECIDED per VISION ✓
  - scope boundary table: overlays IN SCOPE, book store IN SCOPE, extra-sources UNDECIDED, rest OUT OF SCOPE ✓
taxonomy: N/A (census task only)
tool gates: census.py regenerated with extra-sources support. Stdlib-only. ✓
criterion 3 (REDIRECT-002): NOW MET — extra-sources fully censused with sha256 and VISION scope markers. M0 gate CLOSES.

2026-09-24 CYCLE 42 — GATE: TASK-004 (M2 detector family A) — worker sha 74ed664 (head), deliverable sha e7892b8
verdict: PASS
suite: 50 tests OK (40 pass, 10 skipped — corpus-dependent in scratch worktree)
test count: 50 (up from 32 — no tests dropped) ✓
spot-checks (run on my local corpus extraction):
  - A2-nonsense on Love Sep 2011 P1: catches "255%" @ offset 4543 (impossible percent) ✓
  - A2-nonsense on Love Sep 2011 P1: catches script-mix "động" (Vietnamese) and "杛" (CJK) ✓
  - A1-repetition on Love Sep 2011 P1: catches "No." ×26 @ offset 31214 ✓
  - A1-repetition on Love Sep 2011 P1: catches "which all the energies are negative" ×4, "It is discovered that to be loved" ×5 ✓
  - all 3 detectors self-test: OK (printed at suite end) ✓
  - clean-set FPs: 0/59 each (A4 uses held-out lexicon per book) ✓
taxonomy: detections output as CANDIDATE (single detector) or HIGH (≥2 converging), never auto-CERTAIN — correct per STANDARDS. Finding records use STANDARDS format.
tool gates: 3 detector modules + run_detectors.py — all stdlib-only, no network, read-only over corpus/**. ✓
disclosures noted:
  - A4-confusion: 8/18 fixture hits are ALL seeded (not independent recall). Independent recall = 0/18. A4 cutoff calibrated 0.80→0.82 on clean set after 2 FPs. Honest disclosure.
  - Drop-word and speaker/format detectors NOT shipped (could not meet fixture-hitting criterion). Honest — preferred over shipping a non-functional detector.
  - Dry run: 1264 unreviewed records across 210 transcripts (A1 937, A2 171, A4 155, 1 HIGH). Not committed, not a findings ledger — correct, M5 owns the sweep.
  - Korean interpretation in Sedona deliberately not flagged by A2 — correct handling.
noted for M4 (self-improvement loop): A4's seeded hits are not precision evidence; the self-test lexicon must grow through hand-read fixture expansion, not seed injection.

2026-09-24 CYCLE 47 — GATE: SELF-M3a (M3 item 1: book-passage retrieval) — worker sha d249c0c
verdict: PASS
suite: 57 tests OK (45 pass, 12 skipped — corpus-dependent in scratch worktree)
test count: 57 (up from 50 — no tests dropped) ✓
spot-checks:
  - eval_fixtures recall@5: 6/10 book_ref fixtures hit (CF-002@5, CF-004@5, CF-005@5, CF-010@4, CF-012@3, CF-015@3) — matches worker's report ✓
  - misses: CF-001 ("Dilgo. Quince." — too short for TF-IDF), CF-003 ("255%" — numeric, not a book quote), CF-006 (repetition loop), CF-017 (list/table text) — all reasonable TF-IDF limitations
  - non-Hawkins exclusion: Be_as_you_are, I_AM_THAT, Lamsa_bible, ACIM_workbook excluded from index ✓
  - stdlib-only: uses collections, math, re, sys — no external deps ✓
tool gates: retrieval.py stdlib-only, no network, read-only over corpus/**. ✓
notes: self-served by worker (orchestrator at cap, no OPEN task visible). Legitimate per role spec (CANON §7, worker role "No orchestrator lane yet, or no OPEN task → self-serve"). This is M3 item 1 of ~4; remaining M3 items: contradiction detection, terminology drift, misquotation.

2026-09-24T23:27:14Z CYCLE 1 — SUCCESSOR CORRECTION AND INDEPENDENT RE-GATE (all preceding lines imported byte-for-byte from predecessor arena/01a0d582-fleetyard @ 191b1f8a61d3fb2fd6d59c540c3acb2cee635319; do not treat its cycles 41+ as authoritative). Worker frozen head 90080502f9b065be7e70addf121b425690e21359, fetched by explicit refspec. Scratch worktree /tmp (not the predecessor lane), frozen corpus extracted from docdocgo-fixes.zip SHA-256 3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db; book JS SHA-256 c0892fcd20502d49b99fffe87a4ec4b3b5ecc94a1f98606aab7909127934a4a8. 230 .txt + manifest.json.
Suite actually run WITH corpus: `python3 -m unittest discover -s tests -v`: `Ran 57 tests in 18.609s` / `OK` (57 passed, 0 skipped); self-test stdout `A4-confusion self-test OK`, `A2-nonsense self-test OK`, `A1-repetition self-test OK`. `python3 tools/fixtures.py verify`: `fixtures OK`. Independently parsed the JS books without importing worker loaders and checked offsets/hashes: 24 books; all 18/18 transcript quotes at (paragraph 0, char offset), 10/10 cited book passages at book offsets, 59/59 clean-pointer SHA-256 values exact; 3 distinct transcripts; 13 a, 5 b. `python3 tools/retrieval.py --eval`: `book_ref recall@5: 6/10` (CF-002/004/005/010/012/015 hits; CF-001/003/006/017 misses). Stdlib module imports inspected; no network use; run_detectors --out is designated output, corpus read-only. No tests dropped.
Detector evaluation ACTUAL output from `python3 tools/run_detectors.py --eval`:
| A1-repetition | 2/18 CF-005,CF-006 | 0 | 0/59 passages |
| A2-nonsense | 1/18 CF-003 | 0 | 0/59 passages |
| A4-confusion | 0/18 | 8 CF-001,CF-002,CF-004,CF-010,CF-011,CF-012,CF-013,CF-017 | 0/59 passages |
These fractions are fixture overlap/recall, NOT measured precision. A4 8 hits all seeded `seed:CF-xxx` and its threshold was fitted on the original 59 clean passages: A4 0/59 is VOID as independent false-positive evidence (owner errata §3); do not use it for certification or M5. A1/A2 clean checks are measurements on original set, not estimates of unseen-set FP. No detector precision figure exists. Spot-run on Love_Sep_2011_Part_1: 9 unreviewed records, all CANDIDATE; A2 `255%` @ 4543, A4 `Dilgo. Quince` @ 5292 (seeded), A1 `No.` repeated 26 times @ 31214 — each record's quote at the emitted char offset matched frozen transcript bytes. These are NOT confirmed findings/rates.
REDIRECT-005 correction to inherited CYCLE 42 PASS: TASK-004 acceptance criterion 4 (`Each detector catches >=1 of the 18 confirmed fixtures`) was FAILED by A4's 0/18 independent fixture catches; A4 seeded hits do NOT count. That PASS only supports A1/A2, runner, self-tests/suite and stdlib/no-network boundaries, not A4's criterion 4 nor a milestone. Drop-word + speaker/format not shipped. Owner ERRATA-2026-09-25 §3 controls: M2 ACCEPTED INCOMPLETE (deferred gap to M4 fixture expansion), never `M2 PASS`/CERTIFIED. M5 excludes A4 until independent recall and a genuinely held-out clean FP test; no unreviewed signal in headline rates.
SELF-M3a RETRIEVAL: successor re-gate PASS for retrieval alone @ 90080502f9b065be7e70addf121b425690e21359: 6/10 quoted book refs in top 5, cited book offsets checked, 4 non-Hawkins excluded, stdlib/no network; NOT a certification of M3/TASK-005.
M1 TASK-002 finding-quality re-gate: FAIL criterion 4's requirement that each confirmed fixture have an evidence class a/b/c **per STANDARDS**. CF-009 @ Love_Sep_2011_Part_1 paragraph 0 char 315 is byte-exact `it's some wonderful`, proposed `it's so wonderful`, recorded CERTAIN/class a, but its own evidence explicitly calls the utterance a `non-doctrinal announcement`. STANDARDS class a requires an ungrammatical/senseless text AND a near-form that restores **both grammar and doctrinal sense**. No doctrinal proposition, book leg (book_ref null), or lecture contradiction leg is given. Grammar alone does not establish CERTAIN under the current law. Citation exactness is not confidence proof. CF-002 (author-name misspelling, class a) merits the same test; no independent verdict on CF-002 yet. Freeze disputed fixtures out of headline counts; no M1 certification until repair re-gated. M0 certification stays (owner §2, BOSS ratified) and is not vacated. Pause paired with TASK-006, acceptance = repair this failed criterion without weakening the definition or dropping below the 15-confirmed/3-transcript floor. No taxonomy definition changed. A later actual PASS removes the pause; worker TASK-005 remains CLAIMED and resumes from its lane state.

2026-09-24T23:46:00Z CYCLE 3 — NEW WORKER HEAD / TASK-005 M3 DELIVERY GATE + REDIRECTED RUNNER RE-GATE. Explicit-refspec fetch verified worker f1658891a7e9d222a881c5b5384db0e6100b228f (deliverable 1e1c57b9b1a61eaf81c1419a6e4755c7e3b76f68; heartbeat d70d4b9937c57479ef4483f130b9b66c5e9491ae; PAUSE observed, TASK-006 claimed at f165889), boss a78804f88c0f991f1767e8f61cf572f5a5ff2dd7 (REDIRECT-006 to PREDECESSOR only), main 3900071e4d8e25b3923858efe7df31a10f9f9358. Scratch worker worktree replaced with detached f165889, SHA-verified corpus symlink read-only; `python3 -m unittest discover -s tests -v`: `Ran 78 tests in 43.880s` / `OK` (78 pass, 0 skipped, count up from 57); self-test stdout `A4-confusion self-test OK`, `B1-contradiction self-test OK`, `B2-misquote self-test OK`, `A2-nonsense self-test OK`, `A1-repetition self-test OK`; `python3 tools/fixtures.py verify`: `fixtures OK`. Checked new modules' imports/writes: Python stdlib, no network, runner writes only named `--out`, corpus read-only.
`python3 tools/run_detectors.py --eval` ACTUAL rows (fixture overlap = recall, NOT precision):
| B1-contradiction | 2/18 CF-003,CF-006 | 0 | 0/59 passages |
| B2-misquote | 1/18 CF-015 | 0 | 0/59 passages |
A1 2/18, A2 1/18, A4 0 independent/18 + 8 seeded unchanged; 0/59 printed for all five. B1/B2 fixture hits independently located; B1 book values parsed from Hawkins books rather than typed constants, B2 near-verbatim TF-IDF alignment; 4 non-Hawkins books excluded as doctrine. Sample runner --family AB on Love Sep 2011 P1 + bilingual Sedona Dec 2008 P2: 26 unreviewed raw records, 23 CANDIDATE + 3 HIGH. Love P1 @4543 A2+B1 `255%` → proposed `55%`, book `Courage 200 55` in reality_spirituality_and_mode at cited offset: both transcript and book quote independently re-read byte-exact. Love P1 @2318 A1+B1 repeated `which all the energies are negative...`, book `At level 200, energy goes positive` in healing_and_recovery: exact. Sedona P2 @5854 B2 `no influence. Interest` → `no interest`, cited the_map_of_consciousness_expla `Spiritual purity has no interest in the personal lives of` at the exact book offset (same teaching as the fixture's other book); transcript bytes exact. One 10-passage independently selected spot negative sample (first 10 sorted Hawkins books, next sentence after 11% of each, 700 chars, disjoint from legacy 59, exclude own book for B2) yielded B1 0/10 and B2 0/10. These small observations are NOT claimed as detector precision, general FP rate, or a released findings ledger.
TASK-005 verdict: FAIL for full tool-quality criterion 3 / CERTIFICATION HOLD. Code modules, self-tests, independent fixture overlap, suite, runner integration and exact book refs PASS scoped implementation checks (#1,#2,#4,#5,#6,#7); however `tools/DETECTORS.md` disclosures 7–8 admit B1 thresholds calibrated on the clean set/book store and B2 filters adjusted after the 59 clean fixtures. Their printed 0/59 is an *in-sample check*, not an independent clean-set FP measurement required to certify a detector (same leakage defect as A4). Human-reviewed flagged-span precision is also UNMEASURED (worker honestly discloses it). TASK-009 is the focused repair of criterion 3 using new held-out book pointers from TASK-007; do NOT inherit the 0/59 as an M5 rate. M3 is NOT certified: terminology drift and explicit book-attribution handling remain unimplemented despite the narrow B1/B2 delivery, to be separately cut. TASK-005's production effort stands; this is an evidence gate, not an instruction to rebuild it.
Additional independent taxonomy failure in inherited TASK-004 runner, now observed under --family AB: bilingual Sedona Part 2 paragraph 0 char 9671 prints `HIGH CONFIDENCE` for A1-repetition+A2-nonsense. Re-read transcript context: English speech `allows you to say yes or no without any consequences` immediately followed by Korean interpreter text with **legitimate Korean particles** `yes나` / `no를` repeated four times. A1 finds an 11-token unit repeated 4 times @9671..9858 (possible ASR repeat, CANDIDATE); A2 wrongly tags each `yes나` and `no를` (8 signals at 9697..9846) as "script-mix: mixed/foreign letters in token". A2's code-switch is NOT evidence of a transcription error, so the two nominal detectors do not furnish two INDEPENDENT error signals for STANDARDS HIGH. No proof leg; do not promote or headline-count this record. Runner taxonomy gate FAIL; repair TASK-010 with negative bilingual regression fixture. Owner M2 remains ACCEPTED INCOMPLETE, not revoked/re-certified. The worker is already PAUSED for TASK-006; append these failures as sequenced repair duties (do not interrupt TASK-006 mid-flight), no new M1/M2/M3 certification. After TASK-006 PASS switch PAUSE to TASK-010; after its PASS pursue TASK-007 then TASK-009 before releasing family B metrics. Do not claim a prior PASS for any criteria that this gate shows FAILED.

2026-09-24T23:58:00Z CYCLE 4 — TASK-006 (M1 taxonomy fixture repair) SUCCESSOR GATE. Explicit-refspec fetched worker 9f56f3e533af49f003f493cb3a6d7c6dd570915d (deliverables 7c90c94, 0741fd6; heartbeat 9f56f3e), boss 8f3a181574018ae560e5731d20efaa8606e486c6, main 3900071e4d8e25b3923858efe7df31a10f9f9358; own STOP absent. Boss cycle 5 independently CONFIRMED the original CF-009 gate failure and recognised successor; no new order. Scratch detached worker head @ 9f56f3e with frozen corpus. ACTUAL `python3 -m unittest discover -s tests -v`: `Ran 87 tests in 46.562s` / `OK` (87 pass, 0 skipped, up from 78, no drops); `python3 tools/fixtures.py verify`: `fixtures OK (16 confirmed CERTAIN)`; five detector self-tests OK. `python3 tools/run_detectors.py --eval` ACTUAL rows: A1 `1/16 CF-006`; A2 `1/16 CF-003`; A4 `0/16` independent + `7` seeded (CF-001/002/004/010/011/012/017); B1 `2/16 CF-003,CF-006`; B2 `1/16 CF-015`; each prints `0/59 passages` in a column expressly marked `(in-sample 59; tune set, NOT an independent FP rate)`. No precision estimate. `python3 tools/retrieval.py --eval`: `book_ref recall@5: 9/15` — denominator changed from the former 10, not a retrieval algorithm improvement.
Independent read, NOT worker verifier alone: decode JS book store with separate simple literal parser; 24 books; 16/16 current CERTAIN quotes match byte-exact transcript text at paragraph 0 + claimed char offset; 15/15 book references match exact decoded book passage at cited char offset; 59/59 clean pointers match SHA-256; 3 transcript files; no mismatches. Compare prior 18 records from worker f165889 to current 16: append-only correction file has seq 1..22 with all 18 originals accounted for, full original snapshots of six withdrawals are byte-identical JSON to former records and STILL cite frozen text exactly; 4 additions CF-019..022 each cite a book and state hand-read provenance. Current class split a:9,b:7; transcript counts 10/4/2. All statuses in confirmed.json = confirmed/CERTAIN; withdrawn HIGH/CANDIDATE not in the 16-denominator. New CF-019 @ Love P1: `40% happiness` at 4226, same book row `200–300 8% 1.5% 60% 9.0%` at 148737, three other values exactly match slide; leg b supported. CF-020 @ Satsang IX P6: `calibrating at 380` at 14681 in explicit `Truth vs. Falsehood` / Enneagram question; cited book `Enneagrams\n\n390` at 778891, sole Enneagram calibration found by own scan; leg b text contradiction supported, but audio-vs-speaker source unknown. CF-021 @32998 `Perception and infatuation is exaggerated`, CF-022 @33186 `Productivity and infatuation is disrupted`: book confirms Hawkins' infatuation vs Love teaching and repeated slide frame uses `in`; acoustic near-form `and`→`in` restores grammar and doctrinal sense (same pattern as CF-007/008, distinct cited instances NOT independent patterns). CF-002 @15635 `Jerry Jempolski's book` now class b: book at 176547 attributes same named book/title to `Jerry Jampolsky`; class-a grammar-only rationale replaced with book-attribution leg; allowed under VISION's stated default pending owner's other-author ruling. Even excluding this one disputed attribution leaves 15 presently supported CERTAIN; caveat recorded in M1 certificate.
Verdict: TASK-006 PASS (paired repair resolves TASK-002 finding-quality criterion 4 at worker 9f56f3e; M1 foundation all tasks now gated). Repaired fixtures are not detector precision/rates. Independently CERTIFY M1 on this successor lane, evidence index `fleet/queue/pending/M1-CERTIFIED.md`; M0 owner/BOSS-ratified stands. Remove the prior PAUSE reason for TASK-006 and replace the transient control with a NEW PAUSE for independently failed TASK-004 runner taxonomy, repair TASK-010 only (cf. CYCLE 3 gate). M2 owner ACCEPTED INCOMPLETE, M3 held on TASK-009 and missing capabilities. Note lingering test flaw: tests/test_run_detectors.py `test_each_detector_hits_a_fixture` still counts seeded A4 hits as if satisfying criterion 4; its green result is NOT an A4 pass; add regression criterion to TASK-007 before M5. No cert or suite output stamped from predecessor.
