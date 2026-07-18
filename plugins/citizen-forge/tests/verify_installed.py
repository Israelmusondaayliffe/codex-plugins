import hashlib
import json
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1]
CACHE_ROOT = Path.home() / ".codex" / "plugins" / "cache"


def hashes(root: Path):
    values = {}
    for path in root.rglob("*"):
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            values[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    return values


def main() -> int:
    version = json.loads((SOURCE / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]
    candidates = sorted(CACHE_ROOT.glob("*/citizen-forge/{}".format(version)))
    if not candidates:
        raise SystemExit("Installed cache is missing below: {}".format(CACHE_ROOT))
    target = candidates[-1]
    source_hashes = hashes(SOURCE)
    cache_hashes = hashes(target)
    if source_hashes != cache_hashes:
        missing = sorted(set(source_hashes) - set(cache_hashes))
        extra = sorted(set(cache_hashes) - set(source_hashes))
        changed = sorted(key for key in set(source_hashes) & set(cache_hashes) if source_hashes[key] != cache_hashes[key])
        print(json.dumps({"valid": False, "missing": missing, "extra": extra, "changed": changed}, indent=2))
        return 1
    print(json.dumps({"valid": True, "version": version, "cache": str(target), "files": len(source_hashes)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
