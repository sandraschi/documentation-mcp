# README Webapp Screenshots Standard

**Status**: ACTIVE — adopt progressively across fleet webapp MCP repos  
**Adopted**: 2026-05-29  
**Audience**: Repo maintainers, agents editing READMEs, fleet grading  
**Related**: [README_STRUCTURE.md](./README_STRUCTURE.md), [README_WRAPPER_MCP.md](./README_WRAPPER_MCP.md), [rules/playwright_e2e_sota.md](./rules/playwright_e2e_sota.md), [WEBAPP_STANDARDS.md](./WEBAPP_STANDARDS.md)

---

## Why this exists

Fleet MCP servers often wrap **host apps with hyper-complicated native UI** (Blender, GIMP, KiCad, DaVinci Resolve, VRoid Studio, etc.). Our value is not “another copy of the host UI” — it is an **AI-oriented control surface**: fewer clicks, clearer status, demo pipelines, tool catalogs, and agent-friendly REST/MCP bridges.

**Screenshots in READMEs make that contrast obvious in five seconds.**

| Without screenshot | With screenshot |
|--------------------|-----------------|
| Reader imagines “yet another MCP wrapper” | Reader sees a **clean dashboard** vs mental model of native chaos |
| Glama / Smithery / GitHub scroll-past | Visual hook increases installs and stars |
| Agents rely on tool lists only | Humans **and** agents get layout context (“Dashboard shows CRUD backend”) |

This is **self-promotion that earns trust** — not decoration. It answers: *“What do I get that I don’t already have in the host app?”*

**Pair with** [README_WRAPPER_MCP.md](./README_WRAPPER_MCP.md): screenshots sell the **webapp**; How it runs + Hands-in/out explain the **host contract** (headless default, pipeline artifacts). Never show only native host UI screenshots without stating headless mode elsewhere in README.

---

## When screenshots are required

| Repo type | Requirement | Minimum |
|-----------|-------------|---------|
| **Webapp MCP** (Vite/React dashboard on fleet port) | **Required** for README v1.1+ | 1 hero + 1 feature |
| **Wrapper MCP** (host app UI is complex: Blender, GIMP, KiCad, Resolve, …) | **Required** — emphasize simplified UI | 1 hero + 1 “native vs wrapper” caption |
| **stdio-only MCP** (no meaningful UI) | Optional | Architecture diagram instead |
| **mcp-central-docs project page** | Recommended thumbnail | Link to `:PORT` or checked-in PNG |

**Fleet grading** (see [FLEET_GRADING_STANDARDS.md](./FLEET_GRADING_STANDARDS.md)): webapp repos without any README visual after 2026-06-01 should not claim **DONE** marketing/docs tier until screenshots land.

---

## What to show (wrapper repos)

Prioritize **clarity over pixel-perfect marketing**.

### Hero (required)

- **Dashboard** or primary landing page at default zoom
- Visible: app name, connection/status KPIs, sidebar or tool list
- Dark theme OK if that is the default — stay consistent with shipped webapp

### Feature shot (required)

Pick **one** differentiator:

- Demo / one-click pipeline page (kicad-mcp, blender-mcp)
- 3D or media viewer (PCB GLB, model preview)
- Status page showing hybrid backends / bridge mode
- Tool execution result panel (before/after)

### Optional third shot

- Mobile-narrow layout (only if responsive matters)
- Light theme variant (only if user-selectable and maintained)

### Caption pattern (required under each image)

```markdown
![KiCad MCP dashboard — export lane + CRUD backend status](docs/screenshots/dashboard.png)

*AI-oriented dashboard: KiCad’s native UI has dozens of panels; this surface exposes MCP tools, upload/export paths, and backend status in one view.*
```

For **wrapper contrast**, name the host app explicitly in the caption.

---

## File layout

```
repo-root/
├── README.md
└── docs/
    └── screenshots/
        ├── README.md              ← index + capture instructions
        ├── dashboard.png          ← hero (1280×720 or 1440×900)
        ├── feature-demo.png       ← second shot
        └── _source/               ← optional raw Playwright output (gitignored)
```

### Asset rules

| Rule | Value |
|------|--------|
| Format | **PNG** (UI clarity); WebP optional for web-only mirrors |
| Max width | 1280px (resize in CI or before commit) |
| Max file size | **300 KB** per image (use pngquant or similar if needed) |
| Naming | `dashboard.png`, `pcb-viewer.png`, `demo-pipeline.png` — kebab-case |
| Do not commit | Full-window 4K dumps, animated GIFs >2 MB, screenshots with secrets/API keys |

Add to repo `.gitignore` if using automated capture:

```
docs/screenshots/_source/
```

---

## README placement

Insert **after** the one-line description, **before** Features (see [README_STRUCTURE.md](./README_STRUCTURE.md)).

```markdown
# kicad-mcp

AI-driven KiCad automation — MCP tools + a focused web dashboard (not a KiCad clone).

## Preview

| Dashboard | Demo pipeline |
|-----------|---------------|
| ![Dashboard](docs/screenshots/dashboard.png) | ![Demo](docs/screenshots/demo-pipeline.png) |

*Left: fleet dashboard (11017). Right: one-click 12-step export demo — no KiCad GUI required for exports.*

## Features
…
```

**Do not** replace the Documentation table or Quick Install with images-only READMEs — text remains primary for agents; images sell the human evaluators.

---

## Playwright capture pipeline (to develop)

Screenshots should be **regeneratable**, not one-off manual grabs. Extend existing e2e infra ([playwright_e2e_sota.md](./rules/playwright_e2e_sota.md)).

### Phase 1 — Manual (now)

1. `just serve` or `webapp/start.ps1`
2. Open `http://localhost:PORT`
3. Capture at 1280×720 (Windows Snipping Tool or browser devtools device mode)
4. Save to `docs/screenshots/`
5. PR with README update

### Phase 2 — Scripted capture (fleet standard)

Add to `webapp/e2e/screenshots.spec.ts` (or `webapp/scripts/capture-readme-screenshots.ps1` calling Playwright):

```typescript
import { test } from '@playwright/test';

test('capture readme screenshots', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 720 });
  await page.goto('/');
  await page.waitForSelector('[data-testid="dashboard-ready"]', { timeout: 30000 });
  await page.screenshot({ path: '../docs/screenshots/dashboard.png });
  await page.goto('/demo');
  await page.waitForSelector('[data-testid="demo-ready"]');
  await page.screenshot({ path: '../docs/screenshots/demo-pipeline.png' });
});
```

**Requirements for Phase 2:**

- `data-testid="dashboard-ready"` (and similar) on stable UI anchors — not brittle text selectors
- `just screenshots` recipe in `justfile`:

```just
screenshots:
    cd webapp && npx playwright test e2e/screenshots.spec.ts --project=chromium
```

- Optional CI job: on `release` tag or monthly cron, open PR **“chore: refresh README screenshots”** if pixel diff exceeds threshold
- Never fail main CI on screenshot drift initially — **warn-only** until 3+ repos stable

### Phase 3 — Fleet automation (virtualization-mcp / meta)

- Install Test webapp page triggers capture inside consumer sandbox (future)
- Central gallery in mcp-central-docs `projects/*/README.md` thumbnails

---

## Host-app wrapper messaging

Use README screenshots to reinforce this narrative:

```
Native host app          →    Our webapp              →    MCP / agent
(complex, expert UI)         (status, demos, files)        (tools, automation)
```

**Example captions:**

| Repo | Caption angle |
|------|----------------|
| **blender-mcp** | “Blender’s UI spans 20+ editors; this dashboard lists MCP tools and scene status without opening Blender.” |
| **gimp-mcp** | “GIMP’s toolbox + docks vs a single upload/process/download flow.” |
| **kicad-mcp** | “Hybrid KiCad install status + demo pipeline — no pcbnew window required for exports.” |
| **davinci-resolve-mcp** | “Resolve’s page tree vs project/media status for agent-driven renders.” |
| **vroidstudio-mcp** | “VRoid’s 3D studio vs export/status control plane.” |

Avoid misleading shots: if a feature **requires** the host app open, say so in the caption.

---

## mcp-central-docs project pages

Each `projects/{repo}/README.md` should include when webapp exists:

```markdown
## Preview

![{repo} dashboard](../../../path-or-github-raw-url/dashboard.png)

Source: `{repo}/docs/screenshots/` · Live: http://localhost:{PORT}
```

Prefer **GitHub raw URLs** on tagged releases for stable rendering on github.com; checked-in paths for local fleet mirror.

---

## Checklist (per repo)

- [ ] `docs/screenshots/` directory exists
- [ ] `docs/screenshots/README.md` lists files + how to regenerate
- [ ] Primary `README.md` has **Preview** section with ≥2 images
- [ ] Captions mention **AI-oriented / simplified** value vs host app (wrapper repos)
- [ ] No secrets, local paths, or PII in images
- [ ] Images ≤300 KB each at 1280px width
- [ ] Playwright capture spec stubbed or implemented (`just screenshots`)
- [ ] mcp-central-docs project page updated with thumbnail

---

## Anti-patterns

| Don't | Do instead |
|-------|------------|
| Screenshot of native Blender/GIMP as if it were your webapp | Screenshot **your** webapp; mention host in caption |
| 6 MB uncompressed PNG | Resize + compress |
| Screenshot-only README | Preview section + existing text structure |
| Stale UI from 3 releases ago | Regenerate on major webapp changes; date in `docs/screenshots/README.md` |
| Light theme shot when app ships dark-only | Match default theme |

---

## Rollout priority (suggested)

1. **kicad-mcp** — dashboard + demo pipeline (hybrid status story)
2. **blender-mcp**, **gimp-mcp** — strongest wrapper contrast
3. **davinci-resolve-mcp**, **vroidstudio-mcp**, **obs-mcp**
4. Remaining webapp fleet from [SOTA_MASTER_INVENTORY.md](../operations/SOTA_MASTER_INVENTORY.md)

Track completion in fleet inventory notes or per-project STATUS.md.

---

## References

- [README_STRUCTURE.md](./README_STRUCTURE.md) — Primary README sections
- [rules/playwright_e2e_sota.md](./rules/playwright_e2e_sota.md) — e2e baseline
- [WEBAPP_SOTA_STANDARDS.md](./WEBAPP_SOTA_STANDARDS.md) — webapp layout conventions
- [operations/WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md) — port per repo
