# Feature Review

Reviewing software that produces accounting figures, and reporting what is wrong with
it in language a developer can act on.

This is **not** an audit. `compliance-templates.md` reviews financial statements; this
reviews the software that produces them. Nothing here is assurance, an opinion, or
advice on an accounting policy.

**Cost.** A review runs several agents in parallel where the host supports them — one
per standard the feature touches, plus one verification agent per blocking finding.
Say so before starting, and give the count.

---

## 1. Refuse to start without both inputs

| Required | Why |
|---|---|
| **The implementation** — the files or directory that produce the figure | What the code intends |
| **One real generated output** — an actual balance sheet, invoice, report or posting | What it actually produced |

Code alone shows intent. A review that reads code and pronounces it correct is guessing
at the output rather than looking at it. If only one is offered, ask for the other and
do not proceed. If no output can be produced because the feature does not run, that is
itself the finding, and the only one.

Also establish the **reporting period end**. It decides which presentation rules apply
(see step 6).

---

## 2. Locate

Do not read the whole codebase. Find only the files where money is calculated, stored,
or rendered — typically far fewer than expected.

Search for: monetary field names (`amount`, `total`, `net`, `gross`, `tax`, `price`,
`balance`), decimal or money types, currency codes, anything named for a financial
statement or its line items, and the report generation path itself.

Everything after this step reads only the located files. Report how many files were
located out of how many exist; a reader needs to know what was and was not looked at.

---

## 3. Trigger map

Match what the located code contains against this table. It gives the standards to
check, and their sections in `standards-reference.md`. **The number of standards it
returns is the number of review agents to run** — never a fixed number.

| The code contains… | Check | Section |
|---|---|---|
| Invoices, receivables, an AR table | IFRS 15, IFRS 9 | *IFRS 15*, *IFRS 9 Part B* |
| A revenue, bookings or earnings figure | IFRS 15 | *IFRS 15* |
| Subscriptions, plans, deferred or unearned revenue | IFRS 15 | *IFRS 15* |
| Milestones, delivery, fulfilment, `shipped_at`, `delivered_at` | IFRS 15 | *IFRS 15* |
| Discounts, refunds, credit notes, returns, rebates | IFRS 15 | *IFRS 15* |
| Sales tax or VAT fields on amounts | IFRS 15 | *IFRS 15* |
| Payment terms longer than twelve months | IFRS 15, IFRS 9 | *IFRS 15*, *IFRS 9 Part A* |
| An allowance, provision, bad-debt or write-off field | IFRS 9 | *IFRS 9 Part B* |
| Ageing buckets, `days_overdue`, dunning logic | IFRS 9 | *IFRS 9 Part B* |
| Loans, advances, deposits, accrued interest | IFRS 9 | *IFRS 9 Parts A, B* |
| Any receivable with **no** allowance anywhere near it | IFRS 9 | *IFRS 9 Part B* |
| A balance sheet or statement-of-financial-position renderer | IAS 1 **and** IFRS 18 | *IAS 1*, *IFRS 18* |
| A P&L or income statement renderer | IAS 1 **and** IFRS 18 | *IAS 1*, *IFRS 18* |
| Hard-coded line-item names, ordering, subtotals or totals | IFRS 18 | *IFRS 18* |
| A management-defined or non-GAAP metric on a statement | IFRS 18 | *IFRS 18* |
| A currency field, `fx_rate`, exchange conversion | IAS 21 | *IAS 21* |
| Balances held in more than one currency | IAS 21 | *IAS 21* |
| A reporting currency distinct from a transaction currency | IAS 21 | *IAS 21* |
| Leases, rentals, hire agreements, right-of-use terms | IFRS 16 | *IFRS 16* |
| A cash flow statement | IAS 7 | *IAS 7* |
| A cash-equivalents or short-term-investment classification | IAS 7 | *IAS 7* |

**Covered standards are these six only.** Where the code touches anything else —
inventory, share-based payment, insurance, tax provisioning — say so explicitly in the
output as unchecked. Never review it, and never stay silent about it. Silence reads as
approval.

---

## 4. Review — one agent per standard

Run these in parallel where the host supports it, sequentially where it does not. The
findings are identical either way; only the speed differs. Say in the output which
happened.

At most **six** review agents — one per covered standard, with IAS 1 and IFRS 18 sharing
one. Never split a standard across two agents: two agents on the same standard produce the
same finding twice.

Each agent gets: the located files, one section of `standards-reference.md`, the sample
output, the period end. Each returns findings in the schema below, and returns
`Conforms` explicitly when it finds nothing — an agent that reports nothing is
indistinguishable from an agent that failed.

---

## 5. Verify — blocking findings only

Every finding marked **Blocking** goes to a fresh agent whose job is to disprove it. It
re-reads the code and asks: is this actually absent, or did the reviewer miss where it
happens? Is the figure actually wrong, or does something downstream correct it?

A blocking finding that survives is reported. One that does not is either downgraded or
dropped, with the reason. **Needs work** and **Conforms** findings are not verified —
the cost of a wrong "needs work" is a shrug, not a halted release.

This roughly doubles the token cost of a review. It buys a verdict that can stop a
release without being wrong.

---

## 6. The 2027 boundary — always checked

IFRS 18 replaces IAS 1 for periods beginning on or after **1 January 2027** and changes
what financial statements must show. Anything built today is still running then.

Any feature that renders a financial statement is checked against **both**. Where it
works now but breaks later, that is its own finding, severity **Needs work**, never
Blocking. `SKILL.md` §4 carries the full before-and-after table; read it there rather
than restating it.

Phrase it as a date, not a standard: *"This is fine under the rules in force now. They
change on 1 January 2027, and this will need X. Not urgent — cheaper now than later."*

---

## 7. Classifying a finding

Every finding carries exactly one **Class** and one **Severity**.

| Class | The defect is | Who fixes it |
|---|---|---|
| **Non-compliant** | A requirement is broken | Accounting logic |
| **Wrong** | Approach is permitted, figures or timing come out incorrect | Calculation |
| **Incomplete** | Figures right, data for a required disclosure never captured | Data model |
| **Untraceable** | Figures right and complete, no evidence trail | Logging, audit trail |

| Severity | Means |
|---|---|
| **Blocking** | A figure reaching the financial statements is wrong today, or a required figure is absent today. Verified in step 5. |
| **Needs work** | The figures are right today, and will be wrong or unsupportable under conditions that will occur |
| **Conforms** | Checked, nothing found. Stated explicitly. |

**Class and Severity are independent.** Class says what kind of defect it is and who
fixes it; Severity says whether it stops a release. A broken requirement whose figures
happen to be right today is **Non-compliant / Needs work** — the requirement is still
broken, but nothing on today's statement is wrong yet. Never read one off the other.

**The verdict is arithmetic: any Blocking finding means not ready.** It is never a
judgement call, and never a business recommendation.

---

## 8. Writing a finding

The reader is a developer or product manager. Technical, not an accountant. They do not
know what a standard is and will not look one up.

| Rule | |
|---|---|
| **No standard numbers in the body** | They mean nothing to the reader. The evidence line carries them. |
| **Define every accounting term at first use** | Every time. Do not assume a previous finding taught it. |
| **Name the file and function** | A finding without a location is not actionable. |
| **Quantify from the sample output** | "Overstates receivables by 9,600.00" beats "overstates receivables". |
| **Group, never enumerate** | The same defect in eleven places is one finding that lists eleven places. |
| **State the requirement, never the policy** | "An allowance is required and there is none" is the finding. "Use 2%" is not yours to say. |

### Shape

```
**<What is wrong, in one plain sentence.>**

<Why it matters, in the reader's language. What the rules require, what the code
does instead, and what it does to the numbers — with figures from the sample output.>

**Fix:** <what to change in the code or data model.>

**In practice — how finance teams usually handle this. Not a requirement.**
<What teams typically do. Optional. Omitted where there is nothing useful to say.>

<sub>Source: IFRS 9.5.5.15</sub>
```

The **In practice** block is the only uncited content permitted anywhere in this skill,
and its heading is fixed and never varied — see `docs/adr/0001-uncited-practice-notes.md`.
It describes convention, never obligation. If a sentence in it could be read as "you
must", it belongs above the line with a citation, or not at all.

The **evidence line** closes every finding and is the only place a standard is named. It
carries one paragraph reference per rule in force — normally one, and two for a finding that
spans the 2027 boundary, where the rule that applies now and the rule that replaces it are
both named. A reader ignores it; their accountant does not.

---

## 9. Output

````
## IFRS feature review — <feature>

**<Ready | Not ready>.** <n> blocking, <n> need work, <n> conform.

Reviewed <n> of <n> files, against <standards>. <Parallel across n agents |
Run sequentially.> Period end <date>.
Not checked: <standards outside the covered six that this feature touches>.

| # | Finding | Class | Severity |
|---|---|---|---|
| 1 | <one line> | <class> | **Blocking** |

---

### 1. <Finding title>

<the shape from §8>
````

Verdict first, table second, detail third. A product manager reads the first eight
lines and knows what to do. A developer reads the rest.

---

## 10. Never

- Recommend a rate, an estimate, a percentage, an ageing band or a policy choice.
- Give a business recommendation, or a verdict not derived arithmetically from severity.
- Review a standard outside the covered six, or stay silent about one that was touched.
- Report a blocking finding that did not survive step 5.
- Put a standard number in the body of a finding.
- Present an **In practice** note as a requirement, or a requirement as practice.
- Narrow scope silently to fit a context window. Say what was skipped, or do not skip it.
