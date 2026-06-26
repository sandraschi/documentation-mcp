# Control Plane and Agent Stack Install Tiers

**Status**: ACTIVE — advanced / infrastructure repos only  
**Adopted**: 2026-05-28  
**Audience**: Maintainers of RoboFang, DeepFang, OpenClaw, NanoClaw, and agent orchestrators  
**Baseline for normal MCP servers:** [LLM_AND_INSTALL_TIERS.md](./LLM_AND_INSTALL_TIERS.md)

---

## One-line rule

**Control-plane repos orchestrate other repos; they are not Steve-class drag-and-drop MCP servers.** Install docs must state tier, isolation model, and what is cloned vs containerized — never pretend they are Option A `.mcpb` products.

---

## Repo classes

| Class | Examples | Primary install surface | Typical user |
|-------|----------|-------------------------|--------------|
| **MCP hand** | blender-mcp, email-mcp, filesystem-mcp | Option A `.mcpb` or Tauri NSIS | Claude Desktop user, naked PC |
| **Control plane** | robofang | `start.ps1` / hub UI; manifest + `hands/` clones | Fleet operator on one workstation |
| **Isolation stack** | deepfang | `start.ps1` + **Docker required** (multi-container) | Security-conscious operator |
| **Agent runtime / gateway** | openclaw, nanoclaw, openclaw-molt-mcp | CLI + gateway URL; often already running | Power user / homelab |
| **Agent bridge MCP** | openclaw-molt-mcp, openmanus-mcp, goose-mcp | MCP config pointing at **external** CLI/API | IDE user with agent already installed |

Do **not** merge these classes in one INSTALL.md without labeled sections.

---

## RoboFang (fleet supervisor)

**Role:** Thin control plane — index, install, launch, health for MCP **hands** (independent repos).  
**Source of truth:** Each MCP repo. RoboFang does **not** vendor server code in `tools/`.

| Surface | Purpose |
|---------|---------|
| Hub webapp (10870) | Fleet visibility, hand status |
| Bridge (10871) | Clone/install into `hands/<repo>/` |
| Supervisor (10872) | Orchestration hooks |

**Install tier:** **Operator (Tier D+)** — not naked Option A.

**INSTALL.md must say:**
- Requires Git, uv, Node (or document `start.ps1` `Require-Command` auto-install)
- Hands are **cloned on demand** — not bundled in RoboFang installer
- Adding a hand = manifest entry + clone path, not copying server into RoboFang
- See [FLEET_CONTROL_PLANE.md](../operations/FLEET_CONTROL_PLANE.md)

**Naked install testing:** Consumer sandbox validates **individual hands** (e.g. blender-mcp), not RoboFang bootstrap — unless testing RoboFang's own `start.ps1` on Dev Infra sandbox.

---

## DeepFang (execution isolation stack)

**Role:** Sanitize → adjudicate → dispatch pipeline with **hard Docker network isolation** (supervisor, sanitizer, adjudicator, air-gapped worker, Prometheus/Loki/Grafana).

**Install tier:** **Infrastructure (Tier I)** — Docker **required**, not optional.

| Component | Notes |
|-----------|-------|
| `start.ps1` | Naked-PC compliant for *host* prereqs (uv, etc.) |
| `docker compose` | **Required** for the product — document prominently |
| Ollama / DeepSeek | Optional adjudicator backends — document, never bundle models |

**INSTALL.md must say:**
- Docker Desktop required (winget link)
- Multi-port stack (10956–10963) — [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md)
- Not a Claude Desktop `.mcpb` product
- RoboFang may **call** DeepFang preflight — integration doc, not duplicate install

**Naked install testing:** Dev Infra or dedicated Docker host — **not** consumer sandbox alone.

---

## OpenClaw / NanoClaw (agent gateways)

**Role:** External agent runtimes (Gateway, sessions, tools). Fleet repos **bridge** to them; they do not replace Claude Desktop for Steve-class users.

| Pattern | Install |
|---------|---------|
| User runs OpenClaw/NanoClaw separately | Official upstream install + gateway URL |
| Fleet MCP bridge (e.g. openclaw-molt-mcp) | Option C MCP config → `opencode serve` / gateway HTTP |
| Cursor/Claude | MCP stdio or SSE to **bridge repo**, not to OpenClaw core |

**INSTALL.md must say:**
- Prerequisite: OpenClaw (or NanoClaw) **already installed and running**
- Bridge repo does **not** ship the agent runtime
- API keys / gateway token in CONFIGURATION.md
- Tier B cloud LLM may apply inside the agent — document upstream, not duplicated here

**Do not:** List OpenClaw as Option A drag-and-drop for non-dev users unless shipping a tested all-in-one installer (not current fleet standard).

---

## How this maps to LLM tiers A–D

| LLM tier ([LLM_AND_INSTALL_TIERS.md](./LLM_AND_INSTALL_TIERS.md)) | Control-plane usage |
|---------------------------------------------------------------------|---------------------|
| A — Ollama/LM Studio beginner | Individual MCP hands + webapp Settings |
| B — Cloud API weak PC | Hands + agent bridges; OpenCode + cheap model |
| C — vLLM homelab | DeepFang adjudicator, RoboFang routing hints |
| D — Developer | All control-plane repos |
| **I — Infrastructure** | DeepFang Docker stack; observability-only Docker on hands |

---

## INSTALL.md template by class

### MCP hand (blender-mcp — reference pilot)

- Options A–D per [README_STRUCTURE.md](./README_STRUCTURE.md)
- Host app + LLM sections per [LLM_AND_INSTALL_TIERS.md](./LLM_AND_INSTALL_TIERS.md)
- Docker optional footnote

### Control plane (robofang)

```markdown
## Who this is for
Fleet operators — not Claude-only end users.

## Prerequisites
Git, uv, Node (or start.ps1 auto-install)

## Install
git clone … ; .\start.ps1

## Add a hand
Bridge UI or manifest — clones repo to hands/

## Not included
Individual MCP servers (install each hand separately)
```

### Isolation stack (deepfang)

```markdown
## Prerequisites
Docker Desktop (required), uv, Git

## Install
.\start.ps1   # then docker compose up per docs

## Not for
Claude Desktop Option A users without Docker
```

### Agent bridge MCP (openclaw-molt-mcp)

```markdown
## Prerequisites
OpenClaw gateway running (upstream install link)

## Option C — MCP config
… stdio/SSE to this bridge only …

## Not bundled
OpenClaw, NanoClaw, or LLM weights
```

---

## Naked install testing matrix

| Repo | Consumer sandbox | Dev Infra sandbox | Docker VM |
|------|------------------|-------------------|-----------|
| blender-mcp | **Yes** (primary pilot) | Option D smoke | No |
| git-github-mcp | Yes | Option D | No |
| robofang | No (operator tool) | start.ps1 smoke | Optional |
| deepfang | No | Partial | **Yes** |
| openclaw-molt-mcp | No (needs gateway) | With OpenClaw running | Optional |

**Designated pilot for host-app + LLM tier docs:** **blender-mcp** — see [NAKED_INSTALL_TESTING.md](./NAKED_INSTALL_TESTING.md).

---

## Related docs

| Doc | Topic |
|-----|-------|
| [FLEET_CONTROL_PLANE.md](../operations/FLEET_CONTROL_PLANE.md) | RoboFang three-phase model |
| [LLM_AND_INSTALL_TIERS.md](./LLM_AND_INSTALL_TIERS.md) | Bundling, Ollama/cloud, Docker optional for hands |
| [NAKED_INSTALL_TESTING.md](./NAKED_INSTALL_TESTING.md) | Consumer vs Dev Infra sandbox |
| [PYWINAUTO_MCP_SAFETY.md](../patterns/PYWINAUTO_MCP_SAFETY.md) | OpenManus + pywinauto + agent stacks |

---

## Changelog

| Date | Change |
|------|--------|
| 2026-05-28 | Initial standard: RoboFang, DeepFang, OpenClaw/NanoClaw vs MCP hands |
