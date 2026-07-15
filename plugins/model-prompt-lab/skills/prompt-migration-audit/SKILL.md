---
name: prompt-migration-audit
description: Audits a prompt migration for stale model assumptions, unsupported parameters, copied over-instruction, tool-policy drift, output-contract loss, and unverified current claims. Use when moving prompts between GPT, Fable, Mythos, Codex, ChatGPT, or API surfaces. Produces a validated finding ledger and verification list without silently rewriting the prompt.
---

# Prompt Migration Audit

## Overview

Check what must change and what must remain stable before a prompt is migrated. Audit mode is read-only unless the user separately authorizes a rewrite.

## Workflow

1. Record the source model, target model, prompt surface, source prompt, and evidence set.
2. Verify current target-model behavior through the owning documentation when settings or tools matter.
3. Review the prompt with references/workflow.md.
4. Record findings and unsupported parameters in assets/output-template.json.
5. Run scripts/validate_output.py.
6. Prioritize findings by outcome risk and hand the ledger to the correct model-specific prompter for an authorized migration.

## Error Handling

- If the target model is not verified, mark all model-specific recommendations provisional.
- If the source prompt's job is unclear, do not optimize wording before defining the output contract.
- If the user requested an audit only, do not return a rewritten prompt.

## Reliability Notes

The model assesses model-specific drift. The validator requires source and target models, unique findings, unsupported-parameter accounting, and an explicit verification decision.

## Resources

- scripts/validate_output.py validates the structured artifact.
- references/workflow.md defines routing and decision rules.
- assets/output-template.json is the reusable output template.
- assets/output-schema.json is the deterministic validation contract.
