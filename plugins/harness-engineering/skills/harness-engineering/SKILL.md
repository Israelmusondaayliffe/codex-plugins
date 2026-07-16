---
name: harness-engineering
description: Design, build, verify, or maintain a personalized Codex harness from a vague brief or an existing setup. Use when a user asks for a Codex operating system, harness, AGENTS.md chain, workspace architecture, capability stack, guided setup, harness upgrade, or an end-to-end workflow that combines interview, audit, planning, reversible implementation, and verification. Route focused requests to the owned skill that matches the current phase.
---

# Harness Engineering

Build the smallest harness that satisfies the user's real work. Treat the user's existing files and live Codex environment as implementation truth.

## Route

1. Vague or incomplete brief: load `harness-interview`.
2. Existing setup or upgrade request: load `harness-audit` before planning.
3. Confirmed profile plus audit: load `harness-planner`.
4. `AGENTS.md` work only: load `agents-md-engineer`.
5. Approved file operations: load `harness-builder`.
6. Missing reusable skill: load `skill-engineer`.
7. Missing distributable bundle: load `plugin-engineer`.
8. Model-specific prompt work: load `model-prompt-engineer`.
9. Sustained approved build: load `harness-runner`.
10. Completion claim: load `harness-verifier`.
11. Drift or update work: load `harness-maintainer`.

For an end-to-end request, use this order: interview, audit, plan, approve, run, verify, hand off.

## Contract

- Investigate before asking factual questions.
- Keep audit and planning read-only.
- Present the complete plan and operation groups before changing files.
- Back up every existing file before an approved update.
- Do not install third-party code, trust hooks, authenticate accounts, or publish externally without separate approval.
- Require fresh evidence before completion.

Read `../../references/harness-architecture.md` for scope placement and `../../references/safety-and-approvals.md` before any mutation.
