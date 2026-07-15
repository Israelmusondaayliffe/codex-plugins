#!/usr/bin/env python3
"""Deterministic validator for generated /goal and /loop prompts.

Checks the required components of a goal or loop prompt:
  goal mode:  end state, scope, success stop, failure stop, hard cap
  loop mode:  all of the above plus trigger and memory file
Both modes: no em-dashes.

Usage:
  python validate_prompt.py <file> --mode goal
  python validate_prompt.py <file> --mode loop
  cat prompt.txt | python validate_prompt.py - --mode loop

Exit code 0 when all required checks pass, 1 otherwise.
Warnings (optional components) never affect the exit code.
"""

import argparse
import re
import sys

CHECKS = {
    "end_state": {
        "label": "Verifiable end state",
        "patterns": [
            r"\bstop when\b", r"\bdone means\b", r"\buntil\b",
            r"\bmust include\b", r"\bcomplete[d]? (and|with)\b",
            r"\ball .{0,40}(pass|complete)", r"\bproduce\b.{0,80}\bsaved to\b",
            r"\bsave[d]? (the )?(results?|audit|report|brief|output) (to|as)\b",
            r"\bverifier agent\b", r"\buse the verify-\w+ skill\b",
        ],
        "hint": "Add an explicit done definition: 'Stop when ...' or 'Done means ...'. Apply the stranger test.",
    },
    "scope": {
        "label": "Scope constraint",
        "patterns": [
            r"\bonly (touch|touching|modify|create|read|write|edit)\b",
            r"\bdo not (create|modify|change|touch|write)\b",
            r"\bonly (read from|write to)\b",
        ],
        "hint": "Name what may be touched: 'Only create files in /dir/. Do not modify existing files.'",
    },
    "success_stop": {
        "label": "Success stop",
        "patterns": [
            r"\bstop when\b", r"\bstop after producing\b",
            r"\bstop after \d+ (iterations|attempts|changes|runs)\b",
            r"\breport \"?TASK_COMPLETE\"?", r"\bstop and (report|summarize)\b.{0,40}\bcomplete",
        ],
        "hint": "Add a success stop: 'Stop when [end state] is complete and verified.'",
    },
    "failure_stop": {
        "label": "Failure stop",
        "patterns": [
            r"\bif .{0,120}\b(after|within) \d+ (attempts|retries|tries)\b",
            r"\bafter \d+ (attempts|retries|tries)\b",
            r"\b(skip|flag) (it|them)?\b.{0,40}\bnote why\b",
            r"\bstop and (tell me|report)\b",
            r"\bTASK_FAILED\b",
            r"\b\d+ times in a row\b",
        ],
        "hint": "Add a failure stop: 'If this fails after 3 attempts, stop and report what went wrong.'",
    },
    "hard_cap": {
        "label": "Hard cap (iterations or budget)",
        "patterns": [
            r"\bmaximum (of )?\d+ (iterations|attempts|changes|runs)\b",
            r"\bstop after \d+ (iterations|attempts|changes|runs)\b",
            r"\b\d+ dollars?\b", r"\$\d+", r"\bbudget\b.{0,30}\d",
            r"\btried (five|\d+) changes\b",
        ],
        "hint": "Add a numeric cap: 'Maximum 15 iterations' or a dollar budget.",
    },
    "trigger": {
        "label": "Trigger / cadence (loop)",
        "patterns": [
            r"^/loop\b", r"\bevery \d+ (minutes|hours|days)\b",
            r"\bevery (morning|day|week|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
            r"\bon each run\b", r"\brun (it )?(twice )?(a |per )?(day|week|month)\b",
            r"\bon (pr comment|ci failure|push)\b", r"\bat \d{1,2}(:\d{2})? ?(am|pm)\b",
        ],
        "hint": "Name the trigger: an interval, a schedule, an event, or state self-paced by starting with /loop.",
    },
    "memory": {
        "label": "Memory file (loop)",
        "patterns": [
            r"\bmemory file\b", r"\bprogress\.md\b", r"\brun[- ]?(log|history)\b",
            r"\bchangelog\.md\b", r"\blog (every|each) (attempt|run)\b",
            r"\bstore run history\b", r"\bskip anything you have already stored\b",
        ],
        "hint": "Add a memory file: 'keep a memory file at <path>, read it at the start of every run and update it at the end.'",
    },
}

CHECKS["iteration_policy"] = {
    "label": "Iteration policy (Codex six-element contract)",
    "patterns": [
        r"\bbetween iterations\b", r"\biteration policy\b",
        r"\bif .{0,60}\b(cluster|appears?|persists?|no new)\b.{0,60}\b(expand|tighten|switch|rerun|try)\b",
    ],
    "hint": "For Codex goals, state how to choose the next action between iterations.",
}

GOAL_REQUIRED = ["end_state", "scope", "success_stop", "failure_stop", "hard_cap"]
LOOP_REQUIRED = GOAL_REQUIRED + ["trigger", "memory"]
GOAL_OPTIONAL = ["memory", "iteration_policy"]


def check(text, key):
    lowered = text.lower()
    return any(re.search(p, lowered, re.MULTILINE) for p in CHECKS[key]["patterns"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", help="Prompt file, or - for stdin")
    ap.add_argument("--mode", choices=["goal", "loop"], required=True)
    args = ap.parse_args()

    text = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()

    required = LOOP_REQUIRED if args.mode == "loop" else GOAL_REQUIRED
    optional = [] if args.mode == "loop" else GOAL_OPTIONAL

    failures = []
    print(f"Validating ({args.mode} mode)\n" + "-" * 44)

    for key in required:
        ok = check(text, key)
        print(f"[{'PASS' if ok else 'FAIL'}] {CHECKS[key]['label']}")
        if not ok:
            print(f"       fix: {CHECKS[key]['hint']}")
            failures.append(key)

    for key in optional:
        ok = check(text, key)
        print(f"[{'PASS' if ok else 'WARN'}] {CHECKS[key]['label']} (optional for goals)")
        if not ok:
            print(f"       consider: {CHECKS[key]['hint']}")

    if "—" in text or "–" in text:
        print("[FAIL] Em-dash / en-dash found. Replace with a period or comma.")
        failures.append("dashes")
    else:
        print("[PASS] No em-dashes")

    print("-" * 44)
    if failures:
        print(f"RESULT: FAIL ({len(failures)} required check(s) missing)")
        sys.exit(1)
    print("RESULT: PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
