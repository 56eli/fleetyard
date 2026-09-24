# STANDARDS — findings, evidence, and tool quality

## The confidence taxonomy (owner's ladder — never re-defined without a
## recorded errata + a BOSS CONCERN)
- **CERTAIN** — mechanically demonstrable error; at least one hard leg:
  (a) the text is ungrammatical or senseless AND an acoustically near-form
  replacement restores both grammar and doctrinal sense;
  (b) the transcript states something the book texts contradict verbatim on
  the same teaching (cite the book passage);
  (c) the lecture contradicts itself and the near-form resolves it.
- **HIGH CONFIDENCE** — ≥2 independent signals converge (pattern + language
  + doctrine) without a mechanical proof leg.
- **CANDIDATE** — one weak signal; flagged for human review; NEVER counted
  in headline error rates (reported separately always).

## The finding record (a finding is a citation, not a vibe)
Every finding lists: transcript path · location (paragraph index + char
offset) · quoted transcript text (verbatim, bracketed) · suspected intended
text · evidence class (a/b/c per CERTAIN, or the converging signals) ·
detector id · book reference (if doctrinal) · confidence · status
(open/confirmed/discarded — with who and why).

## Tool quality gates (the orchestrator enforces, independently)
1. A detector ships WITH: self-test, fixture results (precision on
   `fixtures/confirmed/`), clean-set results (false positives on
   `fixtures/clean/` — the books are known-good; a detector flagging book
   text is misfiring by definition).
2. The suite (`python3 -m unittest discover -s tests`) is green before
   every push. Never push red. Test count never drops.
3. The orchestrator reproduces detector runs on its own samples; gate
   verdicts quote actual outputs.
4. No detector may read anything but `corpus/**` and write anywhere but the
   outputs the task names. No network. Stdlib only.

## Honesty rules
- Coverage truth: "audited" means detectors ran AND a finding pass reviewed
  the transcript's findings; counts of audited vs pending are always stated.
- Rates are per class. Blending CANDIDATE into a rate is a defect.
- Corpus is frozen: a finding can never be "fixed away" — only confirmed or
  discarded with reasons.
