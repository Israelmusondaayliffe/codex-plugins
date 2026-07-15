#!/usr/bin/env python3
"""Validate a plugin portfolio ledger."""

import json
import sys
from pathlib import Path

STATES = {"planned", "built", "installed", "verified", "deprecated", "retired"}
REQUIRED = ("name", "owner", "purpose", "version", "owned_skills", "companions", "verification", "status")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_portfolio.py PORTFOLIO.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2
    errors = []
    plugins = data.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        errors.append("plugins must be a non-empty list")
        plugins = []
    names = set()
    for index, plugin in enumerate(plugins):
        if not isinstance(plugin, dict):
            errors.append(f"plugins[{index}] must be an object")
            continue
        for field in REQUIRED:
            if field not in plugin:
                errors.append(f"plugins[{index}] missing {field}")
        name = plugin.get("name")
        if not isinstance(name, str) or not name or name in names:
            errors.append(f"plugins[{index}].name must be non-empty and unique")
        names.add(name)
        if plugin.get("status") not in STATES:
            errors.append(f"plugins[{index}].status is invalid")
        for field in ("owned_skills", "companions", "verification"):
            if not isinstance(plugin.get(field), list):
                errors.append(f"plugins[{index}].{field} must be a list")
    print(json.dumps({"valid": not errors, "plugin_count": len(plugins), "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
