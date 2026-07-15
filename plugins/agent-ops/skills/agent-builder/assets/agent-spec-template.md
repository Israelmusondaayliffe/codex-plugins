# Agent Design Spec

Filled by ARCHITECT before any artifact is written. Every field, no blanks.

```
TASK: [what the user wants done, one sentence]

PATTERN: [single call / chaining / routing / parallelization / orchestrator-workers / evaluator-optimizer / autonomous agent]
REJECTED SIMPLER RUNG: [the rung below and the concrete reason it fails this task]
TRADE ACCEPTED: [what this costs in latency and dollars, what it buys]

TARGET: [Claude Code / Codex / both]

AUGMENTATIONS:
- Retrieval: [what, or none]
- Tools: [list, minimal grant]
- Memory: [what persists between steps or runs, or none]

GROUND TRUTH: [the exact commands or environmental checks that verify progress, e.g. pytest, npm run build, diff review]

SUCCESS CRITERIA: [checkable by a stranger without asking questions]

STOP CONDITIONS:
- Success: [condition]
- Failure: [after N attempts, report what went wrong]
- Blocked: [stop and report when no defensible path remains, plus what would clear the block]
- Cap: [max N iterations / $ budget]

ITERATION POLICY: [how the agent chooses the next action between attempts, e.g. expand axes if outputs cluster, tighten constraint if X appears, rerun check]

PAUSE POINTS: [where a human checks in, placed before steps that poison downstream work; map onto the harness four-phase workflow when one exists]

SCOPE: [what it may read, what it may write, what it must never touch. When a harness exists, write scope defaults to its output folder (CLAUDE-OUTPUTS/ or CODEX-OUTPUTS/YYYY-MM-DD/), versioned naming, announce the path when done]

HARNESS: [contract chain layers present (CLAUDE.md / AGENTS.md global, workspace, project), validators to invoke, rules the agent must NOT duplicate because the chain already loads them]
```
