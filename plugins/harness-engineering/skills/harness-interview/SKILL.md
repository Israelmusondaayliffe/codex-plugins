---
name: harness-interview
description: Conduct a persistent, source-first interview that converts a user's incomplete Codex setup idea into a confirmed harness profile. Use when the user says grill me, interview me, design my harness, set up Codex for me, ask what I need, or gives a thin brief whose answers could change global instructions, workspace structure, permissions, skills, plugins, connectors, verification, or maintenance.
---

# Harness Interview

Treat the interview and confirmed profile as the deliverable. Do not build during this phase.

## Workflow

1. Inspect authorized existing files and capability state before asking discoverable facts.
2. Establish the root outcome, users, work types, constraints, and largest unresolved dependency.
3. Follow the decision tree in `../../references/interview-tree.md` one branch at a time.
4. Ask one to three linked questions. Explain a tradeoff only when it changes the answer.
5. Record each answer as fact, constraint, preference, assumption, or decision.
6. Pressure-test authority, failure modes, maintenance, portability, and proof.
7. Present the complete working model and request correction.
8. Save a schema-versioned profile only after confirmation.

## Profile requirements

Include user context, intended scope, workspace choice, project pattern, data sources, capability needs, authority boundaries, verification expectations, maintenance ownership, exclusions, accepted assumptions, and deferred decisions.

Validate saved profiles with `python3 ../../scripts/harnessctl.py validate-profile PROFILE.json`.
