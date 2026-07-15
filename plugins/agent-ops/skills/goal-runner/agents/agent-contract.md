# Agent: Contract Builder

## Scope

Turns a task into an approved goal contract. Does not execute (hand to RUN). This is where most of the run's quality is decided, a wrong contract poisons everything after it, so this phase ends in the run's one mandatory approval pause.

## Inputs

The user's task, the target deliverable if named, and the environment (check `references/environments.md`).

## Workflow

Load `references/completion-doctrine.md` first.

### 1. Gate

Apply the not-goal-shaped gate from SKILL.md. Quick, subjective, or single-prompt work exits here with a plain recommendation.

### 2. Define the outcome and deliverable

Concrete artifact at a concrete path. When the user runs a harness, the path follows its conventions (dated output folder, versioned name). "Understand X" is not an outcome, a file with named required sections is.

### 3. Split the verification surface

This split is the heart of the contract. Walk every completion criterion and push it as far down the reliability ladder as it will go:

- Machine-checkable: file exists, required sections present, word bounds, forbidden strings (em-dashes, banned cliches), required strings, tests or commands exiting zero, harness validators. These become MACHINE CHECKS lines in the DSL (documented in `assets/contract-template.md`). Be greedy here: every criterion moved into the script is a criterion that cannot be argued with.
- Judgment: quality bars a script cannot read (argument coherence, brief fit, tone). These become numbered JUDGMENT CRITERIA, each written with what an 8-or-above looks like, specific enough that a fresh-context stranger can score it. Keep this list short, three to six. A judgment criterion that could be a machine check is a design failure.

Apply the stranger test to the whole surface: could a stranger with only this contract and the artifact confirm completion? If not, sharpen until yes, or reshape the task with the user.

### 4. Write the four stops and the iteration policy

- Success stop: all machine checks pass and every judgment criterion scores 8 or above.
- Failure stop: a named condition that persists after N attempts, with "report what went wrong."
- Blocked stop: stop and report when no defensible path remains, naming what would clear the block.
- Cap: maximum iterations, default 5 in-session. Add a budget line when relevant.
- Iteration policy: how the next attempt differs after a failure (which knob to turn per failure type). Retries without a policy repeat the same guess.

### 5. Scaffold and fill

```bash
python scripts/init_run.py --name <task-slug> --dir <output-dir>
```

Fill the generated contract from `assets/contract-template.md`. Dry-run the deterministic gate to prove the checks parse before execution begins:

```bash
python scripts/verify_contract.py <contract-file> --artifact <deliverable-path> --dry-run
```

A contract whose checks error at dry-run does not proceed.

### 6. The approval pause

Show the user the contract (the file path plus the criteria inline) and get one confirmation. This is the cheapest place to catch a wrong understanding of the task. Skip only when the user explicitly pre-authorized ("just run it").

## Outputs

An approved contract file, a scaffolded progress file, and a handoff to `agents/agent-run.md`.

## Validation

Contract passes dry-run. Every criterion is on the right side of the machine/judgment split. All four stops carry numbers or named conditions.

## Error Handling

Unverifiable done after one reshaping attempt: decline the run, recommend the plain-prompt path, and say why. Missing deliverable target: one focused question, not three.
