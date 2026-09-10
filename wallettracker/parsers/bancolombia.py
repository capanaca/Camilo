"""Parses Bancolombia "Alertas y Notificaciones" emails.

Bancolombia sends these from two different domains that behave the same:
`alertasynotificaciones@bancolombia.com.co` (aggregate/occasional alerts —
card-statement payments, ATM withdrawals, incoming transfers) and
`alertasynotificaciones@an.notificacionesbancolombia.com` (a much higher
volume, near-real-time feed that fires on every single purchase, transfer,
QR payment, etc.).

The sender reuses one subject line ("Alertas y Notificaciones") for every
transaction type, so everything hinges on matching the body sentence.
Amount formatting is inconsistent even within one sender (both
"500.000,00" and "3,925,441.00" show up), which is why amounts.parse_amount
does locale-agnostic normalization rather than assuming one convention.

The transaction date is parsed out of the message body wherever present,
rather than trusting the email's arrival timestamp: a transaction made late
at night in Colombia (UTC-5) can generate an email timestamped after
midnight UTC the *next* day, which would otherwise misfile it into the
wrong day (and wrong month, near month boundaries).
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

SENDERS = (
    "alertasynotificaciones@bancolombia.com.co",
    "alertasynotificaciones@an.notificacionesbancolombia.com",
)

_DATE_DMY = r"(?P<txn_date>\d{2}/\d{2}/\d{2,4})"
_DATE_ISO = r"(?P<txn_date_iso>\d{4}-\d{2}-\d{2})"

_PATTERNS = [
    (
        "compra_rechazada",
        re.compile(
            r"tu compra en (?P<merchant>.+?) por COP\s?(?P<amount>[\d.,]+)\s+no fue exitosa.*?"
            r"T\.Credito \*(?P<card>\d+) no se afecto\.\s*\d{2}:\d{2}\." + _DATE_DMY,
            re.IGNORECASE | re.DOTALL,
        ),
        DIRECTION_EXCLUDED,
        "rechazada",
    ),
    (
        "retiro",
        re.compile(
            r"Retiraste \$(?P<amount>[\d.,]+) en (?P<merchant>.+?) de tu T\.Deb \*\*(?P<card>\d+) el " + _DATE_DMY,
            re.IGNORECASE,
        ),
        DIRECTION_EXPENSE,
        "aprobada",
    ),
    (
        "retiro_fiducuenta",
        re.compile(
            r"RETIRO por \$(?P<amount>[\d.,]+) desde tu producto \*(?P<card>\d+)\s*(?P<merchant>FIDUCUENTA)\s*"
            + _DATE_ISO,
            re.IGNORECASE,
        ),
        DIRECTION_EXPENSE,
        "aprobada",
    ),
    (
        "nomina",
        re.compile(
            r"Recibiste un pago de Nomina de (?P<merchant>.+?) por \$(?P<amount>[\d.,]+) en tu cuenta"
            r".*?el " + _DATE_DMY,
            re.IGNORECASE,
        ),
        DIRECTION_INCOME,
        "aprobada",
    ),
    (
        "pago_tarjeta_credito",
        re.compile(
            r"Pago de Tarjeta de Credito por \$(?P<amount>[\d.,]+) desde cta \*(?P<card>\d+) a la tarjeta "
            r"\*(?P<card2>\d+)\.\s*" + _DATE_DMY,
            re.IGNORECASE,
        ),
        DIRECTION_INTERNAL,
        "aprobada",
    ),
    (
        "pago_tarjeta_credito",
        re.compile(
            r"Pagaste \$(?P<amount>[\d.,]+) en la tarjeta de credito \*(?P<card2>\d+) desde la cuenta "
            r"\*(?P<card>\d+),\s*el " + _DATE_DMY,
            re.IGNORECASE,
        ),
        DIRECTION_INTERNAL,
        "aprobada",
    ),
    (
        "compra",
        re.compile(
            r"Compraste (?P<currency>USD|COP)?\s?(?P<amount>[\d.,]+) en (?P<merchant>.+?)"
            r"(?:\s+con tu T\.Cred \*(?P<card>\d+))?,\s*el " + _DATE_DMY,
            re.IGNORECASE,
        ),
        DIRECTION_EXPENSE,
        "aprobada",
    ),
    (
        "transferencia_recibida",
        re.compile(
            r"Recibiste una transferencia por \$(?P<amount>[\d.,]+) de (?P<merchant>.+?) en tu cuenta"
            r".*?el " + _DATE_DMY,
            re.IGNORECASE,
        ),
        DIRECTION_INCOME,
        "aprobada",
    ),
    (
        "transferencia_enviada",
        re.compile(
            r"Transferiste \$(?P<amount>[\d.,]+) desde tu cuenta \*(?P<card>\d+) a la cuenta \*\s?"
            r"(?P<dest>\d+) el " + _DATE_DMY,
            re.IGNORECASE,
        ),
        DIRECTION_EXPENSE,
        "aprobada",
    ),
    (
        "transferencia_enviada",
        re.compile(
            r"transferiste \$(?P<amount>[\d.,]+) a la llave @(?P<dest>\S+) desde tu cuenta \*(?P<card>\d+)",
            re.IGNORECASE,
        ),
        DIRECTION_EXPENSE,
        "aprobada",
    ),
    (
        "pago_qr",
        re.compile(
            r"pagaste \$(?P<amount>[\d.,]+) por codigo QR desde tu cuenta \*(?P<card>\d+) a la llave "
            r"(?P<dest>\S+)",
            re.IGNORECASE,
        ),
        DIRECTION_EXPENSE,
        "aprobada",
    ),
]


def matches(sender: str) -> bool:
    return any(s in sender for s in SENDERS)


def _resolve_date(groups: dict, email_date_iso: str) -> tuple[str, str]:
    """Prefer the transaction date embedded in the body over the email's
    arrival timestamp (see module docstring for why they can disagree)."""
    if groups.get("txn_date_iso"):
        iso = groups["txn_date_iso"]
        return iso, iso
    txn_date = groups.get("txn_date")
    if txn_date:
        day, month, year = txn_date.split("/")
        if len(year) == 2:
            year = "20" + year
        iso = f"{year}-{month}-{day}"
        return iso, iso
    return email_date_iso[:10], email_date_iso


def parse(raw_email: dict) -> Optional[Transaction]:
    body = " ".join((raw_email.get("plaintextBody") or "").split())

    for kind, pattern, direction, status in _PATTERNS:
        m = pattern.search(body)
        if not m:
            continue
        groups = m.groupdict()
        merchant = groups.get("merchant")
        if not merchant:
            if groups.get("dest"):
                label = "cuenta" if kind == "transferencia_enviada" and groups["dest"].isdigit() else "llave"
                merchant = f"Transferencia a {label} {groups['dest']}" if kind == "transferencia_enviada" \
                    else f"Pago QR a llave {groups['dest']}"
            else:
                merchant = f"Tarjeta *{groups.get('card2', '')}"
        merchant = merchant.strip(" .,")
        card = groups.get("card", "")
        date_iso, datetime_iso = _resolve_date(groups, raw_email["date"])

        return Transaction(
            id=raw_email["id"],
            thread_id=raw_email.get("threadId", raw_email["id"]),
            date=date_iso,
            datetime=datetime_iso,
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
