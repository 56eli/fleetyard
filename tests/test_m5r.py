#!/usr/bin/env python3
"""Tests for the M5-R ledger reducer (stdlib unittest).

Covers: book-store parsing, citation verification, dedupe + overlap merge,
multi-detector split, fixture (seeded) labelling, the classification ladder
(CERTAIN never assigned by the tool; HIGH needs two independent families and a
verified book leg), non-Hawkins labelling, and byte-level determinism.
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import m5r_reduce as m5r  # noqa: E402

BOOKJS = """const the_json_obj_books = {
    "book_one": `
My father was a great musician.
The table says 55% of people are happy.
`,
    "Lamsa_bible": `
Blessed are the meek.
`,
};
"""

T1 = "great musician plays. great musician plays. great musician plays."
T2 = "Amen Amen Amen Amen. The table says 255% of people are happy."
T3 = "classic musician plays well today."
TR = {"T1_enxautogen_html.txt": T1, "T2_enxautogen_html.txt": T2,
      "T3_enxautogen_html.txt": T3}


def rec(transcript, offset, quote, detector, intended=None, book=None):
    return {
        "transcript_path": "corpus/docdocgo/overlays/" + transcript,
        "location": {"paragraph": 0, "char_offset": offset},
        "quoted_text": quote,
        "suspected_intended_text": intended,
        "evidence_class": "signals: %s (test)" % detector,
        "detector_id": detector,
        "book_reference": book,
        "status": "open",
        "status_by": "run_detectors (automatic, unreviewed)",
        "raw_runner_confidence": "CANDIDATE",
        "reporting_class": "CANDIDATE-class raw signal, unreviewed",
        "review_status": "unreviewed",
    }


class M5RCase(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="m5r-test-")
        self.corpus = os.path.join(self.root, "corpus")
        ov = os.path.join(self.corpus, "docdocgo", "overlays")
        html = os.path.join(self.corpus, "docdocgo", "html")
        os.makedirs(ov)
        os.makedirs(html)
        for name, text in TR.items():
            with open(os.path.join(ov, name), "w", encoding="utf-8") as fh:
                fh.write(text)
        with open(os.path.join(html, "merged-book-texts_json_1.js"), "w",
                  encoding="utf-8") as fh:
            fh.write(BOOKJS)
        self.books = m5r.parse_book_store(
            os.path.join(html, "merged-book-texts_json_1.js"))
        self.records = os.path.join(self.root, "records")
        self.fixtures = os.path.join(self.root, "fixtures")
        os.makedirs(self.records)
        os.makedirs(self.fixtures)
        book_one = self.books["book_one"]
        self.off_great = book_one.index("great musician")
        self.off_55 = book_one.index("55% of people are happy")
        self.off_255 = T2.index("255%")
        rows = [
            # T1: A1 repetition, no second signal -> CANDIDATE
            rec("T1_enxautogen_html.txt", 0, T1, "A1-repetition", "great musician plays."),
            # T2: A1 repetition (duplicated row -> dedupe) -> CANDIDATE
            rec("T2_enxautogen_html.txt", 0, "Amen Amen Amen Amen.", "A1-repetition", "Amen"),
            rec("T2_enxautogen_html.txt", 0, "Amen Amen Amen Amen.", "A1-repetition", "Amen"),
            # T2: A2+B1 with a verified book leg, covered by a fixture -> CERTAIN(inherited)
            rec("T2_enxautogen_html.txt", self.off_255, "255%", "A2-nonsense+B1-contradiction", "55%",
                {"slug": "book_one", "char_offset": self.off_55,
                 "quote": "55% of people are happy"}),
            # T3: surface+content families converge, verified book leg -> HIGH (proposed)
            rec("T3_enxautogen_html.txt", 0, "classic musician",
                "A1-repetition+B2-misquote", "great musician",
                {"slug": "book_one", "char_offset": self.off_great,
                 "quote": "great musician"}),
            # citation failure specimen (quote not at offset) -> rejected from ledger
            rec("T3_enxautogen_html.txt", 0, "classic violin", "B2-misquote"),
        ]
        for i, r in enumerate(rows[:5]):
            with open(os.path.join(self.records, "r%d.json" % i), "w",
                      encoding="utf-8") as fh:
                json.dump([r], fh)
        with open(os.path.join(self.records, "r9.json"), "w", encoding="utf-8") as fh:
            json.dump([rows[5]], fh)
        with open(os.path.join(self.fixtures, "confirmed.json"), "w",
                  encoding="utf-8") as fh:
            json.dump([{
                "id": "CF-TEST", "transcript": "corpus/docdocgo/overlays/T2_enxautogen_html.txt",
                "paragraph": 0, "char_offset": self.off_255, "quoted": "255%", "suspected": "55%",
                "evidence_class": "b", "evidence": "test fixture", "detector": "hand-read",
                "book_ref": {"slug": "book_one", "char_offset": self.off_55,
                             "quote": "55% of people are happy"},
                "confidence": "CERTAIN", "status": "confirmed",
                "status_by": "test", }], fh)

    def tearDown(self):
        shutil.rmtree(self.root)

    def run_reducer(self, out):
        rc = m5r.main(["--records", self.records, "--fixtures", self.fixtures,
                       "--corpus", self.corpus, "--out", out,
                       "--utc", "2026-01-01T00:00:00Z"])
        self.assertEqual(rc, 0)
        return json.load(open(os.path.join(out, "PROVENANCE.json"), encoding="utf-8")), \
            [json.loads(l) for l in open(os.path.join(out, "ledger.jsonl"), encoding="utf-8")]

    # ---------------------------------------------------------------- tests
    def test_book_store_parses_all_slugs_with_offsets(self):
        self.assertEqual(sorted(self.books), ["Lamsa_bible", "book_one"])
        self.assertEqual(self.books["book_one"].index("great musician"), self.off_great)

    def test_reduction_counts_classes_and_seeded_flag(self):
        out = os.path.join(self.root, "out")
        prov, findings = self.run_reducer(out)
        s = prov["stats"]
        self.assertEqual(s["raw_signals"], 8)   # 6 records; 2 carry 2 signals
        self.assertEqual(s["citation_failures"], 1)
        self.assertEqual(s["duplicates_removed"], 1)
        self.assertEqual(len(findings), 4)
        by = {f["id"]: f for f in findings}
        t2_255 = [f for f in findings if f["transcript"] == "T2_enxautogen_html.txt"
                  and f["char_offset"] == self.off_255][0]
        self.assertTrue(t2_255["class"].startswith("CERTAIN"))
        self.assertTrue(t2_255["seeded"])
        self.assertEqual(t2_255["fixture_overlap"][0]["id"], "CF-TEST")
        self.assertTrue(all(b["quote_ok"] for b in t2_255["book_checks"]))
        self.assertEqual(t2_255["book_checks"][0]["numbers"]["differ"], True)
        t3 = [f for f in findings if f["transcript"] == "T3_enxautogen_html.txt"][0]
        self.assertTrue(t3["class"].startswith("HIGH"))
        self.assertIn("independent", t3["rationale"].lower())
        self.assertFalse(t3["seeded"])
        amen = [f for f in findings if f["char_offset"] == 0
                and f["transcript"].startswith("T2")][0]
        self.assertEqual(amen["class"], "CANDIDATE")
        self.assertTrue(amen["rederived_repetition"]["span_fully_periodic"])
        self.assertEqual(len(by), len(findings))

    def test_fixture_overlap_uses_the_fixture_quoted_span(self):
        """A finding that starts after the fixture offset but inside its quoted
        text must still be labelled seeded (CF-015 case in the real corpus)."""
        phrase = "255%"
        recs = [rec("T2_enxautogen_html.txt", self.off_255 + 1, "55%",
                    "B2-misquote", "55%")]
        # widen the fixture's quoted text to cover the later finding
        fx = json.load(open(os.path.join(self.fixtures, "confirmed.json"), encoding="utf-8"))
        fx[0]["quoted"] = "says 255%"
        fx[0]["char_offset"] = self.off_255 - 5
        with open(os.path.join(self.fixtures, "confirmed.json"), "w", encoding="utf-8") as fh:
            json.dump(fx, fh)
        with open(os.path.join(self.records, "rz.json"), "w", encoding="utf-8") as fh:
            json.dump(recs, fh)
        out = os.path.join(self.root, "outz")
        _, findings = self.run_reducer(out)
        hits = [x for x in findings if x["transcript"].startswith("T2")
                and x["char_offset"] <= self.off_255 + 1 < x["span_end"]]
        self.assertEqual(len(hits), 1)
        f = hits[0]
        self.assertTrue(f["seeded"])
        self.assertTrue(f["class"].startswith("CERTAIN"))

    def test_never_assigns_certain_without_inherited_fixture(self):
        out = os.path.join(self.root, "out2")
        _, findings = self.run_reducer(out)
        for f in findings:
            if f["class"].startswith("CERTAIN"):
                self.assertTrue(f["fixture_overlap"])

    def test_determinism_byte_identical(self):
        of1 = os.path.join(self.root, "o1")
        of2 = os.path.join(self.root, "o2")
        p1, f1 = self.run_reducer(of1)
        p2, f2 = self.run_reducer(of2)
        self.assertEqual(json.dumps(f1, sort_keys=True), json.dumps(f2, sort_keys=True))
        self.assertEqual(p1["outputs"], p2["outputs"])
        for name in ("ledger.jsonl", "SUMMARY.md"):
            self.assertEqual(open(os.path.join(of1, name), "rb").read(),
                             open(os.path.join(of2, name), "rb").read())

    def test_non_hawkins_book_reference_is_flagged(self):
        rows = [rec("T1_enxautogen_html.txt", 0, "great musician plays.", "B2-misquote",
                    "great musician",
                    {"slug": "Lamsa_bible", "char_offset": 0, "quote": "Blessed are"})]
        with open(os.path.join(self.records, "rx.json"), "w", encoding="utf-8") as fh:
            json.dump(rows, fh)
        out = os.path.join(self.root, "out3")
        prov, findings = self.run_reducer(out)
        f = [x for x in findings if x["transcript"].startswith("T1")][0]
        self.assertEqual(f["book_checks"][0]["hawkins_own"], False)
        self.assertEqual(prov["stats"]["book_refs_nonhawkins"], 1)

    def test_by_transcript_covers_every_corpus_file(self):
        out = os.path.join(self.root, "out4")
        self.run_reducer(out)
        files = sorted(os.listdir(os.path.join(out, "by-transcript")))
        self.assertEqual(files, sorted(n + ".json" for n in TR))
        empty = json.load(open(os.path.join(out, "by-transcript",
                                            "T1_enxautogen_html.txt.json"), encoding="utf-8"))
        self.assertTrue(len(empty) >= 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
