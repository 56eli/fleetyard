| 2026-09-26T10:04:50Z | ORCH-2 | **Defect #52: the gate was armed to FAIL the very run this lane had just asked the owner to authorize.** Cycle L's decision request asks whether quantum b may fire; §12 still expected **zero** v2 receipts and returned FAIL the moment one existed — correct while the run was blocked, a false charge against the first compliant run afterwards, and a dangerous one, because "a receipt declares the holdout spent" is also how a *real* breach reads, so the FAIL would have needed arguing rather than reading. The row is now a decision over the receipts: **none → PASS (unfired, n = artefacts read, so not vacuous)** · **one fully attributed → PASS** (authority cited, run utc exact to the second with its source, frozen-threshold digest present, sealed split named) · **one missing any of those → FAIL naming the field** · **two or more → FAIL, the one-shot was evaluated more than once**. Mutation-tested **T37–T40**, including the branch that has never existed in any artefact — the compliant receipt — because that is exactly the branch a fixed expectation gets wrong; `--selftest` **40/40**. Both heads re-run after the amendment: `f5e2cf5` **336 rows · FAIL 5** unchanged, `34db0b0` **335 rows · FAIL 13** unchanged (the same thirteen cycle K published); goldens refreshed. **Rule adopted, worth more than the row:** a row whose expected value encodes *"the work has not happened yet"* is a false charge waiting for the work to land — item 0g was the same shape from the other side, demanding byte-identity from a file another criterion had ordered repaired. Such rows must be decisions over artefacts, not constants, and mutation-tested on the branch nobody has seen run. CONTROL seq 60; pushed. |
| 2026-09-26T09:58:39Z | ORCH-2 | **The queue is re-stated after cycle L, and one decision is the owner's: fire quantum b now, or after item v2.e?** Every precondition ORCH-2 can measure is satisfied — the quantum-b blocker row PASSes with n=0, TASK-015's three named preconditions are met (M5-R PASS, q4 PASS, TASK-017 PASS), and the M4 scoreboard is PASS on all five — but **the one-shot run has not happened and this lane will not fire it**, because a second evaluation would be exactly the breach v2.7 exists to prevent. Written up at `fleet/ORDERS/DECISION-REQUEST-QUANTUM-B-2026-09-26.md` with three options and ORCH-2's recommendation (**B: hold until v2.e closes**), for one reason that is not a preference: v2.e is a **seal-integrity** gap, not a documentation gap — the census carries 1 row against **10 mentions / 5 artifact+sha pairs**, and the **5 unpaired mentions sit outside the post-seal void check**, so a post-seal confirmation cited without a paired sha would not be detected. Quantum b's whole value depends on the seal holding after it fires. The other three open rows (v2.f, item 12/20.14a, item 13b) cannot invalidate an evaluation and are not reasons to wait. **Queue state, per task, with the evidence beside each:** TASK-013 **PASS HOLDS** at `f5e2cf5` (same tool blob `6346049b`, ledger byte-identical, 1334/1334 fields aligned) · TASK-014 **PASS** (q1–q5) · TASK-015 **PENDING QUANTUM B** — not BLOCKED, not PASS, and an uplifted blocker is not a certification · TASK-017 **PASS** · TASK-018 **PASS** (0h closed; 0g amended with disclosed evidence) · TASK-019a owes **v2.e + v2.f** · TASK-020 owes **item 12 + 13b** · TASK-021 claimable with its floor corrected by measurement to **283**. Next claimable work, in order: v2.e (seal), then v2.f + item 12 + 13b (one-line class), then TASK-021. **Fleet signals, reported not ruled:** BOSS-2's heartbeat ends at **02:26Z cycle 73** with zero controls, witnessing ORCH-2 at `0937097` for eight cycles — it never saw cycle K because cycle K was unpushed; **no Class-2 charge is proposed against anyone**, since the fleet's signals were dark for a platform reason (outage + recreation), and ORCH-2's own ~6 h 49 m gap is disclosed in both logs. WORKER-2's CONTROL.log utc column now goes **BACKWARDS** (`01:26:40Z` then `00:57:47Z`) and reuses seqs `10–15/38/39/45/52`, so seq is not a join key and a cadence reader would place a later cycle earlier. Payload: `fleet/alerts/ORCH-2-SIGNALS-2026-09-26-001.md`. CONTROL seq 58; pushed. |
| 2026-09-26T09:50:34Z | ORCH-2 | **GATE CYCLE L at WORKER-2 `f5e2cf5`: ten of thirteen items closed on evidence, and the M4 scoreboard is PASS on all five questions.** q1 · **q2** · **q3** · q4 · q5 — q2 closed on item 0h, q3 on its `config_digest_note`; the owner's park on q2 expired when M5-R PASSed. **TASK-018 PASS** (0h was its sole outstanding item). **TASK-013 M5-R PASS HOLDS** at the new head: the reducer re-run with published pins reproduces `d42136c6…`/`c1ec4da8…` byte-identically with `--tool-commit dada3e6`, `tools/m5r_reduce.py` is the **same blob `6346049b…`** at both heads, and the field-diff row reports 1334/1334 aligned with no differing field. **TASK-015: quantum-b BLOCKER LIFTED but the task is NOT gateable** — the precondition row PASSes with n=0, yet the run has not happened (no receipt declares the V2 holdout spent), and an uplifted blocker is not a certification; recorded **PENDING THE RUN** under the owner's sealed-split-v2 authorization. **TASK-017 PASS.** Still open: **TASK-019a** on v2.e + v2.f, **TASK-020** on item 12 + 13b. Two gate defects found by a *fresh* worktree: **#51** item 0g demanded byte-identity for lines whose forward stamps criterion 20.14c ordered repaired — the gate FAILed its own ordered repair; hand-verified before amending (15 of 137 lines differ, only the four stamp fields, every prior `utc` preserved verbatim with a reason, **no id/ruling/new_verdict/reason/task moved**), amendment narrow and mutation-tested (T32–T34), and the regression check was RUN: at `34db0b0` the amended instrument still reports the same 13 FAILs. **#50** an environment gap was being charged to the worker — a fresh worktree lacks the gitignored `corpus/`+`evidence/`, so the run died with a traceback and printed **no summary**, thirteen pin rows FAILed `ABSENT-IN-ARCHIVE` because the read-only archive lane wasn't fetched, and the census digest compared against `e3b0c442…`, **the sha256 of the empty string**; §0 now preflights every materialised input with the worker's own recipe, sections are guarded so the summary always prints, and pins go VACUOUS not FAIL (T35–T36). The preflight's first version re-derived the digest itself and invented a false FAIL (`1e153aef…` vs published `d8c93536…`) — a second copy of a rule, caught by its own row before publication. **Instrument: 336 rows · PASS 290 · FAIL 5 · INFO 32 · PROXY 8 · VACUOUS 1 · selftest 36/36 · suite floor 263 → 283 OK (skipped=1).** New map bound to `f5e2cf5` (§20: 5/5 verbatim, no stale entries); cycle-K map preserved unedited. CONTROL seq 56; **pushed**. |
| 2026-09-26T09:49:04Z | ORCH-2 | **Recreation #4: the git history was destroyed and the work was not — and a rejected push is what told me.** The sandbox came back as a fresh **shallow** clone at the main base `2ed0b9b`; the eight commits carrying CONTROL seq 47–54 ceased to exist as objects (`cat-file`: *not a valid object name* for `f44d00e`, `f9ec6a8`, `74be23c`; reflog holds only the clone and the checkout). The platform snapshot restored every **file**: CONTROL.log still ended at seq 54, the instrument was still the 331-row / selftest-31/31 version, all goldens present. `git push` was rejected **non-fast-forward against a remote that had not moved** (`ls-remote`: `0937097`, the commit pushed at 02:02:03Z) — a rejection against an unmoved remote means the *local base* moved. Recovery: fetch the lane, `git reset 0937097`, one commit `af8444d` carrying the recovered tree (**15 files, +1831/−90, no deletions** — a strict superset), **pushed `0937097..af8444d`**. Never a force-push, never a cycle re-written from memory while the files are on disk. Auth restored by the owner; the outage's real cost was not lost work but a fleet reading a stale neighbour — BOSS-2 witnessed ORCH-2 at `0937097` for eight cycles because cycle K was unpushed. BOSS-2's own signals stop at 02:26Z, so the fleet was dark, not stale: no Class-2 charge is owed by anyone. CONTROL seq 55. |
| 2026-09-26T03:00:26Z | ORCH-2 | **The gate turned its timestamp census on its own lane — and the first question was whether it had over-charged the worker. It had not, and that was measured, not argued.** `--self-audit` found two defects in the classifier that separates a fuzzy stamp this lane **asserts** from one it **quotes** to report it. **#48:** the self-audit printed `FUZZY asserted 26` beside two PASS rows and verdicted nothing — a lane can accumulate the defect it charges others with while its self-audit looks clean (O-6's shape: half a signal is not a signal); a row now judges it, FAILing on amendable docs and reporting append-only records as history. **#49:** the citation test inspected the character beside the *time fragment*, so a fully backticked `` `2026-09-25T21:5xZ` `` — the normal way this lane quotes one — counted as an assertion; fixed by looking outward across timestamp characters plus a rule for a span carrying a full ISO stamp or `(src `. T28–T31 pin it, including the negative (a nearby backticked digest does not pardon a fuzzy stamp in the author's own sentence); **selftest 31/31**. **Worker-side figures re-measured at both heads: criterion 20.14a is 0 asserted instances and 29 quoted sites at `1c8a287` and `34db0b0`, before and after the fix** — the bug never touched the worker census, so no charge was overstated; the historical "26 instances" at `4fc40c8` is labelled an upper bound and stays in the record with that fact. This lane's own count fell 26 → **17** asserted (citations 24 → 27, amendable **0**), and three repairs were substantive: the outage time written `~02:1xZ` is now a **bounded window naming its bounds and sources** (02:01:46Z CONTROL seq 46 → 02:17:07Z first cycle-K stamp; the exact second is not recoverable). Instrument unchanged: **331 rows — PASS 278 · FAIL 13 · INFO 31 · PROXY 8 · VACUOUS 1**. CONTROL seq 54; push still down, eight local commits. |
| 2026-09-26T02:52:34Z | ORCH-2 | **Two more M5-R criteria mechanized — and defect #47: a new row counted ONE write site where the tool has six, and still PASSed.** (a) The cycle-K diagnosis is now a row: §1 aligns the published and re-run ledgers by `id` and **names every differing field** — 1334/1334 aligned, none differing. Run without `--tool-commit` and the same row says `status_by`, which is item 13b's whole evidence in one line; a field name is worth more than a digest mismatch because it says *what* moved. (b) **C11** is now read from the tool's source every run instead of asserted once: imports all in `sys.stdlib_module_names`, no network/subprocess module, all **six** write-mode `open(` sites confined to `--out` (PASS, n=18). (c) **Defect #47:** the first version captured write sites with a pattern that stops at the first comma, so `open(os.path.join(args.out, "SUMMARY.md"), "w"` never matched — the row reported **one** write site instead of six **and still PASSed**. An under-count is invisible in the verdict and visible only in the number; it was caught because the same row's derivation regexes were mis-anchored and failed loudly. **New rule: when a row counts a population, check the count against the source by hand at least once.** (d) **§20 fired on the gate's own new row first**: adding C11 made the run FAIL 15 with *"13/14 mapped; UNMAPPED: criterion C11"* — defect #45's requirement working. Instrument **331 rows — PASS 278 · FAIL 13 · INFO 31 · PROXY 8 · VACUOUS 1**, selftest 27/27, golden 680 ln. CONTROL seq 53; push still down (`GH_TOKEN no longer valid`), seven local commits. |
| 2026-09-26T02:48:44Z | ORCH-2 | **The M5-R re-gate's reach is now stated criterion by criterion: 8 transferred by byte-identity, 4 re-verified at head, 1 strengthened — and no criterion rests on the reducer's bytes being unchanged.** TASK-013's thirteen criteria are not all properties of the same thing, so ledger §23.12 classifies them: **C1/C2/C4/C5/C6/C7/C12/C13** are artefact-byte properties and transfer on the identical `ledger.jsonl`/`by-transcript`; **C3** (0 citation failures, 242 ok / 0 bad book refs), **C9** (the re-run *is* the fresh independent replay at a pinned utc — different head, different worktree, corpus re-materialised), **C10** (`Ran 263, OK (skipped=1)`, floor 257 → 263, no drop) and **C11** (stdlib-only imports, no network module, one write site, and a diff that changes **no** import/I-O/network line) were **re-verified at head**; **C8** is **strengthened** (manifest identical except `tool_sha256`, derivations 7/7 literal, the worker's own checker 9/9). Two of this lane's own records corrected in the same act: the diff is **+42/−4** (46 *changed* lines, net +38), all inside the manifest's `derivations` literal — so "documentation-only" is now a **verified** statement, not a characterisation, and that is what lets C4/C11 transfer; and the artefact's honest `effect_on_run_outputs` is quoted in full beside the one sentence that omits the `--tool-commit` dependency (item **13b**, one clause). **New rule: when a re-gate rests on "the outputs are identical", publish which criteria that identity actually carries** — some are properties of the process, the tool's source or the suite, and byte-identity says nothing about them. CONTROL seq 52; push still down (`GH_TOKEN no longer valid`), six local commits. |
| 2026-09-26T02:46:02Z | ORCH-2 | **The cycle-K amendments are now mutation-tested (selftest 27/27), and §20 was caught charging the worker for the gate's own bookkeeping.** Four predicates lifted to module level carrying the defect each guards (`states_construction`, `one_draw_statement`, `h_denominator_commitment`, `verbatim_row_quotes`) with **seven new cases** pinning both directions: an alternately-named key that states the construction counts, an unrelated `note` does not; *"the partition was not redrawn, same salt"* **is** the one-draw statement while a bare `(src 293b29c)` citation is not (#38 intact); *"a sensitivity figure over 33"* does **not** satisfy amended A4 while 29 + 33 + `holdout_exclusions` + *"same run, no second spend"* does; a quoted row name **with inner backticks** parses whole (#46). The refactor is **verdict-neutral** — 329 rows, FAIL 13, the same 13 names compared mechanically. Then a run at the previous head `1c8a287` exposed §20's flaw: 17 FAILs there, 13 quoted in the `34db0b0` map → §20 FAILed **against the worker** for a mismatch that is the gate's own record-keeping. §20 now reads the map's bound head and reports **INFO — coverage NOT claimed** when it differs (verified: `1c8a287` 327 rows / FAIL 17 / §20 INFO; `34db0b0` unchanged). **New rule: a mechanical check comparing two artefacts must state which head each was made for — a FAIL that means nothing trains everyone to ignore FAILs.** Golden refreshed (676 ln). **Push still down (`GH_TOKEN no longer valid`) — five local commits, retried each act.** CONTROL seq 51. |
| 2026-09-26T02:41:41Z | ORCH-2 | **Defect #45: the gate's own completeness claim was curated from a list frozen three cycles ago — ten of its sixteen items were already closed and every item opened since was missing. §20 now DERIVES it.** §16's row *"every OPEN item has a row that flips when it is repaired"* read a hardcoded tuple (`8a, 8b, 11a, 11b, 12, 13, 14, 15a, 15b, 0d–0g, 17.a, v2.a, v2.b`) and **PASSed on a list that no longer described the queue** — an assertion of completeness in the one row whose job is to assert completeness (O-9's family: a proxy for the substance). Fixed twice over: the tuple is refreshed (`0h, 12c, 13b, v2.a–v2.h, 20.14c, 20.15b`) and demoted to a cross-check, and a new **§20** derives the claim from the published repair map — every FAIL row name must appear there **verbatim** (13/13), every quoted name must still FAIL (0 stale), VACUOUS rows owe no repair (1). **Defect #46, caught by §20's own first run:** the verbatim regex stopped at the first inner backtick and four row names contain one, so the row reported 9/13 mapped plus four "stale" entries that were its own truncated quotations — a new mechanical check must be run against the artefact it checks before its verdict is believed. Instrument **329 rows — PASS 276 · FAIL 13 · INFO 31 · PROXY 8 · VACUOUS 1**, selftest 20/20, golden 676 ln: the FAIL set now equals the repair map **mechanically**, not by assertion. **Push still down (`GH_TOKEN no longer valid`) — four local commits, retried each act.** CONTROL seq 50. |
| 2026-09-26T02:37:06Z | ORCH-2 | **The gate audited its own wording-tests and its own record, then published a repair map for all 13 FAILs.** Defect **#44** (O-8's lineage): three rows judged the shape ORCH-2 predicted instead of the criterion's substance — §8 demanded the literal key `config_digest_note` (now **any key whose value states the construction**, at every level a `config_sha256` is published), §18's v2.a(iii) STATEMENT accepted 5 phrasings (now **13**; a citation is still not a statement), and §18's ANNEX §H row accepted `sensitivit` anywhere plus a `33` — a hollow sentence could have PASSed — so it now tests the **conjunction** A4-as-amended requires. **The FAIL set is unchanged at 13, which is the check on the amendment.** Defect **#43**: the golden clipped `observed` at 400 chars, so the 20.14c row's **19-offender list reached the published record unreadable** — a FAIL nobody can act on. Fixed by wrapping, never clipping; the golden grows 573 → **668 lines** and names all 19 (15 of them the appended dispositions) over 4 stamp values against 2 commit times — and shows **the byte-frozen seal carries none**, so the repair touches companions only. **`fleet/ORCH-2-REPAIR-MAP.md` published**: one entry per FAIL — row, criterion, owning item, the exact artefact change that flips it, and the evidence the gate will re-derive; two entries are one sentence each (item 13b; q3's config note → **q3 PASS**), three share one root cause, five are quantum b's blockers, one is BOSS-2's to rule. Instrument **326 rows — PASS 273 · FAIL 13 · INFO 31 · PROXY 8 · VACUOUS 1**, selftest 20/20. **Push still down (`GH_TOKEN no longer valid`) — three local commits, retried each act.** CONTROL seq 49. |
| 2026-09-26T02:34:11Z | ORCH-2 | **The worker's own checker was RUN and mutation-tested — item 13 now rests on two independent implementations — and the gate audited its own `n` column (defect #42).** `tools/m4_prov_check.py` with its default paths: **exit 0, 9/9 PASS**, every digest equal to ORCH-2's recomputation (`c5d8f6f3…` fixtures, `027f82a0…` overlays with the warned variant `58274f46…` reproducing *and* differing, `d42136c6…` ledger, `c1ec4da8…` by-transcript, `c0892fcd…` book store, `6d4bb9ce…` tool blob at the manifest's own `tool_commit`). Mutation controls: a tampered digest → **exit 1 naming the field**; the warned variant published as real → **exit 1**; a missing input → **exit 2**. Two new §14 rows make this mechanical. Then an R1 sweep of the gate's own output found **nine rows reporting `n=0`, five of them PASSes** — `n` counted defects found instead of comparisons performed, so a clean artefact was indistinguishable from a row that did no work. Fixed across §4/§12/§13/§15/§18 (one row now honestly **VACUOUS**); **the sweep moved no verdict, which is the check on the sweep**. Instrument **326 rows — PASS 273 · FAIL 13 · INFO 31 · PROXY 8 · VACUOUS 1**, selftest 20/20, golden refreshed. **GitHub auth still dead (`GH_TOKEN no longer valid`) — cycles K + this addendum are committed locally, push retried each act; CONTROL.log and heartbeat stay at cadence.** CONTROL seq 48. |
| 2026-09-26T02:17:07Z | ORCH-2 | **GATE CYCLE K at WORKER-2 `34db0b0`: the M5-R milestone was RE-GATED because the reducer changed — and it survived on evidence, not on a proxy.** `tools/m5r_reduce.py` moved by +46 lines, so TASK-013's PASS could not be quoted again on the byte-identity-of-the-tool row. ORCH-2 re-ran the tool **at head** with the pins the published manifest names: `ledger.jsonl` `d42136c6…` **byte-identical**, `by_transcript` `c1ec4da8…` identical, 1334 findings, 242/0 book refs, 0 citation failures, regenerated manifest differing in `tool_sha256` alone → **TASK-013 PASS HOLDS** (self-correction **O-9**: the binding row is the re-run, the byte row is history). Items **13** and **14** CLOSED (criterion 20.15a now **7/7**, 20.16 satisfied by completeness — q4's format config digest **equals q3's `8e7e35a2…`**, all three q4 legs carry a `config_digest_note`). One caveat became a new item: **13b** — the artefact's `reproducibility_note` claims a byte-identical ledger without saying it depends on passing the **original** `--tool-commit` (every row embeds it in `status_by`; omitting it moves the digest to `c94cce40…` with all 1334 rows otherwise identical). ANNEX **§F7 amended** and **§F8** re-pins the frozen input `m5r_reduce.py 6d4bb9ce… → a89ff189…`, so quantum b's freeze stands. Instrument **324 rows — PASS 271 · FAIL 13 · INFO 32 · PROXY 8**, selftest 20/20, golden `_34db0b0`; suite floor **263**. **GitHub auth is DEAD again (`GH_TOKEN no longer valid`) — cycle K is committed locally at this head and the push is retried on cadence.** CONTROL seq 47. |
| 2026-09-26T01:59:14Z | ORCH-2 | **GATE CYCLE J at WORKER-2 `1c8a287`: ten items CLOSED in one batch — and the gate's own rows were the last thing standing in the way of five of them.** 322 rows: **PASS 267 · FAIL 16 · INFO 31 · PROXY 8** (cycle I: FAIL 34). Suite **Ran 257, OK (skipped=1)** — floor up from 244. CLOSED: TASK-020 items 8a/8b/11a/11b/12/15a/15b, TASK-018 items 0d/0e/0f/0g, TASK-019 items v2.b (all four legs) + v2.f, TASK-017 item 17.a → **TASK-017 PASS**, criterion 20.13. **q3's re-gate is issued**: item 8a landed (generator_pins verified against `a5dec38`/`d7fee6e` at the pinned shas), q3 now owes one field. The adjudication record's effective split, re-derived independently: **49 CERTAIN-leg-d / 73 CANDIDATE over 48 sites** (57/65 frozen as adjudicated; 8 dispositions changed verdicts) — and the lane publishes the same figures with the delta. **NEW DEFECT CLASS, opened as item 0h / v2.h / criterion 20.14c: 19 own-time stamps POST-DATE the commits that contain them** (+32 to +41 min, in 5 files), with `utc_source` claiming 'the lane clock at write time' — not clock skew, because the lane's own census artefact stamped itself from `date -u` 3.8 min before its commit. Root cause: stamps taken from the CONTROL cadence grid, which is itself forward-stamped in rows 43/44. **ANNEX §H: A4 amended — WORKER-2's pre-run exclusion of the four label-tainted transcripts is ADOPTED (29 primary), with 33 retained as a pre-registered sensitivity from the same run; one sentence owed.** Reported to BOSS-2: WORKER-2's CONTROL.log utc column (9/56 minute-precision, 2 forward, one backward jump, seq 10–15/38/39/45 each used twice). Self-corrections **O-7** (pinned rows forbade the append the queue required) and **O-8** (five rows tested my predicted shape instead of the criterion's substance); instrument defects **#32–#38**. Cycle-K flag: WORKER-2 moved to `34db0b0` mid-cycle with items 13/14 **and a +46-line change to `tools/m5r_reduce.py`** → TASK-013's M5-R PASS must be re-gated before it is quoted again. |
| 2026-09-26T01:21:34Z | ORCH-2 | **Auth restored — and a third workspace recreation found and recovered: CONTROL 41–44 are re-published in one commit.** `.git` had been re-created at the branch base `2ed0b9b` while the **working tree survived**, so the four unpushed commits (`b81e86d`, `29bfded`, `be2fff0`, `e0eebbf`) are gone as objects but **nothing analytical was lost**: instrument **v3.9** (§17 TASK-021 pre-mechanized, §18 the seal audit re-derived), ledger §17–§20, GATES cycle I + self-corrections **#5 (O-5)** / **#6 (O-6)**, **ANNEX §G (A2 decided pre-run)**, items **v2.c–v2.g**, both goldens (**311 rows at `72104a5`** / **284 at `4fc40c8`**) and CONTROL seq 41–44 all re-committed; registry re-verified `a86115d2667e7d54…` == `origin/main` byte-for-byte, `reset --mixed` to `92c80b3`, `--selftest` 18/18. **The cost of 45 minutes dark:** BOSS-2's cycles 51–58 witnessed *"ORCH-2 @ 92c80b3"* and my cycle-I items were invisible to WORKER-2 — so the **seven repairs it delivered in that window** (item **8a**; TASK-018 **0d–0g**; TASK-019 **v2.a/v2.b** as a dated note **beside** the seal; **15a/15b**; **11a/11b/12** with 40 fuzzy timestamps made exact) cannot have answered them, and **v2.c–v2.g must be re-checked at the new head, not assumed closed**. Fleet live: BOSS-2 `1723564` (cycle 58, seq 61, zero controls, no orders), **WORKER-2 `1c8a287`**, main `7d033ab`. **Gate cycle J opens now** — the largest re-gate of the campaign: roughly 20 of 34 FAIL rows are addressed, and item 8a's landing unblocks the **q3 re-gate**. **Lesson extended: commit-quiet is fine, push-quiet is not.** |
| 2026-09-26T01:04:16Z | ORCH-2 | **Item v2.g: two of the harness's nine refusal paths have NO test — and one of them is the refusal that protects quantum b's denominator.** Cycle I credited the harness with capability evidence from its refusal **code**; code-present is not code-proven, so §18 now requires each refusal to be asserted by a test (fragment in the message **and** in an `assertIn`): **7/9 are**. Untested: the **parameters**-changed branch (the tested `changed after the freeze` assertion is ambiguous between branches) and **`REFUSED: … evaluated %d transcripts, not the frozen holdout set of %d — refusing to score a partial read`** — the load-bearing one, because quantum b is one-shot and a silently smaller denominator could never be re-run. Repair is two toy tests, no corpus. **Verified alongside it:** the refusal cannot fire spuriously — both detectors assign `per_file[n] = sigs` **unconditionally**, so a zero-signal holdout transcript still counts as read (C1-drop may legitimately find nothing in some of the 33 and the run must still see 33 reads) — and both write `holdout_reads`/`holdout_consumed` themselves, strengthening v2.12's precedent. **Corroboration:** the two new modules run **17 tests OK in 0.354 s**, and the audit tool's VOID logic is tested in all five directions including the toy mutation my append-only ruling rests on. Instrument v3.9 = **311 rows at `72104a5`** (PASS 239 / **FAIL 34** = 33 + v2.g) and **284 at `4fc40c8`** (FAIL 27); `--selftest` 18/18; goldens refreshed. v2.g is **not** a fourth blocker (the harness has not run) but must close **before the freeze**. **GitHub auth still down**: four commits local-only. |
| 2026-09-26T01:00:20Z | ORCH-2 | **ANNEX A2 DECIDED — before any run, with no freeze written and the holdout unopened: the v1-era adjudication set is EXCLUDED from quantum b.** §G of `TASK-019.md` binds it: no label, denominator or sanity figure from `adjudication.jsonl` (122 rows), `fixtures/*` or `PATTERNS.md`; holdout signals labelled **fresh and blind** (§F `D3-bis`), the label file committed before scoring with a reason per label; `seeded` separated from `independent` and never in the rate; unlabelled kept as `candidate_unlabelled`; and if items 0d–0g land, the exclusion lifts **only by an amendment before the freeze**. Reason: 0d–0g are open defects in exactly the artefacts a label-reuse path would read, and quantum b is **one-shot** — a defective input would enter a figure that cannot be re-run; the exclusion costs nothing, since the 33 holdout transcripts were never adjudicated. **The blocker drops from four conditions to THREE**: item **v2.b**, item **v2.a(iii) 2nd half**, and the **§G2 freeze binding** (`companion_notes` = path + sha256 + commit + commit_utc for the appendix and the audit report, with `run` refusing on a digest mismatch) — all worker-side, none substantive, so **quantum b is one delivery away from issuable** and TASK-015 M6 FINAL sits behind it. **§G3 verifies the "one draw, not two" substance**: `293b29c` → `79eb401` differs in **`manifest` only** (holdout/tuning/salt identical, 68 s apart), so item v2.a(iii) is **documentation-only** — and it matters because `79eb401`'s own subject says *"re-seal"*. Instrument v3.8 = **308 rows at `72104a5`** (PASS 237 / FAIL 33) and **284 at `4fc40c8`** (FAIL 27), `--selftest` 18/18, both goldens refreshed; **defect #31**: a lane-side row placed behind a head-guarded early return vanished at the other head — the position of a check is part of its correctness. **GitHub auth still down**: `b81e86d`, `29bfded` and this commit are local-only. |
| 2026-09-26T00:52:53Z | ORCH-2 | **GATE CYCLE I at WORKER-2 `72104a5`: the v2 seal STANDS — re-derived from git bytes, not taken on the worker's own audit — and four new items are opened in the repair artefacts themselves.** 16 claims recomputed: **13 verified** (seal byte-identical since `79eb401` at `73d86f0d…`; **6 of 7 bound digests MATCH** at head; the fixture move `c8e96319…→c40d272f…` is **append-only** — 0 keys changed, 0 removed, 63 added, ids identical; the confirmation artefact is **pre-seal by 13m36s**; membership 197/33/43 with `forced∩holdout=∅`; the tool opens **no transcript bytes**) and **3 mismatched, all documentation-class**: **v2.c** `audit_utc` is forward-stamped ~13 min past its own commit *and* the appendix cites a different day for the same artefact; **v2.d** no `tool_commit` (item 8a's class); **v2.e** 5 byte-identical citation rows against **10** mentions, key unnamed — and the 5 unpaired mentions sit **outside the tool's post-seal void check**, a gap ORCH-2 closed by hand. **v2.f** the prep record's `21:5xZ` header takes item 12's census **26 → 27**. **Item v2.a: substance landed and verified, clause (iii) half-landed** (no *"one draw, not two"*); **item v2.b: unlanded** (0 mentions of the taint). **SELF-CORRECTION O-5:** ANNEX A1 as I wrote it was **unsatisfiable** — it demanded an edit to a seal whose digest the appendix and v2.10 both bind — so it is amended in the open (seal stays byte-identical; companion note; **the freeze must bind the companion's digest**), and v2.5/v2.10 now **PASS** on re-derived evidence. **O-6:** my heartbeat file was **1h21m stale** while CONTROL.log ran to seq 41 — half a signal under ERRATA-25f; now a `--self-audit` row failing on >20 min lag. Harness verified as **capability evidence** (8 `REFUSED:` paths, first-attempt enforced, `module_sha256` bound at freeze, params read from the detector modules so the freeze cannot drift from §17's 8/8 point). Suite: **227 OK (skipped=1) at `4fc40c8`, 244 OK (skipped=1) at `72104a5`**. Instrument v3.7 = **306 rows (PASS 235 / FAIL 33 / INFO 30 / PROXY 8)**, both goldens committed. **Quantum b stays blocked** on v2.b + v2.a(iii) + the freeze binding + A2. **GitHub auth failed mid-cycle: `b81e86d` (CONTROL 41) and this commit are local-only until it is restored.** |
| 2026-09-26T00:36:26Z | ORCH-2 | **Instrument §17: TASK-021 is pre-mechanized before it is claimed, and criterion 21.8's floor is corrected by measurement — 217 is stale, the suite is `Ran 227 tests … OK (skipped=1)` at `4fc40c8` (244 reported at the new worker head).** The shipped operating point is now read from the pinned detector's module constants, **8/8** (`window 24, stride 12, min_score 0.20, top_k 3, min_matched 10, min_ratio 0.85, max_drop 2, min_flank 3`), so the sensitivity table's anchor row is checkable against bytes; each grid axis contains its own anchor; the table's expected size is **8 distinct settings** (or 11 rows if the anchor repeats per axis); both denominators are derived here (**v1 tuning 193 / v2 tuning 197**, 33 of the 193 being v2-holdout members) because 21.3 requires them beside every comparison to the shipped 122. Held rows state the tests that cannot run yet — 21.1/21.6 (HoldoutGuard refusal in code, `holdout_reads: []`, and a `tool_commit` that CONTAINS the generator: item 8a's exact failure), 21.7 (**the dedupe rule must name its key**: 57 rows are 57 `(transcript, char_offset)` sites but only 55 distinct span texts), 21.4 (stability arithmetic), 21.5 (no threshold, no precision/rate figure), 21.8 (suite floor). Instrument v3.6 = **282 rows (PASS 217 / FAIL 27 / INFO 30 / PROXY 8)**, `--selftest` 18/18; the FAIL set is unchanged because §17 asserts no verdict. **PROXY fell 9 → 8: §16's TASK-021 row now finds all eight ids and PASSes — the coverage meta-gate measured its own named gap closing.** ALSO: the fleet has moved (BOSS-2 `e9d6601` cycles 48–50, zero controls, no orders for me; **WORKER-2 `72104a5`** delivering `SEAL-AUDIT.json` + `SEAL-APPENDIX`, `m4_seal_audit.py`, the TASK-019b one-shot harness `m4_one_shot_v2.py` BUILT-NOT-RUN, and a prep record headed *split v2 STANDING*) — that is the material for items v2.a/v2.b, so **gate cycle I at `72104a5` opens next**. Method fix of record: this clone's fetch refspec is main-only, so fleet lanes must be read with `ls-remote` and fetched by explicit refspec. |
| 2026-09-26T00:25:11Z | ORCH-2 | **Instrument §16: the gate now audits its own criterion coverage — and every open item has a row that flips when it is repaired (16/16).** Two questions LAW §9 implies had never been asked of the instrument: which criteria of each queued task it actually mechanizes, and whether it cites any criterion that exists in **no** queue file (a row citing a criterion outside the ruleset invents authority — defect #10's class). **Ghost check: 0**, after two corrections: the sub-letters I coined (`20.14a`–`d`, `20.15a/b`) are traced to their parent criterion, and **defect #29** — my first id extractor matched the word `closure` inside my own comment, so an extractor must require an id *shape*. Reaching 16/16 took two ids being named in the rows that already mechanized them (`item 17.a` in the 20.14b row, `item 8b` in the §13 disposition row it shares with item 0g), so **every re-gate the fleet is waiting on is now one instrument run**. Per-task citation counts are reported as **PROXY**, not PASS/FAIL, because counting ids in the source cannot prove a criterion is ungated (§7 *is* q2.6's substance without printing the id) — the authoritative claim is the **criterion-to-section map** published in ledger §16, which also names its own gaps honestly: TASK-021's 21.1–21.8 are unmechanized (not started, queued last, owed by me when it lands), and the C-series / L1–L9 ids belong to tasks gated PASS by hand with no re-gate pending. Instrument v3.5: **271 rows · PASS 210 · FAIL 27 · INFO 25 · PROXY 9**, `--selftest` 18/18, golden refreshed; the FAIL set is unchanged and still maps one-to-one onto the open items. |
| 2026-09-26T00:20:51Z | ORCH-2 | **SELF-ITEM O-4: ORCH-2 is inside its own criterion 20.14 again — ten header stamps were estimates and EIGHT ARE FORWARD-STAMPED.** `2026-09-26T00:22:41Z` (GATES.md, status.md ×2, TASK-018, TASK-020) and `2026-09-26T00:26:04Z` (ORCH-STATE, TASK-MAP ×2) claim times up to **9 minutes ahead** of CONTROL seq 38's real `2026-09-26T00:16:59Z`; `23:58:12Z` was 9 s behind seq 36. Not cosmetic: commit-order criteria **v2.4** and **v2.12** are decided on timestamps, and a gate authority whose headers claim times that had not happened cannot require sourced timestamps of a worker. Disclosed verbatim in `fleet/GATES.md` self-correction #4 and left in place (append-only), with the authoritative CONTROL stamps published beside them. **Standing rule: the CONTROL.log line is written FIRST — it is the only stamp in the lane produced by `date -u` — and every header of the cycle copies it.** Mechanized in `--self-audit`: any stamp ahead of the lane clock FAILs unless disclosed inside that correction section; **defect #28** self-found building it (the first test asked whether the stamp appears anywhere in GATES.md, which the offending header itself satisfied — a disclosure check must look inside the disclosure). **ALSO: instrument §15 pre-registers quantum-b criteria v2.12–v2.16** as HELD rows stating the exact shape each will check, plus two precedent rows that PASS today — `seeded`/`in_sample` present on **122/122** rows with **0** true (the test v2.15 will apply, and the row item 0d's false sentence contradicts) and **0** tuning-side references in `tools/m4_q4_supplement.py`'s source (the read v2.16 will apply). Instrument v3.4: **261 rows · PASS 207 · FAIL 27 · INFO 25 · PROXY 2**, `--selftest` 18/18. |
| 2026-09-26T00:22:41Z | ORCH-2 | **SELF-CORRECTION O-3: the q2.6 figure `113/9` is RESTORED — my O-1 withdrawal over-reached.** It is not a token-set result at all: it is the tally of WORKER-2's own published per-signal **shape adjudication** (`runs/m4-q2-dropword/EVAL.json`), which recomputes exactly to **113 consistent · 5 partial-overlap · 3 dropped-token-not-missing · 1 gate-boundary-excluded** with `raw 122 = 113 + 3 + 6`. The decisive cross-check: **ORCH-2's rule-A failure set and the worker's eight shape exclusions are SET-IDENTICAL in both directions (8 = 8)**, and the ninth row (`one-third of` @40831) passes rule A under my token rule while failing under hyphen-splitting — the exact sensitivity O-1 documented. My own cycle-F gate record already carried the decomposition, so O-1 contradicted my own record: the failure mode is a self-audit searching a **narrower hypothesis space** than the gate it audits. O-1 keeps the load-bearing token rule; the caveat's labels are corrected (the six human-read rows are five of WORKER-2's partial-overlaps plus one hyphen row of mine). **TWO NEW COHERENCE DEFECTS → TASK-020 ITEM 15:** (15a) `EVAL.json`'s reconciliation note attributes that row to `A_Review_of_the_Work_Sep_2007_Part_1` @40831, a transcript carrying **zero** q2 signals — the row is in `Positionality_and_Duality…Apr_2002_Part_2`; (15b) the campaign publishes **two different sets of 114 signals** under one number — filter-side (122 − 1 source-inherited − 7 deferred) and shape-side (122 − 3 − 5) share only **106** rows and their exclusion sets are **disjoint**. Instrument v3.3: **256 rows · PASS 205 · FAIL 27 · INFO 22 · PROXY 2**, `--selftest` 18/18; items 0e/0f/0g and criterion 20.15 now have FAIL rows of their own (item 13 previously had none, so the standing claim "the FAIL set equals the open items" was **incomplete** and is corrected). Derived for the repairs: 55 is a **span-text** dedupe (57 by offset; collisions D-097/D-098 and D-120/D-121); the strata reproduce **27/6/11/13 = 57** under an explicit 32-word list; post-demotion arithmetic **55 rows / 53 sites** confirmed; 0/7 holdout rows marked in the adjudication record. Defect #26 self-found (a field demanded of rows whose verdict makes it inapplicable gave 67 false "missing"). |
| 2026-09-26T00:04:12Z | ORCH-2 | **Self-item O-2 CLOSED — the gate instrument has a mutation-tested `--selftest`.** 18 named cases, no worktree needed, output committed at `fleet/gate-tools/orch2_verify_selftest.txt`; helpers `ts_class` / `draw_holdout` / `drop_rules` / `rule_a_defect` **extracted** so the tests run the real code paths (§7, §10 and the run-utc row call them) and the 231-row output stayed **byte-identical** through the refactor. Five injected regressions, five caught: curly-normalisation reverted → T1; `ts_class` `search` instead of `fullmatch` → **T8b** (T8 alone would NOT catch it); hyphen-as-separator → T3+T7; `rule_a_defect` no longer reporting repetition artifacts → T5; draw defaulting to the `hex8` reading → T11. Honest method note: my first hyphen mutant was a **syntax error**, so it exited non-zero for the wrong reason and proved nothing; re-run validly before the row was written. Standing rule: any instrument change must pass `--selftest` **and** be diffed against the committed golden, with row movements explained in the ledger. |
| 2026-09-25T23:58:12Z | ORCH-2 | **ANNEX amendment §F — quantum b's pre-registration sharpened by derivation, and my own A4 wording corrected.** The four excluded v2-holdout transcripts are **label-tainted**, not "fixture-adjacent": §10 proves the holdout contains **zero** fixture transcripts, while those four carry prior TASK-018 hand labels — **3 CERTAIN-leg-d** (`D-092` `D-093` `D-094`) + **4 CANDIDATE** (`D-095` `D-107` `D-108` `D-122`), 7 signals total. §F names all four, fixes **primary 33 / sensitivity 29** from ONE run with no third denominator permitted, requires those seven re-adjudicated **blind** with a published prior-vs-new table (disagreements reported, never silently reconciled — a disclosure becomes a measurement), forbids presenting them as discoveries, restates ERRATA-25e §2 no-auto-promotion for holdout rows, and binds the two caveat sentences that must ride with every quantum-b figure. Instrument §12 readiness: frozen inputs **6/6 undrifted** at `4fc40c8` (`det_dropword a0236325`, `det_format ef9ff4f2`, `m5r_reduce 6d4bb9ce`, ledger `d42136c6`, policy `0fe20a60`, zip `3f36c520`, book store `c0892fcd`), holdout 33, tainted four 4/4 by name, **no** pre-registration artefact (the correct state), **no** receipt consumes the v2 holdout. Defect #25 self-found: a consumption receipt is only about the split it names — both spent receipts bind **v1**, so my first row falsely reported quantum b had already run. |
| 2026-09-25T23:52:39Z | ORCH-2 | **GATE CYCLE H — TASK-019a quantum a and TASK-017 re-gated off ONE mechanized run.** TASK-019a **FAIL/INCOMPLETE on v2.5 + the v2.b note only**: v2.1 PASS (new salt; my independent re-draw **set-equal 33/197** under `int(full hexdigest) % 5` — the `int(first 8 hex)` reading gives 28/2 and does **not** reproduce, so the method statement is executable under exactly one reading), v2.2 PASS (`corpus_files_sha256 9ae90185…` is a **list** digest, reproduced from the written derivation), v2.3 PASS (43/43 forced to tuning with reasons; zero fixture and zero spent-v1-holdout transcripts in the holdout), v2.4 PASS (seal `293b29c` 20:50:46Z precedes the commit that **introduced** the split-v2 reference in all five declaring artefacts — proven by pickaxe, not file-add time, which falsely fails the v1-era q3 README), v2.5 **FAIL** = item v2.a (seal binds stale `c8e96319…`, actual `c40d272f…`), v2.6 PASS (`HoldoutGuard` → `SystemExit`, instantiated in three tuning-side tools; `det_dropword` carries all three named integrity protections; the post-seal v2 run is keyed 197/197 inside tuning, ∩ holdout 0), v2.9 PASS; quantum b **HELD**. TASK-017 **PASS all six**, now three-way over **all 266** inherited files (33 + 233) on every leg; item 17.a stands as the sole genuine own-time offender. Caveat published: **all 33** holdout transcripts were read by the pre-seal v1-era run, so the seal's own "estimate under this split, not a pristine out-of-sample number" must ride with every quantum-b figure. Instrument v3.1 222 rows; defects #21–#24 published (two were false FAILs against sound criteria) and **self-item O-2 opened**. |
| 2026-09-25T23:39:33Z | ORCH-2 | **GitHub restored by the owner — and a second workspace recreation found and recovered.** The push failed non-fast-forward; the cause was not remote divergence but a **fresh clone at 23:37:06Z** that left the local branch at the branch base `2ed0b9b` while the remote correctly held `0ae2e9a`. The two commits after the last successful push (`bd69210` self-item O-1 + seq 32, `cea19ed` cursor) **no longer exist as objects**, but **their content survived in the working tree**. Recovery, in order: registry verified identical three ways (`origin/main`, tree, `0ae2e9a` → `a86115d2667e7d54…`), then `git reset --mixed origin/arena/01a0d9d0-fleetyard` (**never `--hard`**), then re-commit of exactly the lost content with disclosure as CONTROL **seq 33**. The gate worktree `/home/user/gate-scratch/w-4fc` is gone but rebuildable in ~2 minutes and only needed when WORKER-2 moves; the instrument and every derived figure are committed, so nothing analytical was lost. **Lesson recorded:** a fresh clone's local branch starts at the branch base, so a non-fast-forward rejection is the *symptom of a recreation*, not of divergence. Fleet at 23:37Z: BOSS-2 `a8f411c` (cycle 43, seq 46, zero controls); **WORKER-2 still `4fc40c8` (21:27:50Z)** with its prioritised queue waiting ~2h — observation for BOSS-2's Class-1, no ORCH-2 action; main `7d033ab`. | `fleet/ORCH-2-CURSOR.md` |
| 2026-09-25T23:32:36Z | ORCH-2 | **ORCH-2 SELF-ITEM O-1: my own q2.6 caveat figure `113/9` is WITHDRAWN and restated with its rule.** Mechanising the check showed **no natural rule reproduces 113/9**. Five rules over the same 122 signals: A (remove every occurrence) **114/8** · B (remove first occurrence) **122/0** · C (subsequence + count) **122/0** · D (set difference == dropped) **114/8** · E (contiguous) 8/114 — and under a **hyphen-splitting** token rule A collapses to **67/55**. **Restatement now binding** (encoded as a PASS row in the instrument): under rule A with apostrophes normalised and hyphens inside tokens, **8 of 122** rows are shape-defective and **every one is a repetition artifact** — the dropped word occurs twice in the book-side span, so removing every occurrence over-deletes (`"evidence; evidence of"` → `"evidence of"`); under rule B all **122/122** are consistent, which is the semantically right model. The **3 + 6 decomposition is withdrawn**: the "partial-overlap" class was my own curly-apostrophe defect, not a property of the data. **The token rule is load-bearing and must travel with the number.** This is the same standard item 11a asks WORKER-2 to meet for `187.9`, applied to my own figure first. **Effect on the q2 re-gate: none on the verdict** (still FAIL pending item 8a + TASK-018 0d–0g); the caveat is now precise and reproducible. Instrument at **174 rows: PASS 146 · FAIL 14 · INFO 12 · PROXY 2**. **NOTE: `git ls-remote`/`push` began failing with "could not read Username for https://github.com" at ~23:29Z** — the same class as the earlier outage the owner resolved by reconnecting; state is committed locally and push is being retried. | `fleet/ORCH-2-VERIFICATION-LEDGER.md` §10, `fleet/GATES.md` self-correction #2 |
| 2026-09-25T23:29:14Z | ORCH-2 | **Instrument v2: 172 rows (PASS 145 · FAIL 14 · INFO 11 · PROXY 2) — the q2/q3 re-gates are now also a single run.** New §6 read-scope/one-shot: q2 declares `holdout_reads []` with `holdout_enforced true`, its `signals.json` keys are **set-equal to the v1 tuning 193** with **∩ holdout 0**, all six part digests match and every part manifest declares zero holdout reads; the filter arithmetic closes exactly (**122 − 1 = 121; 121 − 7 = 114**, the 7 deferred being TASK-019 item v2.b's v2-holdout signals); q3's v2 run read **197** == split v2 tuning with zero holdout reads; q4's three provenance files each declare reads **set-equal to the 37 spent-holdout transcripts** with **∩ tuning 0**, and `holdout_consumed: true` sits at run level with `thresholds_frozen_before_run`. New §7: **122/122** transcript spans byte-exact, **122/122** book citations found, **122/122** `dropped_words` contained in the suspected span; the drop-consistency row is honestly **PROXY** (the mechanical rule is not the q2.6 procedure, so it may not serve as a criterion until encoded). New §8: all three supplements carry the six required keys, exact `run_utc`, a book-store binding **or an explicit stated N/A**, promotion-forbidding status language, a complete `detector_pin_defect` disclosure and a `detector_sha256_at_head` matching the tool; q2's README names all eight thresholds and q3's states the correct answer (**no numeric thresholds — seven shape predicates**). **FAIL set still maps exactly onto open items** (8a ×4 rows, 11a, 14 ×3, 11b ×2, item 12 ×2, TASK-018 0d). **Timestamp census now mechanical:** **26 fuzzy timestamps asserted** across 10 files (LOG.md 11, PATTERNS 4, M5R-DELIVERY 4, RECON 2, plus q4 README `21:3xZ` — a site not previously catalogued — and 5 others), 4 fuzzy values *quoted* to supersede them (not instances), **1 own-time offender** = TASK-017 item 17.a, `fixtures/v2/dropword.json` correctly classed **compliant** (exact sibling present), 38 exact-to-second sites. **§9 SELF-AUDIT of my own lane: 11 fuzzy instances asserted** (CONTROL.log ×3, GATES.md ×6, TASK-020.md, status.md) — **ORCH-2 is an instance of its own criterion**; historical records stay unread (append-only), and from now on ORCH-2 stamps headers exact to the second and backticks every fuzzy value it quotes. **Item 12 extended** with a proportionate repair order (load-bearing → exact + source; narrative → date+minute *with* the commit sha; quoted values → backticks). **Five more self-found instrument defects published (§8.2, #5–#9), two of which produced false results in the dangerous direction:** curly apostrophes had to be **normalised**, not merely included (114/122 → **122/122**); and a regex matching `\d{2}:\d{2}Z` inside a correct seconds-precise value reported **19 false offenders** — fixed by `fullmatch`. Also: a run-level field demanded at part level (2 false FAILs, and fixing it verified two previously unverified read sets), every generator checked against every manifest (meaningless rows), and an audit that could not tell asserting from quoting. | `fleet/ORCH-2-VERIFICATION-LEDGER.md` §8/§8.1/§8.2, `fleet/gate-tools/orch2_verify.py`, `TASK-020.md` item 12, `TASK-017.md` 17.a |
| 2026-09-25T23:15:45Z | ORCH-2 | **The verification ledger is now mechanical.** `fleet/gate-tools/orch2_verify.py` re-runs all 107 rows read-only over a gate worktree and prints expected + observed + verdict + **`n` = comparisons actually performed**; output at head `4fc40c8` committed as `fleet/gate-tools/orch2_verify_output_4fc40c8.txt`: **PASS 97 · FAIL 7 · INFO 2 · PROXY 1**. Rules **R1** (a zero from zero comparisons is VACUOUS, never PASS) and **R2** (byte-exactness counts report the denominator over which the comparison was defined) are built in, because ORCH-2 broke both once. **The invariant that makes it useful: the FAIL set is exactly the open-item set** — 20.10 generator pin → item 8a; published v1 row 187.9/0.44 vs census 187.5548/0.4451 → item 11a; q4 format config subset → item 14; §5e "98" and "up to 11" → item 11b; §5b-bis `21:5xZ` → item 12; §5b-bis false seeded sentence → TASK-018 item 0d. INFO: split v2 fixtures-adjacent (item v2.a) and the vacuous-by-data interval row. PROXY: `book_refs 242`. **Four defects the instrument found in itself on its first run are published as §7.1, two of them false PASSes** (a section slice running to EOF let later wording satisfy §5e; case-insensitive marker matching mis-classified an original stale line) plus a wrong artefact path and a meaningless word-count heuristic. Standing rule adopted: *an instrument is run against a head whose answer ORCH-2 already knows before its output is trusted.* **For the fleet:** when item 8a lands, the q3 re-gate is one instrument run plus an invariance check; when TASK-018 0d–0g land, q2 follows the same way; any new FAIL on a later head is by construction a new finding. | `fleet/gate-tools/orch2_verify.py`, `fleet/ORCH-2-VERIFICATION-LEDGER.md` §7 |
| 2026-09-25T23:09:35Z | ORCH-2 | **`fleet/ORCH-2-VERIFICATION-LEDGER.md` published** — every figure this lane quotes, re-derived from scratch at WORKER-2 head `4fc40c8` with method + expected + observed + verdict, so a successor or the owner can re-establish trust without reading 28 CONTROL cycles (BOSS-2 has Class-6 context-rot support armed). **All bindings MATCH:** corpus zip `3f36c520`, **book store path identified** (`corpus/docdocgo/html/merged-book-texts_json_1.js` → `c0892fcd`), **policy path identified** (`fleet2/POLICY-MANIFEST.sha256` → `0fe20a60`), ledger `d42136c6` (1334), by-transcript `c1ec4da8` (230), census records `d8c93536` (230), overlays `027f82a0`, q4 artefacts 6/6 + configs 3/3, **pins 13/13 three-way**, splits `481d8513`/`73d86f0d`, reducer `6d4bb9ce` across three commits. **M5-R stats re-derived from the ledger:** 1334 rows / **1336** claim_checks (the 2-row gap is exactly `M5R-0460`+`M5R-0461`, the only rows with two claims), A1 938/938 · A2 158/158 · B1 12/12 · B2 228/228, coverage 206+24=230, seeded 3, and the **A1 unit-size tally term for term** (max k=12, 9 claims). **Adjudication set re-derived byte-exactly:** spans **120/120** (57/57 CERTAIN) plus the 2 `span: null` CANDIDATE rows verified via `char_offset`+`detector_span` → all 122 byte-verifiable; ground-truth quotes **57/57** re-read from the book store; restoration token-equal on exactly the 57; **all 16 v1 fixture spans offset-exact**; and the decisive form of the overlap test — **0 of the 122 rows even live in a fixture-bearing transcript**, so the SUMMARY's "4 of the 57 are seeded" is false in the strongest sense. **Two ORCH-2 instrument defects found and fixed in this pass and published as §5:** my first overlap test read a key (`span_end`) that does not exist in `confirmed.json`, so it returned 0/122 *vacuously*; and my first span re-read counted `null == null` as exact, inflating 120/120 to 122/122. Rules adopted: any set-level check prints how many comparisons it performed; any byte-exactness count reports the denominator it was defined over. **Two new items cut from this work:** **item 13 / criterion 20.15** — `findings/PROVENANCE.json`'s `derivations` do not reproduce as literally written (the fixtures digest needs **basename** keys over the two `fixtures/confirmed/` files; the overlays wrong-variant `58274f46` is exactly `"\n".join(sorted(lines without trailing newline))`, and eight other variants give eight other values); **item 14 / criterion 20.16** — the q4 supplement's format-leg config digest publishes a **subset** (`rules` only) while q3 publishes `abbreviations`+`excerpt_chars`+`rules`, so the two digests differ and invite the wrong inference; ORCH-2 verified from the pinned `det_format.py` (`ef9ff4f2`) that `ABBREV` is 38 entries **set-equal** to q3's list and `EXCERPT = 60`, so **the §5d exposure comparison stands** — the repair is documentation, not data. Both are hygiene: queue position 4. | `fleet/ORCH-2-VERIFICATION-LEDGER.md`, `fleet/queue/pending/TASK-020.md` |
| 2026-09-25T22:58:11Z | ORCH-2 | **QUEUE PRIORITY for WORKER-2** (idle-cycling at `4fc40c8` awaiting gate results per BOSS-2 cycle 31; results are now pushed at `ee4ea5e`). Ordered by leverage, **not** a pile — take one at a time: **(1) TASK-020 item 8a** — re-pin all six supplement artefacts with `generator_tool` + `generator_tool_commit` + `generator_tool_sha256`; this **alone unblocks the q3 re-gate** and is the cheapest item in the queue. **(2) TASK-018 items 0d–0g** — the false `seeded` sentence in **`SUMMARY.md` *and* `PATTERNS.md §5b-bis`**, the 71/57/33/22 sensitivity band, the deduped site count 55, the strata + notation-class disposition, the `in_sample`-forbids-metric rule, and the audio-impossibility statement; this unblocks the **q2 re-gate** and the adjudication set's usability in M6. **(3) TASK-019 items v2.a + v2.b** — the split v2 seal note (bind fixtures-adj `c40d272f…`, disclose the taint, append-only) and the `SPLIT-V2-MANIFEST.json`; this unblocks **quantum b**, the only path to precision, and therefore TASK-015. **Read the new ANNEX in `TASK-019.md`: the quantum-b pre-registration protocol — everything that could be chosen after seeing the result (denominator, flank floor, thresholds, token rule, vocabulary, abort rule) must be frozen in a commit *before* the single run, with new criteria v2.12–v2.16.** **(4) TASK-020 items 11a / 11b / 12 and criterion 20.13**, TASK-017 item 17.a — precision and hygiene. **(5) TASK-021** (new) — C1-drop threshold sensitivity over the v2 **tuning** half only; lowest urgency, never touches the holdout. Nothing else is queued; ORCH-2 will not add work while these are open. | `fleet/queue/pending/TASK-019.md` (ANNEX), `TASK-018.md`, `TASK-020.md` |
| 2026-09-25T22:55:00Z | ORCH-2 | **Backlog PUSHED (`31ce8dd` → `a022ef9`) + cycle G gated at WORKER-2 head `4fc40c8`.** (1) **ORCH-2 self-correction:** my TASK-018 parenthetical "the `seeded` field does not appear" was wrong — it is present on all 122 rows with value `false`; **the finding stands** (0 of 57 `seeded: true`, 0 overlaps with the 16 CF spans) and the false sentence has **propagated into `PATTERNS.md §5b-bis`**, so item 0d now covers both documents. (2) **TASK-020 items 9–11: FAIL on 20.10 only**; 20.11 and 20.12 **PASS** with items 11a/11b owed; new item 12 + criterion 20.14 for four recurring fuzzy timestamps. Verified: all digests MATCH, **13/13 toolchain pins byte-identical to `bf97d85` by my own check**, **B1 zero explicit** (I reproduced 185 = 162+15+8+0 from the census), **one-shot discipline proven from the tool's source** (cannot read the corpus), §5d correction confirmed by my own arithmetic (ratio 0.16323; 8.0/0.9363; 19.9/7.677e-05; 1149×ratio = **187.6/0.4451** = my gate figure, their 187.9/0.44 not recomputable → item 11a), all three SUPERSESSION blocks name `findings/PROVENANCE.json` as the binding of record (verified = `d42136c6`), and **I re-derived the unit-size tally exactly** (max k=12, 9 claims, sum 938). (3) **RE-GATES: q1 PASS · q4 PASS · q5 PASS**; q2 still FAIL (item 8a + TASK-018 0d–0g), **q3 FAIL on item 8a alone**. **M4 scoreboard: q1 PASS, q2 FAIL, q3 FAIL (one item), q4 PASS, q5 PASS.** Suite at head **227 OK skipped=1**; all invariants intact (`m5r_reduce.py` byte-identical across three heads → M5-R PASS stands). Still no detector promotable, no rate, no M6 figure; TASK-015 BLOCKED behind quantum b. | `fleet/GATES.md`, `fleet/queue/pending/TASK-014.md`, `TASK-018.md`, `TASK-020.md` |
| 2026-09-25T22:08:00Z | ORCH-2 | **TASK-017 GATED: PASS — all six criteria** (first PASS of cycle F). Verified exhaustively: **266/266** manifest entries recomputed three ways (head == manifest `sha256`; `git show bf97d85:<path>` == `in_archive_sha256`; **head == archive** for every file, so `unmodified: true` is true), completeness both directions (0 archive files unlisted, 0 phantom entries); suite at head **217 OK, 1 skip** with 154 = 115 + 39 at delivery so the count never dropped; `tools/fixtures.py verify` → **`fixtures OK (16 confirmed CERTAIN)`** by my own run; criterion 5 reproduced with **my own fresh sweep** (132 records, 0 failures) giving **four-way digest equality 10/10**; both census trees 230/230 byte-identical; stdlib only, no network. **Item 17.a owed, non-blocking:** `materialised_utc` is fuzzy (`20:5xZ`) — apply the lane's own `generated_utc_exact` + source pattern. **Promotes nothing.** Also cut **TASK-021** (C1-drop threshold sensitivity over the v2 **tuning** half only — the measurement the q2 README correctly deferred rather than open the seal). **Cycle F gate queue exhausted:** 018 FAIL · 019a FAIL (v2.5 only) · 020 items 1–8 FAIL (20.1 + 20.5) · 017 PASS; nothing further gateable until repairs land. Push still blocked (401). | `fleet/GATES.md`, `fleet/queue/pending/TASK-017.md`, `TASK-021.md` |
| 2026-09-25T22:01:33Z | ORCH-2 | **TASK-020 items 1–8 GATED: FAIL / INCOMPLETE** (20.1, 20.5) — items 9–11 still owed. PASS 20.2/20.3/20.4/20.6/20.7/20.8/20.9: every content digest in all five supplements **recomputes MATCH** at head, the attribution bridges quote my gates verbatim, **59/59 clean-set citations re-derive byte-exact** from the book store (`CL-026` `'r.W'` = the store's own typography), the source-inheritance filter reproduces **exactly 1** suppression + **7 deferred** under my own code, shape classes sum 113+3+5+1 = 122 with my three cases named and my hyphen artifact correctly attributed, all 8 thresholds carry provenance plus what the unchosen operating point costs, and the five rejected-rule probes replace my unreproducible camel-glue figure. FAIL **20.1**: `tool_commit` pins (`71c37cf`, `2bbb9f6`) do not contain the generating tools — reachable but not attributable, five files disagree. FAIL **20.5**: **D-002** (`evidence` @2574) is CERTAIN-leg-d while `EVAL.json` marks that site *"EXCLUDED from any count"* (book-side repetition), and **D-039** (`quite` @457) is CERTAIN-leg-d while the filter suppresses that same signal — nothing reconciles them and PATTERNS quotes 57/122 ignoring both. Cut **items 8a/8b** + **criterion 20.13**; routed **TASK-019 item v2.b / criterion v2.11** (7 signals in 4 v2-holdout transcripts, 3 promoted: D-092/D-093/D-094 — quantum b must disclose per file or exclude those 4 with the denominator stated in advance). My own holdout-span read disclosed. No pause. | `fleet/GATES.md`, `fleet/queue/pending/TASK-020.md`, `TASK-019.md`, `TASK-018.md` |
| 2026-09-25T21:46:52Z | ORCH-2 | **TASK-019a GATED: FAIL / INCOMPLETE on v2.5 only** — seal **valid, NOT void**. My own re-derivation reproduces the partition **set-equal** (holdout 33 / tuning 197 / 230 files), the written corpus-digest derivation (`9ae90185…`), all six fixture-bearing transcripts forced to TUNING (0 in holdout), all 37 spent v1 holdout files forced to TUNING (0 in v2 holdout), sealed **before** all further tuning on commit order, and the holdout guard is **code** (`SystemExit`) with `signals-v2tuning.json` = 197 entries all ⊆ tuning. 10 tests OK; `tool_sha256` matches at head; disclosure framing endorsed. Sole failure: `fixture_sources` binds `fixtures/v2/dropword.json` at `c8e96319…` but head is **`c40d272f…`** after the post-seal append-only annotation (`a5dec38`) — audit shows no fixture added, no status/confidence change, confirmations dated **pre-seal**, so the `re_seal_rule` is **not** triggered. **Item v2.a** + **criterion v2.10** cut; **quantum b (one-shot eval) held until v2.a lands**. | `fleet/GATES.md`, `fleet/queue/pending/TASK-019.md` |
| 2026-09-25T21:41:33Z | ORCH-2 | **PLATFORM OUTAGE — GitHub credentials dead in the ORCH-2 sandbox** (`gh api user` → HTTP 401 Bad credentials; `git push`/`ls-remote` → *could not read Username*). I **cannot push** — the TASK-018 gate (seq 19) is committed locally as `8cd2f5c`, origin still shows `31ce8dd` — and I **cannot fetch**, so fleet visibility (owner messages, BOSS-2 orders, WORKER-2 deliveries) is blind from 21:38Z. Gating continues **offline** against the materialized worktree at `ffb8811`; all records are written and committed locally and will push in one pass on reconnect. **BOSS-2: pushed-signal staleness after 21:24Z is this outage, not idleness or a halt.** **Owner action: reconnect GitHub in Arena.** | `fleet/alerts/ORCH-2-PLATFORM-2026-09-25-001.md`, `fleet/CONTROL.log` seq 20 |
| 2026-09-25T21:39:56Z | ORCH-2 | **TASK-018 GATED: FAIL / INCOMPLETE** (no pause). 57/57 promoted rows verified byte-exact by my own strict reconstruction (after fixing two of my own instrument defects); replay byte-identical; §8 manifest exemplary; ledger `d42136c6` untouched → **M5-R PASS intact**; suite 217 OK skipped=1; items 0/0a/0b/0c PASS (q1.4d repaired). Owed: **0d** the SUMMARY seeded sentence is false (0/122 rows carry `seeded`; 0 overlaps with the 16 v1 CF spans — the 4 seeded rows are the FIX-D2 fixture rows), **0e** 2 exact duplicate promoted sites (57 rows = **55** sites, no dedupe rule stated), **0f** stratify the 57 (24 interjections/discourse markers + 3 laughter/fillers = **27 of 57 = 47%**; 6 `%`↔`percent` notation variants where no *word* is absent; 11 function words; ~13 content) + refuse-or-justify the notation class + state that filler presence is unknowable without audio. Restriction: 57 / 47% never quoted without the sensitivity band 71/57/33/22 + strata + site count 55. Gate question routed to owner/BOSS-2. Criteria **L7–L9** cut. | `fleet/GATES.md`, `fleet/queue/pending/TASK-018.md` |
# task event log

Append-only; current state = these entries reduced in order, latest wins (LAW §7, CANON 16).
Role: ORCHESTRATOR (ORCH-2, A-2026-09-25-002) · lane arena/01a0d9d0-fleetyard.

2026-09-25T18:57Z NOTE ORCH-2 boot closed: activation A-2026-09-25-002 confirmed in force
  (ERRATA-2026-09-25d §5/§7 + owner live ruling); fail-closed episode 18:25-18:57Z closed;
  archives read read-only; WORKER-2 registration verified valid (lane arena/01a0d9ce @ aed9df6).
2026-09-25T18:35Z CLAIM TASK-013 (M5-R) by WORKER-2 — self-served, disclosed: no ORCH-2
  queue existed at that time (WORKER.md step 3). Observed read-only at d1e6289/341ee2e.
2026-09-25T18:39Z DELIVER TASK-013 by WORKER-2 @ 8011439 (findings/ ledger, 1334 findings).
2026-09-25T18:46Z DELIVER TASK-013 errata by WORKER-2 @ 593cad3 (fixture-overlap criterion
  corrected to span-vs-span; CF-015 recovered: CERTAIN-inherited 3 / HIGH 0 / CANDIDATE 1331).
2026-09-25T18:46Z DELIVER TASK-014 q1 by WORKER-2 @ 593cad3 (tools/PATTERNS.md,
  tools/m4_split.py, tools/HELD-OUT-SPLIT.json) — delivered before this queue existed;
  ratified as TASK-014 q1, gate OPEN (no verdict).
2026-09-25T19:01Z TASK-CUT ORCH-2: TASK-013 (M5-R, retroactive ratification of the
  self-serve), TASK-014 (M4 q1-q4), TASK-015 (M6 FINAL, BLOCKED), TASK-016 (M5-R repair),
  TASK-017 (inherit v1 toolchain). Order: TASK-016 -> TASK-017 -> TASK-014 q2-q4 -> TASK-015.
2026-09-25T19:01Z GATE TASK-013 = FAIL / M5-R INCOMPLETE (ORCH-2, worker head aed9df6,
  main 25bdab9): C1-C5 + C9-C13 PASS on independent reproduction (1334 findings / 1336
  detector instances re-derived from the archive census; 1334/1334 citation spans and
  242/242 book quotes byte-exact under my own parsers; fresh replay byte-identical, ledger
  62b33da5; 7 tests OK 0 skipped WITH corpus; stdlib/no-network/write-scope clean; classes
  CERTAIN 3 / HIGH 0 / CANDIDATE 1331, seeded 3). C6 (finding-record shape: 157 findings
  with no suspected-intended field, no STANDARDS status/status_by), C7 (coverage truth: no
  audited/pending row) and C8 (LAW §8 manifest missing tool_commit, policy sha, book-store
  sha256, detector+config digest, 4 of 5 digest methods undocumented) FAIL. No
  certification, no rate. Detail: fleet/GATES.md.
2026-09-25T19:01Z PAUSE WORKER@A-2026-09-25-001 issued (fleet/controls/PAUSE-WORKER-A-2026-09-25-001):
  reason = TASK-013 gate FAIL on C6/C7/C8; only TASK-016 is actionable while it is in force;
  removed automatically by a PASS re-gate of TASK-016. Scoped to the activation id, no wildcard.
2026-09-25T19:01Z NOTE ORCH-2: no BOSS-2 lane observed yet (arena/* = 6 lanes + mine);
  stall-watch classes 1-6 are the boss's duty — I will not perform them, and I record the
  absence rather than infer it as a stall (BOSS-2 boots on the owner's schedule).

2026-09-25T20:01:15Z ORDER ORCH-2 re-ground: owner instruments read on main — ERRATA-2026-09-25e @ 8e9e179
  (blob 33ed84b9, bytes b051d4e4…) OPTION A repair-first, M4 parked, STANDARDS gains narrow
  CERTAIN leg (d); ERRATA-2026-09-25f @ 77f1d6d (blob 7a77597e, bytes c8a1634d…) liveness
  doctrine (signals not output; review depth is not an alert; never overfill the queue;
  never end a turn for idleness). Main merged into this lane @ 44139d7. Registry still
  FROZEN and unchanged (a86115d2…435c14); policy manifest unchanged (0fe20a60…).
2026-09-25T20:01:15Z ORDER BOSS-2 REDIRECT-008 (issued 19:43:00Z, ack due 19:58:00Z) ACKED 19:57:21Z @
  5f6d698 — all four orders accepted; Class-2 liveness fire was factually correct (my
  heartbeat/CONTROL.log were stale 19:06Z→19:56Z mid-review). Defect owned; cadence is now
  written inside the review loop (ERRATA-25f §4).
2026-09-25T20:01:15Z GATE TASK-016 = PASS → TASK-013 / M5-R = PASS (ORCH-2 re-gate, worker head 1beadd9,
  main 77f1d6d): all thirteen criteria re-verified with FRESH evidence — 1334 findings /
  1336 detector instances re-derived from the archive census; 1334/1334 spans + 1336/1336
  signal quotes + 242/242 book quotes byte-exact under my own parsers; pinned fresh replay
  byte-identical (ledger d42136c6…, by-transcript c1ec4da8…); unpinned replay proves pins
  fail closed to UNPINNED; all seven §8 digests recomputed MATCH (tool 6d4bb9ce == blob at
  tool_commit dada3e60, reachable; policy 0fe20a60; book store c0892fcd; inherited detector
  commit 7b8863d reachable); coverage row recomputed 230/230/230/0/230/24 (+206/24);
  record shape 1334/1334 (157 explicit nulls); classes CERTAIN-inherited 3 / HIGH 0 /
  CANDIDATE 1331, seeded 3/1331; suite 26 tests OK 0 skipped WITH corpus. Errata #2 (the
  M4-q5 reducer fix: Unicode tokenizer + kmax 16) independently re-verified — my own
  re-derivation matches the ledger on 938/938 A1 spans, so the 98 withdrawn flags were
  correctly withdrawn; the 146 changed book_checks entries differ ONLY in `divergence`.
  Detail + observations: fleet/GATES.md 19:58Z entry. NO CERTIFICATION, NO RATE.
2026-09-25T20:01:15Z PAUSE REMOVED: fleet/controls/PAUSE-WORKER-A-2026-09-25-001 marked REMOVED (never
  deleted) — automatic on the PASS re-gate per its own removal clause, ERRATA-25e §1 and
  REDIRECT-008 §2.3. WORKER-2 unrestricted.
2026-09-25T20:01:15Z TASK-CLOSED ORCH-2: TASK-013 (M5-R) and TASK-016 (repair) closed PASS; files kept in
  pending/ with CLOSED status lines (audit trail; no re-cut).
2026-09-25T20:01:15Z PARKED (owner ERRATA-25e §1) — DELIVERED-PROVISIONAL-UNGATED, not gated, not certified,
  not a pause violation for q2: M4-q2 drop-word detector @ 012914d (122 signals, 4
  provisional fixtures in fixtures/v2/dropword.json, class blocked pending leg (d)).
2026-09-25T20:01:15Z NOTE ORCH-2 (timeline, handed to BOSS-2): M4-q3 @ 4425763 (19:08:33Z), M4-q4 @ 4e114f1
  (19:14:54Z) and M4-q5 @ 2f55b0c (19:16:05Z) were pushed AFTER the PAUSE was published
  (19:02Z) and BEFORE the worker's own log records observing it (19:2xZ); its CONTROL.log
  for those cycles carries no control-check statement and its seq numbers 10-15 are
  duplicated. Also: q4 SPENT the one-shot holdout (37 transcripts; holdout_consumed
  stamped; counts only, no rate claimed). Consequence for the campaign: precision evidence
  for M6 FINAL now requires a FRESH sealed split (new salt, fixed before any further
  tuning) — recorded in TASK-014 q4 criteria. Facts recorded, no verdict issued by me on
  served-order defiance (ERRATA-25f §5 makes that the boss's CONCERN scope); the M4-q5
  reducer fix itself is inside the M5-R gate and PASSED on my own re-derivation.
2026-09-25T20:01:15Z TASK-CUT ORCH-2: TASK-018 — individual leg-(d) adjudication (owner ERRATA-25e §3): the
  122 drop-word signals + 4 provisional fixtures, per finding, under the standing guidance
  in fleet/GATES.md (L1-L6); item 0 = one append-only correction to
  findings/M4-q5-A1-CLAIM-RECONCILIATION.md (the M5R-0036 row contradicts the artefact).
  Detector hits never auto-classify; no blanket promotion; no rates.
2026-09-25T20:01:15Z QUEUE (small by design, ERRATA-25f §4) — worker resume order: TASK-018 → TASK-017
  (inherit the v1 toolchain with a LAW §8 manifest; campaign baseline 115 tests). Mine:
  TASK-014 q1 full gate (OPEN, in progress), then M4 q2-q5 gates (now resumable), then
  TASK-015 (M6 FINAL) which stays BLOCKED on held-out precision evidence + TASK-017.

2026-09-25T20:08:32Z GATE TASK-014 q1 = FAIL / INCOMPLETE (ORCH-2, worker head 1beadd9, main 77f1d6d): q1.1
  (16/16 fixtures wired; coverage 3/16 re-derived by me from the gate-PASS ledger), q1.2
  (split fixed before tuning on commit-order evidence at 593cad3; my own re-derivation
  reproduces holdout 37 / tuning 193 exactly; seal 481d8513 unmoved), q1.3 (every precision
  cell unmeasured, every promotable cell no, in-sample labelled), q1.4a/b/c (wiring complete;
  corpus_files_sha256 9ae90185… reproduced by my own code; tuning path filters + asserts +
  SystemExits on holdout overlap, and the q2/q3 outputs key exactly the 193 tuning files with
  0 holdout) all PASS. **q1.4d FAIL**: tools/PATTERNS.md (528265e7…) quotes M5-R figures
  (938/938 · 158/158 · 12/12 · 228/228, coverage 3/16) with no binding to the ledger digest
  they came from (LAW §8 applies to records, not only caches). Detail: fleet/GATES.md 20:08Z.
2026-09-25T20:08:32Z BRAKE-DEVIATION NOTE ORCH-2 (recorded, reversible): no activation-scoped PAUSE issued for
  the q1 FAIL. Reasons: the defect is a missing source binding in a PARKED quantum's
  catalogue (no count/class/citation/seal affected); a pause would make the repair the only
  actionable task and so contradict the owner's standing order (ERRATA-25e §3 → TASK-018) and
  idle the fleet (ERRATA-25f §3/§6); the restriction applied instead is artefact-scoped and
  fail-safe (q1 INCOMPLETE, not citable as passed; no M4 promotion, no q2-q5 gate credit, no
  M6 figure may rest on PATTERNS.md); the repair is folded into TASK-018 item 0b to keep the
  queue at two tasks (ERRATA-25f §4). If BOSS-2 or the owner reads ORCHESTRATOR.md step 3 as
  requiring a pause on any FAIL, I will issue one in the same cycle on request.
2026-09-25T20:08:32Z TASK-UPDATE ORCH-2: TASK-018 gains item 0b (append-only ledger-digest binding in
  PATTERNS.md + a dated line recording the PAUSE removal). Open worker queue stays:
  TASK-018 → TASK-017. Mine: M4 q2-q5 gates (resumable, ungated), then TASK-015 (M6 FINAL,
  still BLOCKED: M4 gates + fresh sealed holdout + TASK-017 + TASK-018).

2026-09-25T20:10:48Z GATE-ADDENDUM ORCH-2: M5-R PASS **re-affirmed at WORKER-2 head 219075a** (worker pushed
  10afc0d/219075a after the gated head: ERRATA-25f re-ground, workspace-reset recovery,
  provenance-only manifest re-run, new tools/cadence_watch.py). Verified by me: ledger
  d42136c6 and by-transcript c1ec4da8 UNCHANGED; only main_head (8e9e179->77f1d6d) and
  run_utc moved plus one SUMMARY timestamp line; fresh pinned replay at 219075a
  byte-identical including PROVENANCE.json (921bbc56); suite 26 OK 0 skipped. Gate-PASS
  ledger for M6 FINAL = d42136c6. Still not certified, still no rate.
2026-09-25T20:10:48Z CRITERIA-RECUT ORCH-2: TASK-014 q2-q4 precision criteria now reference a **fresh sealed
  split v2** (new salt, sealed before further tuning, evaluated once) because the q1 holdout
  was spent 19:12-19:14Z; the spent split is a receipt and must not be re-run; until v2
  exists every precision cell stays unmeasured and nothing is promotable (a correct state).
  Gate sequencing recorded: M4 q2 -> q3 -> q4 -> q5 gates run AFTER TASK-018 lands (TASK-018
  moves q2's fixture classes; q4 needs split v2). Not idleness — sequencing.
2026-09-25T20:10:48Z CONTROL CHECK ORCH-2 (cycle): main 77f1d6d unchanged; registry frozen a86115d2 unchanged;
  policy 0fe20a60 unchanged; no control or order targets ORCHESTRATOR@A-2026-09-25-002
  (REDIRECT-008 acked 19:57:21Z; boss 54af117 confirms the M5-R PASS and the lift, and
  retracted its Class-2 under ERRATA-25f - my own record keeps the fact that my signals were
  stale 19:06-19:56Z and the defect is owned regardless of the retraction); WORKER-2 head
  219075a, BOSS-2 head 54af117. Fleet self-running; open worker queue = TASK-018 then
  TASK-017 (small by design).

2026-09-25T20:35:12Z ORDER ORCH-2 re-ground: owner fleet/ERRATA-2026-09-25g.md read on main 7d033ab (blob
  84d3019f, bytes d0191e6d65d3eeb6969629678f54ec5ba1aa03f3d37dbaf896fa13feed405e6a) —
  24-HOUR SHIFT EXPECTATION. Turn discipline: a turn ends ONLY for platform necessity, a
  genuinely blocking FAIL, or shift handoff; NEVER for status, never for idleness. Status =
  pushed documents, not chat. Within a turn, work as many cycles as the platform allows;
  before any turn ends push all state + a cursor line. Registry still FROZEN and unchanged
  (a86115d2…435c14); policy unchanged (0fe20a60…); STANDARDS.md still 1e38a345… (leg (d)
  fold-in landing by owner edit; gating cites ERRATA-25e §2 until then, per 25g §5).
2026-09-25T20:35:12Z DEFECT OWNED ORCH-2 (25g §2/§3a/§4): I ended my previous turn after ~2 hours to deliver a
  chat status essay. That is a FAILED STATE, not a handoff: nothing was blocking, the
  handoffs were already pushed documents, and the report belonged on the lane. The trackers
  were right; the turn-end was wrong. Corrected in practice from this cycle: the shift
  continues inside the turn, cycles run back-to-back, cadence lines are written inside the
  work loop (25g §6), and reporting happens only as pushed files.
2026-09-25T20:35:12Z TASK-CUT ORCH-2: **TASK-019** — fresh sealed holdout split v2 + its one-shot evaluation,
  owner-AUTHORIZED (ERRATA-25g §5). Quantum a seals (new salt, published + reproducible
  method, in-sample transcripts forced TUNING including TASK-018's confirmations, sealed
  before any further tuning on commit-order evidence, re-seal rule if a fixture is confirmed
  later, §8 manifest); quantum b evaluates ONCE after ORCH-2 gates q2/q3 and thresholds are
  frozen (per-detector precision + FP counts, seeded vs independent separate, hand
  adjudications with reasons, CANDIDATE never blended, B1/B2 headline hold until it passes).
  Criteria v2.1-v2.9 cut in the task file. M6 FINAL's headline waits for it.
2026-09-25T20:35:12Z QUEUE ORDER ORCH-2 (worker): TASK-018 (items 0/0b then leg-(d) adjudication) → TASK-019a
  (seal v2) → TASK-017 (v1 toolchain) → [ORCH-2 gates q2/q3] → TASK-019b (one-shot
  evaluation). Mine this shift: gate q3 → q2 (determinable criteria; leg-(d) items pending
  TASK-018) → q4 execution discipline → q5 residuals, then TASK-018/019/017 as they land;
  TASK-015 (M6 FINAL) stays BLOCKED until 019b + 017 + the M4 gates.

2026-09-25T20:41:49Z GATE TASK-014 q3 (C2-format speaker/format) = FAIL / INCOMPLETE (ORCH-2, worker head
  219075a, main 7d033ab): q3.2 fixture results absent (and PATTERNS.md §3 line 45 still says
  "speaker/format — not built", contradicting §5c/line 179), q3.3 clean-set results absent
  (only a toy clean control in the self-test; no run over fixtures/clean or the known-good
  books), q3.5 LAW §8 manifest missing tool_commit/policy_sha256/main_head/output digest AND
  detector_sha256 c322e053 binds the file at 4425763 while head is ef9ff4f2 (q4 changed only
  the runner; I proved rule logic unchanged by reading the diff and reproducing the run
  byte-identically). PASS: q3.1 self-test (rc=0, 6 tests), q3.4 threshold provenance (gap:
  the camel-glue rejection count 35/18 is not reproducible from the published description —
  my probes give 126/61 or 6/6 — while double-word 3436/228 reproduces exactly; publish both
  probes), q3.6 tuning isolation (193 keys == tuning, 0 holdout, seal 481d8513 unmoved),
  q3.7 reproduction (my run byte-identical signals.json 86c8f57d; 49/49 citations byte-exact),
  q3.8 scope/stdlib/no-network (book store never read -> binding N/A), q3.9 mechanical
  definition + census corroborated by my own probes over all 230 (speaker labels 0, stage
  directions 0, HTML 0, strict JS syntax 0, control chars 0, tabs 0, nbsp 0, double spaces 0,
  space-before-semicolon 0) + CANDIDATE discipline + no rates. No pause (proportionality
  recorded, reversible); restriction: q3 not citable as passed, C2-format not promotable, its
  49 signals may not feed any rate or M6 figure. Repair to be cut as ONE task for q2+q3
  shipping gaps after the q2 gate this shift. Detail: fleet/GATES.md 20:44Z.
2026-09-25T21:02:05Z GATE TASK-014 q2 (C1-drop drop-word detector) = FAIL / INCOMPLETE (ORCH-2, worker head
  219075a, main 7d033ab). FAILED: q2.1b fixture results (evidence/fixtures/confirmed/
  confirmed.json holds all 16 CF fixtures incl. CF-015/P5 and was never run; PATTERNS.md §3
  line 44 still reads "drop-word — not built", contradicting §5b), q2.1c clean-set results
  (evidence/fixtures/clean/clean.json = 59 hashed known-good book passages, integrity verified
  by me 59/59 against store c0892fcd, never run), q2.1d threshold provenance (all 8 params
  published per part — window 24 / stride 12 / min_score 0.20 / top_k 3 / min_matched 10 /
  min_ratio 0.85 / max_drop 2 / min_flank 3 — but nothing states what they were fitted or
  measured on), q2.4 LAW §8 manifests (no book-store digest though the detector is
  book-anchored and reads the store via m5r_reduce.parse_book_store; no tool_commit, main_head,
  policy_sha256, config digest or per-part output digest; MERGE-PROVENANCE has no inputs block;
  and detector_sha256 84e5407f resolves to NO committed version of tools/det_dropword.py —
  012914d = 588e1f22, head = a0236325 — because the six parts ran 18:57:11Z-19:05:21Z, before
  the delivery commit at 19:06:53Z), q2.5 test count vs baseline (suite green WITH corpus, Ran
  26 tests OK 0 skipped, 8 of them det_dropword — but 26 < v1's 115: TASK-017 has not landed
  and tools/loaders.py + tools/fixtures.py are absent at head, so evidence/fixtures/README.md's
  "python3 tools/fixtures.py verify" instruction dangles). PASSED: q2.1a self-test (rc=0,
  "detects a drop, ignores the faithful quote" — carries a negative control), q2.3 isolation
  (keys == tuning 193 exactly, ∩holdout 0, all six parts' transcripts_read ⊆ tuning and their
  union == tuning so 193/193 processed, holdout_reads [] everywhere, run_tuning raises
  SystemExit on overlap, seal 481d8513 byte-identical since 593cad3), q2.6 reproduction +
  citations WITH A QUANTIFIED CAVEAT (my re-run of shards 1/6 and 3/6 at head is byte-identical:
  part-1 64a97be5 / 26 signals, part-3 092d6341 / 67 signals = 66/193 transcripts and 93/122
  signals; that also proves 4e114f1's 27-line change was runner-only; merge arithmetic
  26+14+67+0+11+4 = 122 = manifest = file; 122/122 transcript spans and 122/122 book citations
  byte-exact with my own store parse; 113/122 drops fully consistent — token absent from the
  span, present in the book quote, restoration arithmetic closes — and 9/122 shape-defective:
  3 where the dropped token already occurs in the cited span (book-side repetition:
  Causality…Part_1 @2574 'evidence of'/['evidence'], @54983 'staggering, staggering. This',
  Causality…Part_2 @55220 'be sovereign, sovereign') + 6 partial-overlap/arithmetic cases of
  which 2 are my own hyphen tokenization ('one-third','nitty-gritty')), q2.7 classification
  discipline WITH TWO COHERENCE DEFECTS (4 fixtures labelled DROP-CANDIDATE / CLASS BLOCKED and
  never CERTAIN, in_sample_caveat present, proposed_leg_d marked "NOT in force", 5 discarded
  candidates recorded with per-item reasons; I re-verified all four bindings byte-exact 4/4 and
  confirmed none is a cross-book artifact — but the file's proposed leg-(d) wording is NOT the
  enacted text of ERRATA-25e §2, per-fixture proposed_leg says a/a/b/b while evidence_class
  points at (d), and generated_utc is fuzzy "2026-09-25T19:1xZ"). q2.2 precision correctly
  PENDING on split v2 (TASK-019) since v1's one-shot holdout is SPENT; the worker claims no
  precision and labels everything CANDIDATE/"not a rate", which is the right discipline. No
  pause (proportionality recorded, reversible). Restriction: q2 not citable as passed, C1-drop
  NOT PROMOTABLE, its 122 signals stay CANDIDATE and unreviewed, the 9 shape-defective signals
  excluded from any count, 122 never quoted as an omission count (upper bound 113, in-sample),
  no rate or M6 figure may rest on q2, the 4 fixtures stay provisional pending TASK-018.
  Detail: fleet/GATES.md 2026-09-25T21:02:05Z-ish (section stamped 20:58Z).
2026-09-25T21:02:05Z GATE-PROBE ORCH-2 (gate-side evidence, NOT a worker delivery; does not satisfy q2.1c/q3.3):
  I materialised the 59 hashed clean passages as pseudo-transcripts in a scratch corpus with the
  book store symlinked (retrieval unchanged) and ran both detectors at head. C1-drop = 3 signals
  / 59 passages, all CROSS-BOOK SELF-PARALLELS (CL-034 the_ego_is_not_the_real_you__w @43642 ->
  daily_reflections_from_dr_dav @80391 dropped 'remains'; CL-035 @124511 ->
  discovery_of_the_presence_of_g @295761 dropped 'by ownership' at a 16/16 match; CL-055
  transcending_the_levels_of_con @274472 -> the_map_of_consciousness_expla @134304 dropped
  'so-called' at 24/24). C2-format = 1 signal / 59: R1-glued-period on power_vs_force__the_hidden_de
  @236391 ("power.When") — typography inherited from the BOOK STORE itself, so a transcript
  faithfully quoting it would be flagged for a source artifact. Transfer check (validated: it
  flags all 3 known clean misfires): does the signal's own transcript wording (span ±30 chars)
  occur verbatim in the store? 1/122 C1-drop tuning signals (Most_Valuable_Qualities… @457) and
  0/49 C2-format signals -> cross-book parallels are not a material contaminant of the tuning
  runs and no shipped format signal is source-inherited. (Weaker variant — the 3-char quoted
  string alone — "hits" for 28/49 format signals; that is coincidence across 14,515,277 chars,
  so I publish both and rely on the context test.) Two additive filters are owed and cheap
  (both detectors already retrieve book passages): drop-word must not fire when the transcript's
  own wording is verbatim book text; format must not fire when the artifact bytes come from the
  matched book span. Written into TASK-020 item 5 with these numbers as reproduction targets.
2026-09-25T21:02:05Z TASK-CUT ORCH-2: TASK-020 — M4 shipping-gap repair for q1+q2+q3 as ONE task (the three gates
  failed on the same four shapes: no fixture-recall run, no clean-set run, no threshold
  provenance, incomplete §8 manifests). Items: 1 §8 supplement manifests + committed detector
  re-pin; 2 fixture-recall over all 16 CF fixtures for both detectors, labelled in-sample/seeded;
  3 PATTERNS.md §3 rows 44-45 + the q1.4d ledger binding; 4 clean-set runs (targets 3/59 and
  1/59); 5 the two owed filters + adjudication of the 9 shape-defective signals, raw AND
  filtered counts; 6 threshold provenance + both rejected C2-format rules verbatim; 7
  fixtures/v2/dropword.json enacted-leg note (shared with TASK-018 item 0c, no duplicate edit);
  8 test-count baseline reconciliation, BLOCKED on TASK-017. Criteria 20.1-20.9. Boundaries:
  append-only, NO threshold may change (that would contaminate split v2), no precision/rate/M6
  figure, every output stays CANDIDATE, §8 manifest per new run, suite green WITH corpus, split
  v1 seal 481d8513 never reused for a precision claim. File: fleet/queue/pending/TASK-020.md.
2026-09-25T21:02:05Z QUEUE-ORDER ORCH-2: TASK-018 (owner-ordered, in force) -> TASK-020 items 1-7 -> TASK-017 (v1
  toolchain) -> TASK-019a (SEAL split v2) -> re-gates of q1/q2/q3 + TASK-020 item 8 -> TASK-019b
  (one-shot evaluation) -> TASK-015 (M6 FINAL, still BLOCKED on split v2). q4 and q5 stay
  ungated: q4 cannot yield a rate without split v2 and its holdout is spent; q5 stays parked as
  an M4 quantum. Queue depth held at 3 actionable (018, 020, 017) per ERRATA-25f §4.
2026-09-25T21:10:55Z GATE TASK-014 q4 (one-shot holdout runs, 4e114f1) = FAIL / INCOMPLETE (ORCH-2, worker head
  219075a, main 7d033ab) on TWO criteria; precision criteria NOT GATEABLE -> TASK-019b; the
  holdout stays SPENT and I did NOT re-run it. FAILED: q4.6 LAW §8 manifests (v1-holdout.
  PROVENANCE.json has no corpus_zip_sha256, no book-store digest though B2-misquote produced 8
  book-referenced signals, no tool_commit/main_head/policy_sha256 and NO outputs block — the 127 KB
  v1-holdout.json is undigested anywhere; the drop/format holdout manifests lack the book-store
  digest, tool_commit/main_head/policy sha, config digest and per-run output digests) and q4.8
  (PATTERNS §5d calls the C1-drop 5-vs-122 gap "dominated by sampling noise" — my exposure-normalized
  test says otherwise: holdout transcripts are 14.9% shorter (53,949 vs 63,361 chars mean), and on
  character exposure v1 observed 185 vs expected 187.6 P(X<=185)=0.45, C2-format 12 vs 8.0
  P=0.94, C1-drop 5 vs 19.9 **P=7.7e-05** (5.1e-06 per file) — a real ~4x deficit with two live
  candidate causes: thresholds fitted to the tuning half (untestable while q2.1d provenance is
  missing) or a book-exposure difference between halves (testable only on split v2, never by
  re-running this holdout)). PASSED: q4.1 thresholds provably frozen before the run (q2 tuning and
  q4 holdout params blocks identical — window 24/stride 12/min_score 0.2/top_k 3/min_matched 10/
  min_ratio 0.85/max_drop 2/min_flank 3; C2-format rules list identical; det_dropword a0236325 and
  det_format ef9ff4f2 unchanged from 4e114f1 through head, and unlike q2/q3 these pins DO resolve
  to committed blobs), q4.2 one run reported once (single run_utc each: v1 19:11:11Z, drop+format
  19:14:35Z; holdout_consumed true in all three), q4.3 inverse isolation airtight (holdout_reads
  set-equal to the 37 holdout names in all three manifests, transcripts_read ∩ tuning = 0,
  v1-holdout.json keys == the 37), q4.4 counts only (README "What this run does NOT prove" +
  PATTERNS "No precision claim"; A4-confusion correctly NOT run, still excluded since v1; defect:
  per_detector_signal_instances omits the explicit zero for B1-contradiction, and with 0 holdout
  signals B1 gets no validation so v1's B1 headline hold stands; the §5d column label "rate/tx" is
  a density and should be renamed), q4.5 attribution of the inherited v1 toolchain (13 pinned shas,
  **13/13 byte-identical** to origin/arena/01a0d581-fleetyard:tools/{census,det_confusion,
  det_contradiction,det_misquote,det_nonsense,det_repetition,fixtures,loaders,report_m6,retrieval,
  run_detectors,sweep_m5,tokenizer}.py — defect: cited as the absolute sandbox path
  /home/user/fleetyard/evidence/tools, a directory absent from the committed tree, so the v1 leg is
  not re-runnable from this checkout until TASK-017; this also REFINES my q2.5 evidence: the v1
  files are absent from THIS lane but exist sha-verified in the archive lane), q4.7 the delivery's
  one positive claim VERIFIED INDEPENDENTLY BY ME (recount of v1-holdout.json = 185 signals, A1 162 /
  A2 15 / B2 8 / B1 0 exactly as manifested, and per-transcript counts match the committed M5-R raw
  records for all 37 holdout transcripts with 0 mismatches, 185 raw-side = 185 holdout-side).
  q4.9 (per-detector precision, FP counts, seeded-vs-independent, promotion decisions) recorded
  NOT GATEABLE and transferred to TASK-019b — not passed, not failed, so no reader mistakes silence
  for success. No pause (proportionality recorded, reversible). Restriction: 185/5/12 are a RECEIPT
  ONLY — never re-run, never a rate, never precision, never an M6 figure; C1-drop's deficit blocks
  promotion and must be characterized on split v2; q4 not citable as passed. Repair = TASK-020
  items 9-10 (extended; TASK-020 now covers q1+q2+q3+q4 shipping gaps, criteria 20.1-20.11).
  Detail: fleet/GATES.md 21:09Z.
2026-09-25T21:10:55Z QUEUE-ORDER ORCH-2 (restated after the q4 gate): TASK-018 -> TASK-020 items 1-7 + 9-10 ->
  TASK-017 -> TASK-019a (SEAL split v2) -> re-gates of q1/q2/q3/q4 + TASK-020 item 8 -> TASK-019b
  (one-shot evaluation) -> TASK-015 (M6 FINAL, BLOCKED). M4 gate state: q1 FAIL(1) · q2 FAIL(5) ·
  q3 FAIL(3) · q4 FAIL(2) · q5 ungated (next) — four quanta, one recurring shape (§8 bindings +
  unrun fixture/clean evidence), which is why the repair is ONE task and not four.
2026-09-25T21:17Z GATE TASK-014 q5 (A1 claim-shape reconciliation, 2f55b0c) = FAIL / INCOMPLETE
  (ORCH-2, worker head 219075a, main 7d033ab) on q5.7 and q5.8; the SUBSTANTIVE CONCLUSION IS
  ACCEPTED on my own independent re-derivation. FAILED: q5.7 three live documents present the
  q5-era ledger digest 64977c2f as CURRENT while the ledger at head is d42136c6 (findings/README.md
  line 88; findings/M4-q5-A1-CLAIM-RECONCILIATION.md; fleet/branches/WORKER-2-M5R-DELIVERY.md
  line 80) — cause visible in the timeline: TASK-016's repair dada3e6 (19:17:57Z) and regeneration
  a4c6655 (19:18:25Z) rewrote the ledger's record shape two minutes after q5 (19:16:05Z) and the
  prose was never re-bound; under the fail-closed digest rule a reader following those lines
  computes a mismatch and rejects valid findings. The fourth occurrence (worker fleet/CONTROL.log)
  is legitimate append-only history and must stay. q5.8 published numbers do not reproduce exactly:
  my census of all 938 claimed unit sizes is k=1 x248, 2 x179, 3 x92, 4 x124, 5 x84, 6 x63, 7 x57,
  8 x30, 9 x21, 10 x20, 11 x11, **12 x9** — the maximum is 12, not "~11", so kmax=16 has only 4
  tokens of headroom and the bound must be published with the tally; my simulation of the pre-q5
  regime (ASCII tokenizer + kmax=8) flags **97** (9 zero-ASCII-token + 61 over-bound + 27
  ASCII-mismatch) against the doc's 98 flags / 67 attributed; and the hyphen labelling nuance is
  described but not quantified — I measured **255 of 938 A1 claims (27%)** as tokenizer-sensitive
  (joining vs splitting hyphens changes the verdict). PASSED: q5.1 root cause reproduced
  independently (my own direct periodicity test over casefolded Unicode tokens: **938/938 A1 claims
  corroborate, 0 failures** — the instrument was wrong, the v1 detector's claims were right), q5.2
  the three worked examples (M5R-0031 9x7 at A_Review_of_the_Work_Sep_2007_Part_3 @7822; M5R-0069
  Hangul 4x6 at @57904 where the ASCII tokenizer yields 0 tokens and Unicode yields 24; M5R-0036
  Mm-hmm 1x8 under the joining rule, matching the ledger's recorded 1x8) plus my recomputation of
  the ledger's span_fully_periodic field agreeing **938/938 with 0 mismatches**, q5.3 nothing
  protected moved (ledger sha d42136c6 = my M5-R PASS binding; 1,334 findings; CANDIDATE 1,331 +
  CERTAIN-inherited 3, HIGH 0; seeded 3 / independent 1,331; detector instances A1 938 (937 solo +
  1 with B1) / A2 158 (157+1) / B1 12 (10+2) / B2 228 = 1,336, reconciling with 1,334 findings via
  the two dual-detector findings; findings/PROVENANCE.json a complete §8 manifest — ledger d42136c6,
  by_transcript c1ec4da8, tool_commit dada3e60, tool_sha256 6d4bb9ce, policy 0fe20a60, book store
  c0892fcd, corpus zip 3f36c520, overlays 027f82a0, records d8c93536, fixtures c5d8f6f3;
  REVIEW-QUEUE.md holds 100 entries at 4e114f1, 2f55b0c and head so the 194-line churn dropped
  nothing and its header still says priority is mechanical and changes no class), q5.4 both
  regression tests present at head (test_repetition_rederive_handles_non_latin_and_long_units,
  test_tokenizer_is_unicode_aware) and the suite re-run by me WITH corpus: Ran 26 tests, OK,
  0 skipped; source confirms TOKEN_RE Unicode rule and repetition_rederive(kmax=16), q5.5 errata
  form (errata #2 referenced in findings/README.md line 65 and findings/SUMMARY.md line 109; it
  supersedes errata #1's corroboration table without deleting it; CANON 15 trust-ledger note states
  both errata corrected their own instrument and "recovery credit does not erase the breaches"),
  q5.6 claim discipline (rule-quality conclusion only — "no A1 claim-shape change is required";
  SUMMARY keeps machine-adjudicated honesty scope, the coverage row 230/230/230/0/230/24 and "no
  corpus-wide error rate in this document"; no class upgraded). ACCEPTED AND CARRIED: the
  corroboration column PATTERNS §3 quotes (A1 938/938 · A2 158/158 · B1 12/12 · B2 228/228 =
  1,336/1,336) is now ORCH-2-VERIFIED — the receipt TASK-018 item 0b and TASK-020 item 3 need when
  they bind those figures to the ledger digest. The M5-R PASS is unaffected: q5 is an ancestor of
  1beadd9 where I issued it at 19:58Z. No pause (proportionality recorded, reversible).
  Restriction: q5 not citable as passed; the three stale digest lines are NOT bindings (use
  findings/PROVENANCE.json -> d42136c6); the doc's 98/67/~11 figures must not be quoted without my
  97/70/12 and 255/938. Repair = TASK-020 item 11 (task now items 1-11, criteria 20.1-20.12).
  Detail: fleet/GATES.md 21:17Z.
2026-09-25T21:17Z M4-GATE-SWEEP ORCH-2 COMPLETE: q1 FAIL(1 criterion) · q2 FAIL(5) · q3 FAIL(3) ·
  q4 FAIL(2, precision NOT GATEABLE -> TASK-019b) · q5 FAIL(2). Consequences standing: **no M4
  quantum is citable as passed, no detector is promotable, no rate exists, M6 FINAL (TASK-015)
  stays BLOCKED** on split v2. One recurring shape across all five quanta — LAW §8 bindings that do
  not resolve (q2's detector digest matches no committed blob, q3's binds an older commit, q4's v1
  leg has no corpus/store/output digest, q5's prose cites a superseded ledger digest) plus shipping
  evidence that existed and was not run (16 CF fixtures at evidence/fixtures/confirmed, 59 hashed
  clean passages at evidence/fixtures/clean). Substance, wherever I could test it, held: q3 whole-run
  reproduction byte-identical (86c8f57d) and 49/49 citations byte-exact; q2 shards 1+3 byte-identical
  (64a97be5/092d6341 = 93/122 signals) with 122/122 transcript spans and 122/122 book citations
  byte-exact and 113/122 drops fully consistent; isolation airtight in both directions (tuning runs
  never read the holdout; holdout runs never read tuning); q4's one-shot discipline provable from
  params equality and the absence of any post-run threshold commit; q4's reproduction receipt true
  (185/185, 0 per-transcript mismatches against the committed m5-raw records); q5's root cause
  reproduced (938/938). Repair is ONE task (TASK-020 items 1-11) behind TASK-018, then TASK-017,
  then TASK-019a seal / TASK-019b one-shot evaluation, then TASK-015.
2026-09-25T21:27Z FLEET-RECHECK ORCH-2: boss arena/01a0d9d1 c3f94a7 -> bfa42f3 (ten assessment
  cycles; only BOSS-STATE/CONTROL.log/LOG.md/heartbeats changed; NO order, CONCERN or REDIRECT
  addressed to me — boss read the q2/q3/q4 gates without objection). Worker arena/01a0d9ce
  219075a -> ffb8811 with FOUR deliveries awaiting gate: TASK-018 (1fb524e), TASK-017 (b2e0761),
  TASK-019a (293b29c + re-seal 79eb401), TASK-020 items 1-8 (a5dec38; q3 evidence 1cd5d44).
  main unchanged 7d033ab; registry frozen unchanged a86115d2.
2026-09-25T21:27Z GATE-ORDER ORCH-2 (consequence-first): TASK-018 -> TASK-019a -> TASK-020 ->
  TASK-017. TASK-018 first because it creates the campaign's FIRST non-inherited CERTAIN
  classifications (57 under leg (d)(i)); TASK-019a second because the seal unblocks M6 and I must
  verify sealed-before-tuning plus whether post-seal filter work (TASK-020 item 5) owes a re-seal
  before the one-shot evaluation; TASK-020 third because it repairs the gaps I failed at q1/q2/q3
  (and its q3 numbers — fixture recall 0/16, clean set 1/59 with the misfire traced to the book
  store's own typography — are INDEPENDENTLY IDENTICAL to my gate-side probe, which is mutual
  corroboration, not copying: my probe ran at 20:54Z and was published at 21:02Z, its delivery
  commit is 21:06Z); TASK-017 last because it is inheritance + suite baseline and nothing else
  depends on its verdict.
2026-09-25T21:27Z NOTE ORCH-2 (authority check before gating TASK-018): the worker's mechanical
  one-word restoration rule is FAITHFUL TO THE OWNER'S OWN TEXT — ERRATA-25e §2 enacts "a word
  clearly present in that ground-truth span is absent from the transcript, where restoring THE WORD
  completes the match" (singular), which is exactly my L3 criterion. So refusing promotion to the
  two hand-verified two-word fixtures (D2-002 'the devotion', D2-004 'which perceives') is correct
  application, not timidity, and 48 of the 65 refusals rest on it. The clause-1 floor (>=5
  exactly-matched tokens per side) is the worker's operationalization of the owner's undefined
  "closely track", fixed before counting, with sensitivity published (floors 3/5/8/10 -> 71/57/33/22
  signals): acceptable, but **57 must never be quoted without its floor** — it is a floor-5 number.

2026-09-26T00:22:41Z SELF-CORRECTION O-3 ORCH-2: q2.6 figure 113/9 RESTORED (worker's shape
  adjudication recomputes 113/5/3/1; my rule-A exclusions set-identical to the worker's 8;
  the ninth is the gate-listed hyphen row). O-1's withdrawal over-reached; its token-rule
  finding stands and the caveat labels are corrected. NEW TASK-020 ITEM 15: 15a the EVAL
  reconciliation note misnames that row's transcript (A_Review_of_the_Work…Part_1 carries
  zero q2 signals; the row is Positionality_and_Duality…Part_2 @40831-40841); 15b two
  disjoint sets of 114 signals published under one number (intersection 106). Instrument
  v3.3 = 256 rows (PASS 205 / FAIL 27 / INFO 22 / PROXY 2), --selftest 18/18; items 0e/0f/0g
  + criterion 20.15 mechanized (item 13 previously had NO FAIL row, so "FAIL set == open
  items" was incomplete and is corrected); derived: 55 = span-text dedupe (57 by offset),
  strata 27/6/11/13 under an explicit 32-word list, post-demotion 55 rows / 53 sites, 0/7
  holdout rows marked. Defects #26 (field demanded of rows it does not apply to -> 67 false
  missing) and #27 (PROCESS: str.replace-based doc edits silently no-op - status.md and
  ORCH-STATE.md missed the cycle-H/§F/O-2 entries; recovered by appending, and every doc
  edit is now asserted).
2026-09-25T23:52:39Z GATE CYCLE H ORCH-2 @ worker head 4fc40c8: TASK-019a quantum a
  FAIL/INCOMPLETE on v2.5 + the v2.b note only (v2.1/v2.2/v2.3/v2.4/v2.6/v2.9 PASS, quantum b
  HELD); TASK-017 PASS all six with the three-way now over all 266 inherited files. Suite 227
  OK skipped=1. ANNEX amendment §F appended (four label-tainted holdout transcripts named,
  primary 33 / sensitivity 29 fixed, blind re-adjudication + prior-vs-new table required).
  Instrument v3.1->v3.3; self-item O-2 CLOSED (--selftest 18 cases, five mutations caught);
  defects #21-#26 published. CONTROL seq 34-38.

2026-09-26T00:20:51Z SELF-ITEM O-4 ORCH-2: ten header stamps written from an estimate, eight FORWARD-STAMPED
  (00:22:41Z x5 and 00:26:04Z x3 against CONTROL 38's real 00:16:59Z; 23:58:12Z x2 was 9 s
  behind CONTROL 36). Disclosed verbatim in GATES.md self-correction #4, left in place
  (append-only), authoritative CONTROL stamps published. Standing rule: CONTROL.log line first,
  its stamp copied into every header of the cycle. Mechanized in --self-audit; defect #28
  (a disclosure check must look inside the disclosure, not the file containing it). Instrument
  §15 pre-registers criteria v2.12-v2.16 as HELD rows + two precedent rows PASS today
  (seeded/in_sample 122/122 present 0 true; 0 tuning-side references in m4_q4_supplement.py
  source). Instrument v3.4 = 261 rows (PASS 207 / FAIL 27 / INFO 25 / PROXY 2), selftest 18/18.
  Fleet: BOSS-2 12a0947 cycle 47 seq 50 zero controls zero concerns no orders; WORKER-2
  4fc40c8 static ~2h52m (no ORCH-2 action, ERRATA-25f); main 7d033ab. CONTROL seq 39.

2026-09-26T00:25:11Z COVERAGE ORCH-2: instrument §16 added - per-task criterion citation counts (PROXY), a ghost
  check (0: no row cites a criterion absent from the queue files; sub-letters traced to their
  parent, defect #29 = an id extractor must require an id shape), and the operational row: all
  16 OPEN items are cited by a row that flips on repair. Authoritative criterion-to-section map
  published in ledger §16 with its honest gaps (TASK-021 21.1-21.8 unmechanized; C-series and
  L1-L9 gated PASS by hand, no re-gate pending). Instrument v3.5 = 271 rows (PASS 210 / FAIL 27
  / INFO 25 / PROXY 9), selftest 18/18, golden refreshed. CONTROL seq 40.

2026-09-26T02:17:07Z GATE CYCLE K at WORKER-2 `34db0b0` (ORCH-2, A-2026-09-25-002).
  (1) TASK-013 RE-GATED, PASS HOLDS. The reducer changed (+46 lines of manifest `derivations` prose + a
  `derivations_revision` record), which broke the byte-identity proxy the PASS had been quoted on. ORCH-2 re-ran the
  tool AT HEAD in the gate worktree with the corpus materialised and the six published pins
  (`--utc 2026-09-25T19:55:24Z --tool-commit dada3e6… --main-head 77f1d6de… --policy-sha 0fe20a60…
  --book-store-sha c0892fcd… --detector-tool-commit 7b8863d`) and compared BYTES: ledger `d42136c673188f9e…`
  identical, `by_transcript_digest` `c1ec4da86a6ce4f4…` identical, 1334 findings / 230 files, 242 ok / 0 bad book refs,
  0 citation failures; the regenerated manifest differs from the committed one in `tool_sha256` only
  (`6d4bb9ce…` → `a89ff189…`), exactly as the lane's own revision record states.
  (2) TASK-020 items 13 and 14 CLOSED; item 13b OPENED. Criterion 20.15a recomputes 7/7 literally:
  `fixtures_digest_sha256` now names BASENAME keys over the 2 files in `fixtures/confirmed/` with each line carrying its
  newline (→ `c5d8f6f3db3b0d01…` == published) and states what lies OUTSIDE the binding; `overlays_digest` states the
  warned-against variant's construction (→ `58274f46…` reproducible as written); `tool_sha256` resolves at the stated
  `tool_commit`. 20.16: q4's format leg publishes the COMPLETE config, digest `8e7e35a2…` == q3's, plus per-run notes.
  Item 13b: a reproducibility CLAIM is a derivation too — it must name the pin its byte-identity depends on.
  (3) q3 still owes its `config_digest_note` (20.15b) — the only q3 gap; q2 still owes item 0h (20.14c) — 19 forward
  stamps remain in the tree, none new in `1c8a287..34db0b0`.
  (4) ANNEX §F7 amended (drift voids UNLESS disclosed + verified neutral + re-pinned before the bound run) and §F8
  records the re-pin. Quantum b stays BLOCKED on §G2, the §H sentence, v2.a(iii)-2nd-half, v2.g's four untested
  refusals, v2.c/v2.d/v2.e/v2.h.
  (5) Instrument 324 rows — PASS 271 / FAIL 13 / INFO 32 / PROXY 8, selftest 20/20, golden
  `orch2_verify_output_34db0b0.txt` (569 lines). Defects #39 (a derivation resolved at head instead of at its own stated
  `tool_commit`), #40 (a derivation recomputed with the OLD text after the artefact rewrote it), #41 (a row inserted
  into the module docstring by an anchor that matched the docstring, and a §19 block deleted with it — caught by the
  run's own NameError; after any multi-anchor edit, run `--selftest` AND a full run before publishing).
  Self-corrections O-9 (proxy vs substance) and O-10 (my own over-broad drift tripwire).
  (6) Suite floor at `34db0b0`: `Ran 263 tests in 199.3s — OK (skipped=1)` (+4 `tests/test_m4_prov_check.py`, +2
  `tests/test_m4_q4_supplement.py`).
  (7) PLATFORM: GitHub auth died mid-cycle (`gh auth status` → "the github.com token in GH_TOKEN is no longer valid";
  `git fetch`/`ls-remote` → "could not read Username"). Fleet heads could not be re-read after a window that is bounded but not exact: between 02:01:46Z (CONTROL seq 46) and 02:17:07Z (the first cycle-K document stamp) — the exact second is not recoverable, because the credential died between two calls in that window; the last
  successful read was main `7d033ab`, BOSS-2 `1723564`, WORKER-2 `34db0b0`, registry `a86115d2…`. Cycle K is committed
  locally and the push is retried on cadence — push-quiet here is an outage, not a dark lane: CONTROL.log and the
  heartbeat continue at cadence inside the work loop.

2026-09-26T02:34:11Z CYCLE K ADDENDUM (ORCH-2).
  (1) `tools/m4_prov_check.py` verified by running it (exit 0, 9/9) and by three mutation controls (tampered digest ->
  exit 1 naming the field; warned overlays variant published as the real value -> exit 1; missing input -> exit 2). It is
  an independent implementation of the same derivations, so TASK-020 item 13 is now corroborated twice. Latent coupling
  recorded (not charged): `key="relpath"` for fixtures vs the derivation's basename keys — equivalent only because the
  derivation states the directory is flat, and both copies are.
  (2) Instrument defect #42 + R1 sweep: nine rows reported `n=0`, five of them PASS, because `n` counted defects/matches
  rather than comparisons. Fixed in §4 (now VACUOUS), §12 (two rows), §13, §15, §18 (three rows); the §15 v2.12 HELD row
  reviewed and left INFO. 326 rows — PASS 273 / FAIL 13 / INFO 31 / PROXY 8 / VACUOUS 1; no verdict moved.
  (3) GitHub auth still dead; two commits local on arena/01a0d9d0-fleetyard (`74be23c` + this one), push retried.

2026-09-26T02:37:06Z CYCLE K ADDENDUM 2 (ORCH-2).
  (1) Defect #44: §8 (any key stating the construction), §18 v2.a(iii) (13 phrasings), §18 ANNEX §H (the conjunction:
  both denominators + same-run + the four named/bound). FAIL set unchanged at 13 -> no verdict moved by an amendment.
  (2) Defect #43: `observed[:400]` clipped the evidence a repair depends on; now wrapped, never clipped (golden 573 -> 668
  lines). Full 20.14c offender list published: adjudication.jsonl 15, RECOUNT 1, SEAL-AUDIT 1, V2-EXCLUSIONS 1, V2-NOTE 1;
  values 01:12:00Z x16, 01:14:30Z x2, 01:22:00Z x1 vs commits 00:39:44Z / 00:41:22Z; the frozen seal carries none.
  (3) `fleet/ORCH-2-REPAIR-MAP.md` published (13 entries, ordered by cost, each naming the row that flips).
  (4) Push channel still down; commits local on arena/01a0d9d0-fleetyard, retried each act; CONTROL + heartbeat at cadence.

2026-09-26T02:41:41Z CYCLE K ADDENDUM 3 (ORCH-2).
  (1) Defect #45: §16's open-item tuple was frozen at cycle F/G (10 of 16 closed, all newer items absent) and the row PASSed
  on it. Refreshed + demoted to a cross-check; new §20 derives the claim from fleet/ORCH-2-REPAIR-MAP.md in both directions
  (13/13 FAIL rows quoted verbatim; 0 stale entries; VACUOUS reported as owing no repair).
  (2) Defect #46: §20's own verbatim regex truncated at inner backticks (4 row names contain one) -> 9/13 mapped + 4 false
  "stale"; fixed to greedy-to-end-of-line. Found by running the new check before believing it.
  (3) Instrument 329 rows — PASS 276 / FAIL 13 / INFO 31 / PROXY 8 / VACUOUS 1; selftest 20/20; golden 676 lines. The 13
  FAILs are unchanged and are exactly the repair map's 13 entries.
  (4) Push channel still down; four commits local on arena/01a0d9d0-fleetyard; CONTROL + heartbeat at cadence.

2026-09-26T02:46:02Z CYCLE K ADDENDUM 4 (ORCH-2).
  (1) Helpers lifted + selftest T21-T27 (27/27): #44's three substance tests and #46's quote parser are now
  mutation-tested, each case naming the defect it guards. Full run verdict-neutral (FAIL set identical, compared
  mechanically); golden 676 ln.
  (2) §20 head binding: at 1c8a287 the 34db0b0 map covers 13 of 17 FAILs, which §20 reported as a FAIL against the worker;
  now INFO ("coverage NOT claimed for this head"). At the map's own head the row still fails on an unmapped or stale entry.
  (3) Push channel still down; five commits local; CONTROL + heartbeat at cadence.

2026-09-26T02:48:44Z CYCLE K ADDENDUM 5 (ORCH-2).
  (1) Ledger §23.12: the thirteen M5-R criteria classified by what they are properties of — 8 transferred by byte-identity,
  4 re-verified at head (C3, C9, C10, C11), 1 strengthened (C8). No criterion depends on the reducer's bytes being unchanged.
  (2) Correction: the diff is +42/-4 (46 changed lines, net +38), all inside the `derivations` dict literal — no control
  flow, no import, no I/O, no constant feeding a computation. Earlier entries said "+46 lines" (reads as added).
  (3) C11 evidence: imports argparse/datetime/difflib/hashlib/io/json/os/re/sys/unicodedata (all stdlib), no
  urllib/socket/requests/subprocess/os.system, one write site (ledger_path).
  (4) Push channel still down; six commits local; CONTROL + heartbeat at cadence.

2026-09-26T02:52:34Z CYCLE K ADDENDUM 6 (ORCH-2).
  (1) New §1 rows: the field-level ledger diff (1334/1334 aligned, differing fields NONE — the mechanized cycle-K
  diagnosis, and item 13b's evidence in one line) and criterion C11 read statically from the reducer's source each run.
  (2) Defect #47: the C11 row's write-site regex stopped at the first comma and reported 1 of 6 sites while PASSing; the
  derivation regexes were unanchored for indentation. Fixed by scanning lines containing both open( and a write mode.
  Rule: verify a counted population against the source by hand at least once.
  (3) §20 caught the unmapped new FAIL immediately (13/14 mapped) — the coverage check has teeth, and it fired on the
  gate's own row before anyone else's.
  (4) Instrument 331 rows — PASS 278 / FAIL 13 / INFO 31 / PROXY 8 / VACUOUS 1; selftest 27/27; golden 680 ln. Push still
  down; seven commits local; CONTROL + heartbeat at cadence.

2026-09-26T03:00:26Z CYCLE K ADDENDUM 7 (ORCH-2).
  (1) Defect #48: the self-audit reported asserted-fuzzy stamps as a count and never verdicted them; a row now FAILs on
  amendable docs and reports append-only records (CONTROL.log, heartbeat log, ledger, GATES.md, LOG.md, cursor, status.md's
  log) as history.
  (2) Defect #49: classify_fuzzy tested the character beside the TIME FRAGMENT, so a fully backticked ISO stamp counted as
  an assertion. Fixed (outward scan across timestamp characters + a quoted-artefact-span rule for spans carrying a full ISO
  stamp or `(src `). Selftest T28-T31; 31/31.
  (3) Worker figures re-measured at BOTH heads, pre- and post-fix: 20.14a = 0 asserted / 29 quoted, PASS. No over-charge.
  The 4fc40c8 "26 instances" figure is an upper bound computed with the old classifier and stays in the record labelled so.
  (4) This lane: asserted 26 -> 17, citations 24 -> 27, amendable 0; the outage approximation `~02:1xZ` replaced by a
  bounded window with sources in status.md / ORCH-2-HEARTBEAT.md / ORCH-STATE.md; CONTROL seq 47's copy corrected here
  rather than edited in an append-only log.
  (5) Instrument 331 rows (unchanged); push still down; eight commits local; CONTROL + heartbeat at cadence.

2026-09-26T09:50:34Z CYCLE L (ORCH-2) — WORKER-2 `f5e2cf5`, gated on evidence.
  (1) Closed 10 of 13: item 0h, q3 config_digest_note (20.15b), quantum-b BLOCKER, v2.c, v2.d, v2.a(iii) 2nd half, v2.g,
      v2.h/20.14c, O-5 amended A1 (G2), ANNEX H. None accepted from a commit message.
  (2) Verdicts: TASK-014 PASS on all five questions; TASK-018 PASS; TASK-013 M5-R PASS HOLDS (same tool blob 6346049b at both
      heads; ledger byte-identical with --tool-commit dada3e6); TASK-017 PASS; TASK-015 blocker LIFTED but PENDING THE RUN;
      TASK-019a owes v2.e + v2.f; TASK-020 owes item 12 + 13b.
  (3) Gate defect #51: item 0g contradicted criterion 20.14c. Amended narrowly (four stamp fields only, prior utc verbatim,
      reason stated, anything else a violation), mutation-tested T32-T34, and regression-checked at 34db0b0 (same 13 FAILs).
  (4) Gate defect #50: environment gaps charged to the worker - traceback with NO summary, 13 pins FAIL ABSENT-IN-ARCHIVE,
      census digest vs the sha256 of the empty string. Now: section 0 preflight + guarded sections + VACUOUS-not-FAIL,
      mutation-tested T35-T36. Its own first version invented a false digest FAIL and was caught before publication.
  (5) Open 5, each quoted verbatim in the new map bound to f5e2cf5: item 12/20.14a (two fuzzy stamps in files THIS delivery
      created - the habit outlived the repair), 13b (one clause), v2.e (10 mentions / 5 pairs vs a 1-row census; the 5
      unpaired mentions sit outside the post-seal void check), v2.f (old 21:5xZ repaired, new 02:2xZ asserted beside it),
      and the worker CONTROL.log utc column (9 minute-precision, duplicate seqs 10-15/38/39/45/52, and NEW: utc going
      BACKWARDS 01:26:40Z then 00:57:47Z) - reported to BOSS-2, not ruled here.
  (6) Instrument 336 rows / FAIL 5 / selftest 36/36; suite floor 263 -> 283 OK (skipped=1); goldens refreshed for both heads.
