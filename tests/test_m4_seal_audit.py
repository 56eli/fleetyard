#!/usr/bin/env python3
"""Tests for `tools/m4_seal_audit.py` — the post-seal integrity check.

Every test builds a toy git repo (no corpus, no network) and asserts what the
audit says about a seal whose fixture file was edited after the seal: append-only
(seal stands, appendix owed), patched (void), a fixture added (void), a
confirmation artefact that postdates the seal (void), or a fixture transcript
sitting in the holdout (void).
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "tools"))
import m4_seal_audit as audit  # noqa: E402


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


class ToyRepo(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp(prefix="m4seal-")
        self.addCleanup(shutil.rmtree, self.repo)
        self.git("init", "-q")
        self.git("config", "user.email", "worker@example.invalid")
        self.git("config", "user.name", "WORKER-2 test")
        self.set_time("2026-09-25T20:00:00+00:00")

    def git(self, *args, env=None):
        e = dict(os.environ)
        if env:
            e.update(env)
        p = subprocess.run(("git", "-C", self.repo) + args, capture_output=True,
                           text=True, env=e)
        if p.returncode != 0 and args[0] not in ("init",):
            raise AssertionError("git %s failed: %s" % (args, p.stderr))
        return p.stdout

    def set_time(self, iso):
        self.git("config", "user.name", "WORKER-2 test")  # keep identity
        os.environ["GIT_AUTHOR_DATE"] = iso
        os.environ["GIT_COMMITTER_DATE"] = iso
        self._time = iso

    def commit(self, iso, msg):
        os.environ["GIT_AUTHOR_DATE"] = iso
        os.environ["GIT_COMMITTER_DATE"] = iso
        self.git("add", "-A")
        self.git("commit", "-q", "-m", msg)

    def write(self, rel, obj):
        path = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            if isinstance(obj, str):
                fh.write(obj)
            else:
                json.dump(obj, fh, indent=1, sort_keys=True)
                fh.write("\n")

    def seal(self, fixture_rel="fixtures/toy.json", holdout=("hold.txt",),
             tuning=("tune.txt",), forced=("fixture1.txt",), cited=None):
        doc = {"salt": "toy-salt", "holdout": list(holdout), "tuning": list(tuning),
               "fixture_transcripts_forced_tuning": list(forced),
               "fixture_sources": {fixture_rel: sha(os.path.join(self.repo, fixture_rel))}}
        if cited:
            doc["note"] = {"artifact": cited, "artifact_sha256": sha(os.path.join(self.repo, cited))}
        self.write("SPLIT.json", doc)
        self.commit("2026-09-25T20:10:00+00:00", "toy seal")

    def run_audit(self):
        return audit.main(["--seal", "SPLIT.json", "--repo", self.repo,
                           "--utc", "2026-09-25T21:00:00Z"])

    def report(self):
        return audit.audit(self.repo, "SPLIT.json", "2026-09-25T21:00:00Z")


class SealAudit(ToyRepo):
    FIXTURES = {"fixtures": [{"id": "D2-001", "verdict": "CERTAIN-leg-d",
                              "transcript": "corpus/overlays/fixture1.txt"}]}

    # ------------------------------------------------------------- standing
    def test_untouched_seal_stands_with_nothing_outstanding(self):
        self.write("fixtures/toy.json", self.FIXTURES)
        self.commit("2026-09-25T20:05:00+00:00", "fixtures")
        self.seal()
        rep = self.report()
        self.assertFalse(rep["seal_void"])
        self.assertEqual(rep["outstanding"], [])
        self.assertEqual(rep["fixture_sources"][0]["status"], "OK")
        self.assertEqual(self.run_audit(), 0)

    def test_append_only_edit_keeps_the_seal_and_owes_an_appendix(self):
        self.write("fixtures/toy.json", self.FIXTURES)
        self.commit("2026-09-25T20:05:00+00:00", "fixtures")
        self.seal()
        doc = json.load(open(os.path.join(self.repo, "fixtures/toy.json"), encoding="utf-8"))
        doc["enacted_leg_note"] = {"task": "append-only annotation"}
        self.write("fixtures/toy.json", doc)
        self.commit("2026-09-25T20:30:00+00:00", "annotation after the seal")
        rep = self.report()
        self.assertFalse(rep["seal_void"])
        self.assertEqual(rep["fixture_sources"][0]["status"], "APPEND-ONLY-AFTER-SEAL")
        self.assertTrue(rep["fixture_sources"][0]["appendix_needed"])
        self.assertIn("seal STANDS", rep["outstanding"][0])
        self.assertIn("append-only", rep["outstanding"][0])
        # a dated note naming both digests discharges the appendix
        live = sha(os.path.join(self.repo, "fixtures/toy.json"))
        sealed = rep["fixture_sources"][0]["sealed_sha256"]
        self.write("tools/HELD-OUT-SPLIT-V2-NOTE-2026-09-26.md",
                   "sealed %s\nlive %s\n" % (sealed, live))
        self.commit("2026-09-25T20:35:00+00:00", "dated note")
        rep2 = self.report()
        self.assertFalse(rep2["seal_void"])
        self.assertIn("dated note on file", rep2["fixture_sources"][0]["status"])
        self.assertFalse(rep2["fixture_sources"][0]["appendix_needed"])
        self.assertEqual(rep2["outstanding"], [])
        self.assertIn("nothing further", rep2["notes_on_file"][0])
        self.assertIn("dated note on file", rep2["verdict"]["one_line"])

    # ----------------------------------------------------------------- void
    def test_patched_sealed_content_voids_the_seal(self):
        self.write("fixtures/toy.json", self.FIXTURES)
        self.commit("2026-09-25T20:05:00+00:00", "fixtures")
        self.seal()
        doc = json.load(open(os.path.join(self.repo, "fixtures/toy.json"), encoding="utf-8"))
        doc["fixtures"][0]["verdict"] = "CANDIDATE"          # value changed after the seal
        self.write("fixtures/toy.json", doc)
        self.commit("2026-09-25T20:30:00+00:00", "patch")
        rep = self.report()
        self.assertTrue(rep["seal_void"])
        self.assertEqual(rep["fixture_sources"][0]["status"], "PATCHED-AFTER-SEAL")
        self.assertIn("patched", rep["void_reasons"][0])
        self.assertEqual(self.run_audit(), 1)

    def test_new_fixture_after_the_seal_voids_it(self):
        self.write("fixtures/toy.json", self.FIXTURES)
        self.commit("2026-09-25T20:05:00+00:00", "fixtures")
        self.seal()
        doc = json.load(open(os.path.join(self.repo, "fixtures/toy.json"), encoding="utf-8"))
        doc["fixtures"].append({"id": "D2-005", "verdict": "CERTAIN-leg-d",
                                "transcript": "corpus/overlays/new.txt"})
        self.write("fixtures/toy.json", doc)
        self.commit("2026-09-25T20:30:00+00:00", "new fixture")
        rep = self.report()
        self.assertTrue(rep["seal_void"])
        self.assertEqual(rep["fixture_sources"][0]["status"], "NEW-FIXTURE-AFTER-SEAL")
        self.assertEqual(rep["fixture_sources"][0]["new_fixture_ids"], ["D2-005"])

    def test_confirmation_artifact_dating_after_the_seal_voids_it(self):
        # a citation to a PRE-seal adjudication artefact is clean ...
        self.write("runs/adjudication.json", {"verdict": "CERTAIN-leg-d"})
        doc = dict(self.FIXTURES)
        doc["cited"] = {"artifact": "runs/adjudication.json",
                        "artifact_sha256": sha(os.path.join(self.repo, "runs/adjudication.json"))}
        self.write("fixtures/toy.json", doc)
        self.commit("2026-09-25T20:05:00+00:00", "fixtures citing a pre-seal artefact")
        self.seal()
        pre = self.report()
        self.assertFalse(pre["seal_void"], pre["void_reasons"])
        self.assertEqual(pre["confirmation_artifacts"][0]["relation_to_seal"], "pre-seal")
        self.assertTrue(pre["confirmation_artifacts"][0]["digest_matches_head"])
        # ... but a confirmation artefact committed AFTER the seal voids it, even when
        # the edit that cites it is purely append-only
        self.write("runs/adjudication-v2.json", {"verdict": "CERTAIN-leg-d"})
        self.commit("2026-09-25T20:40:00+00:00", "confirmation after the seal")
        doc = json.load(open(os.path.join(self.repo, "fixtures/toy.json"), encoding="utf-8"))
        doc["cited_v2"] = {"artifact": "runs/adjudication-v2.json",
                           "artifact_sha256": sha(os.path.join(self.repo,
                                                               "runs/adjudication-v2.json"))}
        self.write("fixtures/toy.json", doc)
        self.commit("2026-09-25T20:42:00+00:00", "append-only citation of the post-seal artefact")
        rep = self.report()
        self.assertTrue(rep["seal_void"])
        self.assertEqual(len(rep["void_reasons"]), 1, rep["void_reasons"])
        self.assertIn("postdates the seal", rep["void_reasons"][0])
        self.assertEqual(rep["fixture_sources"][0]["status"], "APPEND-ONLY-AFTER-SEAL")

    def test_fixture_transcript_in_the_holdout_voids_it(self):
        self.write("fixtures/toy.json", self.FIXTURES)
        self.commit("2026-09-25T20:05:00+00:00", "fixtures")
        self.seal(holdout=("hold.txt", "fixture1.txt"))       # fixture transcript in holdout
        rep = self.report()
        self.assertTrue(rep["seal_void"])
        self.assertEqual(rep["membership"]["forced_intersect_holdout"], ["fixture1.txt"])

    def test_internally_inconsistent_seal_is_void(self):
        self.write("fixtures/toy.json", self.FIXTURES)
        self.commit("2026-09-25T20:05:00+00:00", "fixtures")
        doc = {"salt": "toy-salt", "holdout": ["hold.txt"], "tuning": ["tune.txt"],
               "fixture_transcripts_forced_tuning": ["fixture1.txt"],
               "fixture_sources": {"fixtures/toy.json": "0" * 64}}
        self.write("SPLIT.json", doc)
        self.commit("2026-09-25T20:10:00+00:00", "seal records a digest its own blob contradicts")
        rep = self.report()
        self.assertTrue(rep["seal_void"])
        self.assertIn("internally inconsistent", " ".join(rep["void_reasons"]))


if __name__ == "__main__":
    unittest.main()
