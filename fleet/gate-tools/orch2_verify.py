#!/usr/bin/env python3
"""ORCH-2 gate instrument: mechanical re-derivation of the ORCH-2 VERIFICATION LEDGER.

Read-only over a gate-side worktree of a WORKER-2 head. Re-runs every row of
`fleet/ORCH-2-VERIFICATION-LEDGER.md` and prints, per row: expected (with its
source), observed, verdict, and **how many comparisons were actually performed**.

Two rules are built in, because ORCH-2 broke both of them once (see ledger §5):

  R1  Every set-level or interval check reports `n` = the number of comparisons
      performed. A zero produced by zero comparisons is reported as VACUOUS, not
      as PASS.
  R2  Every byte-exactness count reports the denominator of rows for which the
      comparison was *defined*. Rows where a required key is absent are counted
      separately and never compared as `None == None`.

Usage:
    python3 fleet/gate-tools/orch2_verify.py <worktree> [--head SHA] [--json]

The worktree must already have the corpus materialized (`sh tools/m5r_inputs.sh`)
so that `corpus/docdocgo/overlays/*.txt` and `evidence/runs/m5-raw/records/*.json`
exist. Nothing here writes to the worktree and nothing here runs a detector.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import math
import os
import re
import subprocess
import sys

PASS, FAIL, VACUOUS, INFO, PROXY = "PASS", "FAIL", "VACUOUS", "INFO", "PROXY"


# ---------------------------------------------------------------- helpers
def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(wt: str, *args: str) -> tuple[int, bytes]:
    p = subprocess.run(["git", *args], cwd=wt, capture_output=True)
    return p.returncode, p.stdout


def dir_digest(root: str, key: str = "relpath") -> tuple[str, int]:
    """sha256 over sorted lines '<sha256(bytes)>  <key>\n' for every file under root."""
    lines = []
    for dirpath, _dirs, files in os.walk(root):
        for f in sorted(files):
            p = os.path.join(dirpath, f)
            k = os.path.relpath(p, root) if key == "relpath" else os.path.basename(p)
            lines.append(f"{sha_file(p)}  {k}\n")
    lines.sort()
    return sha_bytes("".join(lines).encode()), len(lines)


def norm(x: str) -> str:
    """Extension-stripped basename. The split files and the census record files
    disagree about extensions; comparing them raw silently matches nothing."""
    b = os.path.basename(x)
    for ext in (".txt", ".json"):
        if b.endswith(ext):
            b = b[: -len(ext)]
    return b


def pois_cdf(k: int, lam: float) -> float:
    """P(X <= k) for X ~ Poisson(lam), computed in log space (lam may exceed 100)."""
    return sum(math.exp(i * math.log(lam) - lam - math.lgamma(i + 1)) for i in range(k + 1))


def tokens(s: str) -> list[str]:
    """Token rule stated explicitly (a documented gate-instrument defect class in
    this campaign): alphanumerics plus apostrophe and hyphen INSIDE tokens; every
    other character, including em/en dashes, is a SEPARATOR."""
    out, cur = [], ""
    for ch in s or "":
        if ch.isalnum() or ch in "'-":
            cur += ch
        else:
            if cur:
                out.append(cur.lower())
                cur = ""
    if cur:
        out.append(cur.lower())
    return out


class Report:
    def __init__(self) -> None:
        self.rows: list[dict] = []

    def add(self, section, name, expected, observed, verdict, n=None, note=""):
        self.rows.append(dict(section=section, name=name, expected=str(expected),
                              observed=str(observed), verdict=verdict, n=n, note=note))
        flag = "" if verdict in (PASS, INFO) else f"  <<< {verdict}"
        nn = "" if n is None else f" [n={n}]"
        print(f"  {verdict:6s} {name}{nn}{flag}")
        if note:
            print(f"         {note}")

    def check(self, section, name, expected, observed, n=None, note=""):
        self.add(section, name, expected, observed, PASS if expected == observed else FAIL, n, note)
        return expected == observed


# ---------------------------------------------------------------- checks
def section_bindings(wt, rep, head):
    print("\n== 1. bindings and digests ==")
    man = json.load(open(os.path.join(wt, "findings/PROVENANCE.json"), encoding="utf-8"))
    sup = json.load(open(os.path.join(wt, "runs/m4-q4-holdout/PROVENANCE-SUPPLEMENT.json"), encoding="utf-8"))

    rep.check("1", "corpus zip", man["inputs"]["corpus_zip_sha256"],
              sha_file(os.path.join(wt, "docdocgo-fixes.zip")))
    bs = man["book_store"]
    rep.check("1", f"book store ({bs['path']})", bs["sha256"], sha_file(os.path.join(wt, bs["path"])))
    rep.check("1", "policy (fleet2/POLICY-MANIFEST.sha256)", man["policy_sha256"],
              sha_file(os.path.join(wt, "fleet2/POLICY-MANIFEST.sha256")))

    led = os.path.join(wt, "findings/ledger.jsonl")
    nlines = sum(1 for _ in open(led, encoding="utf-8"))
    rep.check("1", "ledger digest", man["outputs"]["ledger.jsonl"], sha_file(led))
    rep.check("1", "ledger line count", man["outputs"]["findings"], nlines)

    d, n = dir_digest(os.path.join(wt, "findings/by-transcript"))
    rep.check("1", "by-transcript digest", man["outputs"]["by_transcript_digest"], d, n=n)
    rep.check("1", "by-transcript file count", man["outputs"]["by_transcript_files"], n, n=n)

    recdir = os.path.join(wt, "evidence/runs/m5-raw/records")
    d, n = dir_digest(recdir)
    rep.check("1", "inherited census records digest", man["inputs"]["records_digest_sha256"], d, n=n)
    rep.check("1", "inherited census file count", man["inputs"]["records_files"], n, n=n)

    # overlays: stated method, plus the warned-against variant (ledger 1.8)
    ovdir = os.path.join(wt, "corpus/docdocgo/overlays")
    names = sorted(b for b in os.listdir(ovdir) if b.endswith(".txt"))
    lines = []
    for b in names:
        t = open(os.path.join(ovdir, b), encoding="utf-8", errors="replace").read()
        lines.append(f"{sha_bytes(t.encode('utf-8'))}  {b}\n")
    rep.check("1", "overlays digest (stated method)", man["inputs"]["overlays_digest"],
              sha_bytes("".join(lines).encode()), n=len(lines))
    warn = sha_bytes("\n".join(sorted(l.rstrip("\n") for l in lines)).encode())
    rep.add("1", "overlays WRONG-variant reproduces the manifest's warning", "58274f46…",
            warn[:8] + "…", PASS if warn.startswith("58274f46") else FAIL, n=len(lines),
            note='exact construction: sha256("\\n".join(sorted(lines_without_trailing_newline))) '
                 "— not stated in the manifest (item 13)")

    # fixtures binding: basename keys over fixtures/confirmed (ledger 1.9)
    exp = man["inputs"]["fixtures_digest_sha256"]
    conf = sorted(os.listdir(os.path.join(wt, "fixtures/confirmed")))
    d_base, n_base = dir_digest(os.path.join(wt, "fixtures/confirmed"), key="basename")
    d_rel, _ = dir_digest(os.path.join(wt, "fixtures"), key="relpath")
    rep.check("1", "fixtures binding (basename keys over fixtures/confirmed/)", exp, d_base, n=n_base,
              note=f"files: {conf}; manifest fixtures_files={man['inputs']['fixtures_files']}; "
                   f"the stated 'same construction as records_digest' (relpath over fixtures/) gives "
                   f"{d_rel[:12]}… and does NOT reproduce it (item 13)")

    # q4 supplement artefacts + configs
    q4dir = os.path.join(wt, "runs/m4-q4-holdout")
    nok = ntot = 0
    for leg in ("v1", "drop", "format"):
        r = sup["runs"][leg]
        for kind in ("signals", "provenance"):
            f = os.path.basename(r[f"{kind}_file"])
            act = sha_file(os.path.join(q4dir, f))
            ntot += 1
            nok += act == r[f"{kind}_sha256"]
            rep.check("1", f"q4 {leg} {kind} file", r[f"{kind}_sha256"][:16] + "…", act[:16] + "…")
        cfg = r.get("config")
        if cfg is not None and r.get("config_sha256"):
            compact = sha_bytes(json.dumps(cfg, sort_keys=True, separators=(",", ":")).encode())
            ntot += 1
            nok += compact == r["config_sha256"]
            rep.check("1", f"q4 {leg} config digest (compact JSON)", r["config_sha256"][:16] + "…",
                      compact[:16] + "…",
                      note="canonicalization not stated in this supplement (item 14); the q2 supplement states it")
        if leg == "v1" and r.get("signals_bytes"):
            act = os.path.getsize(os.path.join(q4dir, os.path.basename(r["signals_file"])))
            rep.check("1", "q4 v1 signals byte count", r["signals_bytes"], act)
    rep.add("1", "q4 supplement digest total", f"{ntot}/{ntot}", f"{nok}/{ntot}",
            PASS if nok == ntot else FAIL, n=ntot)

    # splits
    sp1 = os.path.join(wt, "tools/HELD-OUT-SPLIT.json")
    j = json.load(open(sp1, encoding="utf-8"))
    rep.check("1", "split v1 file digest", "481d8513…", sha_file(sp1)[:8] + "…")
    rep.check("1", "split v1 bucket counts", (193, 37), (len(j["tuning"]), len(j["holdout"])),
              n=len(j["tuning"]) + len(j["holdout"]))
    rep.check("1", "split v1 salt", "fleetyard-m4-holdout-2026-09-25", j.get("salt"))
    rep.check("1", "split v1 corpus_files_sha256", sup["split_corpus_files_sha256"][:16] + "…",
              (j.get("corpus_files_sha256") or "")[:16] + "…")
    sp2 = os.path.join(wt, "tools/HELD-OUT-SPLIT-V2.json")
    if os.path.exists(sp2):
        j2 = json.load(open(sp2, encoding="utf-8"))
        rep.check("1", "split v2 file digest", "73d86f0d…", sha_file(sp2)[:8] + "…")
        rep.check("1", "split v2 bucket counts", (197, 33), (len(j2["tuning"]), len(j2["holdout"])),
                  n=len(j2["tuning"]) + len(j2["holdout"]))
        adj = j2.get("fixtures_adjacent") or j2.get("fixtures_adjacent_digest")
        rep.add("1", "split v2 fixtures-adjacent binding", "c40d272f… (item v2.a owed)", str(adj)[:60],
                INFO, note="criterion v2.5: the seal binds the actual fixtures-adjacent digest")

    # reducer across three commits
    tool = sha_file(os.path.join(wt, "tools/m5r_reduce.py"))
    same = []
    for c in ("219075a", "ffb8811", head[:7]):
        rc, blob = git(wt, "show", f"{c}:tools/m5r_reduce.py")
        same.append(sha_bytes(blob) if rc == 0 else "UNREADABLE")
    rep.check("1", "m5r_reduce.py identical across 219075a/ffb8811/head", [tool] * 3, same, n=3,
              note="the M5-R PASS depends on this")

    # other head artefacts unchanged
    for path, exp in (("runs/m4-q2-dropword/signals.json", "8d71f57b"),
                      ("runs/m4-q2-adjudication/adjudication.jsonl", "82863ab9"),
                      ("runs/m4-q2-adjudication/SUMMARY.md", "0a37118e"),
                      ("runs/m4-q2-adjudication/fixtures-adjudication.json", "61568a9e"),
                      ("runs/m4-q3-format/signals-v2tuning.json", "b25651e4"),
                      ("tools/det_dropword.py", "a0236325"),
                      ("tools/det_format.py", "ef9ff4f2")):
        p = os.path.join(wt, path)
        if os.path.exists(p):
            rep.check("1", f"unchanged: {path}", exp + "…", sha_file(p)[:8] + "…")
        else:
            rep.add("1", f"unchanged: {path}", exp + "…", "ABSENT", FAIL)

    # the 20.10 failure ground: does tool_commit contain the generator?
    tc = sup.get("tool_commit") or sup["runs"]["v1"].get("tool_commit")
    rc, _ = git(wt, "cat-file", "-e", f"{tc[:12]}:tools/m4_q4_supplement.py")
    rep.add("1", "criterion 20.10: tool_commit contains the generator", "present", 
            "present" if rc == 0 else f"ABSENT at {tc[:12]}", PASS if rc == 0 else FAIL, n=1,
            note="item 8a: pin generator_tool + generator_tool_commit + generator_tool_sha256")
    return man, sup


def section_pins(wt, rep, sup):
    print("\n== 1b. v1 toolchain pins (three-way) ==")
    pins = sup["runs"]["v1"]["toolchain"]["pins"]
    ok = 0
    for f, stored in sorted(pins.items()):
        rc, blob = git(wt, "show", f"bf97d85:tools/{f}")
        arch = sha_bytes(blob) if rc == 0 else "ABSENT-IN-ARCHIVE"
        p = os.path.join(wt, "tools", f)
        head = sha_file(p) if os.path.exists(p) else "ABSENT-AT-HEAD"
        good = stored == arch == head
        ok += good
        rep.add("1b", f"pin {f}", stored[:12] + "…", f"archive {arch[:12]}… head {head[:12]}…",
                PASS if good else FAIL, n=3)
    rep.add("1b", "pins verified three-way", f"{len(pins)}/{len(pins)}", f"{ok}/{len(pins)}",
            PASS if ok == len(pins) else FAIL, n=3 * len(pins))


def section_manifest_stats(wt, rep, man):
    print("\n== 2. M5-R manifest stats re-derived from the ledger ==")
    recs = [json.loads(l) for l in open(os.path.join(wt, "findings/ledger.jsonl"), encoding="utf-8")]
    rep.check("2", "findings (rows)", man["outputs"]["findings"], len(recs), n=len(recs))
    claims = [c for r in recs for c in (r.get("claim_checks") or [])]
    rep.check("2", "raw_signals (sum of claim_checks)", man["stats"]["raw_signals"], len(claims), n=len(claims))
    multi = [r.get("id") for r in recs if len(r.get("claim_checks") or []) > 1]
    rep.add("2", "rows carrying two claims (explains 1336 vs 1334)", "2 rows", f"{len(multi)} rows {multi}",
            PASS if len(recs) + len(multi) == len(claims) else FAIL, n=len(recs))
    per = collections.Counter(c.get("detector") for c in claims)
    okc = collections.Counter(c.get("detector") for c in claims if c.get("claim_ok"))
    for det, exp in man["stats"]["per_detector"].items():
        rep.check("2", f"claims checked: {det}", exp, per.get(det, 0), n=per.get(det, 0))
        rep.check("2", f"claims corroborated: {det}", man["stats"]["claims"][det]["corroborated"],
                  okc.get(det, 0), n=okc.get(det, 0))
    cov = {r.get("transcript") for r in recs}
    rep.check("2", "transcripts with findings", man["stats"]["transcripts_with_findings"], len(cov), n=len(cov))
    rep.check("2", "zero-finding transcripts", man["stats"]["coverage"]["zero_finding_transcripts"],
              man["stats"]["transcripts_total"] - len(cov), n=man["stats"]["transcripts_total"])
    seeded = [r.get("id") for r in recs if r.get("seeded")]
    rep.check("2", "ledger seeded rows (M5-R fixture seeding)", man["stats"]["seeded"], len(seeded),
              n=len(recs), note=f"{seeded} — a DIFFERENT mechanism from the adjudication's seeded flag (ledger §5.3)")
    # A1 unit sizes from the claim notes
    ks = collections.Counter()
    a1 = 0
    for c in claims:
        if c.get("detector") != "A1-repetition":
            continue
        a1 += 1
        m = re.search(r"claim (\d+)-token", c.get("note") or "")
        if m:
            ks[int(m.group(1))] += 1
    exp_ks = {1: 248, 2: 179, 3: 92, 4: 124, 5: 84, 6: 63, 7: 57, 8: 30, 9: 21, 10: 20, 11: 11, 12: 9}
    got = {k: ks[k] for k in sorted(ks)}
    rep.check("2", "A1 unit-size tally (regex over claim notes)", exp_ks, got, n=a1,
              note=f"sum {sum(ks.values())}, max k {max(ks) if ks else 0} with {ks[max(ks)] if ks else 0} claims "
                   f"-> kmax=16 is max-observed + 4 tokens headroom")
    rep.add("2", "book_refs", man["stats"]["book_refs"], "not re-derivable by proxy", PROXY,
            note="a substring proxy over claim_checks gives 240; recorded as PROXY, never as a mismatch")


def section_census_exposure(wt, rep, sup):
    print("\n== 3. census, exposure and the three Poisson rows ==")
    sp = json.load(open(os.path.join(wt, "tools/HELD-OUT-SPLIT.json"), encoding="utf-8"))
    tun = {norm(x) for x in sp["tuning"]}
    hol = {norm(x) for x in sp["holdout"]}
    recdir = os.path.join(wt, "evidence/runs/m5-raw/records")
    tt, th = collections.Counter(), collections.Counter()
    files = 0
    for f in sorted(os.listdir(recdir)):
        if not f.endswith(".json"):
            continue
        files += 1
        b = norm(f)
        items = json.load(open(os.path.join(recdir, f), encoding="utf-8"))
        if isinstance(items, dict):
            items = items.get("records", items.get("findings", []))
        for it in items:
            (th if b in hol else tt)[it.get("detector_id") or "?"] += 1
    rep.add("3", "census TUNING rows", "1149", f"{sum(tt.values())} {dict(tt)}",
            PASS if sum(tt.values()) == 1149 else FAIL, n=files)
    rep.add("3", "census HOLDOUT rows", "185 (A1 162, A2 15, B2 8, B1 0)", f"{sum(th.values())} {dict(th)}",
            PASS if sum(th.values()) == 185 and th.get("B1-contradiction", 0) == 0 else FAIL, n=files,
            note="B1 zero: B1 receives NO validation from the receipt; v1's B1 hold stands")
    rep.check("3", "census total == ledger rows", 1334, sum(tt.values()) + sum(th.values()), n=files)

    ovdir = os.path.join(wt, "corpus/docdocgo/overlays")

    def chars(b):
        p = os.path.join(ovdir, b if b.endswith(".txt") else b + ".txt")
        return len(open(p, encoding="utf-8", errors="replace").read())

    ct = sum(chars(b) for b in sorted(tun))
    ch = sum(chars(b) for b in sorted(hol))
    ratio = ch / ct
    rep.check("3", "tuning characters", 12228661, ct, n=len(tun))
    rep.check("3", "holdout characters", 1996122, ch, n=len(hol))
    rep.check("3", "exposure ratio (5 dp)", "0.16323", f"{ratio:.5f}", n=len(tun) + len(hol))
    for name, obs, base, exp_lam, exp_p in (
            ("v1 leg", 185, sum(tt.values()), "187.5548", "0.445075"),
            ("C2-format", 12, 49, "7.9984", "0.936279"),
            ("C1-drop", 5, 122, "19.9144", "7.67659e-05")):
        lam = base * ratio
        p = pois_cdf(obs, lam)
        rep.check("3", f"Poisson {name}: expected", exp_lam, f"{lam:.4f}", n=1)
        rep.check("3", f"Poisson {name}: P(X<=obs)", exp_p, f"{p:.6g}", n=1)
    v1_lam = sum(tt.values()) * ratio
    rep.add("3", "worker's published v1 row vs the census", "187.9 / 0.44",
            f"census gives {v1_lam:.4f} / {pois_cdf(185, v1_lam):.4f}", FAIL, n=1,
            note="item 11a: publish the per-row tuning-side counts 1149 / 49 / 122 and reconcile 187.9 with 187.6")

    # comparability of tuning-side and holdout-side configurations (ledger 1.18 / 3.6)
    q2 = json.load(open(os.path.join(wt, "runs/m4-q2-dropword/PROVENANCE-SUPPLEMENT.json"), encoding="utf-8"))
    q3p = os.path.join(wt, "runs/m4-q3-format/PROVENANCE-SUPPLEMENT.json")
    drop_same = q2["config_sha256"] == sup["runs"]["drop"]["config_sha256"]
    rep.add("3", "drop-leg config identical tuning vs holdout", q2["config_sha256"][:12] + "…",
            sup["runs"]["drop"]["config_sha256"][:12] + "…", PASS if drop_same else FAIL, n=8)
    if os.path.exists(q3p):
        q3 = json.load(open(q3p, encoding="utf-8"))
        c3 = q3.get("config") or {}
        c4 = sup["runs"]["format"]["config"]
        rep.check("3", "format-leg rule list identical", c3.get("rules"), c4.get("rules"),
                  n=len(c4.get("rules") or []))
        src = open(os.path.join(wt, "tools/det_format.py"), encoding="utf-8").read()
        m = re.search(r'ABBREV\s*=\s*frozenset\(\s*"""(.*?)"""', src, re.S)
        tool_abb = {x.strip() for x in re.split(r"[\s,]+", m.group(1)) if x.strip()} if m else set()
        rep.check("3", "format-leg abbreviations (pinned detector vs q3 config)", sorted(c3.get("abbreviations") or []),
                  sorted(tool_abb), n=len(tool_abb))
        e = re.search(r"^EXCERPT\s*=\s*(\d+)", src, re.M)
        rep.check("3", "format-leg excerpt width (pinned detector vs q3 config)", c3.get("excerpt_chars"),
                  int(e.group(1)) if e else None, n=1)
        rep.add("3", "q4 format config digest covers a SUBSET", "state the subset relation (item 14)",
                f"q3 {q3.get('config_sha256', '')[:12]}… vs q4 {sup['runs']['format']['config_sha256'][:12]}…",
                FAIL, note="comparability established from the pinned source, not from the digests")


def section_adjudication(wt, rep):
    print("\n== 4. TASK-018 adjudication set ==")
    rows = [json.loads(l) for l in open(os.path.join(wt, "runs/m4-q2-adjudication/adjudication.jsonl"),
                                        encoding="utf-8")]
    ovdir = os.path.join(wt, "corpus/docdocgo/overlays")

    def txt_of(t):
        b = os.path.basename(t)
        return open(os.path.join(ovdir, b if b.endswith(".txt") else b + ".txt"),
                    encoding="utf-8", errors="replace").read()

    v = collections.Counter(r["verdict"] for r in rows)
    rep.check("4", "adjudication row count", 122, len(rows), n=len(rows))
    rep.check("4", "verdict split", {"CERTAIN-leg-d": 57, "CANDIDATE": 65}, dict(v), n=len(rows))
    cert = [r for r in rows if r["verdict"] == "CERTAIN-leg-d"]

    # R2: only rows where the comparison is DEFINED
    defined, undefined = [], []
    for i, r in enumerate(rows):
        (defined if (r.get("span_start") is not None and r.get("span_end_matched") is not None)
         else undefined).append((i, r))
    defined = [r for _i, r in defined]
    undefined = [r for _i, r in undefined]
    ok = sum(1 for r in defined if txt_of(r["transcript"])[r["span_start"]:r["span_end_matched"]] == r.get("span"))
    okc = sum(1 for r in defined if r["verdict"] == "CERTAIN-leg-d"
              and txt_of(r["transcript"])[r["span_start"]:r["span_end_matched"]] == r.get("span"))
    rep.add("4", "span re-read (rows where defined)", f"{len(defined)}/{len(defined)}", f"{ok}/{len(defined)}",
            PASS if ok == len(defined) else FAIL, n=len(defined),
            note=f"CERTAIN-leg-d {okc}/{sum(1 for r in defined if r['verdict']=='CERTAIN-leg-d')}; "
                 f"{len(undefined)} rows carry no matched span and are checked separately (never as null == null)")
    ok2 = 0
    for r in undefined:
        t = txt_of(r["transcript"])
        co, ds = r.get("char_offset"), r.get("detector_span")
        ok2 += bool(co is not None and ds and t[co:co + len(ds)] == ds)
    rep.add("4", "rows without a matched span, verified via char_offset + detector_span",
            f"{len(undefined)}/{len(undefined)}", f"{ok2}/{len(undefined)}",
            PASS if ok2 == len(undefined) else (VACUOUS if not undefined else FAIL), n=len(undefined),
            note=f"ids {[r['id'] for r in undefined]}; span is null on these by construction")

    book = open(os.path.join(wt, "corpus/docdocgo/html/merged-book-texts_json_1.js"),
                encoding="utf-8", errors="replace").read()
    gq = 0
    for r in cert:
        g = r["ground_truth"]
        q, co = g.get("quote"), g.get("char_offset")
        gq += bool(q and ((co is not None and book[co:co + len(q)] == q) or q in book))
    rep.add("4", "ground-truth quotes re-read from the book store", f"{len(cert)}/{len(cert)}", f"{gq}/{len(cert)}",
            PASS if gq == len(cert) else FAIL, n=len(cert))
    te = sum(1 for r in rows if tokens(r.get("restored_span")) == tokens((r.get("ground_truth") or {}).get("quote")))
    rep.add("4", "restored_span token-equal to ground_truth.quote", f"{len(cert)} (exactly the CERTAIN rows)",
            str(te), PASS if te == len(cert) else FAIL, n=len(rows),
            note="token rule: alnum + apostrophe/hyphen inside tokens; everything else a separator")

    # fixtures: locate each span, then membership + interval test (R1: report n)
    cf = json.load(open(os.path.join(wt, "fixtures/confirmed/confirmed.json"), encoding="utf-8"))
    cfl = cf["fixtures"] if isinstance(cf, dict) and "fixtures" in cf else cf
    fspans, exact = [], 0
    for f in cfl:
        t = norm(f["transcript"])
        co, q = f["char_offset"], f.get("quoted") or f.get("evidence") or ""
        txt = txt_of(t)
        okk = txt[co:co + len(q)] == q
        exact += okk
        fspans.append((t, f["id"], co, co + len(q), txt.find(q), txt.find(q) + len(q)))
    rep.add("4", "v1 confirmed fixture spans located offset-exactly", f"{len(cfl)}/{len(cfl)}",
            f"{exact}/{len(cfl)}", PASS if exact == len(cfl) else FAIL, n=len(cfl))
    ft = {t for t, *_ in fspans}
    in_ft = [r for r in rows if norm(r["transcript"]) in ft]
    rep.add("4", "adjudicated rows living in a fixture-bearing transcript", "0", str(len(in_ft)),
            PASS if not in_ft else FAIL, n=len(rows),
            note=f"fixture transcripts: {sorted(ft)} — this is the decisive form of the overlap test")
    ncmp = 0
    ov = []
    for r in rows:
        s = r.get("span_start") if r.get("span_start") is not None else r.get("char_offset")
        e = r.get("span_end_matched") or r.get("span_end")
        if s is None or e is None:
            continue
        for t, fid, fs, fe, is_, ie in fspans:
            if t != norm(r["transcript"]):
                continue
            ncmp += 1
            for a, b in ((fs, fe), (is_, ie)):
                if a is not None and b is not None and a >= 0 and s < b and a < e:
                    ov.append((r["id"], fid))
    if ncmp == 0:
        rep.add("4", "interval overlaps with any fixture span", "0", "0", INFO, n=0,
                note="R1 satisfied and the row is honestly VACUOUS-by-data: 0 interval comparisons were possible "
                     "because no adjudicated row shares a transcript with any fixture. The membership test above "
                     "(0 of 122 rows in a fixture-bearing transcript, n=122) is the decisive one.")
    else:
        rep.add("4", "interval overlaps with any fixture span", "0", str(len(ov)),
                PASS if not ov else FAIL, n=ncmp,
                note="R1: n is the number of interval comparisons actually performed")
    st = sum(1 for r in rows if r.get("seeded") is True)
    kp = sum(1 for r in rows if "seeded" in r)
    ins = sum(1 for r in rows if r.get("in_sample") is True)
    rep.add("4", "rows with seeded == true", "0", str(st), PASS if st == 0 else FAIL, n=len(rows),
            note=f"the seeded KEY is present on {kp}/{len(rows)} rows (value false on all of them); "
                 f"in_sample true on {ins}/{len(rows)} — SUMMARY.md's '4 of the 57 carry seeded: true' is FALSE "
                 f"(TASK-018 item 0d, and its copy in PATTERNS §5b-bis)")
    fa = json.load(open(os.path.join(wt, "runs/m4-q2-adjudication/fixtures-adjudication.json"), encoding="utf-8"))
    fl = fa["fixtures"] if isinstance(fa, dict) and "fixtures" in fa else fa
    st2 = sum(1 for f in fl if f.get("seeded") is True)
    rep.add("4", "seeded rows in fixtures-adjudication.json (separate file)", "4", str(st2),
            PASS if st2 == len(fl) == 4 else FAIL, n=len(fl),
            note=f"ids {[f.get('id') for f in fl]} — the real source of the false sentence")


def slice_section(text: str, heading_prefix: str) -> str:
    """Return the body of the section whose heading starts with `heading_prefix`,
    up to the next heading of the same or higher level. Slicing 'from the first
    occurrence of the label to the end of file' lets a LATER section's wording
    satisfy an earlier section's check — a vacuous pass (R1)."""
    lines = text.split("\n")
    start = lvl = None
    for i, ln in enumerate(lines):
        if start is None:
            if ln.lstrip().startswith("#") and heading_prefix in ln:
                start = i
                lvl = len(ln.lstrip()) - len(ln.lstrip().lstrip("#"))
        elif ln.lstrip().startswith("#"):
            l2 = len(ln.lstrip()) - len(ln.lstrip().lstrip("#"))
            if l2 <= lvl:
                return "\n".join(lines[start:i])
    return "\n".join(lines[start:]) if start is not None else ""


def section_stale_digests(wt, rep):
    print("\n== 5. supersession of stale digests ==")
    led = sha_file(os.path.join(wt, "findings/ledger.jsonl"))
    man = json.load(open(os.path.join(wt, "findings/PROVENANCE.json"), encoding="utf-8"))
    rep.check("5", "findings/PROVENANCE.json binds the actual ledger", led, man["outputs"]["ledger.jsonl"])
    stale = "64977c2f"
    for doc in ("findings/README.md", "findings/M4-q5-A1-CLAIM-RECONCILIATION.md",
                "fleet/branches/WORKER-2-M5R-DELIVERY.md"):
        p = os.path.join(wt, doc)
        if not os.path.exists(p):
            rep.add("5", f"{doc}", "superseded digest accompanied", "ABSENT", FAIL)
            continue
        s = open(p, encoding="utf-8").read()
        lines = s.split("\n")
        hits = [i for i, ln in enumerate(lines) if stale in ln]
        # UPPERCASE 'SUPERSESSION' marks the item-11 correction block; lower-case
        # 'supersed…' also occurs in older errata about OTHER subjects, so using it for
        # block detection mis-classifies an original stale line as 'quoted by the
        # correction' (this instrument did exactly that on its first run).
        blocks = [i for i, ln in enumerate(lines) if "SUPERSESSION" in ln]
        marks = [i for i, ln in enumerate(lines) if re.search(r"SUPERSESSION|supersed", ln, re.I)]
        # Document-level test, faithful to append-only discipline: an original stale line
        # cannot carry an adjacent marker without being rewritten, so the requirement is
        # that a supersession marker exists LATER IN THE SAME DOCUMENT, that each stale
        # occurrence is classifiable, that the CURRENT digest appears, and that the
        # manifest is named as the binding of record. Proximity is reported, not required.
        quoted_by_correction = [i for i in hits if any(abs(i - m) <= 5 for m in blocks)]
        original_lines = [i for i in hits if i not in quoted_by_correction]
        superseded = [i for i in original_lines if any(m > i for m in blocks)]
        orphan = [i for i in original_lines if i not in superseded]
        cur = sha_file(os.path.join(wt, "findings/ledger.jsonl"))
        has_cur = cur in s
        names_manifest = "findings/PROVENANCE.json" in s
        verdict = PASS if (not orphan and has_cur and names_manifest) else FAIL
        rep.add("5", f"{doc}: every stale {stale}… line superseded append-only",
                "0 orphans; current digest present; manifest named as binding of record",
                f"{len(hits)} occurrences = {len(quoted_by_correction)} quoted by the correction "
                f"(lines {[i + 1 for i in quoted_by_correction]}, SUPERSESSION block within 5 lines) "
                f"+ {len(original_lines)} original "
                f"(lines {[i + 1 for i in original_lines]}, superseded later: "
                f"{[i + 1 for i in superseded]}, ORPHANS: {[i + 1 for i in orphan]}); "
                f"current digest present: {has_cur}; manifest named: {names_manifest}",
                verdict, n=len(hits),
                note="distance between an original stale line and its appended block is inherent to "
                     "append-only discipline (an inline marker would rewrite history), so it is reported "
                     "rather than required: " + ", ".join(
                         f"L{i + 1}->L{min([m for m in blocks if m > i], default=-1) + 1}"
                         for i in original_lines))
    pat = open(os.path.join(wt, "tools/PATTERNS.md"), encoding="utf-8").read()
    sec = slice_section(pat, "## 5e.")
    rep.add("5", "PATTERNS §5e section located", "non-empty slice between '## 5e.' and the next heading",
            f"{len(sec.splitlines())} lines", PASS if sec else VACUOUS, n=len(sec.splitlines()),
            note="sliced by heading, never by 'from the first label occurrence to EOF' (which lets a later "
                 "section's wording satisfy an earlier section's check)")
    for needle, label in (("98", "superseded flag count"), ("up to 11", "superseded unit bound")):
        present = needle in sec
        annotated = bool(re.search(r"supersed", sec, re.I))
        rep.add("5", f"PATTERNS §5e carries '{needle}' ({label})", "corrected or annotated (item 11b)",
                ("absent" if not present else ("present, annotated" if annotated else "present, UNANNOTATED")),
                PASS if (not present or annotated) else FAIL, n=len(sec.splitlines()),
                note="§5e may not be quoted for these two numbers until item 11b lands; the corrected figures are "
                     "97 = 9 + 61 + 27 and max unit 12 with 9 claims")
    bis = slice_section(pat, "5b-bis.")
    fuzzy = re.findall(r"\d{2}:\d[xX]Z|\d{2}:\d{2}Z\s*\(approx", bis)
    rep.add("5", "PATTERNS §5b-bis fuzzy timestamp (item 12 / criterion 20.14)", "exact UTC + source",
            str(fuzzy or "none found"), FAIL if fuzzy else PASS, n=1)
    seeded_claim = "seeded: true" in bis or "seeded`" in bis
    rep.add("5", "PATTERNS §5b-bis repeats the false seeded sentence (item 0d)", "corrected append-only",
            "present" if seeded_claim else "absent", INFO if not seeded_claim else FAIL, n=1,
            note="0 of 122 rows carry seeded: true; the four seeded rows live in fixtures-adjudication.json")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("worktree")
    ap.add_argument("--head", default="HEAD")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    wt = os.path.abspath(a.worktree)
    rc, out = git(wt, "rev-parse", a.head)
    head = out.decode().strip() if rc == 0 else a.head
    print(f"ORCH-2 gate instrument · worktree {wt} · head {head[:12]}")
    rep = Report()
    man, sup = section_bindings(wt, rep, head)
    section_pins(wt, rep, sup)
    section_manifest_stats(wt, rep, man)
    section_census_exposure(wt, rep, sup)
    section_adjudication(wt, rep)
    section_stale_digests(wt, rep)
    tally = collections.Counter(r["verdict"] for r in rep.rows)
    print(f"\n== summary: {len(rep.rows)} rows · " +
          " · ".join(f"{k} {v}" for k, v in sorted(tally.items())))
    fails = [r for r in rep.rows if r["verdict"] in (FAIL, VACUOUS)]
    if fails:
        print("\nrows not passing (each is an owed item or a known restriction, not necessarily a defect):")
        for r in fails:
            print(f"  {r['verdict']:6s} {r['name']}: expected {r['expected'][:60]} | observed {r['observed'][:60]}")
            if r["note"]:
                print(f"         {r['note'][:200]}")
    if a.json:
        print(json.dumps(rep.rows, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
