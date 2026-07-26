#!/usr/bin/env python3
"""
Fleet: Ruff + Biome + justfile `lint` for MCP repos.

Biome is never optional for repos with a web UI: package.json (@biomejs/biome + scripts),
biome.json beside package.json, and justfile steps using `npx @biomejs/biome ci .` (lint)
and `check --write` (fix). `biome lint` in justfiles is normalized to `biome ci`.

Usage:
  uv run python tools/mcp_fleet_lint_apply.py --dry-run
  uv run python tools/mcp_fleet_lint_apply.py
  uv run python tools/mcp_fleet_lint_apply.py --root D:\\Dev\\repos\\email-mcp
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

STANDARD_RUFF_TOML = """

# --- [tool.ruff] fleet block (mcp_fleet_lint_apply) ---
[tool.ruff]
line-length = 120
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "B", "UP", "RUF"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
"""

BIOME_JSON = {
    "$schema": "https://biomejs.dev/schemas/2.4.12/schema.json",
    "vcs": {"enabled": False, "clientKind": "git", "useIgnoreFile": True},
    "files": {"ignoreUnknown": False},
    "formatter": {"enabled": True, "indentStyle": "space"},
    "linter": {"enabled": True, "rules": {"recommended": True}},
    "javascript": {"formatter": {"quoteStyle": "double"}},
}


def find_web_package_dir(repo: Path) -> Path | None:
    candidates = [
        repo / "web_sota" / "package.json",
        repo / "webapp" / "package.json",
        repo / "web" / "package.json",
        repo / "dashboard" / "package.json",
        repo / "webapp" / "frontend" / "package.json",
    ]
    for p in candidates:
        if p.is_file():
            return p.parent
    return None


def pyproject_target_version(text: str) -> str:
    m = re.search(r"requires-python\s*=\s*\"[^\"]*3\.(\d+)", text)
    if m:
        return f"py3{m.group(1)}"
    return "py312"


def ensure_pyproject_ruff(repo: Path, dry: bool) -> bool:
    pp = repo / "pyproject.toml"
    if not pp.is_file():
        return False
    text = pp.read_text(encoding="utf-8")
    changed = False
    if "[tool.ruff]" not in text:
        tv = pyproject_target_version(text)
        text = text.rstrip() + "\n" + STANDARD_RUFF_TOML.replace("py312", tv) + "\n"
        changed = True
    if "ruff>=" not in text and re.search(r"['\"]ruff['\"]", text) is None:
        if "[project.optional-dependencies]" in text and re.search(r"dev\s*=\s*\[", text):
            text = re.sub(r"(dev\s*=\s*\[\s*)", r'\1\n    "ruff>=0.15.2",', text, count=1)
        elif re.search(r"dependencies\s*=\s*\[", text):
            text = re.sub(r"(dependencies\s*=\s*\[\s*)", r'\1\n    "ruff>=0.15.2",', text, count=1)
        else:
            text = text.rstrip() + '\n\n[project.optional-dependencies]\ndev = ["ruff>=0.15.2"]\n'
        changed = True
    if changed and not dry:
        pp.write_text(text, encoding="utf-8", newline="\n")
    return changed


def ensure_package_biome(pkg_dir: Path, dry: bool) -> bool:
    pkg_json = pkg_dir / "package.json"
    raw = pkg_json.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"SKIP invalid JSON {pkg_json}: {e}", file=sys.stderr)
        return False
    dev = data.setdefault("devDependencies", {})
    changed = False
    if "@biomejs/biome" not in dev:
        dev["@biomejs/biome"] = "^2.4.12"
        changed = True
    scripts = data.setdefault("scripts", {})
    if "biome:ci" not in scripts:
        scripts["biome:ci"] = "biome ci ."
        changed = True
    if "biome" not in scripts:
        scripts["biome"] = "biome check --write ."
        changed = True
    if changed and not dry:
        pkg_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    biome_cfg = pkg_dir / "biome.json"
    if not biome_cfg.is_file():
        changed = True
        if not dry:
            biome_cfg.write_text(json.dumps(BIOME_JSON, indent=2) + "\n", encoding="utf-8")
    return changed


def is_recipe_header(line: str) -> bool:
    s = line.strip()
    if not s or s.startswith("#"):
        return False
    return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*:?\s*$", s)) and not s[0].isspace()


def inject_biome_after_lint_ruff(text: str, web_rel: str) -> tuple[str, bool]:
    """Insert Biome lines immediately after the first `uv run ruff check` line inside `lint:` recipe."""
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    in_lint = False
    inserted = False
    rel_win = web_rel.replace("/", "\\")
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if is_recipe_header(line):
            in_lint = s.startswith("lint:") or s == "lint:"
        out.append(line)
        if (
            in_lint
            and not inserted
            and re.match(r"^\s+uv run ruff check\b", line)
        ):
            m = re.match(r"^(\s+)", line)
            ind = m.group(1) if m else "    "
            out.append(f"{ind}Set-Location '{{{{justfile_directory()}}}}\\{rel_win}'\n")
            out.append(f"{ind}npx @biomejs/biome ci .\n")
            inserted = True
        i += 1
    return ("".join(out), inserted)


def inject_biome_after_fix_ruff_format(text: str, web_rel: str) -> tuple[str, bool]:
    """After `uv run ruff format` inside `fix:` recipe, add biome once."""
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    in_fix = False
    inserted = False
    rel_win = web_rel.replace("/", "\\")
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if is_recipe_header(line):
            in_fix = s.startswith("fix:") or s == "fix:"
        out.append(line)
        if in_fix and not inserted and re.match(r"^\s+uv run ruff format\b", line):
            m = re.match(r"^(\s+)", line)
            ind = m.group(1) if m else "    "
            out.append(f"{ind}Set-Location '{{{{justfile_directory()}}}}\\{rel_win}'\n")
            out.append(f"{ind}npx @biomejs/biome check --write .\n")
            inserted = True
        i += 1
    return ("".join(out), inserted)


def normalize_biome_lint_to_ci(text: str) -> tuple[str, bool]:
    """Prefer `biome ci .` over `biome lint .` in justfile (fleet / CI parity)."""
    if re.search(r"@biomejs/biome\s+ci\b|\bbiome\s+ci\b", text, re.I):
        return text, False
    new = re.sub(
        r"(@biomejs/biome\s+)lint(\s*\.)",
        r"\1ci\2",
        text,
        flags=re.IGNORECASE,
    )
    if new == text:
        new = re.sub(
            r"(?<![\w-])biome\s+lint(\s*\.)",
            r"biome ci\1",
            new,
            flags=re.IGNORECASE,
        )
    return new, new != text


def patch_justfile(repo: Path, web_rel: str | None, dry: bool) -> bool:
    jf = repo / "justfile"
    if not jf.is_file():
        return write_minimal_justfile(repo, web_rel, dry)
    text = jf.read_text(encoding="utf-8")
    text, norm = normalize_biome_lint_to_ci(text)
    changed = norm
    # Already has Biome CI in file — only persist normalize, do not duplicate inject
    if re.search(r"@biomejs/biome\s+ci\b|\bbiome\s+ci\b", text, re.I):
        if changed and not dry:
            jf.write_text(text, encoding="utf-8", newline="\n")
        return changed
    if not web_rel:
        if changed and not dry:
            jf.write_text(text, encoding="utf-8", newline="\n")
        return changed
    text, a = inject_biome_after_lint_ruff(text, web_rel)
    changed = changed or a
    text, b = inject_biome_after_fix_ruff_format(text, web_rel)
    changed = changed or b
    if changed and not dry:
        jf.write_text(text, encoding="utf-8", newline="\n")
    return changed


def write_minimal_justfile(repo: Path, web_rel: str | None, dry: bool) -> bool:
    jf = repo / "justfile"
    rel = web_rel.replace("/", "\\") if web_rel else ""
    biome_lint = ""
    biome_fix = ""
    if web_rel:
        biome_lint = f"\tSet-Location '{{{{justfile_directory()}}}}\\{rel}'\n\tnpx @biomejs/biome ci .\n"
        biome_fix = f"\tSet-Location '{{{{justfile_directory()}}}}\\{rel}'\n\tnpx @biomejs/biome check --write .\n"
    body = (
        'set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]\n\n'
        "# Fleet minimal justfile (mcp_fleet_lint_apply)\n\n"
        "default:\n"
        "\t@Write-Host 'Run: just lint | just fix' -ForegroundColor Cyan\n\n"
        "lint:\n"
        "\tSet-Location '{{justfile_directory()}}'\n"
        "\tuv run ruff check .\n"
        f"{biome_lint}\n"
        "fix:\n"
        "\tSet-Location '{{justfile_directory()}}'\n"
        "\tuv run ruff check . --fix\n"
        "\tuv run ruff format .\n"
        f"{biome_fix}\n"
    )
    if not dry:
        jf.write_text(body, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=REPO_ROOT)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    root: Path = args.root.resolve()

    repos: list[Path]
    if (root / "pyproject.toml").is_file():
        repos = [root]
    else:
        repos = sorted(
            p
            for p in root.iterdir()
            if p.is_dir() and "mcp" in p.name.lower() and (p / "pyproject.toml").is_file()
        )

    touched: list[str] = []
    for repo in repos:
        web = find_web_package_dir(repo)
        web_rel = str(web.relative_to(repo)) if web else None
        flags: list[str] = []
        if ensure_pyproject_ruff(repo, args.dry_run):
            flags.append("pyproject")
        if web:
            if ensure_package_biome(web, args.dry_run):
                flags.append("package.json")
        if patch_justfile(repo, web_rel, args.dry_run):
            flags.append("justfile")
        if flags:
            touched.append(f"{repo.name}: {', '.join(flags)}")

    print(f"Summary (dry_run={args.dry_run}): {len(touched)} repos modified")
    for line in touched:
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
