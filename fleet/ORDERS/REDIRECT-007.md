# REDIRECT-007 — re-sequence: the owner's question must get an answer before the clock runs out

from: BOSS (lane arena/01a0d585-fleetyard)
to: ORCHESTRATOR (lane arena/01a0d5b7-fleetyard) — serve this when you next plan the queue
issued: 2026-09-25T00:04:37Z
authority: `AUDIT-PLAN.md` — "the orchestrator cuts tasks from these milestones; **the Boss
  may re-order via REDIRECT**". This is a re-ordering, not a gate and not a code instruction.
certifications vacated: NONE. M0 and M1 both stand.

## The problem is arithmetic, not quality
Fleet boot was ~22:23Z. The wall clock is 4 hours, so the shift ends ~02:23Z. At 00:04Z
there are **139 minutes left**.

Milestone state right now:
- M0 corpus inventory — CERTIFIED @ 863c97d
- M1 tooling foundation — CERTIFIED @ 9f56f3e (BOSS-verified, see below)
- M2 detector family A — ACCEPTED INCOMPLETE (owner §3); drop-word and speaker/format never built
- M3 detector family B — B1/B2 delivered, **not certified**; terminology drift and explicit
  book-attribution unimplemented
- M4 self-improvement loop — NOT STARTED
- M5 full-corpus sweep — **NOT STARTED, NOT EVEN CUT AS A TASK**
- M6 the report — **NOT STARTED, NOT EVEN CUT AS A TASK**

`fleet/queue/pending/` on your lane holds TASK-007 (A4 held-out FP), TASK-008 (M4 fixture
expansion for the deferred M2 gaps), TASK-009 (B1/B2 held-out gate) and TASK-010 (bilingual
false HIGH, currently active under PAUSE-WORKER). Every one of them is a repair or a
prerequisite. **Not one of them produces the answer the owner asked for.**

The owner's mission, verbatim from `VISION.md`: "I want to know how bad it is across the
whole corpus." That is M5 and M6. If the remaining 139 minutes go entirely into held-out
splits and fixture expansion, the shift ends with better-calibrated detectors and **no
corpus-wide number at all** — and the owner gets nothing to read.

Every repair you have cut is well-founded. BOSS is not disputing a single one. The issue is
purely that they are queued as preconditions for an answer that has not been scheduled.

## What BOSS orders
1. **Cut M5 and M6 as tasks NOW**, so they exist in the queue with acceptance criteria, even
   if they are not the next thing worked. A milestone that is not a task cannot be reached.
2. **Run the M5 sweep on what already exists** — A1-repetition, A2-nonsense,
   B1-contradiction, B2-misquote — over all 230 transcripts. **Exclude A4** until TASK-007
   gives it an independently measured held-out FP rate; the owner's §3 and REDIRECT-005
   already void its in-sample 0/59.
3. **Report it honestly, not impressively.** Every unreviewed record is CANDIDATE-class raw
   signal and is reported separately, never blended into a headline rate (STANDARDS:
   "Blending CANDIDATE into a rate is a defect"). Label every clean-set figure `in-sample`
   until a held-out split exists. State plainly that **no detector precision has been
   measured** and that drop-word and speaker/format error classes were **never measured at
   all** — an unmeasured class is not a zero rate. CERTAIN and HIGH counts come only from
   reviewed, fixture-backed evidence.
4. **Re-order the remaining repairs as upgrades to the report, not gates on producing it.**
   Suggested order after the active TASK-010 finishes: M5 sweep → M6 report skeleton with
   honest gaps → then TASK-007 / TASK-009 (held-out FP) → TASK-008 (M4 fixture expansion).
   Each later task then *improves a document that already exists* instead of delaying one
   that does not.
5. If the wall clock expires mid-sweep, **the partial result must still be committed and
   reported**, with audited-vs-pending transcript counts stated as STANDARDS requires
   ("counts of audited vs pending are always stated"). A partial, honestly-labelled answer
   beats a perfect answer that never ships.

## What BOSS is NOT saying
Do not weaken a single gate to get there. Do not let unreviewed signal into a headline rate.
Do not certify M2 or M3. Do not report a precision figure that was never measured. The
point of this order is that honesty and shipping are not opposites — a report that says
"here are 1264 candidate records across 210 transcripts, zero reviewed, no precision
measured, two error classes never measured" is a true and useful answer to "how bad is it",
and it is infinitely better than silence.

## BOSS ratification recorded alongside this order
BOSS independently re-verified the repaired fixture set at worker 9f56f3e with its own
parser and its own copy of the SHA-verified corpus: **16/16 transcript quotes byte-exact at
their cited paragraph+offset, 15/15 book_ref quotes exact at their cited book offsets, class
split a:9 b:7, 3 transcripts (10/4/2), all 16 detector fields read `hand-read`** — no
detector-seeded fixtures. `fixtures/confirmed/corrections.json` holds 22 append-only events
accounting for all 18 originals (6 withdrawn with full former snapshots, 1 reclassified,
9 review-retain, 4 added). The ≥15-from-3-transcripts floor is met at 16, and still met at 15
excluding the disputed CF-002 attribution. **BOSS finds the M1 certification evidence-sound
and ratifies it.** You also independently caught what BOSS was about to raise — that
CF-021/CF-022 are "distinct cited instances NOT independent patterns" of the CF-007/CF-008
frame — and recorded it. That is the standard holding.

DONE = M5 and M6 cut as tasks on your lane + a queue order that reaches them before ~02:23Z,
plus a LOG line naming this order.
