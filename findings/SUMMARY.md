# M5-R — reviewed findings ledger (SUMMARY)

> **Titles qualified (TASK-016 R2):** "reviewed" here means **machine-adjudicated against cited bytes** — this is a machine-adjudicated reduction of the raw census, not a human finding pass. Read every count below with the coverage row immediately following.

**Reduction of the inherited M5 raw census (TASK-011, lane `arena/01a0d581-fleetyard` @ `bf97d85`) into findings with evidence.**

> Honesty scope: every finding here is *machine-adjudicated* — citations and book offsets were re-verified byte-exact, repetition/anomaly structure was re-derived from the frozen bytes, and fixture-tuned hits are separated. **No audio was heard; no human read every transcript.** CERTAIN is assigned only by inheritance from the v1 hand-confirmed fixture set, never by this tool. There is **no corpus-wide error rate** in this document (LAW §9: precision/recall need held-out data; only the ledger is delivered). CANDIDATE is never blended into anything.

**Coverage truth (STANDARDS honesty rule; the campaign's row since v1):**

`transcripts 230 | detector-run 230 | machine-adjudicated 230 | human finding-pass audited 0 | pending human review 230 | zero-finding transcripts 24 (not shown clean)`

## 1. Reduction funnel

| stage | count |
|---|---|
| raw signals loaded (inherited census) | 1336 |
| record files | 230 |
| citation failures (quote not byte-exact at offset) | 0 |
| duplicate signals removed (same detector+quote) | 0 |
| **merged findings** | **1334** |
| transcripts with >=1 finding | 206 of 230 |

Reading of the funnel: the inherited census is **1,334 records**; two of them carry two detector signals each (**1,336 signal instances**), and those two convergent records merge back to one finding each — hence 1,334 findings, one per inherited record, with no exact duplicates found (0 removed).

## 2. Classification (STANDARDS ladder)

| class | findings | seeded | note |
|---|---|---|---|
| CERTAIN (inherited fixture) | 3 | 3 | prior v1 hand-confirmed fixtures; in-sample |
| HIGH (convergence, proposed) | 0 | 0 | >=2 independent families + written rationale; gate review |
| CANDIDATE | 1331 | 0 | single signal; human read required |

Seeded / independent split (LAW §9): **seeded (fixture-overlap, in-sample) = 3**; **independent = 1331**. Seeded findings are excluded from any precision/recall claim by construction.

## 3. By detector (merged findings carrying it)

| detector | findings | raw signals |
|---|---|---|
| A1-repetition | 938 | 938 |
| A2-nonsense | 158 | 158 |
| B1-contradiction | 12 | 12 |
| B2-misquote | 228 | 228 |

## 4. By year (file-name year; unknown kept separate)

| year | findings | CANDIDATE | HIGH | CERTAIN(inherited) |
|---|---|---|---|---|
| 2002 | 282 | 282 | 0 | 0 |
| 2003 | 16 | 16 | 0 | 0 |
| 2004 | 97 | 97 | 0 | 0 |
| 2005 | 90 | 90 | 0 | 0 |
| 2006 | 57 | 57 | 0 | 0 |
| 2007 | 199 | 199 | 0 | 0 |
| 2008 | 175 | 174 | 0 | 1 |
| 2009 | 76 | 76 | 0 | 0 |
| 2010 | 52 | 52 | 0 | 0 |
| 2011 | 60 | 58 | 0 | 2 |
| unknown | 230 | 230 | 0 | 0 |

## 5. Review queue — transcripts by finding count (top 20)

| transcript | findings | classes |
|---|---|---|
| A_Unique_Sedona_Seminar_Dec_2008_Part_1_enxautogen_html.txt | 34 | CANDIDATE |
| Causality_The_Ego_s_Foundation_Jan_2002_Part_3_enxautogen_html.txt | 30 | CANDIDATE |
| Positionality_and_Duality_Transcending_the_Opposites_Apr_2002_Part_2_enxautogen_html.txt | 28 | CANDIDATE |
| The_Levels_of_Consciousness_Subjective_&_Social_Consequences_Mar_2002_Part_1_enxautogen_html.txt | 27 | CANDIDATE |
| The_Levels_of_Consciousness_Subjective_&_Social_Consequences_Mar_2002_Part_2_enxautogen_html.txt | 26 | CANDIDATE |
| A_Unique_Sedona_Seminar_Dec_2008_Part_4_enxautogen_html.txt | 23 | CANDIDATE |
| The_Levels_of_Consciousness_Subjective_&_Social_Consequences_Mar_2002_Part_3_enxautogen_html.txt | 19 | CANDIDATE |
| Causality_The_Ego_s_Foundation_Jan_2002_Part_1_enxautogen_html.txt | 18 | CANDIDATE |
| Happiness_Apr_2009_Part_3_enxautogen_html.txt | 18 | CANDIDATE |
| A_Review_of_the_Work_Sep_2007_Part_1_enxautogen_html.txt | 17 | CANDIDATE |
| God_vs_Science_Limits_of_the_Mind_Feb_2007_Part_3_enxautogen_html.txt | 17 | CANDIDATE |
| Question_Answer_Session_Mar_2011_enxautogen_html.txt | 16 | CANDIDATE |
| Spiritual_Truth_vs_Spiritual_Fantasy_Jun_2006_Part_2_enxautogen_html.txt | 16 | CANDIDATE |
| A_Unique_Sedona_Seminar_Dec_2008_Part_2_enxautogen_html.txt | 15 | CANDIDATE, CERTAIN |
| Causality_The_Ego_s_Foundation_Jan_2002_Part_2_enxautogen_html.txt | 15 | CANDIDATE |
| Positionality_and_Duality_Transcending_the_Opposites_Apr_2002_Part_3_enxautogen_html.txt | 15 | CANDIDATE |
| Positionality_and_Duality_Transcending_the_Opposites_Apr_2002_Part_1_enxautogen_html.txt | 14 | CANDIDATE |
| What_is_the_World_Feb_2009_Part_3_enxautogen_html.txt | 14 | CANDIDATE |
| A_Review_of_the_Work_Sep_2007_Part_3_enxautogen_html.txt | 13 | CANDIDATE |
| Practical_Spirituality_Oct_2008_Part_3_enxautogen_html.txt | 13 | CANDIDATE |

## 6. HIGH findings (each with its independence rationale)

(none)

## 7. CERTAIN (inherited fixture) findings

- **M5R-0078** ↔ CF-015 @5833 — `Spiritual purity has no influence. Interest in the personal lives of s` → `Spiritual purity has no interest in the personal lives of students.` (leg b; WORKER hand-read (TASK-002); re-audited TASK-006: retained C)
- **M5R-0460** ↔ CF-006 @2355 — `And above which all the energies are negative. And above which all the` → `And above which all the energies are positive.` (leg b; WORKER hand-read (TASK-002); re-audited TASK-006: retained C)
- **M5R-0461** ↔ CF-003 @4543 — `255% of people are happy` → `55% of people are happy` (leg b; WORKER hand-read (TASK-002); re-audited TASK-006: retained C)

## 8. Book-byte adjudication

- findings carrying a cited book reference: 242
- cited book quotes verified byte-exact at the cited offset: 242
- cited book offset/slug failures: 0
- book references to non-Hawkins entries (text reliable, doctrine not): 0

## 9. Mechanical facts attached to every finding

`ledger.jsonl` / `by-transcript/*.json` carry, per finding: citation (offset + span_end + verbatim span), the runner's claim (evidence string, asserted intended text), the re-derived repetition structure (A1) or surface anomaly (A2), the verified book check + word-level divergence + number comparison (B1/B2), fixture overlap, class + rationale, `seeded`, and `review_status=machine-adjudicated (mechanical bytes only); human confirmation required`.

## 10. Mechanical corroboration of the runner's own claims

Each raw signal's evidence string was re-derived from the bytes where a mechanical check exists (LAW §7: identical output alone is not suspicion — missing fresh evidence is; this is that fresh evidence). After errata #2 (M4-q5: Unicode tokenizer + unit bound 16) every checkable claim corroborates; a 'not corroborated' row would be a **review flag**, not a verdict.

| detector | signals | corroborated | failed | not machine-checkable |
|---|---|---|---|---|
| A1-repetition | 938 | 938 | 0 | 0 |
| A2-nonsense | 158 | 158 | 0 | 0 |
| B1-contradiction | 12 | 12 | 0 | 0 |
| B2-misquote | 228 | 228 | 0 | 0 |

Review queue: `REVIEW-QUEUE.md` (top 100 by mechanical score; the score is an ordering aid, never a class).

## 11. Coverage truth

- All 230 transcripts are present in `by-transcript/`; **24 carry zero findings** — that is *not* evidence of being error-free (the detectors are known to miss fluent errors; drop-word and speaker/format detectors do not exist).
- Detectors that produced the raw census: A1-repetition, A2-nonsense, B1-contradiction, B2-misquote. A4-confusion, drop-word and speaker/format were not run (unmeasured, not zero).
- Provenance: see `PROVENANCE.json` (inputs pinned by sha256; corpus digest method defined explicitly, unlike the inherited run's).

_Generated 2026-09-25T19:17:57Z by `tools/m5r_reduce.py` (6d4bb9ce78f2964e)._
