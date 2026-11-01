# Fleet visibility / promotion optimization — per-repo plan

**Status:** PLAN (approved to execute in waves)  
**Created:** 2026-07-26  
**Owner:** sandraschi  
**Canonical tone:** [standards/FLEET_PROMOTION.md](../standards/FLEET_PROMOTION.md)  
**Index of playbooks:** [PROMOTION.md](./PROMOTION.md)

---

## Problem

Exact-name GitHub search (`blender-mcp`, `discord-mcp`, …) is **star-sorted**. A 15k-star collision buries median-2 fleet repos on page 1. Description + topics will **not** win that fight — they improve long-tail, topic filters, list hover, and Glama/crawler text.

Obscure / long-tail queries already put us on page 1 when About/README/topics contain the differentiator phrases seekers type.

---

## Goals

1. Every **public** `*-mcp` (and key apps) has an About description matching the formula in FLEET_PROMOTION.
2. Topics always include `mcp`, `fastmcp`, `mcp-server` (+ host + capability tags).
3. README H1 / first 40 lines lead with **distinct job**, not generic “AI MCP”.
4. Per-repo promotion playbook stubs for top collision / dogfood heroes.
5. Track in a simple sheet: description updated? topics OK? long-tail query smoke?

---

## Non-goals

- Buying stars, fake engagement, mass identical issues
- Fighting exact `blender-mcp` SERP vs 15k-star incumbents as primary strategy
- Auto-posting to Mastodon/Reddit without human approve (fleet-PR + mastodon-mcp outbox)

---

## Already done (2026-07-26 wave 0)

| Repo | About refreshed | Topics boosted |
|------|-----------------|----------------|
| blender-mcp | Yes (headless / VSE / bridge) | headless, model-context-protocol |
| kicad-mcp | Yes | mcp-server, headless, … |
| gimp-mcp | Yes (was weak) | mcp, headless, batch-processing |
| mixx-dj-mcp | Yes (Demucs / video / mixxxxx) | mcp, fastmcp, demucs |
| discord-mcp | Yes | mcp-server, discord-bot |
| godot-mcp | Yes | mcp-server, headless |
| calibremcp | Yes | mcp, calibre, ebook |
| immichmcp | Yes | mcp, immich, selfhosted |

`draft_engine.DIFFERENTIATORS` in fleet-public-relations-mcp covers hooks for several of the above.

---

## Wave plan

### Wave 1 — High collision wrappers (public)

Repos where the short name is crowded. Optimize for long-tail differentiators.

| Repo | Diff lead | Status |
|------|-----------|--------|
| blender-mcp | done | wave 0 |
| godot-mcp | done | wave 0 |
| gimp-mcp | done | wave 0 |
| inkscape-mcp | headless SVG/batch | **done 2026-07-26** |
| freecad-mcp | headless CAD + CFD | **done 2026-07-26** |
| libreoffice-mcp | headless docs/calc | **done 2026-07-26** |
| obsmcp | OBS scenes/stream | **done 2026-07-26** |
| resolume-mcp | VJ / clip decks | **done 2026-07-26** (may be private) |
| handbrakemcp | batch encode | **done 2026-07-26** |
| davinci-resolve-mcp | timeline/agent | **done 2026-07-26** |

**Actions per repo:** `gh repo edit` description; `--add-topic`; README first paragraph if soft; add `DIFFERENTIATORS` entry in fleet-PR.

### Wave 2 — Self-host / ops (public)

| Repo | Diff lead | Status |
|------|-----------|--------|
| immichmcp | done | wave 0 |
| calibremcp | done | wave 0 |
| qbtmcp | torrent automation | **done 2026-07-26** |
| plexmcp | library agent | **done 2026-07-26** |
| jellyfin-mcp | self-hosted media | **done 2026-07-26** |
| bookmarks-mcp | bookmark RAG | **done 2026-07-26** |
| home-assistant-mcp | local HA control | pending |

### Wave 3 — Fleet-unique / dogfood heroes

Compete on unique product, not short name:

| Repo | Angle |
|------|-------|
| mixx-dj-mcp + mixxxxx | video Mixxx + Demucs stems — **first Mastodon dogfood** |
| splatmaker-mcp | FOSS Gaussian splats |
| arxiv-mcp | high-density research tools |
| advanced-memory-mcp | Zettel/ADN |
| scraper-mcp | ToolBench+Glama+LobeHub grades hub |
| winops / fileops | Windows control plane |

### Wave 4 — Comms (when public)

| Repo | Note |
|------|------|
| discord-mcp | done metadata |
| mastodon-mcp | **private** — skip public About until `.nopublish` lifted |
| email-mcp | outbound/inbound automation |

---

## Per-repo checklist (agent or human)

```text
[ ] gh repo view — capture current description + topics
[ ] Draft About ≤350 chars: Host + FastMCP + 2–3 concrete caps + Cursor/Claude + differentiator
[ ] Tone lint (no game-changer / 10x / written-by-AI)
[ ] Topics: mcp, fastmcp, mcp-server, {host}, {capability…} (8–12)
[ ] README: H1 or first lines include long-tail phrase
[ ] Optional: DIFFERENTIATORS[repo] in fleet-public-relations-mcp
[ ] Optional: projects/{repo}/PROMOTION.md stub (channels only)
[ ] Smoke: GitHub search `"{diff phrase}" mcp` — note page rank
[ ] Log row in tracking table below
```

### Tracking table (fill as waves run)

| Repo | Wave | Desc date | Topics date | Long-tail query tried | Notes |
|------|------|-----------|-------------|----------------------|-------|
| blender-mcp | 0 | 2026-07-26 | 2026-07-26 | headless blender mcp | |
| mixx-dj-mcp | 0 | 2026-07-26 | 2026-07-26 | mixxx demucs mcp | dogfood |
| … | | | | | |

---

## Automation (optional later)

- Script: `mcp-central-docs/scripts/optimize-repo-visibility.ps1`
  - Input: CSV of repo, description, topics[]
  - Calls `gh repo edit` + `--add-topic`
  - Dry-run default
- fleet-PR tool: `pr_visibility_audit(repo_id)` → current GH About vs formula + scraper grades

---

## Success metrics (lightweight)

| Signal | Target |
|--------|--------|
| Long-tail search page-1 for hero diffs | ≥5 repos documented |
| Public repos missing `mcp` topic | 0 after wave 2 |
| Real issues from discovery (not self) | track quarterly |
| Mastodon dogfood (mixx) dry→live | human-gated |

---

## Execution order (next session)

1. Wave 1 remaining wrappers — **executed 2026-07-26** (inkscape, freecad, libreoffice, obsmcp, handbrakemcp, davinci, resolume)
2. Wave 2 partial — qbtmcp, plexmcp, jellyfin-mcp, bookmarks-mcp
3. Draft `projects/blender-mcp/PROMOTION.md` + `mixx-dj-mcp/PROMOTION.md`
4. Optional dry-run visibility script
5. New-repo gate: root `start.bat` + `mcp-central-docs/starts/{repo}-start.bat` (see START_SCRIPT_STANDARD)

Do **not** mass-open wrappee GitHub issues in the same week.
