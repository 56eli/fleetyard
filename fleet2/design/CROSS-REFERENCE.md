# CROSS-REFERENCE — hub bundle (fleet2/) × independent drafter (fleet2-draft/)

2026-09-25 · hub: `outbound/fleetyard-audit/fleet2/` @ 18efae5 · drafter:
`arena/01a0d816-repotester` @ 9c65302 (16 files + fleet2check.py, 30 tests).
Rule 0 held: drafter's README discloses non-read of fleet2/; its branch adds
only fleet2-draft/ (verified by tree diff). Verdicts below are the hub's,
post-verification.

## 1. Its falsifiable predictions about my draft (SUMMARY §11): 0/7
1 "pills without incarnation scope" — mine HAD scoped pills + -ALL + orphan
  resolution (LAW §4.3). 2 "signatures as identity" — mine proposed none.
  3 "cap-equivalent smuggled back" — none. 4 "fourth watcher" — explicitly
  rejected by mine. 5 "role-declared completion" — mine: owner-only on main
  against a manifest. 6 "identical suite lines ⇒ stamp" — mine reformed this
  (LAW §7). 7 "seeded hits near precision" — mine forbids (LAW §9).
Score 0/7 — but see §2: it still found a real hole my predictions-dodging
didn't cover.

## 2. Where ITS design wins — ADOPTED into v1.1-final
A1 **T2 honesty (biggest one).** My activation registry sits on main and
   assumes "owner writes main." False under the shared credential: Arena
   agent pushes carry the owner's identity, so main's CONTENTS alone cannot
   prove owner authorship. Drafter's fix: out-of-band **owner-chat nonce**
   (single-use) + **ANCHOR hash** binding boot stub → registry record →
   policy SHA; **hash-chained** registry (rewrite alarms); T0–T3 threat
   table with the honest claim (file forgery impossible, replay impossible,
   main-write forgery NON-GRANTING and detectable, owner-account compromise
   = residual risk); owner adds a GitHub ruleset on main as the T2 layer.
   ADOPTED wholesale (LAW §1A).
A2 **Authority tiers D/G/S** — Direction (chat, in-scope, recorded) /
   Grant (nonce'd registry record; fail-hard) / Restriction (any plausible
   form halts; fail-safe). Cleaner and safer than my prose §1.4. ADOPTED
   (LAW §1B).
A3 **Work quanta ≤240 s + CONTROL.log.** My "control check ≤300 s at safe
   points" was unenforceable prose; theirs bounds each work unit, requires
   a CONTROL.log append per check (append-only) + generated CONTROL.md,
   and makes a 2× quantum overrun a STRIKE. This is what makes stop-latency
   promises true (S1's lesson). ADOPTED (LAW §4A).
A4 **VOID doctrine + consumer-side fencing.** Post-HANDOFF/post-END output
   is VOID — not "pending owner"; any lane may reject (FENCE-BREACH) and
   the orchestrator MUST gate-reject it; deleting END.md is itself alarmed.
   This fixes the exact day-1 hole (a shift that ignored its own declared
   handoff for 44 cycles). ADOPTED (LAW §2A + CANON 18–19).

## 3. Where MINE stands — KEPT
K1 Compact deployable file set (8 files) vs 16 — final bundle stays lean;
   drafter's per-part files serve as rationale annexes (linked, not
   merged). K2 Seeder-PR deployment (battle-tested letter→PR pattern) as
   deploy option A. K3 PLAN v2 (M5-R/M4/M6-P/M6 naming continuity + owner
   completion manifest) — equivalent to drafter's sequencing. K4 I1–I16
   patch lines (merge with drafter's 13 at deploy — same targets).
K5 My halt skeletons (main-first HALT, then scoped pills).

## 4. Straight convergence (both drafts, independently)
Owner-declared completion against a manifest · HANDOFF irrevocable ·
control loop separate from cadence, fail-closed on fetch failure · dormancy
honest (≠ termination) · loud-zombie class with acknowledgment deadline ·
all-roles insanity + context-rot cross-sampling · no fourth watcher ·
non-suppressible escalation past the boss · event-log reducer ·
stamp-detection reform · seeded≠independent · held-out seals · cache
provenance manifests · zero agent webhook custody · push-every-commit.

## 5.drafter extras worth shipping as-is
fleet2check.py + tests (registry/void/reducer validator — deploy preflight
and fleet-side verification tool); D-1…D-16 release-drill index with
locked/procedural markers; boss cross-check matrix (mechanical, anyone can
run it); deploy rollback section; first-hour watch list.

## 6. Final bundle (v1.1-final)
fleet2/00-LAW.md (amended in place, §1A/§1B/§2A/§4A + header bump) ·
01-CANON.md (18–19 appended) · 10/11/12 role files (untouched — their §9
shift-day + references already match the amendments) · 20-PLAN-V2.md ·
30-INSTRUMENT-FIXES.md (deploy-merge with drafter 13) · 40-DEPLOY.md
(amended: nonce boot-stub fields, fleet2check preflight, D-1…D-16 drills)
· manifest.sha256. Drafter's fleet2-draft/ ships as the design annex.
