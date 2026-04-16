import hashlib
import logging
from pathlib import Path
from typing import Any

import frontmatter

from .config import config

logger = logging.getLogger(__name__)

# Directories that add noise without search value
EXCLUDE_DIRS = {
    "junk",
    "node_modules",
    ".git",
    "backup",
    "backups",
    "__pycache__",
    "dist",
    "htmlcov",
    ".venv",
    "venv",
}


class ContentIngestor:
    """Crawls and chunks documentation for the VectorStore.

    Federated Edition: Ingests internal /docs and external Advanced Memory roots.
    """

    def __init__(self):
        self.chunk_size = config.CHUNK_SIZE
        self.chunk_overlap = config.CHUNK_OVERLAP

    def glob_markdown(self, root_path: Path) -> list[Path]:
        """Recursively find all .md files, skipping noise directories."""
        if not root_path.is_dir():
            return []
        return [p for p in root_path.rglob("*.md") if not any(part in EXCLUDE_DIRS for part in p.parts)]

    def parse_frontmatter(self, file_path: Path) -> tuple[dict[str, Any], str]:
        """Parse YAML frontmatter from a markdown file."""
        try:
            post = frontmatter.load(str(file_path))
            meta = dict(post.metadata)
            clean = {}
            for k, v in meta.items():
                if isinstance(v, list):
                    clean[k] = ", ".join(str(i) for i in v)
                else:
                    clean[k] = str(v)
            return clean, post.content
        except Exception as e:
            logger.debug(f"No/invalid frontmatter in {file_path}: {e}")
            try:
                return {}, file_path.read_text(encoding="utf-8")
            except Exception:
                return {}, ""

    def chunk_text(self, text: str) -> list[str]:
        """Markdown-aware recursive character chunker."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            if end >= len(text):
                chunks.append(text[start:])
                break

            chunk_slice = text[start:end]
            last_triple = chunk_slice.rfind("\n\n\n")
            if last_triple != -1 and last_triple > self.chunk_size // 2:
                end = start + last_triple + 3
            else:
                last_double = chunk_slice.rfind("\n\n")
                if last_double != -1 and last_double > self.chunk_size // 2:
                    end = start + last_double + 2
                else:
                    last_newline = chunk_slice.rfind("\n")
                    if last_newline != -1 and last_newline > self.chunk_size // 4:
                        end = start + last_newline + 1

            chunks.append(text[start:end])
            start = end - self.chunk_overlap
        return chunks

    def process_file(self, file_path: Path, root_path: Path, extra_meta: dict | None = None) -> list[dict[str, Any]]:
        """Process a single markdown file into chunks with metadata."""
        try:
            fm_meta, body = self.parse_frontmatter(file_path)
            chunks = self.chunk_text(body)
            docs = []
            for i, chunk in enumerate(chunks):
                doc_id = hashlib.sha256(f"{file_path}_{i}".encode()).hexdigest()

                try:
                    # Relativize to the specific root it came from
                    rel_path = str(file_path.relative_to(root_path)).replace("\\", "/")
                except ValueError:
                    rel_path = str(file_path.name)

                metadata = {
                    "filename": file_path.name,
                    "relative_path": rel_path,
                    "fm_title": fm_meta.get("title", ""),
                    "fm_category": fm_meta.get("category", ""),
                    "fm_status": fm_meta.get("status", ""),
                    "fm_audience": fm_meta.get("audience", ""),
                    "fm_skill_candidate": fm_meta.get("skill_candidate", False),
                    "fm_last_updated": fm_meta.get("last_updated", ""),
                }
                if extra_meta:
                    metadata.update(extra_meta)

                docs.append(
                    {
                        "id": doc_id,
                        "content": chunk,
                        "source": str(file_path).replace("\\", "/"),
                        "metadata": metadata,
                    }
                )
            return docs

        except Exception as e:
            logger.error(f"Failed to process {file_path}: {e}")
            return []

    def load_all_docs(self, extra_paths: list[Path] | None = None) -> list[dict[str, Any]]:
        """Scans internal docs and federated external roots."""
        all_docs = []

        # 1. Internal Documentation Root (Public)
        if config.DOCS_INTERNAL.exists():
            paths = self.glob_markdown(config.DOCS_INTERNAL)
            logger.info(f"Found {len(paths)} markdown files in internal docs/")
            for p in paths:
                all_docs.extend(self.process_file(p, config.DOCS_INTERNAL, extra_meta={"type": "core"}))

        # 2. Federated: Advanced Memory Knowledge (Optional)
        if config.knowledge_path.exists():
            paths = self.glob_markdown(config.knowledge_path)
            logger.info(f"Federating {len(paths)} files from advanced-memory/knowledge")
            for p in paths:
                all_docs.extend(
                    self.process_file(
                        p,
                        config.knowledge_path,
                        extra_meta={"type": "intelligence", "source_repo": "advanced-memory-mcp"},
                    )
                )

        # 3. Federated: Advanced Memory Notes (Optional)
        if config.notes_path.exists():
            paths = self.glob_markdown(config.notes_path)
            logger.info(f"Federating {len(paths)} files from advanced-memory/notes")
            for p in paths:
                all_docs.extend(
                    self.process_file(
                        p, config.notes_path, extra_meta={"type": "memory", "source_repo": "advanced-memory-mcp"}
                    )
                )

        # 4. User Provided Custom Paths
        if extra_paths:
            for extra_root in extra_paths:
                if extra_root.exists() and extra_root.is_dir():
                    paths = self.glob_markdown(extra_root)
                    logger.info(f"Found {len(paths)} files in custom path {extra_root}")
                    for p in paths:
                        all_docs.extend(
                            self.process_file(
                                p, extra_root, extra_meta={"type": "custom", "custom_root": str(extra_root)}
                            )
                        )

        logger.info(f"Total: {len(all_docs)} chunks ready for embedding")
        return all_docs
