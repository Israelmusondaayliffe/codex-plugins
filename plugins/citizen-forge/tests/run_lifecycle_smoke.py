import json
import tempfile
from pathlib import Path

from helpers import PLUGIN_ROOT, brief

from citizen_forge.change_classifier import classify
from citizen_forge.checks import run_all
from citizen_forge.intake import initialize_project
from citizen_forge.policy import decide, load_policy
from citizen_forge.provision import plan, provision
from citizen_forge.release import decide_release
from citizen_forge.risk import infer_scores
from citizen_forge.roads import select


def main() -> int:
    policy = load_policy(PLUGIN_ROOT / "policies" / "default-policy.json")
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        value = brief()
        initialize_project(root, value, confirmed=True)
        triage = decide(value, infer_scores(value), policy)
        road = select(value["shape"], PLUGIN_ROOT / "assets" / "roads")
        provisioning = plan(root, road, {})
        result = provision(root, PLUGIN_ROOT / "assets" / "roads" / road["name"], provisioning)
        checks = run_all(root, policy, value)
        release = decide_release(checks, classify("initial release"))
        receipt = {"idea": "confirmed", "triage": triage["final_route"], "road": road["name"], "provisioned_local_only": result["local_only"], "release_decision": release["decision"], "unavailable_controls_blocked": any(item.status.value == "UNAVAILABLE" for item in checks) and release["decision"] == "RELEASE_BLOCKED"}
        print(json.dumps(receipt, indent=2))
        return 0 if receipt == {"idea": "confirmed", "triage": "PROTOTYPE_ONLY", "road": "python-artifact-generator", "provisioned_local_only": False, "release_decision": "RELEASE_BLOCKED", "unavailable_controls_blocked": True} else 1


if __name__ == "__main__":
    raise SystemExit(main())
