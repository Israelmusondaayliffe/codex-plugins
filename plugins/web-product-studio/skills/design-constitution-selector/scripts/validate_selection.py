#!/usr/bin/env python3
"""Validate a design constitution selection."""

import json
import sys
from pathlib import Path

ALLOWED = {
    "design-taste-frontend", "gpt-taste", "hallmark", "high-end-visual-design",
    "industrial-brutalist-ui", "minimalist-ui", "stitch-design-taste", None,
}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_selection.py SELECTION.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2
    errors = []
    if data.get("selected") not in ALLOWED:
        errors.append("selected is not an allowed constitution or null")
    if not isinstance(data.get("evidence"), list) or not data["evidence"]:
        errors.append("evidence must be a non-empty list")
    if not isinstance(data.get("rationale"), str) or not data["rationale"].strip():
        errors.append("rationale must be non-empty")
    if not isinstance(data.get("rejected"), list):
        errors.append("rejected must be a list")
    print(json.dumps({"valid": not errors, "selected": data.get("selected"), "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
