# Delivery Template

Standard output format for all GPT-5.6 prompt deliveries.

## Format

```
## GPT-5.6 [Use Case] Prompt

### Context Type
[ChatGPT / API Responses / GPT Builder / System]

### Model Configuration
- Model: [gpt-5.6-sol / gpt-5.6-terra / gpt-5.6-luna / gpt-5.6 alias]
- Reasoning effort: [none / low / medium / high / xhigh / max] (compare one level lower on representative tasks)
- Reasoning mode: [standard / pro, and why]
- Reasoning context: [auto / all_turns / current_turn, and why]
- Verbosity: [low / medium / high]
- Caching: [implicit / explicit breakpoints, and what sits before the breakpoint]
- Phase parameter: [yes / no, and why]
- safety_identifier: [required for end-user apps / n/a]

### Prompt

[The complete, copy-pasteable prompt formatted for the context type. Lean Markdown body by default. XML blocks only when they earn their place. Every instruction stated once.]

### Structure Applied
- Role: [one-line summary]
- # Goal: [one-line user-visible outcome]
- # Success criteria: [what must be true before final answer]
- # Constraints: [policy, evidence, side-effect limits]
- # Autonomy: [what is safe without asking / what requires confirmation / named ambiguity triggers, or omitted and why]
- # Output: [length, format, must-include contract if short]
- # Stop rules: [when to retry, abstain, ask, or stop]
- # Personality / # Collaboration style: [steady / expressive / omitted, and why]

### XML Blocks Applied (if any)
- [List each block with the measured failure mode or invariant it addresses]
- Example: "<tool_orchestration> - PTC routing for the bounded collection stage"
- Example: "<citation_rules> - invariant against fabricated citations"
- If none: "None. The lean body covers the requirements."

### 5.6-Specific Patterns Applied
- Autonomy policy: [yes / no, and rationale]
- Must-include contract for short answers: [yes / no, and rationale]
- Execution-mode routing (direct / PTC / pro / multi-agent): [route chosen, and rationale]
- Persisted reasoning: [yes / no, and rationale]
- Caching review: [what was decided]
- Retrieval budget: [yes / no, and rationale]
- Creative drafting guardrail: [yes / no, and rationale]
- Preamble pattern: [yes / no, and rationale]
- Validation by running: [yes / no, and rationale]

### Customization Notes
- [What the user can change without breaking the prompt]
- [Which sections to add or remove for different scenarios]
- [Effort adjustments for different task shapes, including the one-lower comparison]

### Validation Results
- [Output of validate_prompt.py or manual checklist]
```

## For Migration Deliveries, Add

```
### Migration Path
- Source model: [model]
- Target model: [gpt-5.6-sol / -terra / -luna]
- Reasoning effort: [baseline kept / dropped one level after comparison; xhigh vs max result if relevant]
- API change: [Chat Completions -> Responses, if applicable]
- Caching change: [prompt_cache_retention -> prompt_cache_options.ttl; implicit -> explicit; what to track]
- Persisted reasoning: [reasoning.context setting adopted, and why]

### Lean Log (one entry per removal group, each eval-verified)
- Removed: [instructions, examples, or tools taken out, with the weakness each was compensating for]
- Consolidated: [duplicated instructions merged into one statement, with prior locations]
- Converted: [ALWAYS/NEVER on judgment calls rewritten as decision rules]
- Re-tested brevity: ["be concise" style instructions removed or kept, with the eval result]
- Kept: [invariants retained, stated once]

### Additions
- [5.6 patterns added: autonomy policy, must-include contract, tool_orchestration, pro mode, persisted reasoning]

### Rollback
- Revert model string to [source model]
- Revert reasoning effort to [original]
- Restore [list of removed groups], if needed
```

## For Troubleshooting Deliveries, Add

```
### Diagnosis
- Symptom: [what the user reported]
- Category: [TOO_BRIEF / APPROVAL_NOISE / APPROVAL_GAP / PTC_FINAL_ANSWER / PTC_MISROUTE / PTC_ROUTING_VAGUE / CACHE_COST / PERSISTED_REASONING / PRO_MODE_MISUSE / SAFEGUARD_FRICTION / OVER_PROMPTING / RETRIEVAL_DRIFT / HALLUCINATED_SPECIFICS / VERBOSITY / SCOPE / etc.]
- Root cause: [why 5.6 exhibits this behavior]
- Duplication check run before adding anything: [yes / no, and what was found]

### Fix Applied
- [Specific change made, copy-pasteable. Consolidation and removal first, addition only if needed.]

### Test Scenario
- [How to verify the fix works, with a specific input that should now produce different output. For PTC fixes: test program_output and the final message separately.]

### If This Doesn't Fix It
- [Next diagnostic step]
- [Alternative fix to try]
```
