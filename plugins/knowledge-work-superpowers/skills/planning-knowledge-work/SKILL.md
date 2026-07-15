---
name: planning-knowledge-work
description: Use when an approved brief needs a concrete research, analysis, writing, or delivery plan with evidence and verification steps.
---

# Planning Knowledge Work

## Purpose

Convert a clear brief into an executable plan. Each task should create a reviewable result and state how completion will be proved.

## Preconditions

Confirm that the plan has:

- A defined outcome.
- A known audience or user.
- Clear scope.
- Named sources of truth.
- Binding constraints.
- Observable success criteria.

If these are missing, load `knowledge-work-superpowers:framing-knowledge-work` first.

## Plan Design

### 1. Map The Artifacts

List the artifacts to create or update, such as:

- Work brief.
- Research plan.
- Source ledger.
- Claim ledger.
- Analysis notes.
- Draft.
- Review.
- Final deliverable.
- Delivery note.

Follow the user's harness and output-path rules.

### 2. Define The Evidence Standard

State what support different claims require. Consider:

- Whether primary sources are required.
- Whether current facts need live verification.
- Whether important claims need independent confirmation.
- How internal and public sources will be combined.
- How disputed or missing evidence will be labeled.

### 3. Split Into Deliverable Units

Each task should have one clear purpose and produce a result that can be checked independently. Keep tightly coupled actions together. Split only where a reviewer could accept one result and reject another.

### 4. Write Each Task Completely

For every task, include:

- Inputs.
- Specific actions.
- Output.
- Dependencies.
- Evidence requirement.
- Verification method.
- Stop or escalation condition.

Avoid placeholders such as "research as needed," "add sources," or "improve the draft." State what the worker must examine and what result must exist.

### 5. Mark Approval Boundaries

Identify decisions that require the user, such as a major scope change, publication, external communication, or choosing between materially different recommendations.

Do not ask for approval between ordinary steps that the user already authorized.

### 6. Set The Final Gate

The last plan stage must include:

- Brief coverage review.
- Source and claim audit.
- Citation and link check.
- Current-fact refresh.
- Format and output-path check.
- Delivery-note preparation.

## Output

Use `../../assets/knowledge-work-plan-template.md` for file-based plans. Adapt headings when the user's template is authoritative.

## Self-Review

Before execution:

1. Match every brief requirement to at least one task.
2. Scan for placeholders and vague verbs.
3. Check dependencies and task order.
4. Confirm every task has a verification surface.
5. Confirm no task silently adds scope.

Fix problems in the plan before executing it.

## Handoff

When the plan is ready, load `knowledge-work-superpowers:executing-knowledge-work-plans`. If several research strands are independent and multi-agent work is permitted, it may route to `knowledge-work-superpowers:dispatching-parallel-research`.
