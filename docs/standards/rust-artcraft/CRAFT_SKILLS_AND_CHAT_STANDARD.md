---
title: "CRAFT_SKILLS_AND_CHAT_STANDARD - Bundled skills and in-app chat for Rust craft apps"
category: standard
status: active
audience: craft-dev, all-agents
last_updated: 2026-11-15
skill_candidate: false
---

# CRAFT_SKILLS_AND_CHAT_STANDARD

**Status: ACTIVE (2026-11-15).** Working pilot implemented in `puppycraft` (`D:\Dev\repos\puppycraft`). Normative for new craft apps; existing apps adopt on touch.

Parent hub: [RUST_ARTCRAFT_STANDARD.md](../RUST_ARTCRAFT_STANDARD.md). Builds on [CRAFT_LLM_PROVIDER_STANDARD.md](./CRAFT_LLM_PROVIDER_STANDARD.md) (providers, config, keys, VRAM) and [CRAFT_MENU_BAR_STANDARD.md](./CRAFT_MENU_BAR_STANDARD.md) (Window and Help menus).

## One-line rule

**A craft app ships its skills inside the binary, serves them to agents over MCP, and uses the same skills as the preprompt of its in-app chat. One source, three readers: agents, the chat model, and the human.**

## 1. Why

The Python fleet already does this. FastMCP's `SkillsDirectoryProvider` serves `skills/<name>/SKILL.md` as `skill://` resources (`standards/FASTMCP_FEATURES.md` section 3). The webapp's Chat page uses a skill as (part of) its preprompt, so you can talk to a model that knows the repo.

Audit of the Rust craft apps on 2026-11-14:

| Finding | Detail |
|---|---|
| Skills | None. 46 Rust craft repos, zero `SKILL.md` files. |
| MCP surface | `craft-biz::mcp` (all back-office apps) advertises only `tools` and answers `tools/list` and `tools/call`. gamecraft answers `resources/list`, moneycraft `prompts/list`, wincraft both (one `wincraft://status` JSON resource). None serves skills. |
| Chat | Five independent attempts, none skill-based: homecraft (Chat view, own `homecraft_core::llm`, user-typed system prompt), studiocraft (Chat view), codercraft (system prompt per agent mode), travelcraft (prompt built from the selected sight's data), vmcraft (own `llm.rs` chat). homecraft and vmcraft bypass `craft-ai-core`, against the LLM provider standard. |
| `craft-ai-core::CraftAiClient::complete()` | Single turn only (system + one user message), no tool calling, no history. **It never returns an error**: if curl is missing, the HTTP call fails, the JSON does not parse or the content is empty, it returns invented text (`[craft-ai sovereign synthesis ...]`, `[craft-ai fallback] ...`) as `Ok`. It also passes the whole request body and the API key as curl command-line arguments. |

The last row blocks chat: a chat that shows invented text as the model's answer is worse than no chat. The fixes are in section 5.

## 2. Skills

### 2.1 Layout and format

```
<repo>/skills/
  <app>-<topic>/
    SKILL.md          # required; served as skill://<app>-<topic>/SKILL.md
    reference.md      # optional sub-doc, served as skill://<app>-<topic>/reference.md
```

`SKILL.md` follows the Agent Skills format: YAML frontmatter with `name` (equal to the folder name) and `description` (one sentence saying when to use it, at most 200 characters), then a markdown body. This is the same shape as the Python repos and Claude / Cursor skill folders, so a skill can be exported unchanged (2.4).

Content rules, enforced by tests (2.6):
- It names only tools the app really has. A skill that tells the model to call a tool that does not exist is a defect.
- It names no cloud-only tool or service as the default path (`LOCAL_LLM_FIRST_DOCTRINE.md`).
- No secrets, no machine-specific paths except documented defaults, LF line endings, no em dashes.
- Size: `SKILL.md` at most 12 KB, all skills of one app together at most 40 KB. These skills become chat preprompt, and a local 12B model has a limited context.

Typical set per app: `<app>-workflow` (the domain model and the everyday flows), plus one skill per tricky area (e.g. taskcraft: blockers, git sync, bus inbox).

### 2.2 Embedding

Skills are compiled into the binary with `include_str!`. There are no files to install next to the exe and nothing to go missing. The new `craft-skills` crate (section 5) provides a macro:

```rust
pub static SKILLS: &[craft_skills::SkillSrc] = craft_skills::bundle![
    "taskcraft-workflow" => "../../../skills/taskcraft-workflow/SKILL.md",
    "taskcraft-blockers" => "../../../skills/taskcraft-blockers/SKILL.md",
];
```

A test walks `skills/` at build time (`CARGO_MANIFEST_DIR`) and fails if a folder exists that `bundle!` does not list, so a new skill cannot be forgotten.

### 2.3 MCP surface

When an app has skills, its MCP server:
- advertises `"resources": { "listChanged": false }` next to `tools` in `initialize`;
- answers `resources/list` with one entry per file: `uri` `skill://<name>/SKILL.md`, `name`, `description` (from frontmatter), `mimeType` `text/markdown`;
- answers `resources/read` with `contents: [{ uri, mimeType, text }]`. An unknown URI is a JSON-RPC error `-32002` (resource not found), never an empty success;
- also exposes the tool `<app>_skill_read { name? }`. Without `name` it lists the skills; with `name` it returns the body. Several MCP clients do not let the model read resources by itself, but every client can call tools.

The URI scheme matches the Python fleet, so an agent sees the same shape from Python and Rust servers.

### 2.4 CLI

```
<app> skills list [--json]
<app> skills show <name>
<app> skills export --to <dir> [--force]
```

`export` writes `<dir>/<name>/SKILL.md` (and sub-docs) for clients that read skill folders, e.g. `~/.claude/skills` or a repo's `.cursor/skills`. It refuses to overwrite without `--force` and prints every path it wrote.

### 2.5 Human surface

Help > Project Files & Docs gets a **Skills** tab with the list and the rendered text. No sixth Help item: the menu standard's five-item Help suite stays as it is.

### 2.6 Tests (per app)

1. `resources/list` returns every bundled skill; `resources/read` returns each body byte for byte; an unknown URI returns `-32002`.
2. Every folder under `skills/` is in `bundle!`.
3. Frontmatter parses; `name` equals the folder; `description` at most 200 characters.
4. **Tool references:** every `<app>_*` identifier in backticks in a skill is a tool in `tools_list()`. This test stops skills drifting when tools are renamed.
5. Size limits from 2.1.

## 3. In-app chat

### 3.1 What it is

A chat dock in the app window (Window > Chat, `Ctrl+J`; it can be maximised to fill the viewport). A local model is the default. Its preprompt is the app's skills plus the live state of the app, so you can ask "why is BC-5 blocked?" or "what does git sync close?" and get answers grounded in this app and this data. It can call the app's own tools, with confirmation for anything that changes data.

### 3.2 Preprompt assembly (in this order)

| # | Part | Source | Cap |
|---|---|---|---|
| 1 | Header | Fixed text: app name and version, today's date, the rules below | ~0.5 KB |
| 2 | Skills | All bundled skills of the app | 40 KB (2.1) |
| 3 | Tool catalogue | Name + one-line description per tool. Full schemas go through the provider's native tool field, not the prompt | ~4 KB |
| 4 | Live status | The app's status command (e.g. `task_status`), as compact JSON | 4 KB, truncated with a marker |
| 5 | Selection | What the user has open (e.g. the issue in the inspector), from the host | 4 KB, truncated with a marker |
| 6 | User extra | Optional user-written instructions from Settings (homecraft has this today) | 2 KB |

Header rules given to the model:
- Answer from the context and tool results.
- Say when you do not know.
- Never invent tool names, issue keys or numbers.
- Quote the tool result you relied on.
- Changing data requires calling a tool, which the user will confirm.

**Transparency:**
- A **View prompt** button shows exactly what was sent, with the token estimate per part.
- A context meter shows the estimate against the model's context.
- If parts 2-6 exceed the budget, the lowest rows are truncated first, never the header, and the meter says so.

**Context size:** chat requests set Ollama `num_ctx` to 16384, an explicit exception to the 8192 loop-prompt rule in the LLM provider standard (section 3 rule 2). That standard's other transport rules apply unchanged: `stream:false`, `think:false`, no `options` field to OpenAI-compatible endpoints.

### 3.3 Tool use

- **Native tool calling:** OpenAI-compatible `tools` / `tool_calls` (also LM Studio, DeepSeek, OpenRouter, custom), Anthropic `tools` / `tool_use`, Ollama `/api/chat` `tools`.
- **Limit:** at most 6 tool rounds per user message, then the model must answer.
- **Read-only tools run directly.** Every tool in the app's table carries `read_only: bool`. Tools without the flag count as **not** read-only.
- **Every other tool shows a confirm card:**
  - The card shows the tool, its arguments and a one-line effect.
  - "Allow once" or "Deny" are the only choices: there is no "always allow" for anything that writes.
  - Confirmed calls go through the same `call_tool` path as MCP. The history actor is `chat:<provider>/<model>`, next to `agent`, `git:` and `bus:`.
- **No tools:** a "Tools off" toggle gives pure Q&A over the preprompt.

### 3.4 Errors are errors

- No fallback text, ever. Unreachable server, missing key, HTTP error, unparsable reply and empty reply each show as an error line in the chat with the cause (never the key) and a "Retry" / "Settings" action.
- Send-time guard from the LLM provider standard (section 5 rule 6): with no model selected, the chat refuses and points to Settings. There is no fallback model.

### 3.5 Privacy

- **Local providers (Ollama, LM Studio, custom localhost):** no banner.
- **Cloud provider:** a persistent banner says "This chat sends app data to `<provider>`". The first send in a session needs one confirm.
- **Transcripts:** stored per app as `%LOCALAPPDATA%\<app>\chat\<YYYY-MM-DD>.jsonl`, outside the app's business DB. Never stored with keys. There is a Clear button and a setting to turn transcripts off.

### 3.6 Threading and cancel

The worker pattern from the LLM provider standard (section 5): `std::thread::spawn` and `mpsc`, polled every frame, with a spinner. **Cancel** kills the curl child process. The UI thread never waits on the network.

### 3.7 UI

- **Header:** a provider/model pill (click opens Settings), the context meter, View prompt, Tools on/off, Clear.
- **Messages:** user and assistant messages, tool calls as collapsible cards (name, arguments, result), confirm cards, and errors in the theme's error tone.
- **Text rendering:** v1 renders plain text with fenced code blocks in monospace and copy buttons; markdown rendering comes later.
- **Fleet egui rules apply:** high contrast in both themes (no light grey on white), Ctrl+wheel zoom, keyboard use (Enter sends, Shift+Enter adds a new line, Esc cancels).
- **egui 0.37 right-dock width guardrail:** `egui::Panel::right("chat_dock")` MUST set `.default_size(360.0).min_size(280.0).max_size(480.0).resizable(true)` (or equivalent bounded `.max_size(...)`), set `ui.style_mut().wrap_mode = Some(egui::TextWrapMode::Wrap)` inside the dock, and lay out the input bar with `Layout::right_to_left` (Send button on the right, `TextEdit` filling remaining space) rather than `available_width() - fixed` so long messages or input never trigger frame-by-frame sidebar auto-growth.

### 3.8 Not in scope (v1)

- Streaming tokens. v1 is request/response with a spinner, consistent with `stream:false`. Streaming (Ollama NDJSON, SSE) is v2.
- Picking skills by relevance when they exceed the budget. v1 truncates and says so.
- Feeding transcripts into memops / advanced-memory.
- A chat tool over MCP: agents already are the chat on that side.

### 3.9 LLM Discovery, Settings Page & Agentic DE Coop (Normative)

Reference implementation: `kittycraft` (`D:\Dev\repos\kittycraft`).

1. **No blind model defaults.** `LlmConfig::default().model` MUST start empty (`""`) — never hardcode `"llama3"`, `"qwen3:8b"`, or any unverified model name. On startup (and on demand), an async discovery scan probes local runtimes and picks an actually installed chat model only if no model is configured yet.
2. **Live local discovery:**
   - **Ollama** (`http://127.0.0.1:11434` / `OLLAMA_HOST`): `GET /api/tags` + `GET /api/ps`. Show installed models with parameter size, GB, `[VRAM]` (currently loaded), `[tools]`, and `[embed]` badges. Exclude embedding-only models (`nomic-embed-text`, etc.) from chat auto-selection and clickable chat pickers.
   - **LM Studio / Local OpenAI-Compat** (`http://127.0.0.1:1234` / `LM_STUDIO_URL`): `GET /v1/models` with short connect timeout (<= 2s) so offline servers never stall the UI.
   - **Environment key presence:** Check `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `OPENROUTER_API_KEY`, `GROQ_API_KEY` and display `SET` / `unset` badges only — never display raw key values.
3. **Dedicated `LLM & Settings` Page (not a cramped modal):**
   - Every craft app with an in-app chat dock MUST provide a full-width `LLM & Settings` view/tab reachable from the main navigation rail, `Edit -> LLM & Chat-Einstellungen...`, and clicking the chat dock's provider/model pill or error `Settings` button.
   - Left column / section: **Live Discovery & Clickable Model Picker**.
   - Right column / section: **Provider & Presets** (`Ollama`, `LM Studio`, `Google Gemini`, `OpenAI-Compat` with OpenAI/OpenRouter/Groq presets, `Anthropic`), **BYOK** password-masked API key input (empty = use matching environment key if present), `tools_enabled` / `save_transcripts` / `user_extra_prompt`, **Test Connection** (async minimal completion reporting latency in `ms` or exact error), and **Save**.
4. **Google Gemini & Cloud BYOK:** Support native Google Gemini (`v1beta/models/{model}:generateContent` + `functionDeclarations` + `x-goog-api-key`) alongside `Ollama`, `LmStudio`, `OpenAiCompat`, and `Anthropic`. Use `--connect-timeout 5 --max-time 120` so cold-loading local models does not time out prematurely.
5. **Coop with Agentic DE (MCP):** The `LLM & Settings` page MUST include an **Agentic DE Coop (MCP)** card showing the `<app>-mcp` stdio command and `.\start.ps1 -Mcp` / `.\start.ps1 -Smoke` instructions so users can run the app's tools and bundled skills directly inside Antigravity, Claude, or Cursor without any separate LLM API key.

## 4. Where things live

| Crate | Repo | New / changed | Depends on |
|---|---|---|---|
| `craft-skills` | craft-ai | **new**: `SkillSrc`, `bundle!`, frontmatter parse, MCP `resources/*` JSON, export, tool-reference check | `serde_json` only |
| `craft-ai-core` | craft-ai | **changed**: `chat()` API with history and tools (5.2); `complete()` stops inventing replies (5.1); request body and headers no longer on the command line (5.3) | as today |
| `craft-ai-ui` | craft-ai | **new**: `ChatPanel` + `ChatHost` trait | `egui` 0.37, `craft-ai-core`, `craft-skills` |
| `craft-biz::mcp` | craft-biz | **changed**: `ToolHost::skills()` (default empty) turns on resources and `<app>_skill_read`; tool table gains `read_only` | `craft-skills` |
| `craft-biz-ui` | craft-biz | **changed**: Window > Chat when the app implements `ChatHost`; Skills tab in Help > Project Files & Docs | `craft-ai-ui` |

Apps outside the back-office suite with their own MCP loop (moneycraft, wincraft, gamecraft and others) call the same `craft-skills` functions from their loop. `scripts/sync-craft-scaffold.ps1` carries the snippet.

## 5. `craft-ai-core` changes

### 5.1 `complete()` stops inventing replies

Every failure path returns `Err(AiError::...)`. Callers that relied on `Ok(fallback)` have to handle the error. Known callers (2026-11-14):
- codercraft: `codercraft-agent/src/lib.rs:443`, `codercraft-app/src/main.rs:1838`, `codercraft-core/src/autonomy.rs:223`, `codercraft-core/src/lib.rs:1723`;
- check travelcraft, writercraft and aicraft (they depend on `craft-ai-core`).

This is a breaking change for those callers and is intended.

### 5.2 New chat API (sketch)

```rust
pub enum Role { System, User, Assistant, Tool }
pub struct ToolCall { pub id: String, pub name: String, pub arguments: serde_json::Value }
pub struct ChatMessage { pub role: Role, pub content: String,
                         pub tool_calls: Vec<ToolCall>, pub tool_call_id: Option<String> }
pub struct ToolSpec { pub name: String, pub description: String,
                      pub input_schema: serde_json::Value, pub read_only: bool }
pub struct ChatRequest { pub messages: Vec<ChatMessage>, pub tools: Vec<ToolSpec>,
                         pub max_tokens: u32, pub num_ctx: Option<u32> }
pub enum ChatReply { Text(String), ToolCalls(Vec<ToolCall>) }
pub struct ChatOutcome { pub reply: ChatReply, pub prompt_tokens: Option<u64>,
                         pub completion_tokens: Option<u64> }

/// Sync, curl-based, cancellable. Never returns invented text.
pub fn chat(config: &CraftAiConfig, req: &ChatRequest, cancel: &Cancel)
    -> Result<ChatOutcome, AiError>;
```

Each provider family gets its own mapping (OpenAI-compatible, Anthropic, Ollama), with a unit test per family on recorded request and response JSON.

### 5.3 Transport

- The request body goes to curl through a file, `--data-binary @<file>`, not as an argument. Windows limits a command line to 32,767 characters, and a skills preprompt goes over that.
- Auth headers go through `-H @<file>`, so the API key does not appear in the process list.
- Both files live in a per-user temp folder (`%LOCALAPPDATA%\craft-ai\tmp`) with unique names, and a drop guard deletes them on every path, including errors and cancel.

### 5.4 `ChatHost` (what an app implements)

```rust
pub trait ChatHost {
    fn app_name(&self) -> &str;
    fn skills(&self) -> &'static [craft_skills::SkillSrc];
    fn tools(&self) -> Vec<craft_ai_core::ToolSpec>;
    fn status(&mut self) -> serde_json::Value;          // part 4
    fn selection(&mut self) -> Option<serde_json::Value>; // part 5
    fn call_tool(&mut self, name: &str, args: serde_json::Value, actor: &str)
        -> Result<serde_json::Value, String>;
}
```

In the back-office suite, `craft-biz` implements most of this generically from the existing `ToolHost`. An app only adds `status` and `selection`.

## 6. Migration of existing chats

Of these, homecraft and vmcraft were only located, not read in detail. Check each one before migrating.

| App | Today | Target |
|---|---|---|
| homecraft | Chat view, own `homecraft_core::llm`, user-typed system prompt | `ChatPanel`; the user prompt becomes part 6; delete the own LLM module |
| vmcraft | Own `llm.rs` with `chat()` | `craft-ai-core::chat()`; delete the own module |
| studiocraft | Chat view (not inspected) | Inspect, then `ChatPanel` |
| codercraft | Agent with a system prompt per mode | Keep the agent; mode prompts become skills; optional `ChatPanel` for Q&A |
| travelcraft | Prompt built from the sight's data blob | The blob becomes `selection()`; the fixed instructions become a skill |

## 7. Rollout and effort (AI-assisted)

| Step | Work | Days |
|---|---|---|
| 1 | `craft-skills` crate; `craft-biz::mcp` resources + `<app>_skill_read`; `read_only` in tool tables; taskcraft skills written | 0.5 |
| 2 | `craft-ai-core`: `complete()` errors, transport via files, `chat()` with three provider families + tests; fix codercraft callers | 1 |
| 3 | `craft-ai-ui::ChatPanel`, confirm cards, View prompt, meter, transcripts | 0.5-1 |
| 4 | taskcraft pilot: `ChatHost` (status = `task_status`, selection = open issue), Window > Chat | 0.25 |
| 5 | Other suite apps: skills + chat | 1-2 h each |
| 6 | Non-suite crafts on next touch; the existing five chats per section 6 | per app |

## 8. Definition of done (pilot = taskcraft)

1. All tests in 2.6 pass, and `<app> skills export` output loads in Claude Code as skills.
2. An MCP client sees `skill://taskcraft-workflow/SKILL.md` in `resources/list` and can read it; `task_skill_read` works in a client without resource support.
3. `complete()` returns `Err` with curl missing, server down, bad JSON or an empty reply (one test each); no string containing `craft-ai fallback` or `sovereign synthesis` remains in the crate.
4. A 60 KB request body reaches the server (command-line limit test); the API key never appears in the curl arguments (asserted on the built `Command`).
5. Recorded-JSON tests for tool calls in all three provider families.
6. With Gemma 4 12B on Ollama: "Why is BC-5 blocked?" on the demo DB is answered by a read-only tool call and names BC-4 and BC-6. "Move BC-5 to done" shows a confirm card; after Allow, the history shows actor `chat:ollama/<model>`; after Deny, nothing changes.
7. Cloud provider selected: the banner shows, and the first send needs a confirm.
8. Cancel during a slow reply stops the curl process within 1 s; the UI never freezes (frame time stays under 50 ms during a request).

## Changelog

| Date | Change |
|---|---|
| 2026-11-15 | Added Section 3.9 (LLM Discovery, Dedicated Settings Page, Gemini/BYOK, Agentic DE MCP Coop); reference: `kittycraft`. |
| 2026-11-14 | Draft: audit, skills (layout, embedding, MCP resources, CLI, Help tab, tests), chat (preprompt, tools, errors, privacy, threading, UI), crate map, `craft-ai-core` fixes, migration, rollout, DoD. Pilot: taskcraft. |
