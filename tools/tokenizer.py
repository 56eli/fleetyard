"""Word tokenizer with char offsets (TASK-002 / M1). Stdlib only.

A token is a run of letters/digits, optionally joined by internal
apostrophes (straight or curly) or hyphens: "don't", "self-healing",
"Hawkins’", "200". Punctuation and whitespace are not tokens.
"""
import re
from collections import namedtuple

Token = namedtuple("Token", "text start end")

_WORD = re.compile(r"[^\W_]+(?:['\u2019\-][^\W_]+)*", re.UNICODE)


def tokenize(text):
    """List of Token(text, start, end) with text == source[start:end]."""
    return [Token(m.group(0), m.start(), m.end())
            for m in _WORD.finditer(text)]


def words(text, lower=True):
    """Plain word list (lower-cased by default; curly apostrophes -> ')."""
    out = [t.text.replace("\u2019", "'") for t in tokenize(text)]
    return [w.lower() for w in out] if lower else out
