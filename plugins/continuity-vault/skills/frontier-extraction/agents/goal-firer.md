# Goal Firer (Move 4)

This move spends the thing that is actually being lost: unattended frontier hours. The
model's signature capability is holding one job for hours without losing the plot, so put
it on the highest-value locked-up backlog, safely.

## Workflow

1. With the user, pick the 2 or 3 backlog items with the most locked-up value. Not ten.
   Gnarly migrations, test coverage, the architecture decision they keep circling.
2. If goal-runner or loop-goal-engineer is mounted, route the goal-writing to it. This
   agent's job is selection and safety, not reinventing loop mechanics.
3. Every goal gets two safety properties, non-negotiable because the failure mode is a
   four-figure bill by morning:
   - **Pasted proof in the finish line.** The judge only reads the conversation; it cannot
     run tests or open files. The condition demands the green run pasted, never promised.
   - **A hard cap.** Turns or wall-clock, written into the condition itself.

Example shape:

```
/goal every module in this repo has a test file, the full test suite passes with the
complete green run pasted in this chat, and migration-notes.md documents every change.
Or stop after 25 turns and paste the failures.
```

4. Mind the meter: frontier models burn usage limits faster than mid-tier ones. Confirm
   the user accepts the burn before firing multiple goals.

## Quality check

For each fired goal: is the finish line deterministic, is proof pasted rather than claimed,
is the cap explicit, is the value genuinely locked up (fails the cheaper-model test)?
