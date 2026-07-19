---
name: harness-verifier
description: Verify a generated or upgraded harness against its approved profile, operations plan, current files, live capability state, and fresh discovery evidence, on Claude Code, Claude Cowork, or Codex. Use when a user asks whether the harness is complete, installed, global, visible, safe, restart-ready, or actually operational rather than merely present on disk.
---

# Harness Verifier

Verify without repairing during the verification pass. Use the platform file to know which proof surfaces exist; never mark a check passed on a surface the platform does not have.

## Workflow

1. Read the profile and plan without relying on the builder's summary.
2. Inspect current files, hashes, manifests, permissions, and backup evidence.
3. Run every safe deterministic check exactly as approved.
4. Verify skills and plugins with the platform's validator: `claude plugin validate` and `claude doctor` on Claude Code, structural checks plus the live plugin list on Cowork, the official skill validators and `codex plugin list` on Codex.
5. Prove installed listing, source-cache parity where a cache exists, and fresh-task discovery.
6. On Cowork, additionally prove that changed files were committed to the connected folder on the user's device, not only staged in the sandbox.
7. Test connectors, hooks, rules, or optional capability bundles only when the plan requires them.
8. Evaluate each judgment criterion with file, line, command, or live-surface evidence.
9. Emit a receipt with one result per required check.

Use `../../references/verification-standard.md`. Missing, skipped, stale, stubbed, or renamed checks fail verification.
