"""Parses Bold payment-gateway emails (approved/rejected purchase receipts)."""
import re
from typing import Optional

from ..amounts import parse_amount
from ..models import Transaction, DIRECTION_EXPENSE, DIRECTION_EXCLUDED

SENDER = "no-responder@bold.co"

_APPROVED = re.compile(r"Transacci[oó]n aprobada", re.IGNORECASE)
_REJECTED = re.compile(r"Transacci[oó]n rechazada", re.IGNORECASE)
_AMOUNT = re.compile(r"\$?\s?(?P<amount>[\d.,]+)\s*COP", re.IGNORECASE)
_MERCHANT = re.compile(r"Comercio\s+(?P<merchant>.+?)(?:\s+M[eé]todo de pago|\s+Referencia|\s+ID transacci[oó]n|$)", re.IGNORECASE)


def matches(sender: str) -> bool:
    return SENDER in sender


def parse(raw_email: dict) -> Optional[Transaction]:
    body = " ".join((raw_email.get("plaintextBody") or "").split())

    approved = _APPROVED.search(body)
    rejected = _REJECTED.search(body)
    if not approved and not rejected:
        return None

    amount_match = _AMOUNT.search(body)
    merchant_match = _MERCHANT.search(body)
    if not amount_match:
        return None

    return Transaction(
        id=raw_email["id"],
        thread_id=raw_email.get("threadId", raw_email["id"]),
        date=raw_email["date"][:10],
        datetime=raw_email["date"],
        amount=parse_amount(amount_match.group("amount")),
        currency="COP",
        direction=DIRECTION_EXCLUDED if rejected else DIRECTION_EXPENSE,
        kind="compra_rechazada" if rejected else "compra",
        status="rechazada" if rejected else "aprobada",
        counterparty=merchant_match.group("merchant").strip() if merchant_match else "Comercio Bold",
        source="bold",
        raw_subject=raw_email.get("subject", ""),
    )
