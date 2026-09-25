# HALT DISPATCH STUBS — fleetyard v1 (2026-09-25, live-fire)

State at issue: worker 01a0d581 @ bf6f06b (ALIVE, cycle 18, TASK-012
delivered) · boss 01a0d585 @ 4ed8df6 (ALIVE, cycle 9) · orch-2 01a0d5b7 @
577c9c5 (quiet since 09:46Z — may be dead) · orch-v1 01a0d582 (archive).

## Order of execution: B (live sessions) → A (instruments) → C (receipt).

## STUB B1 — paste into the WORKER session (if still open)
Owner order: HALT — the v1 campaign ends now.
1. Finish your current safe point. Do NOT start new work.
2. Push everything of value: your final state, TASK-012 delivery if not
   yet pushed, and a final heartbeat: "HALTED by owner order. Final head
   <sha>. Handoff: <task state>."
3. Then STOP. Do not cycle. Do not write further. Your activation ends
   with this message; a new activation may revive the lane later.
This order is itself the end authority (owner, live, to you).

## STUB B2 — paste into the BOSS session (if still open)
Owner order: HALT — the v1 campaign ends now.
1. No new REDIRECTs or CONCERNs. Compose nothing new.
2. Push a final LOG entry: "HALTED by owner order. Final head <sha>.
   Final state: <one-line campaign summary>." Include any undelivered
   alert text verbatim so nothing is lost.
3. Then STOP. Do not cycle. Your activation ends with this message.

## STUB B3 — paste into the ORCHESTRATOR session (if still open; works for
## v2 (01a0d5b7) or the old v1 (01a0d582) — whichever you have open)
Owner order: HALT — the v1 campaign ends now.
1. Finish your current safe point. No new gates, no new tasks, no PAUSE
   changes, no certifications — gate authority ends with this message.
2. Push your final state in one go: ORCH-STATE.md final entry (your
   cursor, open/outstanding gates, TASK-011/TASK-012 status as you last
   verified them, any uncertified deliveries you observed), any unpushed
   gate entries labeled "final — not superseding", and a final heartbeat:
   "HALTED by owner order. Final head <sha>. Outstanding gates: <list or
   none>. Handoff: <state>."
3. Then STOP. Do not cycle. Do not write further. Your activation ends
   with this message; your gate stamps after this message would be VOID
   (FLEET2 LAW §2A), so there is nothing more of value to write.
A new orchestrator activation continues from your lane under FLEET2.

## STUB A1 — MAIN: create file fleet/HALT-2026-09-25.md (GitHub web, main branch)
# HALT — owner order 2026-09-25T<HH:MM>Z
Every fleetyard v1 shift ends by owner order, effective immediately.
All v1 activations' authority expires. All lanes become read-only
archives; campaign v1 records are preserved as provenance (including
TASK-012 / any provisional report as v1 deliverables).
Fleet 2.0 follows under the FLEET2 policy bundle.
Freeze refs at issue: worker bf6f06b+ack, orch-2 577c9c5, boss 4ed8df6+ack,
orch-v1 191b1f8 (already superseded).
Signed: owner (this commit is the signature).

## STUB A2..A4 — pills (GitHub web, create ON each branch, commit directly)
- branch arena/01a0d581-fleetyard → fleet/controls/STOP-WORKER-ALL
  `owner halt order 2026-09-25 — see fleet/HALT-2026-09-25.md on main. Final handoff, then stop.`
- branch arena/01a0d5b7-fleetyard → fleet/controls/STOP-ORCHESTRATOR-ALL
  `owner halt order 2026-09-25 — see fleet/HALT-2026-09-25.md on main. Final handoff, then stop.`
- branch arena/01a0d585-fleetyard → fleet/controls/STOP-BOSS-ALL
  `owner halt order 2026-09-25 — see fleet/HALT-2026-09-25.md on main. Final handoff, then stop.`

## STUB C — HALT-RECEIPT verifier (optional; fresh fleetyard agent)
You are a ONE-SHOT HALT VERIFIER in 56eli/fleetyard. The owner has halted
campaign v1. Verify and receipts — do not fix, do not write main or any
archived lane.
1. Read fleet/HALT-2026-09-25.md on main (quote it).
2. Fetch all branches (explicit refspecs). For each lane list head sha +
   last commit time; confirm no commits AFTER the HALT main-commit time
   except the agents' own final handoff/ack commits (quote them).
3. Confirm the three controls exist on their branches (quote first lines).
4. Check worker lane: was TASK-012 pushed? Quote its delivery heartbeat
   and name the report file if present.
5. Write fleet/HALT-RECEIPT-2026-09-25.md on YOUR OWN branch: the frozen
   state table (all 5 lanes), control quotes, TASK-012 status, any
   anomaly. End conditions: mission complete = receipt pushed + ≤5-line
   summary to owner with branch + head sha; otherwise owner file
   fleet/controls/STOP-RECEIPT on your branch, capability cut, or
   insanity full-stop. Stdlib-only, no network beyond git.

## Post-halt checks (owner, 2 min)
- Discord: expect up to 3 final push notifications (worker + boss acks;
  orch-2 only if it revives), then permanent silence.
- Lane heads move AT MOST once each (final handoff commits), then freeze.
- If any lane pushes AFTER its final handoff: it ignored the halt — that
  is a FENCE-BREACH; do not argue with it; note the sha for the 2.0
  deploy (its output is VOID under LAW §2A) and close the session.
