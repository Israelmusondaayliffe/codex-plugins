---
name: capability-inventory
description: Builds a read-only inventory of loose skills, plugin source bundles, installed plugins, caches, and optional task-visible capabilities. Use before global skill or plugin work, after installs, or when filesystem presence and Codex visibility may disagree. Emits exact paths and fingerprints so later audits can distinguish duplicates from drift.
---

# Capability Inventory

## Overview

Establish what exists at each capability layer before changing anything. Filesystem presence alone does not prove installation or task visibility.

## Workflow

1. Confirm the home directories and plugin source root.
2. Run scripts/collect_inventory.py with an explicit output path.
3. Add task-visible proof through fresh-task-discovery-verifier when discovery matters.
4. Compare the inventory layers using references/layers.md.
5. Report missing layers and stale or unreadable manifests. Do not repair them unless the user authorized changes.

## Error Handling

- Preserve partial results when one root or command is unavailable.
- Record command errors in the inventory rather than treating the missing data as an empty layer.
- Do not follow unknown symlinks outside the selected roots.

## Reliability Notes

The script enumerates paths, reads manifests, and fingerprints SKILL.md files deterministically. Interpretation of ownership and desired state remains a separate audit decision.

## Resources

- scripts/collect_inventory.py creates the inventory.
- references/layers.md defines the evidence layers.
- assets/inventory-template.json documents the output shape.
