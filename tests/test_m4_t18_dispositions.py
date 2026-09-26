#!/usr/bin/env python3
"""Tests for `tools/m4_t18_dispositions.py` (TASK-018 items 0d–0g).

The committed artefacts are read (never written); the append/refuse behaviour is exercised
on a copy in a temp dir.
"""
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
import m4_t18_dispositions as disp  # noqa: E402

ADJ = os.path.join(ROOT, "runs", "m4-q2-adjudication", "adjudication.jsonl")
REC = os.path.join(ROOT, "runs", "m4-q2-adjudication", "RECOUNT-2026-09-26.json")


def rows():
    with open(ADJ, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


class Dispositions(unittest.TestCase):
    def test_committed_file_has_122_signal_rows_and_the_dispositions(self):
        signal = disp.signal_rows(rows())
        ruled = [r for r in rows() if r.get("record") == "disposition"]
        self.assertEqual(len(signal), 122)
        self.assertEqual({r["id"] for r in ruled},
                         set(disp.DEMOTIONS) | set(disp.NOTATION_IDS) | set(disp.HOLDOUT_IDS))

    def test_base_lines_match_the_recorded_digest(self):
        prov = json.load(open(os.path.join(ROOT, "runs", "m4-q2-adjudication",
                                           "PROVENANCE.json"), encoding="utf-8"))
        blob = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n"
                       for r in disp.signal_rows(rows()))
        # PROVENANCE records the tool's own serialisation of the same rows; both digests are
        # published in the recount so the base is provably unedited
        rec = json.load(open(REC, encoding="utf-8"))
        self.assertEqual(rec["base_122_lines_sha256_before_append"],
                         prov["outputs"]["adjudication.jsonl"])
        self.assertEqual(rec["base_lines_reconstructed_digest"],
                         hashlib.sha256(blob.encode("utf-8")).hexdigest())

    def test_dispositions_carry_reasons_and_exact_utc(self):
        for r in [x for x in rows() if x.get("record") == "disposition"]:
            self.assertTrue(r.get("reason"))
            self.assertRegex(r.get("utc", ""), r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
            self.assertIn("utc_source", r)
            # item 12's order / criterion 20.14c: the source must be a DERIVATION, and a repaired
            # stamp must keep the defective value readable with a reason
            self.assertTrue(r["utc_source"].startswith(("git committer time of", "argument/--utc")),
                            r["utc_source"])
            if r.get("utc_superseded"):
                self.assertRegex(r["utc_superseded"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
                self.assertTrue(r.get("utc_superseded_reason"))

    def test_unsourced_stamps_are_refused_and_git_derived_ones_match_the_commit(self):
        """Criterion 20.14c / items 0h-v2.h: an own-time stamp must be exact AND sourced."""
        self.root = tempfile.mkdtemp(prefix="m4t18-")
        self.addCleanup(shutil.rmtree, self.root)
        with self.assertRaises(SystemExit) as ctx:
            disp.main(["build", "--utc", "2026-09-26T01:12:00Z", "--out", self.root,
                       "--repo", self.root])
        self.assertIn("requires --utc-source", str(ctx.exception))
        with self.assertRaises(SystemExit) as ctx:
            disp.main(["build", "--out", self.root, "--repo", self.root])
        self.assertIn("a stamp is required", str(ctx.exception))
        # in a toy git repo, the stamp is derived from the commit that carries the lines
        repo = os.path.join(self.root, "git")
        os.makedirs(os.path.join(repo, "runs", "m4-q2-adjudication"))
        shutil.copytree(os.path.join(ROOT, "fixtures"), os.path.join(repo, "fixtures"))
        with open(os.path.join(repo, "runs", "m4-q2-adjudication", "adjudication.jsonl"),
                  "w", encoding="utf-8") as fh:
            fh.write("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n"
                             for r in rows()[:122]))
        shutil.copy(os.path.join(ROOT, "runs", "m4-q2-adjudication", "PROVENANCE.json"),
                    os.path.join(repo, "runs", "m4-q2-adjudication", "PROVENANCE.json"))
        with open(os.path.join(repo, "runs", "m4-q2-adjudication", "SUMMARY.md"), "w",
                  encoding="utf-8") as fh:
            fh.write("carries the corrections already\n")
        run = lambda *a: subprocess.run(("git", "-C", repo) + a, capture_output=True, text=True)
        run("init", "-q")
        run("config", "user.email", "worker@example.invalid")
        run("config", "user.name", "WORKER-2 test")
        env = dict(os.environ, GIT_AUTHOR_DATE="2026-09-26T00:39:44+00:00",
                   GIT_COMMITTER_DATE="2026-09-26T00:39:44+00:00")
        run("add", "-A")
        subprocess.run(("git", "-C", repo, "commit", "-q", "-m", "base"),
                       capture_output=True, env=env)
        head = run("rev-parse", "HEAD").stdout.strip()
        disp.main(["build", "--utc-from-commit", head, "--repo", repo,
                   "--superseded", "2026-09-26T01:12:00Z",
                   "--superseded-reason", "projected from the CONTROL cadence grid (20.14c)",
                   "--out", os.path.join(repo, "runs", "m4-q2-adjudication")])
        written = [json.loads(x) for x in
                   open(os.path.join(repo, "runs", "m4-q2-adjudication", "adjudication.jsonl"),
                        encoding="utf-8") if x.strip()]
        d = written[122]
        self.assertEqual(d["utc"], "2026-09-26T00:39:44Z")
        self.assertIn("committer time", d["utc_source"])
        self.assertEqual(d["utc_superseded"], "2026-09-26T01:12:00Z")
        rec = json.load(open(os.path.join(repo, "runs", "m4-q2-adjudication",
                                          "RECOUNT-2026-09-26.json"), encoding="utf-8"))
        self.assertEqual(rec["written_utc"], "2026-09-26T00:39:44Z")
        self.assertIn("committer time", rec["utc_source"])

    def test_recount_arithmetic_and_strata(self):
        rec = json.load(open(REC, encoding="utf-8"))
        counts = rec["facts"]["omitted_word_counts"]
        self.assertEqual(sum(counts.values()), 57)
        self.assertEqual(rec["facts"]["seeded_true_rows"], 0)
        self.assertEqual(rec["facts"]["fixture_span_overlaps"], 0)
        self.assertEqual(rec["counts_after_exclusions"]["rows"], 49)
        self.assertEqual(rec["counts_after_exclusions"]["sites"], 48)
        self.assertEqual(rec["stratification"]["after_exclusions"]["sum"], 49)
        self.assertEqual(rec["standing_statements"]["band"]["floors"]["3"], 71)

    def test_build_refuses_a_second_append(self):
        tmp = tempfile.mkdtemp(prefix="t18disp-")
        self.addCleanup(shutil.rmtree, tmp, True)
        out = os.path.join(tmp, "run")
        shutil.copytree(os.path.join(ROOT, "runs", "m4-q2-adjudication"), out)
        os.remove(os.path.join(out, "adjudication.jsonl"))
        shutil.copy(ADJ, os.path.join(out, "adjudication.jsonl"))
        with self.assertRaises(SystemExit) as ctx:
            disp.main(["build", "--out", out, "--utc", "2026-09-26T01:20:00Z",
                       "--utc-source", "operator statement (test)"])
        self.assertIn("already present", str(ctx.exception))

    def test_corrections_prose_carries_the_required_qualifiers(self):
        summary = open(os.path.join(ROOT, "runs", "m4-q2-adjudication", "SUMMARY.md"),
                       encoding="utf-8").read()
        patterns = open(os.path.join(ROOT, "tools", "PATTERNS.md"), encoding="utf-8").read()
        for needle in ("0 of 122", "55 distinct sites", "71/57/33/22", "unknowable"):
            self.assertIn(needle, summary)
            self.assertIn(needle, patterns)


if __name__ == "__main__":
    unittest.main()
