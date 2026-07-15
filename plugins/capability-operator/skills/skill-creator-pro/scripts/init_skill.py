#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from tier-appropriate template

Usage:
    init_skill.py <skill-name> --path <path> [--tier <1|2|3>]

Examples:
    init_skill.py my-new-skill --path skills/public
    init_skill.py my-new-skill --path skills/public --tier 1
    init_skill.py data-processor --path skills/private --tier 2
    init_skill.py studio-production --path skills/private --tier 3
"""

import sys
from pathlib import Path


# ─── Tier 1: Simple Tasks ───────────────────────────────────────────────────

TIER1_SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: WHAT it does + WHEN to use it. Include specific trigger phrases, file types, domain terms. Max 1024 chars. No angle brackets.]
---

# {skill_title}

## Overview

[TODO: 1-2 sentences. What this skill enables. What problem it solves.]

## Instructions

[TODO: Clear workflow instructions. Use imperative form ("Extract text" not "You should extract text").

Key questions to answer:
- What does Claude do when this skill triggers?
- What's the step-by-step workflow?
- What references should Claude load and when?

Include concrete examples with realistic user requests.]

## Examples

[TODO: Show 2-3 realistic input/output pairs.

**Example 1:**
User says: "[realistic request]"
Action: [what the skill does]
Result: [expected output]
]

## Resources

### references/
[TODO: Domain knowledge, style guides, detailed documentation Claude should reference.
Load with: "Load references/[filename].md when [specific condition]."
Delete this directory if not needed.]
"""

TIER1_REFERENCE = """# Reference Documentation for {skill_title}

[TODO: Replace with domain knowledge, style guides, schemas, or detailed documentation.

This file is loaded into context only when needed, keeping SKILL.md lean.
Include table of contents if over 100 lines.]
"""


# ─── Tier 2: Complex Tasks ─────────────────────────────────────────────────

TIER2_SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: WHAT it does + WHEN to use it. Include specific trigger phrases, file types, domain terms. Mention reliability features (deterministic calculations, validation, error handling). Max 1024 chars. No angle brackets.]
---

# {skill_title}

## Overview

[TODO: 1-2 sentences. What this skill enables. What makes it reliable.]

## Workflow

[TODO: Choose workflow pattern. Options:

**Sequential:** Step 1 → Step 2 → Step 3 (clear order)
**Conditional:** IF condition → Path A, ELSE → Path B
**Iterative:** Generate → Validate → Refine → Repeat

For each step, specify:
- What happens (LLM reasoning vs script execution)
- What to validate before proceeding
- What could fail and how to recover]

### Step 1: [Action]

[TODO: Description. Reference scripts/references as needed.

Example:
Run `scripts/validate_input.py` to check data format.
If validation fails, report specific issues to user.]

### Step 2: [Action]

[TODO: Description. For accuracy-critical operations, use scripts.]

### Step 3: [Action]

[TODO: Description. Final validation before presenting results.]

## Error Handling

[TODO: Document common failure modes and recovery:
- What could go wrong at each step?
- What error messages should the user see?
- How to recover from failures?]

## Reliability Notes

[TODO: Document what's deterministic vs probabilistic:
- Scripts handle: [calculations, exact values, formatting]
- LLM handles: [interpretation, decisions, presentation]
- Validation at: [critical checkpoints]]

## Resources

### scripts/
[TODO: Executable code for deterministic operations.
- Scripts handle accuracy-critical operations
- Include error handling and meaningful error messages
- Test with happy path, edge cases, and error cases
Delete this directory if not needed.]

### references/
[TODO: Detailed documentation loaded into context as needed.
- API docs, schemas, complex domain rules
- Load with: "Load references/[filename].md when [condition]."
Delete this directory if not needed.]

### assets/
[TODO: Files used in outputs (templates, fonts, icons).
- Templates for consistent output format
- Not loaded into context, used in final output
Delete this directory if not needed.]
"""

TIER2_SCRIPT = '''#!/usr/bin/env python3
"""
[TODO: Script purpose] for {skill_name}

Replace this with actual implementation.
Scripts should handle accuracy-critical operations:
- Calculations and data transforms
- Exact value operations
- Format validation
- Consistent formatting

Include:
- Error handling with meaningful messages
- Edge case handling
- Docstrings explaining purpose
"""

import sys
import json


def main():
    """[TODO: Describe what this script does]"""
    # TODO: Implement actual logic
    # Example pattern:
    # 1. Parse input (args or stdin)
    # 2. Validate input
    # 3. Perform deterministic operation
    # 4. Validate output
    # 5. Return result

    print(json.dumps({{"status": "success", "message": "Replace with actual implementation"}}))


if __name__ == "__main__":
    main()
'''

TIER2_REFERENCE = """# Reference Documentation for {skill_title}

[TODO: Replace with detailed domain documentation.

This file is loaded into context only when needed.
Include table of contents if over 100 lines.

Good reference content:
- API documentation and examples
- Database schemas and field descriptions
- Complex business rules and edge cases
- Workflow deep-dives for specific scenarios]
"""

TIER2_ASSET = """[TODO: Replace with actual template file.

This is a placeholder for output templates.
Assets are used in final output, not loaded into context.

Examples:
- report_template.md (report structure)
- output_format.json (structured output schema)
- template.docx (Word document template)

Delete this file and replace with actual assets.]
"""


# ─── Tier 3: Multi-Step Agentic Tasks ──────────────────────────────────────

TIER3_SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: WHAT it does + WHEN to use it. Include specific trigger phrases for each phase. Mention multi-phase orchestration, routing, and key capabilities. Max 1024 chars. No angle brackets.]
---

# {skill_title}

## Overview

[TODO: 1-2 sentences. What this system enables. What phases exist and why.]

This skill operates as an **orchestrator**. It assesses requests and routes to the appropriate phase agent. Each phase agent is a focused instruction set in agents/.

## Router Logic

Assess the user's request and route to the appropriate phase:

[TODO: Define routing rules. Example:

**Phase 1 request** → Load `agents/agent-phase-1.md`
  Triggers: [specific user phrases, inputs, or conditions]

**Phase 2 request** → Load `agents/agent-phase-2.md`
  Triggers: [specific user phrases]
  Prerequisite: Phase 1 output exists and approved

**Phase 3 request** → Load `agents/agent-phase-3.md`
  Triggers: [specific user phrases]
  Prerequisite: Phase 2 output exists and approved

If request is ambiguous, ask user which phase they need.]

## Phase Handoff Protocol

Between phases, verify:
- Previous phase output exists and is valid
- User has approved previous phase output (if approval required)
- Required inputs for next phase are available

[TODO: Define specific handoff data for each transition.]

## Shared Resources

All phases reference:
[TODO: List shared knowledge base files.
- `references/[shared-knowledge].md` for [purpose]
- `assets/[shared-template]` for [purpose]]

## Error Recovery

If a phase fails, do not proceed to next phase.
Surface the error to user with:
- What failed and why
- Recovery options
- Whether to retry current phase or start over

## Resources

### agents/
Phase-specific sub-agent instruction sets (one per phase).
[TODO: List each agent file and its purpose.]

### references/
Shared knowledge base across all phases.
[TODO: List knowledge files and when to load them.]

### scripts/
Deterministic operations shared across phases.
[TODO: List scripts and when each phase uses them.]

### assets/
Templates and materials used across phases.
[TODO: List assets and which phases use them.]
"""

TIER3_AGENT = """# Agent: {phase_name}

## Scope

[TODO: What this agent handles. What it does NOT handle (route back to orchestrator).]

## Inputs

[TODO: What this agent expects from the orchestrator or previous phase.
- Required inputs
- Optional inputs
- Format of inputs]

## Workflow

[TODO: Step-by-step instructions for this phase.
Reference scripts and assets as needed.
Use imperative form.]

### Step 1: [Action]
[TODO: Description]

### Step 2: [Action]
[TODO: Description]

## Outputs

[TODO: What this agent produces for the orchestrator or next phase.
- Required outputs
- Format of outputs
- Where outputs are saved]

## Validation

[TODO: How to verify this phase's output before handoff.
- Quality criteria
- Validation script if applicable
- What constitutes a pass vs fail]

## Error Handling

[TODO: Phase-specific failure modes and recovery.
- Common errors
- Recovery actions
- When to escalate back to orchestrator]
"""

TIER3_SHARED_REF = """# Shared Knowledge: {skill_title}

[TODO: Knowledge base shared across all phases.

Examples:
- Brand guidelines and voice
- Platform specifications and constraints
- Domain rules that apply to every phase
- Glossary of terms

All phase agents reference this file.]
"""

TIER3_SCRIPT = '''#!/usr/bin/env python3
"""
[TODO: Script purpose] for {skill_name}

Shared deterministic operation used across phases.
Include error handling and meaningful messages.
"""

import sys
import json


def main():
    """[TODO: Describe what this script does]"""
    # TODO: Implement
    print(json.dumps({{"status": "success"}}))


if __name__ == "__main__":
    main()
'''


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path, tier=2):
    """
    Initialize a new skill directory with tier-appropriate template.

    Args:
        skill_name: Name of the skill (kebab-case)
        path: Path where the skill directory should be created
        tier: Skill tier (1, 2, or 3)

    Returns:
        Path to created skill directory, or None if error
    """
    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"Error: Skill directory already exists: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"Error creating directory: {e}")
        return None

    skill_title = title_case_skill_name(skill_name)

    # ── Tier 1 ──────────────────────────────────────────────────────────
    if tier == 1:
        skill_content = TIER1_SKILL_TEMPLATE.format(
            skill_name=skill_name, skill_title=skill_title
        )
        _write_file(skill_dir / 'SKILL.md', skill_content)

        refs_dir = skill_dir / 'references'
        refs_dir.mkdir(exist_ok=True)
        _write_file(
            refs_dir / 'domain-knowledge.md',
            TIER1_REFERENCE.format(skill_title=skill_title)
        )
        print("Initialized Tier 1 skill (instructions + references)")

    # ── Tier 2 ──────────────────────────────────────────────────────────
    elif tier == 2:
        skill_content = TIER2_SKILL_TEMPLATE.format(
            skill_name=skill_name, skill_title=skill_title
        )
        _write_file(skill_dir / 'SKILL.md', skill_content)

        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        script_path = scripts_dir / 'example_script.py'
        _write_file(script_path, TIER2_SCRIPT.format(skill_name=skill_name))
        script_path.chmod(0o755)

        refs_dir = skill_dir / 'references'
        refs_dir.mkdir(exist_ok=True)
        _write_file(
            refs_dir / 'domain-docs.md',
            TIER2_REFERENCE.format(skill_title=skill_title)
        )

        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        _write_file(assets_dir / 'template-placeholder.md', TIER2_ASSET)

        print("Initialized Tier 2 skill (instructions + scripts + references + assets)")

    # ── Tier 3 ──────────────────────────────────────────────────────────
    elif tier == 3:
        skill_content = TIER3_SKILL_TEMPLATE.format(
            skill_name=skill_name, skill_title=skill_title
        )
        _write_file(skill_dir / 'SKILL.md', skill_content)

        # Create agents/ for phase-specific sub-agents
        agents_dir = skill_dir / 'agents'
        agents_dir.mkdir(exist_ok=True)

        # Create 3 phase agent templates in agents/
        for i, phase in enumerate(["phase-1", "phase-2", "phase-3"], 1):
            phase_name = f"Phase {i}: [TODO: Name]"
            _write_file(
                agents_dir / f'agent-{phase}.md',
                TIER3_AGENT.format(phase_name=phase_name)
            )

        # Create references/ for shared knowledge (not agents)
        refs_dir = skill_dir / 'references'
        refs_dir.mkdir(exist_ok=True)

        # Shared knowledge base
        _write_file(
            refs_dir / 'shared-knowledge.md',
            TIER3_SHARED_REF.format(skill_title=skill_title)
        )

        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        script_path = scripts_dir / 'validate_output.py'
        _write_file(script_path, TIER3_SCRIPT.format(skill_name=skill_name))
        script_path.chmod(0o755)

        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        _write_file(assets_dir / 'template-placeholder.md', TIER2_ASSET)

        print("Initialized Tier 3 skill (orchestrator + agents + references + scripts + assets)")

    else:
        print(f"Error: Invalid tier {tier}. Must be 1, 2, or 3.")
        return None

    print(f"\nSkill '{skill_name}' initialized at {skill_dir} (Tier {tier})")
    print("\nNext steps:")
    print("1. Complete all TODO items in SKILL.md")
    print("2. Replace or delete placeholder files")
    if tier == 2:
        print("3. Implement scripts for accuracy-critical operations")
        print("4. Add templates to assets/ for consistent output")
    elif tier == 3:
        print("3. Define routing logic in SKILL.md")
        print("4. Write each sub-agent in agents/agent-*.md")
        print("5. Implement shared scripts")
    print(f"{3 if tier == 1 else 5 if tier == 2 else 6}. Run quick_validate.py before packaging")

    return skill_dir


def _write_file(path, content):
    """Write content to file, print confirmation."""
    path.write_text(content)
    rel = path.name
    print(f"  Created: {rel}")


def main():
    # Parse args
    args = sys.argv[1:]

    if len(args) < 3 or '--path' not in args:
        print("Usage: init_skill.py <skill-name> --path <path> [--tier <1|2|3>]")
        print("\nTiers:")
        print("  1 - Simple tasks (instructions + references)")
        print("  2 - Complex tasks (+ scripts + templates + validation) [default]")
        print("  3 - Agentic tasks (orchestrator + sub-agents + full stack)")
        print("\nExamples:")
        print("  init_skill.py prompt-gen --path skills/ --tier 1")
        print("  init_skill.py data-processor --path skills/ --tier 2")
        print("  init_skill.py studio-system --path skills/ --tier 3")
        sys.exit(1)

    skill_name = args[0]
    path_idx = args.index('--path')
    path = args[path_idx + 1]

    tier = 2  # default
    if '--tier' in args:
        tier_idx = args.index('--tier')
        try:
            tier = int(args[tier_idx + 1])
        except (IndexError, ValueError):
            print("Error: --tier requires a value of 1, 2, or 3")
            sys.exit(1)

    print(f"Initializing skill: {skill_name} (Tier {tier})")
    print(f"Location: {path}\n")

    result = init_skill(skill_name, path, tier)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
