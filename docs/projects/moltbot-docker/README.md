# Moltbot Docker - Quick Start

Run Moltbot Gateway in Docker for local experimentation.

## Prerequisites

- Docker + Docker Compose
- Node 22+ (for local CLI use; container has Node 22)

## Option A: Build from source (recommended for latest)

```powershell
cd D:\Dev\repos\moltbot-docker

# Generate token
$token = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
Write-Host "MOLTBOT_GATEWAY_TOKEN=$token"
New-Item -ItemType File -Path .env -Force
Set-Content -Path .env -Value "MOLTBOT_GATEWAY_TOKEN=$token"
Add-Content -Path .env -Value "MOLTBOT_GATEWAY_PORT=18789"
Add-Content -Path .env -Value "MOLTBOT_GATEWAY_BIND=loopback"

# Build and run
docker compose build
docker compose up -d

# Onboard (first-time config)
docker compose run --rm moltbot-gateway node dist/index.js onboard --no-install-daemon
```

## Option B: Use prebuilt image (when available)

Edit `docker-compose.yml`: replace `build:` with:

```yaml
image: ghcr.io/moltbot/moltbot:latest
```

Then remove the Dockerfile and run `docker compose up -d`.

## After Start

- **Gateway**: ws://127.0.0.1:18789
- **Control UI**: Served from Gateway (see docs for URL when bound to loopback)
- **moltbot-mcp**: Point `MOLTBOT_MCP_GATEWAY_HOST=host.docker.internal` if MCP runs on host

## Onboarding (channels, providers)

```powershell
# Interactive onboard
docker compose run --rm moltbot-gateway node dist/index.js onboard --no-install-daemon

# Add Telegram
docker compose run --rm moltbot-gateway node dist/index.js channels login --provider telegram
```

## Volumes

- `moltbot-config`: ~/.clawdbot (config, credentials)
- `moltbot-workspace`: Agent workspace, skills

## Docs

- https://docs.molt.bot
- https://docs.clawd.bot/install/docker
- https://github.com/moltbot/moltbot
