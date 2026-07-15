import importlib.util
import sys
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
CORE_PATH = PLUGIN_ROOT / "skills" / "proofloop-run" / "scripts" / "proofloop_core.py"
SPEC = importlib.util.spec_from_file_location("proofloop_core_under_test", CORE_PATH)
CORE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CORE
SPEC.loader.exec_module(CORE)


ZERO_DIGEST = "0" * 64


def valid_contract():
    return {
        "contract_version": "1.0",
        "task_id": "task-1",
        "goal": "Produce a verified artifact",
        "task_family": "structured_artifact",
        "eligibility_class": "objective",
        "success_criteria": [
            {
                "criterion_id": "c1",
                "statement": "Artifact passes validation",
                "evidence_minimum": "E3",
            }
        ],
        "advisory_retrieval": {"enabled": False, "selections": []},
        "aggregation_rule": "all_required",
        "verifiers": [
            {
                "verifier_id": "validator",
                "verifier_version": "1.0",
                "verifier_digest": ZERO_DIGEST,
                "adapter_id": "local",
                "criterion_ids": ["c1"],
                "configuration_digest": ZERO_DIGEST,
                "test_or_data_digests": [],
                "boundary": "contract_pinned",
            }
        ],
        "budgets": {
            "inner_drafts_max": 3,
            "execution_attempts_max": 2,
            "verifier_executions_max": 2,
            "tool_calls": 20,
            "wall_time_minutes": 30,
            "memory_writes": 2,
        },
        "blocked_stop": "Stop when required evidence cannot be produced",
        "privacy_class": "internal",
        "storage_profile": "ephemeral",
    }


def valid_record():
    return {
        "schema_version": "1.0",
        "record_id": "record-1",
        "record_type": "candidate_lesson",
        "status": "candidate",
        "created_at": "2026-07-13T00:00:00Z",
        "task_id": "task-1",
        "privacy_class": "internal",
        "scope": {"project": "proofloop"},
        "content": {"key": "method", "value": "verify first"},
        "provenance": ["test"],
    }


class ProofLoopTests(unittest.TestCase):
    def test_01_canonical_json_sorts_keys(self):
        self.assertEqual(CORE.canonical_json({"b": 2, "a": 1}), '{"a":1,"b":2}')

    def test_02_canonical_json_rejects_floats(self):
        with self.assertRaises(ValueError):
            CORE.canonical_json({"value": 1.5})

    def test_03_generate_id_is_deterministic(self):
        first = CORE.generate_id({"namespace": "x", "content": {"a": 1}})
        second = CORE.generate_id({"namespace": "x", "content": {"a": 1}})
        self.assertEqual(first, second)

    def test_04_valid_contract_passes(self):
        self.assertTrue(CORE.validate_contract(valid_contract())["valid"])

    def test_05_contract_missing_field_fails(self):
        contract = valid_contract()
        del contract["goal"]
        self.assertFalse(CORE.validate_contract(contract)["valid"])

    def test_06_invalid_task_family_fails(self):
        contract = valid_contract()
        contract["task_family"] = "unknown"
        self.assertFalse(CORE.validate_contract(contract)["valid"])

    def test_07_budget_over_maximum_fails(self):
        contract = valid_contract()
        contract["budgets"]["tool_calls"] = 21
        self.assertFalse(CORE.validate_contract(contract)["valid"])

    def test_08_objective_criterion_requires_verifier(self):
        contract = valid_contract()
        contract["verifiers"] = []
        self.assertFalse(CORE.validate_contract(contract)["valid"])

    def test_09_learning_ineligible_requires_no_storage(self):
        contract = valid_contract()
        contract["eligibility_class"] = "learning_ineligible"
        self.assertFalse(CORE.validate_contract(contract)["valid"])

    def test_10_enabled_retrieval_requires_selection(self):
        contract = valid_contract()
        contract["advisory_retrieval"] = {"enabled": True, "selections": []}
        self.assertFalse(CORE.validate_contract(contract)["valid"])

    def test_11_valid_candidate_record_passes(self):
        self.assertTrue(CORE.validate_record(valid_record())["valid"])

    def test_12_candidate_record_requires_candidate_status(self):
        record = valid_record()
        record["status"] = "approved"
        self.assertFalse(CORE.validate_record(record)["valid"])

    def test_13_reserved_record_type_fails(self):
        record = valid_record()
        record["record_type"] = "policy"
        self.assertFalse(CORE.validate_record(record)["valid"])

    def test_14_redacts_openai_style_key(self):
        value = "s" + "k-abcdefghijklmnopqrstuvwxyz123456"
        self.assertEqual(CORE.redact_record(value), "[REDACTED]")

    def test_15_redacts_bearer_token(self):
        value = "Authorization: Bearer abcdefghijklmnop"
        self.assertEqual(CORE.redact_record(value), "[REDACTED]")

    def test_16_detects_conflicting_values(self):
        first = valid_record()
        second = valid_record()
        second["record_id"] = "record-2"
        second["content"]["value"] = "skip verification"
        self.assertEqual(CORE.detect_conflicts([first, second])["count"], 1)

    def test_17_ignores_matching_values(self):
        first = valid_record()
        second = valid_record()
        second["record_id"] = "record-2"
        self.assertEqual(CORE.detect_conflicts([first, second])["count"], 0)

    def test_18_denies_external_connector_write(self):
        result = CORE.evaluate_policy({"requested_action": "external_connector_write"})
        self.assertFalse(result["allowed"])

    def test_19_denies_automatic_promotion(self):
        result = CORE.evaluate_policy({"requested_action": "automatic_promotion"})
        self.assertFalse(result["allowed"])

    def test_20_denies_high_stakes_persistence(self):
        result = CORE.evaluate_policy(
            {"requested_action": "record_lesson", "task_family": "medical"}
        )
        self.assertFalse(result["allowed"])
        self.assertEqual(result["storage_profile"], "none")

    def test_21_downgrades_unsafe_workspace_ledger(self):
        result = CORE.evaluate_policy(
            {"requested_action": "run", "requested_storage_profile": "workspace_ledger"}
        )
        self.assertEqual(result["storage_profile"], "ephemeral")

    def test_22_allows_fully_bound_retrieval(self):
        digest = "a" * 64
        request = {
            "requested_action": "retrieve",
            "task_id": "task-1",
            "record_id": "record-1",
            "content_digest": digest,
            "displayed_content_digest": digest,
            "task_scope": {"project": "proofloop"},
            "record_scope": {"project": "proofloop"},
            "decision": {
                "affirmative": True,
                "current_turn": True,
                "task_id": "task-1",
                "record_id": "record-1",
                "content_digest": digest,
                "operation": "retrieve",
            },
        }
        self.assertTrue(CORE.evaluate_policy(request)["allowed"])

    def test_23_denies_cross_scope_retrieval(self):
        digest = "a" * 64
        request = {
            "requested_action": "retrieve",
            "task_id": "task-1",
            "record_id": "record-1",
            "content_digest": digest,
            "displayed_content_digest": digest,
            "task_scope": {"project": "one"},
            "record_scope": {"project": "two"},
            "decision": {
                "affirmative": True,
                "current_turn": True,
                "task_id": "task-1",
                "record_id": "record-1",
                "content_digest": digest,
                "operation": "retrieve",
            },
        }
        self.assertFalse(CORE.evaluate_policy(request)["allowed"])

    def test_24_regression_runner_counts_results(self):
        result = CORE.run_regressions(
            {
                "cases": [
                    {"case_id": "pass", "actual": 1, "expected": 1},
                    {"case_id": "fail", "actual": 1, "expected": 2},
                ]
            }
        )
        self.assertEqual(result["passed"], 1)
        self.assertEqual(result["failed"], 1)

    def test_25_transfer_export_then_import(self):
        exported = CORE.transfer_records({"mode": "export", "records": [valid_record()]})
        imported = CORE.transfer_records({"mode": "import", "bundle": exported["bundle"]})
        self.assertTrue(imported["valid"])
        self.assertEqual(imported["records"], [valid_record()])


if __name__ == "__main__":
    unittest.main()
