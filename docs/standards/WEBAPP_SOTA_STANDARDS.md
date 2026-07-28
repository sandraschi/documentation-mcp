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
  - standards/WEBAPP_COMPANION_MODE.md
last_updated: 2026-06-16
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
- **Package Manager**: **Bun** (replaces npm). Lockfile `bun.lock` committed. Vite stays as dev server/bundler. See `standards/BUN_STANDARDS.md`.

---

## II. UI/UX Blueprint (AppLayout)

### 1. Persistent Navigation
- **Retractable Sidebar**: Occupies the left column. Collapsible to icons-only. Contains:
  - App Logo & Version.
  - Core Navigation (Dashboard, Tools, Chat, etc.).
  - Connection Status Indicator.
  - **Collapse toggle MUST be at the top** of the sidebar, immediately after the logo/header area (not at the bottom). Use `ChevronLeft`/`ChevronRight` Lucide icons. Bottom-positioned toggles require scrolling to find and break discoverability — this is a fleet-wide UX defect.
- **Fixed Topbar**: Always visible. Contains:
  - Breadcrumbs or Page Title.
  - Search (Global Tool/Resource Search).
  - Quick Actions (Toggle Dark Mode).
  - **Companion Mode toggle** (`Minimize2`/`Maximize2` icon) and **Pop Out** (`ExternalLink` icon) — see [WEBAPP_COMPANION_MODE.md](./WEBAPP_COMPANION_MODE.md).
  - **Emergency Stop (Kill Switch)**: (Conditional) Mandatory for **Audio, Video, and Robotics** fleets. A prominent red button that immediately halts all media/mechanical processes and cancels background timers. *Safety First.*

> **Topbar as global action strip (suggestion, not rule):** Not every app needs a Settings or Logs page when the action is one click away. Consider putting theme toggle, backend connection status dot, fleet apps hub, and quick modals (Help, Logs) in the topbar instead of dedicating sidebar slots to them. This keeps the sidebar lean for navigation while the topbar handles global state and meta-actions. Examples: auth indicator, backend health dot (green/red), fleet apps dropdown, help (? icon → modal), logs (terminal icon → overlay).

### 2. Feedback Systems
- **Global Logger Modal**: A dedicated view (accessed via shortcut or button) showing real-time MCP JSON-RPC logs, `stderr`, and internal events.
- **Help Modal**: Context-aware help system linking to `mcp-central-docs` or local server documentation.
- **Toasts**: Non-intrusive lifecycle alerts (Success, Error, Info).

---

## III. Mandatory Pages & Analytical Views

Every SOTA WebApp MUST implement a dynamic discovery layer. It is forbidden to "hardcode" tool lists.

### Catch-them-all gate (HARD — new repos)

A webapp that only ships domain pages (e.g. Outbox + Settings stub) is a **runt** and fails the new-repo gate. Before calling a scaffold "done", verify **all** of the following exist as routes with real UI (not empty placeholders):

| # | Page / surface | Min bar | Backend |
|---|----------------|---------|---------|
| 1 | **Dashboard** | Hero (brand + one headline + one CTA) + KPI stat cards | `GET /api/dashboard` or equivalent stats |
| 2 | **Inbox** (or domain inbox) | List + empty state | domain notifications/list API |
| 3 | **Tools** | Dynamic tool list; portmanteau drill-down | `GET /api/tools` |
| 4 | **Skills** | List + render `SKILL.md` | `GET /api/skills` |
| 5 | **Chat** | Skill-first, personalities, localStorage history | local LLM and/or `POST /api/llm/chat` |
| 6 | **Settings** | Backend health + **LLM provider/model** probe (Ollama/LM Studio/vLLM) | `GET /api/health`, `GET /api/llm/providers` |
| 7 | **Help** | Full **page** (architecture, ports, env, troubleshooting) — Help **modal** alone is not enough | optional |
| 8 | **Logs** | Logger modal or page (Ctrl+L) | `GET /api/logs` |
| 9 | Domain pages | Whatever the product needs (Compose, Outbox, …) | as required |
| 10 | **AI-assisted compose** (when Compose exists) | Assist button → local LLM rewrite | `POST /api/compose/assist` or chat proxy |

**Also mandatory:** retractable AppLayout sidebar + topbar health dot; `data-testid` on primary controls; Zustand LLM store (`lib/provider.ts` + `store/llm.ts`).

**Apps Hub** remains mandatory when the fleet discovery helper is available; otherwise ship a stub route labeled Experimental and file a follow-up — do **not** drop Chat/Settings/Help to "finish faster."

| Page | Requirement | Depth |
| :--- | :--- | :--- |
| **Dashboard** | Mandatory | Hero + live KPIs, health, dry-run/config badges. |
| **Apps Hub** | Mandatory | **Dynamic Fleet Discovery**: Must scan for other active MCP webapps (via `fleet_discovery.py` or equivalent) to populate cards. |
| **Tools Hub** | Mandatory | **Dynamic Analysis**: Must elicit tools from the host server. |
| **Skill** | Mandatory (when server exposes skills) | When the MCP server exposes FastMCP 3.1 skills (Anthropic-style `SKILL.md` as resources), list and display skill content so users and clients know how to use the server. See [§ V. Skill Page](#v-skill-page-fastmcp-31). |
| **LLM Chat** | Mandatory | Context-aware chat; skill-first; local provider. See `rules/chat_skills_prefab_standard.md`. |
| **Settings** | Mandatory | Health + Local Intelligence provider/model UI (§ VI). |
| **Help** | Mandatory | Dedicated Help **page** plus optional Help modal. |
| **Inbox** | Mandatory when the product has inbound events | Notifications / queue / messages UI. |
| **Status/Audit** | Mandatory | JSON-RPC / ring log viewer (modal OK). |

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

To leverage the user's existing compute investment (RTX 4090/3090), every SOTA WebApp MUST implement **Local Intelligence Auto-Discovery** with a switchable provider UI and model selection populated from the detected engine.

### 1. Provider Detection ("Glom On")

The webapp MUST probe these standard ports on mount and display results in the Settings UI:

| Provider | Port | Probe endpoint | Timeout |
|----------|------|----------------|---------|
| **Ollama** | `11434` | `GET /api/tags` | 3s |
| **LM Studio** | `1234` | `GET /v1/models` | 3s |
| **vLLM** | `8000` | `GET /v1/models` | 3s |

Each provider is shown with a status indicator (Detected / Not found / Probing...).

**UI requirements:**
- Show provider name, port, and a colored status icon:
  - Green check + "Detected" when the probe succeeds
  - Gray "Not found" when the probe fails or times out
  - Animated pulse while probing
- If NO provider is detected, show a non-intrusive amber prompt: *"Install Ollama or LM Studio to enable AI features."*

### 2. Provider Selection (Switchable)

The user MUST be able to select which detected provider to use as the active inference engine:

- **Provider dropdown**: `<select>` element populated with all detected providers. Label: "Provider". `data-testid="llm-provider-select"`.
- **Default selection**: The first detected provider in priority order (Ollama > LM Studio > vLLM).
- **Persistence**: Selected provider is saved to `localStorage` (key: `llm_provider`) and restored on page load.
- **No detected provider**: Dropdown shows "No local LLM detected" as disabled option.

### 3. Model Discovery & Selection

When a provider is selected, the webapp MUST fetch the available models from that provider and populate a model dropdown:

- **Model fetch endpoint**:
  - Ollama: `GET {base}:11434/api/tags` → extract `models[].name`
  - LM Studio: `GET {base}:1234/v1/models` → extract `data[].id`
  - vLLM: `GET {base}:8000/v1/models` → extract `data[].id`
- **Model dropdown**: `<select>` element populated with model names. Label: "Model". `data-testid="llm-model-select"`.
- **Default selection**: The first model in the list. If a model is already saved in `localStorage` (key: `llm_model`) and still exists in the fetched list, restore that one.
- **Persistence**: Selected model is saved to `localStorage` and restored on page load.
- **Re-fetch on provider change**: When the user switches providers, re-fetch the model list and reset the selection.

### 4. Data Flow

```
onMount → probe all providers (parallel, 3s timeout)
       → set detected provider list
       → if saved provider is still detected, select it; else select first detected
       → fetch models for selected provider
       → if saved model exists in list, restore it; else select first model

onProviderChange → save to localStorage
                → fetch models for new provider
                → reset model selection to first

onModelChange → save to localStorage
```

### 5. The "GPU Opportunity" Pattern

- **Hardware Awareness**: If the webapp detects a high-performance GPU (NVIDIA RTX 3060+) but *no* running local LLM:
  - **Prompt**: It MUST display a non-intrusive suggestion: *"High-performance GPU detected. Install Ollama/LM Studio to unlock AI features for free."*
  - **Education**: Link to `mcp-central-docs/standards/LOCAL_LLM_STANDARDS.md` or provide a brief "Getting Started" guide to save the user cloud API costs.

### 6. Chat Integration

The selected provider + model pair is used as the chat completion backend for the Chat page (see [Chat, Skills, and Prefab UI Standard](rules/chat_skills_prefab_standard.md)):

- Chat sends requests to `{provider_base}:{port}/v1/chat/completions` with the selected model
- If no provider is detected, the Chat page shows a disabled state: "No local LLM detected. Start Ollama or LM Studio."
- The Chat page MUST include a provider/model status indicator in the controls bar

### 7. Settings UI Data Contract

```typescript
interface SettingsLLMSection {
  // Detection results
  detectedProviders: Array<{ name: string; port: number; base: string }>;
  providerStatus: Record<string, "probing" | "detected" | "not_found">;

  // Selection (persisted to localStorage)
  selectedProvider: string;   // key: "llm_provider"
  selectedModel: string;       // key: "llm_model"

  // Model list (fetched from selected provider)
  availableModels: string[];
}
```

---

## VII. Startup & Deployment

- **start.ps1**: MUST clear the targeted port (10700-11500 reservoir) before binding.
- **start.bat**: Shell wrapper for Windows "Double-Click" convenience.
- **Port Adjacency (MANDATORY)**: Projects requiring both Frontend and Backend MUST allocate adjacent ports (e.g., 10792/10793) to ensure logical grouping.

---


---

## VIII. SOTA Standard Kit (Universal Common Pack)

The **SOTA Standard Kit** is the mandatory "pack" that must be added to all webapps to maintain ecosystem parity.

| Component | Standard Implementation |
| :--- | :--- |
| **FastMCP 3.2** | Context-aware tools, `run_stdio_async`, Sampling API, GenerativeUI provider (`prefab-ui>=0.14.0`). |
| **Local LLM Chat** | Built-in chat interface with "Glom On" auto-binding to Ollama. |
| **Embedded RAG** | **LanceDB** integration for document indexing (Local first). |
| **Apps Hub** | Dynamic Fleet Discovery of all active apps (filtered by `Projects` registry). |
| **Sampling Patterns** | Tools must use `ctx.sample()` for autonomous reasoning steps. |
| **Tools Page** | Standardized `GrokTools` viewer with portmanteau support. |
| **Skill Page** | When the server exposes skills (FastMCP 3.1), list and display skill content: `GET /api/skills`, `GET /api/skills/{name}`; frontend renders markdown. See [§ V. Skill Page](#v-skill-page-fastmcp-31). |
| **API Docs Page** | FastAPI servers only: `/api-docs` page with embedded Swagger UI + ReDoc iframe, dark theme override, quick-ref strip, "Open in browser" link. Sidebar entry mandatory. See [§ IX. API Docs Page](#ix-api-docs-page-fastapi-servers-only). |
| **Help System** | Unified help modal with deep-links to documentation. |

### Golden Template Lifecycle
1.  **Detect**: Scan for Ollama (11434) and registered Fleet peers.
2.  **Index**: Crawl local `docs/` and ingest into LanceDB.
3.  **Bridge**: Expose MCP capabilities through the Unified Gateway.
4.  **Render**: Populate the AppLayout with dynamic navigation and tool cards.

---

## IX. API Docs Page (FastAPI servers only)

For any server using FastAPI, the webapp MUST expose an **API Docs** page that surfaces the auto-generated Swagger UI and ReDoc. This is the primary benefit of choosing FastAPI — don't bury it.

### Requirements

- **Sidebar entry**: `API Docs` link with `Code2` icon, pointing to `/api-docs`. Positioned between Chat and Logs.
- **`/api-docs` page**: Embeds Swagger UI and ReDoc via iframe, proxied through the frontend dev server (add `/docs`, `/docs/:path*`, `/openapi.json`, `/redoc` rewrites to `next.config.js` or `vite.config.ts`).
- **Dark theme override**: Inject fleet dark CSS (`#09090b` background, Zinc palette, Amber accents, method colour coding) into the iframe `contentDocument` on load. Graceful fallback if cross-origin blocks injection — always show an "Open in browser" direct link to `http://localhost:{backend_port}/docs`.
- **View toggle**: Swagger UI (default) ↔ ReDoc — both useful, different reading modes.
- **Quick-ref strip**: A scrollable row of representative endpoints above the iframe so the shape of the API is visible at a glance without expanding anything.
- **"Open in browser" link**: Always present — direct URL to backend `/docs`, opens in new tab. This is the escape hatch if the iframe is cramped or the CSS injection fails.

### Proxy rewrites (Next.js)

```js
// next.config.js
{ source: '/docs',        destination: 'http://127.0.0.1:{PORT}/docs' },
{ source: '/docs/:path*', destination: 'http://127.0.0.1:{PORT}/docs/:path*' },
{ source: '/openapi.json',destination: 'http://127.0.0.1:{PORT}/openapi.json' },
{ source: '/redoc',       destination: 'http://127.0.0.1:{PORT}/redoc' },
```

### Proxy rewrites (Vite)

```ts
// vite.config.ts
'/docs':        { target: 'http://localhost:{PORT}', changeOrigin: true },
'/openapi.json':{ target: 'http://localhost:{PORT}', changeOrigin: true },
'/redoc':       { target: 'http://localhost:{PORT}', changeOrigin: true },
```

### MCP tool (optional but recommended)

Add a `show_api_docs` or `open_swagger_docs` tool that returns the Swagger URL — useful for Claude to surface it without the user needing to remember the port:

```python
@mcp.tool()
async def show_api_docs(ctx: Context) -> dict:
    """Return the Swagger UI and ReDoc URLs for this server's REST API."""
    base = f"http://localhost:{cfg.backend_port}"
    return {"swagger": f"{base}/docs", "redoc": f"{base}/redoc", "openapi": f"{base}/openapi.json"}
```

### Starlette servers

Starlette has no built-in docs. If a Starlette server grows to the point where docs are useful, that's the signal to migrate to FastAPI — see the decision matrix in `STARLETTE_NO_PYDANTIC_STANDARD.md`. Do not manually wire Swagger into a Starlette app.

---

**Owner:** Sandra Schipal  
**Last Updated:** 2026-05-31
