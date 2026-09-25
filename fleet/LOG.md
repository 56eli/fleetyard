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
2026-09-25T18:4xZ WORKER-2: owner ruling 25d re-grounded, resuming — ERRATA-2026-09-25d
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
2026-09-25T18:5xZ WORKER-2: owner ruling 1 — the nonce-shaped literal on main is INERT
AND RETIRED (v0 posture UNHASHED-OWNER-CHAT-ONLY; boot nonces single-use, consumed at
boot verification; re-verification binds to ACTIVATION ID + normalized registry record).
Retired from attention; not quoted further.
2026-09-25T18:5xZ WORKER-2: owner ruling 2 — manifest pin 4b65145d is the policy-bundle
SOURCE file; deployed fleet/ERRATA-2026-09-25c.md (sha256 7384a608…) is the instrument
OF RECORD and the authoritative hash. Manifest reconciliation deferred to 2.0.1; no file
edits (freeze extends to the manifest; changes ride errata).
2026-09-25T19:1xZ WORKER-2: M4-q2 — C1-drop detector built (tools/det_dropword.py,
self-test + 8 tests green; holdout-refusal enforced). Tuning run: 193 transcripts in
6 bounded shards (LAW §4A) -> 122 CANDIDATE-class raw signals; merge provenance
recorded. Hand-read sample: 4 confirmed omissions kept as provisional fixtures
fixtures/v2/dropword.json (D2-001..004, byte-bound), 5 parked/discarded. Classification
BLOCKED on proposed STANDARDS leg (d) (needs errata + BOSS CONCERN). No rates.
2026-09-25T19:2xZ WORKER-2: M4-q3 — C2-format detector built (7 mechanical rules,
self-test + 6 tests green). Tuning run: 193 transcripts -> 49 CANDIDATE-class format
signals (R1 22/R2 3/R3 5/R4 1/R5 15/R6 2/R7 1); holdout untouched. Scope census over
all 230 transcripts: 0 speaker labels / 0 stage directions / 0 parser residue, so
speaker attribution is NOT mechanically detectable here — recorded as an M6 limitation
(instrument finding). Two candidate rules measured and rejected as noise (camel-glue,
double-word). Next: q4 holdout runs (rates only; precision needs review), q5 A1 claims.
2026-09-25T19:3xZ WORKER-2: M4-q4 — one-shot holdout runs (thresholds frozen before
the run; holdout_consumed stamped): v1 A1,A2,B1,B2 185 raw signals (5.00/tx) and an
exact per-transcript reproduction of the inherited census (0 mismatches of 37 files);
C1-drop 5 signals (0.14/tx vs 0.63 tuning — flagged open question, sampling noise);
C2-format 12 (0.32 vs 0.25 tuning). Counts only: precision/recall still require human
review of holdout labels; no rate claimed anywhere. Holdout now spent for these
detector versions (new salt owed before any further tuning-informed evaluation).
2026-09-25T19:4xZ WORKER-2: M4-q5 — A1 claim-shape reconciliation CLOSED: all 98
"not re-derived" flags were defects in MY reducer (ASCII-only tokenizer; 8-token
search bound vs units up to 11), not in the v1 detector. Fixed with Unicode token
rule + kmax=16 and 2 regression tests; ledger regenerated: corroboration now
A1 938/938, A2 158/158, B1 12/12, B2 228/228, 0 flagged (1,336/1,336 signal claims);
classes unchanged (CERTAIN-inherited 3 / HIGH 0 / CANDIDATE 1331; seeded 3). Errata #2
appended to the M5-R delivery record; analysis in
findings/M4-q5-A1-CLAIM-RECONCILIATION.md. No detector change required.
2026-09-25T19:2xZ WORKER-2: ORCH-2 queue observed (ORCH-2 booted; TASK-013 gated FAIL/
INCOMPLETE on C6/C7/C8 at aed9df6; PAUSE-WORKER-A-2026-09-25-001 in force — only
TASK-016 actionable; M4 paused by control). TASK-016 repair implemented: R1 STANDARDS
record shape (suspected_intended + status/status_by on every finding), R2 coverage row
(230/230/230/0/230/24) in SUMMARY + README with qualified titles, R3 LAW §8 manifest
(tool_commit, policy sha, main head, book-store sha, inherited detector commit,
derivations for all digests); +3 tests (26 green); no classes/ledger substance changed.
M4 q3/q4/q5 deliveries (already pushed) stay PROVISIONAL-UNGATED and are not gated.
2026-09-25T19:4xZ WORKER-2: owner ERRATA-2026-09-25e read and logged — OPTION A
repair-first: M4-q2 + q3-q5 parked (DELIVERED-PROVISIONAL-UNGATED); TASK-016 is my only
task; STANDARDS gains narrow CERTAIN leg (d) (omission within a matched span) with the
122 drop-word signals and 4 provisional fixtures remaining CANDIDATE pending individual
adjudication (no adjudication performed while M4 is parked). TASK-016 taken: per-criterion
evidence (C6/C7/C8) added to the delivery record; fresh manifests bind main 25bdab9 then
8e9e179 with an identical ledger sha; 26 tests green.
2026-09-25T20:0xZ WORKER-2: ERRATA-2026-09-25f read and logged (liveness = signals not output,
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
2026-09-25T20:4xZ WORKER-2: TASK-018 in progress (claimed; items 0/0b pushed at 33b6f36). Adjudicator
tools/m4_q2_adjudicate.py built: per-signal leg-(d) test on re-derived bytes — maximal exactly-equal
flanks around the omission (floor 5 tokens/side; sensitivity published), single-word restoration must
complete the match; two-word omissions never promoted. Result: 57 of 122 signals CERTAIN-leg-d (all
clause (d)(i)), 65 CANDIDATE (48 restoration-not-minimal, 15 flank-too-short, 2 region-not-realignable);
fixtures: D2-001 + D2-003 confirmed, D2-002 + D2-004 discarded from any CERTAIN claim (two-word
omissions — narrowness is the point). 39 tests green (13 new). Artifacts under runs/m4-q2-adjudication/.
2026-09-25T20:5xZ WORKER-2: TASK-018 DELIVERED (fleet/branches/WORKER-2-TASK-018-DELIVERY.md):
57/122 CERTAIN-leg-d (all clause (d)(i); zero (d)(ii)), 65 CANDIDATE (48 two-word, 15 flank-too-short,
2 not-realignable); fixtures D2-001/D2-003 confirmed, D2-002/D2-004 refused promotion under the narrow
leg; L1-L6 evidence recorded; 57/57 promoted citations independently re-verified byte-exact; 39 tests
green; spent holdout untouched. Next: TASK-017 (v1 toolchain inheritance).
