#!/usr/bin/env python3
"""Verify the Matt Partok Codex plugin bundle."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


PLUGIN_NAME = "matt-partok-bundled-plugin-for-knowledge-work"
EXPECTED_SKILLS = {
    "matt-ask-matt",
    "matt-code-review",
    "matt-codebase-design",
    "matt-diagnosing-bugs",
    "matt-domain-modeling",
    "matt-grill-me",
    "matt-grill-with-docs",
    "matt-grilling",
    "matt-handoff",
    "matt-implement",
    "matt-improve-codebase-architecture",
    "matt-prototype",
    "matt-research",
    "matt-resolving-merge-conflicts",
    "matt-setup-matt-pocock-skills",
    "matt-tdd",
    "matt-teach",
    "matt-to-spec",
    "matt-to-tickets",
    "matt-triage",
    "matt-wayfinder",
    "matt-writing-great-skills",
}
EXPLICIT_SKILLS = {
    "matt-grill-me",
    "matt-grill-with-docs",
    "matt-handoff",
    "matt-implement",
    "matt-improve-codebase-architecture",
    "matt-setup-matt-pocock-skills",
    "matt-teach",
    "matt-to-spec",
    "matt-to-tickets",
    "matt-triage",
    "matt-wayfinder",
    "matt-writing-great-skills",
}
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD|FIXME|FILL IN|PLACEHOLDER)\b", re.IGNORECASE)
BAD_RUNTIME_PATTERNS = {
    "Claude background command": re.compile(r"claude\s+--bg", re.IGNORECASE),
    "hard-coded Agent tool": re.compile(r"\bAgent tool\b|subagent_type=", re.IGNORECASE),
    "unprefixed Matt invocation": re.compile(
        r"/(?:ask-matt|code-review|codebase-design|diagnosing-bugs|domain-modeling|grill-me|"
        r"grill-with-docs|grilling|handoff|implement|improve-codebase-architecture|prototype|"
        r"research|resolving-merge-conflicts|setup-matt-pocock-skills|tdd|teach|to-spec|"
        r"to-tickets|triage|wayfinder|writing-great-skills)\b"
    ),
}
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def parse_frontmatter_name(text: str) -> str | None:
    match = re.search(r"(?m)^name:\s*([^\n]+)$", text)
    return match.group(1).strip().strip('"\'') if match else None


def check_links(path: Path, text: str) -> list[str]:
    findings: list[str] = []
    for target in LINK_RE.findall(text):
        clean = target.split("#", 1)[0]
        if not clean or clean.startswith(("http://", "https://", "mailto:")):
            continue
        if not (path.parent / clean).resolve().exists():
            findings.append(f"{path}: broken relative link {target}")
    return findings


def validate_bundle(root: Path) -> list[str]:
    findings: list[str] = []
    manifest_path = root / ".codex-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{manifest_path}: cannot read valid JSON: {exc}"]

    if manifest.get("name") != PLUGIN_NAME:
        findings.append(f"manifest name must be {PLUGIN_NAME}")
    if manifest.get("skills") != "./skills/":
        findings.append("manifest skills path must be ./skills/")
    if not (root / "LICENSE").is_file() or not (root / "NOTICE.md").is_file():
        findings.append("LICENSE and NOTICE.md are required")

    skill_root = root / "skills"
    actual = {path.name for path in skill_root.iterdir() if path.is_dir()}
    missing = sorted(EXPECTED_SKILLS - actual)
    extra = sorted(actual - EXPECTED_SKILLS)
    if missing:
        findings.append(f"missing skills: {', '.join(missing)}")
    if extra:
        findings.append(f"unexpected skills: {', '.join(extra)}")

    for skill_name in sorted(actual & EXPECTED_SKILLS):
        skill_dir = skill_root / skill_name
        skill_path = skill_dir / "SKILL.md"
        yaml_path = skill_dir / "agents" / "openai.yaml"
        if not skill_path.is_file():
            findings.append(f"{skill_dir}: missing SKILL.md")
            continue
        if not yaml_path.is_file():
            findings.append(f"{skill_dir}: missing agents/openai.yaml")
        text = skill_path.read_text(encoding="utf-8")
        if parse_frontmatter_name(text) != skill_name:
            findings.append(f"{skill_path}: frontmatter name must match folder")
        if PLACEHOLDER_RE.search(text):
            findings.append(f"{skill_path}: unresolved placeholder")
        for label, pattern in BAD_RUNTIME_PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{skill_path}: {label}")
        findings.extend(check_links(skill_path, text))

        if yaml_path.is_file() and skill_name in EXPLICIT_SKILLS:
            yaml_text = yaml_path.read_text(encoding="utf-8")
            if "allow_implicit_invocation: false" not in yaml_text:
                findings.append(f"{yaml_path}: explicit skill must disable implicit invocation")

    for markdown_path in root.rglob("*.md"):
        text = markdown_path.read_text(encoding="utf-8")
        if "\u2014" in text:
            findings.append(f"{markdown_path}: em dash found")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).parents[1])
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    findings = validate_bundle(root)
    if findings:
        print(f"FAIL: {len(findings)} finding(s)")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print(f"PASS: {PLUGIN_NAME} contains {len(EXPECTED_SKILLS)} validated skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
