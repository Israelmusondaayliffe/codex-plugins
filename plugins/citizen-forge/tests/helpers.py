import json
import sys
from pathlib import Path
from typing import Any, Dict

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))


def brief(**overrides: Any) -> Dict[str, Any]:
    value = {
        "name": "Project Tracker",
        "problem": "The team cannot see project status.",
        "outcome": "Show current projects in one place.",
        "current_process": "A spreadsheet is emailed.",
        "intended_users": "Creator",
        "expected_users": 1,
        "second_consumer": False,
        "primary_owner": "Owner",
        "backup_owner": "Backup",
        "data_sources": "Local CSV",
        "access": "read only",
        "data_sensitivity": "internal",
        "external_exposure": "none",
        "automation_level": "human run",
        "reversibility": "fully reversible",
        "frequency": "weekly",
        "failure_consequence": "minor delay",
        "overlap": "none known",
        "shape": "personal-analysis",
        "confidence": 0.95,
    }
    value.update(overrides)
    return value


def write_evidence(project: Path, filename: str, value: Dict[str, Any] = None) -> None:
    target = project / ".citizen" / "evidence" / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value or {"passed": True}) + "\n", encoding="utf-8")
