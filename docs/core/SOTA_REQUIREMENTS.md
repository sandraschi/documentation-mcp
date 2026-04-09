# SOTA Requirements (Service-Oriented Thinking Architecture)

## 1. Core Principles

To maintain peer technical contributor status, all MCP servers must adhere to the SOTA v12.0 core principles:

1.  **Architecture**: Strict modularity, dual-transport support (STDIO/HTTP), and clean separation of concerns.
2.  **Behavior**: High-quality tool documentation (including the [agentic checklist & pagination](./TOOL_DESIGN_STANDARDS.md) §4–§9) and iterative sampling patterns.
3.  **Operations**: Complete lifecycle management (Lifespans) and correlation tracing.
4.  **Strategy**: Adherence to the [Container Orchestration Strategy](../patterns/CONTAINER_ORCHESTRATION_STRATEGY.md) (Docker Compose vs. K8s).
5.  **Networking**: MANDATORY port range **10700-10800** for all webapps. Frontend and Backend ports MUST be kept together (Adjacent Rule). See [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md) and [WEBAPP_STANDARDS.md](./WEBAPP_STANDARDS.md) for full specifications.
    - [Bugs Depot](../troubleshooting/BUGS_DEPOT.md) - Registry of critical bugs and race conditions.
    - [React Hardening Standards](./REACT_HARDENING.md) - Proactive stability patterns.
    - [REPO_SOTA_BASH (April 2026)](./REPO_SOTA_BASH.md) - Official recipe for repo modernization sprints.

---

## 2. FastMCP 3.1.1+ Standards

### 2.1. Feature Set
- **Prompts**: Context-aware instruction sets registered via `@mcp.prompt()`.
- **Resources**: Dynamic data streams via `@mcp.resource()`.
- **Async Sampling**: Non-blocking tool orchestration using `ctx.sample()`.
- **Skills Provider**: Ability to register and discover local skill directories.

### 2.2. MCP Apps and Prefab UI (Mandatory for Visual Output)

When a server needs **rich cards or layouts inside the chat** (not the standalone webapp on ports **10700–10800**), follow the fleet guide **[MCP Apps, Prefab UI, and FastMCP](../fastmcp/mcp-apps-prefab-ui.md)**:

- **`@mcp.tool(app=True)`** with **`ToolResult(content=..., structured_content=PrefabApp(...))`**
- Requirement for **`prefab-ui`** (e.g. **`[project.optional-dependencies] apps`**).
- **Plain-text fallbacks** are still required for accessibility, but **Prefab UI is now the primary SOTA interface** for all servers returning non-trivial visual data.

Strategic comparison to standalone webapps: **[prefab-vs-webapps.md](../fastmcp/prefab-vs-webapps.md)**. **Use cases and examples (stats, fleet, health, host UX):** **[mcp-apps-prefab-use-cases-and-examples.md](../fastmcp/mcp-apps-prefab-use-cases-and-examples.md)**.

---

## 3. Repository scaffold (Python MCP — build & distribution)

In addition to FastMCP behavior, Python fleet servers SHOULD ship:

- **`uv`** + **`pyproject.toml`** + committed **`uv.lock`**
- Root **`justfile`** (run, test, lint; optional MCPB pack recipe)
- Root **`llms.txt`** + **`llms-full.txt`** (LLM index + full corpus, **both required**) — [DOCUMENTATION_STANDARDS.md](./DOCUMENTATION_STANDARDS.md) §1 · [integrations/llms-txt-manifest.md](../integrations/llms-txt-manifest.md)
- Root **`glama.json`** (Glama discovery)
- **`mcpb pack`** for **`.mcpb`** when Claude Desktop distribution is in scope — see **[PACKAGING_STANDARDS.md §5](./PACKAGING_STANDARDS.md#5-python-mcp-repo-uv-justfile-llmstxt-glama-mcpb-pack)** and **[MCPB_PACKAGING_STANDARDS.md](./MCPB_PACKAGING_STANDARDS.md)**
- **Pre-commit + Ruff** (`.pre-commit-config.yaml`) and **`ty` in CI** (`continue-on-error: true` until green) — **[PACKAGING_STANDARDS.md §6](./PACKAGING_STANDARDS.md#6-optional-ergonomics-pre-commit-ruff-ty-in-ci-non-blocking)** and **[CODE_QUALITY_STANDARDS.md](./CODE_QUALITY_STANDARDS.md)**
- **Industrialization**: See **[REPO_SOTA_BASH.md](./REPO_SOTA_BASH.md)** for the definitive modernization recipe.
