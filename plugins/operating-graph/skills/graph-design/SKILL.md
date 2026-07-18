---
name: graph-design
description: Convert a goal into a typed, validated operating graph with explicit authority, approvals, node contracts, dependencies, deliverables, independent evaluation, budgets, and safe parallel work. Use for new graph design or topology planning before execution.
---

# Graph Design

This workflow writes graph design artifacts but does not start a run.

1. Restate the immutable goal, deliverables, completion criteria, authority node, approvals, permissions, and hard limits.
2. Choose the smallest sufficient set of typed nodes. Separate authority, controller, production, shared state, and independent evaluation responsibilities.
3. Define every node contract and typed edge. Mark optional work explicitly and use `next_epoch` for every feedback cycle.
4. Add an independent evaluator path for every required deliverable. Add an approval predecessor for every external side-effect node.
5. Save the definition as `graph.json` and a Mermaid representation.
6. Run `python3 scripts/graphctl.py validate <graph.json>` and fix every violation before presenting the graph.
7. Ask for approval before handing the graph to `$graph-run` when material external actions exist.

Do not execute the graph or apply rewrites. Never change authority or weaken completion criteria to make validation pass.

Read [graph-contract.md](../../references/graph-contract.md) before authoring the JSON. Use [graph.json](../../assets/templates/graph.json) as a starting point when available.
