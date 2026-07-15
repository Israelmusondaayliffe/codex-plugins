---
name: web-product-router
description: Routes web product requests to greenfield build, redesign, image-first implementation, targeted fix, or quality assurance. Use when a frontend or web app request could trigger several build and design skills. Selects one primary path, one design constitution, and browser-verifiable acceptance flows before implementation.
---

# Web Product Router

## Overview

Choose the build mode before loading implementation and design skills. Keep visual direction singular and make completion testable in a browser.

## Workflow

1. Inspect the repository, brief, supplied images, and rendered state when available.
2. Choose one route using references/routing.md.
3. Select one visual system with design-constitution-selector when visual direction is in scope.
4. Define browser-verifiable flows with acceptance-flow.
5. Record assets/route-template.json and run scripts/validate_route.py.
6. Load only the route owners and implement.
7. Verify the acceptance flows in the built-in Browser. Use Playwright when repeatable automation or browser diagnostics are needed.

## Error Handling

- If the task is diagnostic only, do not route to implementation.
- If a supplied image is authoritative, preserve its information hierarchy before adding a design constitution.
- If visual systems conflict, select one and record rejected alternatives.
- If a flow cannot be observed, mark it blocked rather than complete.

## Reliability Notes

The model selects the route and implementation skills. The validator enforces one route, one design constitution or none, and a named acceptance-flow artifact.

## Resources

- scripts/validate_route.py validates the plan.
- references/routing.md defines route ownership.
- assets/route-template.json records the decision.
