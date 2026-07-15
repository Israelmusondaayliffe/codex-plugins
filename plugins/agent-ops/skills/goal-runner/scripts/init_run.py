#!/usr/bin/env python3
"""Scaffold the two state files for a goal run.

Usage:
  python init_run.py --name <task-slug> --dir <output-dir> [--version N]

Creates <dir>/<name>_goal-contract_v<N>.md and <dir>/<name>_goal-progress_v<N>.md.
Refuses to overwrite existing files (version every iteration, never overwrite).
Prints the two paths on success.
"""

import argparse
import datetime
import os
import sys

CONTRACT = """GOAL: [outcome in one sentence]
DELIVERABLE: [exact path(s)]
CREATED: {date} | TARGET: [Cowork / Claude Code / chat] | STATUS: active

## MACHINE CHECKS
- file_exists: <path>
- no_dashes: <path>

## JUDGMENT CRITERIA
1. [criterion]. 8+ means: [specific, observable bar]

## SCOPE
Read: [paths]. Write: [paths]. Never touch: [paths].

## STOPS
- Success: all machine checks pass and all judgment criteria score 8 or above.
- Failure: if [condition] persists after [N] attempts, stop and report what went wrong.
- Blocked: if no defensible path remains, stop and report what would clear the block.
- Cap: maximum 5 iterations.

## ITERATION POLICY
[Per failure type, which knob turns.]
"""

PROGRESS = """CONTRACT: {contract_path}
RUN STARTED: {date}

---
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="task slug, kebab-case")
    ap.add_argument("--dir", required=True, help="output directory")
    ap.add_argument("--version", type=int, default=1)
    args = ap.parse_args()

    os.makedirs(args.dir, exist_ok=True)
    date = datetime.date.today().isoformat()
    contract_path = os.path.join(args.dir, f"{args.name}_goal-contract_v{args.version}.md")
    progress_path = os.path.join(args.dir, f"{args.name}_goal-progress_v{args.version}.md")

    for p in (contract_path, progress_path):
        if os.path.exists(p):
            print(f"ERROR: {p} exists. Bump --version, never overwrite.")
            sys.exit(1)

    with open(contract_path, "w", encoding="utf-8") as f:
        f.write(CONTRACT.format(date=date))
    with open(progress_path, "w", encoding="utf-8") as f:
        f.write(PROGRESS.format(contract_path=contract_path, date=date))

    print(contract_path)
    print(progress_path)
    sys.exit(0)


if __name__ == "__main__":
    main()
