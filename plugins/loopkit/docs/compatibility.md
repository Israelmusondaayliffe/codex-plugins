# Agent Ops compatibility window

LoopKit 0.1.x owns generic Codex Goal and loop design, execution, verification, resume, scheduling, and diagnosis.

Agent Ops 0.2.x continues to own reusable agent design, agent-system routing, and agent-system audit. Its `goal-runner`, `loop-goal-engineer`, and `loopy` skills remain available as explicit-only compatibility shims. Each shim redirects generic Codex work to the matching LoopKit skill while retaining its historical name for one release line.

The shims are scheduled for removal only when LoopKit reaches 0.2.0 and Agent Ops reaches 0.3.0. Until then, fresh generic requests should route to LoopKit, while an explicit request for a legacy skill may still load the shim.
