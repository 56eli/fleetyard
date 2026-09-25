#!/usr/bin/env python3
"""Tests for the M4-q2 shipping evidence rebuild (TASK-020 items 2/4/5a/5c) — stdlib unittest."""
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import m4_q2_evidence as q2  # noqa: E402

OUT = os.path.join(ROOT, "runs", "m4-q2-dropword")
CORPUS = os.path.join(ROOT, "corpus")


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def have_corpus():
    return os.path.isdir(os.path.join(CORPUS, "docdocgo", "overlays"))


class AdjudicationCase(unittest.TestCase):
    """Shape classification from the signal record alone (no corpus)."""

    def signals(self):
        return load(os.path.join(OUT, "signals.json"))

    def test_consistent_case_closes(self):
        sig = {"quoted": "the quick brown", "suspected": "the very quick brown",
               "dropped_words": ["very"]}
        out = q2.adjudicate(sig)
        self.assertEqual(out["kind"], "consistent")
        self.assertTrue(out["deletion_closes"])

    def test_typographic_apostrophe_is_not_a_defect(self):
        """The book uses U+2019 where the transcript uses '; a real drop in the
        same window must still close (this shape cost the gate five signals)."""
        sig = {"quoted": "because it's an", "suspected": "because it\u2019s very an",
               "dropped_words": ["very"]}
        out = q2.adjudicate(sig)
        self.assertEqual(out["kind"], "consistent")
        self.assertTrue(out["deletion_closes"])

    def test_dropped_token_still_present_is_excluded(self):
        sig = {"quoted": "evidence of", "suspected": "evidence; evidence of",
               "dropped_words": ["evidence"]}
        out = q2.adjudicate(sig)
        self.assertEqual(out["kind"], "dropped-token-not-missing")
        self.assertIn("EXCLUDED", out["counting"])

    def test_partial_overlap_is_relabelled(self):
        sig = {"quoted": "make sudden", "suspected": "make sudden jumps, sudden",
               "dropped_words": ["sudden", "jumps"]}
        out = q2.adjudicate(sig)
        self.assertEqual(out["kind"], "partial-overlap")
        self.assertIn("RE-LABELLED", out["counting"])

    def test_gates_three_named_defects_are_reproduced(self):
        hits = {}
        for name, sigs in self.signals().items():
            for sig in sigs:
                if sig["start"] in (2574, 54983, 55220):
                    hits[sig["start"]] = q2.adjudicate(sig)["kind"]
        self.assertEqual(sorted(hits), [2574, 54983, 55220])
        self.assertEqual(set(hits.values()), {"dropped-token-not-missing"})

    def test_shape_counts_reconcile_to_the_gate_figure(self):
        counts = q2.shape_counts(self.signals())
        excluded = counts["dropped-token-not-missing"]
        relabelled = counts["partial-overlap"] + counts["gate-boundary-excluded"]
        self.assertEqual(sum(counts.values()), 122)
        self.assertEqual(122 - excluded - relabelled, 113)
        self.assertEqual(counts["gate-boundary-excluded"], 1)

    def test_boundary_item_is_named_and_justified(self):
        name, offset, reason = q2.GATE_BOUNDARY_ITEMS[0]
        self.assertEqual(offset, 40831)
        self.assertIn("one-third", reason)
        self.assertTrue(name.endswith(".txt"))


class CommittedEvidenceCase(unittest.TestCase):
    """The published EVAL/manifest, checked without re-running the corpus pass."""

    def setUp(self):
        self.doc = load(os.path.join(OUT, q2.EVIDENCE_NAME))
        self.prov = load(os.path.join(OUT, q2.PROV_NAME))

    def test_fixture_recall_is_zero_and_labelled_in_sample(self):
        fr = self.doc["fixture_recall"]
        self.assertEqual((fr["hits"], fr["fixtures"]), (0, 16))
        self.assertIn("IN-SAMPLE", fr["label"])
        self.assertIn("never recall evidence", fr["label"])

    def test_cf015_statement_says_why_it_missed(self):
        row = [r for r in self.doc["fixture_recall"]["detail"]
               if r["fixture"] == "CF-015"][0]
        self.assertFalse(row["hit"])
        self.assertIn("NO insertion op", row["required_statement"])
        self.assertEqual(row["diagnosis"]["best"]["alignment_ops"]["replace"], 2)

    def test_clean_set_and_filter_counts(self):
        cs = self.doc["clean_set"]
        self.assertEqual((cs["misfires"], cs["passages"]), (3, 59))
        self.assertEqual(cs["misfires_after_source_filter"], 0)
        ids = sorted(h["id"] for h in cs["raw_misfires_detail"])
        self.assertEqual(ids, ["CL-034", "CL-035", "CL-055"])
        self.assertTrue(all(h["source_inherited"] for h in cs["raw_misfires_detail"]))

    def test_shipped_run_filter_is_raw_and_filtered(self):
        f = self.doc["source_inheritance_filter"]["shipped_run"]
        self.assertEqual((f["raw"], f["inherited"], f["deferred"]), (122, 1, 7))
        self.assertEqual(f["filtered"], 114)

    def test_holdout_bucket_rows_are_deferred_not_measured(self):
        rows = self.doc["shape_adjudication"]["signals"]
        deferred = [r for r in rows if "DEFERRED" in
                    r["source_inheritance"].get("status", "")]
        self.assertEqual(len(deferred), 7)
        self.assertTrue(all("holdout" in r["source_inheritance"]["status"]
                            for r in deferred))

    def test_manifest_carries_law8_bindings_and_pin_defect(self):
        for key in ("tool_commit", "main_head", "policy_sha256", "corpus_zip_sha256",
                    "split_corpus_files_sha256", "book_store_sha256", "config_sha256"):
            self.assertTrue(self.prov.get(key), "manifest lacks %s" % key)
        self.assertIn("84e5407f", self.prov["detector_sha256_original_pin_defect"])
        self.assertEqual(self.prov["holdout_reads"], [])
        self.assertIn("not promotable", self.prov["status"].lower())

    def test_no_rate_or_precision_language_creeps_in(self):
        blob = json.dumps(self.doc)
        for banned in ("precision:", "recall rate", "omission count of"):
            self.assertNotIn(banned, blob)


class CorpusCase(unittest.TestCase):
    def setUp(self):
        if not have_corpus():
            self.skipTest("corpus absent")
        self.split = q2.q3ev.load_split(
            os.path.join(ROOT, "tools", "HELD-OUT-SPLIT-V2.json"))
        self.guard = q2.q3ev.HoldoutGuard(CORPUS, self.split["holdout"])
        self.books = q2.m5r.parse_book_store(
            os.path.join(CORPUS, q2.BOOK_STORE_REL))
        self.index = q2.book_index(self.books)

    def test_the_v2_holdout_is_never_opened(self):
        q2.fixture_recall(q2.fixtures.load_json(q2.fixtures.CONFIRMED_PATH),
                          self.guard, self.index)
        self.assertEqual(set(self.guard.reads) & set(self.split["holdout"]), set())

    def test_clean_set_source_inheritance_decomposes(self):
        clean = q2.fixtures.load_json(q2.fixtures.CLEAN_PATH)
        res = q2.clean_run(clean, self.books, self.index)
        self.assertEqual(res["hits"], 3)
        self.assertTrue(all(h["source_inherited"] for h in res["hits_detail"]))

    def test_fixture_recall_reproduces_zero_with_diagnoses(self):
        res = q2.fixture_recall(q2.fixtures.load_json(q2.fixtures.CONFIRMED_PATH),
                                self.guard, self.index)
        self.assertEqual((res["hits"], res["fixtures"]), (0, 16))
        misses = [r for r in res["detail"] if not r["hit"]]
        self.assertEqual(len(misses), 16)
        self.assertTrue(all("diagnosis" in r for r in misses))

    def test_committed_eval_matches_a_fresh_adjudication(self):
        committed = load(os.path.join(OUT, q2.EVIDENCE_NAME))["shape_adjudication"]
        self.assertEqual(committed["counts"],
                         dict(sorted(q2.shape_counts(load(
                             os.path.join(OUT, "signals.json"))).items())))
        self.assertEqual(committed["countable_shape_consistent"], 113)


class TamperCase(unittest.TestCase):
    def setUp(self):
        if not have_corpus():
            self.skipTest("corpus absent")
        import shutil
        import tempfile
        self.tmp = tempfile.mkdtemp()
        for name in (q2.EVIDENCE_NAME, q2.PROV_NAME, "signals.json"):
            shutil.copy(os.path.join(OUT, name), os.path.join(self.tmp, name))
        self.args = type("A", (), {"corpus": CORPUS,
                                   "split": os.path.join(ROOT, "tools",
                                                         "HELD-OUT-SPLIT-V2.json"),
                                   "out": self.tmp})()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_verify_passes_on_a_faithful_copy(self):
        self.assertEqual(q2.verify(self.args), 0)

    def test_verify_fails_on_a_tampered_clean_set_count(self):
        path = os.path.join(self.tmp, q2.EVIDENCE_NAME)
        doc = load(path)
        doc["clean_set"]["misfires"] = 0
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(doc, fh)
        self.assertEqual(q2.verify(self.args), 1)

    def test_verify_fails_on_a_tampered_shape_count(self):
        path = os.path.join(self.tmp, q2.EVIDENCE_NAME)
        doc = load(path)
        doc["shape_adjudication"]["counts"]["consistent"] = 1
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(doc, fh)
        self.assertEqual(q2.verify(self.args), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
