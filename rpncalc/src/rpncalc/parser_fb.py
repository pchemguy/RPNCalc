# parser_fb.py

"""Feasibility probes for parser.py

This module contains minimalistic code snippets implementing feasibility
probes for parser.py. Routines are intentionally dumb and side-effect free.

"""

from __future__ import annotations


def tokenize(text: str = "") -> list[str]:
    """Return whitespace-delimited tokens with zero validation.

    Feasibility-probe parser:
    - Accepts any input value.
    - Converts to string ("" if None).
    - Splits on arbitrary ASCII whitespace (like str.split()).
    - Never raises for malformed/unknown tokens (no validation performed).

    Args:
      text: Value to tokenize.

    Returns:
      List of tokens (possibly empty).
    """
    # str(...) is the lowest-friction "total" conversion in Python.
    # Using split() (no sep) collapses runs of whitespace and strips edges.
    return str(text).split()
