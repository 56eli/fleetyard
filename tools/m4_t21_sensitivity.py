#!/usr/bin/env python3
"""TASK-021 — C1-drop threshold sensitivity map over the **v2 tuning half only**.

The q2 reader (`runs/m4-q2-dropword/README.md`) states that the shipped operating point is
unchosen and its sensitivity unmeasured, and declines to measure it inside split-v2 discipline
because 33 of the v1 tuning transcripts are now v2-holdout members. This tool measures it on the
side of the seal that may be read: the 197 v2 tuning transcripts.

`build` runs the **unmodified** detector once per setting and writes one part file per setting.

  python3 tools/m4_t21_sensitivity.py build --setting <name> [--scratch DIR] [--out DIR]
  python3 tools/m4_t21_sensitivity.py merge --out DIR --utc <exact> [--tool-commit <sha> ...]
  python3 tools/m4_t21_sensitivity.py verify --out DIR

Every part is one bounded process (LAW §4A): a setting may be sharded from the driver, and each
part carries its own exact `run_utc` and its source.

Holdout discipline is by CONSTRUCTION and by CODE, never by assertion:
  * the run happens over a scratch corpus holding **only the 197 tuning transcripts** (symlinks)
    plus a symlinked book store, so a holdout transcript is absent from the tree being walked;
  * the build refuses if a holdout name is present in that tree, or if the split's tuning and
    holdout sets intersect, and publishes a digest of the sorted overlay listing;
  * a `sys.addaudithook` records every `open` in the process; the part publishes the count of
    holdout files opened (0) and the list is empty by construction;
  * each part publishes `holdout_reads: []` and `holdout_enforced: true`.

What it does NOT do: no threshold is chosen, fitted or recommended; no precision, rate, recall or
M6 figure is produced. Counts only, CANDIDATE-class / PROVISIONAL-UNGATED.

Stdlib only, corpus read-only, writes only under `--out` and the scratch dir (both working trees,
never `corpus/` or `evidence/`).
"""
import argparse
import datetime
import hashlib
import json
import os
import resource
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import det_dropword as dd  # noqa: E402
import m4_q2_evidence as q2ev  # noqa: E402
import m4_t20_supplement as sup  # noqa: E402
import m5r_reduce as m5r  # noqa: E402

SPLIT = "tools/HELD-OUT-SPLIT-V2.json"
CORPUS = "corpus"
OUT = "runs/m4-t21-sensitivity"
STORE_REL = os.path.join("docdocgo", "html", "merged-book-texts_json_1.js")
CORPUS_ZIP_SHA = "3f36c520391049a49876d90e32400d64dd7b721e52b9a1820a0b3b6dca8486db"
SHIPPED = {"min_flank": 3, "min_ratio": 0.85, "min_matched": 10}
FIXED = {"window": 24, "stride": 12, "min_score": 0.20, "top_k": 3, "max_drop": 2}
GRID = (
    ("shipped", {}),
    ("flank-2", {"min_flank": 2}),
    ("flank-5", {"min_flank": 5}),
    ("flank-8", {"min_flank": 8}),
    ("ratio-0.80", {"min_ratio": 0.80}),
    ("ratio-0.90", {"min_ratio": 0.90}),
    ("matched-8", {"min_matched": 8}),
    ("matched-14", {"min_matched": 14}),
)
SHAPE_EXCLUDED = ("dropped-token-not-missing", "partial-overlap")
SITE_KEY_NOTE = ("(transcript basename, start, end, tuple(dropped_words)) — identical spans inside "
                 "one transcript are one site; TASK-018 item 0e's dedupe lesson applied at grid "
                 "level")
HOLDOUT_REASON = ("the 33 holdout transcripts are absent from the scratch corpus by construction; "
                  "holdout_reads: [] is the detector's own record and the listing digest is the "
                  "proof, not the assertion")
RATE_RESTRICTION = ("no precision, rate, recall or M6 figure is stated anywhere in this artefact; "
                    "every output is CANDIDATE-class / PROVISIONAL-UNGATED")


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha(path):
    return m5r.sha256_file(path)


def sha_bytes(blob):
    return hashlib.sha256(blob).hexdigest()


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# Fields that describe THIS execution's environment rather than the measurement: a re-runner
# gets different values for them, so they are excluded from `reproducible_content_sha256` and
# named in the manifest. Everything else - counts, config, digests, site keys, the audit's
# holdout evidence - must reproduce byte-for-byte.
ENVIRONMENT_FIELDS = ("run_utc", "run_utc_source", "wall_seconds", "peak_rss_mb")


def content_digest(obj):
    """digest of the reproducible content: the object minus ENVIRONMENT_FIELDS (+ audit totals)."""
    copy = dict(obj)
    for key in ENVIRONMENT_FIELDS:
        copy.pop(key, None)
    copy.pop("reproducible_content_sha256", None)   # never digest the digest
    if "files_opened" in copy:
        copy["files_opened"] = {k: v for k, v in copy["files_opened"].items() if k != "total"}
    blob = json.dumps(copy, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha_bytes(blob.encode("utf-8"))


def dump(path, obj):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    blob = json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=1) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(blob)
    return sha_bytes(blob.encode("utf-8"))


def config_for(name):
    overrides = dict(GRID)[name]
    return dict(FIXED, **dict(SHIPPED, **overrides))


def config_digest(config):
    return sha_bytes(json.dumps(config, sort_keys=True, separators=(",", ":")).encode("utf-8"))


# ------------------------------------------------------------------ scratch corpus

class OpenAudit:
    """Records every path the process opens, so 'unread' is a measurement, not a promise."""

    def __init__(self, holdout):
        self.holdout = frozenset(holdout)
        self.count = 0
        self.holdout_opened = []

    def install(self):
        guard = self

        def hook(event, args):
            if event != "open":
                return
            path = args[0]
            if isinstance(path, (bytes, bytearray)):
                path = path.decode("utf-8", "replace")
            if not isinstance(path, str):
                return
            guard.count += 1
            base = os.path.basename(path)
            if base in guard.holdout:
                guard.holdout_opened.append(path)

        sys.addaudithook(hook)


def build_scratch(scratch, corpus, split):
    """Symlink ONLY the tuning half; refuse any holdout name anywhere in the tree."""
    holdout = set(split["holdout"])
    tuning = sorted(set(split["tuning"]) - holdout)
    if set(split["tuning"]) & holdout:
        raise SystemExit("m4_t21_sensitivity: split integrity — names in both halves: %r"
                         % sorted(set(split["tuning"]) & holdout)[:3])
    overlays = os.path.join(scratch, "docdocgo", "overlays")
    html = os.path.join(scratch, "docdocgo", "html")
    os.makedirs(overlays, exist_ok=True)
    os.makedirs(html, exist_ok=True)
    src = os.path.join(corpus, "docdocgo", "overlays")
    for name in tuning:
        target = os.path.join(src, name)
        if not os.path.exists(target):
            raise SystemExit("m4_t21_sensitivity: %s is in the tuning half but not in the corpus"
                             % name)
        link = os.path.join(overlays, name)
        try:
            os.symlink(os.path.abspath(target), link)
        except FileExistsError:
            if os.path.realpath(link) != os.path.realpath(target):
                raise SystemExit("m4_t21_sensitivity: %s exists in the scratch corpus and points "
                                 "elsewhere (%s)" % (link, os.path.realpath(link)))
    store = os.path.join(html, os.path.basename(STORE_REL))
    try:
        os.symlink(os.path.abspath(os.path.join(corpus, STORE_REL)), store)
    except FileExistsError:
        pass
    present = sorted(n for n in os.listdir(overlays) if n.endswith(".txt"))
    bad = sorted(set(present) & holdout)
    if bad:
        raise SystemExit("m4_t21_sensitivity: refusing to run — holdout transcripts present in "
                         "the scratch corpus: %r" % bad[:3])
    if len(present) != len(tuning):
        raise SystemExit("m4_t21_sensitivity: scratch corpus holds %d transcripts, the v2 tuning "
                         "half has %d" % (len(present), len(tuning)))
    return {
        "tuning_transcripts": len(tuning),
        "holdout_transcripts": len(holdout),
        "holdout_present": [],
        "overlay_listing_sha256": sha_bytes(("\n".join(present) + "\n").encode("utf-8")),
        "overlay_listing_note": ("sha256 over the sorted basenames of the scratch corpus's "
                                 "overlays, one per line with a trailing newline — the artefact "
                                 "that shows the 33 holdout transcripts cannot be walked"),
    }


# ------------------------------------------------------------------ one setting

def apply_params(config):
    dd.MIN_FLANK = config["min_flank"]
    dd.MIN_RATIO = config["min_ratio"]
    dd.MIN_MATCHED = config["min_matched"]
    dd.MAX_DROP = config["max_drop"]
    dd.MIN_SCORE = config["min_score"]
    dd.TOP_K = config["top_k"]
    dd.WINDOW = config["window"]
    dd.STRIDE = config["stride"]


def site_key(name, sig):
    return "%s#%d-%d#%s" % (name, int(sig["start"]), int(sig["end"]),
                            ",".join(sig.get("dropped_words") or []))


def build(args):
    config = config_for(args.setting)
    split = load(args.split)
    guard_doc = build_scratch(args.scratch, args.corpus, split)
    audit = OpenAudit(split["holdout"])
    audit.install()
    texts = os.path.join(args.scratch, "docdocgo", "overlays")
    books = m5r.parse_book_store(os.path.join(args.corpus, STORE_REL))
    apply_params(config)
    t0 = time.time()
    per_file, total = dd.run_tuning(args.scratch, args.split, None, which="tuning", quiet=True)
    wall = time.time() - t0
    raw_texts = {n: open(os.path.join(texts, n), encoding="utf-8", errors="replace").read()
                 for n in sorted(per_file)}
    shapes, sites, inherited = {}, [], 0
    for name in sorted(per_file):
        for sig in per_file[name]:
            if sup.source_inheritance(sig, raw_texts[name], books)["source_inherited"]:
                inherited += 1
            kind = q2ev.adjudicate(sig)["kind"]
            shapes[kind] = shapes.get(kind, 0) + 1
            sites.append(site_key(name, sig))
    distinct = sorted(set(sites))
    excluded = sum(shapes.get(k, 0) for k in SHAPE_EXCLUDED)
    part = {
        "setting": args.setting,
        "config": config,
        "config_sha256": config_digest(config),
        "config_digest_note": ("sha256 over json.dumps(config, sort_keys=True, "
                               "separators=(',',':')) — `config` is the complete in-force "
                               "parameter object published in this part"),
        "shipped_point": dict(SHIPPED),
        "overrides_vs_shipped": dict(GRID)[args.setting],
        "detector": dd.DETECTOR_ID,
        "detector_sha256": sha(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            "det_dropword.py")),
        "detector_note": ("the unmodified C1-drop detector; only the four published constants "
                          "that this map varies are set before the run, and the detector digest "
                          "is recorded so the bytes are checkable"),
        "split_file": args.split.replace(os.sep, "/"),
        "split_sha256": sha(args.split),
        "split_salt": split.get("salt"),
        "split_counts": split.get("counts"),
        "scratch": guard_doc,
        "holdout_reads": [],
        "holdout_enforced": True,
        "holdout_reason": HOLDOUT_REASON,
        "files_opened": {"total": audit.count, "holdout": sorted(set(audit.holdout_opened)),
                         "method": "sys.addaudithook('open') over the whole process"},
        "transcripts_read": len(per_file),
        "wall_seconds": round(wall, 1),
        "peak_rss_mb": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0, 1),
        "raw_signals": total,
        "transcripts_with_signals": sum(1 for v in per_file.values() if v),
        "per_transcript_counts": {n: len(v) for n, v in per_file.items() if v},
        "source_inherited": inherited,
        "after_source_filter": total - inherited,
        "after_source_filter_note": ("the source-inheritance filter is tools/m4_t20_supplement.py's "
                                     "rule: the signal's own span±60 chars verbatim in the book "
                                     "store; the raw count travels beside it"),
        "shape_counts": dict(sorted(shapes.items())),
        "shape_excluded": excluded,
        "shape_excluded_classes": list(SHAPE_EXCLUDED),
        "after_shape_exclusions": total - excluded,
        "site_key": SITE_KEY_NOTE,
        "sites": distinct,
        "distinct_sites": len(distinct),
        "duplicate_sites": len(sites) - len(distinct),
        "run_utc": args.utc,
        "run_utc_source": ("date -u at run time, passed through verbatim by the driver "
                           "(criterion 20.14c: exact to the second and sourced)"),
        "status": ("CANDIDATE-class sensitivity map over the v2 TUNING half only, unreviewed, "
                   "PROVISIONAL-UNGATED; the 122-signal shipped run is over a different (v1) "
                   "tuning half and the two denominators are not interchangeable"),
        "restrictions": RATE_RESTRICTION,
    }
    part["environment_fields"] = list(ENVIRONMENT_FIELDS)
    part["environment_note"] = ("these fields describe this execution's environment and are "
                                "excluded from reproducible_content_sha256: the counts, config, "
                                "digests, site keys and holdout evidence must reproduce "
                                "byte-for-byte on a re-run of this setting")
    part["reproducible_content_sha256"] = content_digest(part)   # computed last, over all else
    out = os.path.join(args.out, "parts", "%s.json" % args.setting)
    digest = dump(out, part)
    print("%-11s raw %3d | source-filtered %3d | after shape %3d | sites %3d (dups %d) | %d "
          "transcripts | %.1f s (rss %.0f MB)"
          % (args.setting, total, part["after_source_filter"], part["after_shape_exclusions"],
             part["distinct_sites"], part["duplicate_sites"], part["transcripts_read"], wall,
             part["peak_rss_mb"]))
    print("part -> %s  sha256 %s" % (out, digest))
    return 0


# ------------------------------------------------------------------ merge + verify

def merge(args):
    parts = {}
    for name, _o in GRID:
        path = os.path.join(args.out, "parts", "%s.json" % name)
        if not os.path.exists(path):
            raise SystemExit("m4_t21_sensitivity: missing part %s — the grid is not complete"
                             % path)
        parts[name] = load(path)
    sites = {n: set(parts[n]["sites"]) for n in parts}
    everywhere = sorted(set.intersection(*sites.values()))
    shipped_only = sorted(sites["shipped"] - set.union(*[sites[n] for n in sites
                                                         if n != "shipped"]))
    split = load(args.split)
    table = {}
    for name in sorted(parts):
        p = parts[name]
        table[name] = {k: p[k] for k in ("config", "config_sha256", "raw_signals",
                                         "transcripts_with_signals", "source_inherited",
                                         "after_source_filter", "shape_counts",
                                         "shape_excluded", "after_shape_exclusions",
                                         "distinct_sites", "duplicate_sites",
                                         "transcripts_read", "wall_seconds")}
    ev = {
        "task": "TASK-021 — C1-drop threshold sensitivity over the v2 tuning half only",
        "worker": "WORKER-2 (A-2026-09-25-001), lane arena/01a0d9ce-fleetyard",
        "run_utc": args.utc,
        "run_utc_source": ("date -u at merge time, passed through verbatim; each part carries its "
                           "own exact run_utc and source"),
        "set": "v2 tuning half only (197 transcripts)",
        "detector": dd.DETECTOR_ID,
        "detector_sha256": sha(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                           "det_dropword.py")),
        "detector_note": parts["shipped"]["detector_note"],
        "shipped_anchor_params": dict(SHIPPED),
        "fixed_params": dict(FIXED),
        "grid": [n for n, _o in GRID],
        "config_recipe": ("one parameter is changed at a time from the shipped point (no full "
                          "cross-product); every setting publishes its complete in-force object "
                          "and the digest recipe"),
        "split": {"file": args.split.replace(os.sep, "/"), "sha256": sha(args.split),
                  "salt": split.get("salt"), "counts": split.get("counts"),
                  "tuning_transcripts": len(split["tuning"]),
                  "holdout_transcripts": len(split["holdout"])},
        "corpus_zip_sha256": CORPUS_ZIP_SHA,
        "book_store_sha256": sha(os.path.join(args.corpus, STORE_REL)),
        "main_head": args.main_head,
        "policy_sha256": args.policy_sha,
        "tool_commit": args.tool_commit,
        "tool_commit_note": ("the lane head at run time; the generating bytes are attributed by "
                             "generator_pins (criterion 21.6's accepted form 2)"),
        "generator_pins": args.generator_pins,
        "holdout_reads": [],
        "holdout_enforced": True,
        "holdout_reason": HOLDOUT_REASON,
        "scratch_overlay_listing_sha256": parts["shipped"]["scratch"]["overlay_listing_sha256"],
        "part_files_sha256": {n: sha(os.path.join(args.out, "parts", "%s.json" % n))
                              for n, _o in GRID},
        "part_reproducible_content_sha256": {n: parts[n]["reproducible_content_sha256"]
                                             for n, _o in GRID},
        "part_generator_pins": args.part_generator_pins,
        "reproducibility": {
            "how": ("re-run one setting with the same --setting and the manifest's own "
                    "parameters; `reproducible_content_sha256` in each part is the digest of "
                    "everything except the environment fields, so equality of that digest is "
                    "byte-identity of the measurement"),
            "environment_fields": list(ENVIRONMENT_FIELDS),
            "why": ("wall time, RSS and the wall-clock stamp differ between runs by nature; "
                    "claims of reproducibility must not rest on them, and no claim of "
                    "reproducibility rests on any field not covered by that digest"),
            "parts_vs_merge": ("the parts were produced by the tool blob pinned in "
                               "part_generator_pins; the merged EVAL/README by the blob pinned "
                               "in generator_pins; both are recorded separately because they are "
                               "not the same bytes"),
        },
        "denominators": {
            "v1_193": ("the shipped 122-signal run covered the v1 tuning half: 193 files, of "
                       "which 33 are now v2-holdout members"),
            "v2_197": ("this map covers the v2 tuning half: 197 files, disjoint from the 33 "
                       "holdout transcripts"),
            "rule": ("the two denominators are NOT interchangeable; 122 is a v1-half count and "
                     "every count here is a v2-half count"),
            "anchor_vs_shipped": ("the anchor row is the shipped SETTINGS over the v2 half: %d "
                                  "raw signals vs 122 raw signals over the v1 half — same "
                                  "parameters, different transcript sets"
                                  % parts["shipped"]["raw_signals"]),
        },
        "table": table,
        "stability": {
            "present_at_every_setting": len(everywhere),
            "present_at_every_setting_sites": everywhere,
            "shipped_point_only": len(shipped_only),
            "shipped_point_only_sites": shipped_only,
            "neither": ("anchor sites that are neither in every setting nor exclusive to the "
                        "anchor: %d"
                        % (parts["shipped"]["distinct_sites"] - len(everywhere)
                           - len(shipped_only))),
            "definition": ("site keys are compared across the %d settings; 'every setting' means "
                           "the key appears in each of them" % len(parts)),
        },
        "shape_legend": {
            "countable": ["consistent"],
            "excluded_from_counts": list(SHAPE_EXCLUDED),
            "excluded_why": ("`dropped-token-not-missing`: the book span repeats the token, so "
                             "nothing is missing (TASK-018 item 0e); `partial-overlap`: "
                             "re-labelled, excluded until a human read"),
            "recorded_not_counted": ["hyphen-tokenization"],
        },
        "restrictions": {
            "no_threshold_chosen": True,
            "no_rate": RATE_RESTRICTION,
            "holdout_unopened": ("the v2 holdout is unread: the scratch corpus cannot serve it "
                                 "and the open audit records 0 holdout files opened"),
            "not_precision_evidence": ("a books-anchored detector's counts over a tuning half are "
                                       "not precision or recall evidence (LAW §9)"),
        },
        "status": ("CANDIDATE-class sensitivity map, PROVISIONAL-UNGATED, unreviewed; no "
                   "threshold chosen or recommended; no rate of any kind"),
    }
    ev_path = os.path.join(args.out, "EVAL.json")
    digest = dump(ev_path, ev)
    readme_path = os.path.join(args.out, "README.md")
    with open(readme_path, "w", encoding="utf-8") as fh:
        fh.write(readme_text(ev, parts))
    print("EVAL.json -> %s  sha256 %s" % (ev_path, digest))
    print("README.md -> %s  sha256 %s" % (readme_path, sha(readme_path)))
    return 0


def readme_text(ev, parts):
    lines = [
        "# TASK-021 — C1-drop threshold sensitivity over the **v2 tuning half only**",
        "",
        "**This is a sensitivity map, not a tuning run.** No threshold is chosen, fitted or",
        "recommended; no precision, rate, recall or M6 figure appears anywhere in this directory.",
        "Every number is CANDIDATE-class / PROVISIONAL-UNGATED.",
        "",
        "## Denominators — read before comparing anything to 122",
        "",
        "| run | transcript set | size | raw signals |",
        "|---|---|---|---|",
        "| shipped C1-drop run | v1 tuning half | 193 files (33 of them are now v2-holdout members) | 122 |",
        "| this map, anchor row | **v2 tuning half** | **197 files, disjoint from the 33 holdout transcripts** | %d |"
        % parts["shipped"]["raw_signals"],
        "",
        "The two sets are **not interchangeable**: 122 is a v1-half count and every count below is",
        "a v2-half count. Same parameters, different transcript sets.",
        "",
        "## The holdout is absent, not merely refused",
        "",
        "* the detector ran over a scratch corpus holding **only the 197 tuning transcripts**",
        "  (symlinks) plus a symlinked book store — listing digest `%s…`;"
        % ev["scratch_overlay_listing_sha256"][:12],
        "* an audit hook recorded every `open` in the process: **%d holdout files opened**;"
        % len(parts["shipped"]["files_opened"]["holdout"]),
        "* every part publishes `holdout_reads: []` and `holdout_enforced: true`.",
        "",
        "## The grid — one parameter at a time from the shipped point",
        "",
        "| setting | change vs shipped | raw | after source filter | after shape exclusions | distinct sites | duplicate sites |",
        "|---|---|---|---|---|---|---|",
    ]
    for name in sorted(parts):
        p = parts[name]
        over = ", ".join("%s=%s" % (k, v) for k, v in sorted(p["overrides_vs_shipped"].items()))
        lines.append("| `%s` | %s | %d | %d | %d | %d | %d |"
                     % (name, over or "— (anchor)", p["raw_signals"], p["after_source_filter"],
                        p["after_shape_exclusions"], p["distinct_sites"], p["duplicate_sites"]))
    st = ev["stability"]
    lines += [
        "",
        "`after source filter` subtracts signals whose own span±60 chars sit verbatim in the book",
        "store (a cross-book self-parallel cannot be a drop by the speaker). `after shape",
        "exclusions` subtracts `dropped-token-not-missing` and `partial-overlap` (TASK-018 items",
        "0e/0f). `hyphen-tokenization` is recorded but is a checker artifact, not a defect, and is",
        "**not** subtracted.",
        "",
        "## Stability — the point of the map",
        "",
        "| quantity | sites |",
        "|---|---|",
        "| present at **every** setting | %d |" % st["present_at_every_setting"],
        "| present **only** at the shipped point | %d |" % st["shipped_point_only"],
        "| neither (own %d, not exclusive) | %d |"
        % (parts["shipped"]["distinct_sites"], parts["shipped"]["distinct_sites"]
           - st["present_at_every_setting"] - st["shipped_point_only"]),
        "| anchor row total | %d |" % parts["shipped"]["distinct_sites"],
        "",
        "The first two numbers bound how much of any future C1-drop figure is threshold-driven;",
        "they are published per site in `EVAL.json`.",
        "",
        "## Reproduce",
        "",
        "```sh",
        "python3 tools/m4_t21_sensitivity.py build --setting <name> --out %s" % OUT,
        "python3 tools/m4_t21_sensitivity.py merge --out %s --utc <exact>" % OUT,
        "python3 tools/m4_t21_sensitivity.py verify --out %s" % OUT,
        "```",
        "",
        "The manifest carries the detector digest, the per-setting config digests with their",
        "recipe, the corpus/book-store/zip digests, the split digest, salt and counts,",
        "`main_head`, `policy_sha256`, `tool_commit`, `generator_pins`, the part-file digests and",
        "`holdout_reads`/`holdout_enforced`.",
        "",
    ]
    return "\n".join(lines)


def verify(args):
    problems = []
    ev_path = os.path.join(args.out, "EVAL.json")
    if not os.path.exists(ev_path):
        print("FAIL: EVAL.json missing")
        return 1
    ev = load(ev_path)
    if ev.get("holdout_reads") != []:
        problems.append("EVAL: holdout_reads is not empty")
    for name, _o in GRID:
        path = os.path.join(args.out, "parts", "%s.json" % name)
        if not os.path.exists(path):
            problems.append("part %s missing" % name)
            continue
        p = load(path)
        if p.get("holdout_reads") != [] or p.get("files_opened", {}).get("holdout"):
            problems.append("%s: holdout was read" % name)
        if p["raw_signals"] != p["after_source_filter"] + p["source_inherited"]:
            problems.append("%s: raw != after-source + inherited" % name)
        if p["raw_signals"] != p["shape_excluded"] + p["after_shape_exclusions"]:
            problems.append("%s: raw != shape-excluded + after-shape" % name)
        if p["distinct_sites"] + p["duplicate_sites"] != p["raw_signals"]:
            problems.append("%s: sites + duplicates != raw" % name)
        if p["config_sha256"] != config_digest(p["config"]):
            problems.append("%s: config digest does not recompute" % name)
        if p["transcripts_read"] != ev["split"]["tuning_transcripts"]:
            problems.append("%s: read %d transcripts, the v2 tuning half has %d"
                            % (name, p["transcripts_read"], ev["split"]["tuning_transcripts"]))
        if p["scratch"]["overlay_listing_sha256"] != ev["scratch_overlay_listing_sha256"]:
            problems.append("%s: scratch listing digest differs from the merged record" % name)
        if ev["part_files_sha256"].get(name) != sha(path):
            problems.append("%s: part digest does not match the merged record" % name)
        if p.get("reproducible_content_sha256") != content_digest(p):
            problems.append("%s: reproducible_content_sha256 does not recompute" % name)
        if ev["part_reproducible_content_sha256"].get(name) != \
                p.get("reproducible_content_sha256"):
            problems.append("%s: reproducible-content digest differs from the merged record"
                            % name)
    sites = {n: set(load(os.path.join(args.out, "parts", "%s.json" % n))["sites"])
             for n, _o in GRID}
    everywhere = set.intersection(*sites.values())
    shipped_only = sites["shipped"] - set.union(*[sites[n] for n in sites if n != "shipped"])
    if len(everywhere) != ev["stability"]["present_at_every_setting"]:
        problems.append("stability 'every setting' does not recompute")
    if len(shipped_only) != ev["stability"]["shipped_point_only"]:
        problems.append("stability 'shipped only' does not recompute")
    if set(ev["stability"]["present_at_every_setting_sites"]) != everywhere:
        problems.append("stability 'every setting' site list does not recompute")
    if set(ev["stability"]["shipped_point_only_sites"]) != shipped_only:
        problems.append("stability 'shipped only' site list does not recompute")
    if problems:
        for p in problems:
            print("FAIL: %s" % p)
        return 1
    print("TASK-021 sensitivity verify: OK (%d settings, %d tuning transcripts, holdout unopened, "
          "arithmetic + stability + part digests recompute)"
          % (len(GRID), ev["split"]["tuning_transcripts"]))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    m = sub.add_parser("merge")
    v = sub.add_parser("verify")
    for p in (b, m, v):
        p.add_argument("--out", default=OUT)
        p.add_argument("--split", default=SPLIT)
    b.add_argument("--setting", required=True, choices=[n for n, _o in GRID])
    b.add_argument("--corpus", default=CORPUS)
    b.add_argument("--scratch", default="/tmp/m4-t21-scratch")
    b.add_argument("--utc", required=True)
    m.add_argument("--corpus", default=CORPUS)
    m.add_argument("--utc", required=True)
    m.add_argument("--tool-commit", default=None)
    m.add_argument("--main-head", default=None)
    m.add_argument("--policy-sha", default=None)
    m.add_argument("--generator-commit", default=None,
                   help="the commit whose blob produced the merged EVAL/README (this tool's "
                        "committed bytes at merge time)")
    m.add_argument("--parts-generator-commit", default=None,
                   help="the commit whose blob produced the PART files (this tool's committed "
                        "bytes when the settings were run)")
    a = ap.parse_args(argv)
    if a.cmd == "build":
        return build(a)
    if a.cmd == "merge":
        pin = __import__("m4_pin_repair")
        a.generator_pins = (None if not a.generator_commit else
                            pin.generator_pins("tools/m4_t21_sensitivity.py", a.generator_commit))
        a.part_generator_pins = (None if not a.parts_generator_commit else
                                 pin.generator_pins("tools/m4_t21_sensitivity.py",
                                                    a.parts_generator_commit))
        return merge(a)
    return verify(a)


if __name__ == "__main__":
    sys.exit(main())
