# Migration Playbook: Opus 4.6 / 4.7 / 4.8 to Fable 5

The core migration philosophy is inverted from every prior migration: **subtract first**. Capability improvements at this level are, per the guide, "a good prompt to re-evaluate which instructions, tools, and guardrails are still needed." Skills and prompts developed for prior models are often too prescriptive for Fable 5 and **can degrade output quality**. The default action for legacy scaffolding is remove-and-retest, not port-and-keep.

## Migration order of operations

1. **Infrastructure first.** Timeouts, streaming, progress UI, async run checking. A perfect prompt dies in a harness with 4.7-era timeouts.
2. **Hard removals.** Items that break or trigger refusals on Fable 5.
3. **Deprune.** Legacy behavioral scaffolding, removed on the presumption of guilt.
4. **Additions.** The small set of Fable-5-specific guards the workload needs.
5. **Effort re-evaluation.** Usually downward.
6. **Test.** Restore removed items only where regression is measured.

## Step 1: Infrastructure checklist

| Check | Why |
|---|---|
| Client timeouts | Individual turns run many minutes at high effort |
| Streaming enabled | Users need signs of life during long turns |
| Async run checking (scheduled jobs) | Autonomous runs extend for hours; don't block |
| Fallback to `claude-opus-4-8` | `refusal` stop reason re-routing |
| Token countdown hidden from model | Prevents context-anxiety behaviors |

## Step 2: Hard removals (MUST-remove)

| Legacy pattern | Why it must go |
|---|---|
| `budget_tokens` / extended thinking config | Fable 5 is adaptive thinking only; no extended thinking budgets |
| Reasoning-echo instructions ("show your thinking", "explain your reasoning in your answer", reflection blocks, transcribe-your-thought-process patterns) | Triggers the `reasoning_extraction` refusal classifier, causing elevated fallbacks. Audit skills and system prompts for these when migrating. Replace with structured `thinking` block reads and/or a send_to_user tool |
| Remaining-token countdowns surfaced to the model | Main trigger for stop/summarize/hand-off behavior |
| Prefilled assistant turns (if surviving from 4.6-era harnesses) | Deprecated lineage; already removed in the Mythos line. Confirm against current docs |

## Step 3: Deprune candidates (remove, then re-test)

These compensated for prior-model weaknesses Fable 5 no longer has. Each one left in place is now potential quality drag.

| Legacy scaffolding | Written for | Fable 5 reality |
|---|---|---|
| Enumerated behavior lists ("don't do A, don't do B, don't do C...") | 4.x literalism and drift | One brief instruction steers the whole class |
| Anti-laziness language ("be thorough", "don't stop early", "complete ALL items") | 4.5/4.6 early stopping | Strong instruction retention across long tasks; residue now causes over-elaboration |
| Forced interim summaries ("summarize every N tool calls") | 4.6-era opacity | Good default progress updates; use send_to_user for verbatim needs |
| Aggressive subagent authorization ("spawn multiple subagents in the same turn when...") | 4.7 under-spawning | Dispatches parallel subagents readily; keep only when-appropriate guidance |
| Code review recall workarounds (separate find/filter phases to fight over-conservatism) | 4.7 recall drops | Bug-finding recall noticeably higher; re-test the plain harness first |
| Vision compensation (detailed transcription rituals for messy images) | Weaker prior vision | Trained to use bash and crop tools itself; provide the tools instead |
| Tool-triggering pressure ("Use tool X when...", stacked triggers) | 4.7's fewer-tool-calls tendency | Re-test with lighter language; effort remains the primary lever |
| "CRITICAL: You MUST" style emphasis | Older instruction-following | Strong instruction following makes plain statements sufficient |

## Step 4: Fable-5-specific additions (only what the workload needs)

Consult `snippet-library.md` for exact text. By symptom class:

| Risk in this workload | Add |
|---|---|
| Ambiguous tasks at high effort | Snippet 1 (anti-overplanning) |
| Coding/build work at high effort | Snippet 2 (scope restraint) |
| Human-facing output | Snippet 3 (brevity/readability) |
| Long-running interactive work | Snippet 4 (checkpoints) |
| Autonomous runs | Snippets 5 and 9 (progress grounding, autonomy reminder) |
| Users describing problems | Snippet 6 (assessment vs action) |
| Multi-workstream | Snippet 7 (delegation) + long-lived subagent design |
| Recurring agent | Snippet 8 (memory) |
| Async verbatim delivery | Snippet 13 (send_to_user + elicitation) |
| Long builds | Snippet 14 (interval verification with subagents) |

## Step 5: Effort re-evaluation

- Do not carry the prior model's effort setting across unexamined.
- Lower effort on Fable 5 often exceeds `xhigh` on prior models. Default move for routine workloads: drop one tier and test.
- Keep `high` as the general default and `xhigh` for the genuinely capability-sensitive.
- If migrated behavior is correct but slow: drop effort before touching the prompt.

## Step 6: Skill migration specifics

When the artifact being migrated is a skill rather than a bare prompt:

1. Audit SKILL.md and every agent/reference file for reasoning-echo instructions. This is the most commonly missed refusal source because reflection blocks hide deep in older skills.
2. Apply the deprune table to each behavioral instruction. Skills are the worst offenders for accumulated prescriptive scaffolding.
3. Fable 5 "does a good job of updating skills on the fly based on what it learns from the task at hand." Consider adding a line authorizing the model to note skill-improvement observations to a memory file rather than locking every behavior down.
4. Re-run the skill's eval set (or build a minimal one) on Fable 5 before and after depruning. Keep the leaner version unless a specific regression is measured.

## Diff summary template

Report every migration in this shape so the user can accept or reject individual changes:

1. Infrastructure changes (timeouts, streaming, fallback, countdown)
2. Hard removals (with refusal-risk flags)
3. Depruned scaffolding (each item: what, why it existed, why removed)
4. Additions (each snippet: which failure mode it guards)
5. Effort change (old, new, rationale)
6. Risk flags and rollback plan (what to restore first if behavior regresses)
