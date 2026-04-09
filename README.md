# Documentation-MCP (Docs-MCP v14.0)

> [!IMPORTANT]
> **Federated Public Documentation Hub**: This repository is the public-facing control plane for MCP standards, fleet registries, and architectural patterns. It leverages a Federated RAG engine to unify search across internal core documentation and external intelligence repositories (like Advanced Memory MCP).

## Overview

Documentation-MCP is part of the **Alsergrund Industrial Fleet**. It provides:
- **Core Standards**: SOTA v13.1 protocols for FastMCP 3.2+, Git workflows, and UI/UX design.
- **Fleet Registry**: High-fidelity indexing of the 135+ repository MCP ecosystem.
- **Federated RAG**: A neural search engine that cross-links documentation with agentic memory and personal skills.

## Architecture

```mermaid
graph TD
    User([User Agent]) --> MCP[Docs-MCP Server]
    MCP --> RAG[Federated RAG Engine]
    RAG --> Core[Internal /docs]
    RAG --> AMP[Advanced Memory MCP]
    AMP --> Knowledge[/knowledge]
    AMP --> Notes[/notes]
    MCP --> Web[SOTA Dashboard]
```

## Setup

1. **Install Dependencies**:
   ```powershell
   cd src/docs_mcp
   pip install -e .
   ```

2. **Run Server**:
   ```powershell
   python -m docs_mcp.server
   ```

3. **Start Dashboard**:
   ```powershell
   ./web_sota/start.bat
   ```

## Federated Intelligence
This server automatically detects sibling repositories. If `advanced-memory-mcp` is located in the same parent directory, its knowledge and notes will be indexed and prioritized during semantic retrieval.

---
**Maintained by**: FlowEngineer sandraschi (Vienna, AT)
**Philosophy**: Materialist Reductionism & Industrial Efficiency.
