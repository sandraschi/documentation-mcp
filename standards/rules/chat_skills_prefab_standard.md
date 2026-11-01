---
title: "Chat, Skills, and Prefab UI Standard (SOTA 2026)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-21
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
# 2026-09-24: §9.4 added (gtfs-mcp agent-loop reference); rest still unverified.
---
# Chat, Skills, and Prefab UI Standard (SOTA 2026)

**Established**: 2026-06-26  
**Updated**: 2026-09-24  
**Reference impl**: `multi-backup-mcp`, `arxiv-mcp`, `gtfs-mcp` (§9.4 agent loop)

## 1. Chat Page — SOTA Requirements

Every fleet webapp with an LLM backend MUST implement a Chat page with the
following features. This standard replaces ad-hoc chat implementations.

### 1.1 Conversation Memory

| Requirement | Detail |
|-------------|--------|
| Persistence | Messages stored in `localStorage` under a repo-specific key (e.g. `arxiv-mcp-chat-history`). Loaded on mount, saved on every message append. |
| Format | Array of `{role: "user" | "assistant", content: string, ts?: string}`. ISO 8601 timestamps optional but recommended. |
| Cap | 100 messages max. Trim oldest when exceeded. |
| Restoration | On page load, restore previous session's messages exactly. Empty state shows a greeting / help text. |
| System messages | System prompt is prepended at send time, NOT persisted in history (avoids replay of stale system context). |

### 1.2 Skill-First Architecture (Mandatory)

The chat MUST use the server's FastMCP 3+ registered skill(s) as the **base
system prompt** (the "preprompt"). Personality prompts are layered on top.

| Requirement | Detail |
|-------------|--------|
| Fetch on mount | On page load, call `GET /api/skills` to discover registered skills. |
| Load skill content | Fetch the primary skill's content (e.g. from `skill-preprompt.md` or `GET /skill/{name}`) and store it as the base preprompt. |
| Composition | System prompt = skill content + `---` separator + personality role instructions. |
| Fallback | If no skill is available, fall back to a hardcoded default prompt. Never silently use an empty system prompt. |
| UI indicator | Show the loaded skill name in the controls bar (e.g. `skill:arxiv-expert`). |

The skill content teaches the LLM about the server's tool surface, correct API
usage, workflow ordering, and important notes (rate limits, env vars). This is
the single source of truth for how the MCP server should be used.

```typescript
// Build the combined system prompt
function buildSystemPrompt(skillContent: string, personalityId: string,
  personalityPrompt: string, customPrompt: string): string {
  if (personalityId === "custom") return customPrompt || skillContent;
  return `${skillContent}\n\n---\n\n## Role\n${personalityPrompt}`;
}
```

### 1.3 Personality Selector

| Requirement | Detail |
|-------------|--------|
| Minimum | 4+ distinct personalities. |
| Selector UI | Dropdown in the chat header/controls bar. `data-testid="personality-select"`. |
| Built-in personas | Research Assistant, Expert Reviewer, Quick Summarizer, Custom. |
| Custom | A "Custom" option. When selected, the user edits the full combined prompt (skill + role). Stored in localStorage. |
| Persistence | Selected personality ID persisted in `localStorage` (e.g. `arxiv-mcp-chat-personality`). |

Each personality defines a `prompt` string that is appended AFTER the skill
content as a `## Role` section. On send, the frontend builds:

```
messages = [
  {role: "system", content: skillContent + "\n\n---\n\n## Role\n" + personalityPrompt},
  ...history
]
```

For Ollama chat endpoints, this maps to the `system` role natively.

### 1.4 Example Prompts

| Requirement | Detail |
|-------------|--------|
| Minimum | 6+ clickable prompts relevant to the server's domain. |
| Display | Shown below the input area or as an expandable row of pill buttons. |
| Grouping | Grouped by topic/category when >3 (e.g. "Search", "Analysis", "Writing"). |
| Interaction | Click fills the input. No auto-send — user edits or presses Enter. |
| data-testid | `data-testid="example-prompts"` on the container. |

### 1.5 Export

| Requirement | Detail |
|-------------|--------|
| Trigger | Button in chat header/controls bar. `data-testid="chat-export"`. Icon: `Download`. |
| Format | `.txt` file with `[timestamp] Role: content` lines. Downloaded via Blob URL. |
| Filename | `{repo-name}-chat-{timestamp}.txt`. |
| Empty guard | Disabled (dimmed) when no messages. |

### 1.6 Clear

| Requirement | Detail |
|-------------|--------|
| Trigger | Button in chat header/controls bar. `data-testid="chat-clear"`. Icon: `Eraser` or `Trash2`. |
| Action | Instantly clears visible messages AND localStorage history. No confirmation dialog required (instant reset is standard). |
| Empty guard | Disabled when no messages. |

### 1.7 Model & Provider Controls

| Requirement | Detail |
|-------------|--------|
| Model input | Editable text field showing current model name (default detected from backend `/api/llm/discover`). |
| Provider status | Live indicator: "Ollama on :11434" (green), "Not detected" (red), or "Detecting..." (neutral). |
| Detection | On mount, call `/api/llm/discover` for Ollama presence and configured model. |
| Resident-first default | The default model MUST be resolved **resident-first**: probe Ollama `/api/ps`; use the highest-preference model that is already loaded (`qwen3.8:27b` → `gemma4:12b` → tier table); only if nothing is loaded pick the highest-preference installed model from `/api/tags`. Never default to `tags[0]` or a hardcoded model — that evicts the resident model and forces a ~30s cold reload ("Headers Timeout"). Canonical helpers: `templates/llm-detect/model-preference.ts` (frontend) / `detect.py pick_model` (backend). |

### 1.8 Input & Send

| Requirement | Detail |
|-------------|--------|
| Input | Single-line input with Enter-to-send. Shift+Enter for newline (optional but nice). |
| Send button | `data-testid="chat-send"`. Icon: `Send` or `ArrowUp`. Disabled during loading or when provider is down. |
| Loading state | "Thinking..." or pulse animation below the last message. |
| Error state | Error text rendered as an assistant message so it's visible in the scrollback. |

### 1.9 data-testid Requirements

| Attribute | Element |
|-----------|---------|
| `chat-page` | Page container |
| `chat-controls` | Model / personality / export controls bar |
| `chat-messages` | Message scroll container |
| `chat-input` | Text input |
| `chat-send` | Send button |
| `chat-export` | Export button |
| `chat-clear` | Clear button |
| `personality-select` | Personality dropdown |
| `example-prompts` | Example suggestion container |

### 1.10 Streaming (RECOMMENDED)

Streaming response rendering is **RECOMMENDED** for SOTA apps. Pattern:

```ts
const r = await fetch(`${OLLAMA}/api/chat`, { /* ... */ });
const reader = r.body!.getReader();
const decoder = new TextDecoder();
let buffer = "";
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  buffer += decoder.decode(value, { stream: true });
  // parse NDJSON lines, update assistant message incrementally
}
```

**Tier note (2026-09-21).** This was briefly promoted to MANDATORY and reverted to
RECOMMENDED the same day, pending a scoped drift pass. The case for eventual
promotion stands, and the old justification no longer holds: the previous text
claimed "most fleet repos use non-streaming for simplicity", but a 2026-09-21
fleet grep found the `getReader()` token-stream client in chat/LLM files across
roughly **25-30 fleet repos** (arxiv-mcp, aiwatcher-mcp, documentation-mcp,
docker-mcp, devices-mcp, depot-mcp, inkscape-mcp, fleet-agent-mcp,
home-assistant-mcp, godot-mcp, handbrake-mcp, gtfs-mcp, grandorgue-mcp,
git-github-mcp, giskard-mcp, ocr-mcp, podman-mcp, streamfog-mcp, unity3d-mcp,
tvtropes-mcp, rustdesk-mcp, moltbot-mcp, and others). When most of the fleet
already ships a practice, leaving it "recommended" gives new repos no signal.
Promote once the drift impact is scoped, so the gate does not land as a batch of
unexplained failures.

Resilient / resumable streaming (reconnect on drop, resume from offset) remains
**RECOMMENDED** - see §9.1.

---

## 2. Conversation Persistence Schema

```typescript
// localStorage key pattern: {repo-name}-chat-history
// Example: "arxiv-mcp-chat-history"

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  ts?: string;            // ISO 8601, optional
};

// Personality key: {repo-name}-chat-personality
// Example: "arxiv-mcp-chat-personality"
// Value: string (personality ID from the selector)
```

---

## 3. Personality / Prompt Refinement Architecture

### 3.1 Sources of Personalities

| Source | Description |
|--------|-------------|
| Hardcoded | Built into the frontend page (Research Assistant, Expert Reviewer, Quick Summarizer). |
| Skill-loaded | Fetched from `GET /skill/{name}` at runtime and offered as a personality option. |
| Custom | User-authored prompt, stored in localStorage. |

### 3.2 Default Selection

The first personality should be a loaded skill (most domain-relevant). Fallback
to the first hardcoded personality if no skill is available.

### 3.3 Prompt Quality Checklist

Every system prompt SHOULD:
- State the AI's role explicitly ("You are a...")
- Describe response tone and length expectations ("concisely", "in 3 bullets")
- Reference available tools or data sources
- Avoid over-constraining (don't hardcode banned topics unless security-relevant)

---

## 4. Sample & Favorite Prompts

### 4.1 Suggested Prompts

For research/scientific servers (like arxiv-mcp), typical domain prompts:

| Domain | Examples |
|--------|---------|
| Search | "Find papers on topic X", "What's new in cs.LG this week?" |
| Analysis | "Summarize this abstract", "Compare these two approaches" |
| Writing | "Draft a rebuttal", "Expand this outline into a literature review" |
| Discovery | "What are the open problems in X?", "Which papers should I read first?" |

For operations servers (backup, monitoring, etc.), adapt to domain:

| Domain | Examples |
|--------|---------|
| Status | "Show me recent failures", "What's the health dashboard look like?" |
| Actions | "Schedule a backup", "Restore from yesterday's snapshot" |
| Alerts | "Notify me when disk is above 90%", "What changed in the last hour?" |

### 4.2 Favorite Prompts (Recommended)

A "favorite/saved prompts" feature lets users bookmark useful prompts:

- Store as `{repo-name}-chat-saved-prompts` in localStorage
- Render as a list below the example prompt section
- Simple CRUD: add current input as favorite, list favorites, remove
- `data-testid="saved-prompts"`

Not yet mandatory but RECOMMENDED for new webapps.

---

## 5. Skills — Authoring and Surface

### Skill File

Every repo SHOULD ship one or more skills as `src/{package}/skills/{name}/SKILL.md`.

The skill MUST cover:
- What the server does (1 paragraph)
- Every tool category with bullet-point tool lists
- Best practices / methodology
- Configuration requirements (env vars, external services)

### Skill REST Endpoint

The backend MUST expose `GET /skill/{name}` returning the raw SKILL.md content.

```python
@app.get("/skill/{skill_name}")
async def get_skill(skill_name: str):
    skill_path = Path(__file__).parent / "skills" / skill_name / "SKILL.md"
    if skill_path.exists():
        return skill_path.read_text(encoding="utf-8")
    return "not found"
```

### Skill MCP Resource

Skills MUST also be exposed as MCP resources:

```python
@mcp.resource("skill://{name}")
def get_{name}_skill() -> str:
    ...
```

### Skills Page (Frontend)

The webapp MUST have a `/skills` page that:
- Lists available skills from a manifest (hardcoded JSON array in the page)
- Fetches each skill's content via `GET /skill/{name}`
- Renders skill content with `react-markdown` (or equivalent)
- Uses proper markdown styling: heading sizes, code backgrounds, list bullets

### Chat Default

The primary skill MUST be loadable as the default Chat personality — fetched on
mount and used as the `system_prompt` unless the user selects a different personality.

---

## 6. Prefab UI Cards

Tools that primarily **list items**, report **status**, or show **dashboards**
SHOULD ship a Prefab App surface.

### Pattern

```python
from fastmcp.tools.base import ToolResult  # canonical home; NOT fastmcp.server.server (re-export trips pyright reportPrivateImportUsage - BUG-042)
from prefab_ui import PrefabApp
from prefab_ui.components import Heading, Row, Div

@mcp.tool(app=True)
async def show_{name}_app(...) -> ToolResult:
    with PrefabApp(title="...") as app:
        Heading("...")
        for item in items:
            Row(label=..., value=...)
    return ToolResult(content="plain fallback", structured_content=app)
```

### Tools That MUST Have Prefab

| Tool type | Example | Why |
|-----------|---------|-----|
| Status/health | `show_status_app` | Dashboard KPIs in chat |
| List backups | `show_backups_app` | Job list with status |
| List archives | `show_repo_backups_app` | File list with sizes/dates |
| Any multi-row result | N/A | User shouldn't read raw JSON |

### Dependency

`prefab-ui>=0.14.0` MUST be in `[project.dependencies]` — not optional.

---

## 7. Dark Mode

The app MUST be **dark by default** — this is the fleet identity, not optional.
The CSS `:root` variables use dark values (Slate-950 / Zinc-950 backgrounds).
The body sets `color-scheme: dark` so native form controls render with dark OS
theme.

```css
body {
  color-scheme: dark;
}
select, input, textarea {
  color-scheme: dark;
}
```

Native `<select>` elements MUST use explicit dark background/foreground classes
such as `bg-zinc-800 text-zinc-100 border-zinc-600` to ensure readable contrast
regardless of OS/browser defaults.

### 7.1 OPTIONAL: light-mode toggle (invert hack)

Since 2026-08 (validated on opencode-cli-mcp, then rolled out fleet-wide), a
webapp MAY ship a light-mode toggle using the **CSS invert hack** - one CSS
block, no component rewrite. Dark remains the default; the toggle is user
opt-in and persists.

```css
/* EXPERIMENTAL light mode — invert hack. Toggling .dark off inverts the UI.
   Remove this block to revert to permanently-dark. */
html:not(.dark) {
  filter: invert(1) hue-rotate(180deg);
  background: #f4f4f5;
}
html:not(.dark) img,
html:not(.dark) video,
html:not(.dark) canvas,
html:not(.dark) iframe {
  filter: invert(1) hue-rotate(180deg); /* un-invert media */
}
```

Toggle implementation (React): flip `document.documentElement.classList`
`.dark` on/off, persist the choice to `localStorage` (`{repo}-light-mode`),
restore on load. Topbar button with `Sun`/`Moon` icons.

**Why it works**: the fleet token palette (Zinc/Slate surfaces) is consistent
enough that full inversion produces a coherent light UI.

**Guardrails (MANDATORY if you ship the toggle):**

1. **Dark is the DEFAULT.** `<html class="dark">` in `index.html`, and the
   toggle's initial state must be dark. Never default to light.
2. **Un-invert media**: `img`, `video`, `canvas`, `iframe` MUST be
   double-inverted (the un-invert block above) or screenshots/covers/players
   render negative.
3. **Persistence**: the choice MUST survive reloads (localStorage). No
   session-only toggle.
4. **CUA/Playwright verification**: the smoke test and e2e suite MUST run in
   dark mode. If a test machine has the light choice persisted, the toggle
   must be reset (`localStorage.removeItem` or `page.addInitScript` forcing
   `.dark`) before verification — screenshots and OCR checks assume dark.
5. **Reversible**: the CSS block and hook are marked `EXPERIMENTAL` with
   comment banners; deleting them restores permanently-dark with no residue.
6. **Known artifacts (accept them or don't ship)**: accent colors invert
   (amber→cyan-ish), saturated brand colors look wrong, non-fleet custom
   themes may invert badly. The hack is a convenience, not a design system.

Reference implementation: `opencode-cli-mcp` — `web_sota/src/index.css` (invert
block) + `web_sota/src/Layout.tsx` (`useExperimentalTheme` + topbar toggle).

**Fleet rollout (as of 2026-08-01, 42 repos shipped):**

| Mechanism | Repos |
|-----------|-------|
| Invert hack (`{repo}-light-mode` key, Sun/Moon topbar button) | opencode-cli-mcp, advanced-memory-mcp, aiwatcher-mcp, arxiv-mcp, calibre-mcp, plex-mcp, discord-mcp, email-mcp, yahboom-mcp, resonite-mcp, mixx-dj-mcp, grandorgue-mcp, gimp-mcp, blender-mcp, inkscape-mcp, godot-mcp, worldlabs-mcp, overte-mcp (new topbar added), unity3d-mcp, system-admin-mcp, database-operations-mcp, robotics-mcp, avatar-mcp, windows-operations-mcp, virtualization-mcp (sidebar header — no desktop topbar exists), multi-backup-mcp, telephony-mcp, mujoco-mcp (sidebar header — no topbar, emoji icons, no lucide dep), meta_mcp, mastodon-mcp, libreoffice-mcp, freecad-mcp, qcad-mcp, forgejo-mcp (JSX webapp), podman-mcp, docker-mcp, osc-mcp, rtorrent-mcp, sdr-mcp, scraper-mcp, devices-mcp (migrated from Tailwind class system 2026-08-01) |
| Native toggle (app already had a class-based theme system — do NOT invert-hack these) | filesystem-mcp (wired shadcn `ThemeProvider`, added `useTheme()` toggle) |

**Mechanism decision rule:** if the app uses Tailwind `darkMode: ["class"]`
variants or a wired `ThemeProvider`, add a native toggle
(`useTheme().setTheme("dark" | "light")`) — the invert hack would
double-invert. Otherwise use the invert hack. Detection:
`rg "dark:" <webroot>/src` (any hits = native path) or check for
`ThemeProvider` usage.

---

## 8. Reference Implementations

| Feature | Repo | File |
|---------|------|------|
| Conversation memory | `arxiv-mcp` | `web_sota/src/pages/ChatPage.tsx` — `localStorage` history, 100-msg cap, timestamped |
| Personality selector | `arxiv-mcp` | `web_sota/src/pages/ChatPage.tsx` — 4 personas, dropdown, localStorage persistence |
| Skill-as-preprompt | `arxiv-mcp` | `web_sota/src/pages/ChatPage.tsx` — fetches `GET /api/skills`, loads skill content as base, layer personality on top |
| Export .txt | `arxiv-mcp` | `web_sota/src/pages/ChatPage.tsx` — Blob download with ISO timestamps |
| Clear conversation | `arxiv-mcp` | `web_sota/src/pages/ChatPage.tsx` — instant reset |
| Skill-loaded default | `multi-backup-mcp` | `web_sota/src/pages/chat.tsx` — skill as default personality |
| Example prompts | `arxiv-mcp` | `web_sota/src/pages/ChatPage.tsx` — 4 clickable suggestion pills on welcome screen |
| Skills page | `multi-backup-mcp` | `web_sota/src/pages/skills.tsx` — manifest + ReactMarkdown |
| Prefab cards | `multi-backup-mcp` | `src/multi_backup_mcp/tools/prefab_cards.py` |
| Theme | both | `web_sota/src/index.css` — `color-scheme: dark` |
| Agent chat endpoint | `gtfs-mcp` | `src/gtfs_mcp/api/llm.py` — `/api/llm/chat-agent`, allowlist, prefetch, loop guards, `num_ctx` cap |
| Tool trace blocks | `gtfs-mcp` | `web_sota/src/pages/chat.tsx` — trace array rendering + export |
| Agent web_search | `gtfs-mcp` | `src/gtfs_mcp/services/web_search.py` (vendored DDG scraper, no key) |
| Light toggle (optional) | `opencode-cli-mcp` | `web_sota/src/index.css` (invert block) + `web_sota/src/Layout.tsx` (`useExperimentalTheme`) |

---

## 9. Streaming Resilience, Tool Trace, and Conversation Branching (RECOMMENDED)

**Added:** 2026-09-17 — gap-filled from a LibreChat (`danny-avila/LibreChat`, MIT)
analysis. LibreChat independently converged on the same skill/MCP/agent
concepts as the fleet but has three chat-UX patterns this standard lacked.
**Status: RECOMMENDED, not yet MANDATORY** — gtfs-mcp (2026-09-24) is the
first fleet repo to ship the agent loop and simplified trace blocks (§9.4)
and is the reference implementation below. Promote §9 to MANDATORY once 3+
repos ship it; do NOT mass-migrate chat pages — each needs its allowlist and
domain grounding reviewed individually.

### 9.1 Reconnecting / Resumable Streams

**Problem:** A naive `fetch` + `ReadableStream` (§1.10) loses the entire
partial response if the network blips or the SSE connection drops mid-token.
The user sees a dead stream and must resend the whole prompt.

**Requirement:** The chat streaming client MUST track stream progress and
attempt one automatic reconnect on drop, resuming from the last received
token rather than restarting the request.

| Requirement | Detail |
|-------------|--------|
| Stream identity | Backend's first SSE event includes a `streamId`. |
| Client state | Client holds `{streamId, lastOffset}` **in memory only** — not `localStorage`. Stream resume is for a network blip, not surviving a page reload. |
| Reconnect | On `onerror`/close before a terminal event, retry once immediately (then backoff) using `Last-Event-ID` (or an offset query param) so the backend can resume from `lastOffset` instead of replaying the whole response. |
| Give up | After the retry budget (recommend: 1 immediate + 2 backoff, total <10s) exhausted, render "response interrupted — retry?" as an assistant message per §1.8 error-state rules, not a silent failure. |
| UI | `data-testid="chat-stream-retrying"` indicator shown during a reconnect attempt. |
| Scope note | Fleet backends are mostly single-instance/local, not horizontally scaled — only client-side resume-on-blip is in scope. LibreChat's Redis-backed cross-replica/multi-device stream sync is explicitly OUT of scope; don't build that. |

### 9.2 Tool Call / Trace Visualization

**Problem:** When the chat backend proxies MCP tool calls (portmanteau tools,
multi-step agent turns), the user only sees the final answer — no visibility
into which tool fired, with what args, or how long it took. This matters more
for fleet repos than for LibreChat, since every fleet chat page is talking to
MCP tools by design (§1.2 skill-first architecture).

**Requirement:** The chat message stream MUST render inline tool-activity
blocks for any tool call made during a turn.

| Requirement | Detail |
|-------------|--------|
| Placement | Inline in the assistant message at the point the call occurred — not only a separate debug/logs panel. |
| Content | Tool name, status (`pending`/`running`/`done`/`error`), collapsed by default; expand to see args and result/error. |
| Backend contract | Streamed tool-call events distinct from token deltas — SSE event type `tool_call` carrying `{name, args, status}`, emitted before token events resume for that turn. |
| data-testid | `chat-tool-call` (container), `chat-tool-call-status` (status badge). |
| Relation to Prefab | If the tool already ships a Prefab card (§6), render the card as the expanded content instead of raw JSON. |

### 9.3 Conversation Branching / Edit-and-Resubmit

**Problem:** Fleet chat pages (§2 schema) are append-only. Editing an earlier
message re-sends and overwrites history from that point, silently destroying
the original branch.

**Requirement:** The user MUST be able to edit any of their own prior
messages and resubmit, creating a new branch; the original branch remains
reachable via a branch selector on the edited message.

| Requirement | Detail |
|-------------|--------|
| Schema | Extend `ChatMessage` (§2) with optional `branchId`/`parentId`. All branches persist in `localStorage`; only the active path renders. |
| Edit trigger | Hover/click affordance on any user message → inline edit → resubmit creates a sibling branch from that point. |
| Branch selector | `‹ 1/2 ›`-style control on any message with siblings, switches the active rendered path. |
| data-testid | `chat-message-edit`, `chat-branch-selector`. |
| Cap interaction | The 100-message cap (§1.1) applies to the active path's message count, not the total across all branches. |

### 9.4 Server-Side Agent Loop (Reference: gtfs-mcp, 2026-09-24)

§9.2 assumed token streaming with SSE tool events. gtfs-mcp proved a simpler
shape any fleet repo can copy in ~200 lines with no new dependencies: a
non-streaming agent endpoint where the model turn happens server-side, with
tools executed in-process.

| Element | Pattern |
|---|---|
| Endpoint | `POST /api/llm/chat-agent` takes `{model, messages, personality, custom_prompt}`, returns `{success, reply, trace}`. |
| Tools | Ollama native `tools:` on `/api/chat`. Executed in-process against the repo's own `@mcp.tool` functions — FastMCP decorators return plain async functions (verify with `inspect.iscoroutinefunction`), so no MCP client or HTTP-to-self is needed. |
| Allowlist | Hard name→function map. The model never sees the full tool surface. Read-only tools first; never destructive ones (`remove_*`, `shutdown`, …). |
| Grounding | System prompt = role + skill content + live depot state (feed ids/counts) + today's date. Home city/feed default stated explicitly so small models stop guessing (observed failure: "Praterstern? never heard of it — Berlin?"). |
| Deterministic prefetch (recommended) | For the common case, resolve server-side first (e.g. stop-name substring match → `find_stops` → `get_departures`) and inject the results as data. Correct answers then survive even models that fumble the call chain or emit pseudo-calls (`[TOOL_CALLS]{...}`) with invented times. |
| Loop guards | Bounded turns (6). Nudge turn (max 2) when the model answers with zero data calls; restate turn (no tools) when raw tool JSON leaks into the visible reply. |
| VRAM | Pass `"options": {"num_ctx": 16384}` on agent calls. Model default windows (up to 262k) make Ollama reserve tens of GB of KV cache on 24GB cards for turns that never exceed a few thousand tokens. |
| Trace UI | `trace: [{tool, ok, summary}]` rendered as small mono lines above the answer and included in the `.txt` export. Satisfies §9.2's visibility goal without SSE. |
| web_search | Vendor the dependency-light DuckDuckGo scraper (`advanced-memory-mcp` `services/research_sources.web_search`: httpx, regex extraction, no API key) as an allowlisted agent tool for out-of-depot questions. The skill MUST carry a "recent information" section listing trigger words (`this week`, `latest`, `new`, `review`, `vs`, `compare`) that mean web_search, not the depot. |

Do NOT present this as "just point chat at MCP" — an unscoped tool surface plus a small model is how you get confident fabrications with tool-shaped formatting. The allowlist, the grounding, and the prefetch are the feature; the loop is plumbing.

---

## 10. Verification Checklist

Before certifying a webapp as SOTA-compliant:

- [ ] Chat persists conversation across page reloads (localStorage)
- [ ] Chat loads previous session on mount
- [ ] On mount, fetches `GET /api/skills` and loads primary skill as base preprompt
- [ ] System prompt = skill content + `---` separator + personality role instructions
- [ ] Skill name shown in UI controls bar (e.g. `skill:arxiv-expert`)
- [ ] 4+ personalities available, including a loaded skill
- [ ] Personality selection survives page reload
- [ ] Export produces valid .txt, disabled when empty
- [ ] Clear resets both UI and storage
- [ ] Input field has Enter-to-send
- [ ] Loading state shown during LLM response
- [ ] Errors surfaced as messages (not silent)
- [ ] Provider status indicator (green/red)
- [ ] `data-testid` attributes present on all interactive elements
- [ ] API call includes system prompt, history, model
- [ ] No `/v1` in provider base URLs sent to backend

**RECOMMENDED (§1.10 and §9, not yet mandatory):**

- [ ] LLM response streams token-by-token, not a single blocking response (§1.10)
- [ ] Streaming reconnects once on drop and resumes from last offset (§9.1)
- [ ] Tool calls render inline as expandable trace blocks, not just in logs (§9.2)
- [ ] User messages are editable and resubmitting creates a branch, not an overwrite (§9.3)
