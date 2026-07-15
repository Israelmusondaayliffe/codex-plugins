# API Parameters for GPT-5.6

## Model strings

| Variant | String | Best for |
|---------|--------|----------|
| Flagship | `gpt-5.6-sol` | Frontier capability |
| Balanced | `gpt-5.6-terra` | Strong performance at lower price |
| Efficient | `gpt-5.6-luna` | Efficient, high-volume workloads |
| Alias | `gpt-5.6` | Routes requests to `gpt-5.6-sol` |

Pro mode is not a model slug. Enable it with `reasoning.mode: "pro"` on any GPT-5.6 model. Never invent a pro variant string.

## Responses API (recommended)

Use the Responses API for reasoning, tool-calling, and multi-turn workflows. It carries reasoning pass-through, the phase parameter, native compaction, persisted reasoning, Programmatic Tool Calling, and multi-agent beta.

### Basic request structure

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5.6-sol",
    reasoning={"effort": "medium"},
    text={"verbosity": "medium"},
    input=[
        {"role": "developer", "content": "[Lean instructions]"},
        {"role": "user", "content": "[User query]"}
    ]
)
```

## reasoning.effort

GPT-5.6 supports `none`, `low`, `medium`, `high`, `xhigh`, and `max`.

| Level | Use case | Notes |
|-------|----------|-------|
| none | Fast execution, extraction, triage, short transforms | Keep as latency baseline; also test low when the workflow benefits from reasoning or tool use |
| low | Latency-sensitive workloads | |
| medium | Balanced starting point | Default in both standard and pro modes when effort is omitted |
| high | Measured quality gain over medium | |
| xhigh | Long agentic, reasoning-heavy work with proven benefit | |
| max | Hardest quality-first workloads | New in 5.6. Compare max and xhigh to find the best quality/latency/cost tradeoff |

**Selection guidance:**
- New work: pick from task shape, then test one level lower.
- Migration from 5.5/5.4: preserve the current setting as the baseline, then compare the same setting and one level lower on representative tasks. 5.6 often maintains or improves quality with fewer tokens, but the best setting is workload-dependent.
- Current xhigh users: compare xhigh and max before assuming either.
- Set effort intentionally; do not leave it implicit in production.

## reasoning.mode (pro mode)

```python
response = client.responses.create(
    model="gpt-5.6-sol",
    reasoning={"mode": "pro", "effort": "high"},
    input=[...]
)
```

- Keep the selected 5.6 model; do not switch slugs.
- `reasoning.effort` is chosen independently; omitted effort defaults to `medium` in both standard and pro modes.
- Pro mode performs more model work before returning a single final answer. It increases latency and aggregates the work's tokens in reported usage, billed at the selected model's standard token rates.
- Selection criteria and prompting guidance: `references/pro-mode-and-multi-agent.md`.

## reasoning.context (persisted reasoning)

Controls whether the model reuses available reasoning items across turns.

| Value | Behavior | Use when |
|-------|----------|----------|
| auto (or omitted) | Model default | Unsure; check the response's `reasoning.context` field to confirm the effective mode |
| all_turns | Reuses reasoning from earlier turns | Goals, assumptions, and priorities stay stable across turns |
| current_turn | Earlier reasoning not reused | Earlier reasoning is no longer relevant |

With `all_turns`, continue with `previous_response_id` to make earlier reasoning available. When managing history manually, preserve and resend previous user inputs and every response output item. For `store: false` or Zero Data Retention, add `include: ["reasoning.encrypted_content"]` and replay the returned encrypted reasoning items. Full guidance: `references/caching-and-persisted-reasoning.md`.

## text.verbosity

| Level | Effect |
|-------|--------|
| low | Concise answers, minimal commentary |
| medium (default) | Balanced |
| high | Thorough explanations |

Use `text.verbosity` for the default level of detail, then use the prompt for task-specific length, structure, and required content. Note: 5.6 is more concise by default than 5.5; re-check whether prompt-level "be concise" instructions are still needed, and when a short answer is required, specify what it must include. See `references/autonomy-and-response-style.md`.

## Prompt caching

Implicit caching continues to work with no code change. New in 5.6:

- Explicit mode: mark exactly which reusable prompt prefixes get cached, via explicit breakpoints or `prompt_cache_options.mode: "explicit"`.
- Cache writes bill at 1.25x the uncached input rate; cache reads remain discounted.
- Replace `prompt_cache_retention` with `prompt_cache_options.ttl`.
- Track `cached_tokens` and `cache_write_tokens` in usage to understand net cost.

Full guidance: `references/caching-and-persisted-reasoning.md`.

## Programmatic Tool Calling

Add the `programmatic_tool_calling` tool and opt eligible tools in with `allowed_callers`. The application must handle `program` items, program-issued function calls, and `program_output` items while preserving each call's `call_id` and `caller` linkage. PTC is ZDR-compatible with no additional container costs. Routing and prompting guidance: `references/programmatic-tool-calling.md`.

## safety_identifier

If the application serves individual end users, send a stable, privacy-preserving `safety_identifier` with each request. This supports the real-time cyber and biology misuse classifiers that run as outputs are generated. See the safeguards section of `references/gpt-5-6-behavioral-profile.md`.

## Image detail

GPT-5.6 preserves the original dimensions of images sent with `original` or `auto` detail instead of resizing them to a patch budget or pixel-dimension limit.

| Level | Use case | Cost note |
|-------|----------|-----------|
| original / auto | Spatially sensitive work: computer use, localization, OCR, click accuracy, dense documents | Large images can use more input tokens and increase latency |
| high | Standard high-fidelity understanding | |
| low | Speed and cost over fine detail | |

Choose deliberately for large images; original-dimension processing is a quality win and a cost lever at the same time.

## Phase parameter (carried from 5.4/5.5)

For long-running or tool-heavy Responses workflows where preambles or intermediate updates might be mistaken for the final answer.

- `phase: "commentary"` for intermediate user-visible updates
- `phase: "final_answer"` for the completed answer
- Do NOT add `phase` to user messages
- If using `previous_response_id`, prior state is preserved automatically
- If replaying assistant history manually, preserve each original phase value exactly

Developer-message reminder when manually replaying:

```text
If manually replaying assistant items:
- Preserve assistant `phase` values exactly.
- Use `phase: "commentary"` for intermediate user-visible updates.
- Use `phase: "final_answer"` for the completed answer.
- Do not add `phase` to user messages.
```

## Preambles for tool-heavy tasks (carried from 5.5)

For tasks that call tools or run long before visible text, prompt a short user-visible preamble:

```text
Before any tool calls for a multi-step task, send a short user-visible update that acknowledges the request and states the first step. Keep it to one or two sentences.
```

## Parameter compatibility

When reasoning effort is `none`, temperature, top_p, and logprobs become available; they raise an error with any other effort setting. When reasoning is not `none`, use `reasoning.effort`, `text.verbosity`, and `max_output_tokens` as the levers.

## Chat Completions vs Responses API

| Feature | Chat Completions | Responses API |
|---------|------------------|---------------|
| Reasoning pass-through | No | Yes |
| Phase parameter | No | Yes |
| Compaction | No | Yes |
| Persisted reasoning (reasoning.context) | No | Yes |
| Programmatic Tool Calling | No | Yes |
| Multi-agent (beta) | No | Yes |
| Explicit caching controls | Limited | Yes |

**Recommendation:** Responses API for all new GPT-5.6 work.

## Reasoning effort history

| Model | Default | Available levels |
|-------|---------|------------------|
| GPT-5.2 | none | none, low, medium, high |
| GPT-5.4 | none | none, low, medium, high, xhigh |
| GPT-5.5 | none | none, low, medium, high, xhigh |
| GPT-5.6 | medium when omitted in Responses reasoning config | none, low, medium, high, xhigh, max |

## Codex migration helper

The OpenAI Docs Skill can apply 5.6 migration changes via Codex:

```text
$openai-docs migrate this project to the GPT-5.6 model family
```

Available in the OpenAI skills repository (the openai-docs skill). Useful for projects with many prompts to migrate.
