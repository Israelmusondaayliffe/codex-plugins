#!/usr/bin/env python3
"""Tests for the Matt Partok plugin bundle verifier."""

from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).parents[1]
SCRIPT_PATH = PLUGIN_ROOT / "scripts" / "verify_bundle.py"
SPEC = importlib.util.spec_from_file_location("verify_bundle", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {SCRIPT_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class VerifyBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="matt-partok-plugin-")
        self.bundle = Path(self.temp_dir.name) / "bundle"
        shutil.copytree(PLUGIN_ROOT, self.bundle)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_live_bundle_passes(self) -> None:
        self.assertEqual(MODULE.validate_bundle(self.bundle), [])

    def test_extra_skill_is_rejected(self) -> None:
        extra = self.bundle / "skills" / "unprefixed-skill"
        extra.mkdir()
        findings = MODULE.validate_bundle(self.bundle)
        self.assertTrue(any("unexpected skills" in finding for finding in findings))

    def test_bad_frontmatter_name_is_rejected(self) -> None:
        path = self.bundle / "skills" / "matt-grill-me" / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace("name: matt-grill-me", "name: grill-me"), encoding="utf-8")
        findings = MODULE.validate_bundle(self.bundle)
        self.assertTrue(any("frontmatter name" in finding for finding in findings))

    def test_unprefixed_invocation_is_rejected(self) -> None:
        path = self.bundle / "skills" / "matt-ask-matt" / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nRun /to-spec.\n", encoding="utf-8")
        findings = MODULE.validate_bundle(self.bundle)
        self.assertTrue(any("unprefixed Matt invocation" in finding for finding in findings))


if __name__ == "__main__":
    unittest.main()
