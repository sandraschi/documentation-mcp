# Notion: Technical Specifications (SOTA 2026)

This document outlines the high-density technical standards for Notion integration within the Sandra fleet, optimized for the September 2025 API version.

## 🗄️ Core Data Entities
> [!NOTE]
> Following the `2025-09-03` update, "Databases" are functionally treated as parent containers for **Data Sources**.

- **Task Master**: Central registry for agentic task orchestration. Uses the `data_source` primitive for high-speed relational queries.
- **Fleet Inventory**: Relational stack linking hardware IDs to maintenance telemetry.
- **Knowledge Base**: Indexed via the RAG pipeline for semantic retrieval.

## ⚙️ API Integration & Standards
- **Version**: `2025-09-03` (Mandatory).
- **Authentication**: Bearer Token (Internal Integration Secret).
- **Protocol**: HTTPS REST with specialized MCP transport (Stdio/HTTP).
- **Rate Management**: Austrian Efficiency Protocol — agents must batch operations to respect the 3-req/sec baseline and minimize token usage.

## 🏗️ Internal Logic & RAG Pipeline

### Data Source Architecture
Notion data is now consumed via `data_source_id`. Page creation tools must explicitly define the parent type to avoid ambiguity with legacy database structures.

### RAG Strategy (Semantic Memory)
1. **Extraction**: Periodic scanning of shared pages and data sources.
2. **Chunking**: Block-aware decomposition preserving hierarchical context.
3. **Embedding**: Local generation using `all-MiniLM-L6-v2`.
4. **Storage**: LanceDB vector tables located at `D:/Dev/repos/notion-mcp/data/vector_db`.
5. **Retrieval**: Top-k semantic search integrated with LLM prompt context injection.

---
*Last updated: 2026-03-07*
*SOTA v14.0 - Austrian Reductionist Standard*
