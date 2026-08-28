## What this changes

<!-- One or two sentences. If this corrects something, say what was wrong. -->

## Type of change

- [ ] Content correction (a citation, figure, or statement was wrong)
- [ ] Standard update (a standard, amendment, effective date, or endorsement status changed)
- [ ] New coverage (a standard, workflow, checklist, or template)
- [ ] Editorial or structural
- [ ] Tooling, scripts, or CI

## Sources

<!--
List every source you worked from. For a paragraph citation, give the URL of the standard
text you read. For an effective date, give the EFRAG report and its date. For Basis for
Conclusions content, give the accessible document that quotes it.
-->

| Claim or paragraph | Source | Read on |
|---|---|---|
| IFRS 16.26 | https://www.ifrs.org/content/dam/ifrs/publications/html-standards/english/2026/issued/ifrs16.html | 2026-08-28 |

## Verification

- [ ] **Every paragraph reference I added or changed was read in the standard's own text.**
      Not recalled, not inferred from a secondary source, not carried over from an earlier
      draft. If any was not, it is marked `[para-unconfirmed]`.
- [ ] I did not remove a `[para-unconfirmed]` marker without reading the paragraph. If I
      removed one, the paragraph and source are in the table above.
- [ ] Any Basis for Conclusions paragraph I cite is cited as a pointer only, or its content
      is attributed to the accessible document that reproduces it.
- [ ] **Every journal entry I added or changed balances**, and every worked example
      reproduces from the figures stated in it.
- [ ] Where a figure I changed is covered by a python assertion block, I updated the block in
      the same commit.
- [ ] Effective dates I changed are consistent with the amendment and effective-date register
      at the end of `standards-reference.md`, or I updated the register too.
- [ ] I ran the checks locally and they pass:

```bash
python3 scripts/check_skill_structure.py
python3 scripts/check_journal_entries.py
npx --yes markdownlint-cli2@0.23.2 "**/*.md" "#node_modules"
```

- [ ] No copyrighted standard text, or gated third-party material, is reproduced beyond fair
      citation.

## Related issue

<!-- Closes #  -->

## Notes for the reviewer

<!--
Anything you are unsure about. Flagging a doubt here is always better than leaving it for the
reviewer to find. If a paragraph number defeated you, say which one.
-->
