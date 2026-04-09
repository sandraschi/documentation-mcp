import logging
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from docs_mcp.backend.ingestor import ContentIngestor
from docs_mcp.backend.config import config

logging.basicConfig(level=logging.INFO)

def test_ingestion():
    print(f"Testing ingestion from: {config.DOCS_INTERNAL}")
    ingestor = ContentIngestor()
    docs = ingestor.load_all_docs()
    print(f"Successfully loaded {len(docs)} chunks.")
    
    if docs:
        print(f"Sample source from first chunk: {docs[0]['source']}")
        print(f"Metadata sample: {docs[0]['metadata']}")

if __name__ == "__main__":
    test_ingestion()
