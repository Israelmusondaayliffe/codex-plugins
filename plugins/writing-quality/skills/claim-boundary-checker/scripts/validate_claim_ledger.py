#!/usr/bin/env python3
"""Validate a claim-boundary ledger."""

import json
import sys
from pathlib import Path

STATUSES = {"supported", "unsupported", "uncertain", "non-factual"}
REMEDIES = {"keep", "remove", "qualify", "verify", "source"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_claim_ledger.py LEDGER.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2
    errors = []
    claims = data.get("claims")
    if not isinstance(data.get("evidence_scope"), str) or not data["evidence_scope"].strip():
        errors.append("evidence_scope must be a non-empty string")
    if not isinstance(claims, list):
        errors.append("claims must be a list")
        claims = []
    seen = set()
    for index, item in enumerate(claims):
        prefix = f"claims[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        claim_id = item.get("id")
        if not isinstance(claim_id, str) or not claim_id.strip() or claim_id in seen:
            errors.append(f"{prefix}.id must be non-empty and unique")
        seen.add(claim_id)
        if not isinstance(item.get("claim"), str) or not item["claim"].strip():
            errors.append(f"{prefix}.claim must be non-empty")
        if item.get("status") not in STATUSES:
            errors.append(f"{prefix}.status is invalid")
        if item.get("remedy") not in REMEDIES:
            errors.append(f"{prefix}.remedy is invalid")
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
