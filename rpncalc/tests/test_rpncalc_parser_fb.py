"""Tests for feasibility parser tokenization behavior."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from rpncalc.parser_fb import tokenize


@dataclass(frozen=True)
class _SampleValue:
    """Simple value object to exercise __str__ coercion."""

    raw: str

    def __str__(self) -> str:
        return f"value:{self.raw}"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", []),
        ("   ", []),
        ("3 4 +", ["3", "4", "+"]),
        ("3\t4\n+", ["3", "4", "+"]),
        ("  3   4   +  ", ["3", "4", "+"]),
    ],
)
def test_tokenize_basic_whitespace_splitting(
    text: str,
    expected: list[str],
) -> None:
    """Tokenize collapses ASCII whitespace and trims edges."""
    tokens = tokenize(text)

    assert tokens == expected


def test_tokenize_default_is_empty() -> None:
    """Default argument yields no tokens."""
    tokens = tokenize()

    assert tokens == []


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (123, ["123"]),
        (12.5, ["12.5"]),
        (_SampleValue("alpha"), ["value:alpha"]),
    ],
)
def test_tokenize_coerces_non_string_values(
    value: object,
    expected: list[str],
) -> None:
    """Tokenize uses str(...) for non-string inputs."""
    tokens = tokenize(value)

    assert tokens == expected


def test_tokenize_none_current_behavior() -> None:
    """Document current behavior for None input."""
    tokens = tokenize(None)

    assert tokens == ["None"]


def test_tokenize_bytes_string_representation() -> None:
    """Bytes are coerced to their repr-like str value."""
    tokens = tokenize(b"1 2")

    assert tokens == ["b'1", "2'"]


def test_tokenize_repeated_calls_are_deterministic() -> None:
    """Repeated calls with identical input should match."""
    text = "7 8 *"

    first = tokenize(text)
    second = tokenize(text)

    assert first == second
    assert first is not second
