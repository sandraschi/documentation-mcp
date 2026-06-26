# Meta MCP Changelog

All notable changes to Meta MCP will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Canonical changelog:** `D:/Dev/repos/meta_mcp/CHANGELOG.md`

## [Unreleased] - 2026-06-06

### Added
- **Fleet cold-start probe — Broken\* mode:** UI button **Broken\* (N)** re-runs only repos that failed in the last report. API `broken_only: true` on `POST /api/v1/fleet/startup-probe/run`. Service passes `-BrokenOnly` to `fleet-webapp-start-probe.ps1`.

### Fixed
- **FleetStartupProbe.tsx:** `runProbe` modes (`single` | `full` | `broken`); broken count from last complete report.

## [Unreleased] - 2026-05-31

### Added
- **`repo_inspiration` suite** — `inspire_repo_structure`, `inspire_repo_files`, `inspire_repo_patterns` (Python port of [Repomuse](https://www.npmjs.com/package/repomuse), MIT, praveene3127). Fleet doc: [integrations/repo-inspiration.md](../../integrations/repo-inspiration.md).

## [3.4.0] - 2026-02-21 - Toolchains & Presets ðŸ”—

### ðŸš€ Major Feature Expansion
**MetaMCP Enterprise** now features **Toolchain Manager**, a way to curate collections of MCP servers and rapidly hot-swap them into your preferred IDE clients.

### Added
- **ðŸ”— Toolchain Presets**: Create, read, update, and delete curated groups of MCP servers.
- **âš¡ Rapid Deployment**: Apply an entire preset to Cursor, Windsurf, Zed, or Claude Desktop with one click.
- **ðŸŒ Toolchain Dashboard**: A premium UI page in the webapp (`Toolchains.tsx`) to manage your configurations visually.

## [3.2.1] - 2026-02-04 - Stability & Client Detection Fixes ðŸ”§

### Fixed
- **ðŸš€ Discovery Service**: Removed incorrect `await` keywords on synchronous functions (`discover_clients`, `check_client_integration`), resolving a `TypeError` on the Server Repos page.
- **ðŸ” Tools UI**: Increased `z-index` of the search bar container to prevent it from being hidden behind tool cards.

### Added
- **ðŸ–¥ï¸ Client Discovery**: Expanded detection paths for **Zed** (Scoop shims) and **Antigravity** (User-specific AppData).
- **âš™ï¸ Client Configuration**: Implemented functional "Configure" and "View JSON" buttons on the Clients page with a new JSON editor modal.

### Changed
## [3.3.0] - 2026-02-06 - Dynamic Tools & Inspection ðŸ§ 
### ðŸš€ Major Feature Expansion
**MetaMCP Enterprise** now features **intelligent tool execution** and **deep server inspection** capabilities.

### Added
- **ðŸ“ Tool Execution Dynamic Form**: Values are no longer just raw JSON strings.
    -   **Smart Inputs**: `string`, `boolean`, `enum`, and `array` types are now rendered as proper form fields.
    -   **Mode Toggle**: Logic to switch between "Form View" (user friendly) and "JSON View" (power user).
    -   **Schema-Driven**: Form fields are generated in real-time based on the tool's JSON schema.
- **ðŸ” Server Drill-Down**: Deep inspection of active MCP servers.
    -   **Tool List**: View all available tools for a connected server.
    -   **Resource List**: View exposed resources (where supported).
    -   **Prompt List**: View available prompts (where supported).

### Changed
- **ðŸ˜ Renaming**: Globally renamed "Server Zoo" to **"Server Repos"** for improved clarity and semantic alignment.

## [3.2.0] - 2026-02-04 - Premium Webapp & Backend Integration ðŸ’Ž

### ðŸš€ Major Feature Expansion

**MetaMCP Enterprise** now features a **fully integrated, premium web interface** with real-time backend communication, replacing the previous static/mock implementations.

#### Added
- **ðŸ’Ž Premium Dark Theme**: Complete UI overhaul with glassmorphism, smooth transitions, and a refined color palette (`bg-slate-950`).
- **ðŸ—ï¸ Modular Architecture**:
  - **Layout Engine**: Retractable Sidebar, persistent Topbar with emergency stops, and responsive main content area.
  - **Interactive Modals**: Global Logger console (Ctrl+`) and Help dialogs (?).
  - **Atomic Components**: Reusable UI elements for consistency across the application.
- **ðŸ”Œ Backend Integration**:
  - **Live Tool Execution**: Frontend now communicates directly with the Python backend via `executeTool`.
  - **Real-time Status**: Dashboard reflects actual server and tool states.
- **ðŸ§ª Testing Scaffold**:
  - **Vitest + RTL**: Comprehensive testing setup for React components.
  - **CI Integration**: `npm test` script for automated verification.

#### Changed
- **Webapp Core**: Migrated from monolithic `App.tsx` to a structured, scalable directory format (`components/`, `pages/`, `hooks/`, `context/`).
- **Dashboard**: Enhanced visualization of system health and active services.
- **Repository Analysis**: Improved UI for deep codebase inspection.
- **Client Management**: Refined interface for managing IDE configurations.

## [3.1.1] - 2026-02-04 - Protocol Stability Fix ðŸ”§

### Fixed
- **ðŸš¨ Protocol Corruption**: Configured `structlog` to output via standard logging (stderr) instead of printing directly to stdout, which was corrupting the MCP JSON-RPC protocol during startup.

## [3.1.0] - 2026-01-19 - Repomix Integration & Repository Intelligence ðŸ§ 

### ðŸš€ Major Feature Expansion

**MetaMCP Enterprise** now includes **Repomix-inspired repository intelligence** - advanced token analysis and AI-optimized repository packing capabilities.

#### Added
- **ðŸ§  Token Analysis Suite**: Complete token usage analysis for LLM context optimization
  - File-level token counting with language detection
  - Directory-wide token distribution analysis
  - LLM context limit compatibility estimation (GPT-4, Claude, Gemini, etc.)
  - Token efficiency metrics and optimization recommendations

- **ðŸ“¦ Repository Packing Suite**: AI-first repository consolidation inspired by repomix
  - Multi-format output: XML, Markdown, JSON, Plain Text
  - AI-optimized packing with automatic token limits
  - Intelligent file selection prioritizing important code
  - Git-aware filtering with .gitignore and custom exclusions
  - Security filtering to prevent sensitive data leakage

- **ðŸŒ Enhanced Web Dashboard**: New enterprise management sections
  - Token Analysis page with real-time LLM compatibility checking
  - Repository Packing page with format selection and optimization
  - Advanced repository intelligence visualization
  - Interactive token limit estimation tools

- **ðŸ”§ Repomix Integration**: Advanced repository intelligence features
  - Repository consolidation for AI consumption
  - Token-aware content optimization
  - Multi-format AI-friendly packaging
  - Intelligent file prioritization for context limits

#### Technical Enhancements
- **10 Enterprise Tool Suites**: Complete MCP ecosystem coverage
- **Advanced Token Estimation**: Language-specific token counting algorithms
- **AI Context Optimization**: Automatic content selection for LLM consumption
- **Multi-Format Repository Export**: XML (repomix-style), Markdown, JSON, Plain Text
- **Security-Enhanced Packing**: Sensitive data filtering and exclusion

### Breaking Changes
- **New Tool Suites**: Added token_analysis and repo_packing suites
- **API Expansion**: 50+ endpoints across 10 service suites
- **Web Interface**: Added Token Analysis and Repository Packing pages

## [3.0.0] - 2026-01-19 - Enterprise Launch ðŸš€

### ðŸŽ‰ Major Enterprise Release

**MetaMCP Enterprise** - Complete MCP ecosystem orchestrator surpassing mcp-studio functionality.

#### Added
- **ðŸš€ 8 Tool Suites**: Complete MCP ecosystem management platform
  - Server Management: Start/stop/monitor MCP servers with process control
  - Tool Execution: Remote tool invocation across MCP server networks
  - Repository Analysis: Deep codebase analysis with health scoring
  - Client Management: Multi-client configuration for 5+ IDEs (Claude, Cursor, Windsurf, Zed, Antigravity)
  - Diagnostics: Enhanced EmojiBuster and PowerShell validation
  - Analysis: Advanced Runt Analyzer with SOTA compliance
  - Discovery: Comprehensive server and client integration scanning
  - Scaffolding: Enterprise-grade project generation

- **ðŸŒ Enterprise Web Dashboard**: Complete real-time management interface
  - Live API integration (no mock data)
  - 8 service health monitoring
  - Server lifecycle management
  - Tool execution interface
  - Repository intelligence dashboard
  - Client ecosystem management
  - Multi-page enterprise navigation

- **âš™ï¸ Advanced Server Management**: Production-ready MCP server orchestration
  - Process lifecycle control with PID tracking
  - Cross-platform subprocess management
  - Resource monitoring and health checks
  - Graceful shutdown and cleanup
  - Real-time status monitoring

- **ðŸ”§ Tool Execution Engine**: Remote tool invocation across MCP networks
  - Parameter validation and type checking
  - Execution history and performance tracking
  - Error handling and recovery
  - Tool metadata extraction and documentation

- **ðŸ“Š Repository Intelligence**: Deep codebase analysis and health assessment
  - Comprehensive structure analysis
  - Dependency auditing and FastMCP version checking
  - Code quality metrics and complexity scoring
  - Documentation completeness evaluation
  - Testing framework detection and coverage analysis
  - Health scoring algorithm (0-100 scale)
  - Automated improvement recommendations

- **ðŸ–¥ï¸ Client Ecosystem Management**: Multi-IDE integration platform
  - Configuration file parsing for 5+ IDEs
  - Safe configuration updates with backup
  - Server registration and unregistration
  - Integration validation and diagnostics
  - Cross-platform client support

#### Changed
- **ðŸ—ï¸ Architecture Overhaul**: Complete modular service architecture
  - 8 independent services with dedicated responsibilities
  - Service health monitoring and status tracking
  - Graceful error handling and recovery
  - Hot-swappable component design

- **ðŸ”’ Unicode Safety Enhancement**: Enterprise-grade crash prevention
  - Hex escape sequence standardization (`\uXXXX` format)
  - Safe Scanner philosophy implementation
  - Comprehensive validation across all components
  - Pre-commit hooks and CI integration

- **ðŸŒ Web Interface Transformation**: From basic UI to enterprise dashboard
  - Real API integration replacing mock data
  - Live health status and monitoring
  - Interactive server and tool management
  - Professional enterprise design system

#### Technical Improvements
- **FastMCP 3.1.1+.1+**: Enhanced response patterns throughout
- **Cross-platform Compatibility**: Windows, macOS, Linux verified
- **Performance Optimization**: Efficient resource usage and caching
- **Security Hardening**: Safe configuration management and validation
- **Error Resilience**: Comprehensive error handling and recovery

### Breaking Changes
- **API Structure**: Complete overhaul with 8 service endpoints
- **Web Interface**: Real functionality replaces placeholder UI
- **Configuration**: Enhanced client management with backup safety
- **Tool Registry**: 8 modular suites replace simple tool collection

## [2.0.0] - 2026-01-15 - Enterprise Foundation ðŸ—ï¸

### Added
- **ðŸ—ï¸ Modular Service Architecture**: Complete overhaul with 8 dedicated services
- **ðŸŒ Enterprise Web Dashboard**: Real-time monitoring and management interface
- **âš™ï¸ Server Lifecycle Management**: Start/stop/monitor MCP servers with process control
- **ðŸ”§ Tool Execution Framework**: Remote tool invocation across server networks
- **ðŸ“Š Repository Intelligence**: Deep codebase analysis with health assessment
- **ðŸ–¥ï¸ Client Management System**: Multi-client configuration for 5+ IDEs
- **ðŸ”’ Enhanced Security**: Comprehensive Unicode safety and validation
- **ðŸ“ˆ Performance Monitoring**: Real-time service health and metrics

### Changed
- **ðŸ›ï¸ Enterprise Architecture**: From basic server to complete ecosystem platform
- **ðŸ”§ Tool Registry Expansion**: From 4 to 8 comprehensive tool suites
- **ðŸŒ Web Interface**: Complete redesign with real API integration
- **ðŸ“š Documentation**: Enterprise-grade documentation and standards

### Technical Enhancements
- **FastMCP 3.1.1+.1+**: Full protocol compliance with enhanced patterns
- **Cross-platform**: Verified Windows, macOS, Linux compatibility
- **Process Management**: Advanced subprocess control and monitoring
- **API Architecture**: RESTful endpoints for all enterprise functions

## [1.2.0] - 2026-01-05

### Added
- **ðŸ” Client Integration Diagnostics**: New tool to check server health across multiple IDE clients (Antigravity, Claude, Cursor, Windsurf, Zed).
- **ðŸ“Š Runt Analyzer Enhancements**: Added Lines of Code (LoC) counting, dependency parsing, and detailed tool metadata extraction.

### Changed
- **ðŸ›¡ï¸ Project Cleanup**: Removed 15+ "zombie" server files and temporary backups to streamline the repository.
- **ðŸ”§ Robust Configuration**: Refactored server discovery to use dynamic system paths instead of hardcoded strings.

### Fixed
- **ðŸš¨ Code Quality**: Resolved 50+ Ruff linting errors across the entire project.
- **âš›ï¸ JSX Syntax**: Fixed critical React/JSX template corruption in `landing_page.py` caused by f-string escaping issues.
- **ðŸ”„ Async Hygiene**: Eliminated `RuntimeWarning` coroutine errors in diagnostic scripts.

## [1.1.0] - 2026-01-04

### Added
- **ðŸ›¡ï¸ Safe Scanner Standard**: Global repository sweep refactoring 17 files and 219 instances.
- **ðŸš¨ Hex-Based Identification**: All Unicode emojis in patterns and constants now use hex escape sequences (e.g., `\U0001F680`) to prevent grep/terminal crashes.
- **ðŸ” Global Unicode Detection**: EmojiBuster now scans docstrings, return values, and logging globally.
- **ðŸš€ CLI Support**: `safe_scanner.py` updated to accept target paths via command line.

### Changed
- **ðŸ›¡ï¸ EmojiBuster**: Standardized on uppercase hex formatting (`\uXXXX`) for conventional SOTA compliance.
- **ðŸ“š Documentation**: Updated README and PRD to reflect the Safe Scanner as a core SOTA requirement.

## [1.0.0] - 2026-01-04

### Changed
- **ðŸ“– README.md**: Complete rewrite with "Argh-Coding" philosophy
- **ðŸŽ¯ Product Vision**: Focus on preventing developer pain points
- **ðŸ—ï¸ Architecture**: Enhanced response pattern integration

### Fixed
- **ðŸš¨ Critical Issue**: Unicode logging crashes causing production instability
- **ðŸ”„ Restart Loops**: LLM auto-fix trap identification and prevention

## [0.2.1-beta] - 2026-01-02

### Changed
- Refactored project from `mcp-studio` to `meta_mcp` namespace.
- Standardized project structure for MCP SOTA compliance.
- Created `pyproject.toml` and entry points.

## [0.1.0] - 2026-01-02

### Added
- **ðŸ” Basic MCP Server**: FastMCP integration with tool registry
- **ðŸ› ï¸ Tool Discovery Framework**: Auto-discovery system for MCP tools
- **ðŸ“Š Server Management**: Basic server lifecycle management
- **ðŸŒ Web Interface**: Basic web UI for tool interaction
- **ðŸ“‹ Documentation**: Initial README and basic setup guide

### Core Tools Implemented
- **Server Discovery**: Find MCP servers across system
- **Tool Execution**: Execute tools on remote MCP servers
- **Configuration Management**: Basic client configuration updates
- **Health Monitoring**: Basic server status checking

### Architecture
- **FastMCP 3.1.1++**: Core framework integration
- **Tool Registry**: Centralized tool management
- **Enhanced Logging**: Structured logging with Unicode safety awareness
- **Cross-Platform**: Windows, macOS, Linux support

---

## ðŸŽ¯ Development Philosophy

Meta MCP follows the **"Argh-Coding" philosophy** - every feature is designed to prevent a specific developer frustration that we've all experienced:

### ðŸš¨ Critical Issues Addressed
- **Unicode Logging Crashes**: The #1 cause of mysterious service restarts
- **Docker Desktop Confusion**: Maximum confusion scenarios with UI deception
- **Framework Assumption Errors**: Hours wasted on incorrect API usage
- **SOTA Compliance Gaps**: Repositories not following modern standards

### ðŸ›¡ï¸ Prevention Focus
- **Enhanced Response Patterns**: Immediate diagnosis instead of mysterious errors
- **Unicode Safety**: Comprehensive validation and auto-fixing
- **Proactive Tooling**: Prevent problems before they cause crashes
- **Education**: Clear guidance on best practices

### ðŸš€ Impact Metrics
- **Before Meta MCP**: 3+ days cumulative delay from Unicode crashes
- **After Meta MCP**: 5 minutes comprehensive Unicode audit and fix
- **Success Stories**: Real-world stability improvements tracked and reported

---

**Meta MCP**: Turning "Argh!" moments into "Aha!" moments since 2026. ðŸš€

