---
name: matt-handoff
description: Create a durable, redacted Matt-flow handoff so a fresh Codex thread or delegated agent can resume one bounded slice. Use when the user says handoff, switch threads, preserve context, delegate this slice, or continue the Matt workflow in a fresh context.
---

# Matt Handoff

Write the handoff to the user-approved durable workstream location. Use the closest project output convention. Do not use a volatile temporary directory when the handoff must survive across tasks.

Reference existing specs, decisions, tickets, diffs, and evidence by path or URL instead of duplicating them.

Include:

- next objective and active slice
- exact first action for the receiver
- canonical artifact paths or URLs
- decisions and assumptions not recorded elsewhere
- blockers, approval boundaries, and forbidden actions
- current code or knowledge state
- commands or checks already run, with results
- latest proof and remaining untested risks
- suggested Matt-prefixed skills for the next phase

Redact secrets, credentials, private personal data, and irrelevant sensitive details. Re-read live state at resume time because a handoff is context, not proof that the world is unchanged.
