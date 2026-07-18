import tempfile
import unittest
from pathlib import Path

from helpers import PLUGIN_ROOT

from citizen_forge.errors import PolicyError, StorageError
from citizen_forge.policy import load_policy
from citizen_forge.storage import project_lock


class FailureTests(unittest.TestCase):
    def test_missing_policy_blocks(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(PolicyError):
                load_policy(Path(temp) / "missing.json")

    def test_unknown_policy_version_shape_blocks(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "policy.json"
            path.write_text('{"version": null}', encoding="utf-8")
            with self.assertRaises(PolicyError):
                load_policy(path)

    def test_stale_lock_requires_review(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            lock = root / ".write.lock"
            lock.write_text("1", encoding="utf-8")
            with self.assertRaises(StorageError):
                with project_lock(root, stale_after=0):
                    pass
