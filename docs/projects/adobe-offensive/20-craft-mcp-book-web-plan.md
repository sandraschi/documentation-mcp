# 20 - Craft MCP x Books x Web Plan: DesignCraft for book repos, FigCraft for sandras.com

Date: 2026-10-15. Status: plan, not started.
Sources: `D:\Dev\repos\_upstream\designcraft\docs\mcp.md`, `...\figcraft\docs\mcp.md`, installed `C:\Program Files\DesignCraft\`, `C:\Program Files\FigCraft\`, `bookkit/README.md`, `sandras-com/PLAN.md`.

## 0. What is installed (verified 2026-10-15)

`C:\Program Files\` holds: CAD, Deck, Design, Effect, Fig, Film, Grid, Light, Pdf, Photo, Sound, Vector, WordCraft.

- DesignCraft: `designcraft.exe` + `designcraft-cli.exe`
- FigCraft: `figcraft.exe` + `figcraft-cli.exe`
- No build needed. Release MSIs ship the CLI alongside the app.

Upstream (read-only, never edit):
- `D:\Dev\repos\_upstream\designcraft` - InDesign-class, Rust, engine-first, `designcraft-cli run|script|commands|describe`, MCP `designcraft-cli mcp` (headless) / `mcp --connect 7979` (attached), control `designcraft --control 7979`
- `D:\Dev\repos\_upstream\figcraft` - Figma-class, 400+ commands, `figcraft-cli render|export|run|commands|mcp`, MCP `figcraft-cli mcp` / `mcp --attach 47800`, control `figcraft --control <port>`

Pattern both share: everything is a command. UI / CLI / control channel / MCP dispatch the same ids. Programmatic calls never open dialogs.

## 1. MCP registration

```json
{
  "mcpServers": {
    "designcraft": { "command": "C:\\Program Files\\DesignCraft\\designcraft-cli.exe", "args": ["mcp"] },
    "designcraft-app": { "command": "C:\\Program Files\\DesignCraft\\designcraft-cli.exe", "args": ["mcp", "--connect", "7979"] },
    "figcraft": { "command": "C:\\Program Files\\FigCraft\\figcraft-cli.exe", "args": ["mcp"] },
    "figcraft-app": { "command": "C:\\Program Files\\FigCraft\\figcraft-cli.exe", "args": ["mcp", "--attach", "47800"] }
  }
}
```

Attached mode:
```powershell
& "C:\Program Files\DesignCraft\designcraft.exe" --sample --control 7979
& "C:\Program Files\FigCraft\figcraft.exe" --control 47800
```
Ports 7979 / 47800 avoid fleet forbidden 3000/5000/5173/8000/8080. sandras-com stays 11980/11981.

## 2. Track A - book repos x DesignCraft (pilot: on-metacraft)

bookkit stays source of truth: `build`, `lore --strict`, `claims`, `epub`, `pdf`, `cover`, `validate`, `publish` (KDP package, no upload - no API). DesignCraft is the pro layout pass: threaded stories, Knuth-Plass composer, IDML in/out, PDF/X-4 + PDF/A-2b + EPUB out.

Pilot:
1. `py -3 ../bookkit/bk.py lore --strict` + `build` in `D:\Dev\repos\on-metacraft` - clean baseline.
2. Headless smoke: `designcraft-cli run --sample --all-pages out/`, `commands footnote`, `describe xref.insert`.
3. MCP on a copy: `new_document {preset:A4, margins:36}`, `execute {frame.create}`, `set_story_text` / `get_story` (UTF-8 byte offsets), `place_image`, `render_page {page:0}` visual check, `save_document` -> `.designcraft`.
4. Repeatable script `page.dcs` (one `command.id {json}` per line, `$N.path` refs work in CLI `script`, `run --cmd`, MCP `batch`).
5. Export `--export book.pdf --export book.epub`, then `bk.py validate`.
6. Roll to on-ai-takeover / on-hyperwar / on-hyperart after pilot. Never edit `_upstream/designcraft`.

Key tools: `list_commands`, `execute`, `batch`, `inspect_document`, `get_story`, `set_story_text`, `new_document`, `open/save_document`, `place_image`, `render_page`, `export_png`.

## 3. Track B - webpage x FigCraft (sandras-com)

Astro site per `sandras-com/PLAN.md` Phases 0-7. FigCraft = mockup + handoff, not builder.

1. Start from template, not blank: `run_command {file.newFromTemplate, template:landing-page}` (also mobile-app, dashboard, design-system, wireframe-kit, social-posts, slides, icon-set). `template.list` to enumerate.
2. Hero + layout with auto-layout (layout:vertical, gap, padding, sizingH/V hug/fill/fixed), components/variants + Light/Dark variable modes. Coords page units y-down, x/y relative to parent. Colors `#RRGGBB`.
3. Verify each arc: `inspect_document` / `get_node` for numbers, `screenshot` / `export {format:png, scale:2}` for pixels.
4. Handoff: `run_command {inspect.code}` (CSS/HTML/React, components as props), `inspect.properties`, `inspect.assets` -> `sandras-com/src/pages/` + `src/styles/`, `just ci` green.
5. First task: landing-page template re-skinned to sandras.com top bar (Writing/Fleet/Install/Standards/Now/About) + footer (RSS, Impressum, Mastodon, GitHub), export 2x, inspect.code hero.

This chat's figcraft session is headless Untitled - good for throwaway. Installed app/file for real work.

## 4. Order of record

1. mcd (this file) - canonical.
2. figcraft `.figcraft` board - visual plan (Track A/B swimlanes).
3. designcraft `.designcraft` doc - print-layout version of same plan.

Next: build 2 + 3, attach PNG renders here.
