#!/usr/bin/env python3
"""Find exact-name overlaps in a capability inventory."""

import json
import sys
from collections import defaultdict
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: find_overlaps.py INVENTORY.json OUTPUT.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid inventory: {exc}", file=sys.stderr)
        return 2
    groups: dict[str, list[dict]] = defaultdict(list)
    for item in data.get("loose_skills", []):
        groups[item.get("name", "")].append(item)
    for plugin in data.get("plugin_sources", []):
        for name in plugin.get("skills", []):
            groups[name].append({
                "name": name,
                "layer": "plugin",
                "path": f"{plugin.get('path')}/skills/{name}",
                "plugin": plugin.get("name"),
            })
    overlaps = []
    for name, locations in sorted(groups.items()):
        if name and len(locations) > 1:
            fingerprints = {item.get("skill_sha256") for item in locations if item.get("skill_sha256")}
            state = "identical-mirror" if len(fingerprints) == 1 and len(fingerprints) == len(locations) else "unresolved"
            if len(fingerprints) > 1:
                state = "drifted-copy"
            if any(item.get("layer") == "plugin" for item in locations):
                state = "namespaced-bundle" if len(fingerprints) <= 1 else state
            overlaps.append({"name": name, "state": state, "locations": locations})
    output = {"overlap_count": len(overlaps), "overlaps": overlaps}
    Path(sys.argv[2]).write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": sys.argv[2], "overlap_count": len(overlaps)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
