# Phase agent: Schedule

## Scope

Prepare a scheduled task on the host surface (Codex scheduled tasks, or Claude Code scheduled cloud routines via `/schedule`) for a loop that already passed a manual run. Do not emulate the scheduler with shell loops or cron.

## Inputs

Require a tested run, cadence, task prompt, no-op behavior, evidence return, and stop condition.

## Handoff

Load `loop-scheduler`. Record `schedule.json`, then use the current host scheduling surface (Codex desktop or web scheduled-task controls, or Claude Code `/schedule`) when available.

## Validation

Observe at least one scheduled execution before treating the schedule as ready.
