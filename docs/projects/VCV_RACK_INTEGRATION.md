# VCV Rack Integration — Project Page

**Repo:** `D:\Dev\repos\vcv-rack-mcp` · [github.com/sandraschi/vcv-rack-mcp](https://github.com/sandraschi/vcv-rack-mcp)
**Status:** Scaffolded 2026-07-12 (PRD + gated TODO ready for agentic build; zero implementation)
**Fleet context:** `architecture/FLEET_GAP_ANALYSIS_2026-07.md` §12.2 · Stream: artistic
**Tags:** [vcv-rack-mcp, modular-synth, artistic-stream, scaffolded, medium]

---

## What it is

MCP server for VCV Rack 2 built on one insight: **`.vcv` patch files are plain JSON** (modules, params, cables — fully declarative). The server authors synth patches by emitting structured data — never GUI automation. Live control delegates to osc-mcp's existing `vcv_manager`; every generated patch embeds an OSC receiver wired to its headline parameters, so it is born performable. Module catalog: 44–50 curated modules, **fifty-fifty** generative-ambient / DJ-performance personas.

## The VCV ecosystem, demystified

| Piece | What it is | Cost | Our stance |
|---|---|---|---|
| **Rack 2 Free** | The full standalone modular synth. Complete for everything this project builds. | Free | Installed on Goliath: `C:\Program Files\VCV\Rack2Free\Rack.exe` |
| **Rack 2 Pro** | Same synth + VST plugin for hosting Rack inside a DAW (Reaper etc.). That is the ONLY delta. | $149 one-time | Not needed; see render ladder below |
| **VCV Library** | The single official marketplace (library.vcvrack.com). Hosts BOTH free/community plugins (subscribe with free account → Rack downloads on restart) AND commercial plugins (one-time purchase, same flow). | Free account; paid modules optional | Catalog v1 policy: **free Library modules only** — zero cost, zero licensing questions |
| **GitHub sideloading** | Open-source plugins publish `.vcvplugin` builds on their releases; drop into the Rack plugins folder (must match Rack 2.x). The only meaningful channel outside the Library. | Free | Supported as an optional, warned install path in the webapp |
| **Cardinal** | FOSS self-contained plugin wrapper around Rack code. Free DAW hosting — but loads NO external modules, has NO Library connection, replaces Core modules with its own. | Free | Render-ladder rung 2 only; would constrain catalog to Rack∩Cardinal intersection |
| **VCV Recorder** | Free official module that records Rack's output to WAV/video inside standalone Rack. | Free | Render-ladder rung 1: embed in generated patches |

**Key limitation:** the Library has **no programmatic install API** — subscribe on the website, Rack downloads on restart. No headless install of Library modules is possible; the tooling must link, diff, and report rather than pretend to install.

## Render decision ladder (settled 2026-07-12)

1. **VCV Recorder module** embedded in generated patches — free, Free-edition compatible, full Library catalog. Render = open patch, play, collect WAV.
2. **Cardinal** — only if Rack-inside-Reaper becomes a proven want; pay the catalog-intersection tax knowingly.
3. **Rack Pro ($149)** — only if Reaper hosting must keep full Library access. Buy on proven absence, not anticipation.

## Webapp: module depot & download facility

The web_sota frontend includes a **Modules** section with three honesty tiers:

- **Report:** catalog vs installed diff (`vcv_catalog.verify_installed`), wishlist of desirable-but-missing modules
- **Link:** deep-links to each module's VCV Library page for one-click subscribe (install completes inside Rack on restart — the UI says so)
- **Do:** optional sideload of GitHub-released `.vcvplugin` files into the plugins dir (version-check against installed Rack, explicit user confirmation, provenance recorded) — completed by **`rack_cycle`** restart choreography: Rack loads plugins only at startup (no runtime loading exists), so "install into running Rack" = confirm → graceful close (autosave preserves session) → stage plugin → relaunch → verify. Process automation, zero GUI automation — by design (the suno-mcp selector-rot lesson)

Plus the patch **Depot** pages: browse/filter by persona, patch detail (JSON, sidecar, OSC address map, validate, open-in-Rack), catalog browser, jobs.

## Documents

- Repo `PRD.md` — contract: tool specs, patch conventions, risks, ship gate
- Repo `TODO.md` — six gated phases (~4 days agentic work); manual gates at P2/P3 need Sandra + audible Rack
- Repo `docs/ONBOARDING.md` — fresh-machine setup (install, first run, VCV account, Library subscribe, audio check)
- Kickoff prompt for OpenCode: repo `AGENTS.md`

## Decision log

| Date | Decision |
|---|---|
| 2026-07-12 | Approved as P3 artistic build (gap analysis §12.2); patch-authorship core, OSC delegation to osc-mcp |
| 2026-07-12 | Catalog fifty-fifty generative/performance |
| 2026-07-12 | Rack 2 Free confirmed on Goliath; render ladder Recorder → Cardinal → Pro |
| 2026-07-12 | Catalog v1 = free Library modules only; webapp gets Modules depot/download facility (report/link/sideload tiers) |
| 2026-07-12 | Module install-while-running solved via `rack_cycle` restart choreography, NOT Windows GUI automation — Rack has no runtime plugin loading, so restart is mandatory regardless; process lifecycle beats pixel-clicking |
