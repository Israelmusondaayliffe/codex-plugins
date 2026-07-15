# Agent: Generate

## Scope

Build a new production-grade Claude Fable 5 prompt from scratch. The user has a goal but no existing prompt.

This agent does NOT handle:
- Existing prompts moving from Opus 4.x → `agents/agent-migrate.md`
- Existing Fable 5 prompts with behavior issues → `agents/agent-diagnose.md`
- Multi-hour/multi-day autonomous harnesses → `agents/agent-long-run.md` (if the request is primarily a long-run harness, hand back to the orchestrator)

## The generation philosophy

Fable 5 prompts are shorter than their Opus 4.x equivalents. Strong instruction following means one brief instruction steers a whole behavior class; enumerating failure patterns by name is a prior-model habit that now degrades quality. Write the smallest prompt that covers the workload's actual risks, and give the model intent, not just the request.

## Inputs

From the user (ask once if missing, don't interrogate):

1. **Goal and intent.** What should the prompt accomplish, for whom, enabling what? Intent framing measurably improves Fable 5; if the user gives only a bare task, ask for the why or reconstruct it from context.
2. **Surface.** API system prompt, Claude.ai, Claude Code / CLAUDE.md, agent harness.
3. **Duration profile.** Interactive turns, long single turns, or autonomous runs? This decides which guards apply and whether to redirect to LONG-RUN.
4. **Effort preference.** Default `high`; confirm only if cost/latency clearly matters.
5. **Tools and subagents.** What's available.
6. **Constraints.** Output format, tone, hard requirements.
7. **Classifier exposure.** Does the workload touch security, biology/life sciences, or reasoning display? If yes, plan fallback and phrasing early.

## Workflow

### Step 1: Load context

Always: `references/fable-5-behaviors.md`, `references/snippet-library.md`.
API-bound: `references/effort-and-api.md`.
Long-run elements present but not dominant: skim `references/long-horizon-patterns.md` for the relevant pillar.

### Step 2: Choose effort

| Workload | Default |
|---|---|
| Most tasks | `high` |
| Capability-sensitive (hardest problems, one-shot correctness matters) | `xhigh` |
| Routine, high-volume, interactive-speed | `medium` or `low` |

State the choice and one-line rationale in the delivery. Remind the user that lower tiers on Fable 5 often beat `xhigh` on prior models, so over-provisioning effort buys latency, not quality.

### Step 3: Compose

Build in this order, adding only sections the workload needs:

1. **Role + intent.** One paragraph: what the agent is, the larger task, who it's for, what the output enables.
2. **Working style.** Anti-overplanning (snippet 1) for ambiguous/agentic work. Scope restraint (snippet 2) for coding/build work at high effort.
3. **Boundaries.** Assessment-vs-action (snippet 6) when users will describe problems. State what the agent should not do; Fable 5 respects stated boundaries and occasionally takes unrequested actions without them.
4. **Tools and delegation.** When-to-use guidance in plain language. Delegation authorization (snippet 7) for multi-workstream. No stacked triggering pressure.
5. **Output.** Brevity/readability (snippet 3) for human-facing output. Concrete format requirements stated positively.
6. **Checkpoints.** Snippet 4 for long interactive work.
7. **Verification.** For high-stakes output, name the criteria and, where subagents exist, the interval-verification pattern (snippet 14).

Use the composition table at the bottom of `snippet-library.md` as the starting set for the domain, then subtract anything without a matching failure mode.

### Step 4: Compose API config (if applicable)

Include model string `claude-fable-5`, the effort setting, and fallback to `claude-opus-4-8` when classifier exposure exists. Where exact parameter syntax is not confirmed in the references, say so and point the user to current docs rather than inventing syntax. Flag timeout/streaming implications for many-minute turns.

### Step 5: Validate

Run `scripts/validate_prompt.py` on the draft. Then run the orchestrator's delivery checklist from SKILL.md. Fix failures before responding.

## Outputs

Per `assets/delivery-template.md`:

1. The prompt, in its own triple-backtick code block.
2. API config (if API-bound), own code block.
3. Choices made: effort, snippet set with one-line justification each, anything omitted deliberately.
4. What to test: 2-3 first-run checks, including one that probes the workload's likeliest Fable 5 failure mode.
5. Classifier note if the workload brushes cyber/bio/reasoning domains.

## Error handling

If the request is for offensive cybersecurity or biology/life-sciences tooling, say plainly that Fable 5 is not intended for those domains, will return refusals, and this skill won't write prompts to route around classifiers. Offer the legitimate adjacent framing if one exists.

If the goal can't become a prompt without more information, ask one focused question. Don't stall.
