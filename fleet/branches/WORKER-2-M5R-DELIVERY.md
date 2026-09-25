# DELIVERY — WORKER-2 · M5-R reviewed findings ledger

- activation: A-2026-09-25-001 (WORKER-2) · lane: `arena/01a0d9ce-fleetyard`
- delivered_utc: 2026-09-25T18:4xZ · main observed: `5fdd00e` · policy `0fe20a6057ec9fa2…`
- mission: fleet/PLAN-v2.md **M5-R** (first mission per boot prompt; ORCH-2 queue
  absent at boot — self-served, disclosed in heartbeat and here)

## Artifact

- `findings/ledger.jsonl` (1,334 findings), `findings/by-transcript/*.json` (230),
  `findings/SUMMARY.md`, `findings/REVIEW-QUEUE.md`, `findings/PROVENANCE.json`,
  `findings/README.md`
- tools: `tools/m5r_reduce.py` (reducer), `tools/m5r_inputs.sh` (input
  materialisation), `tests/test_m5r.py` (6 tests, green)
- inputs (working evidence, never committed): `evidence/` (archive census +
  fixtures), `corpus/` (zip sha `3f36c5203910…`, 230 transcripts + manifest.json)

## Result (no rates; DELIVERY, not certification — LAW §2.1/§9)

- 1,334 records / 1,336 signal instances → **1,334 findings**; 0 citation failures;
  0 exact duplicates; 2 multi-detector records merged (one finding each).
- Classes: **CERTAIN (inherited fixture) 2** — CF-003 (`255%`→`55%`, M5R-0461) and
  CF-006 (negative/positive energies, M5R-0460) — **HIGH (proposed) 0**,
  **CANDIDATE 1,332**; **seeded 2 / independent 1,332** (LAW §9).
- Book-byte adjudication: **242/242 cited book quotes verified byte-exact** at the
  cited slug + offset (0 failures; 0 non-Hawkins citations).
- Claim corroboration: A1 840/938 · A2 158/158 · B1 12/12 · B2 228/228; the 98 A1
  non-re-derived cases are review flags (+1 queue score), not verdicts.
- Determinism: verified byte-identical on the real inputs (`--utc` pinned);
  ledger sha256 `c05429f941ed2444ed48017748f3cfda2e35b7f313e5fdf018b06eff56c79740`.
- Provenance (LAW §8): inputs pinned in `findings/PROVENANCE.json`; the corpus
  overlays digest is now computed by a **documented method** (fixing the inherited
  gap where `dec55ef1…` had no recorded derivation).

## Honest limits

No audio; no human read of the 1,332 CANDIDATE findings; detectors never seen by
this tool beyond their outputs; drop-word / speaker-format / A4-confusion absent
(unmeasured ≠ zero); 24 transcripts carry zero findings and are **not** shown clean.
`HIGH 0` is a finding of this reduction: no independent cross-family convergence
exists outside the fixture-overlapping (in-sample) spans.

## Awaits

ORCH-2 gate per LAW §9 (per-criterion verdicts; no certification without
held-out/provenance evidence) — **ORCH-2 lane does not exist yet** as of this
delivery. Next in PLAN-v2 order after M5-R: **M4** (self-improvement loop), then the
FINAL **M6** report which this ledger feeds.

## Errata (append-only) — 2026-09-25T18:5xZ · fixture-overlap criterion corrected

M5-R v1 (commit `8011439`) matched fixture overlap by *containment of the fixture's
start offset inside the finding span*. That missed the CF-015 case, where the
detector's span begins **after** the fixture's offset but inside the fixture's quoted
text. Corrected to **span-vs-span overlap** in `tools/m5r_reduce.py` (new test
`test_fixture_overlap_uses_the_fixture_quoted_span`).

Corrected numbers (supersede the block above):

- Classes: **CERTAIN (inherited fixture) 3** — CF-003 (M5R-0461), CF-006 (M5R-0460),
  **CF-015 (M5R-0078, B2-misquote @5854)** — **HIGH 0**, **CANDIDATE 1,331**.
- Seeded 3 / independent 1,331 (LAW §9). This now matches the v1 audit's "detectors
  overlap 3 of the 16 hand-found CERTAIN errors" claim, re-derived from the ledger.
- Everything else (1,334 findings, 0 citation failures, 242/242 book quotes
  byte-exact, determinism) is unchanged. New ledger digest is in
  `findings/PROVENANCE.json`.

## Errata #2 (append-only) — 2026-09-25T19:4xZ · A1 claim re-derivation fixed

M5-R's claim-corroboration table was wrong for A1: 98 "not re-derived" flags came
from **two defects in `tools/m5r_reduce.py`**, not from the v1 detector — (a) an
ASCII-only tokenizer (non-Latin spans tokenized to zero tokens), (b) a unit-length
search bound of 8 tokens while A1 claims reference units up to 11. Both fixed
(Unicode token rule + `kmax=16`), with the full analysis in
`findings/M4-q5-A1-CLAIM-RECONCILIATION.md`.

Corrected corroboration (supersedes the table above): **A1 938/938 · A2 158/158 ·
B1 12/12 · B2 228/228 — 0 flagged.** Everything else unchanged (1,334 findings;
CERTAIN-inherited 3 / HIGH 0 / CANDIDATE 1,331; seeded 3/1,331; 242/242 book quotes
byte-exact; 0 citation failures). New ledger sha256 `64977c2f…` in
`findings/PROVENANCE.json`.

## Errata #3 (append-only) — 2026-09-25T19:2xZ · TASK-016 repair (ORCH-2 gate FAIL→repair)

ORCH-2 gated TASK-013 at head `aed9df6` and returned **FAIL / INCOMPLETE** on three
criteria (C6 finding-record shape, C7 coverage truth, C8 LAW §8 manifest); the other
ten PASSed on independent reproduction. Repair delivered under the scoped PAUSE
control (`fleet/controls/PAUSE-WORKER-A-2026-09-25-001`), per TASK-016:

- **R1 record shape:** every finding now carries `suspected_intended` +
  `suspected_intended_status` (present-and-explicit `null` for the 157 A2-nonsense
  spans: "not proposable mechanically; human read required") and STANDARDS
  `status: open` + `status_by` ("machine-adjudicated by tools/m5r_reduce.py@<commit>;
  human confirmation required"). No class changed: CERTAIN 3 / HIGH 0 / CANDIDATE
  1,331; seeded 3.
- **R2 coverage truth:** explicit row in `findings/SUMMARY.md` §0 and
  `findings/README.md`: `transcripts 230 | detector-run 230 | machine-adjudicated 230 |
  human finding-pass audited 0 | pending human review 230 | zero-finding transcripts
  24 (not shown clean)`; titles qualified ("reviewed" = machine-adjudicated).
- **R3 manifest:** `findings/PROVENANCE.json` binds `tool_commit` (reachable lane
  commit carrying this exact tool file: `dada3e60…`, this repair commit), `policy_sha256`,
  `main_head`, `book_store.sha256` (`c0892fcd…`), the inherited census's
  `detector_tool_commit` (`7b8863d`) + detector set, and a written derivation for every
  digest — including the `overlays_digest` wording trap (sorting the resulting lines
  gives `58274f46…`; the implemented sort-by-basename gives `027f82a0…`, which is the
  correct, reproducible value).
- No detector logic changed in this repair; **three tests added (23 → 26, all green)**.

## TASK-016 — per-criterion evidence (claimed per owner ERRATA-25e §1, OPTION A)

Claim: TASK-016 taken as directed ("your ONLY task now"); boundaries respected — no
new detectors, no tuning, no class promotion, no rates (TASK-016 §Boundaries).

**C6 — STANDARDS finding-record shape.** Fresh reads at head: 1,334 findings; 1,334
carry `suspected_intended`, `suspected_intended_status`, `status`, `status_by`; status
vocabulary `{open: 1334}`; the 157 A2-nonsense spans carry an explicit
`suspected_intended: null` with status "not proposable mechanically; human read
required"; `status_by` = "machine-adjudicated by tools/m5r_reduce.py@dada3e60…; human
confirmation required". Regression test:
`tests/test_m5r.py::test_standards_finding_record_shape_is_complete`.

**C7 — coverage truth.** `findings/PROVENANCE.json` stats.coverage =
`{transcripts 230, detector_run 230, machine_adjudicated 230,
human_finding_pass_audited 0, pending_human_review 230,
zero_finding_transcripts 24, with_findings 206}`; the row is printed verbatim in
`findings/SUMMARY.md` §0 and in `findings/README.md`, with titles qualified
("reviewed" = machine-adjudicated reduction of the raw census). Regression test:
`test_coverage_truth_row_is_emitted`.

**C8 — LAW §8 manifest.** `tool_sha256` `6d4bb9ce…` equals the sha256 of
`tools/m5r_reduce.py` as stored in `dada3e60` (reachable on this lane, verified by
`git show`); `policy_sha256` `0fe20a60…` equals sha256(`fleet2/POLICY-MANIFEST.sha256`
on main, re-verified at main `8e9e179`); `book_store.sha256` `c0892fcd…` recomputed
from the frozen corpus; `inherited_census.detector_tool_commit` `7b8863d` reachable on
the predecessor archive with its detector set and exclusions; `derivations` written for
all seven digest fields (including the trap: sorting the digest *lines* gives
`58274f46…`, the correct sort-by-basename value is `027f82a0…`). Regression test:
`test_law8_manifest_bindings_and_derivations`. Fresh manifests were produced by fresh
runs (never stamped on inherited data): run 1 binds main `25bdab9`; run 2 (after
ERRATA-25e) binds main `8e9e179`; ledger sha is identical in both (`d42136c6…`), so the
manifest change is provenance-only.

**Substance stability (no quiet edit).** Against the gated head `aed9df6`: the
1,334 (transcript, char_offset, span_end, span_text) keys are identical; no field was
removed; the only additions are the four R1 fields; class counts unchanged —
CERTAIN (inherited fixture) 3 · HIGH 0 · CANDIDATE 1,331 · seeded 3; citation
failures 0; book refs 242/242.

**Determinism + suite.** Two runs with the same `--utc` are byte-identical (fresh full
replay against committed `findings/` also byte-identical); `python3 -m unittest
discover -s tests` → **26 tests, OK, 0 skipped, 0 errors** (7 at M5-R delivery → 15 at
M4-q2 → 26 now; never dropped).

> **SUPERSESSION (appended 2026-09-25T21:4xZ, TASK-020 item 11 — q5.7):** the ledger digest
> quoted above (`64977c2f…`) is **no longer current**. TASK-016's regeneration (`a4c6655`)
> rewrote the record shape two minutes after the q5 run, and the ledger at head is
> **`d42136c673188f9e091526083b95941cabc5822a8b5cffeb8913b942cb658a32`** (1,334 findings).
> The old line is left readable, not rewritten — it was true when written. **The binding of
> record is `findings/PROVENANCE.json`** (its `outputs.ledger.jsonl` field), not any digest
> quoted inside prose: any figure on this page is void unless that manifest agrees.
