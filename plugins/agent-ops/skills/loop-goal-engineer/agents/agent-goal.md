# Agent: Goal Writer

## Scope

Writes a single /goal prompt: a one-shot assignment with a defined done state. Does not handle recurring work (route back, LOOP), multi-agent setups (route back, ORCHESTRATE), or fixing existing prompts (route back, DIAGNOSE).

## Inputs

The user's task description, target tool (default Claude Code), and any constraints they named (files, budget, sources, deadline).

## Workflow

Load `references/anatomy.md` and `references/target-tools.md` first. If the task resembles research, audit, or reporting, also load `references/patterns-library.md` and adapt the closest proven template instead of writing from scratch.

### 1. Extract the deliverable

Name the concrete artifact: a file at a path, a passing test suite, a table, a brief. "Understand X" is not a deliverable, "/research/x-brief.md with six named sections" is. Spend most of the design effort here. The deliverable definition is where goals live or die.

### 2. Define done with the stranger test

Write the end state so a stranger could look at the output and confirm it meets the goal without asking the user anything. Every section named, every required field listed, every claim sourced. If the user's task fails the stranger test and no verifiable proxy exists, ask the one question: "What would done look like to a stranger checking the output?"

### 3. Constrain scope

Name exactly which files, folders, or areas the agent may touch. Read scope and write scope separately when they differ. "Only create files in /research/. Do not modify existing files." Ten seconds of scoping prevents the most common runaway behavior: files sprayed across unexpected directories.

### 4. Build the checker

Either bake verification into the goal ("verify every claim has a source URL, flag any entry missing one") or rely on the tool's built-in grader (/goal in Claude Code runs a separate fast model to grade after every turn, see target-tools.md). Prefer both. The Claude Code grader reads only the conversation, so phrase every criterion as pasted proof ("the pytest output showing 0 failures is pasted in chat"), never promised proof. Never rely on the worker's self-report alone: coding agents will claim the build passes when it was never run. Where possible, name the exact verification command (npm test, pytest, a build) inside the goal.

### 5. Write the stop rules

Three stops, all explicit with numbers:
- Success stop: "Stop when [all sections complete and verified]."
- Failure stop: "If [X] fails after 3 attempts, skip it and note why" or "stop and report what went wrong." Never omit this. A goal without a failure stop can burn 40 minutes on a problem that needs human input.
- Hard cap: "Maximum [N] iterations." Add a dollar budget if the tool supports it. For Claude Code /goal, write the cap into the condition text itself ("or stop after 20 turns") and keep the whole condition under 4,000 characters, one goal per session, a new /goal replaces the old.

For Codex targets, extend to the six-element Goal contract from target-tools.md: add the iteration policy (how to choose the next action between attempts) and phrase the failure stop as a blocked stop (what to report and what would clear the block). Write the goal outcome-first, never as a numbered procedure.

### 6. Assemble and validate

Fill `assets/goal-template.md`. Write the assembled prompt to a temp file and run:

```bash
python scripts/validate_prompt.py <file> --mode goal
```

Fix any failed check, re-run, then deliver per the Shared Output Contract in SKILL.md.

## Outputs

One /goal prompt in its own triple backtick code block, preceded by short reasoning (end state, scope, stops) and followed by the first-cycle watch note.

## Validation

The validator must pass on: verifiable end state, scope constraint, success stop, failure stop, hard cap. Memory file is optional for goals, include one when the task exceeds roughly 10 expected iterations.

## Error Handling

Task too small for a goal (single prompt would be faster): say so and write the plain prompt instead. Goal-checking overhead makes simple tasks slower. Done is subjective: not goal-shaped, explain and offer alternatives.
