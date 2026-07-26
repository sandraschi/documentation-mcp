# Changelog

## 0.3.0 (2026-07-15)

### New tools (8)
- `zed_open_tabs()` — list open editor tabs from SQLite DB (path, language, active state)
- `zed_workspace()` — portmanteau: status, diagnostics, bookmarks
- `zed_search_project()` — project-wide file content search via ripgrep
- `zed_list_keybindings()` / `zed_set_keybinding()` — keymap.json read/write
- `zed_snippets()` — portmanteau: list, get, create, delete user snippets
- `zed_git_blame()` — per-line git blame annotations (author, date, summary)
- `zed_tasks()` — portmanteau: list and run .zed/tasks.json build tasks
- 21 total tools

## 0.2.0 (2026-07-15)

- Fleet-standard documentation: README, CHANGELOG, llms.txt, llms-full.txt, glama.json
- Session context injection: .cursorrules, CLAUDE.md, AGENTS.md, .opencode/skills/
- Config files: justfile, .gitignore, .env.example
- Fixed error handling: _error_response() auto-logging (Pattern 3), logged write failures (Pattern 1)
- Conversational `message` key on all tool returns
- Docstring SOTA: Annotated + Field(description=...) for all parameters
- ruff lint + format clean

## 0.1.0 (2026-07-15)

- Initial scaffold: 12 tools for Zed settings, themes, extensions, projects, and agents
- Dual-transport support TBD (stdio-only for initial release)
