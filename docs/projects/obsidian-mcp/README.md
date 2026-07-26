# ObsidianMCP

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>


> 📖 **[Installation Guide](INSTALL.md)** — quick start, manual setup, and troubleshooting

**FastMCP 3.1.0 server for Obsidian vault knowledge management**

> **Status**: Beta - Actively developed, API may change  
> **Changelog**: See [CHANGELOG.md](CHANGELOG.md) for recent changes (Settings, vault API, Help/Tools/Vault/Search/Links pages).

Comprehensive MCP server: 21+ tools (vault, search, links, efficiency, canvas), LanceDB RAG semantic search, and agentic workflow with sampling. Optional unified gateway (FastAPI) and webapp with detailed Help, Tools, Vault (CRUD/viewer), Search, Links, Chat, LLM, and Settings (persistent vault path).

## Quick Start

```powershell
git clone https://github.com/sandraschi/obsidian-mcp
cd obsidian-mcp
just
```

This opens an interactive dashboard showing all available commands. Run `just bootstrap` to install dependencies, then `just serve` or `just dev` to start.

### Manual Setup

If you don't have `just` installed:

## Features

**21+ tools** across 6 categories:

### Vault Operations (6 tools)
- `list_notes` - List vault notes with optional folder filtering, showing modification times, sizes, tags, and links
- `create_note` - Create new notes with title, content, and optional folder placement
- `read_note` - Read complete note content including YAML frontmatter, extracted tags, wikilinks, and metadata
- `update_note` - Update existing note content with automatic backup protection
- `delete_note` - Delete notes with backup protection (moves to backup location)
- `move_note` - Move or rename notes with automatic wikilink updates throughout vault

### Search Operations (3 tools)
- `search_content` - Full-text search across all notes with context snippets
- `search_tags` - Find all notes containing a specific tag (frontmatter or inline)
- `search_links` - Find notes containing specific wikilink targets

### Link Analysis (3 tools)
- `get_backlinks` - Find all notes that link TO a specified note
- `get_outlinks` - Extract all outbound links FROM a specified note
- `find_orphans` - Identify disconnected notes (no backlinks and no outlinks)

### Austrian Efficiency Tools (3 tools)
- `todays_notes` - Get notes for today's workflow focus (recently modified notes)
- `quick_note` - Fast capture without friction - creates timestamped note in quick/ folder
- `vault_stats` - Vault overview metrics including total notes, size, tags, links, and orphans

### Canvas Operations (6 tools)
- `list_canvases` - List all Obsidian Canvas files (.canvas) with metadata
- `read_canvas` - Read and parse canvas files (JSON Canvas 1.0 format)
- `create_canvas` - Create new canvas files with nodes and edges
- `add_canvas_node` - Add new nodes (text, file, link, group) to existing canvases
- `add_canvas_edge` - Add edges connecting nodes in canvases
- `delete_canvas` - Delete canvas files with optional backup protection

### RAG and agentic (FastMCP 3.1.0)
- `rag_status` - Check if global RAG index exists (all vaults)
- `index_vault` - Index notes from **all** configured vaults into LanceDB (sentence-transformers; one global DB)
- `semantic_search_vault` - Meaning-based search over all indexed vaults (results include vault_name)
- `obsidian_agentic_workflow` - Multi-step vault goals via sampling (list_notes, read_note, search_content, semantic_search_vault)

## Gateway and webapp

- **Gateway** (port 10915): `uv run uvicorn obsidian_mcp.gateway:app --host 127.0.0.1 --port 10915`  FastAPI with `/api/help`, `/api/help/detailed`, `/api/tools`, `/api/settings`, `/api/vaults`, `/api/obsidian/*` (live status, insert-at-cursor, open-note URI), `/api/llm/*` (Ollama proxy), `/api/rag/*` (LanceDB; all vaults), and `/api/vault/*` (notes CRUD, stats, search, links; active vault).
- **Webapp**: From `web_sota/` run `./start.ps1` (PowerShell) to start gateway + Vite dev server.
  - **Settings**: Set vault path (persistent; no hardcoded paths). Shows active vault; link to Vaults for multi-vault.
  - **Vaults**: Multiple vaults supported. List vaults, add/edit/delete, switch active, view stats (notes, tags, orphans) per vault. Vault/Search/Links use the active vault; RAG indexes and searches across all vaults.
  - **Help**: Detailed guide (Webapp, MCP Server, Obsidian, **Infinite Canvas**, **Plugins & API**) plus quick reference.
  - **Tools**: List of all MCP tools by category.
  - **Vault**: List notes, open/view/edit/delete, create new notes (folder filter, stats).
  - **Search**: Full-text search with context snippets.
  - **Links**: Orphans, backlinks (by note name), outlinks (by note path).
  - **Semantic**: RAG semantic search (LanceDB; index all vaults once, then search across them; results show vault name).
  - **Chat**, **LLM**, **Status**.
- **Live integration (optional)**: Install the **Obsidian MCP Bridge** plugin (see `plugin/`) in your vault; when Obsidian is open with that vault, the webapp shows **Live** and you get **Open in Obsidian** and **Insert at cursor**. Help has tabs for **Infinite Canvas** and **Plugins & API**.

## Standards and formats

- **File-first**: The MCP server and gateway work by reading/writing the vault folder (markdown, frontmatter, wikilinks, `.canvas` files). No Obsidian app required. Optional **Obsidian MCP Bridge** plugin uses the Obsidian Plugin API for live features (open in app, insert at cursor) when Obsidian is open.
- **Vault format**: Plain markdown (`.md`), YAML frontmatter, `[[wikilinks]]`, `#tags`  standard Obsidian vault conventions, stable.
- **JSON Canvas 1.0**: Canvas tools follow the [JSON Canvas 1.0](https://jsoncanvas.org/spec/1.0/) spec (2024-03): top-level `nodes` and `edges`, node `id`/`type`/`x`/`y`/`width`/`height`, edge `fromNode`/`toNode`, optional `fromSide`/`toSide`/`label`/`color`. Aligned with Obsidians `.canvas` format.

## Requirements

- Python 3.11+
- FastMCP 3.1.0+
- Obsidian vault (any folder with markdown files)
- Optional: Ollama (for gateway LLM and agentic sampling), sentence-transformers (for RAG)

##  Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

###  Quick Start
Run immediately via `uvx`:
```bash
uvx obsidian-mcp
```

###  Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "obsidian-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/obsidian-mcp", "run", "obsidian-mcp"]
  }
}
```
### MCPB Package (Claude Desktop)

1. Build MCPB package:
```bash
npm install -g @anthropic-ai/mcpb
mcpb pack mcp-server dist/obsidian-mcp-v1.0.0.mcpb
```

2. Install in Claude Desktop:
   - Open Claude Desktop settings
   - Drag `obsidian-mcp-v1.0.0.mcpb` file into settings
   - Configure `vault_path` setting

3. Install Python dependencies separately:
```bash
pip install FastMCP 3.1.0,<2.15.0 pydantic>=2.0.0 python-dotenv>=1.0.0 structlog>=23.0.0 pyyaml>=6.0.0 aiofiles>=23.0.0
```

### Glama Client

1. Clone repository:
```bash
git clone https://github.com/sandraschi/obsidian-mcp
cd obsidian-mcp
```

2. Install dependencies:
```bash
pip install -e .
```

3. Configure `glama.json` is already included in repository root

4. Set vault path via environment variable:
```bash
export OBSIDIAN_VAULT_PATH=/path/to/your/vault
```

## Configuration

### Vault path (required for vault and RAG)

- **Webapp (recommended)**: Open **Settings** in the webapp and set the vault path. Stored persistently in a platform-specific config file (e.g. `%APPDATA%/obsidian-mcp/settings.json` on Windows, `~/.config/obsidian-mcp/settings.json` on Unix). No hardcoded paths.
- **Environment variable**: `OBSIDIAN_VAULT_PATH` overrides the saved setting when set. Create a `.env` file or set the variable:

```env
OBSIDIAN_VAULT_PATH=D:\Path\To\Your\Vault
```

### Claude Desktop Config

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "obsidian-mcp": {
      "command": "python",
      "args": ["-m", "src.obsidian_mcp.server"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "D:\\Path\\To\\Your\\Vault",
        "PYTHONPATH": "${PWD}",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### Glama Configuration

The `glama.json` file in the repository root provides Glama client configuration. Ensure `OBSIDIAN_VAULT_PATH` is set in your environment.

## Usage

### Run Server

```bash
uv run python -m src.obsidian_mcp.server
```

Or:

```bash
python -m src.obsidian_mcp.server
```

### Example Workflows

#### Quick Capture

```
"Quick note: Meeting with Alice tomorrow at 3pm about project X"
```

Creates timestamped note in `quick/` folder with automatic title generation.

#### Find Orphan Notes

```
"Show me notes that have no connections"
```

Returns list of isolated notes that need linking to the knowledge graph.

#### Today's Focus

```
"What notes should I focus on today?"
```

Returns recently modified notes for context on current work.

#### Search and Explore

```
"Find all notes about MCP servers"
```

Uses full-text search with context snippets.

```
"What notes link to 'FastMCP Migration'?"
```

Uses backlink analysis to explore knowledge graph connections.

#### Canvas Creation

```
"Create a canvas showing the relationship between my MCP projects"
```

Creates visual knowledge map with nodes and edges.

## Obsidian Vault Structure

### Note Format
- **File Format**: Markdown (.md) files with optional YAML frontmatter
- **Wikilinks**: Use `[[note-name]]` format for bidirectional linking
- **Tags**: Use `#tag` format inline or in frontmatter as `tags: [tag1, tag2]`
- **Frontmatter**: YAML metadata block at top of note (between `---` delimiters)

### Canvas Format
- **File Format**: JSON Canvas 1.0 specification (.canvas files)
- **Node Types**: text (markdown cards), file (vault file references), link (URLs), group (containers)
- **Edges**: Connections between nodes with optional labels and colors
- **Colors**: Use "1" through "6" for Obsidian preset colors or hex codes

### Vault Organization
- **Folder Structure**: Organize notes in folders (e.g., `projects/`, `notes/`, `quick/`)
- **Path Format**: Relative paths from vault root (e.g., `projects/mcp-server.md`)
- **Backup Location**: Deleted notes moved to `.obsidian-mcp-backups/` folder

## Integration

### With Obsidian Desktop

- Use ObsidianMCP for programmatic operations and bulk changes
- Use Obsidian Desktop for visual graph editing and manual organization
- Both can work on same vault simultaneously
- Changes made via MCP appear immediately in Obsidian Desktop

### With Advanced Memory MCP

ObsidianMCP can work alongside Advanced Memory MCP:

1. **Same folder:** Point both at same directory
2. **Composite server:** Mount both in a hub
3. **Bidirectional sync:** Use Obsidian for visual graph, ADN for AI enhancement

See: [ADN and Obsidian Bidirectional Sync Strategy](../mcp-central-docs/docs/projects/obsidianmcp/STATUS.md)

### With Git

- Vault can be version controlled with Git
- MCP operations create standard markdown files compatible with Git
- Canvas files are JSON, also Git-friendly
- Backup folder (`.obsidian-mcp-backups/`) should be in `.gitignore`

## Technical Details

### FastMCP 3.1.0 Compliance

-  FastMCP 3.1.0+ with `run_stdio_async()` method
-  Server lifespan for startup/shutdown lifecycle
-  Comprehensive instructions parameter for AI understanding
-  Structured logging (structlog) with stderr output only
-  Enhanced response patterns for rich dialogue
-  No stdout writes (reserved for MCP protocol)

### Architecture

- **Server**: FastMCP 3.1.0 with async/await support
- **Storage**: File system operations with async I/O (aiofiles)
- **Parsing**: YAML frontmatter, markdown wikilinks, JSON Canvas
- **Logging**: Structured JSON logging to stderr (stdout reserved for MCP protocol)

### Security

- Automatic backup protection for delete/update operations
- Path validation to prevent directory traversal
- Safe file operations with error handling
- No command injection risks (file operations only)

## Troubleshooting

### Vault Not Found

**Error**: "Vault path not configured or invalid" or 503 "Vault path not set"

**Solution**: 
1. Set vault path in the webapp **Settings** page (persistent), or set `OBSIDIAN_VAULT_PATH` in the environment.
2. Verify the path is correct and the directory exists and is accessible.
3. Check file system permissions.

### Note Not Found

**Error**: "Note path does not exist in vault"

**Solution**:
1. Use `list_notes()` to see available notes
2. Use `search_content()` to search for note content
3. Check if note is in subfolder (use folder parameter)
4. Verify note path is relative to vault root

### Permission Errors

**Error**: "File system permission error"

**Solution**:
1. Check file permissions
2. Ensure vault directory is writable
3. Verify user has read/write access

## Development

### Project Structure

```
obsidian-mcp/
 src/
    obsidian_mcp/
        server.py          # Main FastMCP server
        obsidian_manager.py # Vault operations
        config.py          # Configuration management
        canvas_tools.py    # Canvas operations
 mcp-server/                # MCPB package structure
    manifest.json          # MCPB manifest
    assets/
       prompts/           # Prompt templates
    src/                   # Source code (copied)
 tests/                     # Test suite
 glama.json                 # Glama client configuration
 pyproject.toml            # Python project configuration
```

### Running Tests

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src.obsidian_mcp --cov-report=html

# Run specific test file
pytest tests/test_server_tools.py -v
```

### Code Quality

```bash
# Linting
ruff check src/ tests/

# Formatting
ruff format src/ tests/

# Type checking
mypy src/

# Via Makefile
make lint
make format
make type-check
make check  # Run all checks
```


## 🛡️ Industrial Quality Stack

This project adheres to **SOTA 14.1** industrial standards for high-fidelity agentic orchestration:

- **Python (Core)**: [Ruff](https://astral.sh/ruff) for linting and formatting. Zero-tolerance for `print` statements in core handlers (`T201`).
- **Webapp (UI)**: [Biome](https://biomejs.dev/) for sub-millisecond linting. Strict `noConsoleLog` enforcement.
- **Protocol Compliance**: Hardened `stdout/stderr` isolation to ensure crash-resistant JSON-RPC communication.
- **Automation**: [Justfile](./justfile) recipes for all fleet operations (`just lint`, `just fix`, `just dev`).
- **Security**: Automated audits via `bandit` and `safety`.

## License

MIT License

## Author

Sandra Schi - [GitHub](https://github.com/sandraschi)

## Related Projects

- [Advanced Memory MCP](../advanced-memory-mcp) - AI-enhanced knowledge management
- [MCP Central Docs](../mcp-central-docs) - MCP standards and documentation
