"""Parses the itemized transaction table from a Bancolombia credit card
statement PDF ("Detalle del movimiento" pages).

This is the authoritative source for card purchases: unlike the per-purchase
notification emails (which only exist for Mercado Pago/Bold-routed payments),
the statement lists every purchase regardless of payment gateway. Splitting
PDF-to-text extraction (thin, in scripts/ingest_statement_pdf.py) from line
parsing (here, pure) keeps this testable without a PDF fixture.
"""
import re
from datetime import datetime

from ..amounts import parse_amount
from ..models import Transaction, DIRECTION_EXPENSE

_LINE_RE = re.compile(
    r"^(?P<auth>\S+)\s+(?P<date>\d{2}/\d{2}/\d{4})\s+(?P<desc>.+?)\s+\$\s*(?P<amount>-?[\d.,]+)"
)
_CURRENCY_HEADER_RE = re.compile(r"ESTADO DE CUENTA EN:\s*(DOLARES|PESOS)", re.IGNORECASE)
_CURRENCY_MAP = {"DOLARES": "USD", "PESOS": "COP"}


def parse_statement_pages(pages_text: list[str], card_last4: str) -> list[Transaction]:
    transactions = []
    currency = "COP"

    for page_text in pages_text:
        header_match = _CURRENCY_HEADER_RE.search(page_text)
        if header_match:
            currency = _CURRENCY_MAP[header_match.group(1).upper()]

        for line in page_text.splitlines():
            match = _LINE_RE.match(line.strip())
            if not match:
                continue

            groups = match.groupdict()
            desc = groups["desc"].strip()
            amount_str = groups["amount"]

            if amount_str.startswith("-") or "ABONO" in desc.upper():
                # Credits/payments toward the card balance are already
                # captured via the "Pagaste $X en la tarjeta de credito"
                # bank notification emails; skip here to avoid double-counting.
                continue

            date_iso = datetime.strptime(groups["date"], "%d/%m/%Y").strftime("%Y-%m-%d")
            kind = "cuota_manejo" if "CUOTA DE MANEJO" in desc.upper() else "compra"
            statement_id = f"bancolombia_stmt_{card_last4}_{groups['auth']}_{groups['date'].replace('/', '')}"

            transactions.append(Transaction(
                id=statement_id,
                thread_id=statement_id,
                date=date_iso,
                datetime=date_iso,
                amount=parse_amount(amount_str),
                currency=currency,
                direction=DIRECTION_EXPENSE,
                kind=kind,
                status="aprobada",
                counterparty=desc,
                source="bancolombia_extracto",
                account_ref=card_last4,
            ))

    return transactions


def date_range(transactions: list[Transaction]) -> tuple[str, str] | None:
    """Min/max date covered by these transactions, for cross-source dedup."""
    if not transactions:
        return None
    dates = [t.date for t in transactions]
    return min(dates), max(dates)
