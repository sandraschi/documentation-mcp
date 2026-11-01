---
title: "Craft apps: the command bus and the two planes (headless and live)"
category: standard
status: review
audience: mcp-dev, all-agents
last_updated: 2026-10-20
---

# Craft apps: the command bus and the two planes

**Why this doc exists.** Every Craft app is a GUI application that can also be
driven as a headless CLI, a scripted command bus, and a live MCP server attached
to the running window. That is unusual, it is not obvious from the outside, and
it is the reason a Craft app is a better demo target than a screenshot tool.

## The four shapes of app control

| Shape | How it works | Example | Cost |
|---|---|---|---|
| **Headless batch** (typical MCP) | Client spawns a CLI, CLI does the work, returns a file | `photocraft-cli run in.jpg --cmd ... --out out.png` | No GUI, no feedback until done |
| **Scripting bridge** | MCP calls an app's vendor scripting API while the app is open | Reaper OSC, Blender `bpy`, Photoshop ExtendScript | Depends on vendor API coverage and stability |
| **CUA** | MCP drives pixels and keystrokes | pywinauto, Playwright, computer-use | Works anywhere, brittle, no semantic model |
| **Command bus + attach** (Craft) | App exposes a documented command registry over a control port; the CLI/MCP proxies to it | `figcraft-cli mcp --attach 7979` | Semantic, deterministic, visible — requires the app to be running |

Craft is the fourth shape: the app is **designed to be driven by an agent**, not
merely automatable. The command bus is public (`commands`), the parameters are
JSON, and the same command IDs work headless and live.

## The two planes

Every Craft CLI has two ways to execute the same commands:

**Plane 1 — headless.** No app, no window, no control port. The CLI runs an
in-process engine, writes files, exits. This is what `democraft` uses for batch
demos and what CI can use.

**Plane 2 — live.** The GUI is started with a control port, and the MCP server
attaches to it over local TCP. Commands land on the visible canvas; the human
watches them happen. The MCP server still speaks stdio to the client; only the
app leg is a socket.

```
client (Claude/opencode/Antigravity)
   │ stdio (JSON-RPC)
   ▼
<app>-cli.exe mcp --attach|--bridge|--connect PORT
   │ localhost TCP (control channel)
   ▼
<app>.exe --control PORT   ← the window the human sees
```

## The command registry

```powershell
# Machine-readable catalog: id, label, menu, shortcut, params, enabled
figcraft-cli commands --json
designcraft-cli commands --json
photoCraft-cli commands --json
gridcraft-cli commands --json

# Human/engine detail for one command, including its parameter signature
soundcraft-cli describe mix.insert
```

The catalog is the whole API. If a command is not in `commands`, no amount of
clicking will make the MCP server see it; if it is, the CLI and the MCP server
expose it.

## Usage examples (verified 2026-10-20)

**Headless, PhotoCraft** — non-destructive adjustment stack, layered save, then
flatten:

```powershell
photocraft-cli run plate.jpg `
  --cmd layer.newAdjustmentLayer.blackWhite --params '{"reds":45,"yellows":70}' `
  --cmd layer.newAdjustmentLayer.curves    --params '{"points":[[0,10],[128,128],[255,242]]}' `
  --out plate.pcraft
photocraft-cli convert plate.pcraft plate.png
```

Note the PhotoCraft syntax: `--cmd <id> --params <json>`. Most other Craft CLIs
use `--cmd 'id={json}'` instead. See the trap table below.

**Headless, DeckCraft** — three slides, three transitions, real transition
frames:

```powershell
deckcraft-cli run `
  --cmd 'slide.new={"layout":"titleOnly","title":"One"}' `
  --cmd 'transition.set={"kind":"push","duration":900,"index":0}' `
  --save reel.deckcraft --export reel.gif --export-params '{"secondsPerSlide":2}'
deckcraft-cli render-transition reel.deckcraft --slide 1 --t 0,0.5,1 tr1.png
```

**Headless, GridCraft** — data, formula, chart, export:

```powershell
gridcraft-cli run `
  --cmd 'range.setValues={"range":"A1","values":[["Month","Revenue"],["Jan",120],["Feb",145]]}' `
  --cmd 'insert.chart={"range":"A1:B3","type":"column","title":"Revenue","at":"E2"}' `
  --out revenue.xlsx
```

**Headless, SoundCraft** — tempo, MIDI import, bounce (note: bounce range is in
**samples**, not seconds):

```powershell
soundcraft-cli run --demo `
  --cmd 'event.tempo={"bpm":112}' `
  --cmd 'file.import_midi={"path":"melody.mid","at":0}' `
  --bounce melody.wav --start 0 --end 432000
```

**Live, FigCraft** — start the app, attach the MCP server, then let the client
call commands; every call is visible on the canvas:

```powershell
figcraft --control 7979
figcraft-cli mcp --attach 7979
```

If the app is not running, attach exits 1:
`can't reach the FigCraft app at 127.0.0.1:7979 ... (start it with figcraft --control PORT)`.
That is a precondition, not a bug.

**Live, SoundCraft** — method calls against the running app, useful for
scripting without an MCP client:

```powershell
soundcraft --control 11250
soundcraft-cli app --port 11250 engine.commands
soundcraft-cli app --port 11250 engine.execute '{"command":"event.tempo","params":{"bpm":112}}'
soundcraft-cli app --port 11250 session.inspect
```

`engine.execute` is the single dispatch entry; `session.inspect` returns the
session tree (tracks, clips, notes, instruments).

## Control ports: one per app

The control listener is an ordinary TCP socket: two processes cannot bind the
same port. If two Craft apps must run at the same time, each needs its own
`--control` port. The fleet mapping is in
[`operations/WEBAPP_PORTS.md`](../../operations/WEBAPP_PORTS.md): 14100-14112,
one per app, alphabetical.

The examples above used 7979 and 11250 during testing; those were arbitrary.
Use the registered port for anything persistent, so the attach entries and the
apps cannot drift apart.

## Flags differ per app — check before copying

| App | Catalog | Batch syntax | MCP attach flag | GUI control |
|---|---|---|---|---|
| FigCraft | `commands [--json]` | `run <script.json>` | `mcp --attach PORT` | `figcraft --control PORT` |
| PhotoCraft | `commands --json` | `run <file> --cmd id --params json` | `mcp --bridge 127.0.0.1:PORT` | `photocraft --control PORT` |
| DesignCraft | `commands [--json]` | `run --cmd id=json` | `mcp --connect PORT` | `designcraft --control PORT` |
| DeckCraft | `commands` | `run --cmd id=json` | `app` CLI (MCP attach not listed) | `deckcraft --control PORT` |
| GridCraft | `commands --json` | `run --cmd id=json` | `mcp --connect PORT` | `gridcraft --control PORT` |
| SoundCraft | `commands` / `describe` | `run --cmd id=json` | `mcp --connect PORT`; `app --port P METHOD` | `soundcraft --control PORT` |

`--attach`, `--bridge`, and `--connect` are the same idea with three names. The
GUI flag is `--control` everywhere; verify with the app's own help before
automating.

## Client config

The transport is always **stdio**; the app leg is a local socket. The JSON shape
depends on the client:

Claude Desktop / Antigravity (`mcpServers`):

```json
{
  "mcpServers": {
    "figcraft-live": {
      "command": "C:\\Program Files\\FigCraft\\figcraft-cli.exe",
      "args": ["mcp", "--attach", "7979"]
    }
  }
}
```

opencode (`mcp`, `type: "local"`, command array):

```json
{
  "mcp": {
    "figcraft-live": {
      "type": "local",
      "command": ["C:\\Program Files\\FigCraft\\figcraft-cli.exe", "mcp", "--attach", "7979"],
      "enabled": false
    }
  }
}
```

Do not put a live-attach server in an always-start config. Claude launches every
entry at startup and has no per-server toggle; if the app is not up, the entry
fails. opencode can keep it `"enabled": false` and start it when the GUI is
running. A headless entry (`["mcp"]`) has no such precondition.

## Traps

- **`--control` is opt-in.** Launching `figcraft.exe` with no arguments opens the
  window and listens on no port. The control server exists only with the flag.
- **Attach fails fast.** No app on the port means exit 1, not a retry loop.
- **Batch parameter syntax is not uniform.** PhotoCraft takes
  `--cmd id --params json`; Design/Deck/Grid/Sound take `--cmd 'id={json}'`.
- **Ranges differ.** SoundCraft CLI `--start/--end` are seconds; the control
  channel's `file.bounce_mix` takes sample positions.
- **Catalog support varies.** `commands --json` works on most, not all; `describe`
  is the fallback for parameter signatures.
- **Live and headless can disagree.** A plugin that renders in Reaper can be
  silent in a host's offline path (see BUG-082); test both planes when audio or
  plugins are involved.
