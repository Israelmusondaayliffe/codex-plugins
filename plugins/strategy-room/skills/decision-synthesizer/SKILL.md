---
name: decision-synthesizer
description: Turns interviews, research, challenged assumptions, and distinct options into one evidence-linked recommendation with risks, conditions, reversibility, confidence, and a clean handoff. Use when a decision has enough inputs but remains unresolved. Produces a validated decision record and keeps measured evidence separate from judgment.
---

# Decision Synthesizer

## Overview

Converge on one recommendation without hiding uncertainty. Make the choice, conditions, and reasons inspectable by someone who did not join the working session.

## Workflow

1. State the decision and decision owner in one sentence.
2. Collect only evidence and options relevant to that decision.
3. Compare options with references/workflow.md, keeping facts separate from judgment.
4. Choose one recommendation and name its conditions, risks, reversibility, and confidence.
5. Fill assets/output-template.json and run scripts/validate_output.py.
6. Return a handoff that identifies the execution owner without starting execution.

## Error Handling

- If no option clears the minimum evidence bar, recommend a bounded test rather than a false final choice.
- If options are not meaningfully distinct, route back to multi-direction-explorer.
- If a load-bearing assumption remains untracked, add it to assumption-register before delivery.

## Reliability Notes

The model weighs evidence and makes the recommendation. The validator enforces unique options, a single recommendation, explicit risks and conditions, confidence, and handoff.

## Resources

- scripts/validate_output.py validates the structured artifact.
- references/workflow.md defines routing and decision rules.
- assets/output-template.json is the reusable output template.
- assets/output-schema.json is the deterministic validation contract.
