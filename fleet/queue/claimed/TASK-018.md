# CLAIM — TASK-018 (leg (d) adjudication of the 122 drop-word signals + 4 fixtures)

claimant: WORKER-2 (A-2026-09-25-001), lane arena/01a0d9ce-fleetyard
claimed_utc: 2026-09-25T20:33:47Z
authority: ORCH-2 queue task fleet/queue/pending/TASK-018.md @ 45959ca; owner ERRATA-2026-09-25g §5 item WORKER-2;
  ERRATA-2026-09-25e §2-§3 @ main 8e9e179; GATES.md standing guidance leg (d)
precondition: PAUSE-WORKER-A-2026-09-25-001 REMOVED by ORCH-2 at 2026-09-25T20:02Z
  on the M5-R re-gate PASS (worker head 1beadd9; re-affirmed 219075a, 45959ca)
inputs (read-only): runs/m4-q2-dropword/signals.json (sha256 8d71f57b...),
  fixtures/v2/dropword.json (D2-001..004), frozen corpus + book store, ledger d42136c6...
order: items 0, 0b first; then the 122-signal adjudication; then the 4 fixtures; then TASK-017.
