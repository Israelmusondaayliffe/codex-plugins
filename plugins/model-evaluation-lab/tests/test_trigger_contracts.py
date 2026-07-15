#!/usr/bin/env python3
"""Check trigger coverage and target ownership."""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class TriggerContractTests(unittest.TestCase):
    def test_trigger_set_is_balanced_and_owned(self) -> None:
        data = json.loads((ROOT / "tests/trigger-cases.json").read_text(encoding="utf-8"))
        bundled = {path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertGreaterEqual(len(data["should_trigger"]) + len(data["should_not_trigger"]), 10)
        self.assertGreaterEqual(len(data["should_trigger"]), 5)
        self.assertGreaterEqual(len(data["should_not_trigger"]), 5)
        for case in data["should_trigger"]:
            self.assertIn(case["expected_skill"], bundled)
            self.assertGreater(len(case["query"].split()), 6)
        for case in data["should_not_trigger"]:
            self.assertTrue(case["reason"].strip())


if __name__ == "__main__":
    unittest.main()
