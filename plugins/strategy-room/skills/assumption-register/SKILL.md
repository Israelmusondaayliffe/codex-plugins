---
name: assumption-register
description: Creates and maintains a structured register of assumptions, evidence, confidence, reversibility, owners, test plans, and kill conditions. Use when a strategy, product plan, forecast, or decision depends on beliefs that may change. Validates unique assumption records and prevents unsupported certainty from disappearing into prose.
---

# Assumption Register

## Overview

Keep uncertainty durable after a decision. The register shows which beliefs are load-bearing, how they will be tested, and what result should change the plan.

## Workflow

1. Extract assumptions that must be true for the decision or plan to work.
2. Separate factual assumptions, behavioral assumptions, capability assumptions, and timing assumptions.
3. Record evidence, status, confidence, reversibility, owner, test, and kill condition with assets/output-template.json.
4. Use references/workflow.md to identify load-bearing items.
5. Run scripts/validate_output.py.
6. Review the register when evidence changes and preserve prior status in the durable project record.

## Error Handling

- Do not convert opinions into supported assumptions without evidence.
- If an assumption has no owner or test, mark it untested rather than omitting the gap.
- If a kill condition is vague, replace it with an observable threshold or event.

## Reliability Notes

The model identifies and frames assumptions. The validator enforces unique identifiers, required fields, allowed statuses, and allowed reversibility states.

## Resources

- scripts/validate_output.py validates the structured artifact.
- references/workflow.md defines routing and decision rules.
- assets/output-template.json is the reusable output template.
- assets/output-schema.json is the deterministic validation contract.
