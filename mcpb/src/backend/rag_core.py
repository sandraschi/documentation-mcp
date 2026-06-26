import logging

import lancedb
from fastembed import TextEmbedding

logger = logging.getLogger(__name__)


def _create_text_embedding(model_name: str, cache_dir: str) -> tuple[TextEmbedding, str, int]:
    from .fastembed_gpu import create_text_embedding

    return create_text_embedding(model_name, cache_dir)


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

        from .config import config as backend_config

        cache_dir = str(backend_config.CACHE_PATH / "fastembed")
        pathlib.Path(cache_dir).mkdir(parents=True, exist_ok=True)

        self.embedding_model, self.embed_device, self.embed_batch_size = _create_text_embedding(
            embedding_model_name, cache_dir
        )
        self.table_name = table_name

    def _embed_documents(
        self,
        documents: list[dict[str, any]],
        *,
        batch_size: int | None = None,
        progress_callback=None,
    ) -> list[dict[str, any]]:
        if not documents:
            return []

        contents = [doc["content"] for doc in documents]
        all_embeddings = []
        total = len(contents)
        batch = batch_size or self.embed_batch_size

        for start in range(0, total, batch):
            chunk = contents[start : start + batch]
            all_embeddings.extend(list(self.embedding_model.embed(chunk)))
            if progress_callback:
                progress_callback(min(start + len(chunk), total), total)

        data = []
        for doc, emb in zip(documents, all_embeddings, strict=False):
            entry = {
                "id": doc.get("id"),
                "vector": emb.tolist(),
                "content": doc.get("content"),
                "metadata": doc.get("metadata", {}),
            }
            if "source" in doc:
                entry["source"] = doc["source"]
            data.append(entry)
        return data

    def add_documents(
        self,
        documents: list[dict[str, any]],
        overwrite: bool = True,
        *,
        progress_callback=None,
    ):
        if not documents:
            return 0

        logger.info(f"Embedding {len(documents)} items into '{self.table_name}'...")
        data = self._embed_documents(documents, progress_callback=progress_callback)

        if overwrite or self.table_name not in self.db.list_tables():
            self.db.create_table(self.table_name, data=data, mode="overwrite")
        else:
            tbl = self.db.open_table(self.table_name)
            tbl.add(data)

        logger.info(f"Indexed {len(data)} items into LanceDB table '{self.table_name}'.")
        return len(data)

    def search(self, query: str, limit: int = 5, where: str = None) -> list[dict[str, any]]:
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
        if self.table_name not in self.db.table_names():
            return {"exists": False, "row_count": 0}

        tbl = self.db.open_table(self.table_name)
        return {"exists": True, "row_count": tbl.count_rows()}
