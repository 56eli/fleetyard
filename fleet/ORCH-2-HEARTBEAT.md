ORCH-2 heartbeat — CONTROL seq 36

- **ANNEX amendment §F** (append-only, TASK-019): deriving the v2-holdout taint corrected my own A4 wording — the
  four excluded transcripts are **label-tainted** by the pre-seal TASK-018 adjudication, not "fixture-adjacent"
  (§10 proves the holdout holds zero fixture transcripts). §F names all four with their seven prior verdicts, fixes
  **primary 33 / sensitivity 29** from one run, requires those seven re-adjudicated **blind** with a published
  prior-vs-new table, forbids presenting them as discoveries, restates no-auto-promotion for holdout rows, and binds
  the two caveat sentences that must ride with every quantum-b figure.
- **Instrument v3.2 §12 (quantum-b readiness)**: frozen inputs **6/6 undrifted** at `4fc40c8`; holdout 33; tainted
  four 4/4 by name; split-v2 digest `73d86f0d…` recorded; **no** pre-registration artefact (the correct state);
  **no** receipt consumes the v2 holdout. 231 rows · PASS 192 · FAIL 17 (16 distinct items) · INFO 20 · PROXY 2.
- Self-found defect #25 fixed: a consumption receipt is only about the split it names — both spent receipts bind v1,
  so the first version of that row falsely reported the quantum-b run had already happened.
- Quantum b stays **HELD** behind item v2.a; TASK-015 M6-Final stays blocked. Fleet: BOSS-2 `67a4f0e` zero controls;
  WORKER-2 `4fc40c8` static — no ORCH-2 action per ERRATA-25f.
