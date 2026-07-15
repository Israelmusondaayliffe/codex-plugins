# Agent Ops

Agent Ops packages reusable agent design, agent-system routing, and agent-system audit.

## Owned skills

- agent-ops-router
- agent-system-audit
- agent-builder
- goal-runner (explicit-only LoopKit compatibility shim through Agent Ops 0.2.x)
- loop-goal-engineer (explicit-only LoopKit compatibility shim through Agent Ops 0.2.x)
- loopy (explicit-only LoopKit compatibility shim through Agent Ops 0.2.x)

Generic Codex Goals and loops now route to LoopKit. The three historical names remain for one compatibility release and are scheduled for removal in Agent Ops 0.3.0 after LoopKit reaches 0.2.0.

## Companion capabilities

- Outcome Engine for general idea-to-result delivery
- LoopKit for generic Codex Goals, bounded loops, verification, resume, scheduling, and runtime diagnosis
- ProofLoop for bounded evidence and learning checks
- Superpowers for composable development workflows
- Plugin Eval for trigger and bundle evaluation

## Boundaries

- Outcome Engine owns general outcome workflows. LoopKit owns generic Goals and loops. Agent Ops owns reusable agent-system design and audit.
- Missing authority, evidence, or stop conditions blocks autonomous execution.
- Audits remain read-only unless a repair is separately requested.

## Verification

Run scripts/verify_bundle.py and validate each skill. Scenario tests must cover agent design, audit, and the LoopKit handoff.
