---
name: model-selection-memo
description: Produces a model-selection memo that separates measured benchmark results from judgment, tradeoffs, limitations, cost interpretation, and deployment conditions. Use when comparable evaluation runs are complete and a deployment, migration, rollback, or no-decision recommendation is needed.
---

# Model Selection Memo

## Overview

Turn normalized evaluation results into a bounded deployment decision. Preserve the difference between measurement, interpretation, and preference.

## Workflow

1. Confirm the frozen evaluation plan and comparable normalized run artifacts exist.
2. Load `references/workflow.md` and test the evidence against the preregistered decision rule.
3. Record measured results with stable source references and confidence.
4. State the recommendation, selected option, tradeoffs, limitations, and deployment conditions.
5. Separate marginal evaluation cost from whole-session orchestration usage.
6. Fill `assets/output-template.json` and run `scripts/validate_output.py`.
7. Route human-facing prose through Writing Quality when installed.

## Boundaries

- Do not rank candidates with materially different case coverage or runtime conditions.
- Do not replace missing evidence with qualitative preference.
- Do not call a small measured difference meaningful unless the plan defined that threshold.

## Error recovery

Set `decision_ready` to false and use `no-decision` when a candidate run is incomplete, a safety stop fired, plan conditions changed, or the decision rule cannot distinguish the candidates.

## Reliability

Interpretation uses judgment. The contract requires traceable measured results, a bounded recommendation, limitations, tradeoffs, cost treatment, deployment conditions, and a readiness gate.
