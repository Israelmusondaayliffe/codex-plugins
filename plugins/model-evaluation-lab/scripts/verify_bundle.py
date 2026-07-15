#!/usr/bin/env python3
"""Verify a personal plugin bundle against its declared contract."""

from __future__ import annotations

import json
import re
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors: list[str] = []
    try:
        manifest = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        spec = json.loads((root / "bundle-spec.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, indent=2))
        return 2
    plugin_name = manifest.get("name")
    directory_names = {root.name, root.parent.name}
    if spec.get("plugin") != plugin_name or plugin_name not in directory_names:
        errors.append("plugin name must match the source or cache directory")
    if manifest.get("version") != spec.get("version"):
        errors.append("manifest and bundle spec versions differ")
    expected = set(spec.get("skills", []))
    actual = {path.parent.name for path in (root / "skills").glob("*/SKILL.md")}
    if actual != expected:
        errors.append(f"skill set mismatch: missing={sorted(expected - actual)} extra={sorted(actual - expected)}")
    for name in sorted(actual):
        skill_file = root / "skills" / name / "SKILL.md"
        text = skill_file.read_text(encoding="utf-8")
        match = re.search(r"^name:\s*([a-z0-9-]+)\s*$", text, re.MULTILINE)
        if not match or match.group(1) != name:
            errors.append(f"{name}: frontmatter name does not match directory")
    for name in spec.get("coordinator_skills", []):
        skill_root = root / "skills" / name
        for part in ("scripts", "references", "assets"):
            directory = skill_root / part
            if not directory.is_dir() or not any(directory.iterdir()):
                errors.append(f"{name}: missing non-empty {part} directory")
        for path in skill_root.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".py", ".json"}:
                content = path.read_text(encoding="utf-8", errors="replace")
                if "[TODO" in content or "template-placeholder" in content:
                    errors.append(f"{name}: placeholder remains in {path.relative_to(root)}")
    prompts = manifest.get("interface", {}).get("defaultPrompt")
    if not isinstance(prompts, list) or not prompts:
        errors.append("interface.defaultPrompt must be a non-empty list")
    for case in spec.get("routing_cases", []):
        if case.get("expected_skill") not in expected:
            errors.append(f"routing case expects an unbundled skill: {case.get('expected_skill')}")
            continue
        evidence_path = root / str(case.get("evidence_file", ""))
        evidence = str(case.get("evidence_contains", ""))
        if not evidence_path.is_file() or evidence not in evidence_path.read_text(encoding="utf-8", errors="replace"):
            errors.append(f"routing evidence failed: {case.get('evidence_file')} | {evidence}")
    result = {
        "valid": not errors,
        "plugin": plugin_name,
        "version": manifest.get("version"),
        "skill_count": len(actual),
        "coordinator_skill_count": len(spec.get("coordinator_skills", [])),
        "routing_case_count": len(spec.get("routing_cases", [])),
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
