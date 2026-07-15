#!/usr/bin/env python3
"""
Validate a Claude Fable 5 prompt against production requirements.

Usage:
    python validate_prompt.py <prompt_file>
    python validate_prompt.py --text "<prompt_text>"

Checks (derived from the official Fable 5 prompting guide):
- FAIL: budget_tokens / extended thinking config (Fable 5 is adaptive thinking only)
- FAIL: reasoning-echo instructions (trigger the reasoning_extraction refusal classifier)
- FAIL: deprecated/wrong model strings when a model string is present
- WARN: remaining-token countdown patterns without the reassurance line
- WARN: over-prescription (enumerated behavior lists, ALWAYS/NEVER/MUST density)
- WARN: legacy anti-laziness residue from 4.x-era prompts
- WARN: forced interim-summary scaffolding
- INFO: autonomous-run prompts missing progress grounding
- INFO: send_to_user tool referenced without elicitation language
- INFO: XML tag balance when XML is used
"""

import sys
import re
import argparse


def check_thinking_budget(text):
    issues = []
    if re.search(r'budget_tokens', text):
        issues.append(
            "FAIL: 'budget_tokens' found. Fable 5 supports adaptive thinking only; "
            "extended thinking budgets do not exist. Remove the config."
        )
    if re.search(r'"type"\s*:\s*"enabled"', text) and 'thinking' in text:
        issues.append(
            "WARN: extended-thinking style config detected. Fable 5 uses adaptive "
            "thinking; verify the thinking config against current docs."
        )
    return issues


REASONING_ECHO_PATTERNS = [
    r'show\s+your\s+(?:thinking|reasoning|thought\s+process)',
    r'explain\s+your\s+(?:internal\s+)?reasoning\s+in\s+(?:your|the)\s+(?:response|answer|output)',
    r'(?:echo|transcribe|reproduce)\s+your\s+(?:thinking|reasoning|thought\s+process)',
    r'walk\s+(?:me|us|the\s+user)\s+through\s+your\s+(?:internal\s+)?(?:thinking|thought\s+process)\s+in\s+(?:your|the)\s+(?:response|answer)',
    r'think\s+out\s+loud\s+in\s+your\s+(?:response|answer|final)',
    r'include\s+your\s+(?:chain\s+of\s+thought|reasoning\s+trace)',
    r'reflect\s+on\s+your\s+reasoning\s+and\s+(?:write|include|output)',
]


def check_reasoning_echo(text):
    issues = []
    lower = text.lower()
    for pat in REASONING_ECHO_PATTERNS:
        m = re.search(pat, lower)
        if m:
            issues.append(
                f"FAIL: possible reasoning-echo instruction: '...{m.group(0)}...'. "
                f"Instructions to reproduce internal reasoning as response text can "
                f"trigger the reasoning_extraction refusal classifier on Fable 5, "
                f"causing fallbacks to Opus 4.8. Use structured thinking blocks or a "
                f"send_to_user tool instead."
            )
    return issues


def check_model_string(text):
    issues = []
    # Only meaningful when a model string appears at all
    has_model_field = re.search(r'model\s*[=:]\s*["\']', text)
    if not has_model_field:
        return issues
    if re.search(r'claude-fable-5', text):
        pass
    elif re.search(r'claude-(opus|sonnet|haiku)-\d', text):
        issues.append(
            "WARN: prompt/config targets a non-Fable model string. If this is the "
            "Opus 4.8 fallback config, fine; if it's the primary model, update to "
            "'claude-fable-5'."
        )
    if re.search(r'claude-fable-5[.\-]\d', text):
        issues.append(
            "WARN: versioned Fable string detected. The documented string is "
            "'claude-fable-5'; confirm any dated/versioned variant against current docs."
        )
    return issues


def check_context_countdown(text):
    issues = []
    countdown = re.search(
        r'(remaining\s+(?:context|tokens)|tokens?\s+(?:left|remaining)|context\s+budget)',
        text, re.IGNORECASE
    )
    reassurance = re.search(r'ample\s+context\s+remaining', text, re.IGNORECASE)
    if countdown and not reassurance:
        issues.append(
            "WARN: prompt appears to surface a context/token countdown without the "
            "reassurance line. Countdown displays trigger Fable 5's rare "
            "summarize/hand-off behavior. Hide the countdown, or add: 'You have ample "
            "context remaining. Do not stop, summarize, or suggest a new session on "
            "account of context limits.'"
        )
    return issues


def check_over_prescription(text):
    issues = []
    always = len(re.findall(r'\bALWAYS\b', text))
    never = len(re.findall(r'\bNEVER\b', text))
    must = len(re.findall(r'\bMUST\b', text))
    total = always + never + must
    if total > 6:
        issues.append(
            f"WARN: {always} ALWAYS, {never} NEVER, {must} MUST (all-caps) found. "
            f"Fable 5's instruction following makes plain statements sufficient; "
            f"heavy emphasis is prior-model scaffolding and can degrade output. "
            f"Try subtraction first."
        )
    # Enumerated don't-lists: many consecutive "Do not / Don't" lines
    dont_lines = re.findall(r'^\s*[-*]?\s*(?:Do not|Don\'t|Never)\b', text, re.MULTILINE)
    if len(dont_lines) > 8:
        issues.append(
            f"WARN: {len(dont_lines)} prohibition lines found. On Fable 5, one brief "
            f"instruction usually steers the whole behavior class. Consider collapsing "
            f"enumerated lists per the guide's 'Strong instruction following' section."
        )
    return issues


LEGACY_PATTERNS = [
    (r'be\s+thorough\s+and\s+do\s+not\s+stop', "anti-laziness residue (4.5/4.6 era)"),
    (r'do\s+not\s+stop\s+(?:early|until)', "anti-laziness residue (4.5/4.6 era)"),
    (r'complete\s+ALL\s+items', "anti-laziness residue"),
    (r'(?:after|every)\s+(?:each|\d+)\s+tool\s+calls?,?\s+(?:summarize|provide\s+a\s+summary)',
     "forced interim-summary scaffolding (4.6 era; Fable 5 updates well by default)"),
    (r'CRITICAL:\s*You\s+MUST', "aggressive emphasis (prior-model scaffolding)"),
    (r'spawn\s+multiple\s+subagents\s+in\s+the\s+same\s+turn',
     "4.7-era subagent pressure (Fable 5 delegates readily; keep only when-appropriate guidance)"),
]


def check_legacy_residue(text):
    issues = []
    for pat, label in LEGACY_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            issues.append(
                f"WARN: legacy pattern detected ({label}). Deprune candidate per the "
                f"migration playbook: remove and re-test."
            )
    return issues


def check_autonomous_grounding(text):
    issues = []
    autonomous = re.search(r'operating\s+autonomously|autonomous(?:ly)?\b|unattended|long[-\s]running',
                           text, re.IGNORECASE)
    grounding = re.search(r'audit\s+each\s+claim\s+against\s+a\s+tool\s+result', text, re.IGNORECASE)
    if autonomous and not grounding and len(text) > 600:
        issues.append(
            "INFO: prompt appears autonomous/long-running but lacks the "
            "evidence-grounded progress instruction. That snippet nearly eliminated "
            "fabricated status reports in Anthropic testing. Strongly consider adding it."
        )
    return issues


def check_send_to_user_pairing(text):
    issues = []
    if 'send_to_user' in text:
        elicitation = re.search(r'call\s+the\s+send_to_user\s+tool', text, re.IGNORECASE)
        if not elicitation:
            issues.append(
                "INFO: send_to_user referenced without elicitation language. Fable 5 "
                "rarely calls the tool from the definition alone; pair it with the "
                "'Between tool calls, when you have content the user must read "
                "verbatim...' instruction."
            )
    return issues


def check_xml_balance(text):
    issues = []
    open_tags = re.findall(r'<(\w[\w_-]*)(?:\s[^>]*)?>', text)
    close_tags = re.findall(r'</(\w[\w_-]*)>', text)
    self_closing = set(re.findall(r'<(\w[\w_-]*)\s*/>', text))
    open_counts = {}
    for t in open_tags:
        if t not in self_closing:
            open_counts[t] = open_counts.get(t, 0) + 1
    close_counts = {}
    for t in close_tags:
        close_counts[t] = close_counts.get(t, 0) + 1
    for t in set(list(open_counts) + list(close_counts)):
        o, c = open_counts.get(t, 0), close_counts.get(t, 0)
        if o != c:
            issues.append(f"INFO: XML tag '{t}' opened {o} time(s), closed {c} time(s). Verify balance.")
    return issues


def validate(text):
    checks = [
        check_thinking_budget,
        check_reasoning_echo,
        check_model_string,
        check_context_countdown,
        check_over_prescription,
        check_legacy_residue,
        check_autonomous_grounding,
        check_send_to_user_pairing,
        check_xml_balance,
    ]
    issues = []
    for fn in checks:
        issues.extend(fn(text))
    return issues


def main():
    parser = argparse.ArgumentParser(description="Validate a Fable 5 prompt.")
    parser.add_argument("prompt_file", nargs="?", help="Path to prompt file")
    parser.add_argument("--text", help="Prompt text inline")
    args = parser.parse_args()

    if args.text:
        text = args.text
    elif args.prompt_file:
        with open(args.prompt_file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        parser.error("Provide a prompt file or --text.")

    issues = validate(text)
    fails = [i for i in issues if i.startswith("FAIL")]
    warns = [i for i in issues if i.startswith("WARN")]
    infos = [i for i in issues if i.startswith("INFO")]

    if not issues:
        print("PASS: no issues detected.")
        return 0

    for group in (fails, warns, infos):
        for issue in group:
            print(issue)

    print(f"\nSummary: {len(fails)} fail(s), {len(warns)} warning(s), {len(infos)} info.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
