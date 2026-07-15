#!/usr/bin/env python3
"""Verify expected tokens in a clean Codex prompt input."""

import argparse
import json
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expect", action="append", required=True)
    parser.add_argument("--prompt-file", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source = str(args.prompt_file) if args.prompt_file else "codex debug prompt-input"
    if args.prompt_file:
        try:
            prompt = args.prompt_file.read_text(encoding="utf-8")
        except OSError as exc:
            print(json.dumps({"valid": False, "command_error": str(exc)}, indent=2))
            return 2
    else:
        try:
            run = subprocess.run(
                ["codex", "debug", "prompt-input"],
                check=True,
                capture_output=True,
                text=True,
            )
            prompt = run.stdout
        except (OSError, subprocess.CalledProcessError) as exc:
            print(json.dumps({"valid": False, "command_error": str(exc)}, indent=2))
            return 2
    found = [token for token in args.expect if token in prompt]
    missing = [token for token in args.expect if token not in prompt]
    result = {
        "source": source,
        "expected": args.expect,
        "found": found,
        "missing": missing,
        "valid": not missing,
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
