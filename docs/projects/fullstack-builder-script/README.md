# SOTA Fullstack App Builder

This repository showcases the AI-generated PowerShell script that scaffolds a production-ready fullstack application. The script was produced during a single agentic coding session in Cursor to demonstrate what automated tooling can create end-to-end.

## Highlights
- Generates React + TypeScript + Chakra UI frontend
- Builds FastAPI backend with PostgreSQL, Redis, and Prometheus wiring
- Emits Docker Compose, monitoring stack, and helper scripts
- Includes MCP server CLI documentation and Windows-safe Unicode handling

## Usage
```powershell
# Run from the directory where you want the new project folder
.
\new-fullstack-app.ps1 -AppName "MyApp" [-OutputPath "C:\Projects"]
# -OutputPath is optional; when omitted the script writes to the current directory.
```

> **Note**: The generator assumes Windows with Docker Desktop available. A fresh `docker-compose up` smoke test is recommended after generation to validate the scaffold.

## Run the Generated App
```powershell
# From the generated project root (e.g., .\MyApp)
.\START.ps1
```

The starter script checks Docker Desktop, brings up the full stack with `docker-compose up -d`, waits a few seconds, and then launches the browser.

- Dashboard/UI: `http://localhost:9132`
- FastAPI backend: `http://localhost:8000`
- Grafana monitoring: `http://localhost:3001`

Stop the stack when you are done:
```powershell
# From the same project root
docker-compose down
```

## Provenance
- Script location: `new-fullstack-app.ps1`
- Source: AI-assisted session using Cursor
- Reference docs: `mcp-central-docs/FULLSTACK_BUILDER.md`

