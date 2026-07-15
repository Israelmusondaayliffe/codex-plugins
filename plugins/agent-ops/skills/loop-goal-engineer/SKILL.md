---
name: loop-goal-engineer
description: Explicit-only compatibility shim for the historical Loop Goal Engineer name. Use only when the user explicitly says loop-goal-engineer or Loop Goal Engineer. Redirect Codex loop design, scheduling, and diagnosis to LoopKit. Generic loop, Goal, recurring-task, and schedule requests should trigger LoopKit directly.
metadata:
  author: Israel Ayliffe
  version: 1.3.0-compat
---

# Loop Goal Engineer compatibility shim

This historical name remains available through Agent Ops 0.2.x. LoopKit now owns generic Codex Goal and loop contracts.

Route the explicit request as follows:

- Design a Goal or loop contract: `loopkit:loop-designer`.
- Prepare a recurring Codex task: `loopkit:loop-scheduler`.
- Diagnose a stalled or unsafe loop: `loopkit:loop-doctor`.
- Multi-stage or ambiguous work: `loopkit:loopkit`.

Target Codex Goals and scheduled tasks. Do not emit external agent CLI commands, shell loop runners, or a second state protocol. Use the LoopKit contract validator before initialization.

This shim is scheduled for removal in Agent Ops 0.3.0 after LoopKit reaches 0.2.0.
