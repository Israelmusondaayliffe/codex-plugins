# Delivery Template

Every agent in this skill delivers in this shape. Sections marked (if applicable) are omitted, not left empty.

---

## 1. The prompt

Always first. Always in its own triple-backtick code block. Complete and copy-pasteable, never elided with "..." placeholders.

## 2. API / harness config (if applicable)

Own code block. Model string `claude-fable-5`, effort setting, fallback config where classifier exposure exists. Any parameter whose exact syntax is not confirmed in this skill's references is flagged: "confirm against current Anthropic docs."

## 3. Tool definitions (if applicable)

send_to_user or other client-side tools, each in its own code block, each paired with its elicitation language.

## 4. Choices made

3-6 short bullets: effort level and why, which snippets were included and the failure mode each guards, and anything deliberately omitted (depruned or judged unnecessary for Fable 5). Subtraction decisions are choices worth recording.

## 5. What to test

2-5 specific first-run checks. Each names the behavior to probe and what success looks like. For long-run work, always include a mid-run progress-audit check.

## 6. Risk flags (if applicable)

Classifier exposure, unconfirmed API syntax, waived pillars, rollback order for migrations.

---

Style rules for the delivery text around the template: prompt first, explanation after. No preamble. Plain language. No em-dashes.
