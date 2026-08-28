#!/usr/bin/env python3
"""Resolve every paragraph citation in the skill against the standards' own text.

This answers one narrow question: does the cited paragraph exist in the standard?
It does NOT check that the paragraph says what the skill says it says. That is a
separate, manual review — see the "How the content was verified" section of the
README for the distinction, which matters.

Requires the extracted source corpus at .upgrade/sources/std/<id>.para.txt, one
record per paragraph in the form "[IAS 36.104] <text>". That corpus is not
committed (it is third-party copyrighted material); docs/SOURCING.md documents
how to rebuild it. Without it this script exits 0 and reports that it skipped.

Usage:  python3 scripts/check_citations.py [--verbose]
"""
from __future__ import annotations

import glob
import os
import re
import sys

CORPUS = ".upgrade/sources/std"
SKILL = "ifrs"

# IFRS 15.35(c), IAS 36.104, IFRS 9.5.5.3, IAS 8.6K, IFRS 16.B21, IFRS 1.D9E
CITE = re.compile(r"\b(IFRS|IAS|IFRIC|SIC)[ -](\d+)\.([0-9A-Za-z]+(?:\.\d+)*)")


def load_corpus() -> dict[str, set[str]]:
    corpus: dict[str, set[str]] = {}
    for path in glob.glob(os.path.join(CORPUS, "*.para.txt")):
        key = os.path.basename(path).replace(".para.txt", "")
        with open(path, encoding="utf-8") as fh:
            corpus[key] = set(re.findall(r"^\[([^\]]+)\]", fh.read(), flags=re.M))
    return corpus


def resolves(label: str, family: str, number: str, para: str,
             paragraphs: set[str]) -> bool:
    """A citation resolves if the exact label exists, or if it is a sub-item
    (e.g. 35(c)) of a paragraph that exists."""
    if label in paragraphs:
        return True
    if any(p.startswith(label) for p in paragraphs):
        return True
    base = re.match(r"(\d+[A-Za-z]*)", para)
    return bool(base and f"{family} {number}.{base.group(1)}" in paragraphs)


def main() -> int:
    verbose = "--verbose" in sys.argv
    corpus = load_corpus()
    if not corpus:
        print(f"no corpus at {CORPUS}/ — skipping citation resolution")
        print("see docs/SOURCING.md to rebuild it")
        return 0

    total = resolved = no_source = 0
    unresolved: dict[str, int] = {}

    for path in sorted(glob.glob(os.path.join(SKILL, "*.md"))):
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        for family, number, para in CITE.findall(text):
            total += 1
            key = f"{family.lower()}{number}"
            if key not in corpus:
                no_source += 1
                continue
            label = f"{family} {number}.{para}"
            if resolves(label, family, number, para, corpus[key]):
                resolved += 1
            else:
                unresolved[label] = unresolved.get(label, 0) + 1

    checkable = total - no_source
    pct = (resolved / checkable * 100) if checkable else 100.0

    print(f"corpus            : {len(corpus)} standards, "
          f"{sum(len(v) for v in corpus.values())} paragraph labels")
    print(f"citations found   : {total}")
    print(f"  no source text  : {no_source} (not checkable)")
    print(f"  checkable       : {checkable}")
    print(f"  resolved        : {resolved}  ({pct:.2f}%)")
    print(f"  unresolved      : {sum(unresolved.values())} "
          f"({len(unresolved)} distinct)")

    if unresolved and verbose:
        print("\nunresolved citations:")
        for label, count in sorted(unresolved.items()):
            print(f"  {label} x{count}")

    # Unresolved citations are reported, not fatal: some are deliberate
    # (Basis for Conclusions pointers, Illustrative Examples references, and
    # paragraphs correctly described as deleted). Review them; do not assume.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
