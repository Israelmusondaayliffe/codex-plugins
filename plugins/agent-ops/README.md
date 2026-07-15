# Agent Ops

Agent Ops packages the design and operation of reusable agents, persistent Goals, and bounded loops.

## Owned skills

- agent-ops-router
- agent-system-audit
- agent-builder
- loop-goal-engineer
- goal-runner
- loopy

The bundled loopy source is the canonical loose copy at ~/.agents/skills/loopy as of this release.

## Companion capabilities

- Outcome Engine for general idea-to-result delivery
- ProofLoop for bounded evidence and learning checks
- Superpowers for composable development workflows
- Plugin Eval for trigger and bundle evaluation

## Boundaries

- Outcome Engine owns general outcome workflows. Agent Ops owns agent-system design and operation.
- Missing authority, evidence, or stop conditions blocks autonomous execution.
- Audits remain read-only unless a repair is separately requested.

## Verification

Run scripts/verify_bundle.py and validate each skill. Scenario tests must cover design, run, resume, loop, and audit routing.
