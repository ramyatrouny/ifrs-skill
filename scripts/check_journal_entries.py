#!/usr/bin/env python3
"""Assert that every journal entry in the skill balances, and run every embedded
python assertion block.

A journal entry is a run of lines inside a fenced code block that begins with
``Dr`` or ``Cr``. An entry ends at a blank line, at a narrative line, or where a
``Dr`` line follows a ``Cr`` line. Entries whose amounts are placeholders
(``XXX``) are skipped: they illustrate a pattern rather than a figure.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGETS = ["ifrs/workflows.md", "ifrs/transition-guide.md", "ifrs/compliance-templates.md"]

FENCE = re.compile(r"^\s*```(\w*)\s*$")
POSTING = re.compile(r"^\s*(Dr|Cr)\s+(.+?)\s{2,}\(?([0-9][0-9,\. ]*)\)?\s*$")
PLACEHOLDER = re.compile(r"^\s*(Dr|Cr)\s+.*?\s{2,}\(?X+\)?\s*$", re.IGNORECASE)
TOL = 1.0  # currency units; entries are stated in whole units


def amount(raw: str) -> float:
    return float(raw.replace(",", "").replace(" ", ""))


def check_entry(entry, path, start_line, failures, checked):
    if not entry:
        return
    if any(kind is None for kind, _, _ in entry):
        return  # placeholder amounts
    debits = sum(v for kind, v, _ in entry if kind == "Dr")
    credits = sum(v for kind, v, _ in entry if kind == "Cr")
    if not debits or not credits:
        return
    checked.append((path, start_line))
    if abs(debits - credits) > TOL:
        failures.append(
            f"{path}:{start_line}  debits {debits:,.2f} != credits {credits:,.2f} "
            f"(difference {debits - credits:,.2f})"
        )


def scan(path: pathlib.Path, rel: str, failures, checked):
    in_fence = False
    entry: list = []
    start = 0
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if FENCE.match(line):
            check_entry(entry, rel, start, failures, checked)
            entry = []
            in_fence = not in_fence
            continue
        if not in_fence:
            continue
        posting = POSTING.match(line)
        if posting:
            kind, _account, raw = posting.groups()
            if not entry:
                start = lineno
            elif kind == "Dr" and any(k == "Cr" for k, _, _ in entry):
                check_entry(entry, rel, start, failures, checked)
                entry, start = [], lineno
            entry.append((kind, amount(raw), lineno))
            continue
        if PLACEHOLDER.match(line):
            if not entry:
                start = lineno
            entry.append((None, 0.0, lineno))
            continue
        check_entry(entry, rel, start, failures, checked)
        entry = []
    check_entry(entry, rel, start, failures, checked)


def run_python_blocks(path: pathlib.Path, rel: str, failures) -> int:
    text = path.read_text(encoding="utf-8").splitlines()
    blocks, current, start = [], None, 0
    for lineno, line in enumerate(text, 1):
        if current is None:
            if re.match(r"^\s*```python\s*$", line):
                current, start = [], lineno
            continue
        if re.match(r"^\s*```\s*$", line):
            blocks.append((start, "\n".join(current)))
            current = None
            continue
        current.append(line)
    for start, code in blocks:
        if "assert" not in code:
            continue
        try:
            exec(compile(code, f"{rel}:{start}", "exec"), {"__name__": "__block__"})
        except Exception as exc:  # noqa: BLE001 - report, do not raise
            failures.append(f"{rel}:{start}  assertion block failed: {exc!r}")
    return sum(1 for _, code in blocks if "assert" in code)


def main() -> int:
    failures: list[str] = []
    checked: list = []
    blocks = 0
    for rel in TARGETS:
        path = ROOT / rel
        if not path.exists():
            failures.append(f"{rel}  missing")
            continue
        scan(path, rel, failures, checked)
        blocks += run_python_blocks(path, rel, failures)
    print(f"journal entries checked: {len(checked)}")
    print(f"assertion blocks executed: {blocks}")
    if failures:
        print("\nFAILURES")
        for f in failures:
            print(f"  {f}")
        return 1
    print("all journal entries balance; all assertion blocks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
