# Tier Architecture Guide

Detailed implementation guidance for each skill tier. Load this when assessing tier during discovery or when designing Tier 3 orchestrator skills.

## Tier 1: Simple Tasks

### When to Use

- Single workflow path, minimal branching
- Claude's native intelligence handles decisions
- No accuracy-critical calculations
- Instructions + knowledge are sufficient
- Output quality depends on prompt quality, not determinism

### Implementation

The SKILL.md carries the full workload. Keep instructions clear and concise. References provide domain knowledge Claude doesn't have. Assets provide templates if output format matters.

**SKILL.md structure:**
```markdown
## Overview
Brief purpose statement.

## Instructions
Clear workflow. Explain WHY, not just WHAT.
Reference domain knowledge: "Load references/style-guide.md for brand voice."

## Examples
Show realistic input/output pairs.
```

### Example: Prompt Generation Skill

```
prompt-generator/
├── SKILL.md              # Workflow: analyze request → select framework → generate prompts
├── references/
│   └── frameworks.md     # 7 prompt frameworks with examples
└── assets/
    └── template.md       # Output format template
```

The SKILL.md contains the generation logic. References hold the framework library. No scripts needed because output quality is creative, not mathematical.

### Anti-Patterns for Tier 1

- Adding scripts when none are needed (over-engineering)
- Putting all domain knowledge in SKILL.md instead of references (bloated context)
- Missing trigger phrases in description (undertriggering)
- Instructions too vague ("make it good" vs showing examples of good)

---

## Tier 2: Complex Tasks

### When to Use

- Multiple operation types (read, create, edit)
- Some operations must be exact (calculations, data transforms, formatting)
- Validation needed at critical points
- Output feeds downstream systems or is user-facing
- Consistent formatting required across uses

### Implementation

SKILL.md orchestrates the workflow. Scripts handle deterministic operations. References hold complex domain documentation. Assets hold templates for consistent output. Validation scripts verify correctness at critical checkpoints.

**SKILL.md structure:**
```markdown
## Overview
Purpose + reliability approach.

## Workflow
### Step 1: [Action]
LLM determines approach. Load references/schema.md if needed.

### Step 2: [Deterministic Operation]
Run scripts/process.py. Validate output.

### Step 3: [Presentation]
Format results. Apply template from assets/.

## Error Handling
Common failures and recovery.

## Reliability Notes
What's deterministic vs probabilistic.
```

### The Hybrid Pattern (Recommended)

1. **LLM orchestrates:** Reads requirements, makes decisions, plans approach
2. **Scripts execute:** Calculations, data transforms, exact operations
3. **LLM presents:** Formats results, adds narrative, explains context
4. **Scripts validate:** Verify output correctness, check completeness

### Example: Data Processing Skill

```
data-processor/
├── SKILL.md                # Workflow with decision tree for data types
├── scripts/
│   ├── clean_data.py       # Deterministic cleaning
│   ├── transform.py        # Exact transformations
│   ├── validate_input.py   # Input schema validation
│   └── validate_output.py  # Output verification
├── references/
│   ├── schema.md           # Data schema documentation
│   └── transform-rules.md  # Complex transformation rules
└── assets/
    └── report-template.md  # Output format template
```

### Anti-Patterns for Tier 2

- Using LLM for calculations instead of scripts (accuracy risk)
- No validation at critical points (silent failures)
- Scripts without error handling (crashes instead of graceful failure)
- Duplicating content between SKILL.md and references (token waste)
- Missing edge case handling discovered in Step 1

---

## Tier 3: Multi-Step Agentic Tasks

### When to Use

- Multiple distinct phases requiring different approaches
- Routing logic needed (different requests go to different workflows)
- Multi-MCP coordination across services
- Complex enough that a single instruction set becomes unwieldy
- Sub-tasks are independently testable

### The Orchestrator Pattern

SKILL.md is the **router**, not the worker. It:

1. Assesses the incoming request
2. Determines which phase or sub-agent handles it
3. Loads the appropriate sub-agent from agents/
4. Manages handoffs between phases
5. Maintains state across phases

**Critical principle:** Each sub-agent is a focused, self-contained instruction set. It knows its scope, its inputs, its outputs, and when to hand back to the orchestrator. Agents live in `agents/` because they are behavioral instructions, not passive knowledge. References in `references/` are knowledge that agents and the orchestrator both draw from.

### Orchestrator SKILL.md Structure

```markdown
## Overview
System purpose. What phases exist and why.

## Router Logic

Assess the user's request against these categories:

**[Phase A] request** → Load `agents/agent-phase-a.md`
  Triggers: [specific user phrases, inputs, or conditions]

**[Phase B] request** → Load `agents/agent-phase-b.md`
  Triggers: [specific user phrases, inputs, or conditions]
  Prerequisite: Phase A output exists

**[Phase C] request** → Load `agents/agent-phase-c.md`
  Triggers: [specific user phrases, inputs, or conditions]
  Prerequisite: Phase B output approved

If request is ambiguous, ask user which phase they need.

## Phase Handoff Protocol

Between phases, verify:
- Previous phase output exists and is valid
- User has approved previous phase output (if approval required)
- Required inputs for next phase are available

## Shared Resources

All phases reference:
- `references/brand-guidelines.md` for voice and style
- `references/platform-specs.md` for technical constraints

## Error Recovery

If a phase fails, do not proceed to next phase.
Surface the error to user with recovery options.
```

### Sub-Agent Structure

Each sub-agent in agents/ follows this pattern:

```markdown
# Agent: [Phase Name]

## Scope
What this agent handles. What it does NOT handle (route back to orchestrator).

## Inputs
What this agent expects from the orchestrator or previous phase.

## Workflow
Step-by-step instructions for this phase.
Reference scripts and assets as needed.

## Outputs
What this agent produces for the orchestrator or next phase.

## Validation
How to verify this phase's output before handoff.

## Error Handling
Phase-specific failure modes and recovery.
```

### Example: Production Studio Skill

```
studio-production/
├── SKILL.md                        # Orchestrator/Router
├── agents/
│   ├── agent-creative-brief.md     # Phase 1: Brief creation
│   ├── agent-image-production.md   # Phase 2: Image generation
│   ├── agent-review-qa.md          # Phase 3: Quality review
│   └── agent-publish.md            # Phase 4: Publishing
├── references/
│   ├── brand-guidelines.md         # Shared: brand voice/style
│   └── platform-specs.md           # Shared: platform requirements
├── assets/
│   ├── brief-template.md           # Template for creative briefs
│   ├── review-checklist.md         # QA checklist template
│   └── publish-formats.json        # Platform format specs
└── scripts/
    ├── validate_brief.py           # Validates brief completeness
    ├── validate_output.py          # Validates production output specs
    └── format_for_platform.py      # Formats output per platform
```

The orchestrator SKILL.md for this example:

```markdown
## Router Logic

**"Create a brief" / "New project" / "Start from scratch"**
→ Load agents/agent-creative-brief.md
→ Use assets/brief-template.md

**"Generate images" / "Produce the shots" / "Run production"**
→ Verify: brief exists and approved
→ Load agents/agent-image-production.md

**"Review" / "QA" / "Check quality"**
→ Verify: production output exists
→ Load agents/agent-review-qa.md
→ Use assets/review-checklist.md

**"Publish" / "Post" / "Go live"**
→ Verify: review approved
→ Load agents/agent-publish.md
→ Run scripts/format_for_platform.py
```

### Multi-MCP Coordination in Tier 3

When a skill coordinates across multiple MCP servers, structure phases around service boundaries:

```markdown
### Phase 1: Design Export (Figma MCP)
1. Export design assets
2. Generate specifications
3. Create asset manifest

### Phase 2: Asset Storage (Drive MCP)
1. Create project folder
2. Upload all assets
3. Generate shareable links

### Phase 3: Task Creation (Linear MCP)
1. Create development tasks
2. Attach asset links from Phase 2
3. Assign to team

### Phase 4: Notification (Slack MCP)
1. Post handoff summary
2. Include asset links and task references
```

Key techniques: clear phase separation, data passing between MCPs, validation before moving to next phase, centralized error handling.

### Anti-Patterns for Tier 3

- Putting all instructions in SKILL.md instead of sub-agents (defeats the router purpose, context bloat)
- Putting agents in references/ instead of agents/ (muddies the distinction between behavioral instructions and passive knowledge)
- Sub-agents that overlap in scope (ambiguous routing)
- No handoff validation (broken chain, invalid inputs to next phase)
- Missing fallback for ambiguous requests (user gets stuck)
- Sub-agents that reference each other directly instead of going through the orchestrator (spaghetti routing)
- Over-engineering. If you only have 2 phases and no routing ambiguity, Tier 2 is sufficient

---

## Tier Assessment Checklist

Answer these questions after discovery to determine tier:

1. **How many distinct workflow paths exist?**
   - One → Tier 1
   - Multiple operations, single orchestration → Tier 2
   - Multiple phases with routing → Tier 3

2. **Do any operations require deterministic accuracy?**
   - No → Tier 1 candidate
   - Yes → Tier 2 minimum

3. **Does the skill need to route between different sub-workflows?**
   - No → Tier 1 or 2
   - Yes → Tier 3

4. **Does it coordinate across multiple MCP servers?**
   - No → Tier 1 or 2
   - Yes, simple sequence → Tier 2
   - Yes, complex with phases → Tier 3

5. **Would the SKILL.md exceed 500 lines if all instructions were inline?**
   - No → Tier 1 or 2
   - Yes, due to multiple distinct workflows → Tier 3

**Default to Tier 2 when uncertain.** Upgrade to Tier 3 only when routing logic and phase separation provide clear value.
