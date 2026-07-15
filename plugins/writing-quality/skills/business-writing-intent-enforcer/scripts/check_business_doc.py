#!/usr/bin/env python3
import pathlib
import sys

SIGNALS = ("recommendation", "decision", "risk", "next", "assumption", "open question")


def main():
    if len(sys.argv) != 2:
        print("Usage: check_business_doc.py <file>", file=sys.stderr)
        return 2
    path = pathlib.Path(sys.argv[1]).expanduser()
    text = path.read_text(encoding="utf-8").lower()
    found = [signal for signal in SIGNALS if signal in text]
    if len(found) >= 3:
        print(f"PASS {path}: found {', '.join(found)}")
        return 0
    print(f"WARN {path}: weak business-intent signals, found {', '.join(found) or 'none'}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
