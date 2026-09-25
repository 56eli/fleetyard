#!/usr/bin/env python3
"""M0 corpus census: inventory of corpus/docdocgo/overlays/ -> tools/CORPUS.md.

Stdlib only, no network. Reads only corpus/**; writes only the output path
given (default tools/CORPUS.md). Deterministic: same corpus -> same bytes.

Usage:
    python3 tools/census.py [--corpus corpus/docdocgo] [--out tools/CORPUS.md]
    python3 tools/census.py --check   # exit 1 if the committed table is stale
"""
import argparse
import hashlib
import json
import os
import re
import sys

OVERLAYS = "overlays"
BOOK_STORE = os.path.join("html", "merged-book-texts_json_1.js")
EXTRA_SOURCES = "extra-sources"

# Scope markers, verbatim from VISION "The ground truth (owner-stated)".
SCOPE_OVERLAYS = "IN SCOPE — suspect corpus (error-bearing AI transcriptions)"
SCOPE_BOOK = "IN SCOPE — ground truth (book texts, 100% reliable per owner)"
SCOPE_EXTRA = ("UNDECIDED — side not ruled by the owner; treat as suspect "
               "until ruled (VISION open item)")

# Bootstrap battery expectations (BOOTSTRAP-LETTER Step 4, item 2).
BATTERY = {
    "overlay_entries": 231,          # file count under overlays/
    "overlay_total_mb_approx": 14.3,  # "≈14.3"
    "book_store_bytes": 14634979,
}

MONTHS = {m: i for i, m in enumerate(
    "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}
SUFFIX = "_enxautogen_html"
_DATED = re.compile(r"^(?P<title>.+?)_(?P<mon>[A-Z][a-z]{2})_(?P<year>\d{4})"
                    r"(?:_Part_(?P<part>\d+))?$")
_UNDATED = re.compile(r"^(?P<title>.+?)(?:_Part_(?P<part>\d+))?$")


def parse_name(filename):
    """Parse an overlay filename into its title components.

    Returns dict: stem, title, month, year, part, suffix (bool: has
    _enxautogen_html). Missing parts are None - never guessed.
    """
    stem = filename[:-4] if filename.endswith(".txt") else filename
    has_suffix = stem.endswith(SUFFIX)
    base = stem[: -len(SUFFIX)] if has_suffix else stem
    m = _DATED.match(base)
    if m and m.group("mon") in MONTHS:
        title, mon, year = m.group("title"), m.group("mon"), int(m.group("year"))
    else:
        m = _UNDATED.match(base)
        title, mon, year = m.group("title"), None, None
    part = int(m.group("part")) if m.group("part") else None
    return {"stem": stem, "title": title.replace("_", " "), "month": mon,
            "year": year, "part": part, "suffix": has_suffix}


def inspect_bytes(data):
    """Encoding/format facts for one file's raw bytes."""
    facts = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    try:
        text = data.decode("utf-8")
        facts["utf8"] = True
    except UnicodeDecodeError:
        text = data.decode("utf-8", errors="replace")
        facts["utf8"] = False
    facts["bom"] = data.startswith(b"\xef\xbb\xbf")
    facts["crlf"] = b"\r" in data
    facts["newlines"] = data.count(b"\n")
    facts["non_ascii"] = sum(1 for ch in text if ord(ch) > 127)
    facts["replacement_chars"] = text.count("\ufffd")
    facts["control_chars"] = sum(
        1 for ch in text if ord(ch) < 32 and ch not in "\n\r\t")
    facts["chars"] = len(text)
    facts["words"] = len(text.split())
    return facts


def census(corpus_root):
    """Collect the census. Returns a dict (pure data; no writing)."""
    odir = os.path.join(corpus_root, OVERLAYS)
    entries = sorted(os.listdir(odir))
    rows, others = [], []
    for name in entries:
        path = os.path.join(odir, name)
        if not name.endswith(".txt"):
            others.append({"name": name, "bytes": os.path.getsize(path)})
            continue
        with open(path, "rb") as fh:
            data = fh.read()
        row = parse_name(name)
        row.update(inspect_bytes(data))
        row["name"] = name
        rows.append(row)

    manifest = None
    mpath = os.path.join(odir, "manifest.json")
    if os.path.exists(mpath):
        with open(mpath, encoding="utf-8") as fh:
            manifest = json.load(fh)

    book = os.path.join(corpus_root, BOOK_STORE)
    book_bytes = os.path.getsize(book) if os.path.exists(book) else None
    book_sha = _sha_file(book) if book_bytes is not None else None

    extras = []
    edir = os.path.join(corpus_root, EXTRA_SOURCES)
    if os.path.isdir(edir):
        for name in sorted(os.listdir(edir)):
            path = os.path.join(edir, name)
            if os.path.isfile(path):
                extras.append({"name": name, "bytes": os.path.getsize(path),
                               "sha256": _sha_file(path)})
    return {"rows": rows, "others": others, "manifest": manifest,
            "entries": len(entries), "book_bytes": book_bytes,
            "book_sha256": book_sha, "extras": extras}


def _sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def anomalies(data):
    """Derive anomaly lists from a census dict."""
    rows = data["rows"]
    out = {}
    out["empty"] = [r["name"] for r in rows if r["bytes"] == 0]
    by_sha = {}
    for r in rows:
        by_sha.setdefault(r["sha256"], []).append(r["name"])
    out["dup_content"] = sorted(v for v in by_sha.values() if len(v) > 1)
    by_key = {}
    for r in rows:
        by_key.setdefault((r["title"], r["month"], r["year"], r["part"]),
                          []).append(r["name"])
    out["dup_key"] = sorted(v for v in by_key.values() if len(v) > 1)
    out["not_utf8"] = [r["name"] for r in rows if not r["utf8"]]
    out["bom"] = [r["name"] for r in rows if r["bom"]]
    out["crlf"] = [r["name"] for r in rows if r["crlf"]]
    out["replacement"] = [(r["name"], r["replacement_chars"]) for r in rows
                          if r["replacement_chars"]]
    out["control"] = [(r["name"], r["control_chars"]) for r in rows
                      if r["control_chars"]]
    out["no_suffix"] = [r["name"] for r in rows if not r["suffix"]]
    out["undated"] = [r["name"] for r in rows if r["year"] is None]
    out["multiline"] = [(r["name"], r["newlines"]) for r in rows
                        if r["newlines"] > 1]
    # Missing parts within a (title, month, year) series.
    series = {}
    for r in rows:
        series.setdefault((r["title"], r["month"], r["year"]), []).append(r["part"])
    gaps = []
    for key, parts in sorted(series.items(), key=lambda kv: str(kv[0])):
        nums = sorted(p for p in parts if p is not None)
        if nums and nums != list(range(1, nums[-1] + 1)):
            gaps.append((key[0], key[1], key[2], nums))
    out["part_gaps"] = gaps
    # Manifest cross-check.
    man = data["manifest"]
    out["manifest"] = None
    if man is not None:
        mkeys = {e["key"]: e for e in man}
        stems = {r["stem"]: r for r in rows}
        drift = []
        exact = 0
        for stem in sorted(set(mkeys) & set(stems)):
            e, r = mkeys[stem], stems[stem]
            if e.get("chars") == r["chars"] and e.get("words") == r["words"]:
                exact += 1
            else:
                drift.append((stem, e.get("chars"), r["chars"],
                              e.get("words"), r["words"]))
        out["manifest"] = {
            "entries": len(man),
            "missing_files": sorted(set(mkeys) - set(stems)),
            "unlisted_files": sorted(set(stems) - set(mkeys)),
            "exact": exact, "drift": drift,
        }
    return out


def _fmt_mb(n):
    return "%.2f" % (n / 1e6)


def render(data):
    """Render the census as markdown (deterministic)."""
    rows, an = data["rows"], anomalies(data)
    total = sum(r["bytes"] for r in rows)
    L = []
    L.append("# CORPUS — census of `corpus/docdocgo/` (TASK M0 / TASK-001 + TASK-003)")
    L.append("")
    L.append("Paths in scope tables are relative to `corpus/docdocgo/`.")
    L.append("")
    L.append("Generated by `python3 tools/census.py` (stdlib, read-only over "
             "`corpus/**`). Regenerate, never hand-edit. `corpus/` itself is "
             "untracked (ERRATA-2026-09-24 §2); reproduce it from "
             "`docdocgo-fixes.zip` (sha256 prefix `3f36c5203910`).")
    L.append("")
    L.append("## Totals vs bootstrap battery")
    L.append("")
    L.append("| check | battery expects | measured | verdict |")
    L.append("|---|---|---|---|")
    ok = data["entries"] == BATTERY["overlay_entries"]
    L.append("| entries under `overlays/` | %d | %d (%d `.txt` + %s) | %s |" % (
        BATTERY["overlay_entries"], data["entries"], len(rows),
        ", ".join("`%s`" % o["name"] for o in data["others"]) or "none",
        "MATCH" if ok else "MISMATCH"))
    mb_all = total + sum(o["bytes"] for o in data["others"])
    ok = round(total / 1e6, 1) == BATTERY["overlay_total_mb_approx"] or \
        round(mb_all / 1e6, 1) == BATTERY["overlay_total_mb_approx"]
    L.append("| overlays total MB | ≈%.1f | %s MB `.txt` only (%d B); %s MB "
             "all entries (%d B) | %s |" % (
                 BATTERY["overlay_total_mb_approx"], _fmt_mb(total), total,
                 _fmt_mb(mb_all), mb_all, "MATCH (≈)" if ok else "MISMATCH"))
    bb = data["book_bytes"]
    L.append("| book store bytes | %s | %s | %s |" % (
        format(BATTERY["book_store_bytes"], ","),
        format(bb, ",") if bb is not None else "absent",
        "MATCH" if bb == BATTERY["book_store_bytes"] else "MISMATCH"))
    L.append("")
    L.append("Note: the battery's \"231\" counts directory entries; the "
             "transcript count is **%d** (`manifest.json` is not a "
             "transcript). AUDIT-PLAN M5's \"all 231 transcripts\" should "
             "read %d — disclosed here, not silently corrected." %
             (len(rows), len(rows)))
    L.append("")
    L.append("## Scope boundary (per VISION)")
    L.append("")
    L.append("| area | files | bytes | scope |")
    L.append("|---|---|---|---|")
    L.append("| `overlays/*.txt` | %d | %d | %s |" % (len(rows), total,
                                                   SCOPE_OVERLAYS))
    L.append("| `%s` | %d | %s | %s |" % (
        BOOK_STORE, 1 if bb is not None else 0,
        bb if bb is not None else "absent", SCOPE_BOOK))
    ex = data.get("extras", [])
    L.append("| `%s/*` | %d | %d | %s |" % (
        EXTRA_SOURCES, len(ex), sum(e["bytes"] for e in ex), SCOPE_EXTRA))
    L.append("| everything else in `corpus/docdocgo/` | — | — | OUT OF SCOPE "
             "— context only (app code, configs, old reports) |")
    L.append("")
    L.append("### Book store (listed separately)")
    L.append("")
    L.append("| path | bytes | sha256 | scope |")
    L.append("|---|---|---|---|")
    L.append("| `%s` | %s | `%s` | %s |" % (
        BOOK_STORE, bb if bb is not None else "absent",
        data.get("book_sha256") or "—", SCOPE_BOOK))
    L.append("")
    L.append("### Extra sources (`%s/`)" % EXTRA_SOURCES)
    L.append("")
    L.append("| path | bytes | sha256 | scope |")
    L.append("|---|---|---|---|")
    for e in ex:
        L.append("| `%s/%s` | %d | `%s` | UNDECIDED |" % (
            EXTRA_SOURCES, e["name"], e["bytes"], e["sha256"]))
    L.append("| **total** | **%d** | | |" % sum(e["bytes"] for e in ex))
    L.append("")
    years = {}
    for r in rows:
        years.setdefault(r["year"], [0, 0])
        years[r["year"]][0] += 1
        years[r["year"]][1] += r["bytes"]
    L.append("## By year (from filename; `undated` = no date in filename)")
    L.append("")
    L.append("| year | files | bytes |")
    L.append("|---|---|---|")
    for y in sorted(years, key=lambda y: (y is None, y or 0)):
        L.append("| %s | %d | %d |" % (y if y is not None else "undated",
                                        years[y][0], years[y][1]))
    L.append("| **total** | **%d** | **%d** |" % (len(rows), total))
    L.append("")
    L.append("## Anomalies")
    L.append("")

    def lst(label, items, fmt=lambda x: "`%s`" % x):
        L.append("- **%s:** %d" % (label, len(items)))
        for it in items:
            L.append("  - " + fmt(it))

    lst("empty files", an["empty"])
    lst("byte-identical duplicates", an["dup_content"],
        lambda g: ", ".join("`%s`" % n for n in g))
    lst("duplicate title/date/part keys", an["dup_key"],
        lambda g: ", ".join("`%s`" % n for n in g))
    lst("not valid UTF-8", an["not_utf8"])
    lst("UTF-8 BOM", an["bom"])
    lst("CR / CRLF line endings", an["crlf"])
    lst("U+FFFD replacement chars", an["replacement"],
        lambda t: "`%s`: %d" % t)
    lst("control chars (excl. tab/newline)", an["control"],
        lambda t: "`%s`: %d" % t)
    lst("multi-line files (>1 newline; most transcripts are one line)",
        an["multiline"], lambda t: "`%s`: %d newlines" % t)
    lst("naming variant: no `_enxautogen_html` suffix", an["no_suffix"])
    lst("undated filenames (year unknown from name; not guessed)",
        an["undated"])
    lst("part-number gaps within a title/date series", an["part_gaps"],
        lambda g: "%s %s %s: parts %s" % (g[0], g[1] or "", g[2] or "",
                                          g[3]))
    na = sum(r["non_ascii"] for r in rows)
    L.append("- **non-ASCII characters (informational):** %d total across "
             "%d files" % (na, sum(1 for r in rows if r["non_ascii"])))
    m = an["manifest"]
    L.append("")
    L.append("### `overlays/manifest.json` cross-check")
    L.append("")
    if m is None:
        L.append("manifest absent.")
    else:
        L.append("- entries: %d; listed-but-missing files: %d; unlisted "
                 "files: %d" % (m["entries"], len(m["missing_files"]),
                                len(m["unlisted_files"])))
        for n in m["missing_files"]:
            L.append("  - missing: `%s`" % n)
        for n in m["unlisted_files"]:
            L.append("  - unlisted: `%s`" % n)
        drift = m["drift"]
        small = [d for d in drift if abs(d[1] - d[2]) <= 1 and d[3] == d[4]]
        big = [d for d in drift if d not in small]
        L.append("- chars+words exactly equal to measured (Python `len(str)`, "
                 "`str.split()`): %d / %d" % (m["exact"], m["entries"]))
        L.append("- off by ≤1 char, words equal (counting convention, e.g. "
                 "trailing newline): %d" % len(small))
        L.append("- larger drift (manifest counts stale vs file content — "
                 "files changed after the manifest was built): %d" % len(big))
        if big:
            L.append("")
            L.append("| file stem | manifest chars | measured chars | "
                     "manifest words | measured words |")
            L.append("|---|---|---|---|---|")
            for d in big:
                L.append("| `%s` | %s | %d | %s | %d |" % d)
    L.append("")
    L.append("## Per-file table")
    L.append("")
    L.append("Path relative to `corpus/docdocgo/overlays/`. sha256 = first "
             "12 hex.")
    L.append("")
    L.append("| # | path | bytes | year | month | part | title (parsed) | "
             "words | sha256 |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        L.append("| %d | `%s` | %d | %s | %s | %s | %s | %d | `%s` |" % (
            i, r["name"], r["bytes"],
            r["year"] if r["year"] is not None else "—",
            r["month"] or "—", r["part"] if r["part"] is not None else "—",
            r["title"], r["words"], r["sha256"][:12]))
    for o in data["others"]:
        L.append("| — | `%s` | %d | — | — | — | (not a transcript) | — | — |"
                 % (o["name"], o["bytes"]))
    L.append("")
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--corpus", default=os.path.join("corpus", "docdocgo"))
    ap.add_argument("--out", default=os.path.join("tools", "CORPUS.md"))
    ap.add_argument("--check", action="store_true",
                    help="compare against --out instead of writing")
    a = ap.parse_args(argv)
    text = render(census(a.corpus))
    if a.check:
        with open(a.out, encoding="utf-8") as fh:
            same = fh.read() == text
        print("census %s" % ("up to date" if same else "STALE"))
        return 0 if same else 1
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("wrote %s (%d transcripts)" % (a.out, len(census(a.corpus)["rows"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
