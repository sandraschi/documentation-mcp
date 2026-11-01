# Fleet Quality Check — SOP

**Trigger**: `qualitycheck <repo>`
**Reference macro**: `agentic_macros.md` → `qualitycheck`
**Scope**: Strategic quality assessment of a fleet MCP server. Beyond mechanical SOTA compliance — asks whether the repo is worth having, how it fits the fleet, and where it could go.

**Rule**: This is a qualitative assessment by the LLM, not a checklist of binary pass/fail items. Use judgment. Be honest. Flattery helps no one.

---

## Why qualitycheck

assfix tells you if a repo meets the technical bar. qualitycheck tells you if the repo *matters*. A perfectly formatted repo wrapping a service nobody needs is still worthless. A scrappy repo with a unique angle and deep integration potential is valuable despite cosmetic flaws.

Run qualitycheck before deciding to invest significant effort in a repo, or when triaging which repos to promote, archive, or deprecate.

---

## Phase 1 — Context

Read the repo's `README.md`, `llms-full.txt`, `pyproject.toml`, and the project page at `mcp-central-docs/projects/{repo}/README.md` (if it exists). Understand:

- What does this server do? (1-sentence elevator pitch)
- What host app or service does it wrap?
- Who is the target user?
- How long has it existed? (check git log for first commit)

---

## Phase 2 — Strategic dimensions

Score each dimension 1-10. 1 = worst in fleet, 10 = best in class. Explain the score in 1-2 sentences.

### 2A. Originality

| Score | Meaning |
|-------|---------|
| 1-3 | Direct clone of an existing MCP server with trivial changes |
| 4-6 | Novel combination of existing ideas, or a unique wrapper for a well-known service |
| 7-8 | Genuinely novel approach to a known problem space |
| 9-10 | First-of-its-kind MCP server, opens a new category |

**Consider:** Are there 5+ other MCP servers doing the same thing? What differentiates this one? Does it solve a problem no other server addresses?

### 2B. Difficulty

| Score | Meaning |
|-------|---------|
| 1-3 | Thin HTTP wrapper around a well-documented REST API, <200 lines of logic |
| 4-6 | Moderate complexity: state management, multiple API surfaces, some custom logic |
| 7-8 | Hard: protocol translation, host-app IPC, real-time state, multi-process coordination |
| 9-10 | Very hard: compiler/interpreter integration, hardware drivers, novel protocol design |

**Consider:** Lines of code (rough), number of modules, external dependencies, whether it uses `subprocess`, `ctypes`, or platform-specific APIs.

### 2C. Wrappee importance

Not all wrappees are open-source. Use multiple signals to gauge importance:

| Signal | What to look for |
|--------|-----------------|
| **GitHub stars** (if OSS) | Direct popularity signal |
| **User base** (if proprietary) | Downloads, registered users, market share. VirtualDJ has 100M+ users — zero stars but clearly important. |
| **Industry adoption** | Is it standard in its domain? (DaVinci Resolve in film, KiCad in open-source PCB design, Ableton in music production) |
| **Community activity** | Forums, subreddit subscribers, StackOverflow questions, YouTube tutorial count |
| **Enterprise/corporate backing** | Google, Adobe, Autodesk, Blackmagic — a wrappee backed by a major company has staying power |
| **Unique capability** | Is there no alternative? (e.g. a specific robot arm, a niche but irreplaceable protocol) |

| Score | Meaning |
|-------|---------|
| 1-3 | Obscure or abandoned — no community, no users, no corporate backing |
| 4-6 | Niche but active — dedicated user base in its domain, 1k-10k GitHub stars OR comparable proprietary reach |
| 7-8 | Major — industry-standard tool, 10k-100k stars OR millions of users OR major corporate backing |
| 9-10 | Giant — ubiquitous, platform-defining, 100k+ stars OR tens-of-millions of users OR category-defining proprietary product |

**Consider:** Total addressable audience, not just GitHub stars. A wrapper for VirtualDJ (100M+ users, proprietary) is more impactful than a wrapper for a 500-star OSS library. A wrapper for a niche 50k-star OSS tool with no alternative (e.g. KiCad) is more important than a wrapper for a 200k-star tool that already has 10 MCP servers.

### 2C-ii. Wrappability surface

What interface does the wrappee expose for automation? This determines how deep the MCP server can go:

| Surface | Examples | Integration depth |
|---------|----------|------------------|
| **CLI** | `soffice --headless --convert-to`, `ffmpeg -i`, `kicad-cli` | Shallow — command-line flags only. Easy to build, limits what you can do. |
| **REST API** | GitHub API, Notion API, Plex API, Discord API | Medium — well-documented endpoints, rate limits, auth. Fleet standard pattern. |
| **SDK / client library** | `discord.py`, `plexapi`, `boto3`, `gitpython` | Medium-High — language-native, handles auth and retries. Fleet standard pattern. |
| **IPC / sockets** | OSC protocol, WebSocket, named pipes, D-Bus | High — real-time, bidirectional, but fragile. Requires careful lifecycle management. |
| **COM / D-Bus** | LibreOffice UNO, Windows shell, KiCad IPC | High — deep host-app integration, can control the app from inside. Very version-sensitive. |
| **Plugin / extension system** | Blender add-ons, GIMP plugins, VS Code extensions, KiCad actions | High — runs inside the host process, full access. Requires distribution within the host's ecosystem. |
| **File format** | `.blend`, `.kicad_pcb`, `.psd`, `.aup3` | Low-Medium — read/write native files without the host app. Portable but limited to data, no execution. |
| **Headless/server mode** | Unity `-batchmode`, FreeCAD CLI, Godot headless | Medium — runs the full engine without a GUI. Powerful but resource-heavy. |
| **Macro/scripting language** | VBA, AutoHotkey, Lua scripting, Python macro | Medium — pre-written automation scripts. Can be powerful but limited by the host's scripting API. |

**Consider:** What's the primary integration surface? Does the MCP server use the best available surface, or the easiest one? A CLI wrapper is quick to build but often limited — going deeper (IPC, plugin) unlocks more value but costs more to maintain.

Also note the wrappee's release cadence: stable LTS (easy to keep up), monthly releases (moderate maintenance), weekly/rolling (high maintenance). A wrappee that breaks its API every release is a maintenance sink regardless of its popularity.

### 2D. Competitive situation

| Score | Meaning |
|-------|---------|
| 1-3 | 10+ existing MCP servers for the same service, all more mature |
| 4-6 | 3-5 competitors, this one is competitive |
| 7-8 | 1-2 competitors, this one is clearly better |
| 9-10 | No credible competitors — first/only MCP server for this service |

**Consider:** Search GitHub and glama.ai for competing MCP servers. How do they compare on tool count, documentation, stars, release cadence?

**Multi-word wrappee search:** For two-word wrappees like "Virtual DJ", search multiple naming conventions — repos may be named `virtual-dj-mcp`, `virtualdj-mcp`, `virtual_dj_mcp`, or `dj-mcp`. Run at least two searches with different separators. Don't overdo it — three variants max — but a single search often misses half the competitive landscape.

### 2E. Tool surface

| Score | Meaning |
|-------|---------|
| 1-3 | <5 tools, all trivial passthrough |
| 4-6 | 5-15 tools, covers the main use cases |
| 7-8 | 15-30 tools, deep coverage of the wrapped service |
| 9-10 | 30+ tools, portmanteau-structured, comprehensively covers the API surface |

**Consider:** Tool count from `llms-full.txt` or server code. Portmanteau pattern used? Prefab cards for list/status tools? Good docstrings with `## Return Format` and `## Examples`?

### 2F. Webapp quality

| Score | Meaning |
|-------|---------|
| 1-3 | No webapp, or a bare scaffold with placeholder content |
| 4-6 | Functional webapp with core pages, basic styling |
| 7-8 | Good webapp: all mandatory pages, dynamic discovery, dark theme, data-testid |
| 9-10 | Excellent webapp: SOTA-compliant, beautiful, fast, accessible, with Chat + Tools + Skills + Logs |

**Consider:** assfix webapp SOTA score if available. Number of pages, dynamic vs hardcoded content, visual polish.

### 2G. Fleet integration

| Score | Meaning |
|-------|---------|
| 1-3 | Standalone island — no integration with other fleet repos |
| 4-6 | Consumes from or feeds into 1-2 other fleet repos |
| 7-8 | Part of a fleet battlegroup: consumes from and feeds into multiple repos |
| 9-10 | Central node in a fleet battlegroup — critical path for others |

**Consider:** Does it have documented handoffs to other repos? Is it consumed by fleet-agent-mcp, aiwatcher-mcp, or other central services? Does it participate in A2A flows?

### 2H. Battlegroup fit

Identify which fleet battlegroup(s) the repo belongs to:

| Battlegroup | Focus | Example repos |
|-------------|-------|---------------|
| **Artistic / Creative** | Image, video, audio, 3D generation | blender-mcp, comfyops-mcp, godot-mcp, virtualdj-mcp |
| **Infrastructure / Ops** | Monitoring, deployment, security | fleet-agent-mcp, monitoring-mcp, aiwatcher-mcp |
| **Robotics / Hardware** | Physical world interaction | yahboom-mcp, unitree-mcp, limx-robotics-mcp |
| **Generative / AI** | LLM, embedding, inference, agents | local-llm-mcp, advanced-memory-mcp, arxiv-mcp |
| **Media / Library** | Books, video, audio libraries | calibre-mcp, plex-mcp, immich-mcp, bookmarks-mcp |
| **Research / Academic** | Papers, citations, knowledge | arxiv-mcp, notebooklm-fleet-mcp |
| **Communication** | Email, messaging, notifications | email-mcp, discord-mcp, telephony-mcp |
| **Design / CAD** | 3D modeling, PCB design | freecad-mcp, kicad-mcp, qcad-mcp |
| **Productivity / Office** | Documents, spreadsheets | libreoffice-mcp, beyondcompare-mcp |

Score how well it fulfills its battlegroup role:

| Score | Meaning |
|-------|---------|
| 1-3 | Peripheral to its battlegroup — duplicates functionality |
| 4-6 | Solid member — does one thing well |
| 7-8 | Key member — others depend on it |
| 9-10 | Indispensable — the battlegroup would be significantly weaker without it |

### 2I. Gaps & growth scenarios

Identify 3-5 specific gaps or growth opportunities:

| Type | What to look for |
|------|-----------------|
| **Missing tools** | What operations does the wrapped service expose that this server doesn't cover? |
| **Integration gaps** | What handoffs to other fleet repos are missing? |
| **Webapp gaps** | What pages or features would significantly improve UX? |
| **Performance** | Is there a known bottleneck? (e.g. synchronous HTTP in an async tool) |
| **Documentation** | What's missing from README, llms-full.txt, or the project page? |
| **Distribution** | MCPB published? NSIS installer? Claude Desktop snippet in README? |

For each gap, rate the impact of fixing it:

| Impact | Meaning |
|--------|---------|
| **Low** | Nice-to-have, little user-facing difference |
| **Medium** | Noticeable improvement, some users will benefit |
| **High** | Significant value, removes a major friction point |
| **Critical** | Blocking adoption — fix before promoting |

---

## Phase 3 — Overall score

| Dimension | Weight | Score (1-10) | Weighted |
|-----------|--------|-------------|----------|
| Originality | 10% | | |
| Difficulty | 10% | | |
| Wrappee importance | 15% | | |
| Competitive situation | 10% | | |
| Tool surface | 15% | | |
| Webapp quality | 10% | | |
| Fleet integration | 15% | | |
| Battlegroup fit | 15% | | |
| **Total** | **100%** | | |

Overall rating:

| Score | Rating |
|-------|--------|
| 9.0-10 | **Flagship** — promote, invest, reference architecture |
| 7.0-8.9 | **Strong** — solid member, worth maintaining |
| 5.0-6.9 | **Good** — useful but needs work to reach potential |
| 3.0-4.9 | **Weak** — consider deprecation if no growth path |
| 1.0-2.9 | **Runt** — should this exist at all? |

---

## Phase 4 — Report

Write the assessment to `reports/quality-{repo}-{YYYY-MM-DD}.md`:

```powershell
$reportPath = "reports/quality-${repo}-$(Get-Date -Format 'yyyy-MM-dd').md"
```

Also write `.qualitycheck-timestamp` at the repo root (committed):

```powershell
@{ timestamp = (Get-Date -Format "o"); repo = $repo; overall = $score; rating = $rating } | ConvertTo-Json | Set-Content ".qualitycheck-timestamp"
```

The `reports/` directory MUST be in `.gitignore`. Check before writing.

---

## Anti-patterns

| Anti-pattern | Why it fails |
|-------------|-------------|
| **Inflating scores** | A 7/10 on everything is worthless. Be willing to give 1-3 when deserved. |
| **Ignoring competitors** | "This is unique" is only true if you actually searched for alternatives. |
| **Confusing effort with value** | A 5000-line server that wraps a niche tool is less valuable than a 200-line server that wraps GitHub. Effort != impact. |
| **No growth path** | If you can't identify at least 3 ways the repo could improve, you didn't look hard enough. |
| **Same score for every repo** | Calibrate across the fleet. If everything is 7/10, nothing is. |
