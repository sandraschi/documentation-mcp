# Robust Monster Rehydrator 2.0
$monsterConfigPath = "D:\Dev\repos\monster_config.json"
if (-not (Test-Path $monsterConfigPath)) { Write-Error "Config not found!"; return }

$config = Get-Content $monsterConfigPath | ConvertFrom-Json
$paths = $config.mcpServers.PSObject.Properties | ForEach-Object { 
    if ($_.Value.args -contains "--directory") {
        $idx = [array]::IndexOf($_.Value.args, "--directory") + 1
        $_.Value.args[$idx]
    }
} | Select-Object -Unique

Write-Host "Found $($paths.Count) unique repos. Starting robust sync..." -ForegroundColor Cyan

foreach ($p in $paths) {
    if (-not (Test-Path $p)) { 
        Write-Host "[SKIP] Path missing: $p" -ForegroundColor Gray
        continue 
    }

    Write-Host "--- Syncing: $p ---" -ForegroundColor Yellow
    
    # Start-Job allows us to monitor the process and kill it if it hangs
    $job = Start-Job -ScriptBlock {
        param($dir)
        Set-Location $dir
        # Force a quiet sync with a fresh lock check
        & uv sync --frozen --no-install-project 2>&1
    } -ArgumentList $p

    # Wait up to 120 seconds for the repo to sync
    if (Wait-Job $job -Timeout 120) {
        $result = Receive-Job $job
        Write-Host "[SUCCESS] $p" -ForegroundColor Green
    } else {
        Write-Host "[TIMEOUT/FAIL] $p hung or took too long. Moving on..." -ForegroundColor Red
        Stop-Job $job
    }
    Remove-Job $job
}

Write-Host "Rehydration cycle complete." -ForegroundColor Cyan