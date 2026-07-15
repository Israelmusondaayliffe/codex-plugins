# Fable 5 Behavioral Profile

Distilled from the official guide (`fable-5-prompting-guide.md` is the verbatim source and wins on conflict). This file is the fast-load behavioral map for any agent in this skill.

## Identity and family

- **Claude Fable 5** is the first model in the Claude 5 family, in the new Mythos-class tier above Opus. Model string: `claude-fable-5`.
- **Claude Mythos 5** shares the same underlying model. Fable 5 is generally available with additional safety measures for dual-use capabilities; Mythos 5 is available only to approved organizations without those measures. Prompting guidance is identical unless a safety classifier is the issue.
- Prior flagship for comparison: **Claude Opus 4.8** (`claude-opus-4-8`), which also serves as the fallback model for Fable 5 refusals.

## The core prompting shift

The philosophy shift from Opus 4.7/4.8 to Fable 5 is **subtraction and trust**:

1. Instruction following is strong enough that one brief instruction replaces an enumerated list of behaviors. If a prompt lists every failure pattern by name, it was written for an older model.
2. Skills and prompts written for prior models are often **too prescriptive** and can actively degrade Fable 5 output. The migration default is to remove instructions and test, not to add.
3. Steer with reasons and intent, not procedure. Fable 5 uses stated intent ("I'm working on X for Y, they need Z") to connect the task to relevant context instead of guessing.

## Behavioral deltas vs Opus 4.8

| Dimension | Fable 5 behavior | Prompting consequence |
|---|---|---|
| Turn length | Individual turns run many minutes at high effort; autonomous runs extend hours to days | Fix client timeouts, streaming, progress UI before migrating. Check runs asynchronously (scheduled jobs), don't block |
| Planning | Can overplan on ambiguous tasks at high effort | Add the act-when-ready snippet |
| Scope | Can tidy, refactor, or gold-plate beyond the ask at higher effort | Add the scope-restraint snippet |
| Unrequested actions | Occasionally drafts emails, makes git-branch backups, applies fixes when only assessment was asked | Add the assessment-vs-action boundary snippet |
| Progress reporting | Can fabricate status on long runs if unsteered; audit instruction nearly eliminates it | Add the evidence-grounded progress snippet on every long-run prompt |
| Early stopping | Rare: ends turn with stated intent but no tool call, or asks permission it doesn't need, deep in long sessions | Checkpoint snippet + autonomous-pipeline system reminder |
| Context anxiety | Rare: offers to summarize/hand off when harness shows remaining-token countdown | Hide token countdowns; add reassurance line if they must show |
| Subagents | Dispatches parallel subagents readily and dependably; manages long-lived subagents and peer agents | Authorize delegation explicitly, prefer async communication, keep subagents long-lived for cache savings |
| Verification | Excellent at higher effort; fresh-context verifier subagents beat self-critique | Instruct interval-based verification with subagents on long runs |
| Communication | Working shorthand can leak into final summaries (arrow chains, invented labels, references to unseen thinking) | Add the readability addendum for agentic/extended conversations |
| Vision | Much higher accuracy on dense technical images; trained to use bash and crop tools on flipped/blurry/noisy images | Provide bash/crop affordances for image-heavy work |
| Code review | Bug-finding recall noticeably higher, including cross-repo and history search | Deprune old recall-preservation scaffolding, then re-test |
| Memory | Performs particularly well with a lesson-recording memory system | Provide a notes location + the one-lesson-per-file convention |

## Effort levels

Effort is the primary intelligence/latency/cost control.

| Level | Use for |
|---|---|
| `high` | Default for most tasks |
| `xhigh` | Most capability-sensitive workloads |
| `medium` / `low` | Routine work, quicker interactive style |

Lower effort on Fable 5 still performs well and often exceeds `xhigh` on prior models. Reduce effort when a task completes but takes longer than necessary. The guide names only these four tiers for Fable 5; do not assume other tiers exist without confirming current API docs.

## API surface (per the guide's note)

- **Adaptive thinking only.** No extended thinking budgets (`budget_tokens` does not apply).
- **Summarized-only thinking output.** Applications read structured `thinking` blocks; they cannot get raw reasoning.
- **`refusal` stop reason** with server-side or client-side fallback handling to Opus 4.8.
- Full parameter details live in the "Introducing Claude Fable 5 and Mythos 5" doc; confirm exact syntax against current docs rather than inventing it.

## Safety classifiers (Fable 5 specific)

Three classifier domains can return `stop_reason: "refusal"`:

1. **Offensive cybersecurity** (exploits, malware, attack tooling). Benign security work can also trigger.
2. **Biology and life sciences** (lab methods, molecular mechanisms). Beneficial tasks can also trigger.
3. **Reasoning extraction.** Prompts, skills, or harness instructions that tell the model to echo, transcribe, or explain its internal reasoning as response text. This is the one prompt engineers trip most often: "show your thinking," "explain your reasoning step by step in your answer," and reflection blocks from older skills all risk it.

Mitigations: configure fallback to `claude-opus-4-8`; audit prompts and skills for reasoning-echo instructions; use structured `thinking` blocks for reasoning visibility; use a send_to_user tool for progress surfacing.

## What Fable 5 no longer needs (deprune candidates)

When migrating, these older-model patterns are removal candidates. Remove, then re-test; restore only what measurably regresses.

- Enumerated behavior lists where one brief instruction covers the class
- Anti-laziness language ("be thorough", "do not stop early") from the 4.5/4.6 era
- Forced interim-summary scaffolding ("summarize every N tool calls")
- Aggressive subagent-authorization language written to fight 4.7's under-spawning
- Code review recall-preservation workarounds written for 4.7's over-conservatism
- Reflection / show-your-thinking blocks (now actively harmful: refusal risk)
- Hard-capped thinking budgets and any `budget_tokens` config
- Instructions compensating for weak vision (Fable 5 self-serves with bash/crop)
