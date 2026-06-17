set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]
import 'scripts/just/fleet.just'

# ── Dashboard ─────────────────────────────────────────────────────────────────

# Open the interactive recipe dashboard in the browser
default:
    @just --list

# ── Quality ───────────────────────────────────────────────────────────────────

# Execute Ruff SOTA v13.1 linting
lint:
    Set-Location '{{justfile_directory()}}'
    uv run ruff check .
    Set-Location '{{justfile_directory()}}\web_sota'
    npx @biomejs/biome ci .

# Execute Ruff SOTA v13.1 fix and formatting
fix:
    Set-Location '{{justfile_directory()}}'
    uv run ruff check . --fix --unsafe-fixes
    uv run ruff format .
    Set-Location '{{justfile_directory()}}\web_sota'
    npx @biomejs/biome check --write .

# ── Hardening ─────────────────────────────────────────────────────────────────

# Execute Bandit security audit
check-sec:
    Set-Location '{{justfile_directory()}}'
    uv run bandit -r src/

# Execute safety audit of dependencies
audit-deps:
    Set-Location '{{justfile_directory()}}'
    uv run safety check

#
# Primary entry point for documentation infrastructure and fleet management.
#
# Rule: JUST-SOTA-2026-04
# Standard: PowerShell 7.4+ core-compliant

# ── Infrastructure ────────────────────────────────────────────────────────────

# Quantitative snapshot of documentation and tools
stats:
    Set-Location '{{justfile_directory()}}'
    uv run python tools/repo_stats.py

# Sync all environment dependencies
sync:
    Set-Location '{{justfile_directory()}}'
    uv sync --extra dev

# Execute pytest suite
test:
    Set-Location '{{justfile_directory()}}'
    uv run pytest

# Execute pyright type analytics
typecheck:
    Set-Location '{{justfile_directory()}}'
    uv run pyright src

# Unified quality verification
check: lint test typecheck

# Initialize Docs MCP Webapp (Standard)
web:
    Set-Location '{{justfile_directory()}}'
    & '.\web_sota\start.ps1'

# Initialize Docs MCP Webapp (Poll-and-Open)
web-auto:
    Set-Location '{{justfile_directory()}}'
    & '.\web_sota\start.ps1' -Automated

# Open webapp in system browser
docs-open:
    Start-Process 'http://127.0.0.1:11032/'

# ── Backend ──────────────────────────────────────────────────────────────────

# Start Uvicorn API (port 11033)
backend:
    Set-Location '{{justfile_directory()}}'
    $env:PYTHONPATH = '{{justfile_directory()}};{{justfile_directory()}}\src'
    uv run uvicorn docs_mcp.server:app --host 127.0.0.1 --port 11033 --log-level info

# ── Transport ────────────────────────────────────────────────────────────────

# Start FastMCP stdio interface
mcp-stdio:
    Set-Location '{{justfile_directory()}}'
    $env:PYTHONPATH = '{{justfile_directory()}};{{justfile_directory()}}\src'
    uv run python -m docs_mcp.stdio_main

# ── Fleet Management ──────────────────────────────────────────────────────────

# Regenerate fleet registry artifacts
fleet-registry:
    Set-Location '{{justfile_directory()}}'
    uv run python tools/generate_fleet_registry.py

fleet-fastmcp:
    Set-Location '{{justfile_directory()}}'
    uv run python tools/sync_fleet_fastmcp.py

fleet: fleet-registry fleet-fastmcp

# ── RAG (LanceDB doc index) ───────────────────────────────────────────────────

# Full documentation reindex (CPU)
rag:
    @pwsh.exe -NoProfile -ExecutionPolicy Bypass -File scripts/just/rag.ps1

# Full documentation reindex on GPU (after rag-gpu-install)
rag-gpu:
    @pwsh.exe -NoProfile -ExecutionPolicy Bypass -File scripts/just/rag-gpu.ps1

# One-time: install fastembed-gpu + onnxruntime-gpu + NVIDIA CUDA 12 runtimes (~1.5 GB)
rag-gpu-install:
    @pwsh.exe -NoProfile -ExecutionPolicy Bypass -File scripts/just/rag-gpu-install.ps1

# Revert to CPU onnxruntime stack
rag-cpu-install:
    @pwsh.exe -NoProfile -ExecutionPolicy Bypass -File scripts/just/rag-cpu-install.ps1

# ── Docker ───────────────────────────────────────────────────────────────────
# Check Docker Desktop status
docker-status:
    & '{{justfile_directory()}}/docker/check-docker-status.ps1'

docker-update:
    & '{{justfile_directory()}}/docker/update-docker-desktop.ps1'

docker-update-full:
    & '{{justfile_directory()}}/docker/update-docker-desktop.ps1' -FullWipe

docker-fix:
    & '{{justfile_directory()}}/docker/fix-docker-daemon.ps1'

# ── Misc Tools ───────────────────────────────────────────────────────────────
# Generate readme-hero
readme-hero:
    Set-Location '{{justfile_directory()}}'
    uv run python tools/readme_hero.py

toolbench-drift:
    Set-Location '{{justfile_directory()}}'
    uv run python toolbench/scripts/report_reference_drift.py
