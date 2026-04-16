# veogen - Directory Structure

**Last Updated:** 2025-11-25  
**Source Repo:** `D:\Dev\repos\veogen`

---

## Top-Level Layout

```
veogen/
├── backend/                # FastAPI backend services
│   └── app/
│       ├── services/       # Business logic (video gen, MCP client)
│       └── api/            # API routes
├── frontend/               # React/Next.js frontend
├── monitoring/             # Prometheus/Grafana configs
├── docker-compose.yml      # Full stack orchestration
├── docker-compose.dev.yml  # Development override
├── docs/                   # Documentation
├── scripts/                # Utility scripts
├── config/                 # Configuration files
├── credentials/            # Secure credential storage
├── outputs/                # Generated video outputs
├── uploads/                # User uploads
└── README.md               # Main documentation
```

---

## Key Directories

### Backend (`backend/`)
- FastAPI application
- Video generation services
- MCP client integration
- User management APIs

### Frontend (`frontend/`)
- React/Next.js application
- Video generation UI
- Movie Maker interface
- User dashboard

### Monitoring (`monitoring/`)
- Prometheus configuration
- Grafana dashboards (4 dashboards)
- Alertmanager rules

---

## Port Scheme

| Service | Port | Purpose |
|---------|------|---------|
| Main App | 4710 | Frontend |
| API Backend | 4700 | REST API |
| User Manager | 8083 | Admin tool |
| Grafana | 4725 | Monitoring |
| Prometheus | 4740 | Metrics |
| Alertmanager | 4745 | Alerts |

---

## Tech Stack

- **Backend:** FastAPI, Python 3.11
- **Frontend:** React/Next.js, TypeScript
- **AI:** Google Veo AI (Veo 2 - March 2025 build, upgradeable to Veo 3)
- **Video Processing:** FFmpeg
- **Monitoring:** Prometheus, Grafana, Alertmanager
- **Database:** PostgreSQL
- **Auth:** JWT-based

---

## Google AI Context

**VeoGen was built March 2025 using Veo 2.**

**Veo 3 (May 2025)** added:
- Synchronized audio generation
- Dialogue, sound effects, ambient noise
- Cinema-quality output

**Gemini 3 (November 2025)** - See `docs/google-ecosystem/`

Upgrade path documented in STATUS.md.

