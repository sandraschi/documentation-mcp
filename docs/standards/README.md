# Detailed Standards

**Prerequisites:** `docs/core/` (specifically `JUNE_2026_STANDARDS_BAR.md` and `SOTA_REQUIREMENTS.md`)

This directory contains detailed implementation standards that expand on the core bar. Where `docs/core/` tells you *what* to do, this directory tells you *how*.

## Sections

| Area | Key files |
|------|-----------|
| **New-repo bar** | `NEW_REPO_BUILD_COMPLETE.md` (assfix-zero), `ONBOARDING_STANDARD.md` |
| **Webapp** | `WEBAPP_SOTA_STANDARDS.md`, `REACT_HARDENING.md`, `WEBAPP_COMPANION_MODE.md`, `WEBAPP_LOGS_PAGE.md` |
| **Backend** | `STARLETTE_NO_PYDANTIC_STANDARD.md`, `fastmcp-3.2-concurrency.md`, `fastmcp-3.2-startup-probes.md` |
| **CORS** | `CORS_STANDARD.md` — origins, Tailscale, Tauri, unconditional regex |
| **Security** | `PROMPT_INJECTION_HARDENING.md`, `RAT_EMERGENCY_PROTOCOL.md`, `SAFETY_PROTOCOLS.md` |
| **Testing** | `VERIFICATION_STANDARDS.md`, `TESTING_GUIDE.md`, `testing.md`, `testing-tdd-red-green.md` |
| **Tauri** | `TAURI_PRODUCTION_PITFALLS.md`, `TAURI_API_PATTERNS.md`, `TAURI_DO_DONT_MATRIX.md`, `WEBVIEW2_VS_LEGACY.md` |
| **CLI/scripts** | `POWERSHELL_STANDARDS.md`, `START_SCRIPT_STANDARD.md`, `JUSTFILE_STANDARDS.md` |
| **Quality** | `CODE_QUALITY_STANDARDS.md`, `RUFF_STANDARDS.md`, `BIOME_STANDARDS.md`, `GITIGNORE_STANDARDS.md` |
| **AI/Sampling** | `ai-sampling.md`, `ai-rag-2026.md`, `SAMPLING_API_RISKS.md`, `SKILLS_ECOSYSTEM_2026.md` |

## When to read this

- When implementing a specific feature (webapp page, REST endpoint, Tauri build)
- When your CI fails on a rule you don't understand
- When you need the exact CORS config or error handler pattern

The core bar (`docs/core/JUNE_2026_STANDARDS_BAR.md`) is the minimum pass/fail gate. This directory is the implementation reference.
