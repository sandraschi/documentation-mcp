---
name: fleet-expert
description: Fleet-wide reference for what repos do, port assignments, and cross-repo handoffs. Resolves via live indexes (never a static roster): voice-bus aliases for spoken names, FLEET_INDEX for catalog, WEBAPP_PORTS + claim_ports for ports, starts/ scripts for launch, per-repo AGENTS.md for depth. Also covers adjacent/alternative repos, upstream handling, ArtCraft craft apps, and Rustification buckets. Use for fleet catalog lookups, port queries, integration design, and deciding which repo handles a task.
---

# Fleet Expert

**Scope**: The big picture — every repo, port, integration, and architecture pattern across the fleet.

**Canonical source**: `D:\Dev\repos\mcp-central-docs\skills\fleet-expert\SKILL.md` (this file). Vendored by reference into repos — do not fork it per-repo.
**Standards root**: `mcp-central-docs/standards/`
**Port registry**: `mcp-central-docs/operations/WEBAPP_PORTS.md`
**Known bugs**: `mcp-central-docs/troubleshooting/BUGS_DEPOT.md`

**Freshness rule (2026-10-13): this skill contains no repo roster by design.** A static table rots within weeks against daily repo additions. Resolve everything through the live indexes in §2, in order. Indexes live with the work; this skill only holds stable patterns (§1) and illustrative examples (§6, marked as such).

---

## 1. Architecture Patterns (stable — safe to quote)

Two tracks since 2026-10-17 regime change (see `standards/RUST_ARTCRAFT_STANDARD.md`):

**Track A — Pure-Rust ArtCraft** (`Cargo.toml` at root, Buckets A/B):
```
L1 (<domain>-core) direct in-process dispatch, no HTTP sidecar
L2 (<domain>-mcp) CLI-first clap binary (--json) + hand-rolled MCP stdio loop
L3 (<domain>-app) eframe/egui native GPU desktop, zero ports, zero node_modules
```
Gates: `cargo clippy --workspace --all-targets --all-features -- -D warnings` (deny unwrap/expect/panic/todo), `cargo test --workspace`, `cargo fmt --check`. Zero ports claimed. NSIS via `installer/installer.nsi` (no WebView2).

**Track B — Legacy Python / FastMCP** (`pyproject.toml` at root, Buckets C/D):
```
Backend (FastMCP 3.4+ + Starlette/FastAPI, port {B})
  ├── REST API at /api/*
  ├── MCP transport at /mcp (streamable HTTP, plus stdio for local clients)
  └── Health at /health
Frontend (React + Vite + Tailwind, port {F})
  └── Proxies /api and /mcp to backend
Native (Tauri 2.0, optional)
  └── PyInstaller-frozen backend embedded inside NSIS installer
```
Fleet standards: `uv` package manager, `ruff` linter, `pytest` test runner, `biome` for TS/JS.
Version floors move — check `mcp-central-docs/standards/JUNE_2026_STANDARDS_BAR.md` for the current FastMCP floor, never quote one from memory.
Infrastructure tier: repos mark `infrastructure: true` in manifests (credential vaults, artifact depots, shared LLMs, observability, orchestration); webapp for diagnostics only.

### Port Convention (stable — safe to quote, Python track only)

- **Reservoir**: 10700-15000 for webapps (widened to 15000 on 2026-10-13; the registry table itself is truth over any cached number).
- **Adjacency Rule**: Frontend and backend for one project MUST be adjacent (e.g. 10792/10793).
- **Tauri side-by-side**: repo with Tauri desktop app claims a SECOND pair for the installed operator; operator port is never the dev backend port.
- **FORBIDDEN**: 3000, 5000, 5173, 8000, 8080.
- **Never invent a port.** Claim one with `mcp-central-docs/fleet-gate/claim_ports.py`, which checks `WEBAPP_PORTS.md` *and* every `fleet-start.config.ps1`.

---

## 2. Find Any Repo (lookup procedure — follow in order)

### Step 1 — Spoken or colloquial name → voice-bus aliases

`mcp-central-docs/config/voice_command_bus.yaml` maps everyday words to the owning server and tool: aliases like `[dreame, dream, vacuum, robohoove, hoover, robovac]` → server `dreame`, keywords `[clean, vacuum, sweep, mop]` → tool `dreame_tool`. "Hoover bot", "the vacuum", "start cleaning" all resolve here first. If the name isn't an alias, continue.

### Step 2 — Canonical catalog → FLEET_INDEX.md

`mcp-central-docs/projects/FLEET_INDEX.md` is the repo roster: type, status, description, registered ports per repo. Check its `Last Updated` header — if the repo is newer than the header date, fall through to Steps 3-4 rather than concluding it doesn't exist.

### Step 3 — Ports → the registry, never memory

`mcp-central-docs/operations/WEBAPP_PORTS.md` is the port truth. Backend/frontend pairs, claim dates, move history. For a new allocation use `fleet-gate/claim_ports.py`, never hardcode.

### Step 4 — Launch → starts/ scripts and repo entry points

- `mcp-central-docs/starts/<name>-start.bat` — canonical per-repo launchers.
- Repo root `start.ps1` / `start.bat` + `fleet-start.config.ps1` — the repo's own declared startup (ports, venv, preflight).
- Non-MCP upstreams (local models, engines) live outside the fleet pattern — read their own docs (e.g. Strata: `START-HERE.bat`, OpenAI-compat on its own port).

### Step 5 — Depth → per-repo AGENTS.md + skills/

Every active repo has `<repo>/AGENTS.md` (ports, tool pattern, key files, test/lint/build commands) and often `skills/<name>-*.md` operator guides with exact tool operations, device facts, and known issues. Read these before touching the repo — they outrank any summary.

### Step 6 — Prove it by running

A lookup isn't done until something executes: health endpoint answers, `opencode mcp list` shows `✓ connected`, or a stdio handshake prints ready. After any restart, verify a NEW PID owns the port. A gate that reports success having examined nothing is this fleet's most common failure mode.

---

## 3. Adjacent / Alternative Repos (which repo handles it?)

Overlap is intentional — check before building:

1. Search `FLEET_INDEX.md` for the capability noun first (e.g. `audio`, `cad`, `ebook`, `robot`). If 2+ repos match, read both `AGENTS.md` "Scope / Non-goals" sections.
2. Prefer the wrappee-owner: the repo named after the software it wraps owns that API (e.g. `blender-mcp` for Blender, `calibre-mcp` for Calibre). A generic repo doing the same thing is the alternative, not the default.
3. One-hop rule: fleet crossconnects are single-hop (`arxiv-mcp → calibre-mcp`), never chains. If your design needs 2+ hops, you picked the wrong entry point.
4. If both a Python repo and a `rust-*-mcp` exist for the same domain, Rust is canonical for Buckets A/B (REST/clean-hardware/system). Python stays canonical for Buckets C/D (embedded host-app, CUDA/PyTorch). See §5.
5. When in doubt, ask in the repo's `fleet-<name>` Discord channel — each has one — before scaffolding a new repo. New repos need a FLEET_INDEX entry + claimed ports before code.

## 4. Upstream / External Handling (read-only by default)

- `_upstream/` = third-party clones (incl. all xyzcraft + Strata). Check `git remote -v` per dir: `origin=storytold` = pure clone (pull-only), `origin=sandraschi` + `upstream=storytold` = fork (pushable, PRs go upstream). Default read-only either way; never modify without a reason.
- `external/` = 66 vendored reference clones (migration planned, do NOT move anything). `D:\Dev\external\` stray dir (`calibre` duplicates `repos\external\calibre`) is known-misplaced — do not fix by hand.
- `_archives/` = frozen. Never build on top of it; copy out if you must revive.
- Never invent an upstream URL — use the explicit remote URL from `git remote -v`. Hallucinated repo/skill names are a promptware vector (see `standards/threats/AGENTIC_BOTNETS.md`).

## 5. ArtCraft Craft Apps + Rustification (where the fleet is going)

- **Public banner**: 13 pure-Rust Craft apps by storytold (CADCraft, DeckCraft, DesignCraft, EffectCraft, FigCraft, FilmCraft, GridCraft, LightCraft, PdfCraft, PhotoCraft, SoundCraft, VectorCraft, WordCraft). Each = native app + CLI + MCP server. Fleet r11n borrows the harness, does not reimplement. Inventory: `standards/rust-artcraft/CRAFT_APPS_MCP_UTILIZATION.md`. Control planes: `standards/rust-artcraft/CRAFT_COMMAND_BUS.md` (headless `run` vs live `mcp --attach/--bridge/--connect`).
- **4-Bucket Triage** (`standards/RUST_ARTCRAFT_STANDARD.md` §3): A (REST/cloud/SQLite/CLI/system) + B (clean hardware/SCPI/LAN IoT) → build Pure-Rust; C (embedded host-app Python) + D (CUDA/ML) → stay Python/FastMCP. Default is Rust unless the dossier names a Bucket C/D blocker in `docs/DEVELOPMENT.md`.
- **Conversion macro**: `repconv <repo>` per `patterns/REPCONV_SOP.md` (shadow-then-swap vs in-place, 70% reusable kernel, 4-PR tiered factory). Never fail a Rust repo for lacking `pyproject.toml` / `webapp/` / `fastmcp` / `prefab-ui` / ports.
- **Vendoring this skill**: this file is the source. Repos carry a thin shim at `src/<pkg>/skills/fleet-expert/SKILL.md` pointing here — never a full copy. Update here once, all shims follow.

---

## 6. Cross-Fleet Integration Points (ILLUSTRATIVE EXAMPLES, not exhaustive)

| Integration | Source → Destination | What Flows |
|------------|---------------------|------------|
| CFD → Godot | freecad-cfd → godot-mcp | Velocity field CSV → particle animation |
| Paper → Calibre | arxiv-mcp → calibre-mcp | PDF + metadata → ebook library |
| AI video → ittybitty | google-ai-mcp → ittybitty | Veo-generated clips |
| Audio → Game | speech-mcp → godot-mcp | TTS narration → 3D scene |
| News → Digest | aiwatcher-mcp → email | RSS → scored daily digest (+ TTS) |
| Media request | arr-mcp → jellyfin-mcp | Add + scan new media |
| Benchmark verify | arxiv-mcp → epoch | Claimed scores vs public DB |
| Robot teleop | teleoperator-mcp → yahboom-mcp | WebXR → robot action |
| Vacuum map → Robot nav | dreame-mcp → yahboom-mcp | LIDAR floor map (`GET /api/v1/map`) → shared spatial ground truth |

For a real integration design, check both repos' AGENTS.md for current tool surfaces — examples above may predate refactors.

---

## 7. Related Skills

For per-repo implementation work (Tauri build, CUA test, MCPB, assess & fix, webapp SOTA, tool design), use the **repo-expert** skill.
