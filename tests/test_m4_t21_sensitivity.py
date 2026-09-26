#!/usr/bin/env python3
"""Tests for `tools/m4_t21_sensitivity.py` — the TASK-021 sensitivity map.

Everything here runs on a toy corpus + toy split in a temp dir: the real map reads the v2 tuning
half, and no test may touch the real holdout. The properties under test are the ones the task's
acceptance criteria name: the holdout refusal (by construction — a holdout transcript cannot be in
the scratch tree), the grid arithmetic (raw = source-filtered + inherited = shape-excluded +
after-shape; sites + duplicates = raw), the dedupe rule, and that the published grid is the grid
the task asks for.
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import m4_t21_sensitivity as t21  # noqa: E402

BOOK = ("Spiritual purity has no interest in the personal lives of aspirants, or in clothing, "
        "dress, style, sex lives, economics, family patterns, lifestyles, or dietary habits and "
        "preferences of the students who come to study here in this hall. Courage is the critical "
        "point of integrity at two hundred and above, where the energy of the student turns away "
        "from the small self and toward the light that is always present in the quiet hours "
        "before dawn.")
TUNE_TEXT = BOOK.replace("aspirants, ", "") + " Wait____"
HOLD_TEXT = BOOK


def build_toy(root):
    corpus = os.path.join(root, "corpus")
    overlays = os.path.join(corpus, "docdocgo", "overlays")
    html = os.path.join(corpus, "docdocgo", "html")
    os.makedirs(overlays)
    os.makedirs(html)
    with open(os.path.join(overlays, "tune.txt"), "w", encoding="utf-8") as fh:
        fh.write(TUNE_TEXT)
    with open(os.path.join(overlays, "hold.txt"), "w", encoding="utf-8") as fh:
        fh.write(HOLD_TEXT)
    with open(os.path.join(html, "merged-book-texts_json_1.js"), "w", encoding="utf-8") as fh:
        fh.write("const the_json_obj_books = {\n  \"toy_book\": `%s`\n};\n" % BOOK)
    split = {"salt": "toy-salt", "tuning": ["tune.txt"], "holdout": ["hold.txt"],
             "counts": {"total": 2, "tuning": 1, "holdout": 1},
             "corpus_files_sha256": "toy"}
    split_path = os.path.join(root, "SPLIT.json")
    with open(split_path, "w", encoding="utf-8") as fh:
        json.dump(split, fh)
    return corpus, split_path


def args_for(root, corpus, split_path, out, scratch, setting="shipped"):
    return type("A", (), {"setting": setting, "corpus": corpus, "split": split_path,
                          "out": out, "scratch": scratch,
                          "utc": "2026-09-26T03:00:00Z"})()


class ToySensitivity(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="m4t21-")
        self.addCleanup(shutil.rmtree, self.root)
        self.corpus, self.split_path = build_toy(self.root)
        self.out = os.path.join(self.root, "out")
        self.scratch = os.path.join(self.root, "scratch")

    # ------------------------------------------------------- holdout discipline
    def test_scratch_corpus_holds_only_the_tuning_half(self):
        split = t21.load(self.split_path)
        doc = t21.build_scratch(self.scratch, self.corpus, split)
        present = sorted(os.listdir(os.path.join(self.scratch, "docdocgo", "overlays")))
        self.assertEqual(present, ["tune.txt"])
        self.assertEqual(doc["tuning_transcripts"], 1)
        self.assertEqual(doc["holdout_present"], [])
        self.assertNotIn("hold.txt", present)

    def test_scratch_refuses_when_a_holdout_name_is_present(self):
        split = t21.load(self.split_path)
        t21.build_scratch(self.scratch, self.corpus, split)
        # plant the holdout transcript in the tree being walked: the build must refuse
        shutil.copy(os.path.join(self.corpus, "docdocgo", "overlays", "hold.txt"),
                    os.path.join(self.scratch, "docdocgo", "overlays", "hold.txt"))
        with self.assertRaises(SystemExit) as ctx:
            t21.build_scratch(self.scratch, self.corpus, split)
        self.assertIn("holdout transcripts present in the scratch corpus", str(ctx.exception))

    def test_split_with_a_name_in_both_halves_is_refused(self):
        split = t21.load(self.split_path)
        split["holdout"] = ["hold.txt", "tune.txt"]        # a name in both halves
        with self.assertRaises(SystemExit) as ctx:
            t21.build_scratch(self.scratch, self.corpus, split)
        self.assertIn("names in both halves", str(ctx.exception))

    # ------------------------------------------------------------ one setting
    def test_build_writes_a_part_with_recomputable_arithmetic(self):
        rc = t21.build(args_for(self.root, self.corpus, self.split_path, self.out, self.scratch))
        self.assertEqual(rc, 0)
        part = json.load(open(os.path.join(self.out, "parts", "shipped.json"), encoding="utf-8"))
        self.assertEqual(part["setting"], "shipped")
        self.assertEqual(part["config"], dict(t21.FIXED, **t21.SHIPPED))
        self.assertEqual(part["config_sha256"], t21.config_digest(part["config"]))
        self.assertEqual(part["holdout_reads"], [])
        self.assertTrue(part["holdout_enforced"])
        self.assertEqual(part["files_opened"]["holdout"], [])
        self.assertEqual(part["transcripts_read"], 1)
        self.assertEqual(part["raw_signals"],
                         part["after_source_filter"] + part["source_inherited"])
        self.assertEqual(part["raw_signals"],
                         part["shape_excluded"] + part["after_shape_exclusions"])
        self.assertEqual(part["distinct_sites"] + part["duplicate_sites"], part["raw_signals"])
        # the toy drop is detected, so the map is not vacuously empty
        self.assertGreaterEqual(part["raw_signals"], 1, part["per_transcript_counts"])
        self.assertNotIn("hold.txt", part["per_transcript_counts"])
        self.assertRegex(part["run_utc"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        self.assertIn("date -u", part["run_utc_source"])
        self.assertEqual(part["reproducible_content_sha256"], t21.content_digest(part))
        self.assertEqual(sorted(part["environment_fields"]), sorted(t21.ENVIRONMENT_FIELDS))

    def test_holdout_never_reaches_the_detector(self):
        """The audit hook must see holdout-transcript opens as zero, over a whole build."""
        t21.build(args_for(self.root, self.corpus, self.split_path, self.out, self.scratch))
        part = json.load(open(os.path.join(self.out, "parts", "shipped.json"), encoding="utf-8"))
        holdout_opens = [p for p in part["files_opened"]["holdout"]]
        self.assertEqual(holdout_opens, [])
        self.assertGreater(part["files_opened"]["total"], 0, "the audit recorded nothing")

    # ------------------------------------------------------------ dedupe rule
    def test_site_key_is_the_dedupe_rule(self):
        sig = {"start": 10, "end": 20, "dropped_words": ["quite"]}
        same = {"start": 10, "end": 20, "dropped_words": ["quite"], "note": "different note"}
        other_word = {"start": 10, "end": 20, "dropped_words": ["by"]}
        other_span = {"start": 10, "end": 21, "dropped_words": ["quite"]}
        self.assertEqual(t21.site_key("t.txt", sig), t21.site_key("t.txt", same))
        self.assertNotEqual(t21.site_key("t.txt", sig), t21.site_key("t.txt", other_word))
        self.assertNotEqual(t21.site_key("t.txt", sig), t21.site_key("t.txt", other_span))
        self.assertNotEqual(t21.site_key("t.txt", sig), t21.site_key("u.txt", sig))
        self.assertIn("transcript basename", t21.SITE_KEY_NOTE)

    def test_grid_is_the_published_one(self):
        grid = dict(t21.GRID)
        self.assertEqual(t21.SHIPPED, {"min_flank": 3, "min_ratio": 0.85, "min_matched": 10})
        self.assertEqual(grid["shipped"], {})
        self.assertEqual(sorted(n for n in grid if n != "shipped"),
                         ["flank-2", "flank-5", "flank-8", "matched-14", "matched-8",
                          "ratio-0.80", "ratio-0.90"])
        for name, over in grid.items():
            self.assertEqual(len(over) <= 1, True, name)      # one parameter at a time
        self.assertEqual(t21.config_for("flank-2")["min_flank"], 2)
        self.assertEqual(t21.config_for("matched-14")["min_matched"], 14)
        self.assertEqual(t21.config_for("ratio-0.90")["min_ratio"], 0.90)
        # everything the grid does not vary stays at the shipped/fixed point
        for name in grid:
            cfg = t21.config_for(name)
            for key in ("window", "stride", "min_score", "top_k", "max_drop"):
                self.assertEqual(cfg[key], t21.FIXED[key], "%s/%s" % (name, key))

    # --------------------------------------------------------------- merge/verify
    def test_merge_refuses_an_incomplete_grid(self):
        os.makedirs(os.path.join(self.out, "parts"))
        t21.build(args_for(self.root, self.corpus, self.split_path, self.out, self.scratch))
        with self.assertRaises(SystemExit) as ctx:
            t21.merge(type("A", (), {"out": self.out, "split": self.split_path,
                                     "corpus": self.corpus,
                                     "utc": "2026-09-26T03:00:00Z", "tool_commit": "toyc0mm",
                                     "main_head": "toymain", "policy_sha": "toypolicy",
                                     "generator_pins": None, "part_generator_pins": None})())
        self.assertIn("the grid is not complete", str(ctx.exception))

    def test_verify_recomputes_or_fails(self):
        """A complete toy grid merges and verifies; a tampered part fails verify."""
        parts = os.path.join(self.out, "parts")
        os.makedirs(parts)
        for name, _o in t21.GRID:
            t21.build(args_for(self.root, self.corpus, self.split_path, self.out, self.scratch,
                               setting=name))
        args = type("A", (), {"out": self.out, "split": self.split_path, "corpus": self.corpus,
                              "utc": "2026-09-26T03:00:00Z", "tool_commit": "toyc0mm",
                              "main_head": "toymain", "policy_sha": "toypolicy",
                              "generator_pins": None, "part_generator_pins": None})()
        self.assertEqual(t21.merge(args), 0)
        ev = json.load(open(os.path.join(self.out, "EVAL.json"), encoding="utf-8"))
        self.assertEqual(ev["holdout_reads"], [])
        self.assertEqual(ev["split"]["holdout_transcripts"], 1)
        self.assertIn("NOT interchangeable", ev["denominators"]["rule"])
        self.assertEqual(ev["restrictions"]["no_threshold_chosen"], True)
        self.assertEqual(ev["part_reproducible_content_sha256"]["shipped"],
                         json.load(open(os.path.join(parts, "shipped.json"), encoding="utf-8"))
                         ["reproducible_content_sha256"])
        self.assertIn("environment fields", ev["reproducibility"]["how"])
        self.assertIn("wall time", ev["reproducibility"]["why"])
        self.assertIn("no precision, rate", ev["restrictions"]["no_rate"])
        self.assertEqual(t21.verify(type("A", (), {"out": self.out})()), 0)
        # tamper: the anchor's raw count no longer closes with its filters
        path = os.path.join(parts, "shipped.json")
        doc = json.load(open(path, encoding="utf-8"))
        doc["raw_signals"] += 1
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(doc, fh)
        self.assertEqual(t21.verify(type("A", (), {"out": self.out})()), 1)

    def test_readme_states_both_denominators_and_no_rate(self):
        parts = os.path.join(self.out, "parts")
        os.makedirs(parts)
        for name, _o in t21.GRID:
            t21.build(args_for(self.root, self.corpus, self.split_path, self.out, self.scratch,
                               setting=name))
        t21.merge(type("A", (), {"out": self.out, "split": self.split_path, "corpus": self.corpus,
                                 "utc": "2026-09-26T03:00:00Z", "tool_commit": "toyc0mm",
                                 "main_head": "toymain", "policy_sha": "toypolicy",
                                 "generator_pins": None, "part_generator_pins": None})())
        text = open(os.path.join(self.out, "README.md"), encoding="utf-8").read()
        self.assertIn("v1 tuning half", text)
        self.assertIn("v2 tuning half", text)
        self.assertIn("not interchangeable", text)
        self.assertIn("PROVISIONAL-UNGATED", text)
        self.assertIn("not a tuning run", text)
        self.assertIn("197", text)


if __name__ == "__main__":
    unittest.main()
