# mywienerlinien - Directory Structure

**Last Updated:** 2025-11-25  
**Source Repo:** `D:\Dev\repos\mywienerlinien`

---

## Top-Level Layout

```
mywienerlinien/
â”œâ”€â”€ frontend/               # Main FastAPI application
â”‚   â”œâ”€â”€ app.py              # FastAPI web server
â”‚   â”œâ”€â”€ mcp_server/         # FastMCP server (4 tools)
â”‚   â”œâ”€â”€ data_loader.py      # GTFS data loading
â”‚   â”œâ”€â”€ database.py         # PostgreSQL layer
â”‚   â”œâ”€â”€ vehicle_service.py  # Real-time vehicle data
â”‚   â”œâ”€â”€ disruption_alerts.py # Service alerts
â”‚   â”œâ”€â”€ static/             # JS/CSS assets
â”‚   â””â”€â”€ templates/          # Jinja2 templates
â”œâ”€â”€ scripts/                # Data processing scripts
â”‚   â”œâ”€â”€ load_gtfs_to_db.py  # GTFS database loader
â”‚   â”œâ”€â”€ rbl_mapper.py       # RBL number mapping
â”‚   â”œâ”€â”€ gtfs_processor.py   # GTFS processing
â”‚   â””â”€â”€ gtfs_markdown_generator.py
â”œâ”€â”€ grafana/                # Grafana dashboards
â”‚   â””â”€â”€ provisioning/
â”œâ”€â”€ models/                 # SQLAlchemy models
â”œâ”€â”€ data/                   # Generated markdown data
â”œâ”€â”€ gtfs_data/              # GTFS SQLite cache
â”œâ”€â”€ db/                     # Database init scripts
â”œâ”€â”€ mcpb/                   # MCPB packaging
â”œâ”€â”€ docker-compose.yml      # Full stack
â”œâ”€â”€ docker-compose.logs.yml # Logging stack
â”œâ”€â”€ docs/                   # Documentation
â””â”€â”€ README.md               # Main docs
```

---

## Shared Backend Modules

Both web app and MCP server use:

| Module | Purpose |
|--------|---------|
| `data_loader.py` | GTFS data and station management |
| `database.py` | PostgreSQL layer |
| `vehicle_service.py` | Real-time vehicle collection |
| `disruption_alerts.py` | Service disruption monitoring |

---

## MCP Server (`frontend/mcp_server/`)

```
mcp_server/
â”œâ”€â”€ __init__.py
â”œâ”€â”€ server.py           # FastMCP server entry
â”œâ”€â”€ tools.py            # 4 transit tools
â”œâ”€â”€ prompts.py          # 3 AI prompts
â””â”€â”€ resources.py        # 5 reference resources
```

---

## Port Scheme

| Service | Port | Purpose |
|---------|------|---------|
| Frontend | 3079 | Web application |
| Grafana | 3140 | Monitoring |
| Loki (ext) | 3193 | Log access |
| PostgreSQL | 5432 | Internal |

---

## Tech Stack

- **Backend:** FastAPI, Python 3.11
- **MCP:** FastMCP 3.1.1+
- **Database:** PostgreSQL, SQLite (GTFS cache)
- **Frontend:** Jinja2, Vanilla JS, Leaflet maps
- **Monitoring:** Grafana, Loki, Promtail
- **Data:** GTFS, Wiener Linien API


