# TASK-019 — fresh sealed holdout split **v2** (+ its one-shot evaluation), owner-AUTHORIZED

- cut by ORCH-2 (A-2026-09-25-002) 2026-09-25T20:35Z · milestone **M4 → M6 FINAL**
- authority: owner `fleet/ERRATA-2026-09-25g.md` §5 @ main `7d033ab` (blob `84d3019f`,
  bytes sha256 `d0191e6d65d3eeb6969629678f54ec5ba1aa03f3d37dbaf896fa13feed405e6a`):
  "Fresh sealed split v2 is AUTHORIZED: cut it as a queue task (new salt, sealed before
  further tuning, evaluated once); M6-Final headline waits for it."
- why it exists: the q1 split's 37-transcript holdout was **evaluated once and is SPENT**
  (`runs/m4-q4-holdout/`, `holdout_consumed: true`, 19:12–19:14Z, counts only). LAW §9
  requires held-out data **fixed before tuning**; the reducer (errata #2) and the detector
  set have moved since, so no precision figure may rest on the spent split.
- claimant: WORKER-2 (A-2026-09-25-001) · order: **TASK-018 → TASK-019a → TASK-017 →
  (ORCH-2 gates q2/q3) → TASK-019b**

## Quantum a — SEAL split v2 (no evaluation in this quantum)
1. **New salt**, dated and distinct from `fleetyard-m4-holdout-2026-09-25`; publish the
   method (rule, modulus, bucket), the salt, the counts, the per-year table, the corpus
   file-set digest **with its derivation written down** (q1's `corpus_files_sha256`
   derivation reproduced cleanly — do the same, and say so in the file, not only in source).
2. Deterministic and independently reproducible: I must be able to re-derive the exact
   holdout/tuning sets from the published rule with my own code (this is the gate).
3. **In-sample exclusions forced to TUNING:** the 3 v1 fixture-bearing transcripts
   (`A_Unique_Sedona_Seminar_Dec_2008_Part_2`, `Love_Sep_2011_Part_1`,
   `Satsang_Series_Volume_IX_Part_6`) **plus every transcript carrying a fixture confirmed
   by TASK-018** (the 4 provisional dropword fixtures D2-001..D2-004 and anything else the
   leg-(d) adjudication confirms). Seal **after** TASK-018's fixture decisions land, so the
   forced set is complete.
4. **Re-seal rule:** if any fixture is confirmed *after* the seal, the split is void and must
   be re-sealed with a new salt + dated record. Never silently reused, never patched.
5. Seal = a committed file (e.g. `tools/HELD-OUT-SPLIT-V2.json`) + generator/verifier mode,
   committed **before** any further tuning of any detector (commit order is the evidence).
6. Repeat the honesty disclosure: v1 detectors were shaped with corpus-wide knowledge, and
   the drop-word/format rules were shaped on the tuning set — a first figure under v2 is an
   estimate under this split, not pristine out-of-sample.
7. LAW §8 manifest on the run that produces it (corpus + book-store digests, tool commit
   reachable, policy sha, main head, output digest, run utc, derivations).

## Quantum b — ONE-SHOT evaluation (only after ORCH-2 has gated q2/q3 and thresholds are frozen)
1. Thresholds frozen and recorded **before** the run; the run happens **once**; the receipt
   stamps `holdout_consumed`, the full read list, the split salt + digest, and the tool
   commit. Never re-run: a second run needs split v3 and a dated record.
2. Output: per-detector **precision + false-positive counts on the holdout**, with
   **seeded vs independent reported separately** (LAW §9), and per-signal adjudication
   records (each holdout signal confirmed/discarded **with reasons**, cited to bytes) —
   labels are hand reads, not detector agreement.
3. CANDIDATE is never blended into a rate; CERTAIN and HIGH are reported separately; no
   corpus-wide extrapolation beyond what the holdout supports; A4-confusion stays excluded
   unless this run supplies independent fixture recall + a genuinely held-out clean-FP
   measurement (v1's 0/59 is VOID as independent FP evidence — owner ERRATA-2026-09-25 §3).
4. B1/B2 headline gate: v1's hold stands (TASK-005 FAIL / REDIRECT-005 — B1 thresholds
   calibrated on the clean set, B2 filters fitted), so **no headline rate for B1/B2 until
   this quantum passes**.
5. Suite green WITH corpus, skip counts reported, test count never drops (campaign baseline
   v1's 115 tests — TASK-017); stdlib only, no network, corpus read-only, writes only to the
   named outputs.

## Gate (ORCH-2, LAW §9 — any failed criterion = INCOMPLETE)
v2.1 new salt + published method/modulus/bucket, deterministic, **re-derived by me exactly**
(set equality, not counts) · v2.2 corpus file-set digest reproduced from a **written**
derivation · v2.3 all in-sample transcripts (v1 fixtures + TASK-018 confirmations) forced to
TUNING, verified by set membership · v2.4 sealed before any further tuning, on commit-order
evidence · v2.5 §8 manifest complete and recomputed MATCH by me · v2.6 tuning path cannot
read the v2 holdout (filter + assertion + output evidence: keyed transcripts ⊆ tuning,
∩ holdout = 0) · v2.7 (quantum b) one-shot discipline: frozen thresholds, single run,
consumed receipt, no re-run · v2.8 (quantum b) labels are hand adjudications with reasons
and citations I re-derive byte-exact; seeded/independent separated; CANDIDATE never blended;
no rate beyond the holdout · v2.9 no promotion without this evidence; delivery labelled
DELIVERY, never completion or certification.
