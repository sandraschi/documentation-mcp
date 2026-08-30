"""NotebookLM-ready export bundles.

NotebookLM accepts sources of bounded size (roughly 500k words per source). This
module splits an indexed selection of documentation files into a single,
word-counted markdown bundle that stays under the configured limit so it can be
dropped straight into a Notebook - NotebookLM cannot speak MCP, so the corpus
must be exported as a static file.
"""

from __future__ import annotations

import logging
import re
import time
from pathlib import Path

from fastmcp import FastMCP

from docs_mcp.backend.config import config

logger = logging.getLogger(__name__)

_READ_ONLY = {"readonly": True}

_ALLOWED_EXTS = {".md", ".markdown", ".json", ".yaml", ".yml", ".proto", ".toml"}
_SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", "target", "mcpb", "data"}
_DEFAULT_MAX_WORDS = 100_000

# Rough word-count via whitespace split; NotebookLM counts English tokens, so a
# whitespace split is a safe upper-bound approximation.
_WORD_RE = re.compile(r"\S+")


def count_words(text: str) -> int:
    """Count whitespace-delimited words in ``text``.

    ## Return Format
    int word count.
    """
    return len(_WORD_RE.findall(text))


def _fmt(timestamp: float) -> str:
    return time.strftime("%Y%m%d_%H%M%S", time.localtime(timestamp))


def _collect_files(root: Path, subfolder: str | None) -> list[Path]:
    """Walk the corpus root and return allowed doc files, optionally scoped."""
    base = root.resolve()
    if subfolder:
        candidate = (base / subfolder.replace("\\", "/").strip("/")).resolve()
        if not candidate.is_relative_to(base):
            logger.warning("subfolder %r escapes docs root; ignoring", subfolder)
            return []
        base = candidate
    if not base.is_dir():
        return []
    files: list[Path] = []
    for p in sorted(base.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in _ALLOWED_EXTS:
            continue
        rel = p.relative_to(root)
        if any(part in _SKIP_DIRS or part.startswith(".") for part in rel.parts):
            continue
        files.append(p)
    return files


def build_bundle(
    root: Path,
    subfolder: str | None,
    *,
    max_words: int | None = None,
) -> tuple[str, list[str], int]:
    """Join doc file contents into a single high-density markdown bundle.

    ## Return Format
    (bundle_text, file_list, word_count)
    """
    limit = max_words or _DEFAULT_MAX_WORDS
    chunks: list[str] = []
    file_list: list[str] = []
    total_words = 0

    for path in _collect_files(root, subfolder):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:  # pragma: no cover - rare IO error
            logger.warning("Skipping %s: %s", rel, exc)
            continue
        header = f"## File: {rel}\n\n```{path.suffix.lstrip('.')}\n"
        # Over-count slightly to guarantee the cap; trim trailing fence cost.
        approx = count_words(text) + count_words(header) + 2
        if total_words + approx > limit:
            logger.info("Bundle hit word cap (%d >= %d) at %s", total_words, limit, rel)
            break
        chunks.append(f"{header}{text}\n```\n")
        file_list.append(rel)
        total_words += approx

    return f"# High-Density Docs Export\n\n{''.join(chunks)}", file_list, total_words


def export_notebooklm(
    subfolder: str | None = None,
    max_words: int | None = None,
    output_dir: str | None = None,
    *,
    preview: bool = False,
) -> dict:
    """Write (or preview) a NotebookLM-ready bundle of the indexed docs.

    Exports the documentation corpus as a single word-capped markdown file that
    can be dropped straight into Google NotebookLM (which cannot speak MCP).

    Args:
        subfolder (str | None): Limit to a subpath under the docs root
            (e.g. "standards"). None = whole corpus.
        max_words (int | None): Word cap for the bundle. Default 100,000.
        output_dir (str | None): Output directory. Defaults to the package
            data/notebooklm directory.
        preview (bool): If true, return the bundle text instead of writing a file.

    ## Return Format
    {"success": bool, "message": str,
     "result": {"output_path": str|None, "word_count": int, "max_words": int,
                "file_count": int, "files": [str], "bundle": str|None}}

    ## Examples
    - export_notebooklm(subfolder="standards", max_words=50000)
    - export_notebooklm(preview=True)
    """
    root = config.DOCS_ROOT
    bundle, file_list, word_count = build_bundle(root, subfolder, max_words=max_words)
    max_words_used = max_words or _DEFAULT_MAX_WORDS

    if preview:
        return {
            "success": True,
            "message": f"Built bundle preview: {word_count} words from {len(file_list)} files.",
            "result": {
                "output_path": None,
                "word_count": word_count,
                "max_words": max_words_used,
                "file_count": len(file_list),
                "files": file_list,
                "bundle": bundle,
            },
        }

    if not file_list:
        return {
            "success": False,
            "message": "No readable files matched the selection.",
            "result": {
                "output_path": None,
                "word_count": 0,
                "max_words": max_words_used,
                "file_count": 0,
                "files": [],
                "bundle": None,
            },
        }

    default_out = Path(__file__).resolve().parent.parent / "data" / "notebooklm"
    out_root = Path(output_dir).resolve() if output_dir else default_out
    out_root.mkdir(parents=True, exist_ok=True)
    out_path = out_root / f"docs_bundle_{_fmt(time.time())}.md"
    out_path.write_text(bundle, encoding="utf-8")

    return {
        "success": True,
        "message": f"Wrote NotebookLM bundle with {word_count} words from {len(file_list)} files to {out_path}.",
        "result": {
            "output_path": str(out_path),
            "word_count": word_count,
            "max_words": max_words_used,
            "file_count": len(file_list),
            "files": file_list,
            "bundle": None,
        },
    }


def register_export_tools(mcp: FastMCP):
    """Register the NotebookLM export tool."""
    mcp.tool(annotations=_READ_ONLY, version="1.0.0")(export_notebooklm)
