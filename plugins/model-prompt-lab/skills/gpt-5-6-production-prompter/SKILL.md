---
name: gpt-5-6-production-prompter
description: "Generate production-ready GPT-5.6 prompts (gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna), migrate prompts from GPT-5.5/5.4/5.3-Codex/4.1/o3, or troubleshoot GPT-5.6 prompt issues. Use when users request GPT-5.6 prompts, ChatGPT prompts, GPT Builder instructions, API system prompts, Responses API configs, or need help with agentic workflows, coding agents, web research, extraction, long-context, computer use, or frontend design. Also triggers on migrate to gpt-5.6, port to 5.6, openai-docs migrate, prompt debugging, responses too brief, unnecessary approval requests, safeguard refusals on legit work, cache cost surprises, scope drift, tool routing failures, formatting drift. Covers lean prompting, Programmatic Tool Calling, pro mode, multi-agent beta, max reasoning effort, persisted reasoning, explicit prompt caching, autonomy and approval boundaries, verbosity contracts, retrieval budgets, citation gating, phase parameter, 1M context, compaction, frontend design."
---

# GPT-5.6 Production Prompter

Build production-ready GPT-5.6 prompts using the lean, outcome-first philosophy from OpenAI's official guide. GPT-5.6 sets a new quality and efficiency baseline: it is especially token-efficient, more concise by default than 5.5, better at inferring the user's underlying goal, and ships new execution surfaces (Programmatic Tool Calling, pro mode, multi-agent beta, persisted reasoning, explicit caching). Prompts are typically even leaner than 5.5 prompts: state each instruction once, define autonomy boundaries in one place, and let the model choose the path.

## Router logic

Assess the user's request and route to the appropriate agent.

**Build a new prompt** -> Load `agents/agent-prompt-builder.md`
  Triggers: "GPT-5.6 prompt for...", "system prompt for...", "API prompt for...", "ChatGPT prompt for...", "GPT Builder for...", "build me a prompt", "create a prompt", "write a prompt", "production prompt", "lean prompt", any request for a new GPT-5.6 prompt from scratch.

**Migrate an existing prompt** -> Load `agents/agent-migration.md`
  Triggers: "migrate from...", "upgrade from GPT-5.5", "upgrade from GPT-5.4", "convert my prompt", "update for 5.6", "port from o3", "move from 4.1", "migrate from Codex", "$openai-docs migrate", any request involving an existing prompt that needs updating to the GPT-5.6 family.

**Troubleshoot a prompt** -> Load `agents/agent-troubleshooter.md`
  Triggers: "prompt not working", "GPT-5.6 keeps...", "output too brief", "asks permission constantly", "safeguard blocked my request", "cache costs went up", "scope drift", "stops early", "tool issues", "PTC not routing", "pro mode not helping", "formatting wrong", any request to fix, debug, or improve an existing GPT-5.6 prompt.

**If ambiguous:** ask the user which workflow they need. If the user provides an existing prompt plus complaints, route to troubleshooter. If they provide an existing prompt plus a target model, route to migration. If they describe a use case without an existing prompt, route to builder.

## Shared resources

All agents reference these as needed.

Foundational (load these first for any non-trivial task):
- `references/lean-prompting-philosophy.md` . The conceptual anchor. Why 5.6 prompts are leaner still: the measured case for subtraction, state-once discipline, and intent understanding.
- `references/gpt-5-6-behavioral-profile.md` . Model strengths, behavioral shifts from 5.5, token efficiency, default conciseness, safeguard classifiers.

New 5.6 surface (load when the use case touches them):
- `references/programmatic-tool-calling.md` . PTC: when task shape justifies it, routing instructions, the tool_orchestration template, continuation handling, assessment.
- `references/pro-mode-and-multi-agent.md` . reasoning.mode pro configuration and selection criteria; multi-agent beta coordination.
- `references/caching-and-persisted-reasoning.md` . Explicit prompt caching (1.25x write billing, breakpoints, ttl) and reasoning.context modes for multi-turn quality.
- `references/autonomy-and-response-style.md` . Approval boundary policies, verbosity contracts, short-answer must-include lists, concrete tone definition.

Behavior shaping:
- `references/personality-and-collaboration.md` . The split between how the assistant sounds and how it works, updated with 5.6 concrete-tone guidance.
- `references/api-parameters.md` . Model family, reasoning effort tiers including max, verbosity, phase parameter, safety_identifier, image detail levels.

Surgical block patterns (use only when they earn their place):
- `references/core-prompt-blocks.md` . XML prompt patterns, each with a "when to use" gate. Leaner defaults than ever on 5.6.
- `references/research-and-citations.md` . Retrieval budgets, citation gating, grounding rules, creative drafting guardrails (carried from 5.5, still load-bearing).
- `references/agentic-patterns.md` . Lean agent patterns, autonomy boundaries in agent prompts, stopping conditions, PTC handoffs, preambles.
- `references/coding-and-frontend.md` . Coding agent patterns, validation by running, 5.6's stronger frontend judgment.
- `references/extraction-and-vision.md` . Extraction, OCR, bounding boxes, vision, computer use, original image detail behavior.
- `references/long-context-and-compaction.md` . 1M context window, compaction, phase parameter, caching interplay.

Reference library:
- `references/complete-examples.md` . Full copy-pasteable production prompts in 5.6 lean style, including a PTC orchestration agent and a pro-mode review prompt.

Validation and delivery:
- `scripts/validate_prompt.py` . Validates prompt structure against 5.6 requirements, including repeated-instruction detection, approval-repetition detection, brevity-without-contract detection, PTC routing checks, and pro-mode anti-patterns.
- `assets/delivery-template.md` . Standard output format for all agents.

## Phase handoff protocol

Between agents, verify:
- Previous agent output exists if dependent (migration requires source prompt; troubleshooter requires both prompt and symptom)
- User has confirmed the prompt context type and use case
- Required context is available before proceeding

## Prompt context types

All agents share this classification. Always clarify which type the user needs.

| Type | Format | Use case | Trigger |
|------|--------|----------|---------|
| ChatGPT | Natural language | Quick tasks, interactive | "ChatGPT prompt for..." |
| API (Responses) | JSON with developer/user, Responses API | Production agents, backend | "API prompt for...", code mention |
| GPT Builder | Markdown instructions | Custom GPTs, shareable | "GPT Builder...", "Custom GPT for..." |
| System Prompt | Lean Markdown core, optional XML | Reference for any context | "System prompt for..." |

## What changed from 5.5 to 5.6

The skill is structured around six behavioral shifts. Each agent applies them.

1. **Lean prompts are now a measured doctrine, not just a philosophy.** In OpenAI's internal coding-agent eval sample, leaner system prompts improved scores roughly 10-15% while cutting total tokens 41-66% and cost 33-67% (directional figures; validate on your own workload). State each instruction once. Remove repeated instructions and examples. Simplify tool descriptions. See `references/lean-prompting-philosophy.md`.
2. **Reasoning effort: baseline first, then compare one level lower.** Different from the 5.5 advice of starting a tier lower. For 5.6, preserve your current 5.5/5.4 effort as the baseline, then test the same setting and one level lower on representative tasks. New `max` tier exists above `xhigh` for the hardest quality-first work; if you use `xhigh`, compare both.
3. **5.6 is more concise by default than 5.5.** Legacy "be concise" instructions can now make responses too brief. Re-check every brevity instruction, and when a short answer is required, specify what it must still include. See `references/autonomy-and-response-style.md`.
4. **Autonomy and approval boundaries are a first-class prompt block.** One compact policy stating what each request type authorizes, with safe local actions named explicitly. Repeating "ask first" or "do not mutate" across a prompt causes unnecessary approval requests. See `references/autonomy-and-response-style.md`.
5. **New execution surfaces need explicit routing.** Programmatic Tool Calling for bounded tool-heavy stages, pro mode for quality-first hard tasks, multi-agent beta for cleanly divisible work. None of these should be left to generic "use tools efficiently" instructions. See `references/programmatic-tool-calling.md` and `references/pro-mode-and-multi-agent.md`.
6. **Multi-turn and cost mechanics changed.** Persisted reasoning (`reasoning.context`) can reuse reasoning items across turns. Explicit caching bills writes at 1.25x the uncached input rate, so caching config now deserves review. Replace `prompt_cache_retention` with `prompt_cache_options.ttl`. See `references/caching-and-persisted-reasoning.md`.

The phase parameter, 1M context window, compaction, retrieval budgets, creative drafting guardrails, and the personality/collaboration split all carry forward from 5.5.

## Error recovery

If an agent encounters missing information (no source prompt for migration, no symptoms for troubleshooting), surface the gap to the user with a specific ask. Do not guess or proceed with assumptions on critical inputs.

## Model family quick reference

| Variant | String | Best for | Reasoning default |
|---------|--------|----------|-------------------|
| Flagship | `gpt-5.6-sol` | Frontier capability, complex production workflows | medium (re-evaluate per workload) |
| Balanced | `gpt-5.6-terra` | Strong performance at lower price | Match task shape, test one lower |
| Efficient | `gpt-5.6-luna` | High-volume, latency- and cost-sensitive workloads | none or low |
| Alias | `gpt-5.6` | Routes requests to `gpt-5.6-sol` | Same as sol |

Pro mode is not a separate model slug. Enable it with `reasoning.mode: "pro"` on any GPT-5.6 model. If the user asks for "GPT-5.6 Pro", configure pro mode on the selected variant instead of inventing a pro model string.

## Safeguards awareness

GPT-5.6 runs real-time cyber and biology misuse classifiers as outputs are generated. Requests can be blocked, refused, or paused mid-stream for several seconds while classifiers review outputs. Legitimate dual-use work (code review, vulnerability research, patch development, debugging, security education, defensive testing) can occasionally trip them. Applications serving end users should send a stable, privacy-preserving `safety_identifier` with each request. The troubleshooter agent covers prompting around false positives. See `references/gpt-5-6-behavioral-profile.md`.

## Codex migration helper

For users with code repositories, the OpenAI Docs Skill can apply migration changes automatically:

```text
$openai-docs migrate this project to the GPT-5.6 model family
```

Mention this option when the user describes a codebase migration. It pairs well with the migration agent's prompt-level work.
