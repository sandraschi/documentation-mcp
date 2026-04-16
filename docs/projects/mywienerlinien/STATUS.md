# mywienerlinien - Status Report

**Last Updated:** 2025-11-25  
**Status:** Production-Ready  
**Source Repo:** `D:\Dev\repos\mywienerlinien`

---

## Overview

Vienna public transport application with dual-standard architecture: interactive web app with real-time vehicle tracking AND MCP server for AI assistant integration.

---

## Health Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Web Frontend | âœ… Healthy | Port 3079 |
| MCP Server | âœ… Healthy | 4 tools, FastMCP 3.1.1+ |
| GTFS Loader | âœ… Healthy | 25-50x faster |
| Grafana | âœ… Healthy | Port 3140 |
| PostgreSQL | âœ… Healthy | GTFS data |
| Loki | âœ… Healthy | Port 3193 |

---

## Dual Architecture

### ðŸŒ FastAPI Web Application
- **Port:** 3079
- **Features:**
  - Interactive map with real-time vehicle positions
  - Color-coded markers (U-Bahn, tram, bus)
  - Filter by type or line
  - Auto-refresh (15 seconds)
  - WebSocket updates
  - Responsive design
  - Commuter-friendly `/status` page

### ðŸ¤– FastMCP MCP Server
- **Transport:** stdio (Claude Desktop)
- **Location:** `frontend/mcp_server/`
- **FastMCP Version:** 3.1.1+ (current)
- **Tools (4):**
  - `next_departures` - Real-time departures
  - `station_search` - Fuzzy station search
  - `line_status` - Service disruptions
  - `journey_planner` - Route planning
- **Prompts (3):** AI guidance for transit queries
- **Resources (5):** Reference data (network, stations, fares)

---

## Performance Achievements

- **GTFS Loader:** 25-50x faster (13 hours â†’ 15-30 minutes)
- **Trigger optimization** - Disabled during bulk loads
- **Index management** - Created post-load
- **Bulk insert improvements** - Batch processing

---

## Endpoints

| Service | URL | Notes |
|---------|-----|-------|
| Frontend | http://localhost:3079 | Main app |
| Status Page | http://localhost:3079/status | Health check |
| Grafana | http://localhost:3140 | Monitoring |
| Loki | http://localhost:3193 | Logs |

---

## Data Sources

- **GTFS Static:** Wiener Linien schedule data
- **Realtime API:** Live vehicle positions via RBL monitors
- **Disruptions:** Service alerts and delays

---

## Technical Highlights

### Realtime Vehicle Feed
- Fully wired and operational
- RBL number enrichment for GTFS stops
- API call throttling to prevent rate limiting
- WebSocket push to connected clients

### Shared Backend
Both web and MCP interfaces use:
- `data_loader.py` - GTFS data loading and station management
- `database.py` - PostgreSQL database layer
- `vehicle_service.py` - Real-time vehicle data collection
- `disruption_alerts.py` - Service disruption monitoring

---

## Integration Points

- **Claude Desktop** - MCP server via stdio
- **Grafana** - Auto-loads operator dashboard on startup
- **Central Docs** - Pattern documented in `docs/projects/mywienerlinien/`

