# Trigger Optimization

Guide for writing skill descriptions that effectively trigger when users need them.

## How Skill Matching Works

Claude sees `name` and `description` from all skills. When a user makes a request, skills trigger based on:
1. Semantic match between query and description
2. Keyword overlap
3. Context clues (file types, domain terms, task verbs)

**Critical:** If key terms from user queries don't appear in description, skill won't trigger.

## Core Principles

### 1. Include Explicit Keywords

**User says:** "Help me with this DOCX file"  
**Description must contain:** "docx", "Word", "document", ".docx files"

**User says:** "Make a MidJourney prompt"  
**Description must contain:** "MidJourney", "prompt", "image generation"

### 2. Specify Use Cases

Don't just describe what it does - describe WHEN to use it.

**Template:**
```
[What it does]. Use when [scenario 1], [scenario 2], or [scenario 3].
```

**Example:**
```yaml
description: Process expense reports with deterministic calculations and validation. Use when handling expense reports, reimbursements, or financial data requiring exact totals.
```

### 3. Include Action Verbs

Users express intent with verbs. Include variations:

**Creation:** create, build, make, generate, design
**Modification:** edit, modify, update, change, revise
**Analysis:** analyze, review, examine, evaluate
**Transformation:** convert, transform, export, migrate

**Example:**
```yaml
description: Creates PowerPoint presentations (.pptx) with layouts and speaker notes. Use when creating, building, designing, or generating presentations or slide decks.
```

### 4. Mention Reliability Features (If Applicable)

If skill has reliability features, mention them:

```yaml
description: Process data with deterministic calculations, validation, and error handling. Use when data accuracy critical, calculations must be exact, or outputs feed downstream systems.
```

**Keywords for reliability:** deterministic, validation, accuracy, exact, consistent format, error handling

## Formula for Effective Descriptions

```
[PRIMARY FUNCTION] + [SPECIFIC TOOL/FORMAT] + [KEY FEATURES]. 
Use when [SCENARIO 1], [SCENARIO 2], or [SCENARIO 3]. 
[OPTIONAL: Reliability features if applicable]
```

**Example:**
```yaml
description: Generate production-ready prompts for MidJourney v7 with cinematic direction and technical parameters. Use when requesting MidJourney prompts, image generation for photography/fashion/architecture, or visual concepts for creative projects. Includes structured approach and parameter optimization.
```

## Common Mistakes

**Mistake:** Too generic
```yaml
❌ description: Helps with documents
```

**Fix:** Be specific
```yaml
✅ description: Creates and edits Word documents (.docx) with formatting, tracked changes, and comments. Use for .docx files, Word documents, or document editing tasks.
```

**Mistake:** Missing use cases
```yaml
❌ description: Generates image prompts for AI models
```

**Fix:** Specify when
```yaml
✅ description: Generates prompts for MidJourney v7. Use when requesting MidJourney prompts, image generation, or visuals for photography, fashion, or art projects.
```

**Mistake:** Buried key terms
```yaml
❌ description: A comprehensive solution that facilitates the creation of prompts suitable for utilization with MidJourney
```

**Fix:** Lead with key terms
```yaml
✅ description: Generate prompts for MidJourney v7...
```

## Testing Your Description

Ask:
1. **Would user query match this description?**
   - Test with realistic user queries
   - Check if key terms present

2. **Is this differentiated from other skills?**
   - How is it unique?
   - What makes it trigger vs others?

3. **Are all key terms included?**
   - File extensions
   - Tool names
   - Action verbs
   - Domain terms

## Guidelines

**Length:** 75-150 words optimal (comprehensive but focused)

**Structure:** What + When + (optional) How

**Voice:** Third-person ("This skill should be used when..." not "Use this when...")

**Focus:** High-signal terms, not verbose explanations

**Include:**
- Exact file extensions (.docx, .pdf, .pptx)
- Specific tool names (MidJourney v7, GPT-5, BigQuery)
- Action verbs users will say
- Use case scenarios
- Reliability features if applicable

**Avoid:**
- Generic terms without specifics
- Technical jargon users won't say
- Buried key terms in verbose phrasing
- No use cases or scenarios

## Examples

**Good description (file format skill):**
```yaml
description: Creates and edits Word documents (.docx files) with formatting, tracked changes, and comments. Use when working with .docx files, Microsoft Word documents, or document editing tasks requiring format preservation.
```

**Good description (tool-specific skill):**
```yaml
description: Generate production-ready prompts for GPT-5 based on OpenAI's official prompting guide. Use when requesting GPT-5 prompts, ChatGPT instructions, system prompts, API calls, or optimizing GPT-5 behavior for agentic workflows or coding tasks.
```

**Good description (data processing skill):**
```yaml
description: Process data pipelines with deterministic calculations, validation, and error handling. Use when handling data transformations, ETL workflows, or data processing requiring exact calculations and format consistency. Scripts ensure accuracy, validation catches errors early.
```

**Why these work:**
- Specific file types/tools mentioned
- Action verbs included
- Use cases explicit
- Key terms users will say
- Reliability features mentioned where relevant

## Quick Check

Before finalizing description:
- [ ] Includes file extensions or tool names
- [ ] Includes action verbs users will use
- [ ] Specifies when to use (scenarios)
- [ ] Mentions key features
- [ ] Differentiates from similar skills
- [ ] 75-150 words
- [ ] Third-person voice

If any missing → revise description

## Remember

**Goal:** Make skill trigger when needed, not trigger when not needed.

**Balance:** Specific enough to be useful, broad enough to catch variations.

**Test:** Think of 5 ways users might ask for this, does description match them?

---

## Automated Description Optimization (Claude Code Only)

For skills where triggering accuracy matters, use the automated pipeline. This requires `claude -p` (available in Claude Code and Cowork, not Claude.ai).

### Step 1: Generate Trigger Eval Queries

Create 20 eval queries. Mix of should-trigger and should-not-trigger. Save as JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

Queries must be realistic. Include file paths, personal context, casual speech, abbreviations, typos. Mix of lengths. Focus on edge cases rather than clear-cut examples.

**Bad examples:** `"Format this data"`, `"Extract text from PDF"`, `"Create a chart"`

**Good examples:** `"ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit margin as a percentage. The revenue is in column C and costs are in column D i think"`

**For should-trigger queries (8-10):** Different phrasings of same intent, some formal, some casual. Cases where user doesn't name the skill but clearly needs it. Uncommon use cases. Cases where this skill competes with another but should win.

**For should-not-trigger queries (8-10):** Near-misses sharing keywords but needing something different. Adjacent domains. Ambiguous phrasing where naive keyword matching would fire but shouldn't. Don't make them obviously irrelevant. "Write a fibonacci function" as a negative for a PDF skill is too easy.

### Step 2: Review With User

Present the eval set for the user to review. Use the HTML template in `assets/eval_review.html`:

1. Read the template
2. Replace placeholders:
   - `__EVAL_DATA_PLACEHOLDER__` with the JSON array (no quotes, it's a JS variable assignment)
   - `__SKILL_NAME_PLACEHOLDER__` with the skill name
   - `__SKILL_DESCRIPTION_PLACEHOLDER__` with current description
3. Write to temp file and open
4. User edits queries, toggles should-trigger, adds/removes entries, clicks "Export Eval Set"
5. File downloads to `~/Downloads/eval_set.json`

This step matters. Bad eval queries lead to bad descriptions.

### Step 3: Run the Optimization Loop

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Use the model ID from your system prompt so the triggering test matches the user's actual experience.

The loop:
1. Splits eval set into 60% train, 40% held-out test
2. Evaluates current description (3 runs per query for reliability)
3. Calls Claude to propose improvements based on failures
4. Re-evaluates new description on both train and test
5. Iterates up to 5 times
6. Selects by test score (not train) to avoid overfitting
7. Produces HTML report and returns JSON with `best_description`

While it runs, periodically tail output to give the user updates.

### Step 4: Apply the Result

Take `best_description` from JSON output and update the skill's SKILL.md frontmatter. Show user before/after and report scores.

### How Skill Triggering Works

Understanding the mechanism helps design better eval queries. Skills appear in Claude's `available_skills` list with name + description. Claude decides whether to consult based on that description.

Important: Claude only consults skills for tasks it can't easily handle alone. Simple, one-step queries like "read this PDF" may not trigger even if description matches perfectly, because Claude handles them directly. Complex, multi-step, or specialized queries reliably trigger when description matches.

Eval queries should be substantive enough that Claude would benefit from consulting a skill. Simple queries are poor test cases.
