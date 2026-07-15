---
name: executive-readout-builder
description: Builds an answer-first executive readout from checked evidence, with decisions, risks, caveats, and next actions. Use when analysis must become a concise leadership memo, meeting readout, decision brief, report summary, or deck narrative without introducing unsupported claims.
---

# Executive Readout Builder

## Overview

Convert checked evidence into a bounded decision artifact. Lead with the answer, show the evidence that changes the decision, and keep measured results separate from judgment.

## Workflow

1. Confirm the decision question, audience, delivery format, route artifact, and visual audit verdict.
2. Load `references/workflow.md` and assemble the answer-first sequence.
3. Create evidence entries with claim, source, and confidence.
4. State decisions, risks, caveats, and next actions with owners or conditions when known.
5. Separate measured findings from recommendations.
6. Fill `assets/output-template.json` and run `scripts/validate_output.py`.
7. Send human-facing prose through Writing Quality when installed.

## Boundaries

- Do not introduce new claims, estimates, or proof.
- Do not hide contradictory or incomplete evidence in an appendix.
- Do not convert association into causality.

## Error recovery

Set `publish_ready` to false when a material evidence reference is missing, a blocked chart remains unresolved, or the answer cannot be bounded to the decision question. Return the required repair instead of writing around the gap.

## Reliability

Narrative construction uses judgment. The schema requires traceable evidence, explicit caveats, decisions, risks, next actions, and a publish gate.
