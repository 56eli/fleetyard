# fleet log (append-only)
2026-09-25T18:26Z WORKER-2 (A-2026-09-25-001, lane arena/01a0d9ce-fleetyard): boot
fail-closed — registry record A-2026-09-25-001 failed the byte-exact check on main
2ed0b9b (nonce_hash line; no anchor, no hash chain; fleet2check rejects the registry).
No mission work started (M5-R not begun); read-only diagnosis + report only per LAW §1.3.
Alert: fleet/alerts/WORKER-2-FAIL-CLOSED.md. Awaiting owner.
2026-09-25T18:34Z WORKER-2: re-verification PASS after owner repair (main 5fdd00e;
registry a86115d2…; record A-2026-09-25-001 byte-exact; FORMAT v0 note = fleet2check
chain output ADVISORY). Fail-closed episode closed. M5-R begins (ORCH-2 queue absent,
self-served, disclosed).
2026-09-25T18:43Z WORKER-2: M5-R DELIVERY (findings/ ledger, 1334 findings from the
inherited census; CERTAIN-inherited 2 / HIGH 0 / CANDIDATE 1332; seeded 2,
independent 1332; 242/242 cited book quotes byte-exact; determinism verified).
DELIVERY, not certification — awaits ORCH-2 gate (no ORCH-2 lane yet).
2026-09-25T18:45:13Z (src 341ee2e) WORKER-2: owner ruling 25d re-grounded, resuming — ERRATA-2026-09-25d
read at main 25bdab9 (main churn = disclosed owner acts §1; registry rewrite = disclosed
exception §2 and frozen §6; A-2026-09-25-001 confirmed in force §5). Re-verified under
the NORMALIZED standard (§3): record 001 fields 6/6 equal (registry unchanged since
5fdd00e). M5-R delivered (8011439); continuing with M4.
2026-09-25T18:52Z WORKER-2: M5-R errata — fixture-overlap criterion corrected to
span-vs-span (CF-015 recovered): CERTAIN(inherited) 2→3, CANDIDATE 1332→1331,
seeded 3/1331 independent; reconciles with the v1 audit's 3-of-16 detector overlap.
M4 quantum 1: held-out split fixed before tuning (tools/HELD-OUT-SPLIT.json,
193/37 of 230), tools/m4_split.py + 7 m5r tests green, PATTERNS.md rule catalog
published (13 of 16 CERTAIN patterns still invisible to all detectors).
2026-09-25T18:52:41Z (src e07be0e) WORKER-2: owner ruling 1 — the nonce-shaped literal on main is INERT
AND RETIRED (v0 posture UNHASHED-OWNER-CHAT-ONLY; boot nonces single-use, consumed at
boot verification; re-verification binds to ACTIVATION ID + normalized registry record).
Retired from attention; not quoted further.
2026-09-25T18:52:41Z (src e07be0e) WORKER-2: owner ruling 2 — manifest pin 4b65145d is the policy-bundle
SOURCE file; deployed fleet/ERRATA-2026-09-25c.md (sha256 7384a608…) is the instrument
OF RECORD and the authoritative hash. Manifest reconciliation deferred to 2.0.1; no file
edits (freeze extends to the manifest; changes ride errata).
2026-09-25T19:06:53Z (src 012914d) WORKER-2: M4-q2 — C1-drop detector built (tools/det_dropword.py,
self-test + 8 tests green; holdout-refusal enforced). Tuning run: 193 transcripts in
6 bounded shards (LAW §4A) -> 122 CANDIDATE-class raw signals; merge provenance
recorded. Hand-read sample: 4 confirmed omissions kept as provisional fixtures
fixtures/v2/dropword.json (D2-001..004, byte-bound), 5 parked/discarded. Classification
BLOCKED on proposed STANDARDS leg (d) (needs errata + BOSS CONCERN). No rates.
2026-09-25T19:08:35Z (src 4425763) WORKER-2: M4-q3 — C2-format detector built (7 mechanical rules,
self-test + 6 tests green). Tuning run: 193 transcripts -> 49 CANDIDATE-class format
signals (R1 22/R2 3/R3 5/R4 1/R5 15/R6 2/R7 1); holdout untouched. Scope census over
all 230 transcripts: 0 speaker labels / 0 stage directions / 0 parser residue, so
speaker attribution is NOT mechanically detectable here — recorded as an M6 limitation
(instrument finding). Two candidate rules measured and rejected as noise (camel-glue,
double-word). Next: q4 holdout runs (rates only; precision needs review), q5 A1 claims.
2026-09-25T19:14:56Z (src 4e114f1) WORKER-2: M4-q4 — one-shot holdout runs (thresholds frozen before
the run; holdout_consumed stamped): v1 A1,A2,B1,B2 185 raw signals (5.00/tx) and an
exact per-transcript reproduction of the inherited census (0 mismatches of 37 files);
C1-drop 5 signals (0.14/tx vs 0.63 tuning — flagged open question, sampling noise);
C2-format 12 (0.32 vs 0.25 tuning). Counts only: precision/recall still require human
review of holdout labels; no rate claimed anywhere. Holdout now spent for these
detector versions (new salt owed before any further tuning-informed evaluation).
2026-09-25T19:16:05Z (src 2f55b0c) WORKER-2: M4-q5 — A1 claim-shape reconciliation CLOSED: all 98
"not re-derived" flags were defects in MY reducer (ASCII-only tokenizer; 8-token
search bound vs units up to 11), not in the v1 detector. Fixed with Unicode token
rule + kmax=16 and 2 regression tests; ledger regenerated: corroboration now
A1 938/938, A2 158/158, B1 12/12, B2 228/228, 0 flagged (1,336/1,336 signal claims);
classes unchanged (CERTAIN-inherited 3 / HIGH 0 / CANDIDATE 1331; seeded 3). Errata #2
appended to the M5-R delivery record; analysis in
findings/M4-q5-A1-CLAIM-RECONCILIATION.md. No detector change required.
2026-09-25T19:17:57Z (src dada3e6) WORKER-2: ORCH-2 queue observed (ORCH-2 booted; TASK-013 gated FAIL/
INCOMPLETE on C6/C7/C8 at aed9df6; PAUSE-WORKER-A-2026-09-25-001 in force — only
TASK-016 actionable; M4 paused by control). TASK-016 repair implemented: R1 STANDARDS
record shape (suspected_intended + status/status_by on every finding), R2 coverage row
(230/230/230/0/230/24) in SUMMARY + README with qualified titles, R3 LAW §8 manifest
(tool_commit, policy sha, main head, book-store sha, inherited detector commit,
derivations for all digests); +3 tests (26 green); no classes/ledger substance changed.
M4 q3/q4/q5 deliveries (already pushed) stay PROVISIONAL-UNGATED and are not gated.
2026-09-25T19:40:07Z (src 1beadd9) WORKER-2: owner ERRATA-2026-09-25e read and logged — OPTION A
repair-first: M4-q2 + q3-q5 parked (DELIVERED-PROVISIONAL-UNGATED); TASK-016 is my only
task; STANDARDS gains narrow CERTAIN leg (d) (omission within a matched span) with the
122 drop-word signals and 4 provisional fixtures remaining CANDIDATE pending individual
adjudication (no adjudication performed while M4 is parked). TASK-016 taken: per-criterion
evidence (C6/C7/C8) added to the delivery record; fresh manifests bind main 25bdab9 then
8e9e179 with an identical ledger sha; 26 tests green.
2026-09-25T19:55:50Z (src 10afc0d) WORKER-2: ERRATA-2026-09-25f read and logged (liveness = signals not output,
not output quiet; worker steady state = cycle indefinitely for work orders; under a scoped
pause stay paused and keep cadence only). Re-ground: registry a86115d2 unchanged/frozen,
policy 0fe20a60 unchanged, main 77f1d6d (owner rewrite of the 25e commit — disclosed churn per
25d §1). Manifest refreshed provenance-only to the reachable main 77f1d6d (ledger sha d42136c6
unchanged; overlays 027f82a0 and book store c0892fcd re-verified). Pause stands (ORCH-2 head
8ed8d12; control file present). Operating note, disclosed: the workspace was re-materialised
between turns — local .git had been reset to main@2ed0b9b with the lane history absent and the
untracked corpus/ + evidence/ trees missing. Recovered: branch reset to the remote lane head
1beadd9, inputs re-materialised via tools/m5r_inputs.sh (zip 3f36c520… verified; archive ref
bf97d85), all digests re-verified. Cadence watcher started (tools/cadence_watch.py, 300 s
control checks: heartbeat + CONTROL lines; watches pause/queue/main for work orders).
2026-09-25T20:38:02Z (src 9cd905d) WORKER-2: TASK-018 in progress (claimed; items 0/0b pushed at 33b6f36). Adjudicator
tools/m4_q2_adjudicate.py built: per-signal leg-(d) test on re-derived bytes — maximal exactly-equal
flanks around the omission (floor 5 tokens/side; sensitivity published), single-word restoration must
complete the match; two-word omissions never promoted. Result: 57 of 122 signals CERTAIN-leg-d (all
clause (d)(i)), 65 CANDIDATE (48 restoration-not-minimal, 15 flank-too-short, 2 region-not-realignable);
fixtures: D2-001 + D2-003 confirmed, D2-002 + D2-004 discarded from any CERTAIN claim (two-word
omissions — narrowness is the point). 39 tests green (13 new). Artifacts under runs/m4-q2-adjudication/.
2026-09-25T20:38:18Z (src 1fb524e) WORKER-2: TASK-018 DELIVERED (fleet/branches/WORKER-2-TASK-018-DELIVERY.md):
57/122 CERTAIN-leg-d (all clause (d)(i); zero (d)(ii)), 65 CANDIDATE (48 two-word, 15 flank-too-short,
2 not-realignable); fixtures D2-001/D2-003 confirmed, D2-002/D2-004 refused promotion under the narrow
leg; L1-L6 evidence recorded; 57/57 promoted citations independently re-verified byte-exact; 39 tests
green; spent holdout untouched. Next: TASK-017 (v1 toolchain inheritance).
2026-09-25T20:48:00Z (src b2e0761) WORKER-2: TASK-017 DELIVERED (fleet/branches/WORKER-2-TASK-017-DELIVERY.md): v1
toolchain inherited byte-exact from archive bf97d85 (tools 15 + tests 13 + fixtures 5 + committed
census runs/m5-raw 233 files = 266 files, all sha-matched against the archive; manifest
tools/INHERITED-V1-MANIFEST.json). Suite now 154 tests OK with corpus (115 inherited + 39 lane),
1 skip (M6 report not yet committed). fixtures.py verify OK (16 CERTAIN). Fresh sweep baseline:
sweep_m5 --limit 10 --fresh -> 132 records, 10/10 files byte-identical to the inherited census
(runs/m5-raw-freshcheck/). No detector logic modified. Next: cadence / await ORCH-2 gate + fresh
sealed split v2.
2026-09-25T20:50:46Z (src 293b29c) WORKER-2: TASK-019a DELIVERED (fleet/branches/WORKER-2-TASK-019A-DELIVERY.md):
split v2 sealed (tools/HELD-OUT-SPLIT-V2.json, sha256 f357ed21...) — fresh salt v2, rule published,
tuning 197 / holdout 33, forced 43 (6 fixture transcripts + the 37 read-once v1-holdout transcripts,
so the v2 holdout is entirely unseen: v1∩v2 holdout = 0); corpus file-list digest derivation written
into the seal; generator/verifier tools/m4_split_v2.py; 10 new tests (164 total green, 1 skip). No
evaluation run (019b blocked on ORCH-2 q2/q3 gates + frozen thresholds).
2026-09-25T21:06:06Z WORKER-2: TASK-014 q3 SHIPPING EVIDENCE rebuilt (fleet/branches/WORKER-2-TASK-014-Q3-EVIDENCE.md).
ORCH-2's q3 gate was INCOMPLETE on three shipping criteria; the missing measurements now exist:
fixture recall 0/16 (measured, stated), clean-set misfire 1/59 with the single hit traced to the book
store's own typography (power.When verbatim in the book at CL-026 — clean passages are known-good but
not certified artifact-free), rejected-rule probes republished verbatim (pattern+flags) with the
historic 35/18 camel figure marked superseded, and a LAW 8 manifest carrying tool_commit, main_head,
policy_sha256, detector_sha256 at head, corpus/split digests, output digest and holdout_reads []. New
run is over the v2 tuning half (197 -> 48 signals); the historic 193-transcript run was NOT replayed
(33 of its files are v2-holdout members) and is cited by digest 86c8f57d. The transcript/book-window
confound probe returned 0/48 but its control returned 0/15 on the same windows over fixtures that ARE
book text -> probe recorded UNINFORMATIVE, not reported as independence. 19 new tests; suite 183 OK,
1 skip. No detector changed, no threshold set, no rate claimed; C2-format is NOT promoted and the
restriction stands pending ORCH-2 re-gate.
2026-09-25T21:21:00Z WORKER-2: TASK-020 DELIVERED (fleet/branches/WORKER-2-TASK-020-DELIVERY.md) - M4 shipping-gap repair
for q1/q2/q3. New: tools/m4_q2_evidence.py + tools/m4_t20_supplement.py (34 tests) and the artefacts they
produce; runs/m4-q2-dropword/{EVAL,EVIDENCE-PROVENANCE,PROVENANCE-SUPPLEMENT}.json,
runs/m4-q3-format/PROVENANCE-SUPPLEMENT.json, fixtures/v2/dropword.json (appended only: 87 insertions, 0
deletions). Measured: fixture recall 0/16 for both detectors (CF-015 missed because its difference is a
substitution - replace x2/delete x1/equal x2, no insertion op; stated from the bytes); clean set 3/59
(C1-drop, all cross-book self-parallels) and 1/59 (C2-format, book-store typography power.When), both
reproducing ORCH-2's probe; the additive source-inheritance filter gives raw 122 -> filtered 114 (7 deferred
to protect the v2 holdout; 1 inherited reproduces the gate) and 48 -> 48, with the clean set 3 -> 0 and
1 -> 0; the 122 shipped C1-drop signals adjudicated (3 dropped-token-not-missing excluded - the gate's own
three, 5 partial-overlap re-labelled, 1 gate hyphen case excluded pending a human read) for an independently
reconciled bound of 113; threshold provenance published for all eight C1-drop params (chosen by inspection
on the v1 tuning half; sensitivity study impossible under split v2 because 33 v1-tuning files are now v2
holdout) and for C2-format's shape rules with both rejected rules verbatim. Split v2 was re-sealed once this
shift (73d86f0d, same salt/rule/buckets) so its manifest binds the tool's head revision; disclosed. Suite 217
tests OK, 1 skip, WITH corpus (baseline 115). No threshold changed; no rate or precision claimed; C1-drop and
C2-format stay not promotable; TASK-019b still blocked on ORCH-2 re-gates.
2026-09-25T21:27:18Z WORKER-2: TASK-020 items 9-11 delivered. (9) runs/m4-q4-holdout/PROVENANCE-SUPPLEMENT.json (0a1fd43c...) with book-store+corpus digests, tool_commit/main_head/policy, per-part config and output digests (v1-holdout.json cf8e7a7a4f2c..., 127733 bytes), the v1 toolchain re-cited as lane+commit+blob (origin/arena/01a0d581-fleetyard:tools/<file>) with 13/13 pins re-verified against that lane, and an explicit B1-contradiction 0 whose consequence (no validation; v1 B1 headline hold stands) is stated; tools/m4_q4_supplement.py + 10 tests; the spent holdout was not re-run. (10) The 'dominated by sampling noise' claim corrected by append in PATTERNS 5d and the q4 README with exposure-normalized arithmetic WORKER-2 re-derived independently (holdout 14.9% shorter; v1 185 vs 187.9 P=0.44; C2-format 12 vs 8.0 P=0.94; C1-drop 5 vs 19.9 P=7.7e-05 = real ~4x deficit), both candidate causes recorded and the never-re-run prohibition stated; the density column renamed to 'signals/tx - density, not a rate'. (11) The three live documents still calling 64977c2f 'current' now carry append-only supersessions naming d42136c6 and the regenerating commit a4c6655, with the binding-of-record rule (findings/PROVENANCE.json); the reconciliation doc also carries the corrected numbers: 938/938 A1 claims recounted by me, ORCH-2's pre-q5 tally 97=9 zero-ASCII-token+61 over-bound+27 ASCII-mismatch, claimed units running to k=12 with exactly 9 claims so kmax=16 has 4 tokens of headroom (published with the full tally), and the hyphen sensitivity 255/938 (27%) cited as the gate's measurement. CONTROL.log's own digest line was left untouched. Suite 227 tests OK, 1 skip, WITH corpus.
2026-09-26T00:46:30Z WORKER-2: post-seal integrity adjudication + TASK-019b prep. (a) The v2 seal's own tripwire fired benignly: fixtures/v2/dropword.json now hashes c40d272f30d0 (a5dec38) against the seal-time c8e963199a1e. New tools/m4_seal_audit.py (+7 tests) adjudicated it from git bytes — append-only (no fixture added, no sealed value mutated — mutations empty), and the sole cited confirmation artefact runs/m4-q2-adjudication/fixtures-adjudication.json (61568a9e) is commit 1fb524e, 13 minutes BEFORE the seal commit 79eb401. Verdict STANDING (appendix owed): split v2 not void, no new salt, seal file untouched (73d86f0d); report runs/m4-q2-adjudication/SEAL-AUDIT.json, appendix SEAL-APPENDIX-2026-09-25.md; defect class stated (a seal-time digest over an append-only annotation target yields a benign tripwire) with a build-time recommendation for future seals. (b) TASK-019b harness built and NOT run: tools/m4_one_shot_v2.py (freeze/run/score/verify) + tools/c2_detectors.py + 10 toy-corpus tests; the one-shot discipline is enforced by the tool (no freeze => refuse; receipt exists => refuse and name the new-split rule; post-freeze detector edit => refuse; partial read => refuse), scoring separates seeded from independent and never blends CANDIDATE. Preparation record fleet/branches/WORKER-2-TASK-019b-PREP.md. (c) Sandbox lost corpus/ and evidence/ (never committed); re-materialised via tools/m5r_inputs.sh and re-verified — corpus zip 3f36c520, book store c0892fcd, ledger d42136c6 (1334), by-transcript c1ec4da8 (230), split v1 481d8513, split v2 verify OK, q4 supplement 13/13 pins OK. Suite 244 OK 1 skip WITH corpus. No threshold changed, no detector edited, no rate or precision claimed, v2 holdout never opened.
2026-09-26T00:47:00Z WORKER-2: counter note — CONTROL.log seq is max(seq)+1, not last-line+1: the 21:27:18Z line (written before this shift) sits out of order with seq 39 after 40, so a last-line read repeats a number. This cycle's line was corrected 40 -> 41 before commit; the historic duplicates (38 at 21:06/21:21, 39 at 21:21/21:27) are left as written — append-only, and named here rather than edited.
2026-09-26T00:58:50Z WORKER-2: TASK-020 item 8a repaired — generator attribution. The gate's finding was that tool_commit alone (as lane head at run time) never reaches the code: q2 pins 71c37cf, q3 EVAL 2bbb9f6, q4 ffb8811 (a cadence commit) contain neither tools/m4_t20_supplement.py nor tools/m4_q2_evidence.py. All six artefacts (q2 PROVENANCE-SUPPLEMENT / EVAL / EVIDENCE-PROVENANCE, q3 PROVENANCE-SUPPLEMENT / EVAL, q4 PROVENANCE-SUPPLEMENT) now carry generator_pins: generator_tool, generator_tool_commit (full sha), generator_tool_blob (origin/arena/01a0d9ce-fleetyard:tools/<file>), generator_tool_sha256 and a note separating the two commits. tools/m4_pin_repair.py + 5 tests; report runs/m4-pin-repair-2026-09-26.json with old->new digests. Each artefact was rebuilt with its own generator + recorded args and is byte-identical to the committed file; that rebuild also caught and corrected two stale cross-references (q2 EVAL provenance_sha256 605a6495->c1285e01, q3 EVAL afeb5306->b2bf6ad7 — same staleness class as item v2.a). Generator tools emit the block on build; t20/q4 supplements refuse to overwrite a manifest recording another generator. No threshold changed, no detector edited, no rate claimed, holdout reads 0.
2026-09-26T01:14:30Z WORKER-2: TASK-018 items 0d-0g repaired (append-only). 0d: the false "4 of the 57 are seeded" sentence (SUMMARY + PATTERNS §5b-bis) is contradicted by append — rows with seeded:true = 0/122 and 0/57, overlaps with the 16 v1 CF fixture spans = 0/122, and the four seeded rows are FIX-D2-001..004 in fixtures-adjudication.json. 0e: dedupe rule published — 57 promoted rows = 55 distinct sites, key (transcript, restored_span text), collisions D-097/D-098 (percent) and D-120/D-121 (see). 0f: strata published with my own per-word list (27 interjections/fillers · 6 notation · 11 function words · 13 content), the notation class is REFUSED under the enacted narrow leg (the transcript writes the symbol where the book writes the word — no word is absent; reversible only by an owner ruling), the standing statement that speaker-side filler presence is unknowable from text (no audio heard) is published, and every quotation of the number carries the floor band 3/5/8/10 → 71/57/33/22. 0g: D-002 (evidence) and D-039 (quite) are demoted with the reason each sibling instrument gives (EVAL.json shape adjudication; the source-inheritance filter), and the seven rows on v2-holdout transcripts (D-092/093/094 promoted, D-095/107/108/122 CANDIDATE) are marked holdout members. Fifteen disposition lines were APPENDED to adjudication.jsonl with reasons and exact utc; the 122 base signal lines are untouched (their digest is compared against PROVENANCE.json and published), so the tool's determinism test now compares the signal lines. Recount with arithmetic: 57 − 6 notation − 2 demoted = 49 rows; 55 − 5 notation sites − 2 = 48 sites; strata after exclusions 27 + 0 + 11 + 11 = 49. tools/m4_t18_dispositions.py + tests/test_m4_t18_dispositions.py (6 tests); corrections appended to SUMMARY.md, a §3 row qualifier inserted in PATTERNS.md and §5b-ter appended. No threshold changed, no detector edited, no rate or M6 figure.
2026-09-26T01:26:40Z WORKER-2: TASK-019 gate items v2.a and v2.b discharged. New dated file tools/HELD-OUT-SPLIT-V2-NOTE-2026-09-26.md beside the seal: (v2.a) binds the actual fixtures/v2/dropword.json digest c40d272f where the seal records c8e96319, leaves the superseded line readable, records the append-only adjudication (no fixture added, no sealed value mutated; the only confirmation artefact 61568a9e is commit 1fb524e, 13 minutes before the seal 79eb401), states the defect class (seal-time digest over a later-amended file = benign tripwire) and recommends a build-time fix for future seals; the seal file itself is untouched at 73d86f0d. (v2.b) states the taint (four holdout transcripts carrying seven signals — D-092 percent, D-093 it's, D-094 huh promoted, D-095/D-107/D-108/D-122 CANDIDATE), the endorsed deliberate deferral, ORCH-2's gate re-derivation of all 122 span bytes as re-derivation not tuning, and the seal's standing caveat verbatim ("a first figure under v2 is an estimate under this split, not a pristine out-of-sample number"). Quantum-b consequence pre-registered BEFORE the run: the four label-tainted transcripts are excluded from the denominator (evaluated 29 of 33) — machine-readable in tools/HELD-OUT-SPLIT-V2-EXCLUSIONS.json, bound into the freeze, enforced by tools/m4_one_shot_v2.py (post-freeze exclusion edits refused, excluded signals dropped unexamined, receipt lists evaluated/excluded separately). tools/m4_seal_audit.py now finds the dated note and reports STANDING (dated note on file); 19 harness+audit tests green. No threshold changed, no detector edited, no rate or M6 figure.

2026-09-26T00:58:09Z WORKER-2: TASK-020 items 15a/15b repaired. Item 15a: the q2 EVAL note named the alphabetically first transcript (A_Review_of_the_Work_Sep_2007_Part_1, which carries ZERO q2 signals) because it was built from sorted(signals)[0]; the row it explains is D-058 in Positionality_and_Duality_Transcending_the_Opposites_Apr_2002_Part_2 @40831 (27 signals), transcript "states the" where the book (the_evolution_of_consciousness @307559) writes "States. One-third of the". The generator now derives the transcript from the row itself, and the artefact preserves the misnamed text verbatim in note_correction_2026_09_26 so the defect is auditable, not erased. Item 15b: two DIFFERENT sets of 114 signals were published under one number; two_distinct_114s names both - filter side 122 - 1 source-inherited (D-039 quite @457) - 7 deferred holdout = 114, shape side 122 - 3 dropped-token-not-missing - 5 partial-overlap = 114 - with the recomputation published: 106 sites counted by both, 8 differing in each direction, the two exclusion sets disjoint (intersection 0), plus the explicit site lists in runs/m4-q2-dropword/NOTE-2026-09-26.md; the published bound of 113 is unchanged (shape side minus D-058). Rebuild attribution: generator commit cc9ba4617c3844146caa65a621aa738904429ec1 (tools/m4_q2_evidence.py, blob 667409aa), EVAL.json 2baefc09 -> d1e702af, EVIDENCE-PROVENANCE.json c1285e01 -> 982f8d66, both byte-identical on a SECOND rebuild from the recorded args, artifact generator_pins now names cc9ba46 and the artefact carries rebuild_history recording its own prior digest and prior generator pin (8a -> 15 readable in-file); runs/m4-pin-repair-2026-09-26.json refreshed (all six already-present, current digests) and pin repair verify 6/6. Suite 257 tests OK, 1 skip, WITH corpus (244 -> 257 = +5 item-8a tests, +6 0d-0g tests, +2 v2 exclusion tests). CONTROL entries 42/43/44 cited the lane head at write time; the appended ERRATA (seq 45) states that convention and names the commits that actually carry each described batch (7de00df / 7d14685 / c5b5b25) - nothing else in those entries changes. No threshold changed, no detector edited, no rate, holdout not opened.

2026-09-26T01:04:37Z WORKER-2: TASK-020 items 11a/11b/12 repaired. (11a) The v1 exposure row is 185 observed vs 187.6 expected, P=0.4451; the 187.9/0.44 this lane published came from 1,151 detector ROWS where the census holds 1,149 RECORDS (two records in Love_Sep_2011_Part_1 carry two v1 families each: A1+B1 and A2+B1) - the gate's figure is right and the PATTERNS 5d + q4 README correction-2 blocks now say so, with the tuning-side counts published per row (v1 1,149 records / 1,151 rows: A1 776, A2 143, B2 220, B1 12; C1-drop 122; C2-format 49) and the exposure ratio 0.1632327 re-derived at head. (11b) The q5 number treatment is superseded: 97 = 9 zero-ASCII-token + 61 over-bound + 27 ASCII-mismatch (the gate's independent simulation, authoritative for quoting), with my own pre-repair recount stated by its exact rule (98 = 9 + 61 + 28; residual 18 hyphen-bearing + 10 digit-bearing spans) and the one-row difference disclosed rather than smoothed over; the largest claimed unit is k=12 with exactly 9 claims (tally published, sum 938), so kmax=16 is max-observed + 4 tokens; 938/938 A1 claim_ok re-verified at head; the hyphen sensitivity is 255/938 (gate) vs 256/938 (mine), one row apart under the same tokenizer variant. (12) Criterion 20.14: the worker tree carried 40 asserted fuzzy timestamps in 11 files (the gate's 26 in 10 plus fleet/heartbeats/WORKER.log 10, WORKER-2-TASK-019b-PREP.md 1, the M5R item-11 supersession 1, and two LOG entries written after the gate's census) plus the own-time offender. All are now exact to the second with their source named - the committer time of the commit that introduced each line, recovered with git blame - and the old fuzzy values remain readable in backticks with a 'read' marker, so an audit sees both states; LOG and heartbeat beacons carry '(src <commit7>)' beside the exact value. tools/INHERITED-V1-MANIFEST.json's materialised_utc was a FORWARD stamp (20:5xZ, later than its own commit) and is now 2026-09-25T20:48:00Z with materialised_utc_source naming b2e0761; the 266 per-file hashes and the unmodified claim are untouched, JSON re-validated. The sealed fixtures/v2/dropword.json was deliberately NOT touched (its fuzzy value has an in-file exact sibling - the gate's INFO pattern - and the file is digest-bound by split v2). Census table + method: fleet/TIMESTAMP-CENSUS-2026-09-26.md. After: 0 asserted fuzzy timestamps. Suite 257 tests OK, 1 skip, WITH corpus. No threshold changed, no detector edited, no rate, holdout not opened.

2026-09-26T01:49:55Z WORKER-2: TASK-020 item 13 discharged (criterion 20.15). Two of the binding manifest's derivation notes were not literally executable: fixtures_digest_sha256 claimed the records-dir-relative convention for a digest computed over the two fixtures/confirmed files (basename keys; the clean/negative/v2 dirs are outside the binding), and overlays_digest named a wrong variant without saying how to build it. Both are corrected in findings/PROVENANCE.json and in the generator that emits them, so a rebuild keeps the correction; a json_canonicalization line and a derivations_revision block (exact time 2026-09-26T01:45:17Z with its source, and the invariance claim) were added. Verification is mechanical: new tools/m4_prov_check.py follows the manifest text literally and recomputes all nine published values - corpus zip 3f36c520, records d8c93536, fixtures c5d8f6f3, overlays 027f82a0, the warned variant 58274f46 (reproduced AND different from the published value), ledger d42136c6, by-transcript c1ec4da8, book store c0892fcd, tool_sha256 6d4bb9ce = blob at the run-time commit - every row PASS, exit 0. The repair is documentation only and that is proved: a rebuild with the run's arguments reproduces ledger.jsonl and all 230 by-transcript files byte-identically, and the manifest differs from the pre-repair file in derivations alone (921bbc56 -> dce2eb3a). 4 new tests; suite 261 OK, 1 skip, WITH corpus. Sandbox recreation at 01:44Z disclosed: .git had been re-cloned at the base commit, so the lane head was restored with an explicit-refspec fetch plus reset --hard, and corpus/ plus evidence/ were re-materialised with tools/m5r_inputs.sh (its own zip-sha check passing, 230 overlays, 230 record files); the only uncommitted work (this item's generator edit) was re-applied from the preserved working tree. No threshold changed, no detector edited, no rate, holdout not opened.

2026-09-26T01:54:50Z WORKER-2: TASK-020 item 14 discharged (criterion 20.16). The q4 holdout supplement's format leg published only the rules (digest 805241dd) against q3's published abbreviations + excerpt_chars + rules (8e7e35a2) - a reader comparing digests would have concluded the configurations differ. They do not, and the supplement now proves it: the format config is rebuilt from the detector module's own constants (tools/det_format.py @ ef9ff4f2, the blob this run used) plus the seven rules in force, byte-identical to q3's object, so the format leg's digest IS q3's 8e7e35a2 and PATTERNS 5d's exposure comparison rests on a digest match rather than an inference. Every leg now carries a config_digest_note (the q2 convention: sha256 over json.dumps(obj, sort_keys=True, separators=(',',':'))) plus a config_note stating what the object covers; the v1 and drop digests are unchanged and the drop leg remains identical to q2's by digest. Attribution: generator commit d85038c8 (blob d9ddb98d, recorded in the artefact's generator_pins), rebuilt with the recorded run arguments and byte-identical on a second rebuild; supplement digest af6af1b8 -> 9cfd82fa (the item-8a table row is superseded append-only); m4_pin_repair ARTEFACTS re-pinned and verify reports 6/6. Two new tests; suite 263 OK, 1 skip, WITH corpus. No threshold changed, no detector edited, no rate, and the spent holdout was not re-run - the tool reads committed artefacts only.
