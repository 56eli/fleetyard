# TASK-010 — repair false HIGH on legitimate bilingual code-switching

milestone: M2 runner integrity / M4 regression pattern
status: OPEN (priority AFTER already-active TASK-006 repair; only active if successor explicitly updates PAUSE-WORKER to name this task)
cut: 2026-09-24T23:46Z by successor orchestrator arena/01a0d5b7-fleetyard

## Failed criterion to repair
STANDARDS HIGH CONFIDENCE requires >=2 **independent** signals that converge, and CANDIDATE must never enter a headline rate. In the frozen bilingual `corpus/docdocgo/overlays/A_Unique_Sedona_Seminar_Dec_2008_Part_2_enxautogen_html.txt`, paragraph 0 at char **9671**, the Korean interpreter repeats a translated sentence four times. A1-repetition flags the repeat. A2-nonsense falsely flags the *legitimate Korean code-switch* `yes나` / `no를` (English words yes/no with Korean particles) eight times inside that same repeated span; the adjacent English speech says "allows you to say yes or no without any consequences." `tools/run_detectors.py --family AB` merges A1+A2 and outputs `HIGH CONFIDENCE` @9671 despite there being only **one defensible error signal** (A1 repeat; the language mix itself is normal). This breaches the runner's taxonomy gate; it is an unreviewed raw signal, not a confirmed finding. Owner/boss already cautioned that the Sedona interpreter is genuinely bilingual; do NOT treat all Korean as ASR garble. Preventing false certainty is the repair target, not suppressing genuine repetitions.

## Focused deliverable
Introduce a negative regression example with a verbatim passage/offset from the frozen Sedona transcript and the explicit context that `yes나`/`no를` is normal Korean grammar in the interpreter's translation. Fix A2's script-mix logic (or the merge's independence check, with justification) so the normal code-switch no longer counts as an error/convergent signal; the A1 repeat may remain CANDIDATE for human review. Preserve real script-mix detection on garbled short inserts (`spirit持`, Vietnamese `động`), impossible percentages and U+FFFD, with no overbroad language suppression. Log the pattern and fix provenance without changing STANDARDS class definitions.

## Acceptance = failed HIGH-confidence criterion + safety
1. At Sedona Dec 2008 Part 2, paragraph 0 char 9671, the verbatim phrase repeated four times with legitimate `yes나`/`no를` never yields `HIGH CONFIDENCE` solely via A1+A2; show the exact emitted detector IDs/confidence after the fix. A2 no longer flags those Korean-particle tokens as garble; A1 remains detectable if still a repetition.
2. Regression tests include the bilingual negative and ordinary positive garble/percent samples; no precision or independent recall is claimed from a fixture seeded into a detector rule. Suite green with test count >=78, fixture verification and A1/A2 confirmed catches preserved, existing book clean checks show no regression (the A4 0/59 is still void; a genuinely held-out FP check awaits TASK-007). No CANDIDATE blended into headline error rates.
3. Python stdlib only, no network, corpus read-only, writes limited to named tools/fixtures/tests/M4 pattern ledger. A later successor gate independently reproduces the corrected Sedona sample before this repair can PASS.

This task does not reopen owner-disposed M2 as a certification; M2 remains ACCEPTED INCOMPLETE, drop-word + speaker/format deferred to TASK-008.

REDIRECT-007 priority note 2026-09-25T00:12Z — this is the only ACTIVE repair under PAUSE-WORKER (worker CLAIMED @ 749a2e6); the M5 raw sweep TASK-011 follows its PASS, then M6 provisional report TASK-012. No early A4/held-out tasks can displace this repair or the ordered raw census/report. M2 remains owner ACCEPTED INCOMPLETE.

## Successor gate — 2026-09-25T00:21Z (append-only)
PASS @ worker c833bee089deaa75a0ecbac5820b4e09b874385a: independently ran 97 tests, fixture verifier and A/B eval; `NEG-001` hash/quote at Sedona P2 @9671 matches frozen transcript, A1 only CANDIDATE there, A2 zero, combined runner 16 CANDIDATE and zero HIGH on that transcript; positive A2 garble/255%/U+FFFD preserved. PAUSE-WORKER removed; this task CLOSED notwithstanding historical OPEN header. Next worker task TASK-011 M5 provisional raw sweep, not deferred TASK-007/009/008.
