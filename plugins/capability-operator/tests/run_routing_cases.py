#!/usr/bin/env python3
"""Run the deterministic capability routing acceptance cases."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ROUTER = ROOT / "skills" / "capability-router"
sys.path.insert(0, str(ROUTER / "scripts"))

from route_request import route_task  # noqa: E402
from validate_routes import load_json, validate_registry, validate_route  # noqa: E402


def main() -> int:
    registry_path = ROUTER / "assets" / "routing-registry.json"
    cases_path = Path(__file__).resolve().parent / "routing-cases.json"
    registry = load_json(registry_path)
    registry_errors = validate_registry(registry, ROOT.parent)
    failures: list[dict] = []
    if registry_errors:
        failures.append({"id": "registry", "errors": registry_errors})

    data = load_json(cases_path)
    cases = data.get("cases", [])
    for case in cases:
        try:
            route = route_task(
                case["task"],
                registry,
                case.get("explicit_plugin"),
                case.get("explicit_skill"),
            )
            errors = validate_route(route, registry)
            expected = case["expected"]
            for key, value in expected.items():
                if route.get(key) != value:
                    errors.append(f"{key}: expected {value!r}, got {route.get(key)!r}")
            if route.get("load_order", []).count(route.get("primary_route")) != 1:
                errors.append("primary route must appear exactly once in load_order")
            if errors:
                failures.append({"id": case["id"], "errors": errors, "route": route})
        except Exception as exc:  # test harness must report every failing fixture
            failures.append({"id": case.get("id", "unknown"), "errors": [str(exc)]})

    guardrails: list[str] = []
    try:
        route_task("Use this unknown thing", registry, explicit_plugin="not-installed")
        guardrails.append("unknown plugin was accepted")
    except ValueError:
        pass
    inferred = route_task("Audit this agent and capture learning", registry)
    if inferred.get("plugin") == "proofloop":
        guardrails.append("ProofLoop was inferred without an explicit request")
    if guardrails:
        failures.append({"id": "guardrails", "errors": guardrails})

    result = {
        "valid": not failures,
        "case_count": len(cases),
        "passed": len(cases) - sum(1 for item in failures if item.get("id") not in {"registry", "guardrails"}),
        "composite_cases": sum(1 for case in cases if case.get("kind") == "composite"),
        "focused_cases": sum(1 for case in cases if case.get("kind") == "focused"),
        "collision_cases": sum(1 for case in cases if case.get("kind") == "collision"),
        "guardrail_checks": 2,
        "failures": failures,
    }
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
