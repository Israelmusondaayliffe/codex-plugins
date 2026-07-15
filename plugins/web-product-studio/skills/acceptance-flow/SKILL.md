---
name: acceptance-flow
description: Converts a web product brief into browser-verifiable user flows with preconditions, actions, expected observations, evidence, and failure states. Use before implementation or QA when completion needs to be proven through rendered behavior. Produces a validated acceptance-flow JSON that can guide manual Browser checks or Playwright automation.
---

# Acceptance Flow

## Overview

Define success as observable behavior, not as a claim that the code looks correct. Write flows at the user's altitude.

## Workflow

1. Extract actors, goals, starting states, critical paths, and failure paths from the brief.
2. Create one flow per material outcome using assets/acceptance-flow-template.json.
3. Keep actions atomic and expected observations visible in the browser.
4. Name the evidence required for every step.
5. Run scripts/validate_flows.py.
6. Execute flows in the built-in Browser. Use Playwright when repeatability or diagnostics add value.
7. Save pass, fail, or blocked evidence for each flow.

## Error Handling

- If authentication or data fixtures are unavailable, mark affected flows blocked with the missing prerequisite.
- If an expected result is not observable, replace it with a visible proxy or a source-owned API check.
- Do not mark a flow passed from code inspection alone when the requirement is rendered behavior.

## Reliability Notes

The model derives meaningful user flows. The validator enforces unique identifiers, ordered steps, expected observations, and evidence fields. Runtime proof still requires execution.

## Resources

- scripts/validate_flows.py validates flow records.
- references/flow-writing.md defines good checks.
- assets/acceptance-flow-template.json provides the schema.
