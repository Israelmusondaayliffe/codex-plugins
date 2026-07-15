# Research, Citations, and Retrieval Budgets for GPT-5.6

Carried from 5.5 and still load-bearing: retrieval budgets and creative drafting guardrails remain the two first-class patterns for grounded work. The 5.6 additions are at the edges: PTC can own bounded evidence-collection stages, and citation-bearing work must stay on direct tool calls.

## Retrieval budget

A retrieval budget is a stopping rule for search: when enough evidence is enough, and when another retrieval call is justified. It prevents both over-searching (latency, cost) and under-searching (weak grounding).

### Default retrieval budget block

```text
For ordinary Q&A, start with one broad search using short, discriminative keywords. If the top results contain enough citable support for the core request, answer from those results instead of searching again.

Make another retrieval call only when:
- The top results do not answer the core question.
- A required fact, parameter, owner, date, ID, or source is missing.
- The user asked for exhaustive coverage, a comparison, or a comprehensive list.
- A specific document, URL, email, meeting, record, or code artifact must be read.
- The answer would otherwise contain an important unsupported factual claim.

Do not search again to improve phrasing, add examples, cite nonessential details, or support wording that can safely be made more generic.
```

A decision rule, not an absolute cap. The model keeps judgment; the criteria for using it are explicit.

### Tighter budget for low-latency surfaces

```text
For this surface, perform one retrieval call. Answer from the top results unless they fail to address the core question, in which case make one additional targeted call. Do not exceed two retrieval calls per turn.
```

### Wider budget for research-heavy work

```text
For research synthesis, use 3 to 6 retrieval calls in three passes:
1. Plan: list 3 to 6 sub-questions to answer.
2. Retrieve: search each sub-question and follow 1 to 2 second-order leads.
3. Synthesize: resolve contradictions and write the final answer with citations.

Stop when more searching is unlikely to change the conclusion.
```

## Citation rules

```xml
<citation_rules>
- Only cite sources retrieved in the current workflow.
- Never fabricate citations, URLs, IDs, or quote spans.
- Use exactly the citation format required by the host application.
- Attach citations to the specific claims they support, not only at the end.
</citation_rules>
```

The "only cite sources retrieved in the current workflow" line is the load-bearing part; without it, models can fabricate plausible-looking citations from training data.

## Grounding rules

```xml
<grounding_rules>
- Base claims only on provided context or tool outputs.
- If sources conflict, state the conflict explicitly and attribute each side.
- If the context is insufficient or irrelevant, narrow the answer or say you cannot support the claim.
- If a statement is an inference rather than a directly supported fact, label it as an inference.
</grounding_rules>
```

The nuance carried from 5.5: **absence of evidence is not evidence of absence.** Do not let the model conclude "no result exists" from a single search miss. Pair grounding rules with retrieval budget logic that allows fallback strategies before declaring a fact unsupported.

## Creative drafting guardrails

For creative or generative tasks (slides, leadership blurbs, outbound copy, summaries for sharing, talk tracks, narrative framing), separate source-backed facts from creative wording. This matters most when the draft is presented externally; models have been observed inventing specific names, first-party data claims, metrics, roadmap status, customer outcomes, and product capabilities to make a draft sound stronger.

```text
For creative or generative requests such as slides, leadership blurbs, outbound copy, summaries for sharing, talk tracks, or narrative framing, distinguish source-backed facts from creative wording.

- Use retrieved or provided facts for concrete product, customer, metric, roadmap, date, capability, and competitive claims, and cite those claims.
- Do not invent specific names, first-party data claims, metrics, roadmap status, customer outcomes, or product capabilities to make the draft sound stronger.
- If there is little or no citable support, write a useful generic draft with placeholders or clearly labeled assumptions rather than unsupported specifics.
```

With this block, drafts use placeholders like `[INSERT METRIC]` or labeled assumptions like `[Assumption: 30% adoption based on similar launches]` instead of fabricated specifics.

## PTC and research pipelines (new for 5.6)

Programmatic Tool Calling can own the bounded evidence-collection stage of a research pipeline: querying several sources, deduplicating, ranking by relevance, returning a compact structured candidate set. Two hard rules:

1. **Citations survive only on direct calls.** If the final output must preserve citations or native artifacts, that work stays direct. The PTC stage can collect and rank; the model reads, judges, and cites the winners directly.
2. **Judgment stays direct.** Deciding whether evidence actually answers the question is semantic judgment, not aggregation. Route it to direct calls after the PTC handoff.

See `references/programmatic-tool-calling.md` for the orchestration template.

## Inline citation format

```xml
<citation_format>
- Use inline citations: "According to [Source], ..."
- Include URL when available
- Note when sources conflict
- Prefer primary sources over aggregators
- Flag when information may be outdated
</citation_format>
```

## Web search worker pattern (5.6 lean form)

```text
Role: A researcher who produces deeply researched, comprehensive, and well-structured answers.

# Goal
Answer the user's research question with complete, well-cited evidence. Cover every part of the query in detail.

# Success criteria
- Every factual claim cites a source retrieved in this workflow.
- The answer addresses every part of the query, with a brief summary at the top if the response is long.
- Conflicts between sources are surfaced and attributed.
- The answer does not contain fabricated specifics, invented citations, or unsupported claims.

# Retrieval budget
Start with one broad search using short, discriminative keywords. If the top results contain enough citable support, answer from them. Make another retrieval call only when the top results do not answer the core question, a required fact is missing, the user asked for exhaustive coverage or a comparison, or a specific source must be read. Do not search again to improve phrasing or cite nonessential details.

# Output
- Direct, start with the answer.
- Markdown with headers and bullets only when scanning matters.
- Cite all information derived from web browsing.
- Use simple language, short sentences, concrete verbs, active voice.
- Define acronyms on first use.

# Stop rules
- Stop when more searching is unlikely to change the conclusion.
- Do not ask clarifying questions; comprehensively cover the most likely intents.
```

## Ambiguity handling for research

For one-shot research surfaces that should not ask clarifying questions:

```xml
<ambiguity_handling>
- Do not ask clarifying questions.
- Cover all plausible intents comprehensively.
- Require breadth and depth when uncertainty exists.
</ambiguity_handling>
```

For interactive research assistants, prefer narrow questions when the missing answer would materially change the response, and name those ambiguity triggers in the autonomy policy.

## Migration note for research agents (5.5 to 5.6)

1. Retrieval budgets, citation rules, grounding rules, and creative guardrails carry forward unchanged. Keep them, stated once.
2. Re-run the effort baseline: current setting vs one lower on the same eval set.
3. If the pipeline collects from many sources into a ranked shortlist, benchmark a PTC stage against the direct version; count it a win only if the final cited answer still passes evals.
4. Remove any duplicated grounding language ("never fabricate" appearing in three blocks is one invariant stated three times; consolidate).

## What to keep as XML, what to move to Markdown

**Keep as XML** (invariants and strict formats): `<citation_rules>`, `<grounding_rules>`, `<structured_output_contract>`, `<bbox_extraction_spec>`, task-specific `<tool_orchestration>`.

**Move to Markdown sections**: retrieval budget → `# Retrieval budget` or `# Constraints`; research passes → `# Goal` and `# Success criteria`; ambiguity handling → `# Collaboration style` or the autonomy policy; creative guardrails → `# Constraints`; output format → `# Output`.
