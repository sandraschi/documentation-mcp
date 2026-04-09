$repos = Get-ChildItem "D:\Dev\repos" -Directory
$report = @()

foreach ($repo in $repos) {
    $startScripts = Get-ChildItem $repo.FullName -Filter "start.ps1" -Recurse
    foreach ($script in $startScripts) {
        $content = Get-Content $script.FullName -Raw
        
        # Extract WebPort
        $webPort = if ($content -match '\$WebPort\s*=\s*(\d+)') { $Matches[1] } else { "Unknown" }
        
        # Check for Backend Startup
        $hasBackend = $content -match 'uvicorn|python -m|Start-Process.*backend'
        
        # Check for $pid collision
        $hasPidCollision = $content -match 'foreach\s*\(\$pid' -or $content -match '\$pid\s*='
        
        $report += [PSCustomObject]@{
            Repo        = $repo.Name
            ScriptPath  = $script.FullName.Replace("D:\Dev\repos\", "")
            WebPort     = $webPort
            BackendSync = $hasBackend
            PidStable   = -not $hasPidCollision
        }
    }
}

$report | Export-Csv -Path "D:\Dev\repos\mcp-central-docs\operations\startup_audit_report.csv" -NoTypeInformation
$report | Format-Table -AutoSize
