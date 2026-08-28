# IFRS Skill

**IFRS and IAS reference for AI coding agents.** Paragraph-cited guidance on every standard in
force, written for controllers, financial reporting teams and auditors — and for the developers
who install agent skills on their behalf.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/ramyatrouny/ifrs-skill)](https://github.com/ramyatrouny/ifrs-skill/releases)
[![Stars](https://img.shields.io/github/stars/ramyatrouny/ifrs-skill?style=flat)](https://github.com/ramyatrouny/ifrs-skill/stargazers)
[![Content currency](https://img.shields.io/badge/content%20current-28%20August%202026-informational)](docs/SOURCING.md)

```bash
npx skills add ramyatrouny/ifrs-skill
```

Works with Claude Code, Codex CLI, Gemini CLI and Cursor. Installation for each is [below](#installation).

> This skill provides technical guidance. It does not replace professional judgment, and it is not
> a substitute for advice from a qualified accountant or auditor. See [Scope and limitations](#scope-and-limitations).

---

## Contents

- [Why this exists](#why-this-exists)
- [Quickstart](#quickstart)
- [Coverage](#coverage)
- [IFRS 18 — Presentation and Disclosure, mandatory 2027](#ifrs-18--presentation-and-disclosure-mandatory-2027)
- [Installation](#installation)
- [Example queries](#example-queries)
- [How it works](#how-it-works)
- [How the content was verified](#how-the-content-was-verified)
- [Scope and limitations](#scope-and-limitations)
- [Contributing](#contributing)
- [Licence and citation](#licence-and-citation)

---

## Why this exists

General-purpose models answer IFRS questions fluently and are wrong often enough to matter. The
failure mode is not obvious errors — it is confident, plausible, correctly formatted output that a
reviewer would have to check line by line.

Two defects found and corrected in this repository's own content during its August 2026 audit
illustrate the class of error involved. Both are in the git history and can be checked.

**A journal entry that did not balance.** The business combination worked example recorded:

```
Dr  Identifiable Assets      6,000,000
    Cr  Liabilities                     1,800,000
    Cr  Cash                            5,000,000
```

Debits 6,000,000 against credits 6,800,000. The example then reconciled the 800,000 difference by
crediting goodwill to retained earnings — posting a fictitious credit to equity. Goodwill is the
residual debit that makes the entry balance (IFRS 3.32); it is never recognised against equity.

**Relief offered that does not exist.** The transition guide listed the IFRS 1 exemption at
paragraphs D10–D11, permitting cumulative actuarial gains and losses to be reset to zero on
transition. Those paragraphs were deleted by IAS 19 as amended in June 2011, a deletion recorded at
IFRS 1.39L. A company relying on it would budget for a small pension adjustment and meet a large
unrelieved one late in its transition.

Both are now corrected, and the second is stated as an explicit warning rather than silently
removed, so the assumption is not made again from memory.

The point is not that this repository was wrong. It is that IFRS content is easy to get wrong in
ways that read as correct, which is why everything here carries a paragraph reference that has been
checked against the standard's own text.

## Quickstart

**1. Install** — one command, all supported agents:

```bash
npx skills add ramyatrouny/ifrs-skill
```

**2. Verify it loaded.** Paste this into your agent:

> For a 31 December 2027 year-end, which standard and paragraph carries the going concern
> disclosure requirement? Answer with the reference only.

| Answer | Meaning |
|---|---|
| `IAS 8.6K–6L` | Skill loaded and current |
| `IAS 1.25–26` | Skill not loaded — the model is answering from its own knowledge |
| `Unknown command` | Skill not found; see [Troubleshooting](#troubleshooting) |

The distinction matters: IFRS 18 supersedes IAS 1 for periods beginning on or after 1 January 2027
and moves the going concern requirement into IAS 8. Most sources still give the IAS 1 answer.

**3. Ask something real:**

> Our lessee discount rate for a 7-year warehouse lease uses our 5-year unsecured borrowing rate.
> Is that defensible under IFRS 16, and what would an auditor challenge?

## Coverage

| | Count | What it covers |
|---|---|---|
| Standards | **43** | 19 IFRS (1–20) and 24 IAS, every standard in force |
| Interpretations | **20** | Live IFRIC and SIC interpretations, plus IFRS IC agenda decisions to April 2026 |
| Workflows | **17** | Multi-step procedures with worked figures and complete journal entries |
| Templates | **12** | Disclosure checklists, materiality, going concern, interim, audit response |
| Checklist rows | **1,590** | Each carrying its paragraph reference |
| Paragraph citations | **4,240** | Verified against the standards' own text |

Sustainability standards IFRS S1 and IFRS S2 are covered, as is the Conceptual Framework, the
IFRS for SMEs Accounting Standard, and a jurisdictional adoption map including EU and UK
endorsement status.

Content is current as at **28 August 2026**.

## IFRS 18 — Presentation and Disclosure, mandatory 2027

IFRS 18 supersedes IAS 1 for annual periods beginning on or after 1 January 2027, with earlier
application permitted. It is the largest change to the face of the financial statements in two
decades, and it moves several requirements out of IAS 1 into IAS 8, which it retitles
*Basis of Preparation of Financial Statements*.

| Requirement | Periods before 1 Jan 2027 | Periods from 1 Jan 2027 |
|---|---|---|
| Going concern | IAS 1.25–26 | **IAS 8.6K–6L** |
| Critical judgements | IAS 1.122 | **IAS 8.27G** |
| Estimation uncertainty | IAS 1.125–133 | **IAS 8.31A–31I** |
| Material accounting policy information | IAS 1.117 | **IAS 8.27A** |

Every affected disclosure checklist row in this skill carries both references, labelled by the
period each applies to. Also covered: the five categories of the statement of profit or loss, the
two required subtotals, specified main business activities, and management-defined performance
measures (MPMs) with the reconciliation IFRS 18.B137(a) requires.

**IFRS 19** *Subsidiaries without Public Accountability* is covered and is **elective, not
mandatory** — IFRS 19.A1 says an eligible subsidiary *may elect* to apply it from 1 January 2027.
That is the date the election becomes available, not a deadline.

## Installation

Every command below has been tested. Prefer the first.

### One command, all agents

```bash
npx skills add ramyatrouny/ifrs-skill
```

Installs to `~/.agents/skills/ifrs/` and links into each agent's skills directory.

### Per agent

| Agent | Command |
|---|---|
| **Claude Code** | `mkdir -p ~/.claude/skills/ifrs && cp ifrs/*.md ~/.claude/skills/ifrs/` |
| **Codex CLI** | `mkdir -p ~/.agents/skills/ifrs && cp ifrs/*.md ~/.agents/skills/ifrs/` |
| **Gemini CLI** | `mkdir -p ~/.gemini/skills/ifrs && cp ifrs/*.md ~/.gemini/skills/ifrs/` |
| **Cursor** | `mkdir -p ~/.cursor/skills/ifrs && cp ifrs/*.md ~/.cursor/skills/ifrs/` |

For a project-scoped install, use the project equivalent — `.claude/skills/`, `.agents/skills/`,
`.gemini/skills/` or `.cursor/skills/`.

> **Do not install by cloning this repository into a skills directory.** That places `SKILL.md` at
> `ifrs/ifrs/SKILL.md`, one level too deep, and the skill is then never discovered. The failure is
> silent: the files are present and frontmatter linters report success, but the agent does not see
> the skill.

### Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Skill never triggers | Nothing at `<skills-dir>/ifrs/SKILL.md` | `ls ~/.claude/skills/ifrs/SKILL.md`; reinstall if missing |
| Files present, still not found | Nested directory from `git clone` | `rm -rf ~/.claude/skills/ifrs`, then reinstall with the command above |
| Correct layout, agent blind to it | Agent not restarted, or the skills directory did not exist at start-up | Restart the agent. Gemini CLI: `/skills reload` |
| Works in one agent, not another | Wrong directory for that agent | Use `npx skills add`, or the per-agent row above |
| Cites IAS 1.25–26 for a 2027 period | Stale version installed | `npx skills update ifrs`, or re-copy from a fresh checkout |

## Example queries

**Preparers**

> Under IFRS 18, which category do foreign exchange differences on an intragroup monetary liability
> belong in, and does the answer change in the separate financial statements?

> We are transitioning from local GAAP with a corridor pension approach. What is the opening
> balance sheet adjustment, and is any IFRS 1 relief available?

> Walk through the ECL staging assessment for a portfolio that has breached a covenant but remains
> performing.

**Auditors**

> Produce the IFRS 16 lessee disclosure checklist with paragraph references, and flag which items
> are commonly missed.

> Our client capitalised configuration costs for a SaaS implementation. What does the IFRIC agenda
> decision require, and what evidence should I request?

> Which IFRS 18 management-defined performance measure disclosures are required, and what does the
> reconciliation need to show?

**Learners**

> Explain the difference between a mandatory exception and an optional exemption in IFRS 1, with
> an example of each.

> Why can goodwill impairment never be reversed when other impairments can?

## How it works

The skill uses progressive disclosure. `SKILL.md` is a routing file of 82 lines that the agent
always reads; it decides which of four reference files to load based on the question, so a simple
query does not pull all 13,321 lines into context.

| File | Purpose |
|---|---|
| `SKILL.md` | Routing, citation rules, and the 2027 date-check table |
| `standards-reference.md` | Standard-by-standard detail, interpretations, sustainability, amendment register |
| `workflows.md` | Multi-step procedures with worked examples and journal entries |
| `compliance-templates.md` | Per-standard disclosure checklists and audit templates |
| `transition-guide.md` | First-time adoption, IFRS 1 exemptions, GAAP difference matrices |

## How the content was verified

| Check | Result |
|---|---|
| Paragraph citations resolved against the standards' own text | **4,234 of 4,240 (99.86%)** |
| Citations additionally read for meaning, weighted to high-risk claims | 171 sampled, 3 defects found and fixed |
| Journal-entry blocks balancing | **60 of 60** |
| Runnable assertion blocks | **6 blocks, 38 assertions, all passing** |

The assertion blocks are committed inside `workflows.md` and `transition-guide.md` and are intended
to be re-run. They prove, among other things, that the IFRS 17 liability cross-casts to its
components and that an IAS 36 impairment is absorbed by goodwill before pro rata allocation.

Sources, method, and the traps encountered are documented in [`docs/SOURCING.md`](docs/SOURCING.md).

## Scope and limitations

Stated plainly, because knowing where a reference stops is part of using it.

- **This is not professional advice.** It supports judgment; it does not replace it. Conclusions
  affecting financial statements should be reviewed by a qualified professional.
- **IFRS 20** *Regulatory Assets and Regulatory Liabilities* is covered at status level only. It was
  issued on 27 May 2026, after the annual edition of the standards closed, so its paragraph text is
  not yet published and no disclosure checklist exists for it. IFRS 14 applies until an entity
  adopts IFRS 20.
- **US GAAP comparisons are source-verified, not primary-verified.** The FASB Codification is
  registration-gated, so the comparison follows EY *US GAAP versus IFRS* (January 2026) and
  FASB ASU 2025-10. Confirm ASC references against the Codification before relying on them. The US
  federal tax consequences of abandoning LIFO are flagged as requiring a specialist, not stated.
- **Roughly 50 IFRIC citations could not be verified** — IFRIC 2, 10, 12, 17 and 21 have no
  machine-readable source text available.
- **Basis for Conclusions text is not included.** BC paragraphs are cited as pointers, or attributed
  to an agenda decision that quotes them. The skill never characterises what a BC paragraph argues.
- **Jurisdiction matters.** EU-adopted IFRS is not the same as IFRS as issued by the IASB, and an
  unendorsed standard cannot be applied in the EU. The amendment register records endorsement status.
- **Content is current as at 28 August 2026** and will drift. Standards change; verify effective
  dates for periods after that.

## Contributing

Contributions are welcome, subject to the evidentiary standard the content is held to: every
technical claim carries a paragraph-level citation verified against the standard's own text, and
every worked example balances and ships with a runnable assertion. See
[`CONTRIBUTING.md`](CONTRIBUTING.md).

Corrections are especially welcome. If a citation is wrong, open a content-correction issue with the
correct paragraph reference and your source.

## Licence and citation

MIT — see [`LICENSE`](LICENSE). IFRS and IAS standards are copyright of the IFRS Foundation; this
repository paraphrases requirements and cites paragraphs, and reproduces no standard text.

To cite this repository, see [`CITATION.cff`](CITATION.cff) or use the "Cite this repository" button
in the GitHub sidebar.
