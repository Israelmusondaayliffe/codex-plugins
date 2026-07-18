import json
import subprocess


EXPECTED = [
    "citizen-forge:citizen-forge",
    "citizen-forge:citizen-idea",
    "citizen-forge:citizen-register",
    "citizen-forge:citizen-triage",
    "citizen-forge:citizen-provision",
    "citizen-forge:citizen-build",
    "citizen-forge:citizen-release",
    "citizen-forge:citizen-change",
    "citizen-forge:citizen-operate",
    "citizen-forge:citizen-explain",
]


def main() -> int:
    run = subprocess.run(["codex", "debug", "prompt-input"], check=False, capture_output=True, text=True)
    if run.returncode:
        print(json.dumps({"valid": False, "command_error": run.stderr}, indent=2))
        return 2
    missing = [name for name in EXPECTED if name not in run.stdout]
    print(json.dumps({"valid": not missing, "expected": EXPECTED, "missing": missing}, indent=2))
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
