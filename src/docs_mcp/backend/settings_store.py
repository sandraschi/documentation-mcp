"""Persistent settings for webapp: Ollama, local LLM, LM Studio, selected model. No hardcoded defaults for model list."""

import json
import logging
import os
from pathlib import Path
from typing import Any

from docs_mcp.backend.config import config

logger = logging.getLogger(__name__)

SETTINGS_FILENAME = "webapp_settings.json"

# Default URLs when not set (so UI and APIs get them automatically)
DEFAULT_OLLAMA_URL = os.environ.get("OLLAMA_URL") or "http://localhost:11434"
DEFAULT_LMSTUDIO_URL = os.environ.get("LMSTUDIO_URL") or "http://localhost:1234/v1"

ALLOWED_KEYS = {
    "ollama_url",
    "ollama_model",
    "local_llm_key",
    "local_llm_url",
    "lmstudio_url",
    "lmstudio_model",
    "provider",
    "rag_federate_memory",
}


def _settings_path() -> Path:
    return config.DB_PATH.parent / SETTINGS_FILENAME


def _default_settings() -> dict[str, Any]:
    ollama_default = os.environ.get("OLLAMA_URL") or DEFAULT_OLLAMA_URL
    lmstudio_default = os.environ.get("LMSTUDIO_URL") or DEFAULT_LMSTUDIO_URL
    return {
        "ollama_url": ollama_default,
        "ollama_model": "",
        "local_llm_key": "",
        "local_llm_url": "",
        "lmstudio_url": lmstudio_default,
        "lmstudio_model": "",
        "provider": "",
        "rag_federate_memory": False,
        "rag_extra_paths": [],
    }


def load_settings() -> dict[str, Any]:
    """Load settings from JSON file. Applies default ollama_url and lmstudio_url when empty."""
    path = _settings_path()
    defaults = _default_settings()

    if not path.exists():
        return defaults

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        out = {**defaults, **{k: v for k, v in data.items() if k in ALLOWED_KEYS}}
        if "rag_extra_paths" in data and isinstance(data["rag_extra_paths"], list):
            out["rag_extra_paths"] = [str(p).strip() for p in data["rag_extra_paths"] if str(p).strip()]
        if "rag_federate_memory" in data:
            out["rag_federate_memory"] = bool(data["rag_federate_memory"])

        if not (out.get("ollama_url") or "").strip():
            out["ollama_url"] = defaults["ollama_url"]
        if not (out.get("lmstudio_url") or "").strip():
            out["lmstudio_url"] = defaults["lmstudio_url"]

        return out
    except Exception as e:
        logger.warning("Failed to load settings: %s", e)
        return defaults


def save_settings(settings: dict[str, Any]) -> None:
    """Persist allowed scalar keys and rag_extra_paths list."""
    path = _settings_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {k: (settings.get(k) or "") for k in ALLOWED_KEYS}
    data["rag_federate_memory"] = bool(settings.get("rag_federate_memory"))
    raw_paths = settings.get("rag_extra_paths") or []
    if isinstance(raw_paths, str):
        raw_paths = [line.strip() for line in raw_paths.splitlines() if line.strip()]
    data["rag_extra_paths"] = [str(p).strip() for p in raw_paths if str(p).strip()]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    logger.info("Settings saved to %s", path)
