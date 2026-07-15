# Long-Context and Compaction Patterns for GPT-5.6

GPT-5.6 carries forward the 1M token context window, native compaction, and the phase parameter. The 5.6 additions that touch long-context work: persisted reasoning (`reasoning.context`) for multi-turn continuity, and explicit caching economics that reward stable prompt prefixes. Lean prompting compounds here: repeated prompt content is amplified across every turn of a long session.

## 1M token context window

Up to 1M tokens in a single request: entire codebases, long document collections, extended agent trajectories.

**Pricing and rate limits:** verify current tiers against OpenAI documentation before deployment for cost-sensitive workloads. Prior generations priced and rate-limited requests differently above and below 272K tokens; confirm what applies to 5.6 rather than assuming.

## Long-context handling

For inputs longer than approximately 10k tokens, use these patterns to reduce "lost in the scroll" errors.

### Lean long-context pattern

```text
Role: An analyst working with a long document set.

# Goal
Answer the user's question with claims anchored to specific sections of the source.

# Success criteria
- Each factual claim is anchored to a named section, page, or clause.
- Constraints stated by the user (jurisdiction, date range, product, team) are respected.
- Fine details (dates, thresholds, clauses) are quoted or paraphrased rather than summarized away.
- The answer covers every part of the user's question.

# Approach
- Produce a short internal outline of the key sections relevant to the user's request.
- Re-state the user's constraints explicitly before answering.
- Anchor claims to sections ("In the 'Data Retention' section..."), not generic statements.
- Quote relevant language verbatim when fine details matter.

# Constraints
- Do not infer beyond what the source supports.
- If sources conflict, surface the conflict and attribute each side.
```

### Long context handling block (XML form)

```xml
<long_context_handling>
- For inputs longer than ~10k tokens (multi-chapter docs, long threads, multiple PDFs):
  - First, produce a short internal outline of the key sections relevant to the user's request
  - Re-state the user's constraints explicitly (e.g., jurisdiction, date range, product, team) before answering
  - In your answer, anchor claims to sections ("In the 'Data Retention' section...") rather than speaking generically
- If the answer depends on fine details (dates, thresholds, clauses), quote or paraphrase them
</long_context_handling>
```

### Document mapping

```xml
<document_mapping>
1. Identify key sections relevant to the query
2. Note section names/headers
3. Mark sections with critical details (dates, numbers, names)
4. Flag sections that may contain contradictory information
</document_mapping>
```

### Multi-document handling

```xml
<multi_document_handling>
- Process each document separately first
- Identify overlapping or contradictory information
- Cross-reference between documents
- Clearly attribute claims to specific documents
- Note when documents conflict
</multi_document_handling>
```

### Domain patterns

**Legal documents:**

```xml
<long_context_handling>
For legal documents:
1. Identify all parties and their roles
2. Map key dates (effective, termination, renewal)
3. Note jurisdiction and governing law
4. Outline key obligations by party
5. Flag any ambiguous or undefined terms

When answering:
- Cite specific clauses by number/name
- Quote relevant language verbatim
- Note any conflicting provisions
- Distinguish between mandatory and optional terms
</long_context_handling>
```

**Technical documentation:**

```xml
<long_context_handling>
For technical docs:
1. Map the document structure (chapters, sections)
2. Identify API endpoints or functions mentioned
3. Note version-specific information
4. Flag deprecated or upcoming features

When answering:
- Reference specific sections/pages
- Distinguish between versions when relevant
- Quote code examples verbatim
- Note prerequisites or dependencies
</long_context_handling>
```

**Meeting transcripts:**

```xml
<long_context_handling>
For meeting transcripts:
1. Identify all speakers
2. Map topics discussed chronologically
3. Note decisions made and by whom
4. Flag action items and owners

When answering:
- Attribute statements to specific speakers
- Note when topics recur
- Distinguish between suggestions and decisions
- Quote relevant exchanges when needed
</long_context_handling>
```

## Compaction

Compaction extends the effective context window beyond a single window's worth of tokens: long conversations persist across many turns, and agents run trajectories that exceed a typical window.

### When to use

**Use when:** multi-step agent flows with many tool calls; long conversations where earlier turns must be retained; iterative reasoning beyond the maximum window; tool-heavy workflows approaching context limits.

**Do not use when:** the conversation fits within standard context; every detail of prior turns must be preserved exactly; simple short interactions.

### Best practices

**When to trigger:** compact after major milestones, not continuously. Target approximately 75% of the context limit or after 50+ tool calls.

**Preserving critical info:** before compaction, ensure critical state is in the most recent turns:

```python
summary_message = {
    "role": "assistant",
    "content": f"""Critical state summary:
    - Current task: {current_task}
    - Completed steps: {completed_steps}
    - Pending actions: {pending_actions}
    - Key findings: {key_findings}"""
}
conversation.append(summary_message)
```

**After compaction:** treat compacted items as opaque state. Keep prompts functionally identical after compaction.

### Key properties

1. **Loss-aware:** compression preserves task-relevant information
2. **Encrypted:** output is opaque, cannot be inspected or modified
3. **Token-efficient:** dramatically reduces footprint
4. **Continuity:** the model maintains reasoning context
5. **ZDR compatible:** returns an encrypted content item
6. **Model-specific:** compacted state only works within the same model family; re-compact when moving between families

Verify the current compaction endpoint shape against OpenAI's Responses API documentation at implementation time.

## Persisted reasoning and long sessions (new for 5.6)

Persisted reasoning and compaction solve adjacent problems and compose:

- `reasoning.context: "all_turns"` keeps the model's reasoning available across turns, so it stops re-deriving context. Use it for any long session with stable goals. Continue with `previous_response_id`; under ZDR, request and replay `reasoning.encrypted_content`.
- Compaction compresses the transcript itself when it approaches the window.

A long-running agent typically wants both, plus phase on every intermediate update. Full mechanics: `references/caching-and-persisted-reasoning.md`.

## Caching and long-context economics (new for 5.6)

Long-context work is where 5.6's caching change bites hardest: a 200K-token document set written to cache costs 1.25x its uncached input rate. The read/write ratio decides:

- A document set queried many times across a session: explicit caching wins clearly.
- A one-shot analysis of a large corpus: caching the corpus is a pure loss; keep it uncached.
- Structure requests so the stable corpus sits before the volatile question, and place the breakpoint between them.

Track `cached_tokens` and `cache_write_tokens` to verify the config is earning its writes.

## Phase parameter (carried from 5.4/5.5)

- `phase: "commentary"` for intermediate updates
- `phase: "final_answer"` for the completed answer
- Do NOT add to user messages
- Preserve values exactly when replaying assistant history manually
- With `previous_response_id`, prior state is preserved automatically

Developer-message reminder when manually replaying:

```text
If manually replaying assistant items:
- Preserve assistant `phase` values exactly.
- Use `phase: "commentary"` for intermediate user-visible updates.
- Use `phase: "final_answer"` for the completed answer.
- Do not add `phase` to user messages.
```

## Uncertainty handling for long context

```xml
<uncertainty_and_ambiguity>
- If the question is ambiguous or underspecified:
  - Ask up to 1-3 precise clarifying questions, OR
  - Present 2-3 plausible interpretations with clearly labeled assumptions.
- When external facts may have changed and no tools available:
  - Answer in general terms and state details may have changed.
- Never fabricate exact figures, line numbers, or external references when uncertain.
- Prefer "Based on the provided context..." instead of absolute claims.
</uncertainty_and_ambiguity>
```

## High-risk self-check

For legal, financial, compliance, or safety-sensitive long-document analysis, the lean form as success criteria:

```text
# Success criteria
- No claim uses strong words ("always," "guaranteed") unless the source supports them.
- Assumptions are stated explicitly when present.
- Specific numbers and dates are anchored to source sections.
```

XML form for XML-structured prompts:

```xml
<high_risk_self_check>
Before finalizing an answer:
- Briefly re-scan your own answer for unstated assumptions, specific numbers or claims not grounded in context, and overly strong language.
- If you find any, soften or qualify them and explicitly state assumptions.
</high_risk_self_check>
```

## What changed from 5.5 for long context

| Aspect | 5.5 default | 5.6 default | Action |
|--------|-------------|-------------|--------|
| Context window | 1M | 1M | No change |
| Compaction | Native | Native | No change |
| Phase | Preserved | Preserved | No change |
| Multi-turn reasoning | CoT pass-through | reasoning.context all_turns | Adopt for stable-goal sessions |
| Caching | Automatic | Write billing 1.25x; explicit mode | Cache-first prompt structure; verify read/write ratio |
| Long-context blocks | Useful, often surgical | Same | Keep or move to lean form |
