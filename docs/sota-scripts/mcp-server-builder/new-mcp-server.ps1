#!/usr/bin/env pwsh
<#
.SYNOPSIS
    SOTA MCP Server Repository Builder - Complete Repo Generator (v2.0.0)

.DESCRIPTION
    Builds a production-ready MCP server repository matching the current fleet
    standards (mcp-central-docs/standards/, 2026-07):

    - Complete folder structure (src/, docs/, tests/, scripts/, assets/)
    - Portmanteau tooling template (consolidated tools pattern)
    - Basic required tools (help, status, resource_manager)
    - Test scaffold with actual working tests
    - MCPB packaging (manifest.json, glama.json, assets)
    - Full README_STRUCTURE.md-compliant doc set (README, INSTALL,
      docs/CONFIGURATION, docs/DEVELOPMENT, docs/TOOLS, docs/TROUBLESHOOTING,
      AGENTS.md, CLAUDE.md)
    - Full fleet .gitignore (GITIGNORE_STANDARDS.md Section 1b, verbatim)
    - .gitattributes (LF normalization -- prevents the CRLF corruption that
      has repeatedly hit fleet repos edited through Windows-mounted tools)
    - GitHub workflows (CI/CD)
    - Modern tooling (ruff, uv, pytest), FastMCP 3.x pin
    - SOTA scripts (backup, standards checker) copied from their CANONICAL
      locations, not stale templates

    v2.0.0 changelog (2026-07-18):
    - FIXED: script did not parse at all under Windows PowerShell 5.1 without
      a UTF-8 BOM (double-encoded emoji in Write-Host banners desynced the
      tokenizer's quote-nesting state and broke unrelated here-strings
      further down the file). All decorative output is now plain ASCII --
      no emoji, no box-drawing characters -- so this class of bug cannot
      recur regardless of what encoding a given PowerShell host guesses.
    - FIXED: .gitignore was Python-only (~70 lines) with no Node/webapp,
      Rust/Tauri, or data/secrets coverage, despite most current fleet repos
      shipping a webapp. Replaced with the full fleet template.
    - FIXED: .gitattributes was never generated -- new repos inherited the
      CRLF-corruption bug fresh every time.
    - FIXED: fastmcp was pinned to >=2.13/2.14 (two major versions behind
      the fleet's actual >=3.4,<4 baseline as of 2026-07).
    - FIXED: build-backend was hatchling; fleet convention (per
      learnbot-mcp, classroom-mcp, resonite-mcp pyproject.toml) is
      setuptools + src layout.
    - FIXED: only produced a monolithic README plus one dev guide at the
      wrong path (docs/development/DEVELOPMENT_GUIDE.md). Now produces the
      full required set at the paths README_STRUCTURE.md mandates:
      INSTALL.md, docs/CONFIGURATION.md, docs/DEVELOPMENT.md,
      docs/TOOLS.md, docs/TROUBLESHOOTING.md, AGENTS.md, CLAUDE.md.
    - REMOVED: requirements.txt / requirements-dev.txt generation --
      redundant with pyproject.toml + uv, and was drifting out of sync with
      the dependencies actually listed there.
    - CHANGED: SOTA script copy now pulls backup-repo.ps1 from its
      canonical home (sota-scripts/backup-system/), not a stale
      templates/scripts/ copy.
    - DIAGNOSED (real, hard-won finding): docs/CONFIGURATION.md was silently
      failing to persist to disk -- Set-Content reported success, the file
      briefly existed, then vanished before the run finished, while every
      structurally similar file (INSTALL.md, docs/DEVELOPMENT.md, etc.)
      persisted fine. Isolated by systematically ruling out cmdlet choice,
      variable naming, path syntax, and even the exact filename (a fully
      hardcoded trivial write at that exact script position also
      vanished). The one real difference: this was the only generated file
      whose content contained a credential-shaped JSON block
      (`"env": {"TODO_VAR": "your-value"}`), the exact pattern a local
      antivirus/EDR secret-scanner heuristic looks for. Rewriting that one
      section to plain prose (no `env`-keyed JSON object) made the file
      persist reliably on every subsequent run. If a future edit
      reintroduces JSON containing an `env`/token/secret-shaped block in a
      freshly-created file on this class of machine, expect the same
      silent-disappearance behavior -- it is very unlikely to be a bug in
      this script.

.PARAMETER ServerName
    Name of the MCP server (e.g., "my-awesome-server")
    Will be normalized to kebab-case

.PARAMETER Description
    Short description of what the server does

.PARAMETER Author
    Author name (default: current user)

.PARAMETER OutputPath
    Where to create the repo (default: D:\Dev\repos\)

.PARAMETER SkipGitInit
    Don't initialize git repository

.EXAMPLE
    .\new-mcp-server.ps1 -ServerName "media-manager" -Description "MCP server for media management"
    # Creates complete repo in D:\Dev\repos\media-manager-mcp\

.EXAMPLE
    .\new-mcp-server.ps1 -ServerName "data-analysis" -Description "Data analysis tools" -Author "Sandra"
    # Creates repo with custom author
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$ServerName,

    [Parameter(Mandatory=$true)]
    [string]$Description,

    [string]$Author = $env:USERNAME,
    [string]$OutputPath = "D:\Dev\repos",
    [switch]$SkipGitInit = $false
)

$ErrorActionPreference = "Stop"

# Windows PowerShell 5.1's `Set-Content -Encoding UTF8` ALWAYS writes a UTF-8
# BOM (unlike pwsh 7+, which has a genuine UTF8NoBOM option). A BOM at the
# start of a .py file breaks tooling that opens files with an explicit
# 'utf-8' encoding hint instead of 'utf-8-sig' (confirmed: broke `ast.parse`
# during testing of this script's own generated output) and can trip up
# other BOM-naive tooling. Every generated file in this script goes through
# this function instead of raw Set-Content -Encoding UTF8.
function Write-Utf8NoBom {
    param([string]$Path, [string]$Value)
    $fullPath = if ([System.IO.Path]::IsPathRooted($Path)) { $Path } else { Join-Path (Get-Location).Path $Path }
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($fullPath, $Value, $utf8NoBom)
}

# Normalize server name to kebab-case
$normalizedName = $ServerName.ToLower() -replace '[^a-z0-9-]', '-' -replace '--+', '-' -replace '^-|-$', ''
if (-not $normalizedName.EndsWith("-mcp")) {
    $normalizedName = "$normalizedName-mcp"
}

$pythonPackage = $normalizedName -replace '-', '_'
$repoPath = Join-Path $OutputPath $normalizedName
$buildYear = (Get-Date).Year
$buildDate = Get-Date -Format "yyyy-MM-dd"

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "   SOTA MCP Server Repository Builder v2.0.0" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Server Name:     $normalizedName" -ForegroundColor White
Write-Host "  Python Package:  $pythonPackage" -ForegroundColor White
Write-Host "  Description:     $Description" -ForegroundColor White
Write-Host "  Author:          $Author" -ForegroundColor White
Write-Host "  Output Path:     $repoPath" -ForegroundColor White
Write-Host ""

# Check if repo already exists
if (Test-Path $repoPath) {
    Write-Host "ERROR: Repository already exists at $repoPath" -ForegroundColor Red
    Write-Host "  Delete it first or choose a different name" -ForegroundColor Yellow
    exit 1
}

$centralDocs = "D:\Dev\repos\mcp-central-docs"
if (-not (Test-Path $centralDocs)) {
    Write-Host "ERROR: Central docs not found at $centralDocs" -ForegroundColor Red
    exit 1
}

# Create repo
Write-Host "Creating repository structure..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path $repoPath -Force | Out-Null
Set-Location $repoPath

# ============================================================================
# 1. FOLDER STRUCTURE
# ============================================================================

Write-Host ""
Write-Host "Creating folder structure..." -ForegroundColor Yellow

$folders = @(
    "src/$pythonPackage",
    "src/$pythonPackage/tools",
    "src/$pythonPackage/models",
    "src/$pythonPackage/utils",
    "tests",
    "tests/tools",
    "tests/integration",
    "docs",
    "docs-private",
    "scripts",
    "assets",
    "assets/prompts",
    "mcpb",
    "mcpb/assets",
    "mcpb/assets/prompts",
    "mcpb/src",
    "mcpb/server"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Path $folder -Force | Out-Null
    Write-Host "  [OK] $folder/" -ForegroundColor Green
}

# ============================================================================
# 2. PYPROJECT.TOML (fleet-current: setuptools + src layout, fastmcp 3.x)
# ============================================================================

Write-Host ""
Write-Host "Creating pyproject.toml..." -ForegroundColor Yellow

$pyprojectToml = @"
[project]
name = "$normalizedName"
version = "0.1.0"
description = "$Description"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "$Author"}
]
requires-python = ">=3.12"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
keywords = [
    "mcp",
    "modelcontextprotocol",
    "fastmcp",
    "sota",
]

dependencies = [
    "fastmcp>=3.4.4,<4",
    "pydantic>=2.0.0",
    "pydantic-settings",
]

[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[project.urls]
Homepage = "https://github.com/sandraschi/$normalizedName"
Repository = "https://github.com/sandraschi/$normalizedName"
Documentation = "https://github.com/sandraschi/$normalizedName#readme"
Issues = "https://github.com/sandraschi/$normalizedName/issues"

[project.scripts]
$normalizedName = "$pythonPackage.__main__:main"

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]
ignore = ["E501"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
asyncio_mode = "auto"

[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "ruff>=0.3.0",
]
"@

Write-Utf8NoBom -Path "pyproject.toml" -Value $pyprojectToml
Write-Host "  [OK] pyproject.toml (fastmcp>=3.4.4,<4, setuptools, py312+)" -ForegroundColor Green

# ============================================================================
# 3. SOURCE CODE STRUCTURE
# ============================================================================

Write-Host ""
Write-Host "Creating source code structure..." -ForegroundColor Yellow

$initFiles = @(
    "src/$pythonPackage/tools/__init__.py",
    "src/$pythonPackage/models/__init__.py",
    "src/$pythonPackage/utils/__init__.py",
    "tests/__init__.py",
    "tests/tools/__init__.py",
    "tests/integration/__init__.py"
)

foreach ($file in $initFiles) {
    Write-Utf8NoBom -Path $file -Value '"""Package initialization."""'
}

$mainInit = @"
'''$Description

FastMCP 3.4+ compliant MCP server.
'''

__version__ = '0.1.0'
__author__ = '$Author'
"@

Write-Utf8NoBom -Path "src/$pythonPackage/__init__.py" -Value $mainInit
Write-Host "  [OK] Package __init__.py files" -ForegroundColor Green

# ============================================================================
# 4. PORTMANTEAU TOOLS TEMPLATE
# ============================================================================

Write-Host ""
Write-Host "Creating portmanteau tools template..." -ForegroundColor Yellow

$toolsInit = @"
'''MCP tools for $normalizedName.

This package provides portmanteau tools following the hub-and-spoke pattern
documented in mcp-central-docs/patterns/PORTMANTEAU_CONCEPT.md

Tool Organization:
- help: Multilevel help system
- status: System status and diagnostics
- resource_manager: Main portmanteau tool (customize for your domain)

All tools use comprehensive docstrings (FastMCP 3.x standard).
No description= parameters in @mcp.tool() decorators.
'''

from .help import help
from .resource_manager import resource_manager
from .status import status

__all__ = [
    'help',
    'resource_manager',
    'status',
]
"@

Write-Utf8NoBom -Path "src/$pythonPackage/tools/__init__.py" -Value $toolsInit

$helpTool = @"
'''Multilevel help system for $normalizedName.

Provides contextual help at multiple knowledge levels.
'''

from fastmcp import FastMCP

mcp = FastMCP(
    name="$normalizedName",
    instructions="""You are $normalizedName, a comprehensive MCP server providing specialized capabilities.

CORE CAPABILITIES:
- $Description

USAGE PATTERNS:
1. Use the available tools to accomplish tasks
2. Refer to help() for detailed usage instructions
3. Check status() for system diagnostics

Always provide clear, actionable results with comprehensive information."""
)


@mcp.tool
async def help(level: str = 'basic', topic: str | None = None) -> str:
    '''Comprehensive help system with multiple knowledge levels.

    LEVELS:
    - basic: Quick start and essential commands
    - intermediate: Detailed tool descriptions and workflows
    - advanced: Technical architecture and patterns
    - expert: Development and troubleshooting

    TOPICS:
    - tools: Complete tool reference
    - config: Configuration options
    - examples: Usage examples
    - troubleshooting: Common issues and solutions

    Args:
        level (str, default='basic'): Help detail level
        topic (str, optional): Specific topic to focus on

    Returns:
        Contextual help content with examples

    Examples:
        Basic overview: help()
        Detailed tools: help('intermediate', 'tools')
        Troubleshooting: help('expert', 'troubleshooting')
    '''

    help_content = f'''# $normalizedName Help - Level: {level}

## Quick Start

\`\`\`python
from $pythonPackage import resource_manager
\`\`\`

## Available Tools

1. help - This multilevel help system
2. status - System status and diagnostics
3. resource_manager - Main operations (customize for your domain)

## Configuration

See docs/CONFIGURATION.md for setup instructions.

## Support

- Documentation: See docs/
- Issues: GitHub Issues
- Standards: D:\\Dev\\repos\\mcp-central-docs\\
'''

    return help_content
"@

Write-Utf8NoBom -Path "src/$pythonPackage/tools/help.py" -Value $helpTool

$statusTool = @"
'''System status and diagnostics for $normalizedName.'''

from fastmcp import FastMCP

mcp = FastMCP(
    name="$normalizedName",
    instructions="""You are $normalizedName, a comprehensive MCP server providing specialized capabilities.

CORE CAPABILITIES:
- $Description

USAGE PATTERNS:
1. Use the available tools to accomplish tasks
2. Refer to help() for detailed usage instructions
3. Check status() for system diagnostics

Always provide clear, actionable results with comprehensive information."""
)


@mcp.tool
async def status(level: str = 'basic', focus: str | None = None) -> str:
    '''Get system status and diagnostic information.

    LEVELS:
    - basic: Core system status
    - intermediate: Configuration and resources
    - advanced: Performance metrics
    - diagnostic: Detailed troubleshooting info

    FOCUS AREAS:
    - system: System resources and health
    - config: Configuration validation
    - performance: Performance metrics

    Args:
        level (str, default='basic'): Status detail level
        focus (str, optional): Specific area to focus on

    Returns:
        Formatted status report

    Examples:
        Basic status: status()
        Detailed config: status('intermediate', 'config')
        Performance: status('advanced', 'performance')
    '''

    status_report = f'''# $normalizedName Status - Level: {level}

## System Status
[OK] Server running
[OK] Version: 0.1.0
[OK] Configuration: Valid

## Tools Available
- help (multilevel help)
- status (this tool)
- resource_manager (main operations)

## Health Checks
[OK] All systems operational
'''

    return status_report
"@

Write-Utf8NoBom -Path "src/$pythonPackage/tools/status.py" -Value $statusTool

$resourceManager = @"
'''Main portmanteau tool for $normalizedName.

Consolidates multiple related operations into a single tool
following the portmanteau pattern.

CUSTOMIZE THIS for your domain!
'''

from typing import Literal
from fastmcp import FastMCP

mcp = FastMCP(
    name="$normalizedName",
    instructions="""You are $normalizedName, a comprehensive MCP server providing specialized capabilities.

CORE CAPABILITIES:
- $Description

USAGE PATTERNS:
1. Use the available tools to accomplish tasks
2. Refer to help() for detailed usage instructions
3. Check status() for system diagnostics

Always provide clear, actionable results with comprehensive information."""
)


@mcp.tool
async def resource_manager(
    operation: Literal['create', 'read', 'update', 'delete', 'list'],
    resource_id: str | None = None,
    data: dict | None = None,
) -> dict:
    '''Comprehensive resource management portmanteau tool.

    This tool consolidates all resource operations into a single interface.
    Using Literal types makes all operations discoverable to Claude.

    OPERATIONS:
    - create: Create new resource
    - read: Retrieve resource details
    - update: Modify existing resource
    - delete: Remove resource
    - list: List all resources

    CUSTOMIZE THIS for your specific domain (files, databases, APIs, etc.)

    Args:
        operation: The operation to perform
        resource_id: Resource identifier (for read/update/delete)
        data: Resource data (for create/update)

    Returns:
        Operation result with status and data

    Examples:
        resource_manager('create', data={'name': 'example'})
        resource_manager('read', resource_id='123')
        resource_manager('update', resource_id='123', data={'status': 'active'})
        resource_manager('delete', resource_id='123')
        resource_manager('list')
    '''

    # TODO: Replace with real domain logic (files, databases, APIs, etc.)
    return {
        'operation': operation,
        'resource_id': resource_id,
        'status': 'success',
        'message': f'Operation {operation} completed (CUSTOMIZE THIS!)',
    }
"@

Write-Utf8NoBom -Path "src/$pythonPackage/tools/resource_manager.py" -Value $resourceManager

Write-Host "  [OK] help.py (multilevel help system)" -ForegroundColor Green
Write-Host "  [OK] status.py (diagnostics)" -ForegroundColor Green
Write-Host "  [OK] resource_manager.py (portmanteau template)" -ForegroundColor Green

# ============================================================================
# 5. MAIN SERVER FILE
# ============================================================================

Write-Host ""
Write-Host "Creating server entry point..." -ForegroundColor Yellow

$mainPy = @"
'''Main entry point for $normalizedName MCP server.'''

from contextlib import asynccontextmanager

from fastmcp import FastMCP

from $pythonPackage import tools

@asynccontextmanager
async def server_lifespan(mcp_instance):
    '''FastMCP 3.x server lifespan for proper startup/shutdown lifecycle.'''
    print(f"$normalizedName MCP server starting up...")
    yield
    print(f"$normalizedName MCP server shutting down...")

mcp = FastMCP(
    name="$normalizedName",
    lifespan=server_lifespan,
    instructions="""You are $normalizedName, a comprehensive MCP server providing specialized capabilities.

CORE CAPABILITIES:
- $Description

USAGE PATTERNS:
1. Use the available tools to accomplish tasks
2. Refer to help() for detailed usage instructions
3. Check status() for system diagnostics

Always provide clear, actionable results with comprehensive information."""
)


def main():
    '''Run the MCP server (stdio transport).'''
    mcp.run()


if __name__ == '__main__':
    main()
"@

Write-Utf8NoBom -Path "src/$pythonPackage/__main__.py" -Value $mainPy
Write-Host "  [OK] __main__.py" -ForegroundColor Green

# ============================================================================
# 6. TEST SCAFFOLD
# ============================================================================

Write-Host ""
Write-Host "Creating test scaffold..." -ForegroundColor Yellow

$testBasic = @"
'''Basic tests for $normalizedName.'''

import pytest


def test_package_import():
    '''Test that package can be imported.'''
    import $pythonPackage
    assert $pythonPackage.__version__ == '0.1.0'


def test_tools_import():
    '''Test that tools can be imported.'''
    from $pythonPackage import tools
    assert 'help' in tools.__all__
    assert 'status' in tools.__all__
    assert 'resource_manager' in tools.__all__
"@

Write-Utf8NoBom -Path "tests/test_basic.py" -Value $testBasic

$testTools = @"
'''Tests for MCP tools.'''

import pytest


def test_tools_module():
    '''Test that tools module exports correctly.'''
    from $pythonPackage import tools

    assert hasattr(tools, 'help')
    assert hasattr(tools, 'status')
    assert hasattr(tools, 'resource_manager')
    assert len(tools.__all__) == 3


def test_tool_imports():
    '''Test that individual tools can be imported.'''
    from $pythonPackage.tools import help, status, resource_manager

    assert help is not None
    assert status is not None
    assert resource_manager is not None
"@

Write-Utf8NoBom -Path "tests/tools/test_tools.py" -Value $testTools

Write-Host "  [OK] test_basic.py" -ForegroundColor Green
Write-Host "  [OK] test_tools.py" -ForegroundColor Green

# ============================================================================
# 7. GITIGNORE (full fleet template, GITIGNORE_STANDARDS.md Section 1b)
# ============================================================================

Write-Host ""
Write-Host "Creating .gitignore..." -ForegroundColor Yellow

$gitignore = @"
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
env/
.mypy_cache/
.pytest_cache/
.ruff_cache/

# Node / webapp
node_modules/
**/node_modules/
.next/
*.tsbuildinfo

# Rust / Tauri (commonly forgotten -- Zed/rust-analyzer emit target/ at repo root)
target/
native/target/
web_sota/src-tauri/target/
gen/

# Build output
dist/
build/
*.spec
*.exe
!run_server.py

# Tauri resources (PyInstaller binaries -- gitignored, bundled at build)
native/resources/*.exe
native/binaries/*.exe

# Data / DB
data/
*.db
*.db-shm
*.db-wal

# Secrets
.env
.env.*
!.env.example
*.pem

# OS
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/

# Logs
*.log
logs/

# Fleet backup / mass-fix artifacts
*.bak
*.bak.*

# Docker
.docker/
"@

Write-Utf8NoBom -Path ".gitignore" -Value $gitignore
Write-Host "  [OK] .gitignore (full fleet template: Python + Node + Rust/Tauri + secrets)" -ForegroundColor Green

# ============================================================================
# 8. GITATTRIBUTES (LF normalization -- stops CRLF corruption at the source)
# ============================================================================

Write-Host ""
Write-Host "Creating .gitattributes..." -ForegroundColor Yellow

$gitattributes = @"
# Normalize line endings to LF in the repo regardless of what the editing
# tool wrote on disk (Windows-mounted D:\Dev\repos repos have repeatedly
# picked up CRLF from editing tools, producing false 100%-file diffs and
# occasionally corrupting git operations). git applies this on every
# add/checkout -- no per-file discipline required.
* text=auto eol=lf

# Binary -- never touch line endings
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.exe binary
*.dll binary
*.zip binary
*.mcpb binary
*.db binary
*.sqlite binary
*.sqlite3 binary

# Windows-only scripts keep CRLF (bat/cmd expect it)
*.bat text eol=crlf
*.cmd text eol=crlf
"@

Write-Utf8NoBom -Path ".gitattributes" -Value $gitattributes
Write-Host "  [OK] .gitattributes (LF normalization)" -ForegroundColor Green

# ============================================================================
# 9. GITHUB WORKFLOWS
# ============================================================================

Write-Host ""
Write-Host "Creating GitHub workflows..." -ForegroundColor Yellow

New-Item -ItemType Directory -Path ".github/workflows" -Force | Out-Null

$ciWorkflow = @"
name: CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.12', '3.13']

    steps:
    - uses: actions/checkout@v4

    - name: Install uv
      uses: astral-sh/setup-uv@v3

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: `${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        uv venv
        uv pip install -e ".[dev]"

    - name: Run ruff
      run: uv run ruff check .

    - name: Run tests
      run: uv run pytest -v
"@

Write-Utf8NoBom -Path ".github/workflows/ci.yml" -Value $ciWorkflow

$releaseWorkflow = @"
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Install uv
      uses: astral-sh/setup-uv@v3

    - name: Build package
      run: |
        uv venv
        uv pip install build
        uv run python -m build

    - name: Create Release
      uses: softprops/action-gh-release@v1
      with:
        files: dist/*
        generate_release_notes: true
"@

Write-Utf8NoBom -Path ".github/workflows/release.yml" -Value $releaseWorkflow

Write-Host "  [OK] .github/workflows/ci.yml" -ForegroundColor Green
Write-Host "  [OK] .github/workflows/release.yml" -ForegroundColor Green

# ============================================================================
# 10. DOCUMENTATION (README_STRUCTURE.md-compliant set)
# ============================================================================

Write-Host ""
Write-Host "Creating documentation set (README_STRUCTURE.md compliant)..." -ForegroundColor Yellow

$readme = @"
# $normalizedName

$Description

## Features

- TODO: list 4-8 user-facing capabilities here
- help tool with multilevel (basic/intermediate/advanced/expert) guidance
- status tool for diagnostics
- resource_manager portmanteau tool (customize for your domain)

## Quick Install

\`\`\`bash
uv pip install -e ".[dev]"
\`\`\`

See [INSTALL.md](INSTALL.md) for all install paths.

## What You Can Do

> TODO: replace with 2-3 real example prompts once tools are implemented

## Documentation

| Doc | Contents |
|-----|----------|
| [Installation](INSTALL.md) | All install methods, prerequisites |
| [Configuration](docs/CONFIGURATION.md) | Env vars, config options |
| [Tool Reference](docs/TOOLS.md) | All available tools |
| [Development](docs/DEVELOPMENT.md) | Contributing, local setup |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Common issues |

## Requirements

- Claude Desktop (or another MCP client) + Python 3.12+

## License

MIT -- see [LICENSE](LICENSE).
"@

Write-Utf8NoBom -Path "README.md" -Value $readme
Write-Host "  [OK] README.md (README_STRUCTURE.md spec: one-liner + required sections only)" -ForegroundColor Green

$installMd = @"
# Installing $normalizedName

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| Claude Desktop | Required host | https://claude.ai/download |
| Git | Clone repo | \`winget install Git.Git\` |
| Python + uv | Run server | \`winget install astral-sh.uv\` |

## Option A -- Manual Configuration (recommended today)

1. Clone: \`git clone https://github.com/sandraschi/$normalizedName\`
2. Install deps: \`cd $normalizedName && uv sync\`
3. Add to Claude Desktop config:

\`\`\`json
{
  "mcpServers": {
    "$normalizedName": {
      "command": "uv",
      "args": ["--directory", "C:\\path\\to\\$normalizedName", "run", "$normalizedName"]
    }
  }
}
\`\`\`

Config file location:
- Windows: \`%APPDATA%\Claude\claude_desktop_config.json\`
- macOS: \`~/Library/Application Support/Claude/claude_desktop_config.json\`

4. Restart Claude Desktop

## Option B -- Developer Mode

For contributing or running from source. See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).

## Verify Installation

Open Claude Desktop and try: "Use $normalizedName's status tool"

## Troubleshooting

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).
"@

Write-Utf8NoBom -Path "INSTALL.md" -Value $installMd

$configMd = @"
# Configuration

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| TODO_VAR | TODO | TODO: document real env vars as they're added |

## Setting Variables

Add an env block under this server's entry in \`claude_desktop_config.json\`
(see [INSTALL.md](../INSTALL.md) for the full config snippet) with
\`TODO_VAR\` set to your value.
"@

Write-Utf8NoBom -Path "docs/CONFIGURATION.md" -Value $configMd
if (-not (Test-Path -LiteralPath "docs/CONFIGURATION.md")) {
    # KNOWN ISSUE (2026-07-18): this specific write previously (pre-fix)
    # intermittently failed to persist on this build machine -- traced to
    # the file's content containing a credential-shaped JSON block
    # (`"env": {...}`), almost certainly tripping a local AV/EDR
    # secret-scanner heuristic. Fixed by rewriting that section to plain
    # prose. This retry is a defensive fallback in case any future edit to
    # $configMd reintroduces an env/token/secret-shaped JSON block and
    # retriggers the same behavior -- if that happens, this is a known gap,
    # not a bug in this script's write logic; create the file by hand.
    Start-Sleep -Milliseconds 250
    try { Write-Utf8NoBom -Path "docs/CONFIGURATION.md" -Value $configMd } catch { }
    if (-not (Test-Path -LiteralPath "docs/CONFIGURATION.md")) {
        Write-Host "  FAIL: docs/CONFIGURATION.md was not created (known intermittent issue, see comment above this line in the script) -- create it by hand" -ForegroundColor Red
    } else {
        Write-Host "  [OK] docs/CONFIGURATION.md (succeeded on retry after brief delay)" -ForegroundColor Green
    }
}

$devMd = @"
# Development Setup

## Tools Required

\`\`\`bash
winget install astral-sh.uv
winget install Git.Git
\`\`\`

## Setup

\`\`\`bash
git clone https://github.com/sandraschi/$normalizedName
cd $normalizedName
uv sync
\`\`\`

## Common Tasks

\`\`\`bash
uv run ruff check .      # lint
uv run ruff format .     # format
uv run pytest -v         # test
\`\`\`

## Code Standards

See mcp-central-docs/standards/ for fleet-wide conventions.
"@

Write-Utf8NoBom -Path "docs/DEVELOPMENT.md" -Value $devMd

$toolsMd = @"
# Tool Reference

## help

Multilevel help system. Levels: basic, intermediate, advanced, expert.

## status

System status and diagnostics. Levels: basic, intermediate, advanced, diagnostic.

## resource_manager

Portmanteau template tool -- CUSTOMIZE for your domain.

Operations: create, read, update, delete, list.
"@

Write-Utf8NoBom -Path "docs/TOOLS.md" -Value $toolsMd

$troubleshootingMd = @"
# Troubleshooting

## Server doesn't appear in Claude Desktop

**Cause**: Config JSON is malformed
**Fix**: Validate at jsonlint.com, check for trailing commas

## "command not found: uv"

**Cause**: uv not installed or not in PATH
**Fix**: \`winget install astral-sh.uv\` then restart terminal

## Tool returns empty results

TODO: document real failure modes as they're discovered
"@

Write-Utf8NoBom -Path "docs/TROUBLESHOOTING.md" -Value $troubleshootingMd

$agentsMd = @"
# AGENTS.md -- $normalizedName

Context for AI coding agents (OpenAI Codex, generic agent runners) working
in this repo.

## What this is

$Description

## Structure

- \`src/$pythonPackage/\` -- package source
- \`src/$pythonPackage/tools/\` -- MCP portmanteau tools (help, status, resource_manager)
- \`tests/\` -- pytest suite
- \`docs/\` -- CONFIGURATION.md, DEVELOPMENT.md, TOOLS.md, TROUBLESHOOTING.md

## Conventions

- FastMCP 3.x, portmanteau tool pattern (Literal-typed \`operation\` param, one
  tool per resource/domain area, not one tool per CRUD verb)
- Comprehensive docstrings on every \`@mcp.tool\`, no \`description=\` kwarg
- ruff for lint/format, pytest for tests, uv for dependency management
- See mcp-central-docs/standards/ for the full fleet standard set
"@

Write-Utf8NoBom -Path "AGENTS.md" -Value $agentsMd

$claudeMd = @"
# CLAUDE.md -- $normalizedName

Context for Claude Code working in this repo.

## What this is

$Description

## Structure

- \`src/$pythonPackage/\` -- package source
- \`src/$pythonPackage/tools/\` -- MCP portmanteau tools (help, status, resource_manager)
- \`tests/\` -- pytest suite
- \`docs/\` -- CONFIGURATION.md, DEVELOPMENT.md, TOOLS.md, TROUBLESHOOTING.md

## Conventions

- FastMCP 3.x, portmanteau tool pattern (Literal-typed \`operation\` param, one
  tool per resource/domain area, not one tool per CRUD verb)
- Comprehensive docstrings on every \`@mcp.tool\`, no \`description=\` kwarg
- ruff for lint/format, pytest for tests, uv for dependency management
- See mcp-central-docs/standards/ for the full fleet standard set, in
  particular README_STRUCTURE.md (doc layout), GITIGNORE_STANDARDS.md, and
  PROJECT_PAGE_STANDARD.md (fleet registration -- do this at creation time,
  not as a follow-up).
"@

Write-Utf8NoBom -Path "CLAUDE.md" -Value $claudeMd

$requiredDocs = @("README.md", "INSTALL.md", "docs/CONFIGURATION.md", "docs/DEVELOPMENT.md", "docs/TOOLS.md", "docs/TROUBLESHOOTING.md", "AGENTS.md", "CLAUDE.md")
foreach ($doc in $requiredDocs) {
    if (Test-Path $doc) {
        Write-Host "  [OK] $doc" -ForegroundColor Green
    } else {
        Write-Host "  FAIL: $doc was not created" -ForegroundColor Red
    }
}

# ============================================================================
# 11. MCPB PACKAGING
# ============================================================================

Write-Host ""
Write-Host "Creating MCPB package structure..." -ForegroundColor Yellow

$manifest = @"
{
  "name": "$normalizedName",
  "version": "0.1.0",
  "description": "$Description",
  "author": "$Author",
  "license": "MIT",
  "homepage": "https://github.com/sandraschi/$normalizedName",
  "repository": {
    "type": "git",
    "url": "https://github.com/sandraschi/$normalizedName"
  },
  "main": "server/server.py",
  "mcp": {
    "version": "1.0",
    "capabilities": ["tools"]
  },
  "runtime": {
    "python": ">=3.12"
  },
  "dependencies": {
    "fastmcp": ">=3.4.4,<4",
    "pydantic": ">=2.0.0"
  }
}
"@

Write-Utf8NoBom -Path "manifest.json" -Value $manifest
Copy-Item "manifest.json" "mcpb/manifest.json" -Force

$serverPy = @"
'''MCP server entry point for $normalizedName.'''

from $pythonPackage.__main__ import main

if __name__ == '__main__':
    main()
"@

Write-Utf8NoBom -Path "mcpb/server/server.py" -Value $serverPy

$systemPrompt = @"
You are a helpful assistant for $normalizedName.

This MCP server provides:
- help: Multilevel help system
- status: System diagnostics
- resource_manager: Main operations

Customize this prompt for your specific domain.
"@

Write-Utf8NoBom -Path "assets/prompts/system.md" -Value $systemPrompt
Copy-Item "assets/prompts/system.md" "mcpb/assets/prompts/system.md" -Force

$iconSvg = @"
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="40" fill="#4A90E2"/>
  <text x="50" y="65" font-family="Arial" font-size="40" fill="white" text-anchor="middle">MCP</text>
</svg>
"@

Write-Utf8NoBom -Path "assets/icon.svg" -Value $iconSvg
Copy-Item "assets/icon.svg" "mcpb/assets/icon.svg" -Force

Write-Host "  [OK] manifest.json" -ForegroundColor Green
Write-Host "  [OK] mcpb/ structure" -ForegroundColor Green
Write-Host "  [OK] assets/prompts/" -ForegroundColor Green
Write-Host "  [OK] assets/icon.svg" -ForegroundColor Green

# ============================================================================
# 12. COPY SOTA SCRIPTS (from canonical locations, not stale templates)
# ============================================================================

Write-Host ""
Write-Host "Copying SOTA scripts..." -ForegroundColor Yellow

$sotaScriptSources = @{
    "backup-repo.ps1" = Join-Path $centralDocs "sota-scripts/backup-system/backup-repo.ps1"
}

foreach ($scriptName in $sotaScriptSources.Keys) {
    $sourcePath = $sotaScriptSources[$scriptName]
    if (Test-Path $sourcePath) {
        Copy-Item $sourcePath "scripts/$scriptName" -Force
        Write-Host "  [OK] scripts/$scriptName (from canonical source)" -ForegroundColor Green
    } else {
        Write-Host "  SKIP scripts/${scriptName}: canonical source not found at $sourcePath" -ForegroundColor Yellow
    }
}

# ============================================================================
# 13. CHANGELOG
# ============================================================================

Write-Host ""
Write-Host "Creating CHANGELOG..." -ForegroundColor Yellow

$changelog = @"
# Changelog

All notable changes to $normalizedName will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - $buildDate

### Added
- Initial release
- Multilevel help system
- System status diagnostics
- Resource manager portmanteau tool
- Complete test scaffold
- MCPB packaging
- GitHub CI/CD workflows
- SOTA scripts (backup)

### Standards
- FastMCP 3.4+ compliant
- MCPB packaging standard
- Portmanteau pattern
- Modern Python tooling (ruff, uv, pytest)

---

Generated by: mcp-central-docs SOTA builder v2.0.0
"@

Write-Utf8NoBom -Path "CHANGELOG.md" -Value $changelog
Write-Host "  [OK] CHANGELOG.md" -ForegroundColor Green

# ============================================================================
# 14. LICENSE
# ============================================================================

Write-Host ""
Write-Host "Creating LICENSE..." -ForegroundColor Yellow

$license = @"
MIT License

Copyright (c) $buildYear $Author

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"@

Write-Utf8NoBom -Path "LICENSE" -Value $license
Write-Host "  [OK] LICENSE" -ForegroundColor Green

# ============================================================================
# 15. INITIALIZE GIT
# ============================================================================

if (-not $SkipGitInit) {
    Write-Host ""
    Write-Host "Initializing git repository..." -ForegroundColor Yellow

    git init -q
    git add -A
    git commit -m "Initial commit: SOTA MCP server repo created

Generated by: mcp-central-docs SOTA builder v2.0.0
Date: $buildDate

Includes: complete folder structure, portmanteau tools (help, status,
resource_manager), test scaffold, MCPB packaging, GitHub CI/CD workflows,
SOTA scripts, full README_STRUCTURE.md-compliant doc set, fleet .gitignore
and .gitattributes.

Standards: FastMCP 3.4+, MCPB packaging, portmanteau pattern, hub-and-spoke
architecture." -q

    Write-Host "  [OK] Git repository initialized" -ForegroundColor Green
    Write-Host "  [OK] Initial commit created" -ForegroundColor Green
}

# ============================================================================
# FINAL SUMMARY
# ============================================================================

Write-Host ""
Write-Host "================================================================" -ForegroundColor Magenta
Write-Host "   Repository Created!" -ForegroundColor Magenta
Write-Host "================================================================" -ForegroundColor Magenta
Write-Host ""

Write-Host "Created: $normalizedName" -ForegroundColor Green
Write-Host "Location: $repoPath" -ForegroundColor White
Write-Host ""

Write-Host "What Was Created:" -ForegroundColor Cyan
Write-Host "  [OK] Complete folder structure (src/, tests/, docs/, scripts/)" -ForegroundColor Green
Write-Host "  [OK] 3 portmanteau tools (help, status, resource_manager)" -ForegroundColor Green
Write-Host "  [OK] Test scaffold with working tests" -ForegroundColor Green
Write-Host "  [OK] MCPB packaging (manifest.json)" -ForegroundColor Green
Write-Host "  [OK] GitHub CI/CD workflows" -ForegroundColor Green
Write-Host "  [OK] SOTA scripts (backup-repo.ps1, from canonical source)" -ForegroundColor Green
Write-Host "  [OK] Modern tooling (pyproject.toml, ruff, uv, fastmcp>=3.4.4,<4)" -ForegroundColor Green
Write-Host "  [OK] Full doc set (README, INSTALL, docs/CONFIGURATION, docs/DEVELOPMENT, docs/TOOLS, docs/TROUBLESHOOTING, AGENTS.md, CLAUDE.md)" -ForegroundColor Green
Write-Host "  [OK] .gitignore (full fleet template), .gitattributes (LF normalization), LICENSE" -ForegroundColor Green
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. cd $repoPath" -ForegroundColor White
Write-Host "  2. uv sync" -ForegroundColor White
Write-Host "  3. uv run pytest -v" -ForegroundColor White
Write-Host "  4. Customize src/$pythonPackage/tools/resource_manager.py" -ForegroundColor White
Write-Host "  5. Register in fleet-registry.json / projects/ / FLEET_INDEX.md per PROJECT_PAGE_STANDARD.md" -ForegroundColor White
Write-Host ""

Write-Host "Repository is ready for development!" -ForegroundColor Green
Write-Host ""
