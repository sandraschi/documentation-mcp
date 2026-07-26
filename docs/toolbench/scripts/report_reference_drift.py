#!/usr/bin/env python3
r"""Compare two reference snapshot runs and print a drift report.

Usage:
  python .\report_reference_drift.py
  python .\report_reference_drift.py --out-dir ".\reference_out"
  python .\report_reference_drift.py --base-run 20260326T120000Z --new-run 20260327T120000Z
"""

from __future__ import annotations

import argparse
import difflib
import json
from dataclasses import dataclass
from pathlib import Path

IGNORE_SUFFIXES = (".meta.json", ".html")


@dataclass(frozen=True)
class RunSelection:
    base_run: str
    new_run: str
    base_dir: Path
    new_dir: Path


def _list_runs(out_dir: Path) -> list[Path]:
    return sorted([p for p in out_dir.iterdir() if p.is_dir() and p.name], key=lambda p: p.name)


def _resolve_runs(out_dir: Path, base_run: str | None, new_run: str | None) -> RunSelection:
    runs = _list_runs(out_dir)
    if len(runs) < 2:
        raise SystemExit(f"Need at least 2 runs under {out_dir} to compare.")

    if base_run and new_run:
        b = out_dir / base_run
        n = out_dir / new_run
        if not b.is_dir() or not n.is_dir():
            raise SystemExit("Specified --base-run/--new-run not found.")
        return RunSelection(base_run=base_run, new_run=new_run, base_dir=b, new_dir=n)

    if new_run and not base_run:
        n = out_dir / new_run
        if not n.is_dir():
            raise SystemExit("Specified --new-run not found.")
        earlier = [r for r in runs if r.name < n.name]
        if not earlier:
            raise SystemExit("No earlier run found before --new-run.")
        b = earlier[-1]
        return RunSelection(base_run=b.name, new_run=n.name, base_dir=b, new_dir=n)

    if base_run and not new_run:
        b = out_dir / base_run
        if not b.is_dir():
            raise SystemExit("Specified --base-run not found.")
        later = [r for r in runs if r.name > b.name]
        if not later:
            raise SystemExit("No later run found after --base-run.")
        n = later[0]
        return RunSelection(base_run=b.name, new_run=n.name, base_dir=b, new_dir=n)

    b = runs[-2]
    n = runs[-1]
    return RunSelection(base_run=b.name, new_run=n.name, base_dir=b, new_dir=n)


def _load_text_map(run_dir: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for p in sorted(run_dir.iterdir(), key=lambda x: x.name):
        if not p.is_file():
            continue
        if p.suffix != ".txt":
            continue
        if any(p.name.endswith(sfx) for sfx in IGNORE_SUFFIXES):
            continue
        files[p.name] = p.read_text(encoding="utf-8", errors="replace")
    return files


def _summary_counts(
    base: dict[str, str], new: dict[str, str]
) -> tuple[list[str], list[str], list[str]]:
    b = set(base.keys())
    n = set(new.keys())
    added = sorted(n - b)
    removed = sorted(b - n)
    changed = sorted([k for k in b & n if base[k] != new[k]])
    return added, removed, changed


def _make_diff(old: str, new: str, max_lines: int) -> list[str]:
    diff = list(
        difflib.unified_diff(
            old.splitlines(),
            new.splitlines(),
            fromfile="base",
            tofile="new",
            lineterm="",
        )
    )
    if len(diff) > max_lines:
        return diff[:max_lines] + [f"... [truncated to {max_lines} lines]"]
    return diff


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Report drift between two ToolBench reference snapshot runs."
    )
    ap.add_argument("--out-dir", type=Path, default=Path("./reference_out"))
    ap.add_argument("--base-run", type=str, default=None)
    ap.add_argument("--new-run", type=str, default=None)
    ap.add_argument("--max-diff-lines", type=int, default=120)
    ap.add_argument(
        "--write-json", action="store_true", help="Write report JSON into the new run directory."
    )
    args = ap.parse_args()

    out_dir = args.out_dir
    if not out_dir.is_dir():
        raise SystemExit(f"Missing out-dir: {out_dir}")

    selection = _resolve_runs(out_dir, args.base_run, args.new_run)
    base_map = _load_text_map(selection.base_dir)
    new_map = _load_text_map(selection.new_dir)
    added, removed, changed = _summary_counts(base_map, new_map)

    print(f"Base run: {selection.base_run}")
    print(f"New run : {selection.new_run}")
    print(f"Added   : {len(added)}")
    print(f"Removed : {len(removed)}")
    print(f"Changed : {len(changed)}")

    if added:
        print("\nAdded files:")
        for name in added:
            print(f"- {name}")

    if removed:
        print("\nRemoved files:")
        for name in removed:
            print(f"- {name}")

    diffs: dict[str, list[str]] = {}
    if changed:
        print("\nChanged files:")
        for name in changed:
            print(f"\n## {name}")
            diff_lines = _make_diff(base_map[name], new_map[name], max_lines=args.max_diff_lines)
            diffs[name] = diff_lines
            for line in diff_lines:
                print(line)

    if args.write_json:
        payload = {
            "base_run": selection.base_run,
            "new_run": selection.new_run,
            "added": added,
            "removed": removed,
            "changed": changed,
            "diffs": diffs,
        }
        out_path = selection.new_dir / "drift_report.json"
        out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"\nWrote JSON report: {out_path}")


if __name__ == "__main__":
    main()
