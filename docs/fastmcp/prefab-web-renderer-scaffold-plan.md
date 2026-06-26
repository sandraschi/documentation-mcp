# Plan (deferred): minimal Prefab renderer in a fleet webapp

**Status:** Planned — not implemented in central docs repo  
**Last updated:** 2026-03-28  
**Audience:** Fleet webapp authors (React/Vite + FastAPI) who might want **browser** parity with in-chat Prefab **without** reimplementing full product UI in React by hand.

**Context:** MCP hosts (e.g. Claude Desktop) ship a **Prefab React runtime** for `ToolResult.structured_content`. A **standalone webapp** does not. Browsers do not interpret Prefab JSON automatically. A **DIY renderer** is optional and scoped; a **full** renderer parity with upstream is a large ongoing cost — see discussion in **[prefab-vs-webapps.md](./prefab-vs-webapps.md)** and **[mcp-apps-prefab-ui.md](./mcp-apps-prefab-ui.md)**.

---

## When this plan is worth doing

- You want a **debug** or **preview** page (“what the card looks like outside the MCP client”).
- You want **one** generic viewer for **`structured_content`** from tools you control, accepting **subset** support only.
- You are **not** trying to replace the main webapp UI — same **data**, normal React components, remains the default for dashboards.

**When to skip:** No user-facing need for parity; keep Prefab **in-chat only** and use existing REST/MCP tool JSON in the webapp.

---

## Where to scaffold (repository layout)

| Situation | Suggested location |
|-----------|-------------------|
| Single project (e.g. one `*-mcp` webapp) | `webapp/frontend/src/prefab/` or `src/components/prefab/` — `PrefabRenderer.tsx`, `nodes/`, `types.ts`, `fixtures/` |
| Multiple fleet webapps | Small shared package in the monorepo, e.g. `packages/prefab-lite-renderer/`, imported by each Vite app |

---

## Implementation phases (minimal → safe)

### Phase 1 — Capture the wire format

1. Run a Prefab tool (or add a **dev-only** backend route) that returns **`structured_content`** / serialized **`PrefabApp`** as JSON.
2. Save output to a **committed fixture**, e.g. `fixtures/prefab-book-card.json`, for tests and TypeScript inference.
3. **Do not** guess field names from Python alone — **discriminant** names (`type` vs `component`, children shape) come from the fixture.

### Phase 2 — Types and a single recursive renderer

1. Define a **narrow** `PrefabNode` type (or start from `unknown` + runtime guards).
2. Implement **`renderNode(node): ReactNode`** with a **switch** on the node kind.
3. **First milestone:** only primitives your tools actually emit — typically **`Card`**, **`CardHeader`**, **`CardTitle`**, **`CardContent`**, **`Text`**, **`Image`** (see **[mcp-apps-prefab-ui.md §2.3](./mcp-apps-prefab-ui.md)**).

### Phase 3 — Props and styling

1. Map **`css_class`** → **`className`** (Tailwind); **safelist** unknown classes if using strict Tailwind builds.
2. **`Image`:** `src` (including `data:` URIs), `alt`, optional `width` / `height`.
3. **`Text`:** plain text only — **no** `dangerouslySetInnerHTML** unless you explicitly trust the source (default: **off**).

### Phase 4 — Dev UX and tests

1. **`/dev/prefab`** (or similar) route: load fixture or call dev endpoint; render **`PrefabRenderer`**.
2. **Snapshot** or RTL tests against the fixture so upstream **`prefab-ui`** / payload changes fail CI visibly.

---

## Explicit non-goals (initially)

- Covering **every** Prefab component upstream may add.
- Pixel-perfect match with Claude Desktop / Cursor — **close enough** for preview is enough.
- Parsing Python in the browser — only **JSON** the server already produces.

---

## Maintenance risk

Upstream **`prefab-ui`** or host renderers may change serialization. **Fixture + tests** reduce surprise; full parity still implies **ongoing** alignment work — hence **defer** until a concrete product asks for it.

---

## Related docs

| Doc | Role |
|-----|------|
| [mcp-apps-prefab-ui.md](./mcp-apps-prefab-ui.md) | Fleet standard: `ToolResult`, components, UX |
| [prefab-vs-webapps.md](./prefab-vs-webapps.md) | Prefab vs browser webapps; no auto-converter |
| [fastmcp-31-fleet-capability-map.md](./fastmcp-31-fleet-capability-map.md) | When to use what (Prefab vs webapp) |

---

**Version history**

| Date | Change |
|------|--------|
| 2026-03-28 | Initial plan: where to scaffold, phases, non-goals, related docs. |
