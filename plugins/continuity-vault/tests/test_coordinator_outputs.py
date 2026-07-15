#!/usr/bin/env python3
"""Test every coordinator output contract in this plugin."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SPEC = json.loads((ROOT / "bundle-spec.json").read_text(encoding="utf-8"))


class CoordinatorOutputTests(unittest.TestCase):
    def test_templates_pass(self) -> None:
        for name in SPEC["coordinator_skills"]:
            skill = ROOT / "skills" / name
            result = subprocess.run(
                ["python3", str(skill / "scripts/validate_output.py"), str(skill / "assets/output-template.json")],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, f"{name}: {result.stdout}{result.stderr}")

    def test_empty_artifacts_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            artifact = Path(temporary_directory) / "empty.json"
            artifact.write_text("{}\n", encoding="utf-8")
            for name in SPEC["coordinator_skills"]:
                skill = ROOT / "skills" / name
                result = subprocess.run(
                    ["python3", str(skill / "scripts/validate_output.py"), str(artifact)],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertNotEqual(result.returncode, 0, f"{name} accepted an empty artifact")


if __name__ == "__main__":
    unittest.main()
