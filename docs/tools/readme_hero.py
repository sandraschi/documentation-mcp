"""Extract opening title + blurb from a repo README (Starts UI rules, fleet registry).

Skips leading HTML wrappers (e.g. ``<div align="center">``) so the first ``# `` line
becomes the title. Blurb is the hero paragraph(s) before the first ``## `` section.
"""

from __future__ import annotations

import re
from pathlib import Path


def strip_markdown_noise(s: str) -> str:
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"\*([^*]+)\*", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return re.sub(r"\s+", " ", s).strip()


def _strip_leading_atx_heading(line: str) -> str:
    """Remove ``# ...`` / ``###`` prefix from a hero line for plain-text blurbs."""
    return re.sub(r"^#{1,6}\s+", "", line.strip())


def _is_level2_section_heading(line: str) -> bool:
    """True for ``## Foo`` (markdown H2), false for ``###`` and ``#``."""
    s = line.strip()
    return s.startswith("##") and not s.startswith("###")


def _skip_noise_lines(lines: list[str], i: int) -> int:
    """Advance past blanks, HTML, badges, and table rule lines."""
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        if s.startswith("[!") or s.startswith("![") or s.startswith("<"):
            i += 1
            continue
        if s.startswith("|") or s.startswith("---"):
            i += 1
            continue
        break
    return i


def extract_readme_hero(readme_path: Path) -> tuple[str | None, str | None]:
    """First ATX H1 title + hero blurb (text before the first ``## `` section)."""
    try:
        raw = readme_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, None
    lines = raw.splitlines()
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1

    i = _skip_noise_lines(lines, i)

    hero_title: str | None = None
    if i < len(lines):
        first = lines[i].strip()
        if first.startswith("# ") and not first.startswith("##"):
            hero_title = strip_markdown_noise(first[2:].strip())[:120]
            i += 1

    i = _skip_noise_lines(lines, i)

    blurb_lines: list[str] = []
    if i < len(lines) and _is_level2_section_heading(lines[i]):
        i += 1
        while i < len(lines):
            s = lines[i].strip()
            if not s:
                if blurb_lines:
                    break
                i += 1
                continue
            if _is_level2_section_heading(lines[i]):
                break
            if s.startswith("# ") and not s.startswith("##"):
                i += 1
                continue
            blurb_lines.append(_strip_leading_atx_heading(lines[i]))
            if len(" ".join(blurb_lines)) > 480:
                break
            i += 1
    else:
        while i < len(lines):
            s = lines[i].strip()
            if not s:
                if blurb_lines:
                    break
                i += 1
                continue
            if _is_level2_section_heading(lines[i]):
                break
            if s.startswith("# ") and not s.startswith("##"):
                i += 1
                continue
            if s.startswith("[!") or s.startswith("![") or s.startswith("<") or s.startswith("|"):
                i += 1
                continue
            blurb_lines.append(_strip_leading_atx_heading(lines[i]))
            if len(" ".join(blurb_lines)) > 480:
                break
            i += 1

    blurb = strip_markdown_noise(" ".join(blurb_lines))
    if len(blurb) > 450:
        blurb = blurb[:447] + "..."
    if not blurb:
        blurb = None

    if hero_title is None:
        for line in lines:
            t = line.strip()
            if _is_level2_section_heading(t):
                hero_title = strip_markdown_noise(_strip_leading_atx_heading(t))[:120]
                break

    return hero_title, blurb


def read_readme_from_repo(repo_root: Path) -> tuple[str | None, str | None]:
    """Return (hero_title, hero_blurb) from the first README found."""
    for name in ("README.md", "Readme.md", "readme.md"):
        readme = repo_root / name
        if readme.is_file():
            return extract_readme_hero(readme)
    return None, None
