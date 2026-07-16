---
name: harness-planner
description: Turn a confirmed harness profile and read-only audit into a decision-complete architecture and reversible operation plan. Use when a user asks for a harness plan, implementation plan, workspace blueprint, capability plan, migration plan, or wants to see exact proposed changes and checks before Codex edits global or project files.
---

# Harness Planner

Plan the outcome, scopes, operations, approvals, evidence, and rollback. Leave no implementation decisions unresolved.

## Workflow

1. Require a confirmed profile and current audit, or record why one is not applicable.
2. Design the information, execution, and feedback layers.
3. Put each requirement in the narrowest durable scope.
4. Reuse installed capabilities before proposing a new skill or plugin.
5. Prefer scripts, rules, hooks, sandbox settings, and templates when behavior must be exact.
6. Define separate approval groups using `../../references/safety-and-approvals.md`.
7. Generate file previews, operations, expected hashes, checks, failure stops, and rollback actions.
8. Present the human plan and machine operations together.
9. Do not begin implementation until the user accepts the plan or explicitly requests end-to-end execution.

Start from `../../assets/harness-plan.template.json`. Validate it with `python3 ../../scripts/harnessctl.py validate-operations PLAN.json`.
