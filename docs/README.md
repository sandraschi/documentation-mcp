# Documentation Library: The Golden Set

This directory contains the core documentation indexed by the MCP engine. It is organized into functional categories to maximize retrieval precision.

## Content Structure

- **`core/`**: Fundamental standards (e.g., `AGENT_PROTOCOLS.md`, `SOTA_REQUIREMENTS.md`).
- **`fleet/`**: Registries and technical specifications for the MCP fleet repositories.
- **`integrations/`**: Documentation for specific IDE and tool integrations (Cursor, Zed, etc.).
- **`guides/`**: How-to documents and architectural pattern descriptions.

## Contributing

### 1. File Format
All documentation must be in **Markdown (.md)**. Use standard GitHub Flavored Markdown.

### 2. Frontmatter (Optional)
The ingestor recognizes YAML frontmatter for advanced filtering:
```yaml
---
title: "Agent Protocol Specification"
category: "Core"
audience: "Agents/Developers"
skill_candidate: true
---
```

### 3. Standards
- **Conciseness**: Avoid prose; prefer structured lists and code blocks.
- **Cross-linking**: Use absolute URLs or repo-relative paths where possible.
- **Privacy**: Ensure no PII (Private Identifiable Information) or hardcoded local paths are included in files placed here.

## Ingestion Logic
Files in this directory are automatically chunked and embedded when the server starts or when the `reindex_docs` tool is called.
