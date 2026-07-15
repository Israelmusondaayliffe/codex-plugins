# Output Patterns

Use these patterns when skills need to produce consistent, high-quality output.

## Template Pattern

Provide templates for output format. Match the level of strictness to your needs.

**For strict requirements (like API responses or data formats):**

```markdown
## Report Structure

ALWAYS use this exact template structure:

# [Analysis Title]

## Executive Summary
[One-paragraph overview of key findings]

## Key Findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```

**Why this works:** Eliminates format drift, ensures consistency, makes output predictable.

**Reliability:** Store template in `assets/` directory for reuse. Validate output against template structure.

**For flexible guidance (when adaptation is useful):**

```markdown
## Report Structure

Here is a sensible default format, but use your best judgment:

# [Analysis Title]

## Executive Summary
[Overview]

## Key Findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]

Adjust sections as needed for the specific analysis type.
```

**Why this works:** Provides structure while allowing creativity.

**When to choose:** Strict template when consistency critical (APIs, forms, structured data). Flexible template when adaptation needed (creative work, varied contexts).

## Examples Pattern

For skills where output quality depends on seeing examples, provide input/output pairs:

```markdown
## Commit Message Format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

Follow this style: type(scope): brief description, then detailed explanation.
```

**Why this works:** Examples communicate style and level of detail more clearly than descriptions alone.

**Reliability:** Multiple examples prevent edge case failures. Show variety of inputs/outputs.

**When to choose:** When quality is subjective but recognizable (writing style, code conventions, creative formats).

## Quality Criteria Pattern

When format is flexible but quality standards exist:

```markdown
## Output Quality Standards

All responses must meet these criteria:

**Mandatory:**
- Includes specific examples (not generic)
- Provides actionable steps (not vague suggestions)
- Cites sources when claiming facts
- Uses clear, concise language

**Validation:**
After generation, verify:
- [ ] Includes at least 2 concrete examples
- [ ] Every recommendation is actionable
- [ ] Claims are sourced or qualified
- [ ] No jargon without explanation
```

**Why this works:** Makes subjective quality objective and checkable.

**Reliability:** Create validation script that checks criteria programmatically where possible.

**When to choose:** When output format varies but quality standards consistent.

## Combining Patterns

**Template + Examples:** Provide structure (template) with quality guidance (examples)
**Template + Criteria:** Ensure format (template) and quality (criteria validation)
**Examples + Criteria:** Show style (examples) with standards (criteria checks)

**Example: Documentation Skill**
- Template for structure (sections, headings)
- Examples for writing style
- Criteria for quality (clarity, completeness, accuracy)
- Validation script checks for required sections

## Reliability in Output Patterns

**When format consistency matters:**
- Use strict templates (store in `assets/`)
- Validate output against template
- Consider using scripts to generate structure

**When quality matters:**
- Provide multiple diverse examples
- Define specific criteria
- Include validation checks
- Show both good and bad examples

**When both matter:**
- Combine patterns (template + examples + criteria)
- Use deterministic tools for structure
- Use LLM for content within structure
- Validate both format and quality

**Red flag:** Output format drifting over time → Add template or validation
**Red flag:** Quality inconsistent → Add examples and criteria
**Red flag:** Errors in structured output → Use script to generate structure
