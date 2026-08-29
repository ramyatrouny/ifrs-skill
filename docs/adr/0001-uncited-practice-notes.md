---
status: accepted
---

# Practice notes may be uncited

Every other claim in this skill resolves to a paragraph of a standard, and
`scripts/check_citations.py` proves it. Feature reviews additionally need to say what
finance teams *typically do* about a finding — an ageing-based provision matrix, a
quarterly true-up — because that is what makes a finding actionable for a developer
who is not an accountant. No standard says any of it, so none of it is citable.

We allow these **Practice notes** in `ifrs/feature-review.md` only, under a fixed and
visually unmistakable heading marking them as practice rather than requirement.

## Considered options

- **Omit them.** Keeps the citation model absolute, and leaves every finding ending at
  "the rules require an allowance" with no indication of how anyone actually builds one.
- **Cite practice to secondary sources** (Big Four guides, IFRIC agenda decisions).
  Honest, but such sources describe perhaps a third of the cases that arise, so most
  findings would still end where option one leaves them.
- **Allow them, labelled.** Chosen.

## Consequences

The claim "every statement in this skill is cited" acquires a permanent exception, and
that is hard to walk back once practice notes exist and are relied on. The label is
therefore not stylistic: if it ever blurs, a reader cannot tell a requirement from a
convention, which is the one confusion this repository exists to prevent. The README's
description of the verification model must state the exception rather than imply
citation is universal.
