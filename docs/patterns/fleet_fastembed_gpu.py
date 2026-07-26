"""Fleet-standard FastEmbed GPU bootstrap for LanceDB RAG repos.

Copy to ``<package>/backend/fastembed_gpu.py`` or ``<package>/rag/fastembed_gpu.py``.
Install stack: ``just rag-gpu-install``. Run embed jobs: ``just rag-gpu`` (venv python, not ``uv run``).

Env: ``RAG_GPU=1`` or ``MCD_RAG_GPU=1``, or marker ``.venv/rag-gpu-mode``.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

EMBED_BATCH_SIZE_CPU = 64
EMBED_BATCH_SIZE_GPU = 256


def _env_flag(name: str) -> bool:
    raw = os.environ.get(name, "").strip().lower()
    return raw in ("1", "true", "yes", "on")


def embed_use_gpu(repo_root: Path | None = None) -> bool:
    if _env_flag("RAG_GPU") or _env_flag("MCD_RAG_GPU"):
        return True
    if repo_root and (repo_root / ".venv" / "rag-gpu-mode").is_file():
        return True
    return False


def create_text_embedding(
    model_name: str,
    cache_dir: str,
    *,
    repo_root: Path | None = None,
    batch_cpu: int = EMBED_BATCH_SIZE_CPU,
    batch_gpu: int = EMBED_BATCH_SIZE_GPU,
):
    """Return (TextEmbedding, device_label, batch_size)."""
    from fastembed import TextEmbedding

    if embed_use_gpu(repo_root):
        try:
            model = TextEmbedding(
                model_name=model_name,
                cache_dir=cache_dir,
                providers=["CUDAExecutionProvider"],
            )
            providers = model.model.model.get_providers()
            if "CUDAExecutionProvider" in providers:
                logger.info("FastEmbed providers: %s", providers)
                return model, "cuda", batch_gpu
            logger.warning("CUDAExecutionProvider unavailable (%s); using CPU", providers)
        except Exception as exc:
            logger.warning("GPU embed init failed (%s); using CPU", exc)

    model = TextEmbedding(model_name=model_name, cache_dir=cache_dir)
    providers = model.model.model.get_providers()
    logger.info("FastEmbed providers: %s", providers)
    return model, "cpu", batch_cpu
