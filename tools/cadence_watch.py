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


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def next_seq():
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
    a = ap.parse_args()
    n = 0
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
        fact = ("cadence: main %s, orch2 %s, boss2 %s, pause %s, pending %d%s"
                % (main, orch, boss, "REMOVED" if removed else ("present" if paused else "absent"),
                   len(pend), (" [" + ",".join(pend[:4]) + "]") if pend else ""))
        line = "  %s cadence check %d (auto): %s" % (utc(), n, fact)
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        with open(CONTROL, "a", encoding="utf-8") as fh:
            fh.write("%s|%s|A-2026-09-25-001|%s|%d|OK|%s\n"
                     % (utc(), main, REGISTRY_SHA, next_seq(), fact))
        print("[%s] %s" % (utc(), fact), flush=True)
        if (not paused) or removed:
            print("WORK ORDER SIGNAL: pause absent/removed on the ORCH-2 lane", flush=True)
        if a.cycles and n >= a.cycles:
            return 0
        time.sleep(a.interval)


if __name__ == "__main__":
    sys.exit(main())
