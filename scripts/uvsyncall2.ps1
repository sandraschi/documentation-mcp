# uvsyncall2.ps1 - Robust & Flat structure
$root = "D:\Dev\repos"
$cachePath = "D:\.uv_cache"

# Ensure environment is primed
$env:UV_CACHE_DIR = $cachePath
Write-Host ">>> Targeting Cache: $cachePath" -ForegroundColor Cyan

# Find repos - Depth 2 is enough to find /repos/project-name/pyproject.toml
$repos = Get-ChildItem -Path $root -Filter "pyproject.toml" -Recurse -Depth 2

Write-Host ">>> Found $($repos.Count) repos. Starting sync..." -ForegroundColor Yellow

foreach ($file in $repos) {
    $repoPath = $file.DirectoryName
    Write-Host "`n[SYNCING] $repoPath" -ForegroundColor Magenta
    
    # Change directory manually to avoid Push/Pop nesting issues
    Set-Location $repoPath
    
    # Run uv sync directly. 
    # --frozen avoids changing your lockfiles while the cache is cold.
    & uv sync --frozen
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS" -ForegroundColor Green
    } else {
        Write-Warning "FAILED (Code $LASTEXITCODE)"
    }
}

Set-Location $root
Write-Host "`n>>> All toolchains processed." -ForegroundColor Cyan