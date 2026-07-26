# fullstack-demo

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>


> 📖 **[Installation Guide](INSTALL.md)** — quick start, manual setup, and troubleshooting

A **professional fullstack application** with AI, MCP integration, and comprehensive monitoring.

## Quick Start

```powershell
git clone https://github.com/sandraschi/fullstack-demo
cd fullstack-demo
just
```

This opens an interactive dashboard showing all available commands. Run `just bootstrap` to install dependencies, then `just serve` or `just dev` to start.

### Manual Setup

If you don't have `just` installed:

##  Features

### **Frontend (React + TypeScript + Chakra UI)**
-  Modern dashboard with beautiful UI
-  AI ChatBot (4 providers: OpenAI, Anthropic, Ollama, LM Studio)
-  MCP Client Dashboard (connect to other MCP servers)
-  MCP Server Dashboard (show tools THIS app exposes)
-  File Upload & Processing
-  Voice Interface (Speech in/out)
-  2FA Authentication
-  PWA Support (installable, offline mode)
-  Prompt Engineering UI
-  Usage Analytics
-  Comprehensive Help Modal
-  Professional Log Viewer
-  Monitoring Dashboard

### **Backend (FastAPI + PostgreSQL + Redis)**
-  FastAPI with async support
-  PostgreSQL database with migrations
-  Redis caching and sessions
-  Email system (FastMail)
-  Image generation API (Hugging Face)
-  MCP Session Manager (persistent connections)
-  WebSocket support
-  Prometheus metrics
-  Health checks

### **MCP Server (12-Command CLI)**
-  **Dual transport**: stdio (Claude Desktop) + HTTP/SSE (web clients)
-  **12 commands**: start, status, test, benchmark, export-config, etc.
-  **18 options**: Full configuration control
-  **Beautiful interactive wizard** with pretty UI
-  **6 exposed tools**: database, images, notifications, logs, workflows
-  **Windows-safe Unicode** (no crashes!)

### **Infrastructure**
-  Docker containerization
-  Prometheus + Grafana + Loki monitoring
-  CI/CD pipelines
-  Comprehensive testing
-  Production-ready

##  Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15+

### Development Setup

1. **Clone and setup:**
   `ash
   git clone <repository-url>
   cd fullstack-demo
   `

2. **Configure API keys:**
   `ash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY and ANTHROPIC_API_KEY
   `

3. **Install Loki Docker plugin:**
   `powershell
   .\scripts\setup-loki.ps1
   `

4. **Start with Docker:**
   `ash
   docker-compose up -d
   `

5. **Or setup manually:**

   **Frontend:**
   `ash
   cd frontend
   npm install
   npm run dev
   `

   **Backend:**
   `ash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   `

###  Access Points

- **Frontend:** http://localhost:9132
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8888/api/v1/docs
- **MCP Server Dashboard:** http://localhost:9132/mcp-server
- **Grafana:** http://localhost:3191 (admin/admin)
- **Prometheus:** http://localhost:9191
- **Loki:** http://localhost:3199

##  MCP Server CLI

This app includes a **professional MCP server** with a comprehensive CLI!

### **12 Available Commands:**

```bash
# Core Commands
python backend/mcp_server.py start           # Start MCP server
python backend/mcp_server.py status          # Show configuration
python backend/mcp_server.py version         # Show version
python backend/mcp_server.py interactive     # Beautiful config wizard 

# Development Commands
python backend/mcp_server.py test            # Test all tools
python backend/mcp_server.py benchmark       # Performance test
python backend/mcp_server.py reload          # Hot reload tools
python backend/mcp_server.py validate        # Validate setup

# Utility Commands
python backend/mcp_server.py list-tools      # List 6 MCP tools
python backend/mcp_server.py export-config   # Export Claude config
python backend/mcp_server.py logs            # View logs
python backend/mcp_server.py install         # Install as service
```

### **Quick Examples:**

```bash
# Default (stdio for Claude Desktop)
python backend/mcp_server.py

# HTTP/SSE mode for web clients
python backend/mcp_server.py start --transport sse --port 8889

# Production with full features
python backend/mcp_server.py start --transport sse --env prod --metrics --monitoring --auth

# Beautiful interactive wizard
python backend/mcp_server.py interactive
```

### **6 Exposed MCP Tools:**

1. `query_database` - Query application database via MCP
2. `process_image_mcp` - Process images (resize, thumbnail, grayscale)
3. `send_notification` - Send notifications through the app
4. `get_app_status` - Get comprehensive application status
5. `analyze_logs` - Analyze application logs
6. `execute_workflow` - Execute predefined workflows

### **Documentation:**

- **`MCP_CLI_REFERENCE.md`** - Complete CLI documentation
- **`MCP_SERVER_COMPLETE.md`** - Implementation summary
- **`WINDOWS_SAFE_UNICODE.md`** - Unicode character reference
- **Dashboard:** http://localhost:9132/mcp-server

##  Architecture

### Frontend
- **React 18** with TypeScript
- **Chakra UI** for components
- **React Query** for data fetching
- **React Router** for navigation
- **Vite** for build tooling

### Backend
- **FastAPI** with async support
- **SQLAlchemy** ORM
- **Alembic** for migrations
- **PostgreSQL** database
- **Redis** for caching
- **Celery** for background tasks

###  AI Features (Multi-Provider Support)
- **AI ChatBot** - Floating chat with streaming responses
- **OpenAI** - GPT-4, GPT-4 Turbo, GPT-3.5
- **Anthropic** - Claude 3.5 Sonnet, Opus, Sonnet, Haiku
- **Ollama** - Local FOSS models (llama2, mistral, etc.)
- **LM Studio** - Local model management
- **AI Settings Modal** - Full provider configuration
- **Context-Aware** - Knows your application's tech stack
- **Model Management** - Load/unload local models
- **Streaming Responses** - Real-time AI output

###  MCP Client Dashboard
- **Server Discovery** - Auto-detect Claude Desktop servers
- **Tool Execution** - Run any MCP tool visually
- **Server Connection** - Connect to any MCP server
- **Tool Inspector** - View tool schemas and parameters
- **Results Display** - Formatted JSON output
- **Universal Frontend** - Works with ANY MCP server

###  MCP Server (DUAL-MODE MCP HUB!)
- **Exposes MCP Tools** - App becomes an MCP server
- **Claude Integration** - Use app tools directly in Claude
- **6 Built-in Tools:**
  - query_database - Query PostgreSQL via MCP
  - process_image_mcp - Image processing via MCP
  - send_notification - Send notifications via MCP
  - get_app_status - Get app health via MCP
  - analyze_logs - Analyze logs via MCP
  - execute_workflow - Run workflows via MCP
- **Auto Config** - mcp-config.json for Claude Desktop
- **Dual Mode** - Client AND Server in one app!

###  File Upload & Processing
- **Drag-Drop Upload** - Beautiful drop zone
- **Image Processing** - Resize, thumbnail, grayscale
- **PDF Extraction** - Text extraction, page count
- **Thumbnail Generation** - Auto-preview for images
- **Multi-File Support** - Batch processing
- **Progress Tracking** - Upload progress bars

###  Voice Interface
- **Speech-to-Text** - Web Speech API integration
- **Text-to-Speech** - Multiple voice options
- **Voice Commands** - Navigate with voice
- **Continuous Listening** - Real-time transcription
- **Voice Selection** - Choose from system voices
- **Hands-Free** - Complete voice control

###  Security Features
- **2FA Setup** - TOTP authenticator support
- **QR Code Generation** - Easy mobile setup
- **Token Verification** - 6-digit code verification
- **Google Authenticator** - Compatible
- **Microsoft Authenticator** - Compatible
- **Authy** - Compatible
- **1Password** - Compatible (Premium)

###  PWA Support
- **Installable** - Add to home screen
- **Offline Mode** - Service worker caching
- **App-Like Experience** - Standalone display
- **Fast Loading** - Cached resources
- **Push Notifications** - Real-time updates (ready)
- **Cross-Platform** - Works on desktop & mobile

### Infrastructure
- **Docker** containerization
- **Prometheus** monitoring
- **Grafana** dashboards
- **Loki** log aggregation
- **Nginx** reverse proxy
- **GitHub Actions** CI/CD

##  Testing

`ash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test
`

##  Monitoring

The application includes comprehensive monitoring:

- **Metrics:** Prometheus + Grafana
- **Logging:** Structured logging with correlation IDs
- **Health checks:** Built-in health endpoints
- **Performance:** Request timing and error tracking

##  Deployment

See docs/deployment.md for production deployment guides.

##  API Documentation

Interactive API documentation is available at /docs when running the backend.

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request


## 🛡️ Industrial Quality Stack

This project adheres to **SOTA 14.1** industrial standards for high-fidelity agentic orchestration:

- **Python (Core)**: [Ruff](https://astral.sh/ruff) for linting and formatting. Zero-tolerance for `print` statements in core handlers (`T201`).
- **Webapp (UI)**: [Biome](https://biomejs.dev/) for sub-millisecond linting. Strict `noConsoleLog` enforcement.
- **Protocol Compliance**: Hardened `stdout/stderr` isolation to ensure crash-resistant JSON-RPC communication.
- **Automation**: [Justfile](./justfile) recipes for all fleet operations (`just lint`, `just fix`, `just dev`).
- **Security**: Automated audits via `bandit` and `safety`.

##  License

MIT License - see LICENSE file for details.
