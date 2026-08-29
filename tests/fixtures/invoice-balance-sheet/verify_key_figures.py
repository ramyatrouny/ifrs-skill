#!/usr/bin/env python3
"""Assert every figure quoted in tests/expected/invoice-balance-sheet.md.

CONTRIBUTING requires a runnable assertion behind any numerical claim of substance.
The answer key makes several, and a key with a wrong number in it would fail a correct
review. This recomputes each from reports.py rather than restating it.

Usage:  python3 tests/fixtures/invoice-balance-sheet/verify_key_figures.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reports import INVOICES, PERIOD_END, balance_sheet  # noqa: E402

bs = balance_sheet()
assets = dict(bs["assets"])
delivered = [i for i in INVOICES if i.delivered and i.delivered <= PERIOD_END]
inv3 = next(i for i in INVOICES if i.id == "INV-003")
inv4 = next(i for i in INVOICES if i.id == "INV-004")

reported_revenue = bs["total_equity_and_liabilities"]
correct_revenue = sum(i.net for i in delivered)
reported_ar = assets["Trade receivables"]
correct_ar = sum(i.net + i.tax for i in delivered if not i.paid)
tax_total = sum(i.tax for i in INVOICES)
overstatement = reported_revenue / correct_revenue - 1

# "Correct revenue for the period is 18,000.00 against 31,200.00 reported"
assert reported_revenue == 31200.00, reported_revenue
assert correct_revenue == 18000.00, correct_revenue
# "a 73% overstatement"
assert round(overstatement * 100) == 73, overstatement
# "Receivables are 19,200.00 against a correct gross figure of 9,600.00"
assert reported_ar == 19200.00, reported_ar
assert correct_ar == 9600.00, correct_ar
# "Its 9,600.00 is in both revenue and receivables" — INV-003, never delivered
assert inv3.delivered is None
assert inv3.net + inv3.tax == 9600.00
# "5,200.00 of tax is inside the reported 31,200.00 of retained earnings"
assert tax_total == 5200.00, tax_total
# "INV-004 is 117 days past delivery and unpaid at the period end"
assert (PERIOD_END - inv4.delivered).days == 117
assert inv4.paid is False
# The statement balances, which is why the two errors are not otherwise visible
assert bs["total_assets"] == bs["total_equity_and_liabilities"] == 31200.00
# The planted defects are still planted
assert assets["Cash"] == 12000.00, "cash is receipts, not a cash balance"
assert len(bs["assets"]) == 2 and len(bs["equity_and_liabilities"]) == 1, \
    "no current/non-current split, no tax liability"

print(f"reported revenue {reported_revenue:>10,.2f}   correct {correct_revenue:>10,.2f}"
      f"   overstated {overstatement * 100:.0f}%")
print(f"reported AR      {reported_ar:>10,.2f}   correct {correct_ar:>10,.2f}"
      f"   (gross, before allowance)")
print(f"tax in earnings  {tax_total:>10,.2f}   INV-004 overdue 117 days"
      f"   INV-003 undelivered")
print("all answer-key figures verified")
