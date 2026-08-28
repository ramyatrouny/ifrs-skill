#!/usr/bin/env python3
"""Validate the skill against the Agent Skills specification.

Checks:
  1. ifrs/SKILL.md exists and opens with YAML frontmatter.
  2. Frontmatter carries a non-empty `name` and `description`.
  3. `name` matches the skill directory and is a lower-case slug.
  4. Every supporting `.md` file named in SKILL.md exists in ifrs/.
  5. SKILL.md stays under 100 lines - it is a router, not a reference.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "ifrs"
SKILL_FILE = SKILL_DIR / "SKILL.md"
MAX_LINES = 100
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REFERENCE = re.compile(r"`([A-Za-z0-9_.-]+\.md)`")


def main() -> int:
    errors: list[str] = []

    if not SKILL_FILE.exists():
        print(f"FAIL  {SKILL_FILE.relative_to(ROOT)} does not exist")
        return 1

    lines = SKILL_FILE.read_text(encoding="utf-8").splitlines()

    if len(lines) >= MAX_LINES:
        errors.append(
            f"SKILL.md is {len(lines)} lines; the entry point must stay under {MAX_LINES}. "
            "Move detail into a supporting file."
        )

    if not lines or lines[0].strip() != "---":
        errors.append("SKILL.md must open with a '---' YAML frontmatter delimiter on line 1.")
        frontmatter: list[str] = []
    else:
        try:
            close = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
        except StopIteration:
            errors.append("SKILL.md frontmatter is never closed with '---'.")
            frontmatter = []
        else:
            frontmatter = lines[1:close]

    fields = {}
    for line in frontmatter:
        if ":" in line and not line.startswith((" ", "\t", "#")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()

    name = fields.get("name", "")
    description = fields.get("description", "")

    if not name:
        errors.append("Frontmatter is missing a non-empty 'name'.")
    else:
        if not SLUG.match(name):
            errors.append(f"Frontmatter 'name' ({name!r}) must be a lower-case hyphenated slug.")
        if name != SKILL_DIR.name:
            errors.append(
                f"Frontmatter 'name' ({name!r}) does not match the skill directory "
                f"({SKILL_DIR.name!r})."
            )

    if not description:
        errors.append("Frontmatter is missing a non-empty 'description'.")
    elif len(description) < 40:
        errors.append(
            "Frontmatter 'description' is too short to route on. State when the skill applies."
        )

    body = "\n".join(lines[len(frontmatter) + 2 :]) if frontmatter else "\n".join(lines)
    referenced = sorted(set(REFERENCE.findall(body)) - {"SKILL.md"})
    for filename in referenced:
        if not (SKILL_DIR / filename).exists():
            errors.append(f"SKILL.md references '{filename}', which does not exist in ifrs/.")

    shipped = sorted(p.name for p in SKILL_DIR.glob("*.md") if p.name != "SKILL.md")
    unreferenced = [f for f in shipped if f not in referenced]
    for filename in unreferenced:
        print(f"warning: ifrs/{filename} ships but is not referenced from SKILL.md")

    print(f"SKILL.md: {len(lines)} lines, name={name!r}")
    print(f"supporting files referenced and present: {', '.join(referenced) or 'none'}")

    if errors:
        print("\nFAILURES")
        for error in errors:
            print(f"  {error}")
        return 1
    print("skill structure valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
