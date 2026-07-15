---
name: goal-runner
description: Run a task to evidence-gated completion. Takes any deliverable task, converts it into a durable goal contract (outcome, machine checks, judgment criteria, four stops, iteration policy), then drives an execute-verify loop that never reports done unless a deterministic check script passes and a fresh-context verifier that did not do the work confirms every criterion. Never dies silently, it finishes or stops with a blocked report naming what would clear the block. Four routed modes. CONTRACT builds the goal contract. RUN executes the loop. VERIFY checks any existing deliverable against a spec. RESUME continues an interrupted run from the contract and progress files. Triggers on run this as a goal, goal runner, run to completion, make sure this is absolutely complete, don't stop until done, finish this fully, completion contract, verify this against the brief or spec, evidence-gated done, resume the goal run, or any task where completion must be guaranteed rather than claimed.
metadata:
  author: Israel A
  version: 1.1.0
---

# Goal Runner

Take a task, drive it to completion, and prove it. The one promise this skill makes: done is never claimed, it is demonstrated. A deterministic script passes, a verifier that did not do the work confirms the rest, and only then does the run report complete. When it cannot finish, it stops on a stop rule and reports exactly what is missing and what would clear the block.

This is the executor in the family: agent-builder designs agentic systems, loop-goal-engineer writes goal prompts for external CLIs, goal-runner executes goals in the current session.

## The Completion-Assurance Stack

Every run climbs the same five layers:

1. Contract. The task becomes a durable file, not a context memory. Outcome, deliverable path, machine-checkable criteria, judgment criteria, four stops, iteration policy.
2. Execution loop. Milestone-sized iterations. Every progress claim is audited against a tool result from this session before it is reported. Unverified work is labeled unverified.
3. Deterministic gate. `scripts/verify_contract.py` runs the machine checks. Scripts always run and cannot corrupt good output.
4. Fresh-context verifier. A subagent that receives only the contract and the artifact, never the builder's working narrative, scores each judgment criterion 0 to 10 with evidence.
5. Loop control. Failures feed the iteration policy, attempts log to the progress file, stops are enforced (success, failure, blocked, cap).

## Router Logic

**CONTRACT** -> Load `agents/agent-contract.md`
Triggers: any fresh "run this to completion" task. Default entry for new work. Ends with an approved contract and hands to RUN.

**RUN** -> Load `agents/agent-run.md`
Triggers: an approved contract exists (from CONTRACT, or the user supplies one). Executes the loop to completion or stop.

**VERIFY** -> Load `agents/agent-verify.md`
Triggers: "check this against the brief", "is this actually complete", "verify this deliverable", an artifact plus a spec and no execution needed. Runs layers 3 and 4 standalone.

**RESUME** -> Load `agents/agent-resume.md`
Triggers: "resume the goal run", "continue where it stopped", a contract and progress file exist from a prior session or a capped run.

## The Not-Goal-Shaped Gate

Before contracting, apply the gate: quick questions, single-prompt tasks, and work whose done is subjective bypass this skill entirely, the loop overhead makes them slower, not better. If done cannot survive the stranger test (a stranger confirms completion from the output alone, no questions), reshape the task with the user or decline the run. Never run the machine on an unverifiable goal.

## Environment Handling

Load `references/environments.md` at the start of every run. Summary: Cowork is home (subagent verifier, executable scripts, full stack). Claude Code can additionally hand the contract's success condition to native /goal, the skill still supplies what native lacks, contract quality and the deterministic gate. Codex targets are not emulated, translate the contract into the six-element Goal via the loop-goal-engineer skill and hand off. Plain chat runs a degraded self-verification and says so.

## State Files

A run's state lives in two files created by `scripts/init_run.py`, named and versioned per the user's harness conventions when one exists (dated output folder, versioned filenames):

- The goal contract, from `assets/contract-template.md`. The single source of truth for what done means. The verifier anchors on this file.
- The progress file, from `assets/progress-template.md`. One entry per iteration: actions, evidence, check results, verifier score, next action chosen by the iteration policy. Read at the start of every iteration, updated at the end. This is what makes runs resumable and retries non-repeating.

## Shared Resources

- `references/completion-doctrine.md` The stranger test, the four stops, iteration policy, the truthful-progress rule, the critique paradox, why fresh-context verification beats self-critique, the compounding math that keeps iterations few and coarse. Load in every mode.
- `references/environments.md` Per-environment behavior and the native /goal interplay. Load in every mode.
- `assets/contract-template.md` Contract skeleton plus the machine-check DSL reference.
- `assets/progress-template.md` Iteration log skeleton.
- `scripts/init_run.py` Scaffolds the two state files.
- `scripts/verify_contract.py` The deterministic gate. Parses MACHINE CHECKS from the contract and pass/fails each.

## Output Contract

At completion: one line stating the verdict, the evidence summary (which checks passed, verifier scores per criterion), and the deliverable path. At a stop: which stop fired, what is missing, what would clear the block, and the exact resume instruction. No em-dashes, no emojis, plain language throughout.

## Error Recovery

A failed iteration is normal, that is what the loop is for. A failed phase is not: if the contract cannot be made verifiable, if the verifier subagent cannot be spawned, or if machine checks error rather than fail, surface it with options (fix, degrade mode, abandon) rather than papering over. The run is only as honest as its weakest gate.
