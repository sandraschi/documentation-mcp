# json-render - Evaluation (external tool, not adopted)

**Status:** Evaluated - **NOT adopted** (see section 4)
**Last updated:** 2026-09-21
**Audience:** Fleet maintainers, MCP Apps / Prefab owners, webapp authors
**Source basis:** repo README + npm page for `@json-render/mcp`. **Source code was NOT reviewed** - treat API detail as claimed by the vendor, not verified.

Upstream: [vercel-labs/json-render](https://github.com/vercel-labs/json-render) - "The Generative UI framework". Apache-2.0. Listed as a Vercel **Labs** product.

---

## 1. What it is

A **Generative UI** framework. You define a **catalog** (Zod schemas for the components and actions the AI is allowed to use); a model emits a **JSON spec** constrained to that catalog; a renderer turns the spec into UI. The value proposition is guardrails and streaming, not the rendering - the rendering is deliberately boring.

Scale: roughly 30 packages in one pnpm/turbo monorepo. Renderers for React, Vue, Svelte, Solid, React Native, Ink (terminal), Remotion (video), React PDF, React Email, Image (SVG/PNG via Satori), and React Three Fiber (3D). Pre-built shadcn/ui component sets, state adapters (Zustand, Redux, Jotai, XState), devtools, a YAML wire format, and an MCP Apps package.

Repo signal: 17.9k stars, 938 forks, 228 commits, 62 open issues, 47 open PRs.

---

## 2. The only fleet-relevant part: `@json-render/mcp`

Everything else in the monorepo is webapp-side and not relevant to a Python/FastMCP fleet.

- **Version:** 0.21.0, Apache-2.0, 13 published versions, pre-1.0.
- **What it does:** `createMcpApp({ name, version, catalog, html })` returns a fully-configured `McpServer` (from `@modelcontextprotocol/sdk`) exposing a json-render tool plus a UI resource. Client side, a React hook `useJsonRenderApp()` runs **inside an iframe**, receives tool results, and holds the current spec.
- **Target protocol:** the **same MCP Apps extension** the fleet already targets (`modelcontextprotocol.io/docs/extensions/apps`).
- **Server runtime:** **Node / TypeScript** (`new StdioServerTransport()`).
- **Packaging:** the UI is bundled to a **single HTML file** (Vite + `vite-plugin-singlefile`) and passed to `createMcpApp` as the `html` option.
- **Claimed client support:** Claude, ChatGPT, VS Code (Copilot), Cursor, Goose, Postman.

---

## 3. `json-render/mcp` vs fleet Prefab - same protocol, inverted architecture

| Axis | Fleet Prefab | `json-render/mcp` |
|---|---|---|
| Target protocol | MCP Apps extension | MCP Apps extension |
| Server language | Python (FastMCP) | TypeScript / Node |
| What the server sends | `PrefabApp` component tree as `structured_content` | a bundled **HTML application** + a tool |
| Who ships the renderer | **the MCP host** (Prefab React runtime) | **the app itself** (iframe) |
| Build step | none (`uv sync`) | npm / Vite single-file bundle |
| UI authored in | Python DSL (`prefab_ui.components`) | TSX components + Zod catalog |
| Fleet status | mandated core dep `prefab-ui>=0.14.0` | not present |

**The load-bearing difference:** Prefab pushes **data** and relies on the host's renderer. json-render pushes a **self-contained HTML application**. Same extension, opposite answer to "who owns the rendering".

---

## 4. Why it does not fit the fleet (verdict)

1. **Server-language mismatch.** Every fleet MCP server is Python/FastMCP (`uv run python server.py`). `createMcpApp` is a Node server. Adopting it means either a Node sidecar per server or a parallel non-Python stack - neither is on the roadmap.
2. **Duplicate MCP Apps mechanism.** Prefab is **fleet-mandatory** with a list/status/stats coverage rule ([SOTA §2.2](../standards/SOTA_REQUIREMENTS.md#22-mcp-apps-and-prefab-ui-fleet-mandatory)). Two competing implementations of the same protocol extension is precisely the drift the standards exist to prevent.
3. **Maturity.** Pre-1.0, 228 commits, 62 open issues, 47 open PRs, "LABS PRODUCT" badge. 17.9k stars measures the launch, not stability.
4. **Cost / benefit.** The *generative* part is the only capability Prefab lacks. Nothing in the fleet currently needs prompt-generated UI, so the added surface buys nothing.
5. **Wire compatibility unverified.** Whether a json-render payload is compatible with the host's Prefab rendering was not confirmed, and is not worth confirming for a rejected option.

**Net:** correct tool, wrong fleet. Our instinct ("not useful for OUR fleet") is right.

---

## 5. What IS worth taking (patterns, no dependency)

These are transferable even though we take no dependency.

1. **Catalog-as-guardrail + generated prompt.** A Zod schema is both the validator and the source of the system prompt (`catalog.prompt()`). The model *cannot* emit a component outside the catalog. This is the cleanest statement of the "constrain the model to a schema" pattern available, and it applies to any fleet tool that has an LLM emit structured output.
2. **`SpecStream` progressive rendering.** `createSpecStreamCompiler()` consumes partial JSON chunks and returns a progressively-complete spec. **Important distinction:** the fleet chat standard already covers **token streaming** ([§1.10](../standards/rules/chat_skills_prefab_standard.md), RECOMMENDED, implemented in roughly 25-30 fleet repos) and **resilient/reconnecting streaming** (§9.1, RECOMMENDED, zero impls). What it does **not** have is **generative UI streaming** - a model emitting a *UI spec* that renders progressively. That is a different capability from prose streaming, and the fleet already has a safer answer to "UI in chat": tool-result-driven Prefab cards (§9.2). Take SpecStream as a pattern, not as a gap to be filled.
3. **Single-file HTML packaging.** `vite-plugin-singlefile` -> one HTML -> one MCP App UI resource. A tidy answer to "how do I ship an HTML-based in-chat UI", relevant if the fleet ever ships HTML MCP Apps rather than Prefab trees.
4. **One catalog, many renderers.** React / Vue / Svelte / Solid / RN / Ink / PDF / email / image / 3D from a single spec. Independent evidence for the "UI as data" thesis the Prefab standard is already built on.
5. **Devtools.** Spec tree + state editor + action log + stream log inspector. A good model for a future `/dev/prefab` preview page.

---

## 6. Relationship to the deferred browser-renderer plan

[prefab-web-renderer-scaffold-plan.md](../archive/fastmcp/prefab-web-renderer-scaffold-plan.md) proposes a **minimal Prefab JSON renderer** in a fleet React webapp for browser preview, and warns that **full parity with upstream is a large ongoing cost**.

json-render is a mature, maintained implementation of exactly that concept. It therefore (a) **validates the plan's cost warning** - the destination is a 30-package monorepo, and (b) shows how much would have to be built.

**It is not a drop-in for that plan.** json-render renders *json-render* specs, not Prefab JSON; the two wire formats are unrelated. Do not revive the deferred plan on the strength of this doc. Record it and move on.

---

## 7. For a beginning vibecoder - assessment

**Verdict: yes, commendable - with caveats.**

Why it is good teaching material:

- It solves the actual hard problem: **constraining an LLM to emit valid UI** instead of plausible garbage. That is the insight worth absorbing.
- The catalog + Zod + `catalog.prompt()` loop is a clean, correct mental model: *define the guardrails, let the model generate within them*.
- The single-file HTML -> MCP App packaging trick is elegant and genuinely clever.
- One catalog rendering to ten platforms is impressive, and honest about what "UI as data" buys you.

Caveats for a beginner:

- It is a ~30-package pnpm/turbo monorepo with a pre-1.0 API. Not a first project.
- It assumes working familiarity with React, Vite, and MCP concepts.
- The demo requires a working MCP host before anything is visible.
- Docs are good but assume you already know why you want this.

**Beginner recommendation:** excellent to **read** for the catalog-guardrail pattern; **not** a gentle first build. The lesson is portable; the framework is not the point.

---

## 8. If it were ever adopted (options, all currently rejected)

Ranked by cost, lowest first:

1. **Pattern extraction, no dependency.** Reimplement the catalog+prompt idea in Python for fleet LLM tools. Highest value, near-zero cost.
2. **Single experimental repo.** Prototype a generative-UI page in one webapp; pin exact versions; do not touch the fleet standard.
3. **Node sidecar for one server.** Highest cost, lowest value - rejected.
4. **Fleet-wide.** Rejected: conflicts directly with the Prefab mandate.

---

## 9. Related docs

| Doc | Role |
|---|---|
| [../fastmcp/mcp-apps-prefab-ui.md](../fastmcp/mcp-apps-prefab-ui.md) | Fleet standard: MCP Apps, `ToolResult`, `PrefabApp`, list/status/stats coverage |
| [../standards/SOTA_REQUIREMENTS.md](../standards/SOTA_REQUIREMENTS.md) | §2.2 - Prefab fleet mandate |
| [../fastmcp/mcp-apps-prefab-use-cases-and-examples.md](../fastmcp/mcp-apps-prefab-use-cases-and-examples.md) | When Prefab is worth it, host UX, examples |
| [../archive/fastmcp/prefab-vs-webapps.md](../archive/fastmcp/prefab-vs-webapps.md) | Prefab vs standalone webapps; no auto-converter |
| [../archive/fastmcp/prefab-web-renderer-scaffold-plan.md](../archive/fastmcp/prefab-web-renderer-scaffold-plan.md) | Deferred browser renderer plan (section 6 above) |
| [../standards/rules/chat_skills_prefab_standard.md](../standards/rules/chat_skills_prefab_standard.md) | Chat page + Prefab UI standard |

---

## 10. External references

- **Repo** - [vercel-labs/json-render](https://github.com/vercel-labs/json-render)
- **Site** - [json-render.dev](https://json-render.dev)
- **MCP Apps package** - [@json-render/mcp on npm](https://www.npmjs.com/package/@json-render/mcp)
- **MCP Apps spec** - [modelcontextprotocol.io - Apps extension](https://modelcontextprotocol.io/docs/extensions/apps)

---

**Version history**

| Date | Change |
|------|--------|
| 2026-09-21 | Initial evaluation. Verdict: not adopted; pattern extraction only. |
