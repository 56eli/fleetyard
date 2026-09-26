#!/usr/bin/env python3
"""Tests for `tools/m4_one_shot_v2.py` — the TASK-019b one-shot harness.

The harness is built and tested here WITHOUT consuming any real holdout: every
test runs on a tiny toy corpus in a temp dir (a toy book, two toy transcripts, a
toy split). The properties under test are the refusals that protect the
one-shot discipline (thresholds frozen before the run, single attempt, no
post-freeze detector edit), the scoring rules (hand verdicts only, seeded
separated from independent, CANDIDATE never blended) and the receipt verify.
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "tools"))
import m4_one_shot_v2 as one  # noqa: E402

BOOK = ("Spiritual purity has no interest in the personal lives of aspirants, or in "
        "clothing, dress, style, sex lives, economics, family patterns, lifestyles, or "
        "dietary habits and preferences of the students who come to study here in this "
        "hall. Courage is the critical point of integrity at two hundred and above, "
        "where the energy of the student turns away from the small self and toward the "
        "light that is always present in the quiet hours before dawn.")
# dropped word + two format artifacts (space before comma, glued comma)
HOLDOUT_TEXT = (BOOK.replace("aspirants, ", "")
                .replace("sex lives, economics", "sex lives , economics")
                .replace("economics, family", "economics,family") + " Wait____")
TUNE_TEXT = BOOK


def build_toy(root):
    corpus = os.path.join(root, "corpus")
    os.makedirs(os.path.join(corpus, "docdocgo", "overlays"))
    os.makedirs(os.path.join(corpus, "docdocgo", "html"))
    with open(os.path.join(corpus, "docdocgo", "overlays", "hold.txt"), "w",
              encoding="utf-8") as fh:
        fh.write(HOLDOUT_TEXT)
    with open(os.path.join(corpus, "docdocgo", "overlays", "tune.txt"), "w",
              encoding="utf-8") as fh:
        fh.write(TUNE_TEXT)
    with open(os.path.join(corpus, "docdocgo", "html",
                           "merged-book-texts_json_1.js"), "w", encoding="utf-8") as fh:
        fh.write("const the_json_obj_books = {\n  \"toy_book\": `%s`\n};\n" % BOOK)
    split = {"salt": "toy-salt", "tuning": ["tune.txt"], "holdout": ["hold.txt"],
             "counts": {"total": 2, "tuning": 1, "holdout": 1},
             "corpus_files_sha256": "toy"}
    split_path = os.path.join(root, "SPLIT.json")
    with open(split_path, "w", encoding="utf-8") as fh:
        json.dump(split, fh)
    excl = os.path.join(root, "EXCLUSIONS.json")
    with open(excl, "w", encoding="utf-8") as fh:
        json.dump({"excluded_transcripts": []}, fh)
    # §G2/O-5: a toy companion note, bound by the freeze like the seal appendix is
    companion = os.path.join(root, "SEAL-APPENDIX-toy.md")
    with open(companion, "w", encoding="utf-8") as fh:
        fh.write("toy seal appendix: both digests named, append-only, the re-seal rule evaluated\n")
    return corpus, split_path, excl, companion


def freeze(root, corpus, split_path, out, excl=None, companion=None):
    return one.main(["freeze", "--split", split_path, "--out", out,
                     "--exclusions", excl or os.path.join(root, "EXCLUSIONS.json"),
                     "--companion", companion or os.path.join(root, "SEAL-APPENDIX-toy.md"),
                     "--repo", root,
                     "--utc", "2026-09-25T22:00:00Z", "--tool-commit", "toyc0mm",
                     "--main-head", "toymain", "--policy-sha", "toypolicy"])


def run(root, corpus, split_path, out, excl=None, **kw):
    argv = ["run", "--split", split_path, "--out", out, "--corpus", corpus,
            "--exclusions", excl or os.path.join(root, "EXCLUSIONS.json"),
            "--tool-commit", "toyc0mm", "--utc", "2026-09-25T22:00:05Z"]
    for k, v in kw.items():
        argv += ["--" + k.replace("_", "-"), v]
    return one.main(argv)


class OneShotHarness(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="m4oneshot-")
        self.addCleanup(shutil.rmtree, self.root)
        self.corpus, self.split_path, self.excl, self.companion = build_toy(self.root)
        self.out = os.path.join(self.root, "out")
        self.labels = os.path.join(self.root, "labels.json")

    def _freeze_and_run(self):
        freeze(self.root, self.corpus, self.split_path, self.out)
        run(self.root, self.corpus, self.split_path, self.out)
        with open(os.path.join(self.out, one.SIGNALS), encoding="utf-8") as fh:
            return json.load(fh)

    # ---------------------------------------------------------------- freeze
    def test_freeze_binds_split_detectors_and_refuses_overwrite(self):
        freeze(self.root, self.corpus, self.split_path, self.out)
        with open(os.path.join(self.out, one.THRESHOLDS), encoding="utf-8") as fh:
            frozen = json.load(fh)
        self.assertEqual(frozen["split_salt"], "toy-salt")
        self.assertEqual(sorted(frozen["detectors"]), ["C1-drop", "C2-format"])
        self.assertEqual(frozen["detectors"]["C1-drop"]["params"]["min_flank"], 3)
        self.assertEqual(frozen["adjudication_protocol"]["verdicts"],
                         ["confirmed", "discarded"])
        with self.assertRaises(SystemExit) as ctx:
            freeze(self.root, self.corpus, self.split_path, self.out)
        self.assertIn("refusing to overwrite", str(ctx.exception))

    # ------------------------------------------------------------ run refusals
    def test_run_refuses_without_a_freeze(self):
        with self.assertRaises(SystemExit) as ctx:
            run(self.root, self.corpus, self.split_path, self.out)
        self.assertIn("thresholds must be recorded before the run", str(ctx.exception))
        self.assertFalse(os.path.exists(os.path.join(self.out, one.RECEIPT)))

    def test_run_refuses_a_second_time_and_names_the_rule(self):
        self._freeze_and_run()
        with self.assertRaises(SystemExit) as ctx:
            run(self.root, self.corpus, self.split_path, self.out)
        msg = str(ctx.exception)
        self.assertIn("already holds a consumption receipt", msg)
        self.assertIn("NEW SPLIT", msg)

    def test_run_refuses_a_detector_edited_after_the_freeze(self):
        freeze(self.root, self.corpus, self.split_path, self.out)
        path = os.path.join(self.out, one.THRESHOLDS)
        with open(path, encoding="utf-8") as fh:
            frozen = json.load(fh)
        frozen["detectors"]["C2-format"]["module_sha256"] = "0" * 64
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(frozen, fh)
        with self.assertRaises(SystemExit) as ctx:
            run(self.root, self.corpus, self.split_path, self.out)
        self.assertIn("changed after the freeze", str(ctx.exception))

    def test_run_refuses_when_the_split_no_longer_matches_the_freeze(self):
        freeze(self.root, self.corpus, self.split_path, self.out)
        other = os.path.join(self.root, "SPLIT-OTHER.json")
        with open(self.split_path, encoding="utf-8") as fh:
            split = json.load(fh)
        split["holdout"] = ["tune.txt"]
        split["tuning"] = ["hold.txt"]
        with open(other, "w", encoding="utf-8") as fh:
            json.dump(split, fh)
        with self.assertRaises(SystemExit) as ctx:
            run(self.root, self.corpus, other, self.out)
        self.assertIn("does not match the frozen record", str(ctx.exception))

    # ------------------------------------------------------- run + receipt
    def test_run_once_produces_signals_receipt_and_review_queue(self):
        signals = self._freeze_and_run()
        drop = [s for s in signals["C1-drop"]["hold.txt"]
                if s.get("dropped_words") == ["aspirants"]]
        self.assertEqual(len(drop), 1, "the toy drop was not detected")
        self.assertEqual([s["rule"] for s in signals["C2-format"]["hold.txt"]],
                         ["R5-space-before-comma", "R7-glued-comma",
                          "R4-underscore-run"])
        with open(os.path.join(self.out, one.RECEIPT), encoding="utf-8") as fh:
            receipt = json.load(fh)
        self.assertTrue(receipt["holdout_consumed"])
        self.assertEqual(receipt["one_shot"]["attempt"], 1)
        self.assertEqual(receipt["holdout_reads"], ["hold.txt"])
        self.assertEqual(receipt["holdout_transcripts"], 1)
        self.assertEqual(receipt["split_salt"], "toy-salt")
        self.assertEqual(receipt["tool_commit"], "toyc0mm")
        self.assertNotIn("tune.txt", receipt["holdout_reads"])
        self.assertTrue(os.path.exists(os.path.join(self.out, one.REVIEW)))
        self.assertEqual(one.verify(type("A", (), {"out": self.out,
                                                   "split": self.split_path,
                                                   "exclusions": self.excl})()), 0)

    def test_run_writes_nothing_outside_the_out_dir(self):
        before = {}
        for dirpath, _dirs, files in os.walk(self.corpus):
            for f in files:
                p = os.path.join(dirpath, f)
                before[p] = os.path.getsize(p)
        split_before = open(self.split_path, "rb").read()
        self._freeze_and_run()
        after = {}
        for dirpath, _dirs, files in os.walk(self.corpus):
            for f in files:
                p = os.path.join(dirpath, f)
                after[p] = os.path.getsize(p)
        self.assertEqual(before, after)
        self.assertEqual(split_before, open(self.split_path, "rb").read())
        self.assertEqual(sorted(os.listdir(self.out)),
                         sorted([one.THRESHOLDS, one.RECEIPT, one.SIGNALS, one.REVIEW]))

    def test_pre_registered_exclusion_shrinks_the_evaluated_holdout(self):
        with open(self.excl, "w", encoding="utf-8") as fh:
            json.dump({"excluded_transcripts": ["hold.txt"]}, fh)
        freeze(self.root, self.corpus, self.split_path, self.out)
        # hold.txt IS a holdout member, so the run proceeds with an empty evaluated set
        run(self.root, self.corpus, self.split_path, self.out)
        with open(os.path.join(self.out, one.RECEIPT), encoding="utf-8") as fh:
            receipt = json.load(fh)
        self.assertEqual(receipt["holdout_excluded"], ["hold.txt"])
        self.assertEqual(receipt["holdout_evaluated"], 0)
        self.assertEqual(receipt["holdout_reads"], [])

    def test_exclusions_changed_after_the_freeze_are_refused(self):
        freeze(self.root, self.corpus, self.split_path, self.out)
        with open(self.excl, "w", encoding="utf-8") as fh:
            json.dump({"excluded_transcripts": ["hold.txt"]}, fh)
        with self.assertRaises(SystemExit) as ctx:
            run(self.root, self.corpus, self.split_path, self.out)
        self.assertIn("pre-registered exclusions changed after the freeze", str(ctx.exception))

    # ------------------------------------------------------------- scoring
    def _write_labels(self, mapping):
        with open(self.labels, "w", encoding="utf-8") as fh:
            json.dump(mapping, fh)

    def test_score_refuses_bad_verdicts_and_missing_reasons(self):
        self._freeze_and_run()
        self._write_labels({"C1-drop/hold.txt#1": {"verdict": "maybe", "reason": "x"}})
        with self.assertRaises(SystemExit) as ctx:
            one.main(["score", "--out", self.out, "--labels", self.labels])
        self.assertIn("allowed: ['confirmed', 'discarded']", str(ctx.exception))
        self._write_labels({"C1-drop/hold.txt#1": {"verdict": "confirmed"}})
        with self.assertRaises(SystemExit) as ctx:
            one.main(["score", "--out", self.out, "--labels", self.labels])
        self.assertIn("carries no reason", str(ctx.exception))

    def test_score_separates_seeded_candidate_and_counts(self):
        self._freeze_and_run()
        # one confirmed independent drop, one discarded independent format signal,
        # one seeded format signal, one format signal left unlabelled (CANDIDATE)
        self._write_labels({
            "C1-drop/hold.txt#1": {"verdict": "confirmed",
                                   "reason": "hand read: word absent in the book span",
                                   "citation": "toy_book"},
            "C2-format/hold.txt#1": {"verdict": "discarded",
                                     "reason": "hand read: editorial spacing, no defect"},
            "C2-format/hold.txt#2": {"verdict": "confirmed",
                                     "reason": "hand read: overlaps a confirmed fixture",
                                     "seeded": True},
        })
        one.main(["score", "--out", self.out, "--labels", self.labels])
        with open(os.path.join(self.out, one.SCORE), encoding="utf-8") as fh:
            score = json.load(fh)
        c2 = score["detectors"]["C2-format"]
        self.assertEqual(score["detectors"]["C1-drop"]["independent"],
                         {"confirmed": 1, "discarded": 0, "precision": "1/1"})
        self.assertEqual(c2["independent"], {"confirmed": 0, "discarded": 1,
                                             "precision": "0/1"})
        self.assertEqual(c2["seeded_excluded"], {"confirmed": 1, "discarded": 0})
        self.assertEqual(c2["label_coverage"], "2/3")
        self.assertEqual(c2["candidate_unlabelled"], 1)
        self.assertEqual(len(score["detectors"]["C2-format"]["fp_examples"]), 1)
        self.assertIn("never blended", score["protocol"]["rate"])

    # -------------------------------------------------------------- verify
    def test_verify_fails_on_tampering(self):
        self._freeze_and_run()
        args = type("A", (), {"out": self.out, "split": self.split_path,
                              "exclusions": self.excl})()
        sig_path = os.path.join(self.out, one.SIGNALS)
        with open(sig_path, "rb") as fh:
            original = fh.read()
        with open(sig_path, "wb") as fh:
            fh.write(original + b" ")
        self.assertEqual(one.verify(args), 1)
        with open(sig_path, "wb") as fh:
            fh.write(original)
        self.assertEqual(one.verify(args), 0)
        th_path = os.path.join(self.out, one.THRESHOLDS)
        with open(th_path, "rb") as fh:
            frozen = fh.read()
        doc = json.loads(frozen)
        doc["split_salt"] = "tampered"
        with open(th_path, "w", encoding="utf-8") as fh:
            json.dump(doc, fh)
        self.assertEqual(one.verify(args), 1)
        with open(th_path, "wb") as fh:
            fh.write(frozen)
        self.assertEqual(one.verify(args), 0)

    # ------------------------------------------------- §G2/O-5 + item v2.g
    def test_freeze_binds_the_companion_note_and_run_refuses_a_stale_one(self):
        """§G2/O-5: the seal is immutable, so the freeze must bind the note beside it."""
        freeze(self.root, self.corpus, self.split_path, self.out)
        with open(os.path.join(self.out, one.THRESHOLDS), encoding="utf-8") as fh:
            frozen = json.load(fh)
        bound = frozen["companion_notes"]
        self.assertEqual(len(bound), 1, bound)
        note = bound[0]
        self.assertEqual(note["path"], self.companion.replace(os.sep, "/"))
        self.assertEqual(note["sha256"], one.sha(self.companion))
        self.assertIn("commit_source", note)
        self.assertIn("commit_utc_source", note)
        self.assertIn("§G2/O-5", frozen["companion_notes_rule"])
        # a note that moved after the freeze stops the run
        with open(self.companion, "a", encoding="utf-8") as fh:
            fh.write("an edit after the freeze\n")
        with self.assertRaises(SystemExit) as ctx:
            run(self.root, self.corpus, self.split_path, self.out)
        self.assertIn("companion note", str(ctx.exception))
        self.assertIn("changed after the freeze", str(ctx.exception))
        # ... and so does a note that was deleted
        os.remove(self.companion)
        with self.assertRaises(SystemExit) as ctx:
            run(self.root, self.corpus, self.split_path, self.out)
        self.assertIn("bound by the freeze is missing", str(ctx.exception))

    def test_freeze_refuses_an_absent_companion_note(self):
        with self.assertRaises(SystemExit) as ctx:
            freeze(self.root, self.corpus, self.split_path, self.out,
                   companion=os.path.join(self.root, "not-there.md"))
        self.assertIn("companion note", str(ctx.exception))
        self.assertIn("is absent", str(ctx.exception))
        self.assertFalse(os.path.exists(os.path.join(self.out, one.THRESHOLDS)))

    def test_run_refuses_when_the_frozen_parameters_changed(self):
        """v2.g(i): the parameters branch was ambiguous with the module-digest branch."""
        freeze(self.root, self.corpus, self.split_path, self.out)
        path = os.path.join(self.out, one.THRESHOLDS)
        with open(path, encoding="utf-8") as fh:
            frozen = json.load(fh)
        frozen["detectors"]["C1-drop"]["params"]["min_flank"] = 99   # record edited, module untouched
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(frozen, fh)
        with self.assertRaises(SystemExit) as ctx:
            run(self.root, self.corpus, self.split_path, self.out)
        self.assertIn("parameters changed after the freeze", str(ctx.exception))

    def test_run_refuses_a_partial_holdout_read(self):
        """v2.g(ii): the refusal that protects the denominator (one-shot => never re-run)."""
        with open(self.split_path, encoding="utf-8") as fh:
            split = json.load(fh)
        split["holdout"] = ["hold.txt", "tune.txt"]      # a frozen holdout of two
        split["tuning"] = []
        split["counts"] = {"total": 2, "tuning": 0, "holdout": 2}
        with open(self.split_path, "w", encoding="utf-8") as fh:
            json.dump(split, fh)
        freeze(self.root, self.corpus, self.split_path, self.out)
        real = one.c2_detectors.evaluate

        def reads_one(name, corpus_dir, split_path):     # a detector that read 1 of the 2
            per_file, _reads = real(name, corpus_dir, split_path)
            per_file = {k: v for k, v in per_file.items() if k == "hold.txt"}
            return per_file, sorted(per_file)

        one.c2_detectors.evaluate = reads_one
        try:
            with self.assertRaises(SystemExit) as ctx:
                run(self.root, self.corpus, self.split_path, self.out)
        finally:
            one.c2_detectors.evaluate = real
        msg = str(ctx.exception)
        self.assertIn("not the frozen holdout set of 2", msg)
        self.assertIn("refusing to score a partial read", msg)
        self.assertFalse(os.path.exists(os.path.join(self.out, one.RECEIPT)))

    def test_run_refuses_exclusions_that_are_not_holdout_members(self):
        """v2.g(iii): a wrongly-scoped exclusion would silently shrink the denominator."""
        with open(self.excl, "w", encoding="utf-8") as fh:
            json.dump({"excluded_transcripts": ["tune.txt"]}, fh)
        freeze(self.root, self.corpus, self.split_path, self.out)
        with self.assertRaises(SystemExit) as ctx:
            run(self.root, self.corpus, self.split_path, self.out)
        self.assertIn("pre-registered exclusions are not holdout members", str(ctx.exception))
        self.assertFalse(os.path.exists(os.path.join(self.out, one.RECEIPT)))

    def test_score_refuses_a_partial_or_substituted_read(self):
        """v2.g(iv): the score-side half of the denominator guard."""
        self._freeze_and_run()
        sig_path = os.path.join(self.out, one.SIGNALS)
        with open(sig_path, encoding="utf-8") as fh:
            signals = json.load(fh)
        original = json.dumps(signals, ensure_ascii=False, sort_keys=True, indent=1) + "\n"
        # (a) a signals file that covers fewer transcripts than the receipt evaluated
        with open(sig_path, "w", encoding="utf-8") as fh:
            json.dump({}, fh)
        self._write_labels({"C1-drop/hold.txt#1": {"verdict": "confirmed", "reason": "x"}})
        with self.assertRaises(SystemExit) as ctx:
            one.main(["score", "--out", self.out, "--labels", self.labels])
        self.assertIn("covers 0 transcript(s), not the 1 the receipt evaluated", str(ctx.exception))
        self.assertIn("refusing to score a partial read", str(ctx.exception))
        # (b) the right shape, but not the bytes the receipt bound
        with open(sig_path, "w", encoding="utf-8") as fh:
            fh.write(original + " ")
        with self.assertRaises(SystemExit) as ctx:
            one.main(["score", "--out", self.out, "--labels", self.labels])
        self.assertIn("the signals file is not the one the receipt bound", str(ctx.exception))
        # (c) labels written against another read must not be scored against this one
        with open(sig_path, "w", encoding="utf-8") as fh:
            fh.write(original)
        self._write_labels({"C1-drop/gone.txt#1": {"verdict": "confirmed", "reason": "x"}})
        with self.assertRaises(SystemExit) as ctx:
            one.main(["score", "--out", self.out, "--labels", self.labels])
        self.assertIn("name no signal in this run", str(ctx.exception))
        # (d) the unmodified pair still scores, so the refusal is not spurious
        self._write_labels({"C1-drop/hold.txt#1": {"verdict": "confirmed", "reason": "hand read"}})
        self.assertEqual(one.main(["score", "--out", self.out, "--labels", self.labels]), 0)



if __name__ == "__main__":
    unittest.main()
