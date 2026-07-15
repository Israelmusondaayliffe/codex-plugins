#!/usr/bin/env python3
"""Report live companion availability without installing optional plugins."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    spec = json.loads((root / "bundle-spec.json").read_text(encoding="utf-8"))
    proc = subprocess.run(["codex", "plugin", "list", "--json"], capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        print(json.dumps({"valid": False, "error": proc.stderr.strip()}, indent=2))
        return 2
    installed = {item.get("name"): item for item in json.loads(proc.stdout).get("installed", [])}
    results = []
    required_failures = []
    for companion in spec.get("companions", []):
        item = installed.get(companion["name"])
        available = bool(item and item.get("installed") and item.get("enabled"))
        results.append({
            "name": companion["name"],
            "required": bool(companion.get("required", False)),
            "available": available,
            "version": item.get("version") if item else None,
            "purpose": companion.get("purpose"),
        })
        if companion.get("required") and not available:
            required_failures.append(companion["name"])
    output = {
        "valid": not required_failures,
        "plugin": spec["plugin"],
        "required_failures": required_failures,
        "companions": results,
    }
    print(json.dumps(output, indent=2))
    return 1 if required_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
