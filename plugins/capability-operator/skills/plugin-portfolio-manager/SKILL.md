---
name: plugin-portfolio-manager
description: Maintains a decision ledger for personal plugins, their owned skills, companions, tests, versions, and retirement state. Use when planning, building, auditing, upgrading, or retiring multiple plugins. Validates ownership and lifecycle fields so plugin bundles remain intentional instead of becoming untracked collections of copied skills.
---

# Plugin Portfolio Manager

## Overview

Track why each plugin exists, what it owns, what it only coordinates with, and what proof is required before lifecycle changes.

## Workflow

1. Start from assets/portfolio-template.json.
2. Record each plugin owner, purpose, version, owned skills, companion plugins, verification surface, and status.
3. Run scripts/validate_portfolio.py.
4. Reconcile the ledger with capability-inventory and live plugin listing.
5. Use references/lifecycle.md before promoting, replacing, or retiring a plugin.

## Error Handling

- Treat unverified installation or discovery as a failing lifecycle gate.
- Preserve unresolved ownership collisions as explicit decisions required.
- Do not mark a plugin retired until dependents and loose-skill migration are accounted for.

## Reliability Notes

The validator enforces complete records, unique names, and allowed states. Strategic grouping and ownership remain human decisions supported by evidence.

## Resources

- scripts/validate_portfolio.py validates the ledger.
- references/lifecycle.md defines lifecycle gates.
- assets/portfolio-template.json provides the schema.
