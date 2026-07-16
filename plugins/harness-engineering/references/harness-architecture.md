# Harness Architecture

## Three operating layers

1. Information: instructions, context, skills, tools, connectors, project references, and memory.
2. Execution: workspace boundaries, plans, Goals, scripts, rules, hooks, approvals, and recovery.
3. Feedback: checks, receipts, reviews, failure records, maintenance, and model-change audits.

A useful harness is balanced across all three. Do not compensate for missing verification by adding more instructions.

## Scope hierarchy

- Thread prompt: one task.
- Global `AGENTS.md`: personal defaults that should apply across workspaces.
- Workspace `AGENTS.md`: shared workspace layout, routing, and output rules.
- Project or nested `AGENTS.md`: the closest project-specific commands, constraints, and verification rules.
- Skill: a repeatable workflow with optional references, scripts, or assets.
- Plugin: a distributable bundle of skills and optional tools, apps, or lifecycle components.
- MCP or connector: live external data or actions.
- Hook, rule, or script: deterministic enforcement.

Put a requirement in the narrowest scope that must always see it.

## Reliability order

Prefer the least-free mechanism that fits:

1. Script
2. Command rule
3. Hook
4. Sandbox or permission setting
5. Template
6. Prompt instruction
7. `AGENTS.md`
8. Inference

Repeated corrections should move toward deterministic enforcement.
