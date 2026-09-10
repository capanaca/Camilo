"""Parses money amounts out of Latin-American formatted strings.

Bank notification templates mix thousands/decimal separator conventions even
within the same sender (e.g. Bancolombia sends both "500.000,00" and
"3,925,441.00"), so amounts are normalized heuristically rather than assuming
one locale.
"""
import re

_AMOUNT_RE = re.compile(r"-?\d[\d.,]*\d|-?\d")


def parse_amount(text: str) -> float:
    """Extract and normalize the first money amount found in `text`."""
    match = _AMOUNT_RE.search(text.replace(" ", ""))
    if not match:
        raise ValueError(f"No amount found in: {text!r}")
    return _normalize(match.group(0))


def _normalize(raw: str) -> float:
    has_dot = "." in raw
    has_comma = "," in raw

    if has_dot and has_comma:
        decimal_sep = "," if raw.rfind(",") > raw.rfind(".") else "."
        thousands_sep = "." if decimal_sep == "," else ","
        raw = raw.replace(thousands_sep, "")
        raw = raw.replace(decimal_sep, ".")
        return float(raw)

    sep = "." if has_dot else ("," if has_comma else None)
    if sep is None:
        return float(raw)

    digits_after = len(raw) - raw.rfind(sep) - 1
    if digits_after == 2 and raw.count(sep) == 1:
        return float(raw.replace(sep, "."))
    return float(raw.replace(sep, ""))
