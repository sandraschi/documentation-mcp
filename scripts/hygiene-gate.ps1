# Hygiene gate for public doc content.
#
# Scans a directory tree for patterns that must never ship in a public repo:
# machine-local paths, emails, API keys/tokens, and retired-tooling references.
# Exit code 0 = clean. Exit code 1 = hits found (report printed + saved).
#
# Usage:
#   .\scripts\hygiene-gate.ps1 -Path .\docs
#   .\scripts\hygiene-gate.ps1 -Path .\docs -ReportPath .\hygiene-report.txt

param(
    [Parameter(Mandatory = $true)]
    [string]$Path,

    [string]$ReportPath = (Join-Path $PSScriptRoot "..\hygiene-report.txt")
)

# Pattern source: mcp-central-docs/archive/retired-plans/WEED_MANIFEST.md §4
$Patterns = @(
    @{ Name = "windows-dev-path";   Regex = 'D:[\\/]Dev[\\/]' }
    @{ Name = "windows-user-path";  Regex = 'C:[\\/]Users[\\/]' }
    @{ Name = "dxt-reference";      Regex = '\bDXT\b|@anthropic/dxt|\.dxt\b' }
    @{ Name = "fastmcp-2x-floor";   Regex = 'FastMCP 2\.(1[0-9]|[0-9])\b' }
    @{ Name = "api-key-literal";    Regex = '\bapi_key\b\s*[:=]\s*["\x27][^"\x27\s]{8,}' }
    @{ Name = "openai-style-key";   Regex = '\bsk-[A-Za-z0-9]{16,}' }
    @{ Name = "github-pat";         Regex = '\bghp_[A-Za-z0-9]{20,}' }
    @{ Name = "email-address";      Regex = '[A-Za-z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.[A-Za-z]{2,}' }
)

if (-not (Test-Path $Path)) {
    Write-Host "ERROR: path not found: $Path" -ForegroundColor Red
    exit 1
}

$files = Get-ChildItem -Path $Path -Recurse -File -Include *.md, *.txt, *.json, *.ps1, *.py, *.ts, *.tsx
$hits = @()

foreach ($pattern in $Patterns) {
    $matches = $files | Select-String -Pattern $pattern.Regex -AllMatches
    foreach ($m in $matches) {
        $hits += [PSCustomObject]@{
            Pattern = $pattern.Name
            File    = $m.Path
            Line    = $m.LineNumber
            Text    = $m.Line.Trim()
        }
    }
}

if ($hits.Count -eq 0) {
    Write-Host "Hygiene gate: CLEAN - no hits across $($files.Count) files under $Path" -ForegroundColor Green
    exit 0
}

Write-Host "Hygiene gate: $($hits.Count) hit(s) found - fix or exclude before publishing" -ForegroundColor Red
$hits | Format-Table Pattern, File, Line -AutoSize | Out-String | Write-Host
$hits | Format-Table Pattern, File, Line, Text -AutoSize | Out-File -FilePath $ReportPath -Encoding utf8
Write-Host "Full report: $ReportPath"
exit 1
