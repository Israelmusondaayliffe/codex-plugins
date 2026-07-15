#!/usr/bin/env python3
"""Tests for the research-bundle verifier."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "verify_research_bundle.py"
SPEC = importlib.util.spec_from_file_location("verify_research_bundle", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {SCRIPT_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class VerifyResearchBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="research-bundle-test-")
        self.bundle = Path(self.temp_dir.name) / "bundle"
        MODULE.write_valid_fixture(self.bundle)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_valid_research_bundle_passes(self) -> None:
        self.assertEqual(MODULE.validate_bundle(self.bundle, "research"), [])

    def test_placeholder_is_rejected(self) -> None:
        (self.bundle / "work-brief.md").write_text("# Work Brief\n\nTBD\n", encoding="utf-8")
        findings = MODULE.validate_bundle(self.bundle, "research")
        self.assertTrue(any("placeholder" in finding.message for finding in findings))

    def test_unknown_source_id_is_rejected(self) -> None:
        claim_path = self.bundle / "claim-ledger.md"
        content = claim_path.read_text(encoding="utf-8").replace("S1 | high", "S404 | high")
        claim_path.write_text(content, encoding="utf-8")
        findings = MODULE.validate_bundle(self.bundle, "research")
        self.assertTrue(any("unknown source ID 'S404'" in finding.message for finding in findings))

    def test_deliverable_profile_requires_delivery_files(self) -> None:
        findings = MODULE.validate_bundle(self.bundle, "deliverable")
        missing = {finding.path.name for finding in findings if finding.message == "required file is missing"}
        self.assertEqual(missing, {"deliverable.md", "review.md", "delivery-note.md"})


if __name__ == "__main__":
    unittest.main()
