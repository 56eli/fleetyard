# ORCH-2 CURSOR — recovery state for the next turn

Append-only. Each block is a turn-end cursor: where the lane stands, what is unpushed, and the exact next actions.

---

## Cursor 2026-09-25T23:34:01Z — GitHub token invalid; one commit unpushed; cycle G complete up to self-item O-1

**Platform state (diagnosed, not guessed).** `gh auth status` reports verbatim: *"github.com: authentication failed —
The github.com token in `GH_TOKEN` is no longer valid."* Every network git operation fails with
`fatal: could not read Username for 'https://github.com': terminal prompts disabled`. Four push attempts and one
`ls-remote` failed between 23:29Z and 23:33Z. **Owner action needed: reconnect GitHub in Arena.** This is the same
failure class as the outage earlier this shift (which the owner resolved by reconnecting); `remote.origin.fetch` is
still the known main-only quirk, so after any restore use
`git fetch origin '+refs/heads/*:refs/remotes/origin/*'`.

**Lane state.**
- **Confirmed remote head: `0ae2e9a`** (`git ls-remote` succeeded at 23:29:16Z) — instrument v2, 172 rows.
- **Local head: `bd69210`** (23:32:36Z) — *self-item O-1: the q2.6 caveat `113/9` withdrawn and restated with its
  rule*, plus CONTROL seq 32. **UNPUSHED.** Plus this cursor commit, also unpushed.
- Local `origin/...` remote-tracking refs are **stale** (the fetch failed), so `git log origin/<lane>..HEAD` overstates
  the unpushed set (it lists `53c235e` and `0ae2e9a`, both confirmed pushed). Trust `ls-remote`, not the local ref.
- Fleet last read 23:29Z: WORKER-2 **`4fc40c8`** (committed 21:27:50Z, static ~2h — recorded as an observation for
  BOSS-2's Class-1 assessment, no action taken by ORCH-2); BOSS-2 **`22fcb8c`** (cycle 39, seq 42, **zero controls,
  zero CONCERNs**); main **`7d033ab`** (ERRATA-25g).

**Where the work stands (all committed locally, most also pushed).**
- **M4 scoreboard: q1 PASS · q2 FAIL/INCOMPLETE · q3 FAIL/INCOMPLETE (item 8a alone) · q4 PASS · q5 PASS.**
- TASK-020 items 9–11: **FAIL on 20.10 only**; 20.11 PASS (item 11a owed), 20.12 PASS (item 11b owed).
- Open items across the queue, in the published priority order: **8a** (re-pin six supplement artefacts with
  `generator_tool` + `generator_tool_commit` + `generator_tool_sha256`; alone unblocks the q3 re-gate) →
  **TASK-018 0d–0g** (0d now covers `SUMMARY.md` *and* `PATTERNS.md §5b-bis`) → **TASK-019 v2.a/v2.b** (unblocks
  quantum b, whose **pre-registration protocol is a binding ANNEX of `TASK-019.md`** with new criteria v2.12–v2.16) →
  **11a / 11b / 12 (extended: 26 asserted fuzzy sites; 1 own-time offender = TASK-017 17.a) / 13 / 14 + criteria
  20.13–20.16** → **TASK-021**.
- **Gate instrument `fleet/gate-tools/orch2_verify.py`: 174 rows — PASS 146 · FAIL 14 · INFO 12 · PROXY 2** at
  `4fc40c8`, output committed. **The FAIL set maps exactly onto the open items** (8a ×4, 11a, 14 ×3, 11b ×2, item 12
  ×2, TASK-018 0d). Nine self-found instrument defects are published (§7.1 #1–#4, §8.2 #5–#9), two of them false
  PASSes. Rules R1/R2 encoded. Self-audit of my own lane: 11 asserted fuzzy timestamps → ORCH-2 is an instance of
  criterion 20.14.
- **Two ORCH-2 self-corrections recorded append-only in `fleet/GATES.md`:** (#1) the `seeded` key *is* present on all
  122 adjudication rows with value `false` — my "field does not appear" parenthetical was wrong, the finding stands;
  (#2) the q2.6 caveat `113/9` is **withdrawn** — restated as rule A **8/122 shape-defective, all repetition
  artifacts**, rule B **122/122**, hyphen-splitting 67/55, so the token rule must travel with the number.
- Invariants at `4fc40c8` (all re-derived): ledger `d42136c6…` (1334), by-transcript `c1ec4da8…` (230), census
  records `d8c93536…` (230), overlays `027f82a0…`, book store `c0892fcd…` at
  `corpus/docdocgo/html/merged-book-texts_json_1.js`, policy `0fe20a60…` at `fleet2/POLICY-MANIFEST.sha256`,
  `m5r_reduce.py` `6d4bb9ce…` identical at three commits (**M5-R PASS stands**), splits `481d8513…`/`73d86f0d…`,
  pins **13/13 three-way**, suite **227 OK skipped=1**.
- Restrictions unchanged: no detector promotable, no precision, no rate, no M6 figure; 122 + 48 signals
  CANDIDATE/PROVISIONAL-UNGATED; the 57 CERTAIN-leg-d rows restricted (band 71/57/33/22, strata, site count 55,
  notation class); B1 unvalidated by the receipt; the spent v1 holdout is never re-run; TASK-015 M6-Final BLOCKED
  behind quantum b; **M6-P owner-accepted and NOT re-certified**.
- Gate worktree **`/home/user/gate-scratch/w-4fc`** is warm at `4fc40c8` with the corpus materialized (230 overlays,
  230 census records) — reuse it; do not rebuild unless the head moves.

**Exact next actions once GitHub is reconnected.**
1. `git push origin arena/01a0d9d0-fleetyard` (pushes `bd69210` + this cursor commit); verify with
   `git ls-remote origin arena/01a0d9d0-fleetyard`.
2. `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`; read BOSS-2's LOG/CONTROL for any order (boss orders
   first) and WORKER-2's head.
3. If WORKER-2 has landed **item 8a**: re-run the instrument on the new head — the four generator rows must clear — and
   issue the **q3 re-gate** (everything q3 needs is already verified).
4. If **TASK-018 0d–0g** have landed: re-run and issue the **q2 re-gate** with the restated q2.6 caveat (rule A, 8/122,
   all repetition artifacts).
5. If **TASK-019 v2.a/v2.b** have landed: gate split v2 (criterion v2.5) and then check the **pre-registration commit
   precedes any run commit** (v2.12) before quantum b is allowed to start.
6. CONTROL seq 33 + heartbeat at cadence; keep committing every cycle so an outage never costs more than one commit.

---

## Cursor 2026-09-25T23:39:33Z — GitHub restored by the owner; a SECOND workspace recreation found and recovered

**Owner reconnected GitHub at ~23:36Z.** The push then failed non-fast-forward, and the diagnosis was not a divergent
remote: the **workspace had been recreated again** — `git reflog` shows a fresh `clone: from
https://github.com/56eli/fleetyard.git` at **23:37:06Z** followed by `checkout: moving from main to
arena/01a0d9d0-fleetyard`, leaving the local branch at the **branch base `2ed0b9b`** while
`origin/arena/01a0d9d0-fleetyard` correctly held `0ae2e9a`.

**Loss:** the two commits made after the last successful push — `bd69210` (self-item O-1 + CONTROL seq 32) and
`cea19ed` (the cursor above) — **no longer exist as objects** (`git cat-file -t` fails for both; reflog and
`git fsck --lost-found` are empty). **Their content survived in the working tree**, which the recreation preserved.

**Recovery executed (the documented pattern, in order):**
1. **Registry integrity first, three ways:** `origin/main`, the working tree and `0ae2e9a` all hash to
   `a86115d2667e7d54ff418524…` — the frozen registry was never disturbed.
2. `git reset --mixed origin/arena/01a0d9d0-fleetyard` (**never `--hard`**) → HEAD = `0ae2e9a`, working tree untouched.
3. The residual diff was exactly the lost commits' content: `fleet/CONTROL.log` (seq 32), `CONTROL.md`, `GATES.md`
   (self-correction #2), `ORCH-2-VERIFICATION-LEDGER.md` (§10), `ORCH-STATE.md`, `gate-tools/orch2_verify.py` (the
   five-rule table + the stated criterion + observed-value printing), its committed output, heartbeats, `status.md`,
   and the new `ORCH-2-CURSOR.md`. `TASK-020.md` item 12 (extended) and `TASK-017.md` item 17.a were already inside
   `0ae2e9a`, which is why they did not appear as modified.
4. Re-committed with this disclosure, CONTROL **seq 33**, and pushed.

**Also lost: the gate worktree `/home/user/gate-scratch/w-4fc`** (corpus + evidence materialization). It is rebuildable
in about two minutes with `git worktree add` + `sh tools/m5r_inputs.sh` and is **only** needed when a new WORKER-2 head
lands; the instrument and every derived figure are committed, so nothing analytical was lost.

**Standing lesson recorded for the next recreation:** the local branch of a fresh clone starts at the *branch base*, not
at the remote lane head, so a non-fast-forward push rejection is the *symptom* of a recreation, not of remote
divergence. First move is always `git log --oneline -3 HEAD` plus `git rev-parse origin/<lane>`; second is the registry
check; third is `--mixed` to the remote head. Never `--hard`, never force-push the lane.


---

## Cursor at CONTROL seq 44 (2026-09-26T01:04:16Z) — LOCAL-ONLY STATE, push channel down

**Read this first on resumption.** GitHub authentication failed mid-cycle at ~00:37Z (`gh auth status`: *"The github.com
token in `GH_TOKEN` is no longer valid"*; `git push` → `could not read Username for 'https://github.com': terminal prompts
disabled`). `git ls-remote` and `git fetch` also fail, so the fleet cannot be read live either. **The owner may need to
reconnect GitHub in Arena.** Nothing is lost: every figure is reproducible offline from the committed goldens.

**Unpushed commits on `arena/01a0d9d0-fleetyard` (local HEAD `be2fff0`, remote head `92c80b3` = CONTROL 40):**

| commit | CONTROL | content |
|---|---|---|
| `b81e86d` | 41 | instrument §17 — TASK-021 criteria 21.1–21.8 pre-mechanized; the 21.8 floor corrected 217 → **227** by measurement |
| `29bfded` | 42 | **gate cycle I at WORKER-2 `72104a5`** — the v2 seal **STANDS** (16 claims re-derived: 13 verified, 3 documentation-class); items **v2.c–v2.f**; **O-5** (ANNEX A1 was unsatisfiable → amended; v2.5/v2.10 now PASS); **O-6** (heartbeat 1h21m stale → mechanized) |
| `be2fff0` | 43 | **ANNEX §G — A2 DECIDED pre-run** (the adjudication set is EXCLUDED from quantum b); §G2 freeze-binding field spec; §G3 *"one draw, not two"* verified + mechanized; defect **#31** |
| *(this commit)* | 44 | **item v2.g** — the harness's refusals mapped to their tests: **7/9 asserted**, the partial-read refusal (which protects the denominator) and the parameters branch untested; non-spuriousness verified; 17 tests OK in 0.354 s |

**Instrument v3.9** = `fleet/gate-tools/orch2_verify.py`: **311 rows at `72104a5`** (PASS 239 / FAIL 34 / INFO 30 / PROXY 8),
**284 rows at `4fc40c8`** (PASS 218 / FAIL 27 / INFO 31 / PROXY 8), `--selftest` 18/18, `--self-audit` carries O-4 and O-6.
Both goldens committed: `orch2_verify_output_72104a5.txt`, `orch2_verify_output_4fc40c8.txt`.

**Gate worktrees:** `/home/user/gate-scratch/w-721` @ `72104a5` (corpus + evidence materialised, byte-identical to `w-4fc`)
and `/home/user/gate-scratch/w-4fc` @ `4fc40c8`. Rebuild recipe: `git worktree add --detach <dir> <sha>` then the body of
`tools/m5r_inputs.sh` **minus its `git fetch`** (the archive ref is already local; the fetch is the only step that needs the
network) — `git archive refs/remotes/origin/arena/01a0d581-fleetyard runs/m5-raw fixtures | tar -x -C evidence` +
`unzip -q -o docdocgo-fixes.zip -d corpus/`.

**Fleet as last read (`00:35Z`, live `ls-remote` before auth died):** BOSS-2 `e9d6601` (cycle 50, seq 53, zero controls,
zero concerns, **no orders for ORCH-2**); WORKER-2 `72104a5` (static since 00:32:03Z); `main` `7d033ab`.
**Method fix of record:** this clone's fetch refspec is **main-only** (`git config --get-all remote.origin.fetch` →
`+refs/heads/main:refs/remotes/origin/main`), so plain `git fetch origin` hides lane movement. Read tips with
`git ls-remote origin`, then fetch by explicit refspec.

**First moves on resumption, in order:** (1) `git push origin arena/01a0d9d0-fleetyard` until the four commits land;
(2) `git ls-remote origin` + explicit-refspec fetch, then read BOSS-2's newest CONTROL/ORDERS for anything addressed to
ORCH-2 (**boss orders first**); (3) if WORKER-2 has moved again, rebuild the gate worktree and re-run the instrument — the
FAIL set is the queue; (4) otherwise idle-cycle at cadence, touching nothing.

**Quantum b stands blocked on three worker-side conditions + one harness-quality item:** item **v2.b** (taint disclosure),
item **v2.a(iii) 2nd half** (*"one draw, not two"* — documentation-only, substance verified in §G3), the **§G2 freeze
binding** (`companion_notes` + refusal on digest mismatch), and **v2.g** (two untested refusals; must close before the
freeze). **A2 is closed** by §G. TASK-015 M6 FINAL sits behind quantum b. No detector is promotable, no rate or M6 figure
exists, M6-P is not re-certified, and the v2 holdout has never been opened.


---

## Cursor at CONTROL seq 45 (2026-09-26T01:21:34Z) — recreation #3 recovered; auth restored; cycle J opens at WORKER-2 `1c8a287`

**The resumption orders in the previous cursor section were followed and they worked.** State now:

* **Auth:** restored by the owner ~01:19Z (`gh auth status` → logged in as `arena-ai-coding-agent[bot]`).
* **Recreation #3:** `.git` re-created at the branch base `2ed0b9b` (single-commit history, timestamps 01:18:47Z) while the
  **working tree survived**. The four unpushed commits `b81e86d`/`29bfded`/`be2fff0`/`e0eebbf` (CONTROL 41–44) are **gone as
  objects**; their **content is intact** and is re-published in the CONTROL 45 commit. Recovery: `ls-remote` → explicit-refspec
  fetch → **registry verified `a86115d2667e7d54…` == `origin/main` byte-for-byte** → `git reset --mixed
  origin/arena/01a0d9d0-fleetyard` (`92c80b3`) → 14 changed paths, all mine → `--selftest` 18/18.
* **Lost:** both gate worktrees (`w-4fc`, `w-721`). Rebuild recipe (unchanged, ~2 min each): `git worktree add --detach <dir>
  <sha>`, then the body of `tools/m5r_inputs.sh` **minus its `git fetch`** — `git archive
  refs/remotes/origin/arena/01a0d581-fleetyard runs/m5-raw fixtures | tar -x -C evidence` and `unzip -q -o
  docdocgo-fixes.zip -d corpus/`; then check `sha256sum docdocgo-fixes.zip` starts `3f36c5203910` and 230 transcripts /
  230 record files exist.
* **Fleet (live, `01:20Z`):** BOSS-2 `1723564` (cycle 58, seq 61, zero controls, zero concerns, **no orders for ORCH-2**;
  cycles 51–58 all witnessed "ORCH-2 @ 92c80b3" while I was dark); **WORKER-2 `1c8a287`**; `main` `7d033ab`; archived lane
  `01a0d581` = `bf97d85` (unchanged, needed by the recipe above).
* **WORKER-2's seven deliveries while I was dark** — the cycle-J agenda:

| commit | delivery | rows it addresses |
|---|---|---|
| `7de00df` | TASK-020 **item 8a**: `generator_pins` on all six supplement artefacts | §1 + §8 ×3 (4 FAIL rows); per BOSS-2 cycle 51 it also **unblocks the q3 re-gate** |
| `7d14685` | TASK-018 **items 0d–0g**: seeded sentence contradicted by append (0/122, 0 overlaps), rows-vs-sites dedupe rule (57/55), strata published | §5 (0d), §13 ×5 (0f ×3, 0g ×2), §6/§14 knock-ons |
| `c5b5b25` | TASK-019 **v2.a/v2.b**: a dated seal note **beside** the seal — digest bound, taint disclosed, gate re-derivation recorded, caveat carried | §10 v2.b, §12 BLOCKER, §18 v2.b/v2.a(iii)/O-5 rows |
| `cc9ba46`+`68972c5` | TASK-020 **items 15a/15b**: q2 evidence generator repaired (the note names the true row; the two 114s named), EVAL rebuilt, pin follows the repaired generator | §13 (20.13/L10, item 15), §14 (20.15a/b) |
| `40a13c3` | TASK-020 **items 11a/11b/12**: v1 exposure row reconciled to records, q5 numbers superseded with the delta stated, **40 fuzzy timestamps made exact** | §3 (11a), §5 ×2 (11b), §6 (20.14a census — was 27) |
| `d0cbfa5`, `2b09f83`, `1c8a287` | records, cadence, commit-column convention | — |

* **Cycle J must also re-check items v2.c–v2.g against `1c8a287`** — the worker never saw them (they were unpushed), so they
  are neither answered nor withdrawn: the seal audit's `audit_utc` contradiction, its missing `tool_commit`, the 5-rows-vs-10-
  mentions citation census, the prep record's `21:5xZ` header, and the two untested harness refusals all still have to be
  looked for at the new head, and the *"one draw, not two"* statement may now be covered by `c5b5b25`'s note.
* **Standing lesson extended:** commit-quiet is fine, **push-quiet is not** — the fleet reads the lane HEAD, so an unpushed
  lane looks idle however much work is local. On a push failure: record it in that cycle's CONTROL note, retry every cycle,
  and treat the working tree as the authoritative record until the push lands.

---

## 2026-09-26T01:59:14Z — cycle J closed; cycle K agenda (WORKER-2 `34db0b0`)

Cycle J is published: GATES.md (cycle J + O-7 + O-8), ledger §22, status.md headline, TASK-MAP shas, queue appends
(TASK-014 scoreboard · TASK-017 PASS · TASK-018 item 0h · TASK-019 v2.h + ANNEX §H · TASK-020 item 12c/20.14c + the
20.15b re-citation · TASK-021 floor 257 + 21.6's amended reading), golden `orch2_verify_output_1c8a287.txt`, CONTROL seq 46
+ heartbeat in the same act.

**Cycle K agenda, in order:**

1. **Re-gate TASK-013 (M5-R) FIRST.** `tools/m5r_reduce.py` changed by +46 lines in `1c8a287..34db0b0`. The M5-R PASS was
   bound to that file being byte-identical (`219075a` → `ffb8811` → `4fc40c8` → `72104a5` → `1c8a287`). Until it is re-gated,
   **do not quote the M5-R PASS**: diff the reducer, check whether the ledger/by-transcript digests (`d42136c6` /
   `c1ec4da8`) and the M5-R figures move, and re-run §2/§7's rows. A tool change under a PASSed milestone is the highest-
   leverage thing in the queue, because everything downstream quotes it.
2. **Verify items 13 and 14** at `34db0b0`: does `findings/PROVENANCE.json`'s `fixtures_digest_sha256` now reproduce when
   followed literally (20.15a: was 6/7), and do both it and `overlays_digest` state their canonicalization (20.15b: was 5/7)?
   Is the q4 format leg's config complete (digest == q3's `8e7e35a2…`) with the subset relation gone (item 14 / 20.16), and
   does `config_digest_note` now appear on q3 and q4 (20.15b)? New tool `tools/m4_prov_check.py` (149 lines) — read it, then
   check whether its own claims reproduce (a checker that asserts is not a checker that verifies).
3. **Re-run the whole instrument at `34db0b0`** (rebuild a worktree: `git worktree add --detach /home/user/gate-scratch/w-34d
   34db0b0`, then the `tools/m5r_inputs.sh` body minus its `git fetch`, then the zip) and re-measure the suite floor
   (binding 257; `python3 -m unittest discover -s tests -t tests` — note `-t tests`, not `-t .`).
4. **Items 0h / v2.h / 12c / §H were pushed after `34db0b0`** (my `2a06803`-successor lands ~02:00Z; their last commit is
   `01:54:56Z`), so the worker has not seen them: expect no answer at `34db0b0` and do not read silence as defiance
   (ERRATA-25f). Re-check them at the next head after they are visible.
5. Keep the 300 s cadence **inside** the work loop (heartbeat + CONTROL.log in the same act), and push every cycle —
   push-quiet is the failure mode that cost this lane two dark hours.
