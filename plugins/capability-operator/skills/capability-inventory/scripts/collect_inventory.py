#!/usr/bin/env python3
"""Collect a read-only Codex capability inventory."""

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def skill_records(root: Path, layer: str) -> list[dict]:
    records = []
    if not root.exists():
        return records
    for skill_file in sorted(root.glob("*/SKILL.md")):
        records.append({
            "name": skill_file.parent.name,
            "layer": layer,
            "path": str(skill_file.parent),
            "skill_sha256": hashlib.sha256(skill_file.read_bytes()).hexdigest(),
        })
    return records


def plugin_records(root: Path, errors: list[str]) -> list[dict]:
    records = []
    if not root.exists():
        return records
    for manifest in sorted(root.glob("*/.codex-plugin/plugin.json")):
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{manifest}: {exc}")
            continue
        skills = sorted(path.parent.name for path in manifest.parent.parent.glob("skills/*/SKILL.md"))
        records.append({
            "name": data.get("name", manifest.parent.parent.name),
            "version": data.get("version"),
            "path": str(manifest.parent.parent),
            "skills": skills,
        })
    return records


def installed_plugins(errors: list[str]) -> list[dict]:
    try:
        run = subprocess.run(
            ["codex", "plugin", "list", "--json"],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(run.stdout).get("installed", [])
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        errors.append(f"codex plugin list failed: {exc}")
        return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex-skills", type=Path, default=Path.home() / ".codex/skills")
    parser.add_argument("--agent-skills", type=Path, default=Path.home() / ".agents/skills")
    parser.add_argument("--plugins", type=Path, default=Path.home() / "plugins")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    errors: list[str] = []
    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "roots": {
            "codex_skills": str(args.codex_skills),
            "agent_skills": str(args.agent_skills),
            "plugins": str(args.plugins),
        },
        "loose_skills": (
            skill_records(args.codex_skills, "codex")
            + skill_records(args.agent_skills, "agents")
        ),
        "plugin_sources": plugin_records(args.plugins, errors),
        "installed_plugins": installed_plugins(errors),
        "errors": errors,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "errors": len(errors)}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
