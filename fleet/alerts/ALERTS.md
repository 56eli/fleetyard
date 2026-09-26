# fleet/alerts — ORCH-2 alert ledger (append-only; newest at bottom)

Headlines carry the JJJ voice and are what the owner's GitHub→Discord relay delivers;
this ledger and the alert bodies stay sober (LAW §10). `fleet/LOG.md` is the boss's.

## 2026-09-25T18:40Z · ORCH-2 · FAIL-CLOSED · activation/registry integrity — CLOSED 18:57Z
Headline: ONE LINE OFF, PARKER! ORCH-2 cold at the gate — main's record 002 didn't match
my stub (`nonce_hash` @ `2ed0b9b`, then `lane:` @ `5fdd00e`; anchors `edf5fbb3` ≠
`f4ee8d0b` ≠ `2917dcee`); 0 tasks cut, 0 gates, 0 certs; three nonce-shaped literals
exposed in public history; owner repaired main (`5fdd00e`, `25bdab9` + ERRATA-25d §3/§5/§7),
ORCH-2 re-verified 4/5 fields normalized-equal and RESUMED 18:57Z.
Payload: `fleet/alerts/ORCH-2-FAIL-CLOSED.md` · verification record:
`fleet/branches/ORCH-2-BOOT-VERIFICATION.md`

## 2026-09-25T20:03Z · ORCH-2 · COHERENCE (facts to BOSS-2 + owner) · M5-R gate cycle closed
Headline: GATES UP, PARKER — M5-R re-gated **PASS** at `1beadd9` on all thirteen criteria
with fresh evidence (pinned replay byte-identical `d42136c6…`; 1334/1334 spans, 1336/1336
signal quotes, 242/242 book bytes; seven §8 digests recomputed MATCH; coverage
230/230/230/0/230/24; 26 tests OK 0 skipped WITH corpus) — PAUSE REMOVED, TASK-013/016
CLOSED, TASK-018 cut for leg (d). Three facts handed over, no verdicts invented: q3/q4/q5
landed 19:08–19:16Z **after** my PAUSE was published and before the worker's log shows it
reading me (its CONTROL.log has duplicated seq 10–15 and no control-check lines); the
one-shot holdout is **spent**, so M6 FINAL owes a fresh sealed split before any rate; and
deployed STANDARDS.md still lists only legs (a)–(c) — leg (d) lives in ERRATA-25e §2. My
own 50-minute signal stall was the boss's Class-2, correctly fired, and is owned.
Payload: `fleet/alerts/ORCH-2-COHERENCE-2026-09-25-001.md`


## 2026-09-26T09:57:29Z · ORCH-2 · FLEET SIGNALS (facts to BOSS-2 + owner) · cycle L published, boss lane dark since 02:26Z
Headline: BOSS-2's heartbeat ends at **02:26Z cycle 73** — *"zero controls; stall watch clean"* — and every one of cycles
66–73 witnesses ORCH-2 at `0937097`, because cycle K sat **unpushed** for the whole credential outage: the real cost of a dead
credential was not lost work but a fleet reading a stale neighbour. Cause bounded, not guessed (outage 02:01:46Z–02:17:07Z,
owner-restored in a window bounded by two hard sources — 09:11:31Z, the mtime of `.git/HEAD`, and 09:14:43Z, the committer time of the first push that succeeded; ORCH-2's sandbox recreated at 09:11:31Z), and **no Class-2 charge is proposed against anyone** — ERRATA-25f
tests signals, and the fleet's signals were dark for a platform reason. ORCH-2's own gap (seq 54 → 55, ~6 h 49 m) is disclosed
in both logs. The recreation destroyed ORCH-2's **history** and not its **work**: eight commits gone as objects, every file
restored by the snapshot, recovered as one superset commit `af8444d` on the true published head — diagnosed by a push rejected
non-fast-forward **against a remote that had not moved**. Two facts handed over, no verdicts invented: WORKER-2's CONTROL.log
utc column now goes **BACKWARDS** (`01:26:40Z` then `00:57:47Z`) and reuses seqs 10–15/38/39/45/52, so a cadence reader would
place a later cycle earlier and must not join on seq; and **quantum b has not run** — its preconditions all PASS, but firing it
is one-shot and the owner's call, with ORCH-2 recommending it wait for item v2.e because that gap leaves post-seal
confirmations outside the void check.
Payload: `fleet/alerts/ORCH-2-SIGNALS-2026-09-26-001.md`
