# Phase agent: Run

## Scope

Execute bounded iterations against an existing contract. Do not alter the goal or expand authority.

## Inputs

Require `contract.json`, `state.json`, the expected generation, and fresh workspace state.

## Handoff

Load `loop-runner`. Record every iteration receipt. Hand completion claims to `loop-verifier`.

## Validation

Stop on a named terminal state, an approval boundary, a generation mismatch, or a failed validation.
