#!/usr/bin/env python3
"""Validate a video production route."""

import json
import sys
from pathlib import Path

ROUTES = {
    "faceless-explainer", "product-launch", "pr-story", "website-capture",
    "music-visualization", "slideshow", "motion-graphics", "general-video",
}
RUNTIMES = {"hyperframes", "remotion", "prompt-only", "external"}


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
    if data.get("runtime") not in RUNTIMES:
        errors.append("runtime is invalid")
    for field in ("duration_seconds", "width", "height"):
        if not isinstance(data.get(field), int) or data[field] <= 0:
            errors.append(f"{field} must be a positive integer")
    if not isinstance(data.get("skills"), list) or not data["skills"]:
        errors.append("skills must be a non-empty list")
    for field in ("objective", "rationale"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"{field} must be non-empty")
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
