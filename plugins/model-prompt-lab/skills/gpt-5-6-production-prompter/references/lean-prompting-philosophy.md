# Lean Prompting Philosophy for GPT-5.6

This is the conceptual anchor for 5.6 prompting. It is the direct descendant of 5.5's outcome-first philosophy, upgraded from a design preference to a measured practice. Read this before building or migrating any prompt.

## The core idea

GPT-5.5 taught teams to describe the destination, not the path. GPT-5.6 adds two things:

1. **Evidence that leaner wins.** In a sample of OpenAI's internal coding-agent eval runs, configurations with leaner system prompts improved evaluation scores by roughly 10-15% while reducing total tokens by 41-66% and cost by 33-67%. Treat these ranges as directional and validate on representative tasks from your own application. The point stands: removing repeated instructions and examples and simplifying tool descriptions can improve task performance, not just cost.
2. **A model that infers intent.** 5.6 can infer the user's underlying goal and intended level of work from context, so you often do not need to prescribe every step. Your job narrows to supplying what cannot be inferred: domain context, hard constraints, approval boundaries, success criteria, and which ambiguities should trigger a question.

## The subtraction method (now with discipline)

The 5.5 era said "subtract." The 5.6 era says how:

1. Start with a prompt and tool set that already works.
2. Remove one group of instructions, examples, or tools at a time.
3. Rerun the same evals after each removal.
4. Keep the removal if quality holds; restore it if quality drops.

Batching removals destroys attribution. One group, one eval cycle.

What counts as a removable group:
- A repeated instruction (keep one statement, remove the rest)
- An example that no longer encodes a product requirement or corrects a measured gap
- A tool the task does not need
- Verbose passages in tool descriptions
- A protective block compensating for an older model's weakness

What to keep:
- Invariants (safety rules, schema fields, forbidden actions), stated once
- Examples and style guidance that encode a product requirement or correct a measured gap
- Domain context the model cannot infer
- Hard constraints, approval boundaries, success criteria

## Rule 1: State each instruction once

Repetition is not emphasis on 5.6; it is a behavior bug with named consequences:

- Repeating "ask first", "do not mutate", or "wait for approval" causes unnecessary approval requests for safe, expected actions.
- Repeating brevity nudges stacks with 5.6's already-concise default and produces too-brief answers.
- Repeating examples of the same behavior produces mechanical, prompt-shaped output.

If an instruction matters, state it once, in the right section, and trust it. If it matters more than the others, put it earlier.

## Rule 2: Describe outcomes, constraints, and boundaries, not steps

Prefer this:

```text
Resolve the customer's issue end to end.

Success means:
- the eligibility decision is made from the available policy and account data
- any allowed action is completed before responding
- the final answer includes completed_actions, customer_message, and blockers
- if evidence is missing, ask for the smallest missing field
```

Avoid step-by-step procedure unless every step is truly required. 5.6 infers the intended level of work; long procedural lists narrow its search space and produce mechanical answers.

Still provide, always:
- **Domain context** the model cannot infer
- **Hard constraints** that must never be crossed
- **Approval boundaries** for actions (see `references/autonomy-and-response-style.md`)
- **Success criteria** defining done
- **Ambiguity triggers**: "If the target environment is ambiguous, ask before deploying" tells the model which unknowns are worth stopping for.

## Rule 3: Reserve absolute words for true invariants

Use ALWAYS, NEVER, must, only for safety rules, required output fields, and actions that should never happen. For judgment calls (when to search, when to ask, when to keep iterating), use decision rules: a condition and the appropriate response.

```text
After each tool result, ask: "Can I answer the user's core request now with useful evidence and citations for the factual claims?" If yes, answer.
```

## Rule 4: Add explicit stopping conditions

Unchanged from 5.5 and still load-bearing:

```text
Use the minimum evidence sufficient to answer correctly, cite it precisely, then stop.
```

## Rule 5: Keep the tool surface lean

Expose only tools relevant to the task. Keep descriptions concise and precise. Document each tool's expected return fields, types, and error behavior; this matters doubly if Programmatic Tool Calling is in play, because the model writes code against those return shapes before seeing any results.

## Rule 6: Track context weight over the session

Track context both at the start of a run and as the conversation grows. Long sessions amplify repeated prompt and tool content: a duplicated 200-token block costs its weight on every turn. Lean prompts compound their savings across a session; heavy prompts compound their noise.

## The suggested prompt structure

Markdown headers, each section short, detail only where it changes behavior:

```text
Role: [1-2 sentences defining the model's function, context, and job]

# Goal
[user-visible outcome]

# Success criteria
[what must be true before the final answer]

# Constraints
[policy, safety, business, evidence, side-effect limits]

# Autonomy
[one compact approval-boundary policy]

# Output
[sections, length, tone; for short answers, what must still be included]

# Stop rules
[when to retry, fallback, abstain, ask, or stop]
```

`# Personality` and `# Collaboration style` join the scaffold only for customer-facing or conversational surfaces. If a section adds nothing, remove it.

## When XML blocks still earn their place

Same gate as 5.5, applied more strictly:

Good reasons:
- Evals show a specific recurring failure mode the block addresses
- A high-stakes invariant must be guaranteed (`action_safety`, `citation_rules`)
- A structured output contract is required for downstream parsing
- The task genuinely needs a checklist (extraction schemas, completeness for batch work)
- A task-specific `<tool_orchestration>` block is needed to route Programmatic Tool Calling

Bad reasons:
- "It worked in our 5.5 prompt"
- "More instructions feel safer"
- "Just in case"

## The migration corollary

Migrating a 5.5 prompt to 5.6 usually means removing and consolidating, then reviewing the API surface (effort baseline comparison, caching economics, persisted reasoning). A 5.6 prompt that runs cleanly with five short Markdown sections, one autonomy policy, and the right effort tier beats the same prompt with the instructions stated twice.

## What this skill does with this philosophy

The prompt builder uses the lean structure as the default and states every instruction once. The migration agent runs measured subtraction, one group per eval cycle. The troubleshooter checks for duplication before any other diagnosis. The complete examples are written lean so users see the pattern in action.
