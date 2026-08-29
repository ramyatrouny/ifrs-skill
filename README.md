# IFRS Skill

**A cited IFRS and IAS reference that plugs into an AI assistant.** Ask a question in plain
English; get an answer with the paragraph reference attached, so you can check it against the
standard yourself.

Written for controllers, financial reporting teams and auditors, and for the developers who install
it on their behalf.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/ramyatrouny/ifrs-skill)](https://github.com/ramyatrouny/ifrs-skill/releases)
[![Content currency](https://img.shields.io/badge/content%20current-28%20August%202026-informational)](docs/SOURCING.md)

```bash
npx skills add ramyatrouny/ifrs-skill
```

**You need one of these AI assistants already installed:** Claude Code, Codex CLI, Gemini CLI or
Cursor. This adds IFRS knowledge to an assistant you already use; it is not a standalone
application. Installation for each is [below](#installation).

> **This content is compiled with AI assistance and contains known and expected residual errors.**
> Every paragraph reference must be confirmed against the standard before it is relied on in a
> financial statement or working paper. Citations produced by this skill are not audit evidence:
> treat them as a pointer to the paragraph you then read. It does not replace professional
> judgment. See [Scope and limitations](#scope-and-limitations).

---

## Contents

- [Why this exists](#why-this-exists)
- [Quickstart](#quickstart)
- [Coverage](#coverage)
- [IFRS 18 — Presentation and Disclosure, mandatory 2027](#ifrs-18--presentation-and-disclosure-mandatory-2027)
- [Installation](#installation)
- [Troubleshooting](#troubleshooting)
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

**An exemption that no longer exists.** The transition guide listed the IFRS 1 exemption at
paragraphs D10–D11, permitting cumulative actuarial gains and losses to be reset to zero on
transition. Those paragraphs were deleted by IAS 19 as amended in June 2011, a deletion recorded at
IFRS 1.39L — the corridor approach went with them, so there is no longer a deferred actuarial
balance to reset and the full net defined benefit liability is recognised either way.

The exemption is therefore redundant rather than withdrawn, and its absence changes no measurement.
The hazard is that stale secondary sources still list it: a first-time adopter who searches for
D10–D11 finds a live-looking exemption, and plans around relief that is not there.

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

**2. Verify it installed.** Two checks, neither of which requires you to judge an accounting answer.

Files in the right place:

```bash
ls ~/.claude/skills/ifrs/SKILL.md
```

It must print that path. If it prints nothing, or a path ending `ifrs/ifrs/SKILL.md`, see
[Troubleshooting](#troubleshooting).

The agent can actually see it — ask:

> List the supporting files the IFRS skill gives you access to.

It should name four: `standards-reference.md`, `workflows.md`, `compliance-templates.md` and
`transition-guide.md`. That answer is deterministic and checkable by someone who knows no IFRS.
An agent answering from its own knowledge cannot produce that list.

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
| Checklist rows | **1,554** | Cited disclosure requirements, each with its paragraph reference |
| Paragraph citations | **4,438** | Resolved against the standards' own text where a source exists |

Sustainability standards IFRS S1 and IFRS S2 are covered, as is the Conceptual Framework, the
IFRS for SMEs Accounting Standard, and a jurisdictional adoption map including EU and UK
endorsement status.

Content is current as at **28 August 2026**.

## IFRS 18 — Presentation and Disclosure, mandatory 2027

IFRS 18 supersedes IAS 1 for annual periods beginning on or after 1 January 2027, with earlier
application permitted. It moves several requirements out of IAS 1 into IAS 8, which it retitles
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

Prefer the first: it is the only one that does not depend on where you are in the filesystem.

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

These copy from a local checkout, so clone the repository somewhere neutral first — anywhere
outside a skills directory — and run them from inside it:

```bash
git clone https://github.com/ramyatrouny/ifrs-skill.git
cd ifrs-skill
```

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
always reads; it decides which of the four reference files to load based on the question, so a
simple query does not pull the whole repository into context.

**Context cost — read this before deploying.** The reference files are large, and routing narrows
the read without making it small:

| File | Size | Approx. tokens |
|---|---|---|
| `SKILL.md` | 6 KB | ~1,600 |
| `transition-guide.md` | 164 KB | ~43,000 |
| `workflows.md` | 196 KB | ~51,000 |
| `compliance-templates.md` | 322 KB | ~85,000 |
| `standards-reference.md` | 923 KB | ~242,000 |

A guidance question routes to `standards-reference.md`, around **244,000 tokens**. A compliance task
routes to that plus `compliance-templates.md`, around **327,000 tokens**. Use an agent with a large
context window, and name the standard you are asking about — a question scoped to IFRS 16 costs far
less than an open one.

| File | Purpose |
|---|---|
| `SKILL.md` | Routing, citation rules, and the 2027 date-check table |
| `standards-reference.md` | Standard-by-standard detail, interpretations, sustainability, amendment register |
| `workflows.md` | Multi-step procedures with worked examples and journal entries |
| `compliance-templates.md` | Per-standard disclosure checklists and audit templates |
| `feature-review.md` | Reviewing software that produces accounting figures, in plain English |
| `transition-guide.md` | First-time adoption, IFRS 1 exemptions, GAAP difference matrices |

## How the content was verified

Two checks were run, and they measure different things. The distinction matters more than either
number. Both cover every claim in the skill with one stated exception: the labelled practice notes
in `feature-review.md`, which describe convention rather than requirement and are uncited by design
— see Scope and limitations, and [`docs/adr/0001-uncited-practice-notes.md`](docs/adr/0001-uncited-practice-notes.md).

**Resolution — does the cited paragraph exist in the standard's own text?**
Of 4,438 paragraph citations, 4,231 can be checked against an extracted copy of the standard;
**4,225 of those resolve (99.86%)**. The remaining 207 cite standards for which no machine-readable
source was obtainable — chiefly IAS 39 and nine IFRIC and SIC interpretations. Six citations do not
resolve and are correct as written: four Basis for Conclusions pointers, one Illustrative Examples
reference, and `IFRS 7.27A`, which the text identifies as a deleted paragraph.

Reproduce it yourself with `python3 scripts/check_citations.py --verbose`, having rebuilt the source
corpus per [`docs/SOURCING.md`](docs/SOURCING.md).

This check catches a wrong paragraph number. It does **not** catch a correct number attached to a
wrong statement.

**Semantic review — does the paragraph say what this skill says it says?**
A sample of 171 citations was read in full during the August 2026 audit, weighted towards
prohibitions, thresholds, deadlines, lettered sub-items and checklist rows asserting that a
disclosure is required. Three were wrong and were corrected. That sample was a one-off review rather
than a committed artefact, so unlike the resolution figure above it cannot be re-run from this
repository — treat it as a stated finding, not a reproducible measurement.

On that sample, roughly 1.8% of citations carried a semantic defect. **Expect a comparable density
in the ~96% not read for meaning — on the order of several dozen.** Treat every citation here as a
pointer to a paragraph you then read, not as a substitute for reading it.

| Other checks | Result |
|---|---|
| Journal-entry blocks balancing | **60 of 60** |
| Runnable assertion blocks | **6 blocks, 38 assertions, all passing** |

You can re-run the mechanical checks yourself:

```bash
python3 scripts/check_skill_structure.py    # frontmatter, referenced files, size
python3 scripts/check_journal_entries.py    # every Dr/Cr block, every assertion block
python3 scripts/check_citations.py          # every paragraph citation (needs the source corpus)
```

The assertion blocks are committed inside `workflows.md` and `transition-guide.md` and are intended
to be re-run. They prove, among other things, that the IFRS 17 liability cross-casts to its
components and that an IAS 36 impairment is absorbed by goodwill before pro rata allocation.

Sources, method, and the traps encountered are documented in [`docs/SOURCING.md`](docs/SOURCING.md).

## Scope and limitations

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
- **60 interpretation citations could not be verified** — IFRIC 2, 10, 12, 17 and 21 and SIC-7, 10,
  25 and 29 have no machine-readable source text available.
- **Basis for Conclusions text is not included.** BC paragraphs are cited as pointers, or attributed
  to an agenda decision that quotes them. The skill never characterises what a BC paragraph argues.
- **Jurisdiction matters.** EU-adopted IFRS is not the same as IFRS as issued by the IASB, and an
  unendorsed standard cannot be applied in the EU. The amendment register records endorsement status.
- **Practice notes in `feature-review.md` are uncited by design.** Every other claim in this
  skill resolves to a paragraph of a standard. Feature reviews additionally carry blocks headed
  *"In practice — how finance teams usually handle this. Not a requirement."*, describing what
  teams conventionally do rather than what IFRS obliges. No standard says any of it, so none of
  it is citable. The heading is fixed so the two can never be confused; the reasoning is in
  [`docs/adr/0001-uncited-practice-notes.md`](docs/adr/0001-uncited-practice-notes.md).
- **Content is current as at 28 August 2026** and will drift. Standards change; verify effective
  dates for periods after that.

## Contributing

Contributions are welcome, subject to the evidentiary standard the content is held to: every
technical claim carries a paragraph-level citation verified against the standard's own text, and
every worked example balances and ships with a runnable assertion. The single exception is the
labelled practice notes in `feature-review.md`, described under Scope and limitations. See
[`CONTRIBUTING.md`](CONTRIBUTING.md).

Corrections are especially welcome. If a citation is wrong, open a content-correction issue with the
correct paragraph reference and your source.

## Licence and citation

MIT — see [`LICENSE`](LICENSE). IFRS and IAS standards are copyright of the IFRS Foundation; this
repository paraphrases requirements and cites paragraphs, and reproduces no standard text.

To cite this repository, see [`CITATION.cff`](CITATION.cff) or use the "Cite this repository" button
in the GitHub sidebar.
