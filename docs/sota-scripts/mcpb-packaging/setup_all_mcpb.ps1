# Script to set up MCPB packages for all MCP repos
# This script automates the creation of proper MCPB packages

param(
    [string]$Action = "setup",  # setup, build, or verify
    [string]$RepoFilter = "*"   # Filter repos by name pattern
)

# List of all MCP repos that need MCPB setup
$mcpRepos = @(
    "advanced-memory-mcp",
    "avatar-mcp",
    "beyondcompare-mcp",
    "blender-mcp",
    "bookmarks-mcp",
    "calibre-mcp",
    "database-operations-mcp",
    "davinci-resolve-mcp",
    "directmedia-mcp",
    "docker-mcp",
    "edge-bookmark-mcp-server",
    "email-mcp",
    "fastsearch-mcp",
    "filesystem-mcp",
    "gimp-mcp",
    "gtfs-mcp",
    "handbrake-mcp",
    "immich-mcp",
    "llm-txt-mcp",
    "local-llm-mcp",
    "mcp-server-template",
    "multi-backup-mcp",
    "nest-protect-mcp",
    "notepadpp-mcp",
    "obs-mcp",
    "observability-mcp",
    "obsidian-mcp",
    "ocr-mcp",
    "onenote-mcp",
    "osc-mcp",
    "pinokio-mcp",
    "plex-mcp",
    "pywinauto-mcp",
    "qbt-mcp",
    "reaper-mcp",
    "resolume-mcp",
    "resonite-mcp",
    "reversing-mcp",
    "ring-mcp",
    "robotics-mcp",
    "rustdesk-mcp",
    "suno-mcp",
    "system-admin-mcp",
    "tailscale-mcp",
    "tapo-camera-mcp",
    "unity3d-mcp",
    "virtualdj-mcp",
    "virtualization-mcp",
    "vrchat-mcp",
    "web-development-mcp",
    "windows-operations-mcp",
    "winrar-mcp"
)

function Create-McpbStructure {
    param([string]$RepoPath)

    $repoName = Split-Path $RepoPath -Leaf
    Write-Host "Setting up MCPB structure for $repoName..." -ForegroundColor Yellow

    # Create mcpb directory
    $mcpbDir = Join-Path $RepoPath "mcpb"
    if (!(Test-Path $mcpbDir)) {
        New-Item -ItemType Directory -Path $mcpbDir -Force | Out-Null
    }

    # Create src directory and copy source code
    $srcDir = Join-Path $mcpbDir "src"
    if (!(Test-Path $srcDir)) {
        New-Item -ItemType Directory -Path $srcDir -Force | Out-Null
    }

    # Copy source code if it exists
    $sourceSrc = Join-Path $RepoPath "src"
    if (Test-Path $sourceSrc) {
        # Find the main package directory
        $packageDirs = Get-ChildItem -Path $sourceSrc -Directory | Where-Object { $_.Name -like "*$($repoName.Replace('-mcp', '_mcp'))*" -or $_.Name -like "*$($repoName.Replace('mcp-', ''))*" }
        if ($packageDirs) {
            $packageDir = $packageDirs[0]
            Copy-Item -Path $packageDir.FullName -Destination $srcDir -Recurse -Force
            Write-Host "  Copied source code: $($packageDir.Name)" -ForegroundColor Green
        } else {
            Write-Host "  Warning: No matching source directory found" -ForegroundColor Yellow
        }
    }

    # Create assets structure
    $assetsDir = Join-Path $mcpbDir "assets"
    $promptsDir = Join-Path $assetsDir "prompts"
    $screenshotsDir = Join-Path $assetsDir "screenshots"

    New-Item -ItemType Directory -Path $assetsDir, $promptsDir, $screenshotsDir -Force | Out-Null

    # Create minimal icon.png (transparent 256x256 PNG)
    $iconPath = Join-Path $assetsDir "icon.png"
    if (!(Test-Path $iconPath)) {
        # Create minimal valid PNG data
        $pngSignature = [byte[]](0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A)
        $ihdrLength = [byte[]](0x00, 0x00, 0x00, 0x0D)
        $ihdrType = [byte[]](0x49, 0x48, 0x44, 0x52)
        $width = [byte[]](0x00, 0x00, 0x01, 0x00)  # 256
        $height = [byte[]](0x00, 0x00, 0x01, 0x00) # 256
        $ihdrData = $width + $height + [byte[]](0x08, 0x06, 0x00, 0x00, 0x00)
        $ihdrCrc = [byte[]](0x9a, 0x7b, 0x3c, 0x8e)
        $ihdrChunk = $ihdrLength + $ihdrType + $ihdrData + $ihdrCrc

        $idatLength = [byte[]](0x00, 0x00, 0x00, 0x0E)
        $idatType = [byte[]](0x49, 0x44, 0x41, 0x54)
        $idatData = [byte[]](0x78, 0x9c, 0xed, 0xc1, 0x01, 0x01, 0x00, 0x00, 0x00, 0x80, 0x90, 0xfe, 0x37, 0x10)
        $idatCrc = [byte[]](0x00, 0x00, 0x00, 0x00)
        $idatChunk = $idatLength + $idatType + $idatData + $idatCrc

        $iendChunk = [byte[]](0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xae, 0x42, 0x60, 0x82)

        $pngData = $pngSignature + $ihdrChunk + $idatChunk + $iendChunk
        [System.IO.File]::WriteAllBytes($iconPath, $pngData)
        Write-Host "  Created icon.png" -ForegroundColor Green
    }

    # Create prompt files
    $systemMd = Join-Path $promptsDir "system.md"
    $userMd = Join-Path $promptsDir "user.md"
    $examplesJson = Join-Path $promptsDir "examples.json"

    if (!(Test-Path $systemMd)) {
        @"
# $repoName System Prompt

You are an MCP server for $repoName. You provide specialized functionality for [describe what the server does].

## Core Capabilities

- Feature 1
- Feature 2
- Feature 3

Always provide clear, actionable guidance and explain technical concepts in simple terms.
"@ | Out-File -FilePath $systemMd -Encoding UTF8
        Write-Host "  Created system.md" -ForegroundColor Green
    }

    if (!(Test-Path $userMd)) {
        @"
# $repoName User Guide

## Getting Started

1. Install the MCPB package in Claude Desktop
2. Configure settings as needed
3. Start using the tools

## Common Workflows

### Basic Usage
```
1. Step 1
2. Step 2
3. Step 3
```

## Configuration

- Setting 1: Description
- Setting 2: Description

## Troubleshooting

- Issue 1: Solution
- Issue 2: Solution
"@ | Out-File -FilePath $userMd -Encoding UTF8
        Write-Host "  Created user.md" -ForegroundColor Green
    }

    if (!(Test-Path $examplesJson)) {
        @"
{
  "examples": [
    {
      "description": "Basic usage example",
      "commands": ["command1()", "command2()"],
      "expected_result": "Expected outcome"
    }
  ],
  "workflows": {
    "basic_workflow": [
      "Step 1",
      "Step 2",
      "Step 3"
    ]
  }
}
"@ | Out-File -FilePath $examplesJson -Encoding UTF8
        Write-Host "  Created examples.json" -ForegroundColor Green
    }

    # Create manifest.json
    $manifestPath = Join-Path $mcpbDir "manifest.json"
    if (!(Test-Path $manifestPath)) {
        $manifest = @{
            manifest_version = "0.2"
            name = $repoName
            version = "0.1.0"
            description = "MCP server for $repoName"
            author = @{
                name = "Sandra Schi"
                email = "sandra@example.com"
            }
            license = "MIT"
            repository = @{
                type = "git"
                url = "https://github.com/sandraschi/$repoName"
            }
            server = @{
                type = "python"
                entry_point = "src/$($repoName.Replace('-mcp', '_mcp'))/server.py"
                mcp_config = @{
                    command = "python"
                    args = @("src/$($repoName.Replace('-mcp', '_mcp'))/server.py")
                    env = @{
                        PYTHONPATH = "`${__dirname}/src"
                        PYTHONUNBUFFERED = "1"
                    }
                }
            }
        }

        $manifest | ConvertTo-Json -Depth 10 | Out-File -FilePath $manifestPath -Encoding UTF8
        Write-Host "  Created manifest.json" -ForegroundColor Green
    }

    Write-Host "MCPB structure setup complete for $repoName" -ForegroundColor Green
}

function Build-McpbPackage {
    param([string]$RepoPath)

    $repoName = Split-Path $RepoPath -Leaf
    $mcpbDir = Join-Path $RepoPath "mcpb"

    if (!(Test-Path $mcpbDir)) {
        Write-Host "No MCPB directory for $repoName, skipping" -ForegroundColor Yellow
        return
    }

    Write-Host "Building MCPB package for $repoName..." -ForegroundColor Yellow

    try {
        Push-Location $mcpbDir
        $distDir = Join-Path $RepoPath "dist"
        New-Item -ItemType Directory -Path $distDir -Force | Out-Null

        # Run MCPB pack
        $output = & mcpb pack . "../dist/$repoName.mcpb" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  Successfully built $repoName.mcpb" -ForegroundColor Green

            # Get package info
            $packagePath = Join-Path $distDir "$repoName.mcpb"
            if (Test-Path $packagePath) {
                $size = (Get-Item $packagePath).Length
                $sizeKB = [math]::Round($size / 1KB, 1)
                Write-Host "  Package size: $sizeKB KB" -ForegroundColor Cyan
            }
        } else {
            Write-Host "  Failed to build $repoName.mcpb" -ForegroundColor Red
            Write-Host "  Error: $output" -ForegroundColor Red
        }
    } catch {
        Write-Host "  Error building $repoName.mcpb : $($_.Exception.Message)" -ForegroundColor Red
    } finally {
        Pop-Location
    }
}

function Verify-McpbPackage {
    param([string]$RepoPath)

    $repoName = Split-Path $RepoPath -Leaf
    $distDir = Join-Path $RepoPath "dist"
    $packagePath = Join-Path $distDir "$repoName.mcpb"

    if (!(Test-Path $packagePath)) {
        Write-Host "$repoName.mcpb not found" -ForegroundColor Red
        return
    }

    Write-Host "Verifying $repoName.mcpb..." -ForegroundColor Yellow

    try {
        # Run MCPB verify
        $output = & mcpb verify $packagePath 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  Verification passed" -ForegroundColor Green
        } else {
            Write-Host "  Verification failed" -ForegroundColor Red
            Write-Host "  Error: $output" -ForegroundColor Red
        }

        # Check package contents
        $size = (Get-Item $packagePath).Length
        $sizeKB = [math]::Round($size / 1KB, 1)
        Write-Host "  Size: $sizeKB KB" -ForegroundColor Cyan

    } catch {
        Write-Host "  Error verifying $repoName.mcpb : $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Main execution
$reposDir = "D:\Dev\repos"
$filteredRepos = $mcpRepos | Where-Object { $_ -like $RepoFilter }

Write-Host "Processing $($filteredRepos.Count) MCP repos..." -ForegroundColor Cyan
Write-Host "Action: $Action" -ForegroundColor Cyan
Write-Host "Filter: $RepoFilter" -ForegroundColor Cyan
Write-Host ""

foreach ($repo in $filteredRepos) {
    $repoPath = Join-Path $reposDir $repo

    if (!(Test-Path $repoPath)) {
        Write-Host "Repository $repo not found, skipping" -ForegroundColor Yellow
        continue
    }

    switch ($Action) {
        "setup" {
            Create-McpbStructure -RepoPath $repoPath
        }
        "build" {
            Build-McpbPackage -RepoPath $repoPath
        }
        "verify" {
            Verify-McpbPackage -RepoPath $repoPath
        }
        default {
            Write-Host "Unknown action: $Action" -ForegroundColor Red
        }
    }

    Write-Host ""
}

Write-Host "Completed processing $($filteredRepos.Count) repos" -ForegroundColor Green
