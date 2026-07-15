---
name: brand-brief-builder
description: Turns approved business context, positioning, audience, references, and deliverables into a production-ready visual brand brief. Use when generating a logo system, identity board, campaign series, or image prompt pack from settled strategy. Validates audience, positioning, visual principles, forbidden drift, and required deliverables without inventing strategy.
---

# Brand Brief Builder

## Overview

Translate an approved strategy into visual decisions that downstream image tools can follow consistently. Keep unknowns visible instead of filling them with generic taste.

## Workflow

1. Collect the positioning source, audience, desired response, required deliverables, existing assets, and constraints.
2. Extract brand attributes and convert each one into observable visual implications with references/workflow.md.
3. Define visual principles, must-avoid directions, typography and color boundaries when supplied, and evidence references.
4. Fill assets/output-template.json and run scripts/validate_output.py.
5. Send the validated brief to brand-model-router or brandkit.
6. Require a new decision if production feedback would change positioning rather than execution.

## Error Handling

- If positioning is not approved, mark it missing and do not create a substitute claim.
- If a visual adjective has no observable implication, rewrite it into a specific design rule.
- If deliverables have conflicting formats or audiences, split them into named production tracks.

## Reliability Notes

The model interprets brand intent. The validator requires the audience, positioning, attributes, visual principles, must-avoid list, and deliverables.

## Resources

- scripts/validate_output.py validates the structured artifact.
- references/workflow.md defines routing and decision rules.
- assets/output-template.json is the reusable output template.
- assets/output-schema.json is the deterministic validation contract.
