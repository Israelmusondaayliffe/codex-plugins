#!/usr/bin/env python3
import pathlib
import re
import sys


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: validate_prompt_blocks.py <file> [expected-count]", file=sys.stderr)
        return 2
    path = pathlib.Path(sys.argv[1]).expanduser()
    expected = int(sys.argv[2]) if len(sys.argv) == 3 else 10
    text = path.read_text(encoding="utf-8")
    blocks = re.findall(r"```[\w-]*\n.*?\n```", text, flags=re.S)
    errors = []
    if len(blocks) != expected:
        errors.append(f"expected {expected} code blocks, found {len(blocks)}")
    if "--ar" in text or "--v" in text or "--style" in text:
        errors.append("contains MidJourney-style parameter")
    if "\u2014" in text:
        errors.append("contains em-dash")
    if errors:
        print(f"FAIL {path}: " + "; ".join(errors))
        return 1
    print(f"PASS {path}: {len(blocks)} prompt blocks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
