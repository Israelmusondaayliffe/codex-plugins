---
name: agent-ops-router
description: Routes requests among agent design, workflow design, Goal engineering, bounded loop execution, audit, run, and resume. Use when a request mentions agents, autonomous workflows, persistent Goals, monitoring loops, retries, handoffs, or resuming an existing system. Enforces one primary operational route and prevents a general outcome workflow from being mistaken for an agent-system design.
---

# Agent Ops Router

## Overview

Select the operational object before choosing a build or execution skill. Agent systems need explicit authority, stops, evidence, and failure behavior.

## Workflow

1. Determine whether the user is creating, running, auditing, resuming, or monitoring.
2. Choose one primary route with references/routing.md.
3. Complete assets/route-template.json and run scripts/validate_route.py.
4. Load only the route owner:
   - agent-design: agent-builder
   - goal-design: loop-goal-engineer
   - goal-run or resume: goal-runner
   - bounded-loop: loopy
   - audit: agent-system-audit
5. Use outcome-engine only when the request is a general idea-to-result workflow rather than an agent operating system.
6. Verify the chosen route names an outcome, evidence surface, boundaries, and stop condition.

## Error Handling

- If two routes apply, choose a primary route and list the secondary handoff.
- If a run request has no existing contract, route to design before execution.
- If authority or stop conditions are absent, do not start an autonomous loop.

## Reliability Notes

The model classifies the operating object. The validator enforces an allowed route and the four required control fields.

## Resources

- scripts/validate_route.py validates routing records.
- references/routing.md defines boundaries.
- assets/route-template.json provides the record.
