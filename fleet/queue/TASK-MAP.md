# sha-to-task map (append-only)

ORCH-2 (A-2026-09-25-002) · lane arena/01a0d9d0-fleetyard. Maps observed commit shas to
the task they belong to, so a gate can name exactly what it read (LAW §7: gates bind a
fresh run record; CANON 11: quote the sha you acted on).

## WORKER-2 lane arena/01a0d9ce-fleetyard
2026-09-25T18:26:56Z 131bd4b -> (boot) lane registration WORKER-2
2026-09-25T18:26:56Z 0e60214 -> (boot) FAIL-CLOSED verification record
2026-09-25T18:27:09Z dccd3eb -> (boot) control check 2
2026-09-25T18:36:27Z d1e6289 -> (boot) re-verification PASS at main 5fdd00e
2026-09-25T18:39:57Z 8011439 -> TASK-013 (M5-R delivery v1: 1334 findings)
2026-09-25T18:45:13Z 341ee2e -> (boot) ERRATA-25d re-ground
2026-09-25T18:46:05Z 593cad3 -> TASK-013 (errata: fixture-overlap -> span-vs-span; CF-015)
                            -> TASK-014 q1 (PATTERNS.md + held-out split)
2026-09-25T18:46:20Z bca256a -> (hygiene) .gitignore corpus/ evidence/ __pycache__/
2026-09-25T18:46:27Z aed9df6 -> TASK-013 (gated head: control check 8; no content change)

## ORCH-2 lane arena/01a0d9d0-fleetyard (own records)
2026-09-25T18:40Z 574f499 -> (boot) registration + FAIL-CLOSED heartbeat/CONTROL.log
2026-09-25T18:58Z f2da67a -> (boot) ERRATA-25d re-ground, verification record, alert closed

## Inherited (archived lanes, READ-ONLY — cited as evidence, never re-stamped)
worker v1 arena/01a0d581 @ bf97d85: 0923265/2a3eb2b -> v1 TASK-011 raw census (PASS
  provisional-raw-only by ORCH-1); 7b8863d -> census tool commit (reachable replay);
  90077b4/5bf8e42 -> v1 TASK-012 PROVISIONAL M6-P reports/CORPUS-AUDIT.md (owner-accepted)
orch v2 arena/01a0d5b7 @ fcc9834: GATES.md (v1 gate ledger) · ORCH-STATE.md (final handoff)
boss v1 arena/01a0d585 @ 37e7260: final audit of the M6-P numbers (boss audit, not a gate)
orch v1 arena/01a0d582 @ 191b1f8: ARCHIVE (cycles 41+ unauthorised; gates advisory only)
2026-09-25T18:52:41Z e07be0e -> (records) owner rulings 1-2 logged by WORKER-2; M4 q1 approved PROVISIONAL-UNGATED; no task content
