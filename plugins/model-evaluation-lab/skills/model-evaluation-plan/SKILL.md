---
name: model-evaluation-plan
description: Creates a reproducible model evaluation plan with a fixed decision, baselines, candidates, representative cases, metrics, budget, environment, execution backend, and stopping rules. Use when preparing to compare models, prompts, agents, tool behavior, migrations, or deployment configurations.
---

# Model Evaluation Plan

## Overview

Turn a model choice into a preregistered comparison. Fix what will be measured, how it will be run, and what decision the evidence must support before candidate results are inspected.

## Workflow

1. Define one deployment decision and the baseline that remains if the evaluation is inconclusive.
2. Name candidate configurations precisely, including model, prompt, tools, and relevant runtime settings.
3. Load `references/workflow.md` and construct representative success, boundary, and failure cases.
4. Define objective metrics and a named human rubric only where deterministic checks are insufficient.
5. Record dataset provenance, environment, execution backend, budget, cost accounting method, and stopping rules.
6. Fill `assets/output-template.json` and run `scripts/validate_output.py`.
7. Freeze the validated plan before execution.

## Boundaries

- Do not select metrics after seeing results.
- Do not treat a prompt-only comparison as a model comparison when other conditions changed.
- Do not mix whole-session usage with marginal prompt or plugin cost.

## Error recovery

Set `plan_ready` to false when candidate conditions are not comparable, cases lack expected behavior, the budget cannot cover the minimum sample, or the decision rule is ambiguous.

## Reliability

Case design and metric choice require judgment. The schema enforces explicit candidates, unique cases and metrics, provenance, cost limits, stopping rules, backend, and readiness.
