# ObsidianMCP - Project Structure

## Directory Layout

```
obsidian-mcp/
â”œâ”€â”€ src/
â”‚   â””â”€â”€ obsidian_mcp/
â”‚       â”œâ”€â”€ __init__.py
â”‚       â”œâ”€â”€ server.py          # FastMCP 3.1.1+.1 server with 21 tools
â”‚       â”œâ”€â”€ config.py          # Pydantic config (needs V2 migration)
â”‚       â”œâ”€â”€ obsidian_manager.py # Core vault operations
â”‚       â””â”€â”€ canvas_tools.py    # Canvas operations
â”œâ”€â”€ mcp-server/                # MCPB package structure
â”‚   â”œâ”€â”€ manifest.json          # MCPB manifest (v0.2)
â”‚   â”œâ”€â”€ assets/
â”‚   â”‚   â””â”€â”€ prompts/           # Prompt templates
â”‚   â”‚       â”œâ”€â”€ system.md      # System prompt (3000+ words)
â”‚   â”‚       â”œâ”€â”€ user.md        # User guide (4000+ words)
â”‚   â”‚       â””â”€â”€ examples.json  # 100+ examples
â”‚   â”œâ”€â”€ src/
â”‚   â”‚   â””â”€â”€ obsidian_mcp/      # Source code (copied from src/)
â”‚   â””â”€â”€ README.md              # MCPB package docs
â”œâ”€â”€ tests/                     # Comprehensive test suite
â”‚   â”œâ”€â”€ conftest.py            # Pytest fixtures
â”‚   â”œâ”€â”€ pytest.ini             # Pytest configuration
â”‚   â”œâ”€â”€ test_server_tools.py   # Unit tests for all 21 tools
â”‚   â”œâ”€â”€ test_integration.py    # End-to-end workflow tests
â”‚   â”œâ”€â”€ test_canvas.py         # Canvas-specific tests
â”‚   â”œâ”€â”€ test_manager.py        # Manager tests (legacy)
â”‚   â”œâ”€â”€ integration_tests.py   # Integration tests (legacy)
â”‚   â””â”€â”€ README.md              # Test documentation
â”œâ”€â”€ .github/
â”‚   â””â”€â”€ workflows/
â”‚       â””â”€â”€ test.yml           # CI/CD workflow
â”œâ”€â”€ scripts/
â”‚   â”œâ”€â”€ backup-repo.ps1
â”‚   â”œâ”€â”€ check-repo-standards.ps1
â”‚   â””â”€â”€ copy-source-to-mcpb.ps1
â”œâ”€â”€ obsidian/                   # Legacy module (may be unused)
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ link_analyzer.py
â”‚   â”œâ”€â”€ manager.py
â”‚   â”œâ”€â”€ note_manager.py
â”‚   â””â”€â”€ vault_operations.py
â”œâ”€â”€ config/
â”‚   â”œâ”€â”€ note_templates.yaml
â”‚   â””â”€â”€ settings.yaml
â”œâ”€â”€ docs/                       # Extensive documentation
â”‚   â”œâ”€â”€ development/
â”‚   â”œâ”€â”€ glama-platform/
â”‚   â”œâ”€â”€ mcp-technical/
â”‚   â”œâ”€â”€ mcpb-packaging/
â”‚   â””â”€â”€ ...
â”œâ”€â”€ pyproject.toml              # Python project config
â”œâ”€â”€ glama.json                  # Glama client configuration
â”œâ”€â”€ Makefile                    # Development commands
â”œâ”€â”€ UPGRADE_SUMMARY.md          # Upgrade documentation
â””â”€â”€ README.md                   # Main documentation
```

## Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚      FastMCP 3.1.1+.1 Server              â”‚
â”‚      (21 tools exposed)                 â”‚
â”‚   - Structured logging (structlog)      â”‚
â”‚   - Server lifespan management          â”‚
â”‚   - Enhanced instructions               â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                 â”‚
                 â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚        ObsidianManager                   â”‚
â”‚   - Vault operations                    â”‚
â”‚   - File I/O (aiofiles)                 â”‚
â”‚   - Frontmatter parsing (YAML)          â”‚
â”‚   - Wikilink extraction (regex)        â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                 â”‚
                 â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚        CanvasTools                       â”‚
â”‚   - JSON Canvas 1.0 parsing             â”‚
â”‚   - Node/edge management                 â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                 â”‚
                 â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚        Obsidian Vault (Files)           â”‚
â”‚   - Markdown files (.md)                â”‚
â”‚   - Canvas files (.canvas)              â”‚
â”‚   - Frontmatter (YAML)                  â”‚
â”‚   - Wikilinks ([[target]])              â”‚
â”‚   - Tags (#tag or frontmatter)          â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

## Key Components

### server.py

Main FastMCP 3.1.1+.1 server with:
- 21 tools across 5 categories
- Structured logging (structlog, JSON to stderr)
- Server lifespan management
- Comprehensive instructions parameter
- Pydantic models:
  - `NoteInfo` - Note metadata
  - `NoteContent` - Full note with content
  - `SearchResult` - Search result with context
  - `VaultStats` - Vault metrics

### obsidian_manager.py

Core operations:
- `list_notes()` - Directory scanning
- `create_note()` - File creation with templates
- `read_note()` - Content + frontmatter parsing
- `update_note()` - Safe write with backup
- `delete_note()` - Move to backup before delete
- `move_note()` - Rename + update references
- `search_*()` - Various search implementations
- `get_backlinks()` - Reverse link lookup
- `find_orphans()` - Graph connectivity analysis

### config.py

Pydantic settings model:
- `vault_path` - Root of Obsidian vault
- `max_file_size` - Limit for reading
- `backup_retention_days` - How long to keep backups
- `search_context_lines` - Context in search results
- `max_search_results` - Result limit

## Entry Points

```bash
# Via uv (recommended)
uv run python -m src.obsidian_mcp.server

# Direct
python -m src.obsidian_mcp.server

# Via Makefile
make install-dev
make test
```

## Testing

Comprehensive test suite with pytest:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src.obsidian_mcp --cov-report=html

# Run specific categories
pytest tests/test_server_tools.py  # Unit tests
pytest tests/test_integration.py   # Integration tests
pytest tests/test_canvas.py -m canvas  # Canvas tests

# Via Makefile
make test
make test-coverage
```

See [tests/README.md](../../../../obsidian-mcp/tests/README.md) for detailed test documentation.

