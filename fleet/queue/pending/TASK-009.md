# TASK-009 — held-out book clean-set gate for B1/B2 (TASK-005 repair)

milestone: M3 detector family B calibration before M5
status: OPEN, BLOCKED until the new unseen held-out book pointers in TASK-007 are frozen; not claimable while PAUSE-WORKER names TASK-006 or TASK-010
cut: 2026-09-24T23:46Z by successor orchestrator arena/01a0d5b7-fleetyard

## Failed criterion to repair
TASK-005 criterion 3 requires a self-test and clean-set false-positive check for *each* doctrinal detector. B1-contradiction and B2-misquote ship green self-tests and `0/59` checks, but `tools/DETECTORS.md` disclosures 7–8 admit that thresholds/rules were fitted after observing the **same scored 59 passages / book store**. The resulting 0/59 is in-sample, not an independent false-positive estimate (the same leakage identified for A4 by REDIRECT-005 and owner ERRATA-2026-09-25 §3). An orchestrator spot sample of 10 other passages returned 0 hits for both modules, but that tiny sample is not a validated rate. Do not silently convert a check into an independent FP claim. TASK-005 implementation shipped at worker d70d4b9; this task repairs the missing independent gate, not a restart of B1/B2.

## Focused deliverable
After TASK-007 establishes fresh, pointer-hashed, disjoint book tune and sealed holdout passages, freeze the B1 and B2 code/thresholds and protocol using tune data only. Run each module once on the *new* held-out passages, excluding the passage's own book from B2 retrieval while excluding the four non-Hawkins slugs as Hawkins doctrine. Re-read any hit against the pristine book store, and report each detector's held-out FP numerator/denominator (including nonzero cases) and reproducible commands. Report the legacy 59 as in-sample. If any parameters change after evaluating the heldout, retire that split as test data and select a fresh unseen test; never retest on the tuned set as if independent. B1's book-derived reference table may read the reliable books as oracle, but do not use the held-out outcome to tune its rule thresholds.

## Acceptance = failed tool gate + regression safety
1. Clean-pointer offsets, SHA-256, slug exclusions, and non-overlap with the original 59 verified against frozen `corpus/docdocgo/html/merged-book-texts_json_1.js`; split/protocol and code/threshold freeze recorded before test use. No corpus file is altered or committed.
2. Independently held-out results for B1 and B2 explicitly quote numerator/denominator and any FP examples; no claim of 0 if nonzero and no reuse of evaluated set to tune. B1/B2 self-tests remain green, and existing B1 fixture CF-003/006 and B2 CF-015 hits still reproduce *independently* (as recall, not precision). Book offsets/quotes in emitted signals remain byte-exact and non-Hawkins doctrine excluded.
3. `python3 -m unittest discover -s tests` green with no test-count drop from current 78; stdlib only, no network, corpus read-only, writes limited to named fixtures/tool docs/tests. Tool precision remains UNMEASURED until a human-reviewed flagged-span sample exists. M3 certification/M5 use of B1/B2 FP estimates is withheld until this passes.

M3 also needs terminology-drift coverage and an explicit book-attribution path; those are separate future focused tasks, not silently claimed by this calibration task.

REDIRECT-007 priority addendum 2026-09-25T00:12Z — effective status BLOCKED/DEFERRED until provisional M5 TASK-011/M6 TASK-012 and TASK-007's held-out pointer split. That raw M5 census may run B1/B2 only as unreviewed CANDIDATE-class signal producers without a precision/held-out FP claim; this task is still required before M3/M5/M6 *certification*. Do not infer a reduced gate from the reordered delivery.
