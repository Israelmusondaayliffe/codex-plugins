---
name: harness-runner
description: Execute an approved Harness Engineering plan as a bounded autonomous run with durable state, iteration receipts, approval stops, resume behavior, and a verifier handoff, on Claude Code, Claude Cowork, or Codex. Use when a user says run the harness build, keep going until verified, resume the build, or carry an approved multi-stage harness implementation to a named terminal state.
---

# Harness Runner

Map the loop onto the platform's autonomy surface: Codex Goal mode on Codex, a long-running or headless session on Claude Code, an in-session driven loop (optionally continued by scheduled tasks) on Cowork. Use an installed loop or goal framework (for example LoopKit or a goal-runner skill) when present for contract, state, receipts, resume, and terminal-state validation.

## Workflow

1. Require the approved profile, audit, plan, allowed paths, caps, and stop rules.
2. Create or validate durable state before changing files. On Cowork, durable state lives in a connected folder so a later session can resume it; sandbox-only state does not survive.
3. Observe fresh state and choose one bounded action.
4. Apply only an approved operation group.
5. Run current checks and record a receipt.
6. Continue only while progress is measurable and caps remain.
7. Stop as waiting input, blocked, exhausted, failed, cancelled, or completed. Do not rename a failure as success.
8. Send completion candidates to `harness-verifier`.

The run never grants broader filesystem, authentication, publication, or external-action authority.
