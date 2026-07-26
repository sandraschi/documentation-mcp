"""
One-shot: add prefab-ui>=0.14.0 to fleet *-mcp repos (alexa-mcp .. yahboom-mcp).
Run from any cwd:  uv run python D:/Dev/repos/tools/fleet_add_prefab_ui.py
"""
from __future__ import annotations

import os
import subprocess
import sys

ROOT = r"D:\Dev\repos"
LOW, HIGH = "alexa-mcp", "yahboom-mcp"


def main() -> int:
    names = sorted(
        d
        for d in os.listdir(ROOT)
        if d.endswith("-mcp") and LOW <= d <= HIGH
    )
    ok = 0
    skip = 0
    fail: list[tuple[str, str]] = []
    for name in names:
        path = os.path.join(ROOT, name)
        if not os.path.isfile(os.path.join(path, "pyproject.toml")):
            print(f"[skip] {name} (no pyproject.toml)")
            skip += 1
            continue
        print(f"[uv add] {name} ...")
        r = subprocess.run(
            ["uv", "add", "prefab-ui>=0.14.0"],
            cwd=path,
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            fail.append((name, (r.stderr or r.stdout or "")[:800]))
            print(f"  FAIL: {fail[-1][1][:400]}")
        else:
            ok += 1
            print("  ok")
    print(f"\nDone: ok={ok} skip={skip} fail={len(fail)}")
    for name, err in fail:
        print(f"  - {name}: {err[:200]}")
    return 0 if not fail else 1


if __name__ == "__main__":
    sys.exit(main())
