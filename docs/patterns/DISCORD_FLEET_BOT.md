# Discord Fleet Bot

A long-running Discord bot that auto-answers questions about fleet repos in the fleet Discord server. Runs locally on Goliath — no cloud, no per-seat cost.

---

## Architecture

```
User types in #support channel
       │
       ▼
discord bot (Python, discord.py, 24/7)
       │
       ├── intent: "how do I install libreoffice-mcp?"
       │        │
       │        ▼
       │   discord-mcp ask_docs(repo="libreoffice-mcp", query="...")
       │        │
       │        ▼
       │   Ollama (Gemma 4 12B / Qwen 3.5 9B)
       │   reads llms-full.txt + answers
       │
       ├── intent: "convert docx to pdf"
       │        │
       │        ▼
       │   direct tool call via discord-mcp
       │   libreoffice-mcp convert
       │
       └── intent: "what's the status of arxiv-mcp?"
                │
                ▼
           ghaudit or assfixstat result
```

## Components

| Component | Role | Where |
|-----------|------|-------|
| **discord.py bot** | Long-running process, listens to channels, routes intents | Goliath, PM2 or Windows Service |
| **discord-mcp** | MCP tool server for Discord read/write | Goliath, existing port 10756 |
| **Ollama** | Local LLM for RAG Q&A | Goliath, existing port 11434 |
| **ask_docs tool** | Given repo name + query, reads llms-full.txt and answers | discord-mcp tool, or separate fleet-docs-mcp |
| **Fritz (fleet-agent-mcp)** | Manages recurring tasks, cron schedules | Goliath, existing |

## Integration with Fritz

Fritz is the natural scheduler and orchestrator:

| Task | Fritz schedule | What it does |
|------|---------------|--------------|
| **Post release summary** | On `ghaudit` or tag push | Posts release notes from latest GitHub release to #announcements |
| **Weekly fleet pulse** | Every Monday 09:00 | Runs `mcp pulse`, posts alive/dead server table to #general |
| **Stale issue reminder** | Daily | Checks for issues >30d with no activity, posts to #bug-reports |
| **New repo alert** | On `assfix` run completion | Posts "libreoffice-mcp just got its first assfix pass — score 72/100" to #general |
| **Support RAG warm-up** | Every 4 hours | Pre-indexes `llms-full.txt` for all repos into LanceDB for fast Q&A |

The bot process itself is outside Fritz — Fritz triggers events, the bot picks them up and posts. They're decoupled: if the bot is down, Fritz still runs; if Fritz is down, the bot still answers questions.

## Implementation sketch

### Bot script (`scripts/discord-fleet-bot.py`)

```python
import discord
import httpx
import re

INTENT_RE = re.compile(r"(how do I|how to|what is|install|setup|configure)\s+(.+?)(\?|$)", re.I)
REPO_RE = re.compile(r"(libreoffice|arxiv|calibre|plex|kicad|blender|email)-\w*-mcp", re.I)

class FleetBot(discord.Client):
    async def on_message(self, message):
        if message.author.bot or message.channel.name not in ("support", "general"):
            return

        text = message.content
        repo_match = REPO_RE.search(text)
        repo = repo_match.group(0) if repo_match else "libreoffice-mcp"

        if INTENT_RE.search(text):
            # RAG answer via discord-mcp ask_docs or direct Ollama
            answer = await self.ask_docs(repo, text)
            await message.reply(answer[:2000])  # Discord 2000 char limit
        elif "status" in text.lower() or "health" in text.lower():
            pulse = await self.run_mcp_pulse()
            await message.reply(pulse[:2000])

    async def ask_docs(self, repo: str, query: str) -> str:
        """Call discord-mcp tool or Ollama directly with llms-full.txt context."""
        async with httpx.AsyncClient() as client:
            r = await client.post("http://127.0.0.1:10756/mcp", json={
                "jsonrpc": "2.0", "method": "tools/call",
                "params": {"name": "ask_docs", "arguments": {"repo": repo, "query": query}},
                "id": 1,
            })
            return r.json().get("result", {}).get("content", [{}])[0].get("text", "I couldn't find an answer.")
```

### Fritz coworker flow (`fritz`)

```
name: discord-fleet-pulse
cron: "0 9 * * 1"  # Monday 09:00
action: |
  1. Run mcp_pulse tool on fleet-agent-mcp
  2. Format alive/dead table
  3. POST to discord-mcp send_message(channel="general", content=table)
```

## Intel Reports Hub integration

Every event — even silence — should publish a lightweight report to the **Intel Reports Hub** at `http://127.0.0.1:11027/`. This is the pinned tab; it should show everything at a glance.

| Trigger | Report content | Frequency |
|---------|---------------|-----------|
| **New question answered** | Question + answer summary + repo name + timestamp → `intel_reports_publish` | Per message |
| **No questions all day** | "No Discord activity today" heartbeat with fleet pulse summary | Daily at 20:00 |
| **Weekly digest** | Question count by repo, top topics, response time stats | Sunday 18:00 |
| **Bot started / stopped** | Uptime announcement | On event |
| **Error / rate limited** | Brief diagnostic | On event |

This makes `http://localhost:11027/` the true **single-pane-of-glass** for fleet operations: Fritz reports, AIWatcher digests, Discord activity, and ghaudit/assfix/qualitycheck reports all in one place.

The hub already supports `POST /api/reports/publish` with HTML content. The bot just sends a small HTML snippet per event:

```python
async def publish_to_hub(self, title: str, body_html: str):
    async with httpx.AsyncClient() as client:
        await client.post("http://127.0.0.1:11027/api/reports/publish", json={
            "title": title,
            "content": f"<article>{body_html}</article>",
            "source": "discord-fleet-bot",
            "tags": ["discord", "fleet"],
        })
```

## Open questions

| Question | Options |
|----------|---------|
| **Where does the bot run?** | Goliath PM2 service or Windows Scheduled Task |
| **Single channel or all?** | Start with #support only, expand based on usage |
| **How does the bot find the right repo's docs?** | Option A: User mentions repo name in question. Option B: Bot asks "which repo?" Option C: Scans all `llms-full.txt` and picks best match |
| **Do we need a new MCP server (fleet-docs-mcp) or extend discord-mcp?** | Extending discord-mcp with an `ask_docs` tool is cleaner — one server to manage |
| **Rate limiting?** | Discord allows 30 msg/min per bot — fine for a small server |
| **Auth — who can trigger tool calls?** | Only in #support and #general; ignore DMs |

## Next steps

1. Add `ask_docs` tool to discord-mcp (reads llms-full.txt + Ollama RAG)
2. Write the bot script
3. Register it as a Windows service or PM2 process
4. Create Fritz coworker flow for weekly pulse
5. Start with one channel (#support), observe, expand
