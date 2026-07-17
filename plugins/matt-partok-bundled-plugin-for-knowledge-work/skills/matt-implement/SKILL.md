---
name: matt-implement
description: Execute one approved Matt-flow ticket or bounded work slice with continuous feedback and fresh proof. Use when the user explicitly asks to implement a Matt ticket, execute the next Matt slice, or continue a Matt spec after slicing.
---

# Matt Implement

Execute one approved, unblocked slice. Inspect the closest project instructions and source artifacts before changing anything.

## Route by work type

- Software: use `matt-tdd` at the agreed seams, run focused checks during work, run the relevant full checks at the end, then use `matt-code-review`.
- Knowledge work: preserve source and claim evidence, verify the artifact on its real surface, and review it against the originating brief before delivery.
- Mixed work: keep one acceptance surface for the slice and run both relevant verification paths.

## Execution rules

1. Restate the slice, blockers, allowed paths, and acceptance checks.
2. Re-read live state. Do not trust a stale handoff as current state.
3. Make the smallest complete change that produces the observable result.
4. Run the narrowest useful check after each meaningful change.
5. Repair failures before adding scope.
6. Run final checks and compare the result against the spec.
7. Return the evidence, remaining risks, and next unblocked slice.

Do not automatically commit, publish, send, assign, or close tracker items. Take those actions only when the active task authorizes them, then verify the resulting state.
