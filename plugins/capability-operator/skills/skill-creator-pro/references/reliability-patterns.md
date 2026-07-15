# Reliability Patterns

Patterns for creating skills that "just work" through appropriate architecture choices, validation, and error handling.

## Core Insight

LLMs are probabilistic. When accuracy, consistency, or reliability matters, offset with deterministic tools.

## Pattern 1: Deterministic-First

**When to use:**
- Calculations required (math, aggregations, metrics)
- Exact values needed (form filling, data entry, structured generation)
- Consistent formatting required (templates, structured output)
- Operations are repeatable (same code each time)
- Errors are costly (production use, user-facing outputs)

**Architecture:**
```markdown
## Workflow

1. **LLM: Orchestrate** (determine what needs to be done)
   - Read requirements
   - Make decisions about approach
   - Plan operations

2. **Script: Execute** (perform accurate operations)
   - Calculate exact values
   - Fill precise data
   - Format consistently

3. **LLM: Present** (format results, add context)
   - Interpret results
   - Add narrative
   - Format for user
```

**Example: PDF Form Filling**
- LLM reads form structure and determines field mappings
- Script (`fill_form.py`) fills fields with exact values
- Script validates field data types and constraints
- LLM formats confirmation message

**Implementation:**
- Create script for accuracy-critical operation
- Document when to use script vs LLM
- Test script with edge cases from discovery
- Add validation to verify script output

**Signals from discovery:**
- "Must be exact"
- "Calculations"
- "No mistakes allowed"
- "Accuracy critical"
- "Downstream dependencies"

## Pattern 2: Validation-Heavy

**When to use:**
- Errors are costly (financial, legal, user-facing)
- Downstream dependencies exist (output feeds other systems)
- Data quality critical (analytics, compliance, reporting)
- Format requirements strict (APIs, integrations)

**Architecture:**
```markdown
## Workflow with Validation

1. **Validate Input**
   - Check schema (script: validate_input.py)
   - Verify constraints
   - Catch issues early

2. **Process**
   - Execute operation (LLM or script depending on need)
   - Maintain intermediate state

3. **Validate Output**
   - Check format (script: validate_output.py)
   - Verify completeness
   - Ensure consistency

4. **Error Handling**
   - If validation fails, log specific issue
   - Provide recovery options
   - Don't proceed with invalid data
```

**Example: Data Pipeline**
- Validate input schema before processing
- Transform data
- Validate output schema after transformation
- Validate aggregations are mathematically correct
- If any validation fails, stop and report specific issue

**Implementation:**
- Create validation scripts for critical checkpoints
- Define clear pass/fail criteria
- Log validation failures with specifics
- Provide recovery guidance in SKILL.md

**Signals from discovery:**
- "What if this is wrong?"
- "Downstream systems depend on this"
- "Users will see this"
- "Can't have errors"
- "Must be perfect"

## Pattern 3: Template-Driven

**When to use:**
- Format consistency critical (reports, forms, structured docs)
- Structure is standard (established patterns, required sections)
- Quality through constraints (reduce variability, ensure completeness)
- Reusable patterns (same structure, different content)

**Architecture:**
```markdown
## Workflow with Templates

1. **Load Template**
   - Use template from assets/ directory
   - Understand required sections/fields

2. **Fill Template**
   - LLM generates content for each section
   - Scripts handle structured data portions
   - Maintain template structure

3. **Validate Against Template**
   - Verify all required sections present
   - Check format matches template
   - Ensure no drift from structure
```

**Example: Report Generation**
- Load report template from `assets/report_template.docx`
- Fill executive summary (LLM)
- Fill metrics table (script with calculations)
- Fill recommendations (LLM based on data)
- Validate all sections present and formatted correctly

**Implementation:**
- Store templates in `assets/` directory
- Document required vs optional sections
- Create validation script to check template compliance
- Show example of filled template in SKILL.md

**Signals from discovery:**
- "Must match this format"
- "Consistent structure needed"
- "Standard template"
- "Same sections every time"
- "Format keeps drifting"

## Pattern 4: Error-Aware

**When to use:**
- Production use (live systems, real users)
- Complex workflows (many steps, many failure points)
- External dependencies (APIs, databases, file systems)
- Irreversible actions (deletions, payments, submissions)

**Architecture:**
```markdown
## Workflow with Error Handling

1. **Anticipate Failure Modes**
   - What could go wrong at each step?
   - What are common failure scenarios?

2. **Implement Error Handling**
   - Try-catch blocks in scripts
   - Validation at each step
   - Clear error messages

3. **Provide Recovery**
   - Fallback mechanisms
   - Retry logic where appropriate
   - Clear guidance on what to do when errors occur

4. **Document Limitations**
   - Known edge cases that aren't handled
   - Situations where manual intervention needed
   - What errors mean and how to recover
```

**Example: API Integration**
- Anticipate: rate limits, timeouts, malformed responses, authentication failures
- Handle: retry with exponential backoff for transient failures
- Validate: response format matches expected schema
- Fallback: cache last successful response
- Document: known rate limits and how to handle them

**Implementation:**
- List failure modes in SKILL.md
- Add error handling to scripts
- Create fallback mechanisms
- Document recovery procedures
- Test failure scenarios

**Signals from discovery:**
- "What if the API is down?"
- "This is production"
- "Users can't see errors"
- "Must be reliable"
- "Depends on external systems"

## Pattern 5: Hybrid Orchestration

**When to use:**
- Complex tasks requiring both accuracy and flexibility
- Some parts need determinism, others need creativity
- Balance between structure and adaptability
- Most professional/production skills

**Architecture:**
```markdown
## Hybrid Workflow

1. **LLM: Understand and Decide**
   - Read requirements
   - Interpret context
   - Make high-level decisions
   - Plan approach

2. **Scripts: Execute Critical Operations**
   - Calculations (deterministic math)
   - Data transformations (exact operations)
   - Validations (format checks)
   - Structure generation (consistent output)

3. **LLM: Connect and Present**
   - Generate narrative content
   - Explain results
   - Add context and interpretation
   - Format for user comprehension

4. **Scripts: Final Validation**
   - Verify output correctness
   - Check completeness
   - Ensure consistency
```

**Example: Expense Report Processing**
- LLM reads receipts and understands context
- LLM categorizes expenses (requires judgment)
- Script calculates totals (must be exact)
- Script validates amounts match receipts (must be exact)
- Script converts currencies if needed (must be exact)
- LLM generates narrative summary
- LLM flags anomalies based on patterns
- Script does final validation of report format
- LLM formats final report with context

**This is the recommended pattern for most professional skills.**

**Implementation:**
- Identify what needs determinism (scripts)
- Identify what needs flexibility (LLM)
- Create clear handoffs between LLM and scripts
- Document which parts are deterministic vs probabilistic
- Validate at boundaries

## Choosing the Right Pattern

**High-stakes + accuracy needs:**
→ Deterministic-First + Validation-Heavy
Example: Financial calculations, data processing

**User-facing outputs:**
→ Template-Driven + Validation-Heavy
Example: Reports, forms, structured documents

**Production systems:**
→ Error-Aware + Validation-Heavy + Deterministic-First
Example: API integrations, data pipelines, automated workflows

**Creative with structure:**
→ Template-Driven + Hybrid Orchestration
Example: Content generation with consistent format

**Complex professional tasks:**
→ Hybrid Orchestration + Validation-Heavy + Error-Aware
Example: Most real-world business processes

## Implementation Checklist

When implementing reliability patterns:

**For all patterns:**
- [ ] Identify what must be deterministic vs flexible
- [ ] Document reliability approach in SKILL.md
- [ ] Test with edge cases from discovery

**For Deterministic-First:**
- [ ] Create scripts for accuracy-critical operations
- [ ] Test scripts thoroughly with edge cases
- [ ] Document when to use scripts vs LLM

**For Validation-Heavy:**
- [ ] Add validation at critical checkpoints
- [ ] Define clear pass/fail criteria
- [ ] Provide specific error messages

**For Template-Driven:**
- [ ] Store templates in assets/ directory
- [ ] Validate output against template
- [ ] Document required sections

**For Error-Aware:**
- [ ] List anticipated failure modes
- [ ] Implement error handling in scripts
- [ ] Document recovery procedures

**For Hybrid:**
- [ ] Clearly delineate LLM vs script responsibilities
- [ ] Validate at handoff points
- [ ] Test full workflow end-to-end

## Common Failure Modes and Solutions

**Problem:** LLM produces inconsistent calculations
**Solution:** Use Deterministic-First pattern - script handles math

**Problem:** Output format keeps drifting
**Solution:** Use Template-Driven pattern - validate against template

**Problem:** Errors surface late in workflow
**Solution:** Use Validation-Heavy pattern - validate at each step

**Problem:** Production failures with no recovery
**Solution:** Use Error-Aware pattern - handle failures gracefully

**Problem:** Either too rigid or too variable
**Solution:** Use Hybrid pattern - balance structure and flexibility

## Testing Reliability Patterns

**Test scenarios:**
1. **Happy path** - Does it work when everything is normal?
2. **Edge cases** - Does it handle unusual inputs from discovery?
3. **Failure modes** - Does it handle anticipated failures?
4. **Validation** - Do validation steps catch problems?
5. **Recovery** - Can it recover from errors?

**For each pattern, verify:**
- Deterministic parts are truly deterministic
- Validation catches intended issues
- Error handling works as expected
- Documentation matches implementation
- Edge cases from discovery are handled

## Remember

**Skills with "meat" that "just work":**
- Anticipate where probabilistic LLM behavior causes problems
- Use deterministic tools (scripts) when accuracy matters
- Validate outputs at critical points
- Handle errors gracefully with recovery options
- Document what's reliable vs what's approximate
- Test edge cases thoroughly
- Don't assume - validate

**The goal:** Skills that users can depend on, that handle edge cases, that don't break in production, that produce consistent results when consistency matters, and that fail gracefully when things go wrong.
