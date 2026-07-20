from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read_manifest(platform: str) -> dict:
    path = ROOT / f".{platform}-plugin" / "plugin.json"
    return json.loads(path.read_text(encoding="utf-8"))


class BundleContractTests(unittest.TestCase):
    def test_manifest_and_marketplace_ready_shape(self) -> None:
        codex_manifest = read_manifest("codex")
        claude_manifest = read_manifest("claude")
        for field in ("name", "version", "description", "license"):
            self.assertEqual(codex_manifest[field], claude_manifest[field], field)
        self.assertEqual(codex_manifest["name"], "harness-engineering")
        self.assertEqual(codex_manifest["version"], "2.0.0")
        self.assertEqual(codex_manifest["license"], "MIT")
        self.assertEqual(len(codex_manifest["interface"]["defaultPrompt"]), 3)
        for manifest in (codex_manifest, claude_manifest):
            self.assertNotIn("apps", manifest)
            self.assertNotIn("mcpServers", manifest)

    def test_platform_references_exist(self) -> None:
        for name in ("platform-matrix.md", "platform-claude-code.md", "platform-cowork.md", "platform-codex.md"):
            self.assertTrue((ROOT / "references" / name).is_file(), name)

    def test_templates_have_no_unresolved_todo_markers(self) -> None:
        markers = ("[" + "TODO:", "__" + "REPLACE_ME__")
        for path in ROOT.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".json", ".yaml", ".py"}:
                text = path.read_text(encoding="utf-8", errors="replace")
                for marker in markers:
                    self.assertNotIn(marker, text, str(path))

    def test_skill_descriptions_are_in_frontmatter(self) -> None:
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(lines[0], "---")
            self.assertTrue(any(line.startswith("name:") for line in lines[1:5]))
            self.assertTrue(any(line.startswith("description:") for line in lines[1:6]))

    def test_skills_name_all_three_platforms(self) -> None:
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            text = path.read_text(encoding="utf-8")
            self.assertIn("Cowork", text, f"{path} does not mention Cowork")
            self.assertIn("Claude Code", text, f"{path} does not mention Claude Code")
            self.assertIn("Codex", text, f"{path} does not mention Codex")
if __name__ == "__main__":
    unittest.main()
