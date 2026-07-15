---
name: chart-message-audit
description: Audits whether each chart, dashboard panel, diagram, or visual caption supports its stated conclusion. Use when reviewing analytical visuals for evidence alignment, scale and denominator problems, misleading encodings, missing uncertainty, accessibility, or a publish, revise, or block decision.
---

# Chart Message Audit

## Overview

Test the relationship between the stated claim, the visual encoding, and the cited evidence. A visually polished chart fails when the evidence does not support its message.

## Workflow

1. Capture the artifact identifier, claim, visual type, audience, and evidence references.
2. Load `references/workflow.md` and run every required check.
3. Assign pass, warn, or fail to each check with observable evidence.
4. Set the verdict to pass, revise, or block.
5. Write ordered revision actions. Separate data changes, encoding changes, copy changes, and accessibility changes.
6. Fill `assets/output-template.json` and run `scripts/validate_output.py`.

## Boundaries

Do not repair the underlying analysis. Route calculation, sampling, or data-quality failures to the analysis owner. Audit the message and evidence contract only.

## Error recovery

Use `block` when the source is missing, the denominator is unknown, the chart contradicts its caption, or the claim requires causality that the evidence cannot support. Set `handoff_ready` to false and name the owner who must resolve it.

## Reliability

The model judges visual meaning. The validator requires a complete, uniquely identified check set, explicit evidence, an allowed verdict, revision actions, and a handoff state.
