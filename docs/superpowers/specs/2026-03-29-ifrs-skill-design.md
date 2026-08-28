# IFRS Skill Design Spec

## Overview

A comprehensive IFRS skill for Claude Code that provides accounting guidance, compliance/audit support, and GAAP-to-IFRS transition assistance. The skill covers all current IFRS and IAS standards, adapts to the user's expertise level, and produces appropriate output formats depending on the task.

## Architecture: Hub + Reference

### Core Hub — `SKILL.md`

The lightweight entry point (~200-300 words) installed at `~/.claude/skills/ifrs/SKILL.md`. Contains:

- **Decision flowchart** to determine task type (guidance / compliance / transition)
- **Audience detection** logic to adapt depth (professional vs. learner)
- **Citation rules** for when and how to reference IFRS paragraphs
- **Web verification triggers** for currency checks
- **Loading instructions** for supporting reference files

### Supporting Reference Files

| File | Purpose | Loaded When |
|------|---------|-------------|
| `standards-reference.md` | All active IFRS/IAS standards in consistent per-standard format | User asks about a specific standard or needs technical detail |
| `workflows.md` | Step-by-step procedures for complex tasks | User needs to walk through a multi-step IFRS process |
| `compliance-templates.md` | Checklists, gap analysis templates, audit memo formats | User requests compliance check, audit support, or structured deliverable |
| `transition-guide.md` | Framework-agnostic GAAP-to-IFRS transition guidance | User asks about adopting or transitioning to IFRS |

## Decision Flow

### 1. Detect Task Type

- **Guidance question** — Load `standards-reference.md` for the relevant standard(s)
- **Compliance/audit task** — Load `compliance-templates.md` + `standards-reference.md`
- **Transition task** — Load `transition-guide.md` + `standards-reference.md`
- **General/learning question** — Answer from `SKILL.md` core principles; load reference only if deeper detail is needed
- **Mixed task** (e.g., transition + compliance) — Load all relevant reference files; apply the most structured output format among the applicable task types

### 2. Detect Audience

- **Professional mode** — User uses technical language, mentions audit/reporting context. Respond with IFRS paragraph citations, technical terminology, and assume accounting knowledge.
- **Learner mode** — User asks "what is" questions, mentions studying, uses basic framing. Respond with plain language explanations, practical examples, and offer to provide technical references.
- **Default** — Professional. Adjust if user signals otherwise.

### 3. Determine Output Format

- **Compliance/audit task** — Structured format by default (checklist, gap analysis table, audit memo)
- **Specific technical question** — Cited answer with paragraph references
- **Learning/conceptual question** — Conversational with examples
- **User requests a specific format** — Use that format

### 4. Verify Currency

For effective dates, recent amendments, exposure drafts, or jurisdiction-specific adoption timelines, verify via web search before answering.

## Citation & Reference Style

### Professional Mode

- Format: `IFRS 15.35(c)`, `IAS 36.12` — standard number, paragraph, sub-paragraph
- Include Basis for Conclusions references when explaining rationale (e.g., `IFRS 15.BC145`)
- Group citations at end of paragraph, not inline for every clause

### Learner Mode

- No paragraph citations unless the user asks
- Plain language with practical examples
- Offer to provide technical references for deeper study

### Web Verification Triggers

- Questions about effective dates
- Questions about amendments or exposure drafts
- Questions referencing "latest" or "current" requirements
- Jurisdiction-specific adoption timelines

## Standards Reference Structure (`standards-reference.md`)

Each standard follows a consistent template:

- **Standard number & name** (e.g., IFRS 15 — Revenue from Contracts with Customers)
- **Scope** — what it applies to and key exclusions
- **Core principle** — fundamental requirement in 1-2 sentences
- **Key recognition/measurement rules** — critical thresholds, criteria, or models
- **Disclosure requirements** — summary of what must be disclosed
- **Common pitfalls** — frequent mistakes or areas of judgment
- **Related standards** — cross-references to other IFRS/IAS

### Coverage

- IFRS 1-17 (noting IFRS 14 is limited scope)
- IAS 1-41 (active standards only; skip superseded standards like IAS 11, IAS 17, IAS 18)
- Key IFRIC/SIC interpretations referenced within the parent standard's entry

Claude will search for the specific standard number rather than reading the entire file.

## Workflows (`workflows.md`)

Step-by-step procedures for common complex tasks:

### Revenue Recognition (IFRS 15) — 5-Step Model
1. Identify the contract
2. Identify performance obligations
3. Determine transaction price
4. Allocate transaction price to performance obligations
5. Recognize revenue when/as obligations are satisfied

### Lease Accounting (IFRS 16)
1. Determine if arrangement contains a lease
2. Assess lease term and renewal/termination options
3. Classify (all leases on balance sheet for lessees; finance vs. operating for lessors)
4. Calculate right-of-use asset and lease liability

### Impairment Testing (IAS 36)
1. Identify indicators of impairment
2. Determine recoverable amount (higher of fair value less costs of disposal vs. value in use)
3. Compare carrying amount to recoverable amount
4. Recognize or reverse impairment loss

### Financial Instruments (IFRS 9)
1. Classification (amortised cost / FVOCI / FVTPL)
2. Expected credit loss model (simplified vs. general approach)
3. Hedge accounting eligibility and documentation

### First-Time Adoption (IFRS 1)
1. Identify date of transition and first IFRS reporting period
2. Apply mandatory exceptions and optional exemptions
3. Prepare opening IFRS balance sheet
4. Reconcile equity and profit/loss from previous GAAP
5. Meet disclosure requirements

## Compliance Templates (`compliance-templates.md`)

### Disclosure Completeness Checklist
Per-standard checklist of required disclosures with yes/no/N/A columns.

### Gap Analysis Template

| Area | Current Treatment | IFRS Requirement | Gap | Action Required | Priority |
|------|-------------------|-------------------|-----|-----------------|----------|

### Audit Memo Format
- **Issue** — what is being assessed
- **Applicable standard** — IFRS/IAS reference with paragraph citations
- **Facts & analysis** — assessment of the transaction or balance
- **Conclusion** — compliant / non-compliant / requires judgment
- **Recommendation** — action items if applicable

## Transition Guide (`transition-guide.md`)

Framework-agnostic approach to GAAP-to-IFRS transition:

- Focus on IFRS requirements rather than mapping from any specific GAAP
- Flag common areas where differences typically arise (revenue, leases, financial instruments, employee benefits, provisions, etc.)
- IFRS 1 first-time adoption procedure (mandatory exceptions, optional exemptions)
- Reconciliation approach for opening balance sheet
- Disclosure requirements for first IFRS financial statements

## Skill Metadata

```yaml
name: ifrs
description: Use when answering questions about IFRS standards, financial reporting, revenue recognition, lease accounting, impairment, disclosure requirements, IFRS compliance checks, audit support, or transitioning from local GAAP to IFRS.
```

## Installation Path

```
~/.claude/skills/ifrs/
  SKILL.md
  standards-reference.md
  workflows.md
  compliance-templates.md
  transition-guide.md
```

## Key Design Decisions

1. **Hub + Reference architecture** — keeps the core skill lightweight while allowing deep reference on demand
2. **Framework-agnostic transitions** — focuses on IFRS requirements rather than trying to be an expert in every local GAAP
3. **Audience adaptation** — defaults to professional mode, adjusts to learner mode based on signals
4. **Hybrid currency approach** — embeds core principles statically, verifies effective dates and amendments via web search
5. **Structured output for compliance** — produces checklists, gap analyses, and audit memos by default for compliance/audit tasks
6. **Paragraph-level citations** — cites IFRS paragraphs for technical queries, omits for learner-mode responses
