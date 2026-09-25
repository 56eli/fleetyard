# CORPUS-AUDIT — David R. Hawkins lecture transcripts

**PROVISIONAL (TASK-012). Not an M6 certification. No corpus-wide error rate can be stated yet.**

- Rendered by `python3 tools/report_m6.py` at worker commit `5bf8e4219f4a65d364012fd2f02d3a21929cf434` (lane `arena/01a0d581-fleetyard`).
- Corpus: `docdocgo-fixes.zip` sha256 `3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db`; 230 transcript `.txt` files (the 231st directory entry is `manifest.json`, not a transcript); overlays digest `dec55ef15b05a5b4c23bfa98ff578964dd7b19ffe8a44fcd091d08fef7a1751a`.
- Raw census: `runs/m5-raw/` (TASK-011, PASS provisional raw only), tool commit `7b8863d0727b4dd7fbaa71683fd00feeebc832cd`, detectors A1-repetition, A2-nonsense, B1-contradiction, B2-misquote.
- Authority note: produced after the worker's original 4-hour wall, on the owner's chat instruction (main `e8d81ae`: "Chat session is authority"). The orchestrator holds post-cap worker output pending a worker-specific owner record on main.

## 1. Executive answer: how bad is it?

**We don't know yet, in any measured sense, and this report does not pretend to.** What exists:

1. **Reviewed evidence is a tiny, non-random sample.** 16 CERTAIN transcription errors (proof legs: a 9, b 7) plus 5 reviewed HIGH CONFIDENCE ones were found by hand-reading **3 of 230 transcripts** (17,928 words, 0.69% of the corpus's 2,607,819 words). In those 3 transcripts that is at least **8.9 CERTAIN errors per 10,000 words** (11.7 with reviewed HIGH). This is a *lower bound for those 3 files only*: they were not randomly chosen and the hand-read was not proven exhaustive. It must not be extrapolated to the corpus.
2. **Automatic detectors ran on 230/230 transcripts** and emitted **1334 unreviewed raw signals** on 206 transcripts. None has been reviewed. **Finding-pass audited: 0/230; pending review: 230/230.** Detector precision is **unmeasured**, so raw counts are *not* error counts; they may be mostly false alarms or a small fraction of real errors.
3. **The detectors are known to miss most errors.** Together they overlap only 3 of the 16 hand-found CERTAIN errors (CF-003, CF-006, CF-015). Most confirmed errors are fluent, plausible English (homophones, misheard numbers, swapped function words) that no current detector sees.
4. **Whole error classes were never measured:** dropped words and speaker/format errors (no detector built), and acoustic confusion (A4 excluded, no independent false-positive rate). Unmeasured is not zero.

**Qualitative reading (not a rate):** every transcript that has been read closely contains meaning-changing errors, including in doctrinal content (calibration numbers, happiness-table percentages, scripture and prayer wording, the positive/negative polarity of level 200). Readers should treat any exact number, name or quotation in these transcripts as unverified until checked against the books.

## 2. Coverage truth

| transcripts | detector-run | finding-pass audited | pending review | hand-read (M1) | failed reads |
|---|---|---|---|---|---|
| 230 | 230 | 0 | 230 | 3 | 0 |

Excluded from scope: `extra-sources/` Book-of-Slides OCR (owner UNDECIDED); the 4 non-Hawkins books in the book store (never cited as Hawkins teaching).

## 3. Reviewed findings (fixture-backed)

### 3a. CERTAIN (16, hand-read, 3 transcripts)

Each quote is byte-exact at paragraph + char offset in the frozen transcript; each book quote is exact at its book offset (`python3 tools/fixtures.py verify`).

| id | transcript | para @offset | transcript says | intended | leg | book slug @offset: quote |
|---|---|---|---|---|---|---|
| CF-001 | Love_Sep_2011_Part_1 | 0 @5292 | "Dilgo. Quince." | "Dilgo Khyentse." | a | discovery_of_the_presence_of_g @252198: "Dilgo Khyentse Rinpoche 575" |
| CF-002 | Love_Sep_2011_Part_1 | 0 @15635 | "Jerry Jempolski's book" | "Jerry Jampolsky's book" | b | letting_go__the_pathway_of_sur @176547: "psychiatrist Jerry Jampolsky (e.g., Love is Letting Go of Fear)" |
| CF-003 | Love_Sep_2011_Part_1 | 0 @4543 | "255% of people are happy" | "55% of people are happy" | b | reality_spirituality_and_mode @276008: "Courage 200 55" |
| CF-004 | Love_Sep_2011_Part_1 | 0 @31158 | "at the level of unquestionable love, there was no love" | "once the level of Unconditional Love was reached" | b | the_map_of_consciousness_expla @446027: "He knew that once the level of Unconditional Love was reached, the soul’s destiny after d…" |
| CF-006 | Love_Sep_2011_Part_1 | 0 @2355 | "And above which all the energies are negative. And above which all the energies are negat…" | "And above which all the energies are positive." | b | healing_and_recovery @22693: "Above level 200, one is no longer the victim because the energy field is now positive." |
| CF-007 | Love_Sep_2011_Part_1 | 0 @32832 | "Pathology and infatuation is suicide" | "Pathology in infatuation is suicide" | a | the_map_of_consciousness_expla @365505: "the difference between infatuation (cal. 145) and Love (cal. 500)" |
| CF-008 | Love_Sep_2011_Part_1 | 0 @32927 | "Judgment and infatuation is impaired" | "Judgment in infatuation is impaired" | a | the_map_of_consciousness_expla @365505: "the difference between infatuation (cal. 145) and Love (cal. 500)" |
| CF-010 | Satsang_Series_Volume_IX_Part_6 | 0 @3062 | "Given to Caesar that which is Caesar's" | "Give unto Caesar that which is Caesar's" | a | reality_spirituality_and_mode @10429: "Render unto Caesar the things which are Caesar’s" |
| CF-011 | Satsang_Series_Volume_IX_Part_6 | 0 @12766 | "Except that God loves you or he would not have created you." | "Accept that God loves you or he would not have created you." | a | — |
| CF-012 | Satsang_Series_Volume_IX_Part_6 | 0 @32406 | "We are in excelsis Deo." | "Gloria in excelsis Deo." | a | along_the_path_to_enlightenmen @2814: "Gloria in Excelsis Deo!" |
| CF-015 | A_Unique_Sedona_Seminar_Dec_2008_Part_2 | 0 @5833 | "Spiritual purity has no influence. Interest in the personal lives of students." | "Spiritual purity has no interest in the personal lives of students." | b | discovery_of_the_presence_of_g @246508: "Spiritual purity has no interest in the personal lives of aspirants" |
| CF-017 | A_Unique_Sedona_Seminar_Dec_2008_Part_2 | 0 @203 | "spiritual integrus" | "spiritually integrous" | a | discovery_of_the_presence_of_g @36073: "verifiably integrous" |
| CF-019 | Love_Sep_2011_Part_1 | 0 @4226 | "40% happiness" | "60% happiness" | b | the_map_of_consciousness_expla @148737: "200–300 8% 1.5% 60% 9.0%" |
| CF-020 | Satsang_Series_Volume_IX_Part_6 | 0 @14681 | "calibrating at 380" | "calibrating at 390" | b | truth_vs_falsehood @778891: "Enneagrams 390" |
| CF-021 | Love_Sep_2011_Part_1 | 0 @32998 | "Perception and infatuation is exaggerated" | "Perception in infatuation is exaggerated" | a | the_map_of_consciousness_expla @365505: "the difference between infatuation (cal. 145) and Love (cal. 500)" |
| CF-022 | Love_Sep_2011_Part_1 | 0 @33186 | "Productivity and infatuation is disrupted" | "Productivity in infatuation is disrupted" | a | the_map_of_consciousness_expla @365505: "the difference between infatuation (cal. 145) and Love (cal. 500)" |

Proof legs: a (acoustic near-form restores doctrinal sense); b (book contradicts the transcript); c (lecture contradicts itself). Status of all: confirmed, WORKER hand-read (TASK-002/TASK-006), independently re-verified by orchestrator and Boss. Why each is CERTAIN: `fixtures/confirmed/confirmed.json` → `evidence`.

Caveats: CF-007/008/021/022 are one repeated slide pattern (4 instances, 1 pattern; without CF-021/022 the count is 14). CF-020 is a certain text-vs-book discrepancy, but without audio the source (ASR vs the speaker misremembering) is unknown. CF-002 depends on the open owner item on other-author quotes (15 remain without it).

### 3b. Reviewed HIGH CONFIDENCE (5, withdrawn from CERTAIN in TASK-006)

| id | transcript | @offset | transcript says | intended | why not CERTAIN |
|---|---|---|---|---|---|
| CF-005 | Love_Sep_2011_Part_1 | @28028 | "It is discovered that to be loved. It is discovered that to be loved.…" | "It is discovered that to be loving is also to be lovable." | Leg a needs an ACOUSTIC NEAR-FORM replacement; 'to be loved' -> 'to be loving is also to be lovable' is a tru… |
| CF-013 | Satsang_Series_Volume_IX_Part_6 | @26352 | "Custody bills are always too, very nasty." | "Custody battles are always, too, very nasty." | Non-doctrinal Q&A (custody case). Leg a fails its doctrinal-sense half. Leg c read strictly requires the lect… |
| CF-014 | Satsang_Series_Volume_IX_Part_6 | @4906 | "He has drawn to it in addictive ways." | "He is drawn to it in addictive ways." | Non-doctrinal Q&A (a partner's media habits). Leg a fails its doctrinal-sense half; the questioner's restatem… |
| CF-016 | A_Unique_Sedona_Seminar_Dec_2008_Part_2 | @20139 | "the ego, miles away, can spot a mouse" | "the eagle, miles away, can spot a mouse" | Anecdote (wanting to be an eagle), not doctrine: restoring 'eagle' restores sense but not doctrinal sense (le… |
| CF-018 | A_Unique_Sedona_Seminar_Dec_2008_Part_2 | @6029 | "who is now left" | "who has now left" | Non-doctrinal (a teacher who left Sedona): 'has' restores grammar only (leg a half fails); no book or self-co… |

(CF-009 was withdrawn to CANDIDATE and is outside every count here.)

## 4. Error rates by class

| class | corpus-wide rate | why |
|---|---|---|
| CERTAIN | not estimable yet | reviewed denominator is 3 hand-picked transcripts; 0/230 audited |
| HIGH CONFIDENCE | not estimable yet | same; runner HIGH labels are unreviewed |
| CANDIDATE | not a rate | raw signal, precision unmeasured |
| drop-word, speaker/format | unmeasured | no detector exists |

All 0/59 clean-set figures are **in-sample, invalid as an independent FP estimate** (the detectors were tuned on those passages).

## 5. Unreviewed raw signals (CANDIDATE-class, NOT findings)

Everything in this section is automatic output that no human has reviewed. It is never blended into section 3 or 4. The runner's 2 nominal `HIGH CONFIDENCE` labels are the same errors as CERTAIN fixtures CF-003 and CF-006 (dedupe), not additional findings.

| detector | what it flags | records |
|---|---|---|
| A1-repetition | back-to-back repeated phrase loops | 938 |
| A2-nonsense | script-mix / garbled tokens, impossible percentages, U+FFFD | 158 |
| B1-contradiction | level/percentage/polarity values vs book tables | 12 |
| B2-misquote | near-verbatim book passages with divergent words | 228 |
| **total merged records** | | **1334** |

By year (from file name). Raw signals per 10k words is a *signal density*, not an error density:

| year | transcripts | words | raw records | raw / 10k words |
|---|---|---|---|---|
| 2002 | 36 | 419,510 | 282 | 6.7 |
| 2003 | 18 | 223,813 | 16 | 0.7 |
| 2004 | 16 | 252,509 | 97 | 3.8 |
| 2005 | 21 | 260,588 | 90 | 3.5 |
| 2006 | 12 | 148,199 | 57 | 3.8 |
| 2007 | 27 | 346,657 | 199 | 5.7 |
| 2008 | 22 | 239,205 | 175 | 7.3 |
| 2009 | 12 | 141,015 | 76 | 5.4 |
| 2010 | 6 | 63,422 | 52 | 8.2 |
| 2011 | 8 | 80,577 | 60 | 7.4 |
| unknown | 52 | 432,324 | 230 | 5.3 |

B2 hits concentrate in a few 2002 lectures (up to 28 per transcript); unreviewed, these may be read-aloud book passages with loose paraphrase rather than transcription errors. A2 still flags ~34 legitimate short Korean interpreter phrases in Sedona Dec 2008 Parts 1, 2, 4.

## 6. Re-review candidates (most raw signals; NOT proven hotspots)

| transcript | year | words | raw records | per detector |
|---|---|---|---|---|
| A_Unique_Sedona_Seminar_Dec_2008_Part_1 | 2008 | 12,303 | 34 | A1-repetition 8, A2-nonsense 26 |
| Causality_The_Ego_s_Foundation_Jan_2002_Part_3 | 2002 | 13,550 | 30 | A1-repetition 2, B2-misquote 28 |
| Positionality_and_Duality_Transcending_the_Opposites_Apr_2002_Part_2 | 2002 | 15,575 | 28 | B2-misquote 28 |
| The_Levels_of_Consciousness_Subjective_&_Social_Consequences_Mar_2002_Part_1 | 2002 | 15,776 | 27 | A1-repetition 2, B2-misquote 25 |
| The_Levels_of_Consciousness_Subjective_&_Social_Consequences_Mar_2002_Part_2 | 2002 | 15,762 | 26 | A1-repetition 4, A2-nonsense 1, B2-misquote 21 |
| A_Unique_Sedona_Seminar_Dec_2008_Part_4 | 2008 | 11,183 | 23 | A1-repetition 18, A2-nonsense 5 |
| The_Levels_of_Consciousness_Subjective_&_Social_Consequences_Mar_2002_Part_3 | 2002 | 12,749 | 19 | A1-repetition 3, B2-misquote 16 |
| Causality_The_Ego_s_Foundation_Jan_2002_Part_1 | 2002 | 13,305 | 18 | A1-repetition 9, B2-misquote 9 |
| Happiness_Apr_2009_Part_3 | 2009 | 11,482 | 18 | A1-repetition 14, A2-nonsense 4 |
| A_Review_of_the_Work_Sep_2007_Part_1 | 2007 | 13,820 | 17 | A1-repetition 15, A2-nonsense 2 |
| God_vs_Science_Limits_of_the_Mind_Feb_2007_Part_3 | 2007 | 12,942 | 17 | A1-repetition 15, A2-nonsense 2 |
| Question_Answer_Session_Mar_2011 | 2011 | 14,375 | 16 | A1-repetition 12, A2-nonsense 4 |
| Spiritual_Truth_vs_Spiritual_Fantasy_Jun_2006_Part_2 | 2006 | 13,617 | 16 | A1-repetition 11, A2-nonsense 5 |
| A_Unique_Sedona_Seminar_Dec_2008_Part_2 | 2008 | 5,628 | 15 | A1-repetition 8, A2-nonsense 6, B2-misquote 1 |
| Causality_The_Ego_s_Foundation_Jan_2002_Part_2 | 2002 | 12,429 | 15 | A1-repetition 3, B2-misquote 12 |

24 transcripts had zero raw signals; that does not show they are error-free (see section 1, point 3).

## 7. Pattern ledger seed

| pattern | fixtures | note | detector coverage today |
|---|---|---|---|
| P1 function-word swap on a slide table ('in' heard as 'and') | CF-007, CF-008, CF-021, CF-022 | One repeated slide (infatuation row); 4 cited instances, 1 pattern. | none |
| P2 number misheard in a book table / calibration | CF-003, CF-019, CF-020 | 255% for 55%, 40% for 60%, 380 for 390. CF-020 may be speaker misstatement (no audio). | CF-003 |
| P3 proper name rendered as English words / misspelt | CF-001, CF-002 | Dilgo 'Quince' (Khyentse), 'Jempolski' (Jampolsky). | none |
| P4 homophone / near-form of a doctrinal or scriptural phrase | CF-004, CF-010, CF-011, CF-012, CF-017 | unquestionable/unconditional, Given to/Give unto, Except/Accept, We are/Gloria, integrus/integrous. | none |
| P5 polarity flip in a doctrinal statement (inside a repeat loop) | CF-006 | 'negative' for 'positive' above level 200. | CF-006 |
| P6 sentence boundary inserted mid-phrase | CF-015 | 'no influence. Interest' for 'no interest'. | CF-015 |
| N1 NEGATIVE: Korean interpreter code-switch is not garble | NEG-001 | yes나 / no를 in Sedona Dec 2008; fixed in A2 (TASK-010). | none |

## 8. Limitations

- No detector precision measured; no human review of raw output.
- Clean-set checks are in-sample (tuned on the same 59 passages).
- M2 (family A) ACCEPTED INCOMPLETE: drop-word and speaker/format detectors never built; A4 excluded (0/16 independent recall).
- M3 (family B) not certified: terminology drift and explicit book-attribution checks unimplemented; B1 accepts any value any book states (the books contradict each other); B1/B2 calibrated in-sample; B2 cannot catch CF-004-type paraphrase errors.
- Book retrieval finds the cited book for 9/15 book-referenced fixtures.
- The 16 CERTAIN come from 3 transcripts; 4 of them are one slide pattern.
- No audio: a book contradiction proves the text is wrong, not that the ASR (rather than the speaker) caused it.
- Year is parsed from file names; 52 transcripts have no year.

## 9. Recommendations

- **Measure before extrapolating:** hand-review a random sample of raw signals per detector (e.g. 30 each) to get a first precision estimate, and hand-read a *random* sample of transcripts (not hand-picked) to get an unbiased CERTAIN/HIGH density with a confidence interval.
- **Verify every number, name and quotation** against the books before reuse; patterns P2–P4 are the commonest confirmed errors.
- **Re-transcription priority** should wait for reviewed densities; until then use section 6 only as a review queue.
- **Build the missing detectors** (drop-word, speaker/format) and a held-out clean split before any corpus-wide rate is published.

## 10. Next steps

| step | task | unlocks |
|---|---|---|
| A4 held-out FP + fix seeded-hit test | TASK-007 | A4 back into the sweep |
| B1/B2 held-out clean re-test | TASK-009 (after 007) | M3 certification path |
| M4 pattern rules + missing detectors | TASK-008 | drop-word, speaker/format coverage |
| reviewed precision sample + findings ledger | M5 (uncut) | M5 certification, real rates |
| random-sample hand-read | M5/M6 (uncut) | unbiased density |

## 11. Owner open items (unresolved, not guessed)

- Which side of the ledger the Book-of-Slides OCR files sit on: UNDECIDED; excluded here.
- Whether "misquotation" covers other authors' quotes: default applied (Hawkins' teaching plus quotes the transcript attributes to a book that contradicts it); CF-002 depends on this.

## 12. Reproduce

```
sha256sum docdocgo-fixes.zip        # 3f36c5203910...
python3 -c "import zipfile; zipfile.ZipFile('docdocgo-fixes.zip').extractall('corpus')"
python3 -m unittest discover -s tests
python3 tools/fixtures.py verify
python3 tools/sweep_m5.py --out runs/m5-raw --fresh   # ~17 min
python3 tools/report_m6.py
```
