# rpncalc/parser.py

from __future__ import annotations


def tokenize_minimal(text: str) -> list[str]:
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
    if text is None:
        return []

    # str(...) is the lowest-friction "total" conversion in Python.
    # Using split() (no sep) collapses runs of whitespace and strips edges.
    return str(text).split()
