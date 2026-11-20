# LLM Vulnerability Flood vs. Local Fleet Threat Model and Sweep Plan (Nov 2026)

**Last Updated**: 2026-11-18
**Tags**: [llm-vulns, cors, loopback-binding, supply-chain, csrf, dns-rebinding, fleet-hardening]
**Status**: active - sweep plan ready for phased execution

## TL;DR

Automated SOTA LLM exploit discovery (source-to-sink taint analysis + agentic fuzzing against FOSS codebases) has collapsed the disclosure-to-exploit window for public perimeter infrastructure. Our local Windows 11 fleet (~190 active MCP servers and webapps running on `localhost:10700-15000` / Tailscale) is **insulated from direct WAN perimeter scanning**, so daily CVE churn in public web frameworks does not require panic patching.

However, the LLM vuln flood directly threatens this fleet through **four local pivot vectors**:
1. **Browser-to-Localhost Pivot (CSRF / Fetch from Infected Websites)**: Visiting a compromised website while local MCP webapps run with `allow_origins=["*"]` or `0.0.0.0` binding allows malicious page JS to silently invoke local REST/MCP endpoints.
2. **Supply-Chain Poisoning (`PyPI` / `npm` / `crates.io`)**: Compromised upstream FOSS projects or GitHub Actions pipelines push trojaned patch releases that execute during `uv sync` or `bun install`.
3. **Indirect Prompt Injection -> Un-gated Local Actuators**: Poisoned web pages, PDFs, or emails trick an agent into calling local shell, file, or GUI automation tools.
4. **Native Parser Exploitation on Untrusted Artifacts**: Crafted PDFs, EPUBs, media files, or binaries exploiting C/C++ parser libraries (`ffmpeg`, `calibre`, `ghidra`, PDF/archive unpackers) invoked by local MCP servers.

---

## 1. Fleet Exposure Measurement (Measured 2026-11-18)

Full ripgrep and filesystem census across `D:\Dev\repos` (excluding `_upstream`, `_archives`, `_junk`, `external`, `externals`, `.venv`, `node_modules`, `target`, `dist`, `mcpb`, `mcp-central-docs`):

| Vector / Indicator | Line Hits | Files | Repos | Risk Assessment |
|--------------------|-----------|-------|-------|-----------------|
| **Server `0.0.0.0` Binding** (`host="0.0.0.0"`, `--host 0.0.0.0`, `0.0.0.0:<port>`) | 165 | 147 | **61** | Exposes local backends to LAN/Wi-Fi peers and container bridges instead of loopback (`127.0.0.1`). Note: `standards/STARLETTE_NO_PYDANTIC_STANDARD.md` line 124 still shows `host="0.0.0.0"` in its Starlette skeleton. |
| **Wildcard CORS** (`allow_origins=["*"]`, `CorsLayer::permissive()`) | 121 | 118 | **81** | Allows any external website open in the browser to read responses and fire cross-origin requests against `http://localhost:107xx`. |
| **Combined `0.0.0.0` + Wildcard CORS** | - | - | **22** | Highest network/browser pivot exposure; includes Tier 1/2/3 actuator and host-control servers. |
| **Missing `uv.lock` (Python repos)** | - | - | **8 / 251** | 243 of 251 Python repos have `uv.lock`. Missing: `containercraft`, `dj-media-hub`, `doccraft`, `filecraft`, `fleet-tool-bridge`, `gitcraft`, `revecraft`, `rust-test-c`. |
| **Missing Node/Bun lockfile (`package.json`)** | - | - | **6 / 100** | 94 of 100 frontend repos have a lockfile. Missing: `avatar-pipeline-mcp`, `demo-app`, `myvrworlds`, `suno-mcp`, `triton-mcp` (plus orphan dir `DDevrepossysinternals-mcpweb_sota`). |

### The 22 Repos with BOTH `0.0.0.0` Binding and Wildcard CORS

```text
advanced-memory-mcp, ai-games-collection, chitchat, davinci-resolve-mcp,
deepfang, magentart-mcp, mcp-studio, monitoring-mcp, multi-backup-mcp,
myai, nest-protect-mcp, obs-mcp, opencode-cli-mcp, plex-mcp,
pywinauto-mcp, readly-mcp, robotics-mcp, rustdesk-mcp, suno-mcp,
system-admin-mcp, tailscale-mcp, virtualization-mcp
```

### High-Risk Tier 1/2/3 Servers Exposed (Cross-Referenced with `AGENT_ACTION_GATES.md`)

| Repo | Tier / Capability | `0.0.0.0` Bind | Wildcard CORS |
|------|-------------------|----------------|---------------|
| `robotics-mcp` | Tier 1: Physical actuators | Yes | Yes |
| `opencode-cli-mcp` | Tier 2: Whole-machine control / CLI exec | Yes | Yes |
| `pywinauto-mcp` | Tier 2: Windows GUI automation | Yes | Yes |
| `system-admin-mcp` | Tier 2: System administration | Yes | Yes |
| `rustdesk-mcp` | Tier 2: Remote desktop control | Yes | Yes |
| `tailscale-mcp` | Tier 2: Mesh network control | Yes | Yes |
| `virtualization-mcp` | Tier 3: VM lifecycle / exec | Yes | Yes |
| `plex-mcp` | Tier 3: Media library mutation | Yes | Yes |
| `universal-actuator-mcp` | Tier 1: Physical actuators | No | Yes |
| `windows-operations-mcp` | Tier 2: PowerShell/cmd exec, registry, services | No | Yes |
| `autohotkey-mcp` | Tier 2: Input/window automation | No | Yes |
| `devices-mcp` | Tier 1: Home/hardware devices | Yes | No |
| `fleet-agent-mcp` | Tier 2: Fleet agent orchestration | Yes | No |
| `uitars-mcp` | Tier 2: CUA desktop control | Yes | No |
| `podman-mcp` | Tier 3: Container management | Yes | No |
| `arr-mcp` | Tier 3: Media stack management | Yes | No |
| `database-operations-mcp` | Tier 3: Database queries/mutations | Yes | No |

---

## 2. Hardening Rules for the Fleet

### Rule 1: Default Loopback Binding (`127.0.0.1`)
- All FastAPI, Starlette, Uvicorn, and Axum servers MUST bind to `127.0.0.1` by default.
- If LAN or Tailscale access is explicitly required for a specific service, bind to the specific Tailscale IP or gate behind an explicit env var (`<REPO>_HOST=127.0.0.1` default, overridden only in local `.env`), and require Bearer token auth when non-loopback.

### Rule 2: Explicit Local Origin Allowlist (No `allow_origins=["*"]`)
- Replace `allow_origins=["*"]` and `CorsLayer::permissive()` with explicit origin lists restricted to the repo's assigned frontend port from `operations/WEBAPP_PORTS.md` and Tauri webview origins:
  ```python
  ALLOWED_ORIGINS = [
      f"http://localhost:{FRONTEND_PORT}",
      f"http://127.0.0.1:{FRONTEND_PORT}",
      "tauri://localhost",
      "http://tauri.localhost",
      "https://tauri.localhost",
  ]
  ```
- Never combine `allow_credentials=True` with wildcard origins.

### Rule 3: Lockfile Freeze & Supply-Chain Hygiene
- Every repo with `pyproject.toml` MUST commit `uv.lock`; every webapp with `package.json` MUST commit `bun.lock`.
- Do not run automated fleet-wide `uv lock --upgrade` or `bun update` sweeps. Upgrade dependencies only when needed or for a verified CVE affecting our execution path, allowing a cool-down window for registry malware scanners to catch compromised upstream releases.

---

## 3. Phased Fleet Sweep Plan

All execution phases MUST follow fleet safety rules:
- **Batch Size Limit**: Max 10 files modified per commit and per script invocation.
- **Batch Mutation Safety**: Create timestamped `.bak` files (`$filePath.$(Get-Date -Format 'yyyyMMdd_HHmmss').bak`) before mutating 3+ files.
- **Repo-by-Repo Verification**: Run each repo's lint/test/smoke gate (`uv run ruff check`, `just smoke`, or backend startup check) before moving to the next repo.
- **NSSM Restart Rule**: If a modified repo runs as an NSSM service, restart via `sc.exe stop <svc>` + `sc.exe start <svc>` and verify a new PID owns the port.

### Phase 0: Fix Standards & Templates First (DONE - `5532592c`)
Prevent agents from re-introducing `0.0.0.0` or wildcard CORS in new repos:
1. Updated `mcp-central-docs/standards/STARLETTE_NO_PYDANTIC_STANDARD.md` (`host="0.0.0.0"` -> `host="127.0.0.1"`) and added the canonical CORS snippet with explicit frontend port origins.
2. Updated `mcp-central-docs/standards/WEBAPP_SOTA_STANDARDS.md` and `mcp-central-docs/deployment/security.md` to mandate `127.0.0.1` binding and explicit CORS origins.

### Phase 1: Tier 1 & Tier 2 Actuator / Host-Control Repos (15 repos, repo-by-repo)
Highest priority - servers that can execute shell commands, control GUI/mouse/keyboard, manage VMs/containers, or actuate hardware:
1. **Batch 1A (Both `0.0.0.0` + Wildcard CORS, host control) - DONE (2026-11-18)**:
   - `opencode-cli-mcp` (`ebb77f9`)
   - `pywinauto-mcp` (`aa56b8b`, NSSM service `mcp-pywinauto-mcp` restarted via `sc.exe`, verified new PID on `127.0.0.1:10789`)
   - `system-admin-mcp` (`2601920`)
   - `rustdesk-mcp` (`d4a22be`)
   - `tailscale-mcp` (`427fa44`)
   - `robotics-mcp` (`79d83ff`, also fixed PowerShell `$Host` automatic variable collision in `scripts/start-normal.ps1`)
   - `virtualization-mcp` (`89a4053`)
2. **Batch 1B (Wildcard CORS on host/actuator servers) - PENDING**:
   `windows-operations-mcp`, `autohotkey-mcp`, `universal-actuator-mcp`
3. **Batch 1C (`0.0.0.0` bind on host/actuator/DB servers) - PENDING**:
   `devices-mcp`, `fleet-agent-mcp`, `uitars-mcp`, `podman-mcp`, `database-operations-mcp`
- **Verification per repo**: Confirm `127.0.0.1` in `netstat -ano | findstr :<port>`, verify preflight `OPTIONS` with `Origin: https://evil.example` is rejected, and verify the local webapp port is allowed.

### Phase 2: Remaining Intersection Repos (`0.0.0.0` + Wildcard CORS) (15 repos)
Sweep the remaining 15 repos from the 22-repo intersection list:
- **Batch 2A**: `advanced-memory-mcp` (note: NSSM service on 10705 - restart via `sc.exe`), `mcp-studio`, `monitoring-mcp`, `multi-backup-mcp`, `deepfang`, `myai`, `nest-protect-mcp`, `obs-mcp`
- **Batch 2B**: `plex-mcp`, `davinci-resolve-mcp`, `magentart-mcp`, `readly-mcp`, `suno-mcp`, `chitchat`, `ai-games-collection`

### Phase 3: Remaining Wildcard CORS (56 repos) & `0.0.0.0` Bindings (34 repos)
Sweep in groups of 5-8 repos per session (strictly <= 10 files per commit):
- Replace `allow_origins=["*"]` with port-scoped `ALLOWED_ORIGINS` read from each repo's `fleet-start.config.ps1` / `.env`.
- Replace `host="0.0.0.0"` in Python (`uvicorn.run`), Rust (`SocketAddr`), and `start.ps1` / `fleet-start.config.ps1` with `os.getenv("<REPO>_HOST", "127.0.0.1")`.

### Phase 4: Lockfile Closure & Orphan Cleanup (14 repos)
1. Generate and commit missing `uv.lock` in the 8 unlocked Python repos (`containercraft`, `dj-media-hub`, `doccraft`, `filecraft`, `fleet-tool-bridge`, `gitcraft`, `revecraft`, `rust-test-c`).
2. Generate and commit missing `bun.lock` in the 5 active frontend repos (`avatar-pipeline-mcp`, `demo-app`, `myvrworlds`, `suno-mcp`, `triton-mcp`).
3. Inspect and remove or archive the malformed BUG-039 directory `D:\Dev\repos\DDevrepossysinternals-mcpweb_sota`.

### Phase 5: Automated Regression Gate in `fleet-gate`
Add a check in `mcp-central-docs/fleet-gate/` that fails on:
- Un-gated `host="0.0.0.0"` or `--host 0.0.0.0` in `src/`, `backend/`, or `start.ps1`
- `allow_origins=["*"]` or `CorsLayer::permissive()` in `src/` or `backend/`
- Missing `uv.lock` when `pyproject.toml` is present, or missing `bun.lock` when `webapp/package.json` is present

---

## 4. Related Documents

- [2026-10-06-protocol-pivoting-mcp-ssrf.md](2026-10-06-protocol-pivoting-mcp-ssrf.md) - MCP SSRF + cross-agent trust gap
- [linux-vulns/AI_VULN_DISCOVERY_IMPLICATIONS.md](linux-vulns/AI_VULN_DISCOVERY_IMPLICATIONS.md) - AI-assisted 0-day discovery scaling and kernel/container posture
- [../standards/AGENT_ACTION_GATES.md](../standards/AGENT_ACTION_GATES.md) - Operator env gates and MCP elicitation for destructive/actuator tools
- [../deployment/security.md](../deployment/security.md) - MCP server security and VM isolation for reverse engineering
