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

    def months_available(self) -> list:
        cur = self.conn.execute("SELECT DISTINCT substr(date, 1, 7) AS ym FROM transactions ORDER BY ym")
        return [row["ym"] for row in cur.fetchall()]

    def close(self):
        self.conn.close()
