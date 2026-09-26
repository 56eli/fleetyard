"""tests for tools/m4_prov_check.py — criterion 20.15 made mechanical (TASK-020 item 13)."""
import contextlib
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import m4_prov_check as pc  # noqa: E402


def H(blob):
    return hashlib.sha256(blob).hexdigest()


class ProvCheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="provcheck-")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _tree(self):
        """Minimal inputs + a manifest whose digests are computed independently here."""
        os.makedirs(os.path.join(self.tmp, "records"))
        os.makedirs(os.path.join(self.tmp, "fixtures"))
        os.makedirs(os.path.join(self.tmp, "corpus", "docdocgo", "overlays"))
        os.makedirs(os.path.join(self.tmp, "corpus", "docdocgo", "html"))
        open(os.path.join(self.tmp, "records", "a.json"), "w").write('{"x": 1}\n')
        open(os.path.join(self.tmp, "fixtures", "confirmed.json"), "w").write("[1]\n")
        open(os.path.join(self.tmp, "fixtures", "corrections.json"), "w").write("[2]\n")
        for name, text in (("a.txt", "alpha\n"), ("b.txt", "beta\n")):
            open(os.path.join(self.tmp, "corpus", "docdocgo", "overlays", name), "w").write(text)
        open(os.path.join(self.tmp, "corpus", "docdocgo", "html",
                          "merged-book-texts_json_1.js"), "w").write("{}\n")
        open(os.path.join(self.tmp, "pack.zip"), "wb").write(b"zipbytes")

        rec_lines = sorted("%s  %s\n" % (H(open(os.path.join(self.tmp, "records", "a.json"), "rb").read()), "a.json"))
        fx_lines = sorted("%s  %s\n" % (H(open(os.path.join(self.tmp, "fixtures", f), "rb").read()), f)
                          for f in ("confirmed.json", "corrections.json"))
        ov = []
        for f in ("a.txt", "b.txt"):
            t = open(os.path.join(self.tmp, "corpus", "docdocgo", "overlays", f), "rb").read()
            ov.append("%s  %s" % (H(t), f))
        man = {
            "tool": "tools/noop.py", "tool_commit": "deadbeef",
            "tool_sha256": "0" * 64,
            "book_store": {"path": "corpus/docdocgo/html/merged-book-texts_json_1.js",
                           "sha256": H(b"{}\n")},
            "inputs": {"corpus_zip_sha256": H(b"zipbytes"),
                       "records_digest_sha256": H("".join(rec_lines).encode()),
                       "fixtures_digest_sha256": H("".join(fx_lines).encode()),
                       "overlays_digest": H("".join(x + "\n" for x in ov).encode()),
                       "records_dir": "records"},
            "outputs": {"ledger.jsonl": H(b"{}\n"),
                        "by_transcript_digest": H("".join(
                            sorted("%s  %s\n" % (H(b"[]"), "a.txt.json"))).encode())},
            "derivations": {
                "corpus_zip_sha256": "sha256 of the zip bytes",
                "records_digest_sha256": "sorted lines sha  path-relative",
                "fixtures_digest_sha256": "sorted basename lines over --fixtures",
                "overlays_digest": "lines carry newline, basename order; wrong variant sorts+joins",
                "by_transcript_digest": "same as records over by-transcript/",
                "outputs.ledger.jsonl": "sha256 of the file bytes",
                "tool_sha256": "blob at tool_commit",
            },
        }
        os.makedirs(os.path.join(self.tmp, "findings", "by-transcript"))
        open(os.path.join(self.tmp, "findings", "by-transcript", "a.txt.json"), "w").write("[]")
        open(os.path.join(self.tmp, "findings", "ledger.jsonl"), "w").write("{}\n")
        path = os.path.join(self.tmp, "findings", "PROVENANCE.json")
        open(path, "w", encoding="utf-8").write(json.dumps(man, indent=1, sort_keys=True) + "\n")
        return path

    def _args(self, manifest):
        return ["--manifest", manifest,
                "--records", os.path.join(self.tmp, "records"),
                "--fixtures", os.path.join(self.tmp, "fixtures"),
                "--corpus", os.path.join(self.tmp, "corpus"),
                "--zip", os.path.join(self.tmp, "pack.zip")]

    def test_dir_digest_is_the_stated_construction(self):
        os.makedirs(os.path.join(self.tmp, "d"))
        open(os.path.join(self.tmp, "d", "x.json"), "wb").write(b"hello")
        want = H(("%s  %s\n" % (H(b"hello"), "x.json")).encode())
        self.assertEqual(pc.dir_digest(os.path.join(self.tmp, "d")), want)

    def test_overlays_wrong_variant_is_the_stated_construction(self):
        os.makedirs(os.path.join(self.tmp, "c", "docdocgo", "overlays"))
        for name, text in (("b.txt", "two"), ("a.txt", "one")):
            open(os.path.join(self.tmp, "c", "docdocgo", "overlays", name), "w").write(text)
        lines = ["%s  %s" % (H(t.encode()), n) for n, t in (("a.txt", "one"), ("b.txt", "two"))]
        self.assertEqual(pc.overlays_digest(os.path.join(self.tmp, "c"), "correct"),
                         H(("".join(l + "\n" for l in lines)).encode()))
        self.assertEqual(pc.overlays_digest(os.path.join(self.tmp, "c"), "wrong-sorted-join"),
                         H("\n".join(sorted(lines)).encode()))
        self.assertNotEqual(pc.overlays_digest(os.path.join(self.tmp, "c"), "correct"),
                            pc.overlays_digest(os.path.join(self.tmp, "c"), "wrong-sorted-join"))

    def test_reports_failure_on_a_manifest_that_does_not_reproduce(self):
        man = self._tree()
        doc = json.load(open(man, encoding="utf-8"))
        doc["inputs"]["fixtures_digest_sha256"] = "f" * 64      # the defect item 13 found
        open(man, "w", encoding="utf-8").write(json.dumps(doc, indent=1, sort_keys=True))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(pc.main(self._args(man)), 1)

    @unittest.skipUnless(os.path.exists(os.path.join(ROOT, "corpus", "docdocgo", "overlays")),
                         "corpus not materialised (working input, never committed)")
    @unittest.skipUnless(os.path.exists(os.path.join(ROOT, "evidence", "runs", "m5-raw", "records")),
                         "evidence not materialised (working input, never committed)")
    def test_committed_manifest_reproduces_literally(self):
        p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "m4_prov_check.py")],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("prov check: OK", p.stdout)


if __name__ == "__main__":
    unittest.main()
