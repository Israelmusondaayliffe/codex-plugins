---
name: harness-verifier
description: Verify a generated or upgraded Codex harness against its approved profile, operations plan, current files, live capability state, and fresh discovery evidence. Use when a user asks whether the harness is complete, installed, global, visible, safe, restart-ready, or actually operational rather than merely present on disk.
---

# Harness Verifier

Verify without repairing during the verification pass.

## Workflow

1. Read the profile and plan without relying on the builder's summary.
2. Inspect current files, hashes, manifests, permissions, and backup evidence.
3. Run every safe deterministic check exactly as approved.
4. Verify skills and plugins with their official validators.
5. Prove installed listing, source-cache parity, and fresh-task discovery.
6. Test connectors, Browser, Computer Use, rules, or hooks only when the plan requires them.
7. Evaluate each judgment criterion with file, line, command, or live-surface evidence.
8. Emit a receipt with one result per required check.

Use `../../references/verification-standard.md`. Missing, skipped, stale, stubbed, or renamed checks fail verification.
