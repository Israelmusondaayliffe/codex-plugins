#!/usr/bin/env python3
"""Verify personal installation and source-cache parity."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


EXCLUDES = {".DS_Store", "__pycache__"}


def file_map(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in root.rglob("*"):
        if not path.is_file() or any(part in EXCLUDES for part in path.parts):
            continue
        rel = path.relative_to(root).as_posix()
        result[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def main() -> int:
    source = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]).resolve()
    manifest = json.loads((source / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    version = manifest["version"]
    listing = subprocess.run(["codex", "plugin", "list", "--json"], check=True, capture_output=True, text=True)
    installed = [item for item in json.loads(listing.stdout).get("installed", []) if item.get("name") == "harness-engineering" and item.get("marketplaceName") == "personal"]
    if len(installed) != 1 or not installed[0].get("enabled") or installed[0].get("version") != version:
        raise RuntimeError("personal plugin listing does not match the source manifest")
    cache = Path.home() / ".codex" / "plugins" / "cache" / "personal" / "harness-engineering" / version
    if not cache.is_dir():
        raise RuntimeError(f"installed cache is missing: {cache}")
    source_files = file_map(source)
    cache_files = file_map(cache)
    if source_files != cache_files:
        missing = sorted(set(source_files) - set(cache_files))
        extra = sorted(set(cache_files) - set(source_files))
        changed = sorted(path for path in set(source_files) & set(cache_files) if source_files[path] != cache_files[path])
        raise RuntimeError(f"source-cache mismatch missing={missing} extra={extra} changed={changed}")
    print(json.dumps({"plugin": "harness-engineering", "version": version, "files": len(source_files), "parity": True}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"install verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
