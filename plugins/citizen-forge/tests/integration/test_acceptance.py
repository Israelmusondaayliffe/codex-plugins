import tempfile
import unittest
from pathlib import Path

from helpers import PLUGIN_ROOT, brief

from citizen_forge.change_classifier import classify
from citizen_forge.checks import run_all
from citizen_forge.intake import initialize_project, normalize_brief
from citizen_forge.ownership import evaluate
from citizen_forge.policy import ROUTE_APPROVED, ROUTE_PROTOTYPE, ROUTE_REUSE, ROUTE_REVIEW, decide, load_policy
from citizen_forge.provision import adapter_reports, plan, provision
from citizen_forge.release import decide_release
from citizen_forge.risk import infer_scores
from citizen_forge.roads import load_roads, select


POLICY = load_policy(PLUGIN_ROOT / "policies" / "default-policy.json")
ROADS = PLUGIN_ROOT / "assets" / "roads"


class AcceptanceScenarios(unittest.TestCase):
    def test_a_personal_analysis(self):
        value = brief()
        self.assertEqual(decide(value, infer_scores(value), POLICY)["final_route"], ROUTE_PROTOTYPE)

    def test_b_read_only_team_dashboard(self):
        value = brief(intended_users="Twelve internal teammates", expected_users=12, second_consumer=True, data_sources="Confidential internal spreadsheet", data_sensitivity="confidential", shape="interactive-dashboard")
        self.assertEqual(decide(value, infer_scores(value), POLICY)["final_route"], ROUTE_APPROVED)

    def test_c_sensitive_financial_data(self):
        value = brief(intended_users="Twelve internal teammates", expected_users=12, second_consumer=True, data_sensitivity="restricted investor financial data", shape="interactive-dashboard")
        self.assertEqual(decide(value, infer_scores(value), POLICY)["final_route"], ROUTE_REVIEW)

    def test_d_second_consumer_graduates(self):
        value = normalize_brief(brief(intended_users="Creator and colleague", expected_users=2, second_consumer=False))
        self.assertTrue(value["second_consumer"])
        self.assertNotEqual(decide(value, infer_scores(value), POLICY)["final_route"], ROUTE_PROTOTYPE)

    def test_e_confirmed_duplicate_routes_to_reuse(self):
        value = brief()
        decision = decide(value, infer_scores(value), POLICY, {"confirmed": True})
        self.assertEqual(decision["final_route"], ROUTE_REUSE)

    def test_f_external_customer_app_routes_to_engineering(self):
        value = brief(external_exposure="public customer-facing", expected_users=20, second_consumer=True, shape="interactive-dashboard")
        self.assertEqual(decide(value, infer_scores(value), POLICY)["final_route"], ROUTE_REVIEW)

    def test_g_destructive_migration_is_consequential(self):
        value = classify("Delete production data with a destructive migration")
        self.assertTrue(value["human_gate_required"])

    def test_h_constraint_tampering_is_consequential(self):
        value = classify("Change the agent constraint and policy to skip a failed check")
        self.assertEqual(value["classification"], "CONSEQUENTIAL")

    def test_i_missing_infrastructure_is_local_only_and_blocked(self):
        road = select("interactive-dashboard", ROADS)
        value = plan(Path("/tmp/example"), road, {})
        self.assertTrue(value["local_only"])
        self.assertIn("identity", value["unavailable"])
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            initialize_project(root, brief(shape="interactive-dashboard", expected_users=12, second_consumer=True, data_sensitivity="confidential"), confirmed=True)
            checks = run_all(root, POLICY, brief(shape="interactive-dashboard", expected_users=12, second_consumer=True, data_sensitivity="confidential"))
            released = decide_release(checks, classify("initial release"))
            self.assertEqual(released["decision"], "RELEASE_BLOCKED")

    def test_j_ownership_loss_requires_transfer(self):
        self.assertEqual(evaluate({"primary_owner": "", "backup_owner": ""}, True)["required_state"], "TRANSFER_REQUIRED")

    def test_all_four_roads_scaffold(self):
        roads = load_roads(ROADS)
        self.assertEqual(len(roads), 4)
        for road in roads.values():
            with self.subTest(road=road["name"]), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                (root / ".citizen").mkdir()
                value = plan(root, road, {})
                result = provision(root, ROADS / road["name"], value)
                self.assertEqual(sorted(result["created"]), sorted(road["scaffold_files"]))
