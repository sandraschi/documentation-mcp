# AutoHotkey v2 Fleet Reference

## Contents

| Document | Description |
|----------|-------------|
| [History](history.md) | AHK v1→v2 timeline, migration stats, architectural changes |
| [Syntax (v1 vs v2)](syntax.md) | Side-by-side comparison, prohibited patterns, examples |
| [Libraries](libraries.md) | Built-in, bundled, third-party (thqby/ahk2_lib), CLI, MCP, fleet tools |
| [XCGUI](xcgui.md) | DirectX GUI framework — controls, events, styling, vs native Gui() |
| [MCP from AHK](mcp-from-ahk.md) | Call fleet MCP servers, AHK as MCP server, examples |
| [Linter](linter.md) | Fleet's custom AHK v2 linter — usage, fix mode, false positive suppression |
| [Resources & Bibliography](resources.md) | Official docs, community, learning, publications, computer science foundations |
| [Fleet Standard](../standards/rules/autohotkey_v2_standard.md) | Global fleet AHK v2 conventions (SOTA 2026) |

## Fleet Status

| Repo | Role | Health |
|------|------|--------|
| [autohotkey-test](https://github.com/sandraschi/autohotkey-test) | Scriptlet depot — 80+ v2 scripts, HTTP bridge | ✅ Active |
| [autohotkey-mcp](https://github.com/sandraschi/autohotkey-mcp) | FastMCP server — list/run/stop scriptlets, generate AI scripts | ✅ Active |

## Key Files

| File | Purpose |
|------|---------|
| `scriptlets/` | 80+ AHK v2 scripts by category |
| `scriptlets/lib/` | Shared libraries: ScriptletErrorHandler, GdipHelper, JSON, Socket, etc. |
| `ScriptletCOMBridge.ahk` | HTTP bridge on port 10744 — /run, /stop, /scriptlets, /dashboard |
| `utils/linter_headless.ahk` | Custom v2 linter with 33+ checks |
| `justfile` | `lint-ahk`, `lint-fix`, `kill-ahk`, `dash`, `start` |
