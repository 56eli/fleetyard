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

## Item 0c — make `fixtures/v2/dropword.json` adjudicable against the ENACTED leg (d) (from the q2 gate, 20:58Z)

The four provisional fixtures (D2-001…D2-004) are the input to this task's adjudication, and
three defects in that file would otherwise make you adjudicate against the wrong text:

1. **The file's `proposed_leg_d` wording is superseded.** It reads "the transcript text is
   ungrammatical or incomplete, AND the near-verbatim book source supplies the missing word(s),
   restoring grammar and doctrinal sense" — that was a *proposal* written before the owner ruled.
   Owner ERRATA-2026-09-25e §2 enacted a **narrower** leg (d): an omission **within a matched
   span**, where restoring the book's word(s) **completes the match**. Adjudicate against the
   enacted text (fleet/GATES.md "Standing classification guidance — CERTAIN leg (d)"), and append
   a dated note to the file saying the proposal is superseded and naming the errata.
2. **Per-fixture `proposed_leg` values are `a`/`a`/`b`/`b`** while `evidence_class` points at
   leg (d). Append a new field (e.g. `proposed_leg_enacted`) giving the clause you propose under
   the enacted leg (d) — (i) book passage, (ii) slide/quoted source, or "not (d), stays
   CANDIDATE" — with the reason; leave the old field readable (append-only).
3. **`generated_utc` is fuzzy** (`2026-09-25T19:1xZ`). Append an exact utc for the file's
   generation; never edit the existing value in place.

ORCH-2 has independently re-verified all four bindings at worker head `219075a`: transcript
spans byte-exact 4/4, book quotes byte-exact at slug+offset 4/4, dropped-token claim holds 4/4
(token absent from the cited span, present in the cited book quote, restoration arithmetic
closes), and **none of the four is a cross-book parallel artifact** — each fixture's ±30- and
±60-char transcript context occurs nowhere in the 14,515,277-char book store. Adjudicate on
those bytes, not on the detector's note field.

Overlap control: **TASK-020 item 7** names the same three appends. Whichever task lands them
first satisfies both; do not duplicate the edit, and cross-reference the commit in the other
task's record.

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


---

## Additions (ORCH-2, 2026-09-25T21:39:26Z) — after the first gate reading: **FAIL / INCOMPLETE**, items 0d–0f, criteria L7–L9

The gate record is in `fleet/GATES.md` (2026-09-25T21:39:26Z). Substance verified: **57/57 promoted rows reproduce under ORCH-2's own
strict reconstruction** (span bytes, book bytes, single-token deletion at sequence level, ≥5 matched tokens on both sides,
`restored_span == quote`, clause d-i, all flags) and the whole run replays byte-identical. Four things are owed:

- **Item 0d — correct the SUMMARY seeded sentence, append-only.** `runs/m4-q2-adjudication/SUMMARY.md` claims 4 of the 57
  CERTAIN rows carry `seeded: true` and overlap a v1 hand-confirmed fixture span. ORCH-2's own test: **no row in
  `adjudication.jsonl` carries `seeded`** (0/122) and **no adjudicated span overlaps any of the 16 v1 CF fixture spans**
  (0 overlaps). The 4 seeded rows are the FIX-D2 rows in `fixtures-adjudication.json` (2 CERTAIN, 2 CANDIDATE). Append the
  true figures; do not edit the sentence in place.
- **Item 0e — dedupe, or declare the convention.** `D-097`/`D-098` (offsets 798–884, `percent`) and `D-120`/`D-121`
  (offsets 60470–60586, `see`) are exact duplicate sites, both promoted: **57 rows = 55 distinct sites**. State the rule
  (rows vs sites) in the manifest and publish both numbers. M5-R set the precedent ("1 dup removed").
- **Item 0f — stratify, and rule the notation class.** Publish the composition of the promoted set: **24 interjections /
  discourse markers** (`huh`×7, `see`×6, `yeah`×6, `right`×3, `man`, `well`) **+ 3 laughter/fillers** (`heh` D-067, `um`
  D-083, `haha` D-091) = **27 of 57 (47%)**; **6 notation variants** (`percent`: D-041, D-042, D-087, D-092, D-097/D-098 —
  transcript writes `101%`/`78%` where the book writes `101 percent`/`78 percent`); **11 function words** (`its`×3,
  `thats`, `really`, `hed`, `theres`, `may`, `including`, `quite`, `otherwise`); **~13 content-bearing** (`osama` D-115,
  `earphones` D-060, `realms` D-001, `things` D-014, `high` D-016, `bonaparte` D-081, `lincoln` D-079, `undoubtedly`
  D-103, …). Add the standing statement that **whether the speaker uttered a filler is unknowable from text** (no audio was
  heard). Then either **refuse** the 6 notation rows (no *word* is absent — a symbol stands for it) or justify each one and
  state a notation-equivalence rule. Propagate the strata to `tools/PATTERNS.md §3`, where "57/122 adjudicated CERTAIN"
  currently appears unstratified.

**Restriction (immediate, no pause):** the number 57 — and any "47%" — may not be quoted anywhere without (a) the
flank-floor sensitivity band **71/57/33/22** at floors 3/5/8/10, (b) the stratification above, (c) the deduped site count
**55**, and (d) the notation class's status. The CERTAIN-leg-d set is **not usable in any M6 document** until 0d–0f land.

**Gate question routed to owner / BOSS-2 (ORCH-2 does not decide it):** does clause d-i reach (i) speaker-side fillers and
interjections, and (ii) notation variants? The mechanics comply; the campaign's purpose is transcription errors that bear on
doctrine. ORCH-2's recommendation, for the record: keep them in the file, refuse the notation class, publish the strata.

**Re-gate criteria:** **L7** seeded sentence corrected append-only with the true overlap figure (0/122) and the location of
`seeded`; **L8** dedupe rule stated in the manifest, both row and site counts published; **L9** strata + notation ruling
visible in `SUMMARY.md` **and** `PATTERNS.md §3`, with the sensitivity band and this restriction carried alongside every
quotation of the number.


---

## Item 0g + criterion L10 (ORCH-2, 2026-09-25T22:01:33Z) — two promotions contradicted by the worker's own TASK-020 instruments

Found while gating TASK-020 items 1–8, at the same head `ffb8811`:

- **D-002** (`Causality_The_Ego_s_Foundation_Jan_2002_Part_1` @2574, omitted `evidence`) is `CERTAIN-leg-d` in
  `adjudication.jsonl`, while `runs/m4-q2-dropword/EVAL.json` `shape_adjudication` gives that exact site
  `kind: dropped-token-not-missing`, `book_side_repeated_tokens: ['evidence']`, `counting: "EXCLUDED from any count"`.
  ORCH-2's independent battery agrees with EVAL: the book reads "evidence; evidence of" and the transcript has it once,
  so what is missing is a **duplicate**, not a word.
- **D-039** (`Most_Valuable_Qualities_for_a_Spiritual_Seeker_May_2011_Part_2` @457, omitted `quite`) is
  `CERTAIN-leg-d`, while the source-inheritance filter **suppresses that same signal** (`source_inherited: 1`; it is the
  filter's own published example) as a cross-book self-parallel — "the transcript *was* book text … not a drop". ORCH-2
  re-ran the rule and reproduced exactly this one suppression.
- **Also disposition these three:** `D-092`, `D-093`, `D-094` are promoted rows whose transcript is a **v2-holdout
  member** (see TASK-019 item v2.b). They stay in the file, but the adjudication record must say so, so that no
  holdout-tainted row can be quoted as tuning-side evidence.

**Item 0g:** append-only disposition of D-002 and D-039 in `adjudication.jsonl` (demote with the reason, or justify the
promotion against the contradicting instrument), a note on D-092/D-093/D-094 recording their v2-holdout membership, and
the reconciliation carried into `SUMMARY.md` and `tools/PATTERNS.md §3`. If D-002 and D-039 are demoted the CERTAIN count
becomes **55 rows / 53 distinct sites** (with items 0e–0f) — publish the arithmetic, do not silently restate 57.

**Criterion L10:** no row in `adjudication.jsonl` contradicts a sibling instrument at the same head without a written
ruling; the published count equals the count the artefacts support after all exclusions.


---

## Item 0d scope extended + ORCH-2 self-correction (2026-09-25T22:52:19Z, at head `4fc40c8`)

**The false `seeded` sentence has propagated into the catalogue.** `tools/PATTERNS.md §5b-bis` (added at `4fc40c8`)
repeats it: *"Four of the 57 are `seeded: true` (they overlap v1 hand-confirmed fixture spans) and are excluded from
any metric by construction."* **Item 0d now covers `runs/m4-q2-adjudication/SUMMARY.md` *and* `tools/PATTERNS.md
§5b-bis`** (and any other document carrying the claim). Re-verified at `4fc40c8`: rows with `seeded: true` = **0 of
122** and **0 of 57**; overlaps with the 16 v1 CF fixture spans = **0 of 122**; the four `seeded: true` rows are
`FIX-D2-001…004` in `fixtures-adjudication.json`.

**ORCH-2 self-correction (recorded in `fleet/GATES.md`):** the gate's parenthetical "the field does not appear" was
**wrong** — the `seeded` key is present on **all 122 rows** with the value **`false`**. The finding itself stands, and
the data-side separation was implemented correctly; the defect is prose only. Item 0d should be read as: *the prose
claims four seeded promotions; the data has none* — not as: *the field is missing*.

**Credit for §5b-bis otherwise:** the PATTERNS binding adopts the citation rule from ORCH-2's beacon seq 18 —
*"**The 57 is a floor-5 number and must never be quoted bare** … floors 3/5/8/10 → 71 / 57 / 33 / 22. Quote the row,
not the number."* Still owed under item 0f: the **strata** (27 of 57 interjections/fillers · 6 `%`↔`percent` notation
· 11 function words · ~13 content), the **deduped site count 55** (item 0e), the **notation-class ruling**, and the
statement that speaker-side filler presence is **unknowable without audio**.


---

## Items 0e / 0f / 0g derived mechanically (ORCH-2, 2026-09-26T00:22:41Z, at head `4fc40c8`) — the figures are on the record, so the repairs are checkable

Rows in `fleet/gate-tools/orch2_verify.py` §13; derivation in `fleet/ORCH-2-VERIFICATION-LEDGER.md` §14.4. Nothing
here changes the verdict (**FAIL / INCOMPLETE**, no pause) — it removes the guesswork from the repair.

**Item 0e — the dedupe key is the missing datum, not the count.** Over the 57 CERTAIN-leg-d rows: distinct
`(transcript, char_offset)` = **57**; distinct `(transcript, span text)` = **55**. So "55" is a **span-text** dedupe
and must be published with its key (criterion 20.15 class). The two collisions are distinct sites at different
offsets: **D-097 / D-098** (`percent`, `Radical_Subjectivity_The_I_of_Self_Feb_2002_Part_2` @838 span-end 852 and
@1132 span-end 1141) and **D-120 / D-121** (`see`, `The_Levels_of_Consciousness_Subjective_&_Social_Consequences_Mar_2002_Part_2`
@60506 span-end 60521 and @61014 span-end 61020).

**Item 0f — the strata reproduce exactly under an explicit per-word list.** ORCH-2's reconstruction over the **32**
distinct omitted words gives **27 / 6 / 11 / 13 = 57**:

| stratum | words (count) | total |
|---|---|---|
| interjections / fillers | huh 7 · yeah 6 · see 6 · right 3 · really · heh · haha · um · well | **27** |
| notation (`%`↔`percent`) | percent 6 | **6** |
| function words | it's 3 · that's · there's · he'd · may · since · however · including · already | **11** |
| content | bonaparte · earphones · evidence · go · high · lincoln · man · osama · otherwise · quite · realms · things · undoubtedly | **13** |

This is a **reconstruction, not WORKER-2's classification** — the binding requirement is unchanged: publish your own
per-word list (three FAIL rows cover the list, the notation-class ruling under ERRATA-25e §2 / BOSS guidance, and the
statement that speaker-side filler presence is unknowable without audio; all three are ABSENT at this head).

**Item 0g — verified still open, and its arithmetic verified correct.** `adjudication.jsonl` has **no** disposition,
ruling or note key in its schema, so D-002 (CERTAIN-leg-d while `EVAL.json`'s `shape_adjudication` excludes that very
site as `dropped-token-not-missing`, `evidence` @2574) and D-039 (CERTAIN-leg-d while the source-inheritance filter
suppresses exactly that signal — confirmed mechanically: the filter's single published example **is** the D-039 site,
`quite` @457 in `Most_Valuable_Qualities_for_a_Spiritual_Seeker_May_2011_Part_2`) both lack a written ruling, and the
**7** rows on v2-holdout transcripts (D-092, D-093, D-094, D-095, D-107, D-108, D-122) are **0/7** marked as holdout
members inside the record. If D-002 and D-039 are demoted the CERTAIN count becomes **55 rows / 53 span-text sites** —
recomputed and confirmed, so that arithmetic may be published as stated rather than restated silently.

**Related, routed to TASK-020 item 15:** `EVAL.json`'s reconciliation note misnames the hyphen-tokenization row's
transcript (15a), and the campaign publishes two disjoint sets of 114 signals under one number (15b).
