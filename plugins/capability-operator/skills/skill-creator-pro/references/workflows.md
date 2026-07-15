# Workflow Patterns

Patterns for organizing skill instructions and processes. Based on Anthropic's proven patterns, enhanced with reliability considerations and tier awareness.

## Pattern 1: Sequential Orchestration

For multi-step processes in a specific order.

```markdown
## Workflow: [Process Name]

### Step 1: [Action]
Call MCP tool or run script.
Parameters: [what's needed]
Validation: [what to check]

### Step 2: [Action]
Depends on: Step 1 output
Call MCP tool or run script.

### Step 3: [Action]
Depends on: Step 2 output
Final validation before completion.
```

**Key techniques:** Explicit step ordering. Dependencies between steps. Validation at each stage. Rollback instructions for failures.

**Tier fit:** Tier 2 for single-service sequences. Tier 3 when phases are distinct enough to warrant sub-agents.

**Reliability:** Use scripts for accuracy-critical steps. Use LLM for interpretation and presentation steps.

## Pattern 2: Multi-MCP Coordination

For workflows spanning multiple services.

```markdown
### Phase 1: [Service A] (MCP A)
1. [Operation]
2. [Operation]
3. Create output manifest for Phase 2

### Phase 2: [Service B] (MCP B)
1. Receive manifest from Phase 1
2. [Operation]
3. Generate links for Phase 3

### Phase 3: [Service C] (MCP C)
1. Receive links from Phase 2
2. [Operation]
3. Confirm completion

### Phase 4: [Notification Service] (MCP D)
1. Aggregate results from all phases
2. Post summary
```

**Key techniques:** Clear phase separation by service. Data passing between MCPs. Validation before moving to next phase. Centralized error handling. If any phase fails, do not proceed.

**Tier fit:** Tier 3 when phases are complex enough to warrant sub-agents. Tier 2 when MCP calls are straightforward sequences.

## Pattern 3: Iterative Refinement

For output quality that improves with feedback loops.

```markdown
## Iterative Process

### Initial Draft
1. Fetch data (MCP or script)
2. Generate first draft (LLM)
3. Save to temporary file

### Quality Check
Run validation:
1. Check against quality criteria (script or checklist)
2. Identify issues (missing sections, formatting, data errors)

### Refinement Loop
1. Address each identified issue
2. Regenerate affected sections
3. Re-validate
4. Repeat until quality threshold met OR max iterations reached

### Finalization
1. Apply final formatting (template or script)
2. Generate summary
3. Save final version
```

**Key techniques:** Explicit quality criteria. Validation between iterations (script preferred). Clear stopping condition (threshold met or max iterations). Logging of what changed each iteration.

**Tier fit:** Tier 2. Tier 3 if refinement involves routing to different specialists.

## Pattern 4: Context-Aware Tool Selection

For when the same outcome requires different tools depending on context.

```markdown
## Decision Tree

1. Assess input characteristics:
   - File type and size
   - Source and destination
   - User requirements

2. Route to appropriate handler:
   **IF** [condition A] → Use [Tool/Script A]
   **ELSE IF** [condition B] → Use [Tool/Script B]
   **ELSE IF** [condition C] → Use [Tool/Script C]
   **ELSE** → Default handler with explanation

3. Execute with chosen tool

4. Explain to user why that approach was chosen
```

**Key techniques:** Clear decision criteria. Fallback options. Transparency about choices (tell user why this tool was selected). Test each branch independently.

**Tier fit:** Tier 2 for simple routing. Tier 3 when branches lead to substantially different workflows.

## Pattern 5: Domain-Specific Intelligence

For skills that add specialized knowledge beyond just tool access.

```markdown
## Domain Logic

### Before Operation (Domain Check)
1. Fetch relevant data (MCP or input)
2. Apply domain rules:
   - [Domain-specific validation]
   - [Domain-specific risk assessment]
   - [Domain-specific constraints]
3. Document domain decision

### Operation
IF domain checks passed:
  - Proceed with operation
  - Apply domain best practices
ELSE:
  - Flag for review
  - Explain domain-specific concerns

### Audit
- Log all domain checks performed
- Record decisions and rationale
- Surface any domain-specific warnings
```

**Key techniques:** Domain expertise embedded in logic (in references/ for complex rules). Compliance or quality checks before action. Comprehensive documentation of decisions. Domain knowledge stored in references/, not SKILL.md.

**Tier fit:** Tier 2 minimum. Tier 3 if domain rules are complex enough to warrant separate sub-agents per domain area.

## Conditional Workflows

For tasks with branching logic:

```markdown
## Workflow Decision Tree

1. Determine the operation type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow:
   - Generate structure (LLM determines layout)
   - Fill content (templates for consistency)
   - Validate output (script)

3. Editing workflow:
   - Load existing content (script reads file)
   - Apply modifications (LLM or script per operation)
   - Preserve integrity (validation script)
```

**Reliability:** Make decision criteria explicit. When accuracy matters in any branch, use deterministic tools.

## Choosing Workflow Patterns

**Single ordered process** → Sequential Orchestration
**Multiple services** → Multi-MCP Coordination
**Quality-sensitive output** → Iterative Refinement
**Multiple valid approaches** → Context-Aware Tool Selection
**Specialized knowledge required** → Domain-Specific Intelligence
**Input-dependent branching** → Conditional Workflow

**Combining patterns:** Complex skills often combine patterns. A Tier 3 skill might use Multi-MCP Coordination as its overall structure, with Iterative Refinement within individual phases, and Domain-Specific Intelligence informing routing decisions.

## Reliability in Workflows

For each step in any workflow, ask:
- Must this be exact? → Use script
- Must format be consistent? → Use template
- Could this fail? → Add validation
- Is output critical? → Add verification step

**The pattern that applies everywhere:** LLM orchestrates (decides what to do). Scripts execute (does it deterministically). Validation verifies (checks it's correct).
