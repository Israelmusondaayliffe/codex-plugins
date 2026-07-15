# Long-Horizon and Autonomous Agent Patterns for Fable 5

Fable 5's defining capability is long-horizon autonomy: multi-day, goal-directed runs with strong instruction retention. This file is the design manual for harnesses that exploit it. All snippets referenced by number live in `snippet-library.md`.

## Design principle: start at the top of your difficulty range

The guide is explicit: teams see the best outcomes applying Fable 5 to their hardest unsolved problems. Testing only on simpler workloads undersells it. When designing a long-run harness, pick a task harder than what prior models could handle, then have Fable 5 scope it, ask clarifying questions, and execute.

## The five pillars of a Fable 5 long-run harness

A production long-run prompt should address all five. Each maps to a documented failure mode; skipping one leaves that failure mode open.

### 1. Truthful progress (snippet 5)

Evidence-grounded progress reporting is non-optional on autonomous runs. Anthropic's testing showed the audit-against-tool-results instruction nearly eliminated fabricated status reports even on tasks designed to elicit them. Put it in every long-run prompt.

### 2. Verification cadence (snippet 14)

Separate, fresh-context verifier subagents outperform self-critique. Design decisions:

- **Interval.** Tie it to milestones (per module, per spec section) rather than wall-clock time when possible.
- **Fresh context.** The verifier gets the spec and the artifact, not the builder's working narrative. That independence is why it beats self-critique.
- **Spec as anchor.** Verification is "against the specification," so the harness must make the spec durable and addressable (a file, not a memory).

### 3. Turn-ending discipline (snippets 4 and 9)

Interactive long work gets the checkpoint instruction (snippet 4): pause only for destructive/irreversible actions, real scope changes, or input only the user can provide.

Unattended pipelines add the autonomous system reminder (snippet 9): no permission-asking mid-run, no ending a turn on a promise, last-paragraph self-check before ending.

Rare early-stop recovery: if a run ends with stated intent and no tool call, a bare "continue" or "go ahead and do it end to end" resumes it. Build that nudge into pipeline retry logic.

### 4. Memory across runs (snippet 8)

Fable 5 performs particularly well when it can record and reference lessons. Minimum viable memory system:

- A writable directory of Markdown files the agent owns.
- The one-lesson-per-file convention with a one-line summary at top.
- Hygiene rules baked into the prompt: don't duplicate what the repo or chat history records, update rather than duplicate, delete wrong notes.
- Bootstrap on first deployment with the reflect-on-previous-sessions instruction, using subagents to mine history.

### 5. Communication surface (snippets 12 and 13)

Two distinct needs:

- **Final summaries** after unwatched work: the readability addendum (snippet 12). Outcome first, complete sentences, no working shorthand, re-introduce all vocabulary.
- **Mid-run verbatim delivery:** the send_to_user tool (snippet 13). Required when UX depends on exact content arriving intact mid-task (partial deliverables, numeric progress, direct answers to mid-loop questions). Tool inputs are never summarized, so content arrives exactly as written. The definition alone is insufficient; pair it with elicitation language or Fable 5 rarely calls it. Guard against over-calling for narration.

## Subagent orchestration

Fable 5 is significantly more dependable at dispatching and sustaining parallel subagents than prior models, and reliably manages ongoing communication with long-running subagents and peer agents.

Design rules from the guide:

- **Delegate freely.** Use subagents frequently for independent subtasks; give explicit guidance about when delegation is appropriate (snippet 7).
- **Async over blocking.** The orchestrator keeps working while subagents run and intervenes when one goes off track or lacks context. Don't serialize on the slowest subagent.
- **Long-lived over disposable.** Subagents that keep context across subtasks save time and cost through cache reads. Prefer assigning a workstream to one persistent subagent over spawning fresh ones per subtask.
- **Verifiers are subagents too.** The fresh-context verifier from pillar 2 is a dedicated subagent role.

## Context management

- **Hide token countdowns.** Remaining-token displays are the main trigger for context-anxiety behaviors (offering to summarize, hand off, or trim work). Remove them from what the model sees.
- If the harness must show them, include the reassurance line (snippet 10).
- Long-lived subagents also reduce orchestrator context pressure by keeping workstream detail out of the main window.

## Harness infrastructure checklist

- [ ] Client timeouts sized for many-minute turns; streaming on
- [ ] Runs checked asynchronously (scheduled jobs), not blocking
- [ ] "continue" nudge wired into retry logic for rare early stops
- [ ] Spec stored as a durable, addressable artifact
- [ ] Memory directory provisioned and writable
- [ ] send_to_user tool defined + elicitation language in system prompt (if verbatim delivery needed)
- [ ] No remaining-token countdown visible to the model
- [ ] Fallback to Opus 4.8 configured for classifier-adjacent workloads
- [ ] No reasoning-echo instructions anywhere in the harness (refusal risk)

## Skeleton: autonomous long-run system prompt

The skeleton below composes the pillars. It is a starting structure to adapt, not to inflate. Sections in brackets are fill-ins.

```text
You are [role] working autonomously on [the larger task] for [who it's for]. They need [what the output enables].

# Specification
The full specification lives at [path]. It is the single source of truth for what done means.

# Working style
When you have enough information to act, act. Do not re-derive facts already established, re-litigate settled decisions, or narrate options you will not pursue in user-facing messages.

Don't add features, refactor, or introduce abstractions beyond what the task requires. Do the simplest thing that works well. Only validate at system boundaries.

# Delegation
Delegate independent subtasks to subagents and keep working while they run. Intervene if a subagent goes off track or is missing relevant context. Prefer long-lived subagents that keep their context across subtasks.

# Verification
Establish a method for checking your own work at an interval of [milestone] as you build. Run this every [milestone], verifying your work with fresh-context subagents against the specification.

# Progress reporting
Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet verified, say so explicitly. Report outcomes faithfully: if tests fail, say so with the output; if a step was skipped, say that; when something is done and verified, state it plainly without hedging.

# Memory
Record lessons in [memory path]. Store one lesson per file with a one-line summary at the top. Record corrections and confirmed approaches alike, including why they mattered. Don't save what the repo or chat history already records; update an existing note rather than creating a duplicate; delete notes that turn out to be wrong.

# Autonomy
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task. For reversible actions that follow from the original request, proceed without asking. Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done, do that work now with tool calls. End your turn only when the task is complete or you are blocked on input only the user can provide.

# Communicating with the user
Between tool calls, when you have content the user must read verbatim (a partial deliverable, a direct answer to their question), call the send_to_user tool with that content. Use send_to_user only for user-facing content, not for narration or reasoning.

Your final summary is for a reader who saw none of your working thread. Open with the outcome in one sentence. Write complete sentences, spell out terms, drop working shorthand and invented labels, and give every file, commit, or identifier its own plain-language clause. If you have to choose between short and clear, choose clear.
```
