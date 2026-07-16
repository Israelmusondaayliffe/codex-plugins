---
name: agents-md-engineer
description: Design, rewrite, split, or verify a Codex AGENTS.md instruction chain across global, workspace, project, and nested scopes. Use when users ask what belongs in AGENTS.md, want instructions modeled on an existing harness, need shorter or clearer agent guidance, have conflicting instruction files, or need templates that encode role, boundaries, routing, workflow, and verification.
---

# AGENTS.md Engineer

Keep instruction files short, accurate, durable, and scoped to the directories that need them.

## Workflow

1. Inspect the applicable chain and any override files.
2. Identify repeated behavior that truly belongs in persistent instructions.
3. Move detailed workflows into skills or references and exact checks into scripts, rules, hooks, or templates.
4. Separate global personal policy from workspace layout and project commands.
5. Preserve existing load-bearing rules and show a diff for updates.
6. Verify that closer files refine rather than silently contradict broader guidance.

Use the templates under `../../assets/`. Replace every bracketed placeholder. Do not copy the advanced case study as a default.
