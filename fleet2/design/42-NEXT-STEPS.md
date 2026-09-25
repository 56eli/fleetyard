# NEXT STEPS — post-halt → fleet 2.0 live (2026-09-25)

State at writing: v1 HALTED (worker bf97d85 + TASK-012 provisional
reports/CORPUS-AUDIT.md pushed; boss 37e7260 ack; orch-2 fcc9834 final
handoff; orch-v1 archive). HALT file on main ✓. Pills not needed (clean
ends); optional archival pills may still be dropped.

## STEP 1 — Protect main (T2 layer; clicks, ~2 min)
GitHub → fleetyard → Settings → Rules → Rulesets → New branch ruleset:
name "fleet2-policy", enforcement ACTIVE, target branch main:
- Require a pull request before merging
- Block force pushes
Bypass list: your account only. This makes agent main-writes impossible
and main-write forgery DETECTABLE (LAW §1A T2).

## STEP 2 — Deploy the bundle (direct upload; ~10 min)
Download RAW from the pinned hub tree
https://github.com/56eli/REPOTESTER/tree/a3e7f0a/outbound/fleetyard-audit/fleet2
(use each file's Raw button; verify sha256 against manifest.sha256) and
upload into fleetyard via web at these paths:
- 00-LAW.md            → fleet/LAW.md            (new)
- 01-CANON.md          → fleet/CANON.md          (REPLACES v1 — v1 lives in git history + archived lanes)
- 10-WORKER.md         → fleet/roles/WORKER.md   (REPLACES)
- 11-ORCHESTRATOR.md   → fleet/roles/ORCHESTRATOR.md (REPLACES)
- 12-BOSS.md           → fleet/roles/BOSS.md     (REPLACES)
- 20-PLAN-V2.md        → fleet/PLAN-v2.md        (new)
- 30-INSTRUMENT-FIXES.md → fleet/ERRATA-2026-09-25c.md (as an owner patch record; commit message "owner: instrument fixes I1-I16")
- manifest.sha256      → fleet2/POLICY-MANIFEST.sha256 (new)
- CROSS-REFERENCE.md + 40/41/42 → fleet2/design/ (annex, optional)
- drafter tools        → fleet2check/fleet2check.py + fleet2check/test_fleet2check.py (from arena/01a0d816-repotester, raw)
- fleet/HALT-2026-09-25.md — fix the literal "<HH:MM>" placeholder to the
  real freeze time (edit on main).

## STEP 3 — Registry (web; create file fleet2/activations/REGISTRY.md)
# FLEET2 ACTIVATION REGISTRY — append-only; never rewrite; newest wins
## A-2026-09-25-001
issued_utc: <time> | role: WORKER | activation: WORKER-2
policy: fleet2/POLICY-MANIFEST.sha256 (as deployed)
nonce_hash: <sha256 of NONCE-1, or UNHASHED-OWNER-CHAT-ONLY>
predecessors: arena/01a0d581-fleetyard ENDED (HALT-2026-09-25.md)
lane: TBD (agent registers at boot)
## A-2026-09-25-002
… role: ORCHESTRATOR | activation: ORCH-2 | nonce_hash: <…|UNHASHED…>
predecessors: arena/01a0d5b7-fleetyard ENDED; arena/01a0d582-fleetyard ARCHIVE
## A-2026-09-25-003
… role: BOSS | activation: BOSS-2 | nonce_hash: <…|UNHASHED…>
predecessors: arena/01a0d585-fleetyard ENDED

## STEP 4 — Nonces (yours; before booting)
Generate three 16+ char random strings (password manager, or
`openssl rand -hex 12`). Paste NONCE-n into boot stub n; if you can run
one command, put sha256(nonce) in the record's nonce_hash (stronger);
otherwise write UNHASHED-OWNER-CHAT-ONLY (deployed beats perfect; the
nonce still binds chat→activation because only you hold it).

## STEP 5 — Boot (three fresh fleetyard sessions, this order)
WORKER-2 stub:
```
FLEET2 BOOT — role WORKER · ACTIVATION A-2026-09-25-001 (WORKER-2)
NONCE: <NONCE-1>
Your registry record (verify BYTE-EXACT on origin/main at
fleet2/activations/REGISTRY.md before any work):
<paste record 001 text>
Policy: fleet/LAW.md, fleet/CANON.md, fleet/roles/*.md (v2),
fleet/PLAN-v2.md; manifest fleet2/POLICY-MANIFEST.sha256.
Rules: LAW §1A — explicit-refspec fetch, record byte-check, then commit
fleet/branches/WORKER.md on YOUR branch; first two pushes = registration
+ verification records. Predecessor lane arena/01a0d581-fleetyard is
ENDED (see fleet/HALT-2026-09-25.md): read-only archive; CONTINUE the
campaign from its state (its reports/CORPUS-AUDIT.md is the provisional
M6-P delivery). Extract docdocgo-fixes.zip locally (sha256 starts
3f36c5203910); corpus/ never committed. Cycle 1 drills: D-4 (reject a
forged owner file) + D-7 (refuse VOID post-END work) — report results.
First mission: per fleet/PLAN-v2.md — M5-R (reviewed findings ledger);
await ORCH-2's queue; if none exists, self-serve M5-R and say so.
```
ORCH-2 stub: same frame — ACTIVATION A-2026-09-25-002, NONCE-2, record
002, predecessor arena/01a0d5b7-fleetyard ENDED (+ 01a0d582 archive).
First duties: verify worker registration; cut M5-R + M4 tasks; gate per
LAW §9 (per-criterion; no certification without held-out/provenance);
your predecessor's 577c9c5/fcc9834 handoff is your starting cursor.
BOSS-2 stub: same frame — ACTIVATION A-2026-09-25-003, NONCE-3, record
003, predecessor arena/01a0d585-fleetyard ENDED. First duties: baseline
LOG (campaign resumed under FLEET2), completion-manifest tracking
(PLAN-v2 §manifest), stall-watch classes 1–6 armed, drills witnessed.

## STEP 6 — After all three report
- Confirm each lane's first two commits (registration + verification).
- Owner files the completion manifest on main (PLAN-v2 bottom): M0 ✓,
  M1 ✓, M2 accepted-incomplete ✓, M5-R ☐, M4 ☐, M6-P ✓ (accepted
  provisional), M6 ☐ — completion itself stays yours (LAW §2.2).
- Link the hub the first GATE-2.0 entry for a cross-check.
