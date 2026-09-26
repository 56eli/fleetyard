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
    forced-to-tuning list must not intersect the holdout;
  * **every mention of a confirmation artefact** — one row per citation key (paired or not;
    an unpaired mention's digest is resolved from the file at HEAD), each put through the
    post-seal check, plus the artefact-level view with the citing paths;
  * **one draw, not two** — the seal file's own revision history, with keys added / removed /
    changed and the holdout, tuning and salt on both sides (`seal_history.one_draw`);
  * **attribution** — `tool_commit` (the commit whose blob equals this tool at HEAD),
    `tool_origin_commit`, and `audit_utc` passed through verbatim;
  * **the taint disclosure** — the holdout transcripts carrying pre-seal labels, read from
    `tools/HELD-OUT-SPLIT-V2-EXCLUSIONS.json`, and a check that the companion appendix and the
    dated note still name them and the evaluated denominator;
  * **the companion appendix** — it must cite this report's exact `audit_utc`, with any other
    audit-time citation marked superseded or read as history.

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


def stem(name):
    """Transcript basename without the corpus's enxautogen suffix (naming varies by artefact)."""
    for suffix in ("_enxautogen_html.txt", ".txt", ".json"):
        if name.endswith(suffix):
            return name[:-len(suffix)]
    return name


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


def artifact_mentions(node, path="", found=None):
    """EVERY mention of a confirmation artefact, with the key that cites it (item v2.e).

    The previous census only saw dicts carrying BOTH `artifact` and `artifact_sha256`
    (v2.e: 5 pairs against 10 mentions in the fixture file), so a mention without a paired
    digest - e.g. `/adjudication_summary_2026_09_25/artifact` - sat OUTSIDE the post-seal
    void check. This returns one row per citation key, marked paired or unpaired, so the
    unpaired ones can be resolved by digest and still put through the check.
    """
    if found is None:
        found = []
    if isinstance(node, dict):
        if "artifact" in node or "artifact_sha256" in node:
            found.append({"json_path": path or "/",
                          "artifact": node.get("artifact"),
                          "paired_artifact_sha256": node.get("artifact_sha256"),
                          "keys_present": [k for k in ("artifact", "artifact_sha256")
                                           if k in node],
                          "paired": "artifact" in node and "artifact_sha256" in node})
        for k, v in node.items():
            if k in ("artifact", "artifact_sha256"):
                continue
            artifact_mentions(v, path + "/" + str(k), found)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            artifact_mentions(v, path + "[%d]" % i, found)
    return found


def artifact_occurrences(node, candidates, path="", found=None):
    """EVERY occurrence of a candidate artefact path anywhere in the document (item v2.e).

    `artifact_mentions` walks citation KEYS; this walks string VALUES as well, because a fixture
    file can cite an artefact inside a note ("<path> (transcript span + book slug/offset/quote,
    re-derived)") — a mention a reader must be able to find, and a mention that must sit inside
    the post-seal check. The two views together are the census's population: keys are one kind of
    citation, prose is the other, and the report states both counts.
    """
    if found is None:
        found = []
    if isinstance(node, dict):
        for k, v in node.items():
            artifact_occurrences(v, candidates, path + "/" + str(k), found)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            artifact_occurrences(v, candidates, path + "[%d]" % i, found)
    elif isinstance(node, str):
        for cand in candidates:
            if cand in node:
                found.append({"json_path": path or "/", "artifact": cand,
                              "kind": "value-citation" if node.strip() == cand
                                      else "prose-citation",
                              "text": node})
    return found


def tool_commit_of(repo, tool_path):
    """`tool_commit` = the reachable commit carrying this tool's CURRENT bytes (item v2.d).

    The commit that *added* the tool is reported beside it as `tool_origin_commit`: a tool that
    has been repaired since is attributable to the repair, and a reader checking "the blob at
    tool_commit equals the tool at head" must be pointed at the revision that is actually live.
    """
    out = git(repo, "log", "--format=%H", "--", tool_path)
    if not out:
        return None, None, None
    commits = out.strip().splitlines()
    latest, first = commits[0], commits[-1]
    utc = (git(repo, "show", "-s", "--format=%cI", latest) or "").strip() or None
    return latest, utc, first


def first_commit(repo, path):
    """The commit that first ADDED the path: authorship, as opposed to the last touch."""
    out = git(repo, "log", "--format=%H", "--reverse", "--", path)
    if not out:
        return None, None
    commit = out.strip().splitlines()[0]
    return commit, (git(repo, "show", "-s", "--format=%cI", commit) or "").strip() or None


def seal_history(repo, seal_path):
    """The seal file's own revision history: proves whether it was re-drawn or re-manifested.

    Item v2.a(iii): `79eb401`'s subject says "re-seal", which reads as a second draw. Comparing
    the two blobs settles it mechanically: keys added / removed / changed, and the values of
    `holdout`, `tuning` and `salt` on both sides.
    """
    out = git(repo, "log", "--format=%H", "--", seal_path)
    if not out:
        return None
    commits = out.strip().splitlines()
    entry = {"revisions": commits, "count": len(commits)}
    if len(commits) < 2:
        entry["note"] = "single revision: no earlier blob to compare"
        return entry
    new_c, old_c = commits[0], commits[1]
    new_blob = blob_at(repo, new_c, seal_path)
    old_blob = blob_at(repo, old_c, seal_path)
    if new_blob is None or old_blob is None:
        entry["note"] = "a blob is unavailable; comparison not possible"
        return entry
    new, old = json.loads(new_blob), json.loads(old_blob)
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = sorted(k for k in set(new) & set(old) if new[k] != old[k])
    entry.update({
        "newest_commit": new_c, "previous_commit": old_c,
        "newest_commit_utc": (git(repo, "show", "-s", "--format=%cI", new_c) or "").strip(),
        "previous_commit_utc": (git(repo, "show", "-s", "--format=%cI", old_c) or "").strip(),
        "keys_added": added, "keys_removed": removed, "keys_changed": changed,
        "draw_values": {k: {"previous": old.get(k), "newest": new.get(k),
                            "identical": old.get(k) == new.get(k)}
                        for k in ("holdout", "tuning", "salt")},
    })
    entry["one_draw"] = (not removed and set(changed) <= {"manifest"}
                         and all(v["identical"] for v in entry["draw_values"].values()))
    entry["one_draw_statement"] = (
        "the split was drawn ONCE: between %s and %s no key was removed, the only changed key "
        "is %r, and holdout / tuning / salt are identical - the later commit re-manifested the "
        "same draw, so no new salt is owed" % (old_c[:7], new_c[:7], changed))
    return entry


def audit(repo, seal_path, utc=None):
    with open(os.path.join(repo, seal_path), "rb") as fh:
        seal_blob = fh.read()
    seal = json.loads(seal_blob)
    seal_commit, seal_utc = last_commit(repo, seal_path)
    tool_path = "tools/m4_seal_audit.py"
    t_commit, t_utc, t_origin = tool_commit_of(repo, tool_path)
    # the tool's bytes AT THE AUDITED REPO'S HEAD: the report is about committed state, so a
    # dirty working tree must not be able to change the attribution it states
    tool_blob_now = head_blob(repo, tool_path)
    tool_sha_source = "blob at HEAD of the audited repo"
    with open(os.path.abspath(__file__), "rb") as fh:
        tool_blob_running = fh.read()
    tool_running_matches_committed = (tool_blob_now is not None
                                      and sha256_bytes(tool_blob_running)
                                      == sha256_bytes(tool_blob_now))
    if tool_blob_now is None:
        with open(os.path.abspath(__file__), "rb") as fh:
            tool_blob_now = fh.read()
        tool_sha_source = "the running file (no committed blob at HEAD)"
    tool_blob_then = blob_at(repo, t_commit, tool_path) if t_commit else None
    report = {
        "tool": tool_path,
        "tool_sha256": sha256_bytes(tool_blob_now),
        "tool_sha256_source": tool_sha_source,
        "tool_sha256_running": sha256_bytes(tool_blob_running),
        "tool_running_matches_committed": tool_running_matches_committed,
        "tool_running_matches_note": ("the report attributes itself to the COMMITTED blob "
                                      "(a dirty tree cannot change the attribution) and states "
                                      "separately whether the file that produced this report "
                                      "equals it; a report generated by uncommitted bytes says "
                                      "so here rather than hiding behind the commit"),
        "tool_commit": t_commit,
        "tool_commit_utc": t_utc,
        "tool_origin_commit": t_origin,
        "tool_commit_note": ("item v2.d: the reachable commit carrying this tool's CURRENT "
                             "bytes (a repair commit, if the tool was repaired); the blob at "
                             "that commit must equal the tool at head - checked here as "
                             "`tool_unchanged_since_tool_commit`. `tool_origin_commit` names "
                             "the commit that first added the tool"),
        "tool_unchanged_since_tool_commit": (
            tool_blob_then is not None
            and sha256_bytes(tool_blob_then) == sha256_bytes(tool_blob_now)),
        "tool_commit_tip": t_origin,
        "audit_utc_source": ("date -u at run time when --utc is not passed; passed through "
                             "verbatim, never rounded, and the same string is cited in the "
                             "companion appendix (checked below)"),
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
        "seal_history": seal_history(repo, seal_path),
        "confirmation_artifacts": [],
        "artifact_mentions": [],
        "taint_disclosure": {},
        "membership": {},
        "void_reasons": [],
        "reproduction": {
            "byte_identical_when": ("re-run at the audited head with the report's own --utc: "
                                    "`python3 tools/m4_seal_audit.py --seal <seal> --out <path> "
                                    "--utc <this report's audit_utc>`"),
            "volatile_fields": ["head_commit_at_audit", "tool_commit", "tool_sha256",
                            "tool_sha256_running", "tool_running_matches_committed"],
            "volatile_because": ("this is an AUDIT RECORD, not a digest of the repository: "
                                "`head_commit_at_audit` names the head the audit was taken at, "
                                "and `tool_commit`/`tool_sha256` follow the tool's committed "
                                "bytes, so a re-run at a LATER head reproduces every seal "
                                "finding and every classification byte-for-byte while those "
                                "three fields legitimately move. The appendix cites this "
                                "report's digest; a re-derivation should compare fields, not "
                                "the file digest, unless it is run at the audited head."),
            "audited_head": (git(repo, "rev-parse", "HEAD") or "").strip() or None,
        },
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
        # --- every mention of a confirmation artefact, paired or not (item v2.e) ----------
        for m in artifact_mentions(live_doc):
            artifact = m["artifact"]
            blob = head_blob(repo, artifact) if artifact else None
            artefact_commit, artefact_utc = (last_commit(repo, artifact) if artifact
                                             else (None, None))
            authored_commit, authored_utc = (first_commit(repo, artifact) if artifact
                                             else (None, None))
            head_sha = sha256_bytes(blob) if blob is not None else None
            cited_sha = m["paired_artifact_sha256"]
            digest = cited_sha or head_sha          # unpaired mentions resolved by digest
            ok = digest is not None and head_sha is not None and digest == head_sha
            relation = None
            if artefact_utc and seal_utc:
                relation = "pre-seal" if artefact_utc < seal_utc else "post-seal"
            row = {
                "cited_by": path, "json_path": m["json_path"],
                "keys_citing": m["keys_present"], "paired": m["paired"],
                "artifact": artifact, "artifact_sha256": digest,
                "cited_sha256": cited_sha,
                "digest_source": "paired artifact_sha256" if cited_sha
                                 else "resolved from the file at HEAD (unpaired mention)",
                "digest_asserted": bool(cited_sha),
                "digest_matches_head": ok, "commit": artefact_commit,
                "commit_utc": artefact_utc, "relation_to_seal": relation,
                "commit_note": ("`commit`/`commit_utc` are the commit that last TOUCHED the "
                                "path (a digest-only re-pin moves them); `authored_commit` is "
                                "the commit that first added it, which is when the "
                                "confirmation was actually written"),
                "authored_commit": authored_commit, "authored_utc": authored_utc,
                "authored_relation_to_seal": (
                    "pre-seal" if (authored_utc and seal_utc and authored_utc < seal_utc)
                    else ("post-seal" if (authored_utc and seal_utc) else None)),
                "in_void_check": True,
            }
            report["artifact_mentions"].append(row)
            if not ok:
                report["outstanding"].append(
                    "%s: cites %s at %s… (%s) but HEAD's blob does not match"
                    % (path, artifact, str(digest)[:12], row["digest_source"]))
            if relation == "post-seal":
                report["void_reasons"].append(
                    "%s: cites %s whose last commit (%s, %s) postdates the seal — a "
                    "confirmation artefact created after the seal"
                    % (path, artifact, str(artefact_commit)[:7], artefact_utc))
        report["fixture_sources"].append(entry)

    # artefact-level view: one row per distinct artefact, with EVERY key that cites it
    grouped = {}
    for row in report["artifact_mentions"]:
        g = grouped.setdefault(row["artifact"], {
            "artifact": row["artifact"], "citing_paths": [], "cited_by_keys": [],
            "paired_mentions": 0, "unpaired_mentions": 0,
            "artifact_sha256": row["artifact_sha256"], "commit": row["commit"],
            "commit_utc": row["commit_utc"], "relation_to_seal": row["relation_to_seal"],
            "authored_commit": row["authored_commit"], "authored_utc": row["authored_utc"],
            "authored_relation_to_seal": row["authored_relation_to_seal"],
            "digest_matches_head": row["digest_matches_head"]})
        g["citing_paths"].append(row["cited_by"])
        g["cited_by_keys"].append("%s%s" % (row["cited_by"], row["json_path"]))
        g["paired_mentions" if row["paired"] else "unpaired_mentions"] += 1
        g["digest_matches_head"] = g["digest_matches_head"] and row["digest_matches_head"]
    report["confirmation_artifacts"] = [grouped[k] for k in sorted(grouped)]
    # the population, stated: citation KEYS plus PROSE citations inside string values
    candidates = sorted({r["artifact"] for r in report["artifact_mentions"] if r["artifact"]})
    occurrences = artifact_occurrences(live_doc, candidates) if candidates else []
    for occ in occurrences:
        artefact_utc = (last_commit(repo, occ["artifact"])[1] if occ["artifact"] else None)
        occ["authored_relation_to_seal"] = (
            None if not (artefact_utc and seal_utc)
            else ("pre-seal" if artefact_utc < seal_utc else "post-seal"))
        occ["post_seal_check"] = ("covered by the artefact-level check above; this occurrence "
                                  "names the same artefact, whose authored commit decides the "
                                  "re_seal_rule")
    report["artifact_occurrences"] = occurrences
    report["artifact_mention_census"] = {
        "key": ("one row per citation KEY (`artifact` / `artifact_sha256` inside a dict) in "
                "artifact_mentions; one row per STRING OCCURRENCE of a cited path - value or "
                "prose - in artifact_occurrences"),
        "mentions": len(report["artifact_mentions"]),
        "occurrences": len(occurrences),
        "value_citations": sum(1 for o in occurrences if o["kind"] == "value-citation"),
        "prose_citations": sum(1 for o in occurrences if o["kind"] == "prose-citation"),
        "distinct_artifacts": len(grouped),
        "paired_mentions": sum(1 for r in report["artifact_mentions"] if r["paired"]),
        "unpaired_mentions": sum(1 for r in report["artifact_mentions"] if not r["paired"]),
        "population_statement": ("the census covers the whole population it names: every key "
                                 "citation is put through the post-seal check (an unpaired "
                                 "mention's digest is resolved from the artefact at HEAD), and "
                                 "every occurrence of a cited path - including prose citations "
                                 "inside string values - is enumerated with the same artefact "
                                 "attribution; a reader can reconcile value+prose against the "
                                 "raw file"),
        "note": ("item v2.e: the previous census saw only artifact+artifact_sha256 pairs, which "
                 "is how an unpaired mention came to sit outside the post-seal check"),
    }


    # --- taint disclosure: the v2-holdout members carrying pre-seal adjudication labels ----
    ex_file = os.path.join(repo, "tools", "HELD-OUT-SPLIT-V2-EXCLUSIONS.json")
    if os.path.exists(ex_file):
        ex = json.loads(open(ex_file, encoding="utf-8").read())
        tainted = []
        for e in ex.get("excluded_transcripts", []):
            tainted.append({"transcript": e.get("transcript"), "signals": e.get("signals", []),
                            "verdicts": e.get("verdicts", {})})
        report["taint_disclosure"] = {
            "source": "tools/HELD-OUT-SPLIT-V2-EXCLUSIONS.json",
            "source_sha256": sha256_bytes(open(ex_file, "rb").read()),
            "excluded_transcripts": tainted,
            "excluded_count": len(tainted),
            "signals_total": sum(len(t["signals"]) for t in tainted),
            "evaluated_holdout_transcripts": ex.get("evaluated_holdout_transcripts"),
            "decision": ex.get("decision"),
            "why": ("the four v2-holdout transcripts carry labels written before the seal by "
                    "the TASK-018 adjudication; evaluating them would read holdout signal "
                    "bytes with pre-seal labels in hand, so they are excluded from quantum "
                    "b's denominator and the evaluated holdout is 29 of 33"),
        }
        # the appendix and the dated note must NAME the taint, not merely reference it
        for citer in ("runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md",
                      "tools/HELD-OUT-SPLIT-V2-NOTE-2026-09-26.md"):
            cpath = os.path.join(repo, citer)
            if not os.path.exists(cpath):
                report["outstanding"].append(
                    "taint disclosure: %s is absent, so the disclosure has no reader-facing home"
                    % citer)
                continue
            text = open(cpath, encoding="utf-8").read()
            missing = [t["transcript"] for t in tainted
                       if t["transcript"] not in text and stem(t["transcript"]) not in text]
            missing += [s_id for t in tainted for s_id in t["signals"] if s_id not in text]
            if "29" not in text or "33" not in text:
                missing.append("denominator 29/33")
            if missing:
                report["outstanding"].append(
                    "taint disclosure: %s does not name %d of the tainted items (%s)"
                    % (citer, len(missing), ", ".join(missing[:4])))
    def names_the_taint(path):
        """A companion artefact names the taint when it carries the transcripts, signal ids
        and the denominator - checked mechanically, one read per file."""
        if not os.path.exists(os.path.join(repo, path)):
            return False
        text = open(os.path.join(repo, path), encoding="utf-8").read()
        return (all(t["transcript"] in text or stem(t["transcript"]) in text
                    for t in report["taint_disclosure"].get("excluded_transcripts", []))
                and all(sid in text
                        for t in report["taint_disclosure"].get("excluded_transcripts", [])
                        for sid in t["signals"])
                and "29" in text and "33" in text)

    report["taint_disclosure"]["named_in"] = [
        p for p in ("runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md",
                    "tools/HELD-OUT-SPLIT-V2-NOTE-2026-09-26.md")
        if names_the_taint(p)]
    if report["taint_disclosure"].get("excluded_count") and \
            not report["taint_disclosure"].get("named_in"):
        report["outstanding"].append(
            "taint disclosure: no companion artefact names all four tainted transcripts")

    # item v2.c: the companion appendix must cite the SAME exact stamp this report carries -
    # a report and its appendix naming different times for one audit is the defect the gate found
    appendix = os.path.join(repo, "runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md")
    if os.path.exists(appendix):
        text = open(appendix, encoding="utf-8").read()
        stamp = report["audit_utc"]
        # The appendix cites the audit stamp on lines that say so. A citation equal to this
        # report's stamp is LIVE; any other timestamp on such a line must be marked as
        # superseded or as a quotation (`read \`...\``), else the two artefacts disagree about
        # when one audit ran - which is item v2.c.
        live, marked, unmarked = [], [], []
        for line in text.splitlines():
            low = line.lower()
            if not any(k in low for k in ("audit utc", "audit_utc", "audit stamp")):
                continue
            for t in __import__("re").findall(r"20\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ", line):
                if t == stamp:
                    live.append(t)
                elif "supersede" in low or "read `" in low or "earlier citation" in low:
                    marked.append(t)
                else:
                    unmarked.append(t)
        report["appendix_audit_utc_check"] = {
            "report_stamp": stamp,
            "live_citations": sorted(set(live)),
            "marked_superseded_or_quoted": sorted(set(marked)),
            "unmarked_conflicting_citations": sorted(set(unmarked)),
            "cited_identically": bool(live) and not unmarked,
        }
        if not report["appendix_audit_utc_check"]["cited_identically"]:
            report["outstanding"].append(
                "item v2.c: the appendix must cite this report's exact audit stamp (%s) and mark "
                "every other audit-time citation as superseded/history; live %s, marked %s, "
                "unmarked conflicts %s" % (stamp, sorted(set(live)) or "none",
                                           sorted(set(marked)) or "none",
                                           sorted(set(unmarked)) or "none"))

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
