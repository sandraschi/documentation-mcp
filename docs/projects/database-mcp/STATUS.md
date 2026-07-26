# Database Operations MCP - Status

**Last Updated:** 2025-11-29
**Version:** 1.4.0
**FastMCP:** 3.1.1+.1

---

## Overview

FastMCP 3.1.1+ MCP server for database-centric operations on Windows, with powerful bookmark tooling as a secondary feature.

## Tool Count

| Category | Tools |
|----------|-------|
| Database | 7 portmanteau tools |
| Browser Bookmarks | 8 portmanteau tools |
| Media/Support | 4 portmanteau tools |
| **Total** | **21 tools** (Cursor UI) |

## Key Tools

### Database Tools (Primary)
- `db_connection` - Connection management (13 operations)
- `db_operations` - Query execution, transactions, batch ops (6 operations)
- `db_schema` - Schema inspection (4 operations)
- `db_management` - Health checks, optimization
- `db_fts` - Full-text search with ranking
- `db_analysis` - Comprehensive database analysis
- `windows_system` - Windows Registry and system management

### Bookmark Tools (Secondary)
- `browser_bookmarks` - Universal browser portmanteau (Chrome/Edge/Brave/Firefox)
- `firefox_bookmarks` - Firefox-specific operations (20+ operations)
  - Core: list, add, search, find_duplicates
  - Age: find_old_bookmarks (by creation), find_forgotten_bookmarks (by visit)
  - Maintenance: refresh_bookmarks (404 check + URL fix)
  - Tags: list, find_similar, merge, clean_up
- `firefox_profiles` - Profile management
- `firefox_backup` - Backup/restore
- `firefox_tagging` - Automated tagging
- `firefox_utils` - Utility operations
- `chrome_profiles` - Chrome profile management
- `sync_bookmarks` - Cross-browser sync

### Media & Support
- `media_library` - Calibre & Plex library management
- `help_system` - Interactive help and documentation
- `system_init` - System initialization
- `db_operations_extended` - Extended database operations

## Recent Changes (2025-11-29)

### Firefox Bookmark Age Operations
- **Fixed:** `find_old_bookmarks` now uses creation date (`dateAdded`), not visit date
- **Added:** `find_forgotten_bookmarks` - bookmarks not visited in N days (archive candidates)
- **Added:** `refresh_bookmarks` - check for 404s, attempt URL simplification
- **Improved:** Explicit error messages when Firefox is running during write operations

### Firefox Lock Handling
- Write operations fail with clear error if Firefox is running
- Read operations work via `force_access=True` while Firefox is open
- Error includes: `hint_for_mcp_client: "Tell the user to close Firefox"`

## CI/CD Status
- âœ… GitHub Actions workflows
- âœ… Ruff linting
- âœ… pytest test suite

## Repository
- **Location:** `D:\Dev\repos\database-operations-mcp`
- **GitHub:** database-operations-mcp

---

## Related Notes
- [[Database MCP - Firefox Bookmark Age Operations]]


