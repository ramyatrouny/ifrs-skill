# IFRS Skill

A cited IFRS and IAS reference that plugs into an AI assistant, plus the review
activity that applies it to software that produces accounting figures.

## Language

### The thing under review

**Feature**:
A code path in a shipped product that produces an accounting output — a report, a
posted entry, or a figure that reaches a financial statement.
_Avoid_: module, capability, product feature

**Feature review**:
Reading a Feature's implementation and a sample of its real output, and reporting
where it departs from what IFRS requires.
_Avoid_: audit, compliance check, product review, conformance review

**Audit**:
External assurance under ISA, producing an opinion. Reserved — it is the established
meaning throughout `compliance-templates.md` and `SKILL.md` routes on it. Never used
for a Feature review.

**Reader**:
The audience for a Feature review: a developer, engineer or product manager. Technical,
and not an accountant. No output may assume they know what a standard requires.
_Avoid_: user, stakeholder, financial user

### How a review is scoped

**Trigger map**:
The table connecting a code artefact to the standards a Feature review must check
against it — a receivables table to IFRS 15 and IFRS 9, a balance-sheet renderer to
IAS 1 and IFRS 18, and so on. It is the only content the review adds; everything it
points at already exists in the skill.

**Covered standard**:
One of the six a Feature review checks — IFRS 15, IFRS 9, IAS 1/IFRS 18, IAS 21,
IFRS 16, IAS 7. Anything a Feature touches outside these is named as unchecked in the
review's output. Silence is never scope.

The set is stated in four places and has no single source of truth: here, the Trigger map
and section 10 of `ifrs/feature-review.md`, `COVERED` in `scripts/check_feature_review.py`,
and the _Must not appear_ list of each fixture's answer key. Adding a seventh means editing
all four; nothing fails if one is missed.

### What a review produces

**Finding**:
One departure from what IFRS requires, in one Feature. Carries exactly one Class and
one Severity.

**Class**:
Which kind of departure a Finding is, and therefore who fixes it — **Non-compliant**
(breaks a requirement), **Wrong** (permitted approach, incorrect figures or timing),
**Incomplete** (figures right, data for a required disclosure never captured), or
**Untraceable** (figures right, no evidence trail).

**Severity**:
How urgent a Finding is — **Blocking** (a figure reaching the financial statements is
wrong or absent today), **Needs work** (the figures are right today and will be wrong or
unsupportable under conditions that will occur), or **Conforms** (checked, nothing found;
stated so silence is never read as approval). Independent of Class: a broken requirement
whose figures are right today is Non-compliant and Needs work, not Blocking.

**Verdict**:
The readiness of a Feature, derived arithmetically from Severity: any Blocking Finding
means not ready. Never a judgement, never a business recommendation.

**Evidence line**:
The single citation closing a Finding, carrying the paragraph that supports it. The
body of a Finding is plain English; the Evidence line is where the standard is named.

**Practice note**:
A block describing what finance teams typically do about a Finding, as distinct from
what IFRS requires. Uncited by nature, and the only uncited content permitted in the
skill — see `docs/adr/0001-uncited-practice-notes.md`.
_Avoid_: best practice, recommendation, guidance

### Timing

**The 2027 boundary**:
1 January 2027, when IFRS 18 replaces IAS 1 and changes what a set of financial
statements must show. Every Feature that renders a financial statement is checked
against both sides of it; a Feature that presents nothing has no presentation to check.
