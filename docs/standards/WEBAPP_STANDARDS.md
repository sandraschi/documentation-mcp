# SOTA Webapp Standards (The Blueprint)

## 1. Blueprint Architecture

To prevent UI fragmentation and state management "trips" in React, all SOTA webapps MUST adhere to the following layout and component structure.

### 1.1. Shell Layout (The "Iron Shell")
- **Sidebar**: Collapsible, left-aligned. Contains primary navigation (`Home`, `Tools`, `Apps`, `Settings`, `Help`).
- **Topbar**: Fixed height. Contains Page Title, Breadcrumbs, System Status (MCP/GPU), and User Profile/Persona.
- **Main View**: Scrollable area for page-specific content.
- **Logger Panel**: Sticky/Expandable bottom panel. Real-time stream of backend events, console logs, and tool execution status.

### 1.2. Webapp Lifecycle (MANDATORY)
Every webapp MUST include:
1.  **`start.ps1`**: PowerShell script that:
    - Clears target ports from zombies/squatters (using `Stop-Process` on listeners).
    - Triggers the build (if necessary).
    - Launches both Frontend and Backend substrates.
    - **Backend readiness (MANDATORY)**: After spawning the ASGI process, **wait until the backend is actually listening** before starting Vite — e.g. **TCP connect** to the API port, or **`GET /api/v1/health`** (or repo-specific health) when no auth is required. Cold **`uv run`** and heavy imports routinely exceed a fixed sleep; without this step, Vite’s dev proxy logs **`ECONNREFUSED`** to **`127.0.0.1:<backend>`**. Use a bounded wait (e.g. 60–90s) and **exit with a clear error** if the backend never binds (operator checks the uvicorn window). Set **`-WorkingDirectory`** on the backend child to the **repository root** so **`uv run`** resolves the project reliably.
    - **Auto-Open Browser**: Launches a non-blocking background polling task to open the default browser only when the Vite frontend is responsive (200 OK), eliminating cold-start "Connection Refused" errors **for the HTML shell** (distinct from API readiness above).
2.  **`start.bat`**: Double-click wrapper for `start.ps1`.
3.  **`.gitignore`**: Root rules MUST exclude **`node_modules/`** (and nested `**/node_modules/`), local envs, and build caches — see **[GITIGNORE_STANDARDS.md](./GITIGNORE_STANDARDS.md)**. Never commit npm/pnpm dependencies or Vite pre-bundles.

### 1.3. Backend Substrate (MANDATORY)
Every webapp MUST have a FastAPI-powered backend substrate (typically on port **10860** or adjacent to the frontend) providing:
- **Unified Gateway**: Bridges MCP SSE transport with custom REST/WebSocket endpoints.
- **Fleet Discovery**: Implements the [Glama discovery protocol](https://glama.ai) with standardized `glama.json` manifests.
- **State Continuity**: Persistence for session state and prompt refinements.

### 1.4. Capability Introspection Endpoint (MANDATORY)

Every MCP-backed webapp backend MUST expose:

- **`GET /api/capabilities`**

This endpoint is the runtime source of truth for what the server actually supports right now. UIs and agents MUST prefer this endpoint over static assumptions in docs.

Required response shape (minimum):

```json
{
  "status": "ok",
  "server": { "name": "my-mcp", "version": "x.y.z", "fastmcp": "3.4+" },
  "tool_surface": {
    "total": 0,
    "portmanteau_count": 0,
    "atomic_count": 0,
    "portmanteau_tools": [],
    "atomic_tools": []
  },
  "features": {
    "sampling": false,
    "agentic_workflows": false,
    "prompts": false,
    "resources": false,
    "skills": false
  },
  "inventory": {
    "workflow_tools": [],
    "prompt_names": [],
    "resource_uris": [],
    "skill_uris": []
  },
  "runtime": {
    "transport": "stdio|http|dual",
    "surface_mode": "portmanteau|atomic|both"
  },
  "timestamp": "2026-03-26T00:00:00Z"
}
```

Rules:

1. **No secrets**: never expose credentials, tokens, or raw environment variable values.
2. **Runtime truth only**: values must reflect currently registered tools/capabilities.
3. **Stable keys**: keep field names stable for webapp compatibility; add new keys without breaking old ones.
4. **Feature booleans + inventory**: return both high-level flags and concrete lists.

Webapp usage requirements:

1. Fetch `/api/capabilities` on app load and cache it.
2. Use it to conditionally show/hide unsupported pages and actions.
3. Show a dedicated capabilities status panel (sampling/workflows/prompts/resources/skills).
4. Use `tool_surface` counts in dashboard/settings pages to avoid UI-doc drift.

Implementation note:

- This pattern exists because host tool visibility constraints changed over time (older limits like ~50/~100). Capability introspection allows each repo to adapt dynamically (portmanteau, atomic, or hybrid) without hardcoded UI assumptions.

Verification:

- **Assess & Fix** (`repo-assess-and-fix.md` §1B) checks for `GET /api/capabilities` with the standard shape. Run `assfix <repo>` to audit a repo against this requirement.

### 1.2. Design Constants
- **Dark Mode**: Default (required). Use HSL-based palettes with subtle glassmorphism (`backdrop-filter`).
- **Micro-animations**: mandatory transition states for hover, expansion, and page entry.
- **Z-Index Layering**: Standardized layering (Sidebar: 40, Modal: 50, Tooltip: 100).

### 1.3. Tooltip Standard

Every interactive element whose function isn't immediately obvious from its icon alone
MUST have a tooltip. Icons-only sidebar items, action buttons without labels, truncated
text, and status indicators are the most common candidates.

#### Library

Use **Radix UI Tooltip** (`@radix-ui/react-tooltip`) — accessible, keyboard-aware,
supports delay configuration, and follows WAI-ARIA tooltip patterns. Add to
`package.json`:
```json
"dependencies": { "@radix-ui/react-tooltip": "^1.1.0" }
```

#### Fleet Tooltip Component

Every webapp SHOULD ship a shared `Tooltip.tsx` component wrapping Radix with
fleet defaults:

```tsx
import * as TooltipPrimitive from "@radix-ui/react-tooltip";

export function Tooltip({
  children,
  content,
  side = "top",
  delay = 500,
}: {
  children: React.ReactNode;
  content: string;
  side?: "top" | "bottom" | "left" | "right";
  delay?: number;
}) {
  return (
    <TooltipPrimitive.Provider>
      <TooltipPrimitive.Root delayDuration={delay}>
        <TooltipPrimitive.Trigger asChild>{children}</TooltipPrimitive.Trigger>
        <TooltipPrimitive.Portal>
          <TooltipPrimitive.Content
            side={side}
            sideOffset={4}
            className="z-50 rounded-md bg-zinc-800 px-2.5 py-1.5 text-xs text-zinc-200 shadow-lg
                       animate-in fade-in-0 zoom-in-95 data-[state=closed]:animate-out
                       data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95"
          >
            {content}
            <TooltipPrimitive.Arrow className="fill-zinc-800" />
          </TooltipPrimitive.Primitive>
        </TooltipPrimitive.Portal>
      </TooltipPrimitive.Root>
    </TooltipPrimitive.Provider>
  );
}
```

#### Conventions

| Property | Value | Rationale |
|----------|-------|-----------|
| Show delay | 500ms | Prevents flicker during mouse travel; fast enough not to feel sluggish |
| Hide delay | 200ms (Radix default) | Quick dismiss once mouse leaves trigger |
| Position | `top` by default, `bottom` for top-of-page elements, `left`/`right` for edge-adjacent icons | Avoids viewport clipping |
| Max width | 240px | Prevents overly wide tooltips; truncate with `...` if longer |
| Content | Plain text only — no HTML, no formatting | Screen-reader-friendly, consistent rendering |
| Color | `bg-zinc-800 text-zinc-200` — dark but not invisible | High contrast on all backgrounds |
| Arrow | Always show | Anchors tooltip to trigger visually |

#### Anti-Patterns

- **No nested tooltips** — if the user needs to mouse inside a tooltip to interact,
  use a popover or dialog instead
- **No tooltips on hover of disabled buttons** — if the button needs an explanation,
  the explanation should be visible without hovering (e.g., disabled state text)
  _unless_ the tooltip explains *how to enable it*
- **No tooltip on every icon** — use judgment; the trash icon doesn't need "Delete"
  if there's a visible label next to it
- **No tooltip on mobile** — tooltips don't hover on touch devices; use `title`
  attribute as a fallback if the Radix tooltip isn't reachable

---

## 2. Standard Page Sets

Every SOTA webapp MUST implement the following paths:

| Page | Purpose | Key Features |
| :--- | :--- | :--- |
| **`/` (Home)** | Dashboard | Overview of system health, active tasks, and quick-launch cards. |
| **`/tools`** | MCP Inspector | Dynamic list of server tools, schema visualization, and dry-run execution. |
| **`/logs`** | Event logs | Live tail, filter/search/sort, export, ring-buffer stats — see [WEBAPP_LOGS_PAGE.md](./WEBAPP_LOGS_PAGE.md). |
| **`/apps`** | Apps Hub | "Fleet Discovery" using `glama.json`. Navigation to other local MCP services. |
| **`/help`** | Documentation | Integrated Markdown viewer for project-specific docs and SOTA standards. |
| **`/settings`** | Configuration | Theme toggles, API keys, and **Local LLM "Glom On"** settings. |

---

## 3. Local LLM: The "Glom On" Pattern

Automated discovery of local inference engines is mandatory for SOTA compliance.

- **Auto-Discovery**: On mount, check `localhost:11434` (Ollama) and `localhost:1234` (LM Studio).
- **GPU Awareness**: If a high-end GPU (RTX 4090) is detected via system metrics, suggest local LLM installation.
- **Provider Fallback**: Seamless switching between Local (Ollama) and Remote (Gemini/Claude).

---

## 4. Chatbot System (SOTA Chat)

The Chatbot is the primary interaction layer and must be more than a simple text box.

### 4.1. Personas & Prompt Refinement
- **Persona Selector**: Radio button or dropdown in the chat input.
  - **Reductionist** (Sandra): Industrial, technically exhaustive.
  - **Debugger**: Trace-focused, look for edge cases.
  - **Explainer**: Focus on architectural patterns and concepts.
- **Prompt Refinement UI**: 
  - A "Refine" button that uses a smaller model (Flash/Lite) to improve the user's prompt before the "Main" model executes.
  - Shows the refined prompt for user approval/edit.

### 4.2. Implementation
- **Global Modal**: Accessible via `Cmd+K` or a Floating Action Button (FAB).
- **Context Awareness**: The chatbot must automatically receive the "Active Document" or "Current Page" as system context.

---

## 5. React Hardening (Zero-Trip Rule)

- **Anti-Flicker**: Use `Skeleton` loaders for all async data.
## 6. UI Component Hardening (Anti-Bug Patterns)

To prevent recurring UI failures (BUG-002/BUG-003), all components MUST follow these scaling rules.

### 6.1. Dynamic Inputs (The "Accordance Rule")
- **Auto-Expanding**: Textareas MUST expand vertically to fit content up to a `max-height`.
- **Scroll Hygiene**: Beyond `max-height`, inputs MUST have `overflow-y: auto` and a visible scrollbar track.
- **Focus State**: Inputs must never shift layout when focused; use `outline-offset` or `box-shadow` instead of changing border width.

### 6.2. Media Container Hygiene
- **Aspect Ratio**: Video and Image containers MUST use the `aspect-ratio` CSS property to prevent layout shifts.
- **Relative Sizing**: Always use container-relative units (`100%`, `auto`) or viewport units (`vh`, `vw`) rather than fixed `px` for media elements.
- **Object Fit**: Use `object-fit: cover` or `object-fit: contain` explicitly to handle varying asset dimensions without distortion.

### 6.3. Logger Panel Reliability
- **Smooth Auto-Scroll**: The Logger panel MUST automatically scroll to the bottom on new entries but allow "User Override" (pause auto-scroll when user manually scrolls up).
- **Format**: All logs must be timestamped and color-coded by level (`DEBUG`, `INFO`, `SOTA-WARN`, `ERROR`).
- **Full logs page**: Every webapp MUST also ship a dedicated **`/logs`** page with backend **`/api/logs`** — tail, pagination, filters, export. Spec: [WEBAPP_LOGS_PAGE.md](./WEBAPP_LOGS_PAGE.md).

---

## 7. MCP capability boundaries (web vs desktop UI)

**Web dashboard verification** (Vite dev server, Playwright, **cursor-ide-browser**, CDP-attached Chrome) MUST use **in-browser** automation only. Input is scoped to the **browser** process.

**Do not** enable **[pywinauto-mcp](../projects/pywinauto-mcp/README.md)** (or any **Win32 UIAutomation** “click the desktop” MCP) in the **same** MCP chain as routine IDE + webapp work. Those tools drive **whatever HWND has focus** — the **IDE**, **Explorer**, dialogs — not “the webapp tab.” Models may pick the **strongest** tool for “click UI,” causing **runaway OS-level** loops and **cursor capture** (documented fleet incident: Antigravity + pywinauto in chain).

**Rules:**

1. **Default:** IDE MCP configs used for **daily development** and **Webapp UIs** → **browser MCP only**; **pywinauto OFF**.
2. **pywinauto** → **separate profile** or **OpenManus / dedicated desktop** session only; see [FLEET_COMPUTER_USE_MCP.md](../patterns/FLEET_COMPUTER_USE_MCP.md) § *IDE / webapp work*.
3. **Verification** standards for browser tools and anti-loop guards: [VERIFICATION_STANDARDS.md](./VERIFICATION_STANDARDS.md) §2–3.

---

## 8. Accessibility & ARIA (SOTA 2026)

All SOTA webapps MUST be fully accessible and pass automated accessibility audits.

### 8.1. Discernible Text for Interactive Elements
- **Icon-only Buttons**: Every icon-only button MUST have a descriptive `title` attribute or `aria-label`.
  - *Correct*: `<button title="Tilt up"><ArrowUp /></button>`
  - *Incorrect*: `<button><ArrowUp /></button>`
- **Contrast**: Maintain a minimum 4.5:1 contrast ratio for all text elements against their background.

### 8.2. ARIA Attribute Compliance (JSX/React)
- **String Literals**: ARIA boolean attributes (`aria-selected`, `aria-pressed`, `aria-expanded`) MUST be passed as explicit string literals (`"true"` or `"false"`), not as JSX boolean values.
  - *Correct*: `aria-selected={active ? "true" : "false"}`
  - *Incorrect*: `aria-selected={active}`

### 8.3. Focus & Keyboard Navigation
- **Outline**: Do not disable the focus outline on interactive elements.
- **TabIndex**: Only use `tabindex` to fix logical focus order; never use `tabindex > 0`.
