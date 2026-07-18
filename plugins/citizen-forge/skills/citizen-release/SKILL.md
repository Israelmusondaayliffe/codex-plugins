---
name: citizen-release
description: Run Citizen Forge's 35 controls and deterministic release decision. Use when a user asks whether an app is ready, requests a release, wants failed controls explained, or needs a governed transition from release candidate to running.
---

# Citizen Release

Read references/guardrails.md. Run fresh checks and change classification. Do not reuse stale results.

Only the release module decides readiness. FAIL, BLOCKED, or UNAVAILABLE required controls block release. Consequential changes also require the policy-defined human approval evidence. Explain each block, its impact, repair, and whether AI or a human owns the next decision.

Never rename, skip, delete, or stub a required check as a repair.
