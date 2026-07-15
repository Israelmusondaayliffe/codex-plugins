---
name: gpt-5-4-production-prompter
description: "Generate production-ready GPT-5.4 prompts, migrate prompts from GPT-5.2/5.3-Codex/4.1/o3/o4-mini, or troubleshoot existing GPT-5.4 prompt issues. Use when users request GPT-5.4 prompts, ChatGPT prompts, GPT Builder instructions, API system prompts, Responses API configs, or need help with agentic workflows, coding, web research, extraction, long-context, computer use, or frontend design. Also triggers on migration requests, prompt debugging, early stopping, scope drift, tool routing failures, phase parameter problems, or formatting drift. Covers 1M token context, native compaction, phase parameter, tool_search, computer use, xhigh reasoning, personality controls, research mode, citation gating, dependency-aware tool persistence, verification loops, completeness contracts, and frontend design patterns."
---

# GPT-5.4 Production Prompter

Build production-ready GPT-5.4 prompts using patterns from OpenAI's official guide. GPT-5.4 is their most capable frontier model, optimized for coding, agentic workflows, multi-step reasoning, evidence-rich synthesis, and long-context analysis across up to 1M tokens.

## Router Logic

Assess the user's request and route to the appropriate agent.

**Build a new prompt** -> Load `agents/agent-prompt-builder.md`
  Triggers: "GPT-5.4 prompt for...", "system prompt for...", "API prompt for...", "ChatGPT prompt for...", "GPT Builder for...", "build me a prompt", "create a prompt", "write a prompt", "production prompt", any request for a new GPT-5.4 prompt from scratch.

**Migrate an existing prompt** -> Load `agents/agent-migration.md`
  Triggers: "migrate from...", "upgrade from GPT-5.2", "convert my prompt", "update for 5.4", "port from o3", "move from 4.1", "migrate from Codex", any request involving an existing prompt that needs updating to GPT-5.4.

**Troubleshoot a prompt** -> Load `agents/agent-troubleshooter.md`
  Triggers: "prompt not working", "GPT-5.4 keeps...", "output too brief", "scope drift", "stops early", "tool issues", "phase parameter", "formatting wrong", "too cautious", any request to fix, debug, or improve an existing GPT-5.4 prompt.

**If ambiguous:** Ask the user which workflow they need. If the user provides an existing prompt plus complaints, route to troubleshooter. If they provide an existing prompt plus a target model, route to migration. If they describe a use case without an existing prompt, route to builder.

## Shared Resources

All agents reference these as needed:

- `references/gpt-5-4-behavioral-profile.md` . Model strengths, weaknesses, behavioral shifts from 5.2.
- `references/core-prompt-blocks.md` . All official XML prompt patterns from the guide.
- `references/api-parameters.md` . API params, reasoning effort, verbosity, phase parameter.
- `references/coding-and-frontend.md` . Coding agent patterns, frontend design rules, terminal hygiene.
- `references/agentic-patterns.md` . Agentic workflow patterns, tool persistence, completeness contracts.
- `references/research-and-citations.md` . Research mode, citation gating, grounding rules.
- `references/extraction-and-vision.md` . Extraction, OCR, bbox, vision, computer use.
- `references/long-context-and-compaction.md` . 1M context window, compaction, phase parameter details.
- `references/complete-examples.md` . Full copy-pasteable production prompts.

Validation and delivery:

- `scripts/validate_prompt.py` . Validates prompt structure against 5.4 requirements.
- `assets/delivery-template.md` . Standard output format for all agents.

## Phase Handoff Protocol

Between agents, verify:
- Previous agent output exists if dependent (migration requires source prompt, troubleshooter requires problem prompt)
- User has confirmed the prompt type and use case
- Required context is available before proceeding

## Prompt Context Types

All agents share this classification. Always clarify which type the user needs:

| Type | Format | Use Case | Trigger |
|------|--------|----------|---------|
| ChatGPT | Natural language | Quick tasks, interactive | "ChatGPT prompt for..." |
| API (Responses) | JSON with system/user, Responses API | Production agents, backend | "API prompt for...", code mention |
| GPT Builder | Markdown instructions | Custom GPTs, shareable | "GPT Builder...", "Custom GPT for..." |
| System Prompt | XML-structured core | Reference for any context | "System prompt for..." |

## Error Recovery

If an agent encounters missing information (no source prompt for migration, no symptoms for troubleshooting), surface the gap to the user with a specific ask. Do not guess or proceed with assumptions on critical inputs.

## Model Family Quick Reference

| Variant | Best For | Default Reasoning |
|---------|----------|-------------------|
| gpt-5.4 | General-purpose + coding + agentic | none |
| gpt-5.4-pro | Hard problems, deeper reasoning | higher |
| gpt-5.4-mini | High-volume coding, computer use, agents | none |
| gpt-5.4-nano | Simple high-throughput, speed/cost priority | none |
