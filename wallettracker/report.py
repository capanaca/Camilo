"""Builds the monthly Markdown report and maintains the month-over-month summary file."""
import json
import os
from collections import defaultdict

from .models import DIRECTION_EXPENSE, DIRECTION_INCOME, DIRECTION_INTERNAL, DIRECTION_EXCLUDED


def _fmt(amount: float, currency: str = "COP") -> str:
    return f"${amount:,.0f} {currency}"


_PRIMARY_CURRENCY = "COP"


def compute_summary(rows: list) -> dict:
    primary = [r for r in rows if r["currency"] == _PRIMARY_CURRENCY]
    other_currency = [r for r in rows if r["currency"] != _PRIMARY_CURRENCY]

    total_income = sum(r["amount"] for r in primary if r["direction"] == DIRECTION_INCOME)
    total_expense = sum(r["amount"] for r in primary if r["direction"] == DIRECTION_EXPENSE)
    by_category = defaultdict(float)
    by_source = defaultdict(float)
    for r in primary:
        if r["direction"] == DIRECTION_EXPENSE:
            by_category[r["category"]] += r["amount"]
            by_source[r["source"]] += r["amount"]

    other_currency_totals = defaultdict(float)
    for r in other_currency:
        if r["direction"] == DIRECTION_EXPENSE:
            other_currency_totals[r["currency"]] += r["amount"]

    internal = [r for r in rows if r["direction"] == DIRECTION_INTERNAL]
    rejected = [r for r in rows if r["direction"] == DIRECTION_EXCLUDED]

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net": total_income - total_expense,
        "by_category": dict(sorted(by_category.items(), key=lambda kv: -kv[1])),
        "by_source": dict(sorted(by_source.items(), key=lambda kv: -kv[1])),
        "other_currency_totals": dict(other_currency_totals),
        "internal_transfers_total": sum(r["amount"] for r in internal),
        "rejected_count": len(rejected),
        "transaction_count": len(rows),
    }


def render_markdown(year_month: str, rows: list, summary: dict, previous: dict | None) -> str:
    lines = [f"# Reporte de gastos — {year_month}", ""]
    lines.append(f"- **Ingresos:** {_fmt(summary['total_income'])}")
    lines.append(f"- **Gastos:** {_fmt(summary['total_expense'])}")
    lines.append(f"- **Neto (ingresos - gastos):** {_fmt(summary['net'])}")
    lines.append(f"- **Transacciones procesadas:** {summary['transaction_count']}"
                 f" ({summary['rejected_count']} rechazadas, no contabilizadas)")
    if summary["internal_transfers_total"]:
        lines.append(f"- **Pagos a tarjeta de crédito (movimiento interno, no es gasto nuevo):** "
                     f"{_fmt(summary['internal_transfers_total'])}")
    for currency, amount in summary.get("other_currency_totals", {}).items():
        lines.append(f"- **Gastos adicionales en {currency} (no incluidos en el total {'COP'}):** "
                     f"{_fmt(amount, currency)}")
    lines.append("")

    if previous:
        delta = summary["total_expense"] - previous["total_expense"]
        arrow = "más" if delta > 0 else "menos"
        lines.append(f"## Comparación con el mes anterior")
        if previous["total_expense"]:
            pct = delta / previous["total_expense"] * 100
            lines.append(f"Gastaste {_fmt(abs(delta))} {arrow} que el mes pasado ({pct:+.1f}%).")
        elif delta == 0:
            lines.append("Sin gastos registrados este mes ni el anterior.")
        else:
            lines.append(f"Gastaste {_fmt(abs(delta))} {arrow} que el mes pasado (el mes anterior no tuvo gastos registrados).")
        lines.append("")

    lines.append("## Gastos por categoría")
    lines.append("| Categoría | Monto | % del gasto |")
    lines.append("|---|---|---|")
    for category, amount in summary["by_category"].items():
        pct = (amount / summary["total_expense"] * 100) if summary["total_expense"] else 0
        lines.append(f"| {category} | {_fmt(amount)} | {pct:.1f}% |")
    lines.append("")

    lines.append("## Gastos por fuente")
    lines.append("| Fuente | Monto |")
    lines.append("|---|---|")
    for source, amount in summary["by_source"].items():
        lines.append(f"| {source} | {_fmt(amount)} |")
    lines.append("")

    top_expenses = sorted(
        (r for r in rows if r["direction"] == DIRECTION_EXPENSE), key=lambda r: -r["amount"]
    )[:10]
    if top_expenses:
        lines.append("## Top 10 gastos individuales")
        lines.append("| Fecha | Comercio/concepto | Monto | Categoría |")
        lines.append("|---|---|---|---|")
        for r in top_expenses:
            lines.append(f"| {r['date']} | {r['counterparty']} | {_fmt(r['amount'])} | {r['category']} |")
        lines.append("")

    return "\n".join(lines)


def load_history(path: str) -> dict:
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_history(path: str, history: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False, sort_keys=True)


def previous_month_key(year_month: str) -> str:
    year, month = (int(p) for p in year_month.split("-"))
    if month == 1:
        return f"{year - 1}-12"
    return f"{year}-{month - 1:02d}"
