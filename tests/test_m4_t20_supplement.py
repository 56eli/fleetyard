#!/usr/bin/env python3
"""Tests for the TASK-020 §8 supplements + C2-format filter (items 1, 5b) — stdlib unittest."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import m4_t20_supplement as sup  # noqa: E402

Q2 = os.path.join(ROOT, "runs", "m4-q2-dropword")
Q3 = os.path.join(ROOT, "runs", "m4-q3-format")
CORPUS = os.path.join(ROOT, "corpus")
SPLIT = os.path.join(ROOT, "tools", "HELD-OUT-SPLIT-V2.json")
REQUIRED = ("tool_commit", "main_head", "policy_sha256", "book_store_sha256",
            "corpus_zip_sha256", "split_corpus_files_sha256", "config_sha256",
            "config_digest_note",
            "run_utc", "detector_sha256_at_head", "detector_pin_defect")


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def have_corpus():
    return os.path.isdir(os.path.join(CORPUS, "docdocgo", "overlays"))


class SupplementShapeCase(unittest.TestCase):
    """The published supplements, checked without touching the corpus."""

    def test_both_run_directories_carry_a_supplement(self):
        for d in (Q2, Q3):
            path = os.path.join(d, sup.SUPPLEMENT)
            self.assertTrue(os.path.exists(path), path)
            doc = load(path)
            for key in REQUIRED:
                self.assertTrue(doc.get(key), "%s lacks %s" % (path, key))
            self.assertEqual(doc["holdout_reads"], [])
            self.assertIn("not promotable", doc["status"].lower())

    def test_q2_part_digests_match_the_gates_reproduction(self):
        doc = load(os.path.join(Q2, sup.SUPPLEMENT))
        self.assertEqual(len(doc["parts"]), 6)
        self.assertTrue(doc["parts"]["part-1.json"].startswith("64a97be5"))
        self.assertTrue(doc["parts"]["part-3.json"].startswith("092d6341"))
        self.assertEqual(doc["merge"]["signals_total"], 122)

    def test_q2_config_digest_is_recomputable(self):
        doc = load(os.path.join(Q2, sup.SUPPLEMENT))
        self.assertEqual(doc["config_sha256"], sup.digest_config(doc["config"]))
        self.assertEqual(doc["config"], sup.Q2_PARAMS)

    def test_q2_pin_defect_is_stated_with_the_reproduction_bridge(self):
        doc = load(os.path.join(Q2, sup.SUPPLEMENT))
        defect = doc["detector_pin_defect"]
        self.assertIn("84e5407f", defect["original_pin"])
        self.assertIn("NO committed blob", defect["defect"])
        self.assertIn("byte-identical", defect["attribution_bridge"])

    def test_q3_supplement_states_book_store_is_na_not_omitted(self):
        doc = load(os.path.join(Q3, sup.SUPPLEMENT))
        self.assertIn("book_store_digest_status", doc)
        self.assertIn("N/A", doc["book_store_digest_status"])
        self.assertTrue(doc["book_store_sha256"])
        self.assertIn("c322e053", doc["detector_pin_defect"]["original_pin"])
        self.assertIn("byte-identical",
                      doc["detector_pin_defect"]["attribution_bridge"])

    def test_q3_filter_counts_are_raw_and_filtered(self):
        doc = load(os.path.join(Q3, sup.SUPPLEMENT))["source_inheritance_filter"]
        self.assertEqual(doc["run"]["raw"], 48)
        self.assertEqual(doc["run"]["filtered"], 48)
        self.assertEqual(doc["clean_set"]["misfires_raw"], 1)
        self.assertEqual(doc["clean_set"]["misfires_after_filter"], 0)
        self.assertEqual(doc["clean_set"]["source_inherited"], 1)

    def test_q2_filter_counts_name_the_deferred_bucket(self):
        doc = load(os.path.join(Q2, sup.SUPPLEMENT))["source_inheritance_filter"]
        self.assertEqual((doc["raw"], doc["source_inherited"], doc["deferred_holdout"]),
                         (122, 1, 7))
        self.assertEqual(doc["filtered"], 114)
        self.assertEqual(doc["filtered_if_deferred_were_kept"], 121)

    def test_digest_helper_is_stable_and_order_insensitive(self):
        a = sup.digest_config({"b": 2, "a": 1})
        b = sup.digest_config({"a": 1, "b": 2})
        self.assertEqual(a, b)
        self.assertEqual(len(a), 64)
        self.assertEqual(a, hashlib.sha256(b'{"a":1,"b":2}').hexdigest())


class FilterRuleCase(unittest.TestCase):
    def test_source_inheritance_detects_verbatim_book_text(self):
        """The whole ±30-char window must sit inside the book text."""
        book = "x" * 80
        books = {"slug": book}
        text = "PREFIX" + book
        sig = {"start": 6 + 30, "end": 6 + 34, "quoted": "x"}
        out = sup.source_inheritance(sig, text, books)
        self.assertTrue(out["source_inherited"])
        self.assertEqual(out["books"], ["slug"])

    def test_source_inheritance_is_silent_when_text_differs(self):
        books = {"slug": "xx" * 40}
        sig = {"start": 4, "end": 8, "quoted": "word"}
        out = sup.source_inheritance(sig, "yy some other wording here", books)
        self.assertFalse(out["source_inherited"])


class CorpusCase(unittest.TestCase):
    """verify() end to end on copies (never writes into the committed dirs)."""

    def setUp(self):
        if not have_corpus():
            self.skipTest("corpus absent")
        self.root = tempfile.mkdtemp()
        self.q2 = os.path.join(self.root, "m4-q2-dropword")
        self.q3 = os.path.join(self.root, "m4-q3-format")
        os.makedirs(self.q2)
        os.makedirs(self.q3)
        for src, dst, data in ((Q2, self.q2, "signals.json"),
                               (Q3, self.q3, "signals-v2tuning.json")):
            shutil.copy(os.path.join(src, sup.SUPPLEMENT),
                        os.path.join(dst, sup.SUPPLEMENT))
            shutil.copy(os.path.join(src, data), os.path.join(dst, data))
        self.args = type("A", (), {"corpus": CORPUS, "split": SPLIT,
                                   "q2": self.q2, "q3": self.q3})()

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def test_full_verify_passes(self):
        self.assertEqual(sup.verify(self.args), 0)

    def test_verify_fails_when_a_binding_is_missing(self):
        path = os.path.join(self.q2, sup.SUPPLEMENT)
        doc = load(path)
        doc["tool_commit"] = ""
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(doc, fh)
        self.assertEqual(sup.verify(self.args), 1)

    def test_verify_fails_when_a_filter_count_is_tampered(self):
        path = os.path.join(self.q3, sup.SUPPLEMENT)
        doc = load(path)
        doc["source_inheritance_filter"]["run"]["filtered"] = 47
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(doc, fh)
        self.assertEqual(sup.verify(self.args), 1)

    def test_q3_config_digest_note_reproduces_when_followed_literally(self):
        """Criterion 20.15b: the note must let a reader recompute the number it describes."""
        q3 = load(os.path.join(Q3, sup.SUPPLEMENT))
        note = q3["config_digest_note"]
        self.assertIn("sort_keys=True", note)
        self.assertIn("separators", note)
        for part in ("rules", "excerpt_chars", "abbreviations"):
            self.assertIn(part, note)
        # follow the note literally over the object the file itself publishes
        digest = sup.digest_config(q3["config"])
        self.assertEqual(digest, q3["config_sha256"])
        self.assertEqual(digest, "8e7e35a2795f58b97504af440d804e03beb3f66007db9b615bab731972e6f77f")
        self.assertEqual(sorted(q3["config"]), ["abbreviations", "excerpt_chars", "rules"])
        # ... and the q4 holdout supplement's format leg publishes the same number, so the
        # q3/q4 exposure comparison rests on a digest match rather than an inference
        q4 = load(os.path.join(ROOT, "runs", "m4-q4-holdout", sup.SUPPLEMENT))
        self.assertEqual(q4["runs"]["format"]["config_sha256"], digest)
        self.assertIn("config_digest_note", q4["runs"]["format"])

    def test_q3_generator_pin_names_the_commit_carrying_the_generating_bytes(self):
        """Item 8a's substance: an attribution, not a copy of the sibling artefact's pin."""
        q3 = load(os.path.join(Q3, sup.SUPPLEMENT))
        q2 = load(os.path.join(Q2, sup.SUPPLEMENT))
        pins = q3["generator_pins"]
        self.assertEqual(pins["generator_tool"], "tools/m4_t20_supplement.py")
        commit = pins["generator_tool_commit"]
        blob = subprocess.run(("git", "-C", ROOT, "show", "%s:%s" % (commit, pins["generator_tool"])),
                              capture_output=True).stdout
        self.assertTrue(blob, "the pinned commit must carry the generator")
        self.assertEqual(hashlib.sha256(blob).hexdigest(), pins["generator_tool_sha256"])
        # the q2 supplement is unchanged by this rebuild and keeps its own recorded pin
        self.assertEqual(q2["generator_pins"]["generator_tool_sha256"],
                         q2["generator_pins"]["generator_tool_sha256"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
