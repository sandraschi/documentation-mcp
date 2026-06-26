# Prefab vs Standalone Webapps (Tentative)

**Status:** Tentative (strategic comparison)  
**Last Updated:** 2026-03-28  
**Applies to:** FastMCP 3.1+ (Prefab integration is early; 3.2 expected to mature)

> **Implementation standard (fleet):** For **how to ship** MCP Apps, **`prefab-ui`**, **`ToolResult`**, optional extras, and UX rules (HTML stripping, multiple `Text` nodes), use **[mcp-apps-prefab-ui.md](./mcp-apps-prefab-ui.md)** — the canonical doc for multi-repo work.  
> **When / why (examples, Claude Desktop UX):** **[mcp-apps-prefab-use-cases-and-examples.md](./mcp-apps-prefab-use-cases-and-examples.md)**.

This section compares **Prefab** (FastMCP’s Python DSL → React in-conversation UI) with **standalone MCP webapps** (e.g. React/Vite + FastAPI on ports 10700–10800) and answers whether an existing webapp can be “turned into” a Prefab.

---

## Comparison

| | Standalone webapps (our pattern) | Prefab (FastMCP 3.1) |
|--|----------------------------------|------------------------|
| **What it is** | Full site: React/Next/Vite + FastAPI, many pages (dashboard, connections, schema, settings, etc.) | UI defined in **Python DSL** → compiles to JSON → rendered by a React runtime **inside** the MCP client |
| **Where it runs** | Its own URL (e.g. port 10700–10800) | **Inside** the MCP client (Cursor, Claude, etc.) as an MCP App (`ui://` / AppConfig) |
| **Stack** | TypeScript/React + backend API | Python-only UI description; no separate frontend repo |
| **Scope** | Full app, multiple routes | Typically **per-tool or per-resource** (one small UI per capability) |

Prefabs are “like” our webapps only in the sense that both are UIs around MCP tools. Prefab is **in-conversation** UI; standalone webapps are **full applications** in the browser.

---

## Can we turn a webapp into a Prefab?

- **No.** There is no converter from “existing React app” → Prefab. Prefab uses a **Python DSL** that compiles to a JSON protocol and is rendered by its own React runtime. An existing React codebase is a different format and cannot be auto-converted.
- **Yes, in a limited way.** You can **re-implement** a subset of a webapp’s behavior as Prefab UIs: describe screens in Python with Prefab’s primitives (forms, tables, buttons, etc.), register them as MCP Apps (e.g. `app=` / AppConfig), and expose them so they appear inside the client. The **existing webapp remains**; Prefab is an extra, in-client UI (e.g. “run this tool and see a small Prefab form in the chat”).

---

## Recommendation

- **Keep standalone webapps** as the primary, full-featured UIs.
- **Use Prefab** only when you want small, in-conversation UIs for specific tools and are willing to author them in the Prefab Python DSL. Prefab is still early (“probably shouldn’t use it yet”); 3.2 is when it is expected to become more viable.

---

## Optional later: preview Prefab-shaped JSON in the browser

If you need a **webapp page** that renders **similar** UI to chat (e.g. debug/preview), you are not forced to hand-design every screen: you can scaffold a **minimal JSON renderer** (subset of components only). That is a **separate** engineering track from shipping Prefab in Python — see the deferred fleet plan **[prefab-web-renderer-scaffold-plan.md](./prefab-web-renderer-scaffold-plan.md)** (fixtures, recursive `renderNode`, non-goals). Full parity with the host’s Prefab runtime remains **heavy**; subset + tests is the intended scope.

---

**References:** [FastMCP 3.1 release (Code to Joy)](https://github.com/PrefectHQ/fastmcp/releases/tag/v3.1.0), [Prefab](https://prefab.prefect.io/).
