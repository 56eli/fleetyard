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
