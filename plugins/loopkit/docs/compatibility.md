# Agent Ops compatibility window

LoopKit owns generic goal and loop design (Codex Goals or Claude Code `/goal`), execution, verification, resume, scheduling, and diagnosis on Claude Code, Claude Cowork, and Codex.

Agent Ops 0.2.x continues to own reusable agent design, agent-system routing, and agent-system audit. Its `goal-runner`, `loop-goal-engineer`, and `loopy` skills remain available as explicit-only compatibility shims. Each shim redirects generic host-platform work to the matching LoopKit skill while retaining its historical name for one release line.

The shims are scheduled for removal in Agent Ops 0.4.0. Until then, fresh generic requests should route to LoopKit, while an explicit request for a legacy skill may still load the shim.
