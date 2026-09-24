# AUDIT-PLAN — the campaign, in milestones

One task = one focused unit of work on the worker lane (tools, fixtures,
findings batches, or reports). The orchestrator cuts tasks from these
milestones; the Boss may re-order via REDIRECT.

- [ ] **M0 — Corpus inventory (baseline):** census table committed on the
      worker lane (`tools/CORPUS.md`): per-file list (path, bytes, year,
      title parse), totals cross-checked against the bootstrap battery;
      anomalies noted (empty files, duplicates, encoding).
- [ ] **M1 — Tooling foundation:** loaders: transcript reader (plain text →
      paragraphs with offsets), book-store reader (parses the JS-embedded
      book JSON into slug→text); tokenizer; the fixture set: ≥15 CONFIRMED
      errors hand-found by reading 3 full transcripts (each with the full
      evidence chain), stored as `fixtures/confirmed/`; a clean-set sample
      from the book store (`fixtures/clean/`).
- [ ] **M2 — Detector family A (language integrity):** detectors for broken
      grammar / nonsense spans, repeated-word and drop-word artifacts,
      acoustic-confusion candidates (homophone/near-form pairs via stdlib
      difflib + a hand-built confusion list), speaker/format anomalies.
      Each detector: self-test + fixtures precision + clean-set
      false-positive rate.
- [ ] **M3 — Detector family B (doctrinal consistency):** book-passage
      retrieval (stdlib TF-IDF over the book store); transcript claims vs
      retrieved book passages: contradiction and garble detection; Hawkins
      terminology drift (calibrate/calibration, levels of consciousness,
      ego vs Self, etc.); transcript-quotes-a-book checks (the
      misquotation detector).
- [ ] **M4 — Self-improvement loop:** `tools/PATTERNS.md` — every CERTAIN
      finding's pattern becomes a new detector rule + regression fixture;
      per-detector precision tracked over time; detector changes gated on
      the fixture set (no precision regressions).
- [ ] **M5 — Full-corpus sweep:** all detectors over all 231 transcripts;
      findings ledger `findings/` (one file per transcript + a master index)
      with the confidence taxonomy; per-transcript error densities;
      dedupe/cross-detector merge.
- [ ] **M6 — The report:** `reports/CORPUS-AUDIT.md` — how bad is it:
      error rates by confidence class (CERTAIN/HIGH separate, CANDIDATE
      reported separately, never blended), by year, by detector family, by
      transcript (hotspots); the full classified findings list; pattern
