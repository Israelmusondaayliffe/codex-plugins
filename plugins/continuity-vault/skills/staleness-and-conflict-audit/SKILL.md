---
name: staleness-and-conflict-audit
description: Audits a bounded source set for stale claims, conflicting instructions, broken authority assumptions, and unresolved ownership. Use when prior plans, memories, prompt guidance, plugin records, or operating rules may be reused. Produces read-only findings with evidence and recommended review actions. It never resolves a conflict by silently editing or deleting a source.
---

# Staleness And Conflict Audit

## Overview

Test whether prior knowledge is still safe to use. Compare source dates, authority layers, current live state, and ownership before accepting a claim.

## Workflow

1. Define the source set, audit date, current decision, and facts that would be costly to get wrong.
2. Rank the sources by the active authority hierarchy.
3. Check dates, superseding files, live platform state, unresolved placeholders, and instruction conflicts using `references/workflow.md`.
4. Record each finding with its source, kind, severity, evidence, and recommended action.
5. Set the result to `clear`, `needs-review`, or `blocked`, then fill `assets/output-template.json`.
6. Run `scripts/validate_output.py` and return the read-only audit.

## Error Handling

- If a load-bearing source is unavailable, set the result to `blocked`.
- If current platform behavior is involved, verify it live or mark the claim unverified.
- If authority is tied, preserve the conflict and ask the owner to resolve it.

## Reliability Notes

The model interprets evidence and authority. The validator enforces unique findings, named evidence, severity, recommended actions, a review result, and a false mutation flag.
