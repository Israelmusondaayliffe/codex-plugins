# Agent: Run Loop

## Scope

Executes an approved contract to completion or stop. Does not write contracts (route back, CONTRACT) and does not verify third-party artifacts standalone (route back, VERIFY).

## Inputs

The contract file, the progress file, the environment mode from `references/environments.md`.

## The Loop

Each iteration follows the same beat. Read the progress file first, always: it is what keeps attempt N from repeating attempt N-1.

### 1. Work one milestone

Pick the next milestone from the contract's outcome and the progress file's "next action." Work it fully. Do not end the turn on a plan, a promise, or a list of next steps: if the last paragraph describes work not yet done, do that work now. Pause mid-run only for destructive or irreversible actions, real scope changes, or input only the user can provide.

### 2. Truthful progress

Before logging anything: audit each claim against a tool result from this session. Only report work you can point to evidence for. If something is not yet verified, write "unverified" next to it. If a test fails, log the failure with its output. This rule is non-negotiable, it is the difference between a run and a story about a run.

### 3. Deterministic gate

```bash
python scripts/verify_contract.py <contract-file> --artifact <deliverable-path>
```

Any machine-check failure means the iteration is not done, no matter how finished the work feels. Fix or iterate, never argue with the script.

### 4. Fresh-context verification

When all machine checks pass, spawn the verifier as a subagent (the Agent tool). Hand it exactly two things: the contract file path and the artifact path(s). Never the working narrative, never this loop's reasoning, its independence is the entire point. Its instruction: score each judgment criterion 0 to 10 with evidence quoted from the artifact, list concrete gaps for anything below 8, return scores plus gaps. In environments without subagents, use the degraded self-verification protocol in environments.md and label the result as such.

### 5. Decide

- All machine checks pass and every judgment criterion at 8 or above: complete. At 9 or 10 first pass, ship immediately, forced revision on strong output introduces flaws.
- Any criterion below 8: apply the iteration policy to the named gaps, log the iteration, go to 1.
- Failure or blocked condition met, or cap reached: stop per the contract.

### 6. Log

Append the iteration entry to the progress file: actions, evidence, check results, verifier scores, chosen next action. Every entry, every iteration, no exceptions. An unlogged iteration is invisible to RESUME and to the user.

## Completion Report

One line verdict, then evidence: machine checks passed (count), judgment scores per criterion, iterations used, deliverable path announced exactly. Nothing else, the user can read the progress file for the story.

## Stop Report

Which stop fired, what is complete versus missing (from the progress file, with evidence), what would clear the block, and the exact resume line: "invoke goal-runner RESUME on <contract-path>."

## Native /goal Interplay (Claude Code)

Where native /goal is available, optionally set it with the contract's success stop as the condition, the native fast-model evaluator becomes a free extra gate. The skill's own gates still run: native /goal checks the condition as written, and a condition is only as sharp as its contract. Do not rely on native /goal in place of the deterministic gate.

## Error Handling

Verifier subagent fails to spawn: retry once, then degrade per environments.md and flag it in the report. Machine check errors (not fails): stop and surface, an erroring gate is a broken gate, not a passed one. Scope creep mid-run: stop and confirm, a wrong direction at iteration 2 poisons iterations 3 through 5.
