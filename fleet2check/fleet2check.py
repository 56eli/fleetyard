#!/usr/bin/env python3
"""fleet2check — stdlib reference checker for the fleet-2.0 policy bundle.

Implements the record formats specified in outbound/fleetyard-audit/fleet2-draft/
(01 activation registry, 02 terminal records, 03 controls, 04 escalation/
observation, 05 event reduction, 06 run manifests, 07 gates).

    python3 tools/fleet2check.py <subcommand> [args]

Subcommands: manifest, verify-activation, active-role, controls, record-check,
reduce, gate-check, verify-run, zombie, observe, orders, freshness, alerts,
selftest.

Exit codes: 0 = OK, 1 = rejected/invalid, 2 = usage/parse error.

Stdlib only. No network. Nothing here grants authority; it only checks shapes
and hashes that a human can recompute.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys

HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX7 = re.compile(r"^[0-9a-f]{7,40}$")
KINDS = ("ACT", "CTL", "OVR", "CMP", "ERR", "NOTE")
RECORD_FIELDS = ("seq", "prev", "kind", "issuer", "issued_utc", "policy_sha256")
CTL_TARGET = re.compile(r"^([A-Z]+|\*)@([A-Z]-[0-9-]+|\*)$")
RESTRICTING = ("STOP", "PAUSE", "FREEZE")
SUBSTANTIVE_EVENTS = ("DELIVER", "GATE", "CERT")
STATUS_EVENTS = ("NOTE", "ORDER", "PAUSE", "UNPAUSE", "TASK-CUT", "ESCALATION",
                 "STRIKE", "GUARD-STOP", "CHK", "SELFCHECK", "SAMPLE")
ORDER_BANNED = ("override", "extend the shift", "extend your shift",
                "mission complete", "certify", "no-cap", "past the cap",
                "beyond the cap")


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_utc(s):
    s = s.strip().replace("Z", "+00:00")
    try:
        return datetime.datetime.fromisoformat(s.replace("+00:00", "+00:00"))
    except ValueError:
        # allow 20260925T120500Z style
        m = re.match(r"^(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})Z?$", s)
        if not m:
            raise SystemExit("fleet2check: cannot parse utc %r" % s)
        y, mo, d, hh, mm, ss = (int(x) for x in m.groups())
        return datetime.datetime(y, mo, d, hh, mm, ss,
                                 tzinfo=datetime.timezone.utc)


def utc_of(record, key="issued_utc"):
    return parse_utc(record["fields"][key])


# ---------------------------------------------------------------- registry

class Record(object):
    __slots__ = ("id", "fields", "hash", "index")

    def __init__(self, rid, fields, rhash, index):
        self.id = rid
        self.fields = fields
        self.hash = rhash
        self.index = index

    @property
    def kind(self):
        return self.fields.get("kind", "?")

    def __repr__(self):
        return "<%s %s seq=%s>" % (self.kind, self.id, self.fields.get("seq"))


def parse_registry(text):
    """Return (records, errors). Errors are fatal chain/format problems."""
    lines = text.splitlines()
    blocks, cur = [], None
    for ln in lines:
        if ln.startswith("### "):
            if cur is not None:
                blocks.append(cur)
            cur = [ln]
        elif ln.startswith("<!--") or ln.strip() == "":
            if cur is not None:
                # blank lines terminate a governed record (only allowed after hash)
                blocks.append(cur)
                cur = None
        else:
            if cur is None:
                errors = ["content outside a record block: %r" % ln]
                return [], errors
            cur.append(ln)
    if cur is not None:
        blocks.append(cur)

    records, errors = [], []
    for i, block in enumerate(blocks):
        rid = block[0][4:].strip()
        hash_idx = None
        for j, ln in enumerate(block):
            if ln.startswith("hash:"):
                hash_idx = j
        if hash_idx is None:
            errors.append("%s: missing hash: line" % rid)
            continue
        fields = {}
        for ln in block[1:hash_idx]:
            if ":" not in ln:
                errors.append("%s: unparseable field line %r" % (rid, ln))
                continue
            k, v = ln.split(":", 1)
            fields[k.strip()] = v.strip()
        declared = block[hash_idx].split(":", 1)[1].strip()
        governed = "".join(ln + "\n" for ln in block[:hash_idx])
        computed = sha256_text(governed)
        if declared != computed:
            errors.append("%s: hash mismatch (declared %s computed %s)"
                          % (rid, declared[:12], computed[:12]))
        if not HEX64.match(declared or ""):
            errors.append("%s: hash not a 64-hex string" % rid)
        records.append(Record(rid, fields, computed, i))

    for k, r in enumerate(records):
        want = 1 if k == 0 else int(records[k - 1].fields.get("seq", -1)) + 1
        got = r.fields.get("seq")
        if got is None or int(got) != want:
            errors.append("%s: seq %s != expected %s" % (r.id, got, want))
        prev = r.fields.get("prev")
        expect = "GENESIS" if k == 0 else records[k - 1].hash
        if prev != expect:
            errors.append("%s: prev %s != expected %s" % (r.id, prev, expect))
        if r.fields.get("kind") not in KINDS:
            errors.append("%s: unknown kind %r" % (r.id, r.fields.get("kind")))
        for f in RECORD_FIELDS:
            if f not in r.fields:
                errors.append("%s: missing field %s" % (r.id, f))
        if r.kind == "ACT":
            for f in ("role", "lane", "incarnation", "nonce_sha256", "fences"):
                if f not in r.fields:
                    errors.append("%s: ACT missing %s" % (r.id, f))
        if r.kind == "CTL":
            for f in ("target", "control", "reason"):
                if f not in r.fields:
                    errors.append("%s: CTL missing %s" % (r.id, f))
            if r.fields.get("control") in ("UNPAUSE", "ALLOW", "UNFREEZE") \
                    and not HEX64.match(r.fields.get("nonce_sha256", "")):
                errors.append("%s: relaxing control requires nonce_sha256" % r.id)
        if r.kind in ("OVR", "CMP", "ERR") \
                and not HEX64.match(r.fields.get("nonce_sha256", "")):
            errors.append("%s: %s requires nonce_sha256" % (r.id, r.kind))
    return records, errors


def read_registry(path):
    with open(path, "r", encoding="utf-8") as fh:
        return parse_registry(fh.read())


def in_force_controls(records, role, activation):
    """Return list of (record, effect) restricting controls still in force."""
    out = []
    for r in records:
        if r.kind != "CTL":
            continue
        t = r.fields.get("target", "")
        m = CTL_TARGET.match(t)
        if not m:
            out.append((r, "CTL-TARGET-MALFORMED"))
            continue
        trole, tact = m.groups()
        if trole not in (role, "*") and tact not in (activation, "*"):
            continue
        matched_exact = (trole in (role, "*")) and (tact in (activation, "*"))
        if not matched_exact:
            continue
        eff = r.fields.get("control")
        if eff in RESTRICTING:
            out.append((r, eff))
    # relaxations cancel later restrictions of the same target
    resolved = []
    for r, eff in out:
        later_relax = [x for x in records
                       if x.kind == "CTL" and x.index > r.index
                       and x.fields.get("control") in ("UNPAUSE", "ALLOW",
                                                       "UNFREEZE")
                       and x.fields.get("target") == r.fields.get("target")]
        if not later_relax:
            resolved.append((r, eff))
    return resolved


def active_map(records):
    """role -> (ACT record, reason) for the registry's currently active acts."""
    result = {}
    for r in records:
        if r.kind == "ACT":
            result[r.fields["role"]] = r
    for role, act in list(result.items()):
        blocked = []
        for r in records:
            if r.index <= act.index:
                continue
            if r.kind in ("CTL",) and r.fields.get("control") in RESTRICTING:
                t = r.fields.get("target", "")
                m = CTL_TARGET.match(t)
                if m and (m.group(1) in (role, "*")) and \
                        (m.group(2) in (act.id, "*")):
                    blocked.append((r, r.fields.get("control")))
            if r.kind == "CMP":
                blocked.append((r, "CMP"))
        result[role] = (act, blocked)
    return result


# ---------------------------------------------------------------- checks

def cmd_verify_activation(args):
    records, errors = read_registry(args.registry)
    if errors:
        for e in errors:
            print("CHAIN-BREAK %s" % e)
        return 1
    by_id = {r.id: r for r in records}
    if args.activation not in by_id:
        print("VERDICT: REJECT ACTIVATION-UNKNOWN %s" % args.activation)
        return 1
    rec = by_id[args.activation]
    fails = []
    if rec.kind != "ACT":
        fails.append("NOT-AN-ACT")
    if rec.hash != args.anchor:
        fails.append("ANCHOR-MISMATCH")
    if args.role and rec.fields.get("role") != args.role:
        fails.append("ROLE-MISMATCH")
    if args.lane and rec.fields.get("lane") != args.lane:
        fails.append("LANE-MISMATCH")
    if args.nonce is not None:
        if sha256_text(args.nonce) != rec.fields.get("nonce_sha256"):
            fails.append("NONCE-MISMATCH")
    if args.policy and rec.fields.get("policy_sha256") != args.policy:
        fails.append("POLICY-MISMATCH")
    amap = active_map(records)
    act, blocked = amap.get(rec.fields.get("role"), (None, []))
    if act is not None and act.id != rec.id:
        fails.append("SUPERSEDED-BY-%s" % act.id)
    for r, eff in in_force_controls(records, rec.fields.get("role", ""), rec.id):
        fails.append("CTL-%s@%s" % (eff, r.id))
    fences = rec.fields.get("fences", "-")
    if fences not in ("-", "", None):
        for f in [x.strip() for x in fences.split(",") if x.strip()]:
            if f not in by_id:
                fails.append("FENCE-UNKNOWN-%s" % f)
            elif by_id[f].kind != "ACT" or \
                    by_id[f].fields.get("role") != rec.fields.get("role"):
                fails.append("FENCE-NOT-ACT-%s" % f)
    for r, eff in blocked:
        fails.append("BLOCKED-BY-%s-%s" % (eff, r.id))
    if fails:
        print("VERDICT: REJECT %s" % " ".join(fails))
        return 1
    print("VERDICT: OK activation=%s role=%s lane=%s seq=%s hash=%s"
          % (rec.id, rec.fields.get("role"), rec.fields.get("lane"),
             rec.fields.get("seq"), rec.hash))
    if fences not in ("-", "", None):
        print("fences=%s (predecessor(s) must end at their next control check)"
              % fences)
    return 0


def cmd_active_role(args):
    records, errors = read_registry(args.registry)
    if errors:
        for e in errors:
            print("CHAIN-BREAK %s" % e)
        return 1
    amap = active_map(records)
    for role in sorted(amap):
        act, blocked = amap[role]
        status = "ACTIVE" if not blocked else \
            "BLOCKED[" + ",".join("%s@%s" % (e, r.id) for r, e in blocked) + "]"
        print("%-14s %-22s %s lane=%s incarnation=%s policy=%s"
              % (role, act.id, status, act.fields.get("lane"),
                 act.fields.get("incarnation"),
                 (act.fields.get("policy_sha256") or "")[:12]))
    return 0


def cmd_controls(args):
    records, errors = read_registry(args.registry)
    if errors:
        for e in errors:
            print("CHAIN-BREAK %s" % e)
        return 1
    rc = 0
    for r in records:
        if r.kind == "CTL":
            print("CTL %s control=%s target=%s seq=%s reason=%s"
                  % (r.id, r.fields.get("control"), r.fields.get("target"),
                     r.fields.get("seq"), r.fields.get("reason")))
    orphans = []
    for spec in args.legacy or []:
        path = spec
        if not os.path.exists(path):
            continue
        orphans.append(path)
        print("ORPHAN-LEGACY %s (stops %s@* until the owner resolves it in the "
              "registry; never delete)"
              % (path, spec.split("@")[-1] if "@" in spec else "?"))
    if args.role and args.activation:
        inforce = in_force_controls(records, args.role, args.activation)
        for r, eff in inforce:
            print("IN-FORCE %s on %s@%s" % (eff, args.role, args.activation))
            rc = 1
    return rc


def cmd_record_check(args):
    fields = {}
    with open(args.file, "r", encoding="utf-8") as fh:
        for ln in fh:
            if ":" in ln and not ln.startswith("#"):
                k, v = ln.split(":", 1)
                fields[k.strip()] = v.strip()
    kind = fields.get("type")
    fails = []
    if kind not in ("CHK", "DEL", "HO", "RCV"):
        fails.append("BAD-TYPE")
    for f in ("record", "activation", "role", "utc", "control_seq", "main_head",
              "registry_head", "inputs"):
        if f not in fields:
            fails.append("MISSING-%s" % f)
    if kind == "CHK" and fields.get("next_step", "-") == "-":
        fails.append("CHK-NO-NEXT-STEP")
    if kind == "DEL":
        for f in ("run_manifest", "evidence_index", "criterion_id"):
            if fields.get(f, "-") == "-":
                fails.append("DEL-MISSING-%s" % f)
    if kind == "HO":
        if fields.get("ended_by") not in ("capability-cut", "insanity",
                                          "control", "fence", "completion"):
            fails.append("HO-BAD-ENDED-BY")
        if fields.get("unpushed", "none") != "none":
            fails.append("HO-UNPUSHED-NOT-NONE")
        if fields.get("successor_contract", "-") == "-":
            fails.append("HO-NO-SUCCESSOR-CONTRACT")
    if fails:
        print("RECORD: INVALID %s" % " ".join(fails))
        return 1
    print("RECORD: OK %s type=%s activation=%s"
          % (fields["record"], kind, fields["activation"]))
    return 0


def cmd_manifest(args):
    rows = []
    for pat in args.paths:
        base = args.dir
        if os.path.isdir(os.path.join(base, pat)):
            for root, _dirs, files in os.walk(os.path.join(base, pat)):
                for fn in sorted(files):
                    p = os.path.join(root, fn)
                    rows.append((os.path.relpath(p, base).replace(os.sep, "/"),
                                 sha256_file(p)))
        else:
            p = os.path.join(base, pat)
            rows.append((pat.replace(os.sep, "/"), sha256_file(p)))
    rows.sort()
    text = "".join("%s %s\n" % (p, h) for p, h in rows)
    print(text, end="")
    print("BUNDLE_SHA256 %s" % sha256_text(text))
    return 0


# ---------------------------------------------------------------- reduce

def parse_event_line(ln):
    parts = ln.rstrip("\n").split("|")
    if len(parts) < 8 or parts[0] != "E":
        return None
    keys = {}
    if len(parts) >= 9:
        for kv in parts[8].split(";"):
            if "=" in kv:
                k, v = kv.split("=", 1)
                keys[k.strip()] = v.strip()
    return {"seq": int(parts[1]), "utc": parts[2], "role": parts[3],
            "activation": parts[4], "task": parts[5], "criterion": parts[6],
            "type": parts[7], "keys": keys}


def events_void(records, ev):
    amap = active_map(records)
    act = amap.get(ev["role"])
    if act is None:
        return "author-role-never-activated"
    arec, blocked = act
    if arec.id != ev["activation"]:
        # was this activation ever active for the role? if not, void
        acts = [r for r in records if r.kind == "ACT"
                and r.fields.get("role") == ev["role"]]
        mine = [r for r in acts if r.id == ev["activation"]]
        if not mine:
            return "author-activation-unknown"
        # ended: check a later record with issued_utc <= event utc
        later = [r for r in records if r.index > mine[0].index
                 and parse_utc(r.fields["issued_utc"]) <= parse_utc(ev["utc"])
                 and (r.kind == "CMP" or (r.kind == "CTL"
                      and r.fields.get("control") in RESTRICTING)
                      or (r.kind == "ACT"
                          and r.fields.get("role") == ev["role"]))]
        if later:
            return "author-inactive-at-that-time"
    return None


def cmd_reduce(args):
    records, rerrors = [], []
    if args.registry:
        records, rerrors = read_registry(args.registry)
        if rerrors:
            for e in rerrors:
                print("CHAIN-BREAK %s" % e)
            return 1
    events, voids = [], []
    for spec in args.events:
        lane, path = spec.split(":", 1)
        with open(path, "r", encoding="utf-8") as fh:
            for ln in fh:
                if not ln.strip() or ln.startswith("#"):
                    continue
                ev = parse_event_line(ln)
                if ev is None:
                    print("PARSE-FAIL %s: %r" % (path, ln.strip()))
                    return 2
                ev["lane"] = lane
                reason = events_void(records, ev) if records else None
                if reason:
                    voids.append((ev, reason))
                else:
                    events.append(ev)
    order = {"TASK-CUT": 1, "CLAIM": 2, "DELIVER": 3, "GATE": 4, "CERT": 5,
             "PAUSE": 6, "UNPAUSE": 7}
    events.sort(key=lambda e: (parse_utc(e["utc"]), e["lane"], e["seq"]))
    state, blocked_by, claims = {}, {}, {}
    for ev in events:
        t = ev["task"]
        if ev["type"] == "CLAIM":
            claims.setdefault(t, []).append(ev)
        if ev["type"] == "TASK-CUT":
            state[t] = "OPEN"
        elif ev["type"] == "CLAIM":
            state[t] = "CLAIMED"
        elif ev["type"] == "DELIVER":
            state[t] = "DELIVERED"
            if "blocked_by" in ev["keys"]:
                blocked_by[t] = [x for x in ev["keys"]["blocked_by"].split(",")
                                 if x]
        elif ev["type"] == "GATE":
            v = ev["keys"].get("verdict", "?")
            state[t] = {"PASS": "PASSED", "FAIL": "INCOMPLETE",
                        "PARTIAL": "INCOMPLETE"}.get(v, "GATE-" + v)
        elif ev["type"] == "CERT":
            state[t] = "CERTIFIED"
        elif ev["type"] == "PAUSE":
            state[t] = "PAUSED"
        elif ev["type"] == "UNPAUSE":
            state[t] = "OPEN"
    conflicts, cycles, stale = [], [], []
    for t, cs in claims.items():
        acts = {c["activation"] for c in cs}
        if len(acts) > 1 and state.get(t) in ("CLAIMED", "OPEN"):
            conflicts.append("double-claim task=%s activations=%s"
                             % (t, ",".join(sorted(acts))))
    graph = {}
    for t, deps in blocked_by.items():
        graph[t] = deps
    for t, deps in graph.items():
        for d in deps:
            if d not in state or state.get(d) in ("CERTIFIED", "PASSED"):
                stale.append("stale-block task=%s dep=%s" % (t, d))
        seen, stack = set(), [t]
        while stack:
            cur = stack.pop()
            for nxt in graph.get(cur, []):
                if nxt == t:
                    cycles.append("dep-cycle task=%s" % t)
                    break
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
    coverage = {}
    for ev in events:
        if ev["type"] == "DELIVER":
            for k in ("audited", "pending", "records"):
                if k in ev["keys"]:
                    coverage[k] = coverage.get(k, 0) + int(ev["keys"][k])
    out = []
    w = out.append
    w("# fleet queue state (GENERATED by fleet2check reduce; do not edit)")
    w("")
    w("| task | state | last event (utc, lane, type) |")
    w("|---|---|---|")
    last = {}
    for ev in events:
        last[ev["task"]] = ev
    for t in sorted(state, key=lambda x: (state[x], x)):
        ev = last[t]
        w("| %s | %s | %s %s %s |" % (t, state[t], ev["utc"], ev["lane"],
                                      ev["type"]))
    w("")
    w("coverage: %s" % (json.dumps(coverage, sort_keys=True)))
    w("void-events: %d" % len(voids))
    for ev, reason in voids:
        w("  VOID %s %s %s reason=%s" % (ev["utc"], ev["lane"], ev["type"],
                                         reason))
    for c in conflicts:
        w("CONFLICT %s" % c)
    for c in cycles:
        w("DEP-CYCLE %s" % c)
    for st in stale:
        w("STALE-BLOCK %s" % st)
    text = "\n".join(out) + "\n"
    if args.emit_md:
        with open(args.emit_md, "w", encoding="utf-8") as fh:
            fh.write(text)
    sys.stdout.write(text)
    if args.json:
        print(json.dumps({"state": state, "coverage": coverage,
                          "conflicts": conflicts, "cycles": cycles,
                          "stale": stale,
                          "void": [{"seq": e["seq"], "lane": e["lane"],
                                    "type": e["type"], "reason": r}
                                   for e, r in voids]}, sort_keys=True))
    return 1 if (conflicts or cycles) else 0


# ---------------------------------------------------------------- gates

def parse_kv_lines(text, keys=("source", "policy", "suite", "seeded_vs_independent",
                              "verdict", "rotation", "run_manifest")):
    out = {}
    for ln in text.splitlines():
        s = ln.strip()
        for k in keys:
            if s.startswith(k + ":") or s.startswith(k + "="):
                sep = ":" if (k + ":") in s[:len(k) + 1] else "="
                out[k] = s.split(sep, 1)[1].strip()
    return out


def cmd_gate_check(args):
    with open(args.gate, "r", encoding="utf-8") as fh:
        text = fh.read()
    kv = parse_kv_lines(text)
    records, rerrors = [], []
    if args.registry:
        records, rerrors = read_registry(args.registry)
        if rerrors:
            for e in rerrors:
                print("CHAIN-BREAK %s" % e)
            return 1
    fails = []
    gk = kv.get("gatekeeper_activation") or parse_kv_lines(
        text, ("gatekeeper_activation", "producer_activation")).get(
        "gatekeeper_activation")
    kv2 = parse_kv_lines(text, ("gatekeeper_activation", "producer_activation",
                                "source", "policy", "suite", "rotation",
                                "seeded_vs_independent", "verdict",
                                "run_manifest", "adversarial_sample"))
    kv.update(kv2)
    if records:
        amap = active_map(records)
        ok = any(r.id == kv.get("gatekeeper_activation")
                 and r.fields.get("role") == "ORCHESTRATOR"
                 for r in records if r.kind == "ACT")
        if not ok:
            fails.append("GATE-ORPHAN")
        elif amap.get("ORCHESTRATOR") and \
                amap["ORCHESTRATOR"][0].id != kv.get("gatekeeper_activation"):
            fails.append("GATE-ORPHAN")
        if amap.get("ORCHESTRATOR") and amap["ORCHESTRATOR"][1]:
            fails.append("GATE-FROZEN-OR-BLOCKED")
    rows = [ln for ln in text.splitlines()
            if ln.strip().startswith("|") and "CRIT-" in ln]
    if not rows:
        fails.append("CRITERIA-GAP")
    verdicts = []
    for ln in rows:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 4:
            fails.append("CRITERIA-MALFORMED")
            continue
        v = cells[2].upper()
        if v not in ("PASS", "FAIL", "NOT-RUN"):
            fails.append("BAD-VERDICT:%s" % v)
        verdicts.append(v)
    verdict = (kv.get("verdict") or "").upper()
    if verdict == "PASS" and any(v != "PASS" for v in verdicts):
        fails.append("CERT-WITH-FAIL")
    rm = re.search(r"run_manifest=(\S+)\s+([0-9a-f]{64})", text)
    if rm:
        kv["run_manifest"] = rm.group(2)
    if "run_manifest" not in kv or not HEX64.match(
            (kv.get("run_manifest", "").split()[-1] if kv.get("run_manifest")
             else "")):
        fails.append("NO-FRESH-RUN")
    if "seeded_vs_independent" not in kv:
        fails.append("SEEDED-AS-INDEPENDENT")
    if "precision" in text.lower() and "seal" not in text.lower():
        fails.append("NO-SEAL")
    if "rotation" in kv:
        m = re.search(r"#?\s*(\d+)", kv["rotation"])
        if m and int(m.group(1)) > 3:
            fails.append("GATE-ROTATION")
    if "source" not in kv or not HEX7.match(kv.get("source", "")):
        fails.append("NO-SOURCE-BINDING")
    if not HEX64.match(kv.get("policy", "")):
        fails.append("NO-POLICY-BINDING")
    if fails:
        print("GATE: INVALID %s" % " ".join(sorted(set(fails))))
        return 1
    print("GATE: OK criteria=%d pass=%d fail=%d notrun=%d verdict=%s"
          % (len(verdicts), verdicts.count("PASS"), verdicts.count("FAIL"),
             verdicts.count("NOT-RUN"), verdict or "-"))
    return 0


# ---------------------------------------------------------------- run manifest

REQUIRED_RUN_FIELDS = ("run_id", "activation", "started_utc", "command",
                       "fresh", "policy_sha256", "corpus_zip_sha256",
                       "tool_digest", "inputs", "outputs", "resume", "counters")


def cmd_verify_run(args):
    with open(args.manifest, "r", encoding="utf-8") as fh:
        m = json.load(fh)
    fails = []
    for f in REQUIRED_RUN_FIELDS:
        if f not in m:
            fails.append("RUN-MISSING-FIELD:%s" % f)
    if fails:
        print("RUN: REJECT %s" % " ".join(fails))
        return 1
    resume = m.get("resume") or {}
    if m.get("fresh") and resume.get("used_cache"):
        fails.append("RUN-RESUME-LAUNDER")
    if resume.get("used_cache"):
        for item in resume.get("inherited") or []:
            if not isinstance(item, dict) or not item.get("provenance_manifest") \
                    or not HEX64.match(str(item.get("provenance_sha256", ""))) \
                    or not item.get("verified"):
                fails.append("RUN-RESUME-LAUNDER")
    lost = m.get("lost")
    if lost and m.get("tool_commit") and m["tool_commit"] == lost:
        fails.append("RUN-USES-LOST-COMMIT")
    if args.tool_digest and m.get("tool_digest") != args.tool_digest:
        fails.append("RUN-TOOL-DIGEST-MISMATCH")
    if args.previous:
        with open(args.previous, "r", encoding="utf-8") as fh:
            prev = json.load(fh)
        pcount = {i.get("path"): i.get("records", i.get("sha256"))
                  for i in prev.get("outputs", [])}
        for o in m.get("outputs", []):
            old = pcount.get(o.get("path"))
            new = o.get("records", o.get("sha256"))
            if isinstance(old, int) and isinstance(new, int) and new < old:
                fails.append("RUN-COUNT-DROP:%s" % o.get("path"))
    if args.root:
        for o in m.get("outputs", []):
            p = os.path.join(args.root, o["path"])
            if os.path.exists(p) and sha256_file(p) != o.get("sha256"):
                fails.append("RUN-OUTPUT-DIGEST-MISMATCH:%s" % o["path"])
    if args.reject_inherited and resume.get("used_cache"):
        fails.append("RUN-RELEASE-INELIGIBLE-INHERITED")
    if fails:
        print("RUN: REJECT %s" % " ".join(sorted(set(fails))))
        return 1
    label = "inherited" if resume.get("used_cache") else "fresh"
    print("RUN: OK run_id=%s (%s) outputs=%d counters=%s"
          % (m["run_id"], label, len(m.get("outputs", [])),
             json.dumps(m.get("counters", {}), sort_keys=True)))
    return 0


def cmd_control_render(args):
    rows = []
    with open(args.log, "r", encoding="utf-8") as fh:
        for ln in fh:
            if not ln.strip() or ln.startswith("#"):
                continue
            p = ln.rstrip("\n").split("|")
            if len(p) < 6:
                print("PARSE-FAIL %r" % ln.strip())
                return 2
            rows.append(p)
    if not rows:
        print("CONTROL: EMPTY (%s)" % args.log)
        return 1
    last = rows[-1]
    out = ["<!-- GENERATED by fleet2check control-render from %s; do not edit -->"
           % args.log,
           "# control state — %s" % (args.lane or "lane"),
           "",
           "checked_utc: %s" % last[0],
           "main_head: %s" % last[1],
           "registry_head: %s %s" % (last[2], last[3]),
           "record_seq: %s" % last[4],
           "decision: %s" % last[5],
           "note: %s" % (last[6] if len(last) > 6 else "-"),
           "checks_logged: %d" % len(rows)]
    seqs = [int(r[4]) for r in rows]
    out.append("seq_monotonic: %s" % ("yes" if seqs == sorted(seqs) else "NO"))
    text = "\n".join(out) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
    sys.stdout.write(text)
    return 0


# ---------------------------------------------------------------- observe / zombie

def cmd_observe(args):
    obs = []
    for spec in args.control_logs:
        lane, path = spec.split(":", 1)
        with open(path, "r", encoding="utf-8") as fh:
            for ln in fh:
                if not ln.strip() or ln.startswith("#"):
                    continue
                p = ln.rstrip("\n").split("|")
                if len(p) < 6:
                    print("PARSE-FAIL %s %r" % (path, ln.strip()))
                    return 2
                obs.append({"lane": lane, "utc": parse_utc(p[0]),
                            "main_head": p[1], "head_id": p[2], "head_hash": p[3],
                            "seq": int(p[4]), "verdict": p[5]})
    obs.sort(key=lambda o: (o["utc"], o["lane"]))
    fails = []
    seen_seq = {}
    last_seq = -1
    for o in obs:
        if o["seq"] < last_seq:
            fails.append("MAIN-MOVED seq-regression %s:%s< %s"
                         % (o["lane"], o["seq"], last_seq))
        last_seq = max(last_seq, o["seq"])
        prev = seen_seq.get(o["seq"])
        if prev and prev[1] != o["head_hash"]:
            fails.append("MAIN-MOVED hash-divergence seq=%s %s!=%s"
                         % (o["seq"], prev[1][:12], o["head_hash"][:12]))
        seen_seq[o["seq"]] = (o["head_id"], o["head_hash"])
    if fails:
        print("VERDICT: MAIN-MOVED")
        for f in fails:
            print("  " + f)
        return 1
    print("VERDICT: OK observations=%d lanes=%d head_seq=%s"
          % (len(obs), len(set(o["lane"] for o in obs)), last_seq))
    return 0


def cmd_zombie(args):
    rows = []
    for spec in args.events:
        lane, path = spec.split(":", 1)
        with open(path, "r", encoding="utf-8") as fh:
            for ln in fh:
                if not ln.strip() or ln.startswith("#"):
                    continue
                ev = parse_event_line(ln)
                if ev is None:
                    print("PARSE-FAIL %s %r" % (path, ln.strip()))
                    return 2
                ev["lane"] = lane
                rows.append(ev)
    rows.sort(key=lambda e: (parse_utc(e["utc"]), e["lane"], e["seq"]))
    window = datetime.timedelta(minutes=args.window_min)
    verdicts = []
    for lane in sorted(set(r["lane"] for r in rows)):
        lane_rows = [r for r in rows if r["lane"] == lane]
        if not lane_rows:
            continue
        end = parse_utc(lane_rows[-1]["utc"])
        win = [r for r in lane_rows if end - parse_utc(r["utc"]) <= window]
        substance = [r for r in win if r["type"] in SUBSTANTIVE_EVENTS]
        statuses = [r for r in win if r["type"] in STATUS_EVENTS]
        laundering = [r for r in statuses if r["type"] in ("ORDER", "ESCALATION")]
        plain = [r for r in statuses if r["type"] not in ("ORDER", "ESCALATION")]
        if substance:
            verdicts.append((lane, "OK", len(substance), len(statuses)))
            continue
        if len(plain) >= args.threshold or len(laundering) > 1:
            verdicts.append((lane, "ZOMBIE", 0, len(statuses)))
        else:
            verdicts.append((lane, "WATCH", 0, len(statuses)))
    rc = 0
    for lane, v, s, st in verdicts:
        print("ZOMBIE %-10s %-6s substance=%d status_events=%d (window=%dmin)"
              % (lane, v, s, st, args.window_min))
        if v == "ZOMBIE":
            rc = 1
    if not verdicts:
        print("ZOMBIE (no events)")
    return rc


# ---------------------------------------------------------------- orders/freshness/alerts

def cmd_orders(args):
    with open(args.order, "r", encoding="utf-8") as fh:
        text = fh.read()
    kv = parse_kv_lines(text, ("order", "issued_utc", "ack_due_utc", "policy",
                               "target", "activation"))
    fails = []
    for f in ("order", "issued_utc", "ack_due_utc", "policy"):
        if f not in kv:
            fails.append("ORDER-MISSING-%s" % f)
    if not HEX64.match(kv.get("policy", "")):
        fails.append("ORDER-NO-POLICY-SHA")
    low = text.lower()
    for bad in ORDER_BANNED:
        if bad in low:
            fails.append("ORDER-FORBIDDEN-PHRASE:%r" % bad)
    if args.registry:
        records, errors = read_registry(args.registry)
        if errors:
            for e in errors:
                print("CHAIN-BREAK %s" % e)
            return 1
        tgt = kv.get("target", "")
        if tgt:
            m = CTL_TARGET.match(tgt)
            known = {r.id for r in records}
            roles = {r.fields.get("role") for r in records if r.kind == "ACT"}
            if not m:
                fails.append("ORDER-TARGET-MALFORMED")
            elif m.group(1) not in roles and m.group(1) != "*":
                fails.append("ORDER-TARGET-UNKNOWN-ROLE")
            elif m.group(2) not in known and m.group(2) != "*":
                fails.append("ORDER-TARGET-UNKNOWN-ACTIVATION")
    if fails:
        print("ORDER: ILLEGAL %s" % " ".join(sorted(set(fails))))
        return 1
    print("ORDER: OK order=%s target=%s ack_due=%s"
          % (kv.get("order"), kv.get("target", "-"), kv.get("ack_due_utc")))
    return 0


def cmd_freshness(args):
    fails = []
    for spec in args.heartbeat_logs or []:
        lane, path = spec.split(":", 1)
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as fh:
            for i, ln in enumerate(fh, 1):
                s = ln.strip()
                if not s or s.startswith("#"):
                    continue
                if not re.search(r"\b[0-9a-f]{7,40}\b", s):
                    fails.append("STALE-REF %s:%d (no sha in line)" % (lane, i))
    for spec in args.events or []:
        lane, path = spec.split(":", 1)
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as fh:
            for i, ln in enumerate(fh, 1):
                ev = parse_event_line(ln)
                if ev is None:
                    continue
                if ev["type"] in ("GATE", "DELIVER", "HO", "CHK"):
                    k = ev["keys"]
                    if not HEX7.match(k.get("source", "")):
                        fails.append("STALE-REF %s:%d %s missing source ref"
                                     % (lane, i, ev["type"]))
                    if not HEX64.match(k.get("policy", "")):
                        fails.append("STALE-REF %s:%d %s missing policy ref"
                                     % (lane, i, ev["type"]))
    if fails:
        print("FRESHNESS: FAIL")
        for f in fails[:20]:
            print("  " + f)
        return 1
    print("FRESHNESS: OK")
    return 0


CLASS_HINTS = {
    "worker": ("worker quiet", "worker stalled", "zombie"),
    "orchestrator": ("orchestrator quiet", "orchestrator silent"),
    "boss": ("boss quiet", "boss silent"),
    "starvation": ("queue starved", "starvation"),
}


def cmd_alerts(args):
    now = parse_utc(args.now) if args.now else datetime.datetime.now(
        datetime.timezone.utc)
    alerts_text = ""
    if args.alerts and os.path.exists(args.alerts):
        with open(args.alerts, "r", encoding="utf-8") as fh:
            alerts_text = fh.read().lower()
    missing = []
    for spec in args.lanes:
        name, path = spec.split(":", 1)
        if not os.path.exists(path):
            continue
        last = None
        with open(path, "r", encoding="utf-8") as fh:
            for ln in fh:
                m = re.search(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)", ln)
                if m:
                    last = m.group(1)
        if last is None:
            missing.append("%s (no timestamp in heartbeat log)" % name)
            continue
        age = (now - parse_utc(last)).total_seconds() / 60.0
        limit = args.boss_limit if name == "boss" else args.limit
        if age > limit:
            hint = CLASS_HINTS.get(name, (name + " quiet",))
            if not any(h in alerts_text for h in hint):
                missing.append("%s quiet %.1f min but no matching class in "
                               "ALERTS.md" % (name, age))
    if missing:
        print("ALERTS: MISSING-CLASS")
        for m in missing:
            print("  " + m)
        return 1
    print("ALERTS: OK")
    return 0


# ---------------------------------------------------------------- selftest

def cmd_selftest(_args):
    import subprocess
    here = os.path.dirname(os.path.abspath(__file__))
    return subprocess.call([sys.executable, os.path.join(here,
                                                         "test_fleet2check.py")])


def main(argv=None):
    ap = argparse.ArgumentParser(description="fleet-2.0 record checker")
    sub = ap.add_subparsers(dest="cmd")

    p = sub.add_parser("manifest")
    p.add_argument("--dir", required=True)
    p.add_argument("paths", nargs="+")
    p.set_defaults(func=cmd_manifest)

    p = sub.add_parser("verify-activation")
    p.add_argument("--registry", required=True)
    p.add_argument("--activation", required=True)
    p.add_argument("--role")
    p.add_argument("--lane")
    p.add_argument("--nonce")
    p.add_argument("--anchor", required=True)
    p.add_argument("--policy")
    p.set_defaults(func=cmd_verify_activation)

    p = sub.add_parser("active-role")
    p.add_argument("--registry", required=True)
    p.set_defaults(func=cmd_active_role)

    p = sub.add_parser("controls")
    p.add_argument("--registry", required=True)
    p.add_argument("--role")
    p.add_argument("--activation")
    p.add_argument("--legacy", action="append")
    p.set_defaults(func=cmd_controls)

    p = sub.add_parser("record-check")
    p.add_argument("--file", required=True)
    p.set_defaults(func=cmd_record_check)

    p = sub.add_parser("reduce")
    p.add_argument("--registry")
    p.add_argument("--events", action="append", required=True)
    p.add_argument("--json", action="store_true")
    p.add_argument("--emit-md", metavar="PATH",
                   help="write the generated state file (05 §2)")
    p.set_defaults(func=cmd_reduce)

    p = sub.add_parser("gate-check")
    p.add_argument("--gate", required=True)
    p.add_argument("--registry")
    p.set_defaults(func=cmd_gate_check)

    p = sub.add_parser("verify-run")
    p.add_argument("--manifest", required=True)
    p.add_argument("--tool-digest")
    p.add_argument("--previous")
    p.add_argument("--root")
    p.add_argument("--reject-inherited", action="store_true")
    p.set_defaults(func=cmd_verify_run)

    p = sub.add_parser("control-render")
    p.add_argument("--log", required=True)
    p.add_argument("--lane")
    p.add_argument("--out")
    p.set_defaults(func=cmd_control_render)

    p = sub.add_parser("observe")
    p.add_argument("--control-logs", nargs="+", required=True)
    p.set_defaults(func=cmd_observe)

    p = sub.add_parser("zombie")
    p.add_argument("--events", action="append", required=True)
    p.add_argument("--window-min", type=int, default=20)
    p.add_argument("--threshold", type=int, default=3)
    p.set_defaults(func=cmd_zombie)

    p = sub.add_parser("orders")
    p.add_argument("--order", required=True)
    p.add_argument("--registry")
    p.set_defaults(func=cmd_orders)

    p = sub.add_parser("freshness")
    p.add_argument("--heartbeat-logs", action="append")
    p.add_argument("--events", action="append")
    p.set_defaults(func=cmd_freshness)

    p = sub.add_parser("alerts")
    p.add_argument("--lanes", nargs="+", required=True)
    p.add_argument("--alerts")
    p.add_argument("--now")
    p.add_argument("--limit", type=float, default=20.0)
    p.add_argument("--boss-limit", type=float, default=30.0)
    p.set_defaults(func=cmd_alerts)

    p = sub.add_parser("selftest")
    p.set_defaults(func=cmd_selftest)

    args = ap.parse_args(argv)
    if not getattr(args, "func", None):
        ap.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
