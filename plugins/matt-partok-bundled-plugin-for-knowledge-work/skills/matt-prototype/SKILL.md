---
name: matt-prototype
description: Build a cheap, explicitly temporary artifact to answer one design question in a Matt workflow. Use for logic or UI experiments, evidence spikes, sample analyses, draft fragments, or other questions that cannot be settled reliably in conversation.
---

# Matt Prototype

A prototype answers one question. Keep the answer and discard or isolate the artifact.

## Pick the experiment

- Logic or state question: load `LOGIC.md` and build the smallest runnable interaction.
- UI question: load `UI.md` and create several meaningfully different variants on one inspectable surface.
- Knowledge-work question: create the lowest-cost artifact that produces useful feedback, such as a source sample, outline, draft fragment, worked example, small analysis, or audience simulation.

## Rules

1. Write the question and success signal before building.
2. Mark the artifact as temporary and keep it out of production paths unless the user explicitly approves promotion.
3. Provide one simple way to inspect or run it.
4. Skip polish, broad abstractions, and unrelated edge cases.
5. Expose the relevant state, evidence, or variation so the user can react to it.
6. Record the verdict, the question settled, and any remaining uncertainty in the durable decision artifact.
7. Do not create branches, commits, tracker comments, or external artifacts unless the task authorizes them.
