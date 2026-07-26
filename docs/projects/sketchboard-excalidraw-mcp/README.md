# sketchboard-excalidraw-mcp

Excalidraw canvas authorship + headless-render MCP server. Slots next to
[inkscape-mcp](https://github.com/sandraschi/inkscape-mcp) and
[gimp-mcp](https://github.com/sandraschi/gimp-mcp) as the vector/raster/diagram
trio in the fleet.

**Status: day 2.** Server shell, package layout, and fleet standardization
are in place. Headless rendering (`render_svg`/`render_png`) is real and
tested. Canvas bridging, Mermaid conversion, and batch rendering are
registered as MCP tools but return `not_implemented` - see `docs/DESIGN.md`
for what's real vs planned.

## What this is

A merge of two upstream approaches into one fleet-standard server:

- **Canvas workbench** (planned base: fork of
  [lesleslie/excalidraw-mcp](https://github.com/lesleslie/excalidraw-mcp),
  itself built on [yctimlin/mcp_excalidraw](https://github.com/yctimlin/mcp_excalidraw)):
  Python FastMCP server + TypeScript canvas server + React frontend for live,
  interactive diagram authorship. **Not merged in yet** - both upstreams are
  cloned for reference/cherry-picking under `D:\Dev\repos\external\`, but no
  canvas-bridge code has been ported into this repo. See the fork-drift open
  question in `docs/DESIGN.md` before that lands.
- **Headless rendering** (real, implemented): ported from
  [bassimeledath/excalidraw-render-mcp](https://github.com/bassimeledath/excalidraw-render-mcp)'s
  TypeScript/agent-browser renderer into Python/Playwright, rather than
  vendoring a second Node stack. A warm Chromium instance renders Excalidraw
  element JSON to SVG/PNG via `exportToSvg`, reused across calls in the same
  process. **Known gap:** still loads `@excalidraw/excalidraw` from esm.sh at
  runtime rather than a locally vendored bundle, so it needs network access
  on first render and isn't version-pinned yet.

The two modes are deliberately decoupled: headless render tools work without
the canvas server running (agent batch mode), while the canvas/Tauri app is
for interactive human use. Both talk to the same backend; the desktop app is
not a sidecar wrapping the Python server.

## Fork sources on this machine

Both upstream forks were cloned for reference/cherry-picking, not vendored
wholesale:

- `D:\Dev\repos\external\excalidraw-mcp-lesleslie\`
- `D:\Dev\repos\external\excalidraw-render-bassimeledath\`

## Planned extras

- Mermaid-to-Excalidraw conversion, wrapping the official
  `@excalidraw/mermaid-to-excalidraw` npm package rather than reimplementing
  Mermaid parsing.
- `.excalidrawlib` support for reusable fleet-diagram components (server
  boxes, transport arrows).
- Batch-render command for the repo-README diagram pipeline across the
  fleet (~200 repos).

## Ports

| Port | Service |
|------|---------|
| 11107 | Backend (FastMCP HTTP `/mcp` + REST) |
| 11108 | Frontend (Vite React canvas) |

Registered in `mcp-central-docs/operations/WEBAPP_PORTS.md`.

## License and attribution

MIT, same as both upstream sources. Credit chain: this project builds on
lesleslie/excalidraw-mcp (which credits yctimlin/mcp_excalidraw) and borrows
the headless-render architecture from bassimeledath/excalidraw-render-mcp.
Font licensing (Excalidraw's default hand-drawn fonts ship under SIL OFL, not
MIT) is tracked separately in `NOTICE.md` once the JS bundle is vendored.

## Development

```powershell
uv sync
uv run pytest
just release-dry
```

See `docs/DESIGN.md` for the day 1/2/3 build plan and the concrete technical
decisions behind this scaffold.
