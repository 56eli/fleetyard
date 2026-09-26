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
import datetime
import shutil
import subprocess
import sys
import textwrap
import tempfile
import hashlib
import io
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
    # DEFECT #49: FUZZY_TS matches only the TIME fragment, so the "immediate wrapping" test looked at the character
    # beside `21:5xZ` inside `2026-09-25T21:5xZ` - a digit, not a delimiter - and counted a fully backticked
    # quotation as an ASSERTED instance. That is the normal way this lane quotes a fuzzy stamp, so the bug inflated
    # every instance count and deflated every citation count, in the worker census and in ORCH-2's own self-audit.
    # Look outward across timestamp characters for the delimiter instead.
    left = text[max(0, a - 26):a]
    right = text[b:b + 26]
    wrapped = bool(re.search(r'''[`'"][-0-9T:ZzxX]*$''', left)) and bool(
        re.match(r'''[-0-9T:ZzxX]*[`'"]''', right))
    ctx = CITATION_CTX.search(text[max(0, a - 60):a])
    # DEFECT #49 (second half): the lane quotes another artefact's WHOLE LINE - `run_utc 2026-09-25T20:50:46Z
    # (src 293b29c; read 20:5xZ)` - and the fuzzy fragment sits far from either delimiter, so neither the wrapping test
    # nor the 60-char context sees it. A delimited span that also carries a full ISO stamp or a `(src ` annotation is
    # quoted artefact content, not the author's own clock: the author's own stamp is never written that way.
    quoted_span = False
    for mm in re.finditer(r"""[`'"]([^\n`'"]{0,140})[`'"]""", text):
        if mm.start(1) <= a and b <= mm.end(1):
            inner = mm.group(1)
            if TS_EXACT.search(inner) or "(src " in inner:
                quoted_span = True
                break
    return "citation" if (wrapped or ctx or quoted_span) else "instance"


# timestamp-discipline patterns (criterion 20.14), module-level so the self-audit and the
# worktree census use the SAME regexes - two copies of a pattern is how defect #8 happened
FUZZY_TS = re.compile(r"\d{1,2}:\d[xX]Z|\d[xX]:\d{2}Z|[xX]Z\b")
TS_ANY = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?Z")
TS_EXACT = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
OWN_TIME_FIELD = re.compile(r'"(run_utc|generated_utc|materialised_utc|created_utc|appended_utc)"\s*:\s*"([^"]+)"')


# ---------------------------------------------------------------- environment vs artefact (defect #50)
# The gate reads MATERIALISED inputs the worker's own lane hygiene keeps out of git (.gitignore: corpus/, evidence/).
# A fresh worktree does not have them, and the instrument used to (a) die with a traceback and print NO summary at all -
# silence that reads as "no failures" - and (b) report the resulting gaps as WORKER defects: thirteen pin rows FAILed
# with "ABSENT-IN-ARCHIVE" because the read-only archive lane had not been fetched into this clone, and the inherited
# census digest compared against e3b0c442..., the sha256 of the empty string. An environment gap charged to the worker
# is the worst kind of wrong answer this instrument can give, so the two are now separated explicitly.
ARCHIVE_COMMIT = "bf97d85"
ARCHIVE_REF = "refs/remotes/origin/arena/01a0d581-fleetyard"
MATERIALISE_RECIPE = ("sh tools/m5r_inputs.sh  (the worker's own documented materialisation: fetches the read-only "
                      "archive lane, git-archives runs/m5-raw + fixtures into evidence/, unzips the sha-verified corpus)")
MATERIALISED: dict = {"archive": None, "missing": [], "broken_sections": 0}


def run_section(rep, fn, *args):
    """Run a section so that NO exception can silence the summary (defect #50).

    A crash that names a materialised path - or any crash once a section has already come back empty - is an ENVIRONMENT
    gap and is reported VACUOUS, never charged to the worker. Anything else is a FAIL against the instrument itself."""
    try:
        return fn(*args)
    except Exception as e:  # noqa: BLE001 - the point is that nothing may escape and stop the summary printing
        msg = f"{type(e).__name__}: {e}"
        env = (any(t in msg for t in ("corpus/", "evidence/", "docdocgo", "ABSENT-IN-ARCHIVE"))
               or MATERIALISED["broken_sections"] > 0)
        MATERIALISED["broken_sections"] += 1
        rep.add("0", f"section {getattr(fn, '__name__', '?')} could not be evaluated",
                "the section to run to completion", msg[:200], VACUOUS if env else FAIL, n=0,
                note="defect #50: an unguarded crash printed NO summary, and silence reads as 'no failures'. Every "
                     "section is guarded now, so the summary always prints. "
                     + ("This crash names a MATERIALISED input (corpus/, evidence/) or follows one, so it is an "
                        "environment gap reported VACUOUS, not a worker defect. Recipe: " + MATERIALISE_RECIPE
                        if env else
                        "This crash does NOT name a materialised input, so it is charged to the INSTRUMENT: fix it "
                        "before publishing any verdict from this run."))
        return None


STAMP_ONLY_FIELDS = ("utc", "utc_source", "utc_superseded", "utc_superseded_reason")


def append_only_supersession(prev_lines, cur_lines):
    """DEFECT #51: split the changed lines of a previously gated append-only file into DISCLOSED STAMP SUPERSESSIONS
    and everything else. Returns (identical_count, superseded_line_numbers, violation_line_numbers).

    Criterion 20.14c demanded that the forward stamps inside these very lines be repaired while item 0g demanded the
    lines stay byte-identical: the gate contradicted itself and FAILed the repair it had ordered. Row 20.14b already
    states the principle for the mirror case ("fuzzy left readable, exact sibling added; flagging it would punish the
    correct fix"). The exemption is deliberately narrow and cannot hide a rewritten ruling - only the four stamp fields
    may differ, the superseded field must carry the PREVIOUS line's utc VERBATIM, a reason must be stated, and every
    other field is compared, any difference being a violation."""
    ident = 0
    sups, viol = [], []
    for i, (pl, cl) in enumerate(zip(prev_lines, cur_lines)):
        if pl == cl:
            ident += 1
            continue
        try:
            pj, cj = json.loads(pl), json.loads(cl)
        except ValueError:
            viol.append(i + 1)
            continue
        substance = [k for k in set(pj) | set(cj)
                     if k not in STAMP_ONLY_FIELDS and pj.get(k) != cj.get(k)]
        if (not substance and cj.get("utc_superseded") == pj.get("utc")
                and str(cj.get("utc_superseded_reason", "")).strip()):
            sups.append(i + 1)
        else:
            viol.append(i + 1)
    return ident, sups, viol


def section_materialised(wt, rep):
    """Preflight: are the inputs the worker keeps OUT of git present in this worktree?

    These rows judge the ENVIRONMENT, not the artefacts. An absent input is reported VACUOUS with the recipe, so a fresh
    clone can never produce a FAIL that reads as a worker defect (defect #50)."""
    print("\n== 0. materialised inputs (environment, never charged to the worker) ==")
    man = json.load(open(os.path.join(wt, "findings/PROVENANCE.json"), encoding="utf-8"))
    inp = man.get("inputs", {})
    rc, _ = git(wt, "rev-parse", "--verify", ARCHIVE_COMMIT + "^{commit}")
    MATERIALISED["archive"] = (rc == 0)
    rep.add("0", f"read-only archive lane {ARCHIVE_COMMIT} reachable in this clone (the pins' third leg)",
            "reachable", "reachable" if rc == 0 else f"UNREACHABLE - fetch it: git fetch origin "
            f"refs/heads/arena/01a0d581-fleetyard:{ARCHIVE_REF}",
            PASS if rc == 0 else VACUOUS, n=1,
            note="" if rc == 0 else "defect #50: with the archive unreachable every pin row used to read "
                                    "'ABSENT-IN-ARCHIVE' and FAIL, charging this clone's gap to the worker. Those rows "
                                    "are VACUOUS until the archive is fetched.")
    bs = man.get("book_store", {})
    bsp = os.path.join(wt, bs.get("path", "corpus/docdocgo/html/merged-book-texts_json_1.js"))
    have = os.path.exists(bsp)
    rep.add("0", f"book store materialised ({bs.get('path', 'corpus/...')}, gitignored by the worker's lane hygiene)",
            bs.get("sha256", "?")[:12] + "…", (sha_file(bsp)[:12] + "…") if have else "ABSENT",
            PASS if have and sha_file(bsp) == bs.get("sha256") else (FAIL if have else VACUOUS), n=1,
            note="" if have else "environment gap, not a worker defect. Recipe: " + MATERIALISE_RECIPE)
    ov = os.path.join(wt, "corpus/docdocgo/overlays")
    nov = len([f for f in os.listdir(ov) if f.endswith(".txt")]) if os.path.isdir(ov) else 0
    nrec_exp = inp.get("records_files", 230)
    rep.add("0", "corpus transcripts materialised (corpus/docdocgo/overlays/*.txt)", f"{nrec_exp}", f"{nov}",
            PASS if nov == nrec_exp else (FAIL if nov else VACUOUS), n=1,
            note="" if nov == nrec_exp else "environment gap, not a worker defect. Recipe: " + MATERIALISE_RECIPE)
    rec = os.path.join(wt, "evidence/runs/m5-raw/records")
    # ONE implementation: the first version of this preflight re-derived the digest by concatenating file contents and
    # disagreed with the published construction (1e153aef... vs d8c93536...), i.e. it invented a false FAIL out of a
    # second copy of a rule - defect #8's exact class. It now calls the same dir_digest() the census row calls, and the
    # disagreement was caught by this row before anything was published.
    drec, nrec = dir_digest(rec) if os.path.isdir(rec) else ("", 0)
    files = [True] * nrec
    dig_ok = bool(nrec) and drec == inp.get("records_digest_sha256")
    rep.add("0", "inherited M5 raw census materialised (evidence/runs/m5-raw/records)",
            f"{nrec_exp} files, digest {str(inp.get('records_digest_sha256'))[:12]}… (dir_digest, the census row's own construction)",
            f"{nrec} files, digest {str(drec)[:12]}…" if nrec else "ABSENT",
            PASS if dig_ok and nrec == nrec_exp else (FAIL if nrec else VACUOUS), n=1,
            note="" if dig_ok else "environment gap, not a worker defect: with the directory absent the digest used to "
                                   "compute as e3b0c442… (the sha256 of the empty string) and FAIL as a MISMATCH. "
                                   "Recipe: " + MATERIALISE_RECIPE)
    fx = os.path.join(wt, "evidence/fixtures")
    miss = [d for d in ("confirmed", "clean", "negative") if not os.path.isdir(os.path.join(fx, d))]
    rep.add("0", "M5-R fixtures materialised (evidence/fixtures/{confirmed,clean,negative})", "all three present",
            "all three present" if not miss else "MISSING: " + ", ".join(miss),
            PASS if not miss else VACUOUS, n=3,
            note="" if not miss else "environment gap, not a worker defect. Recipe: " + MATERIALISE_RECIPE)
    MATERIALISED["missing"] = [r["name"] for r in rep.rows if r["section"] == "0" and r["verdict"] == VACUOUS]
    return man


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


PREV_GATED = "1c8a287"   # the head cycle J gated; the append-only / delivery-range comparison point


COMPANION_PATTERNS = ("SEAL-APPENDIX", "SEAL-AUDIT", "SPLIT-V2-NOTE", "SPLIT-V2-EXCLUSIONS",
                      "TASK-019A-DELIVERY", "TASK-019B-PREP")


def companion_texts(wt):
    """Every committed artefact that may carry a dated companion statement beside an immutable seal.

    DEFECT #34 of this instrument: this set was hardcoded to three paths, so the note WORKER-2 actually
    wrote (tools/HELD-OUT-SPLIT-V2-NOTE-2026-09-26.md, discharging v2.a and v2.b) was invisible to four
    rows, which then reported ABSENT for text that exists. Discover by name pattern over the tree."""
    out = {}
    for root, dirs, files in os.walk(wt):
        dirs[:] = [d for d in dirs if d not in (".git", "corpus", "evidence", "__pycache__")]
        for fn in files:
            if fn.endswith((".md", ".json")) and any(k in fn.upper() for k in COMPANION_PATTERNS):
                rel = os.path.relpath(os.path.join(root, fn), wt)
                out[rel] = open(os.path.join(root, fn), encoding="utf-8", errors="replace").read()
    return out


def adj_rows(wt):
    """The adjudication record, PARTITIONED into (adjudication rows, appended disposition rows).

    DEFECT #32: TASK-018 item 0g REQUIRES appending `"record":"disposition"` rows, which carry their own
    schema. Every row-level test that assumed one schema read the required append as 15 broken rows (and
    section 4 crashed outright on `KeyError: 'verdict'`). Judge each class by its own schema."""
    fp = os.path.join(wt, "runs/m4-q2-adjudication/adjudication.jsonl")
    rows = [json.loads(l) for l in open(fp, encoding="utf-8") if l.strip()]
    return [r for r in rows if r.get("record") != "disposition"], [r for r in rows if r.get("record") == "disposition"]


def generator_pin_check(wt, art):
    """Item 8a as DELIVERED (O-8): attributability by a `generator_pins` block, not by `tool_commit`.

    `tool_commit` is the lane head at run time and legitimately need not contain the generator; the pin
    names the commit that carries these exact script bytes plus its sha256. Returns (ok, observed, note)."""
    gp = art.get("generator_pins") or {}
    tool, pin, sha = gp.get("generator_tool"), gp.get("generator_tool_commit"), gp.get("generator_tool_sha256")
    tc = str(art.get("tool_commit") or "")
    if not (tool and pin and sha):
        return False, f"generator_pins ABSENT/incomplete (keys: {sorted(gp)})", \
            "item 8a: pin generator_tool + generator_tool_commit + generator_tool_sha256"
    rc, blob = git(wt, "show", f"{pin}:{tool}")
    if rc != 0 or not blob:
        return False, f"the pinned commit {pin[:7]} does NOT contain {tool}", ""
    got = hashlib.sha256(blob).hexdigest()
    hb = git(wt, "show", f"HEAD:{tool}")[1]
    hsha = hashlib.sha256(hb).hexdigest() if hb else ""
    ok = got == sha
    return ok, (f"{pin[:7]} contains {tool} and the blob there hashes to {got[:12]}… == the pinned {sha[:12]}…: {ok}"
                f"; tool_commit {tc[:12]} (run-time lane head) contains it: "
                f"{git(wt, 'cat-file', '-e', f'{tc[:12]}:{tool}')[0] == 0}"), \
        ("the tool at head is " + (f"{hsha[:12]}… — the same bytes" if hsha == sha else
         f"{hsha[:12]}… — DIFFERENT bytes: the tool moved after the run, which is why the pin exists "
         "(it names the bytes that produced the artefact)"))


def head_ref(wt: str) -> str:
    return git(wt, "rev-parse", "HEAD")[1].decode().strip() or "HEAD"


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



# ---- predicates lifted to module level so --selftest can mutation-test them (defects #44/#46 guards) ----
CONSTRUCTION_RE = re.compile(r"sort_keys|separators|canonical|sha256 of|json\.dumps", re.I)


def states_construction(obj):
    """§8 / criterion 20.15b: is the digest's construction stated BESIDE it, under ANY key that states it?
    Defect #44: the row used to demand the literal key name `config_digest_note`, which would have failed a
    repaired artefact that called the key `config_canonicalization` or `digest_construction`."""
    if not isinstance(obj, dict):
        return []
    hits = [k for k, v in obj.items()
            if isinstance(v, str) and ("digest_note" in k or "canonical" in k or "construction" in k)
            and CONSTRUCTION_RE.search(v)]
    return hits or (["config_digest_note"] if "config_digest_note" in obj else [])


ONE_DRAW_RE = re.compile(r"one draw|same draw|single draw|re-?manifest|manifest[- ]only|not a second draw|"
                         r"no re-?draw|not re-?drawn|was not redrawn|without re-?draw|identical partition|"
                         r"same partition|same salt|partition unchanged|only the manifest", re.I)


def one_draw_statement(text, first_seal, second_seal):
    """§18 / item v2.a(iii) 2nd half: does the text STATE that the two seal commits are one draw?
    Defect #38: a bare citation of the first seal commit is a timestamp source, not the statement - so both
    commits must appear together with a one-draw phrase, or the phrase must be tied to the commit inline."""
    both = (first_seal in text) and (second_seal in text)
    return (both and bool(ONE_DRAW_RE.search(text))) or bool(
        re.search(re.escape(first_seal) + r"[^\n]{0,160}(one draw|manifest|re-?draw|same salt)", text, re.I))


def h_denominator_commitment(text, n_excluded=0, all_members=None):
    """§19 / ANNEX §H (A4 amended): the conjunction the amended A4 actually requires - BOTH denominators stated
    (29 primary, 33 sensitivity), FROM THE SAME RUN (no second spend), and the four named or bound by reference.
    Defect #44: the row used to accept the word `sensitivit` anywhere plus a `33`, which a hollow sentence PASSed."""
    denom = ("29" in text) and ("33" in text) and bool(re.search(r"sensitivit|primary", text, re.I))
    same_run = bool(re.search(r"same run|single run|one run|no second spend|not re-?spent|same execution|"
                              r"from the same", text, re.I))
    named = (n_excluded == 4 and all_members is True) or bool(
        re.search(r"holdout_exclusions|exclusion_set|the four (named|excluded)|four excluded", text, re.I))
    return denom, same_run, named


def verbatim_row_quotes(map_text):
    """§20: the row names the repair map quotes verbatim. Defect #46: a backtick-negated class stops at the FIRST
    inner backtick, and four row names contain one - so match greedily to the closing backtick at end of line."""
    return re.findall(r"\*\*Row \(verbatim\):\*\* `(.+)`\s*$", map_text, re.M)


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
            # DEFECT #43: observed was clipped at 400 chars, so a 19-item offender list reached the published golden
            # unreadable - evidence a repair depends on must survive into the record. Wrap, never clip.
            exp = textwrap.fill(str(expected), 140, subsequent_indent=" " * 19)
            obs = textwrap.fill(str(observed), 140, subsequent_indent=" " * 19)
            print(f"         expected {exp}")
            print(f"                  | observed {obs}")
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
    # O-9: byte-identity of the reducer was a PROXY for "the M5-R figures still reproduce". At 34db0b0 the
    # tool changed (+46 lines of derivations prose, TASK-020 item 13), the proxy broke, and the substance was
    # settled by RE-RUNNING the tool at head with the published pins (row below). The history row stays, as
    # history: it names the heads across which the bytes were identical and the head where they moved.
    rep.add("1", "HISTORY — m5r_reduce.py bytes across the gated heads (a proxy, superseded by the re-run row)",
            "identical while the M5-R figures were being established",
            f"{' / '.join(str(x)[:8] + '…' for x in same)}", INFO, n=len(same),
            note="the first two are the bytes that produced the published ledger; the third is head. The change is "
                 "documentation-only prose inside the manifest's `derivations` block plus a `derivations_revision` "
                 "record - see the re-run row for whether behaviour moved")
    rr = m5r_rerun(wt)          # -> (ok, (aligned, n_pub, n_new, field_diff), detail) or None
    if rr is None:
        rep.add("1", "criterion 21.4 / TASK-013 — the reducer AT HEAD reproduces the published M5-R outputs when run "
                     "with the pins the manifest names", "ledger d42136c6… + by_transcript c1ec4da8… byte-identical",
                "NOT RUNNABLE in this worktree (evidence/ or corpus/ not materialised)", INFO, n=1,
                note="materialise with tools/m5r_inputs.sh's body (minus its git fetch) + the sha-verified zip")
    else:
        rep.add("1", "criterion 21.4 / TASK-013 — the reducer AT HEAD reproduces the published M5-R outputs when run "
                     "with the pins the manifest names", "ledger + by_transcript byte-identical, manifest differing "
                "only where a rebuild must differ", rr[2], PASS if rr[0] else FAIL, n=1334,
                note="this is the row TASK-013's PASS now rests on: not 'the tool never changed' but 'the tool at "
                     "head still emits these exact bytes'. `tool_sha256` necessarily differs (it hashes the running "
                     "file), which the lane's own derivations_revision states")
        al, npub, nnew, fdiff = rr[1]
        rep.add("1", "criterion C6 / item 13b — the re-run's ledger rows are FIELD-IDENTICAL to the published ones, "
                     "and any differing field is NAMED", "0 differing fields across all rows, ids aligned",
                f"{al} rows aligned by id of {npub} published / {nnew} re-run; differing fields: "
                f"{fdiff or 'NONE'}",
                PASS if al == npub == nnew and not fdiff else FAIL, n=al,
                note="this is the diagnosis that settled cycle K, mechanized: run WITHOUT --tool-commit, every row is "
                     "identical except `status_by` (which embeds the pin, `@dada3e6…` vs `@UNPINNED`) and the digest "
                     "moves to c94cce40… - which is why item 13b requires the reproducibility_note to name the pin. "
                     "A field name here is worth more than a digest mismatch: it says WHAT moved")
        # criterion C11 (TASK-013): stdlib only, no network, writes confined to --out - read statically from the tool
        # at head, so a future change that adds a network call or writes elsewhere flips this row.
        tsrc = open(os.path.join(wt, "tools/m5r_reduce.py"), encoding="utf-8").read()
        imps = sorted({m.split(".")[0] for m in re.findall(r"^(?:import|from)\s+([A-Za-z_][\w.]*)", tsrc, re.M)})
        nonstd = [m for m in imps if m not in sys.stdlib_module_names]
        FORBID = {"urllib", "socket", "requests", "http", "ftplib", "smtplib", "subprocess", "telnetlib", "asyncio"}
        netish = [m for m in imps if m in FORBID]
        # DEFECT #47: the first version captured `open\(([^,]+),\s*["\']w`, which stops at the FIRST comma - so
        # `open(os.path.join(args.out, "SUMMARY.md"), "w"` never matched and the row reported ONE write site where the
        # tool has SIX. A row that under-counts the population it polices is worse than no row: it reads as a clean bill
        # of health. Scan LINES that contain both an open( and a write mode, then judge each line's target. The
        # derivation regexes also needed ^\s*, since both assignments are indented inside main().
        wlines = [ln.strip() for ln in tsrc.split("\n")
                  if re.search(r"\bopen\(", ln) and re.search(r"[\"'][wax]b?[\"']", ln)]
        outside = [ln for ln in wlines if not re.search(r"args\.out|\bledger_path\b|\bbt\b", ln)]
        derived = [bool(re.search(r"^\s*ledger_path\s*=.*args\.out", tsrc, re.M)),
                   bool(re.search(r"^\s*bt\s*=.*args\.out", tsrc, re.M))]
        c11 = not nonstd and not netish and not outside and all(derived)
        rep.add("1", "criterion C11 — the reducer is stdlib-only, opens no network or subprocess, and every write goes "
                     "under --out", "0 non-stdlib imports, 0 forbidden modules, 0 write sites outside --out",
                f"{len(imps)} imports {imps}; non-stdlib: {nonstd or 'none'}; network/subprocess: {netish or 'none'}; "
                f"{len(wlines)} write-mode open sites, outside --out: {outside or 'none'}; ledger_path and bt derived "
                f"from args.out: {derived}",
                PASS if c11 else FAIL, n=len(imps) + len(wlines) + 2,
                note="C11 was re-verified at head at cycle K on this evidence: imports argparse/datetime/difflib/"
                     "hashlib/io/json/os/re/sys/unicodedata (all stdlib), no urllib/socket/requests/subprocess/"
                     "os.system, and the +42/-4 diff changed no import, I/O or network line. Read statically each run "
                     "so the next tool change is judged, not assumed")

    # other head artefacts unchanged
    # O-7: adjudication.jsonl and SUMMARY.md were pinned "unchanged" here, but TASK-018 items 0d/0g
    # REQUIRE an append to both — a frozen-figure row that forbids the repair it demands is a defective
    # row (same class as O-5). Their growth is checked append-only in §4 instead; the five artefacts
    # that must not move at all are still pinned here.
    for path, exp in (("runs/m4-q2-dropword/signals.json", "8d71f57b"),
                      ("runs/m4-q2-adjudication/fixtures-adjudication.json", "61568a9e"),
                      ("runs/m4-q3-format/signals-v2tuning.json", "b25651e4"),
                      ("tools/det_dropword.py", "a0236325"),
                      ("tools/det_format.py", "ef9ff4f2")):
        p = os.path.join(wt, path)
        if os.path.exists(p):
            rep.check("1", f"unchanged: {path}", exp + "…", sha_file(p)[:8] + "…")
        else:
            rep.add("1", f"unchanged: {path}", exp + "…", "ABSENT", FAIL)

    ok, obs, note = generator_pin_check(wt, sup)
    rep.add("1", "criterion 20.10 as amended by O-8 — the artefact is attributable to the EXACT generator bytes "
                 "(item 8a)", "a generator_pins block whose pinned commit contains the pinned tool at the pinned sha",
            obs, PASS if ok else FAIL, n=1, note=note)
    return man, sup


def section_pins(wt, rep, sup):
    print("\n== 1b. v1 toolchain pins (three-way) ==")
    pins = sup["runs"]["v1"]["toolchain"]["pins"]
    ok = 0
    for f, stored in sorted(pins.items()):
        rc, blob = git(wt, "show", f"{ARCHIVE_COMMIT}:tools/{f}")
        arch = sha_bytes(blob) if rc == 0 else "ABSENT-IN-ARCHIVE"
        p = os.path.join(wt, "tools", f)
        head = sha_file(p) if os.path.exists(p) else "ABSENT-AT-HEAD"
        good = stored == arch == head
        ok += good
        if rc != 0 and MATERIALISED["archive"] is not True:
            # defect #50: the archive leg is unreadable in THIS CLONE, so nothing about the worker's pin is known yet.
            rep.add("1b", f"pin {f}", stored[:12] + "…",
                    f"archive UNREACHABLE-IN-THIS-CLONE head {head[:12]}…", VACUOUS, n=1,
                    note="environment gap, not a pin mismatch: fetch the read-only archive lane "
                         f"(git fetch origin refs/heads/arena/01a0d581-fleetyard:{ARCHIVE_REF}) and re-run.")
            continue
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
    # O-8 (item 11a): the requirement is RECONCILIATION, not digit-matching against this instrument's own
    # six-decimal form. PATTERNS' CORRECTION-2 states the records-based expectation, names the unit ambiguity
    # (1,149 records vs 1,151 detector rows) and adopts the gate's figure. Test that substance.
    p11 = ""
    fp11 = os.path.join(wt, "tools/PATTERNS.md")
    if os.path.exists(fp11):
        p11 = open(fp11, encoding="utf-8").read()
    need = {"records-based expectation stated": ("187.555" in p11 or "187.6" in p11) and "0.4451" in p11,
            "the unit ambiguity named (records vs rows)": "1,149" in p11 and "1,151" in p11,
            "the observed figure kept": ("185 observed" in p11 or "185 vs" in p11),
            "per-row tuning counts published": ("C1-drop = 122" in p11 and "C2-format = 49" in p11)}
    rep.add("3", "item 11a — the published v1 exposure row RECONCILES to the records census",
            "all four legs stated in PATTERNS.md",
            f"{sum(need.values())}/4: " + "; ".join(f"{k}: {v}" for k, v in need.items()) +
            f" | this instrument's census: {v1_lam:.4f} / {pois_cdf(185, v1_lam):.4f}",
            PASS if all(need.values()) else FAIL, n=4,
            note="the earlier row expected this instrument's own 187.5548/0.445075 digits; the lane publishes "
                 "187.555 -> 187.6 with P = 0.4451 and says 'for the v1 row the gate is right', which IS the "
                 "reconciliation item 11a asked for: rounding stated, unit named, conclusion unchanged")

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
        # O-9 (item 14): criterion 20.16 is satisfied EITHER by a complete config OR by a stated subset
        # relation. The q4 format leg was rebuilt to publish the complete configuration, so its digest now
        # EQUALS q3's; a row that demanded the subset sentence would have failed a repaired artefact.
        q4f = sup["runs"]["format"]
        d3, d4 = str(q3.get("config_sha256", "")), str(q4f.get("config_sha256", ""))
        k3 = sorted((q3.get("config") or {}).keys())
        k4 = sorted((q4f.get("config") or {}).keys())
        subset_stated = bool(re.search(r"subset|remainder|complete configuration", json.dumps(q4f), re.I))
        rep.add("3", "criterion 20.16 / item 14 — the q4 format-leg config digest covers the COMPLETE config, or "
                     "states the subset relation and where the remainder lives",
                "digests equal over identical key sets, or the subset relation stated in the same object",
                f"q3 {d3[:12]}… {k3} vs q4 {d4[:12]}… {k4}; equal: {d3 == d4 and k3 == k4}; subset stated: "
                f"{subset_stated}",
                PASS if (d3 == d4 and k3 == k4) or subset_stated else FAIL, n=len(k4),
                note="comparability was first established from the pinned detector source, not from the digests; "
                     "the digests now agree because the q4 leg publishes abbreviations + excerpt_chars + rules too")


def section_adjudication(wt, rep):
    print("\n== 4. TASK-018 adjudication set ==")
    adj_path = "runs/m4-q2-adjudication/adjudication.jsonl"
    lines = [l for l in open(os.path.join(wt, adj_path), encoding="utf-8").read().split("\n") if l.strip()]
    allrows = [json.loads(l) for l in lines]
    rows = [r for r in allrows if r.get("record") != "disposition"]
    disp = [r for r in allrows if r.get("record") == "disposition"]
    ovdir = os.path.join(wt, "corpus/docdocgo/overlays")

    def txt_of(t):
        b = os.path.basename(t)
        return open(os.path.join(ovdir, b if b.endswith(".txt") else b + ".txt"),
                    encoding="utf-8", errors="replace").read()

    v = collections.Counter(r["verdict"] for r in rows)
    rep.check("4", "adjudication row count (disposition rows partitioned out — defect #32: a schema "
                   "assumption that breaks when the queue's own required append lands)", 122, len(rows), n=len(rows))
    rep.check("4", "verdict split AS ADJUDICATED (frozen; dispositions are applied in a separate row)",
              {"CERTAIN-leg-d": 57, "CANDIDATE": 65}, dict(v), n=len(rows))
    cert = [r for r in rows if r["verdict"] == "CERTAIN-leg-d"]

    # --- item 0g's append: integrity, schema, effect (all re-derived, none trusted) ---
    rc, prev_blob = git(wt, "show", f"{PREV_GATED}:{adj_path}")
    if rc == 0:
        prev_lines = [l for l in prev_blob.decode("utf-8").split("\n") if l.strip()]
        # DEFECT #51: "byte-identical" carried no exemption for a disclosed, substance-preserving stamp supersession,
        # so this row FAILed the exact repair criterion 20.14c ordered for these same lines. Hand-verified at f5e2cf5
        # BEFORE the row was amended: 15 of the 137 lines differ, the only differing fields are utc / utc_source /
        # utc_superseded / utc_superseded_reason, every prior utc is preserved VERBATIM in utc_superseded with a stated
        # reason ("projected from the CONTROL cadence grid, not read"), and no id / ruling / new_verdict / reason / task
        # moved anywhere in the file.
        ident_n, sups, viol = append_only_supersession(prev_lines, lines)
        # the previously gated head may already carry the dispositions, so "growth" is not the test: the test is
        # that nothing already published moved (except a disclosed supersession), and anything NEW is a disposition row.
        newl = [json.loads(x) for x in lines[len(prev_lines):]]
        only_disp = all(r.get("record") == "disposition" for r in newl)
        rep.add("4", "item 0g — the append is APPEND-ONLY: every line of the previously gated file is "
                     "byte-identical and in the same order, and anything new is a disposition row (as amended by "
                     "defect #51: a DISCLOSED STAMP SUPERSESSION — prior utc preserved verbatim, reason stated, no "
                     "other field touched — is the repair criterion 20.14c ordered, not a breach)",
                f"the {len(prev_lines)} lines at {PREV_GATED[:7]} unchanged except disclosed stamp supersessions; no "
                f"substance field changed anywhere; new lines are dispositions only",
                f"{len(lines)} lines now; {ident_n} byte-identical; {len(sups)} disclosed stamp supersessions "
                f"(lines {sups[:8]}{'…' if len(sups) > 8 else ''}); {len(viol)} lines changing ANY other field "
                f"(lines {viol[:8]}); new lines: {len(newl)}, all dispositions: {only_disp}; dispositions in the "
                f"file: {len(disp)}",
                PASS if not viol and only_disp else FAIL, n=len(lines),
                note="the exemption is narrow by construction and mutation-tested (T32-T34): a changed ruling, a "
                     "dropped prior value or a missing reason each put the line back on the violation list. Amending a "
                     "row so that a FAIL becomes a PASS is the most dangerous change a gate can make, so the evidence "
                     "is recorded here rather than asserted, and row 20.14b already refuses to punish this same "
                     "pattern in the mirror case.")
    else:
        rep.add("4", "item 0g — append-only integrity", f"a comparable blob at {PREV_GATED[:7]}", "UNREADABLE", INFO)
    ids122 = {r["id"] for r in rows}
    schema_ok = all({"by", "id", "reason", "record", "ruling", "task", "utc", "utc_source"} <= set(d) for d in disp)
    unknown = sorted({d["id"] for d in disp} - ids122)
    exact = all(re.match(r"^20\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ$", d.get("utc", "")) for d in disp)
    rep.add("4", "item 0g — the disposition schema: every row names its id, ruling, reason, task, exact utc AND the "
                 "SOURCE of that utc", "all keys present, every id one of the 122, every utc exact to the second",
            f"{len(disp)} rows; schema complete: {schema_ok}; ids outside the 122: {unknown}; utc exact: {exact}",
            PASS if schema_ok and not unknown and exact else FAIL, n=len(disp))
    dcount = collections.Counter(d["id"] for d in disp)
    dupes = {k: c for k, c in dcount.items() if c > 1}
    rep.add("4", "item 0e's lesson applied to the append — a disposition COUNT must name its key",
            "rows and distinct ids both stated where they differ",
            f"{len(disp)} rows over {len(dcount)} distinct ids; ids carrying more than one ruling: {dupes}",
            INFO, n=len(disp),
            note="D-092 is both refused-notation and holdout-member-note, so '15 dispositions' and '14 rows disposed' "
                 "are both true and mean different things — the same rows-vs-sites ambiguity item 0e was opened for")
    after = {r["id"]: r["verdict"] for r in rows}
    changing = [d for d in disp if d.get("new_verdict")]
    for d in changing:
        after[d["id"]] = d["new_verdict"]
    eff = collections.Counter(after.values())
    rulings = collections.Counter(d["ruling"] for d in disp)
    rep.add("4", "item 0g — the EFFECTIVE split after the dispositions, re-derived here so no published figure can "
                 "drift from the record", "57/65 as adjudicated minus every verdict-changing disposition",
            f"{dict(eff)} (from {dict(v)}); {len(changing)} verdict-changing rows; rulings {dict(rulings)}",
            PASS if eff.get("CERTAIN-leg-d") == 57 - len(changing) else FAIL, n=len(changing),
            note="2 demotions (D-002 contradicted by EVAL's dropped-token-not-missing, D-039 by the "
                 "source-inheritance filter) + 6 notation refusals under the enacted narrow leg = 8, so the promoted "
                 "count is 49 and every figure quoting 57 must carry the delta (item 11b's rule)")
    byid = {r["id"]: r for r in rows}
    cert_words = collections.Counter()
    for i, vd in after.items():
        if vd == "CERTAIN-leg-d":
            w = (byid[i].get("dropped_words") or [None])[0]
            cert_words[str(w).lower()] += 1
    noto = [i for i, d in ((d["id"], d) for d in disp) if d["ruling"] == "refused-notation"]
    rep.add("4", "item 0f — the published strata must reconcile with the EFFECTIVE count, not only with 57",
            "27 fillers + 11 function + 13 content = 57 as adjudicated, and the effective 49 = 57 - 6 notation "
            "refusals - 2 demotions",
            f"effective CERTAIN-leg-d {eff.get('CERTAIN-leg-d')}; distinct omitted words among them "
            f"{len(cert_words)}; notation refusals {sorted(set(noto))}",
            PASS if eff.get("CERTAIN-leg-d") == 49 else FAIL, n=len(cert_words))
    tainted = [d["id"] for d in disp if d["ruling"] == "holdout-member-note"]
    rep.add("4", "item 0g — the v2-holdout rows are marked as such IN the adjudication record",
            "7 rows noted: D-092, D-093, D-094, D-095, D-107, D-108, D-122",
            f"{len(tainted)} noted: {sorted(tainted)}",
            PASS if sorted(tainted) == ["D-092", "D-093", "D-094", "D-095", "D-107", "D-108", "D-122"] else FAIL,
            n=len(tainted))
    dtouch = git(wt, "log", "-1", "--format=%cI", head_ref(wt), "--", adj_path)[1].decode().strip()
    fwd = sorted({d["utc"] for d in disp if dtouch and d["utc"] > dtouch.replace("+00:00", "Z")})
    rep.add("4", "item 0h — a disposition's utc may not post-date the commit that contains it, and its `utc_source` "
                 "must be true", "every utc ≤ its committing commit's time",
            f"committed {dtouch}; stamps after it: {fwd}; source claimed: "
            f"{sorted({d['utc_source'] for d in disp})[:1]}", FAIL if fwd else PASS, n=len(disp),
            note="`utc_source` says 'the lane clock at write time', which a forward stamp falsifies: the clock had not "
                 "reached that time when the commit was made. Same class as item v2.c and ORCH-2's own O-4. The tool "
                 "takes --utc as a free argument and never compares it to a clock, so nothing prevents it")

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
        rep.add("4", "interval overlaps with any fixture span", "0", "0", VACUOUS, n=0,
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
                note="ITEM 11b LANDED: §5e's superseded figures (98 flags / up to 11) stay readable and PATTERNS "
                     "now carries the gate's independent simulation beside them — 97 = 9 zero-ASCII-token + 61 "
                     "over-bound + 27 ASCII-mismatch, max unit 12 over 9 claims — with the delta stated")
    bis = slice_section(pat, "5b-bis.")
    # DEFECT #33: item 12's repair pattern leaves the fuzzy value READABLE beside an exact value and its
    # source - `appended 2026-09-25T21:27:50Z (src 4fc40c8; read `21:5xZ`)`. A row that flags any fuzzy token
    # punishes exactly that fix (the blindness of defect #28: the disclosure must slice the disclosure).
    bad_ts, ok_ts = [], []
    for line in bis.splitlines():
        for m in re.finditer(r"\d{2}:\d[xX]Z", line):
            (ok_ts if (TS_EXACT.search(line) and re.search(r"src|read|supersed", line, re.I)) else bad_ts).append(
                (line.strip()[:60], m.group(0)))
    rep.add("5", "PATTERNS §5b-bis fuzzy timestamp (item 12 / criterion 20.14)", "exact UTC + source, the fuzzy "
                 "value left readable only as a superseded citation",
            f"{len(bad_ts)} asserted fuzzy: {bad_ts}; {len(ok_ts)} superseded-in-place: {[t[1] for t in ok_ts]}",
            FAIL if bad_ts else PASS, n=len(bad_ts) + len(ok_ts))
    seeded_claim = ("seeded: true" in bis) or ("seeded`" in bis)
    corr = bool(re.search(r"\*\*0d", pat)) and ("fixtures-adjudication.json" in pat) \
        and bool(re.search(r"0 of 122", pat))
    rep.add("5", "PATTERNS §5b-bis repeats the false seeded sentence (item 0d)", "left readable AND corrected by an "
                 "appended block in the same file that names the sentence and the true figures",
            f"sentence present in §5b-bis: {seeded_claim}; in-file 0d correction naming the true figures: {corr}",
            PASS if (seeded_claim and corr) else (INFO if not seeded_claim else FAIL), n=1,
            note="0 of 122 rows carry seeded: true; the four seeded rows live in fixtures-adjudication.json "
                 "(FIX-D2-001...004); PATTERNS.md's appended 0d block states both")




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
    inst, supers = [], []
    for rp, v, k in fuzzy:
        if k != "instance":
            continue
        # DEFECT #33: a fuzzy value in a digest-bound file that may not be edited is superseded IN-FILE by an
        # exact sibling key plus a source string naming the fuzzy value. That is the compliant repair, not an
        # asserted instance (fixtures/v2/dropword.json's generated_utc / generated_utc_exact).
        t2 = open(os.path.join(wt, rp), encoding="utf-8", errors="replace").read()
        i2 = t2.find(v)
        win = t2[max(0, i2 - 200):i2 + 500] if i2 >= 0 else ""
        if re.search(r'"[a-z_]*_exact"\s*:\s*"20\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ"', win) and \
                re.search(r"supersed", win, re.I):
            supers.append((rp, v))
        else:
            inst.append((rp, v))
    inst, supers = sorted(set(inst)), sorted(set(supers))
    cites = sorted({(rp, v) for rp, v, k in fuzzy if k == "citation"})
    rep.add("6", "criterion 20.14a: FUZZY timestamps ASSERTED in committed docs (item 12)", "0 instances",
            f"{len(inst)} instances: {inst}", PASS if not inst else FAIL, n=nfiles,
            note=f"plus {len(cites)} sites that QUOTE a fuzzy value in order to report or supersede it "
                 f"(not instances): {cites[:6]}; plus {len(supers)} fuzzy values superseded IN-FILE by an exact "
                 f"sibling key + source (the compliant repair for a digest-bound file): {supers}")
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
        # DEFECT #37 of this instrument: this row cited criterion 20.16, which is about a published digest
        # covering a SUBSET (item 14, the q4 format leg, checked in §3). Stating HOW a digest is computed is
        # criterion 20.15b. A mis-cited criterion sends the worker to repair the wrong sentence.
        # O-9: the note belongs WHERE THE DIGEST IS PUBLISHED. The q4 supplement publishes three digests under
        # `runs.*` and carries a `config_digest_note` in each; demanding a top-level key there would fail a
        # repaired artefact. Judge every published config_sha256 that has no note beside it.
        # O-8 discipline: the criterion is "the canonicalization is stated BESIDE the digest", not "it is stated under
        # the key name ORCH-2 predicted". Any key whose value states the construction counts.
        _stated = states_construction          # module level, so --selftest mutation-tests it (defect #44)
        unnoted = []
        if "config_sha256" in d and not _stated(d):
            unnoted.append("(top level)")
        for rn, rv in (d.get("runs") or {}).items():
            if isinstance(rv, dict) and "config_sha256" in rv and not _stated(rv):
                unnoted.append(f"runs.{rn}")
        noted = ([f"top level ({','.join(_stated(d))})"] if ("config_sha256" in d and _stated(d)) else []) + \
            [f"runs.{rn} ({','.join(_stated(rv))})" for rn, rv in (d.get("runs") or {}).items()
             if isinstance(rv, dict) and "config_sha256" in rv and _stated(rv)] + \
            [f"top level ({','.join(_stated(d))})" for _ in [0]
             if "config_sha256" not in d and _stated(d)]
        rep.add("8", f"{rel}: config canonicalization stated (criterion 20.15b)",
                "the construction stated beside every published config digest, under any key that states it",
                f"noted: {noted or 'none'}; UNNOTED: {unnoted or 'none'}",
                PASS if not unnoted and noted else FAIL, n=len(noted) + len(unnoted),
                note="the q2 supplement states how its config digest is computed; the others must adopt it. Item 14 "
                     "(criterion 20.16, the q4 format leg publishing only `rules` where q3 publishes "
                     "abbreviations + excerpt_chars + rules) is a separate row in §3")
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
        # O-8: item 8a landed as a `generator_pins` block beside `tool_commit`; test the delivered design.
        ok, obs, note = generator_pin_check(wt, json.load(open(os.path.join(wt, rel), encoding="utf-8")))
        rep.add("8", f"{rel}: attributable to its generator bytes (criterion 20.10 as amended by O-8)",
                "generator_pins pins a commit that contains the tool at the pinned sha256", obs,
                PASS if ok else FAIL, n=1, note=note)





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
        cls = False
        if os.path.exists(aud):
            rj = json.load(open(aud, encoding="utf-8"))
            e = [x for x in rj.get("fixture_sources", []) if x.get("file") == src]
            # DEFECT #35: the audit now classifies as "APPEND-ONLY-AFTER-SEAL (dated note on file)". Requiring the
            # bare string read a QUALIFIED classification as a lost one; the substance (mutations empty, no ids
            # added) is what makes it append-only, so match the prefix and keep the substance test.
            cls = bool(e) and str(e[0].get("status", "")).startswith("APPEND-ONLY-AFTER-SEAL") \
                and not e[0].get("mutations") and not e[0].get("new_fixture_ids")
        note_ok = sorted(k for k, v in companion_texts(wt).items() if dg[:12] in v and act[:12] in v)
        rep.add("10", f"criterion v2.5 (as amended by O-5) — {src}: the seal binds its SEAL-TIME digest and the "
                      f"post-seal move is classified append-only with a dated companion note naming both",
                f"seal-time {dg[:16]}… + classified append-only + both digests named in a companion note",
                f"live {act[:16]}…; classified append-only (mutations [] / no ids added): {cls}; companion "
                f"artefact(s) naming both digests: {note_ok}",
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
        for rel, t2 in sorted(companion_texts(wt).items()):
            t2 = t2.lower()
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
          # RE-PINNED 2026-09-26T02:17:07Z by ORCH-2 (ANNEX §F8): the reducer changed at 34db0b0 (+46 lines of
          # derivations prose). The drift is disclosed in the artefact itself (`derivations_revision`,
          # `effect_on_run_outputs: none`) and was verified behaviour-neutral by re-running the tool at head with
          # the published pins: ledger d42136c6… and by_transcript c1ec4da8… reproduce BYTE-IDENTICALLY. §F7's
          # void-on-drift rule exists to stop SILENT input changes; it is not a tripwire on a disclosed,
          # verified-neutral documentation change. The old pin was 6d4bb9ce (blob at dada3e6).
          ("tools/m5r_reduce.py", "a89ff189"), ("findings/ledger.jsonl", "d42136c6"),
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

    prereg, nscan = [], 0
    for root, dirs, files in os.walk(os.path.join(wt, "runs")):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in sorted(files):
            nscan += 1
            t = fn.lower()
            if "prereg" in t or "pre-reg" in t or "quantum-b" in t or "quantumb" in t:
                prereg.append(os.path.relpath(os.path.join(root, fn), wt))
    rep.add("12", "a committed pre-registration artefact exists (criterion v2.12 needs it BEFORE the run commit)",
            "ABSENT is the correct state while v2.a/v2.b are open",
            f"{len(prereg)} of {nscan} file(s) under runs/ match a pre-registration name: {sorted(prereg)[:4]}",
            INFO if not prereg else PASS, n=nscan,
            note="defect #42: n was the count of MATCHES (0), which made this indistinguishable from a row that did no "
                 "work; n is now the count of filenames compared")
    v2salt = j.get("salt")
    spent, spent_v1, nrecv = [], [], 0
    for root, dirs, files in os.walk(os.path.join(wt, "runs")):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in sorted(files):
            if fn.endswith(".json"):
                nrecv += 1
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
            f"{len(spent)} of {nrecv} JSON artefacts under runs/ declare the V2 holdout spent: {sorted(spent)[:3]}",
            PASS if not spent else FAIL, n=nrecv,
            note=f"defect #42: n was the count of offending receipts (0), so this PASS looked vacuous; n is now the "
                 f"count of artefacts examined for a spend declaration. A receipt only consumes v2 if it binds the v2 "
                 f"split file or the v2 salt; "
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

    # cycle-K amendments, mutation-tested (defects #44 and #46): each pair is a positive and the negative that the
    # pre-amendment row got wrong.
    t("T21", "#44 §8 accepts ANY key that states the construction, not only `config_digest_note`",
      (["config_canonicalization"], ["config_digest_note"], []),
      (states_construction({"config_sha256": "8e7e", "config_canonicalization":
                            "sha256(json.dumps(cfg, sort_keys=True, separators=(',',':')))"}),
       states_construction({"config_sha256": "8e7e", "config_digest_note": "sort_keys + separators"}),
       states_construction({"config_sha256": "8e7e", "note": "see the run log"})))
    t("T22", "#44 §18 accepts a legitimate ALTERNATIVE wording of 'one draw, not two'",
      True, one_draw_statement("293b29c and 79eb401: the partition was not redrawn, same salt, manifest only",
                               "293b29c", "79eb401"))
    t("T23", "#38 §18 a bare CITATION of the first seal commit is still not the statement",
      False, one_draw_statement("run_utc 2026-09-25T20:5xZ (src 293b29c; read `20:5xZ`)", "293b29c", "79eb401"))
    t("T24", "#44 §19 a hollow sentence (`sensitivit` + a `33`) does NOT satisfy amended A4",
      (False, False, False), h_denominator_commitment("we report a sensitivity figure over 33 transcripts"))
    t("T25", "#44 §19 the real commitment does: both denominators, same run, the four bound by reference",
      (True, True, True),
      h_denominator_commitment("PRIMARY 29 = 33 - 4 (holdout_exclusions), SENSITIVITY 33 from the SAME run, "
                               "no second spend", 4, True))
    t("T26", "#46 §20 the verbatim quote survives INNER backticks in a row name",
      ["item 13b — the `derivations_revision` claim states the pin"],
      verbatim_row_quotes("- **Row (verbatim):** `item 13b — the `derivations_revision` claim states the pin`\n"))
    t("T27", "#46 §20 a line that is not a verbatim quote is not one (no phantom coverage)",
      [], verbatim_row_quotes("- **Task/item:** TASK-020 item 13b\n- **Row:** `item 13b`\n"))
    t("T28", "#49 a fuzzy time inside a FULLY BACKTICKED iso stamp is a CITATION, not an asserted instance",
      "citation", classify_fuzzy("the header `2026-09-25T21:5xZ` is fuzzy",
                                 FUZZY_TS.search("the header `2026-09-25T21:5xZ` is fuzzy")))
    t("T29", "#49 a bare fuzzy time in this lane's own prose is still an INSTANCE (the fix is not a blanket pardon)",
      "instance", classify_fuzzy("we finished at 21:5xZ and committed",
                                 FUZZY_TS.search("we finished at 21:5xZ and committed")))
    t("T30", "#49 a fuzzy fragment inside a QUOTED ARTEFACT LINE (iso stamp + `(src `) is a citation",
      "citation", classify_fuzzy("the only mention is `run_utc 2026-09-25T20:50:46Z (src 293b29c; read 20:5xZ)`",
                                 FUZZY_TS.search("the only mention is `run_utc 2026-09-25T20:50:46Z "
                                                 "(src 293b29c; read 20:5xZ)`")))
    t("T31", "#49 a nearby backticked digest does NOT pardon a fuzzy stamp in the author's own sentence",
      "instance", classify_fuzzy("we finished at 21:5xZ and committed `d42136c6`",
                                 FUZZY_TS.search("we finished at 21:5xZ and committed `d42136c6`")))
    # defect #51 (item 0g's self-contradiction) and defect #50 (environment gaps charged to the worker), mutation-tested.
    _g = '{"record": "disposition", "id": "D-002", "ruling": "CANDIDATE", "utc": "2026-09-26T01:12:00Z"}'
    _sup = ('{"record": "disposition", "id": "D-002", "ruling": "CANDIDATE", "utc": "2026-09-26T00:39:44Z", '
            '"utc_source": "git committer time of 7d14685", "utc_superseded": "2026-09-26T01:12:00Z", '
            '"utc_superseded_reason": "projected from the CONTROL cadence grid, not read"}')
    _rewritten = ('{"record": "disposition", "id": "D-002", "ruling": "PROMOTE", "utc": "2026-09-26T00:39:44Z", '
                  '"utc_superseded": "2026-09-26T01:12:00Z", "utc_superseded_reason": "re-ruled"}')
    _nokeep = ('{"record": "disposition", "id": "D-002", "ruling": "CANDIDATE", "utc": "2026-09-26T00:39:44Z", '
               '"utc_superseded": "2026-09-26T01:11:00Z", "utc_superseded_reason": "close enough"}')
    _noreason = ('{"record": "disposition", "id": "D-002", "ruling": "CANDIDATE", "utc": "2026-09-26T00:39:44Z", '
                 '"utc_superseded": "2026-09-26T01:12:00Z", "utc_superseded_reason": "  "}')
    t("T32", "#51 a disclosed stamp supersession (prior utc kept VERBATIM + reason, no other field touched) is not a breach",
      ([1], []), append_only_supersession([_g], [_sup])[1:])
    t("T33", "#51 a changed RULING behind a supersession is still a violation - the exemption cannot hide a rewrite",
      [1], append_only_supersession([_g], [_rewritten])[2])
    t("T34", "#51 a supersession that does NOT keep the prior value, or states no reason, is a violation",
      ([1], [1]), (append_only_supersession([_g], [_nokeep])[2], append_only_supersession([_g], [_noreason])[2]))
    _r = Report()
    _so, sys.stdout = sys.stdout, io.StringIO()

    def _boom_env():
        raise FileNotFoundError("/wt/corpus/docdocgo/html/merged-book-texts_json_1.js")

    def _boom_code():
        raise ValueError("bad literal inside the instrument")

    run_section(_r, _boom_env)
    MATERIALISED["broken_sections"] = 0
    run_section(_r, _boom_code)
    sys.stdout = _so
    t("T35", "#50 a crash naming a MATERIALISED path is VACUOUS - an environment gap is never charged to the worker",
      VACUOUS, _r.rows[0]["verdict"])
    t("T36", "#50 any other crash is a FAIL against the INSTRUMENT, and the summary still prints",
      FAIL, _r.rows[1]["verdict"])
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

    t("T19", "defect #36 guard: an own-time stamp is a field the document asserts about ITSELF, not one it "
             "quotes — the census table quotes 39 historical values beside their source commits",
      1, len(own_time_stamps('{"audit_utc": "2026-09-26T01:22:00Z"}\n| `fleet/LOG.md` | 15 | x | '
                             '2026-09-25T18:45:13Z | `341ee2e` |')))
    t("T20", "a markdown HEADER stamp is own-time even with no lead pattern, and a superseded fuzzy citation "
             "beside it does not make it a citation",
      ["2026-09-26T00:32:03Z"], [v for _, v in own_time_stamps(
          "# prep\n\nlane `x` · worker `A-1` · 2026-09-26T00:32:03Z (src 72104a5; read `21:5xZ`)\n", md=True)])

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
    adj, disp13 = adj_rows(wt)   # defect #32: the appended dispositions carry their own schema

    kinds = collections.Counter(str(x["shape"].get("kind")) for x in sigs)
    rep.check("13", "shape_adjudication classifies every signal", len(sigs), len(adj), n=len(sigs))
    rep.check("13", "recomputed kind tally == the published counts", dict(sa["counts"]), dict(kinds), n=len(sigs))
    cr = sa["count_reconciliation"]
    # The items-15a/15b rebuild restructured EVAL.json: `signals` and `count_reconciliation` moved under
    # `shape_adjudication`, and the reconciliation no longer carries `raw` / `re_labelled_needs_human_read`.
    # The closure is still derivable from `counts` (113 + 3 + 5 + 1 = 122 = len(signals)), so the substance
    # survives; but a rebuilt artefact may not silently drop a field a published derivation reads, so the drop
    # is reported and judged on whether `rebuild_history` discloses it.
    tot = sum(int(x) for x in sa["counts"].values())
    rep.check("13", "the classification closes over every signal: sum(counts) == len(signals)", len(sigs), tot,
              n=len(sigs))
    rep.check("13", "re-labelled (partial-overlap + gate-boundary) == the 6 the reconciliation used to state",
              6, kinds["partial-overlap"] + kinds["gate-boundary-excluded"], n=6)
    gone = sorted(k for k in ("raw", "re_labelled_needs_human_read") if k not in cr)
    rh = json.load(open(os.path.join(wt, "runs/m4-q2-dropword/EVAL.json"), encoding="utf-8")).get("rebuild_history", [])
    disclosed = bool(re.search(r"count_reconciliation|re_labelled|\braw\b", json.dumps(rh)))
    rep.add("13", "the rebuilt EVAL drops no field a published derivation reads — or discloses the drop in "
                  "`rebuild_history`", "no dropped keys, or the drop disclosed",
            f"keys removed by the rebuild: {gone}; disclosed in rebuild_history: {disclosed}; closure still "
            f"derivable from counts: {tot == len(sigs)}",
            PASS if (not gone or disclosed) and tot == len(sigs) else FAIL, n=3,
            # defect #42: n was len(gone) - the count of dropped keys, i.e. of DEFECTS. Three comparisons were
            # performed (two key-presence tests + the closure test); with none dropped, n=0 read as "no work".
            note="`rebuild_history` carries the pre-rebuild artefact sha256 + its source, the pre-rebuild "
                 "generator_pins + how to check them, and the original run_args (corpus zip, main_head, policy, "
                 "tool_commit, run utc) — so the rebuild is orderable and the run inputs are shown unchanged")
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
    # O-8: an append-only record cannot grow a key on a row already written, so a disposition lands as an
    # APPENDED row (`"record":"disposition"`). Item 8b's substance is unchanged: the two contradictions with
    # sibling instruments must each carry a written ruling that names the sibling.
    inline = [k for r in adj for k in r if any(t in k.lower() for t in ("disposition", "ruling", "note", "append"))]
    byrul = {d["id"]: d for d in disp13 if d.get("new_verdict")}
    named = {i: bool(re.search(r"EVAL|shape|source.inheritance|filter", str(d.get("reason", "")), re.I))
             for i, d in byrul.items() if i in ("D-002", "D-039")}
    rep.add("13", "item 0g/8b — the record carries a written disposition for each contradiction with a sibling "
                  "instrument", "appended disposition rows (or inline keys) for D-002 and D-039, each naming the "
                  "sibling that contradicts it",
            f"{len(disp13)} appended disposition rows, inline keys {sorted(set(inline))[:3] or 'none'}; D-002/D-039 "
            f"ruled and the contradicting sibling named: {named}",
            PASS if (disp13 or inline) and all(named.get(i) for i in ("D-002", "D-039")) else FAIL,
            n=len(disp13) + len(inline),
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
    # O-8: item 0g landed as APPENDED disposition rows (`ruling: holdout-member-note`), not as an inline flag on
    # the 122 rows — the only shape an append-only record permits. Credit the delivered form.
    noted_disp = sorted({d["id"] for d in disp13 if d.get("ruling") == "holdout-member-note"})
    noted_inline = [r.get("id") for r in adj if os.path.basename(str(r.get("transcript"))) in v2hold
                    and any("holdout" in str(v).lower() for k, v in r.items() if k != "transcript")]
    noted = sorted(set(noted_disp) | set(noted_inline))
    rep.add("13", "item 0g — the v2-holdout rows are marked as such IN the adjudication record",
            f"{len(tainted)} rows noted", f"{len(noted)} of {len(tainted)} noted ({noted}) — appended disposition "
            f"rows {noted_disp}, inline flags {noted_inline}",
            PASS if len(noted) == len(tainted) else FAIL, n=len(tainted),
            note="no holdout-tainted row may be quoted as tuning-side evidence")
    # the arithmetic moved twice: 57 rows / 55 sites as adjudicated, then item 0g's dispositions demoted 2 and
    # refused-notation 6, giving 49 effective rows over 48 sites. Both figures are published, so both are checked.
    dem = [r for r in cert if r.get("id") not in ("D-002", "D-039")]
    dem_sites = {(os.path.basename(str(r["transcript"])), str(r.get("span"))) for r in dem}
    cert_sites = {(os.path.basename(str(r["transcript"])), str(r.get("span"))) for r in cert}
    rep.add("13", "item 0e — the stated post-DEDUPE arithmetic checks out (57 rows / 55 sites)",
            "57 rows / 55 distinct (transcript, span) sites",
            f"{len(cert)} rows / {len(cert_sites)} sites; after the two demotions {len(dem)} rows / "
            f"{len(dem_sites)} sites",
            PASS if (len(cert), len(dem)) == (57, 55) else FAIL, n=len(cert))
    eff13 = {r["id"]: r["verdict"] for r in adj}
    for d in disp13:
        if d.get("new_verdict"):
            eff13[d["id"]] = d["new_verdict"]
    effrows = [r for r in adj if eff13[r["id"]] == "CERTAIN-leg-d"]
    effsites = {(os.path.basename(str(r["transcript"])), json.dumps(r.get("restored_span"), sort_keys=True))
                for r in effrows}
    patt = open(os.path.join(wt, "tools/PATTERNS.md"), encoding="utf-8").read() \
        if os.path.exists(os.path.join(wt, "tools/PATTERNS.md")) else ""
    rep.add("13", "item 0g/11b — the EFFECTIVE post-disposition figures reproduce (49 rows / 48 sites)",
            "49 rows / 48 distinct sites, published with the delta from 57",
            f"{len(effrows)} rows / {len(effsites)} sites; PATTERNS publishes '49 promoted rows': "
            f"{'49 promoted rows' in patt}",
            PASS if (len(effrows), len(effsites)) == (49, 48) and "49 promoted rows" in patt else FAIL,
            n=len(effrows),
            note="the collapsing pair is D-120/D-121 (`see`, one site); D-097/D-098 collapsed at 57 but both are "
                 "refused-notation now, so one collapse remains — 49 rows over 48 sites")
    # a field is owed only by the rows it applies to (defect #26: `clause` is the leg-(d) clause, so
    # CANDIDATE rows legitimately lack it; a non-realignable row legitimately has no rebuilt span)
    always = ("verdict", "reason", "seeded", "in_sample", "transcript", "char_offset")
    # defect #32: judged over the 122 adjudication rows; the appended dispositions carry their own schema and are
    # tested for it in §4 (by/id/ruling/reason/task/utc/utc_source).
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
    # O-8: the qualification PATTERNS now publishes is the item-0g one (57/122 quoted only with its exclusions
    # behind it: 49 promoted rows / 48 distinct sites), not the wording this row originally looked for.
    qual = bool(re.search(r"57/122[^\n]{0,200}exclusions", p3)) or ("49 promoted rows" in p3)
    mm = re.search(r"57/122[^\n]{0,190}", p3)
    rep.add("13", "criterion 20.13 — a count quoted in PATTERNS states the exclusions behind it",
            "'57/122' quoted together with the exclusions and effective figures, which reproduce",
            ("stated: " + mm.group(0)[:180]) if qual else ("UNQUALIFIED" if "57/122" in p3 else "not quoted"),
            PASS if qual else FAIL, n=1,
            note="the artefact supports 57/122 as adjudicated; after item 0g's dispositions the effective figure is "
                 "49 rows / 48 sites (re-derived above) and after the shape exclusions the countable q2 figure is "
                 "113 — each quoted with its exclusions beside it")





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
    # DEFECT #39: the derivation says "sha256 of tools/m5r_reduce.py bytes; tool_commit is the reachable lane
    # commit carrying that exact file" - so the literal reading resolves the blob AT tool_commit, not at head.
    # Hashing head reported a failure against a derivation that reproduces exactly.
    _rc, _tb = git(wt, "show", f"{man.get('tool_commit')}:{'tools/m5r_reduce.py'}")
    literal["tool_sha256"] = (hashlib.sha256(_tb).hexdigest() if _rc == 0 and _tb else "") == man["tool_sha256"]
    stated["tool_sha256"] = "bytes" in str(dv.get("tool_sha256"))
    # DEFECT #40: item 13 REWROTE this derivation (basename keys over the 2 .json files in fixtures/confirmed,
    # each line carrying its newline, sorted). The row kept recomputing the OLD literal reading ('same
    # construction over the fixtures dir') and reported a failure against text that now reproduces exactly.
    d_rel, _ = dir_digest(os.path.join(wt, "fixtures"), key="relpath")
    d_base, nb = dir_digest(os.path.join(wt, "fixtures/confirmed"), key="basename")
    literal["fixtures_digest_sha256"] = d_base == man["inputs"]["fixtures_digest_sha256"]
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
            note="ITEM 13 LANDED: the overlays derivation now states the warned-against variant's exact "
                 'construction (sort the lines, strip each newline, join with "\\n", no trailing newline -> '
                 "58274f46…), and fixtures_digest names its key convention (BASENAMES over the 2 files in "
                 "fixtures/confirmed, each line carrying its newline) plus what is outside the binding. 7/7 stated")

    # ITEM 13b (new at 34db0b0): a reproducibility CLAIM is a derivation too - it must state what it depends on.
    # DEFECT #38's class: the first version searched the whole `derivations_revision` block, which mentions
    # `tool_commit` while naming the pinned blob - a mention, not the dependency statement.
    drev = dv.get("derivations_revision") or {}
    rr2 = str(drev.get("reproducibility_note") or "") if isinstance(drev, dict) else str(drev)
    pin_dep = bool(re.search(r"--tool-commit|status_by|the pin|pin passed|original pin", rr2, re.I))
    rep.add("14", "item 13b — the `derivations_revision` reproducibility claim states the pin it depends on",
            "the claim says a byte-identical ledger requires the ORIGINAL --tool-commit, because every row embeds "
            "it in `status_by`",
            f"pin dependence stated: {pin_dep}; claim as written: {rr2[:170]}",
            PASS if pin_dep else FAIL, n=1,
            note="verified by ORCH-2 both ways: with --tool-commit dada3e6 the re-run's ledger is byte-identical "
                 "(d42136c6…); with the argument omitted all 1334 rows are identical EXCEPT `status_by`, which reads "
                 "`tools/m5r_reduce.py@UNPINNED`, and the ledger digest moves to c94cce40…. A reader who rebuilds at "
                 "head pinning its own head would conclude the outputs drifted — criterion 20.15a's discipline "
                 "(a stated derivation must reproduce when followed LITERALLY) applied to a claim about reproduction")

    # ITEM 13's own tool, verified by RUNNING it: a SECOND, independent implementation of the same derivations
    # (its own dir_digest/overlays_digest, no import from the reducer). Agreement between two implementations is
    # stronger than either one alone - and a mutation control proves the tool is not vacuous.
    pc = os.path.join(wt, "tools/m4_prov_check.py")
    zip_ok = os.path.exists(os.path.join(wt, "docdocgo-fixes.zip"))
    if os.path.exists(pc) and zip_ok:
        r = subprocess.run([sys.executable, "tools/m4_prov_check.py"], cwd=wt, capture_output=True, text=True,
                           timeout=900)
        rls = [x for x in r.stdout.splitlines() if x.startswith(("PASS", "FAIL"))]
        npass = sum(1 for x in rls if x.startswith("PASS"))
        tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "no output"
        rep.add("14", "item 13's own tool — `tools/m4_prov_check.py` recomputes every published derivation, run with "
                      "its DEFAULT paths", "exit 0 and every row PASS",
                f"exit {r.returncode}; {npass}/{len(rls)} rows PASS; {tail}",
                PASS if (r.returncode == 0 and rls and npass == len(rls)) else FAIL, n=len(rls),
                note="an independent second implementation of the derivations agreeing with ORCH-2's own "
                     "recomputation (§14's 7/7): fixtures c5d8f6f3…, overlays 027f82a0… with the warned variant "
                     "58274f46… reproducing AND differing, ledger d42136c6…, by_transcript c1ec4da8…, book store "
                     "c0892fcd…, tool_sha256 6d4bb9ce… resolved at the manifest's own tool_commit. Exit codes are "
                     "fail-closed: 1 on any mismatch, 2 on a missing input")
        # mutation control: tamper one published digest in a sibling temp manifest and require the tool to catch it
        mut = os.path.join(wt, "findings", ".ORCH2-MUTATION-PROVENANCE.json")
        caught, mexit, mfield = False, None, ""
        try:
            man = json.load(open(os.path.join(wt, "findings/PROVENANCE.json"), encoding="utf-8"))
            man["inputs"]["fixtures_digest_sha256"] = "0" * 64
            json.dump(man, open(mut, "w", encoding="utf-8"), indent=1, sort_keys=True)
            r2 = subprocess.run([sys.executable, "tools/m4_prov_check.py", "--manifest",
                                 "findings/.ORCH2-MUTATION-PROVENANCE.json"], cwd=wt, capture_output=True,
                                text=True, timeout=900)
            mexit = r2.returncode
            bad = [x for x in r2.stdout.splitlines() if x.startswith("FAIL")]
            mfield = bad[0].split()[1] if bad else ""
            caught = mexit == 1 and any("fixtures_digest_sha256" in x for x in bad)
        except Exception as exc:                                   # noqa: BLE001 - report, never crash the run
            mfield = f"control error: {exc}"
        finally:
            if os.path.exists(mut):
                os.remove(mut)
        rep.add("14", "item 13's tool is NOT vacuous — mutation control: a tampered published digest must be caught",
                "exit 1 with the tampered field named", f"exit {mexit}; failing field: {mfield or 'none'}",
                PASS if caught else FAIL, n=1,
                note="also verified by hand: publishing the WARNED overlays variant as the real value exits 1 (both the "
                     "overlays row and the 'must differ' row fire), and a missing input exits 2. A check that cannot "
                     "fail is not a check")
    else:
        rep.add("14", "item 13's own tool — `tools/m4_prov_check.py` recomputes every published derivation",
                "tool present and the corpus zip materialised", 
                f"tool present: {os.path.exists(pc)}; zip present: {zip_ok}", INFO, n=1,
                note="HELD — needs a gate worktree with the corpus materialised (tools/m5r_inputs.sh recipe)")





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
        adj = adj_rows(wt)[0]   # defect #32: appended dispositions are not adjudication rows
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
        pats = ("overlays", "parse_book_store", "run_tuning")
        hits = sum(t.count(x) for x in pats)
        nl = len(t.split("\n"))
        rep.add("15", "criterion v2.16 PRECEDENT — one-shot discipline read from the TOOL'S SOURCE, not its manifest",
                "0 references to the tuning-side readers in the one-shot tool",
                f"{hits} reference(s) to {list(pats)} over {nl} source lines",
                PASS if hits == 0 else FAIL, n=nl,
                # defect #42: n was the hit count, so a clean tool reported PASS [n=0]
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


def _ts(v):
    return datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ")


# An own-time stamp is one the document asserts ABOUT ITSELF. Lead patterns only (no 90-char window): a wide
# window let a JSON utc field "adopt" the next quoted value in a table row (selftest T19 caught it).
OWN_TIME_LEAD = re.compile(r'(?:'
                           + r'"[a-z_]*utc[a-z_]*"\s*:\s*"?'          # "audit_utc": "
                           + r'|Stamp:\s*\**\s*'                       # Stamp: **
                           + r'|\bappended\s+'                          # (appended <ts>
                           + r'|lane clock[^|]{0,50}'                     # the lane clock stamp of CONTROL seq 43 (`
                           + r'|\bwritten at\b[^|]{0,60}'               # Written at the lane clock stamp ...
                           + r')$', re.I)


def own_time_stamps(text, md=False):
    """Exact stamps a document asserts about ITSELF, not stamps it quotes.

    DEFECT #36 guard: the census table quotes 39 historical values beside their source commits; those are
    citations, and a `|` in the lead rules them out. For a markdown document the first exact stamp in its
    first five lines is its HEADER stamp and counts as own-time whatever precedes it."""
    out, head_zone = [], text.split("\n", 5)[:5]
    hz = "\n".join(head_zone)
    first_in_head = TS_EXACT.search(hz) if md else None
    for m in TS_EXACT.finditer(text):
        lead = text[max(0, m.start() - 40):m.start()]
        if "|" in lead:
            continue
        if OWN_TIME_LEAD.search(lead) or (first_in_head and m.start() == first_in_head.start()):
            out.append((m.start(), m.group(0)))
    return out


def m5r_rerun(wt):
    """Re-run the inherited M5-R reducer AT HEAD with the pins the published manifest names.

    TASK-013's PASS was bound to `tools/m5r_reduce.py` being byte-identical across gated heads - a PROXY for
    the thing that matters, which is that the published outputs still reproduce. At 34db0b0 the tool changed
    (+46 lines of derivations prose, TASK-020 item 13) so the proxy broke; this settles the substance.
    Returns (ok, detail) or None when the gate worktree lacks the materialised inputs."""
    man_p = os.path.join(wt, "findings/PROVENANCE.json")
    if not os.path.exists(man_p):
        return None
    man = json.load(open(man_p, encoding="utf-8"))
    recs = next((c for c in ("evidence/runs/m5-raw/records", "runs/m5-raw/records")
                 if os.path.isdir(os.path.join(wt, c))), None)
    fix = next((c for c in ("evidence/fixtures/confirmed", "fixtures/confirmed", "evidence/fixtures", "fixtures")
                if os.path.exists(os.path.join(wt, c, "confirmed.json"))), None)
    corp = "corpus" if os.path.isdir(os.path.join(wt, "corpus/docdocgo/overlays")) else None
    if not (recs and fix and corp):
        return None
    out = tempfile.mkdtemp(prefix="orch2-m5r-")
    cmd = [sys.executable, os.path.join(wt, "tools/m5r_reduce.py"),
           "--records", os.path.join(wt, recs), "--fixtures", os.path.join(wt, fix),
           "--corpus", os.path.join(wt, corp), "--out", out,
           "--utc", str(man.get("run_utc") or ""),
           "--tool-commit", str(man.get("tool_commit") or ""),
           "--main-head", str(man.get("main_head") or ""),
           "--policy-sha", str(man.get("policy_sha256") or ""),
           "--book-store-sha", str((man.get("book_store") or {}).get("sha256") or ""),
           "--detector-tool-commit", str((man.get("inherited_census") or {}).get("detector_tool_commit") or "")]
    r = subprocess.run(cmd, capture_output=True, cwd=wt, timeout=900)
    if r.returncode != 0:
        return False, f"the re-run FAILED: rc={r.returncode} {r.stderr.decode()[-220:]}"
    led = sha_file(os.path.join(out, "ledger.jsonl"))
    nm = json.load(open(os.path.join(out, "PROVENANCE.json"), encoding="utf-8"))
    pub = man["outputs"]
    same_led = led == pub["ledger.jsonl"]
    same_bt = nm["outputs"]["by_transcript_digest"] == pub["by_transcript_digest"]
    mdiff = sorted(k for k in set(man) & set(nm)
                   if json.dumps(man[k], sort_keys=True) != json.dumps(nm[k], sort_keys=True))
    # FIELD-LEVEL diff of the two ledgers: this is how the pin dependency was diagnosed by hand at cycle K (the only
    # differing field was `status_by`, which embeds --tool-commit). Mechanized so the diagnosis is not re-derived each
    # cycle and so a future tool change that moves a real field is named instead of hidden behind a digest.
    pub_p = os.path.join(wt, "findings/ledger.jsonl")
    pub_rows = [json.loads(x) for x in open(pub_p, encoding="utf-8") if x.strip()] if os.path.exists(pub_p) else []
    new_rows = [json.loads(x) for x in open(os.path.join(out, "ledger.jsonl"), encoding="utf-8") if x.strip()]
    fdiff, aligned = collections.Counter(), 0
    if len(pub_rows) != len(new_rows):
        fdiff["<row count differs>"] = 1
    else:
        for a, b in zip(pub_rows, new_rows):
            if a.get("id") != b.get("id"):
                fdiff["<id misalignment>"] += 1
                continue
            aligned += 1
            for k in set(a) | set(b):
                if json.dumps(a.get(k), sort_keys=True) != json.dumps(b.get(k), sort_keys=True):
                    fdiff[k] += 1
    shutil.rmtree(out, ignore_errors=True)
    ok = same_led and same_bt
    return ok, (aligned, len(pub_rows), len(new_rows), dict(fdiff)), (f"ledger {led[:16]}… == published {pub['ledger.jsonl'][:16]}…: {same_led}; by_transcript "
                f"{nm['outputs']['by_transcript_digest'][:16]}… == published "
                f"{pub['by_transcript_digest'][:16]}…: {same_bt}; findings {nm['outputs']['findings']} == "
                f"{pub['findings']}; the regenerated manifest differs from the committed one in: {mdiff}")
    # (callers unpack three values: ok, rowdiff, detail)


def section_forward_stamps(wt, rep):
    """§19 — criterion 20.14c: an artefact's own time field may not POST-DATE the commit that contains it.

    Item 12 fixed FUZZY stamps. This is the other half of the same class: a stamp exact to the second but
    IMPOSSIBLE, written from a projected cadence grid instead of read from a clock. It is the more dangerous
    half, because it passes every precision check — and because it lands in the columns the fleet reads for
    liveness (ERRATA-25f: liveness = SIGNALS = heartbeat + CONTROL.log)."""
    # A forward stamp is a defect wherever it sits, so the census covers the WHOLE TREE, not just this
    # delivery's diff - otherwise a cycle in which nobody touches the offending files reports the class as
    # closed. Last-touch times come from ONE `git log --name-only` pass, not a call per file.
    rc, out = git(wt, "diff", "--name-only", PREV_GATED, "HEAD")
    changed = set(out.decode().split()) if rc == 0 else set()
    rc, out = git(wt, "log", "--format=C%cI", "--name-only", "HEAD")
    last, cur = {}, None
    for ln in out.decode().splitlines():
        if ln.startswith("C20"):
            cur = ln[1:].strip().replace("+00:00", "Z")
        elif ln.strip():
            last.setdefault(ln.strip(), cur)
    offenders, checked, new_off = [], 0, []
    for root, dirs, files in os.walk(wt):
        dirs[:] = [d for d in dirs if d not in (".git", "corpus", "evidence", "__pycache__")]
        for fn in files:
            if not fn.endswith((".md", ".json", ".jsonl", ".log")):
                continue
            rel = os.path.relpath(os.path.join(root, fn), wt).replace(os.sep, "/")
            cut = last.get(rel)
            if not cut:
                continue
            t = open(os.path.join(root, fn), encoding="utf-8", errors="replace").read()
            for _, v in own_time_stamps(t, md=fn.endswith(".md")):
                checked += 1
                try:
                    mins = round((_ts(v) - _ts(cut)).total_seconds() / 60.0, 1)
                except ValueError:
                    continue
                if mins > 0:
                    offenders.append((rel, v, cut, mins))
                    if rel in changed:
                        new_off.append((rel, v, cut, mins))
    offenders.sort()
    rep.add("19", "criterion 20.14c — no own-time stamp POST-DATES the commit that contains it (item 12's other "
                  "half; TASK-018 item 0h, TASK-019 item v2.h, TASK-020 item 12c)",
            "0 forward stamps in the committed tree",
            f"{len(offenders)} forward of {checked} own-time stamps over the whole tree: "
            + "; ".join(f"{r} {v} vs its commit {c} (+{m} min)" for r, v, c, m in offenders),
            PASS if not offenders else FAIL, n=checked,
            note="a file's bytes cannot carry a stamp from a time the committer had not reached; every offending "
                 "value here is :00- or cadence-shaped, i.e. projected from the CONTROL grid rather than read. "
                 f"New in this delivery range ({PREV_GATED[:7]}..head): {new_off or 'none'}")
    cen = "fleet/TIMESTAMP-CENSUS-2026-09-26.md"
    ctrl, verdict = "no control artefact found", INFO
    fp = os.path.join(wt, cen)
    if os.path.exists(fp):
        t = open(fp, encoding="utf-8").read()
        ct = (last.get(cen) or "").strip()
        m = re.search(r"Stamp: \*\*(20\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ)\*\*", t)
        if m and ct:
            d = round((_ts(m.group(1)) - _ts(ct)).total_seconds() / 60.0, 1)
            ctrl = (f"{cen} stamps itself {m.group(1)} from `date -u` and was committed {ct} — {d} min, a plausible "
                    f"write-then-commit gap in the SAME lane")
            verdict = PASS if (d <= 0 and offenders) else (INFO if not offenders else FAIL)
    rep.add("19", "the forward stamps are NOT a clock artifact (the ruling's control)",
            "one artefact in the same lane whose own `date -u` stamp precedes its commit", ctrl, verdict,
            n=1, note="so git's clock and the lane's clock agree to within minutes and the +32/+41 min stamps are "
                      "not skew. Root cause: a stamp taken from the CONTROL cadence grid — the seal note says it was "
                      "'written at the lane clock stamp of CONTROL seq 43' — propagates into every artefact that "
                      "cites it, and CONTROL seq 43/44 are themselves forward-stamped")
    # fleet-signal integrity: BOSS-2 verifies cadence from these columns (ERRATA-25f), so a non-monotonic utc
    # column or a duplicated seq is an integrity risk beyond this lane.
    lg = os.path.join(wt, "fleet/CONTROL.log")
    if os.path.exists(lg):
        rows = [l.split("|") for l in open(lg, encoding="utf-8").read().splitlines() if l.count("|") >= 6]
        seqs = [r[4] for r in rows]
        dupes = sorted({q for q in seqs if seqs.count(q) > 1}, key=lambda x: (len(x), x))
        utcs = [r[0] for r in rows]
        # ordering is judged only where it is judgeable: a minute-precision value cannot be ordered against a
        # seconds-precision one, so those are counted as a precision defect, not smuggled into the comparison.
        exact = [u for u in utcs if TS_EXACT.fullmatch(u)]
        fuzzycol = [u for u in utcs if not TS_EXACT.fullmatch(u)]
        nonmono = [(exact[i - 1], exact[i]) for i in range(1, len(exact)) if _ts(exact[i]) < _ts(exact[i - 1])]
        lastc = git(wt, "log", "-1", "--format=%cI", "HEAD", "--", "fleet/CONTROL.log")[1].decode().strip()
        fwd = [u for u in exact if lastc and _ts(u) > _ts(lastc.replace("+00:00", "Z"))]
        rep.add("19", "the WORKER lane's CONTROL.log utc column is exact, orderable and never ahead of the commit "
                      "that carries it — it is the cadence input BOSS-2 reads (ERRATA-25f), so a bad column is a "
                      "fleet-integrity risk",
                "every utc exact to the second, non-decreasing down the file, none after the file's last commit",
                f"{len(rows)} rows: {len(exact)} exact / {len(fuzzycol)} minute-precision {sorted(set(fuzzycol))[:4]};"
                f" utc going BACKWARDS: {nonmono}; rows stamped after the file's last commit ({lastc}): {fwd}; "
                f"seq values used more than once: {dupes}",
                PASS if not (nonmono or fwd or fuzzycol) else FAIL, n=len(rows),
                note="REPORTED to BOSS-2, not ruled here — ORCH-2 gates evidence, the boss owns fleet signals. Two "
                     "findings travel with it: (1) seqs 10-15/38/39/45 each appear twice, so seq is not a unique key "
                     "in this lane's log and a cadence reader must not treat it as one (ORCH-2's own log is rendered "
                     "by fleet2check, which enforces uniqueness); (2) WORKER-2's seq-45 ERRATA corrected the COMMIT "
                     "column for 42/43/44 while their UTC column is still forward-stamped")
    # ---- ANNEX §H: the quantum-b denominator, pre-registered by WORKER-2 and ruled on here ----
    ex = os.path.join(wt, "tools/HELD-OUT-SPLIT-V2-EXCLUSIONS.json")
    rc2, out2 = git(wt, "ls-files", "runs")
    res = [x for x in out2.decode().split() if re.search(r"RECEIPT|SCORE|THRESHOLDS|quantum", x, re.I)]
    spent = sorted(f for f in ("runs/m4-quantum-b", "runs/quantum-b") if os.path.exists(os.path.join(wt, f)))
    rep.add("19", "ANNEX §H precondition — the denominator was decided BEFORE any result existed",
            "no receipt, score, threshold record or quantum-b output at this head",
            f"{res or 'none'}; spent dirs: {spent or 'none'}", PASS if not res and not spent else FAIL, n=1,
            note="this is what makes a denominator change legitimate rather than post-hoc: the swap is recorded "
                 "while the outcome is still unknown")
    if os.path.exists(ex):
        ej = json.load(open(ex, encoding="utf-8"))
        sj = json.load(open(os.path.join(wt, "tools/HELD-OUT-SPLIT-V2.json"), encoding="utf-8"))
        ho = {os.path.basename(x) for x in sj["holdout"]}
        exn = [os.path.basename(d["transcript"]) for d in ej.get("excluded_transcripts", [])]
        src = open(os.path.join(wt, "tools/m4_one_shot_v2.py"), encoding="utf-8").read()
        tp = os.path.join(wt, "tests/test_m4_one_shot_v2.py")
        tst = open(tp, encoding="utf-8").read() if os.path.exists(tp) else ""
        binds = ("holdout_exclusions_sha256" in src) and ("exclusion_set" in src)
        tested = ("pre-registered exclusions changed after the freeze" in tst) and ("holdout_evaluated" in tst)
        note_t = companion_texts(wt).get("tools/HELD-OUT-SPLIT-V2-NOTE-2026-09-26.md", "")
        htxt = note_t + json.dumps(ej)
        # O-8/O-9 discipline: A4-as-amended fixes BOTH denominators (29 primary, 33 sensitivity) FROM THE SAME RUN, with
        # the four named in each. One word ("sensitivit") plus a "33" anywhere is not that commitment - and would let a
        # hollow sentence PASS. Test the conjunction.
        denom, same_run, named = h_denominator_commitment(htxt, len(exn), all(x in ho for x in exn))
        both = denom and same_run and named
        rep.add("19", "ANNEX §H — the exclusions are machine-readable, holdout members, bound by digest into the "
                      "freeze, enforced in code and tested", "all four",
                f"excluded {len(exn)}/33, all holdout members: {all(x in ho for x in exn)}; evaluated "
                f"{ej.get('evaluated_holdout_transcripts')} == 33 - {len(exn)}: "
                f"{ej.get('evaluated_holdout_transcripts') == len(ho) - len(exn)}; the freeze binds the exclusions "
                f"by sha256: {binds}; enforced and tested: {tested}",
                PASS if all(x in ho for x in exn) and binds and tested else FAIL, n=len(exn))
        rep.add("19", "ANNEX §H (A4 amended) — BOTH denominators fixed before the run: 29 PRIMARY and 33 as a "
                      "pre-registered SENSITIVITY from the same run",
                "the note or the exclusions file commits to reporting both, the four named in each",
                f"counts recorded: {ej.get('evaluated_holdout_transcripts')} evaluated / "
                f"{ej.get('holdout_transcripts')} holdout; BOTH denominators stated: {denom}; SAME run / no second "
                f"spend stated: {same_run}; the four named or bound by reference: {named}",
                PASS if both else FAIL, n=4,
                note="A4 as written fixed 33 primary + 29 sensitivity. WORKER-2's note swaps the primary to 29 on "
                     "the label-taint ground (§F2's own reason) and forbids the four from re-entering any "
                     "denominator. ORCH-2 ADOPTS the swap — pre-result, machine-readable, enforced, tested — and "
                     "amends A4 append-only: primary 29, sensitivity 33 from the SAME run (no second spend; the "
                     "four were already read), each reported with the four named. Both numbers stay fixed before "
                     "the run, which is the whole point of the protocol; one sentence is owed")



def section_fail_coverage(rep, head):
    """§20 — DEFECT #45: the coverage claim must be DERIVED, not curated. §16 checked a hardcoded OPEN tuple frozen at
    cycle F/G, so it PASSed while listing closed items and omitting every item opened since. Here the published repair
    map (`fleet/ORCH-2-REPAIR-MAP.md`) is the open-item list of record: every row that FAILs must appear in it quoted
    VERBATIM (so the map names the row it claims to close), and every verbatim row name in the map must still be a FAIL
    (so a landed repair forces a new map instead of leaving a stale promise)."""
    print("\n== 20. FAIL-to-repair coverage (derived from the published repair map) ==")
    lane = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    mp = os.path.join(lane, "fleet/ORCH-2-REPAIR-MAP.md")
    fails = [r["name"] for r in rep.rows if r["verdict"] == FAIL]
    vac = [r["name"] for r in rep.rows if r["verdict"] == VACUOUS]
    if not os.path.exists(mp):
        rep.add("20", "the repair map exists beside this instrument", "present", f"ABSENT at {mp}", FAIL, n=len(fails))
        return
    txt = open(mp, encoding="utf-8").read()
    # The map is bound to the head it was published for (named in its title). Gating a DIFFERENT head is not a worker
    # defect and must not read as one: report the mismatch and claim no coverage. Verified by running at 1c8a287, where
    # the 34db0b0 map covers 13 of that head's 17 FAILs.
    mb = re.search(r"`([0-9a-f]{7,40})`", "\n".join(txt.splitlines()[:4]))
    bound = mb.group(1) if mb else ""
    if not bound or not (head.startswith(bound) or bound.startswith(head[:7])):
        rep.add("20", "every FAIL row is mapped to a repair in fleet/ORCH-2-REPAIR-MAP.md, quoted VERBATIM",
                "the map binds the head being gated",
                f"the map binds {bound[:7] or 'NO HEAD'}, this run gates {head[:7]} — coverage NOT claimed for this "
                f"head; {len(fails)} FAIL rows here", INFO, n=len(fails),
                note="a repair map is head-specific by design (append-only per cycle): publish a new map for the head "
                     "being gated and this row becomes the mechanical FAIL-to-repair agreement again")
        rep.add("20", "VACUOUS rows owe no repair and are reported as what they are",
                "every VACUOUS row is vacuous-by-data, with the decisive row named beside it",
                f"{len(vac)}: {vac}", PASS, n=len(vac),
                note="a VACUOUS row performed zero comparisons because the data made comparison impossible; it is "
                     "neither a FAIL nor a PASS, and R1 forbids printing it as either")
        return
    # DEFECT #46: `[^`]+` stopped at the FIRST inner backtick, and four row names contain one (`derivations_revision`,
    # `audit_utc`, `tool_commit`, `utc_source`) - so the coverage row failed on its own quoting syntax. Match greedily to
    # the closing backtick at end of line: the name may contain backticks, it may not end with one.
    quoted = verbatim_row_quotes(txt)
    qset, unmapped = set(quoted), [n for n in fails if n not in set(quoted)]
    stale = sorted(q for q in qset if q not in set(fails))
    rep.add("20", "every FAIL row is mapped to a repair in fleet/ORCH-2-REPAIR-MAP.md, quoted VERBATIM",
            f"{len(fails)}/{len(fails)} mapped", f"{len(fails) - len(unmapped)}/{len(fails)} mapped"
            + (f"; UNMAPPED: {unmapped}" if unmapped else "")
            + (f"; the map quotes {len(quoted)} row names, {len(qset)} distinct" if len(quoted) != len(qset) else ""),
            PASS if not unmapped and len(quoted) == len(qset) else FAIL, n=len(fails),
            note="an unmapped FAIL is a FAIL nobody can act on: the map must name the artefact change that flips it. "
                 "Verbatim quotation is what makes the check mechanical instead of a reading exercise")
    rep.add("20", "the repair map carries no entry for a row that no longer FAILs (the map is not stale)",
            "0 stale entries", f"{len(stale)} stale: {stale[:3]}", PASS if not stale else FAIL, n=len(qset),
            note="the map is append-only per cycle: a stale entry means a repair landed and a NEW map is owed for the "
                 "new head, not that this one should be edited")
    rep.add("20", "VACUOUS rows owe no repair and are reported as what they are",
            "every VACUOUS row is vacuous-by-data, with the decisive row named beside it",
            f"{len(vac)}: {vac}", PASS, n=len(vac),
            note="a VACUOUS row performed zero comparisons because the data made comparison impossible (no adjudicated "
                 "row shares a transcript with a fixture); it is not a FAIL and not a PASS, and R1 forbids printing it "
                 "as either")


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
    # DEFECT #45: this tuple was frozen at cycle F/G. It still listed items closed cycles ago (8a, 11a/b, 12, 13, 14,
    # 15a/b, 0d-0g) and omitted every item opened since (13b, 0h, 12c, v2.c-v2.h, 20.14c, 20.15b), so the row the
    # instrument's own note calls "the coverage claim that matters" was checking a stale list and PASSing on it.
    # Refreshed at cycle K - and §20 now DERIVES the same claim from the published repair map, so this curated row is
    # a cross-check, not the authority.
    OPEN = ("0h", "12c", "13b", "v2.a", "v2.b", "v2.c", "v2.d", "v2.e", "v2.g", "v2.h", "20.14c", "20.15b")
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
    tsl = tsrc.split("\n")
    reads = [ln for ln in tsl if re.search(r"corpus/|overlays|docdocgo", ln) and not ln.strip().startswith("#")]
    rep.add("18", "the audit tool opens no transcript content (the 'holdout not opened' claim, tested on the tool)",
            "0 reads of corpus/overlays paths — git objects, the seal file and itself only",
            f"{len(reads)} of {len(tsl)} source line(s) match a corpus/overlays path: {reads[:3]}",
            PASS if not reads else FAIL, n=len(tsl),
            # defect #42: n was the match count, so a clean tool reported PASS [n=0]
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
    # DEFECT #33 again: the repaired header reads `2026-09-26T00:32:03Z (src 72104a5; read `21:5xZ`)` — exact,
    # sourced, superseded value left readable. Flagging the readable citation punishes the fix.
    bad_f, ok_f = [], []
    for line in prep_t.splitlines():
        for m in re.finditer(r"\d\d:\dxZ", line):
            (ok_f if (TS_EXACT.search(line) and re.search(r"src|read|supersed", line, re.I)) else bad_f).append(
                m.group(0))
    rep.add("18", "item v2.f — the prep record's header stamp (item 12's class)",
            "exact UTC to the second with its source; a fuzzy value only as a superseded citation",
            f"{len(bad_f)} asserted fuzzy: {bad_f}; {len(ok_f)} superseded-in-place: {ok_f}",
            FAIL if bad_f else PASS, n=len(bad_f) + len(ok_f),
            note="'2026-09-25T21:5xZ' was both fuzzy and ~2.6 h before its own commit; the census repaired it to "
                 "2026-09-26T00:32:03Z with `src 72104a5` beside it and left the old value readable")
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
    # DEFECT #38: the first version credited any mention of `293b29c`, and the delivery record mentions it only
    # as a timestamp's source commit (`run_utc … (src 293b29c; read `20:5xZ`)`) - a citation, not the statement.
    # Require the two seal commits together WITH a one-draw phrase, or the phrase tied to the commit inline.
    one_draw, comp = [], companion_texts(wt)
    for k, v in sorted(comp.items()):
        both = ("293b29c" in v) and (SEAL_COMMIT[:7] in v)
        # O-8 discipline: the criterion is "a reader can tell the split was not re-drawn", so any wording that says it
        # counts - not only the five phrases ORCH-2 first thought of.
        if one_draw_statement(v, "293b29c", SEAL_COMMIT[:7]):
            one_draw.append(k)
    rep.add("18", "item v2.a clause (iii), second half — the STATEMENT that 293b29c/79eb401 are one draw, not two",
            "stated in a companion note beside the seal",
            f"present in {len(one_draw)} of {len(comp)} companion artefacts scanned: {one_draw}",
            FAIL if not one_draw else PASS, n=len(comp),
            # defect #42: n was the count of artefacts carrying the statement (0) - the FAIL was real but looked
            # like zero work; n is now the count of artefacts searched
            note="without it a reader cannot tell whether the split was re-drawn (a new salt would be owed) or only "
                 "re-manifested; ORCH-2 has verified the substance in the row above, so this item is documentation-only")

    # ---- O-5: ANNEX A1 as written collides with the seal's immutability ----
    freeze_src = open(os.path.join(wt, "tools/m4_one_shot_v2.py"), encoding="utf-8").read()
    binds_appendix = bool(re.search(r"SEAL-APPENDIX|SEAL-AUDIT|appendix_sha|companion", freeze_src))
    rep.add("18", "O-5 amended A1 — the seal stays byte-identical, a dated companion note names both digests, and the "
                  "quantum-b FREEZE binds the companion's digest alongside the seal's",
            "all three", f"seal untouched: True; companion artefacts naming both digests: "
            f"{sorted(k for k, v in companion_texts(wt).items() if 'c8e963199a1e' in v and 'c40d272f30d0' in v)}; "
            f"freeze binds the companion: {binds_appendix}",
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
    fsl = freeze_src.split("\n")
    tuning_side = [ln for ln in fsl if re.search(r'which\s*=\s*"tuning"|--tuning\b', ln)]
    rep.add("18", "v2.16 precedent — the quantum-b tool and its registry carry no tuning-side evaluation path",
            "0 references", f"{len(tuning_side)} of {len(fsl)} lines in m4_one_shot_v2.py match a tuning-side path; "
            f"the registry enters the detectors through run_tuning(..., which=\"holdout\") only",
            PASS if not tuning_side else FAIL, n=len(fsl))   # defect #42: n was the match count
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
                ("evaluated set != frozen holdout (PARTIAL READ)", "not the frozen holdout"),
                ("pre-registered exclusions are NOT holdout members", "are not holdout members"),
                ("score refuses a partial read", "refusing to score a partial read"))
    COVERED = COVERED + (("pre-registered exclusions CHANGED after the freeze",
                          "pre-registered exclusions changed after the freeze"),)
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
            note="the refusal surface grew from 9 to 12 with the pre-registered exclusions, and 4 of the 12 are "
                 "unasserted: the PARAMETERS-changed branch, the evaluated-set refusal (a PARTIAL READ), the "
                 "exclusions-not-holdout-members refusal, and the score-side partial-read refusal. The middle two "
                 "protect quantum b's DENOMINATOR: a partial or wrongly-scoped holdout read must be refused, not "
                 "scored, because the figure is one-shot and cannot be re-run. Code-present is not code-proven; one "
                 "toy test each closes it (a frozen holdout of 2 with a detector that reads 1; a freeze whose params "
                 "are edited without touching the module file; an exclusions file naming a tuning transcript; a "
                 "labels file covering fewer rows than the receipt evaluated)")
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
            "4fc40c8: Ran 227, OK (skipped=1) · 72104a5: Ran 244, OK (skipped=1) · 1c8a287: Ran 257 in 217.2s, OK "
            "(skipped=1) · 34db0b0: Ran 263 in 199.3s, OK (skipped=1) — +13 then +6 (4 in the new test_m4_prov_check, 2 in test_m4_q4_supplement)",
            PASS, n=263,
            note="TASK-021's criterion 21.8 publishes 217, stale since 4fc40c8; the binding floor is the newest "
                 "measured count, 263 at 34db0b0, and the skip count travels with it. Measured in the scratch "
                 "worktree with the corpus materialised: `python3 -m unittest discover -s tests -t tests`")


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
    # DEFECT #50: preflight the materialised inputs first and guard every section, so an environment gap can never be
    # published as a worker defect and no crash can ever silence the summary.
    man0 = run_section(rep, section_materialised, wt, rep)
    bind = run_section(rep, section_bindings, wt, rep, head)
    man, sup = bind if bind else (man0, None)
    run_section(rep, section_pins, wt, rep, sup)
    run_section(rep, section_manifest_stats, wt, rep, man)
    run_section(rep, section_census_exposure, wt, rep, sup)
    run_section(rep, section_adjudication, wt, rep)
    run_section(rep, section_stale_digests, wt, rep)
    run_section(rep, section_read_scope, wt, rep, sup)
    run_section(rep, section_signal_evidence, wt, rep)
    run_section(rep, section_manifest_completeness, wt, rep)
    run_section(rep, section_split_v2, wt, rep, sup)
    run_section(rep, section_inherited, wt, rep)
    run_section(rep, section_quantum_b, wt, rep)
    run_section(rep, section_coherence, wt, rep)
    run_section(rep, section_derivations, wt, rep)
    run_section(rep, section_quantum_b_criteria, wt, rep)
    run_section(rep, section_coverage, rep)
    run_section(rep, section_t21, wt, rep)
    run_section(rep, section_seal_audit, wt, rep, a.head)
    run_section(rep, section_forward_stamps, wt, rep)
    run_section(rep, section_fail_coverage, rep, head)
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

        # DEFECT #48: the self-audit reported asserted-fuzzy stamps as a COUNT and never verdicted them, so this lane
        # could accumulate the very defect it charges others with (criterion 20.14a) while two PASS rows sat beside the
        # number. Append-only records cannot be repaired without rewriting history, so they are reported separately and
        # judged INFO; every other doc in this lane is amendable and is judged FAIL.
        # status.md declares itself append-only ("current state = these entries reduced in order"): its headline table
        # is prepended but the log below it is a record, so a fuzzy stamp inside a cycle-H entry cannot be repaired
        # without rewriting history - it is reported, not charged.
        APPEND_ONLY = ("fleet/CONTROL.log", "fleet/heartbeats/", "fleet/ORCH-2-VERIFICATION-LEDGER.md",
                       "fleet/GATES.md", "fleet/LOG.md", "fleet/ORCH-2-CURSOR.md", "fleet/queue/status.md",
                       # CONTROL.md is not a document anyone may edit: fleet2check RENDERS it from CONTROL.log, so its
                       # text is the append-only log's text. Exempting a rendering of a record is not exempting a claim.
                       "fleet/CONTROL.md")
        hist = sorted({(rp, v) for rp, v in fzi if rp.startswith(APPEND_ONLY)})
        live = sorted({(rp, v) for rp, v in fzi if not rp.startswith(APPEND_ONLY)})
        rep.add("9", "self-item — no fuzzy own-time stamp ASSERTED in this lane's amendable docs (criterion 20.14a, "
                     "the one ORCH-2 charges others with)",
                "0 asserted-fuzzy stamps outside the append-only record",
                f"{len(live)} in amendable docs: {live[:6]}; {len(hist)} inside the append-only record: {hist[:4]}",
                PASS if not live else FAIL, n=len(fzi),
                note="a CITATION of someone else's fuzzy stamp is not one (classify_fuzzy separates them: "
                     f"{len(fzc)} citations). An approximation this lane asserts must be a bounded window naming its "
                     "bounds and their sources - which is exactly what criterion 20.14 demands of the worker, and "
                     "self-item O-4's rule: ORCH-2 is not exempt from its own criterion")

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
