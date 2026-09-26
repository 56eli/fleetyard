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

    # ---------------------------------------- repairs asked for by GATE CYCLE I
    # (items v2.c, v2.d, v2.e, v2.a(iii) 2nd half, v2.b - each pinned by the check
    #  that would have caught the defect, so the repair cannot silently regress)
    def test_every_mention_is_checked_even_without_a_paired_digest(self):
        """v2.e: the unpaired mention used to sit outside the post-seal void check."""
        self.write("notes/summary.json", {"note": "confirmation summary"})
        self.commit("2026-09-25T20:05:00+00:00", "the confirmation artefact")
        cited = dict(self.FIXTURES)
        # a citation with NO paired digest, exactly the shape the old census walked past
        cited["adjudication_summary_2026_09_25"] = {"artifact": "notes/summary.json",
                                                    "where": "the confirmation summary"}
        self.write("fixtures/toy.json", cited)
        self.commit("2026-09-25T20:06:00+00:00", "fixtures citing it")
        self.seal()
        rep = self.report()
        self.assertEqual(rep["artifact_mention_census"]["mentions"], 1)
        self.assertEqual(rep["artifact_mention_census"]["unpaired_mentions"], 1)
        row = rep["artifact_mentions"][0]
        self.assertEqual(row["json_path"], "/adjudication_summary_2026_09_25")
        self.assertEqual(row["keys_citing"], ["artifact"])
        self.assertFalse(row["digest_asserted"])
        self.assertTrue(row["digest_matches_head"])
        self.assertEqual(row["authored_relation_to_seal"], "pre-seal")
        self.assertFalse(rep["seal_void"])
        # now touch the cited artefact AFTER the seal: the unpaired mention must void the seal
        self.write("notes/summary.json", {"note": "confirmation summary, extended"})
        self.commit("2026-09-25T20:40:00+00:00", "post-seal extension of the cited artefact")
        rep2 = self.report()
        self.assertTrue(rep2["seal_void"])
        self.assertIn("postdates the seal", " ".join(rep2["void_reasons"]))
        self.assertIn("unpaired mention", rep2["artifact_mentions"][0]["digest_source"])

    def test_appendix_must_cite_the_reports_exact_audit_stamp(self):
        """v2.c: a report and its appendix naming different times for one audit."""
        self.write("fixtures/toy.json", self.FIXTURES)
        self.commit("2026-09-25T20:05:00+00:00", "fixtures")
        self.seal()
        self.write("runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md",
                   "| SEAL-AUDIT.json | see the file (audit utc `2026-09-25T20:00:00Z`) |\n")
        self.commit("2026-09-25T20:20:00+00:00", "appendix with a rounded stamp")
        rep = self.report()                       # audit stamp is 2026-09-25T21:00:00Z
        self.assertFalse(rep["appendix_audit_utc_check"]["cited_identically"])
        self.assertTrue(any("v2.c" in o for o in rep["outstanding"]))
        self.write("runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md",
                   "| SEAL-AUDIT.json | audit utc 2026-09-25T21:00:00Z (supersedes "
                   "`2026-09-25T20:00:00Z`) |\n")
        self.commit("2026-09-25T20:25:00+00:00", "appendix cites the exact stamp")
        rep2 = self.report()
        self.assertTrue(rep2["appendix_audit_utc_check"]["cited_identically"])
        self.assertEqual(rep2["appendix_audit_utc_check"]["unmarked_conflicting_citations"], [])
        self.assertEqual([o for o in rep2["outstanding"] if "v2.c" in o], [])

    def test_tool_commit_points_at_the_blob_at_head(self):
        """v2.d: `tool_commit` must be stated, and the blob at it must equal the tool at head."""
        self.write("fixtures/toy.json", self.FIXTURES)
        self.commit("2026-09-25T20:05:00+00:00", "fixtures")
        self.write("tools/m4_seal_audit.py", "# the audit tool, stub edition\n")
        self.commit("2026-09-25T20:06:00+00:00", "the tool")
        tool_commit = self.git("rev-parse", "HEAD").strip()
        self.seal()
        rep = self.report()
        self.assertEqual(rep["tool_commit"], tool_commit)
        self.assertEqual(rep["tool_origin_commit"], tool_commit)
        self.assertTrue(rep["tool_unchanged_since_tool_commit"])
        self.write("tools/m4_seal_audit.py", "# the audit tool, repaired but not committed\n")
        self.commit("2026-09-25T20:30:00+00:00", "repair the tool")
        rep2 = self.report()
        self.assertNotEqual(rep2["tool_commit"], tool_commit)
        self.assertTrue(rep2["tool_unchanged_since_tool_commit"])
        self.assertEqual(rep2["tool_origin_commit"], tool_commit)

    def test_seal_history_shows_one_draw_and_catches_a_second_one(self):
        """v2.a(iii) 2nd half: 're-seal' in the log, but was the split drawn twice?"""
        self.write("fixtures/toy.json", self.FIXTURES)
        self.commit("2026-09-25T20:05:00+00:00", "fixtures")
        self.seal()
        doc = json.load(open(os.path.join(self.repo, "SPLIT.json"), encoding="utf-8"))
        doc["manifest"] = {"book_store_sha256": "a" * 64}
        self.write("SPLIT.json", doc)
        self.commit("2026-09-25T20:11:00+00:00", "the seal, as sealed")
        doc = json.load(open(os.path.join(self.repo, "SPLIT.json"), encoding="utf-8"))
        doc["manifest"] = {"book_store_sha256": "b" * 64}      # re-manifest, same draw
        self.write("SPLIT.json", doc)
        self.commit("2026-09-25T20:12:00+00:00", "re-seal (subject reads like a second draw)")
        rep = self.report()
        self.assertIn("re-seal", self.git("log", "-1", "--format=%s", "SPLIT.json").strip())
        self.assertEqual(rep["seal_history"]["keys_added"], [])
        self.assertEqual(rep["seal_history"]["keys_removed"], [])
        self.assertEqual(rep["seal_history"]["keys_changed"], ["manifest"])
        self.assertTrue(rep["seal_history"]["one_draw"])
        self.assertIn("drawn ONCE", rep["seal_history"]["one_draw_statement"])
        doc["salt"] = "a-second-salt"                            # now it really is a second draw
        self.write("SPLIT.json", doc)
        self.commit("2026-09-25T20:15:00+00:00", "new salt")
        rep2 = self.report()                       # newest vs previous revision: only the salt
        self.assertFalse(rep2["seal_history"]["one_draw"])
        self.assertEqual(rep2["seal_history"]["keys_changed"], ["salt"])
        self.assertFalse(rep2["seal_history"]["draw_values"]["salt"]["identical"])

    def test_taint_disclosure_must_be_named_in_the_companions(self):
        """v2.b: the taint is disclosed in the report AND has to be named by its readers."""
        self.write("fixtures/toy.json", self.FIXTURES)
        self.commit("2026-09-25T20:05:00+00:00", "fixtures")
        self.seal()
        exclusions = {
            "decision": "the toy tainted transcripts are excluded; the evaluated holdout is 29 of 33",
            "evaluated_holdout_transcripts": 29,
            "excluded_transcripts": [
                {"transcript": "toy_tainted_one_enxautogen_html.txt",
                 "signals": ["D-092", "D-093", "D-094", "D-095"],
                 "verdicts": {"D-092": "refused-notation", "D-095": "CANDIDATE"}},
                {"transcript": "toy_tainted_two_enxautogen_html.txt", "signals": ["D-107"],
                 "verdicts": {"D-107": "CANDIDATE"}},
                {"transcript": "toy_tainted_three_enxautogen_html.txt", "signals": ["D-108"],
                 "verdicts": {"D-108": "CANDIDATE"}},
                {"transcript": "toy_tainted_four_enxautogen_html.txt", "signals": ["D-122"],
                 "verdicts": {"D-122": "CANDIDATE"}},
            ],
        }
        self.write("tools/HELD-OUT-SPLIT-V2-EXCLUSIONS.json", exclusions)
        self.commit("2026-09-25T20:20:00+00:00", "exclusions")
        # first with companions that exist but name nothing (the "does not name" branch) ...
        self.write("runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md",
                   "| nothing named here yet |\n")
        self.write("tools/HELD-OUT-SPLIT-V2-NOTE-2026-09-26.md", "nothing named here yet\n")
        self.commit("2026-09-25T20:21:00+00:00", "companions that name nothing")
        rep = self.report()
        self.assertEqual(rep["taint_disclosure"]["excluded_count"], 4)
        self.assertEqual(rep["taint_disclosure"]["signals_total"], 7)
        self.assertEqual(rep["taint_disclosure"]["named_in"], [])
        self.assertTrue(any("does not name" in o for o in rep["outstanding"]))
        self.assertTrue(any("no companion artefact names" in o for o in rep["outstanding"]))
        # ... and with neither companion on file at all (the "absent" branch)
        os.remove(os.path.join(self.repo, "runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md"))
        os.remove(os.path.join(self.repo, "tools/HELD-OUT-SPLIT-V2-NOTE-2026-09-26.md"))
        self.commit("2026-09-25T20:22:00+00:00", "companions removed")
        rep_absent = self.report()
        self.assertTrue(any("is absent" in o for o in rep_absent["outstanding"]))
        appendix = "\n".join(t["transcript"] for t in exclusions["excluded_transcripts"])
        signals = " ".join(sid for t in exclusions["excluded_transcripts"] for sid in t["signals"])
        self.write("runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md",
                   appendix + "\n" + signals + "\n"
                   "| audit utc 2026-09-25T21:00:00Z | evaluated holdout 29 of 33 |\n")
        self.write("tools/HELD-OUT-SPLIT-V2-NOTE-2026-09-26.md",
                   appendix + "\n" + signals + "\n29 of 33\n")
        self.commit("2026-09-25T20:25:00+00:00", "companions name the taint")
        rep2 = self.report()
        self.assertEqual(sorted(rep2["taint_disclosure"]["named_in"]),
                         ["runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md",
                          "tools/HELD-OUT-SPLIT-V2-NOTE-2026-09-26.md"])
        self.assertEqual([o for o in rep2["outstanding"] if "taint" in o], [])



if __name__ == "__main__":
    unittest.main()
