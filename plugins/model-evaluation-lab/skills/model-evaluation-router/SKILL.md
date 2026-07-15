---
name: model-evaluation-router
description: Routes model evaluation work across planning, benchmark execution or result normalization, and model-selection decisions. Use when a model, prompt, agent, tool, or deployment comparison is new, spans several stages, has unclear prerequisites, or needs the next safe evaluation step.
---

# Model Evaluation Router

## Overview

Act as the single front door for Model Evaluation Lab. Inspect the user's request and the artifacts already present, then route to one stage or sequence the full workflow without skipping a prerequisite.

## Workflow

1. Inventory the decision question, baseline, candidates, frozen plan, raw results, normalized results, and prior decision memo.
2. Load `references/workflow.md` and classify the request as plan, execute, normalize, decide, or full workflow.
3. Select exactly one next skill.
4. Record the required artifacts, missing input, routing reason, and next action.
5. Fill `assets/output-template.json` and run `scripts/validate_output.py` before handoff.
6. For a full workflow, return to this router after each validated stage and choose the next stage from fresh state.

## Boundaries

- Route prompt construction and prompt-only benchmark design to Model Prompt Lab.
- Route dataset preparation, remote jobs, and run tracking to Hugging Face when installed.
- Do not execute a benchmark without a frozen plan.
- Do not write a selection memo from partial or incomparable normalized results.

## Error recovery

Set `handoff_ready` to false when the requested stage lacks its prerequisite. Name the missing input and route back to the earliest stage that can create it. Do not guess that an artifact exists.

## Reliability

Routing uses explicit artifact state. The validator requires one allowed stage, one current state, named prerequisites, a missing-input statement, a next action, and a readiness gate.
