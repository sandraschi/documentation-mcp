# Unified Monitoring Stack Startup Script
# This script starts the unified monitoring stack that serves all MCP repositories

Write-Host "🚀 Starting Unified Monitoring Stack..." -ForegroundColor Green
Write-Host ""

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Host ports (from .env or defaults - never bind 3000/9090/3100 on the host)
function Get-UnifiedPort {
    param([string]$Name, [int]$Default)
    $fromEnv = [Environment]::GetEnvironmentVariable($Name)
    if ($fromEnv) { return [int]$fromEnv }
    if (Test-Path ".env") {
        foreach ($line in Get-Content ".env") {
            if ($line -match "^\s*$([regex]::Escape($Name))\s*=\s*(\d+)") {
                return [int]$Matches[1]
            }
        }
    }
    return $Default
}

$portGrafana = Get-UnifiedPort "UNIFIED_GRAFANA_HOST_PORT" 12000
$portPrometheus = Get-UnifiedPort "UNIFIED_PROMETHEUS_HOST_PORT" 12001
$portLoki = Get-UnifiedPort "UNIFIED_LOKI_HOST_PORT" 12002
$portPromtail = Get-UnifiedPort "UNIFIED_PROMTAIL_HOST_PORT" 12003
$portNodeExporter = Get-UnifiedPort "UNIFIED_NODE_EXPORTER_HOST_PORT" 12004
$portCadvisor = Get-UnifiedPort "UNIFIED_CADVISOR_HOST_PORT" 12005
$portBlackbox = Get-UnifiedPort "UNIFIED_BLACKBOX_HOST_PORT" 12006

# Host log mounts for Promtail (Windows Docker Desktop)
$userLocalShare = Join-Path $env:USERPROFILE ".local\share"
$userLocalShareDocker = ($userLocalShare -replace '\\', '/')
if (Test-Path ".env") {
    $envText = Get-Content ".env" -Raw
    if ($envText -notmatch 'FLEET_USER_LOCAL_SHARE=') {
        Add-Content ".env" "FLEET_USER_LOCAL_SHARE=$userLocalShareDocker"
    }
}
else {
    @"
FLEET_USER_LOCAL_SHARE=$userLocalShareDocker
"@ | Set-Content ".env" -Encoding utf8
}

# Check if Docker is running
try {
    docker version | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
}
catch {
    Write-Host "❌ Docker is not running. Please start Docker first." -ForegroundColor Red
    exit 1
}

# Create necessary directories
Write-Host "📁 Creating necessary directories..." -ForegroundColor Yellow
$directories = @(
    "grafana/dashboards",
    "grafana/provisioning/datasources",
    "grafana/provisioning/dashboards",
    "prometheus/rules",
    "loki/chunks",
    "loki/rules",
    "logs/mcp",
    "logs/myai",
    "logs/veogen",
    "logs/home",
    "logs/applications",
    "logs/errors",
    "logs/host/docs-mcp",
    "logs/host/devices-mcp",
    "logs/host/calibre-mcp",
    "logs/host/plex-mcp"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✅ Created: $dir" -ForegroundColor Green
    }
    else {
        Write-Host "  📁 Exists: $dir" -ForegroundColor Blue
    }
}

# Create Grafana provisioning configuration
Write-Host ""
Write-Host "🔧 Creating Grafana provisioning configuration..." -ForegroundColor Yellow

# Create datasources.yml
$datasourcesConfig = @"
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true

  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    editable: true
"@

$datasourcesConfig | Out-File -FilePath "grafana/provisioning/datasources/datasources.yml" -Encoding UTF8
Write-Host "  ✅ Created: grafana/provisioning/datasources/datasources.yml" -ForegroundColor Green

# Create dashboards.yml
$dashboardsConfig = @"
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards
"@

$dashboardsConfig | Out-File -FilePath "grafana/provisioning/dashboards/dashboards.yml" -Encoding UTF8
Write-Host "  ✅ Created: grafana/provisioning/dashboards/dashboards.yml" -ForegroundColor Green

# Copy unified configurations
Write-Host ""
Write-Host "📋 Copying unified configurations..." -ForegroundColor Yellow

# Prometheus: merge core + fleet (+ optional fleet.local)
$mergeScript = Join-Path $scriptDir "scripts\merge-prometheus-config.ps1"
if (Test-Path $mergeScript) {
    & $mergeScript -MonitoringDir $scriptDir
    Write-Host "  ✅ Merged: prometheus.core.yml + prometheus.fleet.yml → prometheus.yml" -ForegroundColor Green
}
elseif (Test-Path "prometheus/prometheus.core.yml") {
    Copy-Item "prometheus/prometheus.core.yml" "prometheus/prometheus.yml" -Force
    Write-Host "  ✅ Copied: Prometheus core only (no fleet merge script)" -ForegroundColor Green
}

# Copy Loki configuration
if (Test-Path "loki/loki.unified.yml") {
    Copy-Item "loki/loki.unified.yml" "loki/loki.yml" -Force
    Write-Host "  ✅ Copied: Loki unified configuration" -ForegroundColor Green
}

# Promtail: merge docker + host file targets
$mergePromtail = Join-Path $scriptDir "scripts\merge-promtail-config.ps1"
if (Test-Path $mergePromtail) {
    & $mergePromtail -MonitoringDir $scriptDir
    Write-Host "  ✅ Merged: promtail.unified.yml + promtail.host.yml → promtail.yml" -ForegroundColor Green
}
elseif (Test-Path "promtail/promtail.unified.yml") {
    Copy-Item "promtail/promtail.unified.yml" "promtail/promtail.yml" -Force
    Write-Host "  ✅ Copied: Promtail unified only" -ForegroundColor Green
}

# Start the unified monitoring stack
Write-Host ""
Write-Host "🚀 Starting unified monitoring stack..." -ForegroundColor Yellow

docker compose -p monitoring -f docker-compose.unified-monitoring.yml pull
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ docker compose pull failed (exit $LASTEXITCODE)" -ForegroundColor Red
    exit 1
}

docker compose -p monitoring -f docker-compose.unified-monitoring.yml up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ docker compose up failed (exit $LASTEXITCODE)" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Unified monitoring stack started successfully!" -ForegroundColor Green

# Wait for services to be ready
Write-Host ""
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check service status
Write-Host ""
Write-Host "📊 Checking service status..." -ForegroundColor Yellow

$services = @(
    @{Name = "Grafana"; Port = $portGrafana; URL = "http://localhost:$portGrafana/api/health" },
    @{Name = "Prometheus"; Port = $portPrometheus; URL = "http://localhost:$portPrometheus/-/ready" },
    @{Name = "Loki"; Port = $portLoki; URL = "http://localhost:$portLoki/ready" },
    @{Name = "Promtail"; Port = $portPromtail; URL = "http://localhost:$portPromtail/ready" },
    @{Name = "cAdvisor"; Port = $portCadvisor; URL = "http://localhost:$portCadvisor/healthz" }
)

foreach ($service in $services) {
    try {
        $response = Invoke-WebRequest -Uri $service.URL -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "  ✅ $($service.Name) is running on port $($service.Port)" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "  ⚠️  $($service.Name) is starting up on port $($service.Port)" -ForegroundColor Yellow
    }
}

# Display access information
Write-Host ""
Write-Host "🎉 Unified Monitoring Stack is ready!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Access URLs (host ports - see monitoring/.env.example):" -ForegroundColor Cyan
Write-Host "  • Grafana: http://localhost:$portGrafana (admin/admin)" -ForegroundColor White
Write-Host "  • Prometheus: http://localhost:$portPrometheus" -ForegroundColor White
Write-Host "  • Loki: http://localhost:$portLoki" -ForegroundColor White
Write-Host "  • Promtail: http://localhost:$portPromtail" -ForegroundColor White
Write-Host "  • cAdvisor: http://localhost:$portCadvisor" -ForegroundColor White
Write-Host "  • node-exporter: http://localhost:$portNodeExporter/metrics" -ForegroundColor White
Write-Host "  • blackbox: http://localhost:$portBlackbox" -ForegroundColor White
Write-Host "  • MCD RAG metrics: http://localhost:10795/metrics (when docs backend is running)" -ForegroundColor White
Write-Host ""
Write-Host "📱 Mobile Monitoring:" -ForegroundColor Cyan
Write-Host "  • RebootX App: Connect to http://localhost:12010" -ForegroundColor White
Write-Host "  • Grafana Mobile: http://localhost:$portGrafana" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Management Commands:" -ForegroundColor Cyan
Write-Host "  • Stop: docker compose -p monitoring -f docker-compose.unified-monitoring.yml down" -ForegroundColor White
Write-Host "  • Restart: docker compose -p monitoring -f docker-compose.unified-monitoring.yml restart" -ForegroundColor White
Write-Host "  • Logs: docker compose -p monitoring -f docker-compose.unified-monitoring.yml logs -f" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "  • Unified Monitoring Guide: ../UNIFIED_MONITORING_STACK.md" -ForegroundColor White
Write-Host "  • Central Documentation: ../../README.md" -ForegroundColor White
Write-Host ""

# Check if any MCP servers are running
Write-Host "🔍 Checking for running MCP servers..." -ForegroundColor Yellow
$mcpServices = docker ps --filter "label=service=mcp-server" --format "table {{.Names}}\t{{.Status}}" 2>$null
if ($mcpServices) {
    Write-Host "  ✅ Found running MCP servers:" -ForegroundColor Green
    Write-Host $mcpServices -ForegroundColor White
}
else {
    Write-Host "  ⚠️  No MCP servers detected. Start your MCP servers to see them in monitoring." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Start your MCP servers with monitoring enabled" -ForegroundColor White
Write-Host "  2. Access Grafana to view unified dashboards" -ForegroundColor White
Write-Host "  3. Set up RebootX mobile monitoring" -ForegroundColor White
Write-Host "  4. Configure alerts for critical services" -ForegroundColor White
Write-Host ""
Write-Host "✨ Happy Monitoring! 🚀" -ForegroundColor Green
