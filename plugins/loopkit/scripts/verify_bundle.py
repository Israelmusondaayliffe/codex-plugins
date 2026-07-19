#!/usr/bin/env python3
"""Verify the LoopKit plugin bundle without third-party dependencies."""

from __future__ import annotations

import json
import py_compile
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "loopkit",
    "loop-designer",
    "loop-runner",
    "loop-verifier",
    "loop-resumer",
    "loop-scheduler",
    "loop-doctor",
}
REQUIRED_SCRIPTS = {
    "loopkit_core.py",
    "init_run.py",
    "validate_contract.py",
    "transition_run.py",
    "validate_receipt.py",
    "record_receipt.py",
    "checkpoint_run.py",
    "write_schedule.py",
    "doctor_run.py",
    "verify_bundle.py",
}
# Dual-host port (0.2.0): ".claude/" and "CLAUDE.md" are no longer forbidden;
# docs now name both host homes (~/.claude and ${CODEX_HOME:-~/.codex}).
FORBIDDEN_PORTABILITY_MARKERS = ("claude -p", "run.sh")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def frontmatter_name(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^---\n.*?^name:\s*([^\n]+).*?^---$", text, flags=re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else None


def main() -> int:
    errors: list[str] = []
    manifest_path = ROOT / ".codex-plugin" / "plugin.json"
    bundle_path = ROOT / "bundle-spec.json"
    hooks_path = ROOT / "hooks" / "hooks.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
        hooks = json.loads(hooks_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"bundle invalid: {exc}")
        return 1
    if manifest.get("name") != "loopkit":
        fail(errors, "manifest name must be loopkit")
    if manifest.get("version") != bundle.get("version"):
        fail(errors, "manifest and bundle-spec versions differ")
    claude_manifest_path = ROOT / ".claude-plugin" / "plugin.json"
    claude_hooks_path = ROOT / "hooks" / "claude-hooks.json"
    try:
        claude_manifest = json.loads(claude_manifest_path.read_text(encoding="utf-8"))
        claude_hooks = json.loads(claude_hooks_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, f"claude bundle artifacts unreadable: {exc}")
        claude_manifest, claude_hooks = {}, {}
    for field in ("name", "version", "description", "license"):
        if manifest.get(field) != claude_manifest.get(field):
            fail(errors, f"manifest field {field} differs between .codex-plugin and .claude-plugin")
    if claude_manifest.get("hooks") != "./hooks/claude-hooks.json":
        fail(errors, "claude manifest must wire hooks to ./hooks/claude-hooks.json")
    if set(claude_hooks.get("hooks", {})) != {"PreCompact", "SessionStart"}:
        fail(errors, "claude-hooks.json must define exactly PreCompact and SessionStart")
    if "hooks" in manifest:
        fail(errors, "manifest must use default hooks/hooks.json discovery")
    prompts = manifest.get("interface", {}).get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        fail(errors, "interface.defaultPrompt must contain one to three prompts")
    skill_dirs = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
    if skill_dirs != EXPECTED_SKILLS:
        fail(errors, f"skill folders differ: expected {sorted(EXPECTED_SKILLS)}, found {sorted(skill_dirs)}")
    for name in EXPECTED_SKILLS:
        skill_file = ROOT / "skills" / name / "SKILL.md"
        if not skill_file.exists():
            fail(errors, f"missing {skill_file.relative_to(ROOT)}")
        elif frontmatter_name(skill_file) != name:
            fail(errors, f"frontmatter name mismatch for {name}")
    script_names = {path.name for path in (ROOT / "scripts").glob("*.py")}
    missing_scripts = REQUIRED_SCRIPTS - script_names
    if missing_scripts:
        fail(errors, f"missing scripts: {sorted(missing_scripts)}")
    if set(hooks.get("hooks", {})) != {"PreCompact", "SessionStart"}:
        fail(errors, "hooks must contain only PreCompact and SessionStart")
    all_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix in {".md", ".json", ".py"}
        and path.resolve() != Path(__file__).resolve()
    )
    if "[TODO:" in all_text:
        fail(errors, "TODO placeholders remain")
    for marker in FORBIDDEN_PORTABILITY_MARKERS:
        if marker in all_text:
            fail(errors, f"non-Codex portability marker found: {marker}")
    for script in list((ROOT / "scripts").glob("*.py")) + list((ROOT / "hooks").glob("*.py")):
        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError as exc:
            fail(errors, f"python compile failed for {script.name}: {exc.msg}")
    if set(bundle.get("skills", [])) != EXPECTED_SKILLS or len(bundle.get("skills", [])) != len(EXPECTED_SKILLS):
        fail(errors, "bundle-spec skills must be complete and unique")
    if errors:
        print("bundle invalid")
        for error in errors:
            print(f"- {error}")
        return 1
    print("bundle valid: 7 skills, 2 hooks, deterministic state core")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
