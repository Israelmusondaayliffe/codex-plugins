#!/usr/bin/env python3
"""Report live companion-plugin availability for a personal plugin bundle."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    spec = json.loads((root / "bundle-spec.json").read_text(encoding="utf-8"))
    proc = subprocess.run(
        ["codex", "plugin", "list", "--json"],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print(json.dumps({"valid": False, "error": proc.stderr.strip()}, indent=2))
        return 2
    listing = json.loads(proc.stdout)
    installed = {item.get("name"): item for item in listing.get("installed", [])}
    results = []
    required_failures = []
    for companion in spec.get("companions", []):
        name = companion["name"] if isinstance(companion, dict) else companion
        required = bool(companion.get("required", False)) if isinstance(companion, dict) else False
        item = installed.get(name)
        available = bool(item and item.get("installed") and item.get("enabled"))
        result = {
            "name": name,
            "required": required,
            "available": available,
            "installed": bool(item and item.get("installed")),
            "enabled": bool(item and item.get("enabled")),
            "version": item.get("version") if item else None,
            "purpose": companion.get("purpose") if isinstance(companion, dict) else None,
        }
        results.append(result)
        if required and not available:
            required_failures.append(name)
    output = {
        "valid": not required_failures,
        "plugin": spec.get("plugin"),
        "required_failures": required_failures,
        "companions": results,
    }
    print(json.dumps(output, indent=2))
    return 1 if required_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
