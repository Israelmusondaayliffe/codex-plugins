# Effort, Thinking, and API Configuration for Fable 5

Ground truth is the official guide (`fable-5-prompting-guide.md`) plus the "Introducing Claude Fable 5 and Mythos 5" documentation. Where exact parameter syntax is not stated in the guide, this file says so explicitly. Never fabricate parameter names or values; verify against current Anthropic docs at delivery time when the user is shipping to API.

## Model strings

| Model | String | Notes |
|---|---|---|
| Claude Fable 5 | `claude-fable-5` | Flagship, generally available, dual-use safety classifiers active |
| Claude Mythos 5 | consult current docs | Same underlying model, approved organizations only |
| Claude Opus 4.8 | `claude-opus-4-8` | Prior flagship; the designated refusal-fallback target |

## Effort selection

Effort is the primary intelligence/latency/cost lever on Fable 5.

| Effort | When | Fable 5 specifics |
|---|---|---|
| `high` | Default for most tasks | Sensible starting point for nearly everything |
| `xhigh` | Most capability-sensitive workloads | Longest turns; excellent verification behavior and most rigorous output; also the setting most prone to over-gathering context and unrequested tidying on routine work. Pair with scope-restraint and anti-overplanning snippets |
| `medium` | Routine work | Often exceeds `xhigh` performance on prior models |
| `low` | Simple, high-volume, or latency-sensitive work | Still performs well; use for quick interactive style |

Tuning heuristics from the guide:

- Reduce effort if a task completes correctly but takes longer than necessary.
- Reduce effort for a quicker, more interactive working style.
- Do not reflexively carry an Opus 4.7/4.8 effort setting across. Fable 5 at one tier lower frequently matches or beats the prior model. Migration default: re-evaluate, starting one tier down for routine workloads, keeping `high`/`xhigh` for the hardest ones.

Only these four tiers are named for Fable 5 in the guide. If a user asks about other tiers, check current API documentation rather than assuming parity with older models.

## Thinking configuration

- **Adaptive thinking only.** Fable 5 decides when and how much to think. There are no extended thinking budgets; any `budget_tokens` config is a migration artifact to remove.
- **Summarized-only thinking output.** The API returns summarized `thinking` blocks, not raw reasoning. If an application needs reasoning visibility, read those structured blocks. Do not prompt the model to reproduce reasoning in its response text (see refusals below).

## Turn duration and client plumbing

Before shipping any Fable 5 prompt to production, verify the surrounding infrastructure:

1. **Client timeouts.** Individual turns on hard tasks run many minutes at `high`/`xhigh`. Old timeout values will kill healthy runs.
2. **Streaming.** Enable it; users need signs of life during long turns.
3. **Progress UI.** Long turns need progress indicators, and long async agents need a send_to_user tool for verbatim mid-turn delivery (see `snippet-library.md`, snippet 13).
4. **Async harness structure.** For autonomous runs that extend hours: check on runs via scheduled jobs rather than blocking a request thread.

## Refusals and fallback

Fable 5 can return `stop_reason: "refusal"` from safety classifiers in three domains:

1. Offensive cybersecurity (exploits, malware, attack tooling). Benign security work can also trip it.
2. Biology and life sciences (lab methods, molecular mechanisms). Beneficial work can also trip it.
3. **Reasoning extraction.** Instructions to echo, transcribe, or explain internal reasoning as response text.

Handling:

- Configure **server-side or client-side fallback to Claude Opus 4.8** so declined requests re-route automatically.
- For cybersecurity or life-sciences products, expect elevated fallback rates and design for them; Fable 5 is explicitly not intended for offensive cyber or bio/life-sciences work.
- For reasoning-extraction refusals, the fix is in the prompt: audit and remove show-your-thinking, reflection, and reasoning-echo instructions. This is the most common self-inflicted refusal for teams migrating older skills.

## Prompt-audit checklist for API-bound Fable 5 prompts

- [ ] Model string is `claude-fable-5` (or the confirmed Mythos string for approved orgs)
- [ ] Effort stated explicitly with a one-line rationale
- [ ] No `budget_tokens` or extended-thinking config anywhere
- [ ] No instruction that asks the model to reproduce, echo, or explain its internal reasoning in the response
- [ ] Fallback to `claude-opus-4-8` configured if the workload can brush against cyber/bio classifiers
- [ ] Client timeouts, streaming, and progress UI sized for many-minute turns
- [ ] No remaining-token countdown surfaced to the model (or the reassurance line is present)
- [ ] For async agents: send_to_user tool defined AND elicitation language present in the system prompt
