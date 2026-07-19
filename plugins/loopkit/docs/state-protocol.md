# LoopKit state protocol

## Storage

Resolve the host home first (`~/.claude` on Claude Code / Cowork, `${CODEX_HOME:-~/.codex}` on Codex). The runtime detects Claude hosts via the `CLAUDECODE` environment variable, which both Claude Code and Cowork shells set; `LOOPKIT_STATE_ROOT` overrides detection entirely. The state root is `<host-home>/loopkit/`, and a run lives at:

```text
runs/<workspace-hash>/<timestamp>-<slug>/
  contract.json
  state.json
  events.jsonl
  checkpoint.md
  evidence/
  BLOCKED.md        optional
  schedule.json     optional
```

The workspace hash is the first 12 hexadecimal characters of SHA-256 over the resolved workspace path. Timestamps use UTC in `YYYYMMDDTHHMMSSZ` form.

Runs created before the dual-host port live under the Codex root (`~/.codex/loopkit/runs/`). They are not migrated. They can still be resumed by naming that run directory explicitly.

## State machine

The normal path is `draft -> ready -> running -> completed`. A running or scheduled run may enter `waiting_input`, `blocked`, `exhausted`, `failed`, or `cancelled`. `waiting_input`, `blocked`, and `scheduled` may return to `running` after their prerequisites are satisfied.

Every write is atomic. Every state transition requires the caller's expected generation number. A mismatched generation fails rather than overwriting newer state. A per-run lock prevents concurrent writers.

## Receipts

Each iteration receipt records the run id, iteration, status, action, evidence paths, checks, outcome, and next action. Completion receipts must contain at least one passing check and every referenced evidence path must exist.

## Hook behavior

`PreCompact` refreshes `checkpoint.md` for the current workspace's newest active run. `SessionStart` on `resume` or `compact` injects that checkpoint as developer context. Hooks do nothing when no active run exists, do not read transcripts, do not access the network, and never print more than 4096 bytes.
