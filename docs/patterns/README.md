# MCP Development Patterns

**Reusable patterns and best practices for MCP server development**

---

## ðŸ“š Patterns

### **LLM manifest: `llms.txt` + `llms-full.txt`** NEW

ðŸ“„ [LLMS_TXT_FLEET_MANIFEST.md](LLMS_TXT_FLEET_MANIFEST.md)

**Required two-file bar** at repo root for fleet MCP servers: tight **index** + **full** corpus for scrapers and IDEs. Links to [integrations/llms-txt-manifest.md](../integrations/llms-txt-manifest.md) and [DOCUMENTATION_STANDARDS.md](../standards/DOCUMENTATION_STANDARDS.md).

---

### **GitHub maintainer heartbeat (fleet PRs / issues)** NEW

[GITHUB_MAINTAINER_HEARTBEAT.md](GITHUB_MAINTAINER_HEARTBEAT.md)

**Daily or weekly** `github_ops(pr_list)` / `issue_list` across a **repo fleet**; supervisor (**robofang**, OpenManus, OpenClaw, …) owns the **schedule**; **[git-github-mcp](https://github.com/sandraschi/git-github-mcp)** web **`/inbox`** is the human mirror. Reduces “ignored PR” failure mode for small repos.

---

### **Fleet computer use (OpenManus + pywinauto)** NEW

ðŸ“„ [FLEET_COMPUTER_USE_MCP.md](FLEET_COMPUTER_USE_MCP.md)

**Replicate vendor â€œMy Computerâ€â€“style desktop agents using the MCP fleet** â€” OpenManus (local LLM) + **windows-computer-use-mcp** as the primary Windows UI finger, plus OCR/OS tools. Explicit **danger profile** and mitigations (VM, allowlists, human gates, sampling risks). **Caution:** **openmanus-mcp** + **OpenClaw / Manus-class** + pywinauto = **multiplicative** risk â€” see **[PYWINAUTO_MCP_SAFETY.md](PYWINAUTO_MCP_SAFETY.md)** Â§ *OpenManusâ€¦*.

ðŸ“„ **[PYWINAUTO_MCP_SAFETY.md](PYWINAUTO_MCP_SAFETY.md)** â€” HITL vs env kill switch / rate / dry-run; **FastMCP 3.1 sampling** amplification; server-farm checklist; vendor comparison (honest non-parity). **Sandboxed execution:** guest-side pywinauto + **virtualization-mcp** (Windows Sandbox / assets) â€” not host driving the Sandbox window.

---

### **Intel Reports Hub (fleet-wide HTML reports)** NEW

[intel-reports-hub.md](intel-reports-hub.md) — shared HTML reports on port **11027**; Fritz + AIWatcher wired; iPad via Tailscale.

---

### **MCP client config snippets** NEW

ðŸ“„ [MCP_CLIENT_CONFIG_SNIPPETS.md](MCP_CLIENT_CONFIG_SNIPPETS.md)

**JSON snippets and standard locations for adding MCP servers to IDE/client configs.**

Perfect for:
- Clone-based (no PyPI) MCP server distribution
- Documenting Cursor, Claude Desktop, Windsurf, Zed, Antigravity, LM Studio config paths
- UI or scripts that insert a server entry (idempotent, with backup)

**Key features:**
- Generic snippet template (PYTHONPATH, no cwd)
- Client config locations table (Windows: APPDATA, USERPROFILE)
- Snippet files in repos (`snippets/`), insert automation (backup, idempotent)

**Reference:** [clawd-mcp/snippets](https://github.com/sandraschi/clawd-mcp/tree/main/snippets), [mcp_config_insert.py](https://github.com/sandraschi/clawd-mcp/blob/main/webapp_api/mcp_config_insert.py)

---

### **FastMCP 3.1.1+.1 Server Composition Pattern** â­â­ NEW

ðŸ“„ [mcp-server-composition.md](mcp-server-composition.md)

**Compose multiple MCP servers into unified orchestrators**

Perfect for:
- Combining related MCP servers into domain pipelines
- Cross-server workflows (e.g., VR production, smart home)
- Reducing tool fragmentation for clients
- Adding shared middleware (auth, logging)

**6 Orchestrator Architectures:**
| Orchestrator | Servers | Purpose |
|--------------|---------|---------|
| vr-production-mcp | 6 | VTuber/avatar pipeline |
| smart-home-mcp | 4 | Home automation |
| knowledge-mcp | 6 | Universal PKM |
| sysadmin-mcp | 8 | DevOps/system admin |
| media-production-mcp | 6 | Video/audio production |
| music-mcp | 4 | Music/DJ suite |

**Key Features:**
- âœ… `mount()` with `as_proxy=True` for live linking
- âœ… Cross-server workflows via `Client` API
- âœ… Hierarchical middleware (auth flows down)
- âœ… Tag-based tool filtering

---

### **Agent-to-Agent Handoff Pattern (SOTA 2025)** â­â­â­ NEW

ðŸ“„ [AGENT_TO_AGENT_HANDOFF.md](AGENT_TO_AGENT_HANDOFF.md)
ðŸ“„ [MULTI_SERVER_ORCHESTRATION.md](MULTI_SERVER_ORCHESTRATION.md)

**Behavioral delegation between autonomous agents with context transfer.**

Perfect for:
- Multi-agent systems with specialized personas
- Handling complex tasks across domain boundaries (e.g., Generalist â†’ Robotics)
- Large-scale agentic workflows requiring granular tool access

**Key Features:**
- âœ… **Behavioral vs Structural Differentiation**
- âœ… **4-Phase Handoff Protocol** (Decision, Serialization, Identity, Resume)
- âœ… **Identity Proxy Pattern** for secure claim propagation
- âœ… **Pydantic-AI** integration standards
- âœ… **HITL (Human-in-the-loop)** approval flows

---

### **FastMCP 3.1.1+ Persistent Storage Pattern** â­

ðŸ“„ [persistent-storage.md](../fastmcp/persistent-storage.md) (FastMCP 3.1)

**Implement cross-session persistence in MCP servers**

Perfect for:
- Database operations MCP servers
- Library management servers
- Configuration persistence
- User preferences
- Search history
- Reading progress
- Stateful MCP servers

**Key Benefits:**
- âœ… Persists across Claude Desktop restarts
- âœ… Persists across Windows/OS reboots
- âœ… Platform-aware storage (Windows/macOS/Linux)
- âœ… Simple key-value interface
- âœ… Production-ready pattern

**Reference Implementation:**
- CalibreMCP: `src/calibre_mcp/storage/persistence.py`

---

### **Modular MCP Repository Pattern** ⭐ NEW

📄 [MODULAR_MCP_REPOSITORY_PATTERN.md](MODULAR_MCP_REPOSITORY_PATTERN.md)

**Domain-Specific Isolation for Heavy Actuators (Telephony, Robotics, HW Drivers)**

Perfect for:
- Isolation of security-sensitive operations (Telephony, Root Admin)
- Large SDKs/binaries that bloat orchestrator core
- Reusable "clean bridges" across multiple fleet agents

**Key Features:**
- ✅ **Dependency Hygiene**: Zero-leak architecture
- ✅ **Security Boundaries**: Isolated process/permission space
- ✅ **FastMCP Proxying**: Seamless tools-through-hub integration
- ✅ **Scale-Ready**: Independent deployment and versioning

---

### **Docker Hot-Reload Development Pattern** ðŸš€ NEW

ðŸ“„ [docker-development.md](docker-development.md)

**Stop wasting 8+ hours per project on Docker rebuilds**

Perfect for:
- Fast iteration on Dockerized applications
- Full-stack development with hot-reload
- Native Python development with Docker DB
- Team consistency without slow rebuilds

**Key Features:**
- âœ… Volume mounts + `--reload` = 1 second code updates
- âœ… Native development option (5 second startup)
- âœ… BuildKit cache mounts for faster rebuilds
- âœ… Multi-stage builds for dev/prod separation
- âœ… Only rebuild when dependencies change
- âš ï¸ **NEVER use `--no-cache` for code changes!** (wastes 15 min downloading internet)

**Time Savings:**
- Old: 100 changes Ã— 5 min = 8.3 hours wasted
- New: 100 changes Ã— 1 sec = 1.7 minutes
- **Saves 8+ hours per project!**

**Patterns Covered:**
1. Volume Mounts + Hot-Reload (Docker)
2. Native Development (fastest)
3. BuildKit Cache Mounts
4. Dev/Prod Compose Separation
5. .dockerignore Best Practices

---

## ðŸŽ¯ Usage

These patterns are **SOTA (State Of The Art)** and should be copied to individual MCP server repos when implementing the pattern.

1. Read the pattern guide
2. Copy relevant code sections to your MCP server
3. Adapt for your specific use case
4. Test persistence across restarts

### **Turborepo MCP Monorepo Pattern** ðŸš€ NEW

ðŸ“„ [TURBOREPO_MCP_MONOREPO_PATTERN.md](TURBOREPO_MCP_MONOREPO_PATTERN.md)

**Monorepo build orchestration for MCP + web + agent projects**

Perfect for:
- MCP server + Next.js/React frontend in one repo
- Shared packages (UI, config, types)
- Fast incremental builds with caching
- Parallel task execution (build, lint, test, dev)

**Key Features:**
- Dependency-aware task pipeline (`^build`)
- Output caching (Next.js, dist/)
- Workspace layout: apps/*, packages/*
- MCP server as a package
- Python agents via custom tasks or Docker

**Reference Implementation:**
- myconf: LiveKit conferencing with MCP, web app, Python agent

---

### **Webapp Integration Pattern** ðŸš€ NEW

ðŸ“„ [webapp-integration-pattern.md](webapp-integration-pattern.md)

**Integrate MCP servers with web frontends (React, Vue, etc.)**

Perfect for:
- Building web UIs for MCP tools
- Multi-server web applications
- Real-time status monitoring
- Mock data fallback patterns

**Key Features:**
- âœ… Three-layer architecture (Frontend â†’ Backend â†’ MCP Servers)
- âœ… Health checking and status indicators
- âœ… Graceful fallback to mock data
- âœ… Type-safe service layers
- âœ… Multi-server support

**Reference Implementation:**
- robotics-webapp: Full React + FastAPI integration with 7+ MCP servers

---

### **Webapp Tests Page Pattern** ðŸ§ª NEW

ðŸ“„ [WEBAPP_TESTS_PAGE_PATTERN.md](WEBAPP_TESTS_PAGE_PATTERN.md)

**Run the project test suite from the webapp UI (pytest, npm test, etc.)**

Perfect for:
- Local dev and demos: run tests from the browser
- Consistent "run tests and see results" across SOTA webapps
- Dev/local-first apps with a guarded endpoint

**Key Features:**
- Backend: `POST /tests/run` guarded by `ENABLE_WEBAPP_TESTS=1`; subprocess + timeout
- Frontend: Tests page with Run button, target input, stdout/stderr (optionally structured report)
- Optional pattern: document once, adopt per-repo; never enable in production

**Reference Implementation:**
- advanced-memory-mcp: `tests_router.py`, `Tests.tsx`, webapp README; MemOps note in `docs/notes/webapp-tests-page-pattern.md`

---

### **AI/LLM Integration Pattern** ðŸ¤– NEW

ðŸ“„ [ai-llm-integration-pattern.md](ai-llm-integration-pattern.md)

**Integrate AI/LLM capabilities using local-llm-mcp**

Perfect for:
- Chatbot interfaces
- Model management UIs
- Multi-provider LLM support
- Personality systems

**Key Features:**
- âœ… Multi-provider support (Ollama, LM Studio, OpenAI, Anthropic, Google)
- âœ… Model management (list, load, unload, pull)
- âœ… Personality system
- âœ… Chat completion interface
- âœ… Settings management

**Reference Implementation:**
- robotics-webapp: Complete AI/LLM management with chatbot interface

---

### **Agent Demo Verification Pattern (Showboat + Rodney)** â­â­ NEW

ðŸ“„ [AGENT_DEMO_VERIFICATION_PATTERN.md](AGENT_DEMO_VERIFICATION_PATTERN.md)

**Prove agent-built code actually works -- with artifacts, not trust.**

Perfect for:
- Verifying MCP tool outputs after agent changes
- Capturing webapp screenshots as proof of correct rendering
- Standardizing red/green TDD as agent session opener
- Building living documentation from real command output

**Key Features:**
- âœ… Showboat: Agents build Markdown demos with real `exec` output
- âœ… Rodney: CLI browser automation for web UI verification + screenshots
- âœ… Anti-cheat: `showboat verify` re-runs commands and diffs against recorded output
- âœ… Prompt templates for CLI-only, webapp, and TDD session workflows
- âœ… `demos/` directory convention for committed verification artifacts

**Install:** `uv tool install showboat rodney`

**Source:** [Simon Willison, 2026-02-10](https://simonwillison.net/2026/Feb/10/showboat-and-rodney/)

---

## Antipatterns (Must Fix)

**Related (proactive checklist):** [TOOL_DESIGN_STANDARDS.md Â§4â€“Â§9](../standards/TOOL_DESIGN_STANDARDS.md) â€” agent-facing quality (pagination, `ToolAnnotations`, destructive-op guards, optional `output_schema`). Complements the â€œfix whatâ€™s brokenâ€ items below.

### **Dialogic Tool Fluff** â€“ AUDIT REQUIRED

[ANTIPATTERN_DIALOGIC_TOOL_FLUFF.md](ANTIPATTERN_DIALOGIC_TOOL_FLUFF.md)

**Vague, reassuring error messages that obscure the actual failure.**

Wrong: "Something unexpected happened. Don't worry, let's try again."
Correct: Surface the real error and recovery options.

Use the audit checklist to find and fix across all MCP server repos.

---

**Last Updated**: 2026-02-11


