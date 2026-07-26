# Fleet Promotion — Useful Discovery, Not AI Spam

**Status**: ACTIVE — guidance for all sandraschi MCP repos and apps  
**Adopted**: 2026-05-29  
**Audience**: Maintainers, future-you posting on GitHub/Goodreads/forums  
**Related**: [README_WEBAPP_SCREENSHOTS.md](./README_WEBAPP_SCREENSHOTS.md), [README_WRAPPER_MCP.md](./README_WRAPPER_MCP.md), [ecosystem/glama/REGISTRY_GUIDE.md](../ecosystem/glama/REGISTRY_GUIDE.md)

---

## Principle

Promotion should feel like **a useful pointer**, not a product launch.

Readers should finish thinking: *“That solves a problem I have”* — not *“Another AI grifter showed up.”*

| Works | Feels obnoxious |
|-------|-----------------|
| Concrete workflow (“export highlights → Calibre shelf”) | “Revolutionary AI-powered paradigm shift” |
| Link + 3 sentences + screenshot | Emoji thread, “game changer”, “10x productivity” |
| Responding to someone’s existing question | Cold-posting the same pitch on 40 repos |
| “I built X; feedback welcome” | “You MUST try this” |
| Showing hands-in/out artifact paths | Vague “integrates with AI agents” |

**Show the workflow. Skip the rah-rah.**

---

## Promotion stack (do these first)

These are **baseline discovery**, not spam — maintain once, update on releases.

| Layer | Action | Effort |
|-------|--------|--------|
| **README** | Preview screenshots, How it runs, Hands-in/out ([wrapper standard](./README_WRAPPER_MCP.md)) | Per repo |
| **INSTALL.md** | Option A `.mcpb` drag-and-drop path works on naked PC | Per repo |
| **Glama** | `glama.json` + submit/update listing | [REGISTRY_GUIDE](../ecosystem/glama/REGISTRY_GUIDE.md) |
| **Smithery** | Badge + install one-liner in README | When packaged |
| **`llms.txt`** | Accurate tool + artifact summary for indexers | Required fleet bar |
| **GitHub** | Topics (`mcp`, `fastmcp`, host-app tag), Releases with `.mcpb` | Per repo |
| **mcp-central-docs** | `projects/{repo}/README.md` project page | Fleet mirror |

Only after the stack is honest and tested should you post outward.

---

## Channel guide

### A — MCP registries & catalogs (low risk)

**Glama, Smithery, MCP Registry, awesome-mcp lists**

- Factual description, no superlatives
- List **what tools do**, not “AI magic”
- Keep Glama listing in sync when tool count changes

### B — Wrappee GitHub (medium risk, high reward if done right)

Post on the **host app’s** repo when you have a **real integration** (blender-mcp, kicad-mcp, calibre-mcp, gimp-mcp).

**Prefer:**

- **GitHub Discussions** (if enabled) — “Community tools” or “Show and tell”
- **Issues** only when framed as *integration feedback* or *documentation of a working bridge* — not feature requests to upstream

**Before posting, check:**

1. `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, pinned issues — **anti-AI or anti-bot stance?**
2. Recent tone — hostile to automation? **Skip or use personal blog link only**
3. Is there already a community MCP thread? **Reply there; don’t duplicate**

**Template (issue or discussion):**

```markdown
### Community MCP bridge (optional, not official)

I maintain an open-source MCP server that drives {HostApp} headlessly for Claude Desktop / Cursor users:
{repo URL}

**What it does (concrete):**
- {one bullet: e.g. batch export GLB}
- {one bullet: e.g. metadata search without opening Calibre GUI}

**What it does not do:**
- Not affiliated with {HostApp} project
- Does not replace the official app; requires separate install

Happy to adjust if this duplicates an existing effort. No obligation for upstream to endorse.
```

**Do not:**

- Mass-open identical issues across KiCad + Blender + GIMP same week
- Ask upstream to “add to official docs” in the first post
- Use “AI will replace your workflow” framing
- Post in security-sensitive repos without maintainer rapport

### C — User communities (medium risk)

| Community | Fits | Example |
|-----------|------|---------|
| **Goodreads** | calibre-mcp, reading workflows | See [calibre-mcp/PROMOTION.md](../projects/calibre-mcp/PROMOTION.md) |
| **r/selfhosted, r/calibre** | Self-hosted library automation | “I run Calibre + this MCP for…” — follow sub rules |
| **KiCad / Blender forums** | Wrapper MCPs | Technical post: headless export path, link repo |
| **Discord (project official)** | Only if rules allow tools | Ask mods first |

**Reddit rule:** One post per sub, account with history, respond to comments, no cross-post spam.

### D — Fleet cross-promotion (low risk)

Link **downstream** MCPs in Hands-out tables (blender → godot, kicad → freecad, calibre → translate-mcp).

- mcp-central-docs `projects/FLEET_INDEX.md`
- CalFolio / iOS apps → calibreops backend (already documented under `projects/apple/`)

This is **internal SEO** — helpful, not loud.

### E — Technical content (best long-term ROI)

- Blog-style doc in repo: “How I automated Gerber export with kicad-mcp”
- Stammtisch / conference demo kit ([CURSOR_STAMMTISCH_DEMO_KIT.md](../research/agentic-ide/CURSOR_STAMMTISCH_DEMO_KIT.md))
- 2-minute screen recording (webapp demo, no voiceover hype)

### F - Fleet Discord (emerging)

A single fleet Discord server with **one channel per battlegroup**, not per repo:

```
# announcements            - releases, major updates (bot-posted only)
# general                  - anything fleet-related
# artistic-creative        - blender, comfyops, godot, virtualdj, ...
# infrastructure-ops       - fleet-agent, monitoring, aiwatcher, ...
# robotics-hardware        - yahboom, unitree, limx, ...
# generative-ai            - local-llm, arxiv, advanced-memory, ...
# media-library            - calibre, plex, immich, bookmarks, ...
# research                 - arxiv, notebooklm, ...
# communication            - email, discord, telephony, ...
# productivity-office      - libreoffice, beyondcompare, ...
# support                  - how do I install X questions
# bug-reports              - link to GitHub issues
```

**Why battlegroup channels, not per-repo:** 100+ channels for 100+ repos is noise. Most would sit silent for months. Category channels keep conversation findable without overwhelming new joiners.

**Start small:** 3-4 channels initially (general, support, bug-reports, one battlegroup). Let usage guide expansion. A silent 20-channel server feels deader than a silent 3-channel one.

**discord-mcp integration:**
- Agents can post release summaries to announcements channel when a new tag is pushed
- Bug reports cross-posted from GitHub issues to bug-reports channel via webhook
- discord-mcp tool `ask_docs` could answer how-do-I-use-X questions by reading the repo's `llms-full.txt` in real-time, turning the support channel into a RAG-powered helpdesk

Technical posts age well; “🚀 AI MCP” tweets do not.

---

## Tone checklist (read before any public post)

- [ ] First sentence states **what the tool does**, not how “smart” it is
- [ ] No “game-changer”, “10x”, “revolution”, “the future of X”
- [ ] Mentions **host app by name** and clarifies **not official**
- [ ] Includes **one concrete example** (file type, command, screenshot)
- [ ] Offers feedback channel (GitHub issue), not “DM me for beta”
- [ ] If AI-adjacent: say **“MCP / Claude Desktop / Cursor”** plainly — don’t hide the agent angle
- [ ] If community is AI-skeptic: lead with **automation/scripting** angle, mention MCP second

---

## Repo-specific notes

| Repo | Promotion angle | Channels |
|------|-----------------|----------|
| **calibre-mcp** | Library power-users, metadata RAG, companion to Calibre not replacement | Goodreads, r/calibre, MobileRead, Glama |
| **blender-mcp** | Headless batch + optional live watch; VRM/VR pipeline | Blender Artists forum, wrappee discussion, VRChat communities |
| **kicad-mcp** | Hybrid headless exports + agent PCB inspect | KiCad forum (technical), EDA Reddit — avoid “AI designs boards for you” |
| **gimp-mcp / inkscape-mcp** | Batch vector/raster without GUI tour | GIMP/Inkscape issue/discussion if welcoming |
| **translate-mcp** | Human→regex translation, CalFolio chain | Language-learning subs — utility not “AI translator hype” |

Per-repo playbooks: `projects/{repo}/PROMOTION.md` (add as needed).

---

## Anti-AI-community map (rough)

| Signal | Action |
|--------|--------|
| Pinned “no AI PRs” / “no LLM-generated issues” | **Do not** open promotional issues |
| Maintainers actively hostile in issues | Skip GitHub; blog + Glama only |
| Neutral / tools welcome | Discussion post OK with template above |
| Official plugin ecosystem exists | Position as **external** community tool; compare to plugin, don’t compete |

When unsure: **lurk 10 minutes** in Issues/Discussions before posting.

---

## What we do not do (fleet-wide)

- Paid astroturf, fake reviews on Glama
- Bot replies on Stack Overflow with repo links
- Scraping emails / DM spam
- Claiming official partnership without permission
- “AI will fix your {host app} bugs” messaging
- Repeated bump comments on stale issues

---

## Metrics (lightweight)

Track in repo or project STATUS.md — no vanity obsession:

| Metric | Why |
|--------|-----|
| Glama/Smithery install clicks | Discovery working |
| GitHub stars (slow growth OK) | README/screenshots helping |
| Issues from **real users** | Product-market signal |
| Wrappee discussion replies | Community acceptance |
| Goodreads shelf adds / listopia (calibre) | Niche reach |

---

## Rollout

1. **Foundation** — README Preview + wrapper sections on top 5 repos
2. **Registries** — Glama/Smithery audit (Q2 2026)
3. **calibre-mcp** — Goodreads pilot ([PROMOTION.md](../projects/calibre-mcp/PROMOTION.md))
4. **Wrappee posts** — one repo, one host, measure response; then next
5. **Demo videos** — webapp 60s captures for blender-mcp, kicad-mcp

---

## See also

- [PACKAGING_STANDARDS.md](./PACKAGING_STANDARDS.md) — `glama.json`, MCPB
- [README_WEBAPP_SCREENSHOTS.md](./README_WEBAPP_SCREENSHOTS.md) — visual hook
- [README_WRAPPER_MCP.md](./README_WRAPPER_MCP.md) — honest headless messaging
- [projects/PROMOTION.md](../projects/PROMOTION.md) — index of per-repo playbooks
