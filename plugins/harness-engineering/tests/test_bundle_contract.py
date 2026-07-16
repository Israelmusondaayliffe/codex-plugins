from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class BundleContractTests(unittest.TestCase):
    def test_manifest_and_marketplace_ready_shape(self) -> None:
        manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "harness-engineering")
        self.assertEqual(manifest["version"], "1.0.0")
        self.assertEqual(manifest["license"], "MIT")
        self.assertEqual(len(manifest["interface"]["defaultPrompt"]), 3)
        self.assertNotIn("apps", manifest)
        self.assertNotIn("mcpServers", manifest)

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


if __name__ == "__main__":
    unittest.main()
