# fleet log (append-only)
2026-09-25T18:26Z WORKER-2 (A-2026-09-25-001, lane arena/01a0d9ce-fleetyard): boot
fail-closed — registry record A-2026-09-25-001 failed the byte-exact check on main
2ed0b9b (nonce_hash line; no anchor, no hash chain; fleet2check rejects the registry).
No mission work started (M5-R not begun); read-only diagnosis + report only per LAW §1.3.
Alert: fleet/alerts/WORKER-2-FAIL-CLOSED.md. Awaiting owner.
2026-09-25T18:34Z WORKER-2: re-verification PASS after owner repair (main 5fdd00e;
registry a86115d2…; record A-2026-09-25-001 byte-exact; FORMAT v0 note = fleet2check
chain output ADVISORY). Fail-closed episode closed. M5-R begins (ORCH-2 queue absent,
self-served, disclosed).
2026-09-25T18:43Z WORKER-2: M5-R DELIVERY (findings/ ledger, 1334 findings from the
inherited census; CERTAIN-inherited 2 / HIGH 0 / CANDIDATE 1332; seeded 2,
independent 1332; 242/242 cited book quotes byte-exact; determinism verified).
DELIVERY, not certification — awaits ORCH-2 gate (no ORCH-2 lane yet).
2026-09-25T18:4xZ WORKER-2: owner ruling 25d re-grounded, resuming — ERRATA-2026-09-25d
read at main 25bdab9 (main churn = disclosed owner acts §1; registry rewrite = disclosed
exception §2 and frozen §6; A-2026-09-25-001 confirmed in force §5). Re-verified under
the NORMALIZED standard (§3): record 001 fields 6/6 equal (registry unchanged since
5fdd00e). M5-R delivered (8011439); continuing with M4.
2026-09-25T18:52Z WORKER-2: M5-R errata — fixture-overlap criterion corrected to
span-vs-span (CF-015 recovered): CERTAIN(inherited) 2→3, CANDIDATE 1332→1331,
seeded 3/1331 independent; reconciles with the v1 audit's 3-of-16 detector overlap.
M4 quantum 1: held-out split fixed before tuning (tools/HELD-OUT-SPLIT.json,
193/37 of 230), tools/m4_split.py + 7 m5r tests green, PATTERNS.md rule catalog
published (13 of 16 CERTAIN patterns still invisible to all detectors).
2026-09-25T18:5xZ WORKER-2: owner ruling 1 — the nonce-shaped literal on main is INERT
AND RETIRED (v0 posture UNHASHED-OWNER-CHAT-ONLY; boot nonces single-use, consumed at
boot verification; re-verification binds to ACTIVATION ID + normalized registry record).
Retired from attention; not quoted further.
2026-09-25T18:5xZ WORKER-2: owner ruling 2 — manifest pin 4b65145d is the policy-bundle
SOURCE file; deployed fleet/ERRATA-2026-09-25c.md (sha256 7384a608…) is the instrument
OF RECORD and the authoritative hash. Manifest reconciliation deferred to 2.0.1; no file
edits (freeze extends to the manifest; changes ride errata).
2026-09-25T19:1xZ WORKER-2: M4-q2 — C1-drop detector built (tools/det_dropword.py,
self-test + 8 tests green; holdout-refusal enforced). Tuning run: 193 transcripts in
6 bounded shards (LAW §4A) -> 122 CANDIDATE-class raw signals; merge provenance
recorded. Hand-read sample: 4 confirmed omissions kept as provisional fixtures
fixtures/v2/dropword.json (D2-001..004, byte-bound), 5 parked/discarded. Classification
BLOCKED on proposed STANDARDS leg (d) (needs errata + BOSS CONCERN). No rates.
