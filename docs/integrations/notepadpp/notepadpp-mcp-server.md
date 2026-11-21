# Notepad++ MCP Server: The Agentic Control Layer

The Notepad++ MCP server (`notepadpp-mcp`, v0.3.0) gives agents a bridge to Notepad++ on Windows:
open/edit/save files, manage tabs and sessions, lint files, fix display issues and manage plugins.

## Server registration

```json
{
  "notepadpp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/notepadpp-mcp", "run", "notepadpp-mcp"],
    "env": {
      "NOTEPADPP_PATH": "C:/Program Files/Notepad++/notepad++.exe",
      "NOTEPADPP_MCP_ALLOWED_DIRS": "C:/Users/<user>/Documents;D:/Dev/repos"
    }
  }
}
```

`NOTEPADPP_MCP_ALLOWED_DIRS` is a security boundary: every file path the tools receive must resolve
inside one of these folders (default `~/Documents`). Added in 0.2.2 after a coordinated-disclosure
report of arbitrary file read/write via `file_ops` (fixed in commit `410bd77`).

## Tool catalog (portmanteau)

| Tool | Operations |
| :--- | :--- |
| `file_ops` | open, new, save, save_as, info, is_dirty, reload_from_disk, find_in_files, diff_buffer |
| `text_ops` | insert, find, write, replace_all, goto_line, copy_selection, comment_uncomment, case, trim, line_ops, count |
| `tab_ops` | list, switch, close |
| `session_ops` | save, load, list |
| `linting_ops` | auto, python, javascript, typescript, json, markdown, yaml, toml, ahk, tools |
| `display_ops` | fix_invisible_text, fix_display_issue, theme_status, set_dark_mode, set_editor_theme |
| `plugin_ops` | discover, install, list, execute |
| `status_ops` | help, system_status, health_check |

### Linting engines

ruff (Python), Biome (JS/TS), markdownlint-cli2 (Markdown), yamllint (YAML), strict parsers for
JSON/TOML, ahk-lint + structural checks (AutoHotkey); built-in fallbacks when an engine is missing.
ESLint is deliberately not used (its JS config executes from the linted folder). The same engine set
is available fleet-wide via DevCraft (`devcraft_lint`).

## Interaction principles

- **Focus non-disturbance**: avoid switching tabs unless requested.
- **Safety**: `save` makes a timestamped backup; `save_as` refuses to overwrite without `overwrite=true`;
  `reload_from_disk` refuses to discard unsaved changes without `force=true`.
- Lint saved files, convert issues into targeted `text_ops` edits, then re-lint.

---
*Last updated: 2026-11-19*
