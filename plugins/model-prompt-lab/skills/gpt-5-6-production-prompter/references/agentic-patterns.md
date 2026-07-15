# Agentic Patterns for GPT-5.6

GPT-5.6 is proactive and persistent on multi-step tasks by default. The 5.6-specific agent work is therefore less about pushing the model forward and more about drawing the boundaries: one autonomy policy, explicit stopping conditions, and deliberate routing across direct calls, PTC, pro mode, and multi-agent.

## The lean agent pattern (default)

```text
Role: A capable agent that resolves the user's request end to end.

# Goal
[user-visible outcome]

# Success criteria
- [what must be true before final answer]
- [coverage requirement]
- [evidence requirement]

# Constraints
- [policy or safety limits]
- [retrieval budget if tool-using]
- [evidence rules]

# Autonomy
[one compact approval-boundary policy naming safe local actions and
confirmation-required actions; see references/autonomy-and-response-style.md]

# Output
- [response shape; must-include contract if short]

# Stop rules
- [when to stop, retry, fall back, ask, or abstain]
```

This replaces the legacy stack of `<autonomy_and_persistence>` + `<tool_persistence_rules>` + `<dependency_checks>` + `<verification_loop>` + `<completeness_contract>` for routine work. Add blocks individually when evals reveal a specific failure mode, and never let a block restate the autonomy policy.

## Autonomy in agent prompts

The single most important 5.6 agent section. The compact default:

```text
# Autonomy
For requests to answer, explain, review, diagnose, or plan: inspect the relevant
materials and report the result; do not implement changes unless asked.
For requests to change, build, or fix: make the requested in-scope local changes
and run relevant non-destructive validation without asking first.
Safe without asking: [reading files, inspecting logs, editing in-scope code,
running tests].
Require confirmation for external writes, destructive actions, purchases, or a
material expansion of scope.
```

Rules of engagement:
- The policy appears exactly once. No other section repeats "ask first" or "confirm before".
- Name the safe actions for the actual tool surface; a generic list leaves the model guessing.
- Name the ambiguities worth stopping for ("if the target environment is ambiguous, ask").

## Execution-mode routing (new for 5.6)

An agent prompt with multiple execution surfaces available must route explicitly:

| Stage shape | Route |
|-------------|-------|
| One call, small results, or each result changes the next decision | Direct tool calls |
| Bounded processing of many results into a small structured output (filter/join/rank/dedupe/aggregate/validate) | Programmatic Tool Calling with a task-specific `<tool_orchestration>` block |
| Approval-gated or citation-bearing steps | Direct tool calls, always |
| Hard quality-first subproblem with clear criteria | Pro mode |
| Independent workstreams under wall-clock pressure | Multi-agent (beta) |

Generic language ("use tools efficiently") does not produce correct routing. If both direct and programmatic routes exist, define one handoff and instruct the model not to switch routes or repeat completed work. See `references/programmatic-tool-calling.md` and `references/pro-mode-and-multi-agent.md`.

## Persistence (surgical use)

5.6 rarely needs persistence prompting. If evals show the agent stopping at analysis or partial fixes:

```text
# Collaboration style
Assume the user wants the task completed unless they explicitly ask for a plan or are brainstorming. Implement the change rather than describing it. Resolve blockers yourself when possible. If a blocker is genuinely external, name it and propose the smallest ask that unblocks you.
```

Reserve the heavier `<autonomy_and_persistence>` XML block for measured regressions, and check that it does not contradict or duplicate the autonomy policy.

## Stopping conditions

Unchanged from 5.5, still first-class. Use directly in `# Stop rules`:

```text
After each tool result, ask: "Can I answer the user's core request now with useful evidence and citations for the factual claims?" If yes, answer.
```

```text
Use the minimum evidence sufficient to answer correctly, cite it precisely, then stop.
```

```text
Continue tool calls until success criteria are met. If a tool returns empty results, retry with a different strategy at least once before giving up.
```

## Dependency checks (surgical use)

**When to use:** clear prerequisites the agent has been observed skipping.

```xml
<dependency_checks>
- Before taking an action, check whether prerequisite discovery, lookup, or memory retrieval steps are required.
- Do not skip prerequisite steps just because the intended final action seems obvious.
- If the task depends on the output of a prior step, resolve that dependency first.
</dependency_checks>
```

Markdown form: `Required prerequisite checks (X, Y) are completed before any action that depends on them.` in `# Success criteria`.

## Parallel tool calling

```text
# Constraints
When multiple lookups are independent, prefer parallel calls. Do not parallelize dependent steps. After parallel retrieval, synthesize before making more calls.
```

On 5.6, if the parallel calls feed a reduction step (rank, dedupe, aggregate), evaluate a PTC stage instead; that is exactly its task shape.

## Completeness (batch and list work)

```xml
<completeness_contract>
- Treat the task as incomplete until all requested items are covered or explicitly marked [blocked].
- Keep an internal checklist of required deliverables.
- For lists, batches, or paginated results: determine expected scope when possible, track processed items or pages, confirm coverage before finalizing.
- If any item is blocked by missing data, mark it [blocked] and state exactly what is missing.
</completeness_contract>
```

Lighter Markdown form:

```text
# Success criteria
- Every item in the input list has a status entry in the output (processed, skipped with reason, or blocked with missing field).
- Coverage is confirmed before finalizing.
```

Note for PTC pipelines: completeness applies to the final message, not just the program output. A program that processed every item does not guarantee a final answer that reports every item.

## Empty result recovery

```xml
<empty_result_recovery>
If a lookup returns empty, partial, or suspiciously narrow results:
- do not immediately conclude that no results exist,
- try at least one or two fallback strategies, such as alternate query wording, broader filters, a prerequisite lookup, or an alternate source or tool,
- only then report that no results were found, along with what you tried.
</empty_result_recovery>
```

## Verification and action safety (high-impact only)

For irreversible, high-impact, or safety-critical actions, keep `<verification_loop>`, `<action_safety>`, and `<stop_conditions>` from `references/core-prompt-blocks.md`. For routine work, prefer validation by running (see `references/coding-and-frontend.md`). Confirmation requirements live in the autonomy policy; these blocks add the procedural specifics only.

## User communication

### Preamble for time-to-first-token

```text
Before any tool calls for a multi-step task, send a short user-visible update that acknowledges the request and states the first step. Keep it to one or two sentences.
```

### Progress updates

```text
# Collaboration style
- Send brief updates at major phase changes (1 sentence on outcome, 1 on next step). Do not narrate routine tool calls.
```

### Phase parameter

For long-running Responses workflows, `phase: "commentary"` on intermediate updates, `phase: "final_answer"` on the completed answer, never on user messages. See `references/api-parameters.md`.

## Multi-turn agent configuration

For agents whose goals and assumptions persist across turns, set `reasoning.context: "all_turns"` and continue with `previous_response_id`; add compaction milestones for very long trajectories. See `references/caching-and-persisted-reasoning.md` and `references/long-context-and-compaction.md`.

## Multi-step agent pattern (5.6 lean form)

```text
Role: A multi-step agent that resolves the user's request end to end.

# Goal
[outcome]

# Success criteria
- The plan covers all required steps.
- Dependencies between steps are respected.
- Independent steps are parallelized when wall-clock matters.
- Final summary lists what was done and any optional follow-ups.

# Constraints
- Do not parallelize dependent steps.
- Cite sources for any factual claim.

# Autonomy
[compact policy; confirmation for irreversible actions lives here, once]

# Output
- A brief plan if work will take more than one phase.
- Phase-transition updates (1-2 sentences each).
- Final summary of completed work and any follow-up recommendations.

# Stop rules
- Stop when success criteria are met.
- If blocked, name the blocker and propose the smallest ask that unblocks.
```

## Customer service agent pattern

```text
Role: A customer service agent for [Company]. You help customers with orders, returns, and questions.

# Personality
[steady, task-focused block from references/personality-and-collaboration.md]

# Collaboration style
- Match the user's energy. Skip pleasantries when the user signals urgency.
- Ask for clarification only when missing information would materially change the outcome.

# Goal
Resolve the customer's issue end to end.

# Autonomy
Account lookups, order status checks, and drafting responses are safe without asking. For refunds, cancellations, or account changes: list exact details (IDs, amounts, affected items) and get explicit "yes" confirmation before proceeding.

# Constraints
- Do not state policies that are not in the provided context.

# Output
Length: at most 150 words per response. Plain language. Bullets only when listing items.
```

## What changed from 5.5 for agent prompts

| Aspect | 5.5 default | 5.6 default | Action |
|--------|-------------|-------------|--------|
| Follow-through | Collaboration-style bullets | One compact autonomy policy | Consolidate; delete echoes |
| Approval behavior | Follow-through policy block | Same policy; repetition now causes approval noise | State once |
| Tool orchestration | Direct + parallel | Direct + parallel + PTC routing | Route by task shape, explicitly |
| Hard subproblems | Higher effort | Pro mode option | Reserve for measured gains |
| Multi-turn context | CoT pass-through | Persisted reasoning (reasoning.context) | all_turns for stable goals |
| Persistence prompting | Sometimes needed | Rarely needed | Subtract first |
| Stopping conditions | First-class | First-class, unchanged | Keep |
