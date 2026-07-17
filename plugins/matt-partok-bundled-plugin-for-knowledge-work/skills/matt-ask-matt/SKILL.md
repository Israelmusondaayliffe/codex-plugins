---
name: matt-ask-matt
description: Route an explicitly requested Matt workflow across coding and knowledge work. Use when the user says ask Matt, use the Matt Partok bundle, follow Matt Pocock's flow, choose a Matt skill, or take work from idea to verified result with the bundled system.
---

# Ask Matt

Route to the smallest useful Matt-prefixed skill. Keep this router explicit so ordinary research, planning, and review remain owned by the user's existing plugins.

## Main flow

1. Start with `matt-grill-with-docs` when the work has a durable workspace, or `matt-grill-me` for a conversational decision with no files.
2. Use `matt-research` when a fact requires primary-source investigation. Use `matt-prototype` when an open question needs a concrete artifact or runnable test.
3. Branch on size after material decisions are resolved:
   - One bounded session with an agreed acceptance surface: go directly to `matt-implement`. Do not create a spec or tickets as ceremony.
   - Multiple sessions or a durable contract is needed: use `matt-to-spec`, then `matt-to-tickets` when there is more than one execution slice.
4. Use `matt-handoff` before changing threads or delegating a slice.
5. Use `matt-implement` for one approved slice.
6. Close coding work with `matt-code-review`. Close non-code work with the user's evidence and delivery review owner.

Keep clarification, specification, and slicing in one context when the durable branch is needed. Start each execution slice with fresh context and a durable brief.

## On-ramps

- Large, foggy effort: `matt-wayfinder`, then rejoin at `matt-to-spec`.
- Incoming queue or raw request: `matt-triage`.
- Software bug or performance regression: `matt-diagnosing-bugs`.
- Codebase health: `matt-improve-codebase-architecture`.
- Shared terminology or durable decisions: `matt-domain-modeling`.
- Learning program: `matt-teach`.
- Writing exploration: `matt-writing-fragments`, then `matt-writing-beats` or `matt-writing-shape`.
- Questions another person must answer: `matt-to-questionnaire`.

## Coding track

Use `matt-tdd`, `matt-codebase-design`, `matt-code-review`, and `matt-resolving-merge-conflicts` only for software work. Use `matt-prototype` in logic or UI mode when prose cannot settle a design choice.

## Knowledge-work track

Treat a complete slice as one observable result, not one document section or one research activity. Preserve source and claim evidence, review the deliverable against both its brief and its evidence, and verify the final artifact on its real surface.

## Handoff gates

- Do not turn unresolved consequential decisions into hidden assumptions.
- Do not execute from an unapproved spec or an invalid slice.
- Do not publish, send, assign, commit, purchase, delete, or change external state unless the task authorizes it.
- Do not call work complete without fresh evidence against the original brief.

## Setup

Use `matt-setup-matt-pocock-skills` when a project lacks a work tracker, durable context location, or output convention. Prefer local files until the user authorizes external tracker changes.
