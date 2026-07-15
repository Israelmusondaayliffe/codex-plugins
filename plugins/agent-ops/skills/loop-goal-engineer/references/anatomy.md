# Anatomy: Goals and Loops

The knowledge core. Every agent loads this.

## The primitive

A prompt tells the agent what to do. A goal condition tells the agent when to stop. Compare:

Single-turn prompt: "Fix the failing tests in the auth module."

Loop condition:

```
/loop all tests in the auth module pass and coverage is above 80%
```

The shift is from prompting (you driving every turn) to assigning (the agent driving toward a target you defined). The goal stays active until achieved, paused, blocked, cleared, or out of budget. Note: writing "goal:" inside a one-shot command is still just a labeled prompt. The real primitive lives inside an interactive worker session: launch the CLI, submit /goal, walk away.

## The four parts of every working goal

1. The goal. A verifiable end state. The test: could a stranger look at the output and confirm it meets the goal without asking the author any questions? That is the stranger test, apply it to every goal this skill writes.
2. The scope. Which files, folders, or areas the agent may touch. Example phrasing: "Only modify files in /research/. Do not create files outside this directory. Do not change any existing files unless specified." Ten seconds that prevents the most common runaway behavior.
3. The checker. Verification built into the goal ("verify that every claim has a source URL, flag any entry missing a source"), or the tool's grader (/goal runs a separate fast model to grade after every turn), or ideally both. The grader reads only the conversation, it cannot run commands or open files, so the condition must demand pasted proof in the transcript, never promised proof.
4. The stop rule. One for success, one for failure, plus a hard cap: "Stop when all sections are complete and verified. If the same search returns no new information 3 times in a row, stop and report what's missing. Maximum 15 iterations."

## The six working parts of every loop

1. Trigger. What starts the loop. /schedule and /loop in Claude Code. /loop with an interval runs on that interval; without one it self-paces, choosing a delay between one minute and one hour per iteration. Session-scoped: it fires only while the session is open and a recurring loop expires seven days after creation. Event triggers: on PR comment, on CI failure, or a Channel pushing the event in.
2. Execution layer. Where the agent reads state, takes action, produces output. No manual input.
3. Verifier. A checkpoint: tests, a build, a screenshot comparison, a quality-gate skill, or /goal's separate fast grader model after every turn.
4. Stop rules. Success stopping (all tests pass), failure stopping (retry count exceeded, unrecoverable error), optional budget caps. Make them explicit:

```
You have a maximum of 20 attempts. If all tests pass, report "TASK_COMPLETE" and stop. If you encounter an error you cannot resolve after 3 retries, report "TASK_FAILED: [reason]" and stop.
```

5. Memory. A markdown progress file logging what has been done, so work can be checked and rolled back. Read at the start of every run, updated at the end. A loop with no memory of what it changed cannot improve, it just repeats.
6. Skills and CLAUDE.md. Saved instruction sets that freeze project knowledge. CLAUDE.md gives the loop its personality and constraints on every run. Keep it short: a bloated rules file is paid for on every beat of the loop.

## The optimal loop structure, compressed

TRIGGER (every 15 min / on PR comment / on CI failure) -> DOER (agent works the task) -> CHECKER (separate model grades the output) -> STOP (all tests green, or 10 iterations, or 5 dollars spent) -> MEMORY (progress.md updated each run) -> SKILLS (CLAUDE.md read at every session start).

## The base /loop template

```
/loop [verifiable end state/time], only touching [scope], stop after [X] constraints, use [X] Skills, use verifier agents for [x] checkpoint, and keep a memory file of all your work.
```

## Stop-rule taxonomy

- Success stop: the end state is met and verified.
- Failure stop: N retries exceeded on the same error, unrecoverable error, missing required input. Always paired with "report what went wrong."
- No-progress stop (research and search loops): "if the same search query appears 3 times in a row without new information surfacing, stop."
- Hard cap: maximum iterations, always a number.
- Budget cap: dollar ceiling per session where the tool supports it.
- Turn-bound clause (Claude Code /goal): the cap lives inside the condition text itself, "or stop after 20 turns," because the evaluator judges only what the condition says against the conversation.

Every generated prompt carries at least success, failure, and hard cap. Loops add no-progress where search is involved.

## The underlying skeleton

Underneath every loop and goal is the same skeleton: a goal it can recognize as finished, a way to check its own work, and a place to write down what happened. Miss the check and it is not a loop, it is an agent guessing in a circle.
