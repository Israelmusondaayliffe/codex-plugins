# LoopKit

LoopKit is a Codex-native plugin for bounded, resumable work. It separates a loop contract from execution, verification, persistence, scheduling, and diagnosis so each failure has a clear owner.

## What it includes

- `loopkit`: front door and route selector
- `loop-designer`: contract design and validation
- `loop-runner`: bounded execution with receipts
- `loop-verifier`: independent and deterministic completion checks
- `loop-resumer`: checkpoint restoration after interruption or compaction
- `loop-scheduler`: scheduled-task preparation and first-run checks
- `loop-doctor`: diagnosis for repetition, drift, weak verification, and unsafe authority

State is stored under `${CODEX_HOME:-~/.codex}/loopkit/`. LoopKit does not depend on external agent CLIs, MCP servers, or network access.

## Install

Add the marketplace, then install the plugin:

```bash
codex plugin marketplace add Israelmusondaayliffe/codex-plugins
codex plugin add loopkit@israel-codex-plugins
```

Review and trust the plugin hooks in `/hooks`. The hooks only refresh or restore a compact checkpoint for an active run in the current workspace.

## Validate

```bash
python3 scripts/verify_bundle.py
python3 -m unittest discover -s tests -v
```

## Safety boundary

Creating or running a loop does not expand Codex permissions. Schedules, external messages, destructive actions, production changes, purchases, and privacy-sensitive access still require the authority and approvals of the active task.
