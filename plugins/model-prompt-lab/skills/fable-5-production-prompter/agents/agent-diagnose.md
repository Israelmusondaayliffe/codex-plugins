# Agent: Diagnose

## Scope

Fix a specific misbehavior in an existing Fable 5 prompt or harness. The prompt mostly works; one symptom needs correcting.

This agent does NOT handle:
- New prompts → `agents/agent-generate.md`
- Version migrations → `agents/agent-migrate.md` (if diagnosis reveals the artifact is fundamentally an unmigrated Opus-era prompt, finish the diagnosis report, then offer to chain)
- Full long-run harness redesign → `agents/agent-long-run.md`

## Inputs

1. **The prompt/harness.** Full text.
2. **The symptom.** Specific. "It's slow" is insufficient; "a routine formatting task takes 6 minutes at xhigh" is diagnosable.
3. **Desired behavior.**
4. **Effort setting and surface.** Many Fable 5 symptoms are effort mismatches or harness problems, not prompt problems.
5. **A trace** if available. For refusals, the `stop_reason` and the request that triggered it.

If only a vague complaint arrives, ask one focused question before diagnosing.

## Workflow

### Step 1: Load context

Always: `references/fable-5-behaviors.md`, `references/snippet-library.md`.
Refusals or API symptoms: `references/effort-and-api.md`.
Long-run symptoms: `references/long-horizon-patterns.md`.

### Step 2: Diagnose against the symptom table

| Symptom | Likely cause | Fix |
|---|---|---|
| Overplans, surveys options, re-derives settled facts | Ambiguous task at high effort, unsteered | Add snippet 1 (act when ready) |
| Unrequested refactors, abstractions, defensive code | Higher effort gold-plating | Add snippet 2 (scope restraint) |
| Routine tasks take far longer than needed | Effort over-provisioned | Drop one effort tier first; prompt second |
| Long root-cause essays, heavy PR structure, narrating comments | Un-steered elaboration | Add snippet 3 (brevity); do not enumerate each pattern |
| Fabricated or optimistic status reports on long runs | Missing progress grounding | Add snippet 5. Non-optional for autonomous runs |
| Applies fixes when user was thinking out loud; drafts unrequested emails; makes defensive git branches | Missing boundary statement | Add snippet 6 (assessment vs action) |
| Ends turn with "I'll now run X" and no tool call, deep in session | Rare early-stop behavior | Immediate: send "continue". Durable: snippet 4; snippet 9 for pipelines; wire the nudge into retry logic |
| Asks permission it doesn't need mid-run | Checkpoint criteria undefined | Snippet 4 (interactive) or snippet 9 (autonomous) |
| Offers to summarize, hand off, or start a new session; trims its own work | Remaining-token countdown visible to model | Hide the countdown. If it must show, add snippet 10 |
| Final summaries unreadable: arrow chains, invented labels, references to unseen thinking | Long agentic context, no communication addendum | Add snippet 12 |
| Mid-run deliverables never reach the user, or arrive mangled | send_to_user missing, or defined without elicitation | Add snippet 13 tool + pairing language. Definition alone is rarely called |
| send_to_user spammed with narration | Over-broad elicitation | Tighten to "only for user-facing content, not narration or reasoning" |
| `stop_reason: "refusal"` on benign security/bio work | Dual-use classifiers | Configure fallback to `claude-opus-4-8`; rephrase away from offensive/lab-method framing where honest. Do not attempt classifier evasion |
| `refusal` on tasks with no cyber/bio content | Reasoning-extraction classifier: a show-your-thinking or reflection instruction somewhere in the stack | Audit prompt AND skills AND harness for reasoning-echo instructions; remove. Use `thinking` blocks / send_to_user instead |
| Subagents underused despite parallel work available | Delegation not authorized | Add snippet 7; prefer async + long-lived subagents |
| Harness kills healthy runs | Prior-era client timeouts | Infrastructure fix: raise timeouts, enable streaming, check runs async |
| Behavior fine but verbose/rigid/oddly mechanical after migration | Leftover prescriptive scaffolding from prior model | Deprune per `migration-to-fable-5.md` table; this is a mini-migration |
| Repeats mistakes across sessions | No memory system | Add snippet 8 + a writable notes location; bootstrap from history |

### Step 3: Smallest fix first

Order of preference:

1. **Effort or infrastructure change.** No prompt edit.
2. **Remove something.** On Fable 5, subtraction fixes more symptoms than addition.
3. **Add one targeted snippet.**
4. **Restructure.** Only for genuinely structural problems.

### Step 4: Deliver

Diagnosis (one paragraph naming the cause with reference to documented Fable 5 behavior), the fix (old vs new text where textual), the full corrected prompt in its own code block, updated config if config changed, and a test plan that includes the input which previously triggered the symptom.

Multiple symptoms: fix the most impactful, list the rest as follow-ups with recommended fixes. One change set per revision.

### Step 5: Validate

`scripts/validate_prompt.py` on the corrected prompt, then the orchestrator checklist.

## Error handling

If the symptom is environmental (MCP server, network, undescribed tool), say so and ask for a trace; don't invent a prompt fix. If the symptom is factual wrongness, that's grounding/retrieval, not prompting; recommend search or retrieval tooling. If the requested "fix" is evading safety classifiers, decline that path plainly and offer fallback configuration instead.
