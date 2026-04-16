from pathlib import Path

from pydantic import BaseModel, Field


class DocsConfig(BaseModel):
    """Configuration for Docs MCP RAG Backend (Federated Public Edition)"""

    # Paths - Unified relative structure
    # DOCS_ROOT is now where documentation-mcp/docs sits
    ROOT: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent.parent)
    DOCS_INTERNAL: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent.parent / "docs")

    # Federated Paths (External repos found in sibling directories)
    ADVANCED_MEMORY_PATH: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.parent.parent.parent / "advanced-memory-mcp"
    )

    # DB and Cache
    DB_PATH: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data" / "lancedb")
    CACHE_PATH: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data" / "cache")

    # Embedding Configuration
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # Search Configuration
    DEFAULT_TOP_K: int = 5
    MIN_SCORE: float = 0.5

    @property
    def DOCS_ROOT(self) -> Path:
        """Compatibility property for legacy internal references."""
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
