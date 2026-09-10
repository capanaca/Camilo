#!/usr/bin/env python3
"""Generates the Markdown report for one month and updates the running
month-over-month summary (data/monthly_summary.json).

Usage:
    python scripts/make_report.py 2026-09 [--db data/transactions.db] [--out reports/]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from wallettracker.storage import Storage
from wallettracker.report import (
    compute_summary,
    render_markdown,
    load_history,
    save_history,
    previous_month_key,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("year_month", help="YYYY-MM")
    parser.add_argument("--db", default="data/transactions.db")
    parser.add_argument("--out", default="reports")
    parser.add_argument("--history", default="data/monthly_summary.json")
    args = parser.parse_args()

    store = Storage(args.db)
    rows = store.for_month(args.year_month)
    store.close()

    if not rows:
        print(f"No hay transacciones para {args.year_month}.")
        return

    summary = compute_summary(rows)
    history = load_history(args.history)
    previous = history.get(previous_month_key(args.year_month))

    markdown = render_markdown(args.year_month, rows, summary, previous)

    os.makedirs(args.out, exist_ok=True)
    out_path = os.path.join(args.out, f"{args.year_month}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    history[args.year_month] = summary
    save_history(args.history, history)

    print(f"Reporte generado: {out_path}")
    print(f"Resumen actualizado: {args.history}")


if __name__ == "__main__":
    main()
