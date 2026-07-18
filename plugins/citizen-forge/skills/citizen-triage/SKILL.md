---
name: citizen-triage
description: Classify a confirmed Citizen Forge app by application shape and four-part blast radius, then invoke deterministic policy for its route. Use for safety checks, suitability decisions, second-consumer graduation, sensitive-data changes, external exposure, uncertainty, or questions such as "is this safe?"
---

# Citizen Triage

Read references/risk-model.md. Gather any missing risk fact one at a time. AI may propose a shape and cite brief evidence, but only scripts/citizen_forge/policy.py decides the route.

Invoke the triage command. Present facts, AI recommendation, deterministic rule, confidence, policy version, final route, and required next action. Stop on unknown shape, low confidence, any score of three or four, external use, regulated data, or missing facts.
