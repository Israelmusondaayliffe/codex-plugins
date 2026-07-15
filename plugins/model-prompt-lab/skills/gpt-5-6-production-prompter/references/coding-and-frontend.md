# Coding and Frontend Patterns for GPT-5.6

GPT-5.6 carries forward strong coding capability and adds two headline changes: notably better frontend design judgment (layout, visual hierarchy, polish) and a proactive multi-step disposition that makes the autonomy policy the load-bearing section of every coding agent prompt. Validation by running remains the verification default.

## Validation by running

When tools allow, ask the model to run actual validation rather than self-critique:

```text
After making changes, run the most relevant validation available:
- targeted unit tests for changed behavior
- type checks or lint checks when applicable
- build checks for affected packages
- a minimal smoke test when full validation is too expensive

If validation cannot be run, explain why and describe the next best check.
```

This replaces `<verification_loop>` for routine coding work. Reserve the verification block for high-impact changes (production, migrations, security) where available validation tools are insufficient.

## The lean coding agent pattern

```text
Role: A capable coding agent operating in the user's local environment with read, edit, and shell tools.

# Goal
Complete the requested code change end to end: implementation, validation, and a brief summary of what changed.

# Success criteria
- The change implements what the user asked for, no more.
- Targeted tests pass, type checks pass, the affected build succeeds.
- The final response summarizes what changed and what was tested.

# Constraints
- Use the patch or edit tool directly. Do not run patch operations as shell commands.
- Respect the existing design patterns and code style.

# Autonomy
For requests to review, diagnose, or plan: inspect and report; do not change code
unless asked. For requests to change, build, or fix: make the in-scope changes and
run non-destructive validation without asking. Safe without asking: reading files,
inspecting logs, editing in-scope code, running tests, lint, type checks, and
builds. Require confirmation for pushes, deploys, deletions outside the change
scope, dependency upgrades, and any material expansion of scope. If the target
branch or environment is ambiguous, ask.

# Output
- Final response length scaled to change size:
  - Tiny change (up to 10 lines): 2-5 sentences, optional short snippet.
  - Medium change: up to 6 bullets, 1-2 short snippets (up to 8 lines each).
  - Large change: per-file summary, 1-2 bullets each, no full code blocks.
- Never include before/after pairs or full method bodies unless requested.

# Stop rules
- Stop when success criteria are met.
- If a blocker is genuinely external (missing credentials, broken environment), name the blocker and propose the smallest ask.
```

Note what is absent: no persistence block (5.6 is persistent by default), no "be concise" (the output section is a contract, not a mood), no repeated approval language (the autonomy policy owns it, once).

## Autonomy for coding agents

The compact policy above is the default for local dev agents. Tune it per environment:

- **Sandboxed CI agent:** widen safe actions (branch creation, dependency installs); the boundary is anything leaving the sandbox.
- **Production-adjacent agent:** narrow to read-only plus explicitly listed paths; every write confirms.
- **Review-only agent:** the read-shaped clause is the whole policy; "do not implement changes unless the request also asks for them" is the load-bearing line.

Do not repeat "ask first" in constraints, personality, or tool descriptions. On 5.6 that repetition causes the agent to pause on safe, expected actions.

## Intermediary updates

Lean form in the prompt body:

```text
# Collaboration style
- Send brief commentary updates at major phase changes (1-2 sentences). Don't narrate routine tool calls.
- Before file edits, briefly state what's about to change.
- Don't open responses with conversational filler or meta commentary.
```

The detailed `<user_updates_spec>` block from `references/core-prompt-blocks.md` remains available for streaming surfaces where update cadence is a product requirement.

## PTC in coding workflows (new for 5.6)

Bounded code-adjacent stages fit PTC's task shape: collecting lint results across packages, aggregating test failures, joining coverage data with changed files, deduplicating dependency vulnerabilities. The pattern:

- PTC stage: gather and reduce (only read-shaped tools opted into `allowed_callers`)
- Direct calls: every edit, every judgment about what a failure means, every action behind the autonomy boundary

Never opt side-effecting tools (write, deploy, delete) into `allowed_callers`. See `references/programmatic-tool-calling.md`.

## Pro mode for high-value code review

Complex review with clear criteria is a named pro-mode use case. Keep the prompt outcome-focused:

```text
Review this database migration plan for failure modes that could cause data loss
or extended downtime. For each finding, cite the relevant step, estimate impact
and likelihood, and recommend a specific mitigation. Return the five most
important risks in severity order.
```

Configure `reasoning.mode: "pro"`; do not add "think harder" instructions. See `references/pro-mode-and-multi-agent.md`.

## Formatting control

If lists drift into nested bullets:

```text
Never use nested bullets. Keep lists flat (single level). If you need hierarchy, split into separate lists or sections. For numbered lists, only use the 1. 2. 3. style markers (with a period), never 1).
```

Less necessary than on 5.4/5.5; add only when evals show the drift.

## Frontend design patterns

GPT-5.6 creates more polished and usable websites and applications, with stronger layout, visual hierarchy, and design judgment. Practical consequence: the heavy constraint blocks that 5.4/5.5 needed can often shrink. Keep the rules that encode brand and design-system requirements; test removing the rules that merely compensated for weak default taste.

The full constraint block, for when evals still show generic output:

```xml
<frontend_tasks>
When doing frontend design tasks, avoid generic, overbuilt layouts.

Use these hard rules:
- One composition: The first viewport must read as one composition, not a dashboard, unless it is a dashboard.
- Brand first: On branded pages, the brand or product name must be a hero-level signal, not just nav text or an eyebrow. No headline should overpower the brand.
- Brand test: If the first viewport could belong to another brand after removing the nav, the branding is too weak.
- Full-bleed hero only: On landing pages and promotional surfaces, the hero image should usually be a dominant edge-to-edge visual plane or background. Do not default to inset hero images, side-panel hero images, rounded media cards, tiled collages, or floating image blocks unless the existing design system clearly requires them.
- Hero budget: The first viewport should usually contain only the brand, one headline, one short supporting sentence, one CTA group, and one dominant image.
- No hero overlays: Do not place detached labels, floating badges, promo stickers, info chips, or callout boxes on top of hero media.
- Cards: Default to no cards. Never use cards in the hero unless they are the container for a user interaction.
- One job per section: Each section should have one purpose, one headline, and usually one short supporting sentence.
- Real visual anchor: Imagery should show the product, place, atmosphere, or context.
- Reduce clutter: Avoid pill clusters, stat strips, icon rows, boxed promos, schedule snippets, and competing text blocks.
- Use motion to create presence and hierarchy, not noise. Ship 2-3 intentional motions for visually led work.

Exception: If working within an existing website or design system, preserve the established patterns, structure, and visual language.
</frontend_tasks>
```

Migration guidance: on 5.6, run the eval without this block first. Restore individual rules, not the whole block, for the specific defaults that regress.

## Render-and-inspect pattern

```text
Render the artifact before finalizing. Inspect the rendered output for layout, clipping, spacing, missing content, and visual consistency. Revise until the rendered output matches the requirements.
```

Still the right verification for visual work; concrete inspection beats speculative reflection.

## Terminal tool hygiene

```xml
<terminal_tool_hygiene>
- Only run shell commands via the terminal tool.
- Never "run" tool names as shell commands.
- If a patch or edit tool exists, use it directly; do not attempt it in bash.
- After changes, run a lightweight verification step such as ls, tests, or a build before declaring the task done.
</terminal_tool_hygiene>
```

## Scope control

For surgically tight scope when the agent has been observed adding features:

```xml
<design_and_scope_constraints>
- Explore any existing design systems and understand them deeply.
- Implement EXACTLY and ONLY what the user requests.
- No extra features, no added components, no UX embellishments.
- Do not invent colors, shadows, tokens, animations, or new UI elements unless requested.
- If any instruction is ambiguous, choose the simplest valid interpretation.
</design_and_scope_constraints>
```

Try tightening `# Goal` and `# Success criteria` first; add this block only if the drift persists.

## Debugging agent pattern

```text
Role: A debugging agent.

# Goal
Find and fix the root cause of the reported bug.

# Success criteria
- Bug explanation identifies root cause, not symptoms.
- Fix is implemented and verified to work.
- Inline comments added during debugging are removed before finishing.

# Autonomy
Reading code, logs, and test output, adding temporary instrumentation, editing
in-scope files, and running tests are safe without asking. Confirm before touching
config outside the affected module or changing dependencies.

# Output
1. Brief bug explanation.
2. The fix (already verified).
3. What was tested.

# Stop rules
- Stop when the fix is verified.
- After two failed fix attempts, report findings and the most promising remaining hypothesis instead of continuing blind.
```

## Computer use for verification

Carried forward: inspect screenshots after UI changes, validate form behavior, run build-run-verify-fix loops. Use in an isolated browser or VM; keep a human in the loop for high-impact actions. Vision note for 5.6: `original`/`auto` image detail preserves original dimensions, which improves click-accuracy and localization work at the cost of more input tokens on large screenshots. See `references/extraction-and-vision.md`.

## What changed from 5.5 for coding

| Aspect | 5.5 default | 5.6 default | Action |
|--------|-------------|-------------|--------|
| Approval behavior | Collaboration bullets | One autonomy policy; repetition causes pauses | Consolidate |
| Frontend constraints | Full block usually needed | Stronger default judgment | Test without; restore rules individually |
| Verification | Validation by running | Same | Keep |
| Batch code-data stages | Parallel direct calls | PTC candidate | Benchmark both routes |
| High-value review | high/xhigh effort | Pro mode option | Compare on evals |
| Output length | Contract in # Output | Same, plus 5.6 is more concise by default | Drop legacy "be concise"; keep the contract |
