#!/usr/bin/env python3
"""Checkpoint-only hooks for LoopKit compaction and resume events."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


PLUGIN_ROOT = Path(os.environ.get("PLUGIN_ROOT", Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))

from loopkit_core import LoopKitError, newest_active_run, refresh_checkpoint  # noqa: E402


def read_payload() -> dict:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    data = json.loads(raw)
    return data if isinstance(data, dict) else {}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in {"pre-compact", "session-start"}:
        return 0
    try:
        payload = read_payload()
        workspace = Path(payload.get("cwd") or Path.cwd()).resolve()
        run_dir = newest_active_run(workspace)
        if run_dir is None:
            return 0
        checkpoint = refresh_checkpoint(run_dir)
        if sys.argv[1] == "pre-compact":
            return 0
        content = checkpoint.read_text(encoding="utf-8")
        if len(content.encode("utf-8")) > 4096:
            return 0
        response = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": content,
            }
        }
        sys.stdout.write(json.dumps(response))
    except (LoopKitError, OSError, ValueError, json.JSONDecodeError):
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
