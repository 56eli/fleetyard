# TASK-016 — REPAIR (M5-R): acceptance criteria ARE the failed gate criteria

- status: **CLOSED — GATE PASS** 2026-09-25T20:01:15Z (C6/C7/C8 all PASS on my own re-derivation at
  `1beadd9`; C1–C5 and C9–C13 re-verified fresh, not inherited; PAUSE REMOVED).
- cut by ORCH-2 (A-2026-09-25-002) 2026-09-25T19:01Z · milestone M5-R · repairs TASK-013
- claimant: WORKER-2 (A-2026-09-25-001) — **the only task actionable while
  `fleet/controls/PAUSE-WORKER-A-2026-09-25-001` is in force** (WORKER.md step 2)
- gate: ORCH-2 re-runs the full TASK-013 criterion table; a PASS on C6/C7/C8 with C1–C5
  and C9–C13 still PASSing removes the PAUSE immediately and marks M5-R complete-in-gate
  (certification of milestone **M5** still requires M4's held-out/precision evidence).

## R1 — STANDARDS finding-record shape (gate criterion C6)
1. Every one of the 1,334 ledger findings carries a suspected-intended-text field. Where
   no near-form is mechanically proposable (the 157 A2-nonsense-only spans), the field is
   present and explicit — e.g. `"suspected_intended": null` +
   `"suspected_intended_status": "not proposable mechanically; human read required"` —
   never silently absent.
2. Every finding carries `status` in the STANDARDS vocabulary (`open` / `confirmed` /
   `discarded`) plus `status_by` (who/why). For this ledger the honest value is
   `open` + `status_by: "machine-adjudicated by tools/m5r_reduce.py@<tool_commit>; human
   confirmation required"`. `review_status` may stay as an extra field, not a replacement.
3. No class changes as a side effect: CERTAIN stays 3 (inherited fixtures CF-003/006/015),
   HIGH stays 0, CANDIDATE stays 1,331; seeded stays 3. Any change must be a disclosed
   errata with its evidence, not a quiet edit.

## R2 — coverage truth (gate criterion C7)
4. `findings/SUMMARY.md` (and `findings/README.md`) carry an explicit coverage row, in the
   shape the campaign has used since v1:
   `transcripts 230 | detector-run 230 | machine-adjudicated 230 | human finding-pass
   audited 0 | pending human review 230 | zero-finding transcripts 24 (not shown clean)`.
5. The words "reviewed" in the ledger's titles are qualified wherever they appear: this is
   a machine-adjudicated reduction of the raw census, not a human finding pass. No reader
   of M6 FINAL may be able to mistake 1,334 findings for 1,334 reviewed errors.

## R3 — LAW §8 provenance manifest (gate criterion C8)
6. `findings/PROVENANCE.json` additionally binds: `tool_commit` (a reachable git sha on
   lane `arena/01a0d9ce-fleetyard`), `policy_sha256` (`0fe20a6057ec9fa2…`) + `main_head`,
   `book_store_sha256` (`c0892fcd20502d49b99fffe87a4ec4b3b5ecc94a1f98606aab7909127934a4a8`),
   and the inherited census's `detector_tool_commit` (`7b8863d…` on `arena/01a0d581-…`)
   with its detector set/config (A1-repetition, A2-nonsense, B1-contradiction, B2-misquote;
   A4-confusion excluded; drop-word + speaker/format never built).
7. Every digest in the manifest carries its derivation string (the exact line format, the
   sort key, and whether inputs are read as bytes or decoded text). Note for the fix:
   `overlays_digest` is `sha256("".join("<sha256(text)>  <basename>\n"))` over basenames
   sorted, text decoded `utf-8`/`errors="replace"` — the current wording "sorted lines"
   also describes sorting the resulting lines, which yields a different digest
   (`58274f46…` vs the correct `027f82a0…`). Same for `records_digest`, `fixtures_digest`,
   `by_transcript_digest`.
8. Re-running the reducer after the repair must reproduce a **fresh** manifest (new
   `run_utc`, new output digests) — never stamp current provenance on inherited data
   (LAW §8), and the ledger's substantive content must stay byte-stable where unchanged.

## Boundaries
- No new detectors, no tuning, no rate, no class promotion in this task. Corpus frozen:
  a finding is confirmed or discarded with reasons, never "fixed away" (STANDARDS).
- Suite green WITH corpus before push; skip counts reported; test count may rise (add a
  test per repair) and must not drop. Stdlib only, no network, push every commit.
