import logging

from .config import config
from .rag_core import BaseVectorStore

logger = logging.getLogger(__name__)


class DocumentStore(BaseVectorStore):
    """Manages document embeddings and retrieval using LanceDB specifically for the docs_mcp."""

    def __init__(self):
        super().__init__(
            db_path=str(config.DB_PATH),
            embedding_model_name=config.EMBEDDING_MODEL,
            table_name="documents",
        )

    def list_sources(self) -> list[str]:
        """List distinct sources indexed"""
        if self.table_name not in self.db.table_names():
            return []

        # Naive approach for small datasets
        tbl = self.db.open_table(self.table_name)
        return list({r["source"] for r in tbl.to_arrow().to_pylist() if "source" in r})
