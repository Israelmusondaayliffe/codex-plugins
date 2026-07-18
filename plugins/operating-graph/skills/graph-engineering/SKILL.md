---
name: graph-engineering
description: Route operating graph, graph engineering, agent organization design, dynamic agent organization, adaptive multi-agent workflow, and graph-level loop requests to the correct design, run, inspect, rewrite, debug, or verify workflow.
---

# Graph Engineering

Identify the requested operation before touching a run:

- Design a new topology: use `$graph-design`.
- Execute or resume a graph: use `$graph-run`.
- Read current state or lineage: use `$graph-inspect`.
- Change topology: use `$graph-rewrite`.
- Diagnose corruption, deadlock, or failure: use `$graph-debug`.
- Judge the final outcome: use `$graph-verify`.

Explain the boundary when relevant: local loops correct work inside one node, while Operating Graph coordinates and reorganizes work across nodes. Operating Graph owns topology and scheduling even when a node uses LoopKit.

Treat routing and explanation as read-only. Do not initialize a run, mutate topology, or perform an external action unless the user requests the corresponding workflow. Never infer approval for material external actions.

Use `python3 scripts/graphctl.py validate <graph.json>` before handing any graph to execution.

Read [graph-contract.md](../../references/graph-contract.md) when graph semantics or authority boundaries matter.
