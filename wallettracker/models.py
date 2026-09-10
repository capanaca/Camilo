from dataclasses import dataclass, field, asdict
from typing import Optional

# direction groups how a transaction counts toward the monthly totals.
DIRECTION_EXPENSE = "expense"
DIRECTION_INCOME = "income"
DIRECTION_INTERNAL = "internal_transfer"   # e.g. paying your own credit card
DIRECTION_EXCLUDED = "excluded"            # rejected/failed transactions


@dataclass
class Transaction:
    id: str                      # Gmail message id, used as dedupe key
    thread_id: str
    date: str                    # ISO date "YYYY-MM-DD"
    datetime: str                # ISO datetime if available, else same as date
    amount: float
    currency: str
    direction: str
    kind: str                    # compra | retiro | nomina | transferencia_recibida | ...
    status: str                  # aprobada | rechazada
    counterparty: str            # merchant or person name
    source: str                  # bancolombia | mercadopago | bold | santander
    account_ref: str = ""
    category: str = ""
    raw_subject: str = ""

    def to_dict(self) -> dict:
        return asdict(self)
