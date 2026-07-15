# Pro Mode and Multi-Agent for GPT-5.6

Two new execution surfaces for hard work. Pro mode buys reliability on a single difficult task; multi-agent (beta) buys wall-clock time and performance on tasks that divide cleanly.

## Pro mode

Pro mode is a Responses API execution mode that applies more model work to a request before returning a single final answer. It can improve reliability on difficult tasks, at the cost of latency, and it aggregates the tokens from that work in reported usage. Those tokens are billed at the selected model's standard token rates.

### Configuration

```python
response = client.responses.create(
    model="gpt-5.6-sol",
    reasoning={"mode": "pro", "effort": "high"},
    input=[...]
)
```

Rules:
- Keep your selected GPT-5.6 model. There is no separate Pro model slug; do not switch slugs.
- `reasoning.mode` and `reasoning.effort` are independent. Choose effort separately; if omitted, GPT-5.6 defaults to `medium` in both standard and pro modes.
- Start with the same model and effort as your standard-mode baseline, then compare configurations on representative tasks instead of assuming the highest effort is the best tradeoff.

### When to use pro mode

Use it when a marginal quality improvement materially affects the outcome AND the task is difficult enough to benefit:

- Complex optimization
- High-value coding or review
- Deep analysis with clear evaluation criteria

Prefer standard mode for routine, latency-sensitive, or high-volume work, and whenever your evaluations do not show a meaningful gain from pro mode.

### How to prompt pro mode

Keep the same outcome-focused prompt you use in standard mode: goal, relevant context, constraints, required evidence, success criteria, output format.

Do NOT:
- Ask the model to "use pro mode"
- Ask it to "think harder"
- Ask it to generate several candidate answers and pick the best

The mode does the extra work; the prompt's job is unchanged. Example of a well-shaped pro-mode request:

```text
Review this database migration plan for failure modes that could cause data loss
or extended downtime. For each finding, cite the relevant step, estimate impact
and likelihood, and recommend a specific mitigation. Return the five most
important risks in severity order.
```

Note what makes it pro-worthy: high stakes, clear evaluation criteria, evidence requirements, a defined output shape. Nothing in the prompt mentions the mode.

### Compare quality and cost

Compare standard and pro modes on the same representative tasks. Measure task success, answer completeness, required evidence, total tokens, latency, and cost. Use pro mode selectively where its quality or reliability gain justifies the extra model work.

### Pro mode anti-patterns

| Anti-pattern | Why it fails | Fix |
|--------------|-------------|-----|
| Pro mode on routine work | Latency and token cost without quality gain | Standard mode; save pro for eval-proven gains |
| "Think harder" instructions | Redundant with the mode; adds noise | Remove; keep the outcome-focused prompt |
| Candidate-generation instructions | Duplicates what the mode does internally | Remove |
| Pro + max stacked reflexively | Highest everything is not automatically the best tradeoff | Baseline at standard effort, compare configurations |
| Inventing a pro model slug | No such slug exists | `reasoning.mode: "pro"` on the selected 5.6 model |

## Multi-agent (beta)

Multi-agent lets a GPT-5.6 instance coordinate multiple subagents in parallel and synthesize their results. Similar to ultra mode in Codex, it can reduce wall-clock time and improve performance for complex tasks that divide cleanly into independent workstreams. Available as a beta feature in the Responses API while OpenAI iterates on developer feedback.

### When to use it

- The task divides cleanly into independent workstreams (research across distinct source families, per-module code analysis, per-market evaluation)
- Wall-clock time matters
- A synthesis step can meaningfully combine the workstream results

### When not to use it

- Workstreams are dependent (each result changes the next question)
- The task is small enough that coordination overhead exceeds the parallel win
- The feature's beta status is unacceptable for the production surface

### Prompting multi-agent work

The coordinator prompt needs:

- A decomposition rule: what makes a workstream independent for this task
- Per-workstream success criteria and output schema, so results can be synthesized mechanically
- A synthesis contract: how conflicts between workstreams are resolved and attributed
- Stop rules for the whole ensemble, not just each worker

Treat detailed API mechanics as beta-fluid: confirm current request shape against the Responses API multi-agent documentation before production use, and do not hard-code assumptions this reference does not state.

## Choosing between the surfaces

| Task shape | Surface |
|-----------|---------|
| One hard problem, quality-first, clear criteria | Pro mode |
| Bounded tool-heavy processing stage with a small structured result | Programmatic Tool Calling (see `references/programmatic-tool-calling.md`) |
| Cleanly divisible independent workstreams, wall-clock pressure | Multi-agent (beta) |
| Everything else | Standard mode, direct tool calls |

These compose: a multi-agent coordinator can run pro-mode workers on hard subproblems, and a worker can use PTC for its bounded collection stage. Compose only when each surface independently earns its place on evals.
