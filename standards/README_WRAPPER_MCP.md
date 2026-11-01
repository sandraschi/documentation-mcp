---
title: "Wrapper MCP README Standard"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-09
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# Wrapper MCP README Standard

**Status**: ACTIVE - all MCP repos that wrap a host application  
**Adopted**: 2026-05-29  
**Audience**: Repo maintainers, agents editing READMEs, fleet grading  
**Related**: [README_STRUCTURE.md](./README_STRUCTURE.md), [README_WEBAPP_SCREENSHOTS.md](./README_WEBAPP_SCREENSHOTS.md), [LLM_AND_INSTALL_TIERS.md](./LLM_AND_INSTALL_TIERS.md)

---

## Scope

Applies to any MCP server whose **primary job is driving another program**:

| Class | Examples |
|-------|----------|
| Creative / 3D | blender-mcp, gimp-mcp, inkscape-mcp, davinci-resolve-mcp |
| EDA / CAD | kicad-mcp, freecad-mcp, qcad-mcp, chip-design-mcp |
| DCC / animation | tahoma2d-mcp, vroidstudio-mcp, obs-mcp |
| Media | handbrake-mcp, reaper-mcp |

**Not wrapper repos:** pure API MCPs (github, filesystem, email) - they skip this doc except optional pipeline notes.

---

## The two README jobs (wrapper repos)

1. **Execution honesty** - Does the host app run headless, with GUI, or both? Never bury this.
2. **Pipeline clarity** - What goes **in** (hands-in) and what comes **out** (hands-out) for agents and fleet chaining.

Screenshots show the **webapp**; this standard shows the **host-app contract**.

---

## Required README section: How it runs

Place **immediately after** the one-line description (before Features or Preview).

### Template

```markdown
## How it runs

| Mode | Host app | When |
|------|----------|------|
| **Headless (default)** | Blender subprocess, no window | Batch export, CI, agents without display |
| **Live GUI (optional)** | Blender + bridge addon | Watch the agent build; viewport screenshots |
| **Not supported** | - | Sculpting that needs interactive tablet input |

**You do not need to open Blender's UI** for most MCP tools - the server spawns headless `blender --background` automatically.

Install [Blender](https://www.blender.org/download/) separately; it is never bundled.
```

### Rules

| Rule | Detail |
|------|--------|
| **Headless default must be explicit** | If the wrappee runs without GUI for the common path, say so in **bold plain language** in the first paragraph |
| **GUI optional vs required** | Separate rows - never imply “no install” when host app is required |
| **Per-operation exceptions** | If *some* tools need GUI (e.g. tahoma2d scene authoring), list them |
| **Hybrid lanes** | Split table by lane (kicad-mcp: stable CLI vs IPC vs TCP bridge) |
| **No false “fully headless”** | If Docker/Linux headless differs from Windows GUI bridge, document both |

### Fleet examples (copy patterns)

| Repo | Headless story (README must state) |
|------|-------------------------------------|
| **blender-mcp** | Default: headless `BlenderExecutor` subprocess. Optional: live session + bridge addon to watch in GUI. |
| **kicad-mcp** | Exports/DRC: stable `kicad-cli` (no pcbnew window). CRUD: 11 nightly IPC headless **or** KiCad GUI + TCP bridge. |
| **tahoma2d-mcp** | **Render**: headless `tcomposer.exe`. **Scene edit**: Tahoma2D GUI only (ToonzScript unavailable in this build). |
| **gimp-mcp** | Inkscape/GIMP path: clarify which ops spawn GUI vs batch CLI |
| **davinci-resolve-mcp** | Resolve often needs GUI/project open - if any headless path exists, label it experimental |
| **vroidstudio-mcp** | VRoid Studio GUI for authoring; MCP for launch/export/status |
| **obs-mcp** | OBS must be running; webapp is control plane, not a replacement for OBS UI |

---

## Required README section: Hands-in / Hands-out

**Hands-in** = what the agent (or upstream MCP) **feeds into** this wrappee.  
**Hands-out** = what this wrappee **produces** for the user or downstream MCP.

This is the fleet **pipeline vocabulary** - especially for blender-mcp and creative chains.

### Template

```markdown
## Hands-in / Hands-out

| Direction | Artifacts | Notes |
|-----------|-----------|-------|
| **Hands-in** | `.blend`, image refs, natural-language scene prompts | Upload via webapp or tool params |
| **Hands-in** | Rodin/Tripo mesh URLs | `blender_ai_generate` |
| **Hands-out** | `.glb`, `.vrm`, `.fbx`, viewport PNG | `blender_export`, `blender_render` |
| **Hands-out** | `.blend` (saved scene) | After agent edit session |

### Fleet pipelines (downstream)

| Downstream MCP | Takes from blender-mcp |
|----------------|------------------------|
| [tahoma2d-mcp](…) | Rendered image sequences / GP output for compositing |
| [godot-mcp](…) | `.glb` / `.gltf` |
| [vrchat-mcp](…) | `.vrm` after validation |
| [freecad-mcp](…) | `.step` via intermediate export (if documented) |
```

### Rules

| Rule | Detail |
|------|--------|
| **At least one hands-in and one hands-out row** | Even if “prompt text” is the only input |
| **File extensions matter** | Agents choose tools by artifact type |
| **Link downstream MCPs** | When fleet-tested; use mcp-central-docs project paths |
| **Distinguish webapp upload vs MCP tool** | e.g. “`pcb_load` ← `.kicad_pcb` in uploads dir” |
| **Headless outputs** | Mark which hands-out work **without** host GUI |

### Reference: blender-mcp (canonical)

```
Agent prompt / MCP tools
        │  hands-in: prompts, .blend, mesh URLs, bpy scripts
        ▼
   blender-mcp ──► headless Blender OR live bridge
        │  hands-out: .glb, .vrm, .blend, PNG, MP4 (VSE), splat files
        ▼
   tahoma2d-mcp / godot-mcp / vrchat-mcp / freecad-mcp …
```

blender-mcp README should keep this section updated when export formats or fleet partners change.

### Reference: kicad-mcp (hybrid headless)

```
Agent / uploads
        │  hands-in: .kicad_pcb, .kicad_sch (copies in work dir)
        ▼
   kicad-mcp
        ├─ export lane (headless stable CLI) ── hands-out: Gerber, STEP, GLB, DRC JSON
        └─ CRUD lane (IPC nightly or GUI bridge) ── hands-out: modified .kicad_pcb
        ▼
   freecad-mcp (STEP enclosure), chip-design-mcp, fabrication
```

---

## Required doc: `docs/WRAPPEE.md`

**Added 2026-07-30.** A dedicated page for the wrapped host application -
separate from the README, since the README's "What this wraps" section
should stay to a sentence or two.

### Contents

```markdown
# {Host App Name}

One paragraph: what it is, who makes/maintains it, license.

## Disambiguation (when needed)

If the name is easily confused with something else, say so plainly. Example:
Overte split from the original Vircadia/High Fidelity codebase; current
"Vircadia" has since pivoted to an unrelated product (Vircadia World -
Postgres/Bun/TypeScript) that shares no protocol or client with Overte.
This repo targets Overte, not current Vircadia.

## Links

- Official site: …
- Source / GitHub: …
- Documentation: …
- Community: Discord / Matrix / Reddit / Mastodon - whatever actually exists,
  don't pad with a channel that doesn't
```

### Why this matters most for obscure wrappees

A well-known host app (Blender, KiCad) barely needs this - everyone already
knows what it is. An obscure, older, or ambiguously-renamed one (Overte,
Resonite, various niche DCC tools) is exactly where a reader lands confused
("wait, isn't this Vircadia?") without ever finding the disambiguation. This
doc is the fix: one clear, honest, linkable place for "what is the thing
we're wrapping," independent of how well-known it happens to be.

Don't fabricate links or community channels - if there's no Reddit or
Discord, say so or omit the row rather than inventing one.

---

## Combined README order (wrapper + webapp)

**Update (2026-07-30)**: "How it runs" and "Hands-in / Hands-out" now nest
under one `## What You Can Do` heading instead of being separate top-level
sections - see [README_STRUCTURE.md](./README_STRUCTURE.md) for the current
template. The content and rules below are unchanged, just the heading level.

For wrapper repos with a dashboard, use this section order:

```markdown
# repo-name
One sentence.

## What this wraps  ← REQUIRED - name the wrappee immediately, link docs/WRAPPEE.md
…

## Preview              ← REQUIRED if webapp ([screenshots standard](./README_WEBAPP_SCREENSHOTS.md))
…

## What You Can Do      ← REQUIRED (this doc) - How it runs + Hands-in/Hands-out + feature bullets
…

## Quick Install
…
```

---

## Callout boxes (recommended)

Use a visible callout when headless is the main selling point:

```markdown
> **Headless by default** - KiCad's pcbnew window does not need to be open for exports,
> DRC, or Gerber generation. PCB editing uses either headless IPC (KiCad 11 nightly)
> or the legacy GUI bridge - see [NIGHTLY_HEADLESS.md](docs/NIGHTLY_HEADLESS.md).
```

```markdown
> **Watch or batch** - Most tools run headless Blender. Enable the bridge addon only
> if you want to see the viewport update live while the agent works.
```

Avoid burying headless facts only in INSTALL.md or ARCHITECTURE.md - **README is the evaluation surface**.

---

## INSTALL.md alignment

INSTALL.md must repeat the execution table (or link to README § How it runs) and must not contradict it.

| README says | INSTALL must not say |
|-------------|-------------------|
| Headless default | “Open Blender first” as step 1 for every tool |
| GUI required for authoring | “Fully automated, no GUI ever” |
| Hybrid lanes | Single undifferentiated “kicad-cli” without IPC vs stable |

---

## Agent / llms.txt alignment

`llms.txt` should include a short block:

```text
## Execution
- Default: headless Blender subprocess (no GUI)
- Optional: live bridge for viewport watch
## Artifacts
- In: .blend, prompts, mesh URLs
- Out: .glb, .vrm, PNG, .blend
```

---

## mcp-central-docs project pages

Each `projects/{repo}/README.md` for wrapper MCPs must include:

- One-line **headless vs GUI** summary in the opening paragraph
- Mini hands-in / hands-out table (can be shorter than repo README)
- Link to repo `docs/` for execution details

---

## Checklist (wrapper repos)

- [ ] README **What this wraps** - names the wrappee immediately, links `docs/WRAPPEE.md`
- [ ] `docs/WRAPPEE.md` - host app overview, disambiguation if the name is confusable, community/official links (no fabricated links)
- [ ] README **What You Can Do** - headless/GUI honesty + hands-in/hands-out table + capability bullets, in one section
- [ ] Headless callout if default path needs no host GUI
- [ ] INSTALL.md consistent with execution table
- [ ] `llms.txt` execution + artifacts block
- [ ] Preview screenshots (webapp repos) - [README_WEBAPP_SCREENSHOTS.md](./README_WEBAPP_SCREENSHOTS.md)
- [ ] Fleet project page updated

---

## Anti-patterns

| Don't | Do |
|-------|-----|
| “Control Blender with AI” (implies GUI) | “Headless Blender by default; optional live viewport” |
| Hide headless behind “Advanced” | Lead with how it runs |
| List 58 tools with no artifact story | Hands-in / hands-out table |
| Screenshot of Blender UI as product | Screenshot of **your** webapp; Blender only in pipeline diagram |
| “KiCad MCP” without lane split | Stable export vs CRUD backend explicit |

---

## Rollout priority

1. **blender-mcp** - reference implementation (dual mode + fleet pipelines)
2. **kicad-mcp** - hybrid headless lanes
3. **tahoma2d-mcp**, **gimp-mcp**, **davinci-resolve-mcp**
4. Remaining wrapper fleet from [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md)

Track in per-repo STATUS.md and fleet grading notes.

---

## See also

- [README_WEBAPP_SCREENSHOTS.md](./README_WEBAPP_SCREENSHOTS.md) - Preview images
- [README_STRUCTURE.md](./README_STRUCTURE.md) - Primary README skeleton
- [CONTROL_PLANE_INSTALL.md](./CONTROL_PLANE_INSTALL.md) - RoboFang **hands** vs control plane
- [operations/FLEET_CONTROL_PLANE.md](../operations/FLEET_CONTROL_PLANE.md) - `hands/` clones
- [FLEET_PROMOTION.md](./FLEET_PROMOTION.md) - discovery without spam (pairs with screenshots + wrapper honesty)
- blender-mcp: [docs/COMPETITIVE_ANALYSIS.md](https://github.com/sandraschi/blender-mcp/blob/main/docs/COMPETITIVE_ANALYSIS.md) - Live GUI vs headless
- kicad-mcp: [docs/NIGHTLY_HEADLESS.md](https://github.com/sandraschi/kicad-mcp/blob/main/docs/NIGHTLY_HEADLESS.md)

