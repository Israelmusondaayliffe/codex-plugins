---
name: analysis-to-story-router
description: Routes checked analysis to the right notebook, chart, dashboard, report, deck, executive readout, or publishable site. Use when the user has data findings or an analysis artifact and needs to choose a decision-facing format, audience, companion tools, evidence limits, and handoff path before production.
---

# Analysis to Story Router

## Overview

Choose the smallest delivery format that can support the audience's decision. Preserve the analytical source of truth and record uncertainty before production begins.

## Workflow

1. Inventory the source artifacts, decision question, audience, time horizon, and analysis state.
2. Load `references/workflow.md` and apply its routing table.
3. Select one primary format and name any secondary export only when it serves a distinct consumer.
4. Declare the companion capabilities needed for production. Treat unavailable companions as a routing constraint, not as installed functionality.
5. Record evidence limits, risks, and the next coordinator skill.
6. Fill `assets/output-template.json` and run `scripts/validate_output.py` before handoff.

## Boundaries

- Do not recalculate metrics or alter source data.
- Do not select a deck because the output is executive-facing when a one-page readout is sufficient.
- Do not promise interactive behavior without an installed publishing surface and a test plan.

## Error recovery

Set `handoff_ready` to false when the decision question is unclear, the analysis is disputed, or a required source is missing. Return the exact missing input and the safest interim format.

## Reliability

Format selection is judgment. The output contract, readiness state, evidence limits, and named handoff are deterministic and validated.
