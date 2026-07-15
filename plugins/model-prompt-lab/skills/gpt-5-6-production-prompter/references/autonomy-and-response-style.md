# Autonomy Boundaries and Response Style for GPT-5.6

Two first-class 5.6 prompting practices. Both exist because 5.6's defaults moved: it is more proactive and persistent on multi-step tasks, and more concise by default than 5.5. Prompts written for older defaults now overshoot in both directions.

## Autonomy and approval boundaries

GPT-5.6 can be proactive and persistent when carrying out multi-step tasks. Define what level of action each request authorizes so the model can continue safe, in-scope work without unnecessary pauses while stopping before external, destructive, costly, or scope-expanding actions.

### The compact policy (default)

A compact policy is usually sufficient:

```text
For requests to answer, explain, review, diagnose, or plan, inspect the relevant
materials and report the result. Do not implement changes unless the request also
asks for them.

For requests to change, build, or fix, make the requested in-scope local changes
and run relevant non-destructive validation without asking first.

Require confirmation for external writes, destructive actions, purchases, or a
material expansion of scope.
```

The policy's shape: three request classes (read-shaped, write-shaped, and boundary-crossing), each with one clear authorization level.

### Name safe local actions explicitly

Generic policies leave the model guessing about specific actions. Name them for the tool surface at hand:

```text
Safe without asking: reading files, inspecting logs, editing in-scope code,
running tests, running lint and type checks, rendering previews.
```

### The one-place rule

Keep the policy in one place and state each rule once. **Repeating instructions such as "ask first," "do not mutate," or "wait for approval" can cause unnecessary approval requests for safe, expected actions.**

This is the most common autonomy bug in migrated prompts: a 5.4-era prompt with "confirm before acting" in the persona block, "ask before changes" in the constraints, and "wait for approval" in a safety block reads to 5.6 as a mandate to pause constantly. Consolidate to one policy; delete the echoes.

### Tuning the policy

| Surface | Adjustment |
|---------|-----------|
| Local dev agent | Widen the safe list (branch creation, dependency installs in the sandbox); keep pushes, deploys, deletions behind confirmation |
| Customer service agent | Reversible account lookups and drafts are safe; refunds, cancellations, sends require explicit confirmation with exact details |
| Regulated / high-stakes | Narrow the safe list to read-only; add "prefer the most reversible action when two paths achieve the same goal" |
| Research agent | Almost everything is safe (reads); the boundary is publishing, posting, or contacting |

### Ambiguity triggers

Tell the model when an important ambiguity should trigger a question, as part of the same policy:

```text
If the target environment, affected customer set, or deletion scope is ambiguous,
ask before proceeding. For other ambiguities, choose the most reasonable
interpretation and state the assumption inline.
```

## Response length and style

### Re-check every brevity instruction

GPT-5.6 tends to be more concise by default than GPT-5.5. When migrating, check whether broad brevity instructions such as "Be concise" or "Keep it short" are still useful. They may be unnecessary, and they can make responses too brief. Keep them only when they reliably produce the output your application needs.

The failure signature: answers that drop required caveats, evidence, or next steps. The instinctive fix (adding "but be thorough") creates a contradiction; the right fix is removing the legacy brevity instruction and specifying content requirements instead.

### Set the default with text.verbosity

Choose `low`, `medium`, or `high` as the default level of detail for a request. Then use the prompt for task-specific length, structure, and required content. The parameter sets the register; the prompt sets the contract.

### The must-include contract for short answers

When a task calls for a shorter answer, identify the information the model must preserve and the detail it can omit:

```text
Lead with the conclusion. Include the evidence needed to support it, any material
caveat, and the next action. Omit secondary detail and repetition.
```

```text
Keep all required facts, decisions, caveats, and next steps. Trim introductions,
repetition, generic reassurance, and optional background first.
```

This gives the model a priority order: preserve the content needed to complete the task, then remove lower-value detail. A short answer with a must-include contract is safe; a short answer commanded by "be concise" alone is a coin flip on what gets cut.

### Define tone through concrete writing choices

Broad labels such as "friendly" or "empathetic" can be ambiguous. Describe the writing choices that define your product's tone: how directly to state the answer, when to acknowledge a problem, whether reassurance or a sign-off is appropriate.

```text
State the answer directly. If the user reports a problem, acknowledge the
specific issue before giving the next step. Use reassurance only when it is
relevant. Omit generic praise and unnecessary sign-offs.
```

Pair this with the personality/collaboration split in `references/personality-and-collaboration.md`: personality names the character, and these concrete choices are how the character behaves in text.

## Combined section template

For an agent prompt, autonomy and output style typically land as two adjacent sections:

```text
# Autonomy
For requests to answer, review, diagnose, or plan: inspect and report; do not
implement unless asked. For requests to change, build, or fix: make in-scope
local changes and run non-destructive validation without asking. Safe without
asking: [named actions]. Require confirmation for external writes, destructive
actions, purchases, or material scope expansion. If [named ambiguity] is
unclear, ask; otherwise state assumptions inline.

# Output
Lead with the conclusion. Include supporting evidence, material caveats, and
the next action. Omit secondary detail and repetition. [Format and length
specifics for the surface.]
```

## Troubleshooting map

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| Pauses for approval on safe actions | Repeated ask-first instructions, or no named safe list | Consolidate to one policy; name safe actions |
| Acts past authority | Missing or vague confirmation clause | Name the boundary actions (external writes, destructive, purchases, scope expansion) |
| Answers too brief, drops caveats | Legacy brevity instruction stacking on 5.6's concise default | Remove the instruction; add a must-include contract |
| Answers too long | Verbosity set high, or contract lists too much as required | Lower `text.verbosity`; trim the must-include list |
| Tone generic or off-brand | Broad tone labels | Replace with concrete writing choices |
| Never asks about real forks | No ambiguity triggers defined | Name the ambiguities worth stopping for |
