# MemOps Webapp: Research Control Center

The MemOps Webapp is the primary visual interface for the **Advanced Memory MCP** ecosystem. It provides a premium, industrial-grade dashboard for managing autonomous research, semantic knowledge, and high-performance AI services.

## 🚀 Access & Deployment
- **Port**: `10704` (SOTA Standard)
- **Tech Stack**: React + Vite + Tailwind (SOTA Blueprint)
- **Deployment**: Local execution via `start.ps1` or Docker-orchestrated fleet.

## 🛠️ Core Features

### 1. Semantic Knowledge Graph
- **Visualization**: D3-based interactive graph of the SQLite/Markdown Zettelkasten.
- **RAG Inspector**: Real-time visualization of LanceDB retrieval paths and reranking scores.
- **Cross-Reference Hub**: Visual linkage between documents, code snippets, and research notes.

### 2. Autonomous Research Dashboard
- **Mission Control**: Start, monitor, and abort autonomous web-trawling missions.
- **Live Logs**: Real-time streaming of research agents as they gather data from arXiv, GitHub, and the web.
- **Synthesis Engine**: UI for triggering collaborative synthesis between multiple LLM providers.

### 3. Audio & Embodied Workspace
- **Voice Control**: Toggle for Whisper (STT) and Kokoro (TTS) engines.
- **Vbot Bridge**: Visualization of robot perception (if `robotics-mcp` is active).
- **Latency Monitoring**: Sub-100ms auditory loop visualization.

### 4. GPU Performance Monitor
- **RTX 4090 Metrics**: VRAM utilization, Temperature, and Flash Attention 2 throughput.
- **Inference Stats**: Real-time tracking of embedding generation and reranking latency.

## 🔗 Integration
The webapp communicates primarily via the **Bridge API (Port 10705)**, which acts as the gateway between the React frontend and the FastMCP substrate.

---
*Maintained by: Antigravity AI*
*Status: Production Ready*
