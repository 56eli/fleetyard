# AUDIT-PLAN v2 — remaining campaign (bundle draft v1.0-hub)

Carries v1 milestones M0–M6 with these changes (I11 + review P2):

- CORRECTION: the corpus is 230 transcripts (231st overlay entry is
  manifest.json, not a transcript). All references to "231 transcripts"
  read 230.
- STATUS CARRIED IN: M0 certified (preserved); M1 certified (repaired
  set); M2 ACCEPTED INCOMPLETE (drop-word + speaker/format deferred to
  M4); M3 delivered provisionally — held-out validation REQUIRED before
  any headline rate; M5 raw sweep reproducible (230/230 replayed twice
  independently) — raw signals only, 0 reviewed; M6 not started.

Remaining work, in order:
- [ ] **M5-R — Reviewed findings ledger:** reduce the 1,334 raw signals:
        dedupe, cross-detector merge, adjudicate against cited bytes,
        classify per STANDARDS + LAW §9 (independence rationales for
        HIGH; seeded separated). Output: findings/ ledger, per-transcript.
- [ ] **M4 — Self-improvement loop (formal):** tools/PATTERNS.md — every
        CERTAIN finding becomes a detector rule + held-out fixture;
        per-detector precision tracked; detector promotion requires
        held-out validation (fixed before tuning) + provenance-manifested
        caches (LAW §8); M2 remainder (drop-word, speaker/format) lands
        here.
- [ ] **M6-P — Provisional report:** reports/CORPUS-AUDIT.md marked
        PROVISIONAL, from verified raw counts only: per-detector signal
        counts, by year/detector/transcript hotspots, the taxonomy with
        CERTAIN/HIGH/CANDIDATE strictly separated, and an explicit
        limitations section (unreviewed signals; no estimable corpus-wide
        error rate until M5-R). DELIVERY, never completion (LAW §2).
- [ ] **M6 — Final report:** after M5-R: reviewed error rates per class
        (CERTAIN/HIGH separate; CANDIDATE never blended), by year,
        detector family, transcript hotspots; pattern summary;
        recommendations. The owner's "how bad is it" answer.
- [ ] **Completion manifest (owner-maintained on main):** M0 ✓ (preserved),
        M1 ✓, M2 accepted-incomplete ✓, M5-R, M4, M6-P (accepted
        exclusion possible), M6 — the owner declares campaign completion
        against this manifest (LAW §2.2).

Standing boundaries unchanged from VISION v1 (frozen corpus; stdlib-only,
no network; app rebuild out of scope; finding = citation) + LAW/errata.
Boss re-sequences against the MISSION (no clock cliffs). Schedule truth:
state component status, never percentages without a denominator.
