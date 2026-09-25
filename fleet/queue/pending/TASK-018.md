# TASK-018 — leg (d) individual adjudication: the 122 drop-word signals + the 4 provisional fixtures

- cut by ORCH-2 (A-2026-09-25-002) 2026-09-25T20:02Z · milestone **M4** (classification
  boundary) · authority: owner `fleet/ERRATA-2026-09-25e.md` §2–§3 @ main `8e9e179`
- claimant: WORKER-2 (A-2026-09-25-001) — **first task after the PAUSE removal**
  (M5-R re-gate PASS @ `1beadd9`); TASK-017 follows
- inputs (read-only): `runs/m4-q2-dropword/signals.json` (122 signals, sha256
  `8d71f57bcb80313fcf8a635587525e65ff7e4603fd431494c1c45c6d1eea83b4`),
  `fixtures/v2/dropword.json` (D2-001..D2-004, provisional), `tools/det_dropword.py`,
  the frozen corpus + book store, and the gate-PASS M5-R ledger `d42136c6…`
- guidance that binds this task: **fleet/GATES.md → "Standing classification guidance —
  CERTAIN leg (d)"** (restatement of ERRATA-25e §2; criteria L1–L6 are the gate)

## Item 0 — one append-only correction (owed, small, do it first)
`findings/M4-q5-A1-CLAIM-RECONCILIATION.md` row 3 (M5R-0036) states the span re-derived as
"period 2 (`Mm-hmm` = 2 tokens in the Unicode rule), 8 repeats — claim reads the unit as 1
token", and calls it a labelling nuance. The artefact says the opposite: under the actual
token rule `Mm-hmm` is **one** token, the span is 8 tokens, and the ledger records
`unit_tokens 1, span_repeats 8` with the note "claim 1-token x8 vs re-derived 1 x8" — claim
and derivation agree exactly; the nuance does not exist (ORCH-2 tokenised the span
independently: `['mm-hmm'] * 8`). Append a correction line (never edit the claim away —
append-only), and state the correct rule: hyphenated forms are ONE token under
`[^\W_]+(?:['’\-][^\W_]+)*`.

## Item 0b — bind PATTERNS.md to the ledger it quotes (repairs TASK-014 q1.4d, gate FAIL)
`tools/PATTERNS.md` (sha256 `528265e7…`) quotes M5-R-derived figures — coverage 3/16 and the
corroboration column 938/938 · 158/158 · 12/12 · 228/228 — with **no binding to the source
ledger** (ORCH-2 gate, fleet/GATES.md 20:08Z). Append (never rewrite) a provenance block
naming: `findings/ledger.jsonl` sha256 `d42136c673188f9e091526083b95941cabc5822a8b5cffeb8913b942cb658a32`,
`findings/PROVENANCE.json` `by_transcript_digest c1ec4da8…`, the producing `tool_commit
dada3e60…`, the worker head the figures were read at (`1beadd9`), and the read utc — plus the
rule "any figure on this page is void unless the named ledger digest matches". While you are
in the file, append one dated line recording that `PAUSE-WORKER-A-2026-09-25-001` was
**REMOVED** at 2026-09-25T20:02Z on the M5-R re-gate PASS (the page still says M4 is parked
under it). Both are append-only lines; no figure changes.

## Work
1. For **each** of the 122 drop-word signals, individually decide: does it satisfy leg (d)
   (all three clauses, cited to bytes), or does it stay **CANDIDATE**? Record per finding:
   transcript + offsets + verbatim span; the ground-truth span (book slug + offset +
   verbatim passage, or the same transcript's immediately adjacent repetition with its
   offsets); the omitted word; the restored span; clause (d)(i) or (d)(ii); and the reason
   if it fails.
2. The 4 provisional fixtures: confirm or discard each **with reasons** under the same
   clauses (the corpus is frozen — nothing is "fixed", only confirmed/discarded). They are
   in-sample: mark `seeded`/in-sample and keep them out of any metric (LAW §9).
3. Report counts **per clause** (d)(i)/(d)(ii)/CANDIDATE, plus a short list of the closest
   near-misses and why they failed. No rate, no precision, no corpus-wide figure.

## Boundaries (gate-enforced)
- **Detector hits never auto-classify.** No rule, threshold, score or detector name may be
  the reason for a class; every classification is per finding with cited bytes (ERRATA-25e
  §3, LAW §9).
- **Narrowness is the point:** a lecture's free paraphrase of a book is NEVER leg (d);
  omissions outside a matched span stay CANDIDATE unless they independently satisfy leg (a).
- No new detector, no tuning of `det_dropword.py`, no threshold changes in this task; if a
  defect is found, record it as an errata + regression test, do not silently retune.
- **Do not re-run the spent holdout** (`runs/m4-q4-holdout/`, `holdout_consumed` stamped):
  it is single-use evidence; a fresh sealed split is a separate decision (TASK-014 q4).
- No writes outside this lane's outputs; stdlib only; no network; corpus read-only.
- Keep cadence: heartbeat + CONTROL.log at ≤300 s **and read your controls + the
  orchestrator lane every cycle** (ERRATA-25f §2–§3; the 19:08–19:16Z cycles did not).
- Idle cycles are correct when nothing is actionable; never end a turn for idleness.

## Gate (ORCH-2, per LAW §9 — any failed criterion = INCOMPLETE)
L1 per-finding record complete · L2 every citation re-derived byte-exact by me (book bytes
with my own parser; adjacency from the frozen overlay) · L3 restoration is minimal (one
word) and completes the match · L4 no blanket promotion; counts per clause · L5 in-sample
separated, never precision evidence · L6 vocabulary elsewhere unchanged (HIGH still needs
≥2 independent signals + a written independence rationale; CANDIDATE never blended; no rate
without held-out evidence fixed before tuning). Plus the campaign defaults: suite green
WITH corpus and skip counts reported, test count never drops, LAW §8 manifest on every new
run, fresh replay, delivery labelled DELIVERY (not completion).
