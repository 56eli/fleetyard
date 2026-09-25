# TASK-015 — M6 FINAL report (BLOCKED)

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
