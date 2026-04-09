#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Validates FastMCP 2.14.1+ compliance in MCP server repositories

.DESCRIPTION
    Checks for critical FastMCP breaking changes and compliance issues:
    - run_standalone() usage (should be run_stdio_async())
    - description= parameters in @mcp.tool() decorators
    - Enhanced response patterns implementation
    - MCPB packaging standards
    - Security compliance

.PARAMETER Path
    Path to the MCP server repository to validate

.PARAMETER Fix
    Attempt to automatically fix common issues

.EXAMPLE
    .\validate-fastmcp-compliance.ps1 -Path "D:\Dev\repos\rustdesk-mcp"

.EXAMPLE
    .\validate-fastmcp-compliance.ps1 -Path "D:\Dev\repos\rustdesk-mcp" -Fix
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$Path,

    [switch]$Fix
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Initialize counters
$errors = 0
$warnings = 0
$fixed = 0

function Write-CheckResult {
    param(
        [string]$CheckName,
        [string]$Result,
        [string]$Details = "",
        [string]$FixSuggestion = ""
    )

    $script:errors += ($Result -eq "ERROR" ? 1 : 0)
    $script:warnings += ($Result -eq "WARNING" ? 1 : 0)

    $color = switch ($Result) {
        "PASS" { "Green" }
        "WARNING" { "Yellow" }
        "ERROR" { "Red" }
        default { "White" }
    }

    Write-Host "[$Result] $CheckName" -ForegroundColor $color
    if ($Details) {
        Write-Host "       $Details" -ForegroundColor Gray
    }
    if ($FixSuggestion -and $Fix) {
        Write-Host "       FIX: $FixSuggestion" -ForegroundColor Cyan
    }
}

function Test-RunStandaloneUsage {
    param([string]$RepoPath)

    $pythonFiles = Get-ChildItem -Path $RepoPath -Recurse -Include "*.py" -ErrorAction SilentlyContinue

    $foundIssues = $false
    foreach ($file in $pythonFiles) {
        $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
        if ($content -match "run_standalone\(\)") {
            $foundIssues = $true
            $lineNumber = ($content | Select-String "run_standalone\(\)" | Select-Object -First 1).LineNumber
            Write-CheckResult -CheckName "FastMCP Breaking Change" -Result "ERROR" -Details "Found run_standalone() in $($file.Name):$lineNumber" -FixSuggestion "Replace run_standalone() with run_stdio_async()"

            if ($Fix) {
                $newContent = $content -replace "run_standalone\(\)", "run_stdio_async()"
                Set-Content -Path $file.FullName -Value $newContent
                Write-Host "       FIXED: Replaced run_standalone() with run_stdio_async() in $($file.Name)" -ForegroundColor Green
                $script:fixed++
            }
        }
    }

    if (-not $foundIssues) {
        Write-CheckResult -CheckName "FastMCP Breaking Change" -Result "PASS" -Details "No run_standalone() calls found"
    }
}

function Test-ToolDescriptionParameters {
    param([string]$RepoPath)

    $pythonFiles = Get-ChildItem -Path $RepoPath -Recurse -Include "*.py" -ErrorAction SilentlyContinue

    $foundIssues = $false
    foreach ($file in $pythonFiles) {
        $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
        if ($content -match "@mcp\.tool\([^)]*description=") {
            $foundIssues = $true
            $lineNumber = ($content | Select-String "@mcp\.tool\([^)]*description=" | Select-Object -First 1).LineNumber
            Write-CheckResult -CheckName "Tool Documentation" -Result "ERROR" -Details "Found description= parameter in @mcp.tool() in $($file.Name):$lineNumber" -FixSuggestion "Remove description= parameter and ensure comprehensive docstring"
        }
    }

    if (-not $foundIssues) {
        Write-CheckResult -CheckName "Tool Documentation" -Result "PASS" -Details "No description= parameters found in @mcp.tool() decorators"
    }
}

function Test-MCPBManifest {
    param([string]$RepoPath)

    $manifestPath = Join-Path $RepoPath "manifest.json"
    if (-not (Test-Path $manifestPath)) {
        Write-CheckResult -CheckName "MCPB Packaging" -Result "ERROR" -Details "manifest.json not found" -FixSuggestion "Create manifest.json with MCPB 0.2 format"
        return
    }

    $manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json

    # Check manifest version
    if ($manifest.manifest_version -ne "0.2") {
        Write-CheckResult -CheckName "MCPB Packaging" -Result "WARNING" -Details "Manifest version should be '0.2'" -FixSuggestion "Update manifest_version to '0.2'"
    } else {
        Write-CheckResult -CheckName "MCPB Packaging" -Result "PASS" -Details "Correct manifest version (0.2)"
    }

    # Check server configuration
    if (-not $manifest.server.entry_point) {
        Write-CheckResult -CheckName "MCPB Packaging" -Result "ERROR" -Details "Missing server.entry_point in manifest.json"
    } else {
        Write-CheckResult -CheckName "MCPB Packaging" -Result "PASS" -Details "Server entry point configured"
    }
}

function Test-AssetsDirectory {
    param([string]$RepoPath)

    $assetsPath = Join-Path $RepoPath "mcpb\assets"
    if (-not (Test-Path $assetsPath)) {
        Write-CheckResult -CheckName "MCPB Assets" -Result "WARNING" -Details "mcpb/assets directory not found" -FixSuggestion "Create mcpb/assets directory with icon files"
        return
    }

    $iconFiles = Get-ChildItem -Path $assetsPath -Include "icon.*" -ErrorAction SilentlyContinue
    if ($iconFiles.Count -eq 0) {
        Write-CheckResult -CheckName "MCPB Assets" -Result "WARNING" -Details "No icon files found in mcpb/assets" -FixSuggestion "Add icon.svg or icon.png to mcpb/assets"
    } else {
        Write-CheckResult -CheckName "MCPB Assets" -Result "PASS" -Details "Icon files found in mcpb/assets"
    }
}

function Test-FastMCPVersion {
    param([string]$RepoPath)

    $pyprojectPath = Join-Path $RepoPath "pyproject.toml"
    if (-not (Test-Path $pyprojectPath)) {
        Write-CheckResult -CheckName "FastMCP Version" -Result "ERROR" -Details "pyproject.toml not found"
        return
    }

    $content = Get-Content $pyprojectPath -Raw
    if ($content -match "fastmcp>=2\.14\.1") {
        Write-CheckResult -CheckName "FastMCP Version" -Result "PASS" -Details "FastMCP 2.14.1+ specified in dependencies"
    } elseif ($content -match "fastmcp") {
        Write-CheckResult -CheckName "FastMCP Version" -Result "WARNING" -Details "FastMCP found but not 2.14.1+" -FixSuggestion "Update to fastmcp>=2.14.1,<2.15.0"
    } else {
        Write-CheckResult -CheckName "FastMCP Version" -Result "ERROR" -Details "FastMCP not found in dependencies" -FixSuggestion "Add fastmcp>=2.14.1,<2.15.0 to dependencies"
    }
}

function Test-EnhancedResponses {
    param([string]$RepoPath)

    $pythonFiles = Get-ChildItem -Path $RepoPath -Recurse -Include "*.py" -ErrorAction SilentlyContinue

    $foundEnhancedResponses = $false
    $foundRichSuccess = $false
    $foundRichError = $false

    foreach ($file in $pythonFiles) {
        $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue

        # Check for FastMCP 2.14.1+ enhanced patterns
        if ($content -match "execution_time.*recommendations|recovery_options.*diagnostic_info|suggested_fixes.*estimated_resolution_time") {
            $foundEnhancedResponses = $true
        }

        # Check for rich success responses
        if ($content -match "success.*True.*execution_time|quality_metrics.*recommendations") {
            $foundRichSuccess = $true
        }

        # Check for rich error responses
        if ($content -match "success.*False.*recovery_options|diagnostic_info.*suggested_fixes") {
            $foundRichError = $true
        }
    }

    if ($foundEnhancedResponses -and $foundRichSuccess -and $foundRichError) {
        Write-CheckResult -CheckName "Enhanced Responses" -Result "PASS" -Details "FastMCP 2.14.1+ enhanced response patterns found (success + error patterns)"
    } elseif ($foundEnhancedResponses) {
        Write-CheckResult -CheckName "Enhanced Responses" -Result "WARNING" -Details "Basic enhanced responses found, but missing rich success/error patterns" -FixSuggestion "Add complete FastMCP 2.14.1+ response patterns for rich dialogue support"
    } else {
        Write-CheckResult -CheckName "Enhanced Responses" -Result "ERROR" -Details "No FastMCP 2.14.1+ enhanced response patterns found" -FixSuggestion "Implement FastMCP 2.14.1+ enhanced response patterns for rich dialogue support"
    }
}

# Main validation
Write-Host "🔍 FastMCP 2.14.1+ Compliance Check" -ForegroundColor Cyan
Write-Host "Repository: $Path" -ForegroundColor Gray
Write-Host "Fix Mode: $($Fix ? 'Enabled' : 'Disabled')" -ForegroundColor Gray
Write-Host ("-" * 50) -ForegroundColor Gray

# Run all checks
Test-RunStandaloneUsage -RepoPath $Path
Test-ToolDescriptionParameters -RepoPath $Path
Test-MCPBManifest -RepoPath $Path
Test-AssetsDirectory -RepoPath $Path
Test-FastMCPVersion -RepoPath $Path
Test-EnhancedResponses -RepoPath $Path

# Summary
Write-Host ("-" * 50) -ForegroundColor Gray
Write-Host "📊 Summary:" -ForegroundColor White
Write-Host "   Errors: $errors" -ForegroundColor ($errors -gt 0 ? "Red" : "Green")
Write-Host "   Warnings: $warnings" -ForegroundColor ($warnings -gt 0 ? "Yellow" : "Green")

if ($Fix) {
    Write-Host "   Fixed: $fixed" -ForegroundColor ($fixed -gt 0 ? "Green" : "Gray")
}

if ($errors -gt 0) {
    Write-Host "`n❌ CRITICAL ISSUES FOUND - Fix before proceeding!" -ForegroundColor Red
    exit 1
} elseif ($warnings -gt 0) {
    Write-Host "`n⚠️  WARNINGS FOUND - Consider addressing for best practices" -ForegroundColor Yellow
    exit 0
} else {
    Write-Host "`n✅ ALL CHECKS PASSED - FastMCP 2.14.1+ compliant!" -ForegroundColor Green
    exit 0
}