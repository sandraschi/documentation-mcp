# Repair Start Scripts - Fleet SOTA Alignment (v1.0.0)
# This script scans D:\Dev\repos for start.ps1 files and repairs them to follow the premium SOTA standard.

$FleetRoot = "D:\Dev\repos"
$Scripts = Get-ChildItem -Path $FleetRoot -Filter "start.ps1" -Recurse -File | Where-Object { $_.FullName -notmatch "node_modules|\.venv|\.git" }

Write-Host "🚀 Starting Fleet-Wide Start Script Repair..." -ForegroundColor Cyan
Write-Host "🔍 Found $($Scripts.Count) scripts to audit." -ForegroundColor Gray

foreach ($script in $Scripts) {
    Write-Host "`n📝 Auditing: $($script.FullName)" -ForegroundColor Blue
    $content = Get-Content $script.FullName -Raw
    $originalContent = $content
    $changed = $false
    
    # 1. Inject/Fix Port Clearing Logic (MANDATORY SOTA)
    if ($content -notmatch "Get-NetTCPConnection -LocalPort") {
        Write-Host "  🛠️  Adding port-safety logic..." -ForegroundColor Yellow
        
        $PortSafetySnippet = @"
# --- SOTA PORT SAFETY START ---
if (`$Port) {
    Get-NetTCPConnection -LocalPort `$Port -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "🧹 Clearing zombie process on port `$Port (PID: `$($_.OwningProcess))..." -ForegroundColor Yellow
        Stop-Process -Id `$_.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}
# --- SOTA PORT SAFETY END ---
"@
        # Inject after PORT definition or at start of run logic
        if ($content -match "(`$Port\s*=\s*\d+)") {
            $content = $content -replace "(`$Port\s*=\s*\d+)", "`$1`n`n$PortSafetySnippet"
            $changed = $true
        }
    }

    # 2. Normalize Hardcoded Paths to Local Relative if possible, or robust absolute
    if ($content -match "D:\\Dev\\repos\\([a-zA-Z0-9_-]+)") {
        Write-Host "  🛠️  Normalizing project paths..." -ForegroundColor Yellow
        $content = $content -replace "D:\\Dev\\repos\\([a-zA-Z0-9_-]+)", "`$PSScriptRoot"
        $changed = $true
    }

    # 3. Premium SOTA Aesthetics (Header/Banner)
    if ($content -notmatch "Standardized SOTA") {
        Write-Host "  🛠️  Applying Premium SOTA aesthetics..." -ForegroundColor Yellow
        $Header = @"
# *********************************************************************************
# * SOTA Fleet Orchestration - Standardized Start System (v1.19.0)                *
# * Generated/Repaired by Antigravity on $(Get-Date -Format "yyyy-MM-dd")                  *
# *********************************************************************************
"@
        if ($content -notmatch "# \*\*\*\*\*") {
            $content = "$Header`n`n$content"
            $changed = $true
        }
    }

    if ($changed -and $content -ne $originalContent) {
        Set-Content $script.FullName $content -Encoding utf8
        Write-Host "  ✅ Repaired and Saved!" -ForegroundColor Green
    }
    else {
        Write-Host "  ⏭️  Skipped (Already SOTA or No Changes Needed)" -ForegroundColor Gray
    }
}

Write-Host "`n✨ Fleet Repair Complete!" -ForegroundColor Green
Write-Host "📊 Summary: Repaired $($Scripts.Count) files." -ForegroundColor Cyan
