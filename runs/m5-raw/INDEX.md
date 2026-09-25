# M5 raw signal census — PROVISIONAL, UNREVIEWED (TASK-011)

**This is not an audited-findings release.** Every record below is a *CANDIDATE-class raw signal, unreviewed*, including records the runner labelled `HIGH CONFIDENCE`. No detector precision has been measured. Clean-set checks (0/59) are in-sample only, invalid as an independent false-positive estimate. A transcript with zero raw hits is NOT shown to be error-free.

## Provenance

- generated_utc: `2026-09-25T00:54:33Z`
- corpus_zip_sha256: `3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db`
- overlays_sha256: `dec55ef15b05a5b4c23bfa98ff578964dd7b19ffe8a44fcd091d08fef7a1751a`
- tool_commit: `382095fd9d3a84c53e34983c41fb2109e6a8515c`
- detectors: `['A1-repetition', 'A2-nonsense', 'B1-contradiction', 'B2-misquote']`
- command: `python3 tools/sweep_m5.py --out runs/m5-raw`
- excluded:
  - A4-confusion — no independent held-out FP rate; fixture recall 0/16 independent (TASK-007 pending)
  - drop-word — detector never built (M2 accepted incomplete); unmeasured, NOT zero
  - speaker/format — detector never built (M2 accepted incomplete); unmeasured, NOT zero

## Coverage truth

| transcripts (.txt) | detector-run | pending detector run | finding-pass audited | pending review | failed reads |
|---|---|---|---|---|---|
| 230 | 230 | 0 | 0 | 230 | 0 |

## Raw unreviewed signal totals (CANDIDATE-class, not error counts)

Records: **1334**. A record is one merged span; a span flagged by two detectors counts once in the record total and once per detector below.

| detector | records carrying its signal |
|---|---|
| A1-repetition | 938 |
| A2-nonsense | 158 |
| B1-contradiction | 12 |
| B2-misquote | 228 |

| detector combination | records |
|---|---|
| A1-repetition | 937 |
| A1-repetition+B1-contradiction | 1 |
| A2-nonsense | 157 |
| A2-nonsense+B1-contradiction | 1 |
| B1-contradiction | 10 |
| B2-misquote | 228 |

Raw runner label (NOT a reviewed class): CANDIDATE 1332, HIGH CONFIDENCE 2

## By year (from file name; `unknown` kept separate)

| year | transcripts | detector-run | raw records |
|---|---|---|---|
| 2002 | 36 | 36 | 282 |
| 2003 | 18 | 18 | 16 |
| 2004 | 16 | 16 | 97 |
| 2005 | 21 | 21 | 90 |
| 2006 | 12 | 12 | 57 |
| 2007 | 27 | 27 | 199 |
| 2008 | 22 | 22 | 175 |
| 2009 | 12 | 12 | 76 |
| 2010 | 6 | 6 | 52 |
| 2011 | 8 | 8 | 60 |
| unknown | 52 | 52 | 230 |

## Re-review candidates (most raw records; NOT proven hotspots)

| transcript | year | raw records | per detector |
|---|---|---|---|
| A_Unique_Sedona_Seminar_Dec_2008_Part_1_enxautogen_html | 2008 | 34 | A1-repetition 8, A2-nonsense 26 |
| Causality_The_Ego_s_Foundation_Jan_2002_Part_3_enxautogen_html | 2002 | 30 | A1-repetition 2, B2-misquote 28 |
| Positionality_and_Duality_Transcending_the_Opposites_Apr_2002_Part_2_enxautogen_html | 2002 | 28 | B2-misquote 28 |
| The_Levels_of_Consciousness_Subjective_&_Social_Consequences_Mar_2002_Part_1_enxautogen_html | 2002 | 27 | A1-repetition 2, B2-misquote 25 |
| The_Levels_of_Consciousness_Subjective_&_Social_Consequences_Mar_2002_Part_2_enxautogen_html | 2002 | 26 | A1-repetition 4, A2-nonsense 1, B2-misquote 21 |
| A_Unique_Sedona_Seminar_Dec_2008_Part_4_enxautogen_html | 2008 | 23 | A1-repetition 18, A2-nonsense 5 |
| The_Levels_of_Consciousness_Subjective_&_Social_Consequences_Mar_2002_Part_3_enxautogen_html | 2002 | 19 | A1-repetition 3, B2-misquote 16 |
| Causality_The_Ego_s_Foundation_Jan_2002_Part_1_enxautogen_html | 2002 | 18 | A1-repetition 9, B2-misquote 9 |
| Happiness_Apr_2009_Part_3_enxautogen_html | 2009 | 18 | A1-repetition 14, A2-nonsense 4 |
| A_Review_of_the_Work_Sep_2007_Part_1_enxautogen_html | 2007 | 17 | A1-repetition 15, A2-nonsense 2 |
| God_vs_Science_Limits_of_the_Mind_Feb_2007_Part_3_enxautogen_html | 2007 | 17 | A1-repetition 15, A2-nonsense 2 |
| Question_Answer_Session_Mar_2011_enxautogen_html | 2011 | 16 | A1-repetition 12, A2-nonsense 4 |
| Spiritual_Truth_vs_Spiritual_Fantasy_Jun_2006_Part_2_enxautogen_html | 2006 | 16 | A1-repetition 11, A2-nonsense 5 |
| A_Unique_Sedona_Seminar_Dec_2008_Part_2_enxautogen_html | 2008 | 15 | A1-repetition 8, A2-nonsense 6, B2-misquote 1 |
| Causality_The_Ego_s_Foundation_Jan_2002_Part_2_enxautogen_html | 2002 | 15 | A1-repetition 3, B2-misquote 12 |
| Positionality_and_Duality_Transcending_the_Opposites_Apr_2002_Part_3_enxautogen_html | 2002 | 15 | A1-repetition 5, B2-misquote 10 |
| Positionality_and_Duality_Transcending_the_Opposites_Apr_2002_Part_1_enxautogen_html | 2002 | 14 | A1-repetition 3, B2-misquote 11 |
| What_is_the_World_Feb_2009_Part_3_enxautogen_html | 2009 | 14 | A1-repetition 13, A2-nonsense 1 |
| A_Review_of_the_Work_Sep_2007_Part_3_enxautogen_html | 2007 | 13 | A1-repetition 11, A2-nonsense 1, B2-misquote 1 |
| Practical_Spirituality_Oct_2008_Part_3_enxautogen_html | 2008 | 13 | A1-repetition 12, A2-nonsense 1 |

## Overlap with the 16 hand-read CERTAIN fixtures (dedupe before any findings ledger)

3 raw records overlap a confirmed fixture. They are the SAME errors, not additional ones; this is not a precision measurement.

- CF-003 @4543: A2-nonsense+B1-contradiction (runner: HIGH CONFIDENCE)
- CF-006 @2318: A1-repetition+B1-contradiction (runner: HIGH CONFIDENCE)
- CF-015 @5854: B2-misquote (runner: CANDIDATE)

## Zero-raw-hit transcripts (24; not evidence of zero errors)

- Belief,_Trust_and_Credibility_Jun_2008_Part_1_enxautogen_html
- Belief,_Trust_and_Credibility_Jun_2008_Part_2_enxautogen_html
- Devotion_The_Way_to_God_Through_the_Heart_Sep_2002_Part_1
- Devotion_The_Way_to_God_Through_the_Heart_Sep_2002_Part_3_enxautogen_html
- Dialogue,_Questions,_and_Answers_Dec_2003_Part_2_enxautogen_html
- Dialogue_Questions_and_Answers_Dec_2003_Part_3
- Enlightenment_Aug_2003_Part_1_enxautogen_html
- Enlightenment_Aug_2003_Part_3_enxautogen_html
- God_Transcendent_and_Immanent_Nov_2002_Part_3_enxautogen_html
- Integration_of_Spirituality_and_Personal_Life_Feb_2003_Part_1_enxautogen_html
- Integration_of_Spirituality_and_Personal_Life_Feb_2003_Part_3_enxautogen_html
- Perception_vs_Essence_Apr_2006_Part_2_enxautogen_html
- Realization_of_the_Self_The_Final_Moments_Dec_2002_Part_2_enxautogen_html
- Realization_of_the_Self_as_the_I_Nov_2003_Part_2_enxautogen_html
- Realizing_the_Root_of_Consciousness_Meditative_and_Contemplative_Techniques_Jun_2002_Part_3_enxautogen_html
- Satsang_Series_Volume_II_Part_1_enxautogen_html
- Spiritual_Community_Jun_2003_Part_1_enxautogen_html
- Spiritual_Community_Jun_2003_Part_2_enxautogen_html
- Spiritual_Community_Jun_2003_Part_3_enxautogen_html
- Spiritual_Survival_Realization_of_Reality_Nov_2007_Part_1_enxautogen_html
- The_Clear_Pathway_to_Enlightenment_Mar_2008_Part_1_enxautogen_html
- Transcending_Obstacles_Sep_2005_Part_3
- What_is_Real_Jun_2007_Part_2_enxautogen_html
- What_is_the_World_Feb_2009_Part_1_enxautogen_html

Per-transcript counts: `index.json` → `per_transcript`; records: `records/<transcript>.json`.
