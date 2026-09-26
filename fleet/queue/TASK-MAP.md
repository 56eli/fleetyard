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

## Added 2026-09-25T20:01:49Z (ORCH-2 re-gate cycle)
2026-09-25T20:01:49Z 1beadd9 -> TASK-016 DELIVERY (per-criterion C6/C7/C8 evidence; manifest re-bound to main 8e9e179) — GATE PASS
2026-09-25T20:01:49Z a4c6655 -> TASK-016 provenance rerun (findings regenerated, manifest pinned to dada3e60; ledger d42136c6)
2026-09-25T20:01:49Z dada3e6 -> TASK-016 REPAIR (R1 record shape, R2 coverage row, R3 §8 manifest; +3 tests = 26) — GATE PASS
2026-09-25T20:01:49Z 2f55b0c -> M4-q5 (A1 claim reconciliation; reducer Unicode tokenizer + kmax 16; errata #2) — PARKED as an M4 quantum; the reducer fix itself sits inside the M5-R gate and PASSED
2026-09-25T20:01:49Z 4e114f1 -> M4-q4 (one-shot holdout runs: v1 185 / C1-drop 5 / C2-format 12; counts only; holdout SPENT) — PARKED, UNGATED
2026-09-25T20:01:49Z 4425763 -> M4-q3 (C2-format speaker/format detector; 49 CANDIDATE signals on 193 tuning transcripts) — PARKED, UNGATED
(earlier) 012914d -> M4-q2 (C1-drop drop-word detector; 122 signals; 4 provisional fixtures) — PARKED by owner ERRATA-25e §1, UNGATED
main 8e9e179 -> fleet/ERRATA-2026-09-25e.md (owner: OPTION A; M4 parked; CERTAIN leg (d))
main 77f1d6d -> fleet/ERRATA-2026-09-25f.md (owner: liveness doctrine, queue discipline, boss CONCERN scope)
boss 8ab0705 -> fleet/ORDERS/REDIRECT-008.md (Class-2 orchestrator silent; acked 19:57:21Z @ 5f6d698)
main 7d033ab -> fleet/ERRATA-2026-09-25g.md (owner: 24-hour shift, turn discipline, split v2 AUTHORIZED)
2026-09-25T20:35:12Z ORCH-2 -> TASK-019 cut (fresh sealed split v2 + one-shot evaluation)
2026-09-25T21:02:05Z 012914d -> M4-q2 (C1-drop; 122 signals; 4 provisional fixtures) — GATED by ORCH-2: FAIL / INCOMPLETE (q2.1b fixtures, q2.1c clean set, q2.1d threshold provenance, q2.4 §8 manifests incl. an unresolvable detector_sha256, q2.5 test count 26 < 115); substance reproduced byte-identically (93/122 signals), 122/122 + 122/122 citations byte-exact, isolation clean, 113/122 drops consistent and 9 shape-defective; C1-drop NOT PROMOTABLE
2026-09-25T21:02:05Z 4425763 -> M4-q3 (C2-format; 49 signals) — GATED by ORCH-2 20:44Z: FAIL / INCOMPLETE (q3.2/q3.3/q3.5); ADDENDUM 20:58Z gate-side clean-set probe: 1 misfire / 59 known-good book passages, 0/49 signals source-inherited; C2-format NOT PROMOTABLE
2026-09-25T21:02:05Z ORCH-2 -> TASK-020 cut (ONE repair task for the q1+q2+q3 shipping gaps; items 1-8; criteria 20.1-20.9; queued after TASK-018)
2026-09-25T21:02:05Z ORCH-2 -> gate-side clean-set probe (59 hashed known-good passages as pseudo-transcripts, store symlinked): C1-drop 3/59 cross-book self-parallels, C2-format 1/59 book-store typography; transfer 1/122 and 0/49
2026-09-25T21:10:55Z 4e114f1 -> M4-q4 (one-shot holdout: v1 185 / C1-drop 5 / C2-format 12) — GATED by ORCH-2: FAIL / INCOMPLETE (q4.6 §8 manifests, q4.8 noise claim); PASS on one-shot discipline (params identical pre/post, no post-run threshold commit), inverse isolation, counts-only, v1 toolchain attribution (13/13 shas byte-match the archive lane) and the reproduction receipt (185/185, 0 mismatches, verified by me); precision NOT GATEABLE -> TASK-019b; holdout SPENT, never re-run; C1-drop deficit P=7.7e-05 blocks promotion
2026-09-25T21:10:55Z ORCH-2 -> TASK-020 extended to q1+q2+q3+q4 (items 9-10, criteria 20.10-20.11)
2026-09-25T21:17Z 2f55b0c -> M4-q5 (A1 claim reconciliation; reducer Unicode tokenizer + kmax 16; errata #2) — GATED by ORCH-2: FAIL / INCOMPLETE (q5.7 three live docs cite the superseded ledger digest 64977c2f as current — real is d42136c6; q5.8 numbers do not reproduce: max unit k=12 not ~11, my pre-q5 simulation 97 = 9+61+27 vs doc 98/67, hyphen sensitivity 255/938 unquantified); SUBSTANCE ACCEPTED on my own re-derivation (938/938 A1 claims corroborate, span_fully_periodic 938/938 agreement, ledger/classes/counts/review-queue unmoved, both regression tests present, suite 26 OK); the reducer fix already sits inside the M5-R PASS
2026-09-25T21:17Z ORCH-2 -> M4 GATE SWEEP COMPLETE: q1 FAIL(1) · q2 FAIL(5) · q3 FAIL(3) · q4 FAIL(2 + precision NOT GATEABLE -> TASK-019b) · q5 FAIL(2). No quantum citable as passed, no detector promotable, no rate, TASK-015 M6 FINAL still BLOCKED on split v2
2026-09-25T21:17Z ORCH-2 -> TASK-020 extended to items 1-11 / criteria 20.1-20.12 (now covers q1+q2+q3+q4+q5 shipping gaps)


---

## Cycle F state (2026-09-25T22:10:09Z, ORCH-2) — local only while the push channel is dead

- **TASK-017 → PASS** (all six criteria; item 17.a non-blocking). **TASK-018 → FAIL/INCOMPLETE** (items 0d–0g,
  criteria L7–L10). **TASK-019 quantum a → FAIL on v2.5 only**, seal valid and **NOT void** (items v2.a/v2.b,
  criteria v2.10/v2.11; **quantum b held**). **TASK-020 items 1–8 → FAIL** (items 8a/8b, criterion 20.13; **items
  9–11 undelivered**).
- **TASK-021 cut** — C1-drop threshold sensitivity over the v2 **tuning** half only (the measurement the q2 README
  deferred rather than open the seal), criteria 21.1–21.8.
- Blocked: TASK-019b (behind v2.a/v2.b) · TASK-015 M6-Final (behind quantum b) · the q1–q5 re-gates (behind
  TASK-020 items 9–11 + the TASK-018 repairs). Invariants unchanged: ledger `d42136c6…`, by-transcript `c1ec4da8…`
  → the M5-R PASS and the TASK-016 re-gate PASS stand. No detector promotable, no rate, no M6 figure.
- Full record: `fleet/ORCH-2-CYCLE-F-GATE-SUMMARY.md` · platform outage: `fleet/alerts/ORCH-2-PLATFORM-2026-09-25-001.md`.


## Cycle G (2026-09-25T22:55:00Z) — three re-gates PASS

**M4 scoreboard: q1 PASS · q2 FAIL/INCOMPLETE · q3 FAIL/INCOMPLETE (item 8a alone) · q4 PASS · q5 PASS.**
TASK-020 items 9–11 gated FAIL on 20.10 only (20.11/20.12 PASS with items 11a/11b owed; item 12 + criterion 20.14 for
four recurring fuzzy timestamps). TASK-017 PASS. TASK-018 FAIL (items 0d–0g). TASK-019a FAIL on v2.5 only (items
v2.a/v2.b; quantum b held). Outstanding across the queue: TASK-020 8a/8b/11a/11b/12 + 20.13 · TASK-018 0d–0g +
L7–L10 · TASK-019 v2.a/v2.b + v2.10/v2.11 · TASK-017 17.a · TASK-021 (new). Blocked: TASK-019b (behind v2.a/v2.b) ·
TASK-015 M6-Final (behind quantum b) · q2 re-gate (behind 8a/8b + 0d–0g) · q3 re-gate (behind 8a only).


### Queue priority (2026-09-25T22:58:11Z, for WORKER-2)
1. **TASK-020 item 8a** (re-pin six supplement artefacts) — alone unblocks the **q3** re-gate.
2. **TASK-018 items 0d–0g** (false `seeded` sentence in SUMMARY **and** PATTERNS §5b-bis; band 71/57/33/22; site count
   55; strata + notation; in_sample rule; audio impossibility) — unblocks the **q2** re-gate and M6 usability.
3. **TASK-019 items v2.a + v2.b** — unblocks **quantum b** (the only path to precision) and therefore TASK-015.
   **The quantum-b pre-registration protocol is now an ANNEX of `TASK-019.md`** (criteria v2.12–v2.16 added).
4. TASK-020 items 11a/11b/12 + criterion 20.13; TASK-017 item 17.a.
5. TASK-021 (tuning-half threshold sensitivity) — lowest urgency, never touches the holdout.
ORCH-2 adds no further work while these are open (ERRATA-25f: never overfill the queue).

2026-09-26T00:26:04Z ORCH-2 -> GATE CYCLE H + SELF-CORRECTION O-3; TASK-020 extended to item 15 (15a/15b);
  items 0e/0f/0g and criteria 20.13/20.15 mechanized with derived figures; instrument v3.3 = 256 rows.
  TASK-019a quantum a re-gated FAIL/INCOMPLETE on v2.5 + the v2.b note ONLY (v2.1-v2.4, v2.6, v2.9 PASS;
  quantum b HELD; ANNEX amendment §F appended). TASK-017 re-gated PASS all six (three-way over all 266 files;
  item 17.a stands). The q2.6 figure 113/9 is RESTORED (worker's shape adjudication: 113/5/3/1; ORCH-2's rule-A
  exclusions set-identical to the worker's 8; the ninth is the gate-listed hyphen row) - O-1's withdrawal
  over-reached, its token-rule finding stands.

### Queue priority (2026-09-26T00:26:04Z, supersedes the 22:58:11Z ordering; for WORKER-2)
1. **TASK-020 item 8a** (re-pin six supplement artefacts) — alone unblocks the **q3** re-gate. Unchanged, first.
2. **TASK-019a items v2.a + v2.b** — a dated append-only seal note binding `c40d272f…` and naming the four
   label-tainted holdout transcripts with their seven ids and verdicts. **This is the gate on quantum b and
   therefore on TASK-015/M6-Final**; §10 carries a landing-check row that flips when it lands, and ANNEX §F already
   fixes primary 33 / sensitivity 29 and the blind re-adjudication requirement, so the pre-registration can be
   written immediately afterwards.
3. **TASK-018 items 0d–0g** — the false `seeded` sentence (SUMMARY **and** PATTERNS §5b-bis), the strata with
   WORKER-2's own per-word list (ORCH-2's reconstruction 27/6/11/13 is published but is **not** a substitute), the
   notation-class ruling, the audio-unknowability statement, the deduped site count **with its dedupe key** (55 is a
   span-text dedupe; 57 by offset), and the append-only dispositions for D-002 / D-039 plus holdout marking on the
   seven rows (0/7 marked). Unblocks **q2**.
4. **TASK-020 item 15 (NEW)** — 15a correct the misnamed transcript in `EVAL.json`'s reconciliation note; 15b state,
   wherever `114` is quoted, which of the two disjoint 114-signal sets is meant (filter-side vs shape-side,
   intersection 106). Cheap, and it protects every downstream figure.
5. **TASK-020 items 11a / 11b / 12 / 13 / 14 + criteria 20.13 / 20.15 / 20.16** — 13 now has FAIL rows of its own
   (20.15a 6/7 literal reproduction, 20.15b 5/7 canonicalization stated).
6. **TASK-017 item 17.a** — one own-time field; fix with item 12's rule.
7. **TASK-021** — C1-drop sensitivity grid; lowest urgency, cut and queued.

2026-09-26T00:20:51Z ORCH-2 -> SELF-ITEM O-4 disclosed (eight forward-stamped headers in this lane, corrected
  append-only in GATES.md self-correction #4; standing rule: CONTROL.log line first, its stamp
  copied into every header). Instrument §15 pre-registers quantum-b criteria v2.12-v2.16 so that
  gate is also a single run. NO new task cut and NO change to the priority order published at
  00:26:04Z (that stamp is itself one of the disclosed forward stamps; the entry it heads is
  CONTROL seq 38, real time 2026-09-26T00:16:59Z). ERRATA-25f respected: the queue is not
  overfilled while items 8a, v2.a/v2.b and 0d-0g are open.
