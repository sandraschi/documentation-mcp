# MCP Documentation Infrastructure (MCD)

**Private Repository - Internal Documentation Hub**
**By FlowEngineer sandraschi**
**Last Updated:** 2026-03-08

Central documentation for all projects: MCP servers, myai, veogen, mywienerlinien, autohotkey, and more.

###  **CRITICAL: MCP server standards (canonical hub)**

**MCP servers should follow the standards documented here**  first-connection quality, FastMCP 3.1+, webapp ports, and packaging live in the modular docs (not one frozen December 2025 snapshot).

- **Start here:** **[AGENT_PROTOCOLS.md](standards/AGENT_PROTOCOLS.md)**  SOTA_REQUIREMENTS, DEPLOYMENT_STANDARDS, TOOL_DESIGN, WEBAPP_STANDARDS, etc.
- **First-time success (historical doc, STALE):** [MCP_SERVER_FIRST_TIME_SUCCESS_GUARANTEE.md](standards/MCP_SERVER_FIRST_TIME_SUCCESS_GUARANTEE.md)  ideas still valid; **do not treat code samples as current** without cross-checking FastMCP 3.1+.

---

## Documentation Dashboard (v1.22.0)

**Web UI and search**
- **Unified search**: Semantic retrieval across `docs`, `plex`, and `calibre` MCP nodes (with cover art where applicable).
- **Folder ingest**: Point the UI at local folders to add them to the LanceDB vector store.
- **Documents viewer**: Recursive tree and Markdown rendering for this repo.
- **Q&A**: RAG over ingested sources (LanceDB / BGE embeddings).
- **Verification matrix**: IDE/client compatibility notes.
- **Tools hub**: Tool listing and execution from the UI.
- **Ports**: Frontend **11032** (Vite); backend **11033** (Python/docs_mcp). Private mcp-central-docs uses **10794/10795**.
- **MaaS**: Docs MCP can be used as a shared service by other repos (semantic search, get_document, ask_docs, chunk_stats). See **[Docs MCP as MaaS](operations/DOCS_MCP_MAAS.md)** for endpoints and usage.

[Access Dashboard (Local)](http://localhost:11032)

### Just recipes (local dev)

Standardized Just recipes for local development. Run `just` for the industrial dashboard. Use `just stats` for a quantitative snapshot of the documentation and tools. Full list defined in [`justfile`](justfile).

Fleet repos vendor the same script at [`tools/repo_stats.py`](tools/repo_stats.py) (run via `just stats`).

---


## Architectural Reorganization (2025-12-30)

**This repository has been reorganized** to focus exclusively on **MCP (Model Context Protocol) documentation**. Non-MCP content has been moved to `not-mcp-related/` for archival purposes.

####  Semantic Search & RAG
MCD features a built-in LanceDB-powered RAG engine for intelligent documentation retrieval.
- **Vector Search**: Semantic retrieval using `bge-small-en-v1.5`.
- **Integrated Server**: The `docs_mcp` server provides standard tool access to the entire knowledge base.
- **Architecture**: See [docs_mcp ARCHITECTURE](src/docs_mcp/ARCHITECTURE.md) for technical details.

### Protocol Standards (Core)
- MCP protocol documentation and standards
- FastMCP library guides and  practices
- MCP server development resources
- MCP ecosystem tools and integrations

### Peripheral Documentation (Archived)
- General AI documentation  `not-mcp-related/general-ai/`
- AutoHotkey scripting  `not-mcp-related/autohotkey/`
- Development tools  `not-mcp-related/ecmascript/`, `not-mcp-related/git-github/`
- Windows tools  `not-mcp-related/windows-tools/`

**[View archived content ](not-mcp-related/)**

---

### Core standards (v12.0)
| Doc | Purpose |
|-----|---------|
| **[AGENT_PROTOCOLS.md](standards/AGENT_PROTOCOLS.md)** | Primary standards entry point |
| **[toolbench/](toolbench/README.md)** | ToolBench (Arcade) analysis + fleet alignment + per-server improvement notes |
| **[SOTA_REQUIREMENTS.md](standards/SOTA_REQUIREMENTS.md)** | Core Architecture & FastMCP 3.1 features |
| **[WEBAPP_STANDARDS.md](standards/WEBAPP_STANDARDS.md)** | UI/UX Blueprint & Port Allocation Hygiene |
| **[VERIFICATION_STANDARDS.md](standards/VERIFICATION_STANDARDS.md)** | Browser safety & log tail requirements |
| **[BUGS_DEPOT.md](troubleshooting/BUGS_DEPOT.md)** | Centralized Failure Registry (P0-P3) |
| **[VIBE_OPERATIONS.md](operations/VIBE_OPERATIONS.md)** |  Live Infrastructure Status |
| **[DEVELOPER_LINGO.md](operations/DEVELOPER_LINGO.md)** | Shared dev shorthand (e.g., smoke test) |
| **[EXTERNAL_AGENT_SECURITY_SCANNERS.md](operations/EXTERNAL_AGENT_SECURITY_SCANNERS.md)** | Fleet guidance for Cisco/NVIDIA scanner and runtime hardening stack |
| **[SCANNER_PATTERN_ANTIPATTERN_CRITERIA.md](operations/SCANNER_PATTERN_ANTIPATTERN_CRITERIA.md)** | Starter criteria to interpret scanner findings (patterns vs antipatterns) |
| **[SCANNER_ECOSYSTEM_ASSESSMENT_2026-03.md](operations/SCANNER_ECOSYSTEM_ASSESSMENT_2026-03.md)** | Market assessment + external scanner/assessor sites beyond ToolBench/Glama |
| **[DEV_SANDBOX_HARDENING_PROFILE.md](operations/DEV_SANDBOX_HARDENING_PROFILE.md)** | Optional stepwise dev sandbox hardening with rollback and lockout-avoidance guidance |
| **[HERE_NOW_STATIC_PUBLISHING.md](operations/HERE_NOW_STATIC_PUBLISHING.md)** | Optional **here.now** instant static URLs for agent-built pages (fleet overview, demos); static-only + claim-window caveats |
| **[STRUCTURE.md](STRUCTURE.md)** | This repo's directory layout |
| **[GITIGNORE_STANDARDS.md](standards/GITIGNORE_STANDARDS.md)** | **Never commit `node_modules/`, venvs, caches**; VCS recovery |

---

## Protocol Initialization

**New to MCP?** Start here!

```
getting-started/
 README.md                    # Core quick start guide
 what-is-mcp.md              # Understanding MCP
 choosing-transport.md        # Stdio vs HTTP vs SSE vs WebSocket
```

**Quick Links:**
- [Quick Start Guide](getting-started/README.md) - Baseline setup
- [Protocol Overview](getting-started/what-is-mcp.md) - Architectural fundamentals
- [Transport Selection](getting-started/choosing-transport.md) - Transport-specific data flows

---

## MCP Specification

**Learn the fundamentals**

```
protocol/
 README.md                    # Protocol documentation hub
 OVERVIEW.md                  # Protocol fundamentals
 TRANSPORTS.md               #  Stdio, HTTP, SSE, WebSocket
```

**Quick Links:**
- [Protocol Overview](protocol/OVERVIEW.md) - How MCP works
- [Transport Methods](protocol/TRANSPORTS.md) - Complete transport guide

---

## FastMCP Implementation (Python)

**Build MCP servers with Python.** **Current:** FastMCP 3.1. Use [3.1-platform-features.md](fastmcp/3.1-platform-features.md) for providers/transforms/CLI; [3.1-features.md](fastmcp/3.1-features.md) and [3.0-to-3.1-improvements.md](fastmcp/3.0-to-3.1-improvements.md) for prompts/skills/CodeMode and deltas; [migration-guide.md](fastmcp/migration-guide.md) for 2.x3.1. **In-chat rich UI (MCP Apps / Prefab):** [mcp-apps-prefab-ui.md](fastmcp/mcp-apps-prefab-ui.md).

```
fastmcp/
 README.md                    #  Complete FastMCP guide
 migration-guide.md           # Upgrade to 3.1+ (REQUIRED)
 3.1-platform-features.md    # Providers, transforms, CLI, 2.x breaks
 3.1-features.md              # Prompts, Skills, CodeMode
 tool-documentation.md        # Docstring standards
 mcp-apps-prefab-ui.md        # MCP Apps + Prefab UI (fleet standard)
 mcp-apps-prefab-use-cases-and-examples.md  # Examples, host UX, real vs demo
 persistent-storage.md        # State management
 advanced-patterns.md         # Advanced patterns
```

**Quick Links:**
- [FastMCP Guide](fastmcp/README.md) - Complete framework guide
- [3.1 Platform](fastmcp/3.1-platform-features.md) -  Providers, transforms, CLI, 2.x3.x
- [3.1 Features: Prompts & Skills](fastmcp/3.1-features.md) -  Prompts and Skills Provider (FastMCP 3.1+)
- [Migration Guide](fastmcp/migration-guide.md) -  Upgrade to 3.1+
- [MCP Apps & Prefab UI](fastmcp/mcp-apps-prefab-ui.md) - `ToolResult`, `prefab-ui`, in-chat cards (fleet)
- [Prefab use cases & examples](fastmcp/mcp-apps-prefab-use-cases-and-examples.md) - stats, fleet, health, side panel, interaction
- [3.1 Features](fastmcp/3.1-features.md) - Current features (Prompts, Skills, CodeMode)

---

## Infrastructure Deployment

**Deploy to production**

```
docs/deployment/
 README.md                    #  Deployment guide
 production-checklist.md      # Pre-deployment checklist
 security.md                  # Security hardening
 monitoring.md                # Monitoring setup
```

**Quick Links:**
- [Deployment Guide](deployment/README.md) - Complete deployment guide
- [Production Checklist](deployment/production-checklist.md) - Pre-flight checks
- [Security Guide](deployment/security.md) - Secure your server

---

## Containerization (Docker)

**Containerize your MCP servers**

```
docker/
 README.md                    # Docker documentation hub
 BUILD_OPTIMIZATION.md        #  18-90x faster builds
 MONITORING_STACK.md          # Grafana/Prometheus/Loki
 CONTAINERIZATION_GUIDE.md    # When/how to containerize
```

**Quick Links:**
- [Docker Guide](docker/README.md) - Complete Docker guide
- [Build Optimization](docker/BUILD_OPTIMIZATION.md) -  Fast builds
- [Monitoring Stack](docker/MONITORING_STACK.md) - Full observability

---

## Ecosystem Registry

**Tools, platforms, and services**

```
ecosystem/
 README.md                    # Ecosystem overview
 claude-desktop/              # Claude Desktop config
 glama/                       #  Glama registry
    REGISTRY_GUIDE.md        # Publishing guide
 mcpb/                        # MCPB packaging
```

**Quick Links:**
- [Ecosystem Overview](ecosystem/README.md) - MCP ecosystem
- [Claude Integration](ecosystem/claude/README.md) - Configuration
- [Cursor Integration](ecosystem/cursor/README.md) - Innovations & Rules
- [Antigravity Integration](ecosystem/antigravity/README.md) - Google's flagship agentic IDE
- [Zed Integration](ecosystem/zed/README.md) - FOSS agentic IDE
- [FOSS Extensions](ecosystem/foss-extensions/README.md) - Roo Code, Cline, Continue
- [Glama Registry](ecosystem/glama/REGISTRY_GUIDE.md) - Publish your server
- [MCPB Packaging](standards/MCPB_PACKAGING_STANDARDS.md) - Package your server

---

## Architecture Patterns

** practices and patterns**

```
patterns/
 README.md                    # Patterns overview
 MCP_ORPHAN_GUARD_PATTERN.md  #  Prevent zombie processes
 mcp-server-composition.md    # Server composition

patterns/                        # (root level patterns)
 PORTMANTEAU_CONCEPT.md       #  Reduce tool explosion
 MCP_PORTMANTEAU__PRACTICES.md
 TOOL_EXPLOSION_FIX.md
 AGENTIC_AESTHETIC_PROACTIVITY.md #  Autonomous visual debt resolution
```

**Quick Links:**
- [Orphan Guard Pattern](patterns/MCP_ORPHAN_GUARD_PATTERN.md) -  Prevent zombies
- [Portmanteau Pattern](patterns/PORTMANTEAU_CONCEPT.md) -  Consolidate tools
- [ Practices](patterns/MCP_PORTMANTEAU__PRACTICES.md) - Implementation guide

---

## Technical Debt & Failures

Centralized tracking of failures, race conditions, and architectural hardening.

```
troubleshooting/
 BUGS_DEPOT.md                #  Central Bug Registry (P0-P3)
 details/                     #  High-fidelity bug reports + log tails
 README.md                    # Troubleshooting guide
```

| Component | Status |
| :--- | :--- |
| **[Bugs Depot](troubleshooting/BUGS_DEPOT.md)** |  **P0-P3 Bug Registry** |
| **[Vibe Operations](operations/VIBE_OPERATIONS.md)** |  **Live Infrastructure Status** |
| [Bugfix Log](docs/bugfixing/BUGFIX_LOG.md) | Archive of historical fixes |

---

##  Bugfixing

**Fleet-wide bugs and fixes (must document every fix here)**

```
docs/bugfixing/
 README.md                    #  How to log fixes
 BUGFIX_LOG.md                # Chronological log of bugs and fixes
```

**Quick Links:**
- [Bugfixing README](docs/bugfixing/README.md) - Log every bug fix here
- [BUGFIX_LOG](docs/bugfixing/BUGFIX_LOG.md) - Full log of symptoms, causes, fixes, scope
- [Fleet rule: fix everywhere](docs/operations/FLEET_RULE_FIX_EVERYWHERE.md) - Apply same fix across all servers

---

##  Development Tools

**Tools for building MCP servers**

```
tools/
 README.md                    # Tools overview
 zoo-analyzer.md             # MCP Zoo analyzer

 APP_RESILIENCE.md           #  App resilience & crash recovery
 ecmascript/                 # JavaScript/TypeScript standards
 fastmcp/                    # Python FastMCP framework
```

**Quick Links:**
- [Tools Overview](tools/README.md) - Development tools
- [Zoo Analyzer](tools/zoo-analyzer.md) - Server quality analysis
- [Build Tools & MCP Clients](ecmascript/BUILD_TOOLS.md) - Client/server integration standards
- [App Resilience](safety/APP_RESILIENCE.md) -  Crash recovery & monitoring

---

##  Monitoring

**Observability and monitoring**

```
monitoring/
 README.md                    #  Monitoring overview
 QUICK_START.md              # 5-minute setup
 UNIFIED_MONITORING_STACK.md  # Full stack guide
 MCP_MONITORING_STANDARDS.md  # Standards
 configs/                     # Ready-to-use configs
     docker-compose.yml
     grafana/dashboards/
     prometheus/
     loki/
```

**Quick Links:**
- [Monitoring Overview](monitoring/README.md) - Complete monitoring guide
- [Quick Start](monitoring/QUICK_START.md) - 5-minute setup
- [Unified Stack](monitoring/UNIFIED_MONITORING_STACK.md) - Grafana/Prometheus/Loki

---

##  Apple ecosystem (2026)

**Hardware, OS, and Vibecoding**

```
apple/
 README.md                    #  Overview & Xcode 26.3 Revolution
 hardware/                    # Apple Silicon (M5/M6)
 ios/                         # iOS 19+ and Apple Intelligence
 macos/                       # macOS 16+ Productivity
 development/                 # Swift 7+, SwiftUI, Vibearchitecting
 publishing/                  # App Store 2.0
```

**Quick Links:**
- [Apple Overview](apple/README.md) - The Xcode 26.3 Revolution
- [Vibecoding Standards](apple/development/VIBECODING_STANDARDS.md) -conductor of intent
- [Hardware Roadmap](apple/hardware/README.md) - Silicon evolution

---

##  Languages (Tiered Documentation)

**Multilevel tiered knowledge for multi-language engineering**

```
languages/
 README.md                    #  Hub Entry Point
 python/                      # Docs, Learning, Reference
 rust/                        # Docs, Learning, Reference
 go/                          # Docs, Learning, Reference
 csharp/                      # Docs, Learning, Reference
 cpp/                         # Docs, Learning, Reference
 lisp/                        # Docs, Learning, Reference
 ahk/                         # Docs, Learning, Reference
```

**Quick Links:**
- [Language Hub](languages/README.md) - Structure and standards
- [Python Mastery](languages/python/) - From scripting to async
- [Rust Systems](languages/rust/) - Memory safety and speed
- [AHK Automation](languages/ahk/) - Windows productivity

---

##  AI Protoconsciousness

**The Vanguard of Embodied Intelligence**

```
protoconsciousness/
 README.md                    #  Overview: The materialist framework
 01_FOUNDATIONS.md            # Theory of digital sentience
 02_CONTINUOUS_PERCEPTION.md  # The "Heartbeat" streaming paradigm
 03_PROACTIVE_EMBODIMENT.md   # Anticipatory agents & World Models
 04_META_COGNITION_AND_EVALUATION.md # Internal states & Sage evaluation
```

**Quick Links:**
- [AI Protoconsciousness Hub](protoconsciousness/README.md) - Complete theoretical framework
- [The Heartbeat Paradigm](protoconsciousness/02_CONTINUOUS_PERCEPTION.md) - Decoupling perception from reasoning
- [Anticipatory Intelligence](protoconsciousness/03_PROACTIVE_EMBODIMENT.md) - Moving beyond reactive QA

---

##  Google Ecosystem (Archived)

**Google AI stack (Consult `not-mcp-related/`)**

```
not-mcp-related/google-ecosystem/
 README.md                    # Ecosystem overview
 gemini/                      # Gemini 3
 antigravity/                 #  DATA SAFETY RISK - AI-powered IDE
 nano-banana-pro/             # Image generation
 deepmind/                    # DeepMind projects
 infrastructure/              # TPU vs Nvidia
```

**Quick Links:**
- [Google Ecosystem](not-mcp-related/google-ecosystem/README.md) - Complete overview
- [Gemini 3](not-mcp-related/google-ecosystem/gemini/) - Gemini notes
- [ Antigravity IDE](not-mcp-related/google-ecosystem/antigravity/) - **DATA DESTRUCTION RISK**

---

##  General AI Landscape (Archived)

**The complete state of AI (Consult `not-mcp-related/`)**

```
not-mcp-related/general-ai/
 README.md                    # AI landscape overview
 models/                      # Model comparison notes
 hardware/                    # Chip wars
 regions/                     # US-China race
 history/                     # Timeline
```

**Quick Links:**
- [AI Landscape](not-mcp-related/general-ai/README.md) - Complete overview
- [Model comparison](not-mcp-related/general-ai/models/sota-comparison.md)
- [Chip Wars](not-mcp-related/general-ai/hardware/chip-wars.md) - Hardware competition

---

##  Git & GitHub

**Git, GitHub, CI/CD**

```
git-github/
 README.md                    # Git/GitHub hub
 git/                         # Git fundamentals
 github/                      #  16 comprehensive guides
 ci-cd/                       # CI/CD  practices
 troubleshooting/             # Common issues
```

**Quick Links:**
- [Git/GitHub Hub](git-github/README.md) - Complete guide
- [GitHub CLI vs MCP](git-github/github/GITHUB_CLI_VS_MCP.md) - 50-70% token reduction
- [CI Success Guide](git-github/github/CI_SUCCESS_WORKFLOW_GUIDE.md) - Never break CI

---

##  Robotics

**Complete robotics ecosystem: MCP server + webapp + MCP zoo integration**

```
robotics/
 README.md                    #  Start here
 yahboom/                     #  **Yahboom SOTA (Raspbot, M1, etc.)**
    YAHBOOM_ROBOTICS_ECOSYSTEM.md
 ros/                         # ROS2 Fundamentals & Patterns
    ROS_FUNDAMENTALS.md
    ROS_MCP_INTEGRATION.md
 scout/                       # Moorebot Scout Integration
    MOOREBOT_SCOUT.md
 vrobs-vrealm/                # Virtual Robotics & VRChat
    VIRTUAL_ROBOTICS_APPROACH.md
 UNITREE_ROBOTS.md            # Quadruped/humanoid
```

**Quick Links:**
- **[Robotics Ecosystem](robotics/yahboom/YAHBOOM_ROBOTICS_ECOSYSTEM.md)** -  **Complete guide: robotics-mcp + robotics-webapp**
- **[Workflow System Plan](robotics/WORKFLOW_SYSTEM_PLAN.md)** -  **IMPLEMENTED: Preprogrammed workflow system**
- [Robotics Overview](robotics/README.md) - Complete guide
- [Moorebot Scout](robotics/scout/MOOREBOT_SCOUT.md) - Complete MCP integration
- [Virtual Robotics](robotics/vrobs-vrealm/VIRTUAL_ROBOTICS_APPROACH.md) - Test virtually first

**Ecosystem Components:**
- **robotics-mcp** - Core robot control MCP server (port 8888)
- **robotics-webapp** - Full-stack React + FastAPI web application
  -  **Workflow System** - Preprogrammed flows for complex multi-step operations
- **7+ MCP Servers** - Unity3D, VRChat, Avatar, OSC, Resonite, VRoid, Local LLM

---

##  Projects

**Project-specific documentation**

```
projects/
 README.md                    # Project index
 vienna-life-assistant/       #  Personal Life Management with MCP + Celery
 vienna-live-mcp/             #  Vienna Life Assistant MCP Server (63 tools)
 myai/                        # AI microservices platform
 veogen/                      # AI video generator
 mywienerlinien/              # Vienna transit
 plexmcp/                     #  Plex Media Server MCP
 robotics-mcp/                #  Unified Robotics Control (Physical + Virtual)
 autohotkey/                  # AutoHotkey v2
 ... (more projects)
```

**Quick Links:**
- [Projects Index](projects/README.md) - All projects
- [Vienna Life Assistant](projects/vienna-life-assistant/STATUS.md) -  Personal management with MCP + Celery
- [Vienna Live MCP](projects/vienna-live-mcp/STATUS.md) -  60+ tools, 5 portmanteaus, programmable life management
- [myai](projects/myai/STATUS.md) - Port 3060, 11 MCP tools
- [veogen](projects/veogen/STATUS.md) - Ports 4700-4745
- [Plex MCP](projects/plexmcp/STATUS.md) - 15 tools, 100+ operations
- [Robotics MCP](projects/robotics-mcp/STATUS.md) - 11 tools, physical + virtual robots

---

##  AutoHotkey

**Extensive AutoHotkey v2 documentation**

```
autohotkey/
 AUTO_HOTKEY_V2_CHEAT_SHEET.md        # Quick reference
 Complete_V1_to_V2_Migration_Guide.md # Full migration
 AutoHotkey_v2_Syntax_Reference.md    # Syntax reference
 ... (30+ files)
```

**Quick Links:**
- [AutoHotkey Cheat Sheet](autohotkey/AUTO_HOTKEY_V2_CHEAT_SHEET.md)
- [V1 to V2 Migration](autohotkey/Complete_V1_to_V2_Migration_Guide.md)

---

## Quality & Stability Critical Review

The current state of AI engineering tools presents significant operational risks:
- **Cursor IDE**: High update frequency with unvetted regressions.
- **Antigravity IDE**: Documented data safety issues and opaque runtime integrations.
- **Windsurf IDE**: Unstable repository management practices.
- **Societal Impact**: Perception asymmetry fuels disproportionate responses to technical failures.
- **Standards Drift**: Widespread abandonment of formal changelogs and communication protocols.
- [AI IDE Destruction Pattern](development/AI_IDE_DESTRUCTION_PATTERN.md) - Three-strikes analysis of AI IDE failures
- [AI Safety Guardrails Analysis](development/AI_SAFETY_GUARDRAILS.md) - Why guardrails fail in practice
- [Prompt Engineering Safety](development/PROMPT_ENGINEERING_SAFETY.md) - Destructive prompt dangers
- [Universal Perception Asymmetry](development/UNIVERSAL_PERCEPTION_ASYMMETRY.md) - Why success = silence, failure = amplification (affects ALL complex systems)
- [Social Toxicity Analysis](development/SOCIAL_TOXICITY_RAGEBAIT.md) - How perception asymmetry fuels hatred and extremism
- [Cursor Quality Analysis](../mcp-studio/docs/development/CURSOR_UPDATE_QUALITY_CONCERNS.md)
- [IDE Transparency Standards](../mcp-studio/docs/development/IDE_TRANSPARENCY_STANDARDS.md)
- [Antigravity Data Safety Analysis](not-mcp-related/google-ecosystem/antigravity/CHANGELOG_ANALYSIS.md)

---

##  Claude Skills

**Claude Skills collection**

```
claude-skills/
 README.md                    # Overview
 INSTALLATION_GUIDE.md        # How to install
 official/                    # Anthropic official skills
 community/                   # Community skills
 daft/                        # Daft skills pack
```

**Quick Links:**
- [Claude Skills](claude-skills/README.md) - Overview
- [Installation Guide](claude-skills/INSTALLATION_GUIDE.md) - Setup guide

---

##  Tailscale

**Tailscale VPN documentation**

```
tailscale/
 README.md                    # Overview
 MCP_INTEGRATION.md           # MCP + Tailscale
 INTEGRATION_GUIDE.md         # Setup guide
```

**Quick Links:**
- [Tailscale Overview](tailscale/README.md)
- [MCP Integration](tailscale/MCP_INTEGRATION.md)

---

##  Templates

**Reusable templates and scripts**

```
templates/
 README_TEMPLATE.md           # Project README template
 ARCHITECTURE_TEMPLATE.md     # Architecture docs template
 PORTMANTEAU_TEMPLATE.md      # Portmanteau tool template
 mcp_orphan_guard.py          #  Zombie process guard
 ci.yml.template              # GitHub Actions template
 scripts/                     #  DEPRECATED - Use sota-scripts/
     new-mcp-server.ps1       #  MOVED to sota-scripts/mcp-server-builder/
     new-mcp-server-intelligent.ps1 #  MOVED to sota-scripts/intelligent-builder/
     new-fullstack-app.ps1    #  MOVED to sota-scripts/fullstack-builder/
     check-repo-standards.ps1 #  MOVED to sota-scripts/repo-standards/
     backup-repo.ps1          #  MOVED to sota-scripts/backup-system/

sota-scripts/                    #  NEW CANONICAL script location
 backup-system/               # Repository backup tools
 mcp-server-builder/          # MCP server generators
 intelligent-builder/         # AI-powered builders
 fullstack-builder/           # Fullstack app builders
 repo-standards/              # Quality assurance
 propagation-tools/           # Deployment automation
```

**Quick Links:**
- [Templates Overview](templates/) - All templates
- [Orphan Guard Script](templates/mcp_orphan_guard.py) -  Prevent zombies
- [MCP Scanner Workflow Template](templates/github-actions/mcp-scanner.yml.template) - Reusable GitHub Actions baseline
- [Skill Scanner Workflow Template](templates/github-actions/skill-scanner.yml.template) - Reusable GitHub Actions baseline
- [SOTA Scripts](sota-scripts/) -  New script location
- [New MCP Server Script](sota-scripts/mcp-server-builder/new-mcp-server-enhanced.ps1) -  Enhanced server generator

---

### `archive/`
Superseded docs (e.g., legacy FastMCP 2.x migration). **Current:** FastMCP 3.1.

---

##  Quick Start Paths

### New MCP Server?
1. Read [docs/getting-started/README.md](getting-started/README.md) - 5-minute quick start
2. Choose transport: [docs/getting-started/choosing-transport.md](getting-started/choosing-transport.md)
3. Follow [docs/fastmcp/migration-guide.md](fastmcp/migration-guide.md) - Use FastMCP 3.1+
4. Use patterns from [docs/patterns/](patterns/)
5. Repo bar: [PACKAGING_STANDARDS.md](standards/PACKAGING_STANDARDS.md) 5 (**uv**, **justfile**, **`llms.txt` + `llms-full.txt`**, **glama.json**, **`mcpb pack`**)  [integrations/llms-txt-manifest.md](integrations/llms-txt-manifest.md)
6. MCPB manifest + assets: [MCPB_PACKAGING_STANDARDS.md](standards/MCPB_PACKAGING_STANDARDS.md)
7. Publish / discovery: [Glama](ecosystem/glama/) (`glama.json`)

### Docker & Containerization?
1. Start with [docs/docker/README.md](docker/README.md)
2. Read [docs/docker/BUILD_OPTIMIZATION.md](docker/BUILD_OPTIMIZATION.md) - Fast builds
3. See [docs/docker/CONTAINERIZATION_GUIDE.md](docker/CONTAINERIZATION_GUIDE.md)

### Adding Monitoring?
1. Start with [monitoring/QUICK_START.md](monitoring/QUICK_START.md) - 5-minute setup
2. See [docs/docker/MONITORING_STACK.md](docker/MONITORING_STACK.md)
3. Copy configs from `monitoring/configs/`

### Working on Projects?
1. Check `docs/projects/{project}/STATUS.md`
2. Follow project-specific standards

---

##  Standards Summary

| Standard | Document |
|----------|----------|
| Documentation Quality | [standards/STANDARDS.md](standards/STANDARDS.md) |
| FastMCP 3.1+ | [docs/fastmcp/migration-guide.md](fastmcp/migration-guide.md) |
| MCPB Packaging | [standards/MCPB_PACKAGING_STANDARDS.md](standards/MCPB_PACKAGING_STANDARDS.md) |
| Repo build bar (uv, justfile, llms.txt + llms-full.txt, glama, `mcpb pack`) | [standards/PACKAGING_STANDARDS.md](standards/PACKAGING_STANDARDS.md) 5  [integrations/llms-txt-manifest.md](integrations/llms-txt-manifest.md) |
| Portmanteau Pattern | [patterns/PORTMANTEAU_CONCEPT.md](patterns/PORTMANTEAU_CONCEPT.md) |
| Orphan Guard | [docs/patterns/MCP_ORPHAN_GUARD_PATTERN.md](patterns/MCP_ORPHAN_GUARD_PATTERN.md) |
| Docker Builds | [docs/docker/BUILD_OPTIMIZATION.md](docker/BUILD_OPTIMIZATION.md) |
| Monitoring | [monitoring/MCP_MONITORING_STANDARDS.md](monitoring/MCP_MONITORING_STANDARDS.md) |
| Justfile SOTA | [standards/JUSTFILE_STANDARDS.md](standards/JUSTFILE_STANDARDS.md)  [integrations/justfile.md](integrations/justfile.md) |

---

##  Navigation Tips

### Finding Documentation

**"I want to..."**

- **Learn MCP**  [docs/getting-started/](getting-started/)
- **Build with FastMCP**  [docs/fastmcp/](fastmcp/)
- **Deploy to production**  [docs/deployment/](deployment/)
- **Fix an issue**  [docs/troubleshooting/](troubleshooting/)
- **Use Docker**  [docs/docker/](docker/)
- **Add monitoring**  [monitoring/](monitoring/)
- **Learn patterns**  [docs/patterns/](patterns/) + [patterns/](patterns/)

### Cross-References

Use [docs/CROSS_REFERENCE_INDEX.md](docs/CROSS_REFERENCE_INDEX.md) to find topics across all documentation.

---

**Private Repository** - Not for public distribution  
**Owner:** Sandra Schipal  
**Last Major Reorganization:** 2026-02-13


##  Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

###  Quick Start
Run immediately via `uvx`:
```bash
uvx mcp-central-docs
```

###  Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "mcp-central-docs": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/mcp-central-docs", "run", "mcp-central-docs"]
  }
}
```
