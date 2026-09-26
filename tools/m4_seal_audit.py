#!/usr/bin/env python3
"""Seal audit — did anything change after the holdout split was sealed?

The v2 seal carries its own rule, verbatim:

  "if any fixture is confirmed after this seal, the split is VOID and must be
   re-sealed with a new salt + a dated record; never silently reused, never
   patched"

That rule is only as good as the check, so this tool re-derives the answer from
git bytes instead of trusting prose. For a seal file it reports, mechanically:

  * **fixture digests** — the sha256 the seal recorded for each fixture source,
    against the content actually committed at HEAD, plus the commit that last
    touched the file;
  * **append-only vs patched** — the seal-time blob (`git show <seal-commit>:<file>`)
    is compared key-by-key with the live file. New keys/ids are *append-only*
    (allowed; owed an appendix naming both digests). A changed value for a key
    that already existed at seal time is a **mutation** — the rule's "never patched" is violated;
  * **new confirmations** — any fixture id that did not exist at seal time, and
    any adjudication artefact newly cited after the seal, with that artefact's own
    commit time, so a confirmation can be placed before or after the seal;
  * **membership** — fixture transcripts must not be holdout members, and the
    forced-to-tuning list must not intersect the holdout.

Verdict: `seal_void: true` when the seal was patched, a fixture was added or a
confirmation artefact postdates the seal, or a fixture transcript sits in the
holdout; `true` with `void_reasons` naming bytes otherwise. A stale-but-append-only
fixture digest leaves the seal standing and asks for an appendix (`outstanding`).

Usage:
  python3 tools/m4_seal_audit.py --seal tools/HELD-OUT-SPLIT-V2.json [--out FILE] [--repo .]

Stdlib only, read-only (writes only the optional --out report).
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import sys


def git(repo, *args):
    p = subprocess.run(("git", "-C", repo) + args, capture_output=True, text=True)
    if p.returncode != 0:
        return None
    return p.stdout


def sha256_bytes(blob):
    return hashlib.sha256(blob).hexdigest()


NOTE_GLOBS = ("tools/HELD-OUT-SPLIT-V2-NOTE-*.md", "tools/*SEAL-NOTE*.md")


def find_note(repo, sealed_sha, live_sha):
    """A dated note that names both digests: the thing a verifying reader needs to find."""
    import glob
    for pattern in NOTE_GLOBS:
        for path in sorted(glob.glob(os.path.join(repo, pattern))):
            try:
                text = open(path, encoding="utf-8").read()
            except OSError:
                continue
            if sealed_sha[:16] in text and live_sha[:16] in text:
                return os.path.relpath(path, repo).replace(os.sep, "/")
    return None


def blob_at(repo, ref, path):
    p = subprocess.run(("git", "-C", repo, "show", "%s:%s" % (ref, path)),
                       capture_output=True)
    return p.stdout if p.returncode == 0 else None


def head_blob(repo, path):
    return blob_at(repo, "HEAD", path)


def last_commit(repo, path):
    out = git(repo, "log", "-1", "--format=%H%n%cI", "--", path)
    if not out:
        return None, None
    head, when = out.strip().split("\n")[:2]
    return head, when


def diff_paths(old, new, prefix=""):
    """Paths where a value that existed at seal time has changed (mutation)."""
    out = []
    if isinstance(old, dict) and isinstance(new, dict):
        for k in old:
            if k not in new:
                out.append("%s/%s: REMOVED" % (prefix, k))
            else:
                out.extend(diff_paths(old[k], new[k], "%s/%s" % (prefix, k)))
    elif isinstance(old, list) and isinstance(new, list):
        if len(old) <= len(new):
            for i, v in enumerate(old):
                out.extend(diff_paths(v, new[i], "%s[%d]" % (prefix, i)))
        else:
            out.append("%s: list shortened (%d -> %d)" % (prefix, len(old), len(new)))
    else:
        if old != new:
            out.append("%s: %r -> %r" % (prefix, old, new))
    return out


def collect_ids(doc, key):
    """Fixture ids: {id: index} for a list-valued key, else {str: index} for dicts."""
    if isinstance(doc, dict):
        v = doc.get(key)
        if isinstance(v, list):
            return {str(f.get("id", i)): i for i, f in enumerate(v)
                    if isinstance(f, dict)}
        if isinstance(v, dict):
            return {str(k): i for i, k in enumerate(sorted(v))}
    return {}


def cited_artifacts(node, found=None):
    """Every {'artifact': path, 'artifact_sha256': sha} pair anywhere in the doc."""
    if found is None:
        found = []
    if isinstance(node, dict):
        if isinstance(node.get("artifact"), str) and isinstance(
                node.get("artifact_sha256"), str):
            found.append((node["artifact"], node["artifact_sha256"]))
        for v in node.values():
            cited_artifacts(v, found)
    elif isinstance(node, list):
        for v in node:
            cited_artifacts(v, found)
    return found


def audit(repo, seal_path, utc=None):
    seal_blob = open(os.path.join(repo, seal_path), "rb").read()
    seal = json.loads(seal_blob)
    seal_commit, seal_utc = last_commit(repo, seal_path)
    report = {
        "tool": "tools/m4_seal_audit.py",
        "tool_sha256": sha256_bytes(open(os.path.abspath(__file__), "rb").read()),
        "head_commit_at_audit": (git(repo, "rev-parse", "HEAD") or "").strip() or None,
        "head_commit_note": ("the lane head the audit ran against; this report is "
                             "committed as its own commit after it"),
        "audit_utc": utc or datetime.datetime.now(datetime.timezone.utc)
                                  .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "seal_file": seal_path.replace(os.sep, "/"),
        "seal_sha256": sha256_bytes(seal_blob),
        "seal_salt": seal.get("salt"),
        "seal_commit": seal_commit,
        "seal_commit_utc": seal_utc,
        "split": {"holdout": len(seal.get("holdout", [])),
                  "tuning": len(seal.get("tuning", [])),
                  "forced_to_tuning": len(seal.get("fixture_transcripts_forced_tuning", []))},
        "fixture_sources": [],
        "confirmation_artifacts": [],
        "membership": {},
        "void_reasons": [],
        "outstanding": [],
        "notes_on_file": [],
        "verdict": {},
    }
    hold = set(seal.get("holdout", []))
    forced = set(seal.get("fixture_transcripts_forced_tuning", []))

    for path, sealed_sha in sorted(seal.get("fixture_sources", {}).items()):
        live = head_blob(repo, path)
        entry = {"file": path, "sealed_sha256": sealed_sha,
                 "live_sha256": sha256_bytes(live) if live is not None else None,
                 "last_commit": None, "last_commit_utc": None, "status": None,
                 "sealed_shape": {}, "new_fixture_ids": [], "mutations": [],
                 "appendix_needed": False}
        if live is None:
            entry["status"] = "ABSENT-AT-HEAD"
            report["void_reasons"].append("%s: committed at seal, absent at HEAD" % path)
            report["fixture_sources"].append(entry)
            continue
        entry["last_commit"], entry["last_commit_utc"] = last_commit(repo, path)
        seal_time_blob = blob_at(repo, seal_commit, path) if seal_commit else None
        live_doc = json.loads(live)
        if seal_time_blob is None:
            entry["status"] = "NO-SEAL-TIME-BLOB"
            report["outstanding"].append(
                "%s: no seal-time blob available (seal commit %s); digest comparison "
                "only" % (path, str(seal_commit)[:7]))
        else:
            if sha256_bytes(seal_time_blob) != sealed_sha:
                report["void_reasons"].append(
                    "%s: the seal-time blob's own digest (%s…) differs from the digest "
                    "the seal recorded (%s…) — the seal is internally inconsistent"
                    % (path, sha256_bytes(seal_time_blob)[:12], sealed_sha[:12]))
            if entry["live_sha256"] == sealed_sha:
                entry["status"] = "OK"
            else:
                old = json.loads(seal_time_blob)
                entry["mutations"] = diff_paths(old, live_doc)
                old_ids = collect_ids(old, "fixtures")
                new_ids = collect_ids(live_doc, "fixtures")
                entry["new_fixture_ids"] = sorted(set(new_ids) - set(old_ids))
                entry["sealed_shape"] = {"fixtures_at_seal": len(old_ids),
                                         "fixtures_at_head": len(new_ids)}
                if entry["mutations"]:
                    entry["status"] = "PATCHED-AFTER-SEAL"
                    report["void_reasons"].append(
                        "%s: sealed content was patched after the seal (%d changed "
                        "path(s), first: %s)" % (path, len(entry["mutations"]),
                                                 entry["mutations"][0]))
                elif entry["new_fixture_ids"]:
                    entry["status"] = "NEW-FIXTURE-AFTER-SEAL"
                    report["void_reasons"].append(
                        "%s: %d fixture id(s) added after the seal (%s) — a confirmation "
                        "after the seal voids it"
                        % (path, len(entry["new_fixture_ids"]),
                           ", ".join(entry["new_fixture_ids"][:4])))
                else:
                    note = find_note(repo, sealed_sha, entry["live_sha256"])
                    entry["note_file"] = note
                    if note:
                        entry["status"] = "APPEND-ONLY-AFTER-SEAL (dated note on file)"
                        report["notes_on_file"].append(
                            "%s: digest moved %s… -> %s… by an append-only edit; the dated "
                            "note %s names both digests — the seal STANDS, nothing further "
                            "is owed" % (path, sealed_sha[:12], entry["live_sha256"][:12], note))
                    else:
                        entry["status"] = "APPEND-ONLY-AFTER-SEAL"
                        entry["appendix_needed"] = True
                        report["outstanding"].append(
                            "%s: digest moved after the seal %s… -> %s… by an append-only "
                            "edit (commit %s, %s); content at seal time is unmodified and no "
                            "fixture was added — the seal STANDS, an appendix must name both "
                            "digests" % (path, sealed_sha[:12], entry["live_sha256"][:12],
                                         str(entry["last_commit"])[:7],
                                         entry["last_commit_utc"]))
        for path2, sha2 in cited_artifacts(live_doc):
            blob = head_blob(repo, path2)
            artefact_commit, artefact_utc = last_commit(repo, path2)
            ok = blob is not None and sha256_bytes(blob) == sha2
            relation = None
            if artefact_utc and seal_utc:
                relation = "pre-seal" if artefact_utc < seal_utc else "post-seal"
            report["confirmation_artifacts"].append({
                "cited_by": path, "artifact": path2, "artifact_sha256": sha2,
                "digest_matches_head": ok, "commit": artefact_commit,
                "commit_utc": artefact_utc, "relation_to_seal": relation})
            if not ok:
                report["outstanding"].append(
                    "%s: cites %s at %s… but HEAD's blob does not match the cited digest"
                    % (path, path2, sha2[:12]))
            if relation == "post-seal":
                report["void_reasons"].append(
                    "%s: cites %s whose last commit (%s, %s) postdates the seal — a "
                    "confirmation artefact created after the seal"
                    % (path, path2, str(artefact_commit)[:7], artefact_utc))
        report["fixture_sources"].append(entry)

    report["membership"] = {
        "forced_intersect_holdout": sorted(forced & hold),
        "holdout_size": len(hold),
    }
    if forced & hold:
        report["void_reasons"].append(
            "forced-to-tuning names appear in the holdout (%d)" % len(forced & hold))

    report["seal_void"] = bool(report["void_reasons"])
    report["verdict"] = {
        "seal_void": bool(report["void_reasons"]),
        "reasons": report["void_reasons"],
        "outstanding": report["outstanding"],
        "one_line": ("VOID — " + report["void_reasons"][0] if report["void_reasons"]
                     else ("STANDING" + (" (appendix owed)" if report["outstanding"]
                                         else (" (dated note on file)" if report["notes_on_file"]
                                               else " (nothing stale)")))),
    }
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seal", required=True)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--out", default=None)
    ap.add_argument("--utc", default=None)
    a = ap.parse_args(argv)
    report = audit(a.repo, a.seal, a.utc)
    text = json.dumps(report, indent=1, sort_keys=True) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("seal audit -> %s" % a.out)
    print("verdict: %s" % report["verdict"]["one_line"])
    for line in report["outstanding"]:
        print("  outstanding: %s" % line)
    return 1 if report["seal_void"] else 0


if __name__ == "__main__":
    sys.exit(main())
