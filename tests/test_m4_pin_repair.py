#!/usr/bin/env python3
"""Tests for `tools/m4_pin_repair.py` (TASK-020 item 8a) — generator attribution.

A toy git repo is used throughout; the real artefacts are only read, never written.
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
import m4_pin_repair as pin  # noqa: E402


class Pins(unittest.TestCase):
    def test_generator_pins_bind_a_commit_that_carries_the_bytes(self):
        pins = pin.generator_pins("tools/m4_q4_supplement.py",
                                  "d7fee6e142ebbeecbd0e605395aa3d848499bf8a", repo=ROOT)
        blob = pin.blob_at(ROOT, "d7fee6e142ebbeecbd0e605395aa3d848499bf8a",
                           "tools/m4_q4_supplement.py")
        self.assertEqual(pins["generator_tool_sha256"], hashlib.sha256(blob).hexdigest())
        self.assertEqual(pins["generator_tool_blob"],
                         "origin/arena/01a0d9ce-fleetyard:tools/m4_q4_supplement.py")
        self.assertIn("lane head at run time", pins["generator_tool_note"])

    def test_generator_pins_commit_actually_contains_the_tool(self):
        # the q2/q3 supplements were blamed for pinning a tool_commit that lacks the tool;
        # the generator commit must not repeat that defect
        for tool, commit in (("tools/m4_t20_supplement.py",
                              "a5dec38865babe312b38046a4c5500f234ce94bd"),
                             ("tools/m4_q2_evidence.py",
                              "a5dec38865babe312b38046a4c5500f234ce94bd"),
                             ("tools/m4_q3_evidence.py",
                              "1cd5d444fb3ae05ad3ff74aa61323e67422eebf7"),
                             ("tools/m4_q4_supplement.py",
                              "d7fee6e142ebbeecbd0e605395aa3d848499bf8a")):
            self.assertIsNotNone(pin.blob_at(ROOT, commit, tool),
                                 "%s is absent at %s" % (tool, commit))

    def test_all_six_artefacts_carry_matching_pins(self):
        for rel, tool, commit in pin.ARTEFACTS:
            doc = json.load(open(os.path.join(ROOT, rel), encoding="utf-8"))
            got = doc.get("generator_pins") or {}
            self.assertEqual(got.get("generator_tool"), tool, rel)
            self.assertEqual(got.get("generator_tool_commit"), commit, rel)
            self.assertEqual(got.get("generator_tool_sha256"),
                             pin.generator_pins(tool, commit, repo=ROOT)["generator_tool_sha256"], rel)

    def test_guard_refuses_a_manifest_owned_by_another_tool(self):
        root = tempfile.mkdtemp(prefix="pin-")
        self.addCleanup(shutil.rmtree, root)
        path = os.path.join(root, "PROVENANCE-SUPPLEMENT.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"generator_pins": {"generator_tool": "tools/m4_q3_evidence.py"}}, fh)
        with self.assertRaises(SystemExit) as ctx:
            pin.guard_overwrite(path, "tools/m4_t20_supplement.py")
        self.assertIn("refusing to overwrite", str(ctx.exception))
        pin.guard_overwrite(path, "tools/m4_q3_evidence.py")   # its own path is fine
        pin.guard_overwrite(os.path.join(root, "absent.json"), "tools/m4_t20_supplement.py")

    def test_report_records_old_and_new_digests(self):
        report = json.load(open(os.path.join(ROOT, pin.REPORT), encoding="utf-8"))
        self.assertEqual(len(report["artefacts"]), 6)
        for a in report["artefacts"]:
            self.assertEqual(a["sha256_before"] == a["sha256_after"], not a["changed"])
            live = hashlib.sha256(open(os.path.join(ROOT, a["file"]), "rb").read()).hexdigest()
            self.assertEqual(live, a["sha256_after"], a["file"])


if __name__ == "__main__":
    unittest.main()
