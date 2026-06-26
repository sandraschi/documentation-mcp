# Justfile Recipe Patterns (Fleet Standard)

Every MCP server repo SHOULD have repo-specific `just` recipes beyond the standard `lint`/`test`/`serve` ones. These give the developer (or agent) one-shot access to the server's core functionality without crafting MCP tool calls or opening the webapp.

## Standard Sections

Every justfile should have these sections in order:

```
# ── Quality ──    lint, fix, tsc
# ── Testing ──   test, test-v
# ── Serving ──   serve, stdio, dev
# ── Python ──    sync, sync-web
# ── <REPO> ──    domain-specific recipes
# ── Utilities ── mcpb-pack, install-mcp
```

## Repo-Specific Recipe Patterns

### Universal `install` recipe (first Python recipe)

Every repo MUST have an `install` recipe that handles post-clone setup:

```just
# Install all deps (Python + frontend). Run after git clone.
install sync="":
    cd '{{justfile_directory()}}'
    uv sync {{sync}}
    if (Test-Path '{{justfile_directory()}}\web_sota') { \
        Push-Location '{{justfile_directory()}}\web_sota'; npm install; Pop-Location }
    elseif (Test-Path '{{justfile_directory()}}\webapp') { \
        Push-Location '{{justfile_directory()}}\webapp'; npm install; Pop-Location }
    Write-Host "Install complete. Run: just install-mcp claude" -ForegroundColor Green
```

This enables the post-clone workflow:

```powershell
git clone https://github.com/sandraschi/arxiv-mcp.git
cd arxiv-mcp
just install
just install-mcp claude    # optional: configure Claude Desktop
just serve                 # start the server
```

| Repo | Recipe | One-liner |
|------|--------|-----------|
| ***generic*** | `just install-mcp <client>` | Install MCP into client config |
| ***generic*** | `just mcpb-pack` | Create .mcpb bundle |
| **arxiv-mcp** | `just search "<query>"` | Search arXiv papers |
| **arxiv-mcp** | `just paper "<id>"` | Get paper details |
| **arxiv-mcp** | `just resolve-doi "<doi>"` | Resolve DOI to metadata |
| **arxiv-mcp** | `just full-text "<id>"` | Fetch full text |
| **aiwatcher-mcp** | `just poll` | Poll all feeds (HTTP API; server must be running) |
| **aiwatcher-mcp** | `just poll-ingest` | Poll feeds in-process (no server) |
| **aiwatcher-mcp** | `just distill` | Run Claude distillation (HTTP API) |
| **aiwatcher-mcp** | `just distill-ingest` | Distill in-process (no server) |
| **aiwatcher-mcp** | `just alerts` | Check critical alerts |
| **obsidian-mcp** | `just vault-stats` | Vault statistics |
| **obsidian-mcp** | `just reindex` | Rebuild LanceDB index |
| **robofang** | `just council-status` | Council health summary |
| **robofang** | `just heartbeat` | Heartbeat status |
| **deepfang** | `just supervisor` | Supervisor status |
| **federation-hub** | `just servers` | List all fleet servers |
| **federation-hub** | `just peers` | Mesh peer status |
| **speech-mcp** | `just speak "<text>"` | Speak via TTS |
| **speech-mcp** | `just voices` | List available voices |
| **godot-mcp** | `just demo-run <game>` | Run sample (heart, dodge, platformer, …) |
| **godot-mcp** | `just install-export-templates` | Download Godot export templates (once) |
| **godot-mcp** | `just little-game-export web [game]` | Export HTML5 for itch.io |
| **godot-mcp** | `just little-game-pack web [game]` | Zip web build for manual itch upload |
| **godot-mcp** | `just little-game-export windows [game]` | Export Windows `.exe` |
| **godot-mcp** | `just itch-status` | Butler + API key status |
| **godot-mcp** | `just itch-push <dir>` | Butler push via REST |
| **godot-mcp** | `just ship web [game]` | Export + preview + push to itch.io |
| **godot-mcp** | `just bridge-test` | Smoke: godot_status via REST |

## Implementation Pattern

Each recipe should be a single `uv run python -c` or `curl` call that:

1. Uses the server's own code/API (no external deps)
2. Formats output as clean text (JSON for pipes, pretty-print for humans)
3. Exits non-zero on failure

```just
# Search arXiv papers
search query="transformer":
    uv run python -c "import asyncio; from arxiv_mcp.services.papers import search_papers; r=asyncio.run(search_papers('{{query}}',limit=5)); [print(f'{p.paper_id}: {p.title[:80]}') for p in r]"

# Speak via TTS
speak text="hello":
    curl -s -X POST http://127.0.0.1:10909/api/v1/tts -H "Content-Type: application/json" -d '{"text":"{{text}}"}'
```

Recipes that call the server API assume the backend is running. Add a health check guard if needed.
