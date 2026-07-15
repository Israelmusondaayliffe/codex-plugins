#!/usr/bin/env python3
import pathlib
import re
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_video_prompt.py <file>", file=sys.stderr)
        return 2
    path = pathlib.Path(sys.argv[1]).expanduser()
    text = path.read_text(encoding="utf-8")
    blocks = re.findall(r"```[\w-]*\n.*?\n```", text, flags=re.S)
    errors = []
    if not blocks:
        errors.append("no shot prompt code blocks found")
    if "\u2014" in text:
        errors.append("contains em-dash")
    if re.search(r"\b(stunning|breathtaking|game-changing)\b", text, flags=re.I):
        errors.append("contains hype language")
    if errors:
        print(f"FAIL {path}: " + "; ".join(errors))
        return 1
    print(f"PASS {path}: {len(blocks)} shot prompt blocks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
