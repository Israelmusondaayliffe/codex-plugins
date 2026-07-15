# Target Tools

Load before writing any final prompt. Covers Claude Code, Codex CLI, and the orchestrator layer.

## Claude Code

Version gates: /loop requires v2.1.72 or later, /goal requires v2.1.139 or later. Both are session-scoped: they live in the current conversation and fire only while it is open. Resuming with --resume or --continue restores an unexpired loop and an active goal; a fresh conversation clears both.

### /goal

- Submit a done definition once; the agent keeps working turn after turn until the condition is met or the goal is cleared. Setting a goal starts a turn immediately, no separate prompt needed. One goal per session; a new /goal replaces the active one. Condition cap: 4,000 characters. This is the recommended entry point: same behavior as a loop, easier to reason about.
- The evaluator is a prompt-based Stop hook running the configured small fast model (Haiku by default). After every turn it reads the condition and the conversation, returns met or not met plus a short reason, and that reason steers the next turn.
- The rule that decides whether a goal works: the evaluator reads only the conversation. It cannot run commands or open files. Every condition this skill writes demands pasted proof in the transcript ("npm test exits 0 with the output shown in chat"), never promised proof ("tests pass"). Accepted promises are the number one way goals falsely complete.
- Bound the run inside the condition text: "or stop after 20 turns." The evaluator judges the clause from the conversation like any other criterion.
- Lifecycle: /goal with no argument shows the condition, elapsed time, turns, tokens, and the latest evaluator reason. /goal clear stops it (aliases: stop, off, reset, none, cancel). On resume the condition carries over but turns, timer, and token baseline reset.
- Runs non-interactively too: claude -p "/goal <condition>" drives the loop to completion in a single invocation. Requires the workspace trust dialog accepted; unavailable when disableAllHooks or allowManagedHooksOnly is set.
- Pairs with auto mode: auto mode removes per-tool prompts, /goal removes per-turn prompts. A custom prompt-based Stop hook is the escape hatch when the check needs logic the evaluator cannot express.

### /loop

- With an interval ("/loop 5m check the deploy"): converted to a cron expression and run on that schedule. The interval can lead as a bare token (30m) or trail as a clause (every 2 hours). Units s, m, h, d; one-minute granularity; intervals that do not map to clean cron steps are rounded and announced.
- Without an interval: self-pacing. After each iteration the agent picks a delay between one minute and one hour based on what it observed, and can end the loop itself when the work is done. For watch-this-command work it may use the Monitor tool instead of polling, usually cheaper and more responsive.
- Bare /loop runs the built-in maintenance prompt (continue unfinished work, tend the branch PR, cleanup passes), or the user's loop.md when one exists: .claude/loop.md (project) beats ~/.claude/loop.md (user), plain markdown, keep under 25,000 bytes. loop.md replaces the default prompt only, it is not a task list.
- A skill can be the prompt: "/loop 20m /review-pr 1234". Only skills the model may invoke on its own actually run; built-in commands and disable-model-invocation skills arrive as plain text.
- One-shot reminders need no /loop: plain language ("remind me at 3pm to push the release branch") schedules a single-fire task that deletes itself.
- Scheduling mechanics that shape loop design:
  - Jitter: recurring fires land up to 30 minutes after the scheduled time (half the interval for sub-hourly). One-shots at :00 or :30 fire up to 90 seconds early. When exact timing matters, pick an off minute ("3 9 * * *" not "0 9 * * *").
  - Seven-day expiry: a recurring task fires one final time at day seven, then deletes itself. Longer-lived work moves up the durability ladder below.
  - No catch-up: a fire missed while the agent was busy runs once when idle, not once per missed interval.
  - Fires land between turns, in local time. Session cap: 50 scheduled tasks. Esc clears a waiting loop's next wakeup. Underneath sit CronCreate, CronList, CronDelete; plain language lists or cancels tasks.

### The durability ladder

/loop dies with the session and expires at seven days. When the session or machine cannot be trusted to stay open, move up: Desktop scheduled tasks (local machine, no open session needed, 1-minute minimum interval), then Routines via /schedule (Anthropic cloud, no machine at all, 1-hour minimum, runs on a fresh clone so no local files). Event-driven beats polling where it exists: Channels push CI failures into the session directly. Every generated loop names which rung it assumes and why.

### Shared machinery

- Skills: saved instruction sets, referenced by name inside loops ("use the verify-research skill after each section").
- CLAUDE.md: read at every session start, gives the loop its constraints on every run. Keep it short, it is paid for on every beat.
- Subagents: can be deployed inside loops, each starts with a fresh context window. Use for verifier agents at checkpoints.
- /compact: run manually before long sessions.
- Reasoning effort: xhigh is the recommended default for agentic and coding work on frontier models (Fable 5, Opus 4.7 and later, Sonnet 5). Drop to high or medium for routine loops where each beat is simple, effort is paid on every beat.
- Role strength: reviewing. Claude Code tends to be strong at reading a builder's output and finding spec violations, safety issues, error states, and security holes.

## Codex (app and CLI)

- /goal: same primitive, a durable objective attached to the thread with a lifecycle and budget, completion gated on evidence rather than the model believing it is done. Lifecycle: /goal set or view, /goal pause, /goal resume, /goal clear. Side chats inside a Goal thread let the user check progress without interrupting the active turn.
- Every Codex Goal this skill writes carries six required elements: outcome (what should be true when done), verification surface (the test, benchmark, artifact, or command output that proves it), constraints (what must not regress), boundaries (which files, tools, data, repos may be used), iteration policy (how to choose the next action after each attempt), and blocked stop condition (when to stop and report that no defensible path remains, plus what would clear the block). The most common Goal failure is no stop condition, it runs to budget exhaustion, and reaching budget is not completing the objective. Template shape:

```
/goal <desired end state> verified by <specific evidence> while preserving <constraints>. Use <allowed inputs, tools, boundaries>. Between iterations, <how to choose next action>. If blocked or no valid paths, <what to report and what would clear the block>.
```

- Prompt style: GPT-5.5 is outcome-first. State the outcome, criteria, and constraints, let the model pick the path. Step-by-step procedural prompts make it brittle. Never write a Codex goal as a numbered procedure.
- Constraints placement: Codex reads a four-layer AGENTS.md chain on every task (global ~/.codex/AGENTS.md, override, workspace, project, most-specific wins). Standing constraints belong in the right chain layer, not repeated inside every goal. Goal text carries only task-specific boundaries.
- Recurring work: Codex uses Automations for scheduled runs and Goals for sustained autonomous work. /loop and /schedule are Claude Code vocabulary, do not emit them for Codex.
- Subagents: first-class, configured under [agents] in ~/.codex/config.toml with named pre-scoped blocks and lifecycle verbs (spawn_agent, wait_agent, close_agent). Each subagent is a full model round-trip, cost scales, cap max_concurrent. Verifier agents inside Codex loops use this mechanism.
- Role strength: building and sustained Goal-driven execution with tool chaining. The proven cross-tool pattern: plan in Claude with explicit success criteria, paste into Codex prefixed with /goal, review the diff.

## Harness inheritance (both tools)

When the user runs an operating harness (CLAUDE.md or AGENTS.md contract chain, a single dated write destination like CLAUDE-OUTPUTS/ or CODEX-OUTPUTS/YYYY-MM-DD/, validators, a four-phase workflow), generated goals and loops inherit it: scope defaults to the harness output folder with versioned naming and an announced output path, verification maps onto the harness verify phase (score 0 to 10, revise once below 8), and the prompt repeats nothing the contract chain already loads every turn, every duplicated line is paid on every beat.

## The distinction that matters for both

Writing "goal:" inside the body of an ordinary prompt is a labeled prompt, not the primitive. The primitive is /goal itself: interactive (submit it, walk away) or headless (claude -p "/goal ..."). When a user wants one-shot single-turn behavior, write a strong prompt and say so, do not dress it as a goal.

## Orchestrator layer (multi-agent)

Three roles, constant across tools:

- Orchestrator: control loop, task decomposition, worker selection, cards, background processes, dependencies, final verification, user-facing summary.
- Builder: spec in, working code out. Default: Codex.
- Reviewer: finds what is wrong with the builder's output. Default: Claude Code.

The verification rule: after the builder marks done, the orchestrator runs the named commands itself (npm test, npm run build, pytest). Never trust self-report. Without verification /goal is a fancier prompt, with it, a contract.

Parallelism: default one main builder per repo. Parallel only across clear boundaries: repos, branches, git worktrees, packages, docs vs code, tests vs implementation. Never multiple workers on the same file. Competing approaches: N builders in N worktrees, orchestrator picks the best. A board with a card per goal makes parallel background work manageable.

## Unknowns to flag rather than fabricate

Exact flag names, budget syntax, and plan gating change between releases. The Codex facts above are grounded in the user's harness hub (v5, June 2026). When a user needs the precise current syntax of a flag or a budget parameter beyond what is stated here, say the structure is stable but the flag surface may have changed, and verify against current docs rather than guessing.
