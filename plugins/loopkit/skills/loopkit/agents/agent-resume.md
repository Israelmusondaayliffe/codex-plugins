# Phase agent: Resume

## Scope

Restore a nonterminal run from durable files. Do not reconstruct state from conversational memory.

## Inputs

Use the run directory or the current workspace's newest active run.

## Handoff

Load `loop-resumer`. After integrity checks, route to `loop-runner`, `loop-verifier`, or the user if an approval is required.

## Validation

Confirm the current generation and refresh the checkpoint before the next write.
