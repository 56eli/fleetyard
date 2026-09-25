#!/usr/bin/env python3
"""Tests for the M4-q3 shipping evidence rebuild (TASK-014 q3 gaps) — stdlib unittest."""
import json
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import m4_q3_evidence as ev  # noqa: E402

CORPUS = os.path.join(ROOT, "corpus")
SPLIT = os.path.join(ROOT, "tools", "HELD-OUT-SPLIT-V2.json")
OUT = os.path.join(ROOT, "runs", "m4-q3-format")
SPLIT_V1 = os.path.join(ROOT, "tools", "HELD-OUT-SPLIT.json")


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def have_corpus():
    return os.path.isdir(os.path.join(CORPUS, "docdocgo", "overlays"))


def have_books():
    return os.path.exists(os.path.join(CORPUS, "docdocgo", "html",
                                       "merged-book-texts_json_1.js"))


class PureCase(unittest.TestCase):
    """Checks that need no corpus."""

    def test_split_integrity_rejects_overlap(self):
        doc = {"tuning": ["a.txt"], "holdout": ["a.txt"], "corpus_files_sha256": "x"}
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "split.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(doc, fh)
            with self.assertRaises(SystemExit):
                ev.load_split(path)

    def test_split_requires_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "split.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump({"tuning": [], "holdout": []}, fh)
            with self.assertRaises(SystemExit):
                ev.load_split(path)

    def test_committed_provenance_carries_the_law8_bindings(self):
        prov = load(os.path.join(OUT, ev.PROV_NAME))
        for key in ("tool_commit", "main_head", "policy_sha256",
                    "detector_sha256", "split_corpus_files_sha256",
                    "corpus_zip_sha256", "run_utc"):
            self.assertTrue(prov.get(key), "manifest lacks %s" % key)
        self.assertEqual(prov["outputs"]["signals_file"], ev.SIGNALS_NAME)
        self.assertEqual(len(prov["outputs"]["signals_sha256"]), 64)
        self.assertEqual(prov["holdout_reads"], [])
        self.assertTrue(prov["holdout_enforced"])
        self.assertNotEqual(prov["tool_commit"], "PENDING")

    def test_committed_eval_is_honest_about_what_it_is(self):
        doc = load(os.path.join(OUT, ev.EVAL_NAME))
        self.assertIn("not promotable", doc["status"])
        self.assertEqual(doc["fixture_recall"]["fixtures"], 16)
        self.assertEqual(doc["clean_set"]["passages"], 59)
        self.assertIn("NOT an independent FP rate", doc["clean_set"]["reading"])
        self.assertEqual(doc["historic_signals_sha256"],
                         "86c8f57dea9443f3b9758add19dbfe01e75b1369b144c74a58d1735b5a8c15ee")

    def test_historic_run_is_cited_by_digest_not_replayed(self):
        doc = load(os.path.join(OUT, ev.EVAL_NAME))
        historic = load(os.path.join(OUT, "signals.json"))
        self.assertEqual(doc["historic_signals_sha256"],
                         ev.m5r.sha256_file(os.path.join(OUT, "signals.json")))
        # the new run is a different artefact over the v2 tuning half
        self.assertNotEqual(doc["signals_sha256"], doc["historic_signals_sha256"])
        self.assertEqual(len(historic), 193)
        split = load(SPLIT)
        self.assertEqual(len(split["tuning"]), 197)

    def test_probe_table_publishes_patterns_and_flags(self):
        doc = load(os.path.join(OUT, ev.EVAL_NAME))
        probes = doc["rejected_rule_probes"]["probes"]
        self.assertEqual([p["probe"] for p in probes],
                         [p[0] for p in ev.PROBES])
        for p in probes:
            self.assertTrue(p["pattern"])
            self.assertIn(p["flags"], ("0", "re.IGNORECASE"))
            self.assertTrue(p["examples"] or p["hits"] == 0)


class CorpusCase(unittest.TestCase):
    """Checks that need the materialised corpus (skip otherwise)."""

    def setUp(self):
        if not have_corpus():
            self.skipTest("corpus absent")
        self.split = ev.load_split(SPLIT)
        self.guard = ev.HoldoutGuard(CORPUS, self.split["holdout"])

    def test_guard_refuses_holdout_names(self):
        name = self.split["holdout"][0]
        with self.assertRaises(SystemExit):
            self.guard.text(name)
        # and refuses a corpus-relative path to a holdout file
        with self.assertRaises(SystemExit):
            self.guard.text("corpus/docdocgo/overlays/" + name)

    def test_guard_refuses_unknown_names(self):
        with self.assertRaises(SystemExit):
            self.guard.text("nosuchtranscript.txt")

    def test_guard_normalises_fixture_paths(self):
        name = self.split["tuning"][0]
        self.assertTrue(self.guard.text("corpus/docdocgo/overlays/" + name))

    def test_fixture_recall_is_measured_and_zero(self):
        recall = ev.fixture_recall(
            ev.fixtures.load_json(ev.fixtures.CONFIRMED_PATH), self.guard)
        self.assertEqual(recall["fixtures"], 16)
        self.assertEqual(recall["hits"], 0)
        for row in recall["detail"]:
            self.assertIn("hit", row)
            self.assertEqual(bool(row["signals"]), row["hit"])

    def test_v2_holdout_reuses_nothing_spent_and_the_run_never_touches_it(self):
        """The v2 holdout shares no file with the spent v1 holdout, and a v2
        tuning run reads only v2 tuning files."""
        v1 = load(SPLIT_V1)
        self.assertEqual(set(self.split["holdout"]) & set(v1["holdout"]), set())
        guard = ev.HoldoutGuard(CORPUS, self.split["holdout"])
        per_file, total, per_rule, texts = ev.tuning_run(self.split, guard)
        self.assertEqual(len(per_file), len(self.split["tuning"]))
        self.assertEqual(set(per_file) & set(self.split["holdout"]), set())
        self.assertEqual(set(guard.reads) & set(self.split["holdout"]), set())

    def test_holdout_guard_covers_every_read_of_a_build(self):
        guard = ev.HoldoutGuard(CORPUS, self.split["holdout"])
        ev.tuning_run(self.split, guard)
        ev.fixture_recall(ev.fixtures.load_json(ev.fixtures.CONFIRMED_PATH), guard)
        self.assertEqual(set(guard.reads) & set(self.split["holdout"]), set())

    def test_rebuild_is_byte_stable_for_a_fixed_utc(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = type("A", (), {
                "corpus": CORPUS, "split": SPLIT, "out": tmp,
                "utc": "2026-09-25T00:00:00Z", "tool_commit": "deadbeef",
                "main_head": "deadbeef", "policy_sha": "0" * 64})()
            ev.build(args)
            first = {n: ev.m5r.sha256_file(os.path.join(tmp, n))
                     for n in (ev.SIGNALS_NAME, ev.PROV_NAME, ev.EVAL_NAME)}
            ev.build(args)
            second = {n: ev.m5r.sha256_file(os.path.join(tmp, n))
                      for n in (ev.SIGNALS_NAME, ev.PROV_NAME, ev.EVAL_NAME)}
            self.assertEqual(first, second)

    def test_verify_accepts_the_committed_artefacts(self):
        args = type("A", (), {"corpus": CORPUS, "split": SPLIT, "out": OUT})()
        self.assertEqual(ev.verify(args), 0)

    def test_verify_rejects_a_tampered_eval(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in (ev.EVAL_NAME, ev.SIGNALS_NAME, ev.PROV_NAME):
                shutil.copy(os.path.join(OUT, name), os.path.join(tmp, name))
            path = os.path.join(tmp, ev.EVAL_NAME)
            doc = load(path)
            doc["signals_total"] += 1
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(doc, fh)
            args = type("A", (), {"corpus": CORPUS, "split": SPLIT, "out": tmp})()
            self.assertEqual(ev.verify(args), 1)


class BookCase(unittest.TestCase):
    """Clean-set and confound checks (need corpus + book store)."""

    def setUp(self):
        if not (have_corpus() and have_books()):
            self.skipTest("corpus or book store absent")
        self.books = ev.loaders.read_book_store()
        self.split = ev.load_split(SPLIT)

    def test_clean_set_scores_59_passages_and_one_misfire(self):
        clean = ev.fixtures.load_json(ev.fixtures.CLEAN_PATH)
        res = ev.clean_run(clean, self.books)
        self.assertEqual(res["passages"], 59)
        self.assertEqual(res["false_positives"], 1)
        fp = res["fp_detail"][0]
        self.assertEqual(fp["id"], "CL-026")
        self.assertEqual(fp["rule"], "R1-glued-period")

    def test_the_single_clean_misfire_is_also_in_the_book_store(self):
        """The R1 misfire is the book's own typography — recorded, not hidden."""
        clean = ev.fixtures.load_json(ev.fixtures.CLEAN_PATH)
        res = ev.clean_run(clean, self.books)
        row = [d for d in res["detail"] if d["id"] == "CL-026"][0]
        glue = row["signals"][0]["quoted"]
        self.assertEqual(glue, "r.W")
        self.assertIn("power.When", self.books[row["slug"]])
        self.assertIn(glue, self.books[row["slug"]])

    def test_confound_control_reports_uninformative(self):
        guard = ev.HoldoutGuard(CORPUS, self.split["holdout"])
        ctl = ev.confound_control(
            ev.fixtures.load_json(ev.fixtures.CONFIRMED_PATH), self.books, guard)
        self.assertEqual(ctl["with_book_ref"], 15)
        self.assertEqual(ctl["quote_in_book"], 15)
        self.assertEqual(ctl["ctx50_in_book"], 0)
        self.assertEqual(ctl["verdict"], "UNINFORMATIVE")

    def test_committed_confound_block_matches_a_fresh_measurement(self):
        doc = load(os.path.join(OUT, ev.EVAL_NAME))
        guard = ev.HoldoutGuard(CORPUS, self.split["holdout"])
        per_file, total, per_rule, texts = ev.tuning_run(self.split, guard)
        fresh = ev.book_confound(per_file, texts, self.books)
        self.assertEqual(doc["book_store_confound"]["signals_ctx50"],
                         fresh["signals_ctx50"])
        self.assertEqual(doc["book_store_confound"]["per_rule"], fresh["per_rule"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
