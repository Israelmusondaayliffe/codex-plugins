---
name: prompt-benchmark-designer
description: Designs reproducible prompt benchmarks with success, boundary, and failure cases, objective assertions, metrics, cost limits, and stopping rules. Use when comparing prompts, migrating models, testing tool behavior, or deciding whether a prompt change is production-ready. Produces a validated benchmark specification but does not claim results before runs occur.
---

# Prompt Benchmark Designer

## Overview

Turn a prompt-quality question into a testable benchmark. Separate benchmark design from execution so expected behavior is fixed before results are seen.

## Workflow

1. Define the user task, baseline, candidate prompt, model conditions, and decision the benchmark must support.
2. Create representative success, boundary, and failure cases with references/workflow.md.
3. Write objective assertions for deterministic behavior and reserve subjective qualities for a named human rubric.
4. Set metrics, sample size, cost or time limits, and stopping rules.
5. Fill assets/output-template.json and run scripts/validate_output.py.
6. Hand the validated specification to an authorized benchmark runner. Do not fill result fields from expectation.

## Error Handling

- Reject cases that only check whether an output file exists when content correctness matters.
- If a metric cannot distinguish the candidates, replace it before running.
- If model or tool settings are unstable, record and verify them before comparison.

## Reliability Notes

The model designs cases and metrics. The validator requires non-empty cases, metrics, stopping rules, unique case identifiers, and all required case fields.

## Resources

- scripts/validate_output.py validates the structured artifact.
- references/workflow.md defines routing and decision rules.
- assets/output-template.json is the reusable output template.
- assets/output-schema.json is the deterministic validation contract.
