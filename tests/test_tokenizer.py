"""Tests for tools/tokenizer.py (TASK-002)."""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import tokenizer  # noqa: E402


class TokenizerTest(unittest.TestCase):
    def test_tokens_and_offsets(self):
        text = "Don't self-heal, Hawkins\u2019 200 calibrations!"
        toks = tokenizer.tokenize(text)
        self.assertEqual([t.text for t in toks],
                         ["Don't", "self-heal", "Hawkins", "200",
                          "calibrations"])
        for t in toks:
            self.assertEqual(text[t.start:t.end], t.text)

    def test_words_normalizes(self):
        self.assertEqual(tokenizer.words("It\u2019s THE Self"),
                         ["it's", "the", "self"])
        self.assertEqual(tokenizer.words("A b", lower=False), ["A", "b"])

    def test_no_punctuation_or_underscore_tokens(self):
        self.assertEqual(tokenizer.words("... -- _ ' \u2014 !?"), [])

    def test_unicode_letters(self):
        self.assertEqual(tokenizer.words("caf\u00e9 \uc9c4\uc2e4"),
                         ["caf\u00e9", "\uc9c4\uc2e4"])
