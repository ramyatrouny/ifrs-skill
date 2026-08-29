# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
For a content repository, the version components are read as: **major** for a change that
alters guidance a reader may already have relied on, **minor** for new coverage, **patch**
for corrections and editorial work.

## [Unreleased]

## [2.1.0] - 2026-08-29

Adds a capability the skill did not previously have: reviewing software that produces
accounting figures, rather than answering questions about the standards. Released as a minor
version because it is new coverage — nothing in versions 1.0.0 or 2.0.0 changes meaning, and
no guidance a reader may already have relied on is altered.

### Added

- **`ifrs/feature-review.md`** — an IFRS review of an implementation. Given a feature that
  produces an accounting figure and one real output it produced, it reports what is wrong in
  language a developer can act on. It refuses to run on code alone. Findings carry a class
  (Non-compliant, Wrong, Incomplete, Untraceable) saying who fixes the defect, and a severity
  (Blocking, Needs work, Conforms) from which the verdict follows arithmetically. Standard
  numbers appear only in the evidence line closing each finding, never in its body, because
  the reader is technical and not an accountant.
- **A trigger map** connecting code artefacts to the standards to check against them — an
  invoices table to IFRS 15 and IFRS 9, a balance-sheet renderer to IAS 1 and IFRS 18, a
  currency field to IAS 21. It covers six standards: IFRS 15, IFRS 9, IAS 1 and IFRS 18,
  IAS 21, IFRS 16 and IAS 7. Anything a feature touches outside them is reported as unchecked
  rather than guessed at.
- **The 1 January 2027 presentation change in every review.** Code written today is still
  running when IFRS 18 replaces IAS 1, so a statement renderer is checked against both, and
  what breaks later is its own finding at Needs work rather than Blocking.
- **`tests/`** — the acceptance fixture. A deliberately defective balance-sheet generator with
  four planted defects, its real generated output, and an answer key held outside the fixture
  directory so a reviewing agent cannot read what it is being tested on.
- **`scripts/check_feature_review.py`** — checks a review's shape against the rules the skill
  sets: citations only in evidence lines, nothing cited outside the covered standards, the
  fixed practice-note heading, and a verdict consistent with the severities. It checks shape,
  never whether the findings are correct.
- **`tests/fixtures/invoice-balance-sheet/verify_key_figures.py`** — asserts every figure the
  answer key quotes, and now runs in CI.
- **`CONTEXT.md`** — the domain glossary, and **`docs/adr/`** recording two decisions: that
  practice notes may be uncited under a fixed heading, and that reviews split by standard.

### Changed

- `SKILL.md` routes to the new file, discriminating on whether code is involved:
  `compliance-templates.md` reviews financial statements, `feature-review.md` reviews the
  software that produces them.
- `scripts/check_citations.py` now resolves the citations in `tests/expected/` as well as
  `ifrs/`. An answer key with a wrong paragraph reference in it would fail a correct review,
  so keys are held to the same bar as the skill. 4,239 of 4,245 checkable citations resolve.
- The README states the one exception to the repository's citation rule rather than implying
  citation is universal. Labelled practice notes describe what finance teams conventionally do,
  which no standard says and nothing can cite.

## [2.0.0] - 2026-08-28

A full content re-verification and expansion. Every paragraph citation in the repository was
re-checked against the standards' own text; 4,234 of 4,240 citations resolve against source
paragraph text, with the remainder being Basis for Conclusions pointers and IAS 39, for
which no extracted source exists. The skill grew from 4,771 to 13,321 lines.

Released as a major version because two errors corrected below produced incorrect output in
version 1.0.0, and readers who relied on them need to know.

### Added

- **IFRS 18 _Presentation and Disclosure in Financial Statements_** — the three income and
  expense categories, the required subtotals, management-defined performance measures, and
  aggregation and disaggregation, including the April 2026 IFRS IC agenda decision on the
  separate financial statements of a parent.
- **IFRS 19 _Subsidiaries without Public Accountability: Disclosures_** — scope, eligibility,
  and the reduced disclosure regime.
- **IFRS 20 _Regulatory Assets and Regulatory Liabilities_** at status level. Issued 27 May
  2026, after the 2026 annotated edition closed; its paragraph text is unpublished, so there
  is no IFRS 20 disclosure checklist and IFRS 14 continues to apply until an entity adopts it.
- **IFRS S1 and IFRS S2** — the ISSB sustainability disclosure standards, with the
  general requirements, the climate-related disclosures, and the transition reliefs.
- **An interpretations section** covering the IFRIC and SIC interpretations in force and the
  IFRS IC agenda decisions annotated onto the standards, including the seven standards
  (IFRS 9, IFRS 15, IFRS 17, IAS 7, IAS 29, IAS 37, IAS 38) that carry agenda decisions
  published since 1 January 2025.
- **An amendment and effective-date register** at the end of `standards-reference.md`,
  established as the date spine for the whole skill: where a date elsewhere disagrees with
  the register, the register governs. Includes EU endorsement status and the not-yet-endorsed
  pipeline.
- Workflows for deferred tax (IAS 12), business combinations (IFRS 3), sale-and-leaseback,
  IFRS 9 journal entries, the CSM roll-forward, goodwill impairment, diluted EPS, and IFRS 18
  categorisation.
- Compliance templates for materiality, going concern, interim reporting, first-time
  adoption, and management-defined performance measures.
- Six committed python assertion blocks, carrying 38 assertions, proving the arithmetic of
  the worked examples in `workflows.md` and `transition-guide.md`. They are intended to be
  re-run and are now executed in CI.
- `docs/SOURCING.md`, documenting the free ifrs.org URL pattern, the paywall and
  table-of-contents traps, the edition-year offset, and the re-verification procedure.
- The `[para-unconfirmed]` and `[ASC-para-unconfirmed]` markers, and the convention that a
  bare citation means the paragraph was read in the standard's own text.

### Changed

- `SKILL.md` rewritten as a routing hub, with explicit task-type routing, audience detection,
  and citation rules. It stays under 100 lines by design.
- Transition guide expanded with the US GAAP and local GAAP difference matrices, the IFRS 1
  mandatory exceptions, deferred tax on transition, IT and systems guidance, and transition
  to IFRS 18.
- Standards reference reordered, and editorial commentary removed in favour of requirement
  statements with citations.

### Fixed

- **An IFRS 3 acquisition journal entry that did not balance.** The entry debited CU 6,000,000
  against credits of CU 6,800,000; the CU 800,000 gap was the omitted goodwill. Goodwill is a
  residual under IFRS 3.32, and the debit to goodwill is what makes the acquisition entry
  balance. The corrected entry and a runnable proof are in `workflows.md`.
- **A withdrawn IFRS 1 exemption presented as available.** The D10–D11 exemption was removed.
- **The IFRS 16 lessor net-investment schedule**, which used a discount rate that left a
  residual rather than the rate implicit in the lease. The implicit rate is 5.3686%, at which
  the net investment amortises exactly to nil and cross-casts to total payments.
- **The IFRS 9 ECL sequence**, where the initial-recognition allowance was stated as the
  reporting-date figure.

### Removed

- Statements of Basis for Conclusions content that could not be attributed to an accessible
  source. BC paragraph numbers are retained as pointers only.

### Known limitations

- IFRS 20 is covered at status level only; its paragraph text is unpublished.
- US GAAP comparisons are source-verified rather than primary-verified: the FASB Codification
  is registration-gated, so ASC references follow published secondary sources and carry
  `[ASC-para-unconfirmed]`.
- Approximately 50 IFRIC citations are unverifiable — IFRIC 2, 10, 12, 17 and 21 have no
  source text in the extracted corpus.

## [1.0.0] - 2026-03-29

### Added

- Initial release. 4,771 lines covering the then-current IFRS and IAS standards.
- `SKILL.md` entry point with task-type routing.
- `standards-reference.md` — standard-by-standard scope, core principles, key requirements,
  disclosure requirements, common pitfalls, and cross-references.
- `workflows.md` — step-by-step procedures for revenue (IFRS 15), leases (IFRS 16),
  impairment (IAS 36), financial instruments (IFRS 9), and first-time adoption (IFRS 1).
- `compliance-templates.md` — disclosure checklist, gap analysis, audit memo, management
  representation letter, and accounting policy summary.
- `transition-guide.md` — GAAP-to-IFRS transition guidance with the IFRS 1 exemption
  framework and a three-phase project plan.

[Unreleased]: https://github.com/ramyatrouny/ifrs-skill/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/ramyatrouny/ifrs-skill/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/ramyatrouny/ifrs-skill/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/ramyatrouny/ifrs-skill/releases/tag/v1.0.0
