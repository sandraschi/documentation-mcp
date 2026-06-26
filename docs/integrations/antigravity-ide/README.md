# Google Antigravity IDE — MCP Client Reference

**Last Updated:** 2026-03-23
**Also known as:** Google AI Studio IDE, Gemini IDE
**MCP config location:** `C:\Users\sandr\.gemini\antigravity`
**⚠️ Non-standard path** — NOT in AppData\Roaming, NOT in standard IDE config locations

---

## What Antigravity Is

Google's AI-first IDE (VS Code fork, similar positioning to Cursor/Windsurf). Uses Gemini
models as the primary AI backend. MCP support added in early 2026.

One of our three primary MCP clients alongside Claude Desktop and Cursor. Less mature MCP
implementation than Claude Desktop or Cursor as of March 2026, but actively developed.

---

## ⚠️ Critical: Non-Standard Config Path

**Config location:** `C:\Users\sandr\.gemini\antigravity`

This is unusual — most IDE MCP configs are in:
- `AppData\Roaming\<AppName>\` (Windows standard)
- `%USERPROFILE%\.<appname>\` (Unix-style dotfile)

Antigravity uses `%USERPROFILE%\.gemini\antigravity` — the `.gemini` parent directory
suggests Google is consolidating AI tool configs under a shared namespace.

Do NOT look for it in AppData — it won't be there.

---

## MCP Config Format

Format is the same JSON structure as Claude Desktop and Cursor:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["D:\\Dev\\repos\\my-server\\server.py"]
    }
  }
}
```

**Sync with master config:** `D:\Dev\repos\mcp-central-docs\operations\MASTER_MCP_CONFIG.json`

---

## CodeMode / tool_search in Antigravity

Antigravity handles CodeMode the same way as Claude Desktop and Cursor at the protocol level
— it calls `tool_search` before using tools on a CodeMode server. As of March 2026,
Antigravity's MCP client is newer and may behave slightly differently in edge cases.

The benefit is the same: CodeMode prevents Antigravity from loading hundreds of tool schemas
into the Gemini model context at session start — important because Gemini's tool-use context
handling differs from Claude's.

**If tools seem not to work in Antigravity:** Check that `tool_search` is being called first.
Some MCP client implementations skip the discovery step and try to call tools directly,
which fails if the server uses CodeMode.

---

## Gemini Model Context

Antigravity uses Gemini models. Gemini handles MCP tool schemas differently from Claude:
- Gemini has a very large context window (1M+ tokens in Gemini 2.5 Pro / 3 Pro)
- Context bloat is less catastrophic than in Claude Desktop, but still wastes tokens
- Gemini's tool-calling format differs from Anthropic's — FastMCP handles translation
- CodeMode still valuable: keeps the active context clean regardless of window size

---

## Known Antigravity MCP Quirks (as of March 2026)

| Issue | Status |
|-------|--------|
| MCP support added early 2026 — still maturing | Expect occasional issues |
| Config path non-standard | Always check `.gemini\antigravity`, not AppData |
| Gemini tool call format differences | FastMCP 3.x handles this transparently |
| Restart required after config changes | Same as all MCP clients |

---

## AI Models Available

(as of March 2026 — update when model roster changes)

| Model | Use case |
|-------|---------|
| Gemini 3 Pro | Flagship, best quality |
| Gemini 3 Flash | Fast, everyday tasks |
| Gemini 3 Deep Think | Extended reasoning |
| Gemini 2.5 Flash-Lite | Budget/fast |

Local via Ollama (on Goliath): Gemma 3 27B, Llama 3.3 70B — NOT available in Antigravity
directly, but accessible via `local-llm-mcp` server if configured.

---

## Relevant Docs

- Master MCP config: `operations/MASTER_MCP_CONFIG.json`
- CodeMode / tool_search: `fastmcp/code-mode.md`
- Claude Desktop comparison: `integrations/claude-desktop/README.md`
- Cursor IDE: `integrations/cursor-ide/README.md`
- Local LLM standards: `standards/LOCAL_LLM_STANDARDS.md`
