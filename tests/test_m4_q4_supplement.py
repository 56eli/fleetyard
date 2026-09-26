#!/usr/bin/env python3
"""Tests for the TASK-020 item-9 q4 holdout §8 supplement — stdlib unittest."""
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import m4_q4_supplement as q4  # noqa: E402

OUT = os.path.join(ROOT, "runs", "m4-q4-holdout")
CORPUS = os.path.join(ROOT, "corpus")
PARTS = ("v1", "drop", "format")


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def have_corpus():
    return os.path.exists(os.path.join(CORPUS, q4.BOOK_STORE_REL))


class SupplementCase(unittest.TestCase):
    def setUp(self):
        path = os.path.join(OUT, q4.SUPPLEMENT)
        if not os.path.exists(path):
            self.skipTest("supplement absent")
        self.doc = load(path)

    def test_top_level_bindings_present(self):
        for key in ("tool_commit", "main_head", "policy_sha256", "corpus_zip_sha256",
                    "book_store_sha256", "split_corpus_files_sha256", "run_utc"):
            self.assertTrue(self.doc.get(key), key)
        self.assertEqual(self.doc["corpus_zip_sha256"], q4.CORPUS_ZIP_SHA)
        self.assertTrue(self.doc["holdout_consumed"])
        self.assertIn("NOT re-run", self.doc["one_shot_discipline"])

    def test_every_part_carries_a_config_and_output_digest(self):
        for part in PARTS:
            row = self.doc["runs"][part]
            self.assertEqual(len(row["config_sha256"]), 64)
            self.assertEqual(len(row["signals_sha256"]), 64)
            self.assertEqual(row["config_sha256"], q4.digest_params(row["config"]))

    def test_v1_holdout_json_is_digested(self):
        row = self.doc["runs"]["v1"]
        self.assertEqual(row["signals_file"], "v1-holdout.json")
        self.assertEqual(row["signals_bytes"], 127733)
        self.assertEqual(len(row["signals_sha256"]), 64)

    def test_toolchain_is_cited_by_lane_and_commit_not_a_path(self):
        chain = self.doc["runs"]["v1"]["toolchain"]
        self.assertTrue(chain["cited_as"].startswith("origin/arena/01a0d581-"))
        self.assertIn("evidence/tools", chain["replaces"])
        self.assertEqual(len(chain["pins"]), 13)
        self.assertIn("13/13", chain["verification"]["result"])
        self.assertIn("ORCH-2", chain["verification"]["orchestrator"])

    def test_b1_zero_is_explicit_with_its_consequence(self):
        sup = self.doc["runs"]["v1"]["per_detector_signal_instances_supplement"]
        self.assertEqual(sup["B1-contradiction"], 0)
        self.assertIn("NO validation", sup["note"])
        self.assertIn("REDIRECT-005", sup["note"])
        self.assertNotIn("B1-contradiction", sup["original_values"])

    def test_detector_counts_in_supplement_match_the_original_provenances(self):
        v1 = load(os.path.join(OUT, "v1-holdout.PROVENANCE.json"))
        drop = load(os.path.join(OUT, "part-holdout-drop.PROVENANCE.json"))
        fmt = load(os.path.join(OUT, "part-holdout-format.PROVENANCE.json"))
        self.assertEqual(self.doc["runs"]["v1"]["config"]["detectors"],
                         v1["detectors"].replace("A1,A2,B1,B2", "A1,A2,B1,B2"))
        self.assertEqual(self.doc["runs"]["drop"]["config"], drop["params"])
        self.assertEqual(self.doc["runs"]["format"]["config"]["rules"], fmt["rules"])

    def test_every_leg_publishes_a_complete_config_with_its_convention(self):
        """item 14 / criterion 20.16: digest note + a note stating what the object covers."""
        for part in PARTS:
            row = self.doc["runs"][part]
            self.assertIn("sort_keys=True", row["config_digest_note"])
            self.assertIn("separators", row["config_digest_note"])
            self.assertTrue(row["config_note"], part)

    def test_format_config_is_the_complete_in_force_configuration(self):
        """The defect: the format leg published `rules` alone (805241dd) while q3 published
        abbreviations + excerpt_chars + rules (8e7e35a2). The object must now cover the module
        constants AND the rules, and must equal q3's published object digest-for-digest."""
        row = self.doc["runs"]["format"]
        self.assertEqual(sorted(row["config"]), ["abbreviations", "excerpt_chars", "rules"])
        self.assertEqual(len(row["config"]["abbreviations"]), 38)
        self.assertEqual(row["config"]["excerpt_chars"], 60)
        self.assertEqual(row["config"]["abbreviations"], sorted(q4.fmt_det.ABBREV))
        self.assertEqual(row["config"]["excerpt_chars"], q4.fmt_det.EXCERPT)
        self.assertNotIn("config_subset_matching_q3", row)
        q3path = os.path.join(ROOT, "runs", "m4-q3-format", "PROVENANCE-SUPPLEMENT.json")
        if os.path.exists(q3path):
            q3 = load(q3path)
            self.assertEqual(row["config"], q3["config"])
            self.assertEqual(row["config_sha256"], q3["config_sha256"])


class VerifyCase(unittest.TestCase):
    def setUp(self):
        if not have_corpus():
            self.skipTest("corpus absent")
        self.root = tempfile.mkdtemp()
        for name in os.listdir(OUT):
            src = os.path.join(OUT, name)
            if os.path.isfile(src):
                shutil.copy(src, os.path.join(self.root, name))
        self.args = type("A", (), {"out": self.root, "corpus": CORPUS,
                                   "archive_ref": q4.ARCHIVE_REF_DEFAULT})()

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def test_verify_passes_on_a_faithful_copy(self):
        self.assertEqual(q4.verify(self.args), 0)

    def test_verify_fails_when_an_output_digest_is_tampered(self):
        path = os.path.join(self.root, q4.SUPPLEMENT)
        doc = load(path)
        doc["runs"]["v1"]["signals_sha256"] = "0" * 64
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(doc, fh)
        self.assertEqual(q4.verify(self.args), 1)

    def test_verify_fails_when_the_b1_zero_is_dropped(self):
        path = os.path.join(self.root, q4.SUPPLEMENT)
        doc = load(path)
        del doc["runs"]["v1"]["per_detector_signal_instances_supplement"][
            "B1-contradiction"]
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(doc, fh)
        self.assertEqual(q4.verify(self.args), 1)

    def test_verify_fails_on_a_wrong_archive_ref(self):
        self.args.archive_ref = "origin/nonexistent-lane"
        self.assertEqual(q4.verify(self.args), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
