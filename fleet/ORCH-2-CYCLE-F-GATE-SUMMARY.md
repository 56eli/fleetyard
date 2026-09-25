# ORCH-2 — CYCLE F GATE SUMMARY (four deliveries gated; push channel dead)

- activation **ORCH-2** (A-2026-09-25-002), lane `arena/01a0d9d0-fleetyard`, role ORCHESTRATOR
- written 2026-09-25T22:09:38Z · gated against WORKER-2 head `ffb8811` in worktree `/home/user/gate-scratch/w-71c`
- origin/main last read `7d033ab` (21:24Z) · registry digest last read `a86115d2…435c14` (FROZEN per ERRATA-25d §6)
- **platform state: GitHub credentials dead since 21:38Z** (`gh api user` → 401). This document and every cycle-F
  record are **committed locally, not pushed** — origin still shows `31ce8dd`. Alert:
  `fleet/alerts/ORCH-2-PLATFORM-2026-09-25-001.md`.

## Verdicts

| task | verdict | fails | passes | owed |
|---|---|---|---|---|
| **TASK-018** leg-(d) adjudication | **FAIL / INCOMPLETE** (no pause) | L5 (false `seeded` sentence) · counting hygiene (2 duplicate sites) · notation class (6 rows) · no stratification of the 57 | L1 · L2 (**57/57 citations byte-exact by my own re-derivation**) · L3-mechanics (**57/57** single-word alignment + flanks ≥5 reproduced by my own code) · L4 · L6 · items 0/0a/0b/0c · §8 manifest exemplary · replay byte-identical · ledger `d42136c6` untouched · suite 217 OK skip 1 | items **0d, 0e, 0f, 0g**; criteria **L7–L10** |
| **TASK-019a** sealed split v2 | **FAIL / INCOMPLETE on v2.5 only** — seal **valid, NOT void** | v2.5 (one stale bound digest: `fixtures/v2/dropword.json` `c8e96319…` recorded, `c40d272f…` at head) | v2.1 (**my own draw reproduces the partition set-equal**, 33/197 over 230) · v2.2 · v2.3 (0 fixture contamination; 37 spent v1 holdout files all in tuning) · v2.4 (sealed before tuning, commit order) · v2.6 (**guard is code**: `SystemExit`; 197 signals all ⊆ tuning) · v2.9 · 10 tests OK · `tool_sha256` matches | items **v2.a, v2.b**; criteria **v2.10, v2.11**; **quantum b held** |
| **TASK-020** items 1–8 | **FAIL / INCOMPLETE** (items 9–11 undelivered) | 20.1 (`tool_commit` pins don't contain the generating tools; five files disagree) · 20.5 (**D-002** and **D-039** promoted CERTAIN while sibling instruments exclude/suppress them) | 20.2 · 20.3 · 20.4 (**59/59 clean-set citations byte-exact from the store**) · 20.6 (all 8 thresholds + 5 reproducible probes replacing my unreproducible camel-glue figure) · 20.7 · 20.8 (217 vs the 115 baseline) · 20.9 · every content digest recomputes MATCH · filter reproduces 1 + 7 under my own code | items **8a, 8b**; criterion **20.13**; items **9–11** still owed |
| **TASK-017** inherit v1 toolchain | **PASS — all six criteria** | — | 1 (**266/266** entries verified three ways: head == manifest, archive == manifest, **head == archive**; 0 unlisted, 0 phantom) · 2 (217 OK skip 1; 154 = 115 + 39) · 3 (`fixtures OK (16 confirmed CERTAIN)` by my own run) · 4 · 5 (**my own fresh sweep → four-way digest equality 10/10**, 132 = 132) · 6 (stdlib only, no network) | item **17.a** non-blocking (fuzzy `materialised_utc`) |

## Restrictions in force (unchanged until the repairs land)

1. **57 / 47% may never be quoted without** the flank-floor sensitivity band **71/57/33/22** (floors 3/5/8/10), the
   stratification (**27 of 57 interjections/fillers · 6 `%`↔`percent` notation · 11 function words · ~13 content**),
   the deduped **site count 55**, and the notation class's status. The CERTAIN-leg-d set is **unusable in any M6
   document** until TASK-018 items 0d–0g land.
2. **No detector is promotable; no precision, rate or M6 figure exists.** q1–q5 remain FAIL/INCOMPLETE; **185/5/12
   is a receipt only**; the 122 drop-word signals and 48 format signals stay **CANDIDATE / PROVISIONAL-UNGATED**.
3. **Quantum b (the one-shot v2 holdout evaluation) is held** until TASK-019 items v2.a and v2.b land: the seal note
   must bind the post-append fixture digest and disclose that **4 of the 33 holdout transcripts already carry 7
   pre-seal C1-drop signals (3 promoted: D-092/D-093/D-094)** — then quantum b states in advance whether it reports
   per file or excludes those 4 with the denominator change.
4. **TASK-015 (M6 Final) stays BLOCKED** behind quantum b. **M6-P is owner-accepted and is not re-certified.**
5. The ledger is invariant at `d42136c6…` (1334 findings) and by-transcript at `c1ec4da8…` (230 files): **the M5-R
   PASS and the TASK-016 re-gate PASS stand.**

## Questions routed out of my lane (I do not decide these)

- **To the owner / BOSS-2 (from the TASK-018 gate):** does clause d-i reach (i) **speaker-side fillers and
  interjections** (`huh`×7, `see`×6, `yeah`×6, `right`×3, `man`, `well`, `heh`, `um`, `haha` — 27 of the 57) and
  (ii) **notation variants** (`101%`/`78%` in the transcript vs the book's word `percent` — 6 rows, where no *word*
  is absent)? The mechanics comply with ERRATA-25e §2 as enacted; the campaign's purpose is transcription errors that
  bear on doctrine. My recommendation, for the record only: keep them in the file, refuse the notation class, publish
  the strata.
- **To BOSS-2 (from the platform alert):** if ORCH-2's pushed signals look stale after 21:24Z, that is the credential
  outage, not idleness, a halt, or defiance — an ERRATA-25f Class-2 staleness finding against ORCH-2 after that
  timestamp would be misdiagnosed.

## Queue state after cycle F

- **Claimable now (worker):** TASK-020 items **9–11** (q4 manifests, PATTERNS §5d correction, the three stale
  ledger-digest lines + q5's numbers) · TASK-018 items **0d–0g** · TASK-019 items **v2.a/v2.b** · TASK-020 items
  **8a/8b** · TASK-017 item **17.a** · **TASK-021** (newly cut: C1-drop threshold sensitivity over the **v2 tuning
  half only**, criteria 21.1–21.8).
- **Blocked:** TASK-019 quantum b (behind v2.a/v2.b) · TASK-015 M6 Final (behind quantum b) · the q1–q5 re-gates
  (behind TASK-020 items 9–11 and the TASK-018 repairs).
- **Nothing further is gateable** until deliveries land, and I cannot read deliveries while fetch is dead.

## My own instrument defects, recorded (honesty about the gate)

Four false failures this cycle were **mine**, not the worker's, and each is written into the relevant gate record:
(1) curly vs straight apostrophes breaking token equality (false-failed 44/57 CERTAIN rows); (2) normalizing em/en
dashes **to hyphens**, which glued the book's `do—psychological` into one token (false-failed 5 more); (3) hyphen
tokenization inside tokens; (4) fixture files store **paths** while the split stores **basenames** (false-failed
fixture membership). Rule adopted: every token- or set-level claim I check states its token rule and key convention
in the record.

## On reconnect, in order

1. `git fetch`; re-check the fleet (owner messages on main, BOSS-2 orders/CONCERNs, WORKER-2 head).
2. Push the backlog in commit order: `8cd2f5c` (TASK-018 gate) → `cba2550` (platform alert) → `3dd0b45` (TASK-019a)
   → `1ca3941` (TASK-020) → `430706b` (TASK-017 + TASK-021) → this summary.
3. Re-verify the registry digest against the **current** `origin/main` and record any main churn.
4. Resume the 300 s cadence (heartbeat + CONTROL.log) and continue the queue.
