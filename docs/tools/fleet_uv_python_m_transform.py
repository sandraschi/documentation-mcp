"""Rewrite MASTER_MCP_CONFIG.json uv console-script launches to `uv run python -m ...`.

Windows: avoids shared `.venv\\Scripts\\*.exe` replacement (error 32) when multiple MCP
clients start the same project.

Run from anywhere:
  py -3 tools/fleet_uv_python_m_transform.py
  py -3 tools/fleet_uv_python_m_transform.py --dry-run
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MASTER = ROOT / "operations" / "MASTER_MCP_CONFIG.json"

# Typer CLIs that expose `mcp` and need explicit stdio for IDE configs.
MCP_SUBCOMMAND_STDIO = frozenset(
    {
        "advanced_memory.cli.main",
        "basic_memory.cli.main",
    }
)

# script name in config -> (module, extra_args after -m)
# Use when [project.scripts] is absent or config script name mismatches pyproject.
MANUAL_SCRIPT_TARGETS: dict[str, tuple[str, list[str]]] = {
    "avatarmcp": ("avatarmcp", ["--stdio"]),
    "tapo-camera-mcp": ("devices_mcp.cli_v2", []),  # master used stale script name
    "email-mcp": ("email_mcp.server", []),
    "qbt-mcp": ("rtorrent_mcp.__main__", []),  # pyproject script is rtorrent-mcp
}


def _load_scripts(pyproject: Path) -> dict[str, str]:
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    return (data.get("project") or {}).get("scripts") or {}


def _entry_module(entry: str) -> str:
    return entry.split(":", 1)[0].strip()


def _transform_args(args: list[str]) -> tuple[list[str] | None, str]:
    """Return (new_args, reason) or (None, skip_reason)."""
    if len(args) < 4 or args[0] != "--directory" or args[2] != "run":
        return None, "not uv-directory-run"
    if args[3] == "python":
        return None, "already python -m"

    directory = Path(args[1])
    script = args[3]
    tail = list(args[4:])
    pyproject = directory / "pyproject.toml"

    module: str | None = None
    extra: list[str] = []

    if not pyproject.is_file():
        return None, f"missing pyproject: {directory}"

    scripts = _load_scripts(pyproject)
    if script in MANUAL_SCRIPT_TARGETS:
        module, extra = MANUAL_SCRIPT_TARGETS[script]
    elif script in scripts:
        module = _entry_module(scripts[script])
    else:
        return None, f"script {script!r} not in {pyproject.name} keys={list(scripts)[:6]}"

    if module in MCP_SUBCOMMAND_STDIO:
        t = list(tail)
        if t and t[0] == "mcp":
            t = t[1:]
        merged_tail = ["mcp", "--transport", "stdio", *t]
    else:
        merged_tail = [*extra, *tail]

    new_args = [
        "--directory",
        str(directory).replace("\\", "/"),
        "run",
        "python",
        "-m",
        module,
        *merged_tail,
    ]
    return new_args, "ok"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_MASTER,
        help="MCP JSON file (default: operations/MASTER_MCP_CONFIG.json)",
    )
    args = parser.parse_args()

    target = args.file
    data = json.loads(target.read_text(encoding="utf-8"))
    servers = data["mcpServers"]
    changed = 0
    skipped: list[tuple[str, str]] = []

    for name, cfg in servers.items():
        cmd = cfg.get("command") or ""
        if Path(cmd).name.removesuffix(".exe") != "uv" and cmd != "uv":
            continue
        raw_args = cfg.get("args")
        if not isinstance(raw_args, list):
            continue

        new_args, reason = _transform_args(raw_args)
        if new_args is None:
            skipped.append((name, reason))
            continue
        if new_args == raw_args:
            skipped.append((name, "unchanged"))
            continue
        if not args.dry_run:
            cfg["args"] = new_args
        changed += 1

    if not args.dry_run:
        target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"{target}: updated entries: {changed}")
    print("skipped:")
    for n, r in sorted(skipped, key=lambda x: x[0].lower()):
        print(f"  {n}: {r}")


if __name__ == "__main__":
    main()
