---
name: using-knowledge-work-superpowers
description: Use when substantial non-coding work needs research, analysis, planning, writing, review, or evidence-backed delivery. Skip for simple lookups.
---

# Using Knowledge Work Superpowers

## Purpose

Route substantial knowledge work through the smallest set of skills that protects quality. Do not force the full workflow onto a simple lookup, translation, formatting request, or short conversational answer.

## First Decision

Classify the request before acting.

Use the full or partial workflow when one or more of these apply:

- The work has several steps or sources.
- The output will guide a decision.
- The user wants deep research, an evidence-backed result, or a reusable artifact.
- Current or disputed facts matter.
- Errors would be costly or embarrassing.
- The task will produce a report, memo, brief, comparison, recommendation, or research package.

Use a fast path when the task is one direct lookup, one simple transformation, or a low-stakes answer that does not need an evidence trail.

## Skill Router

Load the relevant skill before taking its action:

- Unclear outcome, audience, scope, or success criteria: `knowledge-work-superpowers:framing-knowledge-work`
- Approved brief or clear multi-step requirements: `knowledge-work-superpowers:planning-knowledge-work`
- Deep, current, disputed, or multi-source research: `knowledge-work-superpowers:systematic-research`
- Important claims or recommendations need support: `knowledge-work-superpowers:evidence-first-analysis`
- A sourced draft must be written: `knowledge-work-superpowers:drafting-from-evidence`
- A written plan must be carried out: `knowledge-work-superpowers:executing-knowledge-work-plans`
- Independent research strands and permitted multi-agent work: `knowledge-work-superpowers:dispatching-parallel-research`
- A draft or deliverable needs quality review: `knowledge-work-superpowers:reviewing-knowledge-work`
- Feedback has arrived: `knowledge-work-superpowers:receiving-work-review`
- A completion or readiness claim is near: `knowledge-work-superpowers:verification-before-delivery`
- Verified work needs packaging and handoff: `knowledge-work-superpowers:finishing-a-deliverable`

## Default Sequence

For a new substantial task:

1. Frame the work.
2. Plan the work.
3. Research and build the evidence record.
4. Analyze claims.
5. Draft from evidence.
6. Review the result.
7. Verify with fresh checks.
8. Finish and hand off.

Skip a phase only when its output already exists or the task does not need it. State the reason briefly.

## Source Ownership

Use the source closest to the fact:

- Internal notes and wiki content: the owning internal connector.
- Working documents, sheets, and slides: their storage connector.
- Email facts: the email connector.
- Schedule facts: the calendar connector.
- Public current facts: live web research.
- Platform behavior: official documentation or the live product.

Do not substitute public search for an available internal source of truth.

## State And Recovery

For long work, preserve progress in files rather than relying on chat history. Keep the brief, plan, source ledger, claim ledger, review, and delivery note beside the deliverable or in the user-approved output location.

After compaction or a resumed task, inspect those artifacts before repeating work.

## Non-Negotiable Rules

- Do not present inference as sourced fact.
- Do not cite a source that does not support the nearby claim.
- Do not claim completion without fresh verification.
- Do not expand scope silently.
- Do not use multi-agent work when user or platform instructions prohibit it.
