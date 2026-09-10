"""Rule-based categorization: transaction kind wins for non-purchase movements,
merchant-keyword lookup decides the category for purchases."""
import json
import os
from .models import Transaction

_KIND_CATEGORY = {
    "retiro": "Retiros de efectivo",
    "retiro_fiducuenta": "Retiros de efectivo",
    "nomina": "Ingresos - Nómina",
    "transferencia_recibida": "Ingresos - Transferencias",
    "transferencia_enviada": "Transferencias enviadas",
    "pago_qr": "Pagos QR",
    "pago_tarjeta_credito": "Pagos tarjeta de crédito (interno)",
    "compra_rechazada": "Rechazadas (no contabilizadas)",
    "cuota_manejo": "Servicios bancarios",
}

_CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "config")
_DEFAULT_PATH = os.path.join(_CONFIG_DIR, "categories.json")
_LOCAL_PATH = os.path.join(_CONFIG_DIR, "categories.local.json")


def _load_rules() -> dict:
    rules = {}
    for path in (_DEFAULT_PATH, _LOCAL_PATH):
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            for category, keywords in data.items():
                if category.startswith("_"):
                    continue
                rules.setdefault(category, []).extend(k.lower() for k in keywords)
    return rules


_RULES = _load_rules()


def categorize(txn: Transaction) -> str:
    if txn.kind in _KIND_CATEGORY:
        return _KIND_CATEGORY[txn.kind]

    merchant = (txn.counterparty or "").lower()
    for category, keywords in _RULES.items():
        if any(kw in merchant for kw in keywords):
            return category
    return "Otros gastos"
