#!/usr/bin/env python3
"""Cadence watcher (WORKER-2) — liveness + work-order watch.

Owner ERRATA-2026-09-25f: the worker's steady state is to cycle indefinitely
looking for work orders; liveness = heartbeat + CONTROL.log at cadence, not
output. This watcher keeps that cadence while the shift is paused, and watches
for (a) the scoped PAUSE being lifted/removed on the ORCH-2 lane, (b) a new
ORCH-2 head carrying a gate verdict, (c) queue changes (pending/claimed task
files), (d) main-head changes. It WRITES ONLY the two log files below and
prints to stdout. It never commits, pushes, or touches any other file/branch.

Usage:  python3 tools/cadence_watch.py [--interval 300] [--cycles 0]
        (--cycles 0 = run until stopped)
"""
import argparse
import datetime
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "fleet", "heartbeats", "WORKER.log")
CONTROL = os.path.join(ROOT, "fleet", "CONTROL.log")
ORCH_LANE = "refs/remotes/origin/arena/01a0d9d0-fleetyard"
PAUSE_PATH = "fleet/controls/PAUSE-WORKER-A-2026-09-25-001"
REGISTRY_SHA = "a86115d2667e7d54ff418524303c9adeca2348709d233e9e1c39480251435c14"


def sh(args, check=False):
    r = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit("cmd failed: %s\n%s" % (" ".join(args), r.stderr))
    return r.stdout.strip()


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import control_row as _control_row  # noqa: E402  (locked CONTROL append)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def next_seq():
    """Kept for callers that only want the number; the APPEND is what must be atomic.

    Cycle J reported reused seqs in `fleet/CONTROL.log`: two writers (this watcher's auto-rows and
    hand-written rows) each computed `max + 1` from a file the other was changing. The row is now
    written by `tools/control_row.py` under an exclusive lock, so `seq` is unique by construction.
    """
    seq = 0
    if os.path.exists(CONTROL):
        for line in open(CONTROL, encoding="utf-8"):
            parts = line.split("|")
            if len(parts) > 4 and parts[4].isdigit():
                seq = max(seq, int(parts[4]))
    return seq + 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", type=int, default=300)
    ap.add_argument("--cycles", type=int, default=0)
    ap.add_argument("--commit", action="store_true",
                    help="commit+push the two log files each cycle (durable steps)")
    a = ap.parse_args()
    n = 0
    last = None
    while True:
        n += 1
        subprocess.run(["git", "fetch", "-q", "origin",
                        "refs/heads/main:refs/remotes/origin/main",
                        "refs/heads/arena/01a0d9d0-fleetyard:" + ORCH_LANE,
                        "refs/heads/arena/01a0d9d1-fleetyard:refs/remotes/origin/arena/01a0d9d1-fleetyard"],
                       cwd=ROOT, capture_output=True, text=True)
        main = sh(["git", "rev-parse", "--short", "origin/main"])
        orch = sh(["git", "rev-parse", "--short", ORCH_LANE])
        boss = sh(["git", "rev-parse", "--short", "origin/arena/01a0d9d1-fleetyard"])
        pause_txt = sh(["git", "cat-file", "-p", "%s:%s" % (ORCH_LANE, PAUSE_PATH)])
        paused = bool(pause_txt)
        # removal marker is a dedicated status line, never a substring match
        # (the file's own "removal:" instruction paragraph mentions REMOVED)
        removed = any(l.strip().upper().startswith(("REMOVED", "STATUS: REMOVED"))
                      for l in pause_txt.splitlines())
        q = sh(["git", "ls-tree", "-r", "--name-only", ORCH_LANE, "fleet/queue/"])
        pend = sorted(l.split("/")[-1] for l in q.splitlines() if "/pending/" in l and l.endswith(".md"))
        gates_tail = sh(["git", "show", "%s:fleet/GATES.md" % ORCH_LANE]).splitlines()
        gates_sig = sum(1 for l in gates_tail if l.startswith("## 2026-"))
        status_tail = sh(["git", "show", "%s:fleet/queue/status.md" % ORCH_LANE])
        status_sig = len(status_tail)
        fact = ("cadence: main %s, orch2 %s, boss2 %s, pause %s, pending %d%s"
                % (main, orch, boss, "REMOVED" if removed else ("present" if paused else "absent"),
                   len(pend), (" [" + ",".join(pend[:4]) + "]") if pend else ""))
        line = "  %s cadence check %d (auto): %s" % (utc(), n, fact)
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        _control_row.append(main, "OK", fact)
        signals = []
        pause_state = "REMOVED" if removed else ("present" if paused else "absent")
        now = (orch, tuple(pend), gates_sig, status_sig, main, boss, pause_state)
        if last is not None and now != last:
            if now[0] != last[0]:
                signals.append("ORCH-2 lane head moved %s -> %s (read the new GATES/queue)"
                               % (last[0], now[0]))
            if now[1] != last[1]:
                signals.append("queue changed: %s" % (sorted(set(now[1]) ^ set(last[1])),))
            if now[2] != last[2]:
                signals.append("GATES.md gained entries (%d -> %d)" % (last[2], now[2]))
            if now[3] != last[3]:
                signals.append("queue/status.md grew (%d -> %d bytes)" % (last[3], now[3]))
            if now[4] != last[4]:
                signals.append("main moved %s -> %s" % (last[4], now[4]))
            if now[5] != last[5]:
                signals.append("BOSS-2 lane moved %s -> %s" % (last[5], now[5]))
            if now[6] != last[6]:
                signals.append("PAUSE control state changed %s -> %s" % (last[6], now[6]))
        last = now
        print("[%s] %s" % (utc(), fact), flush=True)
        for sig in signals:
            print("WORK ORDER SIGNAL: %s" % sig, flush=True)
        if a.commit:
            subprocess.run(["git", "add", "fleet/CONTROL.log", "fleet/heartbeats/WORKER.log"],
                           cwd=ROOT, capture_output=True, text=True)
            r = subprocess.run(["git", "commit", "-q", "-m",
                                "cadence check %d (auto): %s" % (n, fact)],
                               cwd=ROOT, capture_output=True, text=True)
            if r.returncode == 0:
                subprocess.run(["git", "push", "-q", "origin",
                                "arena/01a0d9ce-fleetyard"], cwd=ROOT, capture_output=True)
        if signals:
            print("STOPPING WATCH: work-order signal(s) present", flush=True)
            return 0
        if a.cycles and n >= a.cycles:
            return 0
        time.sleep(a.interval)


if __name__ == "__main__":
    sys.exit(main())
