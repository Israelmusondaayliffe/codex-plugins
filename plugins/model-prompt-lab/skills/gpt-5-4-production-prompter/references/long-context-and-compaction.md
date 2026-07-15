# Long-Context and Compaction Patterns for GPT-5.4

GPT-5.4 supports up to a 1M token context window and is the first mainline model trained to support compaction natively.

## 1M Token Context Window

GPT-5.4 supports up to 1M tokens in a single request. This enables:
- Analyzing entire codebases
- Long document collections
- Extended agent trajectories

**Pricing note:** Separate pricing for requests under 272K and over 272K tokens. Priority processing requests above 272K tokens are automatically processed at standard rates.

**Rate limits:** Different limits for under and over 272K tokens.

## Long-Context Handling

For inputs longer than approximately 10k tokens, use these patterns to reduce "lost in the scroll" errors.

### Core Long-Context Spec

```xml
<long_context_handling>
- For inputs longer than ~10k tokens (multi-chapter docs, long threads, multiple PDFs):
  - First, produce a short internal outline of the key sections relevant to the user's request
  - Re-state the user's constraints explicitly (e.g., jurisdiction, date range, product, team) before answering
  - In your answer, anchor claims to sections ("In the 'Data Retention' section...") rather than speaking generically
- If the answer depends on fine details (dates, thresholds, clauses), quote or paraphrase them
</long_context_handling>
```

### Document Mapping

```xml
<document_mapping>
1. Identify key sections relevant to the query
2. Note section names/headers
3. Mark sections with critical details (dates, numbers, names)
4. Flag sections that may contain contradictory information
</document_mapping>
```

### Multi-Document Handling

```xml
<multi_document_handling>
- Process each document separately first
- Identify overlapping or contradictory information
- Cross-reference between documents
- Clearly attribute claims to specific documents
- Note when documents conflict
</multi_document_handling>
```

### Legal Document Pattern

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

### Technical Documentation Pattern

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

### Meeting Transcript Pattern

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

Compaction unlocks significantly longer effective context windows. User conversations can persist for many turns without hitting context limits, and agents can perform very long trajectories that exceed a typical context window.

### When to Use Compaction

**Use when:**
- Multi-step agent flows with many tool calls
- Long conversations where earlier turns must be retained
- Iterative reasoning beyond the maximum context window
- Tool-heavy workflows approaching context limits

**Do NOT use when:**
- Conversation fits within standard context
- Every detail of prior turns must be preserved exactly
- Simple, short interactions

### API Endpoint

```
POST https://api.openai.com/v1/responses/compact
```

### Basic Usage

```python
from openai import OpenAI
client = OpenAI()

# After many turns/tool calls, when approaching context limits:
compacted = client.responses.compact(
    model="gpt-5.4",
    conversation_id="conv_abc123"
)

# Continue workflow with compacted state
response = client.responses.create(
    model="gpt-5.4",
    input=[
        {"role": "developer", "content": "[Your system prompt]"},
        {"role": "assistant", "content": compacted.state},
        {"role": "user", "content": "[New user message]"}
    ]
)
```

### Best Practices

**When to trigger:** Compact after major milestones, not continuously. Target approximately 75% of context limit or after 50+ tool calls.

**Preserving critical info:** Before compaction, ensure critical information is in the most recent turns.

```python
# Summarize critical state before compacting
summary_message = {
    "role": "assistant",
    "content": f"""Critical state summary:
    - Current task: {current_task}
    - Completed steps: {completed_steps}
    - Pending actions: {pending_actions}
    - Key findings: {key_findings}"""
}
conversation.append(summary_message)
compacted = client.responses.compact(...)
```

**After compaction:** Treat compacted items as opaque state. Keep prompts functionally identical after compaction.

### Key Properties

1. **Loss-aware:** Compression preserves task-relevant information
2. **Encrypted:** Output is opaque, cannot be inspected or modified
3. **Token-efficient:** Dramatically reduces footprint
4. **Continuity:** Model maintains reasoning context
5. **ZDR compatible:** Returns encrypted_content item
6. **Model-specific:** Compacted state only works with same model family

### Long-Running Agent Pattern

```python
class LongRunningAgent:
    def __init__(self):
        self.conversation = []
        self.compaction_count = 0
    
    def run(self, task):
        self.conversation.append({"role": "user", "content": task})
        
        while not self.is_complete():
            response = self.execute_step()
            self.conversation.append(response)
            
            if self.should_compact():
                self.compact_conversation()
            
            if response.tool_calls:
                self.process_tools(response.tool_calls)
    
    def should_compact(self):
        token_count = count_tokens(self.conversation)
        return token_count > MAX_CONTEXT * 0.75
    
    def compact_conversation(self):
        compacted = client.responses.compact(
            model="gpt-5.4",
            conversation=self.conversation
        )
        self.conversation = [
            {"role": "assistant", "content": compacted.state}
        ]
        self.compaction_count += 1
```

## Phase Parameter Details

The `phase` field helps in long-running or tool-heavy flows where preambles or intermediate assistant updates might be mistaken for the final answer.

See `references/api-parameters.md` for full phase parameter documentation.

**Quick summary:**
- `phase: "commentary"` for intermediate updates
- `phase: "final_answer"` for completed answer
- Do NOT add to user messages
- Preserve when replaying assistant history
- Missing or dropped phase can cause preambles to be treated as final answers

## Uncertainty Handling

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

## High-Risk Self-Check

For legal, financial, compliance, or safety-sensitive long-document analysis:

```xml
<high_risk_self_check>
Before finalizing an answer:
- Briefly re-scan your own answer for:
  - Unstated assumptions,
  - Specific numbers or claims not grounded in context,
  - Overly strong language ("always," "guaranteed," etc.).
- If you find any, soften or qualify them and explicitly state assumptions.
</high_risk_self_check>
```
