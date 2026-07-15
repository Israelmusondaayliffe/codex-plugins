#!/usr/bin/env python3
"""Deterministic gate for goal-runner. Parses MACHINE CHECKS from a goal
contract and pass/fails each. Scripts run the same way every time,
instructions drift.

Usage:
  python verify_contract.py <contract.md> [--artifact <path>] [--dry-run]

- The token ARTIFACT inside any check is replaced by the --artifact path.
- --dry-run validates that checks parse (types known, args well-formed)
  without executing them. Use at contract time.

DSL (one per line under '## MACHINE CHECKS'):
  - file_exists: <path>
  - section: <path> | <exact heading line>
  - contains: <path> | <required substring>
  - forbid: <path> | <forbidden substring>
  - min_words: <path> | <N>
  - max_words: <path> | <N>
  - no_dashes: <path>
  - command: <shell command, exit 0 = pass>

Exit codes: 0 all pass, 1 any check fails, 2 contract/parse error.
"""

import argparse
import re
import subprocess
import sys

ARG_COUNTS = {"file_exists": 1, "section": 2, "contains": 2, "forbid": 2,
              "min_words": 2, "max_words": 2, "no_dashes": 1, "command": 1}


def parse_checks(contract_text):
    m = re.search(r"^## MACHINE CHECKS\s*$(.*?)(?=^## |\Z)", contract_text,
                  re.MULTILINE | re.DOTALL)
    if not m:
        return None
    checks = []
    for line in m.group(1).splitlines():
        cm = re.match(r"\s*- (\w+):\s*(.+)", line)
        if not cm:
            continue
        ctype, raw = cm.group(1), cm.group(2).strip()
        if raw.startswith("<"):  # unfilled template placeholder, skip
            continue
        args = [a.strip() for a in raw.split("|")] if ARG_COUNTS.get(ctype, 1) > 1 else [raw]
        checks.append((ctype, args, line.strip()))
    return checks


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def run_check(ctype, args):
    """Returns (ok: bool, detail: str)."""
    try:
        if ctype == "file_exists":
            import os
            return os.path.isfile(args[0]), args[0]
        if ctype == "section":
            text = read(args[0])
            ok = any(line.strip() == args[1] for line in text.splitlines())
            return ok, f"heading '{args[1]}'"
        if ctype == "contains":
            return args[1] in read(args[0]), f"required '{args[1][:60]}'"
        if ctype == "forbid":
            return args[1] not in read(args[0]), f"forbidden '{args[1][:60]}'"
        if ctype == "min_words":
            n = len(read(args[0]).split())
            return n >= int(args[1]), f"{n} words, need >= {args[1]}"
        if ctype == "max_words":
            n = len(read(args[0]).split())
            return n <= int(args[1]), f"{n} words, cap {args[1]}"
        if ctype == "no_dashes":
            text = read(args[0])
            return ("—" not in text and "–" not in text), args[0]
        if ctype == "command":
            r = subprocess.run(args[0], shell=True, capture_output=True,
                               text=True, timeout=120)
            tail = (r.stdout + r.stderr).strip().splitlines()
            return r.returncode == 0, f"exit {r.returncode}" + (f", {tail[-1][:80]}" if tail else "")
        return False, f"unknown check type '{ctype}'"
    except FileNotFoundError as e:
        return False, f"missing file: {e.filename}"
    except subprocess.TimeoutExpired:
        return False, "command timeout (120s)"
    except Exception as e:  # an erroring gate is a broken gate, surface it
        return False, f"check error: {e}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("contract")
    ap.add_argument("--artifact", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    try:
        text = read(args.contract)
    except OSError as e:
        print(f"ERROR: cannot read contract: {e}")
        sys.exit(2)

    checks = parse_checks(text)
    if checks is None:
        print("ERROR: no '## MACHINE CHECKS' section in contract")
        sys.exit(2)
    if not checks:
        print("ERROR: MACHINE CHECKS section has no filled checks")
        sys.exit(2)

    if args.artifact:
        checks = [(t, [a.replace("ARTIFACT", args.artifact) for a in aa], ln)
                  for t, aa, ln in checks]

    print(f"{'Dry-run' if args.dry_run else 'Verifying'}: {len(checks)} machine check(s)")
    print("-" * 56)
    failures = 0
    for ctype, cargs, line in checks:
        if ctype not in ARG_COUNTS:
            print(f"[ERR ] unknown type: {line}")
            failures += 1
            continue
        if len(cargs) != ARG_COUNTS[ctype]:
            print(f"[ERR ] wrong arg count ({len(cargs)}, need {ARG_COUNTS[ctype]}): {line}")
            failures += 1
            continue
        if args.dry_run:
            print(f"[ OK ] parses: {line}")
            continue
        ok, detail = run_check(ctype, cargs)
        print(f"[{'PASS' if ok else 'FAIL'}] {ctype}: {detail}")
        if not ok:
            failures += 1

    print("-" * 56)
    if failures:
        print(f"RESULT: FAIL ({failures} of {len(checks)})")
        sys.exit(1)
    print("RESULT: PASS" + (" (syntax only, dry run)" if args.dry_run else ""))
    sys.exit(0)


if __name__ == "__main__":
    main()
