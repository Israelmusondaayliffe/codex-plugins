#!/usr/bin/env python3
"""Validate a web product route."""

import json
import sys
from pathlib import Path

ROUTES = {"greenfield", "redesign", "image-first", "targeted-fix", "quality-assurance"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_route.py ROUTE.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2
    errors = []
    if data.get("route") not in ROUTES:
        errors.append("route is invalid")
    for field in ("objective", "acceptance_flow", "rationale"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"{field} must be non-empty")
    constitution = data.get("design_constitution")
    if constitution is not None and (not isinstance(constitution, str) or not constitution.strip()):
        errors.append("design_constitution must be a non-empty string or null")
    if not isinstance(data.get("implementation_skills"), list):
        errors.append("implementation_skills must be a list")
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
