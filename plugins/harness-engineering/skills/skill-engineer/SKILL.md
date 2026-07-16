---
name: skill-engineer
description: Create or upgrade a missing Codex skill identified during harness design, using the official Skill Creator workflow and evidence that the skill fixes a repeated failure. Use when the harness plan requires a new reusable workflow, validator, script, reference set, or asset bundle that is not already supplied by an installed skill or plugin.
---

# Skill Engineer

Reuse an existing capability when it already owns the task. Create a skill only for a repeated, named failure or workflow.

## Workflow

1. Define concrete trigger examples and the failure the skill prevents.
2. Search installed namespaced and loose skills for an existing owner.
3. Load the system `skill-creator` skill.
4. Initialize the skill with its provided `init_skill.py` script.
5. Keep `SKILL.md` concise and move depth into directly linked references.
6. Add deterministic scripts only when exact behavior warrants them.
7. Generate matching `agents/openai.yaml` metadata.
8. Run the official quick validator and realistic forward tests.
9. Add the skill to the harness plan and discovery checks.

Do not create a broad everything-skill or load an entire library by default.
