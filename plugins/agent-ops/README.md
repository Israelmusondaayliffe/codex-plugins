# Agent Ops

Agent Ops packages reusable agent design, agent-system routing, and agent-system audit for Claude Code, Claude Cowork, and Codex. The design principles are shared across hosts; the subagent surfaces are not. On Claude Code and Cowork, subagents are `agents/*.md` files dispatched via the Agent tool. On Codex, subagents are named `[agents.<name>]` blocks in `config.toml` driven by lifecycle verbs.

## Owned skills

- agent-ops-router
- agent-system-audit
- agent-builder
- goal-runner (explicit-only LoopKit compatibility shim through Agent Ops 0.3.x)
- loop-goal-engineer (explicit-only LoopKit compatibility shim through Agent Ops 0.3.x)
- loopy (explicit-only LoopKit compatibility shim through Agent Ops 0.3.x)

Generic Goals and loops, on Claude Code, Claude Cowork, or Codex, now route to LoopKit. The three historical names remain for one compatibility release and are scheduled for removal in Agent Ops 0.4.0 after LoopKit reaches 0.2.0.

## Companion capabilities

- Outcome Engine for general idea-to-result delivery
- LoopKit for generic Goals, bounded loops, verification, resume, scheduling, and runtime diagnosis on any host
- ProofLoop for bounded evidence and learning checks
- Superpowers for composable development workflows
- Plugin Eval for trigger and bundle evaluation

## Boundaries

- Outcome Engine owns general outcome workflows. LoopKit owns generic Goals and loops. Agent Ops owns reusable agent-system design and audit.
- Missing authority, evidence, or stop conditions blocks autonomous execution.
- Audits remain read-only unless a repair is separately requested.

## Verification

Run scripts/verify_bundle.py and validate each skill. Scenario tests must cover agent design, audit, and the LoopKit handoff.
