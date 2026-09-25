"""Self-test + fixture/clean checks for tools/det_nonsense.py (TASK-004)."""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import det_nonsense as det  # noqa: E402


class SelfTest(unittest.TestCase):
    def test_builtin_self_test(self):
        self.assertTrue(det.self_test())

    def test_signal_shape(self):
        for text, _want in [(t[0], t[-1]) for t in det.SELF_TEST]:
            for s in det.detect(text):
                self.assertEqual(s["detector"], det.DETECTOR_ID)
                self.assertEqual(text[s["start"]:s["end"]], s["quoted"])
                self.assertTrue(s["note"])


class NonsenseDetails(unittest.TestCase):
    def test_percent_forms(self):
        self.assertEqual(len(det.detect("a 150 percent rise")), 1)
        self.assertEqual(det.detect("100% and 99.5 percent and 1,000 people"),
                         [])
        self.assertEqual(len(det.detect("rose 1,200% overnight")), 1)

    def test_long_korean_run_is_not_garble(self):
        run = " ".join(["\uc9c4\uc2e4\uc740"] * det.MIN_FOREIGN_RUN)
        self.assertEqual(det.detect("Truth. " + run + ". Next."), [])
        short = " ".join(["\uc9c4\uc2e4\uc740"] * (det.MIN_FOREIGN_RUN - 1))
        self.assertEqual(len(det.detect("Truth. " + short + ". Next.")), 1)


# --- TASK-010: legitimate Korean code-switch is not garble -----------------
import hashlib  # noqa: E402
import json  # noqa: E402

CORPUS = os.path.join(ROOT, "corpus", "docdocgo")
NEGATIVE = os.path.join(ROOT, "fixtures", "negative", "negative.json")


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


KO_UNIT = ("\uadf8\ub798\uc11c \uc9c4\uc815\ud55c \uc2a4\uc2b9\uc740 "
           "\uc790\uc720\ub97c \ud5c8\ub77d\ud558\uace0, \uadf8\uc5d0\uac8c "
           "yes\ub098 no\ub97c \uc120\ud0dd\ud560 \uae30\ud68c\ub97c \uc8fc\uace0, ")


class KoreanCodeSwitchTest(unittest.TestCase):
    def test_particle_tokens_in_korean_are_not_flagged(self):
        text = ("allows you to say yes or no without any consequences. " +
                KO_UNIT * 4)
        self.assertEqual(det.detect(text), [])

    def test_same_shape_in_english_context_still_flagged(self):
        sig = det.detect("didn't answer. No, never. My hand\uc740 You saw it")
        self.assertEqual([s["quoted"] for s in sig], ["hand\uc740"])

    def test_non_particle_suffix_still_flagged(self):
        # "sub\uc5c8\ub294\ub370" (verb ending, English context) stays garble
        self.assertEqual(len(det.detect("success in this sub\uc5c8\ub294\ub370 "
                                        "bullshit how about")), 1)

    def test_real_garble_preserved(self):
        self.assertEqual(len(det.detect("spirit\u6301 is here")), 1)
        self.assertEqual(len(det.detect("are met. kennt \u0111\u1ed9ng ether")),
                         1)
        self.assertEqual(len(det.detect("By courage. 255% are happy.")), 1)
        self.assertEqual(len(det.detect("bad \ufffd byte")), 1)
        # Han (not Hangul) suffix is never a Korean particle
        self.assertEqual(len(det.detect(KO_UNIT + "question\u541b " + KO_UNIT)),
                         1)

    def test_codeswitch_predicate(self):
        import tokenizer
        toks = tokenizer.tokenize(KO_UNIT)
        flags = [t.text for i, t in enumerate(toks)
                 if det.is_korean_codeswitch(toks, i)]
        self.assertEqual(flags, ["yes\ub098", "no\ub97c"])

    def test_negative_fixture_shape(self):
        (rec,) = _load(NEGATIVE)
        self.assertEqual(rec["id"], "NEG-001")
        self.assertEqual(rec["char_offset"], 9671)
        self.assertEqual(rec["expected"]["max_confidence"], "CANDIDATE")
        self.assertTrue(rec["unit_quote"].startswith(KO_UNIT[:10]))


@unittest.skipUnless(os.path.isdir(CORPUS), "corpus/ not extracted locally")
class SedonaNegativeCorpusTest(unittest.TestCase):
    """TASK-010 criterion 1 on the frozen transcript (paragraph 0, @9671)."""

    @classmethod
    def setUpClass(cls):
        import loaders
        import run_detectors as rd
        (cls.rec,) = _load(NEGATIVE)
        cls.t = loaders.read_transcript(os.path.join(ROOT,
                                                     cls.rec["transcript"]))
        cls.a = cls.rec["char_offset"]
        cls.b = cls.a + cls.rec["length"]
        cls.recs = rd.records(cls.t, detectors=rd.select("A"))

    def test_span_matches_frozen_corpus(self):
        span = self.t.text[self.a:self.b]
        self.assertEqual(hashlib.sha256(span.encode("utf-8")).hexdigest(),
                         self.rec["sha256"])
        self.assertTrue(span.startswith(self.rec["unit_quote"]))

    def test_no_a2_signal_in_span(self):
        self.assertEqual([s for s in det.detect(self.t.text)
                          if s["start"] < self.b and self.a < s["end"]], [])

    def test_runner_emits_only_candidate_a1(self):
        hits = [r for r in self.recs
                if self.a <= r["location"]["char_offset"] < self.b]
        self.assertEqual([(r["detector_id"], r["confidence"]) for r in hits],
                         [("A1-repetition", "CANDIDATE")])

    def test_no_high_anywhere_in_transcript_from_family_a(self):
        self.assertFalse([r for r in self.recs
                          if r["confidence"] != "CANDIDATE"])
