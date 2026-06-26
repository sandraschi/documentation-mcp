# Documentation Library

Self-contained RAG corpus for **documentation-mcp**. Synced from the private fleet hub (`mcp-central-docs`); the server indexes **`documentation-mcp/docs`** by default.

## Content Structure

| Area | Purpose |
|------|---------|
| [`core/`](./core/) | Fleet standards (agent protocols, FastMCP, webapp, quality) |
| [`projects/`](./projects/) | Per-repo README, STATUS, CHANGELOG, PRD mirrors |
| [`integrations/`](./integrations/) | External tools and fleet service integration guides |
| [`patterns/`](./patterns/) | Reusable MCP architecture patterns |
| [`operations/`](./operations/) | Ports, bootstrap, fleet control plane |
| [`ecosystem/`](./ecosystem/) | IDE and agent-platform research |
| [`fastmcp/`](./fastmcp/) | FastMCP 3.x feature reference |
| [`robotics/`](./robotics/) | Yahboom, digital twin, hardware bringup |
| [`getting-started/`](./getting-started/) | Onboarding |
| [`guides/`](./guides/) | Procedural workflows |
| [`safety/`](./safety/) | High-risk server safety protocols |
| [`mcp-technical/`](./mcp-technical/) | MCP protocol technical notes |
| [`troubleshooting/`](./troubleshooting/) | Fleet debugging playbooks |
| [`architecture/`](./architecture/) | System architecture references |
| [`pico/`](./pico/) | Pico 4 / WebXR teleop |
| [`deployment/`](./deployment/) | Deployment patterns |
| [`monitoring/`](./monitoring/) | Observability |
| [`skills/`](./skills/) | Fleet skill documentation |
| [`research/`](./research/) | Public research notes |
| [`adn-notes/`](./adn-notes/) | Advanced Memory / ADN notes |

**Not copied:** `docs-private`, `scratch`, `politics`, archives, session logs, `.bak` files.

## RAG indexing

| Setting | Where |
|---------|--------|
| Primary root | `documentation-mcp/docs` (`DOCS_ROOT` overrides) |
| Extra paths | Webapp **Settings → Extra RAG paths**, or `DOCS_EXTRA_PATHS` env |
| Advanced Memory | Settings checkbox or `DOCS_FEDERATE_MEMORY=1` |

After changes, run **Reindex** in the webapp or call `reindex_docs`.

## Contribution

1. Add markdown under the appropriate subdirectory.
2. Use YAML frontmatter where applicable.
3. Prefer relative links within `docs/`.
4. Reindex so semantic search picks up changes.
