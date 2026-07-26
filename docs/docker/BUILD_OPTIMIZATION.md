# Docker Build Optimization - Smart Caching Strategy

**Last Updated:** 2025-12-04  
**Status:** Superseded by DOCKER_DEV_GUIDE.md for development workflows

> **⚠️ NOTE:** For development workflows with hot-reload and volume mounts, see **[DOCKER_DEV_GUIDE.md](DOCKER_DEV_GUIDE.md)** instead.
> 
> This guide focuses on **build optimization** when you DO need to rebuild. For **avoiding rebuilds entirely** (the better approach), use hot-reload.

## Overview

Docker layer caching dramatically speeds up incremental builds during development. This guide documents best practices for optimizing Docker builds across all MCP repositories, reducing build times from minutes to seconds for code changes.

**However:** The BEST optimization is to **avoid rebuilding entirely** using hot-reload + volume mounts (see DOCKER_DEV_GUIDE.md).

## Problem

Using `--no-cache` for every build is slow and unnecessary. It forces a complete rebuild of all layers, including:
- System package installation (apt-get)
- Python package installation (pip)
- Source code copying

For incremental code changes, we only need to rebuild the source code layer.

## Solution: Smart Layer Caching

### Dockerfile Structure (Best Practice)

Order layers from least to most frequently changing:

```dockerfile
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

# 1. System dependencies (rarely change)
# This layer is cached unless system deps change
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 2. Copy requirements file (changes less frequently)
# This layer is cached unless requirements-docker.txt changes
COPY requirements-docker.txt /app/requirements-docker.txt

# 3. Install Python packages (changes when requirements change)
# This layer is cached unless requirements-docker.txt changes
RUN python -m pip install --upgrade pip \
 && pip install -r requirements-docker.txt

# 4. Copy source code last (changes most frequently)
# This layer invalidates cache on code changes, but previous layers stay cached
COPY . /app

EXPOSE 7777

ENTRYPOINT ["python", "-m", "tapo_camera_mcp.web.server"]
```

### Key Principles

1. **Copy requirements before source code** - Requirements change less frequently
2. **Install packages before copying code** - Package installation is slow, cache it
3. **Copy source code last** - Code changes most frequently, rebuild only this layer
4. **Combine RUN commands** - Reduces layer count (but don't over-optimize)

## Build Scripts

### Standard Build Script (`scripts/docker-build.ps1`)

```powershell
#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Build Docker containers with smart caching

.DESCRIPTION
    Builds Docker containers using layer caching for faster incremental builds.
    Use --no-cache only when you need a completely fresh build (e.g., after
    dependency changes or when debugging build issues).

.PARAMETER NoCache
    Force a complete rebuild without using cache (slower but ensures fresh build)

.PARAMETER Service
    Specific service to build (default: all services)

.EXAMPLE
    .\scripts\docker-build.ps1
    # Fast incremental build using cache

.EXAMPLE
    .\scripts\docker-build.ps1 -NoCache
    # Complete rebuild without cache (use when dependencies change)
#>

param(
    [switch]$NoCache = $false,
    [string]$Service = ""
)

$composeFile = "deploy/myhomecontrol/docker-compose.yml"

if (-not (Test-Path $composeFile)) {
    Write-Host "❌ Docker Compose file not found: $composeFile" -ForegroundColor Red
    exit 1
}

Write-Host "`n╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          🐳 Docker Build (Smart Caching) 🐳            ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

if ($NoCache) {
    Write-Host "⚠️  Building WITHOUT cache (slower but fresh)" -ForegroundColor Yellow
    Write-Host "   Use this when:" -ForegroundColor Gray
    Write-Host "   - Dependencies changed" -ForegroundColor Gray
    Write-Host "   - Debugging build issues" -ForegroundColor Gray
    Write-Host "   - Need completely fresh build`n" -ForegroundColor Gray
    $buildArgs = @("--no-cache")
} else {
    Write-Host "✅ Building WITH cache (faster incremental builds)" -ForegroundColor Green
    Write-Host "   Docker will reuse cached layers when possible`n" -ForegroundColor Gray
    $buildArgs = @()
}

if ($Service) {
    Write-Host "📦 Building service: $Service" -ForegroundColor Cyan
    $buildArgs += $Service
} else {
    Write-Host "📦 Building all services" -ForegroundColor Cyan
}

Write-Host ""

# Change to compose file directory
Push-Location (Split-Path $composeFile -Parent)

try {
    $buildStart = Get-Date
    
    if ($buildArgs.Count -gt 0) {
        docker compose -f (Split-Path $composeFile -Leaf) build @buildArgs
    } else {
        docker compose -f (Split-Path $composeFile -Leaf) build
    }
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n❌ Build failed!" -ForegroundColor Red
        exit $LASTEXITCODE
    }
    
    $buildDuration = (Get-Date) - $buildStart
    
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║              ✅ Build Complete! ✅                       ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "⏱️  Build time: $([math]::Round($buildDuration.TotalSeconds, 1))s" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "💡 Next steps:" -ForegroundColor White
    Write-Host "   docker compose -f deploy/myhomecontrol/docker-compose.yml up -d" -ForegroundColor Gray
    Write-Host ""
    
} finally {
    Pop-Location
}
```

### Quick Update Script (`scripts/docker-update.ps1`)

```powershell
#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Quick container update: rebuild and restart

.DESCRIPTION
    Rebuilds containers with cache (fast) and restarts them.
    Perfect for incremental code changes during development.

.EXAMPLE
    .\scripts\docker-update.ps1
    # Fast rebuild and restart
#>

$composeFile = "deploy/myhomecontrol/docker-compose.yml"

if (-not (Test-Path $composeFile)) {
    Write-Host "❌ Docker Compose file not found: $composeFile" -ForegroundColor Red
    exit 1
}

Write-Host "`n🔄 Quick container update (with cache)..." -ForegroundColor Cyan
Write-Host ""

# Change to compose file directory
Push-Location (Split-Path $composeFile -Parent)

try {
    $startTime = Get-Date
    
    # Build with cache (fast)
    Write-Host "📦 Building (using cache)..." -ForegroundColor Cyan
    docker compose -f (Split-Path $composeFile -Leaf) build
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n❌ Build failed!" -ForegroundColor Red
        exit $LASTEXITCODE
    }
    
    # Restart containers
    Write-Host "`n🚀 Restarting containers..." -ForegroundColor Cyan
    docker compose -f (Split-Path $composeFile -Leaf) up -d
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`n❌ Restart failed!" -ForegroundColor Red
        exit $LASTEXITCODE
    }
    
    $duration = (Get-Date) - $startTime
    
    Write-Host ""
    Write-Host "✅ Update complete in $([math]::Round($duration.TotalSeconds, 1))s!" -ForegroundColor Green
    Write-Host ""
    
} finally {
    Pop-Location
}
```

## When to Use `--no-cache`

### ✅ Use `--no-cache` when:
- **Dependencies changed** - `requirements-docker.txt` or `package.json` modified
- **System packages changed** - Dockerfile `RUN apt-get` commands modified
- **Base image changed** - `FROM` statement updated
- **Debugging build issues** - Suspect cached layer corruption
- **Production builds** - Some teams prefer fresh builds for releases

### ❌ Don't use `--no-cache` when:
- **Only source code changed** - Regular build is much faster
- **Incremental development** - Use cached layers for speed
- **Testing code changes** - No need to reinstall packages

## Performance Comparison

### With Cache (Incremental Code Change)
```
Layer 1: System deps      → CACHED (0s)
Layer 2: Requirements     → CACHED (0s)
Layer 3: Install packages → CACHED (0s)
Layer 4: Copy source      → REBUILD (2-5s)
Total: ~2-5 seconds
```

### Without Cache (Full Rebuild)
```
Layer 1: System deps      → REBUILD (30-60s)
Layer 2: Requirements     → REBUILD (0s)
Layer 3: Install packages → REBUILD (60-120s)
Layer 4: Copy source      → REBUILD (2-5s)
Total: ~90-185 seconds
```

**Speed improvement: 18-90x faster for incremental changes**

## Docker Compose Best Practices

### Remove Obsolete Fields

```yaml
# ❌ OLD (Docker Compose v2+)
version: '3.8'  # Obsolete, causes warnings

# ✅ NEW (Docker Compose v2+)
name: myhomecontrol  # Use 'name' instead
```

### Multi-Stage Builds (Advanced)

For even better caching, use multi-stage builds:

```dockerfile
# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements-docker.txt .
RUN pip install --user -r requirements-docker.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . /app
ENV PATH=/root/.local/bin:$PATH
```

## Repository-Specific Considerations

### Python Projects
- Use `requirements-docker.txt` for minimal production deps
- Keep `requirements.txt` for full dev dependencies
- Copy requirements before source code

### Node.js Projects
- Copy `package.json` and `package-lock.json` before source
- Run `npm ci` (not `npm install`) for reproducible builds
- Use `.dockerignore` to exclude `node_modules`

### Multi-Service Projects
- Build services independently when possible
- Use `docker compose build <service>` for single service updates
- Share base images across services

## .dockerignore Best Practices

Exclude files that change frequently but don't affect the build:

```
# Git
.git
.gitignore

# IDE
.vscode
.idea
*.swp

# Build artifacts
__pycache__
*.pyc
*.pyo
*.pyd
.Python

# Dependencies (if copying source)
node_modules
venv
env

# Dynamic data (GitLab, databases, etc.)
deploy/gitlab/data/
deploy/gitlab/logs/
*.db
*.sqlite

# Sensitive config
*.key
*.pem
*.env.local
```

## Troubleshooting

### Cache Not Working
- Check Dockerfile layer order
- Verify `.dockerignore` isn't excluding needed files
- Ensure requirements file is copied before source code

### Stale Cache Issues
- Use `--no-cache` to force fresh build
- Or `docker builder prune` to clear all build cache

### Build Context Too Large
- Improve `.dockerignore`
- Use multi-stage builds
- Consider `.dockerignore` patterns for large directories

## Implementation Checklist

For each repository:

- [ ] Review Dockerfile layer order (deps → requirements → code)
- [ ] Create `scripts/docker-build.ps1` with smart caching
- [ ] Create `scripts/docker-update.ps1` for quick updates
- [ ] Remove obsolete `version` field from docker-compose.yml
- [ ] Optimize `.dockerignore` for build context size
- [ ] Document when to use `--no-cache` in README
- [ ] Test incremental build performance

## Related Patterns

- **Multi-stage builds** - Further optimize image size and caching
- **BuildKit** - Enable with `DOCKER_BUILDKIT=1` for better caching
- **Layer optimization** - Combine RUN commands to reduce layers
- **Dependency management** - Separate dev and production requirements

## References

- [Docker Layer Caching Best Practices](https://docs.docker.com/build/cache/)
- [Docker Compose v2 Migration](https://docs.docker.com/compose/compose-file/compose-file-v3/)
- [.dockerignore Documentation](https://docs.docker.com/engine/reference/builder/#dockerignore-file)
- [Containerization Guidelines](./CONTAINERIZATION_GUIDELINES.md) - General containerization guidance

---

**Last Updated**: 2025-11-17  
**Related Documents**: [CONTAINERIZATION_GUIDELINES.md](./CONTAINERIZATION_GUIDELINES.md)

