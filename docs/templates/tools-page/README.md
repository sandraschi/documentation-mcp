# MCP Tools page (tool harness)

Canonical frontend for **WEBAPP_SOTA_STANDARDS** Tools row: dynamic catalog + schema forms, not hardcoded REST buttons.

**Reference implementation:** `docker-mcp/web_sota` (`tools.tsx`, `tool-runner.tsx`, `lib/tool-schema.ts`).

## Copy map

| Template | Target in repo |
|----------|----------------|
| `tool-schema.ts` | `web_sota/src/lib/tool-schema.ts` (or `webapp/src/lib/`) |
| `ToolsPage.tsx` | `pages/tools.tsx` — export `Tools` |
| `ToolRunnerPage.tsx` | `pages/tool-runner.tsx` — export `ToolRunner` |
| `ToolsHarnessExplainer.tsx` | `components/tools-harness-explainer.tsx` |

Fix `@/` imports to match your Vite aliases. Edit `HARNESS_*` constants in the explainer and `toolCategory` / `relatedPage` / `CATEGORY_ORDER` in `tool-schema.ts`.

## Routes (react-router)

```tsx
<Route path="/tools" element={<Tools />} />
<Route path="/tools/:name" element={<ToolRunner />} />
```

Sidebar label: **Tools** or **MCP Tools**.

## Backend (FastMCP web bridge)

Required routes (same contract as `docker_mcp/web.py` fleet pattern):

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/tools` | `{ tools: [{ name, description?, parameters?, needs_confirm? }] }` |
| GET | `/api/tools/{name}` | `{ tool: ToolMeta }` |
| POST | `/api/tools/{name}` | `{ arguments: object, confirm?: bool }` → `{ result }` |

Tool list MUST come from server introspection, not a static JSON file in the webapp.

## Dashboard optional

```tsx
import { ToolsHarnessExplainer } from "@/components/tools-harness-explainer";
// ...
<ToolsHarnessExplainer variant="dashboard" />
```

## Test IDs (keep for Playwright / demo-vid)

- `tools-loading`, `tool-run-{name}`, `tool-runner-loading`, `tool-runner-run`, `tool-runner-result`

## Anti-pattern

Do **not** ship a Tools page that only calls a handful of hardcoded `/api/...` GETs. That fails the catch-them-all gate and duplicates MCP surface. Use this harness instead; add browse pages only where tables help.
