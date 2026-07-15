# Core Prompt Blocks for GPT-5.6

XML prompt patterns that still earn their place in 5.6 prompts. **Use these as surgical fixes for measured failure modes, not as defaults.** The default scaffolding for 5.6 is the lean Markdown structure documented in `references/lean-prompting-philosophy.md`.

Each block includes a "when to use" note. If the answer is "just in case," skip the block. A 5.6-specific rule on top of the 5.5 gate: before adding any block, confirm no existing instruction already covers it. A block that restates a sentence from `# Constraints` is a duplication bug, not insurance.

## Output and verbosity control

### Output contract

**When to use:** the output feeds another system, has a strict format requirement, or sections must appear in a specific order.

```xml
<output_contract>
- Return exactly the sections requested, in the requested order.
- If the prompt defines a preamble, analysis block, or working section, do not treat it as extra output.
- Apply length limits only to the section they are intended for.
- If a format is required (JSON, Markdown, SQL, XML), output only that format.
</output_contract>
```

In 5.6-style prompts, this usually becomes a `# Output` section. Use the XML version only when nested inside a larger XML-structured prompt.

### Verbosity controls

**When to use:** evals show consistent over-writing or under-writing that `text.verbosity` alone does not fix. On 5.6, check first whether a legacy "be concise" instruction is causing the under-writing; removing it is cheaper than adding this block.

```xml
<verbosity_controls>
- Prefer concise, information-dense writing.
- Avoid repeating the user's request.
- Keep progress updates brief.
- Do not shorten the answer so aggressively that required evidence, reasoning, or completion checks are omitted.
</verbosity_controls>
```

The last line is a must-include contract in miniature. On 5.6, prefer the full contract from `references/autonomy-and-response-style.md`.

## Stopping conditions and missing-evidence behavior

First-class since 5.5, unchanged in 5.6.

### Stopping conditions (decision rule form)

```text
After each tool result, ask: "Can I answer the user's core request now with useful evidence and citations for the factual claims?" If yes, answer.
```

```text
Resolve the user query in the fewest useful tool loops, but do not let loop minimization outrank correctness, accessible fallback evidence, calculations, or required citation tags for factual claims.
```

### Missing-evidence behavior

```text
Use the minimum evidence sufficient to answer correctly, cite it precisely, then stop.
```

```text
If a required fact is missing, ask for the smallest missing field rather than searching indefinitely or guessing.
```

## Follow-through and instruction handling

### Autonomy policy (replaces default_follow_through_policy on 5.6)

The 5.4/5.5-era `<default_follow_through_policy>` block is superseded by the compact autonomy policy. Use the Markdown `# Autonomy` form from `references/autonomy-and-response-style.md`. The XML form, for prompts that must stay XML-structured:

```xml
<autonomy_policy>
For requests to answer, explain, review, diagnose, or plan: inspect the relevant materials and report the result. Do not implement changes unless the request also asks for them.
For requests to change, build, or fix: make the requested in-scope local changes and run relevant non-destructive validation without asking first.
Require confirmation for external writes, destructive actions, purchases, or a material expansion of scope.
</autonomy_policy>
```

Whichever form you use, it appears exactly once, and no other block repeats its rules.

### Instruction priority

**When to use:** mid-conversation steering changes are common in your product, or instructions can conflict.

```xml
<instruction_priority>
- User instructions override default style, tone, formatting, and initiative preferences.
- Safety, honesty, privacy, and permission constraints do not yield.
- If a newer user instruction conflicts with an earlier one, follow the newer instruction.
- Preserve earlier instructions that do not conflict.
</instruction_priority>
```

### Mid-conversation task updates

For scoped, explicit steering changes:

```xml
<task_update>
For the next response only:
- Do not complete the task.
- Only produce a plan.
- Keep it to 5 bullets.

All earlier instructions still apply unless they conflict with this update.
</task_update>
```

## Tool use patterns

### Tool orchestration (new for 5.6)

**When to use:** Programmatic Tool Calling is enabled and a bounded stage needs explicit routing. This is the one block category that grew in 5.6. Template and worked example: `references/programmatic-tool-calling.md`. Never ship the template with unfilled brackets.

### Tool persistence rules

**When to use:** evals show the model stopping early on multi-step tasks, or giving up after one tool failure.

```xml
<tool_persistence_rules>
- Use tools whenever they materially improve correctness, completeness, or grounding.
- Do not stop early when another tool call is likely to materially improve correctness or completeness.
- Keep calling tools until:
  (1) the task is complete, and
  (2) the success criteria are met.
- If a tool returns empty or partial results, retry with a different strategy.
</tool_persistence_rules>
```

The lighter 5.6 alternative: one sentence in `# Stop rules` plus explicit success criteria.

### Dependency checks

**When to use:** the task has clear prerequisites the model has been observed skipping.

```xml
<dependency_checks>
- Before taking an action, check whether prerequisite discovery, lookup, or memory retrieval steps are required.
- Do not skip prerequisite steps just because the intended final action seems obvious.
- If the task depends on the output of a prior step, resolve that dependency first.
</dependency_checks>
```

### Parallel tool calling

**When to use:** wall-clock time matters and several tool calls are genuinely independent. On 5.6, if the parallel calls also need processing into a smaller result, evaluate PTC instead.

```xml
<parallel_tool_calling>
- When multiple retrieval or lookup steps are independent, prefer parallel tool calls to reduce wall-clock time.
- Do not parallelize steps that have prerequisite dependencies or where one result determines the next action.
- After parallel retrieval, pause to synthesize the results before making more calls.
- Prefer selective parallelism: parallelize independent evidence gathering, not speculative or redundant tool use.
</parallel_tool_calling>
```

## Completeness

### Completeness contract

**When to use:** batch work, lists, paginated results, where partial coverage is an observed failure mode.

```xml
<completeness_contract>
- Treat the task as incomplete until all requested items are covered or explicitly marked [blocked].
- Keep an internal checklist of required deliverables.
- For lists, batches, or paginated results:
  - determine expected scope when possible,
  - track processed items or pages,
  - confirm coverage before finalizing.
- If any item is blocked by missing data, mark it [blocked] and state exactly what is missing.
</completeness_contract>
```

Lighter alternative in `# Success criteria`:

```text
- Every item in the input list has a status entry in the output (processed, skipped with reason, or blocked with missing field)
```

## Verification (high-impact only)

### Verification loop

**When to use:** the action is irreversible, high-impact, or safety-critical. For routine work, prefer validation by running (tests, lint, build, render-and-inspect); see `references/coding-and-frontend.md`.

```xml
<verification_loop>
Before finalizing:
- Check correctness: does the output satisfy every requirement?
- Check grounding: are factual claims backed by the provided context or tool outputs?
- Check formatting: does the output match the requested schema or style?
- Check safety and irreversibility: if the next step has external side effects, ask permission first.
</verification_loop>
```

### Action safety

**When to use:** agents that take real-world actions (writes, sends, transfers, deletions).

```xml
<action_safety>
- Pre-flight: summarize the intended action and parameters in 1-2 lines.
- Execute via tool.
- Post-flight: confirm the outcome and any validation that was performed.
</action_safety>
```

### Stop conditions for consequential actions

```xml
<stop_conditions>
For consequential actions (returns, refunds, cancellations, deletions, production writes):
1. List exact details of action
2. Show IDs, amounts, affected items
3. Get explicit "yes" confirmation
4. Do NOT proceed without confirmation
</stop_conditions>
```

"Do NOT proceed" is a true invariant; ALL CAPS is appropriate. Note: if the prompt already has an autonomy policy requiring confirmation for destructive actions, this block only adds value through its procedural specifics (IDs, amounts, explicit yes). Keep the specifics, drop any sentence that merely restates the policy.

### Missing context gating

```xml
<missing_context_gating>
- If required context is missing, do not guess.
- Prefer the appropriate lookup tool when the missing context is retrievable; ask a minimal clarifying question only when it is not.
- If you must proceed, label assumptions explicitly and choose a reversible action.
</missing_context_gating>
```

## Structured output

### Structured output contract

**When to use:** SQL, JSON, or other parse-sensitive outputs.

```xml
<structured_output_contract>
- Output only the requested format.
- Do not add prose or markdown fences unless they were requested.
- Validate that parentheses and brackets are balanced.
- Do not invent tables or fields.
- If required schema information is missing, ask for it or return an explicit error object.
</structured_output_contract>
```

### Bbox extraction spec

```xml
<bbox_extraction_spec>
- Use the specified coordinate format exactly, such as [x1,y1,x2,y2] normalized to 0..1.
- For each box, include page, label, text snippet, and confidence.
- Add a vertical-drift sanity check so boxes stay aligned with the correct line of text.
- If the layout is dense, process page by page and do a second pass for missed items.
</bbox_extraction_spec>
```

## User communication

### User updates spec (coding and agentic)

**When to use:** streaming surfaces where a detailed update cadence is a product requirement.

```xml
<user_updates_spec>
- Intermediary updates go to the commentary channel.
- Use 1-2 sentence updates to communicate progress and new information while you work.
- Do not begin responses with conversational interjections or meta commentary.
- Before exploring or doing substantial work, send a user update explaining your understanding of the request and your first step.
- When work is substantial, provide a longer plan after you have enough context. This is the only update that may be longer than 2 sentences and may contain formatting.
- Before file edits, explain what you are about to change.
- Keep the tone of progress updates consistent with the assistant's overall personality.
</user_updates_spec>
```

### Simpler update spec (non-coding)

```xml
<user_updates_spec>
- Only update the user when starting a new major phase or when something changes the plan.
- Each update: 1 sentence on outcome + 1 sentence on next step.
- Do not narrate routine tool calls.
- Keep the user-facing status short; keep the work exhaustive.
</user_updates_spec>
```

## Deprecated on 5.6

| Legacy block | Replacement |
|--------------|-------------|
| `<default_follow_through_policy>` | `# Autonomy` policy (or `<autonomy_policy>` in XML prompts) |
| `<personality_and_writing_controls>` (combined) | `# Personality` + `# Collaboration style` + `# Autonomy` + `# Output` split |
| `<output_verbosity_spec>` | `# Output` section, `text.verbosity`, must-include contract |
| `<dig_deeper_nudge>` | Sharper `# Success criteria` (the nudge usually signals over-prompting) |
| `<solution_persistence>` | High-initiative `# Collaboration style` bullet |
| `<tool_efficiency>` with hard call caps | Retrieval budget (`references/research-and-citations.md`), or PTC for bounded stages |

## How to use this catalog

1. Start every prompt from the lean Markdown structure.
2. Note the specific, measured failure mode you are seeing.
3. Pick the matching block, add it as a surgical fix, stated once.
4. Re-evaluate. Remove the block if it does not measurably improve the failure mode.

The wrong move is stacking blocks "to be safe" before evaluating. On 5.6 that pattern measurably hurts.
