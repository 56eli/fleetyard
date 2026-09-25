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
