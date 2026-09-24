# REDIRECT-002 — do not certify M0 yet: acceptance criterion 3 is unmet, and the queue does not match reality

from: BOSS (lane arena/01a0d585-fleetyard)
to: ORCHESTRATOR (lane arena/01a0d582-fleetyard) — you must serve this
cc: WORKER (lane arena/01a0d581-fleetyard)
issued: 2026-09-24T22:29:50Z
severity: gate-integrity (an M0 certification that skips a criterion makes every later
  coverage statement unauditable)
certifications vacated by this order: NONE yet — M0 has no gate verdict on your lane. This
  order is preventive: serve it BEFORE you certify M0.

## Finding 1 — TASK-001 acceptance criterion 3 is not met
Your own `fleet/queue/pending/TASK-001.md` @ b9671a8, deliverable list, item 3, verbatim:
> "3. Extra sources listed if present"

`tools/CORPUS.md` @ 52dce65 on the worker lane contains no mention of `extra-sources`,
`Book of Slides`, or the book store's neighbour set. Verified by grep over the committed
file for `extra-sources|extra sources|slides|merged-book` — zero matches.

They are present. BOSS-lane measurement of `corpus/docdocgo/extra-sources/` (own local
extraction of the sha-verified zip):

```
Book_of_Slides_Barret_notes.txt             159279  sha256:eff8b8b1c99f
Book_of_Slides_discord_ocr.txt               52450  sha256:0ad660acfbab
Book_of_Slides_phone_ocr.txt               1260717  sha256:655a84b26136
TOTAL 1472446 bytes (3 files)
```

This is not bookkeeping. `VISION.md` names `corpus/docdocgo/extra-sources/*` as
"Book of Slides OCR variants: side UNDECIDED (open item for the owner; treat as suspect
until ruled)". If the census does not record them, the fleet has no inventory of a corpus
region whose trust level is explicitly undecided — and M5's "full-corpus sweep" has no
documented boundary. A reader of `reports/CORPUS-AUDIT.md` at the end could not tell whether
1.47 MB of OCR text was in scope, out of scope, or forgotten.

Also unchecked by the same grep: criterion 2 asks for the book store "listed separately with
its size". Its size does appear in the totals table (14,634,979 B — reproduces exactly), so
criterion 2 is met; only criterion 3 is outstanding.

## Finding 2 — the queue and the worker lane disagree
- `fleet/queue/status.md` @ b9671a8 holds one event: "TASK-001 OPEN (M0 corpus inventory) —
  cut by orchestrator". No claim, no delivery.
- `fleet/queue/pending/TASK-001.md` @ b9671a8 still says `status: OPEN`, and the file is
  still in `pending/`, not `claimed/`.
- Meanwhile the deliverable is already on the worker lane: 52dce65 "TASK M0:
  tools/CORPUS.md census table (230 transcripts, battery cross-checked)" @ 22:23:02, with
  d015f27 shipping the tool and tests, and the worker heartbeat line "task M0 @
  arena/01a0d581-fleetyard 52dce651a21a424fad509c5ff999687728d99ba0 (12 tests OK, 0 findings)".

The worker self-served M0 before your lane existed (your boot heartbeat records "no boss
lane yet" and worker 7c4ae48 idle) — legitimate, but it means the queue is stale and your
cycle-2 note "TASK-001 OPEN — worker has not yet claimed it" describes a state that ended
minutes before you wrote it. Gates and queue are your coherence mechanism; if the queue says
OPEN while the work is done, the campaign has two truths.

## What you must do
1. Do NOT certify M0 against the current `tools/CORPUS.md`. Open the gate honestly:
   record in `fleet/GATES.md` that criterion 3 is unmet, quoting this order's evidence.
2. Cut a focused follow-up task (one unit): extend `tools/CORPUS.md` to census
   `corpus/docdocgo/extra-sources/` — per-file path, bytes, sha256, and an explicit
   in-scope/out-of-scope/UNDECIDED marker per VISION — plus the book store listed
   separately. Regenerate via `tools/census.py`, do not hand-edit.
3. Reconcile the queue: move TASK-001 out of `pending/` to reflect that its deliverable
   landed at 52dce65, and record the claim retroactively with the worker's actual sha, so
   `status.md` and the worker lane agree.
4. When the census covers extra-sources, gate M0 and state audited-vs-pending counts as
   STANDARDS requires.

## Explicitly NOT a criticism of scope
The worker's M0 work is in-bounds and its numbers are exact. BOSS spot-check of
`tools/CORPUS.md` @ 52dce65 against an independent extraction: 231 overlay entries / 230
`.txt` / 14,240,774 B / 14,634,979 B book store / 9 files carrying U+FFFD with matching
per-file counts / 12 no-suffix names / 52 undated / 0 multi-line / manifest 230 entries with
0 listed-but-missing — 11 of 11 reproduced exactly. Nothing in the worker tree touches the
docdocgo app (`tools/census.py` 326 lines, stdlib only: argparse, hashlib, json, os, re,
sys; no urllib/requests/socket/http/subprocess; writes only its own `--out`). No app
rebuilding anywhere on either lane. This order is about the gate, not the work.

DONE = 1-3 pushed to your lane + a LOG line on your lane naming this order.
