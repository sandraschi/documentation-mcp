# Propagate SOTA .cursorrules to all repos in D:\Dev\repos
# This ensures all repos reference central documentation

$centralDocs = "D:\Dev\repos\mcp-central-docs"
$reposRoot = "D:\Dev\repos"
$cursorrulesSource = Join-Path $centralDocs "templates\.cursorrules"

if (-not (Test-Path $cursorrulesSource)) {
    Write-Error "Source .cursorrules not found at: $cursorrulesSource"
    exit 1
}

Write-Host "Propagating .cursorrules to all repos..." -ForegroundColor Cyan
Write-Host "Source: $cursorrulesSource" -ForegroundColor Gray
Write-Host ""

$repos = Get-ChildItem -Path $reposRoot -Directory | Where-Object {
    $_.Name -ne "mcp-central-docs" -and
    $_.Name -ne "junk" -and
    $_.Name -ne "temp" -and
    $_.Name -ne "external"
}

$copied = 0
$skipped = 0
$errors = 0

foreach ($repo in $repos) {
    $targetPath = Join-Path $repo.FullName ".cursorrules"
    
    try {
        # Check if .cursorrules already exists
        if (Test-Path $targetPath) {
            $existing = Get-Content $targetPath -Raw
            $new = Get-Content $cursorrulesSource -Raw
            
            # Only update if different
            if ($existing -ne $new) {
                Copy-Item -Path $cursorrulesSource -Destination $targetPath -Force
                Write-Host "✅ Updated: $($repo.Name)" -ForegroundColor Green
                $copied++
            } else {
                Write-Host "⏭️  Skipped (unchanged): $($repo.Name)" -ForegroundColor Yellow
                $skipped++
            }
        } else {
            Copy-Item -Path $cursorrulesSource -Destination $targetPath -Force
            Write-Host "✅ Created: $($repo.Name)" -ForegroundColor Green
            $copied++
        }
    } catch {
        Write-Host "❌ Error: $($repo.Name) - $($_.Exception.Message)" -ForegroundColor Red
        $errors++
    }
}

Write-Host ""
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Created/Updated: $copied" -ForegroundColor Green
Write-Host "  Skipped (unchanged): $skipped" -ForegroundColor Yellow
Write-Host "  Errors: $errors" -ForegroundColor $(if ($errors -gt 0) { "Red" } else { "Gray" })
Write-Host ""
Write-Host "Done! All repos now reference central documentation." -ForegroundColor Cyan

