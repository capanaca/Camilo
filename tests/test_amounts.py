import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from wallettracker.amounts import parse_amount


def test_latin_thousands_and_decimals():
    assert parse_amount("500.000,00") == 500000.0


def test_us_thousands_and_decimals():
    assert parse_amount("3,925,441.00") == 3925441.0


def test_dot_as_thousands_only():
    assert parse_amount("120.840") == 120840.0
    assert parse_amount("1.100.000") == 1100000.0


def test_comma_as_decimal_only():
    assert parse_amount("5,66") == 5.66


def test_plain_integer():
    assert parse_amount("18000") == 18000.0


def test_with_currency_prefix():
    assert parse_amount("$960.000 COP") == 960000.0
