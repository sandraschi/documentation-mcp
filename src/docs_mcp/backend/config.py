import logging
import os
from pathlib import Path

from pydantic import BaseModel, Field, model_validator

logger = logging.getLogger(__name__)


def _repo_root() -> Path:
    return Path(__file__).parent.parent.parent.parent


def _parse_path_list(env_value: str) -> list[Path]:
    return [Path(p.strip()) for p in env_value.split(",") if p.strip()]


class DocsConfig(BaseModel):
    """Configuration for Docs MCP RAG Backend (self-contained public edition)."""

    # ROOT is where the repo lives; DOCS_ROOT indexes documentation-mcp/docs by default.
    ROOT: Path = Field(default_factory=_repo_root)
    DOCS_INTERNAL: Path = Field(default_factory=lambda: _repo_root() / "docs")

    # Optional federated sibling (off unless DOCS_FEDERATE_MEMORY=1)
    ADVANCED_MEMORY_PATH: Path = Field(default_factory=lambda: _repo_root().parent / "advanced-memory-mcp")

    # Optional extra markdown roots from DOCS_EXTRA_PATHS (comma-separated absolute paths)
    EXTRA_PATHS: list[Path] = Field(default_factory=list)
    FEDERATE_MEMORY: bool = False

    # DB and Cache
    DB_PATH: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data" / "lancedb")
    CACHE_PATH: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data" / "cache")

    # Embedding Configuration
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    EMBED_BATCH_SIZE_CPU: int = 64
    EMBED_BATCH_SIZE_GPU: int = 256

    # Search Configuration
    DEFAULT_TOP_K: int = 5
    MIN_SCORE: float = 0.5

    @model_validator(mode="after")
    def _load_env(self) -> "DocsConfig":
        extra = os.environ.get("DOCS_EXTRA_PATHS", "")
        if extra:
            self.EXTRA_PATHS = _parse_path_list(extra)
        self.FEDERATE_MEMORY = os.environ.get("DOCS_FEDERATE_MEMORY", "").strip().lower() in {
            "1",
            "true",
            "yes",
        }
        return self

    @property
    def DOCS_ROOT(self) -> Path:
        """Primary RAG root - defaults to this repo's docs/ folder."""
        env_root = os.environ.get("DOCS_ROOT", "").strip()
        if env_root:
            resolved = Path(env_root).resolve()
            internal = self.DOCS_INTERNAL.resolve()
            if resolved != internal:
                logger.warning(
                    "DOCS_ROOT override (%s) differs from repo docs (%s). "
                    "Unset DOCS_ROOT to index documentation-mcp/docs only.",
                    resolved,
                    internal,
                )
            return Path(env_root)
        return self.DOCS_INTERNAL

    @property
    def knowledge_path(self) -> Path:
        return self.ADVANCED_MEMORY_PATH / "knowledge"

    @property
    def notes_path(self) -> Path:
        return self.ADVANCED_MEMORY_PATH / "notes"

    @property
    def skills_path(self) -> Path:
        return self.ADVANCED_MEMORY_PATH / "skills"


config = DocsConfig()
