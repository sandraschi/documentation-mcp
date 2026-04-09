# check_ports.ps1
# Checks the 10700-10800+ port range for active listeners (zombies/squatters).

$StartPort = 10700
$EndPort = 10850

Write-Host "🔍 Scanning MCP Port Range ($StartPort - $EndPort)..." -ForegroundColor Cyan

$Listeners = Get-NetTCPConnection -LocalPort ($StartPort..$EndPort) -ErrorAction SilentlyContinue

if ($null -eq $Listeners) {
    Write-Host "✅ No squatters detected in the range." -ForegroundColor Green
} else {
    Write-Host "⚠️ Active Listeners Found:" -ForegroundColor Yellow
    $Listeners | Select-Object LocalPort, OwningProcess, State | Format-Table -AutoSize
    
    foreach ($Conn in $Listeners) {
        $Proc = Get-Process -Id $Conn.OwningProcess -ErrorAction SilentlyContinue
        if ($Proc) {
            Write-Host "Port $($Conn.LocalPort) is held by: $($Proc.Name) (PID: $($Proc.Id))" -ForegroundColor Gray
        }
    }
}
