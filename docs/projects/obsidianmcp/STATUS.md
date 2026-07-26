# ObsidianMCP - Status

## Health Check

| Metric | Status |
|--------|--------|
| **Server Starts** | âœ… Yes |
| **Python Version** | 3.11+ (3.13 works) |
| **Framework** | FastMCP 3.1.1+.1 |
| **Tools Count** | 21 (6 vault + 3 search + 3 links + 3 efficiency + 6 canvas) |
| **Status** | Beta - Actively developed, API may change |
| **Test Coverage** | âœ… Comprehensive test harness (pytest) |
| **MCPB Packaging** | âœ… Complete (manifest + prompts) |
| **Glama Support** | âœ… Configured |
| **Last Verified** | December 2025 |

## Recent Upgrades (December 2025)

### âœ… FastMCP 3.1.1+.1 Migration
- Migrated from FastMCP 3.1.1+.0 to 3.1.1+.1
- Updated to `run_stdio_async()` method
- Added server lifespan with `@asynccontextmanager`
- Added comprehensive `instructions` parameter
- All tools use docstring-based documentation (no `description=` parameters)

### âœ… Structured Logging
- Replaced `rich.console` with `structlog`
- JSON logging output to stderr only (stdout reserved for MCP protocol)
- Removed all stdout writes

### âœ… MCPB Packaging
- Complete MCPB package structure (`mcp-server/`)
- Comprehensive prompt templates (system.md, user.md, examples.json)
- Manifest with proper metadata and configuration

### âœ… Test Harness
- Comprehensive pytest test suite
- Unit tests for all 21 tools
- Integration tests for end-to-end workflows
- Canvas-specific tests
- GitHub Actions CI/CD workflow

### âœ… Code Quality
- All ruff linting issues resolved
- Proper async/await patterns
- Structured error handling
- Type hints throughout

## Known Issues

### Pydantic V1 Validators (Minor)

The `config.py` uses deprecated Pydantic V1 `@validator` decorators. Should migrate to `@field_validator`. Non-blocking but will break in Pydantic V3.

```python
# Current (deprecated)
@validator('vault_path')

# Should be
@field_validator('vault_path')
```

## Tool Categories

### Vault Operations (6 tools)

| Tool | Purpose |
|------|---------|
| `list_notes` | List notes with folder filtering |
| `create_note` | Create new note in vault |
| `read_note` | Read with frontmatter parsing |
| `update_note` | Update with automatic backup |
| `delete_note` | Delete with backup protection |
| `move_note` | Move/rename with link updates |

### Search Operations (3 tools)

| Tool | Purpose |
|------|---------|
| `search_content` | Full-text search with context snippets |
| `search_tags` | Find notes by tag |
| `search_links` | Find notes by wikilink target |

### Link Analysis (3 tools)

| Tool | Purpose |
|------|---------|
| `get_backlinks` | Find notes linking TO a note |
| `get_outlinks` | Find what a note links TO |
| `find_orphans` | Find disconnected notes |

### Austrian Efficiency (3 tools)

| Tool | Purpose |
|------|---------|
| `todays_notes` | Today's workflow focus |
| `quick_note` | Fast capture with auto-timestamp |
| `vault_stats` | Vault metrics and health |

### Canvas Operations (6 tools) - NEW

| Tool | Purpose |
|------|---------|
| `list_canvases` | List all .canvas files in vault |
| `read_canvas` | Read and parse canvas JSON |
| `create_canvas` | Create new canvas with nodes/edges |
| `add_canvas_node` | Add node to existing canvas |
| `add_canvas_edge` | Add edge connecting nodes |
| `delete_canvas` | Delete with optional backup |

See [CANVAS_TOOLS.md](./CANVAS_TOOLS.md) for detailed canvas documentation.

## Configuration

Requires `.env` or environment variables:

```env
OBSIDIAN_VAULT_PATH=/path/to/vault
```

## Dependencies

- `fastmcp>=3.1.1+.1,<2.15.0`
- `pydantic>=2.0.0`
- `python-dotenv>=1.0.0`
- `structlog>=23.0.0` (replaced rich for structured logging)
- `pyyaml>=6.0.0`
- `aiofiles>=23.0.0`
- `pytest>=7.0.0` (dev)
- `pytest-asyncio>=0.21.0` (dev)
- `pytest-cov>=4.0.0` (dev)

## Integration Opportunities

### Composite Servers

Could mount in:
- `ai-producer-hub` - For production documentation
- `knowledge-hub` (planned) - ADN + Obsidian bidirectional sync

### ADN Integration

See: [[ADN and Obsidian Bidirectional Sync Strategy]]

Potential workflows:
1. Search Obsidian vault from Claude
2. Sync notes between ADN and Obsidian
3. Use Obsidian as visual graph, ADN as AI-enhanced backend


