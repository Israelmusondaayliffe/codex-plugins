# Coding and Frontend Patterns for GPT-5.4

GPT-5.4 brings GPT-5.3-Codex coding capabilities to the flagship model. Strong out-of-the-box coding personality means less prompt tuning is needed. More thorough end-to-end on coding/tool-use tasks than earlier models.

## Autonomy and Persistence

GPT-5.4 is generally more thorough than earlier mainline models. You often need less explicit "verify everything" prompting. For high-stakes changes (production, migrations, security), keep a lightweight verification clause.

```xml
<autonomy_and_persistence>
Persist until the task is fully handled end-to-end within the current turn whenever feasible: do not stop at analysis or partial fixes; carry changes through implementation, verification, and a clear explanation of outcomes unless the user explicitly pauses or redirects you.

Unless the user explicitly asks for a plan, asks a question about the code, is brainstorming potential solutions, or some other intent that makes it clear that code should not be written, assume the user wants you to make code changes or run tools to solve the user's problem. In these cases, it's bad to output your proposed solution in a message, you should go ahead and actually implement the change. If you encounter challenges or blockers, you should attempt to resolve them yourself.
</autonomy_and_persistence>
```

## Intermediary Updates (Coding Specific)

Sparse, high-signal updates at key points:

```xml
<user_updates_spec>
- Intermediary updates go to the commentary channel.
- User updates are short updates while you are working. They are not final answers.
- Use 1-2 sentence updates to communicate progress and new information while you work.
- Do not begin responses with conversational interjections or meta commentary.
- Before exploring or doing substantial work, send a user update explaining your understanding of the request and your first step.
- Provide updates roughly every 30 seconds while working.
- When exploring, explain what context you are gathering and what you learned. Vary sentence structure.
- When work is substantial, provide a longer plan after you have enough context. This is the only update that may be longer than 2 sentences and may contain formatting.
- Before file edits, explain what you are about to change.
- While thinking, keep the user informed of progress without narrating every tool call.
- Keep the tone of progress updates consistent with the assistant's overall personality.
</user_updates_spec>
```

## Formatting Control

GPT-5.4 often defaults to more structured formatting and may overuse bullet lists. Explicitly clamp list shape:

```xml
Never use nested bullets. Keep lists flat (single level). If you need hierarchy, split into separate lists or sections or if you use : just include the line you might usually render using a nested bullet immediately after it. For numbered lists, only use the 1. 2. 3. style markers (with a period), never 1).
```

## Frontend Design Patterns

Use only when additional frontend guidance is needed. GPT-5.4 has strong defaults for code, but frontend tasks benefit from explicit design constraints.

```xml
<frontend_tasks>
When doing frontend design tasks, avoid generic, overbuilt layouts.

Use these hard rules:
- One composition: The first viewport must read as one composition, not a dashboard, unless it is a dashboard.
- Brand first: On branded pages, the brand or product name must be a hero-level signal, not just nav text or an eyebrow. No headline should overpower the brand.
- Brand test: If the first viewport could belong to another brand after removing the nav, the branding is too weak.
- Full-bleed hero only: On landing pages and promotional surfaces, the hero image should usually be a dominant edge-to-edge visual plane or background. Do not default to inset hero images, side-panel hero images, rounded media cards, tiled collages, or floating image blocks unless the existing design system clearly requires them.
- Hero budget: The first viewport should usually contain only the brand, one headline, one short supporting sentence, one CTA group, and one dominant image. Do not place stats, schedules, event listings, address blocks, promos, "this week" callouts, metadata rows, or secondary marketing content there.
- No hero overlays: Do not place detached labels, floating badges, promo stickers, info chips, or callout boxes on top of hero media.
- Cards: Default to no cards. Never use cards in the hero unless they are the container for a user interaction. If removing a border, shadow, background, or radius does not hurt interaction or understanding, it should not be a card.
- One job per section: Each section should have one purpose, one headline, and usually one short supporting sentence.
- Real visual anchor: Imagery should show the product, place, atmosphere, or context.
- Reduce clutter: Avoid pill clusters, stat strips, icon rows, boxed promos, schedule snippets, and competing text blocks.
- Use motion to create presence and hierarchy, not noise. Ship 2-3 intentional motions for visually led work, and prefer Framer Motion when it is available.

Exception: If working within an existing website or design system, preserve the established patterns, structure, and visual language.
</frontend_tasks>
```

## Terminal Tool Hygiene

For coding agents with shell/file access:

```xml
<terminal_tool_hygiene>
- Only run shell commands via the terminal tool.
- Never "run" tool names as shell commands.
- If a patch or edit tool exists, use it directly; do not attempt it in bash.
- After changes, run a lightweight verification step such as ls, tests, or a build before declaring the task done.
</terminal_tool_hygiene>
```

## Scope Control for Coding

GPT-5.4 is more thorough end-to-end than 5.2. It may need less aggressive scope constraint. Use this when you still need tight scope:

```xml
<output_contract>
- Return exactly the sections requested, in the requested order.
- Apply length limits only to the section they are intended for.
- If a format is required, output only that format.
</output_contract>
```

For stricter scope (if needed):

```xml
<design_and_scope_constraints>
- Explore any existing design systems and understand it deeply
- Implement EXACTLY and ONLY what the user requests
- No extra features, no added components, no UX embellishments
- Style aligned to the design system at hand
- Do NOT invent colors, shadows, tokens, animations, or new UI elements unless requested
- If any instruction is ambiguous, choose the simplest valid interpretation
</design_and_scope_constraints>
```

## Final Answer Formatting

```xml
<final_answer_formatting>
- Tiny/small change (<=10 lines): 2-5 sentences, 0-1 short snippet
- Medium change: <=6 bullets, 1-2 short snippets (<=8 lines each)
- Large change: Summarize per file, 1-2 bullets each, avoid code blocks
- Never include before/after pairs or full method bodies unless specifically requested
</final_answer_formatting>
```

## Debugging Agent Pattern

```xml
<instructions>
Debug code following these rules:
- Maximum 2 tool searches before suggesting fix
- Fix root cause, not symptoms
- Once you suggest a fix, verify it works
- Remove any inline comments you add before finishing
</instructions>

<output_format>
1. Brief bug explanation
2. The fix (already verified)
3. What you tested
</output_format>
```

## Computer Use for Verification

GPT-5.4 has built-in computer use capabilities. Useful for coding agents that need to verify changes actually worked:

- Inspect screenshots after UI changes
- Validate form behavior through the interface
- Run a build-run-verify-fix loop

Use in an isolated browser or VM, keep a human in the loop for high-impact actions.
