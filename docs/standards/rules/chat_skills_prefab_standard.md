# Chat, Skills, and Prefab UI Standard (SOTA 2026)

**Established**: 2026-06-26  
**Updated**: 2026-06-30  
**Reference impl**: `multi-backup-mcp`, `arxiv-mcp`

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

### 1.10 Streaming (recommended)

Streaming response rendering is RECOMMENDED for SOTA apps. Pattern:

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

Not a hard requirement (most fleet repos use non-streaming for simplicity), but
strive for it in new webapps.

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
from fastmcp.server.server import ToolResult
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

The app MUST be permanently dark. No light mode toggle. The CSS `:root` variables
use dark values (Slate-950 / Zinc-950 backgrounds). The body sets
`color-scheme: dark` so native form controls render with dark OS theme.

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

---

## 9. Verification Checklist

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
