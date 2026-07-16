---
name: plugin-engineer
description: Create, update, validate, install, or package a Codex plugin required by an approved harness architecture. Use when several related skills need a public or team bundle, when the harness needs plugin metadata or a marketplace entry, or when an existing local plugin must be updated and reinstalled with source-cache and fresh-discovery proof.
---

# Plugin Engineer

Use the system `plugin-creator` skill as the source of truth for scaffolding, manifests, marketplace entries, validation, cachebusters, and reinstall behavior.

## Workflow

1. Confirm that a plugin is justified instead of a local skill.
2. Define owned skills, front door, external tools, hooks, apps, and explicit exclusions.
3. Scaffold with Plugin Creator. Do not hand-write initial marketplace structure.
4. Include only component fields backed by real files.
5. Validate every owned skill and the complete plugin.
6. Install or reinstall from the correct marketplace.
7. Compare source and installed cache.
8. Prove visibility from a new task or fresh prompt inventory.

Public repository creation and marketplace submission remain separate external actions.
