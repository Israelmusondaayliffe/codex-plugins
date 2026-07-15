# Agent: Resume

## Scope

Continues an interrupted or capped run. Reads state from files, never from memory of a prior session. Does not renegotiate the contract (that is a new CONTRACT pass if the user wants changes).

## Inputs

The contract file path and the progress file path. If the user cannot name them, look in the harness output folder for the most recent `*goal-contract*` and its sibling progress file, confirm the match before proceeding.

## Workflow

### 1. Reconstruct state

Read both files fully. From the progress file: iterations used, what passed, what failed last, what the last chosen next action was. From the contract: the criteria and stops, unchanged. State reconstruction comes only from these files, prior-session context is gone and guessing at it is fabrication.

### 2. Re-run the gates before doing any work

```bash
python scripts/verify_contract.py <contract-file> --artifact <deliverable-path>
```

The world may have changed since the last session (files moved, edits made by the user). The current truth is what the checks say now, not what the log says they said then. Log a resume entry recording the re-check results.

### 3. Budget the remaining cap

Iterations used count against the contract cap. If the cap is already exhausted, do not silently extend it: report the state and ask the user for one of extend (name the new cap), close with a blocked report, or re-contract.

### 4. Continue

Hand the reconstructed state to the RUN loop (`agents/agent-run.md`), starting at the last chosen next action, or at the first failed check if the world changed. Everything in RUN applies, including truthful progress and the logging discipline.

## Outputs

Either the RUN loop's completion or stop report, or the cap-exhausted question. The resume entry in the progress file marks the session boundary so the log stays auditable.

## Error Handling

Contract file missing or progress file corrupted: report which state is unrecoverable and offer re-contracting from the artifact's current condition (VERIFY can establish what is already done, so nothing finished is redone). Contract and artifact contradict each other (deliverable path renamed): one focused question rather than a guess.
