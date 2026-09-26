# TASK-015 — M6 FINAL report (BLOCKED)

**STATUS UPDATE (ORCH-2 2026-09-26T09:55:22Z, gate cycle L at WORKER-2 `f5e2cf5`) — supersedes the BLOCKED line below, which stays readable.**
All three of this task's named preconditions are now **satisfied**: TASK-016/TASK-013 M5-R **PASS** (re-gated again at
`f5e2cf5` — the reducer with published pins reproduces ledger `d42136c6…` and by-transcript `c1ec4da8…` byte-identically,
`tools/m5r_reduce.py` the same blob `6346049b…` at both heads), TASK-014 q4 **PASS**, TASK-017 **PASS**. The instrument's
quantum-b precondition row also PASSes with **n=0 open preconditions**, and the v2.16 precedent row PASSes (n=521).
**But M6 FINAL is NOT gateable and nothing is certified:** the quantum-b run **has not happened** — no receipt declares the
V2 holdout spent (row PASS, n=268) — and LAW §9 allows no rate without held-out evidence. Status is therefore
**PENDING QUANTUM B**, not BLOCKED and not PASS. An uplifted blocker is not a certification. The firing decision is the
owner's and is written up at `fleet/ORDERS/DECISION-REQUEST-QUANTUM-B-2026-09-26.md`: quantum b is **one-shot** (v2.7:
frozen thresholds, single run, consumed receipt, no re-run), so whether it fires before or after the remaining v2.e/v2.f and
item-12/13b repairs is a sequencing choice with an irreversible cost. M6-P stays owner-accepted PROVISIONAL and is never
re-certified here.

- status (ORCH-2 2026-09-25T20:02:49Z): still **BLOCKED**. M5-R is no longer the blocker (re-gate PASS
  @ `1beadd9`, ledger `d42136c6…` is the verified input). Remaining blockers: (1) M4
  q1-q5 gates; (2) **held-out precision evidence** — the one-shot holdout was spent
  19:12-19:14Z (counts only, no rate), so any headline rate needs a fresh sealed split
  (new salt, fixed before any further tuning) evaluated once; (3) TASK-017 toolchain
  inheritance with a LAW §8 manifest; (4) leg-(d) adjudication (TASK-018) for any
  CERTAIN count that M6 FINAL quotes. No rate without (2). M6-P stays owner-accepted
  PROVISIONAL and is never re-certified by me.
- milestone: **M6** (fleet/PLAN-v2.md) · cut by ORCH-2 (A-2026-09-25-002) 2026-09-25T19:01Z
- status: **BLOCKED** — not claimable until: TASK-016 PASS (M5-R complete-in-gate),
  TASK-014 q4 PASS (B1/B2 held-out validation + per-detector precision), TASK-017 PASS
  (toolchain on the working lane). LAW §9: precision/recall claims require held-out data
  fixed before tuning; no certification without held-out/precision evidence.
- explicitly out of scope: re-certifying the PROVISIONAL M6-P report
  (`reports/CORPUS-AUDIT.md` @ `90077b4`, worker lane `bf97d85`) — it is owner-accepted as
  a v1 deliverable (HALT on main; boot stub duty 4). M6 FINAL supersedes it with reviewed
  numbers; it is never "re-gated" and never called M6-P's certification.

## Deliverable (PLAN-v2 M6)
Reviewed error rates **per class** (CERTAIN and HIGH separate; CANDIDATE reported
separately, never blended), by year, by detector family, transcript hotspots; pattern
summary from `tools/PATTERNS.md`; recommendations. This is the owner's "how bad is it"
answer — and it must state its denominator (words/transcripts actually human-read) next to
every rate, with the unmeasured classes named (A4, drop-word, speaker/format until shipped).

## Acceptance criteria (gate criteria)
1. Every rate carries: numerator, denominator, class, and whether the denominator is
   hand-read transcripts or holdout transcripts. No rate without a stated denominator
   (PLAN-v2: "state component status, never percentages without a denominator").
2. CERTAIN counts only findings with a STANDARDS hard leg (a/b/c) — the CF-009 precedent
   stands: grammar alone is not CERTAIN. HIGH counts only findings with ≥2 independent
   signals **and** a written independence rationale. CANDIDATE appears in its own section.
3. Seeded/in-sample hits excluded from every rate and listed separately (LAW §9).
4. Held-out figures come from the q1 split (37 transcripts), fixed before tuning; the split
   seal must be unchanged between q1 and the report (digest re-verified at gate time).
5. Every quoted citation re-readable byte-exact at its offset (ORCH-2 re-verifies a sample
   independently, as for TASK-013: 1334/1334 spans + 242/242 book bytes this cycle).
6. LAW §8 manifest for the report run: renderer tool commit + digest, ledger digest it
   consumes, corpus/book-store digests, policy sha, output digest, run utc.
7. Coverage truth row: audited vs pending vs machine-adjudicated, zero-finding transcripts
   not clean, unmeasured classes named.
8. Labelled DELIVERY (LAW §2.1). Completion is the owner's declaration against the
   completion manifest on main — never the report's own claim.
