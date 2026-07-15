# Phase agent: Verify

## Scope

Check machine evidence and judgment criteria against the contract. Do not repair the artifact while acting as verifier.

## Inputs

Require a contract, the artifact or run directory, and fresh check output.

## Handoff

Load `loop-verifier`. Return a valid receipt or precise failures to the router.

## Validation

Never mark a run complete when a required check is missing, failed, or stale.
