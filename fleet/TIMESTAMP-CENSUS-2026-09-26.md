# Timestamp census and repair — criterion 20.14 / TASK-020 item 12

Written by WORKER-2, lane `arena/01a0d9ce-fleetyard`. Stamp: **2026-09-26T01:00:55Z** — exact to the
second; source: `date -u` on the lane clock when this file was written (the commit carrying
it is the source of record).

## What the gate found, and what this census found

- Gate (instrument §6, 2026-09-25T23:27:53Z): **26 asserted fuzzy timestamps in 10 files**,
  4 sites quoting a fuzzy value as a citation, and **1 own-time offender**:
  `tools/INHERITED-V1-MANIFEST.json` → `materialised_utc` (TASK-017 item 17.a).
- This census (same regexes: `\d{1,2}:\d[xX]Z|\d[xX]:\d{2}Z|[xX]Z\b`, citation classifier by
  backtick wrapping or a 60-char context of `fuzzy|supersed|read|…)`: **40 asserted
  instances in 11 files** — the gate's 26 plus `fleet/heartbeats/WORKER.log` (10),
  `fleet/branches/WORKER-2-TASK-019b-PREP.md` (1), `fleet/branches/WORKER-2-M5R-DELIVERY.md`'s
  item-11 supersession (1) and two further `fleet/LOG.md` entries written after the gate's run.

## The rule applied (the gate's item-12 ruling, stated exactly)

An exact value **plus its source** wherever a timestamp is evidence — a run, generation,
materialisation or appended correction that must be orderable against a commit. The source
recovering each value: **the committer timestamp of the commit that introduced the line**,
derived with `git blame -L n,n --porcelain` at the time of repair (the gate named
`d7fee6e` / `4fc40c8` / `b2e0761` as the recoverable set; blame is the mechanical generalisation).
Narrative beacons (`fleet/LOG.md`, `fleet/heartbeats/WORKER.log`) carry the exact value with
`(src <commit7>)` beside it. Fuzzy values are left readable in backticks (`read \`21:3xZ\``),
so an audit can still see what was published before the repair. **No fuzzy value is asserted
any more.** The sealed `fixtures/v2/dropword.json` fuzzy `generated_utc` is left untouched:
its exact sibling is in-file (the gate's INFO pattern) and the file is digest-bound by split v2
(`c40d272f…`), so editing it would void the seal.

## Sites repaired (39)

| file | line | previous value | exact value | source commit |
|---|---|---|---|---|
| `fleet/LOG.md` | 15 | `leading field` | 2026-09-25T18:45:13Z | `341ee2e` |
| `fleet/LOG.md` | 26 | `leading field` | 2026-09-25T18:52:41Z | `e07be0e` |
| `fleet/LOG.md` | 30 | `leading field` | 2026-09-25T18:52:41Z | `e07be0e` |
| `fleet/LOG.md` | 34 | `leading field` | 2026-09-25T19:06:53Z | `012914d` |
| `fleet/LOG.md` | 40 | `leading field` | 2026-09-25T19:08:35Z | `4425763` |
| `fleet/LOG.md` | 47 | `leading field` | 2026-09-25T19:14:56Z | `4e114f1` |
| `fleet/LOG.md` | 54 | `leading field` | 2026-09-25T19:16:05Z | `2f55b0c` |
| `fleet/LOG.md` | 62 | `leading field` | 2026-09-25T19:17:57Z | `dada3e6` |
| `fleet/LOG.md` | 70 | `leading field` | 2026-09-25T19:40:07Z | `1beadd9` |
| `fleet/LOG.md` | 77 | `leading field` | 2026-09-25T19:55:50Z | `10afc0d` |
| `fleet/LOG.md` | 89 | `leading field` | 2026-09-25T20:38:02Z | `9cd905d` |
| `fleet/LOG.md` | 96 | `leading field` | 2026-09-25T20:38:18Z | `1fb524e` |
| `fleet/LOG.md` | 101 | `leading field` | 2026-09-25T20:48:00Z | `b2e0761` |
| `fleet/LOG.md` | 109 | `leading field` | 2026-09-25T20:50:46Z | `293b29c` |
| `fleet/branches/WORKER-2-M5R-DELIVERY.md` | 4 | `18:4xZ` | 2026-09-25T18:39:57Z | `8011439` |
| `fleet/branches/WORKER-2-M5R-DELIVERY.md` | 50 | `18:5xZ` | 2026-09-25T18:46:05Z | `593cad3` |
| `fleet/branches/WORKER-2-M5R-DELIVERY.md` | 68 | `19:4xZ` | 2026-09-25T19:16:05Z | `2f55b0c` |
| `fleet/branches/WORKER-2-M5R-DELIVERY.md` | 83 | `19:2xZ` | 2026-09-25T19:18:25Z | `a4c6655` |
| `fleet/branches/WORKER-2-M5R-DELIVERY.md` | 154 | `21:4xZ` | 2026-09-25T21:27:18Z | `d7fee6e` |
| `fleet/branches/WORKER-2-TASK-019a-DELIVERY.md` | 26 | `20:5xZ` | 2026-09-25T20:50:46Z | `293b29c` |
| `fleet/branches/WORKER-2-TASK-019b-PREP.md` | 3 | `21:5xZ` | 2026-09-26T00:32:03Z | `72104a5` |
| `fleet/heartbeats/WORKER.log` | 10 | `leading field` | 2026-09-25T19:06:53Z | `012914d` |
| `fleet/heartbeats/WORKER.log` | 11 | `leading field` | 2026-09-25T19:08:35Z | `4425763` |
| `fleet/heartbeats/WORKER.log` | 12 | `leading field` | 2026-09-25T19:14:56Z | `4e114f1` |
| `fleet/heartbeats/WORKER.log` | 13 | `leading field` | 2026-09-25T19:16:05Z | `2f55b0c` |
| `fleet/heartbeats/WORKER.log` | 14 | `leading field` | 2026-09-25T19:17:57Z | `dada3e6` |
| `fleet/heartbeats/WORKER.log` | 15 | `leading field` | 2026-09-25T19:40:07Z | `1beadd9` |
| `fleet/heartbeats/WORKER.log` | 19 | `leading field` | 2026-09-25T20:34:58Z | `33b6f36` |
| `fleet/heartbeats/WORKER.log` | 72 | `leading field` | 2026-09-25T20:38:02Z | `9cd905d` |
| `fleet/heartbeats/WORKER.log` | 97 | `leading field` | 2026-09-25T20:48:00Z | `b2e0761` |
| `fleet/heartbeats/WORKER.log` | 106 | `leading field` | 2026-09-25T20:50:46Z | `293b29c` |
| `findings/M4-q5-A1-CLAIM-RECONCILIATION.md` | 67 | `20:1xZ` | 2026-09-25T20:34:58Z | `33b6f36` |
| `findings/M4-q5-A1-CLAIM-RECONCILIATION.md` | 82 | `21:4xZ` | 2026-09-25T21:27:18Z | `d7fee6e` |
| `findings/README.md` | 107 | `21:4xZ` | 2026-09-25T21:27:18Z | `d7fee6e` |
| `runs/m4-q4-holdout/README.md` | 36 | `21:3xZ` | 2026-09-25T21:27:18Z | `d7fee6e` |
| `tools/PATTERNS.md` | 143 | `21:5xZ` | 2026-09-25T21:27:50Z | `4fc40c8` |
| `tools/PATTERNS.md` | 220 | `21:3xZ` | 2026-09-25T21:27:18Z | `d7fee6e` |
| `tools/PATTERNS.md` | 348 | `21:2xZ` | 2026-09-25T21:21:28Z | `08498e4` |
| `tools/PATTERNS.md` | 355 | `21:2xZ` | 2026-09-25T21:21:03Z | `a5dec38` |

## The own-time offender (item 17.a)

- `tools/INHERITED-V1-MANIFEST.json`: `materialised_utc` `20:5xZ` → **2026-09-25T20:48:00Z**
  with a new `materialised_utc_source` naming commit `b2e0761` (the TASK-017 delivery commit
  carrying the manifest). Note the old value was a **forward stamp** — it named a minute after
  its own commit — which is exactly why minutes cannot serve as evidence. JSON re-validated; the
  266 per-file hashes and the `unmodified` claim are untouched (no inherited file was edited).

## After

- asserted fuzzy timestamps in the worker tree: **0** (the single remaining match is the sealed
  fixture's compliant INFO pattern).
- every value above is checkable: `git show <commit7>` gives the committer time; the file at that
  commit carries the line the value was derived from.
