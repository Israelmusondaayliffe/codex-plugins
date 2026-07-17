---
name: matt-setup-matt-pocock-skills
description: Configure a project for the Matt-prefixed Codex workflow by recording its tracker, terminology and decision docs, output paths, and verification surfaces. Use once before a project runs the full Matt flow or when its workflow configuration changes.
---

# Setup Matt Pocock Skills for Codex

Follow the active `AGENTS.md` chain. Inspect the project before proposing changes.

## Discover

Identify:

- the work tracker, if any
- durable context, glossary, decision, spec, and evidence locations
- existing project instructions and output rules
- software test, build, lint, and review commands
- non-code verification surfaces such as renderers, source ledgers, connector checks, or approval gates
- external actions that remain permission-gated

## Recommend

Prefer the project's existing conventions. When none exist, recommend local Markdown tracking and one durable context file before introducing an external tracker. Use the bundled tracker and domain templates as examples, not as mandatory structure.

## Confirm and write

Show the exact proposed changes before editing project contract files. Do not create or replace an `AGENTS.md` file when the current chain already provides the needed rules. Do not edit `CLAUDE.md` as a substitute for Codex instructions.

Record the smallest configuration the Matt flow needs:

- where specs and tickets live
- how blocking edges are represented
- where shared terms and decisions live
- where handoffs and evidence live
- which checks prove a slice complete

Creating tracker labels, issues, remote folders, or connector state requires task-specific authorization and post-action verification.
