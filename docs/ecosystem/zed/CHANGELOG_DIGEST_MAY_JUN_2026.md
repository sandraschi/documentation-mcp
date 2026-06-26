# Zed Changelog Digest — May–June 2026

**Status:** Active  
**Updated:** 2026-06-06  
**Source:** [zed.dev/releases/stable](https://zed.dev/releases/stable) · [Releasebot feed](https://releasebot.io/updates/zed)  
**Prior digest:** [ZED_LATEST_RESEARCH_APR_2026.md](../../integrations/zed/ZED_LATEST_RESEARCH_APR_2026.md) (0.230.x)

Fleet-focused summary of Zed **1.3.5 → 1.4.4** and June weekly stable. Contrast with [Cursor Jun digest](../cursor/CHANGELOG_DIGEST_JUN_2026.md).

---

## Timeline

| Date | Version | Headline |
|------|---------|----------|
| May 20 | 1.3.5 | **Terminal Threads**, Mermaid/images in agent, `subagent_model`, Git history |
| May 21–28 | 1.3.6–1.4.4 | Gemini 3.5 Flash, Copilot fixes |
| May 27 | 1.4.2 | **Agent Skills**, global **AGENTS.md**, MCP OAuth + image output |
| Jun weekly | (stable) | Mermaid v2, thread rename, OpenAI Fast Mode, ACP registry migration |

---

## 1. Agent / MCP (May–Jun)

### Terminal Threads (1.3.5)

Run **Claude Code, Amp, OpenCode**, etc. as threads in the sidebar — external agents beside Zed’s built-in agent.

**Fleet stance:** Second lane for ACP-native tools without leaving Zed; does not replace Fritz/cursor-mcp orchestration.

### Skills replace Rules (1.4.2) — breaking

- Rules library **removed** → **Agent Skills** (aligned with Cursor skills direction)
- Global **`AGENTS.md`** next to `settings.json` — user-wide instructions in every project system prompt
- Commands to open global vs project `AGENTS.md`
- Skill Creator: import from GitHub Markdown URLs (preview); copy/move/delete under `~/.agents/skills/`

**Fleet stance:** Mirror fleet skills into `~/.agents/skills/` or project `.agents/skills/`; keep canonical docs in `mcp-central-docs`.

### MCP upgrades (1.4.2+)

| Feature | Detail |
|---------|--------|
| **Image output** from MCP tools | Agent panel renders tool images |
| **OAuth pre-registration** | Client id/secret for MCP servers in built-in client |
| **OAuth fixes** | Broken metadata URLs, registration failures |
| **Gemini schema fixes** | Tool calls via MCP no longer break on JSON schema |

### Agent UX (May–Jun)

- **Mermaid** in agent (1.3.5); **faster/accurate renderer** (June)
- **Inline images** in agent output
- **`subagent_model`** — pick model for spawned subagents
- Clickable `` `path:line` `` in agent panel
- Thread rename in sidebar; project reorder; completion notification on collapsed headers
- OpenAI **Fast Mode** (priority tier) for API + ChatGPT subscription providers

### ACP (June) — breaking

- **ACP extensions removed** → migrate to **ACP registry** servers
- ACP logout flow; external agents can access all worktrees in a project

---

## 2. Git / editor (still Zed’s strength)

- Git panel **branch history** + custom commands from Git Graph (1.3.5)
- Choose **base branch** in diff view; **toggle all diff hunks** (1.4.2)
- Changes/History tab shortcuts (`ctrl-1` / `ctrl-2` on Windows)
- Zoomable commit message editor; Forgejo/GitLab/Bitbucket remote icons
- Dev container **local features** (June)
- LSP **clickable document links** (default on)

---

## 3. FOSS and token cost — fleet stance

### Still FOSS?

**Yes.** Zed remains open source ([zed-industries/zed](https://github.com/zed-industries/zed), GPL). No proprietary fork required to build or audit the editor. Optional Zed account / hosted models are **add-ons**, not lock-in on the binary.

### Nullify token cost?

| Provider | Inference cost | Fleet default |
|----------|----------------|---------------|
| **Ollama** (`localhost:11434`) | **$0** (electricity + GPU you own) | **Primary** — pairs with [local-llm-mcp](../../integrations/local-llm/README.md) |
| **LM Studio** (OpenAI-compatible local) | **$0** | **Primary** on Windows when Ollama model set differs |
| **OpenAI API Compatible** | Depends on endpoint | Local vLLM, LM Studio, fleet gateways |
| **OpenRouter** | **Pay per token** — not $0 | **Fallback only** — use `sort: "price"`, cheap models, budgets |
| **DeepSeek cloud** (`deepseek-v4-flash`) | **Cheap paid** — strong agentic/$ | **Sweet spot** for Zed built-in agent + MCP (needs Zed **≥1.4** / V4 PR merged) |
| **DeepSeek** (`deepseek-v4-pro`) | Higher $, more capability | Hard refactors only |
| **Zed-hosted / ChatGPT sub / Copilot** | Subscription or metered | Avoid for fleet default |

**Docs:** [zed.dev/docs/ai/llm-providers](https://zed.dev/docs/ai/llm-providers) — Ollama, LM Studio, OpenRouter all first-class in `settings.json` → `language_models`.

### Example — $0 default (Ollama)

```json
{
  "agent": {
    "default_model": {
      "provider": "ollama",
      "model": "qwen3.5:9b"
    }
  },
  "language_models": {
    "ollama": {
      "api_url": "http://localhost:11434",
      "available_models": [
        {
          "name": "qwen3.5:9b",
          "max_tokens": 32768,
          "supports_tools": true
        }
      ]
    }
  }
}
```

### Example — cheap cloud fallback (OpenRouter)

```json
{
  "agent": {
    "default_model": {
      "provider": "openrouter",
      "model": "openrouter/auto"
    }
  },
  "language_models": {
    "open_router": {
      "api_url": "https://openrouter.ai/api/v1",
      "available_models": [
        {
          "name": "openrouter/auto",
          "max_tokens": 200000,
          "supports_tools": true,
          "provider": {
            "sort": "price",
            "allow_fallbacks": true
          }
        }
      ]
    }
  }
}
```

Set `OPENROUTER_API_KEY` in env. This **minimizes** cost; it does **not** nullify it.

### Example — cheap cloud default (DeepSeek V4 Flash)

Requires **updated Zed** (native `deepseek-v4-flash` / `deepseek-v4-pro` since ~1.4, [PR #54731](https://github.com/zed-industries/zed/pull/54731)). Set `DEEPSEEK_API_KEY`; use `https://api.deepseek.com` **without** `/v1`.

```json
{
  "agent": {
    "default_model": {
      "provider": "deepseek",
      "model": "deepseek-v4-flash"
    }
  },
  "language_models": {
    "deepseek": {
      "api_url": "https://api.deepseek.com",
      "available_models": [
        {
          "name": "deepseek-v4-flash",
          "display_name": "DeepSeek V4 Flash",
          "max_tokens": 1000000,
          "max_output_tokens": 384000,
          "supports_tools": true
        }
      ]
    }
  }
}
```

**Tiering:** Ollama/LM Studio for $0 drafts → **DS V4 Flash** for tool+MCP sessions → V4 Pro only when Flash stalls.

### Zed agent vs OpenCode (arms race)

| Lane | What | When |
|------|------|------|
| **Zed built-in agent** | Native panel + fleet MCP + DeepSeek/Ollama provider | Daily edit, fast UI, Git-native |
| **OpenCode** (`opencode-cli-mcp` :10951, Terminal Threads) | Separate agent runtime; fleet uses `deepseek/deepseek-v4-flash` in opencode run | Heavy multi-file jobs, Fritz `fleet_bridge` |
| **Cursor** | MCP + cloud agents + spend watch (`cursor-mcp`) | Where Cursor-specific features matter |

Zed ships **OpenCode as a provider** and **Terminal Threads** — they are integrating the competitor, not ignoring it. Fleet can use **both**: Zed for interaction, OpenCode when the harness wins.

**Watch:** DeepSeek **DSML** tool-call format vs standard JSON tools — verify MCP tool rounds on V4 Flash before making it the only default.

### MCP in Zed

MCP servers (fleet FastMCP) attach via `%APPDATA%\Zed\settings.json` — same servers as Cursor, **no Cursor subscription** required. Agent tool calls hit **your** chosen model provider.

---

## 4. Zed vs Cursor (Jun 2026)

| Dimension | Zed | Cursor |
|-----------|-----|--------|
| **License** | FOSS (GPL) | Proprietary |
| **$0 inference** | Ollama / LM Studio native | **No** — see [cursor/NO_LOCAL_PROVIDER.md](../cursor/NO_LOCAL_PROVIDER.md), [IDE matrix](../IDE_LOCAL_INFERENCE.md) |
| **Agent spectacle** | Steady weekly editor releases | Feature bombs (canvas, Design Mode, cloud agents, SDK) |
| **Token diagnostics** | No context-usage canvas yet | Context canvas + billing anxiety |
| **Orchestration** | Sidebar threads + ACP | Parallel cloud agents, SDK automation |
| **Fleet fit** | Local LLM sovereignty, fast UI | MCP-heavy daily driver, cursor-mcp spend watch |

**Honest gap:** Zed still lacks Cursor-scale cloud agent factory, Design Mode, and org spend APIs. **Honest win:** you can run the agent panel on **local models only** and keep inference off Cursor’s meter.

---

## Fleet adoption priority

| Priority | Action |
|----------|--------|
| **P0** | Default Zed agent to **Ollama/LM Studio**; OpenRouter only for tasks local models fail |
| **P1** | Migrate rules → **skills**; add fleet `AGENTS.md` globally |
| **P1** | Register fleet MCP in Zed `settings.json` (stdio + OAuth where needed) |
| **P2** | Try **Terminal Threads** for Claude Code/Amp beside built-in agent |
| **P2** | Git panel history + base-branch diffs for PR hygiene |
| **P3** | ACP registry agents after extension migration |

---

## Risks

- **Vulkan on Windows/Linux:** Still experimental for heavy agent streaming — prefer **DirectX 11** on Sandra workstations
- **Tool-capable local models:** Verify `supports_tools: true` in Ollama model config
- **OpenRouter:** Easy to accidentally burn tokens — not a $0 path

---

## References

- [Stable releases](https://zed.dev/releases/stable)
- [LLM providers](https://zed.dev/docs/ai/llm-providers)
- [ZED_FOSS_AND_LOCAL_LLM.md](../../integrations/zed/ZED_FOSS_AND_LOCAL_LLM.md)
- [local-llm-mcp](../../integrations/local-llm/README.md)
- [Cursor Jun digest](../cursor/CHANGELOG_DIGEST_JUN_2026.md)
