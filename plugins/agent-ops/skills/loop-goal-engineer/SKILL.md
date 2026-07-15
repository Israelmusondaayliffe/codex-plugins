---
name: loop-goal-engineer
description: Write production-ready /goal and /loop prompts for Claude Code and Codex CLI. User describes a thing they want done, this skill engineers the goal condition, the loop, or both. Four routed modes. GOAL writes a one-shot verifiable finish line. LOOP writes a recurring or self-pacing loop with all six working parts (trigger, execution, verifier, stop rules, memory, skills). ORCHESTRATE writes multi-agent goal setups (orchestrator, builder, reviewer) across Codex and Claude Code. DIAGNOSE fixes loops that run away, stall, or waste tokens. Triggers on write a goal, write a loop, /goal, /loop, goal condition, loop engineering, turn this into a loop, make this autonomous, codex goal, claude code loop, schedule a loop, stop rules, fix my loop, my loop ran away, orchestrate codex and claude, or any request to convert a task into an autonomous agent loop or goal.
metadata:
  author: Israel A
  version: 1.2.0
---

# Loop Goal Engineer

Turn "a thing I wanna do" into a goal condition or a self-running loop for Claude Code or Codex CLI.

The core shift this skill encodes: a prompt tells the agent what to do, a goal condition tells the agent when to stop. Instead of prompt, respond, iterate, the user defines a verifiable finish line and the agent works toward it, checking its own output until the goal is met. This skill writes those finish lines and loops so the user never has to hand-build them.

## Router Logic

Assess the request and route to exactly one agent. Load only that agent.

**GOAL request** -> Load `agents/agent-goal.md`
Triggers: "write a goal", "goal for this", a one-off deliverable with a recognizable end state (build X, research Y, audit Z once). Anything that finishes and stays finished.

**LOOP request** -> Load `agents/agent-loop.md`
Triggers: "write a loop", "every day / week / Monday", "keep going until", "on each run", metric optimization ("get load time under 2s"), anything recurring, scheduled, or self-pacing across many iterations.

**ORCHESTRATE request** -> Load `agents/agent-orchestrate.md`
Triggers: "orchestrate", "multi-agent", "codex builds and claude reviews", "use both tools", parallel builders, worktree racing, anything with more than one agent role.

**DIAGNOSE request** -> Load `agents/agent-diagnose.md`
Triggers: user pastes an existing goal or loop that misbehaves. "Fix my loop", "it ran 40 minutes", "it created files everywhere", "it keeps repeating", "why did it stop".

**BOTH** -> When the user asks for goal and loop, or the task naturally splits (a /goal to build the thing now, a /loop to maintain it), run agent-goal.md first, then agent-loop.md. Deliver both, clearly labeled.

## Auto-Decision When the User Just Describes a Task

When the request names no format, decide with this tree:

1. Is the task recurring, scheduled, or a number to push toward a target? -> LOOP
2. Does it finish once with a verifiable end state? -> GOAL
3. Does it need more than one agent role (build plus review, parallel approaches)? -> ORCHESTRATE
4. Is done subjective, creative-judgment-heavy, or a quick question? -> Not loop-shaped. Say so, explain why (see `references/failure-modes.md`, "Where loops do not work"), and offer a regular prompt instead.

State the chosen mode in one line, then proceed. Do not ask which mode unless the tree genuinely ties.

## Target Tool Handling

Default target is Claude Code. If the user says Codex, target Codex CLI. If they say "both tools", produce one prompt per tool or route to ORCHESTRATE if roles differ. Syntax and behavioral differences live in `references/target-tools.md`. Load it in every mode before writing the final prompt.

## Shared Output Contract

Every agent in this skill delivers in this shape, no exceptions:

1. One line naming the mode and target tool.
2. Short reasoning: what the verifiable end state is, what the scope is, what the stop rules are. A few sentences, not a report.
3. The prompt itself, copy-pasteable, in its own triple backtick code block. If multiple prompts (both mode, orchestrate mode), each gets its own block.
4. A one-line watch note: what to check on the first cycle, because a wrong loop repeats the same mistake faster.

Formatting rules baked into every generated prompt: no em-dashes anywhere (period or comma instead), no emojis, plain language, concrete file paths, explicit numbers for caps and retries.

## Validation Gate

Before delivering, run the deterministic validator on each generated prompt:

```bash
python scripts/validate_prompt.py <file-with-prompt> --mode goal|loop
```

It checks the six required components: verifiable end state, scope constraint, success stop, failure stop, iteration or budget cap, and memory file (loops only, warning for goals). It also strips-checks em-dashes. If any required check fails, fix the prompt and re-run before delivering. Scripts run the same way every time, instructions drift.

## Shared Resources

All agents draw from:

- `references/anatomy.md` The six working parts of a loop, the four parts of a goal, the stranger test for verifiability, the stop-rule taxonomy. Load in every mode.
- `references/patterns-library.md` Worked, proven templates: research brief, content audit, weekly report, and the eight reusable loop skeletons (ingest, build, improve groups). Load when the task resembles a known pattern.
- `references/failure-modes.md` The five mistakes that waste tokens, where loops do not work, and pro tips. Load in every mode, mandatory in DIAGNOSE.
- `references/target-tools.md` Claude Code /goal, /loop, /schedule specifics, Codex CLI /goal, orchestrator roles, reasoning effort guidance. Load before writing the final prompt.
- `assets/goal-template.md` and `assets/loop-template.md` Fill-in skeletons the agents assemble against.

## Error Recovery

If the user's task lacks a verifiable end state and one cannot be inferred, do not fabricate one. Ask one focused question: "What would done look like to a stranger checking the output?" That is the only clarifying question this skill ever needs.
