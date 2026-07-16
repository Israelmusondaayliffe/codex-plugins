#!/usr/bin/env python3
"""Verify the Harness Engineering source bundle."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


EXPECTED_SKILLS = {
    "agents-md-engineer",
    "harness-audit",
    "harness-builder",
    "harness-engineering",
    "harness-interview",
    "harness-maintainer",
    "harness-planner",
    "harness-runner",
    "harness-verifier",
    "model-prompt-engineer",
    "plugin-engineer",
    "skill-engineer",
}
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py"}


def fail(message: str) -> None:
    raise RuntimeError(message)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]).resolve()
    manifest_path = root / ".codex-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("name") != "harness-engineering" or manifest.get("version") != "1.0.0":
        fail("manifest identity or version is incorrect")
    if manifest.get("author", {}).get("name") != "Israel Ayliffe" or manifest.get("license") != "MIT":
        fail("publisher or license metadata is incorrect")
    if "apps" in manifest or "mcpServers" in manifest or "hooks" in manifest:
        fail("manifest declares a component that v1 does not ship")

    actual = {path.parent.name for path in (root / "skills").glob("*/SKILL.md")}
    if actual != EXPECTED_SKILLS:
        fail(f"skill set mismatch: expected {sorted(EXPECTED_SKILLS)}, got {sorted(actual)}")

    validator = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    validations = []
    for name in sorted(EXPECTED_SKILLS):
        skill_dir = root / "skills" / name
        result = subprocess.run([sys.executable, str(validator), str(skill_dir)], capture_output=True, text=True)
        if result.returncode != 0:
            fail(f"skill validation failed for {name}: {result.stdout}{result.stderr}")
        metadata = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
        if f"${name}" not in metadata:
            fail(f"default prompt does not name ${name}")
        validations.append(name)

    for path in root.rglob("*"):
        if path.is_symlink():
            fail(f"bundle contains a symbolic link: {path}")
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            text = path.read_text(encoding="utf-8", errors="replace")
            markers = ("[" + "TODO:", "__" + "REPLACE_ME__")
            if any(marker in text for marker in markers):
                fail(f"placeholder remains in {path}")
            if "\u2014" in text:
                fail(f"em dash remains in {path}")
            personal_path = "/Users/" + "israelayliffe"
            if personal_path in text:
                fail(f"personal absolute path remains in {path}")

    required = [
        root / "README.md",
        root / "LICENSE",
        root / "PRIVACY.md",
        root / "SECURITY.md",
        root / "TERMS.md",
        root / "scripts" / "harnessctl.py",
        root / "schemas" / "profile.schema.json",
        root / "schemas" / "operations.schema.json",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        fail(f"required files missing: {missing}")
    print(json.dumps({"plugin": "harness-engineering", "version": "1.0.0", "skills_validated": validations}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"bundle verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
