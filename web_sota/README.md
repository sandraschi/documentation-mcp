# Frontend: SOTA Documentation Dashboard

A premium React-based Single Page Application (SPA) for interacting with the Documentation MCP Hub.

## Design Philosophy
- **Dark Mode Default**: Premium night-first aesthetics.
- **Glassmorphism**: Modern UI components with subtle transparency and gradients.
- **SOTA UI/UX**: Adheres to Alsergrund v14.0 standards (Vibrant colors, high-density telemetry).

## Technical Stack
- **Framework**: React 18+ via Vite.
- **Styling**: Tailwind CSS for rapid, low-friction design.
- **State Management**: React Context & Hooks for local store integration.

## Key Hubs
- **Search**: High-fidelity semantic search interface with score visualization.
- **Documents**: Interactive file explorer for repo-internal and federated documentation.
- **Settings**: Dynamic configuration for LLM endpoints (Ollama/LM Studio).
- **Tools**: Real-time analysis of the host MCP server tools and metadata.

## Ports & Orchestration
- **Frontend Port**: **10794**
- **Startup**: Use `./start.ps1` or `start.bat`. These scripts:
  1. Kill any zombie processes squatting on the ports.
  2. Start the Python backend (hidden).
  3. Start the Vite dev server.
- **Build**: `npm run build` generates a production bundle in `dist/`, which is automatically served by the Starlette backend.
