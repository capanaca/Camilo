#!/usr/bin/env python3
"""Ingests a Bancolombia credit card statement PDF (password-protected)
into the local transactions ledger.

The statement itemizes every purchase in its billing period, so it
supersedes narrower per-gateway notification emails (Mercado Pago, Bold,
and Bancolombia's own foreign-currency purchase alerts) for that same date
range — those are deleted before the statement lines are inserted, to avoid
double-counting a purchase that both a gateway email and the statement
reported.

Usage:
    python scripts/ingest_statement_pdf.py extracto.pdf CEDULA_O_NIT 4491 \
        [--db data/transactions.db]
"""
import argparse
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from wallettracker.categorize import categorize
from wallettracker.storage import Storage
from wallettracker.parsers.bancolombia_statement import parse_statement_pages, date_range

_SUPERSEDED_SOURCES = ["mercadopago", "bold", "bancolombia"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_path")
    parser.add_argument("password", help="Cédula/NIT used to decrypt the statement")
    parser.add_argument("card_last4")
    parser.add_argument("--db", default="data/transactions.db")
    args = parser.parse_args()

    import pikepdf
    import pdfplumber

    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        with pikepdf.open(args.pdf_path, password=args.password) as pdf:
            pdf.save(tmp.name)

        with pdfplumber.open(tmp.name) as decrypted:
            pages_text = [page.extract_text() or "" for page in decrypted.pages]

    transactions = parse_statement_pages(pages_text, args.card_last4)
    if not transactions:
        print("No se encontraron movimientos en el extracto.")
        return

    os.makedirs(os.path.dirname(args.db), exist_ok=True)
    store = Storage(args.db)

    span = date_range(transactions)
    deleted = store.delete_purchases_in_range(_SUPERSEDED_SOURCES, span[0], span[1])

    new_count = 0
    for txn in transactions:
        txn.category = categorize(txn)
        if store.upsert(txn):
            new_count += 1
    store.commit()
    store.close()

    print(f"Extracto {span[0]} a {span[1]}: {len(transactions)} movimientos, "
          f"{new_count} nuevos. {deleted} transacciones de correos de pasarela "
          f"(Mercado Pago/Bold/Bancolombia) reemplazadas por el detalle del extracto.")


if __name__ == "__main__":
    main()
