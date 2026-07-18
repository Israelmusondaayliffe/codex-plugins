---
name: citizen-provision
description: Select and create a Citizen Forge project only from an approved versioned paved road. Use after deterministic triage approves a route, when a user asks to set up the project, or when production capabilities and adapter availability must be distinguished from local scaffolding.
---

# Citizen Provision

Read references/paved-roads.md and references/adapters.md. Require an approved decision and selected project root.

1. Generate a plan that separates files created, credentials, human authorization, unavailable capabilities, and local-only work.
2. Invoke deterministic provisioning inside the selected root.
3. Verify every created file.
4. Report missing adapters as UNAVAILABLE.

Never simulate SSO, cloud, production database, secrets, monitoring, backup, CI, or approval success. Elevated provisioning requires a verified adapter and an explicit approval event.
