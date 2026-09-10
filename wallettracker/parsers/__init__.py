"""Parser registry: dispatches a raw email to the parser matching its sender."""
from typing import Optional
from ..models import Transaction
from . import bancolombia, mercadopago, bold, santander

_PARSERS = [bancolombia, mercadopago, bold, santander]


def parse_email(raw_email: dict) -> Optional[Transaction]:
    """raw_email: {id, threadId, date, sender, subject, plaintextBody}."""
    sender = (raw_email.get("sender") or "").lower()
    for module in _PARSERS:
        if module.matches(sender):
            return module.parse(raw_email)
    return None
