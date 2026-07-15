---
name: verification-before-delivery
description: Use when substantial knowledge work is about to be called complete, accurate, ready, or verified and needs fresh evidence checks.
---

# Verification Before Delivery

## Purpose

Require evidence for completion claims. A polished artifact and a previous review are not fresh verification.

## Core Rule

Do not say the work is complete, accurate, ready, or verified until the relevant checks have just been run and their results inspected.

## Gate

Before any completion statement:

1. Identify what would prove the claim.
2. Run the complete fresh check.
3. Read the result.
4. Compare it with the brief.
5. Fix failures or report the actual status.
6. State completion only when the evidence supports it.

## Verification Checklist

### Brief

- Every required question is answered.
- Scope and exclusions are respected.
- Intended audience and decision are served.
- Required format, length, and template are followed.

### Evidence

- Every key factual claim has support.
- Citations open and support the nearby claim.
- Quotations and numbers match their sources.
- Primary sources are used where required and available.
- Counterevidence and source conflicts are represented.

### Analysis

- Fact, inference, dispute, and recommendation are distinguished.
- Assumptions are visible.
- Recommendations follow from the evidence and decision.
- Unresolved claims are narrowed, labeled, or removed.

### Freshness

- Time-sensitive facts were checked live.
- Publication and update dates were inspected.
- Memory or prior notes were not treated as confirmed current state.

### Calculations And Data

- Calculations were rerun with an appropriate deterministic tool.
- Units, denominators, date ranges, and populations match.
- Tables and charts agree with the underlying data.

### Safety And Permissions

- Confidential or personal information is handled within scope.
- No external message, publication, or destructive action occurred without authority.
- Domain-specific review was used when the task requires it.

### Artifact

- The file exists in the correct output location.
- The filename and version follow the applicable rules.
- The file opens, renders, or parses correctly.
- No placeholders remain.
- The evidence package is present when required.

## File-Based Check

For a standard research bundle, run:

```bash
python3 ../../scripts/verify_research_bundle.py /path/to/bundle --profile deliverable
```

This structural check does not replace opening sources and inspecting claim support.

## Failed Verification

If any required check fails:

- Do not claim completion.
- State the failing check and evidence.
- Fix it when the fix is within scope.
- Re-run the complete affected check.
- Record any unresolved limitation.

## Completion Statement

State what was verified and name the evidence briefly. Avoid claims broader than the checks that ran.

After verification passes, load `knowledge-work-superpowers:finishing-a-deliverable`.
