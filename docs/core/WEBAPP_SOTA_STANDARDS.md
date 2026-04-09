---
title: "SOTA WebApp Implementation Standards"
category: standard
status: active
audience: mcp-dev
skill_candidate: true
related:
  - standards/AGENT_PROTOCOLS.md
  - operations/WEBAPP_PORTS.md
  - standards/HOST_APP_LIFECYCLE.md
last_updated: 2026-02-26
---

# SOTA WebApp Implementation Standards (v1.0)

**"Zero Runts Policy" - Mandatory Blueprint for MCP Server Frontends**

All web applications in this repository collection MUST follow these strict guidelines to ensure a premium, unified, and functionally exhaustive user experience.

---

## I. Technical Stack & Architecture

To prevent "runts" (low-quality generated apps), EVERY webapp MUST use:

- **Framework**: [React](https://react.dev/) (Vite-based for speed).
- **Styling**: [TailwindCSS](https://tailwindcss.com/) with a strict "Slate/Amber" or "Zinc/Blue" Dark Theme.
- **Icons**: [Lucide React](https://lucide.dev/) for industrial, clean iconography.
- **Animations**: [Framer Motion](https://www.framer.com/motion/) for micro-interactions and smooth transitions.
- **State Management**: [Zustand](https://github.com/pmndrs/zustand) for lightweight, persistent global state.
- **Connectivity**: Native [MCP SDK](https://github.com/modelcontextprotocol/sdk) wrapper (SSE or Stdio).

---

## II. UI/UX Blueprint (AppLayout)

### 1. Persistent Navigation
- **Retractable Sidebar**: Occupies the left column. Collapsible to icons-only. Contains:
  - App Logo & Version.
  - Core Navigation (Dashboard, Tools, Chat, etc.).
  - Connection Status Indicator.
- **Fixed Topbar**: Always visible. Contains:
  - Breadcrumbs or Page Title.
  - Search (Global Tool/Resource Search).
  - Quick Actions (Toggle Dark Mode, Notification Bell).

### 2. Feedback Systems
- **Global Logger Modal**: A dedicated view (accessed via shortcut or button) showing real-time MCP JSON-RPC logs, `stderr`, and internal events.
- **Help Modal**: Context-aware help system linking to `mcp-central-docs` or local server documentation.
- **Toasts**: Non-intrusive lifecycle alerts (Success, Error, Info).

---

## III. Mandatory Pages & Analytical Views

Every SOTA WebApp MUST implement a dynamic discovery layer. It is forbidden to "hardcode" tool lists.

| Page | Requirement | Depth |
| :--- | :--- | :--- |
| **Dashboard** | Mandatory | Live stats, health, and port reservation status. |
| **Apps Hub** | Mandatory | **Dynamic Fleet Discovery**: Must scan for other active MCP webapps (via `fleet_discovery.py` or equivalent) to populate cards. |
| **Tools Hub** | Mandatory | **Dynamic Analysis**: Must elicit tools from the host server. |
| **Skill** | Mandatory (when server exposes skills) | When the MCP server exposes FastMCP 3.1 skills (Anthropic-style `SKILL.md` as resources), list and display skill content so users and clients know how to use the server. See [§ V. Skill Page](#v-skill-page-fastmcp-31). |
| **LLM Chat** | Mandatory | Context-aware chat with direct server tool-calling. |
| **Status/Audit** | Mandatory | JSON-RPC log viewer and system resources. |

---

## IV. The "Tools Hub" Specification

To prevent "Runts", the Tools page MUST be powerful and analytical:

### 1. Portmanteau Aware
- **Drill-down Logic**: When a tool follows the portmanteau pattern (e.g., `plex_media`), the UI must provide a "drill-down" view illustrating sub-tools, their distinct arguments, and specific docstrings.
- **Visual Separation**: Solo tools (simple utility functions) vs. Portmanteaus (broad orchestration interfaces) must be clearly distinguished.

### 2. Anti-Junk Registry Matching
- **Verification**: Discovered "Fleet" apps MUST be validated against the `Projects` registry in `mcp-central-docs/README.md`.
- **Filtering**: Any active webapp not found in the official registry/structure documentation MUST be relegated to a "Experimental/Untrusted" section or entirely hidden to prevent UI clutter from junk/ghost processes.

### 3. Rich Documentation (PrettyPrint)
- **Docstring Extraction**: Automated parsing of docstrings to extract:
  - Rationale (Why does this tool exist?)
  - Parameters (Detailed type/default info)
  - Examples (Rendered code blocks)
- **Schema Validation**: Display the underlying JSON Schema for every tool.

### 3. Automated Generation (`GrokTools`)
- **Integration**: Webapps should ideally leverage a meta-analysis tool (e.g., `meta-mcp:grok_tools`) to generate the initial "Tools Page" layout based on real-time server introspection. 

- **Dark Mode First**: No white/light backgrounds. Use `#09090b` (Zinc-950) or `#020617` (Slate-950).
- **Glassmorphism**: Use `backdrop-blur` for modals and sidebars.
- **Neon Accents**: Use primary colors like `#f59e0b` (Amber-500) or `#3b82f6` (Blue-500) for interactive elements.
- **Typography**: Primary: `Inter` or `Geist`. Monospace: `JetBrains Mono` for code/logs.

---

## V. Skill Page (FastMCP 3.1)

When the MCP server exposes **skills** (e.g. via FastMCP 3.1 `SkillsDirectoryProvider`, yielding `skill://…/SKILL.md` resources), the webapp MUST provide a **Skill** page.

### 1. Requirement
- **Backend**: `GET /api/skills` — list skills (names and URIs). `GET /api/skills/{name}` — return the markdown content of the given skill.
- **Frontend**: A dedicated page that lists skills, lets the user select one, and renders the skill content as Markdown (so the client/IDE knows how to use the server).
- **Source of content**: Skills are exposed by the server as MCP **resources** (`resources/list`, `resources/read`). The webapp may implement the Skill page by calling the same server (e.g. `list_resources` / `read_resource`) or by exposing the same content via REST for the browser.

### 2. How the MCP client reads and uses the skill
- **Discovery**: The client uses the MCP **Resources** protocol. It sends `resources/list` to the server and receives a list of resource URIs (e.g. `skill://email-compose/SKILL.md`).
- **Fetch**: For each skill URI the client cares about, it sends `resources/read` with that URI. The server returns the resource contents (e.g. the `SKILL.md` markdown).
- **Use**: The client (IDE or agent runtime) injects that content into the LLM context—e.g. as a system message, a retrieved document, or a tool-use hint—so the model has explicit instructions on when and how to call the server’s tools, in Anthropic skill format. The **Skill page** in the webapp is the human-facing mirror: same content, delivered via REST and rendered in the browser for discoverability and reference.

---

## VI. Local Intelligence Integration (MANDATORY)

To leverage the user's existing compute investment (RTX 4090/3090), every SOTA WebApp MUST implement **Local Intelligence Auto-Discovery**.

### 1. The "Glom On" Pattern
- **Detection**: The webapp must scan standard local ports to detect running inference engines:
  - `11434` (Ollama)
  - `1234` (LM Studio)
  - `8000` (vLLM/Compat)
- **Zero-Config Binding**: If a local LLM is detected, the webapp MUST automatically configure itself to use it for semantic operations (summarization, tagging, analysis) without forcing the user to manually enter API keys or URLs.
- **Graceful Fallback**: If no local LLM is found, features requiring intelligence should disable gracefully.

### 2. The "GPU Opportunity" Pattern
- **Hardware Awareness**: If the webapp detects a high-performance GPU (NVIDIA RTX 3060+) but *no* running local LLM:
  - **Prompt**: It MUST display a non-intrusive suggestion: *"High-performance GPU detected. Install Ollama/LM Studio to unlock AI features for free."*
  - **Education**: Link to `mcp-central-docs/standards/LOCAL_LLM_STANDARDS.md` or provide a brief "Getting Started" guide to save the user cloud API costs.

### 3. Semantic Features
- **Usage**: Use the discovered local LLM for:
  - Content summaries.
  - Smart filtering/sorting.
  - Natural language querying of the dataset.
  - Context-aware chat with direct server tool-calling.

### 4. Hybrid Intelligence Strategy (Cloud + Local)
- **Mandatory Settings**: The "AI Settings" page MUST explicitly support configuration for:
  - **Local**: Ollama/LM Studio (Auto-Discovered)
  - **Cloud**: OpenAI, Anthropic, Google/Gemini
- **Routing**: The webapp should intelligently route requests (e.g., Local for bulk summarization, Cloud for complex reasoning) or allow user preference overrides.

---

## VII. Startup & Deployment

- **start.ps1**: MUST clear the targeted port (10700-10800 reservoir) before binding.
- **start.bat**: Shell wrapper for Windows "Double-Click" convenience.
- **Port Adjacency (MANDATORY)**: Projects requiring both Frontend and Backend MUST allocate adjacent ports (e.g., 10792/10793) to ensure logical grouping.

---


---

## VIII. SOTA Standard Kit (Universal Common Pack)

The **SOTA Standard Kit** is the mandatory "pack" that must be added to all webapps to maintain ecosystem parity.

| Component | Standard Implementation |
| :--- | :--- |
| **FastMCP 3.1** | Context-aware tools, `run_stdio_async`, and Sampling API support. |
| **Local LLM Chat** | Built-in chat interface with "Glom On" auto-binding to Ollama. |
| **Embedded RAG** | **LanceDB** integration for document indexing (Local first). |
| **Apps Hub** | Dynamic Fleet Discovery of all active apps (filtered by `Projects` registry). |
| **Sampling Patterns** | Tools must use `ctx.sample()` for autonomous reasoning steps. |
| **Tools Page** | Standardized `GrokTools` viewer with portmanteau support. |
| **Skill Page** | When the server exposes skills (FastMCP 3.1), list and display skill content: `GET /api/skills`, `GET /api/skills/{name}`; frontend renders markdown. See [§ V. Skill Page](#v-skill-page-fastmcp-31). |
| **Help System** | Unified help modal with deep-links to documentation. |

### Golden Template Lifecycle
1.  **Detect**: Scan for Ollama (11434) and registered Fleet peers.
2.  **Index**: Crawl local `docs/` and ingest into LanceDB.
3.  **Bridge**: Expose MCP capabilities through the Unified Gateway.
4.  **Render**: Populate the AppLayout with dynamic navigation and tool cards.

---

**Owner:** Sandra Schipal  
**Last Updated:** 2026-03-04
