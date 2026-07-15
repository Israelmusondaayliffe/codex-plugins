---
name: signal-to-icp
description: Converts recent public pain, buying, engagement, and language signals into an evidence-backed ideal-customer profile with disqualifiers, confidence, and verification gaps. Use when market research or first-customer discovery must become a bounded ICP hypothesis instead of a generic persona. Validates source-linked signals and unique evidence records.
---

# Signal To Icp

## Overview

Build the customer hypothesis from observed signals. Keep the profile narrow enough to guide prospecting and honest enough to show what is still unproven.

## Workflow

1. Define the offer, evidence window, allowed sources, and commercial decision.
2. Collect or receive source-linked signals and remove duplicates or weak paraphrases.
3. Cluster pain, urgency, buying context, role, company state, and language with references/workflow.md.
4. Write the ICP hypothesis, disqualifiers, confidence, and gaps in assets/output-template.json.
5. Run scripts/validate_output.py.
6. Hand the validated profile to first-customer-finder or market-narrative-builder.

## Error Handling

- If signals are older than the allowed window, label them stale or exclude them.
- If a signal has no source or date, do not treat it as evidence.
- If the profile is broad enough to include everyone, narrow it by pain, trigger, role, and company state.

## Reliability Notes

The model interprets evidence clusters. The validator requires unique source-linked signals, a complete ICP hypothesis, disqualifiers, confidence, and verification gaps.

## Resources

- scripts/validate_output.py validates the structured artifact.
- references/workflow.md defines routing and decision rules.
- assets/output-template.json is the reusable output template.
- assets/output-schema.json is the deterministic validation contract.
