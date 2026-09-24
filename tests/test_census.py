"""Tests for tools/census.py (TASK M0)."""
import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import census  # noqa: E402

CORPUS = os.path.join(ROOT, "corpus", "docdocgo")


class ParseNameTest(unittest.TestCase):
    def test_dated_with_suffix(self):
        r = census.parse_name("Alignment_Apr_2005_Part_1_enxautogen_html.txt")
        self.assertEqual((r["title"], r["month"], r["year"], r["part"],
                          r["suffix"]), ("Alignment", "Apr", 2005, 1, True))

    def test_dated_without_suffix(self):
        r = census.parse_name("Serenity_Aug_2005_Part_2.txt")
        self.assertEqual((r["title"], r["year"], r["part"], r["suffix"]),
                         ("Serenity", 2005, 2, False))

    def test_dated_no_part(self):
        r = census.parse_name(
            "Question_Answer_Session_Jan_2011_enxautogen_html.txt")
        self.assertEqual((r["title"], r["month"], r["year"], r["part"]),
                         ("Question Answer Session", "Jan", 2011, None))

    def test_undated_is_not_guessed(self):
        r = census.parse_name(
            "Satsang_Series_Volume_IX_Part_3_enxautogen_html.txt")
        self.assertEqual((r["title"], r["month"], r["year"], r["part"]),
                         ("Satsang Series Volume IX", None, None, 3))
        r = census.parse_name("Spiritual_First_Aid_enxautogen_html.txt")
        self.assertEqual((r["title"], r["year"], r["part"]),
                         ("Spiritual First Aid", None, None))

    def test_commas_and_apostrophe_stems(self):
        r = census.parse_name(
            "Belief,_Trust_and_Credibility_Jun_2008_Part_3_enxautogen_html.txt")
        self.assertEqual((r["title"], r["year"]),
                         ("Belief, Trust and Credibility", 2008))


class InspectBytesTest(unittest.TestCase):
    def test_facts(self):
        f = census.inspect_bytes("a b\u00e9\r\n".encode("utf-8"))
        self.assertTrue(f["utf8"])
        self.assertTrue(f["crlf"])
        self.assertEqual((f["words"], f["non_ascii"], f["newlines"]),
                         (2, 1, 1))

    def test_invalid_utf8_and_bom(self):
        f = census.inspect_bytes(b"\xef\xbb\xbfok \xff")
        self.assertFalse(f["utf8"])
        self.assertTrue(f["bom"])
        self.assertEqual(f["replacement_chars"], 1)


class SyntheticCorpusTest(unittest.TestCase):
    """Anomaly detection on a tiny synthetic corpus (no real corpus needed)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = self.tmp.name
        od = os.path.join(root, "overlays")
        os.makedirs(od)
        files = {
            "X_Jan_2002_Part_1_enxautogen_html.txt": b"one two",
            "X_Jan_2002_Part_3_enxautogen_html.txt": b"one two",  # dup+gap
            "X_Jan_2002_Part_3.txt": b"three",                     # dup key
            "Empty_Feb_2003_Part_1_enxautogen_html.txt": b"",
        }
        for n, b in files.items():
            with open(os.path.join(od, n), "wb") as fh:
                fh.write(b)
        man = [{"key": "X_Jan_2002_Part_1_enxautogen_html", "chars": 7,
                "words": 2},
               {"key": "Gone_Part_1", "chars": 1, "words": 1},
               {"key": "Empty_Feb_2003_Part_1_enxautogen_html", "chars": 9,
                "words": 2}]
        with open(os.path.join(od, "manifest.json"), "w") as fh:
            json.dump(man, fh)
        self.data = census.census(root)
        self.an = census.anomalies(self.data)

    def tearDown(self):
        self.tmp.cleanup()

    def test_counts(self):
        self.assertEqual(self.data["entries"], 5)
        self.assertEqual(len(self.data["rows"]), 4)
        self.assertIsNone(self.data["book_bytes"])

    def test_anomalies(self):
        an = self.an
        self.assertEqual(an["empty"],
                         ["Empty_Feb_2003_Part_1_enxautogen_html.txt"])
        self.assertEqual(len(an["dup_content"]), 1)
        self.assertEqual(len(an["dup_key"]), 1)
        self.assertEqual(an["no_suffix"], ["X_Jan_2002_Part_3.txt"])
        self.assertEqual(an["part_gaps"], [("X", "Jan", 2002, [1, 3, 3])])
        m = an["manifest"]
        self.assertEqual(m["missing_files"], ["Gone_Part_1"])
        self.assertEqual(len(m["unlisted_files"]), 2)
        self.assertEqual(m["exact"], 1)
        self.assertEqual(len(m["drift"]), 1)

    def test_render_deterministic(self):
        self.assertEqual(census.render(self.data), census.render(self.data))
        self.assertIn("MISMATCH", census.render(self.data))


@unittest.skipUnless(os.path.isdir(CORPUS), "corpus/ not extracted locally")
class RealCorpusTest(unittest.TestCase):
    """Battery cross-check + committed table freshness (needs corpus/)."""

    @classmethod
    def setUpClass(cls):
        cls.data = census.census(CORPUS)

    def test_battery(self):
        self.assertEqual(self.data["entries"], 231)
        self.assertEqual(self.data["book_bytes"], 14634979)
        # The battery's "≈14.3 MB" is all 231 entries (manifest included).
        total = sum(r["bytes"] for r in self.data["rows"]) + \
            sum(o["bytes"] for o in self.data["others"])
        self.assertEqual(round(total / 1e6, 1), 14.3)

    def test_committed_table_is_fresh(self):
        with open(os.path.join(ROOT, "tools", "CORPUS.md"),
                  encoding="utf-8") as fh:
            self.assertEqual(fh.read(), census.render(self.data))


if __name__ == "__main__":
    unittest.main()
