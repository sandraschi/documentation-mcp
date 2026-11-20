# Craft Showcase

**Version**: v0.2.0 (2026-11-15) — Dual web showcase for the **Sovereign Back-Office Suite** (12 apps + in-browser `egui` WASM studio + ROI calculator) and the **DIY Craft Fleet** (33 local-first ArtCraft apps, dynamically synced from the local fleet).

## Ports & Public Tailscale Funnel

| Endpoint | Target | Scope |
|---|---|---|
| `http://localhost:11270/` | Back-Office Suite Showcase (`web/index.html`) | Local |
| `http://localhost:11270/diy.html` | DIY Craft Fleet Showcase (`web/diy.html`) | Local |
| `http://localhost:11270/wasm/` | In-Browser `egui` WASM Studio (`web/wasm/`) | Local |
| `http://localhost:11270/data/diy-apps.json` | Synced DIY catalog JSON | Local |
| `https://goliath.<tailnet>.ts.net:8443/` | Public Tailscale Funnel → `127.0.0.1:11270` | Public Internet |
| `https://goliath.<tailnet>.ts.net:8443/diy.html` | DIY Craft Fleet Showcase (Public) | Public Internet |
| `https://goliath.<tailnet>.ts.net:8443/wasm/` | In-Browser WASM Studio (Public) | Public Internet |

## Architecture

```
D:\Dev\repos\*craft* (local fleet)
          │
          ▼  .\start.ps1 -Sync  (scripts/sync-diy-catalog.ps1)
web/data/diy-apps.json  ──(fetch)──▶  web/diy.html (DIY Craft Fleet, 33 apps)
                                            ▲
                                            │ header switcher
web/index.html (Back-Office Suite, 12 apps) ┴─▶ embeds web/wasm/ (egui 0.37 -> wasm32)
```

- **Separate Showcases by Audience**:
  - `web/index.html` stays focused on the B2B **Sovereign Back-Office Suite** (HelmCraft, BillCraft, SpendCraft, HireCraft, TaskCraft, DeskCraft, ContractCraft, GainCraft, TeamCraft, AssetCraft, FormCraft, WikiCraft), Austrian statutory compliance, ROI calculator, and WASM studio.
  - `web/diy.html` showcases all other **DIY Craft Apps** across 5 categories (`AI & Agents`, `Creative & Media`, `Writing & Knowledge`, `Hardware, CAD & GIS`, `Data & Fleet Infra`) with category filters and live search.
- **GitHub Links**: Every card on both `index.html` and `diy.html` includes a `GitHub ↗` link (resolved from `git remote get-url origin` during sync, with `https://github.com/sandraschi/<repo>` fallback).

## Quick Start & Maintenance

```powershell
# Rescan D:\Dev\repos\*craft* and regenerate web/data/diy-apps.json
D:\Dev\repos\craft-showcase\start.ps1 -Sync

# Smoke check (verifies web/index.html, web/diy.html, web/data/diy-apps.json, web/wasm/index.html)
D:\Dev\repos\craft-showcase\start.ps1 -Smoke

# Rebuild WASM studio from crates/craft-showcase-wasm
D:\Dev\repos\craft-showcase\start.ps1 -Build

# Serve locally on port 11270
mcp-central-docs\starts\craft-showcase-start.bat
```

### Tailscale Funnel Control

```powershell
# Enable public internet access on port 8443
tailscale funnel --bg --https=8443 11270

# Check active Funnel routes
tailscale funnel status

# Disable public access
tailscale funnel --https=8443 off
```

> **Note**: Funnel proxies live to `127.0.0.1:11270`, so `goliath` and the `11270` server must remain running for the public URLs to stay reachable.

## Links

- **Repository**: [craft-showcase](file:///D:/Dev/repos/craft-showcase) (`https://github.com/sandraschi/craft-showcase`)
- **Spoke Assessment**: [craft-showcase.md](../craft-fleet/craft-showcase.md)
