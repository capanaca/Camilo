"""SQLite-backed ledger. Transactions are deduplicated by their Gmail message id."""
import sqlite3
from typing import Iterable, Optional

from .models import Transaction

_SCHEMA = """
CREATE TABLE IF NOT EXISTS transactions (
    id TEXT PRIMARY KEY,
    thread_id TEXT,
    date TEXT NOT NULL,
    datetime TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,
    direction TEXT NOT NULL,
    kind TEXT NOT NULL,
    status TEXT NOT NULL,
    counterparty TEXT,
    source TEXT NOT NULL,
    account_ref TEXT,
    category TEXT,
    raw_subject TEXT
);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
"""


class Storage:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(_SCHEMA)

    def upsert(self, txn: Transaction) -> bool:
        """Returns True if this was a new transaction (not seen before)."""
        cur = self.conn.execute("SELECT 1 FROM transactions WHERE id = ?", (txn.id,))
        is_new = cur.fetchone() is None
        self.conn.execute(
            """
            INSERT INTO transactions
                (id, thread_id, date, datetime, amount, currency, direction, kind,
                 status, counterparty, source, account_ref, category, raw_subject)
            VALUES (:id, :thread_id, :date, :datetime, :amount, :currency, :direction, :kind,
                    :status, :counterparty, :source, :account_ref, :category, :raw_subject)
            ON CONFLICT(id) DO UPDATE SET
                amount=excluded.amount, category=excluded.category, status=excluded.status
            """,
            txn.to_dict(),
        )
        return is_new

    def commit(self):
        self.conn.commit()

    def for_month(self, year_month: str) -> list:
        """year_month: 'YYYY-MM'."""
        cur = self.conn.execute(
            "SELECT * FROM transactions WHERE date LIKE ? ORDER BY date, datetime",
            (f"{year_month}-%",),
        )
        return [dict(row) for row in cur.fetchall()]

    def delete_matching_gateway_purchase(self, sources: list, date: str, amount: float) -> int:
        """Removes 'compra' rows from `sources` on `date` matching `amount`.

        Bancolombia notifies every card purchase regardless of which gateway
        routed it, while Mercado Pago/Bold only notify their own subset — so
        when a Bancolombia purchase email arrives, any gateway-email row for
        the same day and amount is almost certainly the same purchase under
        a different merchant descriptor (e.g. "SABAI" vs "BOLD SA*SABAI").
        """
        placeholders = ",".join("?" for _ in sources)
        cur = self.conn.execute(
            f"DELETE FROM transactions WHERE source IN ({placeholders}) "
            f"AND kind = 'compra' AND date = ? AND amount = ?",
            (*sources, date, amount),
        )
        return cur.rowcount

    def delete_purchases_in_range(self, sources: list, date_from: str, date_to: str) -> int:
        """Removes 'compra' rows from `sources` within [date_from, date_to].

        Used when a more authoritative source (e.g. the credit card
        statement PDF, which itemizes every purchase) supersedes narrower
        per-gateway notification emails (Mercado Pago, Bold) for the same
        billing period, to avoid counting the same purchase twice.
        """
        placeholders = ",".join("?" for _ in sources)
        cur = self.conn.execute(
            f"DELETE FROM transactions WHERE source IN ({placeholders}) "
            f"AND kind = 'compra' AND date BETWEEN ? AND ?",
            (*sources, date_from, date_to),
        )
        return cur.rowcount

    def months_available(self) -> list:
        cur = self.conn.execute("SELECT DISTINCT substr(date, 1, 7) AS ym FROM transactions ORDER BY ym")
        return [row["ym"] for row in cur.fetchall()]

    def close(self):
        self.conn.close()
