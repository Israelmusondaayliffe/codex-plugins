---
name: benchmark-runner
description: Executes or delegates a frozen model evaluation plan, records reproducible run conditions, and normalizes raw case results into a stable comparison schema. Use when running model, prompt, agent, or tool benchmarks locally or through Hugging Face jobs, or when completed raw runs need validation and aggregation.
---

# Benchmark Runner

## Overview

Execute the frozen plan on the authorized backend or normalize completed case results. Preserve raw evidence, record conditions, and stop when plan comparability breaks.

## Workflow

1. Validate that the evaluation plan is frozen and `plan_ready` is true.
2. Load `references/workflow.md` and choose local execution or an installed companion backend.
3. Record the plan hash, model and prompt identifiers, environment, dataset version, tool state, repetitions, and cost-accounting method.
4. Execute every frozen case or delegate it to the named backend. Do not add cases after results are visible.
5. Save raw case-level results before aggregation.
6. Run `scripts/normalize_results.py RAW.json NORMALIZED.json`.
7. Run `scripts/validate_output.py NORMALIZED.json` before handoff.

## Boundaries

The runner does not invent missing executions, scores, latency, cost, or safety outcomes. It does not change the frozen plan to improve a candidate's result.

## Error recovery

Mark the run partial when an execution fails or coverage differs. Preserve successful raw records, list the failed case identifiers, and require an equivalent rerun before comparison. Stop immediately when the plan's safety rule fires.

## Reliability

Backend invocation depends on the installed execution surface. Result normalization, aggregation, validation, and completeness checks are deterministic scripts.
