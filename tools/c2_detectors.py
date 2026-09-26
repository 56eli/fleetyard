#!/usr/bin/env python3
"""Registry bridging the one-shot harness (`tools/m4_one_shot_v2.py`) to the M4 detectors.

One place, so the freeze/run/verify machinery never re-implements a detector:
each entry names the real module, its frozen parameters, and the canonical
holdout path (`run_tuning(..., which="holdout")`, which itself enforces that the
split's tuning and holdout sets do not overlap). Nothing here tunes anything.

  C1-drop   tools/det_dropword.py   (M4-q2; holdout mode = one-shot evaluation)
  C2-format tools/det_format.py     (M4-q3; holdout mode = one-shot evaluation)

`evaluate(name, corpus, split_path)` runs the module's own one-shot holdout path
and returns `(per_transcript_signals, transcripts_read)`.
Stdlib only, read-only.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import det_dropword  # noqa: E402
import det_format  # noqa: E402

MODULES = {"C1-drop": det_dropword, "C2-format": det_format}


def params(name):
    """The frozen parameters of one detector — the values a freeze record binds."""
    if name == "C1-drop":
        m = MODULES[name]
        return {"window": m.WINDOW, "stride": m.STRIDE, "min_score": m.MIN_SCORE,
                "top_k": m.TOP_K, "min_matched": m.MIN_MATCHED, "min_ratio": m.MIN_RATIO,
                "max_drop": m.MAX_DROP, "min_flank": m.MIN_FLANK}
    if name == "C2-format":
        m = MODULES[name]
        return {"rules": ["R1-glued-period", "R2-repeated-punct", "R3-long-dot-run",
                          "R4-underscore-run", "R5-space-before-comma",
                          "R6-spaced-period", "R7-glued-comma"],
                "excerpt": m.EXCERPT}
    raise SystemExit("c2_detectors: unknown detector %r" % name)


def evaluate(name, corpus_dir, split_path):
    """Holdout-mode run of one detector -> (per_transcript_signals, transcripts_read)."""
    module = MODULES.get(name)
    if module is None:
        raise SystemExit("c2_detectors: unknown detector %r" % name)
    per_file, _total = module.run_tuning(corpus_dir, split_path, None, which="holdout")
    return per_file, sorted(per_file)
