#!/usr/bin/env python3
"""Print one paragraph of an IFRS standard from a file downloaded from ifrs.org.

    curl -sL --max-time 90 -A "Mozilla/5.0" -o ifrs16.html \
      "https://www.ifrs.org/content/dam/ifrs/publications/html-standards/english/2026/issued/ifrs16.html"

    python3 scripts/paragraph.py ifrs16.html IFRS16 26
    python3 scripts/paragraph.py ifrs3.html  IFRS03 32     # standard number padded to two digits
    python3 scripts/paragraph.py ifrs16.html IFRS16 B34    # appendix paragraphs work too
"""

import html
import re
import sys

if len(sys.argv) != 4:
    sys.exit(__doc__)

path, prefix, number = sys.argv[1], sys.argv[2].upper(), sys.argv[3]
source = open(path, encoding="utf-8", errors="replace").read()

if "IFRS Digital subscription required" in source:
    sys.exit("PAYWALL - this file is a subscription stub, not the standard text.")

# Anchor on the paragraph wrapper div, never on a bare paragraph number: the first
# match for a bare number is usually a table-of-contents entry or a cross-reference.
match = re.search(
    rf'<div class="topic paragraph[^"]*" id="{prefix}_{number}">(.*?)(?=<div class="topic )',
    source,
    re.S,
)
if not match:
    sys.exit(
        f"no paragraph wrapper found for {prefix}_{number}. "
        "Check the padding: the standard number is zero-padded to two digits "
        "(IFRS03_32), the paragraph number is not (IFRS16_26)."
    )

text = re.sub(r"<[^>]+>", " ", match.group(1))
print(re.sub(r"\s+", " ", html.unescape(text)).strip())
