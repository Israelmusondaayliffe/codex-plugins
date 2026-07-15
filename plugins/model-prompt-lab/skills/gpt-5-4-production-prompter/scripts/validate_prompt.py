#!/usr/bin/env python3
"""
Validate a GPT-5.4 prompt against production requirements.

Usage:
    python validate_prompt.py <prompt_file>
    python validate_prompt.py --text "<prompt_text>"

Checks:
- XML tag balance
- Required blocks for task type
- Reasoning effort appropriateness
- Model string correctness
- Deprecated patterns
- Phase parameter presence for multi-step
"""

import sys
import re
import json
import argparse


def check_xml_balance(text):
    """Check that all XML-style tags are properly opened and closed."""
    issues = []
    open_tags = re.findall(r'<(\w[\w_-]*)(?:\s[^>]*)?>(?!</)', text)
    close_tags = re.findall(r'</(\w[\w_-]*)>', text)
    self_closing = re.findall(r'<(\w[\w_-]*)\s*/>', text)

    open_counts = {}
    for tag in open_tags:
        if tag not in [t for t in self_closing]:
            open_counts[tag] = open_counts.get(tag, 0) + 1

    close_counts = {}
    for tag in close_tags:
        close_counts[tag] = close_counts.get(tag, 0) + 1

    for tag in set(list(open_counts.keys()) + list(close_counts.keys())):
        o = open_counts.get(tag, 0)
        c = close_counts.get(tag, 0)
        if o > c:
            issues.append(f"FAIL: Tag <{tag}> opened {o} time(s) but closed {c} time(s)")
        elif c > o:
            issues.append(f"FAIL: Tag </{tag}> closed {c} time(s) but opened {o} time(s)")

    return issues


def check_model_string(text):
    """Check for correct model string usage."""
    issues = []
    deprecated = ["gpt-5-2", "gpt-5-1", "gpt-5-0", "gpt-5.0", "gpt-5.1", "gpt-5.2", "gpt-5.3"]
    for dep in deprecated:
        if dep in text.lower():
            issues.append(f"WARN: Found deprecated model string '{dep}'. Should be 'gpt-5.4' or variant.")

    if "gpt-5.4" not in text.lower() and "gpt-5-4" not in text.lower():
        issues.append("WARN: No GPT-5.4 model string found. Confirm this is a 5.4 prompt.")

    return issues


def check_reasoning_effort(text):
    """Check reasoning effort configuration."""
    issues = []
    effort_match = re.search(r'reasoning.*?effort.*?["\'](\w+)["\']', text, re.IGNORECASE)
    if effort_match:
        effort = effort_match.group(1).lower()
        valid = ["none", "low", "medium", "high", "xhigh"]
        if effort not in valid:
            issues.append(f"FAIL: Invalid reasoning effort '{effort}'. Valid: {valid}")
    return issues


def check_deprecated_patterns(text):
    """Check for patterns from older models that should be updated."""
    issues = []
    deprecated_patterns = {
        "design_and_scope_constraints": "Consider using output_contract instead (5.4 is more thorough, may need less constraint)",
        "solution_persistence": "Consider using autonomy_and_persistence instead (5.4 naming)",
        "output_verbosity_spec": "Consider using output_contract and verbosity_controls instead (5.4 naming)",
    }
    for pattern, note in deprecated_patterns.items():
        if pattern in text:
            issues.append(f"INFO: Found '{pattern}'. {note}")

    return issues


def check_recommended_blocks(text):
    """Check for recommended blocks based on detected task type."""
    issues = []
    text_lower = text.lower()

    # Detect task type and check for recommended blocks
    if any(w in text_lower for w in ["tool", "function", "search", "fetch", "api call"]):
        if "tool_persistence_rules" not in text and "dependency_checks" not in text:
            issues.append("WARN: Tool-using prompt without tool_persistence_rules or dependency_checks. "
                          "GPT-5.4 can be less reliable at tool routing early in session.")

    if any(w in text_lower for w in ["research", "search", "browse", "web"]):
        if "citation_rules" not in text:
            issues.append("WARN: Research prompt without citation_rules. Citations may drift.")
        if "grounding_rules" not in text:
            issues.append("WARN: Research prompt without grounding_rules. Claims may lack grounding.")

    if any(w in text_lower for w in ["extract", "json", "schema", "parse"]):
        if "structured_output_contract" not in text and "extraction_spec" not in text:
            issues.append("WARN: Extraction prompt without structured_output_contract or extraction_spec.")

    if any(w in text_lower for w in ["refund", "cancel", "delete", "production", "deploy"]):
        if "verification_loop" not in text and "action_safety" not in text:
            issues.append("WARN: High-impact action prompt without verification_loop or action_safety.")

    if any(w in text_lower for w in ["batch", "list", "all items", "paginated", "every"]):
        if "completeness_contract" not in text:
            issues.append("WARN: Batch/list prompt without completeness_contract. May stop at partial coverage.")

    return issues


def check_phase_parameter(text):
    """Check for phase parameter awareness in multi-step prompts."""
    issues = []
    text_lower = text.lower()
    is_multistep = any(w in text_lower for w in [
        "multi-step", "multi_step", "tool call", "agent", "workflow",
        "preamble", "commentary", "long-running"
    ])
    if is_multistep and "phase" not in text_lower:
        issues.append("INFO: Multi-step prompt without phase parameter mention. "
                       "Consider adding phase handling to prevent preamble-as-final-answer issues.")

    return issues


def validate_prompt(text):
    """Run all validation checks."""
    all_issues = []
    all_issues.extend(check_xml_balance(text))
    all_issues.extend(check_model_string(text))
    all_issues.extend(check_reasoning_effort(text))
    all_issues.extend(check_deprecated_patterns(text))
    all_issues.extend(check_recommended_blocks(text))
    all_issues.extend(check_phase_parameter(text))

    fails = [i for i in all_issues if i.startswith("FAIL")]
    warns = [i for i in all_issues if i.startswith("WARN")]
    infos = [i for i in all_issues if i.startswith("INFO")]

    return {
        "passed": len(fails) == 0,
        "fails": fails,
        "warnings": warns,
        "info": infos,
        "total_issues": len(all_issues)
    }


def main():
    parser = argparse.ArgumentParser(description="Validate GPT-5.4 prompt")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("file", nargs="?", help="Path to prompt file")
    group.add_argument("--text", help="Prompt text directly")
    args = parser.parse_args()

    if args.text:
        text = args.text
    else:
        with open(args.file, "r") as f:
            text = f.read()

    result = validate_prompt(text)

    print(f"\n{'=' * 50}")
    print(f"GPT-5.4 Prompt Validation")
    print(f"{'=' * 50}")
    print(f"Status: {'PASS' if result['passed'] else 'FAIL'}")
    print(f"Issues: {result['total_issues']}")

    if result["fails"]:
        print(f"\nFAILURES ({len(result['fails'])}):")
        for f in result["fails"]:
            print(f"  {f}")

    if result["warnings"]:
        print(f"\nWARNINGS ({len(result['warnings'])}):")
        for w in result["warnings"]:
            print(f"  {w}")

    if result["info"]:
        print(f"\nINFO ({len(result['info'])}):")
        for i in result["info"]:
            print(f"  {i}")

    if not result["fails"] and not result["warnings"]:
        print("\nAll checks passed.")

    print(f"{'=' * 50}\n")

    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
