# lane registry (append-only) — ORCHESTRATOR

ORCH-2 lane: arena/01a0d9d0-fleetyard, 2026-09-25T18:40Z, policy 0fe20a6057ec9fa2
activation: A-2026-09-25-002 (role ORCHESTRATOR · fleet/roles/ORCHESTRATOR.md v2)
boot main head: 5fdd00e7519daae9773c23658d632e45aca31b8b (explicit-refspec fetch; this
  lane was created at 2ed0b9bb736e338af00adaf2157781b02d27b540 and fast-forwarded to
  5fdd00e before any record was written — main moved twice during boot, owner web edits)
registry file sha256: a86115d2667e7d54ff418524303c9adeca2348709d233e9e1c39480251435c14
record A-2026-09-25-002 block sha256: 2917dcee286035a5e265aad7d2ebd007fd80c0465b973ab0f99fde46a386c190
boot-stub record text sha256:      edf5fbb3e5a43ba9a855dbd109d8428d8b8e49fbe927c29368ee283638734a97
predecessors (READ-ONLY archives — never resumed, never re-read as checkpoints, LAW §1.5/§2A):
  arena/01a0d5b7-fleetyard @ fcc9834e88302db8bed9216ae9e19ba5ba07e9a0 (ORCH v2, ENDED by
    owner HALT at 2026-09-25T17:30:12Z; final handoff in its GATES.md/ORCH-STATE.md)
  arena/01a0d582-fleetyard @ 191b1f8a61d3fb2fd6d59c540c3acb2cee635319 (ORCH v1, ARCHIVE)
  arena/01a0d581-fleetyard @ bf97d85962d5e4950fc75374da6b700744b220b5 (worker v1, ENDED
    13:22:24Z) — evidence source only (runs/m5-raw, reports/CORPUS-AUDIT.md)
  arena/01a0d585-fleetyard @ 37e726006cfe002f82b0c019cf503db7272da2ad (boss v1, ENDED
    13:28:05Z) — evidence source only
boot verdict: **FAIL-CLOSED** — record A-2026-09-25-002 does NOT verify byte-exact against
  origin/main. Exactly one of six lines differs (line 6: stub `lane: TBD`, main
  `lane: TBD (agent registers at boot)`). Triggers: boot prompt's own rule
  (mismatch = FAIL-CLOSED) · LAW §1.3 (registry conflict → no new work) · LAW §1B
  (activation is a Grant; grants fail-hard).
authority held: NONE. Not done and not started: M5-R/M4 task cuts, gates, certifications,
  PAUSE/STOP/FREEZE controls, queue/status/TASK-MAP writes, GATES.md entries.
  Permitted and done: read-only diagnosis (archives, main, sibling lane) + these durable
  records + owner alert (LAW §1.3 "owner alerted at next successful push").
nonce: the boot prompt carried the literal placeholder `<NONCE-2>` — no nonce value was
  delivered. Nothing printed, hashed or committed here (custody rule, LAW §1A).
anchor: none supplied in the boot prompt; none carried by the deployed registry.
controls on this lane at boot (resolved per LAW §4.3): `fleet/controls/.keep` and
  `fleet/controls/owner-hash-clarification` — the latter is not a STOP/PAUSE/FREEZE (no
  restriction in force) and, as a relaxing instrument with no nonce_sha256, is
  NON-GRANTING under LAW §1B and fleet2check's own relaxing-control rule.
sibling registration (duty 5, verified read-only): WORKER-2 on arena/01a0d9ce-fleetyard
  @ d1e6289b02940954ffee05e72fc2566737943689 (18:36:27Z) — fail-closed at 18:26Z on the
  same defect, re-verified PASS at main 5fdd00e (its record 001 IS byte-exact), M5-R
  self-served because no ORCH-2 queue exists. See §7 of the verification record.
evidence: fleet/branches/ORCH-2-BOOT-VERIFICATION.md · fleet/alerts/ORCH-2-FAIL-CLOSED.md
