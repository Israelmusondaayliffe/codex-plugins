#!/usr/bin/env python3
"""Test coordinator output contracts and deterministic normalization."""

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
            command = [
                "python3",
                str(skill / "scripts/validate_output.py"),
                str(skill / "assets/output-template.json"),
            ]
            result = subprocess.run(
                command, capture_output=True, text=True, check=False
            )
            self.assertEqual(result.returncode, 0, f"{name}: {result.stdout}{result.stderr}")

    def test_empty_artifacts_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            artifact = Path(temporary_directory) / "empty.json"
            artifact.write_text("{}\n", encoding="utf-8")
            for name in SPEC["coordinator_skills"]:
                skill = ROOT / "skills" / name
                command = [
                    "python3",
                    str(skill / "scripts/validate_output.py"),
                    str(artifact),
                ]
                result = subprocess.run(
                    command, capture_output=True, text=True, check=False
                )
                self.assertNotEqual(result.returncode, 0, f"{name} accepted an empty artifact")

    def test_raw_results_normalize_and_validate(self) -> None:
        runner = ROOT / "skills/benchmark-runner"
        with tempfile.TemporaryDirectory() as temporary_directory:
            normalized = Path(temporary_directory) / "normalized.json"
            command = [
                "python3",
                str(runner / "scripts/normalize_results.py"),
                str(ROOT / "tests/fixtures/raw-support-routing.json"),
                str(normalized),
            ]
            result = subprocess.run(
                command, capture_output=True, text=True, check=False
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            validation = subprocess.run(
                [
                    "python3",
                    str(runner / "scripts/validate_output.py"),
                    str(normalized),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
            data = json.loads(normalized.read_text(encoding="utf-8"))
            self.assertEqual(data["execution_status"], "complete")
            self.assertEqual(len(data["aggregates"]), 2)


if __name__ == "__main__":
    unittest.main()
