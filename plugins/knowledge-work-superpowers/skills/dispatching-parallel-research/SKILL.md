---
name: dispatching-parallel-research
description: Use when permitted multi-agent research has two or more independent question domains that can run concurrently without shared writes.
---

# Dispatching Parallel Research

## Purpose

Use parallel agents to shorten independent research work without creating duplicated searches, inconsistent evidence standards, or conflicting edits.

## Permission Gate

Use this skill only when:

- Multi-agent tools are available.
- User, developer, project, and platform instructions permit delegation.
- At least two research strands are independent.
- Agents do not need to edit the same files or shared state concurrently.

If any condition fails, execute the work sequentially.

## Independence Test

Research strands are independent when each can be understood and completed from its own brief and sources, and one strand's result does not determine how another must research.

Good split:

- Current market size.
- Competitor offerings.
- Relevant regulation.

Poor split:

- Find sources.
- Interpret those same sources.
- Draft from those same interpretations.

The poor split is sequential because later work depends on earlier results.

## Workflow

### 1. Define Shared Standards

Before dispatching, provide every agent with:

- Overall decision or outcome.
- Its exact research question.
- Scope and exclusions.
- Source hierarchy.
- Freshness requirement.
- Required source and claim ledger fields.
- Citation rules.
- Output location or report contract.
- Stop conditions.

### 2. Create Focused Strands

Give each agent one problem domain. Remove overlap explicitly. State what the agent must return and what it must not do.

### 3. Dispatch Concurrently

Dispatch only strands that can run without shared writes. Use separate artifact paths or return reports to the coordinator.

### 4. Review Each Return

For every strand:

- Check that the question was answered.
- Inspect source quality and freshness.
- Confirm claims link to sources.
- Note contradictions, missing evidence, and uncertainty.
- Reject outputs that rely on search snippets or unsupported summaries.

### 5. Integrate

The coordinator owns synthesis. Merge source and claim ledgers, resolve duplicate source IDs, compare definitions and date ranges, and surface cross-strand conflicts.

Do not ask a synthesis agent to hide contradictions for the sake of a clean narrative.

### 6. Verify The Combined Result

Run the same evidence and brief checks that would apply to single-agent work. Parallel execution changes speed, not the quality standard.

## Agent Brief Shape

```text
Research question:
Why it matters:
Scope:
Excluded:
Source hierarchy:
Freshness rule:
Required artifacts:
Verification:
Stop conditions:
Return format:
```

## Common Failures

- Splitting by activity instead of independent question.
- Giving every agent the whole research problem.
- Allowing concurrent edits to one ledger.
- Combining repeated claims as if they were independent support.
- Trusting agent summaries without checking the evidence.
