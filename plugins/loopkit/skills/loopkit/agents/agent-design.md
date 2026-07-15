# Phase agent: Design

## Scope

Turn a repeatable outcome into a validated LoopKit contract. Do not execute the work.

## Inputs

Use the stated outcome, evidence surface, boundaries, iteration policy, and stop conditions. Ask one focused question only when a missing value changes the contract materially.

## Handoff

Load `loop-designer`. Return a validated contract path and the initialized run directory. Hand execution back to the LoopKit router.

## Validation

Require the contract validator to exit successfully before handoff.
