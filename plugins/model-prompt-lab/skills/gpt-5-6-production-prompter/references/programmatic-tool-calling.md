# Programmatic Tool Calling (PTC) for GPT-5.6

New in 5.6. The model writes JavaScript to call eligible tools, passes results between calls, and processes intermediate outputs in a hosted runtime. PTC is ZDR-compatible with no additional container costs.

The prompting stakes: PTC is a routing decision, and 5.6 will not route correctly from generic instructions. Every PTC prompt needs task-specific orchestration language.

## When PTC is the right shape

PTC works best for **bounded workflows where code can process several tool results or large intermediate outputs and return a much smaller structured result.** The canonical operations: filtering, joining, ranking, deduplication, aggregation, validation, and other predictable processing.

The test: could you describe the stage as a function signature? "Take the results of tools A, B, C; join on X; rank by Y; return the top N with fields Z" is PTC-shaped. "Look at each result and decide what to do next" is not.

## When to prefer direct tool calls

Multiple, parallel, or dependent calls alone do NOT justify PTC. Use direct, non-PTC calls when:

- One call is sufficient
- The intermediate outputs are already small
- Each result may change the model's next decision (fresh judgment needed between steps)
- An action requires approval
- The final output must preserve citations or native artifacts

## API setup

1. Add the `programmatic_tool_calling` tool to the request.
2. Opt eligible tools in with `allowed_callers`. Tools not opted in stay direct-only.
3. Update the application to handle three item types: `program` items (the code the model wrote), program-issued function calls, and `program_output` items (the program's structured result).
4. Preserve each call's `call_id` and `caller` linkage when round-tripping items.

## Tool descriptions become contracts

PTC means the model writes code against your tools' return shapes **before seeing any results.** Tool descriptions must document:

- Expected return fields and their types
- Error behavior (what a failure looks like, what an empty result looks like)

If the model cannot determine the return shape before writing the program, prefer direct tool calling so it can inspect the result before deciding how to use it.

## Routing instructions must be task-specific

Do not rely on tool availability or generic instructions such as "use Programmatic Tool Calling efficiently." When both direct and programmatic calling are available, explicitly state:

- Which bounded stage should use PTC
- Which tools it may call
- The exact output schema and required evidence
- Concurrency, retry, and stopping limits
- Which work should remain direct

If both routes are needed, define one clear handoff and tell the model not to switch routes or repeat completed work.

### The tool_orchestration template

```text
<tool_orchestration>
Use Programmatic Tool Calling for [bounded stage] using only [eligible tools].
Run independent calls concurrently when safe. Use only documented tool input
and output fields.

Process and reduce the intermediate results, then emit exactly [output schema],
including the evidence needed for the final answer.

Stop when [condition] is met. Retry transient failures at most [R] times.
Do not repeat completed calls or perform side-effecting actions. If a required
result is still missing, return a clear structured failure.

Use direct tool calls for [semantic judgment, approval, or final validation].
</tool_orchestration>
```

Fill every bracket with the task's specifics. An unfilled template is a generic instruction wearing XML.

### Worked example

```text
<tool_orchestration>
Use Programmatic Tool Calling for the candidate-collection stage using only
search_tickets, get_ticket_details, and get_customer_tier.
Run independent get_ticket_details calls concurrently. Use only documented
tool input and output fields.

Process and reduce the intermediate results, then emit exactly:
{
  "candidates": [
    {"ticket_id": string, "customer_tier": string, "age_days": number,
     "summary": string, "evidence_url": string}
  ]
}
sorted by age_days descending, maximum 20 entries, including the evidence_url
needed for the final answer.

Stop when all open tickets matching the filter have been processed. Retry
transient failures at most 2 times. Do not repeat completed calls or perform
side-effecting actions. If a required result is still missing, return a clear
structured failure naming the ticket_id.

Use direct tool calls for the escalation decision on each candidate and for
posting any comment (requires confirmation).
</tool_orchestration>
```

## Assess the final answer, not just the program

The `program_output` item and the final assistant `message` are separate outputs. Test both. A program can return the correct records while the final message omits a required field, citation, or caveat.

Put the requirement in success criteria:

```text
# Success criteria
- The final answer includes every field from the program output that the user needs,
  plus the evidence_url for each claim.
```

## Benchmarking PTC

Compare direct and programmatic calling on the same representative tasks. Check whether the final response is correct, complete, and includes the required evidence. Then compare total tokens, latency, cost, calls, turns, and retries.

Count fewer calls, turns, or intermediate outputs as improvements **only when the final answer still passes your existing evals.** A cheaper wrong answer is a regression.

## Failure modes and fixes

| Symptom | Root cause | Fix |
|---------|-----------|-----|
| Program right, final answer wrong | Two outputs, one tested | Test both; add required evidence to success criteria |
| PTC used for judgment-dependent steps | Routing too broad | Bound the PTC stage; route judgment, approvals, final validation to direct calls |
| Model inspects results one by one instead of writing a program | Routing too vague, or return shapes undocumented | Task-specific orchestration block; document tool return fields |
| Program guesses at fields that don't exist | Tool descriptions missing return contracts | Document expected return fields, types, error behavior |
| Repeated or looping work across routes | No handoff defined | Define one handoff; instruct not to switch routes or repeat completed work |
| Side effects executed inside a program | Side-effecting tool opted into allowed_callers | Keep side-effecting tools direct-only; state "do not perform side-effecting actions" in the orchestration block |
| Citations lost | PTC used where native artifacts must survive | Keep citation-bearing work on direct calls |
