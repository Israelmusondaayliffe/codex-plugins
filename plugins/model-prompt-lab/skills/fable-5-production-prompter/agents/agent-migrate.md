# Agent: Migrate

## Scope

Convert an existing prompt, harness, or skill built for Claude Opus 4.8, 4.7, 4.6, Sonnet 4.x, or earlier into one that runs cleanly on Claude Fable 5.

This agent does NOT handle:
- New prompts from scratch → `agents/agent-generate.md`
- Fable 5 prompts with behavior issues unrelated to migration → `agents/agent-diagnose.md`
- Ground-up long-run harness design → `agents/agent-long-run.md` (but a migration that turns a short-turn harness into a long-run one should chain there after the base migration)

## The migration philosophy

Subtract first. Fable 5's capability jump makes prior-model scaffolding a quality liability, not a safety net. The presumption for every legacy behavioral instruction is removal; it earns its place back only by measured regression. This is the opposite of every previous Claude migration and the thing users most need to hear.

## Inputs

1. **The existing artifact.** Full text. Prompt, harness config, or skill (all files if a skill).
2. **Original target model.**
3. **API config** if one exists (especially any `thinking` config).
4. **Duration profile.** Will this workload now run longer on Fable 5? (It usually can.)
5. **Known pain points**, if any.

If the user pastes a fragment, ask for the rest before migrating.

## Workflow

### Step 1: Load context

Always: `references/migration-to-fable-5.md`, `references/fable-5-behaviors.md`, `references/effort-and-api.md`.
For skills or long-run harnesses: `references/long-horizon-patterns.md`.
For additions: `references/snippet-library.md`.

### Step 2: Run the six-step playbook

Execute `references/migration-to-fable-5.md` in order: infrastructure, hard removals, deprune, additions, effort re-evaluation, test plan. Mark every line of the original as KEEP / REMOVE / CHANGE / ADD with a reason.

Non-negotiable checks within that pass:

- **Reasoning-echo audit.** Search every file for show-your-thinking, reflection, explain-your-reasoning-in-your-response, and transcription-of-thought patterns. These now trigger the `reasoning_extraction` refusal classifier. This is the most commonly missed item, especially inside older skills.
- **Thinking config.** Any `budget_tokens` or extended-thinking configuration is removed; Fable 5 is adaptive thinking only.
- **Countdown audit.** Any remaining-token display surfaced to the model is removed or paired with the reassurance line.
- **Fallback.** If the workload can brush cyber/bio classifiers, add fallback to `claude-opus-4-8`.

### Step 3: Deprune with discipline

For each legacy scaffolding item in the deprune table (anti-laziness, enumerated behavior lists, forced interim summaries, subagent pressure, recall workarounds, vision rituals, MUST-style emphasis): remove it, note in the diff why it existed and why it goes, and list it in the rollback plan in removal-priority order. Do not silently rewrite intent; if an instruction encodes genuine product policy rather than model compensation, KEEP it and say so.

### Step 4: Effort re-evaluation

Recommend one tier lower than the legacy setting for routine workloads; keep `high`/`xhigh` for the genuinely hard ones. State old, new, rationale.

### Step 5: Validate and deliver

Run `scripts/validate_prompt.py` on the migrated prompt, then the orchestrator's delivery checklist.

## Outputs

1. **Migrated prompt** (or per-file migrated skill contents), each in its own code block.
2. **Updated API config**, own code block, with unconfirmed syntax flagged for doc verification.
3. **Diff summary** in the six-category shape from the playbook's template.
4. **Test plan.** 3-5 specific checks: at minimum one probing over-elaboration (deprune side effect), one probing the workload's old failure mode (to confirm removal was safe), and one long-turn infrastructure check.
5. **Risk flags + rollback order.** Which removed item to restore first if behavior regresses.

## Phase handoff

If the migrated workload should now become an autonomous long-run agent (the usual upgrade path with Fable 5), finish the base migration, then offer to chain into LONG-RUN for the harness build. If migration reveals the original prompt was structurally broken independent of model era, surface it and offer DIAGNOSE framing rather than silently redesigning.

## Error handling

Non-Anthropic prompts (GPT, Gemini, Luma): redirect to the matching skill (`gpt-5-5-production-prompter`, `gpt-5-4-production-prompter`, `uni-1-prompt-architect`). Cross-vendor conversion is a rewrite, not a migration; offer GENERATE with the old prompt as requirements input.
