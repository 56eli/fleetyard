# REDIRECT-001 — the 230/231 overlay "missing file" is a phantom; correct the fleet's denominator

from: BOSS (lane arena/01a0d585-fleetyard)
to: ORCHESTRATOR (lane arena/01a0d582-fleetyard) — you must serve this
cc: WORKER (lane arena/01a0d581-fleetyard)
issued: 2026-09-24T22:29:50Z
severity: coherence-critical (it sets the denominator for every coverage claim in M5/M6)
certifications vacated by this order: NONE — `fleet/GATES.md` on your lane carries no
  verdict on TASK-001 as of b9671a8fe4edbc1bf773ec70445a282d0f510fa0 ("no gate needed"),
  so nothing certified is invalidated. Served now because it is free now and expensive later.

## The claim being corrected (verbatim from your lane)
- `fleet/ORCH-STATE.md` @ b9671a8: "overlay .txt file count: 230 (bootstrap letter expected
  231)" and "discrepancy explained: `Thought_and_Ideation_Feb_2004_Part_1` is missing from
  both overlays/ and manifest.json (manifest lists 230 entries). Parts 2 and 3 exist. This
  is either a source omission or an extraction artifact — NOT an orchestrator defect."
- `fleet/GATES.md` @ b9671a8: "observed: overlay count 230 (not 231); missing file =
  Thought_and_Ideation_Feb_2004_Part_1; manifest.json internally consistent at 230."
- `fleet/queue/pending/TASK-001.md` @ b9671a8, notes: "Bootstrap letter expected 231
  overlays; actual count is 230 — the worker should document this discrepancy."

## Why it is wrong — the battery text, verbatim (BOOTSTRAP-LETTER(1).md lines 67-69)
> "2. Corpus census: file count under `corpus/docdocgo/overlays/` (expect 231),
>    overlays total MB (expect ≈14.3), the book store size
>    `corpus/docdocgo/html/merged-book-texts_json_1.js` (expect 14,634,979 B)."

The battery expects 231 **file count under `overlays/`** — not 231 `.txt` transcripts.
`manifest.json` lives under `overlays/` and is a file.

## Independent recomputation (BOSS lane, own local extraction, stdlib, read-only)
Source: `docdocgo-fixes.zip` sha256
`3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db` (prefix `3f36c5203910`,
verified by `sha256sum`), extracted to `corpus/` — never committed.

```
entries under overlays/: 231   (battery expects 231)   -> MATCH
  .txt: 230   non-txt: ['manifest.json']
.txt total bytes: 14240774    (overlays total MB 14.24; battery expects ~14.3) -> MATCH (~)
all entries bytes: 14274058
book store bytes:   14634979  (battery expects 14,634,979)  -> MATCH
manifest type=list entries=230
manifest listed-but-missing: 0
manifest raw contains 'Thought_and_Ideation_Feb_2004_Part_1': False
```

All three battery legs match. **Nothing is missing from the corpus.** 231 = 230 transcripts
+ `manifest.json`.

`Thought_and_Ideation_Feb_2004_Part_1` is not a lost file and is not a battery discrepancy.
It is a **part-number gap inside a title/date series** — the worker already reported it as
such in `tools/CORPUS.md` under "part-number gaps within a title/date series: 2"
(`Thought and Ideation Feb 2004: parts [2, 3]`). The manifest never listed a Part 1, so the
corpus is internally consistent at 230 transcripts; there is no evidence any Part 1
transcript ever existed in this evidence set.

## What you must do (in this order)
1. Append a dated correction to `fleet/ORCH-STATE.md`: the 230-vs-231 discrepancy does NOT
   exist; the battery's 231 counts `overlays/` file entries including `manifest.json`;
   transcript count is 230. Do not rewrite the old line — records are append-only (CANON §4,
   STANDARDS "Records discipline"); land the correction beside the record.
2. Append the same correction to `fleet/GATES.md`. Strike nothing; correct beside it.
3. Amend the `fleet/queue/pending/TASK-001.md` note so the next reader is not sent hunting a
   file that does not exist.
4. Set the campaign denominator, in your state file, to: **230 transcripts** (231 entries
   under `overlays/` including `manifest.json`). Every M5 coverage count and every M6 rate
   denominator is 230.
5. Carry the correction to the owner as an errata item: `AUDIT-PLAN.md` M5 still reads "all
   231 transcripts" (AUDIT-PLAN.md is byte-identical at 0684af57 on main, worker, and
   orchestrator lanes — verified by blob sha). The BOSS does not write `AUDIT-PLAN.md`
   (write set is `fleet/LOG.md`, `fleet/ORDERS/`, `fleet/BOSS-STATE.md`,
   `fleet/heartbeats/BOSS.log`), so it is raised as a BOSS CONCERN for owner action and must
   not be silently edited by anyone.

## Credit where due
The worker's handling was correct and is the standard: `tools/CORPUS.md` states "the
battery's '231' counts directory entries; the transcript count is **230**" and "AUDIT-PLAN
M5's 'all 231 transcripts' should read 230 — disclosed here, not silently corrected." Every
census number in that file reproduced exactly on an independent extraction (see REDIRECT-002
and the BOSS LOG entry for the spot-check).

DONE = 1-4 pushed to your lane + a LOG line on your lane naming this order. Report the
denominator you are now using.
