"""Balance sheet generation from uploaded customer invoices.

Users upload a CSV of invoices; this module turns them into a balance sheet
for the reporting period.
"""

from datetime import date
from typing import NamedTuple, Optional

PERIOD_END = date(2026, 12, 31)


class Invoice(NamedTuple):
    id: str
    issued: date
    delivered: Optional[date]
    net: float
    tax: float
    paid: bool


# In production these come from the invoices table. Inlined here so the module
# runs standalone.
INVOICES = [
    Invoice("INV-001", date(2026, 3, 12), date(2026, 3, 20), 10000.0, 2000.0, True),
    Invoice("INV-002", date(2026, 8, 4), date(2026, 8, 11), 5000.0, 1000.0, False),
    Invoice("INV-003", date(2026, 12, 22), None, 8000.0, 1600.0, False),
    Invoice("INV-004", date(2026, 9, 1), date(2026, 9, 5), 3000.0, 600.0, False),
]


def gross(invoice):
    """Total amount on the invoice, including sales tax."""
    return invoice.net + invoice.tax


def revenue_for_period(invoices, period_end=PERIOD_END):
    """Revenue earned in the period.

    An invoice counts once it has been issued to the customer.
    """
    return sum(gross(i) for i in invoices if i.issued <= period_end)


def trade_receivables(invoices, period_end=PERIOD_END):
    """What customers still owe us at the period end."""
    return sum(gross(i) for i in invoices if not i.paid and i.issued <= period_end)


def cash_collected(invoices, period_end=PERIOD_END):
    """Cash received from customers who have paid."""
    return sum(gross(i) for i in invoices if i.paid and i.issued <= period_end)


def balance_sheet(invoices=None, period_end=PERIOD_END):
    invoices = invoices if invoices is not None else INVOICES

    cash = cash_collected(invoices, period_end)
    receivables = trade_receivables(invoices, period_end)
    earnings = revenue_for_period(invoices, period_end)

    return {
        "period_end": period_end,
        "assets": [
            ("Cash", cash),
            ("Trade receivables", receivables),
        ],
        "total_assets": cash + receivables,
        "equity_and_liabilities": [
            ("Retained earnings", earnings),
        ],
        "total_equity_and_liabilities": earnings,
    }


def render(bs):
    out = [f"BALANCE SHEET as at {bs['period_end'].isoformat()}", ""]
    out.append("ASSETS")
    for name, amount in bs["assets"]:
        out.append(f"  {name:<28}{amount:>12,.2f}")
    out.append(f"  {'Total assets':<28}{bs['total_assets']:>12,.2f}")
    out.append("")
    out.append("EQUITY AND LIABILITIES")
    for name, amount in bs["equity_and_liabilities"]:
        out.append(f"  {name:<28}{amount:>12,.2f}")
    out.append(
        f"  {'Total equity and liabilities':<28}"
        f"{bs['total_equity_and_liabilities']:>12,.2f}"
    )
    return "\n".join(out)


if __name__ == "__main__":
    print(render(balance_sheet()))
