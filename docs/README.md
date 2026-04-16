# Documentation Library

This directory serves as the static source for the Documentation MCP Hub. It contains the "Golden Set" of protocols, standards, and ecosystem guides.

## Content Structure

### 1. [Standards](./standards/)
Defines the authoritative protocols for the RoboFang ecosystem:
- **`AGENT_PROTOCOLS.md`**: Behavioral and communication standards for AI agents.
- **`SOTA_REQUIREMENTS.md`**: Technical standards for industrial-grade repositories.

### 2. [Operations](./operations/)
Infrastructure and lifecycle documentation:
- **`WEBAPP_PORTS.md`**: Port allocation registry.
- **`BOOTSTRAP.md`**: Environment initialization procedures.

### 3. [Guides](./guides/)
Procedural documentation for common workflows:
- **`MCP_DEVELOPMENT.md`**: Guide for building FastMCP servers.
- **`FLEET_MANAGEMENT.md`**: Handling multi-repo orchestration.

## Contribution
To add new documentation:
1. Create a markdown file in the appropriate subdirectory.
2. Ensure the file contains structured YAML frontmatter (Title, Date, Category).
3. Run `npm run reindex` (or trigger via UI) to update the semantic search index.
