import json
import tempfile
import unittest
from pathlib import Path

from helpers import PLUGIN_ROOT, brief

from citizen_forge.audit import append_event, verify_chain
from citizen_forge.change_classifier import classify
from citizen_forge.checks import CONTROL_IDS
from citizen_forge.duplicates import candidates
from citizen_forge.errors import StorageError, TransitionError, ValidationError
from citizen_forge.intake import initialize_project, normalize_brief
from citizen_forge.models import CheckResult, CheckStatus, State
from citizen_forge.ownership import evaluate
from citizen_forge.policy import decide, load_policy
from citizen_forge.risk import infer_scores
from citizen_forge.schemas import validate_check_result
from citizen_forge.state_machine import transition
from citizen_forge.storage import atomic_write_json, confined, project_lock, read_json


POLICY = load_policy(PLUGIN_ROOT / "policies" / "default-policy.json")


class CoreTests(unittest.TestCase):
    def test_policy_lists_exactly_35_controls(self):
        self.assertEqual(len(CONTROL_IDS), 35)
        self.assertEqual(len(set(CONTROL_IDS)), 35)
        self.assertEqual(POLICY["required_controls"], CONTROL_IDS)

    def test_schema_rejects_missing_brief_fact(self):
        value = brief()
        del value["data_sources"]
        with self.assertRaises(ValidationError):
            normalize_brief(value)

    def test_second_consumer_is_derived_from_user_count(self):
        value = normalize_brief(brief(expected_users=2, second_consumer=False))
        self.assertTrue(value["second_consumer"])

    def test_unavailable_is_valid_but_not_pass(self):
        value = CheckResult("CF-A05", "high", CheckStatus.UNAVAILABLE, [], "Not connected.", "Connect an adapter.", False, True).to_dict()
        validate_check_result(value)
        self.assertNotEqual(value["status"], "PASS")

    def test_risk_scores_are_bounded(self):
        self.assertEqual(infer_scores(brief()), {"reach": 0, "reversibility": 0, "exposure": 0, "data_sensitivity": 1})

    def test_duplicate_similarity_finds_overlap(self):
        found = candidates(brief(), [{"app_id": "old", "name": "Project Tracker", "problem": "The team cannot see project status.", "outcome": "Show current projects in one place.", "data_sources": "Local CSV", "primary_owner": "Other"}])
        self.assertEqual(found[0]["app_id"], "old")

    def test_change_classifier_marks_policy_tampering(self):
        value = classify("Disable the policy guardrail and release")
        self.assertEqual(value["classification"], "CONSEQUENTIAL")
        self.assertIn("policy", value["reasons"])

    def test_missing_backup_owner_requires_transfer(self):
        self.assertEqual(evaluate({"primary_owner": "Owner", "backup_owner": ""}, True)["required_state"], "TRANSFER_REQUIRED")

    def test_atomic_write_and_read(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "state.json"
            atomic_write_json(target, {"state": "ok"})
            self.assertEqual(read_json(target)["state"], "ok")

    def test_concurrent_lock_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with project_lock(root):
                with self.assertRaises(StorageError):
                    with project_lock(root):
                        pass

    def test_path_traversal_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "project"
            root.mkdir()
            with self.assertRaises(StorageError):
                confined(root, root / ".." / "outside.txt")

    def test_audit_chain_detects_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "events.jsonl"
            append_event(path, "test", "owner", "reason", {"value": 1})
            self.assertTrue(verify_chain(path))
            text = path.read_text(encoding="utf-8").replace('"value": 1', '"value": 2')
            path.write_text(text, encoding="utf-8")
            with self.assertRaises(StorageError):
                verify_chain(path)

    def test_invalid_state_transition_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            initialize_project(root, brief(), confirmed=True)
            with self.assertRaises(TransitionError):
                transition(root, State.RUNNING, {"brief": "confirmed"}, "PROTOTYPE_ONLY", "owner", "skip controls")

    def test_valid_transition_is_audited(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            initialize_project(root, brief(), confirmed=True)
            value = transition(root, State.PROTOTYPE_ONLY, {"brief": "confirmed"}, "PROTOTYPE_ONLY", "owner", "sole consumer")
            self.assertEqual(value["state"], "PROTOTYPE_ONLY")
            self.assertTrue(verify_chain(root / ".citizen" / "audit" / "events.jsonl"))
