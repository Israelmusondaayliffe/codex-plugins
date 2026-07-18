# Runtime Protocol

## Storage and ownership

Each run contains `graph.json`, `policies.json`, `state.json`, `events.jsonl`, `artifacts.jsonl`, `approvals.jsonl`, rewrite proposals and applications, immutable graph versions, node-run attempts, and node-owned artifacts.

The controller is the sole writer of state, events, artifact registry records, approvals, graph versions, and rewrite records. Workers write only inside their assigned `node-runs/<node-id>/attempt-<number>/` and `artifacts/<node-id>/` directories. Write structured runtime files through temporary files and atomic replacement.

## Integrity

Every runtime state change emits a canonical JSON event with a sequence number, previous hash, and SHA-256 event hash. Inspection, replay, resume, debugging, and verification validate the full chain. Stop automatic execution on any break.

Artifacts must remain inside the run directory, exist, match their registered hash, and belong to the declaring node. Failed, invalidated, superseded, missing, corrupt, or wrongly owned artifacts cannot activate or complete downstream work.

## Scheduling

A ready node is enabled, dependency-complete, approval-complete, within node and run budgets, and valid for the current epoch. Sort by higher priority, critical before optional, more downstream required nodes released, then lexical node ID. Runtime concurrency is the lower of the graph limit and available worker slots, reserving a controller slot in fixed pools.

## State transitions

Allowed transitions are `pending` to `ready`, `blocked`, `skipped`, or `cancelled`; `ready` to `running`, `blocked`, or `cancelled`; `running` to `succeeded`, `failed`, or `blocked`; `failed` to retryable `ready`; and `blocked` to `ready` or `cancelled`.

A retry requires remaining attempts, valid inputs, a recorded retry event, and no pending approval. Never silently rerun a succeeded node.

Use `status`, `ready`, `transition`, `register-artifact`, `signal`, `replay`, `resume-check`, `inspect`, and `verify` through `python3 scripts/graphctl.py`.
