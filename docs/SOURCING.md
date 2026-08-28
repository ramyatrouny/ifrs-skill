# Sourcing and maintenance

How the content in `ifrs/` was verified, and how to re-verify it when standards change.
Written for whoever updates this skill next.

The research working area (`.upgrade/`) is not committed: it holds around 520 fetched
documents, roughly 90 MB of IFRS Foundation, EFRAG and Big Four material that is
third-party copyrighted content and cannot be redistributed under this repository's MIT
licence. Everything in it is re-derivable from the sources below.

## Content currency

All content is stated as at **28 August 2026**. The amendment and effective-date register
at the end of `ifrs/standards-reference.md` is the date spine: where a date elsewhere in
the skill disagrees with the register, the register governs.

## Primary sources that work

### Full standard text, free and ungated

```
https://www.ifrs.org/content/dam/ifrs/publications/html-standards/english/2026/issued/<id>.html
```

`<id>` is lower-case with no space or zero-padding: `ifrs16`, `ias36`, `ifric23`, `sic32`,
`ps2` (Practice Statement 2), `cf` (Conceptual Framework). These files carry every numbered
paragraph in full, Appendix A definitions, Appendix B application guidance, Appendix C
effective dates and transition, inline `[Refer: Basis for Conclusions paragraph BCxxx]`
cross-references, and the full text of IFRS IC agenda decisions annotated at the paragraph
each affects.

Fetch with `curl`, not a markdown-converting fetcher — files run to 1.5 MB.

```bash
curl -sL --max-time 90 -A "Mozilla/5.0" -o ias36.html \
  "https://www.ifrs.org/content/dam/ifrs/publications/html-standards/english/2026/issued/ias36.html"
```

**Anchor paragraph extraction on the wrapper `div` id, not on the bare number.** Each
paragraph sits in `id="IAS36_104"` (zero-padded for single digits: `IFRS03_39`). A plain
text strip loses that, and the table of contents then yields a decoy match — the first
grep hit for a paragraph number is frequently a heading rather than the paragraph.

### Known exceptions

| Standard | Where it is |
|---|---|
| IAS 1 | 404 on the 2025 and 2026 paths (superseded by IFRS 18); served from **`/2024/issued/ias1.html`**. 2021–2024 all serve it. |
| IFRS 20 | No file in any edition. Issued 27 May 2026, after the annual edition closed. |
| IFRS 4 | 404 — superseded by IFRS 17. |

### The edition year is one ahead of its content

The "2026" annotated edition contains documents **issued as at 31 December 2025** — its own
front matter says so. Nothing issued in calendar 2026 is in it. For 2026 issuances use the
standard's landing page, IASB Updates, the agenda-decision compilations, and EFRAG.

One exception worth knowing: agenda decisions published since 1 January 2025 were added as
annotations to **IFRS 9, IFRS 15, IFRS 17, IAS 7, IAS 29, IAS 37 and IAS 38** only. For
those seven, a 2025 pull undercounts; for every other standard the two editions agree.

### EU and UK endorsement

EFRAG publishes an Endorsement Status Report roughly monthly. It is authoritative for issue
dates, IASB effective dates, EU endorsement dates, Official Journal publication dates, and
the not-yet-endorsed pipeline with ARC vote dates.

**Check the live page for a newer report before relying on a saved copy.** During this
build the report in hand was six days stale, and the newer one had moved an amendment from
"endorsement process not started" to EFRAG final advice issued — the difference between
"nothing is happening" and "only the vote remains" for an EU preparer.

- Status page: `https://www.efrag.org/en/financial-reporting/endorsement-status`
- UK: the UK Endorsement Board's adoption status report.

EU-adopted IFRS is not the same as IFRS as issued by the IASB. An unendorsed standard
cannot be applied in the EU.

## Traps

### A 200 status proves nothing

Gated resources on ifrs.org return **HTTP 200** with a subscription stub. Do not trust the
status code, and do not trust a byte-size constant — the stub embeds the requested filename
so its length varies, and identical sizes have been observed with differing checksums.

```bash
grep -q "IFRS Digital subscription required" f.html && echo "PAYWALL — discard"
wc -w f.html   # real standards run to tens of thousands of words
```

### The Basis for Conclusions is not available

`<std>-bc.html` returns HTTP 200 with the subscription stub for every standard. **The BC
text cannot be read.** BC paragraph numbers may be cited as pointers, using the inline
`[Refer: …]` cross-references in the standard text. State what a BC paragraph *says* only
where an accessible document quotes it — an IFRIC agenda decision, an effect analysis, a
feedback statement — and attribute it to that document.

`<std>-ie.html` (Illustrative Examples) **is** genuine where it exists, and contains the
IASB's own worked figures. But the suffix depends on what the supplement is called:
IFRS 1's is Implementation Guidance, so `ifrs1-ie` 404s and `ifrs1-ig` is paywalled.

### Dead sources

`iasplus.com` is a JavaScript shell and returns no readable content to a fetcher.
PwC Viewpoint, KPMG Insights and EY's technical library are login-gated, though public PDFs
on those domains sometimes resolve.

## Agenda decisions

Compilation volumes are free PDFs; use `curl` plus `pdftotext -layout`. They quote paragraph
numbers *and* what those paragraphs say, which makes them the route to citing BC content
legitimately.

To enumerate the agenda decisions annotated onto a standard:

```bash
grep -o "Agenda Decision, ‘[^’]*" ias37.txt | sed "s/Agenda Decision, ‘ *//" | tr -s ' ' | sort -u
```

`tr -s ' '` is not optional — entries differ only by internal whitespace and dedupe badly
without it.

## Citation conventions used in this skill

- A paragraph citation means the paragraph was read in the standard's own text.
- `[para-unconfirmed]` means the standard is right but the paragraph was not verified.
  Reproduce the marker; never silently upgrade it to a bare citation.
- `[ASC-para-unconfirmed]` marks a US GAAP reference verified through a secondary source.
  The FASB Codification is registration-gated, so ASC references in the transition guide
  follow EY *US GAAP versus IFRS* (January 2026) and FASB ASU 2025-10 rather than the
  Codification itself.

## Verification performed

Reproducible against the repository:

- **4,234 of 4,240 paragraph citations resolve** against source paragraph text (99.86%).
  The remainder are Basis for Conclusions pointers and IAS 39, for which no extracted
  source exists.
- **171 citations were read semantically** — not merely resolved — weighted towards
  prohibitions, thresholds, deadlines, lettered sub-items and checklist rows asserting a
  disclosure is required.
- **All 60 journal-entry blocks balance**; all 6 embedded assertion blocks pass (38
  assertions). The assertion blocks are committed inside `workflows.md` and
  `transition-guide.md` and are intended to be re-run.

## Known limitations

- **IFRS 20** is covered at status level only. Its paragraph text is unpublished, so there
  is no IFRS 20 disclosure checklist. IFRS 14 applies until an entity adopts IFRS 20.
- **US GAAP comparisons are source-verified, not primary-verified**, for the reason above.
  The US federal tax consequences of abandoning LIFO are flagged as requiring a specialist
  rather than stated.
- **Roughly 50 IFRIC citations are unverifiable** — IFRIC 2, 10, 12, 17 and 21 have no
  source text in the corpus.

## When re-verifying

1. Pull the current EFRAG Endorsement Status Report and diff it against the register.
2. Re-check the standards landing pages for anything issued since the last annual edition.
3. Re-run the assertion blocks in `workflows.md` and `transition-guide.md`.
4. Check the IASB work plan and pipeline for projects that have moved stage.
5. Refresh the IAS 29 hyperinflationary economies list, maintained by the IPTF/CAQ rather
   than by the IASB.
