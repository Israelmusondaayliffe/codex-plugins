---
name: model-prompt-engineer
description: Create, migrate, or test prompts used by a Codex harness while adapting to the selected current OpenAI model and prompt surface. Use for global instruction prompts, Goal prompts, verification prompts, API system prompts, model migrations, prompt regressions, or requests to support GPT-5.6 and later models without freezing the harness to one model generation.
---

# Model Prompt Engineer

Keep stable user policy separate from temporary model compensation.

## Workflow

1. Classify the prompt surface: thread, `AGENTS.md`, skill, Goal, API system prompt, or GPT Builder.
2. Preserve an explicitly named target model.
3. If the user requests latest, current, or default, load the official `openai-docs` skill and verify current guidance.
4. Load an installed model-specific prompting skill when one exists and is visible.
5. State the outcome, necessary context, constraints, authority, output contract, and completion evidence once each.
6. Remove duplicate reminders and obsolete workarounds.
7. Test representative success, ambiguity, approval, tool-routing, formatting, and stop cases.
8. Record model-specific blocks as provisional.

Follow `../../references/model-change-policy.md`. Never invent a model name, parameter, price, or availability claim.
