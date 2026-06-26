"""Resolve effective RAG roots from env vars and persisted webapp settings."""

from __future__ import annotations

from pathlib import Path

from docs_mcp.backend.config import config


def _dedupe_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    out: list[Path] = []
    for path in paths:
        key = str(path.resolve()) if path.exists() else str(path)
        if key in seen:
            continue
        seen.add(key)
        out.append(path)
    return out


def effective_extra_paths() -> list[Path]:
    """Merge DOCS_EXTRA_PATHS (env) with rag_extra_paths from webapp settings."""
    from docs_mcp.backend.settings_store import load_settings

    paths: list[Path] = list(config.EXTRA_PATHS)
    settings = load_settings()
    for raw in settings.get("rag_extra_paths") or []:
        if isinstance(raw, str) and raw.strip():
            paths.append(Path(raw.strip()))
    return _dedupe_paths(paths)


def effective_federate_memory() -> bool:
    """True when env DOCS_FEDERATE_MEMORY=1 or webapp rag_federate_memory is enabled."""
    if config.FEDERATE_MEMORY:
        return True
    from docs_mcp.backend.settings_store import load_settings

    return bool(load_settings().get("rag_federate_memory"))


def rag_sources_summary() -> dict:
    """Human-readable summary of what will be indexed on reindex."""
    extra = effective_extra_paths()
    return {
        "docs_root": str(config.DOCS_ROOT.resolve()),
        "extra_paths": [str(p) for p in extra],
        "federate_memory": effective_federate_memory(),
        "advanced_memory_path": str(config.ADVANCED_MEMORY_PATH),
    }
