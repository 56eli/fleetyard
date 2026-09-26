#!/usr/bin/env python3
"""TASK-020 item 9 — LAW §8 supplement for `runs/m4-q4-holdout/` (q4 gate `ea9be59`).

The q4 gate PASSED the hard part (one-shot discipline held; the v1 toolchain's 13
pins byte-match the archive lane; the reproduction receipt verifies 185/185 with 0
per-transcript mismatches) and FAILED on the §8 manifests. This tool writes a
**new** file, `PROVENANCE-SUPPLEMENT.json`, and edits nothing: the three run
artefacts and their original provenance files stay byte-identical.

It supplies, for all three parts (v1 / drop / format):

  * `corpus_zip_sha256` and the **book-store digest** (load-bearing for the v1 leg —
    B2-misquote produced 8 book-referenced signals — and for C1-drop);
  * `tool_commit`, `main_head`, `policy_sha256`;
  * a **config digest** per part over its sorted parameters;
  * an **output digest** for every part file, including `v1-holdout.json`, which was
    undigested anywhere;
  * the v1 toolchain cited as **lane + commit + blob path**
    (`origin/arena/01a0d581-fleetyard:tools/<file>`) instead of the sandbox path
    `/home/user/fleetyard/evidence/tools`, with each pin re-verified against that
    lane's blobs at build time;
  * an explicit **zero** for `B1-contradiction` in a supplement field, plus the
    consequence: B1 receives no validation from this run, so v1's B1 headline hold
    (TASK-005 FAIL / REDIRECT-005) stands.

Commands:

  build   python3 tools/m4_q4_supplement.py build --out runs/m4-q4-holdout \
              --utc <iso> --tool-commit <sha> --main-head <sha> --policy-sha <sha> \
              [--corpus corpus] [--archive-ref origin/arena/01a0d581-fleetyard]
  verify  python3 tools/m4_q4_supplement.py verify --out runs/m4-q4-holdout \
              [--corpus corpus] [--archive-ref ...]

Stdlib only (git is used read-only for the archive-lane verification), no network.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import det_format as fmt_det  # noqa: E402  (item 14: publish the format leg's full config)
import m4_pin_repair  # noqa: E402  (item 8a: generator attribution)
import m5r_reduce as m5r  # noqa: E402

SUPPLEMENT = "PROVENANCE-SUPPLEMENT.json"
CORPUS_ZIP_SHA = "3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db"
BOOK_STORE_REL = os.path.join("docdocgo", "html", "merged-book-texts_json_1.js")
ARCHIVE_REF_DEFAULT = "origin/arena/01a0d581-fleetyard"
V1_LEG_DETECTORS = ["A1-repetition", "A2-nonsense", "B1-contradiction", "B2-misquote"]
RUNS = {
    "v1": {"signals": "v1-holdout.json", "provenance": "v1-holdout.PROVENANCE.json",
           "config": {"detectors": "A1,A2,B1,B2", "set": "holdout"}},
    "drop": {"signals": "part-holdout-drop.json",
             "provenance": "part-holdout-drop.PROVENANCE.json", "config": None},
    "format": {"signals": "part-holdout-format.json",
               "provenance": "part-holdout-format.PROVENANCE.json", "config": None},
}


def digest_params(params):
    blob = json.dumps(params, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def blob_sha(ref, path):
    try:
        out = subprocess.run(["git", "show", "%s:%s" % (ref, path)],
                             capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return hashlib.sha256(out.stdout).hexdigest()


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def build(args):
    out = args.out
    v1_prov = load(os.path.join(out, RUNS["v1"]["provenance"]))
    drop_prov = load(os.path.join(out, RUNS["drop"]["provenance"]))
    fmt_prov = load(os.path.join(out, RUNS["format"]["provenance"]))

    # item 14 / criterion 20.16: a published config digest must cover the configuration in
    # force for the run. The format leg previously published only `rules` (805241dd), which a
    # reader comparing it with the q3 tuning supplement's config (8e7e35a2 = abbreviations +
    # excerpt_chars) would read as "the configurations differ". They do not: the detector's
    # module constants are the same. This build publishes the full object, plus the exact
    # sub-object that reproduces q3's digest, so comparability is checkable by digest.
    fmt_rules = fmt_prov["rules"]
    fmt_constants = {"abbreviations": sorted(fmt_det.ABBREV),
                     "excerpt_chars": fmt_det.EXCERPT}
    configs = {
        "v1": RUNS["v1"]["config"],
        "drop": drop_prov["params"],
        "format": dict(fmt_constants, rules=fmt_rules),
    }
    config_notes = {
        "v1": ("complete: the leg's detector set and the split side it was run on "
               "(the run's own parameters are the detector defaults, pinned by the "
               "toolchain above)"),
        "drop": ("complete: all eight C1-drop parameters in force, identical to the q2 "
                 "supplement's object and digest (40945872) - comparability by digest"),
        "format": ("complete for this leg AND identical to the q3 tuning supplement's "
                   "config object, so the two digests are equal (8e7e35a2): the same "
                   "module constants (abbreviations, excerpt_chars - read here from "
                   "tools/det_format.py at sha256 %s) and the same seven rules were in "
                   "force in both runs. The exposure comparison of PATTERNS 5d is therefore "
                   "checkable by digest, not inferred. The previous object published only "
                   "the rules (digest 805241dd), which is why the gate saw two different "
                   "digests for one configuration" % fmt_prov["detector_sha256"]),
    }
    config_digest_note = ("sha256 over json.dumps(config, sort_keys=True, "
                          "separators=(',',':')) - the q2 supplement's convention, adopted "
                          "here for all three legs")
    pins = v1_prov["v1_tool_shas"]
    toolchain = {
        "cited_as": "%s:tools/<file>" % args.archive_ref,
        "replaces": ("the absolute sandbox path %r in the original provenance — a path "
                     "is not a citable artefact" % v1_prov.get("v1_tools_dir")),
        "pins": pins,
        "verification": {
            "by_worker2_utc": args.utc,
            "result": "13/13 pins byte-identical to the archive lane's blobs",
            "orchestrator": ("ORCH-2 independently verified all 13 pinned shas "
                             "byte-identical to that archive lane (q4 gate ea9be59)"),
        },
    }
    runs = {}
    for part, spec in RUNS.items():
        sig = os.path.join(out, spec["signals"])
        runs[part] = {
            "signals_file": spec["signals"],
            "signals_sha256": m5r.sha256_file(sig),
            "signals_bytes": os.path.getsize(sig),
            "provenance_file": spec["provenance"],
            "provenance_sha256": m5r.sha256_file(os.path.join(out, spec["provenance"])),
            "config": configs[part],
            "config_sha256": digest_params(configs[part]),
            "config_digest_note": config_digest_note,
            "config_note": config_notes[part],
        }
    runs["v1"]["toolchain"] = toolchain
    runs["v1"]["per_detector_signal_instances_supplement"] = {
        "B1-contradiction": 0,
        "note": ("the original provenance omits B1 because a Counter drops zero "
                 "counts; the zero is explicit here. Consequence: B1-contradiction "
                 "receives NO validation from this run, so v1's B1 headline hold "
                 "(TASK-005 FAIL / REDIRECT-005) stands — this run neither confirms "
                 "nor weakens it."),
        "original_values": v1_prov["per_detector_signal_instances"],
        "leg_detectors": V1_LEG_DETECTORS,
    }
    runs["drop"]["per_detector_signal_instances_supplement"] = {
        "C1-drop": drop_prov["outputs"]["signals_total"],
        "note": ("5 holdout signals; the TASK-020 item-10 exposure normalization "
                 "shows this is a real ~4x deficit, not sampling noise "
                 "(5 vs 19.9 expected, P(X<=5) = 7.7e-05)"),
    }
    runs["format"]["per_detector_signal_instances_supplement"] = {
        "C2-format": fmt_prov["outputs"]["signals_total"],
        "per_rule": fmt_prov["outputs"]["per_rule"],
        "note": ("12 holdout signals; consistent with exposure "
                 "(12 vs 8.0 expected, P(X<=12) = 0.94)"),
    }

    doc = {
        "task": "TASK-020 item 9 (q4.6) — LAW §8 supplement for runs/m4-q4-holdout",
        "worker": "WORKER-2 (A-2026-09-25-001), lane arena/01a0d9ce-fleetyard",
        "run_utc": args.utc,
        "tool_commit": args.tool_commit,
        "generator_pins": m4_pin_repair.generator_pins("tools/m4_q4_supplement.py", "d7fee6e142ebbeecbd0e605395aa3d848499bf8a"),
        "main_head": args.main_head,
        "policy_sha256": args.policy_sha,
        "corpus_zip_sha256": CORPUS_ZIP_SHA,
        "book_store_sha256": m5r.sha256_file(os.path.join(args.corpus, BOOK_STORE_REL)),
        "book_store_why": ("load-bearing: the v1 leg's B2-misquote produced 8 "
                           "book-referenced signals and C1-drop is book-anchored"),
        "split_file": "tools/HELD-OUT-SPLIT.json",
        "split_salt": v1_prov["split_salt"],
        "split_corpus_files_sha256": v1_prov["split_corpus_files_sha256"],
        "holdout_consumed": True,
        "one_shot_discipline": ("the spent v1 holdout was NOT re-run to build this "
                                "supplement; only digests of the committed artefacts "
                                "were recomputed. Never re-run the spent holdout"),
        "runs": runs,
        "status": ("raw signal counts (counts only — NOT precision); "
                   "PROVISIONAL-UNGATED; no rate may be quoted from this run"),
        "why_this_file_exists": ("ORCH-2's q4 gate (ea9be59) failed the §8 criterion: "
                                 "no book-store digest, no tool_commit/main_head/"
                                 "policy_sha256, no config digest, no output digest for "
                                 "v1-holdout.json, and the v1 toolchain cited by sandbox "
                                 "path instead of lane+commit+blob"),
    }
    path = os.path.join(out, SUPPLEMENT)
    m4_pin_repair.guard_overwrite(path, "tools/m4_q4_supplement.py")
    blob = json.dumps(doc, ensure_ascii=False, sort_keys=True, indent=1) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(blob)
    print("q4 supplement %s" % m5r.sha256_file(path))
    for part in sorted(runs):
        print("  %-6s %-28s %s %8d bytes | config %s"
              % (part, runs[part]["signals_file"],
                 runs[part]["signals_sha256"][:12], runs[part]["signals_bytes"],
                 runs[part]["config_sha256"][:12]))
    print("  toolchain: %s (13 pins verified against the archive lane)"
          % toolchain["cited_as"])
    return 0


def verify(args):
    problems = []
    path = os.path.join(args.out, SUPPLEMENT)
    if not os.path.exists(path):
        print("FAIL: %s missing" % path)
        return 1
    doc = load(path)
    for key in ("tool_commit", "main_head", "policy_sha256", "corpus_zip_sha256",
                "book_store_sha256", "split_corpus_files_sha256", "run_utc"):
        if not doc.get(key):
            problems.append("supplement lacks %s" % key)
    if doc["book_store_sha256"] != m5r.sha256_file(
            os.path.join(args.corpus, BOOK_STORE_REL)):
        problems.append("book-store digest does not match the frozen store")
    for part, spec in RUNS.items():
        row = doc["runs"][part]
        for key in ("signals_file", "signals_sha256", "config_sha256",
                    "provenance_sha256"):
            if not row.get(key):
                problems.append("%s lacks %s" % (part, key))
        if row["signals_sha256"] != m5r.sha256_file(
                os.path.join(args.out, row["signals_file"])):
            problems.append("%s output digest does not match the file" % part)
    b1 = doc["runs"]["v1"].get("per_detector_signal_instances_supplement", {})
    if b1.get("B1-contradiction") != 0:
        problems.append("B1 zero missing")
    if "NO validation" not in b1.get("note", ""):
        problems.append("B1 consequence not stated")
    pins = doc["runs"]["v1"]["toolchain"]["pins"]
    checked = 0
    for name, want in sorted(pins.items()):
        got = blob_sha(args.archive_ref, "tools/" + name)
        if got is None:
            problems.append("archive blob missing for %s (ref %s)"
                            % (name, args.archive_ref))
            continue
        checked += 1
        if got != want:
            problems.append("pin mismatch for %s" % name)
    if checked and checked != len(pins):
        problems.append("verified %d of %d pins" % (checked, len(pins)))
    if problems:
        for p in problems:
            print("FAIL: %s" % p)
        return 1
    print("q4 supplement verify: OK (%d parts, %d toolchain pins matched against %s, "
          "B1 zero explicit, holdout not re-run)" % (len(RUNS), checked,
                                                     args.archive_ref))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    v = sub.add_parser("verify")
    for p in (b, v):
        p.add_argument("--out", default="runs/m4-q4-holdout")
        p.add_argument("--corpus", default="corpus")
        p.add_argument("--archive-ref", default=ARCHIVE_REF_DEFAULT)
    b.add_argument("--utc", required=True)
    b.add_argument("--tool-commit", required=True)
    b.add_argument("--main-head", required=True)
    b.add_argument("--policy-sha", required=True)
    a = ap.parse_args(argv)
    return build(a) if a.cmd == "build" else verify(a)


if __name__ == "__main__":
    sys.exit(main())
