"""Parses Bancolombia "Alertas y Notificaciones" emails.

The sender reuses one subject line ("Alertas y Notificaciones") for many
transaction types, so everything hinges on matching the body sentence.
Amount formatting is inconsistent even within this one sender (both
"500.000,00" and "3,925,441.00" show up), which is why amounts.parse_amount
does locale-agnostic normalization rather than assuming one convention.
"""
import re
from typing import Optional

from ..amounts import parse_amount
from ..models import (
    Transaction,
    DIRECTION_EXPENSE,
    DIRECTION_INCOME,
    DIRECTION_INTERNAL,
    DIRECTION_EXCLUDED,
)

SENDER = "alertasynotificaciones@bancolombia.com.co"

_PATTERNS = [
    (
        "compra_rechazada",
        re.compile(
            r"tu compra en (?P<merchant>.+?) por COP\s?(?P<amount>[\d.,]+)\s+no fue exitosa.*?"
            r"T\.Credito \*(?P<card>\d+)",
            re.IGNORECASE | re.DOTALL,
        ),
        DIRECTION_EXCLUDED,
        "rechazada",
    ),
    (
        "retiro",
        re.compile(
            r"Retiraste \$(?P<amount>[\d.,]+) en (?P<merchant>.+?) de tu T\.Deb \*\*(?P<card>\d+)",
            re.IGNORECASE,
        ),
        DIRECTION_EXPENSE,
        "aprobada",
    ),
    (
        "retiro_fiducuenta",
        re.compile(
            r"RETIRO por \$(?P<amount>[\d.,]+) desde tu producto \*(?P<card>\d+)\s*(?P<merchant>FIDUCUENTA)",
            re.IGNORECASE,
        ),
        DIRECTION_EXPENSE,
        "aprobada",
    ),
    (
        "nomina",
        re.compile(
            r"Recibiste un pago de Nomina de (?P<merchant>.+?) por \$(?P<amount>[\d.,]+) en tu cuenta",
            re.IGNORECASE,
        ),
        DIRECTION_INCOME,
        "aprobada",
    ),
    (
        "pago_tarjeta_credito",
        re.compile(
            r"Pago de Tarjeta de Credito por \$(?P<amount>[\d.,]+) desde cta \*(?P<card>\d+) a la tarjeta \*(?P<card2>\d+)",
            re.IGNORECASE,
        ),
        DIRECTION_INTERNAL,
        "aprobada",
    ),
    (
        "pago_tarjeta_credito",
        re.compile(
            r"Pagaste \$(?P<amount>[\d.,]+) en la tarjeta de credito \*(?P<card2>\d+) desde la cuenta \*(?P<card>\d+)",
            re.IGNORECASE,
        ),
        DIRECTION_INTERNAL,
        "aprobada",
    ),
    (
        "compra",
        re.compile(
            r"Compraste (?P<currency>USD|COP)?\s?(?P<amount>[\d.,]+) en (?P<merchant>.+?) con tu T\.Cred \*(?P<card>\d+)",
            re.IGNORECASE,
        ),
        DIRECTION_EXPENSE,
        "aprobada",
    ),
    (
        "transferencia_recibida",
        re.compile(
            r"Recibiste una transferencia por \$(?P<amount>[\d.,]+) de (?P<merchant>.+?) en tu cuenta",
            re.IGNORECASE,
        ),
        DIRECTION_INCOME,
        "aprobada",
    ),
]


def matches(sender: str) -> bool:
    return SENDER in sender


def parse(raw_email: dict) -> Optional[Transaction]:
    body = " ".join((raw_email.get("plaintextBody") or "").split())

    for kind, pattern, direction, status in _PATTERNS:
        m = pattern.search(body)
        if not m:
            continue
        groups = m.groupdict()
        merchant = groups.get("merchant", "").strip(" .,") or f"Tarjeta *{groups.get('card2', '')}"
        card = groups.get("card", "")
        return Transaction(
            id=raw_email["id"],
            thread_id=raw_email.get("threadId", raw_email["id"]),
            date=raw_email["date"][:10],
            datetime=raw_email["date"],
            amount=parse_amount(groups["amount"]),
            currency=groups.get("currency") or "COP",
            direction=direction,
            kind=kind,
            status=status,
            counterparty=merchant,
            source="bancolombia",
            account_ref=card,
            raw_subject=raw_email.get("subject", ""),
        )
    return None
