# Little Game Guide (godot-mcp)

**Canonical copy (edit there first):** `D:/Dev/repos/godot-mcp/docs/little-game-guide.md`

Fleet summary for AI-assisted **small** Godot games — study repos, sample mapping, Windows/iOS distribution. Not an indie-dev career path.

---

## Study five repos (aligned with `just demo-run`)

| # | Repository | godot-mcp sample |
|---|------------|------------------|
| 1 | [godotengine/godot-demo-projects](https://github.com/godotengine/godot-demo-projects) | `just demo-run platformer` · `dodge` · `pong` |
| 2 | [uheartbeast/Heart-Platformer-Godot-4](https://github.com/uheartbeast/Heart-Platformer-Godot-4) | `just demo-run heart` |
| 3 | [gdquest-demos/godot-4-procedural-generation](https://github.com/gdquest-demos/godot-4-procedural-generation) | `just demo-run procedural` |
| 4 | [miskatonicstudio/intrepid](https://github.com/miskatonicstudio/intrepid) | Full shipped-game source (Godot 3.x reference) |
| 5 | [KipJM/ACEDIA](https://github.com/KipJM/ACEDIA) | Full Godot 4.4 project (open code + CC assets) |

**Bonus (iPad FOSS):** [adchamberlain/into-the-wild](https://github.com/adchamberlain/into-the-wild)

Samples live under `godot-mcp/samples/` — see repo `samples/README.md`.

---

## AI + godot-mcp loop

```
Idea → MCP tools or AI file edits → F5 in Godot → export → ship
```

- **MCP:** bulk scenes, STL/particles, `godot_export_web`, `ship_to_itch`, `godot_read_scene_tree`  
- **Dashboard:** **`/ship`** — export, Butler preview, push (no secrets in UI)  
- **Editor:** feel, animation, UI layout  
- **Start:** `just serve` · `just godot-bridge` · `just bridge-test` (bridge optional for ship tools)

godot-mcp **Tauri** (`native/`) wraps the MCP dashboard, **not** your game binary — export the game from your own Godot project.

---

## Distribution (Windows & iOS)

| Platform | Easiest path | Notes |
|----------|--------------|-------|
| **Everywhere** | Web/HTML5 export + itch.io | No store account; works on iOS Safari |
| **Windows** | Godot → Windows Desktop → zip or itch.io | `just little-game-export windows dodge` |
| **iOS (App Store / TestFlight)** | Mac + **Xcode 26.3** + Apple Developer ($99/yr) | Agentic IDE — see [AGENTIC_XCODE_26.md](../../apple/development/AGENTIC_XCODE_26.md) |
| **iOS (VRM dance app)** | Swift native — **not Godot** | [VRM_DANCE_APP.md](../../apple/ios/VRM_DANCE_APP.md) |
| **iOS (casual)** | Web export, “Add to Home Screen” | Good enough for a toy game |

### Export recipes (godot-mcp)

```powershell
just install-export-templates
just little-game-export web dodge
just little-game-pack web dodge       # zip → manual itch upload
just little-game-export windows dodge
just little-game-pack windows dodge
```

### Butler ship (automated)

Set `BUTLER_API_KEY` + `ITCH_TARGET=user/game`, then:

```powershell
just ship web dodge
# or dashboard: just web → /ship
```

MCP: `ship_to_itch(target="web", game="dodge")` · Workflow: `ship_web_itch`

Canonical ship doc: **`godot-mcp/docs/ship-to-itch.md`**

### Store guides (MCD)

- **[itch.io platform](../../docs/gamedev/ITCH_IO_PLATFORM.md)** — web, app, Butler CLI, API  
- **[itch.io — games](../../docs/gamedev/ITCH_IO_GUIDE.md)** — free hosting, HTML + zip uploads  
- **[itch.io — tools & assets](../../docs/gamedev/ITCH_IO_TOOLS_ASSETS.md)** — addons, packs, MCP zips  
- **[Steam publishing](../../docs/gamedev/STEAM_PUBLISHING.md)** — $100 Direct fee, Steamworks pipeline  

**90-minute first ship:** fork Dodge the Creeps → tweak with AI → `just ship web dodge` (or pack + manual upload).

---

## Commercial context (closed source)

Notable Steam Godot titles: **Slay the Spire 2**, **Buckshot Roulette**, **Brotato**, **Cassette Beasts**, **Halls of Torment**. Showcase: [godotengine.org/showcase](https://godotengine.org/showcase/).

Full guide (study notes, export commands, caveats): **`godot-mcp/docs/little-game-guide.md`**

**AI vs indie:** [AI_AND_INDIE_GAMES.md](./AI_AND_INDIE_GAMES.md) — hobby toys vs commercial craft
