---
name: design-constitution-selector
description: Selects exactly one visual design skill for a web product based on brand, audience, content density, product type, and supplied references. Use before frontend styling when several installed design systems could conflict. Records one selected constitution or none, validates the choice, and keeps non-selected style skills out of the implementation context.
---

# Design Constitution Selector

## Overview

Choose a single visual authority for the build. Multiple broad style skills produce conflicting defaults and should not be loaded together.

## Workflow

1. Inspect brand references, product purpose, audience, content density, and existing interface.
2. Compare candidates using references/selection-guide.md.
3. Select one constitution, or none when the supplied design already controls the visual system.
4. Record assets/selection-template.json and run scripts/validate_selection.py.
5. Load only the selected skill. Keep all other style skills out of the implementation context.
6. Recheck the rendered product against that constitution and the source brief.

## Error Handling

- If a user explicitly names a style, honor it unless it conflicts with a higher-priority project contract.
- If no candidate fits, select none and derive tokens from the supplied brand or product reference.
- If two candidates appear equal, choose the one with fewer assumptions and record the rejected option.

## Reliability Notes

The model makes the aesthetic decision. The validator enforces exactly one allowed selection or none and requires evidence and rationale.

## Resources

- scripts/validate_selection.py validates the record.
- references/selection-guide.md maps contexts to candidates.
- assets/selection-template.json provides the schema.
