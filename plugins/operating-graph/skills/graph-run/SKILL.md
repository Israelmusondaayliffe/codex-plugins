---
name: graph-run
description: Initialize, execute, resume, and coordinate a validated operating graph with deterministic scheduling, bounded concurrency, node packets, artifact registration, policy-gated rewrites, and terminal verification. Use when the user asks to run or continue an operating graph.
---

# Graph Run

This workflow mutates runtime state. The controller is the sole writer of runtime records. Workers may write only within their assigned node-run and artifact directories.

1. Validate with `python3 scripts/graphctl.py validate <graph.json>`.
2. Initialize with `python3 scripts/graphctl.py init <graph.json> --run-root <directory>`.
3. Detect worker capacity, reserving one fixed slot for the controller. Use inline execution if subagents are unavailable.
4. List deterministic work with `python3 scripts/graphctl.py ready <run-directory>`.
5. Generate an immutable node packet from [node-packet.md](../../references/node-packet.md), dispatch the node, validate its result, and register owned artifacts with `python3 scripts/graphctl.py register-artifact <run-directory> <node-id> <artifact-type> <path>`.
6. Record controller-owned transitions with `python3 scripts/graphctl.py transition <run-directory> <node-id> <status>` and signals with `python3 scripts/graphctl.py signal <run-directory> <name> <value>`.
7. Evaluate rewrite triggers only after the events defined in [rewrite-policy.md](../../references/rewrite-policy.md). Use `$graph-rewrite` for proposals and applications.
8. Continue until completion, escalation, cancellation, or a hard limit. Before resuming, run `python3 scripts/graphctl.py resume-check <run-directory>`.
9. Finish with `python3 scripts/graphctl.py verify <run-directory>` and report graph versions, artifacts, evidence, unresolved issues, and the exact verdict.

Stop automatic execution on event-chain corruption. Do not synthesize approvals, exceed budgets, or let workers edit controller-owned files.

Read [runtime-protocol.md](../../references/runtime-protocol.md) before execution.
