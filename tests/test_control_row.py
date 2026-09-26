#!/usr/bin/env python3
"""Tests for `tools/control_row.py` — the lane's cadence row must be appendable atomically.

ORCH-2's cycle-J report (`fleet/ORCH-2-REPAIR-MAP.md`, entry 13) found the column this tool
writes in a state BOSS-2 must read as a *liveness signal* (ERRATA-25f): minute-precision stamps,
two forward stamps, a backward jump, and seq values used twice — i.e. `seq` is not a unique key
in that file's history. These tests pin the invariants the tool establishes for every row written
from here on, and the `--check` mode that reports the historical ones.
"""
import multiprocessing
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "tools"))
import control_row  # noqa: E402


def _append(args):
    """Child-process worker: append one row through the real CLI (separate interpreters)."""
    root, stamp, n = args
    env = dict(os.environ)
    return subprocess.run(
        [sys.executable, os.path.join(root, "tools", "control_row.py"),
         "--commit", "deadbeef%s" % n, "--status", "OK", "--note", "parallel writer %d" % n,
         "--utc", stamp], cwd=root, env=env, capture_output=True, text=True).returncode


class ControlRowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="control-row-")
        os.makedirs(os.path.join(self.tmp, "tools"))
        os.makedirs(os.path.join(self.tmp, "fleet"))
        self._orig = (control_row.CONTROL, control_row.REGISTRY, control_row.WORKER)
        control_row.CONTROL = os.path.join(self.tmp, "fleet", "CONTROL.log")
        control_row.REGISTRY = os.path.join(self.tmp, "fleet2", "REGISTRY.md")
        # the CLI resolves ROOT from the tool's own path: copy the tool so a child can run it
        src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools",
                           "control_row.py")
        with open(src, encoding="utf-8") as fh:
            body = fh.read()
        with open(os.path.join(self.tmp, "tools", "control_row.py"), "w", encoding="utf-8") as fh:
            fh.write(body)

    def tearDown(self):
        control_row.CONTROL, control_row.REGISTRY, control_row.WORKER = self._orig

    def rows(self):
        with open(control_row.CONTROL, encoding="utf-8") as fh:
            return control_row.parse(fh.readlines())

    def test_rows_are_exact_unique_and_non_decreasing(self):
        control_row.append("aaaa111", "OK", "first", utc="2026-09-26T10:00:00Z")
        control_row.append("bbbb222", "OK", "second", utc="2026-09-26T10:00:30Z")
        rows = self.rows()
        self.assertEqual([r["seq"] for r in rows], ["1", "2"])
        self.assertEqual([r["utc"] for r in rows],
                         ["2026-09-26T10:00:00Z", "2026-09-26T10:00:30Z"])
        self.assertEqual(control_row.check(verbose=False), [])

    def test_minute_precision_stamp_is_refused(self):
        with self.assertRaises(SystemExit) as ctx:
            control_row.append("aaaa111", "OK", "coarse", utc="2026-09-26T10:00Z")
        self.assertIn("exact to the second", str(ctx.exception))
        self.assertFalse(os.path.exists(control_row.CONTROL),
                         "a refused row must not create or touch the file")

    def test_backward_stamp_needs_a_stated_reason(self):
        control_row.append("aaaa111", "OK", "first", utc="2026-09-26T10:00:00Z")
        with self.assertRaises(SystemExit) as ctx:
            control_row.append("bbbb222", "OK", "earlier", utc="2026-09-26T09:59:00Z")
        self.assertIn("backward stamp", str(ctx.exception))
        control_row.append("bbbb222", "ERRATA", "earlier, because the clock was read late",
                           utc="2026-09-26T09:59:00Z", allow_backward="clock read late")
        self.assertEqual(len(self.rows()), 2)
        problems = control_row.check(verbose=False)
        self.assertTrue(any("goes backwards" in p for p in problems))

    def test_multiline_note_is_refused(self):
        with self.assertRaises(SystemExit):
            control_row.append("aaaa111", "OK", "line one\nline two", utc="2026-09-26T10:00:00Z")
        self.assertFalse(os.path.exists(control_row.CONTROL))

    def test_parallel_writers_never_reuse_a_seq(self):
        """The defect was two writers computing max+1 from a file the other was changing."""
        procs = []
        for n in range(6):
            # the SAME stamp for all six: equal is orderable, and this test is about seq, not
            # about the backward guard (which would refuse out-of-order stamps — as designed)
            p = multiprocessing.Process(target=_append, args=(
                (self.tmp, "2026-09-26T10:00:00Z", n),))
            p.start()
            procs.append(p)
        for p in procs:
            p.join()
        rows = self.rows()
        seqs = [r["seq"] for r in rows]
        self.assertEqual(len(rows), 6, "every writer's row must be present: %r" % (rows,))
        self.assertEqual(sorted(seqs), ["1", "2", "3", "4", "5", "6"],
                         "seq must be unique across parallel appenders: %r" % (seqs,))
        self.assertEqual(control_row.check(verbose=False), [])

    def test_check_reports_the_historical_defects(self):
        with open(control_row.CONTROL, "w", encoding="utf-8") as fh:
            fh.write("2026-09-25T18:26Z|c1|A-2026-09-25-001|r|1|OK|coarse\n"
                     "2026-09-25T18:57Z|c2|A-2026-09-25-001|r|2|OK|fine\n"
                     "2026-09-25T18:55:15Z|c3|A-2026-09-25-001|r|2|OK|backwards and reused\n")
        problems = control_row.check(verbose=False)
        self.assertTrue(any("not exact to the second" in p for p in problems))
        self.assertTrue(any("already used" in p for p in problems))
        self.assertTrue(any("goes backwards" in p for p in problems))


if __name__ == "__main__":
    unittest.main()
