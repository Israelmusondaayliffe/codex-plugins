# Target Formats: Claude Code and Codex

Load before emitting any final artifact.

## The CLI translation table

How the five patterns and the agent loop map onto daily Claude Code and Codex work, no SDK required:

- Prompt chaining = phase-gated plans with tests per phase.
- Routing = model and effort selection per task type, small model for triage.
- Parallelization = multiple sessions or subagents in git worktrees, cross-model review (Claude Code plus Codex on the same diff).
- Orchestrator-workers = the orchestrator/builder/reviewer setup with a board of cards, one message spawning decomposed work.
- Evaluator-optimizer = /loop and /goal with a separate grader model, fresh-context review subagents, never letting the builder grade its own work.
- Ground truth rule = the verification rule: run the tests yourself, never trust the worker's self-report.

## Claude Code artifacts

### Subagent files

Destination: `.claude/agents/<name>.md` (project) or `~/.claude/agents/<name>.md` (user-wide). Shape:

```
---
name: kebab-case-name
description: When the main agent should delegate to this subagent. Write it delegation-first, it is read by the router, not the human.
tools: Tool1, Tool2        # optional, omit to inherit; grant minimally
---

System prompt for the subagent. Scope, workflow, ground truth commands,
stop conditions, what to hand back.
```

Design notes: the description is the trigger, treat it like a skill description (assertive, specific phrases). Grant the minimum tool set, a reviewer subagent rarely needs write access. Subagents start with fresh context, which is exactly what makes them honest reviewers.

### CLAUDE.md

Project constraints read at every session start. Constraints only, keep it short, every line is paid on every session.

### Skills

Reusable instruction sets in `.claude/skills/`. When the built agent needs a repeatable procedure, package it as a skill rather than inflating the agent prompt.

### Launch prompts

/goal and /loop launch autonomous work. Compose with the loop-goal-engineer skill for these rather than hand-writing.

## Codex artifacts

### The AGENTS.md chain (four layers, not one file)

Codex assembles an instruction chain at the start of every task: `~/.codex/AGENTS.md` (global identity, voice, working rules), `~/.codex/AGENTS.override.md` (temporary rules), the workspace `AGENTS.md` (write-folder discipline, read-only zones, routing), and the project `AGENTS.md` (project contract). Most-specific layer wins on conflicts. When emitting agent constraints for Codex, name the layer: global for identity-level defaults, workspace for file-system rules, project for the contract. Never duplicate a rule the chain already carries, the whole chain loads on every turn and every duplicated line is paid forever.

### Subagents: the [agents] config block

Codex has a first-class subagent system (MultiAgentV2) configured in `~/.codex/config.toml` and driven from prompts via spawn_agent, send_input, wait_agent, resume_agent, followup_task, close_agent. Reusable pre-scoped subagents are named blocks:

```
[agents]
max_concurrent = 3            # each subagent is a full model round-trip, cost scales, cap it
default_model = "gpt-5.5"
default_reasoning = "high"

[agents.reviewer]
model = "gpt-5.5"
reasoning = "high"
instructions = "You review only. Read the target, list concrete issues with line references, propose fixes. You do not edit files."
```

Emit this block for any reusable Codex subagent, with the four loop mechanics folded into `instructions`. One-off delegations go in the prompt instead ("use sub-agents so these three independent passes run in parallel, wait for all three, then synthesize").

### Goals

Sustained Codex work is wrapped in a /goal with six required elements: outcome, verification surface (the evidence that proves it), constraints (what must not regress), boundaries (files, tools, data allowed), iteration policy (how to choose the next action between attempts), and blocked stop condition (when to stop and report that no defensible path remains). Lifecycle: /goal pause, resume, clear. The most common Goal failure is no stop condition, it runs to budget exhaustion, and reaching budget is not completing the objective. Compose with loop-goal-engineer for the launch prompt, but carry all six elements.

### Prompt style: outcome-first, not procedural

GPT-5.5 is outcome-first. Step-by-step procedural prompts make it brittle, they constrain it to a path that may not be best. Every Codex-bound worker prompt this skill emits states outcome, success criteria, and constraints, then lets the model pick the path. "Reduce p95 latency below 120 ms without regressing correctness tests" beats "step 1 profile, step 2 identify." Claude-bound prompts can stay instruction-literal. This is a per-target rule, apply it at emission time.

### Role strengths (for cross-tool setups)

Codex tends to be strong as builder and at sustained Goal-driven execution and tool chaining. Claude Code tends to be strong as reviewer and planner (spec compliance, safety, security, contested-question synthesis). The proven cross-tool pattern: plan in Claude with explicit success criteria, execute in Codex under a /goal, review the diff.

## Harness awareness (both tools)

When the user runs an operating harness (a CLAUDE.md or AGENTS.md contract, a single write destination like CLAUDE-OUTPUTS/ or CODEX-OUTPUTS/YYYY-MM-DD/, validators, a four-phase workflow), built agents inherit it:

- Write scope defaults to the harness output folder, dated subfolder, versioned naming, and the agent announces the exact output path when done.
- Approval gates map onto the harness four-phase workflow (Explore, Plan, Execute, Verify): the plan sign-off is the gate, verification scores 0 to 10 against criteria and revises once below 8.
- The critique paradox rule carries into evaluator loops: at 9 or 10 on first pass, ship, forced revision on strong output introduces flaws. Deterministic script checks always run regardless, they cannot corrupt good output.
- Nothing goes in the agent prompt that the contract chain already loads every turn.

## Subagent economics (per platform)

Claude Code and Cowork: subagents share prompt caches, parallelism is nearly free token-wise, but the field consensus is a single deep agent with explicit spawning only where pieces are genuinely independent. Fan-out by default burns tokens and produces weak handoffs. The instruction to emit: "do not spawn a subagent for work you can complete directly."

Codex: each subagent is a full model round-trip, cost scales linearly, always cap max_concurrent. Same independence rule: dependent work stays in one thread.

## Version caution

Frontmatter fields, file locations, and command flags evolve between releases. The shapes above are the stable core. When a user needs the exact current field list or flag, verify against current docs rather than guessing, and say so.
