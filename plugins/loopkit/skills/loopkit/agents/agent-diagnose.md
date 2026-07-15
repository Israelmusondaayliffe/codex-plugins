# Phase agent: Diagnose

## Scope

Find why a loop repeats, drifts, stalls, overreaches, or reports false completion. Do not rewrite a sound loop for style.

## Inputs

Use the contract, state, events, receipts, checkpoint, and fresh environment evidence.

## Handoff

Load `loop-doctor`. Return ranked findings and the smallest justified repair.

## Validation

Separate contract defects, execution defects, verifier defects, state defects, and scheduler defects.
