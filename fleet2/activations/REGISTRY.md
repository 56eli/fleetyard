# FLEET2 ACTIVATION REGISTRY — append-only; never rewrite; newest wins

FORMAT v0 (owner note, 2026-09-25): these simple records are the
authoritative activation law. The hash-chain/ANCHOR mechanics of LAW §1A
and fleet2check's registry-chain module are DEFERRED to policy 2.0.1;
until then fleet2check registry-chain output is ADVISORY. The binding
mechanism in v0 is: this main-record text (verified byte-exact at boot)
+ the owner-held nonce delivered only in the boot prompt, posture
UNHASHED-OWNER-CHAT-ONLY.

## A-2026-09-25-001
issued_utc: 2026-09-25 (owner, pre-boot) | role: WORKER | activation: WORKER-2
policy: fleet2/POLICY-MANIFEST.sha256 (as deployed; sha256 0fe20a6057ec9fa2)
nonce_hash: UNHASHED-OWNER-CHAT-ONLY
predecessors: arena/01a0d581-fleetyard ENDED (HALT-2026-09-25.md)
lane: TBD (agent registers at boot)

## A-2026-09-25-002
issued_utc: 2026-09-25 (owner, pre-boot) | role: ORCHESTRATOR | activation: ORCH-2
policy: fleet2/POLICY-MANIFEST.sha256 (as deployed; sha256 0fe20a6057ec9fa2)
nonce_hash: UNHASHED-OWNER-CHAT-ONLY
predecessors: arena/01a0d5b7-fleetyard ENDED (final handoff fcc9834); arena/01a0d582-fleetyard ARCHIVE
lane: TBD (agent registers at boot)

## A-2026-09-25-003
issued_utc: 2026-09-25 (owner, pre-boot) | role: BOSS | activation: BOSS-2
policy: fleet2/POLICY-MANIFEST.sha256 (as deployed; sha256 0fe20a6057ec9fa2)
nonce_hash: UNHASHED-OWNER-CHAT-ONLY
predecessors: arena/01a0d585-fleetyard ENDED (37e7260)
lane: TBD (agent registers at boot)
