# Contributing

This repository is an IFRS knowledge base read by AI agents and, through them, by people
doing financial reporting work. A wrong paragraph reference here does not produce a failing
test. It produces a confident, plausible, incorrect answer in someone's accounts.

Contributions are therefore held to an evidentiary standard closer to an audit working
paper than to a documentation pull request. Read this file before opening one.
`docs/SOURCING.md` records how the existing content was verified and is the companion to
this document.

## Contributions that are wanted

- Corrections to a citation, figure, effective date, or statement of a requirement.
- New or amended standards, interpretations, and IFRS IC agenda decisions.
- Additional workflows, disclosure checklists, and worked examples.
- Structural and editorial improvements to the skill files.

Corrections are the most valuable contribution and are reviewed first.

## The evidentiary standard

### 1. Every technical claim carries a paragraph-level citation

A statement that IFRS requires, permits, or prohibits something cites the paragraph that
says so. Standard-level references such as "under IAS 36" are not citations and are not
accepted for a requirement.

The house format is the standard, a full stop, and the paragraph, in the form already used
throughout the repository: `IFRS 16.26`, `IAS 36.104`, `IFRS 3.32`, `IFRS 1.B1`,
`IFRS 18.55(b)`. Ranges use an en dash: `IFRS 2.59A–59B`.

### 2. Citations are verified against the standard's own text, not from memory

Read the paragraph. Model recall of paragraph numbers is unreliable in exactly the way that
matters here: it produces a number that looks right, sits in the right neighbourhood of the
standard, and is wrong. The next section gives the commands.

If you cannot open the paragraph, you have not verified it, and rule 3 applies.

### 3. `[para-unconfirmed]` is used honestly, and is never silently upgraded

`[para-unconfirmed]` means the substantive statement is correct but the paragraph number was
not read in the source text. It is written inline, in the position the citation would
occupy:

```
NRV is estimated selling price less estimated costs of completion and costs to
make the sale (IAS 2 [para-unconfirmed]).
```

Three rules govern the marker:

- **Use it rather than guessing.** A marked claim is honest. A fabricated paragraph number
  is not, and it is indistinguishable from a verified one once merged.
- **Never remove it without reading the paragraph.** Converting `IAS 2 [para-unconfirmed]`
  to `IAS 2.6` is a substantive change requiring the same verification as a new citation.
  State in the pull request which paragraph you read and where.
- **Never add it to a claim you have not otherwise checked.** The marker qualifies the
  paragraph reference, not the accounting.

`[ASC-para-unconfirmed]` is the equivalent marker for US GAAP references in
`ifrs/transition-guide.md`. The FASB Codification is registration-gated, so those references
follow published secondary sources rather than the Codification itself. The same three rules
apply.

### 4. Basis for Conclusions paragraphs are pointers, not quotations

The BC text is subscription-gated on ifrs.org. Every `<standard>-bc.html` URL returns HTTP
200 with a subscription stub, so **the BC cannot be read from the free sources**.

- A BC paragraph number **may** be cited as a pointer, taken from the inline
  `[Refer: Basis for Conclusions paragraph BCxxx]` cross-references that appear in the
  standard text itself.
- A statement of **what a BC paragraph says** is accepted only where an accessible document
  quotes or paraphrases it — an IFRS IC agenda decision, an effect analysis, a feedback
  statement — and the passage is attributed to that document.

The existing content follows this. See the IFRS 18 holding-company discussion in
`ifrs/standards-reference.md`, which cites BC98–BC99 and states plainly that the text is the
Committee's paraphrase rather than a reading of the BC.

### 5. Worked examples balance, and ship with a runnable assertion block

Every journal entry must balance. Every arithmetic example must be reproducible from the
figures given. Where a workflow makes a numerical claim of substance — an amortisation
schedule, an ECL progression, a CSM roll-forward, a purchase price allocation — it carries a
python assertion block in the file, next to the example, that proves it:

````
```python
# IFRS 16 lessor: the net investment amortises exactly to nil at the implicit rate
pva = lambda p, rate, n: sum(p / (1 + rate) ** t for t in range(1, n + 1))
assert round(pva(70_000, 0.056, 5), 2) == 298_101.98   # 5.6% leaves a residual
```
````

These blocks are committed, executed by CI, and intended to be re-run. There are six of them
today, carrying 38 assertions between them. If you change a figure that an assertion block
covers, update the block in the same commit.

## Verifying a citation against the standard text

The full text of every standard is free and ungated at:

```
https://www.ifrs.org/content/dam/ifrs/publications/html-standards/english/2026/issued/<id>.html
```

`<id>` is lower case, no space, no zero padding: `ifrs16`, `ias36`, `ifric23`, `sic32`,
`ps2` (Practice Statement 2), `cf` (Conceptual Framework). These files carry every numbered
paragraph, the Appendix A definitions, Appendix B application guidance, Appendix C effective
dates, the inline `[Refer: …]` cross-references, and the full text of IFRS IC agenda
decisions annotated at the paragraph each affects.

Fetch with `curl`, not a markdown-converting fetcher — the files run to 1.5 MB.

```bash
curl -sL --max-time 90 -A "Mozilla/5.0" -o ifrs16.html \
  "https://www.ifrs.org/content/dam/ifrs/publications/html-standards/english/2026/issued/ifrs16.html"
```

Then read the paragraph:

```bash
python3 scripts/paragraph.py ifrs16.html IFRS16 26
```

```
26 At the commencement date, a lessee shall measure the lease liability at the present
value of the lease payments that are not paid at that date. The lease payments shall be
discounted using the interest rate implicit in the lease, if that rate can be readily
determined. If that rate cannot be readily determined, the lessee shall use the lessee's
incremental borrowing rate. [ Refer: Basis for Conclusions paragraphs BC86 (materiality)
and BC160–BC162 (discount rate) ]
```

### Four traps

**A 200 status proves nothing.** Gated resources return HTTP 200 with a subscription stub.
Do not trust the status code, and do not trust a byte-size constant — the stub embeds the
requested filename, so its length varies.

```bash
grep -q "IFRS Digital subscription required" ifrs16.html && echo "PAYWALL - discard"
wc -w ifrs16.html    # a real standard runs to tens of thousands of words
```

**Anchor on the wrapper `div` id, not the bare paragraph number.** Each paragraph sits in
`<div class="topic paragraph …" id="IFRS16_26">`. A plain grep for the number matches the
table of contents first, and the table of contents is a decoy: it yields a heading, not the
paragraph. Note that the **standard** number is zero-padded to two digits and the
**paragraph** number is not — `IFRS03_32`, but `IFRS16_26`. `scripts/paragraph.py` handles
this.

**The edition year runs one ahead of its content.** The 2026 annotated edition contains
documents issued as at 31 December 2025; its own front matter says so. Nothing issued in
calendar 2026 is in it. For a 2026 issuance use the standard's landing page, IASB Updates,
the agenda-decision compilations, and EFRAG.

**Known exceptions.** IAS 1 404s on the 2025 and 2026 paths, having been superseded by
IFRS 18; it is served from `/2024/issued/ias1.html`. IFRS 20 has no file in any edition — it
was issued on 27 May 2026, after the annual edition closed, so it is covered at status level
only and there is no IFRS 20 disclosure checklist. IFRS 4 404s, superseded by IFRS 17.

### Effective dates and endorsement

The amendment and effective-date register at the end of `ifrs/standards-reference.md` is the
date spine. Where a date elsewhere in the skill disagrees with the register, the register
governs, and a pull request that changes a date changes the register too.

EFRAG's Endorsement Status Report is authoritative for issue dates, IASB effective dates, EU
endorsement dates, Official Journal publication, and the not-yet-endorsed pipeline. Check the
live page rather than a saved copy; the reports move monthly and a stale one has already
misrepresented an amendment's status once during this project.

- `https://www.efrag.org/en/financial-reporting/endorsement-status`
- UK: the UK Endorsement Board adoption status report.

EU-adopted IFRS is not IFRS as issued by the IASB. An unendorsed standard cannot be applied
in the EU, and the skill states both positions where they differ.

## Journal entry format

`scripts/check_journal_entries.py` parses every entry in the skill and asserts that debits
equal credits. It reads a specific shape, so keep to it:

```
Dr  Cash                                1,000,000
Dr  Right-of-Use Asset                    480,000
    Cr  Building (carrying amount)                    800,000
    Cr  Lease Liability                               600,000
    Cr  Gain on Disposal (P&L)                         80,000
To recognise the sale-and-leaseback.
```

- The entry sits inside a fenced code block with no language tag.
- Each posting is one line: `Dr` or `Cr`, the account name, **two or more spaces**, then the
  amount with comma thousands separators. The two spaces are the column separator — a single
  space between account and amount will not parse.
- Indenting the credits is the house style. The parser does not require it.
- An entry ends at a blank line, at a narrative line, or where a `Dr` line follows a `Cr`
  line. Several entries may share one code block.
- A pattern entry with no figures uses `XXX` as the amount. Those entries are skipped rather
  than balanced.

## Running the checks locally

```bash
python3 scripts/check_skill_structure.py
python3 scripts/check_journal_entries.py
python3 tests/fixtures/invoice-balance-sheet/verify_key_figures.py
npx --yes markdownlint-cli2@0.23.2 "**/*.md" "#node_modules"
```

All four run in CI on every pull request. Run them before you push; a failing check is the
most common reason a pull request sits unreviewed.

Two further checks do not run in CI, because each needs something the repository does not
hold:

```bash
python3 scripts/check_citations.py                      # needs the source corpus
python3 scripts/check_feature_review.py <review.md> --fixture invoice-balance-sheet
```

`check_citations.py` resolves every paragraph citation in `ifrs/` and `tests/expected/`
against the standards' own text. It needs the extracted corpus, which is third-party
copyrighted material and is not committed — `docs/SOURCING.md` says how to rebuild it.
Without the corpus it reports that it skipped and exits 0.

`check_feature_review.py` checks the shape of a feature review's output against the rules in
`ifrs/feature-review.md`: that standard numbers appear only in evidence lines, that nothing
outside the covered standards is cited, that practice notes carry the fixed heading, and that
the verdict follows arithmetically from the severities. It needs a review to check, and no
review output is committed — see `tests/README.md`. It checks shape, never whether the
findings are correct; that judgement is made against the answer key by a person.

## Making the change

1. Fork the repository and branch from `main`.
2. Keep the change focused. A citation correction and a new workflow are two pull requests.
3. Write the change in the register-neutral, formal style of the surrounding text. The
   audience is a qualified accountant.
4. Run the four checks above.
5. Complete the pull request template in full. It asks for your sources, and for explicit
   confirmation that you read the paragraphs and that the examples balance. Those are the
   two things a reviewer cannot verify cheaply and must take on trust.

## Review process

Every pull request is reviewed by the maintainer. Content changes are reviewed on four
points:

1. **Is the accounting right?** Read against the standard, not against plausibility.
2. **Does every citation resolve?** A sample of the paragraph references is opened in the
   source text. A sample failure escalates to a full check of the pull request.
3. **Is the marker discipline intact?** Any `[para-unconfirmed]` removed in the diff must be
   accounted for in the description.
4. **Do the checks pass, and do the examples balance?**

Expect a first response within two weeks. Corrections to incorrect published guidance are
handled ahead of everything else; if the current content is materially wrong, open an issue
using the content correction template rather than waiting on a pull request.

Substantive review comments are technical, not stylistic, and are meant to be argued with.
If you believe a review comment is wrong about the accounting, say so and cite the paragraph.

## What will cause a pull request to be rejected

- **A fabricated or unverified paragraph number.** The single most damaging defect this
  repository can ship. If the paragraph was not read, mark it `[para-unconfirmed]`.
- **Silently upgrading a `[para-unconfirmed]` marker** to a bare citation without stating in
  the pull request which paragraph was read and where.
- **Quoting or asserting the content of a Basis for Conclusions paragraph** without
  attributing it to an accessible document that reproduces it.
- **A journal entry that does not balance**, or a worked example whose arithmetic does not
  reproduce from the stated figures.
- **A changed figure without a corresponding update to the assertion block** that covers it.
- **Content copied from a gated or copyrighted source** — IFRS Foundation publications beyond
  fair citation, Big Four technical libraries, textbooks. Cite them; do not paste them.
- **An effective date changed in one file only**, leaving it inconsistent with the amendment
  register.
- **Unattributed AI-generated content presented as verified.** Drafting with a model is fine.
  Shipping its recollection of paragraph numbers is not. Every citation still has to be
  opened.

## Licence

The repository is MIT licensed. By contributing you agree that your contribution is licensed
under the same terms, and that you have the right to submit it.

The content of the IFRS Standards themselves is copyright of the IFRS Foundation. This
repository contains original explanatory material and paragraph references, not reproductions
of the standards. Keep it that way.
