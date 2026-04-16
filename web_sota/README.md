# Frontend: SOTA Documentation Dashboard

A professional React-based interface for the Documentation MCP Hub, providing centralized access to fleet telemetry and project documentation.

## Navigational Hubs

| Hub | Description |
| :--- | :--- |
| **Fleet Dashboard** | Operational launcher for active MCP servers and ecosystem webapps. |
| **Project Portfolio** | Searchable index of all 100+ repositories with integrated "Deep Research" tools. |
| **Search (RAG)** | Federated semantic search interface for technical documentation. |
| **Persistence** | Visualization of stored memories via the `advanced-memory-mcp` integration. |
| **Docker Desktop** | Real-time monitoring of local container orchestration. |

## Technical Implementation
- **Architecture**: React 18 / Vite SPA.
- **Styling**: Tailwind CSS with glassmorphism design tokens.
- **Routing**: Component-based layout with deep-link support for research queries.

## Ports & Orchestration
- **Development Port**: **10794**
- **Production Port**: Served via the Python backend on **10795**.
- **Startup Logic**: 
    1. `./start.ps1` clears port squatters.
    2. Backend (Uvicorn/Starlette) initializes the vector store and registry.
    3. Frontend is served via Vite (dev) or Backend (production bundle).

## Development
```bash
npm install
npm run dev
```
For production testing, run `npm run build` and launch the Python server.
