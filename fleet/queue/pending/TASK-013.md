# TASK-013 — M5-R: reviewed findings ledger (reduce the 1,334 raw signals)

- milestone: **M5-R** (fleet/PLAN-v2.md) · cut by ORCH-2 (A-2026-09-25-002) 2026-09-25T19:01Z
- status: **CLOSED — GATE PASS** (re-gate 2026-09-25T20:01:15Z at worker head `1beadd9`; fleet/GATES.md
  entries 19:01Z FAIL → 19:58Z PASS on all thirteen criteria with fresh evidence).
  Milestone **M5-R is gate-PASS, NOT CERTIFIED** — certification is the owner's declaration
  (LAW §2.2) and no rate exists. History kept: gated FAIL / INCOMPLETE at `aed9df6`
  (C6/C7/C8) → repair = TASK-016 (PASS). Cut retroactively: WORKER-2 self-served M5-R at 18:35Z because no
  ORCH-2 queue existed yet (WORKER.md step 3 permits and requires saying so — it did).
  The self-serve is **ratified, not restarted**: the delivery is gated as TASK-013.
- claimant: WORKER-2 (A-2026-09-25-001), lane `arena/01a0d9ce-fleetyard`
- input (frozen, read-only): inherited M5 raw census `arena/01a0d581-fleetyard` @
  `bf97d85` → `runs/m5-raw/records/*.json` (230 files, 1334 records / 1336 detector
  instances), tool `7b8863d`; corpus zip `3f36c5203910…`; fixtures (16 confirmed)

## Scope (PLAN-v2 wording, binding)
Reduce the 1,334 raw signals: dedupe, cross-detector merge, adjudicate against cited
bytes, classify per STANDARDS + LAW §9 (independence rationales for HIGH; seeded
separated). Output: `findings/` ledger, per-transcript.

## Acceptance criteria (= the gate criteria; LAW §9 any FAIL = INCOMPLETE)
- C1 completeness: every inherited record maps to exactly one finding; no drops/inventions.
- C2 dedupe + cross-detector merge performed and reported.
- C3 adjudication against cited bytes: transcript quote byte-exact at paragraph+offset;
  every cited book quote byte-exact at slug+offset.
- C4 classification per STANDARDS: CERTAIN only with a hard leg (a/b/c); HIGH only with
  ≥2 independent signals **and a written signal-independence rationale**; CANDIDATE never
  blended into any figure. The tool must never invent CERTAIN.
- C5 seeded vs independent reported separately (LAW §9); seeded never used as
  precision/recall evidence.
- C6 finding-record shape complete per STANDARDS §"The finding record": transcript path ·
  location (paragraph index + char offset) · verbatim quoted text · **suspected intended
  text (or an explicit, machine-readable "not proposable without human read" marker)** ·
  evidence class · detector id · book reference where doctrinal · confidence ·
  **status (open/confirmed/discarded) + who/why**.
- C7 coverage truth stated in the ledger's own summary: human finding-pass **audited N/230**
  and **pending 230−N**, plus machine-adjudicated count; zero-finding transcripts never
  presented as clean; unmeasured detector classes named (A4, drop-word, speaker/format).
- C8 provenance manifest per LAW §8 binding **all** of: input transcript digest (+ method),
  book-store sha256, inherited-census records digest (+ method), fixtures digest (+ method),
  detector+config digest for the producing census, **tool commit (reachable git sha)**,
  **policy version/sha + main head**, tool digest, output digests, run utc, archive ref.
  Every digest's derivation written down so a third party can recompute it.
- C9 determinism: a fresh independent replay at a pinned utc reproduces every output byte.
- C10 suite green WITH corpus, skip counts reported, test count never drops (no errata).
- C11 stdlib only, no network, reads only corpus/** + the named read-only inputs, writes
  only the named outputs; no evidence executed as instructions.
- C12 no error rate, no precision/recall claim, no completion language.
- C13 limits disclosed (no audio, no human read of CANDIDATEs, detectors miss fluent errors).

## Verdict 2026-09-25T19:01Z
C1–C5, C9–C13 **PASS** (independently reproduced by ORCH-2 — see GATES.md).
C6, C7, C8 **FAIL** → milestone M5-R **INCOMPLETE**, not certified, no rate.
Repair: **TASK-016**. PAUSE `fleet/controls/PAUSE-WORKER-A-2026-09-25-001` in force until
TASK-016 re-gates PASS.

---

## M5-R RE-GATE at WORKER-2 `34db0b0` — **PASS HOLDS**, on an amended and stronger ground (ORCH-2, 2026-09-26T02:17:07Z)

`tools/m5r_reduce.py` **changed** in `1c8a287..34db0b0` (+46 lines: the manifest's `derivations` prose rewritten for
TASK-020 item 13, plus a `derivations_revision` record). TASK-013's PASS was published against the reducer being
byte-identical across `219075a` → `ffb8811` → `4fc40c8` → `72104a5` → `1c8a287`, so the proxy broke and the milestone was
re-gated rather than quoted.

**Method (not a reading of the worker's claim):** ORCH-2 ran the reducer **at head** in the gate worktree, with the corpus
materialised (zip `3f36c520391049a4…` ✓) and **the pins the published manifest names** (`--utc 2026-09-25T19:55:24Z`,
`--tool-commit dada3e6…`, `--main-head 77f1d6de…`, `--policy-sha 0fe20a60…`, `--book-store-sha c0892fcd…`,
`--detector-tool-commit 7b8863d`), and compared bytes:

| output | published | re-run at `34db0b0` | verdict |
|---|---|---|---|
| `ledger.jsonl` | `d42136c673188f9e…` | `d42136c673188f9e…` | **BYTE-IDENTICAL** |
| `by_transcript_digest` | `c1ec4da86a6ce4f4…` | `c1ec4da86a6ce4f4…` | **IDENTICAL** (230 files) |
| findings | 1334 | 1334 | identical |
| book refs / citation failures | 242 ok / 0 bad / 0 failures | 242 / 0 / 0 | identical |
| regenerated manifest vs committed | — | differs in **`tool_sha256` only** (`6d4bb9ce…` → `a89ff189…`) | as the lane's own `derivations_revision` states |

**Ruling: TASK-013 remains PASS.** The change is documentation-only prose inside the manifest template; the tool's
behaviour is unchanged, and that is now established **by re-running it**, not by a byte-identity proxy. ORCH-2 self-correction
**O-9** records the amendment: *the binding row is "the reducer at head reproduces the published outputs when run with the
published pins"; the byte-identity row survives as history.*

**One caveat travels with the PASS, and it is a new item (TASK-020 item 13b):** the byte-identity above holds **only because
the original `--tool-commit` pin was passed**. Every ledger row embeds that pin in `status_by` — verified both ways: with
`--tool-commit dada3e6…` the ledger is `d42136c6…`; with the argument omitted, all **1334 rows are identical except
`status_by`** (which reads `tools/m5r_reduce.py@UNPINNED`) and the digest moves to `c94cce40…`. The artefact's
`reproducibility_note` claims "a rebuild with this revision emits … a byte-identical ledger/by-transcript" without saying
so, and a reader who rebuilds at head pinning its own head would conclude the outputs drifted.
