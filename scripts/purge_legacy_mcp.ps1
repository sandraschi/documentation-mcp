# purge_legacy_mcp.ps1
$searchDir = "D:\Dev\repos\mcp-central-docs"
$legacyVersions = @("2.10", "2.11", "2.12", "2.13", "2.14")
$newVersion = "3.1.1+"

Write-Host "🚀 Starting Global Legacy Purge in $searchDir..."

# Use Get-ChildItem to find all .md files recursively
$mdFiles = Get-ChildItem -Path $searchDir -Filter "*.md" -Recurse

foreach ($file in $mdFiles) {
    if ($file.FullName -like "*node_modules*" -or $file.FullName -like "*dist*" -or $file.FullName -like "*toolbench*") {
        continue
    }

    $content = Get-Content -Path $file.FullName -Raw
    $modified = $false

    foreach ($v in $legacyVersions) {
        if ($content -match [regex]::Escape($v)) {
            $content = $content -replace [regex]::Escape($v), $newVersion
            $modified = $true
            Write-Host "✅ Purging $v from $($file.FullName)"
        }
    }

    if ($modified) {
        $content | Set-Content -Path $file.FullName -Encoding UTF8
    }
}

Write-Host "🎉 Purge Complete."
