# WORKER-2 — TASK-017 DELIVERY (inherit the v1 detector toolchain)

- task: **TASK-017** (ORCH-2 queue `fleet/queue/pending/TASK-017.md` @ `45959ca`)
- claimant: WORKER-2 (A-2026-09-25-001), lane `arena/01a0d9ce-fleetyard`
- status: **DELIVERY** (not completion, not certification)
- order: taken immediately after TASK-018 per the owner's 25g §5 order

## What was materialised (read-only archive, byte-exact)

Source: archived lane `arena/01a0d581-fleetyard` @ `bf97d85962d5e4950fc75374da6b700744b220b5`
(ENDED, read-only), via `git archive <ref> tools tests fixtures runs | tar -x`.

| set | files | check |
|---|---|---|
| `tools/` (15 modules incl. `run_detectors.py`, `sweep_m5.py`, `fixtures.py`, detectors A1/A2/B1/B2/A4, `retrieval.py`, `tokenizer.py`, `loaders.py`, `report_m6.py`, `census.py`) | 15 | byte-identical to the archive |
| `tests/` (13 v1 test modules) | 13 | byte-identical |
| `fixtures/` (confirmed + clean + negative + README + `corrections.json`) | 5 | byte-identical |
| `runs/m5-raw/` (committed v1 raw census: 230 record files + INDEX/PROVENANCE/index.json) | 233 | byte-identical |

**Manifest (LAW §8):** `tools/INHERITED-V1-MANIFEST.json` — archive ref, archive commit sha,
per-file `sha256` for all **266** inherited files **and** the corresponding
`in_archive_sha256` recomputed from `git show <ref>:<path>`, so any future drift is
mechanically detectable. **266/266 match; 0 mismatches at materialisation.**
`runs/m5-raw` was added to the working tree so the inherited corpus-dependent tests run
against their own committed baseline instead of skipping (they look for `runs/m5-raw`, not
the lane's `evidence/` copy; the two trees were compared and are identical).

## Acceptance-criteria evidence

1. **Materialised byte-exact, manifest published** — see the table + manifest above.
2. **Suite green WITH corpus, counts reported** —
   `python3 -m unittest discover -s tests` → **154 tests, OK, 1 skipped**
   (the single skip is `report_m6` "report not committed yet" — the M6 report is a later
   milestone; it is not a corpus or environment skip). Before this task the lane ran 39
   tests; the inherited set adds 115 (v1 baseline @ `90077b4`), so **154 = 115 + 39** and the
   count did not drop. Skips fell from 5 to 1 because the census is now present.
3. **Fixtures verify** — `python3 tools/fixtures.py verify` → `fixtures OK (16 confirmed
   CERTAIN)`; `corrections.json` (withdrawals CF-005/009/013/014/018) is in place.
4. **No modification of inherited detector logic** — the manifest records `unmodified: true`
   and per-file hashes; no inherited file was edited to run on this lane (the toolchain ran
   as-is against `corpus/`).
5. **Fresh v1 baseline reproduction** — `python3 tools/sweep_m5.py --out <scratch> --limit 10
   --fresh` (inherited tool, unmodified) → 10 transcripts, **132 records**; compared against
   the inherited census for those files: **10/10 files byte-identical, 0 differences**
   (`runs/m5-raw-freshcheck/fresh-vs-inherited.json`, per-file sha256 pairs). This extends
   the M4-q4 holdout reproduction (37 files, 185/185 signals, 0 mismatches) to a fresh sweep
   run under the V1 sweep tool itself.
6. **Scope** — reads `corpus/**` + the inherited tree; writes only under `--out`; stdlib
   only; no network (the sweep shells out to `git` only for the zip-hash note, as inherited).

## Boundaries honoured

No detector logic changed, no thresholds touched, no new detectors; the archive is cited,
never re-stamped; the inherited tests are the campaign's own (RUN_WITH_CORPUS), so
"test count never drops" now has teeth on this lane.

## Next

- Per the owner's 25g §5 order: after TASK-018 → TASK-017, the re-cut M4 q2–q4 work proceeds
  against the **fresh sealed split v2** (ORCH-2 to cut, per 25g §5); the q1 holdout remains
  spent and will not be re-run.
- Nothing else is claimable from the queue while this delivery awaits ORCH-2's gate; cadence
  continues (heartbeat + CONTROL.log at ≤300 s, controls and the orchestrator lane read every
  cycle).
