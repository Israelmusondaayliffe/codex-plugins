# API Parameters for GPT-5.4

## Responses API (Recommended)

GPT-5.4 works best with the Responses API, which supports passing chain of thought (CoT) between turns. This leads to fewer generated reasoning tokens, higher cache hit rates, and less latency.

### Basic Request Structure

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    reasoning={"effort": "none"},
    text={"verbosity": "medium"},
    input=[
        {
            "role": "developer",
            "content": "[System/developer instructions]"
        },
        {
            "role": "user",
            "content": "[User query]"
        }
    ]
)
```

### reasoning_effort

Controls how many reasoning tokens the model generates before producing a response. Default for GPT-5.4 is `none`.

| Level | Use Case | Latency | Notes |
|-------|----------|---------|-------|
| none (default) | Fast execution, field extraction, triage, short transforms | Lowest | Prompting is important at this level. Encourage "think" or outline steps. |
| low | Light reasoning with complex instructions | Low | Meaningful accuracy gain over none |
| medium | Research, multi-doc review, strategy | Medium | With well-engineered prompt, squeezes a lot of performance |
| high | Complex analysis, multi-step coding | Higher | Clear reasoning gains |
| xhigh | Long agentic, reasoning-heavy tasks | Highest | Only when evals show clear benefit |

**Selection guidance:**
- Start with none for execution-heavy workloads
- Start with medium or higher for research-heavy workloads
- For GPT-5.4 specifically, none can already perform well on action-selection and tool-discipline tasks
- If workload depends on nuanced interpretation (implicit requirements, ambiguity, cancelled-tool-call recovery), start with low or medium
- Before increasing reasoning effort, first add completeness_contract, verification_loop, tool_persistence_rules

### text.verbosity

Controls how many output tokens are generated. Lowering reduces overall latency.

| Level | Effect |
|-------|--------|
| low | Concise answers, minimal commentary, short code with less explanation |
| medium (default) | Balanced |
| high | Thorough explanations, longer code with inline comments |

You can still steer verbosity through prompting after setting it to low in the API. The parameter defines a general token range, but actual output is flexible to both developer and user prompts.

## Phase Parameter

For GPT-5.4 and later Responses models. Helps in long-running or tool-heavy flows where preambles or intermediate assistant updates might be mistaken for the final answer.

**Usage:**
- `phase: "commentary"` for intermediate assistant updates (preambles before tool calls)
- `phase: "final_answer"` for the completed answer
- Do NOT add `phase` to user messages

**Critical rules:**
- Highly recommended (optional at API level, but strictly better when used)
- If using `previous_response_id`, prior state is preserved automatically
- If replaying assistant history manually, preserve each original phase value
- Missing or dropped phase can cause preambles to be treated as final answers

```python
response = client.responses.create(
    model="gpt-5.4",
    input=[
        {
            "role": "assistant",
            "phase": "commentary",
            "content": "I'll inspect the logs and then summarize root cause and remediation."
        },
        {
            "role": "assistant",
            "phase": "final_answer",
            "content": "Root cause: cache invalidation race."
        },
        {
            "role": "user",
            "content": "Great, now give me a rollout-safe fix plan."
        }
    ]
)
```

## Parameter Compatibility

When reasoning effort is `none`, these additional parameters are available:
- temperature
- top_p
- logprobs

These raise an error with any other reasoning effort setting, or with older GPT-5 models.

**Alternatives when reasoning is not none:**
- reasoning.effort for reasoning depth
- text.verbosity for output verbosity
- max_output_tokens for output length

## Tool Configuration

### Web Search

```python
response = client.responses.create(
    model="gpt-5.4",
    input=[{"role": "user", "content": "Latest AI research developments"}],
    tools=[
        {
            "type": "web_search_20250305",
            "name": "web_search"
        }
    ]
)
```

### Custom Tools (Freeform Input)

GPT-5.4 supports custom tools with freeform text input (code, SQL, shell commands, prose):

```python
tools=[
    {
        "type": "custom",
        "name": "code_exec",
        "description": "Executes arbitrary python code"
    }
]
```

### Allowed Tools

Pass N tool definitions but restrict to M of them:

```python
tool_choice={
    "type": "allowed_tools",
    "mode": "auto",
    "tools": [
        {"type": "function", "name": "get_weather"},
        {"type": "function", "name": "search_docs"}
    ]
}
```

### Tool Search (Deferred Loading)

For large tool surfaces. Loads only relevant definitions at runtime:

```python
tools=[
    {
        "type": "tool_search",
        "tool_search": {
            "type": "hosted",
            "tools": [...]  # Full tool list, loaded selectively
        }
    }
]
```

## Preambles

GPT-5.4 generates brief, user-visible explanations before invoking tools. To enable:

Add to system/developer instructions: "Before you call a tool, explain why you are calling it."

Preambles boost tool-calling accuracy without bloating reasoning overhead.

## Chat Completions vs Responses API

| Feature | Chat Completions | Responses API |
|---------|-----------------|---------------|
| CoT pass-through | No | Yes |
| Phase parameter | No | Yes |
| Compaction | No | Yes |
| Custom tools (freeform) | No | Yes |
| Tool search | No | Yes |
| Reasoning effort | Yes (different format) | Yes |
| Verbosity | Yes (different format) | Yes |

**Recommendation:** Use Responses API for all new GPT-5.4 work. Chat Completions still works but misses key 5.4 features.

## Model Strings

| Variant | String | Best For |
|---------|--------|----------|
| GPT-5.4 | `gpt-5.4` | General-purpose + coding + agentic |
| GPT-5.4 Pro | `gpt-5.4-pro` | Tough problems, deeper reasoning |
| GPT-5.4 Mini | `gpt-5.4-mini` | High-volume coding, computer use, agents |
| GPT-5.4 Nano | `gpt-5.4-nano` | Simple high-throughput, speed/cost |

## Reasoning Effort History

| Model | Default | Available Levels |
|-------|---------|------------------|
| GPT-5 | medium | minimal, low, medium, high |
| GPT-5.2 | none | none, low, medium, high |
| GPT-5.4 | none | none, low, medium, high, xhigh |
