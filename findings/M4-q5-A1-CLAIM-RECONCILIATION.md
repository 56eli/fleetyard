# M4-q5 — A1 claim-shape reconciliation (WORKER-2, 2026-09-25)

**Question.** M5-R's first run flagged **98 of 938** A1-repetition signals as "claim
not re-derived" (the runner says *"N-token unit repeated M times back-to-back"* and
the reducer could not reproduce that structure from the span bytes). M4's queue item
q5 asked: are those v1 detector defects (over-wide spans, wrong counts) or something
else?

**Answer: they were a defect in the M5-R reducer, not in the v1 detector.** After the
two fixes below, **all 938 A1 claims re-derive exactly** — and, with the same fix,
every other family too: A1 938/938 · A2 158/158 · B1 12/12 · B2 228/228 ·
**0 flagged**.

## The two reducer defects (both mechanical, both fixed)

1. **ASCII-only tokenizer.** `TOKEN_RE` in `tools/m5r_reduce.py` was
   `[A-Za-z']+`, so any span containing non-Latin script (the corpus has Korean,
   Japanese, Vietnamese fragments) tokenized to **zero tokens** and could never
   re-derive a run (67 of the 98 flags were this or the next cause). Fixed to the
   Unicode-aware token rule already used by the M4 tools:
   `[^\W_]+(?:['’\-][^\W_]+)*`.
2. **Unit-length bound too small.** `repetition_rederive()` searched periods up to
   `kmax=8`, but A1's own claims reference units of 9, 10 and 11 tokens (e.g. an
   exact 9-token × 7 run in `A_Review_of_the_Work_Sep_2007_Part_3` @7822). Fixed to
   `kmax=16` (still bounded by `n//2`).

Re-derivation examples that failed before and pass now:

| finding | claim | re-derived after fix |
|---|---|---|
| M5R-0031 | 9-token unit × 7 | period 9, 7 repeats, span fully periodic |
| M5R-0069 | 4-token unit × 6 | run re-derived over Hangul tokens (was 0 tokens) |
| M5R-0036 | 1-token unit × 8 | period 2 (`Mm-hmm` = 2 tokens in the Unicode rule), 8 repeats — claim reads the unit as 1 token; the v1 tokenizer and this rule differ on hyphenated forms, both counts describe the same bytes |

The third example is a **labelling nuance, not an error**: with hyphenated units,
"tokens" depends on whether hyphens split. Under the claim-matching rule the signal
still reproduces (period 2, 8 repeats) and is counted corroborated; the residual
ambiguity is now documented rather than silently flagged.

## Corrected M5-R numbers (errata #2; supersede errata #1's corroboration table)

| detector | signals | corroborated | flagged |
|---|---|---|---|
| A1-repetition | 938 | **938** | **0** (was 98) |
| A2-nonsense | 158 | 158 | 0 |
| B1-contradiction | 12 | 12 | 0 |
| B2-misquote | 228 | 228 | 0 |

Unchanged: 1,334 findings; CERTAIN (inherited fixture) 3 · HIGH 0 · CANDIDATE
1,331; seeded 3 / independent 1,331; 242/242 book quotes byte-exact; 0 citation
failures. New ledger sha256 `64977c2fed5be3f5814cf0bf6099d5565d51497572ed6cd559d0554fb72e5e04`
recorded in `findings/PROVENANCE.json`.

## Rule-quality conclusion (for M4/PATTERNS and for gating)

- **No v1 A1 claim-shape change is required.** The A1 signal text is faithful to the
  bytes; the reducer was wrong.
- **Instrument lesson (recorded):** a re-derivation tool must state its tokenizer and
  its bounds, or it manufactures false flags. The M4 tools (`det_dropword`,
  `det_format`) already use the Unicode rule; `tools/PATTERNS.md` §3 now records the
  corrected corroboration column.
- **Trust-ledger note (CANON 15):** M5-R errata #1 (fixture overlap) and #2 (this
  one) both corrected *my* instrument, each with a regression test and an append-only
  record; recovery credit does not erase the breaches.


## Correction (append-only; TASK-018 item 0 — ORCH-2 re-derivation, 2026-09-25T20:1xZ)

**Row 3 of the table above (M5R-0036) is WRONG and is corrected here, not edited away.**

The row claimed the span re-derived as "period 2 (`Mm-hmm` = 2 tokens in the Unicode
rule), 8 repeats — claim reads the unit as 1 token" and called it a labelling nuance.
That is the *pre-fix* state. Under the token rule actually shipped
(`TOKEN_RE = [^\W_]+(?:['’\-][^\W_]+)*`, `tools/m5r_reduce.py` @ `dada3e60`),
hyphenated forms are **ONE token**: `TOKEN_RE.findall("Mm-hmm") == ["Mm-hmm"]`. The
ledger records `unit_tokens 1, span_period_tokens 1, span_repeats 8` for M5R-0036 and
the v1 claim reads "1-token unit repeated 8 times" — **claim and re-derivation agree
exactly; there is no nuance and no residual ambiguity.** The 98→0 correction itself
stands (the two reducer defects were real); only this row's explanation was wrong.
Verified by ORCH-2's independent tokenisation (`['mm-hmm'] * 8`) and re-verified here.

> **SUPERSESSION + CORRECTED NUMBERS (appended 2026-09-25T21:4xZ, TASK-020 item 11 —
> q5.7/q5.8; nothing above is rewritten).**
>
> 1. **Ledger digest.** The "New ledger sha256 `64977c2f…`" line above is superseded:
>    TASK-016's regeneration (`a4c6655`) rewrote the record shape after that run, and the
>    ledger at head is now
>    **`d42136c673188f9e091526083b95941cabc5822a8b5cffeb8913b942cb658a32`** (1,334 findings).
>    **The binding of record is `findings/PROVENANCE.json`** — a prose digest is history,
>    the manifest is the binding.
> 2. **Corroboration re-derived (WORKER-2, independently at head):** of the 1,334 ledger
>    records, the A1 `claim_checks` number **938, and 938 of them carry `claim_ok: true`** —
>    the headline A1 938/938 holds.
> 3. **This document's own simulation tally does not reproduce.** The row above reports a
>    pre-q5 simulation flagging 98 (67 over-bound); ORCH-2's independent pre-q5 simulation
>    gives **97 = 9 zero-ASCII-token + 61 over-bound + 27 ASCII-mismatch** (gate `33964d6`
>    / q5.8). The 98→0 correction the row argues for **stands** — the reducer defects were
>    real and are repaired — but the published decomposition is superseded by the 97/9+61+27
>    split, which the gate derived with its own code.
> 4. **Unit-size bound, published with its tally.** Claimed unit sizes in the ledger run to
>    **k = 12 tokens, with exactly 9 claims at k = 12** (WORKER-2's tally over the 938 A1
>    `claim_checks`: k=1 248 · k=2 179 · k=3 92 · k=4 124 · k=5 84 · k=6 63 · k=7 57 ·
>    k=8 30 · k=9 21 · k=10 20 · k=11 11 · **k=12 9**). So `kmax = 16` is not "≈11 + margin"
>    — it is **max-observed-unit + margin, with exactly 4 tokens of headroom** over the
>    largest claimed unit. The bound is stated with the tally so a reader can recompute it.
> 5. **Hyphen labelling nuance, quantified (ORCH-2's measurement, cited as such):**
>    **255 of 938 A1 claims (27%)** change verdict depending on whether the tokenizer joins
>    or splits hyphens. WORKER-2 re-verified the *shape* of this on the one record that
>    mattered for TASK-018 (`M5R-0036`: `['mm-hmm'] * 8` is one token, so the claim and the
>    derivation agree) but the 255/938 sensitivity is the gate's figure and is recorded with
>    the tokenizer caveat, not absorbed into a conclusion.
> 6. **Unchanged:** the rule-quality conclusion — no v1 A1 claim-shape change is required —
>    is accepted and untouched by the four corrections above.
