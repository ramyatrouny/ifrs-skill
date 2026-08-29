# Expected findings — `invoice-balance-sheet`

Answer key for `tests/fixtures/invoice-balance-sheet/`. Kept outside the fixture
directory so a review agent pointed at the fixture cannot read it.

This is a key, not review output: it names standards in prose so a human can check a review
against it quickly. Sections 8 and 10 of `ifrs/feature-review.md` — which confine standard
numbers to the evidence line — bind review output, not this file. Do not copy its shape.

**The review passes when all four required findings appear, each with the stated
Class and Severity.** Extra findings from the list at the bottom are fine. A missed
required finding is a failure; so is a required finding at the wrong Severity, because
Severity is what drives the Verdict.

## Required

### 1. Trade receivables carry no loss allowance

`trade_receivables()` returns the full unpaid amount. Nothing anywhere in the module
estimates or subtracts credit losses.

- **Class** Non-compliant · **Severity** Blocking
- **Evidence** IFRS 9.5.5.15 — a lifetime expected-credit-loss allowance is required on
  trade receivables at all times, not from the point a receivable looks doubtful.
- INV-004 is 117 days past delivery and unpaid at the period end; it carries no
  allowance either.

### 2. Sales tax is counted as revenue and as an asset

`gross()` adds `tax` to `net`, and every figure in the balance sheet is built from it.
Tax collected on behalf of the tax authority is treated as the entity's own income.

- **Class** Non-compliant · **Severity** Blocking
- **Evidence** IFRS 15.47 — the transaction price excludes amounts collected on behalf
  of third parties, sales taxes given as the example.
- 5,200.00 of tax is inside the reported 31,200.00 of retained earnings, and no
  corresponding liability to the tax authority appears anywhere on the statement.

### 3. Revenue is recognised on the invoice date, not on delivery

`revenue_for_period()` filters on `issued` and never reads `delivered`, which is
carried on every invoice and is `None` for INV-003.

- **Class** Non-compliant · **Severity** Blocking
- **Evidence** IFRS 15.31 — revenue is recognised when a performance obligation is
  satisfied by transferring control, not when a document is sent.
- INV-003 was issued 22 December 2026 and never delivered. Its 9,600.00 is in both
  revenue and receivables.
- Correct revenue for the period is **18,000.00** (delivered, net of tax) against
  **31,200.00** reported — a 73% overstatement. Receivables are 19,200.00 against a
  correct gross figure of 9,600.00 before any allowance.

### 4. The balance sheet has no current / non-current split

`balance_sheet()` returns two flat lists. Nothing classifies any item by when it will
be realised or settled.

- **Class** Incomplete · **Severity** Needs work
- **Evidence** IAS 1.60 for periods before 1 January 2027; IFRS 18.96 from that date.

## Acceptable extras

Correct if reported, not required to pass. The first four were produced by the first
reviewer to sit this fixture and were verified against the standards' own text:

- **The `Cash` line is not cash.** `cash_collected()` sums paid invoices, so the figure
  omits the opening balance and every outflow. IAS 1.54 requires the cash balance.
- **No comparative period.** One column only; IAS 1.38 requires the preceding period for
  every amount. Fixing it is a data-model change, because a boolean `paid` cannot say
  whether an invoice was outstanding a year ago.
- **No entity name, presentation currency or rounding** in the rendered header — IAS 1.51.
- **No line identifiers for note cross-referencing** — IFRS 18.114 from 1 January 2027,
  which additionally requires the reverse link that IAS 1.113 does not.

Also correct:

- Minimum line items absent from the statement — IAS 1.54, or IFRS 18.104 from 2027.
- The 2027 boundary as its own finding — the presentation rules change on 1 January
  2027 and this renderer will need rework. Severity must be **Needs work**, never
  Blocking.
- Undelivered invoices should not produce a receivable at all — IFRS 15.105 draws the
  line between a contract asset and a receivable.
- `PERIOD_END` is hard-coded, so the report cannot be run for any other period.

## Must not appear

- Any recommendation of a specific provision rate, ageing band or accounting policy.
  Stating that an allowance is required is the finding; choosing its size is not the
  reviewer's call.
- Any finding on IAS 2, IFRS 2, IFRS 17 or any standard outside the covered six.
  Anything outside them is named as unchecked, never reviewed.
