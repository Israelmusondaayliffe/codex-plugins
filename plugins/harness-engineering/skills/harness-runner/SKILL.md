---
name: harness-runner
description: Execute an approved Harness Engineering plan as a bounded Goal with durable state, iteration receipts, approval stops, resume behavior, and a verifier handoff. Use when a user says run the harness build, keep going until verified, use a Goal, resume the build, or carry an approved multi-stage harness implementation to a named terminal state.
---

# Harness Runner

Use Codex Goal mode for the visible outcome. Use LoopKit when installed for contract, state, receipts, resume, and terminal-state validation.

## Workflow

1. Require the approved profile, audit, plan, allowed paths, caps, and stop rules.
2. Create or validate durable state before changing files.
3. Observe fresh state and choose one bounded action.
4. Apply only an approved operation group.
5. Run current checks and record a receipt.
6. Continue only while progress is measurable and caps remain.
7. Stop as waiting input, blocked, exhausted, failed, cancelled, or completed. Do not rename a failure as success.
8. Send completion candidates to `harness-verifier`.

The Goal never grants broader filesystem, authentication, publication, or external-action authority.
