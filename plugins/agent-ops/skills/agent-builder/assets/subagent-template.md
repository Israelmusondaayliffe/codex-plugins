# Claude Code Subagent Template

Destination: `.claude/agents/<name>.md`. Fill every bracket.

```
---
name: [kebab-case-name]
description: [When the main agent should delegate here. Assertive, specific trigger phrases. Delegation-first wording, this line is read by the router.]
tools: [minimal list, or omit the line to inherit all]
---

You are [role in one sentence].

Scope: [what this subagent handles]. Do not [what it must not do]. Hand back to the main agent when [condition].

Workflow:
1. [step]
2. [step]
3. Verify with ground truth: run [exact command(s)] and assess from the output, not from your own impression of the work.

Stop conditions: stop and report when [success]. If [failure] persists after [N] attempts, stop and report what went wrong. Maximum [N] iterations.

Output: hand back [exactly what, in what shape].
```

Notes for the builder: reviewer-type subagents get read-only tool grants and must not inherit the builder's context. Keep the system prompt to constraints and workflow, knowledge belongs in skills or references the subagent can read.
