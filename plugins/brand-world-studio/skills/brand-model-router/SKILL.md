---
name: brand-model-router
description: Selects the image model, mode, source requirements, and prompt format for a brand visual job. Use when choosing between GPT Image 2, Nano Banana, Canva, Creative Production, or a no-generation route for identity boards, edits, series, logos, and campaign assets. Validates one model route and records alternatives and missing companions.
---

# Brand Model Router

## Overview

Choose the production surface from the job, not habit. Model strengths, edit needs, reference handling, text rendering, and available companions should drive the route.

## Workflow

1. Read the approved brand brief and define the exact output job, mode, references, text needs, series size, and edit constraints.
2. Check available companion plugins before selecting a connected surface.
3. Compare options using references/workflow.md.
4. Fill assets/output-template.json and run scripts/validate_output.py.
5. Hand off to gpt-image-2-unified, nano-banana-unified, brandkit, Canva, Creative Production, or a manual production route.
6. Keep model-specific claims provisional until verified against current documentation.

## Error Handling

- If a required companion is unavailable, choose an owned prompt route or report the missing capability.
- If source images are required but absent, do not route to edit or composition.
- If the user names a model explicitly, honor it unless the requested operation is unsupported.

## Reliability Notes

The model makes the creative production choice. The validator enforces one allowed model, job, mode, requirements, rationale, and alternatives.

## Resources

- scripts/validate_output.py validates the structured artifact.
- references/workflow.md defines routing and decision rules.
- assets/output-template.json is the reusable output template.
- assets/output-schema.json is the deterministic validation contract.
