#!/usr/bin/env pwsh

Write-Host "🔍 Analyzing rustdesk-source directory sizes..." -ForegroundColor Cyan

$dirs = Get-ChildItem -Directory -ErrorAction SilentlyContinue | Sort-Object Name

foreach ($dir in $dirs) {
    try {
        $size = (Get-ChildItem $dir.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
        $sizeMB = [math]::Round($size / 1MB, 2)
        Write-Host "$($dir.Name.PadRight(30)) : $([math]::Round($sizeMB, 1).ToString().PadLeft(8)) MB" -ForegroundColor White
    }
    catch {
        Write-Host "$($dir.Name.PadRight(30)) : Error calculating size" -ForegroundColor Red
    }
}

Write-Host "`n🎯 Looking for specific large directories..." -ForegroundColor Yellow

# Check specific Rust/Cargo directories
$cargoDirs = @("target", ".cargo", "libs", "src", "flutter")
foreach ($dir in $cargoDirs) {
    if (Test-Path $dir) {
        try {
            $size = (Get-ChildItem $dir -Recurse -File -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
            $sizeMB = [math]::Round($size / 1MB, 2)
            Write-Host "$($dir.PadRight(30)) : $([math]::Round($sizeMB, 1).ToString().PadLeft(8)) MB" -ForegroundColor $(if ($sizeMB -gt 100) { "Red" } elseif ($sizeMB -gt 50) { "Yellow" } else { "Green" })
        }
        catch {
            Write-Host "$($dir.PadRight(30)) : Error calculating size" -ForegroundColor Red
        }
    }
}
