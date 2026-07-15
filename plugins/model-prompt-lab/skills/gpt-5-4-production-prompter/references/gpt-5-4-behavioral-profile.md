# GPT-5.4 Behavioral Profile

Model strengths, weaknesses, behavioral shifts, and what changed from GPT-5.2.

## Where GPT-5.4 Is Strongest

- Strong personality and tone adherence, with less drift over long answers
- Agentic workflow robustness. Stronger tendency to stick with multi-step work, retry, and complete agent loops end to end
- Evidence-rich synthesis, especially in long-context or multi-tool workflows
- Instruction adherence in modular, skill-based, block-structured prompts when the contract is explicit
- Long-context analysis across large, messy, or multi-document inputs
- Batched or parallel tool calling while maintaining tool-call accuracy
- Spreadsheet, finance, and Excel workflows with instruction following, formatting fidelity, and self-verification
- Coding: production-quality code, polished front-end UI, repo-specific patterns, multi-file changes with fewer retries
- Strong out-of-the-box coding personality (less prompt tuning needed)
- Agentic web search and multi-source synthesis, especially for hard-to-locate information
- 1M token context window
- Native compaction support for longer trajectories
- Built-in computer use capabilities

## Where Explicit Prompting Still Helps

These are 5.4's known weaker areas. Always prompt for these:

- **Low-context tool routing** early in a session, when tool selection can be less reliable
- **Dependency-aware workflows** that need explicit prerequisite and downstream-step checks
- **Reasoning effort selection.** Higher effort is not always better. The right choice depends on task shape.
- **Research tasks** that require disciplined source collection and consistent citations
- **Irreversible or high-impact actions** that require verification before execution
- **Terminal or coding-agent environments** where tool boundaries must stay clear

## Behavioral Shifts from GPT-5.2

| Aspect | GPT-5.2 | GPT-5.4 | Action |
|--------|---------|---------|--------|
| Default reasoning | none | none | No change needed |
| Default verbosity | Lower | medium | May need less verbosity prompting |
| Scope control | May over-deliver | More thorough end-to-end | May need less constraint than 5.2 |
| Tool eagerness | More eager | More strategic, but can be less reliable early | Add dependency_checks |
| Grounding | Conservative bias | Improved but still needs citation gating | Keep citation_rules |
| Coding | Strong structured code | Even stronger, out-of-box personality | Less prompt tuning needed |
| Agentic | Good with scaffolding | Better end-to-end completion | Less "verify everything" needed |
| Long context | Standard | 1M tokens native | New capability |
| Compaction | New feature | Native, trained for it | More reliable |
| Computer use | Not available | Built-in | New capability |
| Formatting | Baseline | May overuse bullet lists | Add flat list constraint if needed |

## Key Differences for Prompt Authors

### 1. Less "Verify Everything" Prompting Needed

GPT-5.4 is more thorough end-to-end than earlier models on coding and tool-use tasks. Over-prompting with verification clauses can slow it down without adding value. For high-stakes changes (production, migrations, security), keep a lightweight verification clause. For routine work, let 5.4 handle it.

### 2. Formatting May Need Clamping

GPT-5.4 often defaults to more structured formatting and may overuse bullet lists. If you want clean prose or flat lists, explicitly clamp:

```xml
Never use nested bullets. Keep lists flat (single level). If you need hierarchy, split into separate lists or sections. For numbered lists, only use the 1. 2. 3. style markers (with a period), never 1).
```

### 3. Reasoning Effort Is a Last-Mile Knob

Most teams should default to none, low, or medium. Before increasing reasoning effort, first add completeness_contract, verification_loop, and tool_persistence_rules. These prompt-level fixes often recover the performance teams seek through higher reasoning.

### 4. Phase Parameter Matters for Multi-Step

For multi-step or tool-heavy flows, the phase field prevents intermediate updates from being treated as final answers. This is new and important for production agents.

### 5. Personality Can Be Separated from Writing Controls

GPT-5.4 is steerable when you separate persistent personality (tone, verbosity, decision style) from per-response writing controls (channel, register, formatting, length). Useful for customer-facing workflows.

## Small Model Profiles

### gpt-5.4-mini

- More literal, makes fewer assumptions
- Strong when task is clearly structured
- Weaker on implicit workflows and ambiguity handling
- May try to keep conversation going with follow-up questions unless suppressed
- Prompts are often longer and more explicit than for gpt-5.4

**Prompting rules:**
- Put critical rules first
- Specify full execution order when tool use or side effects matter
- Don't rely on "you MUST" alone. Use structural scaffolding: numbered steps, decision rules, explicit action definitions
- Separate "do the action" from "report the action"
- Show the correct flow, not just the final format
- Define ambiguity behavior explicitly: when to ask, abstain, or proceed
- Specify packaging directly: answer length, follow-up behavior, citation style, section order
- Be careful with "output nothing else." Prefer scoped: "after the final JSON, output nothing further"

**Good pattern for mini:**
1. Task
2. Critical rule
3. Exact step order
4. Edge cases or clarification behavior
5. Output format
6. One correct example

### gpt-5.4-nano

- Only for narrow, well-bounded tasks
- Prefer closed outputs: labels, enums, short JSON, fixed templates
- Avoid multi-step orchestration unless extremely constrained
- Route ambiguous or planning-heavy tasks to a stronger model

## Reasoning Effort Defaults by Task Shape

| Task Shape | Start With | Notes |
|-----------|------------|-------|
| Field extraction, support triage, short transforms | none | Execution-heavy, not reasoning-heavy |
| Light reasoning, complex instructions | low | Latency-sensitive with accuracy gain |
| Research, multi-doc review, strategy writing | medium | With well-engineered prompt |
| Complex analysis, multi-step coding | high | When reasoning gains justify latency |
| Long agentic, reasoning-heavy tasks | xhigh | Only when evals show clear benefit |

## Parameter Compatibility

When reasoning effort is set to `none`, these additional parameters are available:
- temperature
- top_p
- logprobs

These parameters raise an error with any other reasoning effort setting. Use reasoning depth, output verbosity, and max_output_tokens instead.
