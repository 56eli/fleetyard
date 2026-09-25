#!/usr/bin/env python3
"""Tests for fleet2check (drafter-local evidence; not a fleet gate).

Run:  python3 tools/test_fleet2check.py
"""
import contextlib
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fleet2check as fc  # noqa: E402


def sha(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def mk_record(rid, fields, prev="GENESIS"):
    lines = ["### %s" % rid]
    for k, v in fields.items():
        lines.append("%s: %s" % (k, v))
    governed = "".join(ln + "\n" for ln in lines)
    h = sha(governed)
    return "\n".join(lines + ["hash: %s" % h]) + "\n", h


def act(rid, seq, prev, role, lane, inc, nonce, policy, fences="-"):
    return mk_record(rid, {
        "seq": seq, "prev": prev, "kind": "ACT", "issuer": "owner",
        "issued_utc": "2026-09-25T12:00:00Z", "policy_sha256": policy,
        "role": role, "lane": lane, "incarnation": inc,
        "nonce_sha256": sha(nonce), "scope": "mission:test",
        "ends": "capability-cut|insanity|control|fence|completion",
        "fences": fences, "notes": "test"})


def ctl(rid, seq, prev, target, control, policy, nonce=None):
    f = {"seq": seq, "prev": prev, "kind": "CTL", "issuer": "owner",
         "issued_utc": "2026-09-25T12:01:00Z", "policy_sha256": policy,
         "target": target, "control": control, "reason": "test"}
    if nonce:
        f["nonce_sha256"] = sha(nonce)
    return mk_record(rid, f)


POLICY = "a" * 64


class RegistryCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="f2c-")
        self.reg = os.path.join(self.dir, "REGISTRY.md")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def write(self, text):
        with open(self.reg, "w", encoding="utf-8") as fh:
            fh.write(text)

    def build_two_acts(self):
        r1, h1 = act("A-001", 1, "GENESIS", "WORKER", "arena/w", "W-1",
                     "nonce-one", POLICY)
        r2, h2 = act("A-002", 2, h1, "WORKER", "arena/w", "W-2", "nonce-two",
                     POLICY, fences="A-001")
        return r1, h1, r2, h2

    def test_valid_activation(self):
        r1, h1, r2, h2 = self.build_two_acts()
        self.write(r1 + "\n" + r2)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["verify-activation", "--registry", self.reg,
                          "--activation", "A-002", "--role", "WORKER",
                          "--lane", "arena/w", "--nonce", "nonce-two",
                          "--anchor", h2, "--policy", POLICY])
        self.assertEqual(rc, 0, out.getvalue())
        self.assertIn("VERDICT: OK", out.getvalue())

    def test_wrong_nonce(self):
        r1, h1, r2, h2 = self.build_two_acts()
        self.write(r1 + "\n" + r2)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["verify-activation", "--registry", self.reg,
                          "--activation", "A-002", "--nonce", "forged",
                          "--anchor", h2])
        self.assertEqual(rc, 1)
        self.assertIn("NONCE-MISMATCH", out.getvalue())

    def test_superseded(self):
        r1, h1, r2, h2 = self.build_two_acts()
        self.write(r1 + "\n" + r2)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["verify-activation", "--registry", self.reg,
                          "--activation", "A-001", "--nonce", "nonce-one",
                          "--anchor", h1])
        self.assertEqual(rc, 1)
        self.assertIn("SUPERSEDED", out.getvalue())

    def test_campaign_stop_blocks_boot(self):
        r1, h1, r2, h2 = self.build_two_acts()
        r3, h3 = ctl("C-001", 3, h2, "*@*", "STOP", POLICY)
        self.write(r1 + "\n" + r2 + "\n" + r3)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["verify-activation", "--registry", self.reg,
                          "--activation", "A-002", "--nonce", "nonce-two",
                          "--anchor", h2])
        self.assertEqual(rc, 1)
        self.assertIn("CTL-STOP@C-001", out.getvalue())

    def test_relaxing_control_needs_nonce(self):
        r1, h1 = act("A-001", 1, "GENESIS", "WORKER", "arena/w", "W-1",
                     "n1", POLICY)
        bad, bh = ctl("C-002", 2, h1, "WORKER@*", "UNPAUSE", POLICY)
        self.write(r1 + "\n" + bad)
        records, errors = fc.read_registry(self.reg)
        self.assertTrue(any("requires nonce" in e for e in errors), errors)
        good, gh = ctl("C-003", 2, h1, "WORKER@*", "UNPAUSE", POLICY,
                       nonce="lift")
        self.write(r1 + "\n" + good)
        records, errors = fc.read_registry(self.reg)
        self.assertEqual(errors, [])

    def test_tamper_detected(self):
        r1, h1 = act("A-001", 1, "GENESIS", "WORKER", "arena/w", "W-1",
                     "n1", POLICY)
        tampered = r1.replace("incarnation: W-1", "incarnation: W-9")
        self.write(tampered)
        records, errors = fc.read_registry(self.reg)
        self.assertTrue(any("hash mismatch" in e for e in errors), errors)

    def test_orphan_legacy_control(self):
        r1, h1 = act("A-001", 1, "GENESIS", "WORKER", "arena/w", "W-1",
                     "n1", POLICY)
        self.write(r1)
        legacy = os.path.join(self.dir, "STOP-WORKER")
        with open(legacy, "w", encoding="utf-8") as fh:
            fh.write("owner stop\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["controls", "--registry", self.reg,
                          "--role", "WORKER", "--activation", "A-001",
                          "--legacy", legacy])
        self.assertIn("ORPHAN-LEGACY", out.getvalue())


class ReduceCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="f2r-")
        self.reg = os.path.join(self.dir, "REGISTRY.md")
        self.ev = os.path.join(self.dir, "events.log")
        r1, h1 = act("A-001", 1, "GENESIS", "WORKER", "arena/w", "W-1",
                     "n1", POLICY)
        r2, h2 = act("A-002", 2, h1, "ORCHESTRATOR", "arena/o", "O-1",
                     "n2", POLICY)
        with open(self.reg, "w", encoding="utf-8") as fh:
            fh.write(r1 + "\n" + r2)
        self.actid = "A-001"

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def run_reduce(self, lines, expect_rc=None):
        with open(self.ev, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["reduce", "--registry", self.reg,
                          "--events", "worker:" + self.ev, "--json"])
        if expect_rc is not None:
            self.assertEqual(rc, expect_rc, out.getvalue())
        return rc, out.getvalue()

    def test_last_wins_and_void(self):
        lines = [
            "E|1|2026-09-25T12:00:00Z|WORKER|A-001|T-1|-|TASK-CUT|",
            "E|2|2026-09-25T12:01:00Z|WORKER|A-001|T-1|-|CLAIM|",
            "E|3|2026-09-25T12:02:00Z|WORKER|A-999|T-1|-|DELIVER|"
            "record=r;run_manifest=m 0;criteria=c1",
            "E|4|2026-09-25T12:03:00Z|WORKER|A-001|T-1|-|DELIVER|"
            "record=r;run_manifest=" + "b" * 64 + ";criteria=c1",
        ]
        rc, text = self.run_reduce(lines)
        self.assertIn("author-activation-unknown", text)
        self.assertIn("| T-1 | DELIVERED", text)

    def test_double_claim_conflict(self):
        lines = [
            "E|1|2026-09-25T12:00:00Z|WORKER|A-001|T-1|-|TASK-CUT|",
            "E|2|2026-09-25T12:01:00Z|WORKER|A-001|T-1|-|CLAIM|",
            "E|3|2026-09-25T12:01:30Z|WORKER|A-001|T-1|-|CLAIM|",
        ]
        rc, _ = self.run_reduce(lines, expect_rc=0)  # same activation: fine
        lines[2] = ("E|3|2026-09-25T12:01:30Z|ORCHESTRATOR|A-002|T-1|-|CLAIM|")
        rc, text = self.run_reduce(lines)
        self.assertEqual(rc, 1)
        self.assertIn("double-claim", text)

    def test_dep_cycle_and_stale_block(self):
        lines = [
            "E|1|2026-09-25T12:00:00Z|WORKER|A-001|T-1|-|TASK-CUT|",
            "E|2|2026-09-25T12:00:10Z|WORKER|A-001|T-2|-|TASK-CUT|",
            "E|3|2026-09-25T12:00:20Z|WORKER|A-001|T-1|-|DELIVER|"
            "blocked_by=T-2;record=r;run_manifest=m 0;criteria=c",
            "E|4|2026-09-25T12:00:30Z|WORKER|A-001|T-2|-|DELIVER|"
            "blocked_by=T-1,ghost;record=r;run_manifest=m 0;criteria=c",
        ]
        rc, text = self.run_reduce(lines)
        self.assertEqual(rc, 1)
        self.assertIn("DEP-CYCLE", text)
        self.assertIn("STALE-BLOCK", text)


class GateCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="f2g-")
        self.reg = os.path.join(self.dir, "REGISTRY.md")
        r1, h1 = act("A-001", 1, "GENESIS", "ORCHESTRATOR", "arena/o", "O-1",
                     "n1", POLICY)
        with open(self.reg, "w", encoding="utf-8") as fh:
            fh.write(r1)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def gate_text(self, verdict="PASS", criteria=("PASS",), run_manifest=None,
                  seeded=True, rate=False, rotation=2):
        rm = run_manifest if run_manifest is not None else "c" * 64
        rows = "\n".join("| CRIT-T-%d | requirement | %s | ev | obs |"
                         % (i + 1, v) for i, v in enumerate(criteria))
        seeded_line = ("seeded_vs_independent: seeded=1 independent=15"
                       if seeded else "")
        return """gate: G-1
gatekeeper_activation: A-001
producer_activation: A-004
source: 1a2b3c4d
fenced: -
policy: %s
suite: ran=109 skipped=0 result=OK run_manifest=runs/r/MANIFEST.json %s
adversarial_sample: x#y (selection_seal=S-1)
rotation: gate #%d of this producer pair in this activation (max 3, 04 §5)
%s
%s
counts: criteria_pass=1 fail=0 notrun=0
verdict: %s
%s
""" % (POLICY, rm, rotation, seeded_line, rows, verdict,
       "precision: 0.9 measured" if rate else "")

    def check(self, text, expect_rc, expect_token):
        p = os.path.join(self.dir, "GATE.md")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(text)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["gate-check", "--gate", p, "--registry", self.reg])
        self.assertEqual(rc, expect_rc, out.getvalue())
        if expect_token:
            self.assertIn(expect_token, out.getvalue())

    def test_good_gate(self):
        self.check(self.gate_text(), 0, "GATE: OK")

    def test_cert_with_fail(self):
        self.check(self.gate_text(verdict="PASS", criteria=("PASS", "FAIL")),
                   1, "CERT-WITH-FAIL")

    def test_no_fresh_run(self):
        self.check(self.gate_text(run_manifest="-"), 1, "NO-FRESH-RUN")

    def test_seeded_missing(self):
        self.check(self.gate_text(seeded=False), 1, "SEEDED-AS-INDEPENDENT")

    def test_precision_without_seal(self):
        txt = self.gate_text(rate=True).replace("selection_seal=S-1", "-")
        self.check(txt, 1, "NO-SEAL")

    def test_rotation(self):
        self.check(self.gate_text(rotation=4), 1, "GATE-ROTATION")


class RunCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="f2m-")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def write_run(self, obj, name="M.json"):
        p = os.path.join(self.dir, name)
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(obj, fh)
        return p

    def base(self, **kw):
        m = {"run_id": "r1", "activation": "A-001",
             "started_utc": "2026-09-25T12:00:00Z", "command": "cmd",
             "fresh": True, "policy_sha256": POLICY,
             "corpus_zip_sha256": "3f36c520" + "0" * 56,
             "tool_digest": "d" * 64,
             "inputs": [{"path": "corpus/a.txt", "sha256": "e" * 64}],
             "outputs": [{"path": "out/a.json", "sha256": "f" * 64,
                          "records": 3}],
             "resume": {"used_cache": False, "inherited": []},
             "counters": {"processed": 1, "records": 3}}
        m.update(kw)
        return m

    def verify(self, m, expect_rc, token, extra=None):
        p = self.write_run(m)
        argv = ["verify-run", "--manifest", p] + (extra or [])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(argv)
        self.assertEqual(rc, expect_rc, out.getvalue())
        if token:
            self.assertIn(token, out.getvalue())

    def test_fresh_ok(self):
        self.verify(self.base(), 0, "RUN: OK")

    def test_resume_launder(self):
        m = self.base(fresh=True, resume={"used_cache": True, "inherited": []})
        self.verify(m, 1, "RUN-RESUME-LAUNDER")

    def test_resume_unverified_inherited(self):
        m = self.base(fresh=False, resume={"used_cache": True, "inherited": [
            {"path": "out/a.json", "records": 0}]})
        self.verify(m, 1, "RUN-RESUME-LAUNDER")

    def test_resume_verified_but_release_ineligible(self):
        m = self.base(fresh=False, resume={"used_cache": True, "inherited": [
            {"path": "out/a.json", "provenance_manifest": "runs/old/M.json",
             "provenance_sha256": "a" * 64, "verified": True}]})
        self.verify(m, 0, "RUN: OK")
        self.verify(m, 1, "RUN-RELEASE-INELIGIBLE-INHERITED",
                    extra=["--reject-inherited"])

    def test_lost_commit(self):
        m = self.base(lost="8" * 40, tool_commit="8" * 40)
        self.verify(m, 1, "RUN-USES-LOST-COMMIT")

    def test_count_drop(self):
        prev = self.base(outputs=[{"path": "out/a.json", "records": 5}])
        pp = self.write_run(prev, "OLD.json")
        m = self.base(outputs=[{"path": "out/a.json", "records": 0}])
        p = self.write_run(m)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["verify-run", "--manifest", p, "--previous", pp])
        self.assertEqual(rc, 1)
        self.assertIn("RUN-COUNT-DROP:out/a.json", out.getvalue())


class ObserveZombieCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="f2o-")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_observe_ok_and_divergence(self):
        a = os.path.join(self.dir, "a.log")
        b = os.path.join(self.dir, "b.log")
        with open(a, "w", encoding="utf-8") as fh:
            fh.write("2026-09-25T12:00:00Z|main1|A-001|%s|1|PROCEED|x\n"
                     % ("1" * 64))
            fh.write("2026-09-25T12:05:00Z|main1|A-002|%s|2|PROCEED|x\n"
                     % ("2" * 64))
        with open(b, "w", encoding="utf-8") as fh:
            fh.write("2026-09-25T12:03:00Z|main1|A-002|%s|2|PROCEED|x\n"
                     % ("2" * 64))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["observe", "--control-logs", "w:" + a, "o:" + b])
        self.assertEqual(rc, 0, out.getvalue())
        with open(b, "w", encoding="utf-8") as fh:
            fh.write("2026-09-25T12:03:00Z|main2|A-002|%s|2|PROCEED|x\n"
                     % ("9" * 64))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["observe", "--control-logs", "w:" + a, "o:" + b])
        self.assertEqual(rc, 1)
        self.assertIn("MAIN-MOVED", out.getvalue())

    def test_zombie_and_laundering(self):
        p = os.path.join(self.dir, "w.log")
        lines = [
            "E|1|2026-09-25T12:00:00Z|WORKER|A-001|T| -|NOTE|",
            "E|2|2026-09-25T12:01:00Z|WORKER|A-001|T|-|NOTE|",
            "E|3|2026-09-25T12:02:00Z|WORKER|A-001|T|-|NOTE|",
        ]
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["zombie", "--events", "worker:" + p])
        self.assertEqual(rc, 1)
        self.assertIn("ZOMBIE", out.getvalue())
        lines = [
            "E|1|2026-09-25T12:00:00Z|WORKER|A-001|T|-|ORDER|",
            "E|2|2026-09-25T12:01:00Z|WORKER|A-001|T|-|ESCALATION|",
        ]
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["zombie", "--events", "worker:" + p])
        self.assertEqual(rc, 1)  # two order/alert resets in one window: laundering
        lines = ["E|1|2026-09-25T12:00:00Z|WORKER|A-001|T|-|ORDER|"]
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["zombie", "--events", "worker:" + p])
        self.assertEqual(rc, 0)  # a single order may reset the streak once


class MiscCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="f2x-")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def test_manifest_deterministic(self):
        os.makedirs(os.path.join(self.dir, "tools"))
        for n in ("a.py", "b.py"):
            with open(os.path.join(self.dir, "tools", n), "w",
                      encoding="utf-8") as fh:
                fh.write("print(%r)\n" % n)
        out1, out2 = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out1):
            fc.main(["manifest", "--dir", self.dir, "tools"])
        with contextlib.redirect_stdout(out2):
            fc.main(["manifest", "--dir", self.dir, "tools"])
        self.assertEqual(out1.getvalue(), out2.getvalue())
        self.assertIn("BUNDLE_SHA256", out1.getvalue())

    def test_record_check(self):
        chk = os.path.join(self.dir, "CHK.md")
        chk_text = """record: 2026-09-25T1200Z-CHK-T1
type: CHK
activation: A-001
role: WORKER
utc: 2026-09-25T12:00:00Z
task: T-1
criterion_id: -
control_seq: 3
main_head: abc1234
registry_head: A-001 %s
inputs: z=1
run_manifest: -
evidence_index: -
next_step: continue
ended_by: -
successor_contract: -
unpushed: none
notes: x
""" % ("f" * 64)
        with open(chk, "w", encoding="utf-8") as fh:
            fh.write(chk_text)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["record-check", "--file", chk])
        self.assertEqual(rc, 0, out.getvalue())
        ho = chk_text.replace("CHK-T1", "HO-A-001").replace("type: CHK", "type: HO") \
                .replace("ended_by: -", "ended_by: nonsense") \
                .replace("successor_contract: -", "successor_contract: x") \
                .replace("unpushed: none", "unpushed: 2 commits")
        p2 = os.path.join(self.dir, "HO.md")
        with open(p2, "w", encoding="utf-8") as fh:
            fh.write(ho)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["record-check", "--file", p2])
        self.assertEqual(rc, 1)
        self.assertIn("HO-BAD-ENDED-BY", out.getvalue())
        self.assertIn("HO-UNPUSHED-NOT-NONE", out.getvalue())

    def test_orders(self):
        p = os.path.join(self.dir, "ORDER-1.md")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("order: O-1\nissued_utc: 2026-09-25T12:00:00Z\n"
                     "ack_due_utc: 2026-09-25T12:15:00Z\npolicy: %s\n"
                     "target: WORKER@*\nbody: cut the repair next\n" % POLICY)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["orders", "--order", p])
        self.assertEqual(rc, 0, out.getvalue())
        with open(p, "a", encoding="utf-8") as fh:
            fh.write("body2: I authorise an override for this shift\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["orders", "--order", p])
        self.assertEqual(rc, 1)
        self.assertIn("ORDER-FORBIDDEN-PHRASE", out.getvalue())

    def test_freshness(self):
        hb = os.path.join(self.dir, "W.log")
        with open(hb, "w", encoding="utf-8") as fh:
            fh.write("2026-09-25T12:00:00Z task T-1 @ arena/w abc1234 (109 OK)\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["freshness", "--heartbeat-logs", "worker:" + hb])
        self.assertEqual(rc, 0, out.getvalue())
        with open(hb, "w", encoding="utf-8") as fh:
            fh.write("2026-09-25T12:00:00Z task T-1 done, all good\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["freshness", "--heartbeat-logs", "worker:" + hb])
        self.assertEqual(rc, 1)
        self.assertIn("STALE-REF", out.getvalue())

    def test_control_render_and_emit_md(self):
        log = os.path.join(self.dir, "CONTROL.log")
        with open(log, "w", encoding="utf-8") as fh:
            fh.write("2026-09-25T12:00:00Z|main1|A-001|%s|1|PROCEED|x\n"
                     % ("1" * 64))
            fh.write("2026-09-25T12:05:00Z|main1|A-002|%s|2|PROCEED|x\n"
                     % ("2" * 64))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["control-render", "--log", log, "--lane", "worker"])
        self.assertEqual(rc, 0, out.getvalue())
        self.assertIn("GENERATED by fleet2check control-render", out.getvalue())
        self.assertIn("seq_monotonic: yes", out.getvalue())
        # reducer --emit-md writes the state file
        ev = os.path.join(self.dir, "e.log")
        with open(ev, "w", encoding="utf-8") as fh:
            fh.write("E|1|2026-09-25T12:00:00Z|WORKER|A-001|T-1|-|TASK-CUT|\n")
        md = os.path.join(self.dir, "STATE.md")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["reduce", "--events", "worker:" + ev,
                          "--emit-md", md])
        self.assertEqual(rc, 0, out.getvalue())
        with open(md, "r", encoding="utf-8") as fh:
            self.assertIn("GENERATED by fleet2check reduce", fh.read())

    def test_alerts_missing_class(self):
        hb = os.path.join(self.dir, "W.log")
        with open(hb, "w", encoding="utf-8") as fh:
            fh.write("2026-09-25T12:00:00Z heartbeat sha abc1234\n")
        alerts = os.path.join(self.dir, "ALERTS.md")
        with open(alerts, "w", encoding="utf-8") as fh:
            fh.write("# alerts\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["alerts", "--lanes", "worker:" + hb,
                          "--alerts", alerts, "--now",
                          "2026-09-25T12:45:00Z"])
        self.assertEqual(rc, 1)
        self.assertIn("MISSING-CLASS", out.getvalue())
        with open(alerts, "w", encoding="utf-8") as fh:
            fh.write("# alerts\nworker quiet 45 min\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = fc.main(["alerts", "--lanes", "worker:" + hb,
                          "--alerts", alerts, "--now",
                          "2026-09-25T12:45:00Z"])
        self.assertEqual(rc, 0, out.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
