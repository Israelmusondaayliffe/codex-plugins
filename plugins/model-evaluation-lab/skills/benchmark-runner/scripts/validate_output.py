#!/usr/bin/env python3
"""Validate a normalized Benchmark Runner artifact and its aggregates."""

from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from validate_skill_output import load_json, validate


def close(actual: object, expected: float) -> bool:
    numeric = isinstance(actual, (int, float)) and not isinstance(actual, bool)
    return numeric and math.isclose(
        float(actual), expected, rel_tol=1e-6, abs_tol=1e-6
    )


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_output.py ARTIFACT.json", file=sys.stderr)
        return 2
    artifact = Path(sys.argv[1])
    try:
        result = validate(Path(__file__).resolve().parent.parent / "assets/output-schema.json", artifact)
        data = load_json(artifact, "artifact")
    except ValueError as exc:
        result = {"valid": False, "skill": "benchmark-runner", "errors": [str(exc)]}
        data = {}
    errors = list(result.get("errors", []))
    if isinstance(data, dict):
        failures = data.get("failures")
        if not isinstance(failures, list):
            errors.append("failures must be a list")
        groups: dict[str, list[dict[str, object]]] = defaultdict(list)
        for index, item in enumerate(data.get("results", []) if isinstance(data.get("results"), list) else []):
            if not isinstance(item, dict):
                continue
            if not isinstance(item.get("passed"), bool):
                errors.append(f"results[{index}].passed must be boolean")
            for field in ("score", "latency_ms", "cost_usd"):
                value = item.get(field)
                if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
                    errors.append(f"results[{index}].{field} must be a non-negative number")
            candidate = item.get("candidate")
            if isinstance(candidate, str):
                groups[candidate].append(item)
        aggregate_values = data.get("aggregates", [])
        aggregates = (
            {
                item.get("candidate"): item
                for item in aggregate_values
                if isinstance(item, dict)
            }
            if isinstance(aggregate_values, list)
            else {}
        )
        if set(aggregates) != set(groups):
            errors.append("aggregate candidates must exactly match result candidates")
        for candidate, records in groups.items():
            aggregate = aggregates.get(candidate, {})
            expected_values = {
                "case_count": float(len(records)),
                "pass_rate": sum(1 for item in records if item.get("passed")) / len(records),
                "mean_score": mean(float(item["score"]) for item in records),
                "mean_latency_ms": mean(float(item["latency_ms"]) for item in records),
                "total_cost_usd": sum(float(item["cost_usd"]) for item in records),
            }
            for field, expected in expected_values.items():
                if not close(aggregate.get(field), expected):
                    errors.append(f"aggregate {candidate}.{field} does not match case results")
        if data.get("execution_status") == "complete" and not data.get("results_complete"):
            errors.append("complete execution requires results_complete=true")
    result = {"valid": not errors, "skill": "benchmark-runner", "errors": errors}
    print(json.dumps(result, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
