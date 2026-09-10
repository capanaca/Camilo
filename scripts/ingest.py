#!/usr/bin/env python3
"""Ingests a JSON export of raw Gmail messages into the local transactions ledger.

Input file format: a JSON list of objects shaped like:
    {"id": "...", "threadId": "...", "date": "2026-09-08T16:15:47Z",
     "sender": "no-responder@bold.co", "subject": "...", "plaintextBody": "..."}

These fields map directly onto what the Gmail get_message/get_thread tools
return, so raw email data fetched there can be dumped to a file and passed
straight to this script.

Usage:
    python scripts/ingest.py path/to/emails.json [--db data/transactions.db]
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from wallettracker.parsers import parse_email
from wallettracker.categorize import categorize
from wallettracker.storage import Storage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("emails_json")
    parser.add_argument("--db", default="data/transactions.db")
    args = parser.parse_args()

    with open(args.emails_json, encoding="utf-8") as f:
        emails = json.load(f)

    os.makedirs(os.path.dirname(args.db), exist_ok=True)
    store = Storage(args.db)

    new_count = 0
    unmatched = 0
    for raw_email in emails:
        txn = parse_email(raw_email)
        if txn is None:
            unmatched += 1
            continue
        txn.category = categorize(txn)
        if store.upsert(txn):
            new_count += 1
    store.commit()
    store.close()

    print(f"Procesados {len(emails)} correos: {new_count} transacciones nuevas, "
          f"{unmatched} sin reconocer (marketing/otros).")


if __name__ == "__main__":
    main()
