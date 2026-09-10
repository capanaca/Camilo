import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from wallettracker.parsers.bancolombia_statement import parse_statement_pages, date_range
from wallettracker.models import DIRECTION_EXPENSE

# Lines mirror the real column layout Bancolombia's statement PDF extracts
# to (auth code, date, description, value, [installments], cuota, interest%,
# interest%, balance), with fake amounts/merchants.

PESOS_PAGE = """Tarjeta: ****1234
NIT: 890.903.938-8 ESTADO DE CUENTA EN: PESOS
Detalles del movimiento
R20071 13/01/2026 TIENDA DEMO $ 10.000,00 1/1 $ 10.000,00 0,0000 % 00,0000 % $ 0,00
000000 17/01/2026 CUOTA DE MANEJO $ 50.960,00 $ 50.960,00 $ 0,00
C56093 17/01/2026 ABONO SUCURSAL VIRTUAL $ -20.000,00 $ -20.000,00 $ 0,00
"""

DOLARES_PAGE = """Tarjeta: ****1234
NIT: 890.903.938-8 ESTADO DE CUENTA EN: DOLARES
Detalles del movimiento
X99887 05/01/2026 TIENDA EXTRANJERA $ 45,30 1/1 $ 45,30 0,0000 % 00,0000 % $ 0,00
"""


def test_parses_purchase_and_fee_skips_abono():
    txns = parse_statement_pages([PESOS_PAGE], "1234")
    kinds = {t.id: t.kind for t in txns}
    assert len(txns) == 2  # ABONO line excluded
    assert any(t.kind == "compra" and t.counterparty == "TIENDA DEMO" for t in txns)
    assert any(t.kind == "cuota_manejo" for t in txns)
    for t in txns:
        assert t.direction == DIRECTION_EXPENSE
        assert t.currency == "COP"
        assert t.source == "bancolombia_extracto"


def test_amounts_and_dates():
    txns = parse_statement_pages([PESOS_PAGE], "1234")
    compra = next(t for t in txns if t.kind == "compra")
    assert compra.amount == 10000.0
    assert compra.date == "2026-01-13"
    manejo = next(t for t in txns if t.kind == "cuota_manejo")
    assert manejo.amount == 50960.0


def test_currency_detected_per_page():
    txns = parse_statement_pages([DOLARES_PAGE], "1234")
    assert len(txns) == 1
    assert txns[0].currency == "USD"
    assert txns[0].amount == 45.30


def test_stable_id_across_reingestion():
    first = parse_statement_pages([PESOS_PAGE], "1234")
    second = parse_statement_pages([PESOS_PAGE], "1234")
    assert [t.id for t in first] == [t.id for t in second]


def test_date_range_helper():
    txns = parse_statement_pages([PESOS_PAGE], "1234")
    assert date_range(txns) == ("2026-01-13", "2026-01-17")
    assert date_range([]) is None
