# Ownership and state

## Ownership

- LoopKit owns generic Codex loop and Goal contracts, execution, receipts, resume, scheduling, and runtime diagnosis.
- Agent Ops owns reusable agent design, agent-system routing, and agent-system audit.
- Outcome Engine owns general idea-to-result shaping when no feedback loop is needed.
- ProofLoop remains explicit-only.

## State lookup

Resolve the state root in this order:

1. `LOOPKIT_STATE_ROOT` for tests or an explicit isolated run.
2. `$CODEX_HOME/loopkit` when `CODEX_HOME` is set.
3. `~/.codex/loopkit` otherwise.

Each workspace uses a 12-character hash of its resolved path. Every run contains a contract, current state, append-only events, compact checkpoint, and evidence directory.

## Authority

LoopKit records authority but does not create it. Scheduled tasks, external messages, destructive actions, privacy-sensitive access, purchases, and production changes remain separately approval-gated.
