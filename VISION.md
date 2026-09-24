# VISION — the fleetyard transcription-integrity audit

Authored 2026-09-24 at the owner's direction; the Boss ratifies or amends at
its first wake. After ratification, THIS file is the measuring stick every
review uses to flag drift.

## The owner's mission (verbatim, 2026-09-24)
> "I want the fleet to audit the docdocgo project i uploaded in there.
> In that project there will also be AI transcription of lectures from David
> R Hawkins. These transcription have errors. I want to know how bad it is
> across the whole corpus. There will also be book texts in the project
> which are 100% reliable. The AI fleet should build and self-improve tools
> to find patterns of mistakes in the AI transcriptions. Then the mistakes
> or possible mistakes need to be listed from 'certain' misquotation to
> 'high confidence' down to 'candidate'. Sentences not making sense is one
> thing, but also internal consistency of the teaching of Hawkins."
> "The Boss agent wants to see work done. The Orchestrator wants for the
> project to be long-term coherent. The worker works."

## The ground truth (owner-stated)
- `corpus/docdocgo/overlays/*.txt` — AI lecture transcriptions (2002–2011),
  ERROR-BEARING. The suspect corpus.
- `corpus/docdocgo/html/merged-book-texts_json_1.js` — book texts, 100%
  reliable per the owner. The doctrine ground truth AND the clean-text
  negative set for tool testing.
- `corpus/docdocgo/extra-sources/*` — Book of Slides OCR variants: side
  UNDECIDED (open item for the owner; treat as suspect until ruled).
- Everything else in `corpus/docdocgo/` (app code, configs, old reports) —
  context only, out of audit scope.

## Role intents (owner's words, mapped)
- WORKER works: builds and runs the audit tooling on its lane (its own
  Arena session branch), files findings.
- ORCHESTRATOR = long-term coherence: gates tools and findings, keeps the
  confidence taxonomy and pattern ledger stable across the whole campaign.
- BOSS = work must get done: watches progress and stall, intervenes on drift.

## Standing boundaries (the Boss polices these)
1. `corpus/**` and `docdocgo-fixes.zip` are FROZEN EVIDENCE — never edited.
2. Tools are Python, standard library ONLY; no network calls, ever.
3. Nothing ever merges, and no agent ever writes `main` (the owner's
   noticeboard). Every role lives on its own Arena session branch — its
   LANE; lanes register themselves in `fleet/branches/<ROLE>.md` on their
   own branch; the owner integrates by checking out certified lane states.
4. The audit is the product. Rebuilding/fixing/deploying the docdocgo APP is
   OUT OF SCOPE (its code is context, not cargo).
5. Every finding carries its evidence or it does not exist (see STANDARDS).
6. Records discipline: logs append-only; deviations disclosed, never silent.
7. Agents never merge; the owner is the root of activation; pills and pause
   are the brakes.

## Open items for the owner
- Which side of the ledger the Book-of-Slides OCR files sit on.
- Whether "misquotation" includes misattributed quotes of OTHER authors
  inside transcripts, or only Hawkins' own teaching (default: only Hawkins'
  teaching, plus any quote the transcript attributes to a book that the book
  contradicts).
