"""Set operations/fleet-registry.json `fastmcp` from each entry's repo pyproject.toml scan.

Run:
  uv run python tools/sync_fleet_fastmcp.py

Also invoked at the end of tools/generate_fleet_registry.py.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))
from fastmcp_version import parse_fastmcp_version_from_pyproject

REPO_ROOT = Path(__file__).resolve().parents[1]
FLEET_PATH = REPO_ROOT / "operations" / "fleet-registry.json"


def apply_fastmcp_to_fleet_items(fleet: list[dict]) -> tuple[list[dict], dict[str, int]]:
    """Return new fleet list with `fastmcp` set from disk scan. Stats: found, missing_repo, no_pyproject, no_fastmcp."""
    stats = {"found": 0, "missing_repo": 0, "no_pyproject": 0, "no_fastmcp": 0}
    out: list[dict] = []

    for raw in fleet:
        if not isinstance(raw, dict):
            out.append(raw)
            continue
        entry = dict(raw)
        rp = entry.get("repo_path")
        if not isinstance(rp, str) or not rp.strip():
            out.append(entry)
            continue
        root = Path(rp.replace("\\", "/"))
        if not root.is_dir():
            stats["missing_repo"] += 1
            entry.pop("fastmcp", None)
            out.append(entry)
            continue
        pyproject = root / "pyproject.toml"
        if not pyproject.is_file():
            stats["no_pyproject"] += 1
            entry.pop("fastmcp", None)
            out.append(entry)
            continue
        ver = parse_fastmcp_version_from_pyproject(pyproject)
        if ver:
            entry["fastmcp"] = ver
            stats["found"] += 1
        else:
            stats["no_fastmcp"] += 1
            entry.pop("fastmcp", None)
        out.append(entry)

    return out, stats


def main() -> None:
    data = json.loads(FLEET_PATH.read_text(encoding="utf-8"))
    fleet = data.get("fleet", [])
    if not isinstance(fleet, list):
        raise SystemExit("fleet-registry.json: missing 'fleet' array")

    new_fleet, stats = apply_fastmcp_to_fleet_items(fleet)
    data["fleet"] = new_fleet
    FLEET_PATH.write_text(json.dumps(data, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Wrote {FLEET_PATH}")
    print(
        "fastmcp scan: "
        f"set={stats['found']}, "
        f"no_repo={stats['missing_repo']}, "
        f"no_pyproject={stats['no_pyproject']}, "
        f"no_fastmcp_dep={stats['no_fastmcp']}"
    )


if __name__ == "__main__":
    main()
