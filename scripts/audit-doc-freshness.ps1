# Documentation Freshness Audit Script
# Scans all markdown files for Last Updated dates and flags stale content

param(
    [int]$WarnDays = 30,
    [int]$ArchiveDays = 90,
    [switch]$Verbose = $false
)

Write-Host "📊 Documentation Freshness Audit" -ForegroundColor Cyan
Write-Host "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -ForegroundColor Gray
Write-Host "Warn threshold: $WarnDays days | Archive threshold: $ArchiveDays days" -ForegroundColor Gray
Write-Host ""

$stale = @()
$archived = @()
$current = @()
$missing = @()
$totalDocs = 0

# Scan all markdown files
Get-ChildItem -Path "docs" -Recurse -Filter "*.md" | ForEach-Object {
    $totalDocs++
    $relativePath = $_.FullName.Replace((Get-Location).Path + "\", "")
    $content = Get-Content $_.FullName -Raw
    
    # Check for Last Updated date
    if ($content -match '\*\*Last Updated:\*\*\s*(\d{4}-\d{2}-\d{2})') {
        $lastUpdated = [datetime]::Parse($Matches[1])
        $age = (Get-Date) - $lastUpdated
        
        # Check for Status marker
        $status = "UNKNOWN"
        if ($content -match '\*\*Status:\*\*\s*(\w+)') {
            $status = $Matches[1]
        }
        
        $docInfo = [PSCustomObject]@{
            File = $relativePath
            LastUpdated = $lastUpdated.ToString('yyyy-MM-dd')
            Age = $age.Days
            Status = $status
        }
        
        if ($age.Days -gt $ArchiveDays) {
            $archived += $docInfo
        }
        elseif ($age.Days -gt $WarnDays) {
            $stale += $docInfo
        }
        else {
            $current += $docInfo
        }
    }
    else {
        # No Last Updated date found
        $missing += [PSCustomObject]@{
            File = $relativePath
            Issue = "Missing 'Last Updated' header"
        }
    }
}

# Generate Report
Write-Host "=" * 80 -ForegroundColor Gray
Write-Host ""

# Summary
Write-Host "📈 Summary" -ForegroundColor Cyan
Write-Host "Total Documents: $totalDocs" -ForegroundColor White
Write-Host "✅ CURRENT (<$WarnDays days): $($current.Count)" -ForegroundColor Green
Write-Host "⚠️  OUTDATED ($WarnDays-$ArchiveDays days): $($stale.Count)" -ForegroundColor Yellow
Write-Host "🔴 ARCHIVED (>$ArchiveDays days): $($archived.Count)" -ForegroundColor Red
Write-Host "❓ MISSING DATE: $($missing.Count)" -ForegroundColor Magenta
Write-Host ""

# Archived docs (critical)
if ($archived.Count -gt 0) {
    Write-Host "=" * 80 -ForegroundColor Gray
    Write-Host "🔴 ARCHIVED DOCUMENTS (>$ArchiveDays days old)" -ForegroundColor Red
    Write-Host "These docs are likely OBSOLETE and should be reviewed/archived" -ForegroundColor Yellow
    Write-Host ""
    $archived | Sort-Object Age -Descending | Format-Table -AutoSize
}

# Stale docs (warning)
if ($stale.Count -gt 0) {
    Write-Host "=" * 80 -ForegroundColor Gray
    Write-Host "⚠️  OUTDATED DOCUMENTS ($WarnDays-$ArchiveDays days old)" -ForegroundColor Yellow
    Write-Host "These docs may have stale information - review and update" -ForegroundColor Gray
    Write-Host ""
    $stale | Sort-Object Age -Descending | Format-Table -AutoSize
}

# Missing dates (must fix)
if ($missing.Count -gt 0) {
    Write-Host "=" * 80 -ForegroundColor Gray
    Write-Host "❓ DOCUMENTS MISSING 'Last Updated' HEADER" -ForegroundColor Magenta
    Write-Host "Add standard header to these files" -ForegroundColor Gray
    Write-Host ""
    $missing | Format-Table -AutoSize
}

# Current docs (if verbose)
if ($Verbose -and $current.Count -gt 0) {
    Write-Host "=" * 80 -ForegroundColor Gray
    Write-Host "✅ CURRENT DOCUMENTS (<$WarnDays days old)" -ForegroundColor Green
    Write-Host ""
    $current | Sort-Object Age -Descending | Format-Table -AutoSize
}

# Version-specific warnings
Write-Host "=" * 80 -ForegroundColor Gray
Write-Host "🔍 Version-Specific Checks" -ForegroundColor Cyan
Write-Host ""

# Check for old FastMCP references
$oldFastMCP = Get-ChildItem -Path "docs" -Recurse -Filter "*.md" | 
    Select-String -Pattern "FastMCP 2\.(10|11|12)" -SimpleMatch:$false |
    Select-Object -ExpandProperty Path -Unique

if ($oldFastMCP) {
    Write-Host "⚠️  Found references to OLD FastMCP versions (<2.13):" -ForegroundColor Yellow
    $oldFastMCP | ForEach-Object {
        $rel = $_.Replace((Get-Location).Path + "\", "")
        Write-Host "   - $rel" -ForegroundColor Gray
    }
    Write-Host ""
}

# Check for old Flux references
$oldFlux = Get-ChildItem -Path "docs" -Recurse -Filter "*.md" | 
    Select-String -Pattern "Flux 1" |
    Select-Object -ExpandProperty Path -Unique

if ($oldFlux) {
    Write-Host "⚠️  Found references to OLD Flux 1 (superseded by Flux 2):" -ForegroundColor Yellow
    $oldFlux | ForEach-Object {
        $rel = $_.Replace((Get-Location).Path + "\", "")
        Write-Host "   - $rel" -ForegroundColor Gray
    }
    Write-Host ""
}

# Final status
Write-Host "=" * 80 -ForegroundColor Gray
Write-Host ""

if ($archived.Count -eq 0 -and $stale.Count -eq 0 -and $missing.Count -eq 0 -and -not $oldFastMCP -and -not $oldFlux) {
    Write-Host "✅ All documentation is FRESH and UP-TO-DATE!" -ForegroundColor Green
    Write-Host "   No action needed." -ForegroundColor Gray
} else {
    Write-Host "⚠️  Action Required:" -ForegroundColor Yellow
    if ($archived.Count -gt 0) {
        Write-Host "   - Review and archive $($archived.Count) old documents" -ForegroundColor Gray
    }
    if ($stale.Count -gt 0) {
        Write-Host "   - Update $($stale.Count) outdated documents" -ForegroundColor Gray
    }
    if ($missing.Count -gt 0) {
        Write-Host "   - Add headers to $($missing.Count) documents" -ForegroundColor Gray
    }
    if ($oldFastMCP) {
        Write-Host "   - Update FastMCP version references" -ForegroundColor Gray
    }
    if ($oldFlux) {
        Write-Host "   - Update Flux version references" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "💡 Tip: Run with -Verbose to see all current documents" -ForegroundColor Cyan
Write-Host ""

