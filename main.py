#!/usr/bin/env python3
"""One-Liner Laughs entry: write one joke line to the output file.

The joke is a single line of at most 200 characters. The program validates
that limit itself, then writes exactly that line (no trailing newline) to
/output/entry.txt, or to $OUTPUT_PATH when that variable is set.
"""

import os

JOKE = (
    "My fitness tracker congratulated me on 10,000 steps "
    "\u2014 I\u2019d just been pacing while my Wi-Fi was down."
)
MAX_CHARS = 200


def validate(line: str) -> str:
    """Check the joke against the bounty gate; return it unchanged."""
    if not line.strip():
        raise SystemExit("joke line is empty")
    if len(line) > MAX_CHARS:
        raise SystemExit(
            "joke is %d characters, over the %d limit" % (len(line), MAX_CHARS)
        )
    if "\n" in line or "\r" in line:
        raise SystemExit("joke must be a single line")
    if any(ord(ch) < 0x20 for ch in line):
        raise SystemExit("joke must not contain control characters")
    return line


def main() -> None:
    os.umask(0o022)
    line = validate(JOKE)
    out_path = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    # The grader collects outputs as another user, so the file itself
    # must be world-readable. Only the file is chmodded, never the
    # output directory (it is root-owned; chmod on it would fail).
    os.chmod(out_path, 0o644)


if __name__ == "__main__":
    main()
