import unittest

from helpers import PLUGIN_ROOT, brief

from citizen_forge.policy import decide, load_policy
from citizen_forge.risk import infer_scores


class GoldenTests(unittest.TestCase):
    def test_personal_decision_shape(self):
        value = brief()
        decision = decide(value, infer_scores(value), load_policy(PLUGIN_ROOT / "policies" / "default-policy.json"))
        self.assertEqual(
            {key: decision[key] for key in ("deterministic_rule", "policy_version", "final_route", "required_next_action")},
            {
                "deterministic_rule": "sole_consumer",
                "policy_version": "1.0.0",
                "final_route": "PROTOTYPE_ONLY",
                "required_next_action": "Continue locally with prototype protections.",
            },
        )
