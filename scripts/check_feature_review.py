#!/usr/bin/env python3
"""Check a feature review's output against the rules ifrs/feature-review.md sets.

This checks the review's SHAPE, mechanically: that citations sit only in evidence
lines, that no standard outside the covered six is cited, that practice notes carry
the exact fixed heading, and that the verdict follows arithmetically from severity.

It does NOT check that the findings are correct. For the invoice-balance-sheet
fixture that judgement is made against tests/expected/invoice-balance-sheet.md by a
reader, and --fixture invoice-balance-sheet additionally asserts that the four
required evidence citations are present.

Usage:  python3 scripts/check_feature_review.py <review.md> [--fixture <name>]
"""
from __future__ import annotations

import re
import sys

# The six covered standards, plus IAS 8: SKILL.md section 4 routes the 2027
# presentation change through IAS 8 (going concern, judgements, estimation
# uncertainty all relocated there from IAS 1), so a review that follows section 6
# of the procedure may legitimately land on it.
COVERED = {("IFRS", "9"), ("IFRS", "15"), ("IFRS", "16"), ("IFRS", "18"),
           ("IAS", "1"), ("IAS", "7"), ("IAS", "21"), ("IAS", "8")}

CITE = re.compile(r"\b(IFRS|IAS|IFRIC|SIC)[ -](\d+)\.([0-9A-Za-z]+(?:\.\d+)*)")
SOURCE = re.compile(r"<sub>\s*Source:.*?</sub>", re.S)
PRACTICE = "**In practice — how finance teams usually handle this. Not a requirement.**"
VERDICT = re.compile(
    r"\*\*(Ready|Not ready)\.?\*\*\s*(\d+)\s+blocking,\s*(\d+)\s+need work,\s*(\d+)\s+conform",
    re.I)

# Minimum severity spread for a fixture, as (blocking, needs work). Catches a review
# that finds the right defects and misjudges every one of them.
SEVERITY_FLOOR = {"invoice-balance-sheet": (3, 1)}

REQUIRED = {
    "invoice-balance-sheet": [
        ({"IFRS 9.5.5.15"}, "no loss allowance on trade receivables"),
        ({"IFRS 15.47"},    "sales tax treated as revenue"),
        ({"IFRS 15.31"},    "revenue recognised on invoice date, not delivery"),
        ({"IAS 1.60", "IFRS 18.96"}, "no current/non-current split"),
    ],
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    path = sys.argv[1]
    fixture = None
    if "--fixture" in sys.argv:
        i = sys.argv.index("--fixture") + 1
        if i >= len(sys.argv):
            print("--fixture needs a name, e.g. --fixture invoice-balance-sheet")
            return 2
        fixture = sys.argv[i]

    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    fails: list[str] = []

    # 1 — citations belong in evidence lines only (feature-review.md section 8)
    outside = SOURCE.sub("", text)
    stray = sorted({f"{f} {n}.{p}" for f, n, p in CITE.findall(outside)})
    if stray:
        fails.append(f"citations outside an evidence line: {', '.join(stray)}")

    # 2 — nothing cited beyond the covered six
    uncovered = sorted({f"{f} {n}" for f, n, _ in CITE.findall(text)
                        if (f, n) not in COVERED})
    if uncovered:
        fails.append(f"standards cited outside the covered six: {', '.join(uncovered)}")

    # 3 — practice notes use the fixed heading, never a variant
    for variant in re.findall(r"^\*\*In practice.*$", text, re.M):
        if variant.strip() != PRACTICE:
            fails.append(f"practice-note heading varies: {variant.strip()!r}")

    # 4 — the verdict is arithmetic: any blocking means not ready
    m = VERDICT.search(text)
    if not m:
        fails.append("no verdict line in the form '**Not ready.** n blocking, n need work, n conform'")
    else:
        verdict, blocking = m.group(1).lower(), int(m.group(2))
        if blocking > 0 and verdict != "not ready":
            fails.append(f"{blocking} blocking finding(s) but verdict is '{verdict}'")
        if blocking == 0 and verdict == "not ready":
            fails.append("verdict 'not ready' with no blocking findings")

    # 5 — scope must be stated, not implied
    if not re.search(r"^Not checked:", text, re.M):
        fails.append("no 'Not checked:' line — silence about unreviewed standards reads as approval")

    # 6 — fixture-specific: the required findings' evidence must be present
    if fixture in REQUIRED:
        for accepted, label in REQUIRED[fixture]:
            if not any(c in text for c in accepted):
                fails.append(f"missing required finding: {label} ({' or '.join(sorted(accepted))})")

    if fixture in SEVERITY_FLOOR and m:
        need_b, need_n = SEVERITY_FLOOR[fixture]
        if int(m.group(2)) < need_b:
            fails.append(f"only {m.group(2)} blocking finding(s); fixture requires at least {need_b}")
        if int(m.group(3)) < need_n:
            fails.append(f"only {m.group(3)} 'needs work' finding(s); fixture requires at least {need_n}")

    print(f"reviewed file : {path}")
    print(f"citations     : {len(CITE.findall(text))} "
          f"({len(SOURCE.findall(text))} evidence lines)")
    if m:
        print(f"verdict       : {m.group(1)} — {m.group(2)} blocking, "
              f"{m.group(3)} need work, {m.group(4)} conform")
    if fails:
        print(f"\nFAIL ({len(fails)}):")
        for failure in fails:
            print(f"  - {failure}")
        return 1
    print("\nPASS — shape conforms to ifrs/feature-review.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
