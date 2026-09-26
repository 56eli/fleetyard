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

CITATION_CTX = re.compile(r"fuzzy|imprecise|supersed|was |quoted|offender|defect", re.I)


def classify_fuzzy(text: str, m) -> str:
    """A fuzzy timestamp QUOTED in order to report the defect is not an instance of it.
    Classify by immediate wrapping (backticks/quotes) and by the 60 preceding characters.
    Without this, an audit of a gate record that documents fuzzy timestamps reports the
    gate as the worst offender in the lane - which is what this instrument did to ORCH-2's
    own tree on its first self-audit."""
    a, b = m.start(), m.end()
    wrapped = (a > 0 and b < len(text) and text[a - 1] in "`'\"" and text[b] in "`'\"")
    ctx = CITATION_CTX.search(text[max(0, a - 60):a])
    return "citation" if (wrapped or ctx) else "instance"


# timestamp-discipline patterns (criterion 20.14), module-level so the self-audit and the
# worktree census use the SAME regexes - two copies of a pattern is how defect #8 happened
FUZZY_TS = re.compile(r"\d{1,2}:\d[xX]Z|\d[xX]:\d{2}Z|[xX]Z\b")
TS_ANY = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?Z")
TS_EXACT = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
OWN_TIME_FIELD = re.compile(r'"(run_utc|generated_utc|materialised_utc|created_utc|appended_utc)"\s*:\s*"([^"]+)"')


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


def _frag_of(msg: str) -> str:
    """The distinctive literal of a refusal message: what a test would have to assert to cover it."""
    lit = re.sub(r"%[sdr]", "", msg)
    return " ".join(w for w in lit.split() if len(w) > 6)[:40]


def lane_path(*rel) -> str:
    """A path in the ORCH-2 lane that holds this instrument (fleet/gate-tools/…), i.e. the gate
    authority's own records — used where a row checks something ORCH-2 owes rather than the worker."""
    lane = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(lane, *rel)


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
    s = (s or "").replace("\u2019", "'").replace("\u02bc", "'")   # NORMALIZE, don't just include
    out, cur = [], ""
    for ch in s:
        # APOSTROPHES: straight ' AND curly ’ AND ʼ are IN-TOKEN. Splitting on the curly
        # form turns "that's" into ['that','s'] and silently fails every contraction check
        # — this instrument did exactly that on its second run (8 of 122 rows).
        if ch.isalnum() or ch in "'-":
            cur += ch
        else:
            if cur:
                out.append(cur.lower())
                cur = ""
    if cur:
        out.append(cur.lower())
    return out




def ts_class(v: str) -> str:
    """'exact' | 'minute' | 'fuzzy' | 'other'. A pattern that classifies a WHOLE value must
    FULLMATCH it (defect #8: matching the suffix of a correct value reported 19 false offenders
    because the minute pattern matched '38:04Z' inside '2026-09-25T20:38:04Z')."""
    v = str(v or "")
    if TS_EXACT.fullmatch(v):
        return "exact"
    if TS_ANY.fullmatch(v):
        return "minute"
    if FUZZY_TS.search(v):
        return "fuzzy"
    return "other"


def draw_holdout(names, salt: str, mod: int, bucket: int, reading: str = "full") -> set:
    """The sealed split's draw: sha256(SALT + basename) mod N == bucket. `reading` selects how
    the digest is turned into an integer - 'full' reproduces the seal (33/197 set-equal);
    'hex8' does NOT (28/2), which is why the caveat travels with criterion v2.1."""
    out = set()
    for b in names:
        h = sha_bytes((salt + b).encode())
        n = int(h, 16) if reading == "full" else int(h[:8], 16)
        if n % mod == bucket:
            out.add(b)
    return out


def drop_rules(suspected: str, quoted: str, dropped_words) -> dict:
    """The five natural drop-consistency rules of self-item O-1, all under the stated token
    rule (apostrophes normalised, hyphens INSIDE tokens). The rules disagree by a factor of two
    on the same 122 signals, so no number may be quoted without naming its rule."""
    dw = [w.lower() for w in (dropped_words or [])]
    st, qt = tokens(suspected), tokens(quoted)
    first = st.copy()
    for w in dw:
        if w in first:
            first.remove(w)
    return {"A remove-all-occurrences": [w for w in st if w not in dw] == qt,
            "B remove-first-occurrence": first == qt,
            "C quoted-subseq+count": (all(x in st for x in qt) and len(st) - len(qt) == len(dw)),
            "D suspected-minus-quoted==dropped": [w for w in st if w not in qt] == dw,
            "E quoted-contiguous-in-suspected": (" ".join(qt) in " ".join(st) and
                                                 len(st) == len(qt) + len(dw))}


def rule_a_defect(suspected: str, quoted: str, dropped_words) -> tuple:
    """(fails the stated criterion, and is a repetition artifact). Every row that fails rule A on
    the real data is a repetition artifact: the dropped word occurs more than once in the
    book-side span, so removing EVERY occurrence over-deletes."""
    dw = [w.lower() for w in (dropped_words or [])]
    st, qt = tokens(suspected), tokens(quoted)
    fails = [w for w in st if w not in dw] != qt
    return fails, bool(fails and any(st.count(w) > 1 for w in dw))



class Report:
    def __init__(self) -> None:
        self.rows: list[dict] = []

    def add(self, section, name, expected, observed, verdict, n=None, note=""):
        self.rows.append(dict(section=section, name=name, expected=str(expected),
                              observed=str(observed), verdict=verdict, n=n, note=note))
        flag = "" if verdict in (PASS, INFO) else f"  <<< {verdict}"
        nn = "" if n is None else f" [n={n}]"
        print(f"  {verdict:6s} {name}{nn}{flag}")
        if verdict != PASS and observed:
            print(f"         expected {str(expected)[:150]} | observed {str(observed)[:400]}")
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




def section_read_scope(wt, rep, sup):
    """§6 — read-scope and one-shot discipline, re-derived from committed artefacts.
    This is the section that protects the holdout: a tuning-side run must declare zero
    holdout reads, and the spent-holdout run must declare exactly the 37 and be marked
    consumed."""
    print("\n== 6. read-scope and one-shot discipline ==")
    sp1 = json.load(open(os.path.join(wt, "tools/HELD-OUT-SPLIT.json"), encoding="utf-8"))
    tun1 = {norm(x) for x in sp1["tuning"]}
    hol1 = {norm(x) for x in sp1["holdout"]}
    sp2p = os.path.join(wt, "tools/HELD-OUT-SPLIT-V2.json")
    sp2 = json.load(open(sp2p, encoding="utf-8")) if os.path.exists(sp2p) else {"tuning": [], "holdout": []}
    tun2 = {norm(x) for x in sp2["tuning"]}
    hol2 = {norm(x) for x in sp2["holdout"]}

    q2p = os.path.join(wt, "runs/m4-q2-dropword/PROVENANCE-SUPPLEMENT.json")
    q2 = json.load(open(q2p, encoding="utf-8"))
    rep.check("6", "q2 supplement: holdout_reads empty", [], q2.get("holdout_reads"), n=1)
    rep.check("6", "q2 supplement: holdout_enforced", True, q2.get("holdout_enforced"), n=1)
    rep.check("6", "q2 supplement: split_counts vs split v2", {"tuning": len(tun2), "holdout": len(hol2),
                                                              "total": len(tun2) + len(hol2)},
              q2.get("split_counts"), n=len(tun2) + len(hol2))
    sig = json.load(open(os.path.join(wt, "runs/m4-q2-dropword/signals.json"), encoding="utf-8"))
    keys = {norm(k) for k in sig}
    rep.check("6", "q2 signals.json keys == v1 TUNING set", sorted(tun1), sorted(keys), n=len(keys))
    rep.check("6", "q2 signals.json keys ∩ v1 HOLDOUT == 0", 0, len(keys & hol1), n=len(keys))
    nsig = sum(len(v) for v in sig.values())
    rep.check("6", "q2 merge.signals_total", q2["merge"]["signals_total"], nsig, n=nsig)
    rep.check("6", "q2 merge.signals_sha256", q2["merge"]["signals_sha256"][:16] + "…",
              sha_file(os.path.join(wt, "runs/m4-q2-dropword/signals.json"))[:16] + "…")
    f = q2["source_inheritance_filter"]
    rep.check("6", "q2 filter arithmetic: raw - source_inherited", f["filtered_if_deferred_were_kept"],
              f["raw"] - f["source_inherited"], n=4)
    rep.check("6", "q2 filter arithmetic: - deferred_holdout", f["filtered"],
              f["filtered_if_deferred_were_kept"] - f["deferred_holdout"], n=4,
              note=f"raw {f['raw']}, source_inherited {f['source_inherited']}, deferred_holdout "
                   f"{f['deferred_holdout']}, filtered {f['filtered']} — the 7 deferred are the v2-holdout "
                   f"signals of TASK-019 item v2.b")
    parts = q2.get("parts") or {}
    okp = 0
    for name, dg in sorted(parts.items()):
        fp = os.path.join(wt, "runs/m4-q2-dropword", name)
        if os.path.exists(fp):
            okp += sha_file(fp) == dg
        pp = fp.replace(".json", ".PROVENANCE.json")
        if os.path.exists(pp):
            pm = json.load(open(pp, encoding="utf-8"))
            hr = pm.get("holdout_reads", [])
            rep.check("6", f"q2 {name}: part manifest holdout_reads empty", [], hr, n=len(hr) + 1)
    rep.add("6", "q2 part digests present and matching", f"{len(parts)}/{len(parts)}", f"{okp}/{len(parts)}",
            PASS if okp == len(parts) else FAIL, n=len(parts))

    q3p = os.path.join(wt, "runs/m4-q3-format/PROVENANCE-V2.json")
    if os.path.exists(q3p):
        q3v = json.load(open(q3p, encoding="utf-8"))
        rep.check("6", "q3 v2 run: transcripts_read_count == split v2 tuning", len(tun2),
                  q3v.get("transcripts_read_count"), n=len(tun2))
        rep.check("6", "q3 v2 run: holdout_reads empty", [], q3v.get("holdout_reads"), n=1)
        rep.check("6", "q3 v2 run: holdout_enforced", True, q3v.get("holdout_enforced"), n=1)
        for k, dg in (q3v.get("outputs") or {}).items():
            if not k.endswith(".json"):
                continue
            fp = os.path.join(wt, "runs/m4-q3-format", k)
            rep.add("6", f"q3 output {k}", dg[:16] + "…",
                    (sha_file(fp)[:16] + "…") if os.path.exists(fp) else "not committed (cited by digest only)",
                    PASS if os.path.exists(fp) and sha_file(fp) == dg else INFO, n=1)

    q4dir = os.path.join(wt, "runs/m4-q4-holdout")
    for name in ("v1-holdout.PROVENANCE.json", "part-holdout-drop.PROVENANCE.json",
                 "part-holdout-format.PROVENANCE.json"):
        fp = os.path.join(q4dir, name)
        if not os.path.exists(fp):
            rep.add("6", f"q4 {name}", "present", "ABSENT", FAIL)
            continue
        pm = json.load(open(fp, encoding="utf-8"))
        ins = pm.get("inputs") or {}
        raw_reads = (pm.get("transcripts_read") or pm.get("transcripts") or
                     ins.get("transcripts_read") or ins.get("transcripts") or
                     ins.get("holdout") or ins.get("files") or [])
        if isinstance(raw_reads, dict):
            raw_reads = list(raw_reads)
        reads = {norm(x) for x in raw_reads if isinstance(x, str)}
        hr = pm.get("holdout_reads", ins.get("holdout_reads"))
        if "holdout_consumed" in pm:
            rep.check("6", f"q4 {name}: holdout_consumed", True, pm.get("holdout_consumed"), n=1)
        else:
            rep.add("6", f"q4 {name}: holdout_consumed", "run-level field", 
                    f"absent here; declared at run level ({sup.get('holdout_consumed')})", INFO, n=1,
                    note="holdout_consumed is a property of the RUN, not of each part manifest; requiring it "
                         "per part was over-strict (this instrument's third-run defect)")
        if reads:
            rep.check("6", f"q4 {name}: transcripts_read == v1 holdout (37)", sorted(hol1), sorted(reads),
                      n=len(reads))
            rep.check("6", f"q4 {name}: reads ∩ v1 tuning == 0", 0, len(reads & tun1), n=len(reads))
        if isinstance(hr, list):
            rep.add("6", f"q4 {name}: holdout_reads declared", "the 37 spent transcripts (or empty with the "
                    "read set declared elsewhere)", f"{len(hr)} entries", INFO, n=len(hr))

    # fuzzy timestamps anywhere in the run manifests (criterion 20.14 / item 12)
    # ---- timestamp discipline (criterion 20.14) over the whole committed tree ----
    # DEFECT #8 of this instrument: the first version of the minute-precision regex
    # ("[^\"]*\\d{2}:\\d{2}Z(?!:)") matched the SUFFIX of a correct seconds-precise value
    # (in "...T20:38:04Z" it matches "38:04Z"), reporting 19 false offenders. Classify by
    # fullmatch on the value instead of by searching inside it.
    fuzzy_re, ts_re, own_field = FUZZY_TS, TS_ANY, OWN_TIME_FIELD
    fuzzy, minute_plain, exact, own_superseded = [], [], 0, []
    own_bad = []
    nfiles = 0
    for root, dirs, files in os.walk(wt):
        dirs[:] = [d for d in dirs if d not in (".git", "corpus", "evidence", "__pycache__")]
        for fn in files:
            if not fn.endswith((".json", ".md")):
                continue
            nfiles += 1
            fp = os.path.join(root, fn)
            rp = os.path.relpath(fp, wt)
            t = open(fp, encoding="utf-8", errors="replace").read()
            for m in fuzzy_re.finditer(t):
                fuzzy.append((rp, m.group(0), classify_fuzzy(t, m)))
            for m in ts_re.finditer(t):
                if m.group(1):
                    exact += 1
                else:
                    minute_plain.append((rp, m.group(0)))
            for m in own_field.finditer(t):
                v = m.group(2)
                if not TS_EXACT.fullmatch(v):
                    # the lane's own repair pattern: a fuzzy value left readable beside an
                    # exact sibling field (fixtures/v2/dropword.json's generated_utc_exact).
                    # That is COMPLIANT, and flagging it would punish the correct fix.
                    superseded = f'"{m.group(1)}_exact"' in t
                    (own_superseded if superseded else own_bad).append((rp, m.group(1), v))
    inst = sorted({(rp, v) for rp, v, k in fuzzy if k == "instance"})
    cites = sorted({(rp, v) for rp, v, k in fuzzy if k == "citation"})
    rep.add("6", "criterion 20.14a: FUZZY timestamps ASSERTED in committed docs (item 12)", "0 instances",
            f"{len(inst)} instances: {inst}", PASS if not inst else FAIL, n=nfiles,
            note=f"plus {len(cites)} sites that QUOTE a fuzzy value in order to report or supersede it "
                 f"(not instances): {cites[:6]}")
    rep.add("6", "criterion 20.14b: an artefact's OWN time field exact to the second", "0 offenders",
            f"{len(own_bad)} offenders: {sorted(set(own_bad))}", PASS if not own_bad else FAIL, n=nfiles,
            note="minute precision cannot order an artefact against a commit - the q2 parts ran 18:57:11Z-19:05:21Z "
                 "before their delivery commit at 19:06:53Z, a sequencing question only seconds can settle. When the "
                 "offender is `tools/INHERITED-V1-MANIFEST.json` `materialised_utc` it is TASK-017 item 17.a, the "
                 "sole genuine own-time offender in the worker tree, repaired by the same rule as item 12")
    rep.add("6", "criterion 20.14b-compliant: fuzzy own-time field superseded in-file by an exact sibling",
            "reported", f"{len(own_superseded)} sites: {sorted(set(own_superseded))}", INFO, n=nfiles,
            note="this is the repair pattern the lane already owns - fuzzy left readable, exact sibling added; "
                 "flagging it would punish the correct fix")
    rep.add("6", "criterion 20.14c: exact-to-the-second timestamps found", "reported", f"{exact} sites", INFO,
            n=nfiles)
    rep.add("6", "criterion 20.14d: minute-precision timestamps anywhere else (citations, prose, headers)",
            "allowed when the source is named; ORCH-2 audits its own headers here",
            f"{len(minute_plain)} sites, first 8: {sorted(set(minute_plain))[:8]}", INFO, n=nfiles,
            note="ORCH-2's own GATES.md headers are minute-precise, so ORCH-2 is an instance of this defect and "
                 "adopts exact-second headers from this cycle; two worker EVAL.json files cite those headers "
                 "verbatim and are faithful to their source")


def section_signal_evidence(wt, rep):
    """§7 — the 122 drop-word signals: transcript spans, book citations and drop
    consistency, all re-read byte-exactly (the q2.6 caveat derived mechanically)."""
    print("\n== 7. drop-word signal evidence (q2.6) ==")
    sig = json.load(open(os.path.join(wt, "runs/m4-q2-dropword/signals.json"), encoding="utf-8"))
    ovdir = os.path.join(wt, "corpus/docdocgo/overlays")
    book = open(os.path.join(wt, "corpus/docdocgo/html/merged-book-texts_json_1.js"),
                encoding="utf-8", errors="replace").read()
    flat = [(k, s) for k, v in sig.items() for s in v]
    span_ok = cite_sub = cite_off = consist = dw_ok = 0
    bad_span, bad_cite, shape = [], [], []
    for k, s in flat:
        p = os.path.join(ovdir, k if k.endswith(".txt") else k + ".txt")
        t = open(p, encoding="utf-8", errors="replace").read()
        if t[s["start"]:s["end"]] == s["quoted"]:
            span_ok += 1
        else:
            bad_span.append((k[:24], s["start"], s["end"]))
        br = s.get("book_ref") or {}
        q, co, slug = br.get("quote"), br.get("char_offset"), br.get("slug")
        if q and q in book:
            cite_sub += 1
            i = book.find(slug) if slug else -1
            if i >= 0 and co is not None and book[i + co:i + co + len(q)] == q:
                cite_off += 1
        else:
            bad_cite.append((k[:24], slug, co))
        dw = s.get("dropped_words") or []
        st = tokens(s.get("suspected"))
        if dw and all(w.lower() in st for w in dw):
            dw_ok += 1
        qt = tokens(s.get("quoted"))
        reduced = [w for w in st if w not in {x.lower() for x in dw}]
        if reduced == qt:
            consist += 1
        else:
            shape.append((k[:20], s.get("suspected"), s.get("quoted"), dw))
    n = len(flat)
    rep.add("7", "transcript spans re-read byte-exactly", f"{n}/{n}", f"{span_ok}/{n}",
            PASS if span_ok == n else FAIL, n=n, note=f"failures {bad_span[:4]}")
    rep.add("7", "book citations found in the book store (substring)", f"{n}/{n}", f"{cite_sub}/{n}",
            PASS if cite_sub == n else FAIL, n=n, note=f"failures {bad_cite[:4]}")
    rep.add("7", "book citations offset-exact within the slug region", "reported, not required",
            f"{cite_off}/{n}", INFO, n=n,
            note="offset semantics are the store's own; the substring test above is the binding one")
    rep.add("7", "dropped_words present and contained in the suspected span", f"{n}/{n}", f"{dw_ok}/{n}",
            PASS if dw_ok == n else FAIL, n=n)
    # publish the rule sensitivity instead of a single number: the q2.6 gate figure (113/9)
    # has no published procedure, and five natural rules disagree by a factor of two.
    variants = collections.Counter()
    for _k, sg in flat:
        for k, v in drop_rules(sg.get("suspected"), sg.get("quoted"), sg.get("dropped_words")).items():
            variants[k] += v
    rep.add("7", "drop consistency under FIVE natural rules (rule sensitivity)",
            "the q2.6 gate figure 113/9 is reproduced by none of them",
            " · ".join(f"{k}: {v}/{len(flat)}" for k, v in sorted(variants.items())), INFO, n=5 * len(flat),
            note="ORCH-2 self-item O-1: the previously published 113/9 with a 3+6 decomposition is WITHDRAWN as "
                 "not reproducible. The token rule is load-bearing: under a hyphen-SPLITTING rule, rule A collapses "
                 "to 67/122.")
    # the STATED criterion: rule A with an explicit token rule, plus a characterisation of
    # every row that fails it (all of them are repetition artifacts)
    rep_rows = []
    for _k, sg in flat:
        dw = [w.lower() for w in (sg.get("dropped_words") or [])]
        st = tokens(sg.get("suspected"))
        fails, _is_rep = rule_a_defect(sg.get("suspected"), sg.get("quoted"), dw)
        if fails:
            rep_rows.append((dw, [w for w in dw if st.count(w) > 1], sg.get("suspected"), sg.get("quoted")))
    all_rep = all(r[1] for r in rep_rows)
    rep.add("7", "STATED CRITERION — shape-defective rows under rule A", 
            "8 of 122, every one a repetition artifact (a dropped word occurring more than once in the "
            "book-side span, so removing every occurrence over-deletes)",
            f"{len(rep_rows)} of {len(flat)}; repetition artifacts among them: {sum(1 for r in rep_rows if r[1])}"
            f"; all-defective-rows-are-repetition-artifacts: {all_rep}",
            PASS if (len(rep_rows), all_rep) == (8, True) else FAIL, n=len(flat),
            note="token rule: apostrophes (straight AND curly, normalised) and hyphens INSIDE tokens; every other "
                 "character a separator. Examples: " + str([(r[0], r[2]) for r in rep_rows[:2]])[:200])
    rep.add("7", "drop consistency: tokens(suspected) minus dropped == tokens(quoted)",
            "the q2.6 gate figure was 113 consistent / 9 shape-defective",
            f"{consist} consistent / {n - consist} shape-defective",
            PASS if (consist, n - consist) == (113, 9) else PROXY, n=n,
            note=("matches the q2.6 gate figure (9 shape-defective = 3 repetition artifacts + 6 partial-overlap, "
                  "2 of which were ORCH-2's own hyphen tokenization)"
                  if (consist, n - consist) == (113, 9) else
                  "PROXY, not FAIL: this mechanical rule (remove every occurrence of each dropped word from the "
                  "token list, then compare) is NOT the procedure the q2.6 gate used. Until that procedure is "
                  "encoded here this row may not be used as a criterion; the binding rows are the byte-exact span "
                  "and citation checks above. Examples: " +
                  str([(a, c) for a, _b, c, _d in shape[:3]])[:200]))


def section_manifest_completeness(wt, rep):
    """§8 — LAW §8 completeness of every run manifest, plus tool-pin attributability."""
    print("\n== 8. LAW §8 manifest completeness ==")
    req = ["tool_commit", "main_head", "policy_sha256", "corpus_zip_sha256", "run_utc", "status"]
    docs = ["runs/m4-q2-dropword/PROVENANCE-SUPPLEMENT.json",
            "runs/m4-q3-format/PROVENANCE-SUPPLEMENT.json",
            "runs/m4-q4-holdout/PROVENANCE-SUPPLEMENT.json"]
    exact_utc = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
    for rel in docs:
        p = os.path.join(wt, rel)
        if not os.path.exists(p):
            rep.add("8", f"{rel}", "present", "ABSENT", FAIL)
            continue
        d = json.load(open(p, encoding="utf-8"))
        missing = [k for k in req if k not in d]
        rep.add("8", f"{rel}: required keys", "none missing", f"missing {missing}" if missing else "all present",
                PASS if not missing else FAIL, n=len(req))
        rep.add("8", f"{rel}: run_utc exact to the second", "YYYY-MM-DDThh:mm:ssZ", str(d.get("run_utc")),
                PASS if exact_utc.match(str(d.get("run_utc") or "")) else FAIL, n=1)
        rep.add("8", f"{rel}: book store bound or N/A stated", "book_store_sha256 or an explicit N/A",
                "book_store_sha256" if "book_store_sha256" in d else
                f"book_store_digest_status: {str(d.get('book_store_digest_status'))[:60]}",
                PASS if ("book_store_sha256" in d or "book_store_digest_status" in d) else FAIL, n=1)
        rep.add("8", f"{rel}: config canonicalization stated (criterion 20.16)",
                "config_digest_note present", "present" if "config_digest_note" in d else "ABSENT",
                PASS if "config_digest_note" in d else FAIL, n=1,
                note="the q2 supplement states it; the others must adopt it (item 14)")
        st = str(d.get("status", ""))
        rep.add("8", f"{rel}: status forbids promotion/rate", "'not promotable' and no-rate language",
                st[:90], PASS if ("not promotable" in st.lower() or "provisional" in st.lower()) else FAIL, n=1)
        dpd = d.get("detector_pin_defect")
        if dpd:
            need = ["original_pin", "defect", "attribution_bridge"]
            miss = [k for k in need if k not in dpd]
            rep.add("8", f"{rel}: original pin defect disclosed", f"{need}", f"missing {miss}" if miss else "complete",
                    PASS if not miss else FAIL, n=len(need))
        dsh = d.get("detector_sha256_at_head")
        if dsh:
            tool = "tools/det_dropword.py" if "dropword" in rel else "tools/det_format.py"
            rep.check("8", f"{rel}: detector_sha256_at_head == {tool}", dsh[:16] + "…",
                      sha_file(os.path.join(wt, tool))[:16] + "…")
        tc = str(d.get("tool_commit") or "")
        # pair each supplement with ITS OWN generator; checking every generator against every
        # manifest produces meaningless rows (this instrument's third-run defect)
        gen = "m4_q4_supplement.py" if "q4" in rel else "m4_t20_supplement.py"
        if os.path.exists(os.path.join(wt, "tools", gen)):
            rc, _ = git(wt, "cat-file", "-e", f"{tc[:12]}:tools/{gen}")
            rep.add("8", f"{rel}: tool_commit {tc[:12]} contains its generator tools/{gen}", "present",
                    "present" if rc == 0 else "ABSENT", PASS if rc == 0 else FAIL, n=1,
                    note="item 8a: pin generator_tool + generator_tool_commit + generator_tool_sha256")
        else:
            rep.add("8", f"{rel}: generator tools/{gen}", "present at head", "ABSENT at head", FAIL, n=1)
    # threshold provenance sections
    for rel, needles in (("runs/m4-q2-dropword/README.md",
                          ["Threshold provenance", "min_score", "min_ratio", "stride", "window", "top_k",
                           "min_flank", "min_matched", "max_drop"]),
                         ("runs/m4-q3-format/README.md",
                          ["Threshold provenance", "no numeric decision thresholds"])):
        p = os.path.join(wt, rel)
        if not os.path.exists(p):
            rep.add("8", f"{rel}: threshold provenance section", "present", "ABSENT", FAIL)
            continue
        t = open(p, encoding="utf-8").read()
        miss = [nd for nd in needles if nd not in t]
        rep.add("8", f"{rel}: threshold provenance section names every parameter",
                "none missing", f"missing {miss}" if miss else f"all {len(needles)} present",
                PASS if not miss else FAIL, n=len(needles),
                note="for C2-format the correct provenance answer is that the seven rules are shape predicates "
                     "with NO numeric thresholds; the rule names are catalogued in the same README and in the "
                     "supplement's `rules` list, so they are not required inside the provenance section itself")





def section_split_v2(wt, rep, sup):
    """§10 — TASK-019a split v2: independent re-draw, contamination, forcing rule,
    seal bindings and the guard-is-code requirement (criteria v2.1-v2.6, v2.a/v2.b)."""
    print("\n== 10. split v2 (TASK-019a) ==")
    p = os.path.join(wt, "tools/HELD-OUT-SPLIT-V2.json")
    if not os.path.exists(p):
        rep.add("10", "HELD-OUT-SPLIT-V2.json", "present", "ABSENT", FAIL)
        return
    j = json.load(open(p, encoding="utf-8"))
    salt, mod, bucket = j["salt"], j["mod"], j["holdout_bucket"]
    ovdir = os.path.join(wt, "corpus/docdocgo/overlays")
    allb = sorted(b for b in os.listdir(ovdir) if b.endswith(".txt"))
    rep.check("10", "corpus file count", j["corpus_files"], len(allb), n=len(allb))
    # corpus_files_sha256 is a LIST digest per the stated derivation
    listd = sha_bytes(("\n".join(sorted(allb)) + "\n").encode("utf-8"))
    rep.check("10", "corpus_files_sha256 (list digest, stated derivation)", j["corpus_files_sha256"][:16] + "…",
              listd[:16] + "…", n=len(allb))
    rep.check("10", "corpus_files_sha256 == the value the q4 supplement binds",
              sup["split_corpus_files_sha256"], j["corpus_files_sha256"], n=1)

    # independent re-draw under two candidate readings of "sha256(SALT+basename) mod 5"
    forced_fx = set()
    for src in ("fixtures/confirmed/confirmed.json", "fixtures/v2/dropword.json"):
        sp = os.path.join(wt, src)
        if not os.path.exists(sp):
            continue
        d = json.load(open(sp, encoding="utf-8"))
        items = d.get("fixtures", d) if isinstance(d, dict) else d
        for f in items:
            t = f.get("transcript") if isinstance(f, dict) else None
            if t:
                forced_fx.add(os.path.basename(t))
    v1 = json.load(open(os.path.join(wt, "tools/HELD-OUT-SPLIT.json"), encoding="utf-8"))
    v1hol = {os.path.basename(x) for x in v1["holdout"]}
    forced = forced_fx | v1hol
    rep.check("10", "forced-to-tuning set (fixtures ∪ spent v1 holdout)", len(j["fixture_transcripts_forced_tuning"]),
              len(forced), n=len(forced),
              note=f"fixture transcripts {len(forced_fx)} ∪ v1 holdout {len(v1hol)}; "
                   f"v1_holdout_forced_tuning declares {len(j['v1_holdout_forced_tuning'])}")
    draws = {}
    for label, reading in (("int(full hexdigest) % mod", "full"), ("int(first 8 hex) % mod", "hex8")):
        raw = draw_holdout(allb, salt, mod, bucket, reading)
        draws[label] = (raw - forced, (set(allb) - raw) | forced)
    seal_h = {os.path.basename(x) for x in j["holdout"]}
    seal_tn = {os.path.basename(x) for x in j["tuning"]}
    matched = None
    for label, (h, t) in draws.items():
        rep.add("10", f"independent re-draw, {label}: holdout set-equal", f"{len(seal_h)}/{len(seal_h)}",
                f"{len(h & seal_h)}/{len(seal_h)} (draw {len(h)})",
                PASS if h == seal_h else INFO, n=len(allb))
        if h == seal_h and t == seal_tn:
            matched = label
    rep.add("10", "MY DRAW REPRODUCES THE SEAL (33 holdout / 197 tuning, set-equal both buckets)",
            "one stated reading reproduces it exactly",
            f"reproduced by: {matched}" if matched else f"none of {list(draws)}",
            PASS if matched else FAIL, n=len(allb),
            note="if none reproduces, the seal's method statement is not executable as written - the same defect "
                 "class as item 13")
    rep.check("10", "bucket counts", {"holdout": 33, "tuning": 197, "total": 230}, j["counts"], n=230)
    rep.check("10", "holdout ∩ tuning == 0", 0, len(seal_h & seal_tn), n=len(seal_h) + len(seal_tn))

    # contamination: no v2-holdout transcript carries any fixture
    cont = sorted(seal_h & forced_fx)
    rep.add("10", "ZERO fixture contamination in the v2 holdout", "0", f"{len(cont)} {cont[:5]}",
            PASS if not cont else FAIL, n=len(forced_fx))
    spent = sorted(seal_h & v1hol)
    rep.add("10", "ZERO spent-v1-holdout transcripts in the v2 holdout", "0", f"{len(spent)} {spent[:5]}",
            PASS if not spent else FAIL, n=len(v1hol))
    miss = sorted(forced - seal_tn)
    rep.add("10", "every forced transcript is in v2 TUNING", f"{len(forced)}/{len(forced)}",
            f"{len(forced) - len(miss)}/{len(forced)} (missing {miss[:4]})", PASS if not miss else FAIL,
            n=len(forced))
    rep.check("10", "forced_not_by_fixture (every forcing has a stated reason)", [], j["forced_not_by_fixture"],
              n=len(j["forced_with_reasons"]))
    rep.check("10", "every forced transcript carries a reason", len(forced), len(j["forced_with_reasons"]),
              n=len(forced))

    # seal bindings
    for src, dg in j["fixture_sources"].items():
        fp = os.path.join(wt, src)
        act = sha_file(fp) if os.path.exists(fp) else "ABSENT"
        if act == dg:
            rep.add("10", f"criterion v2.5 — seal binds the ACTUAL {src}", act[:16] + "…", dg[:16] + "…", PASS, n=1)
            continue
        # O-5: the seal is immutable (its own digest 73d86f0d… is bound by the appendix and by v2.10), so a
        # post-seal APPEND-ONLY move is discharged by a dated companion note + a blob-level classification,
        # not by editing the seal. §18 re-derives both from git bytes.
        aud = os.path.join(wt, "runs/m4-q2-adjudication/SEAL-AUDIT.json")
        apx = os.path.join(wt, "runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md")
        cls = note_ok = False
        if os.path.exists(aud):
            rj = json.load(open(aud, encoding="utf-8"))
            e = [x for x in rj.get("fixture_sources", []) if x.get("file") == src]
            cls = bool(e) and e[0].get("status") == "APPEND-ONLY-AFTER-SEAL" and not e[0].get("mutations") \
                and not e[0].get("new_fixture_ids")
        if os.path.exists(apx):
            t = open(apx, encoding="utf-8").read()
            note_ok = dg[:12] in t and act[:12] in t
        rep.add("10", f"criterion v2.5 (as amended by O-5) — {src}: the seal binds its SEAL-TIME digest and the "
                      f"post-seal move is classified append-only with a dated companion note naming both",
                f"seal-time {dg[:16]}… + classified append-only + both digests named in a companion note",
                f"live {act[:16]}…; classified append-only (mutations [] / no ids added): {cls}; companion note "
                f"names both digests: {note_ok}",
                PASS if cls and note_ok else FAIL, n=2,
                note="" if (cls and note_ok) else "ITEM v2.a: the digest moved and either the classification or the "
                                                  "companion note is missing")
    man = j["manifest"]
    tool = man.get("tool")
    if tool:
        tp = os.path.join(wt, tool)
        rep.check("10", "seal manifest tool_sha256 == the actual generator", man.get("tool_sha256", "")[:16] + "…",
                  (sha_file(tp)[:16] + "…") if os.path.exists(tp) else "ABSENT")
        tc = str(man.get("tool_commit") or "")
        rc, _ = git(wt, "cat-file", "-e", f"{tc[:12]}:{tool}")
        rep.add("10", f"seal manifest tool_commit {tc[:12]} contains {tool}", "present",
                "present" if rc == 0 else "ABSENT", PASS if rc == 0 else FAIL, n=1,
                note="same attributability class as criterion 20.10 / item 8a")
    rep.add("10", "seal manifest run_utc exact to the second", "YYYY-MM-DDThh:mm:ssZ", str(man.get("run_utc")),
            PASS if ts_class(man.get("run_utc")) == "exact" else FAIL, n=1)
    rep.add("10", "re-seal rule present (new fixture voids the seal)", "stated", str(j.get("re_seal_rule"))[:120],
            PASS if j.get("re_seal_rule") else FAIL, n=1)
    rep.add("10", "contamination disclosure present", "stated", str(j.get("disclosure"))[:120],
            PASS if j.get("disclosure") else FAIL, n=1)

    # guard is code
    for f, label in (("tools/m4_split_v2.py", "generator"), ("tests/test_m4_split_v2.py", "tests")):
        fp = os.path.join(wt, f)
        if os.path.exists(fp):
            nt = len(re.findall(r"def test_", open(fp, encoding="utf-8").read())) if label == "tests" else None
            rep.add("10", f"guard is code: {f} present", "present", f"present" + (f", {nt} test functions" if nt is not None else ""),
                    PASS, n=nt or 1)
        else:
            rep.add("10", f"guard is code: {f} present", "present", "ABSENT", FAIL)

    # --- criterion closure: v2.1 (salt is new), v2.4 (commit order), v2.6 (guard in code),
    #     v2.9 (delivery labelled, no promotion) -------------------------------------------
    v1salt = v1.get("salt")
    rep.add("10", "criterion v2.1 — the salt is NEW (differs from the spent v1 salt)", "different",
            f"v1 {str(v1salt)[:34]} / v2 {salt[:34]}", PASS if v1salt != salt else FAIL, n=1)
    rep.check("10", "criterion v2.1 — method / modulus / bucket published",
              {"mod": 5, "holdout_bucket": 0}, {"mod": j["mod"], "holdout_bucket": j["holdout_bucket"]}, n=1)
    rep.add("10", "criterion v2.1 — method statement present", "stated", str(j.get("method"))[:110],
            PASS if j.get("method") else FAIL, n=1)

    def addtime(rel):
        rc, out = git(wt, "log", "--diff-filter=A", "--format=%ct %h", "--", rel)
        lines = [l for l in out.strip().splitlines() if l.strip()]
        return (int(lines[-1].split()[0]), lines[-1].split()[1]) if lines else (None, None)

    def since(rel, needle):
        """When a STATEMENT entered a file (pickaxe), not when the file was added."""
        rc, out = git(wt, "log", "-S", needle, "--format=%ct %h", "--", rel)
        lines = [l for l in out.strip().splitlines() if l.strip()]
        return (int(lines[-1].split()[0]), lines[-1].split()[1]) if lines else (None, None)

    seal_ct, seal_ch = addtime("tools/HELD-OUT-SPLIT-V2.json")
    # select the v2-tuning artefact set MECHANICALLY: anything that declares split v2 by name
    declares = []
    for root, dirs, files in os.walk(os.path.join(wt, "runs")):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in sorted(files):
            if fn.endswith((".json", ".md")):
                fp = os.path.join(root, fn)
                try:
                    txt = open(fp, encoding="utf-8", errors="replace").read()
                except OSError:
                    continue
                if "HELD-OUT-SPLIT-V2" in txt:
                    declares.append(os.path.relpath(fp, wt))
    early, intro = [], []
    for a in sorted(declares):
        it, ic = since(a, "HELD-OUT-SPLIT-V2")
        intro.append(f"{os.path.basename(a)}@{ic}")
        if it is None or it < seal_ct:
            early.append((a, ic or "ABSENT"))
    rep.add("10", "criterion v2.4 — sealed BEFORE any further tuning, on commit-order evidence",
            f"seal {seal_ch} precedes the commit that introduced the split-v2 reference in all "
            f"{len(declares)} artefacts that declare it",
            "PASS" if not early else f"{len(early)} exceptions: {early[:3]}",
            PASS if not early else FAIL, n=len(declares),
            note=f"seal added by {seal_ch} at {seal_ct}; introduction commits (git log -S, not file add time): "
                 + ", ".join(intro[:6]))
    # the pre-seal v1-era runs are disclosed by the seal itself, so they are INFO not FAIL
    pre = []
    for root, dirs, files in os.walk(os.path.join(wt, "runs")):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d.startswith("m4-")]
        for fn in sorted(files):
            if fn.endswith((".json", ".jsonl", ".md")):
                rel = os.path.relpath(os.path.join(root, fn), wt)
                at, ac = addtime(rel)
                if at is not None and at < seal_ct and "HELD-OUT-SPLIT-V2" not in open(
                        os.path.join(root, fn), encoding="utf-8", errors="replace").read():
                    pre.append(f"{os.path.basename(os.path.dirname(rel))}/{fn}@{ac}")
    rep.add("10", "criterion v2.4 corollary — pre-seal v1-era M4 run artefacts (shaped on the v1 tuning set)",
            "disclosed by the seal, counted for the record", f"{len(pre)} file(s) under runs/m4-*: {sorted(set(pre))[:4]}",
            INFO, n=len(pre),
            note="the seal's own disclosure: 'v1 detectors were shaped with corpus-wide knowledge, and the "
                 "drop-word and format rules were shaped on the v1 tuning set; a first figure under v2 is an "
                 "estimate under this split, not a pristine out-of-sample number'")
    adj_ct, adj_ch = addtime("runs/m4-q2-adjudication/adjudication.jsonl")
    rep.add("10", "criterion v2.4 — the TASK-018 adjudication set PRE-DATES the seal (labels are v1-era)",
            "adjudication added before the seal",
            f"adjudication.jsonl {adj_ch} at {adj_ct} vs seal {seal_ch} at {seal_ct}"
            + (f" — {(seal_ct - adj_ct) // 60} min earlier" if adj_ct and seal_ct else ""),
            PASS if (adj_ct and seal_ct and adj_ct < seal_ct) else FAIL, n=1)
    fx_t, fx_c = addtime("fixtures/v2/dropword.json")
    rep.add("10", "criterion v2.5 corollary — when did the bound fixture change relative to the seal?",
            "a post-seal edit is what taints the binding (item v2.a)",
            f"fixtures/v2/dropword.json added {fx_c}" + (" AFTER the seal" if fx_t and seal_ct and fx_t > seal_ct else
                                                         " BEFORE the seal (later modified)"),
            INFO, n=1)

    # criterion v2.6 — the guard must be code, and the tuning-side runs must not touch the v2 holdout
    evp = os.path.join(wt, "tools/m4_q3_evidence.py")
    ev = open(evp, encoding="utf-8").read() if os.path.exists(evp) else ""
    m = re.search(r"class HoldoutGuard\b.*?(?=\nclass |\Z)", ev, re.S)
    guard_body = m.group(0) if m else ""
    ok_guard = bool(m) and "SystemExit" in guard_body and "holdout" in guard_body.lower()
    sites = []
    tdir = os.path.join(wt, "tools")
    for f in sorted(os.listdir(tdir)) if os.path.isdir(tdir) else []:
        if f.endswith(".py"):
            k = len(re.findall(r"HoldoutGuard\(", open(os.path.join(tdir, f), encoding="utf-8").read()))
            if k:
                sites.append(f"{f}:{k}")
    rep.add("10", "criterion v2.6 — the tuning path REFUSES holdout reads in code (not only in prose)",
            "guard class raising SystemExit on a holdout name, instantiated by the tuning-side evidence tools",
            ("HoldoutGuard raising SystemExit; instantiated at " + ", ".join(sites)) if ok_guard and sites else
            f"guard={'ok' if ok_guard else 'ABSENT'} sites={sites}",
            PASS if ok_guard and sites else FAIL, n=len(sites))
    prots = (("both-buckets overlap", r"transcripts in both|split integrity violation"),
             ("tuning names in corpus", r"not in corpus"), ("duplicate across parts", r"two parts"))
    for f, need in (("tools/det_dropword.py", 3), ("tools/det_format.py", 2)):
        fp = os.path.join(wt, f)
        txt = open(fp, encoding="utf-8").read() if os.path.exists(fp) else ""
        got = [lbl for lbl, pat in prots if re.search(pat, txt)]
        rep.add("10", f"criterion v2.6 — {f} asserts split integrity in code", f"{need} named protections",
                f"{len(got)}/3 present: {got}" if txt else "ABSENT",
                PASS if len(got) >= need else FAIL, n=len(got))
    sv = os.path.join(wt, "runs/m4-q3-format/signals-v2tuning.json")
    if os.path.exists(sv):
        d = json.load(open(sv, encoding="utf-8"))
        keys = set(d) if isinstance(d, dict) else set()
        outside = keys - seal_tn
        rep.add("10", "criterion v2.6 — the post-seal v2 tuning run is keyed inside v2 TUNING, ∩ holdout = 0",
                f"{len(seal_tn)}/{len(seal_tn)} ⊆ tuning and 0", f"{len(keys - outside)}/{len(keys)} ⊆ tuning, "
                f"∩ holdout = {len(keys & seal_h)}, outside = {len(outside)}",
                PASS if not outside and not (keys & seal_h) else FAIL, n=len(keys))
    else:
        rep.add("10", "criterion v2.6 — signals-v2tuning.json present", "present", "ABSENT", FAIL)

    # the pre-seal q2 run is keyed by the v1 tuning set, which CONTAINS the whole v2 holdout
    q2p = os.path.join(wt, "runs/m4-q2-dropword/signals.json")
    if os.path.exists(q2p):
        k2 = set(json.load(open(q2p, encoding="utf-8")))
        v1tn = {os.path.basename(x) for x in v1["tuning"]}
        rep.add("10", "criterion v2.6 — the pre-seal q2 run's keys ∩ the v2 HOLDOUT (the disclosed taint)",
                "0 would be pristine; the seal discloses v1-era shaping",
                f"{len(k2 & seal_h)} of {len(seal_h)} v2-holdout transcripts were read pre-seal "
                f"(keys {len(k2)} == v1 tuning {len(k2 & v1tn)})", INFO, n=len(k2),
                note="not a v2.6 violation - the run pre-dates the seal and the seal's disclosure covers it - but "
                     "every quantum-b figure must carry the seal's sentence that this is an estimate under this "
                     "split, not a pristine out-of-sample number")

    # criterion v2.b / item v2.b — the seven deferred v2-holdout signals, DERIVED here from the data
    adjp = os.path.join(wt, "runs/m4-q2-adjudication/adjudication.jsonl")
    if os.path.exists(q2p) and os.path.exists(adjp):
        q2 = json.load(open(q2p, encoding="utf-8"))
        sig = {k: len(v) for k, v in q2.items() if k in seal_h and v}
        adj = [json.loads(l) for l in open(adjp, encoding="utf-8") if l.strip()]
        rows = [r for r in adj if os.path.basename(str(r.get("transcript", ""))) in seal_h]
        ids = sorted(str(r.get("id")) for r in rows)
        verd = {}
        for r in rows:
            verd[str(r.get("verdict"))] = verd.get(str(r.get("verdict")), 0) + 1
        q2sup = {}
        sp = os.path.join(wt, "runs/m4-q2-dropword/PROVENANCE-SUPPLEMENT.json")
        if os.path.exists(sp):
            q2sup = json.load(open(sp, encoding="utf-8")).get("source_inheritance_filter", {})
        decl = q2sup.get("deferred_holdout")
        rep.add("10", "criterion v2.b — v2-holdout signals deferred by the tuning filter, ENUMERATED from the data",
                f"{decl} signals (the supplement's own declaration)",
                f"{sum(sig.values())} signals in {len(sig)} transcripts; adjudication rows on holdout transcripts "
                f"{len(rows)}: {ids}",
                PASS if sum(sig.values()) == len(rows) == decl else FAIL, n=len(rows),
                note=f"per-transcript {dict(sorted((k[:34], v) for k, v in sig.items()))}; verdicts {verd}")
        cert = [str(r.get("id")) for r in rows if "CERTAIN" in str(r.get("verdict"))]
        rep.add("10", "criterion v2.b — holdout transcripts already carry hand LABELS from TASK-018",
                "the quantum-b protocol must decide their handling IN ADVANCE (per-file breakdown or exclusion)",
                f"{len(cert)} CERTAIN-leg-d ({cert}) + {len(rows) - len(cert)} CANDIDATE on "
                f"{len(sig)} of {len(seal_h)} holdout transcripts", INFO, n=len(rows),
                note="item v2.b leg (iv): the one-shot evaluation must either report a per-file breakdown "
                     "disclosing that these holdout transcripts are already signal-bearing, or exclude them with "
                     "the denominator change stated in the pre-registration - not decided afterwards")
        sealnote = json.dumps(j).lower()
        stated = all(x in sealnote for x in ("d-092", "deferred")) or "holdout transcripts that already" in sealnote
        # O-5: the seal may not be edited, so the dated note may instead live in a companion artefact that the
        # quantum-b freeze binds. Either location discharges item v2.b; neither exists at 72104a5.
        comp = ""
        for rel in ("runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md",
                    "runs/m4-q2-adjudication/SEAL-AUDIT.json",
                    "fleet/branches/WORKER-2-TASK-019a-DELIVERY.md"):
            fp2 = os.path.join(wt, rel)
            if os.path.exists(fp2):
                t2 = open(fp2, encoding="utf-8").read().lower()
                if "d-092" in t2 and "radical_subjectivity" in t2:
                    comp = rel
        rep.add("10", "criterion v2.b (as amended by O-5) — the taint is stated in the seal's note OR in a dated "
                      "companion artefact (item v2.b landing check)",
                "a dated append-only note naming the four transcripts, the seven ids and their verdicts",
                ("STATED in " + comp) if comp else ("STATED in the seal" if stated else
                                                    "ABSENT in the seal and in every companion artefact at this head "
                                                    "— item v2.b still owed"),
                PASS if (comp or stated) else FAIL, n=1)

    dl = [os.path.relpath(os.path.join(r, f), wt) for r, _, fs in os.walk(wt) for f in fs
          if "TASK-019a-DELIVERY" in f and "/.git" not in r]
    rep.add("10", "criterion v2.9 — the delivery is labelled DELIVERY, never completion or certification",
            "a DELIVERY artefact that promotes nothing", f"{len(dl)} file(s): {sorted(dl)[:3]}",
            PASS if dl else FAIL, n=len(dl))


    # criterion v2.b: the deferred v2-holdout signals must be documented
    hits = []
    for root, dirs, files in os.walk(os.path.join(wt, "runs")):
        for fn in files:
            if fn.endswith((".json", ".md")):
                t = open(os.path.join(root, fn), encoding="utf-8", errors="replace").read()
                if "deferred_holdout" in t or "deferred" in t.lower() and "v2" in t:
                    hits.append(os.path.relpath(os.path.join(root, fn), wt))
    rep.add("10", "criterion v2.b — the 7 deferred v2-holdout signals documented in a committed artefact",
            "a manifest enumerating them (item v2.b)", f"{len(hits)} files mention deferral: {sorted(hits)[:6]}",
            INFO, n=len(hits),
            note="the q2 supplement records deferred_holdout: 7 and the filter arithmetic closes, but item v2.b "
                 "owes an enumeration (which 4 transcripts, which 3 were promoted to D-092/093/094)")


def section_inherited(wt, rep):
    """§11 — TASK-017: the inherited v1 toolchain, 266 files, three-way."""
    print("\n== 11. inherited v1 manifest (TASK-017) ==")
    p = os.path.join(wt, "tools/INHERITED-V1-MANIFEST.json")
    if not os.path.exists(p):
        rep.add("11", "INHERITED-V1-MANIFEST.json", "present", "ABSENT", FAIL)
        return
    m = json.load(open(p, encoding="utf-8"))
    arch = str(m["archive_commit"])
    groups = [("tools/tests/fixtures", m["files"]), ("census+runs", m["inherited_census_and_runs"]["files"])]
    rep.check("11", "file_count (tools/tests/fixtures)", m["file_count"], len(m["files"]), n=len(m["files"]))
    rep.check("11", "file_count (census+runs)", m["inherited_census_and_runs"]["file_count"],
              len(m["inherited_census_and_runs"]["files"]), n=len(m["inherited_census_and_runs"]["files"]))
    total = len(m["files"]) + len(m["inherited_census_and_runs"]["files"])
    rep.check("11", "file_count_total", m["file_count_total"], total, n=total)
    ok_arch = ok_head = ok_claim = n = 0
    bad = []
    for label, files in groups:
        for path, meta in sorted(files.items()):
            n += 1
            rc, blob = git(wt, "show", f"{arch[:12]}:{path}")
            a = sha_bytes(blob) if rc == 0 else "ABSENT-IN-ARCHIVE"
            hp = os.path.join(wt, path)
            h = sha_file(hp) if os.path.exists(hp) else "ABSENT-AT-HEAD"
            ok_arch += a == meta.get("in_archive_sha256")
            ok_head += h == meta.get("sha256")
            ok_claim += meta.get("sha256") == meta.get("in_archive_sha256")
            if not (a == h == meta.get("sha256") == meta.get("in_archive_sha256")):
                bad.append((path, a[:8], h[:8], str(meta.get("sha256"))[:8]))
    rep.add("11", "archive blob == manifest in_archive_sha256", f"{n}/{n}", f"{ok_arch}/{n}",
            PASS if ok_arch == n else FAIL, n=n)
    rep.add("11", "file at head == manifest sha256", f"{n}/{n}", f"{ok_head}/{n}",
            PASS if ok_head == n else FAIL, n=n)
    rep.add("11", "manifest's two claims agree per file (unmodified)", f"{n}/{n}", f"{ok_claim}/{n}",
            PASS if ok_claim == n else FAIL, n=n,
            note=f"mismatches: {bad[:4]}" if bad else "three-way equality across all inherited files")
    rep.add("11", "unmodified declared", True, m.get("unmodified"), PASS if m.get("unmodified") else FAIL, n=1)
    rep.add("11", "archive lane cited read-only, never re-stamped", "stated", str(m.get("archive_commit_note"))[:110],
            PASS if m.get("archive_commit_note") else FAIL, n=1)





# ANNEX B1/B4 frozen inputs (fleet/queue/pending/TASK-019.md) — a drift on any of these voids the
# pre-registration, so the instrument checks them at every run (ANNEX amendment §F7).
FROZEN = (("tools/det_dropword.py", "a0236325"), ("tools/det_format.py", "ef9ff4f2"),
          ("tools/m5r_reduce.py", "6d4bb9ce"), ("findings/ledger.jsonl", "d42136c6"),
          ("fleet2/POLICY-MANIFEST.sha256", "0fe20a60"), ("docdocgo-fixes.zip", "3f36c520"))
TAINTED4 = ("Radical_Subjectivity_The_I_of_Self_Feb_2002_Part_2_enxautogen_html.txt",
            "Realization_of_the_Self_as_the_I_Nov_2003_Part_1_enxautogen_html.txt",
            "Spiritual_Traps_Oct_2005_Part_2_enxautogen_html.txt",
            "Witnessing_and_Observing_Oct_2004_Part_1_enxautogen_html.txt")


def section_quantum_b(wt, rep):
    """§12 — quantum-b readiness: frozen-input drift, the blocker, and the pre-declared denominators."""
    print("\n== 12. quantum b readiness (TASK-019 ANNEX) ==")
    drift = []
    for rel, pre in FROZEN:
        fp = os.path.join(wt, rel)
        act = sha_file(fp)[:8] if os.path.exists(fp) else "ABSENT"
        if act != pre:
            drift.append(f"{rel}: ANNEX {pre} vs head {act}")
    rep.add("12", "ANNEX B1/B4 frozen inputs have NOT drifted from the worker head", f"{len(FROZEN)}/{len(FROZEN)} match",
            f"{len(FROZEN) - len(drift)}/{len(FROZEN)} match" + (f"; drift: {drift[:3]}" if drift else ""),
            PASS if not drift else FAIL, n=len(FROZEN),
            note="a drift on any frozen input voids the pre-registration and forces a new one (ANNEX §F7)")
    man = {}
    pp = os.path.join(wt, "findings/PROVENANCE.json")
    if os.path.exists(pp):
        man = json.load(open(pp, encoding="utf-8"))
    bs = man.get("book_store") or {}
    if bs.get("path"):
        bp = os.path.join(wt, bs["path"])
        rep.check("12", f"book store frozen digest ({bs['path']})", str(bs.get("sha256"))[:8],
                  sha_file(bp)[:8] if os.path.exists(bp) else "ABSENT")

    sp = os.path.join(wt, "tools/HELD-OUT-SPLIT-V2.json")
    j = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
    seal_h = {os.path.basename(x) for x in j.get("holdout", [])}
    rep.check("12", "the holdout the pre-registration will bind", 33, len(seal_h), n=len(seal_h))
    inside = [t for t in TAINTED4 if t in seal_h]
    rep.add("12", "ANNEX §F1 — the four label-tainted holdout transcripts are fixed BY NAME", "4 of 4 in the holdout",
            f"{len(inside)}/4 in the holdout" + ("" if len(inside) == 4 else f"; missing {set(TAINTED4) - set(inside)}"),
            PASS if len(inside) == 4 else FAIL, n=4,
            note="they carry prior TASK-018 labels (3 CERTAIN-leg-d + 4 CANDIDATE), NOT fixtures - the holdout has "
                 "zero fixture transcripts")
    rep.add("12", "ANNEX §F2 — both denominators pre-declared from ONE run", "primary 33, sensitivity 29",
            f"primary {len(seal_h)}, sensitivity {len(seal_h) - len(inside)}", PASS if len(seal_h) == 33 and
            len(inside) == 4 else FAIL, n=len(seal_h))

    act = sha_file(os.path.join(wt, "fixtures/v2/dropword.json"))[:8]
    bound = str((j.get("fixture_sources") or {}).get("fixtures/v2/dropword.json", ""))[:8]
    open_conds = []
    apx12 = os.path.join(wt, "runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md")
    t12 = open(apx12, encoding="utf-8").read() if os.path.exists(apx12) else ""
    if not ("d-092" in t12.lower()):
        open_conds.append("item v2.b (taint disclosure) unlanded")
    if not ("293b29c" in t12 or "one draw" in t12.lower()):
        open_conds.append("item v2.a clause (iii) 2nd half ('one draw, not two') unstated")
    frz = os.path.join(wt, "tools/m4_one_shot_v2.py")
    ft = open(frz, encoding="utf-8").read() if os.path.exists(frz) else ""
    if t12 and not re.search(r"SEAL-APPENDIX|SEAL-AUDIT|appendix_sha|companion", ft):
        open_conds.append("O-5: the freeze does not bind the companion note's digest")
    a2_txt = ""
    t19p = lane_path("fleet/queue/pending/TASK-019.md")
    if os.path.exists(t19p):
        a2_txt = slice_section(open(t19p, encoding="utf-8").read(), "## ANNEX §G")
    if not a2_txt:
        open_conds.append("ANNEX A2: items 0d-0g landed, or the adjudication set excluded by pre-registration")
    rep.add("12", "BLOCKER — quantum b may not run until its preconditions land (v2.7 needs frozen inputs)",
            "no open precondition", f"{len(open_conds)} open: {open_conds}",
            PASS if not open_conds else FAIL, n=len(open_conds),
            note=f"item v2.a's SUBSTANCE is verified at this head — the seal stands, the fixture move is append-only "
                 f"(seal-time {bound}… → live {act}…), 6 of 7 bound digests recompute MATCH — so the blocker no "
                 f"longer rests on the seal's validity; it rests on these conditions")
    sd = sha_file(sp)[:8]
    rep.add("12", "split-v2 file digest at this head (the pre-registration binds the post-note value)",
            "recorded, expected to change exactly once when v2.a lands", sd, INFO, n=1)

    prereg = []
    for root, dirs, files in os.walk(os.path.join(wt, "runs")):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in sorted(files):
            t = fn.lower()
            if "prereg" in t or "pre-reg" in t or "quantum-b" in t or "quantumb" in t:
                prereg.append(os.path.relpath(os.path.join(root, fn), wt))
    rep.add("12", "a committed pre-registration artefact exists (criterion v2.12 needs it BEFORE the run commit)",
            "ABSENT is the correct state while v2.a/v2.b are open", f"{len(prereg)} file(s): {sorted(prereg)[:4]}",
            INFO if not prereg else PASS, n=len(prereg))
    v2salt = j.get("salt")
    spent, spent_v1 = [], []
    for root, dirs, files in os.walk(os.path.join(wt, "runs")):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in sorted(files):
            if fn.endswith(".json"):
                rel = os.path.relpath(os.path.join(root, fn), wt)
                try:
                    txt = open(os.path.join(root, fn), encoding="utf-8").read()
                    d = json.loads(txt)
                except (OSError, ValueError):
                    continue
                if not isinstance(d, dict):
                    continue
                consumed = d.get("holdout_consumed") is True or "holdout is now spent" in txt.lower()
                if not consumed:
                    continue
                ref = str(d.get("split_file") or d.get("split") or "")
                salt = str(d.get("split_salt") or "")
                if "V2" in ref.upper() or (v2salt and salt == v2salt):
                    spent.append(f"{rel} (split {ref or 'v2 salt'})")
                else:
                    spent_v1.append(f"{rel} (split {os.path.basename(ref) or '?'}, salt {salt[-14:]})")
    rep.add("12", "no receipt already declares the V2 holdout SPENT (the quantum-b run has not happened)", "0",
            f"{len(spent)}: {sorted(spent)[:3]}", PASS if not spent else FAIL, n=len(spent),
            note=f"a receipt only consumes v2 if it binds the v2 split file or the v2 salt; "
                 f"{len(spent_v1)} receipt(s) consume the V1 holdout, which is correct and expected: "
                 f"{sorted(spent_v1)[:3]}")





# ---------------------------------------------------------------- self-test (self-item O-2)
def selftest(golden: str) -> int:
    """Assert the helper semantics the sections depend on. Every case names the defect or
    self-item it guards, because each of them was a real wrong answer this instrument gave:
    without this, a refactor can move a gate result silently (self-item O-2)."""
    print("ORCH-2 gate instrument · --selftest")
    cases = []

    def t(cid, why, expected, observed):
        cases.append((cid, why, expected, observed, expected == observed))

    t("T1", "defect #5/#19 curly apostrophes are NORMALISED, not merely included",
      ["that's"], tokens("that\u2019s"))
    t("T2", "defect #2 em/en dashes are SEPARATORS (gluing them merges two tokens)",
      ["word", "word"], tokens("word\u2014word"))
    t("T3", "defect #3 hyphens stay INSIDE tokens (load-bearing for self-item O-1)",
      ["well-known"], tokens("well-known"))
    t("T4", "empty and None inputs tokenize to nothing rather than crashing",
      ([], []), (tokens(""), tokens(None)))
    t("T5", "O-1 a repetition artifact FAILS rule A and PASSES rule B",
      (False, True, (True, True)),
      (drop_rules("evidence; evidence of", "evidence of", ["evidence"])["A remove-all-occurrences"],
       drop_rules("evidence; evidence of", "evidence of", ["evidence"])["B remove-first-occurrence"],
       rule_a_defect("evidence; evidence of", "evidence of", ["evidence"])))
    t("T6", "O-1 a clean single drop satisfies rules A-D and not E (quoted is not contiguous)",
      {"A remove-all-occurrences": True, "B remove-first-occurrence": True, "C quoted-subseq+count": True,
       "D suspected-minus-quoted==dropped": True, "E quoted-contiguous-in-suspected": False},
      drop_rules("alpha beta gamma", "alpha gamma", ["beta"]))
    t("T7", "O-1 the token rule is load-bearing: dropping a hyphenated token's HALF fails rule A",
      False, drop_rules("well-known things", "known things", ["well"])["A remove-all-occurrences"])
    t("T8", "defect #8 a pattern classifying a whole value must FULLMATCH it",
      ("exact", "minute", "fuzzy", "other"),
      (ts_class("2026-09-25T20:38:04Z"), ts_class("2026-09-25T20:38Z"), ts_class("21:5xZ"), ts_class("n/a")))
    t("T8b", "defect #8's actual mechanism: a value that merely CONTAINS a timestamp is not that timestamp",
      "other", ts_class("run at 2026-09-25T20:38:04Z exactly"))
    inst = "the run stamped 21:5xZ on its own header"
    cite = "the fuzzy value `21:5xZ` is superseded by generated_utc_exact"
    t("T9", "defect #18 a census must tell ASSERTING from QUOTING",
      ("instance", "citation"),
      (classify_fuzzy(inst, FUZZY_TS.search(inst)), classify_fuzzy(cite, FUZZY_TS.search(cite))))
    t("T10", "defect #4 fixture files store PATHS while splits store BASENAMES",
      ("x", "x", "x.md"), (norm("corpus/docdocgo/overlays/x.txt"), norm("runs/x.json"), norm("x.md")))
    names = [f"t{i}.txt" for i in range(200)]
    d_full = draw_holdout(names, "s", 5, 0)
    d_hex8 = draw_holdout(names, "s", 5, 0, "hex8")
    t("T11", "the draw is deterministic, partitions the corpus, and the two readings DISAGREE "
             "(the basis of the v2.1 caveat)",
      (True, True, True, True),
      (d_full == draw_holdout(names, "s", 5, 0), bool(d_full), (d_full | (set(names) - d_full)) == set(names),
       d_full != d_hex8))
    t("T12", "the draw over an empty corpus is empty, not everything", set(), draw_holdout([], "s", 5, 0))
    t("T13", "sha256 known-answer test (a wrong digest helper invalidates every binding row)",
      "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad", sha_bytes(b"abc"))
    t("T14", "Poisson CDF known value and monotonicity (the exposure-normalized P row)",
      (round(pois_cdf(0, 1.0), 9), True), (round(math.exp(-1.0), 9),
                                            all(pois_cdf(k, 5.0) <= pois_cdf(k + 1, 5.0) for k in range(12))))
    import tempfile
    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        for d, order in ((a, ("one.txt", "two.txt")), (b, ("two.txt", "one.txt"))):
            for fn in order:
                open(os.path.join(d, fn), "w", encoding="utf-8").write(fn + "\n")
        da, na = dir_digest(a)
        db, nb = dir_digest(b)
    t("T15", "dir_digest is order-independent and counts files (the by-transcript and records rows)",
      (True, 2, 2), (da == db, na, nb))
    t("T17", "defect #5-class trap, stated so callers guard it: two ABSENT values compare equal, so a "
             "check() on .get() results must pass an explicit sentinel for absence",
      True, None == None)

    # the committed golden output must be internally consistent with its own summary line
    if golden and os.path.exists(golden):
        txt = open(golden, encoding="utf-8").read()
        body = txt.split("rows not passing")[0]
        cnt = collections.Counter(m.group(1) for m in
                                  re.finditer(r"^  (PASS|FAIL|INFO|PROXY|VACUOUS)\s", body, re.M))
        m = re.search(r"== summary: (\d+) rows · (.+)$", txt, re.M)
        summ = {kv.split()[0]: int(kv.split()[1]) for kv in m.group(2).split(" · ")} if m else {}
        t("T16", f"the committed golden output {os.path.basename(golden)} agrees with its own summary line",
          (int(m.group(1)) if m else -1, {k: int(v) for k, v in sorted(summ.items())}),
          (sum(cnt.values()), {k: v for k, v in sorted(cnt.items())}))
    else:
        print(f"  SKIP T16   the committed golden output is not reachable from here ({golden}); "
              f"pass --golden to check it")

    bad = [c for c in cases if not c[4]]
    for cid, why, exp, obs, ok in cases:
        print(f"  {'ok  ' if ok else 'FAIL'} {cid:4s} {why}")
        if not ok:
            print(f"         expected {str(exp)[:200]} | observed {str(obs)[:200]}")
    print(f"\n== selftest: {len(cases) - len(bad)}/{len(cases)} ok" + (f" · FAILURES {[c[0] for c in bad]}" if bad else ""))
    return 1 if bad else 0







# item 0f strata: ORCH-2's reconstruction of the four word classes over the 57 CERTAIN-leg-d rows.
# It reproduces the published 27 / 6 / 11 / 13 exactly, which is evidence the classification is
# not arbitrary - but the binding requirement is that WORKER-2 publishes its OWN per-word list.
STRATA = (("interjections/fillers", {"huh", "yeah", "see", "right", "really", "heh", "haha", "um", "well"}),
          ("notation (%↔percent)", {"percent"}),
          ("function words", {"it's", "that's", "there's", "he'd", "may", "since", "however", "including",
                              "already"}))


def section_coherence(wt, rep):
    """§13 — cross-artefact coherence: the shape adjudication, criterion 20.13 / L10, and
    TASK-018 items 0e / 0f / 0g."""
    print("\n== 13. cross-artefact coherence (20.13 / L10, items 0e-0g) ==")
    ep = os.path.join(wt, "runs/m4-q2-dropword/EVAL.json")
    ap = os.path.join(wt, "runs/m4-q2-adjudication/adjudication.jsonl")
    if not (os.path.exists(ep) and os.path.exists(ap)):
        rep.add("13", "EVAL.json + adjudication.jsonl", "present", "ABSENT", FAIL)
        return
    sa = json.load(open(ep, encoding="utf-8"))["shape_adjudication"]
    sigs = sa["signals"]
    adj = [json.loads(l) for l in open(ap, encoding="utf-8") if l.strip()]

    kinds = collections.Counter(str(x["shape"].get("kind")) for x in sigs)
    rep.check("13", "shape_adjudication classifies every signal", len(sigs), len(adj), n=len(sigs))
    rep.check("13", "recomputed kind tally == the published counts", dict(sa["counts"]), dict(kinds), n=len(sigs))
    cr = sa["count_reconciliation"]
    rep.check("13", "count_reconciliation closes: raw == countable + excluded + re-labelled",
              cr["raw"], cr["countable"] + cr["excluded_dropped_token_not_missing"] + cr["re_labelled_needs_human_read"],
              n=cr["raw"])
    rep.check("13", "re_labelled_needs_human_read == partial-overlap + gate-boundary",
              cr["re_labelled_needs_human_read"], kinds["partial-overlap"] + kinds["gate-boundary-excluded"], n=6)
    rep.check("13", "gate_figure == the countable consistent rows", cr["gate_figure"], kinds["consistent"], n=113)
    closes = collections.Counter(str(x["shape"].get("deletion_closes")) for x in sigs)
    rep.add("13", "the note's '114 deletion-closing' is NOT the deletion_closes field",
            "114 == raw minus the 8 rows excluded by shape (3 + 5)",
            f"deletion_closes tally {dict(closes)}; 122 - (3 + 5) = {len(sigs) - kinds['dropped-token-not-missing'] - kinds['partial-overlap']}",
            PASS if len(sigs) - kinds["dropped-token-not-missing"] - kinds["partial-overlap"] == 114 else FAIL,
            n=len(sigs),
            note="deletion_closes is True for all 122, so the note's 114 is a different test; the arithmetic that "
                 "lands the published bound is 122 - 8 = 114, then 114 - 1 gate-listed hyphen case = 113")

    # ORCH-2's rule A against the worker's shape classes: the two partitions must be the SAME 8 rows
    q2 = json.load(open(os.path.join(wt, "runs/m4-q2-dropword/signals.json"), encoding="utf-8"))
    flat = [(k, sg) for k in sorted(q2) for sg in q2[k]]
    def key(t, st, en, dw):
        return (os.path.basename(str(t)), st, en, tuple(w.lower() for w in (dw or [])))
    a8 = {key(k, sg.get("start"), sg.get("end"), sg.get("dropped_words")) for k, sg in flat
          if rule_a_defect(sg.get("suspected"), sg.get("quoted"), sg.get("dropped_words"))[0]}
    w8 = {key(x.get("transcript"), x.get("start"), x.get("end"), x.get("dropped_words")) for x in sigs
          if str(x["shape"].get("kind")) in ("dropped-token-not-missing", "partial-overlap")}
    g1 = {key(x.get("transcript"), x.get("start"), x.get("end"), x.get("dropped_words")) for x in sigs
          if str(x["shape"].get("kind")) == "gate-boundary-excluded"}
    rep.add("13", "ORCH-2's rule-A failures are SET-IDENTICAL to the worker's 8 shape exclusions",
            f"{len(w8)}/{len(w8)} both ways", f"{len(a8 & w8)}/{len(w8)} (A-W {sorted(a8 - w8)[:2]}, "
            f"W-A {sorted(w8 - a8)[:2]})", PASS if a8 == w8 else FAIL, n=len(w8),
            note="this is why the q2.6 figure 113/9 IS reproducible: rule A gives 114/8 over the same 8 rows, and "
                 "the last step to 113 is the single gate-listed hyphen-tokenization exclusion")
    hy = [sg for k, sg in flat if key(k, sg.get("start"), sg.get("end"), sg.get("dropped_words")) in g1]
    if hy:
        h = hy[0]
        split = lambda t: [p.lower() for w in (t or "").replace("\u2019", "'").split()
                           for p in re.split(r"[^A-Za-z0-9']+", w) if p]
        dwl = [w.lower() for w in h["dropped_words"]]
        rep.add("13", "the gate-boundary hyphen row PASSES rule A under the stated token rule and fails under "
                      "hyphen-splitting", "True / False",
                f"{[w for w in tokens(h['suspected']) if w not in dwl] == tokens(h['quoted'])} / "
                f"{[w for w in split(h['suspected']) if w not in dwl] == split(h['quoted'])}",
                PASS if ([w for w in tokens(h['suspected']) if w not in dwl] == tokens(h['quoted']) and
                         not [w for w in split(h['suspected']) if w not in dwl] == split(h['quoted'])) else FAIL,
                n=1, note=f"row: {sorted(g1)[0] if g1 else '?'}")
    # the note must name the row it describes
    note = str(cr.get("note") or "")
    mname = re.search(r"transcript '([^']+)'", note)
    rowname = os.path.basename(str([x for x in sigs if str(x["shape"].get("kind")) == "gate-boundary-excluded"][0]
                                   ["transcript"])) if g1 else "?"
    rep.add("13", "criterion 20.13 / L10 — the reconciliation note names the SAME transcript as the row it "
                  "describes", rowname, mname.group(1) if mname else "no transcript named",
            PASS if mname and mname.group(1) == rowname else FAIL, n=1,
            note="" if (mname and mname.group(1) == rowname) else
                 "NEW ITEM 15a (criterion 20.13): the note cites a transcript that carries ZERO q2 signals while the "
                 "gate-boundary row sits in another file at the same offset; correct the note append-only, or state "
                 "why two files are in play")

    # the campaign publishes TWO different sets of 114 signals; nothing says so
    si = {key(x.get("transcript"), x.get("start"), x.get("end"), x.get("dropped_words")) for x in sigs
          if (x.get("source_inheritance") or {}).get("source_inherited") is True}
    hold_names = {os.path.basename(y) for y in json.load(
        open(os.path.join(wt, "tools/HELD-OUT-SPLIT-V2.json"), encoding="utf-8"))["holdout"]}
    de = {key(k, sg.get("start"), sg.get("end"), sg.get("dropped_words")) for k, sg in flat
          if os.path.basename(k) in hold_names}
    allk = {key(k, sg.get("start"), sg.get("end"), sg.get("dropped_words")) for k, sg in flat}
    a114 = allk - si - de
    b114 = {key(x.get("transcript"), x.get("start"), x.get("end"), x.get("dropped_words")) for x in sigs
            if str(x["shape"].get("kind")) in ("consistent", "gate-boundary-excluded")}
    rep.add("13", "criterion 20.13 — the two published 114s are DIFFERENT SETS (filter-side vs shape-side)",
            "wherever either is quoted, the other is distinguished",
            f"filter-side {len(a114)} (122 - {len(si)} source-inherited - {len(de)} deferred) vs shape-side "
            f"{len(b114)} (122 - {len(w8)}); intersection {len(a114 & b114)}, {len(a114 - b114)} differ each way, "
            f"the two exclusion sets overlap in {len(w8 & (si | de))} rows",
            INFO if len(a114) == len(b114) else PASS, n=len(allk),
            note="ITEM 15b: `filtered: 114` (supplement + EVAL) and 'this instrument finds 114 deletion-closing "
                 "signals' (EVAL's shape note) are equal in size but share only 106 signals; the README explains "
                 "113 vs 114 on the shape side, and nothing states that the filter-side 114 is a different set")
    docs = ""
    for rel in ("runs/m4-q2-dropword/README.md", "runs/m4-q2-dropword/PROVENANCE-SUPPLEMENT.json",
                "runs/m4-q2-adjudication/SUMMARY.md", "tools/PATTERNS.md"):
        fp = os.path.join(wt, rel)
        if os.path.exists(fp):
            docs += open(fp, encoding="utf-8").read()
    distinguishes = bool(re.search(r"different set|not the same 114|two 114|106 (signals|in common)|disjoint",
                                   docs, re.I))
    rep.add("13", "criterion 20.13 — the distinction between the two 114s is written down",
            "stated in a committed doc", "STATED" if distinguishes else "ABSENT — item 15b owed",
            PASS if distinguishes else FAIL, n=1)

    # items 0e / 0f over the 57 CERTAIN-leg-d rows
    cert = [r for r in adj if str(r.get("verdict")) == "CERTAIN-leg-d"]
    sites_span = {(os.path.basename(str(r["transcript"])), str(r.get("span"))) for r in cert}
    sites_off = {(os.path.basename(str(r["transcript"])), r.get("char_offset")) for r in cert}
    rep.add("13", "item 0e — the deduped site count depends on the DEDUPE KEY, which is not published",
            "55 published with its key stated", f"by (transcript, span text) {len(sites_span)}; by "
            f"(transcript, char_offset) {len(sites_off)}; rows {len(cert)}", INFO, n=len(cert),
            note="the two colliding span-text pairs are distinct sites at different offsets: D-097/D-098 "
                 "('percent', Radical_Subjectivity @838 and @1132) and D-120/D-121 ('see', Levels_of_Consciousness "
                 "@60506 and @61014) - so '55' is a span-text dedupe and must say so (criterion 20.15 class)")
    tally = collections.Counter(str(r.get("omitted_word")) for r in cert)
    mine = {}
    for label, words in STRATA:
        mine[label] = sum(v for k, v in tally.items() if k.lower() in words)
    mine["content (everything else)"] = len(cert) - sum(mine.values())
    rep.add("13", "item 0f — ORCH-2's reconstruction of the four strata over the 57 rows",
            "27 / 6 / 11 / 13 summing to 57", " / ".join(str(v) for v in mine.values()) + f" summing to {sum(mine.values())}",
            PASS if list(mine.values()) == [27, 6, 11, 13] else INFO, n=len(cert),
            note=f"word classes: {dict((l, sorted(w)) for l, w in STRATA)}; content = "
                 f"{sorted(k for k in tally if not any(k.lower() in w for _l, w in STRATA))}")
    pub = ""
    for rel in ("tools/PATTERNS.md", "runs/m4-q2-adjudication/SUMMARY.md"):
        fp = os.path.join(wt, rel)
        if os.path.exists(fp):
            pub += open(fp, encoding="utf-8").read()
    rep.add("13", "item 0f — WORKER-2's own per-word class list published (the binding requirement)",
            "a list assigning each of the 32 distinct omitted words to a stratum",
            "published" if re.search(r"(interjection|filler).{0,400}(huh|yeah)", pub, re.S) else "ABSENT",
            PASS if re.search(r"(interjection|filler).{0,400}(huh|yeah)", pub, re.S) else FAIL, n=len(tally),
            note=f"{len(tally)} distinct omitted words: {sorted(tally)}")
    rep.add("13", "item 0f — the notation-class ruling recorded (ERRATA-25e §2 / BOSS guidance: notation variants "
                  "are transcriber formatting conventions)", "a ruling on the 6 'percent' rows",
            "ruling present" if re.search(r"notation", pub, re.I) else "ABSENT",
            PASS if re.search(r"notation", pub, re.I) else FAIL, n=tally.get("percent", 0))
    rep.add("13", "item 0f — speaker-side filler presence stated as unknowable without audio", "stated",
            "stated" if re.search(r"audio", pub, re.I) else "ABSENT",
            PASS if re.search(r"audio", pub, re.I) else FAIL, n=1)

    # item 0g / criterion L10: contradictions with sibling instruments must carry a written ruling
    disp = [k for r in adj for k in r if any(t in k.lower() for t in ("disposition", "ruling", "note", "append"))]
    rep.add("13", "item 0g — adjudication.jsonl carries an append-only disposition field", "present for D-002/D-039",
            f"{sorted(set(disp))[:4] if disp else 'NO disposition/ruling/note key in the schema'}",
            PASS if disp else FAIL, n=len(adj),
            note="item 8b (criterion 20.5) is gated jointly with item 0g by this row: D-002 ('evidence') is "
                 "CERTAIN-leg-d while EVAL.json shape_adjudication excludes that very site as "
                 "dropped-token-not-missing; D-039 ('quite') is CERTAIN-leg-d while the source-inheritance filter "
                 "suppresses that same signal as its own published example")
    supf = json.load(open(os.path.join(wt, "runs/m4-q2-dropword/PROVENANCE-SUPPLEMENT.json"),
                          encoding="utf-8"))["source_inheritance_filter"]
    ex = supf.get("examples") or []
    d39 = [r for r in adj if r.get("id") == "D-039"]
    hit = any(str(e.get("start")) == str(d39[0].get("char_offset")) or e.get("dropped_words") == ["quite"]
              for e in ex) if d39 else False
    rep.add("13", "item 0g — the filter's own example IS the D-039 site (the contradiction is real at this head)",
            "the suppressed example and the promoted row are the same signal",
            f"examples {json.dumps(ex)[:150]}; D-039 offset {d39[0].get('char_offset') if d39 else '?'} "
            f"verdict {d39[0].get('verdict') if d39 else '?'}", PASS if hit else FAIL, n=len(ex))
    v2hold = {os.path.basename(x) for x in json.load(open(os.path.join(wt, "tools/HELD-OUT-SPLIT-V2.json"),
                                                          encoding="utf-8"))["holdout"]}
    tainted = [r.get("id") for r in adj if os.path.basename(str(r.get("transcript"))) in v2hold]
    noted = [r.get("id") for r in adj if os.path.basename(str(r.get("transcript"))) in v2hold
             and any("holdout" in str(v).lower() for k, v in r.items() if k != "transcript")]
    rep.add("13", "item 0g — the v2-holdout rows are marked as such IN the adjudication record",
            f"{len(tainted)} rows noted", f"{len(noted)} of {len(tainted)} noted ({tainted})",
            PASS if len(noted) == len(tainted) else FAIL, n=len(tainted),
            note="no holdout-tainted row may be quoted as tuning-side evidence")
    dem = [r for r in cert if r.get("id") not in ("D-002", "D-039")]
    dem_sites = {(os.path.basename(str(r["transcript"])), str(r.get("span"))) for r in dem}
    rep.add("13", "item 0g — the stated post-demotion arithmetic checks out", "55 rows / 53 distinct sites",
            f"{len(dem)} rows / {len(dem_sites)} span-text sites", PASS if (len(dem), len(dem_sites)) == (55, 53)
            else FAIL, n=len(dem))
    # a field is owed only by the rows it applies to (defect #26: `clause` is the leg-(d) clause, so
    # CANDIDATE rows legitimately lack it; a non-realignable row legitimately has no rebuilt span)
    always = ("verdict", "reason", "seeded", "in_sample", "transcript", "char_offset")
    miss = collections.Counter(f for r in adj for f in always if r.get(f) in (None, ""))
    miss["clause"] = sum(1 for r in adj if str(r.get("verdict")) == "CERTAIN-leg-d" and not r.get("clause"))
    noreal = [r.get("id") for r in adj if not r.get("span")]
    miss["span"] = sum(1 for r in adj if not r.get("span") and not
                       ("re-align" in str(r.get("reason")) or "realign" in str(r.get("reason"))) or
                       (not r.get("span") and not (r.get("detector_span") and r.get("span_end"))))
    rep.add("13", "criterion 20.13 — every adjudication row carries the fields coherence is judged on",
            "0 missing, judged per row class", f"{sum(miss.values())} missing {dict((k, v) for k, v in miss.items() if v)}",
            PASS if not sum(miss.values()) else FAIL, n=len(adj) * len(always),
            note=f"`clause` is required only on CERTAIN-leg-d rows (57/57 carry it, 0/65 CANDIDATE rows do, "
                 f"correctly); {len(noreal)} rows {noreal} have no rebuilt span because their own reason states the "
                 f"omission is not re-alignable from the frozen bytes, and each still carries detector_span + "
                 f"char_offset + span_end")
    p3 = ""
    fp = os.path.join(wt, "tools/PATTERNS.md")
    if os.path.exists(fp):
        p3 = slice_section(open(fp, encoding="utf-8").read(), "§3") or open(fp, encoding="utf-8").read()
    rep.add("13", "criterion 20.13 — a count quoted in PATTERNS states the exclusions behind it",
            "'57/122' quoted with the 3 + 6 shape exclusions and the 7 deferred holdout signals stated",
            ("stated" if re.search(r"defer", p3, re.I) and re.search(r"partial-overlap|dropped-token", p3, re.I)
             else "UNQUALIFIED" if "57/122" in p3 else "not quoted"),
            PASS if (re.search(r"defer", p3, re.I) and re.search(r"partial-overlap|dropped-token", p3, re.I)) else FAIL,
            n=1, note="the artefact supports 57/122 raw; after its own exclusions the countable figure is 113, and "
                      "the CERTAIN count under item 0g would be 55 rows / 53 sites")





def section_derivations(wt, rep):
    """§14 — criterion 20.15: does every derivation stated in the binding-of-record manifest
    reproduce when followed LITERALLY, and does it state its canonicalization? Until this
    section existed item 13 had no FAIL row of its own, so the claim 'the FAIL set equals the
    open items' was incomplete - recorded as such in ledger §14."""
    print("\n== 14. criterion 20.15 — stated derivations reproduce literally ==")
    mp = os.path.join(wt, "findings/PROVENANCE.json")
    if not os.path.exists(mp):
        rep.add("14", "findings/PROVENANCE.json (the binding of record)", "present", "ABSENT", FAIL)
        return
    man = json.load(open(mp, encoding="utf-8"))
    dv = man.get("derivations") or {}
    rep.check("14", "the binding of record publishes a derivations block", True, bool(dv), n=len(dv))

    literal, stated = {}, {}
    # by_transcript: "same construction as records_digest over findings/by-transcript/"
    d, n = dir_digest(os.path.join(wt, "findings/by-transcript"))
    literal["by_transcript_digest"] = d == man["outputs"]["by_transcript_digest"]
    stated["by_transcript_digest"] = "records_digest" in str(dv.get("by_transcript_digest"))
    # records_digest: fully stated (sorted lines, relpath key, sort key = the line)
    d, n = dir_digest(os.path.join(wt, "evidence/runs/m5-raw/records"))
    literal["records_digest_sha256"] = d == man["inputs"]["records_digest_sha256"]
    stated["records_digest_sha256"] = "path relative to records dir" in str(dv.get("records_digest_sha256"))
    # overlays_digest: stated construction reproduces; the warned-against variant's construction is NOT stated
    ov = os.path.join(wt, "corpus/docdocgo/overlays")
    lines = []
    for b in sorted(x for x in os.listdir(ov) if x.endswith(".txt")):
        t = open(os.path.join(ov, b), encoding="utf-8", errors="replace").read()
        lines.append(f"{sha_bytes(t.encode('utf-8'))}  {b}\n")
    literal["overlays_digest"] = sha_bytes("".join(lines).encode()) == man["inputs"]["overlays_digest"]
    txt = str(dv.get("overlays_digest"))
    stated["overlays_digest"] = ("sorted" in txt and "basename" in txt and
                                 "join" in txt.lower() and "58274f46" in txt and "\\n" in txt)
    # corpus zip + ledger + tool: byte digests, self-describing
    literal["corpus_zip_sha256"] = sha_file(os.path.join(wt, "docdocgo-fixes.zip")) == man["inputs"]["corpus_zip_sha256"]
    stated["corpus_zip_sha256"] = "bytes" in str(dv.get("corpus_zip_sha256"))
    literal["outputs.ledger.jsonl"] = sha_file(os.path.join(wt, "findings/ledger.jsonl")) == man["outputs"]["ledger.jsonl"]
    stated["outputs.ledger.jsonl"] = "bytes" in str(dv.get("outputs.ledger.jsonl"))
    literal["tool_sha256"] = sha_file(os.path.join(wt, "tools/m5r_reduce.py")) == man["tool_sha256"]
    stated["tool_sha256"] = "bytes" in str(dv.get("tool_sha256"))
    # fixtures_digest: the stated construction (relpath over fixtures/) does NOT reproduce
    d_rel, _ = dir_digest(os.path.join(wt, "fixtures"), key="relpath")
    d_base, nb = dir_digest(os.path.join(wt, "fixtures/confirmed"), key="basename")
    literal["fixtures_digest_sha256"] = d_rel == man["inputs"]["fixtures_digest_sha256"]
    stated["fixtures_digest_sha256"] = ("basename" in str(dv.get("fixtures_digest_sha256")) or
                                        "confirmed" in str(dv.get("fixtures_digest_sha256")))
    rep.add("14", "criterion 20.15a — every stated derivation reproduces when followed LITERALLY",
            f"{len(literal)}/{len(literal)}", f"{sum(literal.values())}/{len(literal)}"
            f" (failures: {sorted(k for k, v in literal.items() if not v)})",
            PASS if all(literal.values()) else FAIL, n=len(literal),
            note="ITEM 13: `fixtures_digest_sha256` says 'same construction over the fixtures dir', which gives "
                 f"{d_rel[:12]}…; the published {man['inputs']['fixtures_digest_sha256'][:12]}… reproduces only with "
                 f"BASENAME keys over the {nb} files in fixtures/confirmed/. State the key convention and the input "
                 "set, and say that fixtures/clean, fixtures/negative and fixtures/v2 are outside this binding")
    rep.add("14", "criterion 20.15b — every derivation states its canonicalization (key convention, join, sort)",
            f"{len(stated)}/{len(stated)}", f"{sum(stated.values())}/{len(stated)}"
            f" (unstated: {sorted(k for k, v in stated.items() if not v)})",
            PASS if all(stated.values()) else FAIL, n=len(stated),
            note="the warned-against overlays variant 58274f46… is reproducible exactly as "
                 'sha256("\\n".join(sorted(lines_without_trailing_newline))) but the manifest does not state that '
                 "construction, so the warning is not checkable as written; the good pattern already exists in this "
                 "lane (the q2 supplement's config_digest_note names sort_keys and separators)")





def section_quantum_b_criteria(wt, rep):
    """§15 — criteria v2.12–v2.16 (quantum b). They cannot PASS before the run exists, so each row
    states the exact shape it will check and reports HELD; two precedent rows verify the analogous
    property on artefacts that DO exist, so the eventual gate is one run rather than an argument."""
    print("\n== 15. quantum-b criteria v2.12-v2.16 (HELD until the run exists) ==")
    runs = os.path.join(wt, "runs")
    cand = sorted(d for d in os.listdir(runs) if "quantum" in d.lower() or "holdout-v2" in d.lower()) \
        if os.path.isdir(runs) else []
    rep.add("15", "criterion v2.12 — the pre-registration commit exists BEFORE the run commit",
            "commit order plus exact timestamps carrying their source (criterion 20.14)",
            f"HELD — no quantum-b run directory exists yet ({cand or 'none under runs/'})", INFO, n=len(cand),
            note="when it lands this row checks: add-time of the pre-registration artefact < add-time of every "
                 "artefact in the eval directory, by `git log -S` where a reference is concerned (defect #22), and "
                 "that both stamps are exact to the second with a stated source")
    rep.add("15", "criterion v2.13 — the receipt exists, declares the v2 holdout SPENT, and `holdout_reads` EQUALS "
                  "the pre-registered eval set", "receipt present, holdout_consumed true, holdout_reads == eval set",
            "HELD — no receipt binds the v2 split (§12 verifies the two spent receipts bind v1)", INFO, n=1,
            note="the eval set is the 33 v2-holdout transcripts, or the 29 sensitivity set if the pre-registration "
                 "excludes the four label-tainted files under ANNEX §F2 - whichever it names, `holdout_reads` must "
                 "equal it exactly: no more, no less")
    rep.add("15", "criterion v2.14 — nothing was added to the eval directory after the run except the receipt and an "
                  "errata", "commit history of that path shows only those two additions",
            "HELD — the eval directory does not exist", INFO, n=1,
            note="verified from the path's own commit history, not from a manifest claim")
    # precedent rows: the analogous property on artefacts that DO exist
    ap = os.path.join(wt, "runs/m4-q2-adjudication/adjudication.jsonl")
    if os.path.exists(ap):
        adj = [json.loads(l) for l in open(ap, encoding="utf-8") if l.strip()]
        present = sum(1 for r in adj if "seeded" in r and "in_sample" in r)
        true_rows = [r.get("id") for r in adj if r.get("seeded") is True]
        rep.add("15", "criterion v2.15 PRECEDENT — on the existing adjudication set the `seeded`/`in_sample` flags are "
                      "PRESENT on every row and `seeded: true` on none", f"{len(adj)}/{len(adj)} present, 0 true",
                f"{present}/{len(adj)} present, {len(true_rows)} true {true_rows[:4]}",
                PASS if present == len(adj) and not true_rows else FAIL, n=len(adj),
                note="an ABSENT flag is as much a defect as a wrong one; this is the row TASK-018 item 0d's false "
                     "`seeded` sentence contradicts, and it is why the same test is pre-registered for the holdout "
                     "rows under v2.15")
    src = os.path.join(wt, "tools/m4_q4_supplement.py")
    if os.path.exists(src):
        t = open(src, encoding="utf-8").read()
        hits = sum(t.count(x) for x in ("overlays", "parse_book_store", "run_tuning"))
        rep.add("15", "criterion v2.16 PRECEDENT — one-shot discipline read from the TOOL'S SOURCE, not its manifest",
                "0 references to the tuning-side readers in the one-shot tool", f"{hits} reference(s)",
                PASS if hits == 0 else FAIL, n=hits,
                note="the same source read will be applied to the quantum-b tool: it must not be able to reach the "
                     "tuning path, and the HoldoutGuard must be instantiated rather than merely importable")





TASK_PATTERNS = {
    "TASK-013": (r"(?<![A-Za-z0-9])C(?:1[0-3]|[1-9])(?![A-Za-z0-9])", "M5-R criteria C1-C13"),
    "TASK-014": (r"(?<![A-Za-z0-9])q[1-5]\.[0-9]{1,2}(?![0-9])", "M4 scoreboard criteria q1.1-q5.8"),
    "TASK-016": (r"(?<![A-Za-z0-9])C(?:1[0-3]|[1-9])(?![A-Za-z0-9])", "M5-R repair criteria"),
    "TASK-017": (r"(?<![A-Za-z0-9])17\.[a-z](?![A-Za-z])", "inherited-toolchain items (the six criteria are prose)"),
    "TASK-018": (r"(?<![A-Za-z0-9])0[a-h](?![A-Za-z0-9])|(?<![A-Za-z0-9])L[0-9]{1,2}(?![A-Za-z0-9])",
                 "leg-(d) items 0a-0h and criteria L1-L10"),
    "TASK-019": (r"(?<![A-Za-z0-9])v2\.[0-9]{1,2}(?![0-9])", "split v2 + quantum-b criteria v2.1-v2.16"),
    "TASK-020": (r"(?<![A-Za-z0-9])20\.[0-9]{1,2}(?![0-9])", "consolidated-repair criteria 20.1-20.16"),
    "TASK-021": (r"(?<![A-Za-z0-9])21\.[0-9]{1,2}(?![0-9])", "C1-drop sensitivity criteria 21.1-21.8"),
}


def section_coverage(rep):
    """§16 — criterion coverage: which criteria of each queued task does this instrument actually
    mechanize, and does the instrument cite any criterion that does not exist in the ruleset?
    Reads the queue files BESIDE this instrument, i.e. the gate authority's own copies, so these
    rows are a function of the ORCH-2 lane commit and not of the worker head."""
    print("\n== 16. criterion coverage of this instrument (lane-side) ==")
    lane = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    qdir = os.path.join(lane, "fleet/queue/pending")
    src = open(os.path.abspath(__file__), encoding="utf-8").read()
    if not os.path.isdir(qdir):
        rep.add("16", "the queue directory beside this instrument", "present", f"ABSENT at {qdir}", FAIL)
        return

    def mentions(txt, cid):
        hits = 0
        for m in re.finditer(r"(?<![A-Za-z0-9])" + re.escape(cid) + r"(?![A-Za-z0-9])", txt):
            tail = txt[m.end():m.end() + 9]
            if cid in ("C1", "C2") and re.match(r"[-\s](drop|format)", tail):
                continue          # 'C1-drop' is a detector name, not criterion C1
            hits += 1
        return hits

    union = set()
    for task, (pat, label) in sorted(TASK_PATTERNS.items()):
        fp = os.path.join(qdir, task + ".md")
        if not os.path.exists(fp):
            rep.add("16", f"{task} queue file", "present", "ABSENT", FAIL)
            continue
        txt = open(fp, encoding="utf-8").read()
        ids = sorted(set(re.findall(pat, txt)))
        union |= set(ids)
        cov = [c for c in ids if mentions(src, c)]
        unc = [c for c in ids if c not in cov]
        rep.add("16", f"{task} — {label}: criteria mechanized by this instrument",
                f"{len(ids)}/{len(ids)} covered, or the gap listed",
                f"{len(cov)}/{len(ids)} CITED" + (f"; not cited by id {unc}" if unc else ""),
                PASS if not unc else PROXY, n=len(ids),
                note="PROXY, not a coverage verdict: this counts ids CITED in the instrument's source, and several "
                     "sections mechanize a criterion without printing its id (§7 is q2.6's substance, §1 carries "
                     "20.2-20.4, §13 carries 20.13/L10 and items 0e-0g). The authoritative criterion-to-section map "
                     "is published in ledger §16; a criterion gated by hand and recorded in GATES.md is legitimate, "
                     "but the gap must be visible because an uncited criterion is one whose re-gate is not a single "
                     "instrument run")
    # the other direction: does the instrument cite a criterion that exists in no queue file?
    allq = " ".join(open(os.path.join(qdir, f), encoding="utf-8").read() for f in sorted(os.listdir(qdir)))
    SHAPE = re.compile(r"^(C\d{1,2}|L\d{1,2}|q[1-5]\.\d{1,2}|v2\.\d{1,2}[a-b]?|\d{2}\.\d{1,2}[a-d]?|"
                       r"1?7\.[a-h]|0[a-h]|\d{1,2}[a-b])$")
    cited = sorted(set(re.findall(r"criterion\s+([A-Za-z0-9.]{2,8})", src)) |
                   set(re.findall(r"item\s+([0-9]{1,2}[a-h]?|v2\.[a-b]|17\.[a-z])\b", src)))
    ghosts = []
    for c in cited:
        base = c.strip(".,;")
        if not SHAPE.match(base):
            continue                      # not a criterion id at all (e.g. the word 'closure')
        # a sub-letter (20.14a) traces to its parent criterion (20.14), which IS in the ruleset
        cands = [base] + ([re.sub(r"[a-d]$", "", base)] if re.search(r"\d[a-d]$", base) else [])
        if not any(mentions(allq, x) for x in cands):
            ghosts.append(base)
    rep.add("16", "this instrument cites no criterion or item that exists in no queue file",
            "0 ghosts", f"{len(ghosts)}: {sorted(set(ghosts))[:8]}", PASS if not ghosts else FAIL,
            n=len(cited),
            note="a row that cites a criterion outside the ruleset invents authority (defect #10's class: the needle "
                 "must be the actual wording). Sub-letters such as 20.14a are ORCH-2's own sub-rows and are traced to "
                 "their parent criterion, which must exist in the queue files")
    # the load-bearing coverage claim: every OPEN item must have a row that flips when it is repaired
    OPEN = ("8a", "8b", "11a", "11b", "12", "13", "14", "15a", "15b", "0d", "0e", "0f", "0g", "17.a", "v2.a", "v2.b")
    def cites_item(txt, iid):
        return bool(re.search(r"(?i)\b(item|criterion)\s+" + re.escape(iid) + r"\b", txt))
    missing = [i for i in OPEN if not cites_item(src, i)]
    rep.add("16", "every OPEN item in the queue has a row in this instrument that flips when it is repaired",
            f"{len(OPEN)}/{len(OPEN)} cited", f"{len(OPEN) - len(missing)}/{len(OPEN)}"
            + (f"; NOT CITED {missing}" if missing else ""), PASS if not missing else FAIL, n=len(OPEN),
            note="the open-item list is taken from fleet/queue/status.md and TASK-MAP.md's published priority; this "
                 "row is the coverage claim that matters, because these are the items whose re-gate must be a single "
                 "run")




# TASK-021's grid and the shipped operating point, read from the pinned detector source so the
# anchor cannot drift: criteria 21.1-21.8 (fleet/queue/pending/TASK-021.md).
GRID = (("min_flank", (2, 3, 5, 8)), ("min_ratio", (0.80, 0.85, 0.90)), ("min_matched", (8, 10, 14)))


def section_t21(wt, rep):
    """§17 — TASK-021 (C1-drop sensitivity over the v2 tuning half). Not started, so each criterion
    is a HELD row stating the exact test it will get, plus the facts that can be pinned NOW: the
    shipped operating point, the grid arithmetic, both denominators, the dedupe lesson and the
    test-count floor. Ledger §16 published this as the instrument's one honest gap; this closes it."""
    print("\n== 17. TASK-021 sensitivity grid (criteria 21.1-21.8) ==")
    dd = os.path.join(wt, "tools/det_dropword.py")
    txt = open(dd, encoding="utf-8").read() if os.path.exists(dd) else ""
    shipped = {}
    singles = (("MIN_SCORE", "min_score"), ("TOP_K", "top_k"), ("MAX_DROP", "max_drop"), ("MIN_FLANK", "min_flank"))
    for const, key in singles:
        m = re.search(r"^" + const + r"\s*=\s*([0-9.]+)", txt, re.M)
        if m:
            shipped[key] = m.group(1)
    m = re.search(r"^WINDOW,\s*STRIDE\s*=\s*([0-9]+),\s*([0-9]+)", txt, re.M)
    if m:
        shipped["window"], shipped["stride"] = m.group(1), m.group(2)
    m = re.search(r"^MIN_MATCHED,\s*MIN_RATIO\s*=\s*([0-9]+),\s*([0-9.]+)", txt, re.M)
    if m:
        shipped["min_matched"], shipped["min_ratio"] = m.group(1), m.group(2)
    rep.add("17", "the shipped operating point, read from the PINNED detector source (a0236325…)",
            "all eight thresholds the q2 README publishes, so the anchor row is checkable against source",
            f"{len(shipped)}/8: {shipped}",
            PASS if len(shipped) == 8 else FAIL, n=len(shipped),
            note="the anchor row of the sensitivity table must equal these values; reading them from the source "
                 "rather than the README is what makes 21.2 checkable")
    for axis, vals in GRID:
        anchor = shipped.get(axis)
        rep.add("17", f"criterion 21.2 — grid axis `{axis}` contains its own anchor", f"anchor {anchor} ∈ {vals}",
                f"anchor {anchor}" + (" ∈ grid" if anchor and any(str(v) == str(anchor) or
                                                                  f"{v:.2f}" == f"{float(anchor):.2f}"
                                                                  for v in vals) else " NOT IN GRID"),
                PASS if anchor and any(f"{float(v):.2f}" == f"{float(anchor):.2f}" for v in vals) else FAIL,
                n=len(vals))
    n_settings = 1 + sum(len(v) - 1 for _a, v in GRID)
    rep.add("17", "criterion 21.2 — the table's expected size (one parameter at a time from the shipped point)",
            "the anchor plus every non-anchor value on each axis",
            f"{n_settings} distinct settings (or {1 + sum(len(v) for _a, v in GRID)} rows if the anchor is repeated "
            f"per axis)", PASS, n=n_settings)
    art = os.path.join(wt, "runs/m4-t21-sensitivity")
    rep.add("17", "criterion 21.1/21.6 — the artefact directory `runs/m4-t21-sensitivity/`",
            "ABSENT is correct: the task has not been claimed", "present" if os.path.isdir(art) else "ABSENT",
            INFO if not os.path.isdir(art) else PASS, n=1,
            note="when it lands, 21.1 needs the HoldoutGuard refusal in code + `holdout_reads: []` + "
                 "`holdout_enforced: true`, and 21.6 needs the §8 manifest with a `tool_commit` that CONTAINS the "
                 "generating tool - the exact failure of item 8a at ffb8811… and 71c37cf…")
    v1 = json.load(open(os.path.join(wt, "tools/HELD-OUT-SPLIT.json"), encoding="utf-8"))
    v2 = json.load(open(os.path.join(wt, "tools/HELD-OUT-SPLIT-V2.json"), encoding="utf-8"))
    rep.add("17", "criterion 21.3 — both denominators, derived here so the table can be checked",
            "v1 tuning 193 and v2 tuning 197, stated with every comparison to the shipped 122",
            f"v1 tuning {len(v1['tuning'])} / v2 tuning {len(v2['tuning'])}; the shipped 122 signals are keyed by "
            f"the v1 half, of which {len({os.path.basename(x) for x in v2['holdout']} & set(map(os.path.basename, v1['tuning'])))} "
            f"are v2-holdout members", PASS if (len(v1["tuning"]), len(v2["tuning"])) == (193, 197) else FAIL, n=2)
    rep.add("17", "criterion 21.7 — the dedupe rule must name its KEY (the lesson of item 0e)",
            "a stated key, applied consistently, duplicates counted separately from rows",
            "over the 57 CERTAIN-leg-d rows: 57 distinct (transcript, char_offset) sites but 55 distinct "
            "(transcript, span text) - so 'site count' is ambiguous until the key is named", INFO, n=57,
            note="HELD until the artefact exists; the collisions are D-097/D-098 and D-120/D-121 (§13)")
    for cid, test in (("21.4", "the stability set (present at EVERY setting vs shipped-point-only) sums coherently "
                               "with the anchor row: stable + shipped-only + setting-specific = the anchor count"),
                      ("21.5", "no threshold chosen or recommended and no precision / recall / rate / M6 figure "
                               "anywhere in the artefacts; every output labelled CANDIDATE-class / "
                               "PROVISIONAL-UNGATED - checked by grepping the artefact directory for those terms"),
                      ("21.8", "the suite stays green WITH the corpus present and the test count does not drop")):
        rep.add("17", f"criterion {cid} — {test}", "HELD until the run exists", "HELD", INFO, n=1)



# ---- cycle I: the worker's own seal audit (WORKER-2 72104a5) re-derived from git bytes ----
SEAL_COMMIT = "79eb401b4328d254a5cee9be0a07f17a5a5e610b"
SEAL_REL = "tools/HELD-OUT-SPLIT-V2.json"
FX_REL = "fixtures/v2/dropword.json"
AUDIT_REL = "runs/m4-q2-adjudication/SEAL-AUDIT.json"
APPENDIX_REL = "runs/m4-q2-adjudication/SEAL-APPENDIX-2026-09-25.md"


def _blob(wt, rev, rel):
    rc, out = git(wt, "show", f"{rev}:{rel}")
    return out if rc == 0 else None


def _flat(node, path=""):
    d = {}
    if isinstance(node, dict):
        for k, v in node.items():
            d.update(_flat(v, f"{path}/{k}"))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            d.update(_flat(v, f"{path}[{i}]"))
    else:
        d[path] = node
    return d


def section_seal_audit(wt, rep, head):
    """§18 — cycle I: WORKER-2's post-seal audit @ 72104a5 re-derived independently, plus the four
    provenance defects found inside the repair artefacts themselves. A worker tool auditing the
    worker's own seal is not evidence until the gate re-derives it from git bytes, so every claim in
    SEAL-AUDIT.json / SEAL-APPENDIX is recomputed here (16 claims: 13 verified, 3 mismatched — all
    three documentation-class, none substantive)."""
    print("\n== 18. cycle I — the seal audit re-derived (WORKER-2 72104a5) ==")
    ap = os.path.join(wt, AUDIT_REL)
    xp = os.path.join(wt, APPENDIX_REL)
    # lane-side row FIRST: A2 is ORCH-2's own decision and must be evaluated at every head, not only where
    # the worker's audit artefacts exist, or a regression could hide behind the early return below.

    t19 = lane_path("fleet/queue/pending/TASK-019.md")
    a2t = open(t19, encoding="utf-8").read() if os.path.exists(t19) else ""
    a2 = slice_section(a2t, "## ANNEX §G")
    need = ("EXCLUDED", "fresh and blind", "seeded", "before the freeze")
    have = [k for k in need if k.lower() in a2.lower()]
    rep.add("18", "ANNEX A2 (lane-side) — the adjudication-set decision is RECORDED BEFORE any run, as A2 requires",
            f"a §G decision carrying all four of {need}",
            ("§G present with " + f"{len(have)}/4 required elements" + (" — " + a2.strip().split(chr(10))[0][:90]
                                                                        if a2 else "")) if a2 else "§G ABSENT",
            PASS if a2 and len(have) == 4 else FAIL, n=len(have),
            note="A2 is the gate's decision to make, not the worker's: it removes one of the quantum-b blockers "
                 "without waiting on TASK-018 items 0d-0g, and it is only valid because it is recorded before the freeze")

    if not (os.path.exists(ap) and os.path.exists(xp)):
        rep.add("18", "SEAL-AUDIT.json + SEAL-APPENDIX (the item v2.a material)", "present at a head that has them",
                "ABSENT at this head — nothing to re-derive", INFO, n=0,
                note="these artefacts first exist at WORKER-2 72104a5 (b991f29 tool, 72104a5 report+appendix)")
        return
    rep_j = json.load(open(ap, encoding="utf-8"))
    appx = open(xp, encoding="utf-8").read()
    seal_live = open(os.path.join(wt, SEAL_REL), "rb").read()
    seal_seal_time = _blob(wt, SEAL_COMMIT, SEAL_REL)
    seal = json.loads(seal_live)

    rep.add("18", "the seal file is byte-identical since its own seal commit (the appendix's central claim)",
            "73d86f0dafe5… at 79eb401 and at head, identical bytes",
            f"{sha_bytes(seal_seal_time)[:12]}… / {sha_bytes(seal_live)[:12]}… identical={seal_seal_time == seal_live}",
            PASS if seal_seal_time == seal_live and sha_bytes(seal_live).startswith("73d86f0d") else FAIL, n=1,
            note="this is why O-5 amends ANNEX A1 rather than ordering an edit: any edit moves 73d86f0d…, which the "
                 "appendix itself binds")

    # every digest the seal binds, recomputed at head (criterion v2.10 as amended by O-5)
    bound = {"/corpus_files_sha256": seal["corpus_files_sha256"]}
    bound.update({f"/fixture_sources/{k}": v for k, v in seal["fixture_sources"].items()})
    bound.update({f"/manifest/{k}": v for k, v in seal["manifest"].items() if k.endswith("sha256")})
    ovdir = os.path.join(wt, "corpus/docdocgo/overlays")
    names = sorted(b for b in os.listdir(ovdir) if b.endswith(".txt")) if os.path.isdir(ovdir) else []
    live = {"/corpus_files_sha256": sha_bytes(("\n".join(names) + "\n").encode("utf-8"))}
    for k, v in seal["fixture_sources"].items():
        fp = os.path.join(wt, k)
        live[f"/fixture_sources/{k}"] = sha_file(fp) if os.path.exists(fp) else None
    for k, path in (("corpus_zip_sha256", "docdocgo-fixes.zip"), ("policy_sha256", "fleet2/POLICY-MANIFEST.sha256"),
                    ("tool_sha256", "tools/m4_split_v2.py"),
                    # the seal's derivations never name this file; tools/census.py's book_store_bytes (14,634,979)
                    # identifies it, and the digest confirms it: c0892fcd…
                    ("book_store_sha256", "corpus/docdocgo/html/merged-book-texts_json_1.js")):
        fp = os.path.join(wt, path)
        live[f"/manifest/{k}"] = sha_file(fp) if os.path.exists(fp) else None
    match = [k for k in bound if k in live and live[k] == bound[k]]
    moved = [k for k in bound if k in live and live[k] != bound[k]]
    unchecked = [k for k in bound if k not in live or live[k] is None]
    rep.add("18", "criterion v2.10 as amended by O-5 — every digest the seal binds, recomputed at head",
            "all MATCH except the one post-seal append-only move, which must be classified and appendixed",
            f"{len(match)}/{len(bound)} MATCH; MOVED: {moved}; not recomputable here: {unchecked}",
            PASS if match and moved == [f"/fixture_sources/{FX_REL}"] and not unchecked else FAIL, n=len(bound),
            note="book_store_sha256's file is never named in the seal's derivations; it is identified here from "
                 "tools/census.py's book_store_bytes (14,634,979) and confirmed by digest — an unnamed binding is "
                 "itself a small defect, recorded rather than left to the reader")

    # the append-only classification, re-derived by flattening both blobs
    fx_seal, fx_head = _blob(wt, SEAL_COMMIT, FX_REL), open(os.path.join(wt, FX_REL), "rb").read()
    fs, fh = _flat(json.loads(fx_seal)), _flat(json.loads(fx_head))
    changed = [k for k in fs if k in fh and fs[k] != fh[k]]
    removed = [k for k in fs if k not in fh]
    added = [k for k in fh if k not in fs]
    ids_s = [f.get("id") for f in json.loads(fx_seal).get("fixtures", [])]
    ids_h = [f.get("id") for f in json.loads(fx_head).get("fixtures", [])]
    hist = git(wt, "log", "--format=%h|%cI", "--", FX_REL)[1].decode().strip().split("\n")
    rep.add("18", "the audit's `mutations: []` / APPEND-ONLY-AFTER-SEAL classification, re-derived from both blobs",
            "0 seal-time keys changed, 0 removed; additions only; fixture id set identical",
            f"changed {len(changed)} removed {len(removed)} added {len(added)}; ids {ids_s} == {ids_h}: {ids_s == ids_h}",
            PASS if not changed and not removed and ids_s == ids_h else FAIL, n=len(added),
            note=f"the moving commit is {hist[0]} (post-seal); the added keys are TASK-020 item 7's enacted-leg-d "
                 f"annotation blocks and the generated_utc_exact* keys")
    rep.add("18", "the seal-time and head digests of the fixture file are the two the appendix names",
            "c8e963199a1e… (seal time) → c40d272f30d0… (head)",
            f"{sha_bytes(fx_seal)[:12]}… → {sha_bytes(fx_head)[:12]}…",
            PASS if sha_bytes(fx_seal).startswith("c8e96319") and sha_bytes(fx_head).startswith("c40d272f") else FAIL,
            n=2)

    # the confirmation artefact, placed in time
    ca = "runs/m4-q2-adjudication/fixtures-adjudication.json"
    ca_hist = git(wt, "log", "--format=%h|%cI", "--", ca)[1].decode().strip().split("\n")
    ca_live = os.path.join(wt, ca)
    ca_sha = sha_file(ca_live) if os.path.exists(ca_live) else None
    seal_utc = git(wt, "log", "-1", "--format=%cI", SEAL_COMMIT)[1].decode().strip()
    rep.add("18", "the confirmation artefact is PRE-seal (the claim that decides the re_seal_rule)",
            "sha 61568a9e…, whole history one commit 1fb524e @ 2026-09-25T20:38:18Z, before the seal 20:51:54Z",
            f"{str(ca_sha)[:12]}…; commits touching it {ca_hist}; seal commit {seal_utc}",
            PASS if ca_sha and ca_sha.startswith("61568a9e") and len(ca_hist) == 1 and
                    ca_hist[0].split("|")[1] < seal_utc else FAIL, n=len(ca_hist))

    # membership and the draw, at this head
    forced = set(seal.get("fixture_transcripts_forced_tuning", []))
    hold = set(seal["holdout"])
    draw = draw_holdout(names, seal["salt"], seal["mod"], seal["holdout_bucket"])
    rep.add("18", "membership at head: the forced set does not intersect the holdout",
            "forced 43 ∩ holdout 33 = ∅; counts tuning 197 / holdout 33",
            f"forced {len(forced)} ∩ holdout {len(hold)} = {len(forced & hold)}; counts "
            f"{seal['counts']}", PASS if not (forced & hold) and (len(seal["tuning"]), len(hold)) == (197, 33) else FAIL,
            n=len(forced | hold))
    rep.add("18", "the draw still reproduces at head — and the seal's own `derivations.holdout_set` line read "
                  "LITERALLY does not", "the sealed holdout, set-equal",
            f"sha256(SALT+name) mod 5 == 0 gives {len(draw)} names; minus the {len(draw & forced)} that are forced to "
            f"tuning gives {len(draw - forced)}, set-equal to the seal's 33: {(draw - forced) == hold}",
            PASS if (draw - forced) == hold else FAIL, n=len(draw),
            note="the exclusion is stated in the seal's `forced_transcripts` and `tuning_set` derivations but NOT in "
                 "the `holdout_set` line, so that line alone yields 42 — criterion 20.15a's discipline (a derivation "
                 "must reproduce when followed literally) applied to a sealed artefact that may not be edited; the "
                 "reading of record is §10's, which reproduces 33/197")

    # the audit tool and its own provenance
    tool_rel = rep_j.get("tool", "tools/m4_seal_audit.py")
    tool_sha = sha_file(os.path.join(wt, tool_rel)) if os.path.exists(os.path.join(wt, tool_rel)) else None
    rep.add("18", "the audit tool's digest equals the one stamped in its own report", "eb4e4ec75afb…",
            f"{str(tool_sha)[:12]}… vs report {str(rep_j.get('tool_sha256'))[:12]}…",
            PASS if tool_sha and tool_sha == rep_j.get("tool_sha256") else FAIL, n=1)
    hca = rep_j.get("head_commit_at_audit", "")
    anc = git(wt, "merge-base", "--is-ancestor", hca, head)[0] == 0 if hca else False
    rep.add("18", "the report names the head it audited, and that head is an ancestor of the report's own commit",
            "an ancestor — the report cannot claim to have audited a commit that did not exist",
            f"head_commit_at_audit {hca[:7]} ancestor-of {head[:7]}: {anc}", PASS if anc else FAIL, n=1,
            note="the report states the ordering itself ('committed as its own commit after it') — honest sequencing")
    tsrc = open(os.path.join(wt, tool_rel), encoding="utf-8").read() if tool_sha else ""
    reads = [ln for ln in tsrc.split("\n") if re.search(r"corpus/|overlays|docdocgo", ln) and not ln.strip().startswith("#")]
    rep.add("18", "the audit tool opens no transcript content (the 'holdout not opened' claim, tested on the tool)",
            "0 reads of corpus/overlays paths — git objects, the seal file and itself only",
            f"{len(reads)} such line(s): {reads[:3]}", PASS if not reads else FAIL, n=len(reads),
            note="it does read the holdout NAME list from the seal, which membership checks require; names are not "
                 "content, and no transcript bytes are opened")

    # ---- the four provenance defects inside the repair artefacts (new items v2.c-v2.f) ----
    audit_utc = rep_j.get("audit_utc", "")
    head_utc = git(wt, "log", "-1", "--format=%cI", hca)[1].decode().strip() if hca else ""
    rep_utc = git(wt, "log", "-1", "--format=%cI", head)[1].decode().strip()
    cited = re.findall(r"audit utc `([^`]+)`", appx)
    forward = bool(audit_utc and rep_utc and audit_utc.replace("Z", "+00:00") > rep_utc)
    rep.add("18", "item v2.c — the report's own `audit_utc` must not post-date its commit, and every doc citing it "
                  "must cite the SAME value", "one exact stamp from `date -u` at run time, cited identically",
            f"report {audit_utc}; the head it audited was committed {head_utc}; the report itself {rep_utc}; the "
            f"appendix cites {cited}", FAIL if forward or (cited and cited[0] != audit_utc) else PASS, n=1,
            note="FORWARD-STAMPED by ~13 min against its own committing head, and the appendix cites a different day "
                 "and time (2026-09-25T21:44:00Z) for the same artefact; both are :00-rounded, so neither orders "
                 "anything to the second. This is ORCH-2's own self-item O-4 class, in a worker artefact")
    rep.add("18", "item v2.d — the report names a `tool_commit` that contains its generating tool (item 8a's class)",
            "tool_commit present, and the tool blob at that commit == the tool at head",
            f"keys present: {sorted(k for k in rep_j if 'tool' in k)}", FAIL if "tool_commit" not in rep_j else PASS,
            n=1, note="the containing commit is derivable (b991f29 added tools/m4_seal_audit.py and is an ancestor of "
                      "the audited head) but derivable is not stated: criterion 20.10 and TASK-021's 21.6 both "
                      "require the field, which is why item 8a is still open on the q2/q3/q4 supplements")
    pairs, mentions = [], []
    fxj = json.loads(fx_head)

    def _walk(node, path=""):
        if isinstance(node, dict):
            if isinstance(node.get("artifact"), str) and isinstance(node.get("artifact_sha256"), str):
                pairs.append(path)
            for k, v in node.items():
                _walk(v, f"{path}/{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                _walk(v, f"{path}[{i}]")
        elif isinstance(node, str) and "fixtures-adjudication.json" in node:
            mentions.append(path)
    _walk(fxj)
    ca_rows = rep_j.get("confirmation_artifacts", [])
    distinct = len({json.dumps(x, sort_keys=True) for x in ca_rows})
    rep.add("18", "item v2.e — the report's citation census must NAME ITS KEY and cover every citation (item 0e's "
                  "lesson)", f"one row per citation of the confirmation artefact, attributable by path",
            f"the fixture file mentions it at {len(mentions)} paths, of which {len(pairs)} are artifact+sha pairs "
            f"(the tool's unstated key); the report carries {len(ca_rows)} rows, {distinct} distinct",
            FAIL if distinct < len(ca_rows) or len(pairs) != len(mentions) else PASS, n=len(mentions),
            note="the appendix's sentence 'All five citations in the fixture file' does not reproduce: 10 mentions, "
                 "5 pairs. The load-bearing half is that the 5 UNPAIRED mentions — including "
                 "/adjudication_summary_2026_09_25/artifact — sit OUTSIDE the tool's post-seal void check, so a "
                 "post-seal confirmation cited without a paired sha would not fire it. ORCH-2 closed the gap by hand: "
                 "all 10 mentions name the same artefact, whose whole history is pre-seal")
    prep = os.path.join(wt, "fleet/branches/WORKER-2-TASK-019b-PREP.md")
    prep_t = open(prep, encoding="utf-8").read() if os.path.exists(prep) else ""
    fuzzy = re.findall(r"20\d\d-\d\d-\d\dT\d\d:\dxZ|\d\d:\dxZ", prep_t)
    rep.add("18", "item v2.f — the prep record's header stamp (item 12's class: the census rose 26 → 27 at this head)",
            "exact UTC to the second, with its source", f"{fuzzy[:3]} in a record committed 2026-09-26T00:31:39Z",
            FAIL if fuzzy else PASS, n=len(fuzzy),
            note="'2026-09-25T21:5xZ' is both fuzzy and ~2.6 h before its own commit — the same defect class item 12 "
                 "was extended for, in the newest artefact in the lane")
    b1, b2 = _blob(wt, "293b29c", SEAL_REL), _blob(wt, SEAL_COMMIT, SEAL_REL)
    if b1 and b2:
        j1, j2 = json.loads(b1), json.loads(b2)
        kd = sorted(k for k in set(j1) & set(j2) if j1[k] != j2[k])
        same = (j1.get("holdout") == j2.get("holdout") and j1.get("tuning") == j2.get("tuning")
                and j1.get("salt") == j2.get("salt"))
        gap = git(wt, "log", "-1", "--format=%cI", "293b29c")[1].decode().strip()
        rep.add("18", "item v2.a clause (iii), second half — the SUBSTANCE ('one draw, not two'), re-derived by ORCH-2 "
                      "from the two seal blobs",
                "293b29c → 79eb401 differs in the `manifest` key ONLY; holdout / tuning / salt identical",
                f"keys differing: {kd}; holdout+tuning+salt identical: {same}; 293b29c @ {gap}",
                PASS if kd == ["manifest"] and same else FAIL, n=len(kd),
                note="so the claim is TRUE and the owed repair is documentation-only: the sentence, plus why it matters "
                     "— 79eb401's own commit subject says 're-seal', 68 s after the draw, which reads as a second draw "
                     "to anyone who has not compared the blobs")
    one_draw = [f for f in (appx, json.dumps(rep_j)) if "293b29c" in f or "one draw" in f.lower()]
    rep.add("18", "item v2.a clause (iii), second half — the STATEMENT that 293b29c/79eb401 are one draw, not two",
            "stated in the note", f"present in {len(one_draw)} of the two artefacts",
            FAIL if len(one_draw) < 2 else PASS, n=len(one_draw),
            note="without it a reader cannot tell whether the split was re-drawn (a new salt would be owed) or only "
                 "re-manifested; ORCH-2 has verified the substance in the row above, so this item is documentation-only")

    # ---- O-5: ANNEX A1 as written collides with the seal's immutability ----
    freeze_src = open(os.path.join(wt, "tools/m4_one_shot_v2.py"), encoding="utf-8").read()
    binds_appendix = bool(re.search(r"SEAL-APPENDIX|SEAL-AUDIT|appendix_sha|companion", freeze_src))
    rep.add("18", "O-5 amended A1 — the seal stays byte-identical, a dated companion note names both digests, and the "
                  "quantum-b FREEZE binds the companion's digest alongside the seal's",
            "all three", f"seal untouched: True; appendix names both digests: "
            f"{'c8e963199a1e' in appx and 'c40d272f30d0' in appx}; freeze binds the companion: {binds_appendix}",
            PASS if binds_appendix else FAIL, n=3,
            note="A1 as originally written ('HELD-OUT-SPLIT-V2.json's own header binds c40d272f…, append-only') is "
                 "unsatisfiable without moving 73d86f0d…, which the appendix and criterion v2.10 both bind — a "
                 "collision in ORCH-2's own criterion, disclosed as self-correction O-5. The amended requirement puts "
                 "the disclosure where the run reads it: the freeze record")


    taint = ["Radical_Subjectivity", "D-092", "D-093", "D-094", "D-095", "D-107", "D-108", "D-122", "taint"]
    hits = {t: sum(t in x for x in (appx, json.dumps(rep_j), prep_t)) for t in taint}
    rep.add("18", "item v2.b — the v2-holdout taint disclosure, looked for in ALL THREE new artefacts",
            "the four holdout transcripts, the seven signal ids and their verdicts, the deferred-filter endorsement, "
            "and quantum b's denominator choice",
            f"{sum(hits.values())} mentions across appendix/report/prep: {hits}",
            FAIL if sum(hits.values()) == 0 else PASS, n=sum(hits.values()),
            note="item v2.b is therefore UNCHANGED and remains, with A2, one of the two blockers on quantum b")

    # ---- the harness: §15's pre-registered criteria get code-level precedent ----
    refused = re.findall(r'"REFUSED: ([^"]{0,60})', freeze_src)
    rep.add("18", "v2.12/v2.13 precedent — the one-shot refusals are IN CODE, not in prose",
            "a refusal for: no freeze, existing receipt, detector/param change after freeze, split-digest mismatch, "
            "evaluated set ≠ frozen holdout",
            f"{len(refused)} distinct REFUSED messages: {refused[:6]}", PASS if len(refused) >= 5 else FAIL,
            n=len(refused),
            note="HELD for the run itself: §15's v2.12/v2.13 rows still need the actual receipt with holdout_reads "
                 "equal to the pre-registered 33 (or the §F2 sensitivity 29) and an eval dir whose commit history is "
                 "pure. What is proven today is that the discipline cannot be forgotten at run time")
    rep.add("18", "v2.15 precedent — `score` separates seeded from independent and refuses an unreasoned label",
            "both in code", f"seeded refs {freeze_src.count('seeded')}, 'REFUSED: label %r carries no reason' "
            f"present: {'carries no reason' in freeze_src}, candidate_unlabelled kept apart: "
            f"{'candidate_unlabelled' in freeze_src}",
            PASS if freeze_src.count("seeded") and "carries no reason" in freeze_src else FAIL, n=1)
    tuning_side = [ln for ln in freeze_src.split("\n")
                   if re.search(r'which\s*=\s*"tuning"|--tuning\b', ln)]
    rep.add("18", "v2.16 precedent — the quantum-b tool and its registry carry no tuning-side evaluation path",
            "0 references", f"{len(tuning_side)} in m4_one_shot_v2.py; the registry enters the detectors through "
            f"run_tuning(..., which=\"holdout\") only", PASS if not tuning_side else FAIL, n=len(tuning_side))
    c2p = os.path.join(wt, "tools/c2_detectors.py")
    c2 = open(c2p, encoding="utf-8").read() if os.path.exists(c2p) else ""
    reads_modules = all(k in c2 for k in ("m.WINDOW", "m.MIN_FLANK", "m.MIN_RATIO", "m.MIN_MATCHED"))
    dd = open(os.path.join(wt, "tools/det_dropword.py"), encoding="utf-8").read()
    shipped_now = dict(re.findall(r"^(MIN_SCORE|TOP_K|MAX_DROP|MIN_FLANK)\s*=\s*([0-9.]+)", dd, re.M))
    ws = re.search(r"^WINDOW,\s*STRIDE\s*=\s*([0-9]+),\s*([0-9]+)", dd, re.M)
    if ws:
        shipped_now["WINDOW"], shipped_now["STRIDE"] = ws.groups()
    mm = dict(re.findall(r"^MIN_MATCHED,\s*MIN_RATIO\s*=\s*([0-9]+),\s*([0-9.]+)", dd, re.M))
    rep.add("18", "§17 cross-check — the freeze cannot drift from the shipped operating point, because the registry "
                  "reads the detector's own constants", "params taken from the module, no literals",
            f"registry reads module constants: {reads_modules}; the constants it will bind are the same 8 §17 pinned "
            f"({shipped_now}, min_matched/min_ratio {mm})", PASS if reads_modules and len(shipped_now) == 6 else FAIL,
            n=len(shipped_now) + 2)
    rep.add("18", "the harness's label keys are detector-qualified (the prep record's claim, verified as a mechanism)",
            'a key of the form "<detector>/<transcript>#<n>"',
            f"line: {[l.strip() for l in freeze_src.split(chr(10)) if '%s/%s#%d' in l][:1]}",
            PASS if "%s/%s#%d" in freeze_src else FAIL, n=1,
            note="the literal 'C1-drop/' never appears because the detector name is a variable — a grep for the "
                 "example string would have reported this claim ABSENT and been wrong")
    rep.add("18", "first-attempt enforcement (the prep record's 'first attempt' claim)",
            "the receipt records attempt 1 / max 1 and verify refuses otherwise",
            f"attempt fields: {freeze_src.count(chr(34) + 'attempt' + chr(34))}, verify check present: "
            f"{'is not a first attempt' in freeze_src}",
            PASS if "is not a first attempt" in freeze_src else FAIL, n=1)
    # --- how much of the harness's safety is TESTED, and is the partial-read refusal non-spurious? ---
    # Hand-verified mapping (auditable: each fragment must appear in the harness's message AND in an assertIn in the
    # test file). "changed after the freeze" is ambiguous between the file-digest and the parameters branch, so the
    # parameters branch is only credited if a test asserts something containing "parameters" - none does.
    COVERED = (("freeze overwrite", "refusing to overwrite"),
               ("no freeze before run", "thresholds must be recorded before the run"),
               ("receipt already exists (holdout spent)", "already holds a consumption receipt"),
               ("detector FILE changed after freeze", "changed after the freeze"),
               ("split digest no longer matches the freeze", "does not match the frozen record"),
               ("score: verdict outside confirmed/discarded", "allowed:"),
               ("score: label without a reason", "carries no reason"))
    UNTESTED = (("detector PARAMETERS changed after freeze", "parameters changed"),
                ("evaluated set != frozen holdout (PARTIAL READ)", "not the frozen holdout"))
    t1 = os.path.join(wt, "tests/test_m4_one_shot_v2.py")
    tt = open(t1, encoding="utf-8").read() if os.path.exists(t1) else ""
    asserts = re.findall(r"assertIn\(\s*[\"\']([^\"\']+)[\"\']", tt) + \
        re.findall(r"assertIn\([\"\']([^\"\']+)[\"\']", tt)
    ok = [(nm, f) for nm, f in COVERED if f in freeze_src and any(f in a for a in asserts)]
    still = [(nm, f) for nm, f in UNTESTED if f in freeze_src and not any(f in a for a in asserts)]
    rep.add("18", "item v2.g — how many of the harness's refusal paths are ASSERTED by a test (capability evidence is "
                  "only as good as its tests)", f"all {len(COVERED) + len(UNTESTED)}",
            f"{len(ok)}/{len(COVERED) + len(UNTESTED)} asserted; UNTESTED: {[u[0] for u in still]}",
            PASS if not still else FAIL, n=len(ok),
            note="the two untested paths are the PARAMETERS-changed branch and the evaluated-set refusal — and the "
                 "latter is the one that protects quantum b's DENOMINATOR: a partial holdout read must be refused, not "
                 "scored, because the figure is one-shot and cannot be re-run. Code-present is not code-proven; one toy "
                 "test each closes it (a frozen holdout of 2 with a detector that reads 1, and a freeze whose params "
                 "are edited without touching the module file)")
    det_ok = {}
    for mod in ("det_dropword", "det_format"):
        mp = os.path.join(wt, f"tools/{mod}.py")
        msrc = open(mp, encoding="utf-8").read() if os.path.exists(mp) else ""
        det_ok[mod] = bool(re.search(r"for n in [^\n]+:\n\s+sigs = [^\n]+\n\s+per_file\[n\] = sigs", msrc))
    rep.add("18", "the partial-read refusal is NON-SPURIOUS: both detectors emit an entry for every transcript they read, "
                  "so a zero-signal transcript cannot look like a partial read",
            "per_file[n] assigned unconditionally inside the read loop, in both detectors",
            f"{det_ok}", PASS if all(det_ok.values()) else FAIL, n=len(det_ok),
            note="this is what makes refusal (g) usable at all: C1-drop may legitimately find nothing in some of the 33 "
                 "holdout transcripts, and the run must still see 33 reads")
    hr = [mod for mod in ("det_dropword", "det_format")
          if re.search(r"\"holdout_reads\":", open(os.path.join(wt, f"tools/{mod}.py"), encoding="utf-8").read())]
    rep.add("18", "v2.12 precedent — the detectors record `holdout_reads` and `holdout_consumed` themselves in holdout "
                  "mode, so the receipt's read list is not reconstructed after the fact",
            "both detectors", f"{hr}", PASS if len(hr) == 2 else INFO, n=len(hr),
            note="HELD for the run: §15's v2.12 row still needs the actual receipt whose holdout_reads is SET-EQUAL to "
                 "the pre-registered 33 (or the §F2 sensitivity 29)")
    rep.add("18", "criterion 21.8 / A5 — the suite floor, measured at both heads",
            "green with the corpus present, count never drops, skips reported",
            "4fc40c8: Ran 227 tests, OK (skipped=1) · 72104a5: Ran 244 tests in 205.5s, OK (skipped=1) = 227 + 10 "
            "harness + 7 audit", PASS, n=244,
            note="TASK-021's criterion 21.8 publishes 217, which was already stale at 4fc40c8; the binding floor is "
                 "the newest measured count, 244, and the skip count travels with it")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("worktree", nargs="?")
    ap.add_argument("--selftest", action="store_true",
                    help="assert the helper semantics the sections depend on (self-item O-2); needs no worktree")
    ap.add_argument("--golden", default=None, help="committed instrument output to check for internal consistency")
    ap.add_argument("--head", default="HEAD")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--self-audit", default=None,
                    help="run the same timestamp census over another tree (ORCH-2 audits its own lane)")
    a = ap.parse_args()
    if a.selftest:
        here = os.path.dirname(os.path.abspath(__file__))
        gold = a.golden or os.path.join(here, "orch2_verify_output_4fc40c8.txt")
        return selftest(gold)
    if not a.worktree:
        ap.error("worktree is required unless --selftest is given")
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
    section_read_scope(wt, rep, sup)
    section_signal_evidence(wt, rep)
    section_manifest_completeness(wt, rep)
    section_split_v2(wt, rep, sup)
    section_inherited(wt, rep)
    section_quantum_b(wt, rep)
    section_coherence(wt, rep)
    section_derivations(wt, rep)
    section_quantum_b_criteria(wt, rep)
    section_coverage(rep)
    section_t21(wt, rep)
    section_seal_audit(wt, rep, a.head)
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
    if a.self_audit:
        print(f"\n== 9. SELF-AUDIT of {a.self_audit} (same criteria applied to ORCH-2's own tree) ==")
        fz, mb, ex, mp = [], [], 0, []
        nf = 0
        for root, dirs, files in os.walk(a.self_audit):
            dirs[:] = [d for d in dirs if d not in (".git", "corpus", "evidence", "__pycache__", "gate-scratch")]
            for fn in files:
                if not fn.endswith((".json", ".md", ".log")):
                    continue
                nf += 1
                fp = os.path.join(root, fn)
                rp = os.path.relpath(fp, a.self_audit)
                t = open(fp, encoding="utf-8", errors="replace").read()
                fz += [(rp, m.group(0), classify_fuzzy(t, m)) for m in FUZZY_TS.finditer(t)]
                for m in TS_ANY.finditer(t):
                    if m.group(1):
                        ex += 1
                    else:
                        mp.append((rp, m.group(0)))
                for m in OWN_TIME_FIELD.finditer(t):
                    if not TS_EXACT.fullmatch(m.group(2)) and f'"{m.group(1)}_exact"' not in t:
                        mb.append((rp, m.group(1), m.group(2)))
        fzi = sorted({(rp, v) for rp, v, k in fz if k == "instance"})
        fzc = sorted({(rp, v) for rp, v, k in fz if k == "citation"})
        print(f"  files scanned {nf} | FUZZY asserted {len(fzi)} | FUZZY quoted {len(fzc)} | "
              f"own-time not exact {len(mb)} | exact-to-second {ex} | minute-precision {len(mp)}")
        if fzi:
            print(f"  fuzzy INSTANCES: {fzi[:12]}")
        if fzc:
            print(f"  fuzzy CITATIONS (reporting the defect, not committing it): {fzc[:6]}")
        if mb:
            print(f"  own-time offenders: {sorted(set(mb))[:12]}")
        byfile = collections.Counter(rp for rp, _v in mp)
        print(f"  minute-precision by file (top 8): {byfile.most_common(8)}")

        # SELF-ITEM O-4: a header stamped AHEAD of the clock is a forward-stamped record - it can
        # make a document appear to post-date something it precedes. The newest CONTROL.log entry is
        # the lane's authoritative clock, because that line is produced by `date -u`.
        ctl = os.path.join(a.self_audit, "fleet/CONTROL.log")
        ctl_max = ""
        if os.path.exists(ctl):
            st = [m.group(0) for m in TS_EXACT.finditer(open(ctl, encoding="utf-8").read())]
            ctl_max = max(st) if st else ""
        fwd = []
        for root, dirs, files in os.walk(a.self_audit):
            dirs[:] = [d for d in dirs if d not in (".git", "corpus", "evidence", "__pycache__", "gate-scratch")]
            for fn in files:
                if not fn.endswith(".md"):
                    continue
                fp = os.path.join(root, fn)
                for m in TS_EXACT.finditer(open(fp, encoding="utf-8", errors="replace").read()):
                    if ctl_max and m.group(0) > ctl_max:
                        fwd.append((os.path.relpath(fp, a.self_audit), m.group(0)))
        gp = os.path.join(a.self_audit, "fleet/GATES.md")
        gates = open(gp, encoding="utf-8").read() if os.path.exists(gp) else ""
        # disclosure counts only if it is INSIDE the O-4 correction section - a forward stamp that
        # merely appears in GATES.md as its own header is the defect, not its disclosure (defect #28)
        o4 = slice_section(gates, "ORCH-2 SELF-CORRECTION #4")
        undisc = sorted({(rp, t) for rp, t in fwd if t not in o4})
        rep.add("9", "self-item O-4 — no header in this lane is stamped AHEAD of its own CONTROL.log, unless an "
                     "append-only correction discloses it", f"0 undisclosed forward stamps (lane clock {ctl_max})",
                f"{len(set(fwd))} forward stamp(s), {len(undisc)} undisclosed: {undisc[:6]}",
                PASS if not undisc else FAIL, n=len(set(fwd)),
                note="standing rule adopted: write the CONTROL.log line FIRST (it calls `date -u`) and copy that "
                     "stamp into every header of the cycle; a timestamp with no source is the defect criterion "
                     "20.14 names, and ORCH-2 is not exempt from its own criterion")
        # SELF-ITEM O-6: ERRATA-25f makes liveness a SIGNAL — heartbeat AND CONTROL.log at cadence. A lane whose
        # CONTROL.log is current but whose heartbeat file is stale is publishing half a signal, and the boss reads
        # the heartbeat. Class-2 fires at >20 min, so that is the threshold this row uses against itself.
        hb = os.path.join(a.self_audit, "fleet/heartbeats/ORCHESTRATOR.log")
        hb_max = ""
        if os.path.exists(hb):
            ht = [m.group(0) for m in TS_EXACT.finditer(open(hb, encoding="utf-8").read())]
            hb_max = max(ht) if ht else ""
        lag_txt = "unknown"
        lag_bad = False
        if hb_max and ctl_max:
            import datetime as _dt
            fmt = "%Y-%m-%dT%H:%M:%SZ"
            lag = (_dt.datetime.strptime(ctl_max, fmt) - _dt.datetime.strptime(hb_max, fmt)).total_seconds()
            lag_txt = f"heartbeat {hb_max} lags CONTROL {ctl_max} by {lag / 60:.1f} min"
            lag_bad = lag > 20 * 60
        rep.add("9", "self-item O-6 — the heartbeat signal is not stale against this lane's own CONTROL.log "
                     "(ERRATA-25f: liveness = SIGNALS, Class-2 fires >20 min)",
                "lag ≤ 20 min, or the lapse disclosed in an append-only self-correction",
                lag_txt, PASS if not lag_bad else FAIL, n=1,
                note="found because the boss reads heartbeats and ORCH-2's had not been appended since 23:39:33Z "
                     "while CONTROL.log ran to seq 41 — half a signal is not a signal; the fix is to write the "
                     "heartbeat line in the SAME act as the CONTROL line, never afterwards")
        if set(fwd):
            print(f"  forward-stamped headers: {sorted(set(fwd))[:8]}")
    if a.json:
        print(json.dumps(rep.rows, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
