"""Parses Banco Santander (Chile) fund-transfer receipt emails."""
import re
from typing import Optional

from ..amounts import parse_amount
from ..models import Transaction, DIRECTION_INCOME

SENDER = "mensajeria@santander.cl"

_SENDER_NAME = re.compile(r"nuestro cliente (?P<merchant>.+?) realiz[oó] una transferencia", re.IGNORECASE)
_AMOUNT = re.compile(r"Monto transferido\s*\$\s?(?P<amount>[\d.,]+)", re.IGNORECASE)


def matches(sender: str) -> bool:
    return SENDER in sender


def parse(raw_email: dict) -> Optional[Transaction]:
    body = " ".join((raw_email.get("plaintextBody") or "").split())

    if "transferencia de fondos" not in raw_email.get("subject", "").lower():
        return None

    amount_match = _AMOUNT.search(body)
    sender_match = _SENDER_NAME.search(body)
    if not amount_match:
        return None

    return Transaction(
        id=raw_email["id"],
        thread_id=raw_email.get("threadId", raw_email["id"]),
        date=raw_email["date"][:10],
        datetime=raw_email["date"],
        amount=parse_amount(amount_match.group("amount")),
        currency="CLP",
        direction=DIRECTION_INCOME,
        kind="transferencia_recibida",
        status="aprobada",
        counterparty=sender_match.group("merchant").strip() if sender_match else "Desconocido",
        source="santander",
        raw_subject=raw_email.get("subject", ""),
    )
