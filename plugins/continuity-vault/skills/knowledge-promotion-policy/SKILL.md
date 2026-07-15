---
name: knowledge-promotion-policy
description: Decides whether extracted knowledge belongs in a durable file, project reference, graph, memory candidate, or nowhere. Use when reusable context needs a governed destination with provenance, ownership, staleness review, and authority preserved. It recommends or records a promotion decision but does not rewrite authoritative sources without explicit scope.
---

# Knowledge Promotion Policy

## Overview

Promote only knowledge with a clear future use, named source, and suitable owner. A convenient recall surface is not automatically an authoritative destination.

## Workflow

1. Name the source, the reusable claim or procedure, and the future task it should support.
2. Determine its current authority and whether the content is stable, project-specific, derived, or temporary.
3. Choose a destination using `references/workflow.md`.
4. Record the owner, review trigger, provenance link, rationale, and any required approval.
5. Fill `assets/output-template.json` and run `scripts/validate_output.py`.
6. If writing is already authorized, create a new version without silently replacing the source. Otherwise return the decision only.

## Error Handling

- If provenance is missing, choose `none` until the source is recovered.
- If the content duplicates an authoritative file, link to that file instead of creating a competing copy.
- If sensitivity or ownership is unclear, mark approval required and stop before writing.

## Reliability Notes

The model judges reuse and authority. The validator requires the destination, source, authority, rationale, owner, review trigger, provenance action, and approval state.
