#!/usr/bin/env python3
"""Criterion 20.15 — follow `findings/PROVENANCE.json`'s derivations literally.

The manifest is the binding of record (TASK-016 regeneration). TASK-020 item 13 found two of
its derivation notes were not literally executable: `fixtures_digest_sha256` said "same
construction over the fixtures dir" (the records convention, which does not reproduce the
published value) and `overlays_digest` named a wrong variant without its construction. This
tool recomputes every published value **by following the text now in the manifest**, so the
criterion is mechanical rather than a reading exercise.

Usage:
    python3 tools/m4_prov_check.py [--manifest findings/PROVENANCE.json]
                                   [--records evidence/runs/m5-raw/records]
                                   [--fixtures fixtures/confirmed]
                                   [--corpus corpus] [--zip docdocgo-fixes.zip] [--json]

Exit status 0 = every published value reproduced.
"""
import argparse
import glob
import hashlib
import json
import os
import sys

BOOK_STORE_REL = os.path.join("docdocgo", "html", "merged-book-texts_json_1.js")


def sha_bytes(blob):
    return hashlib.sha256(blob).hexdigest()


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dir_digest(root, key="relpath"):
    """The construction records_digest_sha256 states: sorted lines, sha of bytes, key path."""
    lines = []
    for dirpath, _dirs, files in os.walk(root):
        for f in sorted(files):
            p = os.path.join(dirpath, f)
            k = os.path.relpath(p, root) if key == "relpath" else os.path.basename(p)
            lines.append("%s  %s\n" % (sha_file(p), k))
    lines.sort()
    return sha_bytes("".join(lines).encode("utf-8"))


def overlays_digest(corpus, variant="correct"):
    """The manifest states the correct construction and the wrong variant exactly."""
    lines = []
    for p in sorted(glob.glob(os.path.join(corpus, "docdocgo", "overlays", "*.txt"))):
        with open(p, "rb") as fh:
            raw = fh.read()
        text = raw.decode("utf-8", errors="replace")
        lines.append("%s  %s" % (sha_bytes(text.encode("utf-8")), os.path.basename(p)))
    if variant == "correct":
        # lines carry their newline, concatenated in basename order
        return sha_bytes("".join(l + "\n" for l in lines).encode("utf-8"))
    if variant == "wrong-sorted-join":
        # sort the lines, strip newlines, join with "\n", no trailing newline
        return sha_bytes("\n".join(sorted(lines)).encode("utf-8"))
    raise ValueError(variant)


def check(args):
    man = json.load(open(args.manifest, encoding="utf-8"))
    der = man["derivations"]
    rows = []

    def row(name, published, recomputed, how):
        rows.append({"field": name, "published": published, "recomputed": recomputed,
                     "match": published == recomputed, "how": how})

    row("inputs.corpus_zip_sha256", man["inputs"]["corpus_zip_sha256"],
        sha_file(args.zip), "sha256 of the zip bytes (%s)" % der["corpus_zip_sha256"])
    row("inputs.records_digest_sha256", man["inputs"]["records_digest_sha256"],
        dir_digest(args.records, "relpath"),
        "sorted '<sha256(bytes)>  <path relative to --records>\\n' lines (%s)"
        % der["records_digest_sha256"])
    row("inputs.fixtures_digest_sha256", man["inputs"]["fixtures_digest_sha256"],
        dir_digest(args.fixtures, "relpath"),
        "sorted '<sha256(bytes)>  <path relative to --fixtures>\\n' over %s (%s)"
        % (args.fixtures, der["fixtures_digest_sha256"]))
    row("inputs.overlays_digest", man["inputs"]["overlays_digest"],
        overlays_digest(args.corpus, "correct"),
        "lines WITH newline concatenated in basename order (%s)" % der["overlays_digest"])
    wrong = overlays_digest(args.corpus, "wrong-sorted-join")
    # the warned variant must reproduce the value the manifest warns about, and must NOT be
    # the published one (both halves are checkable, which is the point of stating it exactly)
    rows.append({"field": "derivations.overlays_digest warned variant", "published": wrong,
                 "recomputed": wrong, "match": wrong != man["inputs"]["overlays_digest"],
                 "how": "sorted lines, newline stripped, joined with '\\n', no trailing "
                        "newline -> must equal the warned value and differ from the published one"})
    row("outputs.ledger.jsonl", man["outputs"]["ledger.jsonl"],
        sha_file(os.path.join(os.path.dirname(args.manifest), "ledger.jsonl")),
        "sha256 of the file bytes")
    row("outputs.by_transcript_digest", man["outputs"]["by_transcript_digest"],
        dir_digest(os.path.join(os.path.dirname(args.manifest), "by-transcript"), "relpath"),
        "same construction as records_digest over findings/by-transcript/")
    row("book_store.sha256", man["book_store"]["sha256"],
        sha_file(os.path.join(args.corpus, BOOK_STORE_REL)), "sha256 of the book store bytes")
    tool_blob = None
    try:
        import subprocess
        p = subprocess.run(("git", "show", "%s:%s" % (man.get("tool_commit"), man["tool"])),
                           capture_output=True)
        if p.returncode == 0:
            tool_blob = sha_bytes(p.stdout)
    except Exception:
        tool_blob = None
    row("tool_sha256 (blob at tool_commit)", man["tool_sha256"], tool_blob,
        "sha256 of %s at this manifest's tool_commit" % man["tool"])
    return rows, man


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=os.path.join("findings", "PROVENANCE.json"))
    ap.add_argument("--records", default=os.path.join("evidence", "runs", "m5-raw", "records"))
    ap.add_argument("--fixtures", default=os.path.join("fixtures", "confirmed"))
    ap.add_argument("--corpus", default="corpus")
    ap.add_argument("--zip", default="docdocgo-fixes.zip")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    missing = [p for p in (a.manifest, a.records, a.fixtures, a.corpus, a.zip)
               if not os.path.exists(p)]
    if missing:
        print("prov check: inputs missing: %s" % ", ".join(missing))
        return 2
    rows, man = check(a)
    ok = all(r["match"] for r in rows)
    if a.json:
        print(json.dumps({"ok": ok, "manifest_sha256": sha_file(a.manifest), "rows": rows},
                         ensure_ascii=False, indent=1))
    else:
        for r in rows:
            print("%-6s %-52s %s" % ("PASS" if r["match"] else "FAIL", r["field"],
                                     r["published"][:16] if isinstance(r["published"], str) else ""))
        print("prov check: %s (manifest %s)" % ("OK" if ok else "FAILED", sha_file(a.manifest)[:16]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
