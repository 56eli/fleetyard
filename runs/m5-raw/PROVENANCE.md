# runs/m5-raw provenance (TASK-011)

- First generation: 2026-09-25 ~00:37–00:55Z by `tools/sweep_m5.py` at worker
  commit 5ea8de8 (records) / local 382095f (index). 382095f was lost unpushed
  in an environment re-clone (GitHub token expired); its content was
  re-committed byte-identical as df5542b, so the original index cited an
  unreachable sha.
- Fresh replay: 2026-09-25 ~09:16–09:33Z, `python3 tools/sweep_m5.py --out
  /tmp/replay --fresh` at reachable worker commit
  7b8863d0727b4dd7fbaa71683fd00feeebc832cd (tools/ and tests/ identical to
  df5542b), corpus re-extracted from `docdocgo-fixes.zip` (sha256 prefix
  3f36c5203910). Result: 230/230 processed, 1334 records, 0 failures;
  `diff -r` of all 230 `records/*.json` against the committed files: **identical**.
  index.json differed only in generated_utc / tool_commit / command.
- index.json / INDEX.md were then re-rendered from the committed records at
  7b8863d (`python3 tools/sweep_m5.py --out runs/m5-raw`), so `tool_commit`
  is now reachable.
