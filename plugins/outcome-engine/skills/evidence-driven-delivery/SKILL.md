---
name: evidence-driven-delivery
description: "Execute approved work one observable result at a time through a check-change-verify loop. Use when the user asks to implement a plan, complete an action slice, work test-first, prove each step, or finish a bounded result. Adapt proof to research, writing, creative work, operations, data, personal plans, or software."
---

# Evidence-Driven Delivery

Build from proof instead of confidence. Complete one bounded behavior or outcome per cycle.

## The loop

1. Check: define one observable acceptance check through the real user or audience interface.
2. Confirm unmet state: run the check or show that the required artifact or behavior is absent. A check that already passes does not prove the new work.
3. Change: make the smallest useful change that can satisfy this one check.
4. Verify: rerun the same check and read the full result.
5. Improve: simplify structure only after the check passes. Rerun it after every structural change.
6. Repeat with the next acceptance check.

Load `references/evidence-surfaces.md` before choosing proof for an unfamiliar domain or a high-stakes task.

## Rules

- Work one slice at a time. Do not create all checks first and all outputs second.
- Test observable results, not the internal steps used to produce them.
- Derive expected results from the brief, an approved example, or an independent source.
- Prefer real interfaces over mocks, summaries, prompts, or proxy metrics.
- Keep evidence fresh. Run the proving check in the same phase where completion is claimed.
- Stop when the proof fails for an unknown reason. Diagnose before adding more changes.

## Domain adaptation

The loop stays fixed while the proof surface changes:

- Research uses cited claims and source checks.
- Writing uses reader intent, required content, and rendered-file review.
- Creative work uses brief fidelity and inspection of the delivered media.
- Operations use safe dry runs, handoff checks, and recovery tests.
- Data work uses known examples, formula inspection, and reconciliation.
- Communications use draft review. Sending remains a separate authorization step.
- Personal plans use real schedule, budget, and dependency checks.
- Software uses automated tests, builds, browser checks, and regression proof.

## Completion contract

Report the outcome, the exact proof run, its fresh result, and any untested risk. Do not claim that a whole plan is complete because one slice passed.
