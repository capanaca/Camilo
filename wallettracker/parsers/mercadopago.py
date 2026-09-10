"""Parses Mercado Pago payment-notification emails (approved/rejected/received)."""
import re
from typing import Optional

from ..amounts import parse_amount
from ..models import Transaction, DIRECTION_EXPENSE, DIRECTION_EXCLUDED

SENDERS = ("info@mercadopago.com", "no-responder@mercadopago.com")

_MERCHANT_FROM_SUBJECT = re.compile(r"Pago (?:aprobado|rechazado) en (?P<merchant>.+)", re.IGNORECASE)
# Approved emails say "Pagaste $ X"; rejected ones just show "$ X" with no
# verb, so the amount is picked up as the last "$ ..." occurrence in the body
# rather than requiring the "Pagaste" prefix.
_AMOUNT_ANY = re.compile(r"\$\s?(?P<amount>[\d.,]+)")
_RECEIVED_AMOUNT = re.compile(r"ya recibi[oó] tu pago.*?\$\s?(?P<amount>[\d.,]+)", re.IGNORECASE | re.DOTALL)
_RECEIVED_MERCHANT = re.compile(r"^(?P<ref>\S+)?\s*(?P<merchant>.+?) ya recibi[oó] tu pago", re.IGNORECASE)


def matches(sender: str) -> bool:
    return any(s in sender for s in SENDERS)


def parse(raw_email: dict) -> Optional[Transaction]:
    subject = raw_email.get("subject", "")
    body = " ".join((raw_email.get("plaintextBody") or "").split())

    subj_match = _MERCHANT_FROM_SUBJECT.search(subject)
    if subj_match:
        merchant = subj_match.group("merchant").strip()
        rejected = "rechazado" in subject.lower()
        amount_matches = list(_AMOUNT_ANY.finditer(body))
        if not amount_matches:
            return None
        amount_match = amount_matches[-1]
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
            counterparty=merchant,
            source="mercadopago",
            raw_subject=subject,
        )

    if "ya recibi" in body.lower() and "tu pago" in body.lower():
        amount_match = _RECEIVED_AMOUNT.search(body)
        merchant_match = _RECEIVED_MERCHANT.search(body)
        if amount_match and merchant_match:
            return Transaction(
                id=raw_email["id"],
                thread_id=raw_email.get("threadId", raw_email["id"]),
                date=raw_email["date"][:10],
                datetime=raw_email["date"],
                amount=parse_amount(amount_match.group("amount")),
                currency="COP",
                direction=DIRECTION_EXPENSE,
                kind="compra",
                status="aprobada",
                counterparty=merchant_match.group("merchant").strip(),
                source="mercadopago",
                raw_subject=subject,
            )
    return None
