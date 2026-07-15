---
name: brand-world-router
description: Routes brand visual work across decision brief, identity system, image-model selection, production prompt pack, and consistency verification. Use when a brand, campaign, logo system, visual world, or image series needs one coherent production path. Keeps positioning upstream, selects only the skills needed, and validates a primary route before generation.
---

# Brand World Router

## Overview

Choose the brand-production stage before generating images. Brand World owns the visual system after positioning and business strategy are settled.

## Workflow

1. Confirm the business or product context, audience, positioning source, visual deliverables, source assets, and forbidden directions.
2. Choose one primary route with references/workflow.md.
3. Run the plugin companion preflight when Canva or Creative Production may be needed.
4. Fill assets/output-template.json and run scripts/validate_output.py.
5. Use brand-brief-builder for decisions, brandkit for identity boards, brand-model-router for model choice, the selected image prompter for production prompts, and brand-consistency-verifier for series review.
6. Do not invent positioning or brand claims that the supplied strategy does not support.

## Error Handling

- If positioning is missing, stop at a bounded brief gap and hand off to Strategy Room.
- If source assets are required but missing, request or record them before an edit route.
- If visual directions conflict, choose one primary system and record rejected directions.

## Reliability Notes

The model selects the creative route. The validator enforces one allowed route, a named brand job, a rationale, and a positioning-source decision.

## Resources

- scripts/validate_output.py validates the structured artifact.
- references/workflow.md defines routing and decision rules.
- assets/output-template.json is the reusable output template.
- assets/output-schema.json is the deterministic validation contract.
