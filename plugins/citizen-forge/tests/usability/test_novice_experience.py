import unittest
from pathlib import Path

from helpers import PLUGIN_ROOT, brief

from citizen_forge.explain import explain
from citizen_forge.intake import missing_questions


class UsabilityTests(unittest.TestCase):
    def test_only_one_question_is_presented_next(self):
        questions = missing_questions({"name": "Example"})
        self.assertGreater(len(questions), 1)
        card = {"status": "QUESTION_REQUIRED", "next_question": questions[0]}
        self.assertEqual(len([card["next_question"]]), 1)
        self.assertIn("why", card["next_question"])

    def test_unknown_can_be_escalated_without_jargon(self):
        value = explain("EXPERT_REVIEW_REQUIRED")
        self.assertNotIn("stack trace", value["what_happened"].lower())
        self.assertFalse(value["state_changed"])

    def test_all_skills_avoid_manual_user_commands(self):
        for skill in (PLUGIN_ROOT / "skills").glob("*/SKILL.md"):
            text = skill.read_text(encoding="utf-8")
            self.assertNotIn("Tell the user to run", text)

    def test_status_explanation_has_three_plain_parts(self):
        value = explain("RELEASE_BLOCKED")
        self.assertEqual(set(value), {"what_happened", "impact", "safest_next_action", "state_changed"})
