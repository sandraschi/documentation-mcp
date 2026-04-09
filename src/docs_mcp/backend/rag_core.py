import logging

import lancedb
from fastembed import TextEmbedding

logger = logging.getLogger(__name__)


class BaseVectorStore:
    """Manages document embeddings and retrieval using LanceDB for generic media."""

    def __init__(
        self,
        db_path: str,
        embedding_model_name: str = "BAAI/bge-small-en-v1.5",
        table_name: str = "documents",
    ):
        import pathlib

        self.db_path = pathlib.Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db = lancedb.connect(str(self.db_path))

        # Define cache path to avoid temp folder corruption
        from .config import config as backend_config

        cache_dir = str(backend_config.CACHE_PATH / "fastembed")
        pathlib.Path(cache_dir).mkdir(parents=True, exist_ok=True)

        self.embedding_model = TextEmbedding(model_name=embedding_model_name, cache_dir=cache_dir)
        self.table_name = table_name

    def add_documents(self, documents: list[dict[str, any]], overwrite: bool = True):
        """
        Embed and index documents.
        documents: List of dicts with 'content' and 'metadata'.
        Required fields in each dict: 'id', 'content', 'metadata' (dict)
        """
        if not documents:
            return

        logger.info(f"Embedding {len(documents)} items into '{self.table_name}'...")

        contents = [doc["content"] for doc in documents]
        embeddings = list(self.embedding_model.embed(contents))

        data = []
        for doc, emb in zip(documents, embeddings, strict=False):
            entry = {
                "id": doc.get("id"),
                "vector": emb.tolist(),
                "content": doc.get("content"),
                "metadata": doc.get("metadata", {}),
            }
            # Add source for backwards compatibility with docs_mcp
            if "source" in doc:
                entry["source"] = doc["source"]

            data.append(entry)

        if overwrite or self.table_name not in self.db.table_names():
            # Create or completely overwrite
            self.db.create_table(self.table_name, data=data, mode="overwrite")
        else:
            # Append to existing table
            tbl = self.db.open_table(self.table_name)
            tbl.add(data)

        logger.info(f"Indexed {len(data)} items into LanceDB table '{self.table_name}'.")

    def search(self, query: str, limit: int = 5, where: str = None) -> list[dict[str, any]]:
        """Semantic search with optional Pre-filter (where clause)"""
        if self.table_name not in self.db.table_names():
            logger.warning(f"Table '{self.table_name}' not found.")
            return []

        tbl = self.db.open_table(self.table_name)
        query_embedding = list(self.embedding_model.embed([query]))[0]

        search_req = tbl.search(query_embedding).limit(limit)
        if where:
            search_req = search_req.where(where)

        return search_req.to_arrow().to_pylist()

    def get_table_metadata(self) -> dict:
        """Return basic stats about the table."""
        if self.table_name not in self.db.table_names():
            return {"exists": False, "row_count": 0}

        tbl = self.db.open_table(self.table_name)
        # Using count_rows() correctly for LanceDB
        return {"exists": True, "row_count": tbl.count_rows()}
