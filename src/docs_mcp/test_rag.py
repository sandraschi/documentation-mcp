import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

import logging

from backend.ingestor import ContentIngestor
from backend.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)


def test_backend():
    print("Initializing Ingestor...")
    ingestor = ContentIngestor()
    docs = ingestor.load_all_docs()
    print(f"Found {len(docs)} documents.")

    if not docs:
        print("No documents found! Check paths.")
        return

    print("Initializing VectorStore...")
    vs = VectorStore()
    vs.add_documents(docs)

    print("Testing Search...")
    results = vs.search("What is FastMCP?", limit=2)
    for r in results:
        print(f"\nSource: {r['source']}")
        print(f"Score: {r['_distance']}")  # LanceDB returns distance usually, or we can check what it returns
        print(f"Content: {r['content'][:100]}...")


if __name__ == "__main__":
    test_backend()
