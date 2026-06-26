# Homarr Integration Guide

**Status:** Active Deployment
**Stack Location:** `D:\Dev\repos\homarr` (or typical Docker deployment)
**Role:** Central Dashboard / "The Bridge"

## Overview

Homarr is the central command deck. It creates order from chaos by aggregating all services (Plex, Arrs, HA, Grafana) into a single, cohesive interface. It's not just a launcher; it's a status monitor and integration hub.

## Key Integrations

### 1. The Arr Stack ("The Crew")
Homarr connects directly to the API of each Arr service to show:
- **Sonarr/Radarr**: Upcoming releases calendar.
- **Lidarr**: Recent albums.
- **qBittorrent**: Active download speeds and progress bars directly on the dash.

**Configuration:**
- **Add App**: Select "Sonarr", enter `http://host.docker.internal:8989` and API key.
- **Widget**: Enable "Calendar" widget and select the Arr instances.

### 2. Plex Media Server ("The Treasure")
- Displays current streams (who is watching what).
- Recent library additions.
- Server health status.

### 3. System Stats (Glances/Dash.)
- Integrates with system monitoring to show CPU/RAM/Disk usage of the host machine (our 24-core Ryzen beast).

## Deployment Strategy
We run Homarr in the `management-stack` or alongside the `media-stack`.

```yaml
  homarr:
    container_name: homarr
    image: ghcr.io/ajnart/homarr:latest
    restart: unless-stopped
    volumes:
      - ./homarr/configs:/app/data/configs
      - ./homarr/icons:/app/public/icons
      - /var/run/docker.sock:/var/run/docker.sock # Optional: for container control
    ports:
      - 7575:7575
```

## "Morning Tide" Protocol 🌊
Check Homarr first thing in the morning (`http://localhost:7575`).
- **Red indicators**: Service down (Wake up the sysadmin).
- **Green indicators**: All systems nominal.
- **Calendar**: What shows dropped last night?

*One dashboard to rule them all.*
