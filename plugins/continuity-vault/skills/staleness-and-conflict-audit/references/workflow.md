# Staleness And Conflict Audit Workflow

Audit only a bounded source set. For each load-bearing claim:

1. Identify its source and last known verification date.
2. Check whether a closer `AGENTS.md`, project file, live connector, CLI, or official documentation now supersedes it.
3. Classify the issue as `stale-claim`, `instruction-conflict`, `authority-gap`, `missing-owner`, or `broken-reference`.
4. Set severity to `low`, `medium`, or `high` based on the consequence of reuse.
5. Recommend verification, owner review, source repair, or retirement. Do not perform mutation as part of the audit.

Use `clear` only when no actionable finding remains. Use `needs-review` for resolvable findings. Use `blocked` when a required authority source is absent or two controlling sources conflict without an owner decision.
