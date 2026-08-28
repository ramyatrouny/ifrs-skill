# IFRS Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a comprehensive IFRS skill for Claude Code that provides accounting guidance, compliance/audit support, and GAAP-to-IFRS transition assistance across all current IFRS/IAS standards.

**Architecture:** Hub + Reference pattern. A lightweight `SKILL.md` hub handles decision logic (task type, audience, output format, currency checks) and loads heavy reference files on demand. Four supporting files provide standards reference, workflows, compliance templates, and transition guidance.

**Tech Stack:** Claude Code skill (Markdown files installed to `~/.claude/skills/ifrs/`)

**Spec:** `docs/superpowers/specs/2026-03-29-ifrs-skill-design.md`

---

## Task 1: Create Skill Directory and Core Hub (`SKILL.md`)

**Files:**
- Create: `~/.claude/skills/ifrs/SKILL.md`

This is the lightweight entry point. It must stay under 300 words to be token-efficient. It contains the decision flowchart, audience detection, citation rules, web verification triggers, and instructions for loading supporting files.

- [ ] **Step 1: Create the skill directory**

```bash
mkdir -p ~/.claude/skills/ifrs
```

- [ ] **Step 2: Write `SKILL.md`**

Create `~/.claude/skills/ifrs/SKILL.md` with the following content:

```markdown
---
name: ifrs
description: Use when answering questions about IFRS standards, financial reporting, revenue recognition, lease accounting, impairment, disclosure requirements, IFRS compliance checks, audit support, or transitioning from local GAAP to IFRS.
---

# IFRS

Comprehensive IFRS guidance, compliance support, and GAAP-to-IFRS transition assistance covering all current IFRS and IAS standards.

## Decision Flow

### 1. Detect Task Type

- **Guidance question** — Read `standards-reference.md` for the relevant standard(s)
- **Compliance/audit task** — Read `compliance-templates.md` + `standards-reference.md`
- **Transition task** — Read `transition-guide.md` + `standards-reference.md`
- **General/learning question** — Answer from this file; load reference only if deeper detail needed
- **Mixed task** (e.g., transition + compliance) — Load all relevant files; use the most structured output format

### 2. Detect Audience

- **Professional** (default) — Technical language, mentions audit/reporting. Cite IFRS paragraphs (e.g., `IFRS 15.35(c)`, `IAS 36.12`). Include Basis for Conclusions refs for rationale. Group citations at end of paragraph.
- **Learner** — Asks "what is", mentions studying, basic framing. Plain language with examples. No citations unless asked. Offer technical references for deeper study.

### 3. Output Format

- **Compliance/audit** — Structured: checklist, gap analysis, audit memo (see `compliance-templates.md`)
- **Technical question** — Cited answer with paragraph references
- **Learning question** — Conversational with examples
- **User requests format** — Use that format

### 4. Verify Currency

For effective dates, amendments, exposure drafts, or jurisdiction-specific timelines: **search the web** before answering.

## Workflows

For multi-step IFRS procedures (revenue recognition, lease accounting, impairment testing, financial instruments, first-time adoption), read `workflows.md`.

## Reference

For standard-by-standard details (scope, core principle, recognition/measurement, disclosure, pitfalls), search `standards-reference.md` for the specific standard number.
```

- [ ] **Step 3: Verify the file exists and frontmatter is valid**

```bash
head -5 ~/.claude/skills/ifrs/SKILL.md
```

Expected output:
```
---
name: ifrs
description: Use when answering questions about IFRS standards, financial reporting, revenue recognition, lease accounting, impairment, disclosure requirements, IFRS compliance checks, audit support, or transitioning from local GAAP to IFRS.
---
```

- [ ] **Step 4: Verify word count is under 300**

```bash
wc -w ~/.claude/skills/ifrs/SKILL.md
```

Expected: under 300 words.

- [ ] **Step 5: Commit**

```bash
git add ~/.claude/skills/ifrs/SKILL.md
git commit -m "feat: add IFRS skill core hub (SKILL.md)"
```

---

## Task 2: Write Standards Reference (`standards-reference.md`)

**Files:**
- Create: `~/.claude/skills/ifrs/standards-reference.md`

This is the largest file. Each standard follows a consistent template: standard number & name, scope, core principle, key recognition/measurement rules, disclosure requirements, common pitfalls, related standards. Covers IFRS 1-17 and active IAS standards. Claude will search for specific standard numbers rather than reading the whole file.

- [ ] **Step 1: Write the IFRS standards section (IFRS 1-17)**

Create `~/.claude/skills/ifrs/standards-reference.md` with the following content for IFRS 1 through IFRS 17. Each entry follows this template:

```markdown
# IFRS Standards Reference

## How to Use This File

Search for the specific standard number (e.g., "IFRS 15" or "IAS 36") rather than reading the entire file. Each standard follows a consistent format: scope, core principle, key rules, disclosure requirements, common pitfalls, and related standards.

---

## IFRS 1 — First-time Adoption of International Financial Reporting Standards

**Scope:** Applies to an entity's first IFRS financial statements and interim reports within that first IFRS reporting period.

**Core principle:** An entity prepares an opening IFRS statement of financial position at the date of transition, applying IFRS standards retrospectively, subject to mandatory exceptions and optional exemptions.

**Key rules:**
- Select IFRS accounting policies and apply them retrospectively to all periods presented
- Mandatory exceptions: derecognition of financial assets/liabilities, hedge accounting, estimates, non-controlling interests, classification of financial assets, embedded derivatives, government loans
- Optional exemptions: business combinations, share-based payment, insurance contracts, deemed cost for PP&E/intangibles/investment property, leases, cumulative translation differences, compound financial instruments, assets/liabilities of subsidiaries, and others
- Prepare reconciliations of equity and total comprehensive income from previous GAAP to IFRS

**Disclosure requirements:**
- Reconciliation of equity at date of transition and end of last period under previous GAAP
- Reconciliation of total comprehensive income for last period under previous GAAP
- Explanation of material adjustments to statement of financial position and comprehensive income
- If entity used fair value as deemed cost, disclose aggregated amounts

**Common pitfalls:**
- Applying exemptions inconsistently across group entities
- Failing to identify all mandatory exceptions (they are not optional)
- Incomplete reconciliation disclosures
- Using hindsight when IFRS 1 prohibits it for estimates

**Related standards:** All IFRS/IAS standards (IFRS 1 governs the transition to all of them)

---

## IFRS 2 — Share-based Payment

**Scope:** Transactions where entity receives goods/services in exchange for equity instruments, or incurs liabilities based on entity's share price.

**Core principle:** Recognize goods/services received at fair value; for equity-settled transactions, measure at grant-date fair value of equity instruments granted; for cash-settled, remeasure liability at each reporting date.

**Key rules:**
- Equity-settled: measure at grant-date fair value using option pricing model; recognize expense over vesting period; no subsequent remeasurement
- Cash-settled: measure at fair value of liability at each reporting date until settled; changes in fair value recognized in profit or loss
- Transactions with cash alternatives: account for as cash-settled if entity has obligation to settle in cash; otherwise equity-settled
- Vesting conditions: service and performance conditions affect number of instruments expected to vest; market conditions reflected in grant-date fair value
- Modifications: if beneficial to employee, recognize incremental fair value; if not beneficial, continue recognizing original grant-date fair value

**Disclosure requirements:**
- Nature and extent of share-based payment arrangements
- How fair value was determined (model, inputs, assumptions)
- Effect on profit or loss and financial position

**Common pitfalls:**
- Failing to distinguish market vs. non-market performance conditions
- Not recognizing expense for awards that fail to vest due to market conditions
- Incorrect modification accounting when terms are changed

**Related standards:** IAS 19 (employee benefits), IAS 32/IFRS 9 (financial instruments classification)

---

## IFRS 3 — Business Combinations

**Scope:** Transactions or events where an acquirer obtains control of one or more businesses. Excludes joint arrangements, common control combinations, and acquisition of an asset or group of assets that is not a business.

**Core principle:** The acquirer recognizes identifiable assets acquired and liabilities assumed at acquisition-date fair value, with any excess of consideration over net assets recognized as goodwill.

**Key rules:**
- Identify the acquirer (the entity that obtains control)
- Determine the acquisition date
- Recognize and measure identifiable assets, liabilities, and non-controlling interest at fair value
- Goodwill = consideration transferred + NCI + previously held equity interest - net identifiable assets at fair value
- Bargain purchase (negative goodwill): reassess, then recognize gain in profit or loss
- Measurement period: up to 12 months to finalize provisional amounts
- Acquisition-related costs expensed (not included in consideration)
- Contingent consideration: recognized at fair value at acquisition date; subsequent changes in P&L (unless equity-classified)

**Disclosure requirements:**
- Name and description of acquiree
- Acquisition date and percentage of voting equity acquired
- Primary reasons for the combination and description of how control was obtained
- Fair values of consideration, assets acquired, liabilities assumed
- Goodwill amount and factors contributing to it
- Revenue and profit/loss of acquiree since acquisition date

**Common pitfalls:**
- Including acquisition costs in goodwill instead of expensing them
- Failing to identify and separately recognize intangible assets (customer relationships, brand, technology)
- Not reassessing before recognizing a bargain purchase gain
- Measurement period adjustments treated as current period changes

**Related standards:** IAS 36 (goodwill impairment), IAS 38 (intangible assets), IFRS 10 (control)

---

## IFRS 5 — Non-current Assets Held for Sale and Discontinued Operations

**Scope:** Non-current assets (or disposal groups) whose carrying amount will be recovered principally through sale rather than continuing use, and discontinued operations.

**Core principle:** Assets held for sale are measured at the lower of carrying amount and fair value less costs to sell, and presented separately. Discontinued operations are presented separately in profit or loss.

**Key rules:**
- Held for sale criteria: available for immediate sale in present condition, sale highly probable (committed plan, active buyer search, expected within 12 months)
- Measure at lower of carrying amount and fair value less costs to sell
- Cease depreciation/amortization once classified as held for sale
- Present separately on the face of the statement of financial position
- Discontinued operation: component disposed of or classified as held for sale that represents a separate major line of business or geographical area, or is a subsidiary acquired exclusively for resale

**Disclosure requirements:**
- Description of non-current asset or disposal group
- Description of facts and circumstances of the sale/expected disposal
- Gain or loss recognized
- Segment in which the asset is reported
- For discontinued operations: single amount on face of statement of comprehensive income, with analysis in notes or on face

**Common pitfalls:**
- Classifying as held for sale when sale is not highly probable within 12 months
- Continuing to depreciate held-for-sale assets
- Not presenting discontinued operations separately
- Failing to meet the "separate major line of business" threshold for discontinued operations

**Related standards:** IAS 36 (impairment), IFRS 13 (fair value measurement)

---

## IFRS 6 — Exploration for and Evaluation of Mineral Resources

**Scope:** Expenditures incurred in connection with exploration for and evaluation of mineral resources before technical feasibility and commercial viability of extracting the resource are demonstrable.

**Core principle:** Entity may develop its own accounting policy for exploration and evaluation assets, subject to IAS 8 hierarchy. Must assess for impairment when facts and circumstances suggest carrying amount may exceed recoverable amount.

**Key rules:**
- Exploration and evaluation assets measured at cost on initial recognition
- Entity determines policy for which expenditures are recognized as E&E assets (at least cost of acquiring exploration rights)
- Classify as tangible or intangible depending on nature
- Impairment assessment required when: exploration rights expire, no further exploration planned, sufficient data shows resources are not commercially viable, carrying amount unlikely to be recovered through development or sale

**Disclosure requirements:**
- Accounting policy for exploration and evaluation expenditures
- Amounts of assets, liabilities, income, and expense and cash flows from exploration and evaluation

**Common pitfalls:**
- Not reclassifying out of E&E when technical feasibility and commercial viability are demonstrable
- Inconsistent policy application across exploration projects
- Missing impairment indicators specific to E&E assets

**Related standards:** IAS 36 (impairment), IAS 38 (intangible assets), IAS 16 (PP&E)

---

## IFRS 7 — Financial Instruments: Disclosures

**Scope:** All entities for all types of financial instruments recognized and unrecognized, except specific exclusions (e.g., subsidiaries, associates, employee benefits, insurance contracts, share-based payment).

**Core principle:** Disclose information that enables users to evaluate the significance of financial instruments and the nature and extent of risks arising from them.

**Key rules:**
- Significance disclosures: carrying amounts by category (amortised cost, FVOCI, FVTPL), reclassifications, offsetting, collateral, defaults
- Risk disclosures: credit risk (ECL, credit quality, concentrations), liquidity risk (maturity analysis), market risk (sensitivity analysis for interest rate, currency, other price risks)
- Hedge accounting disclosures: hedging strategy, risk management, amounts/timing/uncertainty of future cash flows, effects on financial statements
- Transfer disclosures: transferred assets not derecognized, continuing involvement

**Disclosure requirements:** This IS the disclosure standard — all requirements are disclosure requirements. Key tables include:
- Financial instruments by measurement category
- Credit risk exposure and ECL reconciliation
- Maturity analysis of financial liabilities
- Sensitivity analysis for each type of market risk

**Common pitfalls:**
- Incomplete maturity analysis (not using contractual undiscounted cash flows)
- Inadequate credit risk concentration disclosures
- Missing ECL reconciliation (stage movements)
- Not disaggregating sufficiently by risk type

**Related standards:** IFRS 9 (recognition/measurement), IFRS 13 (fair value), IAS 32 (presentation)

---

## IFRS 8 — Operating Segments

**Scope:** Entities whose debt or equity instruments are traded in a public market, or that are in the process of filing financial statements with a securities commission for the purpose of issuing instruments.

**Core principle:** Disclose information about operating segments, products/services, geographical areas, and major customers based on the internal reports regularly reviewed by the chief operating decision maker (CODM).

**Key rules:**
- Operating segment: component that engages in business activities, whose results are regularly reviewed by CODM, and for which discrete financial information is available
- Aggregation criteria: similar economic characteristics plus similar in nature of products, production processes, customer type, distribution methods, and regulatory environment
- Quantitative thresholds: report separately if revenue, profit/loss, or assets are 10% or more of combined totals
- At least 75% of external revenue must be included in reportable segments
- Measurement: use amounts reported to CODM (may differ from IFRS amounts)

**Disclosure requirements:**
- General information about how segments were identified
- Segment revenue (external and intersegment), profit/loss, assets, liabilities
- Reconciliations of segment totals to entity totals
- Entity-wide disclosures: products/services, geographical areas, major customers (10%+ of revenue)

**Common pitfalls:**
- Identifying segments based on external reporting structure rather than internal reports to CODM
- Aggregating segments that don't meet all aggregation criteria
- Incomplete reconciliations between segment and entity amounts

**Related standards:** IAS 1 (presentation), IAS 33 (EPS by segment if disclosed)

---

## IFRS 9 — Financial Instruments

**Scope:** All financial assets and financial liabilities, except interests in subsidiaries/associates/JVs, employee benefit rights, insurance contracts, share-based payment, and certain loan commitments.

**Core principle:** Financial assets classified based on business model and contractual cash flow characteristics. Impairment based on expected credit losses. Hedge accounting aligns with risk management.

**Key rules:**
- **Classification of financial assets:**
  - Amortised cost: hold to collect contractual cash flows; cash flows are solely payments of principal and interest (SPPI)
  - FVOCI: hold to collect and sell; cash flows pass SPPI test
  - FVTPL: all others, or fair value option to eliminate accounting mismatch
- **Classification of financial liabilities:** amortised cost (default) or FVTPL (fair value option with own credit in OCI)
- **Impairment — Expected Credit Loss (ECL):**
  - General approach (3-stage model): Stage 1 = 12-month ECL; Stage 2 = lifetime ECL (significant increase in credit risk); Stage 3 = lifetime ECL (credit-impaired)
  - Simplified approach: lifetime ECL from initial recognition (trade receivables, contract assets, lease receivables)
- **Hedge accounting:**
  - Cash flow hedge, fair value hedge, net investment hedge
  - Qualifying criteria: documented hedging relationship, hedging instrument and hedged item are eligible, hedge effectiveness requirements met
  - Effectiveness: economic relationship, credit risk does not dominate, hedge ratio matches risk management

**Disclosure requirements:** See IFRS 7 (separate disclosure standard for financial instruments)

**Common pitfalls:**
- Failing the SPPI test due to contractual features (e.g., leverage features, non-recourse)
- Not assessing significant increase in credit risk at each reporting date
- Using incurred loss model instead of expected credit loss model
- Inadequate hedge documentation at inception

**Related standards:** IFRS 7 (disclosures), IFRS 13 (fair value), IAS 32 (presentation/offsetting)

---

## IFRS 10 — Consolidated Financial Statements

**Scope:** Entities that are parents, except parents that meet all criteria for the exemption from preparing consolidated financial statements.

**Core principle:** A parent consolidates all entities it controls. Control exists when the investor has power over the investee, exposure to variable returns, and ability to use power to affect those returns.

**Key rules:**
- Three elements of control: (1) power over investee, (2) exposure/rights to variable returns, (3) ability to use power to affect returns
- Power: existing rights that give current ability to direct relevant activities (voting rights, contractual rights, potential voting rights)
- Assess control on continuous basis; reassess when facts and circumstances change
- De facto control possible with less than majority of voting rights
- Structured entities: assess power and variable returns even without voting rights
- Consolidation procedures: combine like items, eliminate intercompany transactions, uniform accounting policies, align reporting dates (max 3-month difference)

**Disclosure requirements:** See IFRS 12

**Common pitfalls:**
- Assuming majority ownership always means control (or minority always means no control)
- Not reassessing control when circumstances change
- Failing to identify de facto control situations
- Not consolidating structured entities where control exists

**Related standards:** IFRS 12 (disclosures), IFRS 3 (business combinations), IAS 27 (separate financial statements), IAS 28 (associates)

---

## IFRS 11 — Joint Arrangements

**Scope:** Arrangements where two or more parties have joint control.

**Core principle:** A party classifies its interest in a joint arrangement as either a joint operation (rights to assets and obligations for liabilities) or a joint venture (rights to net assets), and accounts for it accordingly.

**Key rules:**
- Joint control: contractually agreed sharing of control; decisions about relevant activities require unanimous consent
- Joint operation: parties have rights to assets and obligations for liabilities; recognize own assets, liabilities, revenue, expenses, and share of joint assets/liabilities/revenue/expenses
- Joint venture: parties have rights to net assets; account for using equity method per IAS 28
- Classification depends on structure, legal form, contractual terms, and other facts and circumstances
- Separate vehicle does not automatically make it a joint venture; assess whether structure gives parties rights to assets/obligations for liabilities

**Disclosure requirements:** See IFRS 12

**Common pitfalls:**
- Defaulting to joint venture classification for all arrangements in separate vehicles
- Not considering substance over legal form when classifying
- Applying equity method to joint operations

**Related standards:** IFRS 12 (disclosures), IAS 28 (equity method), IFRS 10 (control assessment)

---

## IFRS 12 — Disclosure of Interests in Other Entities

**Scope:** Entities with interests in subsidiaries, joint arrangements, associates, or unconsolidated structured entities.

**Core principle:** Disclose information that enables users to evaluate the nature of and risks associated with interests in other entities and the effects on financial position, performance, and cash flows.

**Key rules:**
- Significant judgments and assumptions in determining control, joint control, significant influence, type of joint arrangement
- Subsidiary disclosures: NCI composition, summarized financials for material subsidiaries, significant restrictions
- Joint arrangement and associate disclosures: nature, summarized financials, risks
- Unconsolidated structured entities: nature, purpose, risks, maximum exposure to loss
- Investment entity disclosures (if applicable)

**Disclosure requirements:** This IS the disclosure standard. Key areas:
- Significant judgments about control/joint control/significant influence
- Interests in subsidiaries (NCI, restrictions, changes in ownership without loss of control)
- Interests in joint arrangements and associates (summarized financial information)
- Interests in unconsolidated structured entities (nature of risks)

**Common pitfalls:**
- Omitting structured entity disclosures
- Insufficient disclosure of significant judgments
- Not providing summarized financials for material associates/JVs

**Related standards:** IFRS 10 (control), IFRS 11 (joint arrangements), IAS 28 (associates)

---

## IFRS 13 — Fair Value Measurement

**Scope:** Applies when another IFRS requires or permits fair value measurement or disclosures. Does not apply to share-based payment (IFRS 2), leases (IFRS 16), or measurements that are similar to but not fair value (e.g., NRV in IAS 2, VIU in IAS 36).

**Core principle:** Fair value is the price that would be received to sell an asset or paid to transfer a liability in an orderly transaction between market participants at the measurement date (exit price).

**Key rules:**
- Unit of account: determined by other standards; IFRS 13 determines how to measure
- Market participants: knowledgeable, willing, able, independent
- Fair value hierarchy:
  - Level 1: quoted prices in active markets for identical items (unadjusted)
  - Level 2: inputs other than Level 1 that are observable (directly or indirectly)
  - Level 3: unobservable inputs (entity's own assumptions)
- Non-financial assets: highest and best use concept
- Liabilities and own equity instruments: assume transfer (not settlement); non-performance risk included
- Valuation techniques: market approach, income approach, cost approach — maximize observable inputs

**Disclosure requirements:**
- Fair value measurements by hierarchy level
- Level 3: reconciliation, valuation techniques, significant unobservable inputs, sensitivity
- Transfers between levels
- Recurring vs. non-recurring measurements

**Common pitfalls:**
- Using entry price instead of exit price
- Ignoring highest and best use for non-financial assets
- Insufficient Level 3 disclosures
- Not maximizing use of observable inputs

**Related standards:** IFRS 9 (financial instruments at FV), IAS 40 (investment property at FV), IAS 41 (biological assets at FV)

---

## IFRS 14 — Regulatory Deferral Accounts

**Scope:** Limited to first-time adopters of IFRS that conduct rate-regulated activities and recognized regulatory deferral account balances under previous GAAP. Not available to existing IFRS reporters.

**Core principle:** Permits (but does not require) first-time adopters to continue recognizing regulatory deferral account balances on transition to IFRS, with specific presentation and disclosure requirements.

**Key rules:**
- Optional standard — entity may elect to apply
- Continue previous GAAP accounting policies for regulatory deferral accounts
- Present regulatory deferral account balances as separate line items on statement of financial position
- Present net movement in regulatory deferral account balances as separate line item(s) in profit or loss and OCI
- Interim standard pending IASB's comprehensive project on rate-regulated activities (now IFRS 14 is effectively superseded by IFRS 18 considerations)

**Disclosure requirements:**
- Nature and risks of rate regulation and its effects
- Accounting policies for regulatory deferral accounts
- Reconciliation of carrying amounts

**Common pitfalls:**
- Available only to first-time IFRS adopters, not existing reporters
- Cannot be adopted by entities that did not recognize such balances under previous GAAP

**Related standards:** IFRS 1 (first-time adoption)

---

## IFRS 15 — Revenue from Contracts with Customers

**Scope:** All contracts with customers, except leases (IFRS 16), insurance contracts (IFRS 17), financial instruments (IFRS 9), and certain non-monetary exchanges between entities in the same line of business.

**Core principle:** Recognize revenue to depict the transfer of promised goods or services to customers in an amount that reflects the consideration to which the entity expects to be entitled.

**Key rules:**
- **5-step model:**
  1. Identify the contract (enforceable rights and obligations, commercial substance, probable collection)
  2. Identify performance obligations (distinct goods/services, or series of distinct goods/services)
  3. Determine transaction price (variable consideration constrained, significant financing component, non-cash consideration, consideration payable to customer)
  4. Allocate transaction price (relative standalone selling prices; residual approach or adjusted market assessment if standalone price not directly observable)
  5. Recognize revenue when (or as) performance obligation is satisfied
- Point in time vs. over time: over time if customer simultaneously receives/consumes benefits, entity's performance creates/enhances customer-controlled asset, or entity has no alternative use and enforceable right to payment for performance to date
- Contract modifications: treated as separate contract if additional distinct goods/services at standalone selling price; otherwise prospective or cumulative catch-up
- Contract costs: incremental costs of obtaining a contract capitalized if expected to be recovered; costs to fulfill capitalized if relate directly to contract, generate resources, and expected to be recovered
- Licensing: right to access (over time) vs. right to use (point in time)

**Disclosure requirements:**
- Disaggregation of revenue (nature, timing, uncertainty)
- Contract balances (receivables, contract assets, contract liabilities) with explanations of changes
- Performance obligations (when typically satisfied, significant payment terms, variable consideration, obligations for returns/refunds)
- Transaction price allocated to remaining performance obligations
- Significant judgments (timing of satisfaction, transaction price determination)

**Common pitfalls:**
- Not identifying distinct performance obligations in bundled arrangements
- Incorrectly constraining variable consideration (either too aggressively or not enough)
- Failing to identify significant financing components
- Misclassifying over-time vs. point-in-time recognition
- Not capitalizing contract costs when criteria are met
- License classification errors (access vs. use)

**Related standards:** IFRS 9 (financial instruments aspects of contracts), IAS 37 (onerous contracts), IFRS 16 (lease components in contracts)

---

## IFRS 16 — Leases

**Scope:** All leases, including subleases, except leases of minerals/petroleum/gas, biological assets, service concession arrangements, IP licenses (IFRS 15), and rights held under licensing agreements (IAS 38).

**Core principle:** A lessee recognizes a right-of-use asset and a lease liability for all leases (with optional exemptions for short-term leases and low-value assets). Lessors classify leases as finance or operating.

**Key rules:**
- **Lessee accounting:**
  - Recognize right-of-use (ROU) asset and lease liability at commencement
  - Lease liability: present value of lease payments (fixed, variable linked to index/rate, expected residual guarantees, purchase option if reasonably certain, termination penalties) discounted at rate implicit in lease or incremental borrowing rate
  - ROU asset: lease liability + initial direct costs + prepayments - lease incentives + estimated restoration costs
  - Subsequently: depreciate ROU asset; accrete interest on lease liability
  - Optional exemptions: short-term leases (12 months or less), low-value assets (below ~US$5,000 when new)
  - Lease modifications: remeasure liability (separate lease if increases scope at standalone price; otherwise adjust ROU and liability)
- **Lessor accounting:**
  - Finance lease: derecognize underlying asset, recognize net investment; recognize finance income over lease term
  - Operating lease: retain underlying asset; recognize lease income straight-line (or another systematic basis)
  - Classification criteria (substantially similar to legacy IAS 17): transfer of substantially all risks and rewards = finance lease

**Disclosure requirements:**
- Lessee: depreciation by class of ROU asset, interest expense, short-term/low-value lease expense, variable lease payments not in liability, total cash outflow for leases, additions to ROU assets, maturity analysis of lease liabilities
- Lessor: finance lease - selling profit/loss, finance income, net investment; operating lease - lease income, maturity analysis

**Common pitfalls:**
- Not identifying embedded leases in service contracts
- Using incorrect discount rate (incremental borrowing rate is entity- and asset-specific)
- Excluding variable payments linked to index/rate from initial measurement
- Lease term determination: not properly assessing extension/termination options
- Short-term exemption: cannot apply if lease has a purchase option

**Related standards:** IFRS 15 (separating lease and non-lease components), IAS 36 (ROU asset impairment), IAS 40 (investment property held as ROU)

---

## IFRS 17 — Insurance Contracts

**Scope:** Insurance contracts (including reinsurance contracts) issued, reinsurance contracts held, and investment contracts with discretionary participation features (if entity also issues insurance contracts).

**Core principle:** Measure insurance contracts as the total of the fulfilment cash flows and the contractual service margin (CSM), recognizing profit as service is provided.

**Key rules:**
- **General Measurement Model (GMM/BBA):**
  - Fulfilment cash flows = estimates of future cash flows + discount adjustment + risk adjustment for non-financial risk
  - CSM = unearned profit, released to P&L as coverage units are provided
  - Onerous contracts: recognize loss immediately; no CSM
  - Subsequent measurement: unlock fulfilment cash flows; adjust CSM for changes in future service
- **Premium Allocation Approach (PAA):** simplified approach for short-duration contracts (coverage period of one year or less, or qualifies). Similar in outcome to current non-life unearned premium approach.
- **Variable Fee Approach (VFA):** for direct participating contracts (substantial share of fair value of underlying items). CSM adjusted for entity's share of changes in fair value of underlying items.
- **Reinsurance contracts held:** measured similarly but separately from underlying insurance contracts; may recognize gain on initial recognition if onerous underlying contracts
- **Discount rates:** reflect characteristics of cash flows (currency, timing, liquidity)
- **Risk adjustment:** compensation entity requires for bearing uncertainty of cash flows (not prescribed method)
- **Level of aggregation:** groups of contracts issued within one year, subdivided into onerous, no significant possibility of becoming onerous, and remaining

**Disclosure requirements:**
- Reconciliation of carrying amounts (opening to closing, showing each component)
- Expected recognition of CSM
- Insurance revenue (by method)
- Insurance finance income/expense
- Significant judgments (methods, inputs, assumptions for estimating cash flows, discount rates, risk adjustment)
- Nature and extent of risks from insurance contracts (insurance risk, market risk, credit risk, liquidity risk)
- Effect of regulatory frameworks

**Common pitfalls:**
- Incorrect level of aggregation (cannot group contracts from different annual cohorts)
- Not identifying onerous groups at initial recognition
- Applying PAA to contracts that don't qualify
- Incorrect CSM allocation (choosing inappropriate coverage units)
- Not separating embedded derivatives or distinct investment/service components
- Mixing locked-in and current discount rates inappropriately between P&L and OCI

**Related standards:** IFRS 9 (financial instruments not in scope of IFRS 17), IFRS 13 (fair value concepts), IFRS 7 (some disclosure concepts)

---

## IAS 1 — Presentation of Financial Statements

**Scope:** General purpose financial statements prepared in accordance with IFRS.

**Core principle:** Financial statements provide a structured representation of the financial position, performance, and cash flows of an entity, with information useful for economic decision-making.

**Key rules:**
- Complete set: statement of financial position, statement of profit or loss and OCI, statement of changes in equity, statement of cash flows, notes (including accounting policies)
- Fair presentation and compliance with IFRS
- Going concern assessment required
- Accrual basis of accounting
- Materiality and aggregation: do not obscure material information
- Offsetting: not permitted unless required or permitted by another IFRS
- Comparative information: minimum one comparative period
- Current/non-current distinction for assets and liabilities (unless liquidity presentation is more relevant)
- Specific line items required on face of each statement; additional line items/headings when relevant

**Disclosure requirements:**
- Accounting policies (material policies, judgments in applying them)
- Sources of estimation uncertainty (key assumptions about the future with significant risk of material adjustment)
- Capital management
- Dividends
- Domicile, legal form, country of incorporation, registered office, nature of operations, name of parent

**Common pitfalls:**
- Inappropriate offsetting of assets and liabilities or income and expenses
- Not disclosing sources of estimation uncertainty
- Inadequate going concern assessment or disclosure
- Mixing OCI items that will be reclassified to P&L with those that won't

**Related standards:** IAS 8 (accounting policies/estimates), IAS 10 (events after reporting period), IAS 34 (interim reporting)

---

## IAS 2 — Inventories

**Scope:** All inventories except: work in progress from construction contracts (no longer relevant — use IFRS 15), financial instruments, biological assets at fair value less costs to sell (IAS 41).

**Core principle:** Inventories are measured at the lower of cost and net realisable value (NRV).

**Key rules:**
- Cost includes: purchase price, conversion costs (direct labor, systematic allocation of fixed and variable production overhead based on normal capacity), other costs to bring inventory to present location and condition
- Cost formulas: FIFO or weighted average. LIFO is not permitted.
- NRV: estimated selling price less estimated costs of completion and estimated costs to sell
- Write-down to NRV recognized as expense; reversal recognized as reduction of expense (limited to original write-down)
- Specific identification required for items not ordinarily interchangeable and goods/services produced for specific projects

**Disclosure requirements:**
- Accounting policies (cost formula)
- Total carrying amount and carrying amount by classification
- Carrying amount at fair value less costs to sell
- Amount of inventories recognized as expense
- Write-downs and reversals
- Carrying amount of inventories pledged as security

**Common pitfalls:**
- Using LIFO (not permitted under IFRS)
- Allocating fixed production overhead based on actual production instead of normal capacity
- Not writing down to NRV when cost exceeds NRV
- Including abnormal waste, storage costs, or administrative overhead in cost of inventory

**Related standards:** IAS 36 (if impairment concepts are confused with NRV), IFRS 15 (cost of inventories sold as revenue cost)

---

## IAS 7 — Statement of Cash Flows

**Scope:** All entities preparing financial statements under IFRS.

**Core principle:** Provide information about changes in cash and cash equivalents, classified by operating, investing, and financing activities.

**Key rules:**
- Cash equivalents: short-term (3 months or less from acquisition), highly liquid, readily convertible, insignificant risk of value change
- Operating activities: direct method (encouraged) or indirect method
- Investing activities: acquisition/disposal of long-term assets and investments
- Financing activities: changes in size/composition of equity and borrowings
- Interest and dividends: classify consistently period to period (operating or financing for interest paid; operating or investing for interest/dividends received; financing or operating for dividends paid)
- Income taxes: operating (unless specifically identified with financing/investing)
- Non-cash transactions: disclose but exclude from cash flow statement

**Disclosure requirements:**
- Components of cash and cash equivalents, reconciled to statement of financial position
- Reconciliation of liabilities arising from financing activities (IAS 7.44A-E)
- Significant non-cash transactions
- Restricted cash (if material)

**Common pitfalls:**
- Inconsistent classification of interest/dividends between periods
- Including non-cash transactions in the statement
- Incorrect classification of bank overdrafts (only include if integral part of cash management)
- Missing financing activities reconciliation

**Related standards:** IAS 1 (complete set of financial statements), IFRS 16 (lease payments classification)

---

## IAS 8 — Accounting Policies, Changes in Accounting Estimates and Errors

**Scope:** Selection and application of accounting policies, changes in policies, changes in estimates, and correction of prior period errors.

**Core principle:** Apply accounting policies consistently; changes in policy are applied retrospectively; changes in estimates are applied prospectively; prior period errors are corrected retrospectively.

**Key rules:**
- Accounting policy selection: follow specific IFRS; if no specific standard, use judgment (IAS 8 hierarchy: analogous IFRS, Conceptual Framework)
- Change in accounting policy: only if required by IFRS or results in more relevant/reliable information; apply retrospectively (restate comparatives) unless impracticable
- Change in accounting estimate: apply prospectively (current and future periods)
- Distinguishing policy change from estimate change: if uncertain, treat as change in estimate
- Prior period errors: correct retrospectively by restating comparatives; if impracticable for earliest period, adjust opening balances of earliest practicable period

**Disclosure requirements:**
- Policy changes: nature, reasons, amounts of adjustments for each line item, impact on EPS
- Estimate changes: nature and amount of change affecting current period, expected future effect (if practicable)
- Errors: nature, amounts of corrections for each line item, impact on EPS

**Common pitfalls:**
- Treating a change in estimate as a change in policy (or vice versa)
- Not restating comparatives for policy changes or error corrections
- Claiming impracticability without sufficient justification
- Applying prospective treatment to corrections of errors

**Related standards:** IAS 1 (presentation of accounting policies), IAS 10 (events after reporting period)

---

## IAS 10 — Events after the Reporting Period

**Scope:** Events occurring between the end of the reporting period and the date financial statements are authorized for issue.

**Core principle:** Adjust financial statements for events that provide evidence of conditions existing at the end of the reporting period (adjusting events); disclose but do not adjust for events indicative of conditions arising after the reporting period (non-adjusting events).

**Key rules:**
- Adjusting events: settlement of court case confirming obligation existed, bankruptcy of customer confirming loss existed, discovery of fraud or error, sale of inventory confirming NRV
- Non-adjusting events: decline in market value after reporting date, business combination, major restructuring plan announced, natural disaster, share transactions
- Going concern: if management determines after reporting period that entity will liquidate or cease trading, do not prepare on going concern basis
- Dividends: declared after reporting period are non-adjusting (disclose, do not recognize as liability)

**Disclosure requirements:**
- Date financial statements were authorized for issue and who authorized them
- For non-adjusting events: nature and financial effect estimate (or statement that estimate cannot be made)

**Common pitfalls:**
- Adjusting for events that are non-adjusting (e.g., post-year-end market decline)
- Not adjusting for events that are adjusting (e.g., resolution of contingency)
- Declaring dividend before year-end but board approval after — must assess timing carefully
- Not disclosing material non-adjusting events

**Related standards:** IAS 37 (provisions/contingencies), IAS 1 (going concern)

---

## IAS 12 — Income Taxes

**Scope:** All income taxes, including foreign taxes and withholding taxes. Also addresses deferred tax arising from temporary differences.

**Core principle:** Recognize current and deferred tax consequences of transactions, using the balance sheet liability method for deferred taxes.

**Key rules:**
- Current tax: amount payable/recoverable for the period based on taxable profit
- Deferred tax: arising from temporary differences between carrying amount and tax base
- Deferred tax liability (DTL): for all taxable temporary differences, except initial recognition exemption (not a business combination, affects neither accounting nor taxable profit), and investments in subsidiaries/associates/JVs if timing of reversal is controlled and not expected to reverse in foreseeable future
- Deferred tax asset (DTA): for deductible temporary differences, unused tax losses, and unused tax credits, to the extent probable that taxable profit will be available
- Measurement: enacted or substantively enacted tax rates expected to apply when the asset is realized or liability is settled; not discounted
- Uncertain tax treatments: IFRIC 23 — assess whether each uncertain position will be accepted by tax authority; if not, measure using most likely amount or expected value method

**Disclosure requirements:**
- Major components of tax expense
- Reconciliation of effective tax rate to applicable tax rate
- Deferred tax assets and liabilities by type of temporary difference
- Unrecognized DTAs (amount and expiry dates of losses)
- Tax-related contingent liabilities and contingent assets

**Common pitfalls:**
- Not recognizing DTA for tax losses when probable future profits exist
- Recognizing DTA when no probable future taxable profits
- Incorrect tax rate (using current rate instead of enacted rate for period of expected reversal)
- Failing to assess uncertain tax positions under IFRIC 23
- Not reassessing unrecognized DTAs at each reporting date

**Related standards:** IAS 1 (presentation), IAS 37 (contingencies vs. uncertain tax), IFRIC 23 (uncertain tax treatments)

---

## IAS 16 — Property, Plant and Equipment

**Scope:** Tangible assets held for use in production/supply of goods/services, rental, or administrative purposes and expected to be used during more than one period. Excludes biological assets (IAS 41), mineral rights and reserves (IFRS 6), and assets held for sale (IFRS 5).

**Core principle:** Recognize PP&E at cost when it is probable future economic benefits will flow to the entity and cost can be measured reliably. Subsequently measure using cost model or revaluation model.

**Key rules:**
- Cost: purchase price + directly attributable costs to bring asset to intended use + estimated dismantling/restoration costs (IAS 37)
- Subsequent costs: capitalize if meet recognition criteria; expense maintenance/repairs
- Depreciation: systematic allocation over useful life; component depreciation required for significant parts with different useful lives
- Depreciation methods: straight-line, diminishing balance, units of production (reflect pattern of benefit consumption)
- Revaluation model: carry at fair value less subsequent depreciation and impairment; revaluation surplus in OCI (recycled to retained earnings on disposal, not through P&L)
- Derecognition: on disposal or when no future economic benefits expected; gain/loss in P&L

**Disclosure requirements:**
- Measurement bases, depreciation methods, useful lives or depreciation rates
- Gross carrying amount and accumulated depreciation at start and end of period
- Reconciliation of carrying amount (additions, disposals, depreciation, impairment, revaluations, reclassifications)
- If revaluation model: effective date, whether independent valuer, carrying amount under cost model, revaluation surplus

**Common pitfalls:**
- Not componentizing assets with significantly different useful lives
- Capitalizing costs that do not meet recognition criteria (e.g., general overhead, training)
- Using a depreciation method that does not reflect the pattern of benefit consumption
- Not reviewing useful life and residual value at least annually
- Revaluation surplus: recycling through P&L instead of retained earnings

**Related standards:** IAS 36 (impairment), IAS 23 (borrowing costs), IAS 40 (investment property), IFRS 13 (fair value for revaluation model)

---

## IAS 19 — Employee Benefits

**Scope:** All employee benefits except share-based payment (IFRS 2).

**Core principle:** Recognize a liability when an employee has provided service in exchange for benefits to be paid in the future, and an expense when the entity consumes the economic benefit arising from service.

**Key rules:**
- **Short-term benefits** (expected to be settled within 12 months): recognize expense as employee renders service; accrue for compensated absences
- **Post-employment benefits — defined contribution:** expense = contributions payable for service rendered in period
- **Post-employment benefits — defined benefit:**
  - Net defined benefit liability/asset = present value of defined benefit obligation (DBO) - fair value of plan assets
  - DBO: projected unit credit method with actuarial assumptions (demographic and financial)
  - Service cost (current, past, settlements) in P&L
  - Net interest on net defined benefit liability/asset in P&L
  - Remeasurements (actuarial gains/losses, return on plan assets excluding net interest, asset ceiling effects) in OCI — never reclassified to P&L
  - Past service cost: recognize in P&L when plan is amended or curtailed
- **Other long-term benefits:** similar to defined benefit but remeasurements in P&L (not OCI)
- **Termination benefits:** recognize when entity can no longer withdraw offer or recognizes restructuring cost (IAS 37), whichever is earlier

**Disclosure requirements:**
- Characteristics of defined benefit plans and associated risks
- Amounts recognized in financial statements (DBO, plan assets, net liability/asset)
- Reconciliation of opening to closing balances
- Actuarial assumptions (sensitivity analysis for significant assumptions)
- Asset-liability matching strategies
- Effect on future cash flows (expected contributions, maturity profile)

**Common pitfalls:**
- Using discount rate that does not reflect high-quality corporate bonds (or government bonds where no deep market)
- Recognizing actuarial gains/losses in P&L instead of OCI for defined benefit plans
- Not recognizing past service cost immediately when plan is amended
- Confusing defined benefit and defined contribution classifications (substance over form)

**Related standards:** IFRS 2 (share-based payment), IAS 37 (termination benefits vs. restructuring provisions), IAS 26 (retirement benefit plan reporting)

---

## IAS 20 — Accounting for Government Grants and Disclosure of Government Assistance

**Scope:** Government grants and other forms of government assistance, except government assistance in the form of tax benefits (IAS 12), or participation in ownership (IAS 32).

**Core principle:** Recognize government grants when there is reasonable assurance the entity will comply with conditions and the grant will be received. Recognize in profit or loss on a systematic basis over the periods in which the entity recognizes the related costs.

**Key rules:**
- Grant related to assets: deduct from carrying amount of asset, or recognize as deferred income and release to P&L over useful life
- Grant related to income: present as income (separately or net against related expense), or deduct from related expense
- Repayment of grant: treat as change in accounting estimate (IAS 8); reverse deferred income or increase carrying amount of asset
- Non-monetary grants: measure at fair value (or nominal amount)
- Forgivable loans: treat as grant when reasonable assurance conditions will be met

**Disclosure requirements:**
- Accounting policy (presentation method)
- Nature and extent of grants recognized
- Unfulfilled conditions and contingencies
- Government assistance that does not meet grant recognition criteria

**Common pitfalls:**
- Recognizing grant before reasonable assurance exists
- Mismatch between grant income recognition and related expense recognition
- Not disclosing unfulfilled conditions

**Related standards:** IAS 12 (tax benefits), IAS 41 (agricultural grants at fair value)

---

## IAS 21 — The Effects of Changes in Foreign Exchange Rates

**Scope:** Translating foreign currency transactions and foreign operations into the entity's functional currency, and translating results into a presentation currency.

**Core principle:** Determine functional currency, translate foreign currency transactions at spot rate, and translate foreign operations using closing rate (assets/liabilities) and transaction date rate (income/expenses).

**Key rules:**
- Functional currency: primary economic environment in which entity operates (considers currency of sales, costs, financing)
- Foreign currency transactions: initial recognition at spot rate; at reporting date: monetary items at closing rate (exchange differences in P&L), non-monetary items at historical rate (unless measured at fair value — then rate at FV measurement date)
- Translation to presentation currency: assets/liabilities at closing rate; income/expenses at transaction date rates (average if reasonable approximation); resulting exchange differences in OCI (cumulative translation adjustment)
- Disposal of foreign operation: reclassify cumulative exchange differences from equity to P&L

**Disclosure requirements:**
- Exchange differences recognized in P&L and OCI
- Net exchange differences in separate component of equity, reconciliation
- Functional currency if different from presentation currency, and reason
- Change in functional currency and reason

**Common pitfalls:**
- Incorrectly determining functional currency (using presentation or parent currency instead of entity's own)
- Using average rate when exchange rate fluctuates significantly during the period
- Not reclassifying cumulative translation differences on disposal of foreign operation
- Translating goodwill and fair value adjustments from business combination at historical rate instead of closing rate

**Related standards:** IAS 29 (hyperinflationary economies), IFRS 9 (hedging foreign currency risk), IAS 12 (tax effects of exchange differences)

---

## IAS 23 — Borrowing Costs

**Scope:** Borrowing costs directly attributable to the acquisition, construction, or production of a qualifying asset.

**Core principle:** Capitalize borrowing costs directly attributable to qualifying assets as part of the cost of that asset. Expense all other borrowing costs.

**Key rules:**
- Qualifying asset: takes a substantial period of time to get ready for intended use or sale (e.g., inventory manufactured over extended period, manufacturing plants, power generation facilities, intangible assets, investment properties)
- Capitalize: borrowing costs that would have been avoided if expenditure on qualifying asset had not been made
- Specific borrowings: actual costs less investment income on temporary investment of those borrowings
- General borrowings: apply capitalization rate (weighted average of borrowing costs applicable to general borrowings outstanding during the period) to expenditures on the asset
- Begin: when expenditures are incurred, borrowing costs are incurred, and activities necessary to prepare asset for use/sale are in progress
- Suspend: during extended periods of inactivity in active development
- Cease: when substantially all activities necessary to prepare asset for intended use/sale are complete

**Disclosure requirements:**
- Amount of borrowing costs capitalized during the period
- Capitalization rate used

**Common pitfalls:**
- Capitalizing borrowing costs for assets that do not qualify (e.g., inventory produced in large quantities on a repetitive basis unless substantial period)
- Not suspending capitalization during extended periods of inactivity
- Using incorrect capitalization rate for general borrowings
- Continuing to capitalize after asset is substantially ready for use

**Related standards:** IAS 16 (PP&E cost), IAS 38 (intangible asset cost), IAS 2 (inventory cost), IAS 40 (investment property cost)

---

## IAS 24 — Related Party Disclosures

**Scope:** All entities preparing financial statements under IFRS.

**Core principle:** Disclose related party relationships and transactions to alert users that financial position and profit or loss may have been affected by such relationships.

**Key rules:**
- Related parties include: parent, subsidiaries, associates, JVs, key management personnel (KMP), close family members of KMP, entities controlled/jointly controlled/significantly influenced by KMP or their close family
- Transactions: transfer of resources/services/obligations regardless of whether a price is charged
- Government-related entities: partial exemption from disclosure (disclose name of government and nature of relationship, nature and amount of individually significant transactions, qualitative/quantitative indication of collectively significant transactions)

**Disclosure requirements:**
- Parent-subsidiary relationships (even if no transactions)
- KMP compensation (short-term, post-employment, other long-term, termination, share-based payment)
- Related party transactions: nature, amount, outstanding balances, terms, provisions for doubtful debts
- Cannot state transactions were at arm's length unless that can be substantiated

**Common pitfalls:**
- Incomplete identification of related parties (missing close family members, entities they control)
- Claiming arm's length terms without substantiation
- Missing KMP compensation disclosure categories
- Not disclosing parent-subsidiary relationship when there are no transactions

**Related standards:** IFRS 10 (control), IAS 28 (significant influence), IFRS 11 (joint control)

---

## IAS 27 — Separate Financial Statements

**Scope:** Entities that prepare separate financial statements (in addition to or instead of consolidated financial statements, if exempted from consolidation).

**Core principle:** In separate financial statements, investments in subsidiaries, joint ventures, and associates are accounted for at cost, in accordance with IFRS 9, or using the equity method.

**Key rules:**
- Choice of method: cost, IFRS 9 (fair value through profit or loss), or equity method — apply same method to each category of investment
- Dividends from subsidiaries/associates/JVs: recognized in P&L when right to receive is established
- If parent is exempt from preparing consolidated FS, separate FS may be the only FS

**Disclosure requirements:**
- List of significant investments (name, place, proportion of ownership, method used)
- Nature of relationship
- Reasons for using equity method in separate FS (if chosen)

**Common pitfalls:**
- Applying different methods within the same category of investment
- Confusing separate financial statements with consolidated financial statements

**Related standards:** IFRS 10 (consolidated FS), IAS 28 (equity method), IFRS 9 (financial instruments)

---

## IAS 28 — Investments in Associates and Joint Ventures

**Scope:** Investments where the entity has significant influence (associates) or joint control (joint ventures, per IFRS 11).

**Core principle:** Account for associates and joint ventures using the equity method, unless exemption applies.

**Key rules:**
- Significant influence: presumed if 20-50% of voting power; consider potential voting rights, board representation, participation in policy-making, material transactions, interchange of management, provision of essential technical information
- Equity method: initially at cost; adjust for post-acquisition share of profit/loss (P&L), OCI (OCI), and distributions (reduce carrying amount)
- Eliminate unrealized profits on upstream/downstream transactions (to extent of investor's interest)
- Losses: reduce carrying amount to zero; further losses recognized only if investor has legal or constructive obligation
- Impairment: apply IAS 36 to entire carrying amount (including goodwill)
- Loss of significant influence: derecognize at fair value; recognize gain/loss in P&L; reclassify OCI amounts

**Disclosure requirements:** See IFRS 12

**Common pitfalls:**
- Applying equity method when significant influence is lost
- Not eliminating unrealized intercompany profits
- Using different accounting policies between investor and investee without adjustment
- Misalignment of reporting dates (max 3 months difference)

**Related standards:** IFRS 11 (joint ventures), IFRS 12 (disclosures), IAS 36 (impairment), IFRS 10 (control vs. significant influence)

---

## IAS 32 — Financial Instruments: Presentation

**Scope:** Classification of financial instruments as financial assets, financial liabilities, or equity instruments; classification of related interest, dividends, losses, and gains; offsetting conditions.

**Core principle:** Classify financial instruments based on substance of contractual arrangement, not legal form. Distinguish liabilities (obligation to deliver cash or another financial asset) from equity (residual interest).

**Key rules:**
- Liability vs. equity: issuer has obligation to deliver cash/assets = liability; no such obligation = equity
- Puttable instruments classified as equity: specific narrow exception if lowest subordination class, identical features, no contractual obligation other than repurchase, total expected cash flows based substantially on P&L
- Compound instruments (e.g., convertible bonds): split into liability and equity components at issuance; liability = fair value of similar instrument without conversion option; equity = residual
- Treasury shares: deducted from equity; no gain/loss on purchase/sale/issue/cancellation recognized in P&L
- Offsetting: only when entity has legally enforceable right to set off AND intends to settle net or simultaneously

**Disclosure requirements:** See IFRS 7

**Common pitfalls:**
- Classifying mandatorily redeemable preference shares as equity instead of liability
- Not splitting compound instruments
- Offsetting without meeting both conditions (legal right AND intention)
- Recognizing gain/loss on treasury share transactions in P&L

**Related standards:** IFRS 9 (recognition/measurement), IFRS 7 (disclosures), IAS 1 (presentation)

---

## IAS 33 — Earnings Per Share

**Scope:** Entities whose ordinary shares or potential ordinary shares are traded in a public market, or that are in the process of filing for such.

**Core principle:** Present basic and diluted earnings per share for profit or loss from continuing operations and total profit or loss attributable to ordinary equity holders.

**Key rules:**
- Basic EPS: profit attributable to ordinary equity holders / weighted average number of ordinary shares outstanding
- Diluted EPS: adjust numerator for effects of dilutive potential ordinary shares; adjust denominator for shares that would be issued on conversion
- Dilutive instruments: options/warrants (treasury stock method), convertible instruments (if converted method), contingently issuable shares
- Anti-dilutive: exclude from diluted EPS calculation (they would increase EPS or decrease loss per share)
- Bonus issues and share splits: retrospective adjustment of all periods presented

**Disclosure requirements:**
- Numerators and denominators for basic and diluted EPS, with reconciliation to reported profit
- Instruments excluded from diluted EPS because anti-dilutive but could become dilutive
- Transactions after reporting period that would significantly change share count

**Common pitfalls:**
- Including anti-dilutive instruments in diluted EPS
- Not adjusting retroactively for bonus issues/splits
- Incorrect weighted average calculation for shares issued/repurchased mid-period
- Not presenting EPS for discontinued operations

**Related standards:** IAS 1 (presentation), IFRS 5 (discontinued operations EPS)

---

## IAS 36 — Impairment of Assets

**Scope:** All assets except inventories (IAS 2), contract assets (IFRS 15), deferred tax (IAS 12), employee benefits (IAS 19), financial assets (IFRS 9), investment property at fair value (IAS 40), biological assets at fair value (IAS 41), insurance contract assets (IFRS 17), non-current assets held for sale (IFRS 5).

**Core principle:** An asset is impaired when its carrying amount exceeds its recoverable amount. Recoverable amount is the higher of fair value less costs of disposal and value in use.

**Key rules:**
- Assess at each reporting date whether any indication of impairment exists (external and internal indicators)
- Regardless of indication: test annually for goodwill, indefinite-life intangibles, and intangibles not yet available for use
- Cash-generating unit (CGU): smallest identifiable group of assets that generates cash inflows largely independent of other assets
- Goodwill: allocate to CGU or group of CGUs expected to benefit from the combination; test CGU including goodwill
- Value in use: present value of future cash flows expected from the asset, using pre-tax discount rate reflecting current market assessments of time value of money and risks specific to the asset
- Impairment loss: reduce carrying amount to recoverable amount; allocate to CGU by reducing goodwill first, then other assets pro rata
- Reversal: permitted for assets other than goodwill, up to carrying amount that would have been determined (net of depreciation) had no impairment been recognized

**Disclosure requirements:**
- Impairment losses and reversals by class of asset and segment
- For material impairments: events and circumstances, recoverable amount, basis (FVLCOD or VIU)
- For CGUs with significant goodwill/indefinite-life intangibles: carrying amount of goodwill, basis of recoverable amount, key assumptions, sensitivity/headroom

**Common pitfalls:**
- Not testing goodwill annually regardless of indicators
- Using post-tax discount rate instead of pre-tax
- Including future restructuring or asset enhancement cash flows in VIU
- Reversing impairment losses on goodwill
- Incorrect CGU identification (too large or too small)
- Not disclosing key assumptions and sensitivity for goodwill impairment testing

**Related standards:** IFRS 3 (goodwill from business combinations), IAS 38 (intangible assets), IAS 16 (PP&E), IFRS 13 (fair value for FVLCOD)

---

## IAS 37 — Provisions, Contingent Liabilities and Contingent Assets

**Scope:** Provisions, contingent liabilities, and contingent assets, except those arising from executory contracts (unless onerous), or covered by another standard (e.g., income taxes, leases, employee benefits, insurance contracts).

**Core principle:** Recognize a provision when entity has a present obligation from a past event, it is probable an outflow of economic resources will be required, and a reliable estimate can be made. Disclose contingent liabilities. Do not recognize contingent assets (disclose if probable).

**Key rules:**
- Provision: best estimate of expenditure required to settle at reporting date
- Discount to present value if time value of money is material (pre-tax rate reflecting current market assessments)
- Restructuring provisions: only when entity has detailed formal plan and raised valid expectation in those affected
- Onerous contracts: unavoidable costs of meeting obligations exceed economic benefits expected; recognize provision for net cost (lower of cost of fulfilling and any compensation/penalties for failing to fulfill)
- Reimbursements: recognize as separate asset (not offset) when virtually certain
- Review provisions at each reporting date; adjust to current best estimate

**Disclosure requirements:**
- For each class of provision: carrying amount reconciliation, nature, timing, uncertainties, reimbursement
- For contingent liabilities: nature, estimate of financial effect, uncertainties, reimbursement possibility
- For contingent assets: nature, estimated financial effect

**Common pitfalls:**
- Recognizing provision without present obligation (e.g., future operating losses)
- Restructuring: recognizing before formal plan and valid expectation exist
- Not discounting long-term provisions
- Recognizing contingent assets or not disclosing contingent liabilities

**Related standards:** IAS 10 (events after reporting period), IFRS 15 (onerous contract interaction), IAS 19 (employee-related provisions)

---

## IAS 38 — Intangible Assets

**Scope:** Intangible assets except financial assets (IFRS 9), mineral rights (IFRS 6), intangible assets from insurance contracts (IFRS 17), goodwill from business combinations (IFRS 3), and intangible assets covered by other standards.

**Core principle:** Recognize an intangible asset when it is identifiable, entity has control, and future economic benefits are probable. Measure initially at cost.

**Key rules:**
- Identifiable: separable (can be sold, transferred, licensed) OR arises from contractual/legal rights
- Internally generated intangibles: research phase costs expensed; development costs capitalized when ALL six criteria met (technical feasibility, intention to complete, ability to use/sell, probable future benefits, adequate resources, reliable measurement of cost)
- Internally generated brands, mastheads, publishing titles, customer lists: never recognized (cannot be distinguished from cost of developing business as a whole)
- Subsequent measurement: cost model or revaluation model (only if active market exists — rare for intangibles)
- Useful life: finite (amortize over useful life) or indefinite (do not amortize; test annually for impairment)
- Amortization: begin when asset is available for use; method reflects pattern of benefit consumption (straight-line if cannot determine)

**Disclosure requirements:**
- Finite vs. indefinite life: useful lives/amortization rates, amortization methods, gross carrying amount and accumulated amortization
- Reconciliation of carrying amount
- Research and development expenditure recognized as expense
- Intangible assets with indefinite useful life: carrying amount, reasons for indefinite assessment
- Restrictions on title, pledged as security

**Common pitfalls:**
- Capitalizing research costs
- Capitalizing development costs before all six criteria are met
- Attempting to recognize internally generated goodwill, brands, or customer lists
- Using revaluation model without an active market
- Not reviewing useful life assessment annually for indefinite-life intangibles

**Related standards:** IFRS 3 (intangibles acquired in business combination), IAS 36 (impairment), IAS 16 (tangible vs. intangible distinction)

---

## IAS 40 — Investment Property

**Scope:** Property held to earn rentals or for capital appreciation (or both), rather than for use in production/supply/administration (IAS 16) or sale in ordinary course of business (IAS 2).

**Core principle:** Recognize investment property when probable future economic benefits will flow and cost can be measured reliably. Subsequently measure using either cost model or fair value model (choice applied to all investment property).

**Key rules:**
- Classification: property held for rental income, capital appreciation, or both; if partly owner-occupied, investment property only if owner-occupied portion is insignificant (or can be sold/leased separately)
- Initial measurement: cost (including transaction costs)
- Fair value model: measure at fair value at each reporting date; changes in fair value in P&L; no depreciation
- Cost model: IAS 16 applies (depreciate; impairment per IAS 36); disclose fair value
- Transfers: to/from investment property when there is a change in use; from fair value to owner-occupied: deemed cost = fair value at date of change; from owner-occupied to fair value: treat difference per IAS 16 revaluation rules

**Disclosure requirements:**
- Whether fair value or cost model
- If fair value model: methods and significant assumptions, extent of independent valuation, amounts recognized in P&L, reconciliation of carrying amounts
- If cost model: depreciation methods and useful lives, reconciliation, fair value disclosure (or state why not determinable)

**Common pitfalls:**
- Mixing cost and fair value models for different investment properties
- Classifying owner-occupied property as investment property
- Not recognizing fair value changes in P&L under fair value model
- Missing fair value disclosure when using cost model

**Related standards:** IAS 16 (owner-occupied property), IFRS 13 (fair value measurement), IFRS 16 (ROU asset as investment property), IAS 36 (impairment under cost model)

---

## IAS 41 — Agriculture

**Scope:** Biological assets (living animals and plants), agricultural produce at the point of harvest, and government grants related to biological assets.

**Core principle:** Measure biological assets at fair value less costs to sell at each reporting date (unless fair value cannot be measured reliably on initial recognition). Recognize changes in fair value less costs to sell in profit or loss.

**Key rules:**
- Biological asset: living animal or plant managed for sale, agricultural produce, or additional biological assets
- Agricultural produce: harvested product; measured at fair value less costs to sell at point of harvest; this becomes cost for IAS 2 purposes
- Government grants: unconditional grant recognized when receivable; conditional grant recognized when conditions are met
- Inability to measure fair value reliably: only on initial recognition; measure at cost less accumulated depreciation and impairment; once fair value becomes reliably measurable, use FVLCS until disposal

**Disclosure requirements:**
- Nature of activities
- Aggregate gain or loss from initial recognition and changes in FV
- Description of each group of biological assets (quantitative, consumable vs. bearer, mature vs. immature)
- Methods and assumptions for determining fair value
- Reconciliation of carrying amounts

**Common pitfalls:**
- Not recognizing fair value changes in P&L
- Measuring agricultural produce at fair value beyond the point of harvest (IAS 2 applies after harvest)
- Not distinguishing bearer plants (IAS 16) from other biological assets

**Related standards:** IAS 16 (bearer plants), IAS 2 (agricultural produce after harvest), IAS 20 (government grants), IFRS 13 (fair value measurement)
```

- [ ] **Step 2: Verify the file was created and check approximate length**

```bash
wc -l ~/.claude/skills/ifrs/standards-reference.md
```

Expected: a large file (likely 800+ lines).

- [ ] **Step 3: Spot-check searchability — verify searching for "IFRS 15" finds the right section**

```bash
grep -n "## IFRS 15" ~/.claude/skills/ifrs/standards-reference.md
```

Expected: one match pointing to the IFRS 15 section header.

- [ ] **Step 4: Commit**

```bash
git add ~/.claude/skills/ifrs/standards-reference.md
git commit -m "feat: add IFRS standards reference (IFRS 1-17, IAS 1-41)"
```

---

## Task 3: Write Workflows (`workflows.md`)

**Files:**
- Create: `~/.claude/skills/ifrs/workflows.md`

Step-by-step procedures for the five core workflow areas: revenue recognition (IFRS 15), lease accounting (IFRS 16), impairment testing (IAS 36), financial instruments (IFRS 9), and first-time adoption (IFRS 1). Each workflow includes detailed substeps with decision points, examples, and journal entry guidance.

- [ ] **Step 1: Write `workflows.md`**

Create `~/.claude/skills/ifrs/workflows.md` with the following content:

```markdown
# IFRS Workflows

Step-by-step procedures for complex IFRS tasks. Each workflow includes decision points, key judgments, and example journal entries.

---

## Revenue Recognition (IFRS 15) — 5-Step Model

### Step 1: Identify the Contract

A contract exists when ALL criteria are met:
- Parties have approved the contract and are committed to their obligations
- Each party's rights regarding goods/services can be identified
- Payment terms can be identified
- Contract has commercial substance
- Probable that entity will collect consideration

**Key judgments:**
- Combine contracts if negotiated as a package, consideration in one depends on the other, or goods/services are a single performance obligation
- Contract modifications: assess whether to treat as separate contract or modification of existing

### Step 2: Identify Performance Obligations

A performance obligation is a promise to transfer a distinct good or service (or a series of distinct goods/services that are substantially the same and have the same pattern of transfer).

**Distinct test — BOTH conditions must be met:**
1. Customer can benefit from good/service on its own or with readily available resources (capable of being distinct)
2. Promise is separately identifiable from other promises in the contract (distinct within the context of the contract)

**Indicators that promises are NOT separately identifiable:**
- Entity provides significant integration service
- Good/service significantly modifies or customizes another
- Goods/services are highly interdependent or interrelated

### Step 3: Determine Transaction Price

Transaction price = amount of consideration the entity expects to be entitled to.

**Include:**
- Fixed consideration
- Variable consideration (constrained — include only to extent highly probable no significant reversal)
  - Methods: expected value (probability-weighted) or most likely amount
- Significant financing component (adjust if > 12 months between payment and transfer; practical expedient if <= 12 months)
- Non-cash consideration (fair value)
- Consideration payable to customer (reduce transaction price, unless payment for distinct good/service)

### Step 4: Allocate Transaction Price

Allocate to each performance obligation based on relative standalone selling prices (SSP).

**Determining SSP:**
1. Observable price (best evidence)
2. If not directly observable:
   - Adjusted market assessment approach
   - Expected cost plus margin approach
   - Residual approach (only if highly variable or uncertain SSP)

**Discount allocation:** allocate entirely to one or more (but not all) performance obligations only if specific criteria met.

**Variable consideration allocation:** allocate entirely to specific performance obligation if variable payment relates specifically to that obligation AND allocation is consistent with overall allocation objective.

### Step 5: Recognize Revenue

**Over time — if ANY ONE criterion met:**
1. Customer simultaneously receives and consumes benefits (e.g., routine services)
2. Entity's performance creates or enhances customer-controlled asset (e.g., building on customer's land)
3. Entity's performance does not create asset with alternative use AND entity has enforceable right to payment for performance to date (e.g., custom manufacturing)

**Measure progress over time:**
- Output methods: surveys, milestones, units delivered, time elapsed
- Input methods: costs incurred, labor hours, machine hours, time elapsed
- Choose method that best depicts transfer of control

**Point in time — if none of the over-time criteria are met.** Indicators of transfer of control:
- Entity has present right to payment
- Customer has legal title
- Entity has transferred physical possession
- Customer has significant risks and rewards of ownership
- Customer has accepted the asset

### Example Journal Entries

**Point-in-time recognition:**
```
Dr  Trade Receivable / Cash          XXX
  Cr  Revenue                           XXX
  Cr  Contract Liability (if advance)   XXX
```

**Over-time recognition (progress billing):**
```
Dr  Contract Asset                    XXX
  Cr  Revenue                           XXX

Dr  Cash / Trade Receivable           XXX
  Cr  Contract Asset                    XXX
```

---

## Lease Accounting (IFRS 16)

### Step 1: Identify Whether Arrangement Contains a Lease

A contract contains a lease if it conveys the right to control the use of an identified asset for a period of time in exchange for consideration.

**Identified asset:**
- Explicitly or implicitly specified in the contract
- Supplier does NOT have substantive right to substitute the asset

**Right to control use:**
- Customer has right to obtain substantially all economic benefits from use
- Customer has right to direct the use (decide how and for what purpose asset is used throughout the period of use)

### Step 2: Separate Lease and Non-Lease Components

- Allocate consideration based on relative standalone prices
- Practical expedient: lessee may elect (by class of underlying asset) not to separate and account for entire contract as a lease

### Step 3: Determine Lease Term

Lease term = non-cancellable period + periods covered by extension option (if reasonably certain to exercise) + periods covered by termination option (if reasonably certain NOT to exercise).

**Factors for "reasonably certain":**
- Contractual terms (penalties, bargain options)
- Significant leasehold improvements
- Costs relating to termination (relocation, disruption)
- Importance of underlying asset to lessee's operations
- Conditionality (wide vs. narrow conditions)

### Step 4: Lessee — Initial Measurement

**Lease liability = present value of:**
- Fixed payments (less any lease incentives receivable)
- Variable payments that depend on an index or rate (using index/rate at commencement)
- Amounts expected to be payable under residual value guarantees
- Exercise price of purchase option (if reasonably certain)
- Penalties for terminating the lease (if lease term reflects exercise of termination option)

**Discount rate:** rate implicit in the lease; if not readily determinable, lessee's incremental borrowing rate

**ROU asset = lease liability + initial direct costs + prepaid lease payments - lease incentives received + estimated costs of dismantling/restoration**

### Step 5: Lessee — Subsequent Measurement

**Lease liability:**
- Increase for interest (effective interest method)
- Decrease for lease payments made
- Remeasure for lease modifications, revised assessments of options, changes in index/rate

**ROU asset:**
- Depreciate over shorter of useful life and lease term (unless transfer of ownership or purchase option reasonably certain — then useful life)
- Impairment per IAS 36

**Exemptions (expense on straight-line basis or other systematic basis):**
- Short-term leases (12 months or less, no purchase option)
- Low-value assets (~US$5,000 or less when new)

### Step 6: Lessor Classification

**Finance lease — if arrangement transfers substantially all risks and rewards. Indicators:**
- Transfer of ownership by end of lease term
- Bargain purchase option
- Lease term is for major part of economic life
- PV of lease payments amounts to substantially all of fair value
- Specialized asset with no alternative use without major modification

**Operating lease** — all other leases

### Example Journal Entries

**Lessee initial recognition:**
```
Dr  Right-of-Use Asset                XXX
  Cr  Lease Liability                    XXX
```

**Lessee subsequent (each period):**
```
Dr  Interest Expense                   XXX
Dr  Lease Liability                    XXX
  Cr  Cash (lease payment)               XXX

Dr  Depreciation Expense               XXX
  Cr  Accumulated Depreciation — ROU     XXX
```

---

## Impairment Testing (IAS 36)

### Step 1: Identify Indicators of Impairment

**External indicators:**
- Significant decline in market value beyond normal wear
- Significant adverse changes in technological, market, economic, or legal environment
- Increase in market interest rates or discount rates
- Carrying amount of net assets exceeds market capitalization

**Internal indicators:**
- Evidence of obsolescence or physical damage
- Significant adverse changes in extent or manner of use (idle, discontinuation, restructuring)
- Internal reporting indicates asset's economic performance is or will be worse than expected

**No indicators needed for:** goodwill, indefinite-life intangibles, intangibles not yet available for use — test annually.

### Step 2: Determine Recoverable Amount

**Recoverable amount = higher of:**
- Fair value less costs of disposal (FVLCOD)
- Value in use (VIU)

If either exceeds carrying amount, no impairment — no need to calculate both.

**Fair value less costs of disposal:**
- IFRS 13 fair value hierarchy applies
- Deduct incremental costs directly attributable to disposal (legal fees, stamp duty, costs of removing asset — NOT reorganization or workforce reduction)

**Value in use:**
- Estimate future cash flows from continuing use and ultimate disposal
- Cash flows based on most recent budgets/forecasts (maximum 5 years; extrapolate beyond using steady or declining growth rate)
- Pre-tax cash flows, pre-tax discount rate
- Exclude: future restructuring not committed to, future capital expenditure that will enhance the asset
- Include: cash flows to maintain current service potential, proceeds from disposal

### Step 3: Compare Carrying Amount to Recoverable Amount

- If carrying amount > recoverable amount → impairment loss = difference
- If carrying amount <= recoverable amount → no impairment

### Step 4: Recognize Impairment Loss

**Individual asset:**
```
Dr  Impairment Loss (P&L)             XXX
  Cr  Asset (carrying amount)            XXX
```
(If revalued asset: reduce revaluation surplus first, excess to P&L)

**CGU allocation order:**
1. Reduce goodwill allocated to the CGU to zero
2. Reduce other assets of the CGU pro rata based on carrying amounts
3. Do not reduce any asset below the highest of: FVLCOD, VIU, or zero

### Step 5: Assess Reversal (Subsequent Periods)

- Reversal permitted for all assets except goodwill
- Increase carrying amount to recoverable amount, but not above the carrying amount that would have been determined (net of depreciation) had no impairment been recognized
- Reversal recognized in P&L (or revaluation surplus if previously revalued)

---

## Financial Instruments (IFRS 9)

### Step 1: Classification of Financial Assets

**Decision tree:**

1. Is the asset a derivative? → FVTPL (unless designated hedging instrument)
2. Is the asset an equity investment?
   - Held for trading → FVTPL
   - Not held for trading → FVTPL (default) or irrevocable election for FVOCI (no recycling)
3. Is the asset a debt instrument?
   - Does it pass the SPPI test (solely payments of principal and interest)?
     - No → FVTPL
     - Yes → What is the business model?
       - Hold to collect → Amortised cost
       - Hold to collect and sell → FVOCI (with recycling)
       - Other → FVTPL
   - Fair value option available if eliminates accounting mismatch

**SPPI test:**
- Principal = fair value at initial recognition
- Interest = consideration for time value of money, credit risk, other basic lending risks, and a profit margin
- Features that fail: leverage features, non-recourse features beyond the asset, equity conversion features

### Step 2: Classification of Financial Liabilities

- Default: amortised cost
- FVTPL: held for trading or designated (fair value option)
- If fair value option: own credit risk changes in OCI (not P&L), unless creates accounting mismatch

### Step 3: Expected Credit Loss (ECL) Impairment

**General approach (3-stage model):**

| Stage | Trigger | ECL Measurement | Interest Revenue |
|-------|---------|-----------------|-----------------|
| 1 | Initial recognition (performing) | 12-month ECL | Gross carrying amount |
| 2 | Significant increase in credit risk since initial recognition | Lifetime ECL | Gross carrying amount |
| 3 | Credit-impaired | Lifetime ECL | Amortised cost (net of loss allowance) |

**Significant increase in credit risk (SICR) indicators:**
- Significant change in external/internal credit rating
- Existing or forecast adverse changes in business, financial, or economic conditions
- Significant change in operating results
- Payment is more than 30 days past due (rebuttable presumption)

**Default definition:** payment more than 90 days past due (rebuttable presumption)

**Simplified approach (mandatory for trade receivables without significant financing component; optional for trade receivables with significant financing component, contract assets, and lease receivables):**
- Always recognize lifetime ECL
- Provision matrix (based on historical loss rates, adjusted for forward-looking information)

### Step 4: Hedge Accounting (Optional)

**Types:**
- Fair value hedge: changes in FV of hedged item and hedging instrument both in P&L
- Cash flow hedge: effective portion of hedging instrument changes in OCI; reclassify to P&L when hedged item affects P&L
- Net investment hedge: similar to cash flow hedge for foreign currency risk on net investment

**Qualifying criteria:**
1. Formal designation and documentation at inception (risk management objective, hedging strategy, hedged item, hedging instrument, how effectiveness will be assessed)
2. Hedge effectiveness requirements:
   - Economic relationship between hedged item and hedging instrument
   - Credit risk does not dominate value changes
   - Hedge ratio consistent with risk management

**Discontinuation:** only when hedging relationship no longer meets qualifying criteria (after rebalancing)

---

## First-Time Adoption of IFRS (IFRS 1)

### Step 1: Identify Key Dates

- **Date of transition:** beginning of the earliest comparative period presented in the first IFRS financial statements
- **Reporting date:** end of the first IFRS reporting period
- Example: first IFRS FS for year ending 31 Dec 2026 with one year comparatives → date of transition = 1 Jan 2025

### Step 2: Prepare Opening IFRS Statement of Financial Position

At the date of transition:
- Recognize all assets and liabilities required by IFRS
- Derecognize assets and liabilities not permitted by IFRS
- Reclassify items as required by IFRS
- Measure all recognized assets and liabilities in accordance with IFRS
- Adjustments to retained earnings (or other equity category)

### Step 3: Apply Mandatory Exceptions

These are NOT optional — entity must apply them:
- Estimates: use estimates consistent with those under previous GAAP (unless evidence of error); do not use hindsight
- Derecognition of financial assets/liabilities: apply IFRS 9 derecognition prospectively
- Hedge accounting: apply IFRS 9 hedge accounting from transition date; do not retrospectively designate hedges
- Non-controlling interests: apply IFRS 10 requirements prospectively
- Classification and measurement of financial assets: assess based on facts at date of transition
- Embedded derivatives: assess based on conditions at date of transition (or when terms last modified, if later)
- Government loans: apply IFRS 9 and IAS 20 prospectively

### Step 4: Consider Optional Exemptions

Entity may elect (not exhaustive):
- **Business combinations:** not restate combinations before date of transition
- **Share-based payment:** not apply IFRS 2 to instruments granted before 7 Nov 2002 (or later dates)
- **Insurance contracts:** apply IFRS 17 transition provisions
- **Deemed cost:** use fair value at date of transition as deemed cost for PP&E, intangibles, investment property, or ROU assets
- **Leases:** apply IFRS 16 from date of transition using practical expedients
- **Cumulative translation differences:** reset to zero at date of transition
- **Compound financial instruments:** do not split if liability component no longer outstanding
- **Borrowing costs:** apply IAS 23 prospectively from date of transition (or earlier elected date)
- **Joint arrangements:** apply IFRS 11 from date of transition

### Step 5: Prepare Reconciliations

**Required reconciliations:**
1. Equity at date of transition (previous GAAP to IFRS)
2. Equity at end of last period reported under previous GAAP
3. Total comprehensive income for last period reported under previous GAAP

**Format:**
| Item | Previous GAAP | IFRS Adjustment | IFRS |
|------|---------------|-----------------|------|
| [Line item] | XXX | XXX | XXX |

Explain nature of material adjustments.

### Step 6: Disclosure Requirements

- Explanation of how transition from previous GAAP to IFRS affected reported financial position, performance, and cash flows
- Reconciliations with sufficient detail to understand material adjustments
- If entity recognized or reversed impairment losses for the first time in preparing opening IFRS statement, disclose as if IAS 36 required
- Fair values used as deemed cost: aggregate amount and aggregate adjustment to carrying amounts under previous GAAP
```

- [ ] **Step 2: Verify the file was created**

```bash
wc -l ~/.claude/skills/ifrs/workflows.md
```

- [ ] **Step 3: Commit**

```bash
git add ~/.claude/skills/ifrs/workflows.md
git commit -m "feat: add IFRS workflows (IFRS 15, 16, IAS 36, IFRS 9, IFRS 1)"
```

---

## Task 4: Write Compliance Templates (`compliance-templates.md`)

**Files:**
- Create: `~/.claude/skills/ifrs/compliance-templates.md`

Structured output templates for compliance/audit tasks: disclosure completeness checklist, gap analysis template, and audit memo format.

- [ ] **Step 1: Write `compliance-templates.md`**

Create `~/.claude/skills/ifrs/compliance-templates.md` with the following content:

```markdown
# IFRS Compliance Templates

Structured output formats for compliance checks, audit support, and gap analysis. Use these templates when the user requests a compliance review, audit memo, or structured deliverable.

---

## Disclosure Completeness Checklist

Use this format to check whether financial statements include all required disclosures for a given IFRS standard. Generate one checklist per standard being assessed.

### Template

**Standard: [IFRS/IAS X — Name]**
**Entity: [Name]**
**Reporting Period: [Date]**
**Prepared by: [Name/AI-assisted]**
**Date of Review: [Date]**

| # | Disclosure Requirement | Paragraph Ref | Included | Notes |
|---|----------------------|---------------|----------|-------|
| 1 | [Specific disclosure requirement] | [X.XX] | Yes / No / N/A | [Observation] |
| 2 | [Specific disclosure requirement] | [X.XX] | Yes / No / N/A | [Observation] |
| ... | ... | ... | ... | ... |

**Summary:**
- Total requirements assessed: [N]
- Included: [N]
- Missing: [N]
- Not applicable: [N]

**Key gaps identified:**
1. [Description of missing disclosure and recommendation]

### Example: IFRS 16 Lessee Disclosures

**Standard: IFRS 16 — Leases (Lessee Disclosures)**

| # | Disclosure Requirement | Paragraph Ref | Included | Notes |
|---|----------------------|---------------|----------|-------|
| 1 | Depreciation charge for ROU assets by class of underlying asset | 53(a) | | |
| 2 | Interest expense on lease liabilities | 53(b) | | |
| 3 | Expense relating to short-term leases | 53(c) | | |
| 4 | Expense relating to leases of low-value assets | 53(d) | | |
| 5 | Expense relating to variable lease payments not included in lease liabilities | 53(e) | | |
| 6 | Income from subleasing ROU assets | 53(f) | | |
| 7 | Total cash outflow for leases | 53(g) | | |
| 8 | Additions to ROU assets | 53(h) | | |
| 9 | Gains or losses from sale and leaseback transactions | 53(i) | | |
| 10 | Carrying amount of ROU assets at end of period by class | 53(j) | | |
| 11 | Maturity analysis of lease liabilities (separate from other financial liabilities) | 58 | | |
| 12 | Significant judgments about extension/termination options | 59(b) | | |

---

## Gap Analysis Template

Use this format to assess the gap between current accounting treatment and IFRS requirements, typically for transition projects or compliance remediation.

### Template

**Entity: [Name]**
**Assessment Date: [Date]**
**Scope: [Standards or areas covered]**
**Current Framework: [Previous GAAP / Current Practice]**

| # | Area / Topic | Current Treatment | IFRS Requirement | Standard Ref | Gap Description | Impact (H/M/L) | Action Required | Priority | Status |
|---|-------------|-------------------|-------------------|-------------|-----------------|-----------------|-----------------|----------|--------|
| 1 | [Area] | [Current practice] | [IFRS requirement] | [Ref] | [What needs to change] | [H/M/L] | [Specific action] | [1-5] | [Open/In Progress/Resolved] |

**Impact scale:**
- **H (High):** Material impact on financial statements; affects key metrics or regulatory compliance
- **M (Medium):** Moderate impact; requires policy change or system update but not material to overall position
- **L (Low):** Minor impact; disclosure enhancement or presentational change

**Summary of findings:**
- Total gaps identified: [N]
- High impact: [N]
- Medium impact: [N]
- Low impact: [N]

**Recommended implementation sequence:**
1. [Highest priority gap and rationale]
2. [Next priority]
3. ...

### Example: Lease Accounting Gap Analysis (Local GAAP to IFRS 16)

| # | Area | Current Treatment | IFRS Requirement | Ref | Gap | Impact | Action | Priority | Status |
|---|------|-------------------|-------------------|-----|-----|--------|--------|----------|--------|
| 1 | Operating leases — lessee | Off-balance sheet; rent expense on straight-line basis | Recognize ROU asset and lease liability for all leases (except short-term and low-value) | IFRS 16.22-28 | All operating leases must come on balance sheet | H | Identify all lease contracts; calculate ROU assets and lease liabilities; determine discount rates | 1 | Open |
| 2 | Discount rate | N/A (no discounting) | Discount lease payments using rate implicit in lease or incremental borrowing rate | IFRS 16.26 | Need to determine IBR for each lease | M | Establish IBR methodology; consider currency, term, credit standing | 2 | Open |
| 3 | Lease term | Contract term only | Include extension/termination options if reasonably certain | IFRS 16.18-21 | Must assess options for each lease | M | Review each lease for renewal/termination options; document assessment | 2 | Open |
| 4 | Disclosures | Minimal lease disclosures | Extensive lessee disclosures (ROU assets, interest, depreciation, maturity analysis, etc.) | IFRS 16.47-60 | Significant additional disclosures required | M | Design disclosure templates; set up data collection | 3 | Open |

---

## Audit Memo Format

Use this format for documenting the assessment of a specific accounting issue, transaction, or balance against IFRS requirements. Suitable for audit working papers, technical accounting memos, or position papers.

### Template

**ACCOUNTING ISSUE MEMO**

**Entity:** [Name]
**Prepared by:** [Name/AI-assisted]
**Date:** [Date]
**Reviewed by:** [Name]
**Review Date:** [Date]

---

**1. Issue**
[Clear, concise description of the accounting question or transaction being assessed. What decision needs to be made?]

**2. Applicable Standards**
- Primary: [IFRS/IAS X — Name, specific paragraphs]
- Secondary: [Other relevant standards]
- Interpretations: [IFRIC/SIC if applicable]

**3. Facts and Circumstances**
[Relevant facts about the transaction or arrangement. Include:
- Nature and terms
- Key dates
- Amounts involved
- Parties involved
- Contractual terms and conditions
- Business rationale]

**4. Analysis**

**[Sub-issue A: First key question]**
[Analysis applying the relevant IFRS requirements to the facts. Reference specific paragraphs. Consider alternatives if judgment is required.]

**[Sub-issue B: Second key question]**
[Continue for each significant judgment area.]

**5. Conclusion**
[Clear statement of the accounting treatment:
- **Compliant** — current treatment is consistent with IFRS
- **Non-compliant** — current treatment does not meet IFRS requirements; adjustment required
- **Judgment required** — IFRS permits alternative treatments; recommended approach with rationale]

**6. Journal Entry Impact** (if applicable)
```
Dr  [Account]     XXX
  Cr  [Account]     XXX
```
[Explanation of amounts and basis for measurement]

**7. Disclosure Impact**
[What disclosures are required as a result of this assessment?]

**8. Recommendation**
[Specific action items:
1. [Action]
2. [Action]
3. [Action]]

### Example: Revenue Recognition for Multi-Element Software Arrangement

**ACCOUNTING ISSUE MEMO**

**Entity:** TechCo Ltd
**Prepared by:** AI-assisted
**Date:** 2026-03-29

---

**1. Issue**
TechCo sells a bundled software package consisting of a perpetual license, 12 months of post-contract support (PCS), and implementation services for a total fee of $500,000. How should revenue be recognized under IFRS 15?

**2. Applicable Standards**
- Primary: IFRS 15 — Revenue from Contracts with Customers (paras 22-30 for performance obligations, paras 47-72 for transaction price allocation, paras 31-45 for recognition)
- Secondary: IFRS 15.B52-B63B (licensing guidance)

**3. Facts and Circumstances**
- Single contract for $500,000
- Perpetual software license delivered on day 1
- Implementation services over 3 months (not highly customized; software is functional without them)
- PCS for 12 months from go-live (bug fixes, minor updates, helpdesk)
- Observable standalone selling prices: license $300,000, implementation $75,000, PCS $125,000

**4. Analysis**

**Performance obligations:**
- Software license: distinct (customer can benefit from license on its own; implementation is not highly customized)
- Implementation services: distinct (available from third parties; does not significantly modify the software)
- PCS: distinct (provides ongoing service separate from license)
- Conclusion: three separate performance obligations

**Transaction price allocation:**
- Total standalone selling prices: $300,000 + $75,000 + $125,000 = $500,000
- No discount to allocate (contract price equals sum of SSPs)
- License: $300,000; Implementation: $75,000; PCS: $125,000

**Timing of recognition:**
- License: right to use (functional IP) → point in time when license is delivered (IFRS 15.B58)
- Implementation: over time as services are rendered (IFRS 15.35(a))
- PCS: over time, straight-line over 12-month support period (IFRS 15.35(a))

**5. Conclusion**
Three distinct performance obligations recognized separately. License revenue at a point in time; implementation and PCS over time. **Compliant** with IFRS 15.

**6. Journal Entry Impact**
```
On delivery of license:
Dr  Trade Receivable     500,000
  Cr  Revenue (License)    300,000
  Cr  Contract Liability   200,000

Monthly (implementation — 3 months):
Dr  Contract Liability     25,000
  Cr  Revenue (Services)     25,000

Monthly (PCS — 12 months):
Dr  Contract Liability     10,417
  Cr  Revenue (PCS)          10,417
```

**7. Disclosure Impact**
- Disaggregate revenue by type (license, services, PCS)
- Disclose contract liability balance and changes
- Disclose remaining performance obligations

**8. Recommendation**
1. Recognize license revenue on delivery date
2. Recognize implementation revenue over 3-month period
3. Recognize PCS revenue straight-line over 12-month support period
4. Ensure contract liability is properly tracked and disclosed
```

- [ ] **Step 2: Verify the file was created**

```bash
wc -l ~/.claude/skills/ifrs/compliance-templates.md
```

- [ ] **Step 3: Commit**

```bash
git add ~/.claude/skills/ifrs/compliance-templates.md
git commit -m "feat: add IFRS compliance templates (checklists, gap analysis, audit memos)"
```

---

## Task 5: Write Transition Guide (`transition-guide.md`)

**Files:**
- Create: `~/.claude/skills/ifrs/transition-guide.md`

Framework-agnostic GAAP-to-IFRS transition guidance covering IFRS 1 procedure, common difference areas, reconciliation approach, and project planning.

- [ ] **Step 1: Write `transition-guide.md`**

Create `~/.claude/skills/ifrs/transition-guide.md` with the following content:

```markdown
# GAAP-to-IFRS Transition Guide

Framework-agnostic guidance for transitioning from any local GAAP to IFRS. Focuses on IFRS requirements and flags common areas where differences typically arise, rather than mapping from any specific GAAP.

---

## Overview

Transitioning to IFRS requires applying IFRS 1 — First-time Adoption of International Financial Reporting Standards. The process involves preparing an opening IFRS balance sheet at the date of transition, restating comparative periods, and presenting first IFRS financial statements with required reconciliations.

For detailed IFRS 1 steps, see the **First-Time Adoption workflow** in `workflows.md`.

---

## Key Dates

| Date | Definition | Example (FY2026 adoption, 1 year comparatives) |
|------|-----------|----------------------------------------------|
| Date of transition | Beginning of earliest comparative period | 1 January 2025 |
| Comparative period end | End of last period under previous GAAP | 31 December 2025 |
| First IFRS reporting date | End of first IFRS reporting period | 31 December 2026 |
| First IFRS financial statements | Complete set including comparatives | Year ending 31 Dec 2026 |

---

## Common Difference Areas

The following areas frequently require adjustment when transitioning from local GAAP to IFRS. Assess each area for your entity and document differences in a gap analysis (see `compliance-templates.md`).

### 1. Revenue Recognition
**IFRS requirement:** IFRS 15 five-step model with contract-based approach
**Common local GAAP differences:**
- Risks-and-rewards model instead of transfer-of-control
- Less granular identification of performance obligations
- Different treatment of variable consideration
- Different criteria for over-time vs. point-in-time recognition
- Contract costs (obtaining and fulfilling) may not be capitalized

### 2. Leases
**IFRS requirement:** IFRS 16 requires lessees to recognize ROU asset and lease liability for virtually all leases
**Common local GAAP differences:**
- Operating leases off-balance sheet
- Different classification criteria for finance vs. operating
- No requirement for incremental borrowing rate methodology
- Less extensive disclosure requirements

### 3. Financial Instruments
**IFRS requirement:** IFRS 9 classification based on business model and SPPI test; expected credit loss impairment
**Common local GAAP differences:**
- Different classification categories (e.g., held-to-maturity, available-for-sale under older frameworks)
- Incurred loss model instead of expected credit loss
- Different hedge accounting qualifying criteria
- Different treatment of own credit risk for financial liabilities at fair value

### 4. Employee Benefits
**IFRS requirement:** IAS 19 requires projected unit credit method for defined benefit obligations; remeasurements in OCI
**Common local GAAP differences:**
- Corridor approach for actuarial gains/losses (not permitted under IFRS)
- Different discount rate requirements
- Past service cost amortization (IFRS requires immediate recognition)
- Different treatment of plan curtailments and settlements

### 5. Impairment of Non-Financial Assets
**IFRS requirement:** IAS 36 uses higher of fair value less costs of disposal and value in use; CGU-based testing
**Common local GAAP differences:**
- Undiscounted cash flow screening test (US GAAP-style)
- Different impairment indicator requirements
- Different goodwill testing methodology
- No reversal of impairment under some GAAPs (IFRS permits reversal for assets other than goodwill)

### 6. Property, Plant and Equipment
**IFRS requirement:** IAS 16 requires component depreciation; revaluation model optional
**Common local GAAP differences:**
- No component depreciation requirement
- Different capitalization criteria
- Revaluation not permitted or required
- Different treatment of borrowing costs

### 7. Intangible Assets
**IFRS requirement:** IAS 38 requires capitalization of development costs when six criteria are met
**Common local GAAP differences:**
- All R&D expensed (some GAAPs)
- Different criteria for capitalization
- Different treatment of internally generated intangibles

### 8. Provisions and Contingencies
**IFRS requirement:** IAS 37 uses "probable" threshold (>50%); best estimate measurement; discounting required if material
**Common local GAAP differences:**
- Different probability thresholds
- Different measurement approaches (most likely vs. expected value)
- Different discounting requirements
- Different restructuring provision criteria

### 9. Consolidation and Group Accounting
**IFRS requirement:** IFRS 10 control model (power, variable returns, link between power and returns)
**Common local GAAP differences:**
- Majority-of-voting-rights model
- Different treatment of structured/special purpose entities
- Different requirements for uniform accounting policies within group

### 10. Presentation and Disclosure
**IFRS requirement:** IAS 1 requirements for complete financial statements; specific line items and disclosures
**Common local GAAP differences:**
- Different financial statement formats
- Different classification requirements (current/non-current)
- Different OCI presentation
- Generally more extensive IFRS disclosure requirements

---

## Transition Project Planning

### Phase 1: Assessment (3-6 months before transition date)

1. **Identify all IFRS standards applicable to the entity**
2. **Perform gap analysis** against current accounting policies (use gap analysis template in `compliance-templates.md`)
3. **Assess optional exemptions** under IFRS 1 — determine which to elect
4. **Estimate financial impact** of key adjustments
5. **Identify system and process changes** required
6. **Develop transition timeline and resource plan**

### Phase 2: Preparation (transition date to comparative period)

1. **Prepare opening IFRS balance sheet** at date of transition
2. **Document all accounting policy choices** under IFRS
3. **Establish parallel reporting** (if feasible) to capture IFRS data during comparative period
4. **Train finance team** on new accounting policies
5. **Update chart of accounts and reporting systems** as needed
6. **Engage auditors** early for pre-transition consultation

### Phase 3: Execution (comparative period to first IFRS reporting date)

1. **Apply IFRS policies** throughout the first reporting period
2. **Prepare reconciliations** (equity at transition date, equity at end of comparative period, total comprehensive income for comparative period)
3. **Compile first IFRS financial statements** with all required disclosures
4. **Include IFRS 1 specific disclosures** (reconciliations, explanations of material adjustments)
5. **Obtain audit opinion** on first IFRS financial statements

---

## IFRS 1 Exemption Decision Framework

When deciding which optional exemptions to elect, consider:

| Factor | Elect Exemption | Do Not Elect |
|--------|----------------|--------------|
| **Cost of retrospective application** | Disproportionate cost relative to benefit | Reasonable cost to apply retrospectively |
| **Data availability** | Historical data not available or unreliable | Complete historical records available |
| **Comparability** | Users will understand the limitation | Retrospective application provides better comparability |
| **Subsequent measurement** | Exemption does not distort future periods materially | Exemption would create ongoing measurement anomalies |

**Document the rationale** for each exemption election/non-election. Auditors and regulators will ask.

---

## Reconciliation Checklist

For each reconciliation required by IFRS 1:

- [ ] Starting balance under previous GAAP stated correctly
- [ ] All IFRS adjustments identified and calculated
- [ ] Adjustments classified correctly (equity component: retained earnings, OCI, other reserves)
- [ ] Tax effects of adjustments included (deferred tax impact per IAS 12)
- [ ] Non-controlling interests adjusted if applicable
- [ ] Narrative explanation for each material adjustment
- [ ] Cross-referenced to supporting calculations/working papers
- [ ] Reconciliation agrees to opening IFRS balance sheet / closing comparative balance sheet / comparative comprehensive income
```

- [ ] **Step 2: Verify the file was created**

```bash
wc -l ~/.claude/skills/ifrs/transition-guide.md
```

- [ ] **Step 3: Commit**

```bash
git add ~/.claude/skills/ifrs/transition-guide.md
git commit -m "feat: add IFRS transition guide (GAAP-to-IFRS, framework-agnostic)"
```

---

## Task 6: Final Verification

**Files:**
- Verify: all files in `~/.claude/skills/ifrs/`

- [ ] **Step 1: Verify all files exist**

```bash
ls -la ~/.claude/skills/ifrs/
```

Expected: `SKILL.md`, `standards-reference.md`, `workflows.md`, `compliance-templates.md`, `transition-guide.md`

- [ ] **Step 2: Verify SKILL.md word count is under 300**

```bash
wc -w ~/.claude/skills/ifrs/SKILL.md
```

- [ ] **Step 3: Verify all supporting files are searchable by standard number**

```bash
grep -c "## IFRS" ~/.claude/skills/ifrs/standards-reference.md
grep -c "## IAS" ~/.claude/skills/ifrs/standards-reference.md
```

Expected: counts matching the number of IFRS and IAS standards included.

- [ ] **Step 4: Verify cross-references between files are consistent**

Check that `SKILL.md` references the correct filenames:
```bash
grep -o '[a-z-]*\.md' ~/.claude/skills/ifrs/SKILL.md | sort -u
```

Expected: `standards-reference.md`, `workflows.md`, `compliance-templates.md`, `transition-guide.md`

- [ ] **Step 5: Final commit (if any fixes needed)**

```bash
git add ~/.claude/skills/ifrs/
git commit -m "fix: address any issues found during final verification"
```
