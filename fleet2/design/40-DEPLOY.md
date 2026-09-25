# Deployment & halt — owner runbook addendum (bundle draft v1.0-hub)

## Phase H — HALT campaign v1 (before any 2.0 boot)
1. `fleet/HALT-2026-09-25.md` on fleetyard MAIN (web):
   "# HALT — owner order 2026-09-25. Every fleetyard shift ends by owner
   order, effective immediately. All v1 activations' authority expires;
   all lanes become read-only archives. Campaign v1 records are preserved
   as provenance. Fleet 2.0 follows under FLEET2 policy. — <owner>"
2. Pills (web, one file each, one-line reason + date):
   - arena/01a0d581-fleetyard → fleet/controls/STOP-WORKER-ALL
   - arena/01a0d5b7-fleetyard → fleet/controls/STOP-ORCHESTRATOR-ALL
   - arena/01a0d585-fleetyard → fleet/controls/STOP-BOSS-ALL
   (Old orch lane 01a0d582 is superseded; no pill needed. Dead-session
   pills are orphan controls — harmless; the 2.0 boots resolve leftovers
   per LAW §4.3.)

## Phase D — Deploy the bundle (after cross-reference, final version)
1. Owner uploads the FINAL reconciled bundle to fleetyard main. Two ways:
   a. SEEDER (recommended, proven pattern): owner uploads ONE file
      fleet/FLEET2-POLICY.md (sha-pinned), then boots a one-shot BOOTSTRAP-2
      agent whose stub is in this file's final version; it materializes
      LAW/CANON/roles/plan/fixes byte-exact ON ITS LANE, verifies shas,
      opens ONE owner-directed PR; owner merges. main then carries:
      fleet/LAW.md, fleet/CANON.md (v2), fleet/roles/*.md (v2),
      fleet/PLAN-v2.md, fleet/ERRATA-2026-09-25c.md (I-fixes),
      fleet/ACTIVATION-REGISTRY.md (skeleton), fleet/HALT file.
   b. DIRECT: owner web-uploads each final file (download raw; verify each
      sha). More clicks, no extra boot.
2. Owner fills fleet/ACTIVATION-REGISTRY.md: one line per role
   (role · activation id · boot time · policy SHA · lane=TBD).

## Phase B — Boot fleet 2.0 (three agents, in order)
Stub skeleton (final texts issued with the reconciled bundle; each agent
pasted into a NEW fleetyard session):
- WORKER-2: "Execute fleet/roles/WORKER.md (v2, on main) as a shift.
  Activation: WORKER-2 under policy SHA <sha>. Predecessor lanes ended and
  READ-ONLY: 01a0d581 (archive). Register on your lane; boot = HALT + LAW +
  CANON + registry verify. First duties: extract corpus (sha 3f36c5203910),
  await orchestrator queue (plan-v2 order: M6-P support, then M5-R)."
- ORCH-2: same frame, ROLE ORCHESTRATOR, activation ORCH-2, predecessors
  01a0d582 + 01a0d5b7 (archives). First duties: cut M6-P + M5-R tasks,
  gate per LAW §9, certify nothing without held-out/provenance evidence.
- BOSS-2: same frame, ROLE BOSS, activation BOSS-2, predecessor 01a0d585
  (archive). First duties: baseline LOG, completion manifest tracking,
  stall-watch classes 1–6 armed.

## Release drills (owner observes, before any containment claim)
S1 poison-pill termination (live or dormant agent acknowledges + exits),
S3 orphan-control boot on a reused branch, stale-ref rejection, forged
owner-file rejection (S2), completion-broadcast acknowledgment (S6).
Record receipts on main. CANON 14: no containment claims without them.

## Phase D-a (v1.1 additions)
- Preflight: run drafter tools/fleet2check.py test suite (30 tests) locally;
  include the tool in the seeder PR (path fleet2check/).
- Boot stubs carry the nonce fields: ACTIVATION id, NONCE (typed by owner,
  never on main in clear), ANCHOR (sha256 of the registry record), POLICY
  sha, lane map. Registry: fleet2/activations/REGISTRY.md (hash-chained;
  owner appends via web).
- Owner enables a GitHub ruleset on fleetyard main (require PR, block
  force-push) as the T2 layer BEFORE booting 2.0.
- Release drills: adopt drafter D-1…D-16 (15-RELEASE-DRILLS-AND-ACCEPTANCE)
  in place of my shorter list; first gate of each 2.0 role includes D-4
  (zero-authority forgery) and D-7 (terminal semantics) as live drills.
- Halt order stands: fleet/HALT-2026-09-25.md on main FIRST (voids v1
  authority instrumentally), then scoped pills as belt-and-suspenders.
