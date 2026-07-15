#!/usr/bin/env python3
"""Validate a writing-quality routing record."""

import json
import sys
from pathlib import Path

ALLOWED = {"intent-architecture", "rewrite", "detect-only", "validation"}


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
    if data.get("route") not in ALLOWED:
        errors.append("route must be one allowed value")
    for field in ("operation", "rationale"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"{field} must be a non-empty string")
    if not isinstance(data.get("claim_check_required"), bool):
        errors.append("claim_check_required must be boolean")
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        return 1
    print(json.dumps({"valid": True, "route": data["route"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
