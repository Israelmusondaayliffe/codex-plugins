---
name: writing-quality-router
description: Routes writing requests to intent architecture, rewriting, detect-only review, or validation. Use when a user asks to draft, rewrite, tighten, humanize, review, or quality-check prose and the correct degree of intervention is unclear. Preserves source claims, separates diagnosis from mutation, and validates the route before execution.
---

# Writing Quality Router

## Overview

Choose the smallest writing workflow that can satisfy the request. Do not rewrite text when the user asked only for findings.

## Workflow

1. Identify the requested operation, audience, medium, decision, and constraints.
2. Select exactly one primary route using references/routing.md.
3. Record the route in assets/route-template.json and run scripts/validate_route.py.
4. Execute the selected skill:
   - intent-architecture: business-writing-intent-enforcer
   - rewrite: business-writing-intent-enforcer, then writing-enforcer
   - detect-only: writing-enforcer in report-only mode
   - validation: writing-enforcer against the supplied draft and constraints
5. Use claim-boundary-checker when factual claims exceed the supplied evidence or are unstable.
6. Recheck that the final response matches the requested operation and did not silently expand the factual scope.

## Error Handling

- If the operation is ambiguous but low-risk, choose the least mutating route and state the assumption.
- If the route JSON fails validation, fix the invalid route or missing rationale before writing.
- If sources conflict, preserve the conflict and route factual review to claim-boundary-checker.
- If the user asks for output only, keep routing notes internal.

## Reliability Notes

The model interprets intent and performs the prose work. The validator enforces one allowed route and a recorded rationale. Claim support is checked separately so style edits do not fabricate evidence.

## Resources

- scripts/validate_route.py validates routing records.
- references/routing.md defines selection rules and boundaries.
- assets/route-template.json is the reusable route record.
