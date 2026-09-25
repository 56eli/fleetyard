#!/usr/bin/env python3
"""Tests for the sealed holdout split v2 (TASK-019 quantum a) — stdlib unittest."""
import hashlib
import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import m4_split_v2 as sp  # noqa: E402

SEAL = os.path.join(ROOT, "tools", "HELD-OUT-SPLIT-V2.json")
CORPUS = os.path.join(ROOT, "corpus")
V1 = os.path.join(ROOT, "tools", "HELD-OUT-SPLIT.json")


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


class MethodCase(unittest.TestCase):
    """Rule-level checks that need no corpus."""

    def test_salt_is_fresh(self):
        seal = load(SEAL) if os.path.exists(SEAL) else self.skipTest("seal absent")
        self.assertNotEqual(seal["salt"], "fleetyard-m4-holdout-2026-09-25")
        self.assertIn("2026-09-25", seal["salt"])

    def test_bucket_rule_is_published_and_deterministic(self):
        seal = load(SEAL) if os.path.exists(SEAL) else self.skipTest("seal absent")
        name = seal["tuning"][0]
        expected = int(hashlib.sha256((seal["salt"] + name).encode("utf-8")).hexdigest(),
                       16) % seal["mod"]
        self.assertEqual(sp.bucket(name), expected)
        self.assertEqual(seal["method"],
                         "sha256(SALT+basename) mod 5 == 0 -> HOLDOUT; fixture transcripts "
                         "forced to TUNING")

    def test_sets_are_disjoint_and_forced_are_in_tuning(self):
        seal = load(SEAL) if os.path.exists(SEAL) else self.skipTest("seal absent")
        tun, hol = set(seal["tuning"]), set(seal["holdout"])
        self.assertEqual(tun & hol, set())
        forced = set(seal["fixture_transcripts_forced_tuning"])
        self.assertEqual(hol & forced, set())
        self.assertTrue(forced <= tun)
        self.assertEqual(len(tun) + len(hol), seal["counts"]["total"])

    def test_spent_v1_holdout_is_entirely_excluded_from_v2_holdout(self):
        if not os.path.exists(V1):
            self.skipTest("v1 split absent")
        seal = load(SEAL) if os.path.exists(SEAL) else self.skipTest("seal absent")
        v1h = set(load(V1)["holdout"])
        self.assertEqual(v1h & set(seal["holdout"]), set())
        self.assertTrue(v1h <= set(seal["tuning"]))

    def test_re_seal_rule_is_recorded(self):
        seal = load(SEAL) if os.path.exists(SEAL) else self.skipTest("seal absent")
        self.assertIn("VOID", seal["re_seal_rule"])

    def test_manifest_binds_law8_fields(self):
        seal = load(SEAL) if os.path.exists(SEAL) else self.skipTest("seal absent")
        m = seal["manifest"]
        for key in ("run_utc", "tool_sha256", "corpus_zip_sha256", "book_store_sha256",
                    "tool_commit", "main_head", "policy_sha256"):
            self.assertIn(key, m, key)


class CorpusCase(unittest.TestCase):
    @unittest.skipUnless(os.path.isdir(CORPUS), "corpus not extracted")
    def test_corpus_digest_derivation_reproduces(self):
        seal = load(SEAL)
        files = sp.corpus_files(CORPUS)
        self.assertEqual(seal["corpus_files_sha256"],
                         hashlib.sha256(("\n".join(files) + "\n").encode("utf-8")).hexdigest())
        self.assertEqual(seal["corpus_files"], len(files))

    @unittest.skipUnless(os.path.isdir(CORPUS), "corpus not extracted")
    def test_verifier_passes_on_the_committed_seal(self):
        ok, problems = sp.verify(SEAL, CORPUS)
        self.assertTrue(ok, problems)

    @unittest.skipUnless(os.path.isdir(CORPUS), "corpus not extracted")
    def test_verifier_detects_tampering(self):
        seal = load(SEAL)
        seal = dict(seal)
        seal["holdout"] = list(seal["holdout"])
        seal["tuning"] = list(seal["tuning"])
        seal["tuning"].append(seal["holdout"].pop())      # move a holdout name to tuning
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            json.dump(seal, fh)
            path = fh.name
        try:
            ok, problems = sp.verify(path, CORPUS)
            self.assertFalse(ok)
            self.assertTrue(any("bucket mismatch" in p for p in problems))
        finally:
            os.unlink(path)

    @unittest.skipUnless(os.path.isdir(CORPUS), "corpus not extracted")
    def test_rebuild_is_set_stable(self):
        """A rebuild must reproduce the same sets (run_utc differs by design)."""
        seal = load(SEAL)
        fresh = sp.build(CORPUS, "X", "Y", "Z", "W")
        for key in ("tuning", "holdout", "counts", "by_year", "corpus_files_sha256",
                    "fixture_transcripts_forced_tuning"):
            self.assertEqual(fresh[key], seal[key], key)


if __name__ == "__main__":
    unittest.main(verbosity=2)
