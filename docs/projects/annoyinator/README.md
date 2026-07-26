# Annoyinator: Doofenshmirtz PowerShell Script Toolkit

> **Salvaged July 2026** from the May 2025 vibecoding era. See [SALVAGE.md](SALVAGE.md) for details.

## About

Annoyinator is a collection of PowerShell utility and prank scripts ("-inators")
with a WPF Doofenshmirtz Control Panel. Originally also had Flask Python apps
("barnacles"), but those were culled during the July 2026 salvage.

## Quick Start

```powershell
just dashboard
```

Or double-click `start-dashboard.ps1` / `start.bat`.

## Most Useful Scripts

- **Temp-File-Annihilator.ps1** -- Obliterates temp files for a cleaner system
- **Taskbar-AutoHide-Fixinator.ps1** -- Fixes stubborn Windows taskbar auto-hide
- **Network-Adapter-Resetinator.ps1** -- Resets network adapters in one click
- **Desktop-Organize-Inator.ps1** -- Tidy desktop icons into grids
- **Font-Cache-Rebuildinator.ps1** & **IconCache-Rebuildinator.ps1** -- Fix font/icon glitches
- **System-Tray-Declutterinator.ps1** -- Clean up system tray
- **Window-Position-Restorizer.ps1** -- Restore windows to saved positions
- **Notification-Silencinator.ps1** -- Silence notification spam

## Most Annoying Scripts

- **Fart-Annoyinator.ps1** -- Randomly plays fart noises
- **Noise-Annoyinator.ps1** -- Random system beeps and sounds
- **Speech-Annoyinator.ps1 / 2** -- Makes your PC say things
- **Extreme-Annoyance-Inator.ps1** -- Maximum annoyance
- **Bluescreen-Simulationator.ps1** -- Fakes a Windows crash
- **Desktop-Critters-Inator-Improved.ps1** -- Animated critters crawl across your screen

*All scripts are reversible. Use responsibly -- and with a sense of humor!*

## Tools

- **Doofenshmirtz Control Panel** (WPF GUI) -- `scripts/script_launcher.ps1`
- **Animations**: desktop critters (bunnies, spiders, flies, kittens, cockroaches)
- **Sound effects**: 23 MP3 files in `tools/Sounds/`
- **Bitmap sprites**: PowerShell-drawn sprites in `tools/BitmapSprites/`

## Fleet Tooling

| Command | What it does |
|---------|-------------|
| `just dashboard` | Launch WPF Doofenshmirtz Control Panel |

## Structure

```
scripts/            -- 26 PowerShell scripts (pranks + utilities)
  pranks_scripts/   -- 10 prank subdirectories
  useful_scripts/   -- 13 utility subdirectories
  script_launcher.ps1 -- WPF Doofenshmirtz Control Panel
Modules/            -- PowerShell drawing/animation modules
  CritterAnimation.psm1, AnnoyingCritters.psm1, ...
  BunnyDrawing.ps1, SpiderDrawing.ps1, ...
tools/
  Sounds/           -- 23 MP3 sound effects
  BitmapSprites/    -- PowerShell sprite drawing scripts
  killallservers.bat, killserverson3000.bat
docs/               -- Legacy documentation
rules/              -- Windsurf/Cascade agentic rulebooks
script_shortcuts/   -- Windows .lnk shortcuts
```
