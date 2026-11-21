---
title: "Which MCP repos become a craft app"
status: scheduled
last_updated: 2026-11-13
starts: 2026-11-14
---

# Craft apps from the MCP fleet

Written 13 November 2026. The work starts 14 November 2026. This note is the queue. It does not start the apps.

A craft app owns a local document: a file, a command line, an MCP server, and a window. A repo that only drives someone else's program stays an MCP server.

Storytold already ships WordCraft, GridCraft, DeckCraft, MailCraft, DesignCraft, FigCraft, VectorCraft, PhotoCraft, FilmCraft, LightCraft, EffectCraft, SoundCraft, PdfCraft, CADCraft, SolidCraft, TextureCraft, and MaterialCraft. Those names stay theirs.

## Tomorrow

### 1. HealthCraft, one new app, from `health-mcp`

A local health log: weight, sleep, blood pressure, meals, steps, an Apple Health import, and pet notes. One SQLite file. SportsCraft is the gym plan and the match table. HomeCraft is the house. The camera watchers in `health-mcp` stay with HomeCraft.

First cut: the log, the import, and a window that shows the series. No diagnosis. No cloud account.

### 2. One reader for `digibib5-mcp` and `directmedia-mcp`

Both repos read the same Digitale Bibliothek discs (the `.DKI` volumes). One app, one shelf of volumes, the text and the table of contents. BookCraft remains the Calibre shelf. PhotoCraft remains photographs. Name the reader when the repo is created. Do not make two apps.

### 3. Fold the bench into MakerCraft

Started 13 November 2026. `instrument.capture` writes one labelled demo file per source. The Machines tab lists the seven. Live scope, logic, and Bus Pirate probes were already commands. The meter, generator, spectrum analyzer, and JTAG adapter are files only. The Python servers are still on disk. Handover: `D:\Dev\repos\makercraft\HANDOVER.md`.

MakerCraft is already the fabrication bench and already talks to a Bus Pirate. These repos become sources in that app, each behind the command bus, with the capture saved as a file:

- `oscilloscope-mcp`
- `logic-analyzer-mcp`
- `multimeter-mcp`
- `function-generator-mcp`
- `spectrum-analyzer-mcp`
- `jtag-swd-mcp`
- `bus-pirate-mcp`

No separate bench app.

## These stay MCP servers

| Owner | Repos |
|---|---|
| HomeCraft | home-assistant, devices, tapo, nuki, nest, netatmo, ring |
| BookCraft | calibre, rust-calibre |
| RobotCraft | robotics, ros, unitree, yahboom, mujoco, gazebo, isaac |
| TravelCraft | publictransport, gtfs, mywienerlinien |
| VMCraft, SpeechCraft, WinCraft, DatabaseCraft | virtualization, speech, windows-operations, sysinternals, database-operations |
| MailCraft, LookCraft, DeskCraft | email, ms-graph, teams |
| BillCraft, PdfCraft, WikiCraft | stripe, pdf, obsidian, notion, onenote, quicknotes, advanced-memory |
| GameCraft and the Storytold art apps | godot, unity, blender, gimp, inkscape, kicad, freecad, obs, reaper, davinci |

Docker, Kubernetes, git, fastsearch, monitoring, arXiv, NotebookLM, Hugging Face, and Tailscale stay admin and bridge servers. `sdr-mcp` stays a GNU Radio bridge. SoundCraft is the audio editor.

## Already waiting, and not this queue

ShopCraft is the shop, the plan, and the buyer message. It is an idea in `CUSTOMER_FACING_CRAFT.md`. The thin back-office queue is `BACKOFFICE_THIN_RUNT_PLAN.md`. Neither one moves because this list exists.
