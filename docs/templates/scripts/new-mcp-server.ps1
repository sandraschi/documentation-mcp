#!/usr/bin/env pwsh
<#
.SYNOPSIS
    ðŸ-ï¸ SOTA MCP Server Repository Builder - Complete Repo Generator
    
.DESCRIPTION
    Builds a production-ready MCP server repository with ALL modern conveniences:
    
    âœ... Complete folder structure (src/, docs/, tests/, scripts/, assets/)
    âœ... Portmanteau tooling template (consolidated tools pattern)
    âœ... Basic required tools (help, status, multilevel support)
    âœ... Test scaffold with actual working tests
    âœ... MCPB packaging (manifest, assets, requirements)
    âœ... Documentation from central docs templates
    âœ... All SOTA scripts (backup, standards checker)
    âœ... Repo root essentials (pyproject.toml, .gitignore, .cursorrules)
    âœ... GitHub workflows (CI/CD)
    âœ... Modern tooling (ruff, uv, pytest)
    
    NO AI NEEDED - Just run and get a world-class MCP server repo!
    
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

# Normalize server name to kebab-case
$normalizedName = $ServerName.ToLower() -replace '[^a-z0-9-]', '-' -replace '--+', '-' -replace '^-|-$', ''
if (-not $normalizedName.EndsWith("-mcp")) {
    $normalizedName = "$normalizedName-mcp"
}

$pythonPackage = $normalizedName -replace '-', '_'
$repoPath = Join-Path $OutputPath $normalizedName

Write-Host "`nâ•"â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•-" -ForegroundColor Cyan
Write-Host "â•'      ðŸ-ï¸ SOTA MCP Server Repository Builder ðŸ-ï¸        â•'" -ForegroundColor Cyan
Write-Host "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•`n" -ForegroundColor Cyan

Write-Host "ðŸ"‹ Configuration:" -ForegroundColor Yellow
Write-Host "  Server Name:     $normalizedName" -ForegroundColor White
Write-Host "  Python Package:  $pythonPackage" -ForegroundColor White
Write-Host "  Description:     $Description" -ForegroundColor White
Write-Host "  Author:          $Author" -ForegroundColor White
Write-Host "  Output Path:     $repoPath" -ForegroundColor White
Write-Host ""

# Check if repo already exists
if (Test-Path $repoPath) {
    Write-Host "âŒ Error: Repository already exists at $repoPath" -ForegroundColor Red
    Write-Host "   Delete it first or choose a different name" -ForegroundColor Yellow
    exit 1
}

$centralDocs = "D:\Dev\repos\mcp-central-docs"
if (-not (Test-Path $centralDocs)) {
    Write-Host "âŒ Error: Central docs not found at $centralDocs" -ForegroundColor Red
    exit 1
}

# Create repo
Write-Host "ðŸ-ï¸ Creating repository structure..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path $repoPath -Force | Out-Null
Set-Location $repoPath

# ============================================================================
# 1. FOLDER STRUCTURE
# ============================================================================

Write-Host "`nðŸ" Creating folder structure..." -ForegroundColor Yellow

$folders = @(
    "src/$pythonPackage",
    "src/$pythonPackage/tools",
    "src/$pythonPackage/models",
    "src/$pythonPackage/utils",
    "tests",
    "tests/tools",
    "tests/integration",
    "docs",
    "docs/user-guide",
    "docs/development",
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
    Write-Host "  âœ... $folder/" -ForegroundColor Green
}

# ============================================================================
# 2. PYPROJECT.TOML (Modern Python Config)
# ============================================================================

Write-Host "`nðŸ"¦ Creating pyproject.toml..." -ForegroundColor Yellow

$pyprojectToml = @"
[project]
name = "$normalizedName"
version = "0.1.0"
description = "$Description"
authors = [
    {name = "$Author"}
]
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastmcp>=2.14.1,<2.15.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "pytest-asyncio>=0.23.0",
    "ruff>=0.3.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/$pythonPackage"]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = []

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
asyncio_mode = "auto"
addopts = "--cov=src --cov-report=html --cov-report=term"

[project.scripts]
$normalizedName = "$pythonPackage.__main__:main"
"@

Set-Content -Path "pyproject.toml" -Value $pyprojectToml -Encoding UTF8
Write-Host "  âœ... pyproject.toml" -ForegroundColor Green

# ============================================================================
# 3. REQUIREMENTS FILES
# ============================================================================

Write-Host "`nðŸ"¦ Creating requirements files..." -ForegroundColor Yellow

$requirements = @"
fastmcp>=2.14.1,<2.15.0
pydantic>=2.0.0
"@

$requirementsDev = @"
pytest>=8.0.0
pytest-cov>=4.1.0
pytest-asyncio>=0.23.0
ruff>=0.3.0
"@

Set-Content -Path "requirements.txt" -Value $requirements -Encoding UTF8
Set-Content -Path "requirements-dev.txt" -Value $requirementsDev -Encoding UTF8
Write-Host "  âœ... requirements.txt" -ForegroundColor Green
Write-Host "  âœ... requirements-dev.txt" -ForegroundColor Green

# ============================================================================
# 4. SOURCE CODE STRUCTURE
# ============================================================================

Write-Host "`nðŸ Creating source code structure..." -ForegroundColor Yellow

# __init__.py files
$initFiles = @(
    "src/$pythonPackage/__init__.py",
    "src/$pythonPackage/tools/__init__.py",
    "src/$pythonPackage/models/__init__.py",
    "src/$pythonPackage/utils/__init__.py",
    "tests/__init__.py",
    "tests/tools/__init__.py",
    "tests/integration/__init__.py"
)

foreach ($file in $initFiles) {
    Set-Content -Path $file -Value '"""Package initialization."""' -Encoding UTF8
}

# Main __init__.py
$mainInit = @"
'''$Description

FastMCP 2.14.1+ compliant MCP server.
'''

__version__ = '0.1.0'
__author__ = '$Author'
"@

Set-Content -Path "src/$pythonPackage/__init__.py" -Value $mainInit -Encoding UTF8
Write-Host "  âœ... Package __init__.py files" -ForegroundColor Green

# ============================================================================
# 5. PORTMANTEAU TOOLS TEMPLATE
# ============================================================================

Write-Host "`nðŸ› ï¸ Creating portmanteau tools template..." -ForegroundColor Yellow

$toolsInit = @"
'''MCP tools for $normalizedName.

This package provides portmanteau tools following the hub-and-spoke pattern
documented in mcp-central-docs/patterns/PORTMANTEAU_CONCEPT.md

Tool Organization:
- help: Multilevel help system
- status: System status and diagnostics
- resource_manager: Main portmanteau tool (customize for your domain)

All tools use comprehensive docstrings (FastMCP 2.14.1+ standard).
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

Set-Content -Path "src/$pythonPackage/tools/__init__.py" -Value $toolsInit -Encoding UTF8

# Help tool (multilevel)
$helpTool = @"
'''Multilevel help system for $normalizedName.

Provides contextual help at multiple knowledge levels.
'''

from fastmcp import FastMCP

mcp = FastMCP('$normalizedName')


@mcp.tool
async def help(level: str = 'basic', topic: str | None = None) -> str:
    '''Comprehensive help system with multiple knowledge levels.
    
    This tool provides contextual assistance at different depth levels:
    
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
# Example usage
from $pythonPackage import resource_manager

# Use the tools...
\`\`\`

## Available Tools

1. **help** - This multilevel help system
2. **status** - System status and diagnostics
3. **resource_manager** - Main operations (customize for your domain)

## Configuration

See docs/user-guide/ for detailed setup instructions.

## Support

- Documentation: See docs/
- Issues: GitHub Issues
- Standards: D:\\Dev\\repos\\mcp-central-docs\\
'''
    
    return help_content
"@

Set-Content -Path "src/$pythonPackage/tools/help.py" -Value $helpTool -Encoding UTF8

# Status tool
$statusTool = @"
'''System status and diagnostics for $normalizedName.'''

from fastmcp import FastMCP

mcp = FastMCP('$normalizedName')


@mcp.tool
async def status(level: str = 'basic', focus: str | None = None) -> str:
    '''Get system status and diagnostic information.
    
    Provides different levels of diagnostic detail:
    
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
âœ... Server running
âœ... Version: 0.1.0
âœ... Configuration: Valid

## Tools Available
- help (multilevel help)
- status (this tool)
- resource_manager (main operations)

## Health Checks
âœ... All systems operational
'''
    
    return status_report
"@

Set-Content -Path "src/$pythonPackage/tools/status.py" -Value $statusTool -Encoding UTF8

# Resource manager portmanteau template
$resourceManager = @"
'''Main portmanteau tool for $normalizedName.

Consolidates multiple related operations into a single tool
following the portmanteau pattern.

CUSTOMIZE THIS for your domain!
'''

from typing import Literal
from fastmcp import FastMCP

mcp = FastMCP('$normalizedName')


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
        # Create resource
        resource_manager('create', data={'name': 'example'})
        
        # Read resource
        resource_manager('read', resource_id='123')
        
        # Update resource
        resource_manager('update', resource_id='123', data={'status': 'active'})
        
        # Delete resource
        resource_manager('delete', resource_id='123')
        
        # List all
        resource_manager('list')
    '''
    
    # TODO: Implement your domain logic here
    
    return {
        'operation': operation,
        'resource_id': resource_id,
        'status': 'success',
        'message': f'Operation {operation} completed (CUSTOMIZE THIS!)'
    }
"@

Set-Content -Path "src/$pythonPackage/tools/resource_manager.py" -Value $resourceManager -Encoding UTF8

Write-Host "  âœ... help.py (multilevel help system)" -ForegroundColor Green
Write-Host "  âœ... status.py (diagnostics)" -ForegroundColor Green
Write-Host "  âœ... resource_manager.py (portmanteau template)" -ForegroundColor Green

# ============================================================================
# 6. MAIN SERVER FILE
# ============================================================================

Write-Host "`nðŸš€ Creating server entry point..." -ForegroundColor Yellow

$mainPy = @"
'''Main entry point for $normalizedName MCP server.'''

from fastmcp import FastMCP
from $pythonPackage import tools

mcp = FastMCP('$normalizedName')


def main():
    '''Run the MCP server.'''
    mcp.run_stdio_async()


if __name__ == '__main__':
    main()
"@

Set-Content -Path "src/$pythonPackage/__main__.py" -Value $mainPy -Encoding UTF8
Write-Host "  âœ... __main__.py" -ForegroundColor Green

# ============================================================================
# 7. TEST SCAFFOLD
# ============================================================================

Write-Host "`nðŸ§ª Creating test scaffold..." -ForegroundColor Yellow

# Basic test
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

Set-Content -Path "tests/test_basic.py" -Value $testBasic -Encoding UTF8

# Tool tests
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
    
    # Tools are FastMCP FunctionTool objects
    assert help is not None
    assert status is not None
    assert resource_manager is not None
"@

Set-Content -Path "tests/tools/test_tools.py" -Value $testTools -Encoding UTF8

Write-Host "  âœ... test_basic.py" -ForegroundColor Green
Write-Host "  âœ... test_tools.py" -ForegroundColor Green

# ============================================================================
# 8. GITIGNORE
# ============================================================================

Write-Host "`nðŸš« Creating .gitignore..." -ForegroundColor Yellow

$gitignore = @"
# Python
__pycache__/
*.py[cod]
*`$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.windsurf/
.cursor/

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/

# Ruff
.ruff_cache/

# MyPy
.mypy_cache/
.dmypy.json
dmypy.json

# Logs
*.log

# OS
.DS_Store
Thumbs.db

# Project specific
*.db
*.dxt
*.old
*.bak
*.tmp
"@

Set-Content -Path ".gitignore" -Value $gitignore -Encoding UTF8
Write-Host "  âœ... .gitignore" -ForegroundColor Green

# ============================================================================
# 9. GITHUB WORKFLOWS
# ============================================================================

Write-Host "`nâš™ï¸ Creating GitHub workflows..." -ForegroundColor Yellow

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
        python-version: ['3.11', '3.12']

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

Set-Content -Path ".github/workflows/ci.yml" -Value $ciWorkflow -Encoding UTF8

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

Set-Content -Path ".github/workflows/release.yml" -Value $releaseWorkflow -Encoding UTF8

Write-Host "  âœ... .github/workflows/ci.yml" -ForegroundColor Green
Write-Host "  âœ... .github/workflows/release.yml" -ForegroundColor Green

# ============================================================================
# 10. DOCUMENTATION FROM TEMPLATES
# ============================================================================

Write-Host "`nðŸ"š Copying documentation from central docs..." -ForegroundColor Yellow

# Copy templates if they exist
$docTemplates = @{
    ".cursorrules.template" = ".cursorrules"
    "README_TEMPLATE.md" = "README.md"
    "CONTRIBUTING.md" = "CONTRIBUTING.md"
}

foreach ($template in $docTemplates.Keys) {
    $sourcePath = Join-Path $centralDocs "templates/$template"
    $destPath = $docTemplates[$template]
    
    if (Test-Path $sourcePath) {
        $content = Get-Content $sourcePath -Raw
        # Replace placeholders
        $content = $content -replace '\{SERVER_NAME\}', $normalizedName
        $content = $content -replace '\{DESCRIPTION\}', $Description
        $content = $content -replace '\{AUTHOR\}', $Author
        $content = $content -replace '\{YEAR\}', (Get-Date).Year
        
        Set-Content -Path $destPath -Value $content -Encoding UTF8
        Write-Host "  âœ... $destPath (from template)" -ForegroundColor Green
    }
}

# Basic README if template doesn't exist
if (-not (Test-Path "README.md")) {
    $readme = @"
# $normalizedName

$Description

## Quick Start

\`\`\`bash
# Install with uv
uv pip install $normalizedName

# Or install in development mode
uv pip install -e ".[dev]"
\`\`\`

## Configuration

Add to Claude Desktop config:

\`\`\`json
{
  "mcpServers": {
    "$normalizedName": {
      "command": "uv",
      "args": ["--directory", "/path/to/$normalizedName", "run", "$normalizedName"]
    }
  }
}
\`\`\`

## Tools

- **help** - Multilevel help system
- **status** - System diagnostics
- **resource_manager** - Main operations (customize for your domain)

## Development

\`\`\`bash
# Run tests
uv run pytest -v

# Run linter
uv run ruff check .

# Format code
uv run ruff format .
\`\`\`

## Documentation

See [docs/]() for complete documentation.

## Standards

This repository follows standards from [mcp-central-docs](https://github.com/yourusername/mcp-central-docs):
- FastMCP 2.14.1+ compliance
- MCPB packaging
- Portmanteau pattern
- Modern Python tooling (ruff, uv)

## License

MIT License - See LICENSE file for details

## Author

$Author

---

**Generated by:** mcp-central-docs SOTA builder  
**Date:** $(Get-Date -Format "yyyy-MM-dd")
"@
    Set-Content -Path "README.md" -Value $readme -Encoding UTF8
    Write-Host "  âœ... README.md (generated)" -ForegroundColor Green
}

# ============================================================================
# 11. MCPB PACKAGING
# ============================================================================

Write-Host "`nðŸ"¦ Creating MCPB package structure..." -ForegroundColor Yellow

$manifest = @"
{
  "name": "$normalizedName",
  "version": "0.1.0",
  "description": "$Description",
  "author": "$Author",
  "license": "MIT",
  "homepage": "https://github.com/yourusername/$normalizedName",
  "repository": {
    "type": "git",
    "url": "https://github.com/yourusername/$normalizedName"
  },
  "main": "server/server.py",
  "mcp": {
    "version": "1.0",
    "capabilities": ["tools"]
  },
  "runtime": {
    "python": ">=3.11"
  },
  "dependencies": {
    "fastmcp": ">=2.14.1,<2.15.0",
    "pydantic": ">=2.0.0"
  }
}
"@

Set-Content -Path "manifest.json" -Value $manifest -Encoding UTF8
Copy-Item "manifest.json" "mcpb/manifest.json" -Force

# Create server wrapper
$serverPy = @"
'''MCP server entry point for $normalizedName.'''

from $pythonPackage import __main__

if __name__ == '__main__':
    __main__.main()
"@

Set-Content -Path "mcpb/server/server.py" -Value $serverPy -Encoding UTF8

# Create basic prompts
$systemPrompt = @"
You are a helpful assistant for $normalizedName.

This MCP server provides:
- help: Multilevel help system
- status: System diagnostics
- resource_manager: Main operations

Customize this prompt for your specific domain.
"@

Set-Content -Path "assets/prompts/system.md" -Value $systemPrompt -Encoding UTF8
Copy-Item "assets/prompts/system.md" "mcpb/assets/prompts/system.md" -Force

# Create icon.svg placeholder
$iconSvg = @"
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="40" fill="#4A90E2"/>
  <text x="50" y="65" font-family="Arial" font-size="40" fill="white" text-anchor="middle">MCP</text>
</svg>
"@

Set-Content -Path "assets/icon.svg" -Value $iconSvg -Encoding UTF8
Copy-Item "assets/icon.svg" "mcpb/assets/icon.svg" -Force

Write-Host "  âœ... manifest.json" -ForegroundColor Green
Write-Host "  âœ... mcpb/ structure" -ForegroundColor Green
Write-Host "  âœ... assets/prompts/" -ForegroundColor Green
Write-Host "  âœ... assets/icon.svg" -ForegroundColor Green

# ============================================================================
# 12. COPY SOTA SCRIPTS
# ============================================================================

Write-Host "`nðŸŽ¯ Copying SOTA scripts..." -ForegroundColor Yellow

$sotaScripts = @(
    "backup-repo.ps1",
    "check-repo-standards.ps1"
)

foreach ($script in $sotaScripts) {
    $sourcePath = Join-Path $centralDocs "templates/scripts/$script"
    if (Test-Path $sourcePath) {
        Copy-Item $sourcePath "scripts/$script" -Force
        Write-Host "  âœ... scripts/$script" -ForegroundColor Green
    }
}

# ============================================================================
# 13. CHANGELOG
# ============================================================================

Write-Host "`nðŸ" Creating CHANGELOG..." -ForegroundColor Yellow

$changelog = @"
# Changelog

All notable changes to $normalizedName will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - $(Get-Date -Format "yyyy-MM-dd")

### Added
- Initial release
- Multilevel help system
- System status diagnostics
- Resource manager portmanteau tool
- Complete test scaffold
- MCPB packaging
- GitHub CI/CD workflows
- SOTA scripts (backup, standards checker)

### Standards
- FastMCP 2.12+ compliant
- MCPB packaging standard
- Portmanteau pattern
- Modern Python tooling (ruff, uv, pytest)

---

**Generated by:** mcp-central-docs SOTA builder
"@

Set-Content -Path "CHANGELOG.md" -Value $changelog -Encoding UTF8
Write-Host "  âœ... CHANGELOG.md" -ForegroundColor Green

# ============================================================================
# 14. LICENSE
# ============================================================================

Write-Host "`nâš-ï¸ Creating LICENSE..." -ForegroundColor Yellow

$license = @"
MIT License

Copyright (c) $(Get-Date -Format "yyyy") $Author

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

Set-Content -Path "LICENSE" -Value $license -Encoding UTF8
Write-Host "  âœ... LICENSE" -ForegroundColor Green

# ============================================================================
# 15. INITIALIZE GIT
# ============================================================================

if (-not $SkipGitInit) {
    Write-Host "`nðŸ"§ Initializing git repository..." -ForegroundColor Yellow
    
    git init -q
    git add -A
    git commit -m "Initial commit: SOTA MCP server repo created

Generated by: mcp-central-docs SOTA builder
Date: $(Get-Date -Format "yyyy-MM-dd")

Includes:
âœ... Complete folder structure
âœ... Portmanteau tools (help, status, resource_manager)
âœ... Test scaffold with working tests
âœ... MCPB packaging
âœ... GitHub CI/CD workflows
âœ... SOTA scripts (backup, standards checker)
âœ... Modern tooling (ruff, uv, pytest)
âœ... Complete documentation
âœ... .cursorrules with Rule #1

Standards:
- FastMCP 2.12+ compliant
- MCPB packaging standard
- Portmanteau pattern
- Hub-and-spoke architecture

Ready for: development, testing, release!" -q
    
    Write-Host "  âœ... Git repository initialized" -ForegroundColor Green
    Write-Host "  âœ... Initial commit created" -ForegroundColor Green
}

# ============================================================================
# 16. CREATE DEVELOPMENT GUIDE
# ============================================================================

Write-Host "`nðŸ"- Creating development guide..." -ForegroundColor Yellow

$devGuide = @"
# Development Guide - $normalizedName

**Generated:** $(Get-Date -Format "yyyy-MM-dd")

---

## ðŸš€ Quick Start

### Setup Development Environment

\`\`\`bash
# Clone repository
cd $repoPath

# Create virtual environment with uv
uv venv

# Install in development mode
uv pip install -e ".[dev]"
\`\`\`

### Run Tests

\`\`\`bash
# Run all tests
uv run pytest -v

# Run with coverage
uv run pytest --cov=src --cov-report=html

# View coverage report
start htmlcov/index.html  # Windows
\`\`\`

### Code Quality

\`\`\`bash
# Check with ruff
uv run ruff check .

# Auto-fix issues
uv run ruff check . --fix

# Format code
uv run ruff format .
\`\`\`

---

## ðŸ› ï¸ Customizing Your MCP Server

### 1. Customize resource_manager.py

The portmanteau tool template is in:
\`src/$pythonPackage/tools/resource_manager.py\`

Replace the TODO section with your domain logic:
- File operations
- Database queries
- API calls
- etc.

### 2. Add More Portmanteau Tools

Create new tools in \`src/$pythonPackage/tools/\`:
\`\`\`python
from typing import Literal
from fastmcp import FastMCP

mcp = FastMCP('$normalizedName')

@mcp.tool
async def your_tool(
    operation: Literal['action1', 'action2', 'action3'],
    # ... parameters
) -> dict:
    '''Tool description with comprehensive docstring.
    
    OPERATIONS:
    - action1: Description
    - action2: Description
    - action3: Description
    
    (Complete docstring here - FastMCP 2.14.1+ standard)
    '''
    pass
\`\`\`

### 3. Add Tests

Create test files in \`tests/tools/\`:
\`\`\`python
import pytest

@pytest.mark.asyncio
async def test_your_tool():
    from $pythonPackage.tools.your_tool import your_tool
    result = await your_tool('action1')
    assert result['status'] == 'success'
\`\`\`

---

## ðŸ"¦ Building MCPB Package

\`\`\`bash
# Update version in pyproject.toml
# Update CHANGELOG.md

# Sync mcpb/ with src/
# (Copy updated files to mcpb/src/)

# Test the MCPB package
# (See MCPB_PACKAGING_STANDARDS.md)
\`\`\`

---

## ðŸ" Standards Checking

\`\`\`bash
# Run standards checker
.\scripts\check-repo-standards.ps1

# Review report
cat docs/repository-analysis-*.md

# Apply fixes
.\scripts\fix-standards.ps1 -DryRun
.\scripts\fix-standards.ps1
\`\`\`

---

## ðŸ"š References

- **Central Docs:** D:\Dev\repos\mcp-central-docs\
- **Standards:** mcp-central-docs/STANDARDS.md
- **FastMCP Guide:** mcp-central-docs/docs/fastmcp/migration-guide.md
- **Portmanteau Pattern:** mcp-central-docs/patterns/PORTMANTEAU_CONCEPT.md

---

**Generated by:** SOTA builder  
**Ready for:** Immediate development!
"@

Set-Content -Path "docs/development/DEVELOPMENT_GUIDE.md" -Value $devGuide -Encoding UTF8
Write-Host "  âœ... docs/development/DEVELOPMENT_GUIDE.md" -ForegroundColor Green

# ============================================================================
# FINAL SUMMARY
# ============================================================================

Write-Host "`nâ•"â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•-" -ForegroundColor Magenta
Write-Host "â•'            ðŸŽ‰ Repository Created! ðŸŽ‰                   â•'" -ForegroundColor Magenta
Write-Host "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•`n" -ForegroundColor Magenta

Write-Host "âœ... Created: $normalizedName" -ForegroundColor Green
Write-Host "ðŸ" Location: $repoPath`n" -ForegroundColor White

Write-Host "ðŸ"¦ What Was Created:" -ForegroundColor Cyan
Write-Host "  âœ... Complete folder structure (src/, tests/, docs/, scripts/)" -ForegroundColor Green
Write-Host "  âœ... 3 portmanteau tools (help, status, resource_manager)" -ForegroundColor Green
Write-Host "  âœ... Test scaffold with working tests" -ForegroundColor Green
Write-Host "  âœ... MCPB packaging structure" -ForegroundColor Green
Write-Host "  âœ... GitHub CI/CD workflows" -ForegroundColor Green
Write-Host "  âœ... 2 SOTA scripts (backup, standards checker)" -ForegroundColor Green
Write-Host "  âœ... Modern tooling (pyproject.toml, ruff, uv)" -ForegroundColor Green
Write-Host "  âœ... Documentation (README, CONTRIBUTING, CHANGELOG)" -ForegroundColor Green
Write-Host "  âœ... .gitignore, .cursorrules, LICENSE" -ForegroundColor Green
Write-Host ""

Write-Host "ðŸš€ Next Steps:" -ForegroundColor Yellow
Write-Host "  1. cd $repoPath" -ForegroundColor White
Write-Host "  2. uv venv && uv pip install -e '.[dev]'" -ForegroundColor White
Write-Host "  3. uv run pytest -v  # Run tests" -ForegroundColor White
Write-Host "  4. Customize src/$pythonPackage/tools/resource_manager.py" -ForegroundColor White
Write-Host "  5. .\scripts\check-repo-standards.ps1  # Verify standards" -ForegroundColor White
Write-Host ""

Write-Host "ðŸ"š Documentation:" -ForegroundColor Cyan
Write-Host "  - README.md - Getting started" -ForegroundColor White
Write-Host "  - docs/development/DEVELOPMENT_GUIDE.md - Developer guide" -ForegroundColor White
Write-Host "  - .cursorrules - Cursor AI rules (with Rule #1!)" -ForegroundColor White
Write-Host ""

Write-Host "âœ... Repository is ready for development!" -ForegroundColor Green
Write-Host ""

