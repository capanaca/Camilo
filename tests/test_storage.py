import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from wallettracker.storage import Storage
from wallettracker.models import Transaction, DIRECTION_EXPENSE


def _compra(id_, source, amount, date="2026-01-15", counterparty="DEMO"):
    return Transaction(
        id=id_, thread_id=id_, date=date, datetime=date, amount=amount, currency="COP",
        direction=DIRECTION_EXPENSE, kind="compra", status="aprobada",
        counterparty=counterparty, source=source,
    )


def _store():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    return Storage(path)


def test_delete_matching_gateway_purchase_removes_same_day_same_amount():
    store = _store()
    store.upsert(_compra("bold1", "bold", 960000.0, counterparty="SABAI"))
    store.upsert(_compra("mp1", "mercadopago", 226600.0, counterparty="OTRO"))
    store.commit()

    deleted = store.delete_matching_gateway_purchase(["bold", "mercadopago"], "2026-01-15", 960000.0)

    assert deleted == 1
    remaining = store.for_month("2026-01")
    assert [r["id"] for r in remaining] == ["mp1"]


def test_delete_matching_gateway_purchase_ignores_different_amount_or_date():
    store = _store()
    store.upsert(_compra("bold1", "bold", 960000.0, date="2026-01-15"))
    store.commit()

    deleted_wrong_amount = store.delete_matching_gateway_purchase(["bold"], "2026-01-15", 1.0)
    deleted_wrong_date = store.delete_matching_gateway_purchase(["bold"], "2026-01-16", 960000.0)

    assert deleted_wrong_amount == 0
    assert deleted_wrong_date == 0
    assert len(store.for_month("2026-01")) == 1


def test_delete_purchases_in_range():
    store = _store()
    store.upsert(_compra("a", "bold", 1000.0, date="2026-01-10"))
    store.upsert(_compra("b", "mercadopago", 2000.0, date="2026-01-20"))
    store.upsert(_compra("c", "bold", 3000.0, date="2026-02-01"))
    store.commit()

    deleted = store.delete_purchases_in_range(["bold", "mercadopago"], "2026-01-01", "2026-01-31")

    assert deleted == 2
    remaining = store.for_month("2026-02")
    assert [r["id"] for r in remaining] == ["c"]
