---
name: framing-knowledge-work
description: Use when substantial research or writing lacks a clear outcome, audience, scope, source of truth, constraints, or success criteria.
---

# Framing Knowledge Work

## Purpose

Turn a rough request into a clear work brief. The brief prevents a polished answer to the wrong question.

## Gate

For substantial or high-stakes work, do not begin deep research or drafting until the work is framed.

Do not add a needless pause when the user already supplied the outcome, audience, scope, sources, constraints, and success criteria. Summarize the frame and proceed unless two viable directions would produce meaningfully different results.

## Workflow

### 1. Inspect Available Context

Read the closest project rules, registry, brief files, templates, and source locations before asking questions. Resolve discoverable facts through files or connectors.

### 2. Define The Outcome

State what must exist when the task is finished. Use an observable result, not an activity.

Weak: "Research employee curiosity."

Strong: "Produce a cited decision brief comparing three employee-curiosity program models and recommend one pilot."

### 3. Define The Intended User

Record:

- Who will read or use the result.
- What they already know.
- What decision or action should follow.
- What level of detail they can use.

### 4. Define Questions And Scope

List the questions the work must answer. Separate included and excluded areas so research does not grow without control.

If the request contains several independent deliverables, split them into separate workstreams and frame the first one fully.

### 5. Identify Sources Of Truth

Name the files, connectors, datasets, official sources, or people that own the facts. Mark missing or inaccessible sources.

### 6. Record Constraints

Capture binding requirements such as:

- Deadline or freshness window.
- Output format and length.
- Confidentiality or permissions.
- Required or forbidden sources.
- Voice, brand, or template rules.
- Actions that require approval.

### 7. Define Success Criteria

Use checks that can be verified at the end. Examples:

- Every key factual claim has direct support.
- The recommendation answers the named decision.
- Conflicting evidence is surfaced.
- The requested file and format exist in the approved location.

### 8. Resolve Open Decisions

Ask one focused question only when a preference cannot be discovered or safely inferred and the answer changes the result. Otherwise, state the assumption and proceed.

## Output

For file-based work, use `../../assets/work-brief-template.md` and save the brief in the user-approved location.

For chat-only work, present a compact frame:

```text
Outcome:
Audience:
Questions:
Scope:
Sources of truth:
Constraints:
Success criteria:
Assumptions:
```

## Approval Rule

Request approval when the frame introduces a meaningful interpretation, tradeoff, or scope choice. If the user's request already authorizes a clear execution path, record the frame and continue.

After approval or clear authorization, load `knowledge-work-superpowers:planning-knowledge-work` for multi-step work.

## Review

Before handoff, check the brief for:

- Missing audience or decision.
- Questions that cannot be answered by the named sources.
- Contradictory constraints.
- Vague success criteria.
- Hidden scope expansion.
