# 🚀 SOTA Fullstack App Builder

**The Ultimate Web Application Generator**

> Build production-ready fullstack applications in minutes, not weeks!

## 🎯 What Is This?

A revolutionary PowerShell script that generates complete, enterprise-grade fullstack web applications with:

- **React/TypeScript Frontend** - Modern UI with Chakra
- **FastAPI Backend** - High-performance async API
- **Full Infrastructure** - Docker, PostgreSQL, Redis
- **AI Integration** - 4 providers (OpenAI, Anthropic, Ollama, LMStudio)
- **MCP Dual-Mode** - Client AND Server capabilities
- **Complete Monitoring** - Prometheus, Grafana, Loki
- **Security** - 2FA, Auth, RBAC ready
- **PWA Support** - Installable, offline-capable
- **Voice Interface** - Speech in/out
- **File Processing** - Images, PDFs
- **Interactive Selection** - Choose only what you need!

## 🌟 Key Features

### 📦 **11 Optional Features**

1. **🤖 AI ChatBot** - Multi-provider (OpenAI, Anthropic, Ollama, LMStudio)
2. **🔌 MCP Client** - Connect to any MCP server
3. **📁 File Upload** - Image/PDF processing
4. **🎤 Voice Interface** - Speech-to-text & text-to-speech
5. **🔐 2FA Auth** - TOTP authenticator support
6. **📱 PWA** - Installable, offline mode
7. **📊 Monitoring** - Prometheus + Grafana + Loki
8. **📈 Analytics** - Advanced dashboards
9. **📧 Email** - Service integration
10. **🔔 Real-time** - WebSocket support
11. **🌐 MCP Server** - Expose app as MCP server!

### 💼 **4 Quick Bundles**

- **A. Minimal** - Core only (FastAPI + React)
- **B. Standard** - Core + AI + 2FA + PWA + Monitoring
- **C. Enterprise** - Everything!
- **D. Custom** - Pick individual features

## 🚀 Quick Start

### Prerequisites

- PowerShell 7+
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- Git

### Installation

```powershell
# Interactive mode (recommended for first time)
.\new-fullstack-app.ps1 -AppName "MyAwesomeApp" -Interactive

# Enterprise bundle (all features)
.\new-fullstack-app.ps1 -AppName "MyApp" -Description "My awesome app"

# Minimal bundle (core only)
.\new-fullstack-app.ps1 -AppName "MyApp" -IncludeAI:$false -IncludeMCP:$false -IncludeMonitoring:$false

# Custom selection
.\new-fullstack-app.ps1 -AppName "MyApp" -IncludeAI:$true -IncludeVoice:$true -Include2FA:$true
```

### Running Your App

```powershell
cd MyAwesomeApp

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Install Loki plugin (one-time)
.\scripts\setup-loki.ps1

# Start everything
docker-compose up -d

# Access points
# Frontend: http://localhost:9132
# Backend: http://localhost:8000
# Grafana: http://localhost:3001 (admin/admin)
```

## 🏗️ What Gets Generated

### **Frontend (React/TypeScript)**
- 20+ Components (Dashboard, ChatBot, MCPDashboard, FileUpload, VoiceInterface, etc.)
- 10+ Routes with lazy loading
- Complete theme system (dark/light mode)
- PWA manifest + service worker
- Professional UI/UX

### **Backend (FastAPI)**
- 50+ API endpoints
- Multi-provider AI chat
- MCP client integration
- File processing (images, PDFs)
- 2FA authentication
- Prometheus metrics
- Full CORS, middleware

### **Infrastructure**
- Docker Compose (8 services)
- PostgreSQL database
- Redis cache
- Prometheus monitoring
- Grafana dashboards
- Loki log aggregation
- Nginx reverse proxy

### **MCP Server Mode**
- 6 exposed MCP tools
- Claude Desktop integration
- FastMCP-based implementation
- Auto-generated config

### **Scripts & Docs**
- Setup scripts (Loki, dev, build)
- Comprehensive README
- API documentation
- Deployment guides

## 🎮 Interactive Menu

When you use `-Interactive` flag:

```
╔══════════════════════════════════════════════════════════╗
║      🚀 FULLSTACK APP BUILDER - Feature Selection       ║
╚══════════════════════════════════════════════════════════╝

📦 CORE FEATURES (Always Included)
   ✓ FastAPI Backend + PostgreSQL + Redis
   ✓ React Frontend + TypeScript + Chakra UI
   ✓ Docker Setup + Basic Auth

Select features to include:
  1. 🤖 AI ChatBot (OpenAI, Anthropic, Ollama, LMStudio)
  2. 🔌 MCP Client Dashboard (Universal MCP Frontend)
  3. 📁 File Upload & Processing (Images/PDFs)
  4. 🎤 Voice Interface (Speech in/out)
  5. 🔐 2FA Authentication (TOTP)
  6. 📱 PWA Support (Offline, Installable)
  7. 📊 Full Monitoring (Prometheus, Grafana, Loki)
  8. 📈 Advanced Analytics Dashboard
  9. 📧 Email Service Integration
 10. 🔔 Real-time Features (WebSockets)
 11. 🌐 MCP SERVER (Expose app as MCP server!)

💼 QUICK BUNDLES:
  A. Minimal (Core only)
  B. Standard (Core + AI + 2FA + PWA + Monitoring)
  C. Enterprise (Everything!)
  D. Custom (Pick individual features)

Enter your choice [A/B/C/D]: _
```

## 🌐 MCP Server Mode

When enabled, your app exposes these tools to Claude and other MCP clients:

### **Available Tools:**

#### `query_database`
Query your application's PostgreSQL database
```json
{
  "query": "SELECT * FROM users WHERE active = true",
  "limit": 10
}
```

#### `process_image_mcp`
Process images through your app
```json
{
  "image_path": "/path/to/image.jpg",
  "operation": "resize",
  "width": 800,
  "height": 600
}
```

#### `get_app_status`
Get comprehensive app health and metrics
```json
{}
```

#### `analyze_logs`
Analyze application logs
```json
{
  "timeframe": "24h",
  "level": "error",
  "limit": 100
}
```

### **Setup in Claude Desktop:**

1. Run your app's MCP server:
   ```powershell
   cd MyApp
   .\scripts\run-mcp-server.ps1
   ```

2. Copy config from `mcp-config.json` to Claude Desktop config:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

3. Restart Claude Desktop

4. Use in Claude:
   ```
   "Query MyApp database for active users"
   "Process this image using MyApp"
   "Get MyApp status"
   ```

## 📚 Documentation

### **Generated Files:**
- `README.md` - Complete project documentation
- `docs/deployment.md` - Production deployment guide
- `mcp-config.json` - Claude Desktop configuration
- `.env.example` - Environment configuration

### **Architecture:**
- Microservices-ready backend
- Component-based frontend
- Containerized infrastructure
- Scalable design patterns

## 🧪 Testing

Every generated app includes:
- Backend tests (pytest)
- Frontend tests (Vitest)
- Integration tests
- API endpoint tests
- Component tests

## 🔧 Customization

### **Feature Flags:**
```powershell
-IncludeAI          # AI ChatBot
-IncludeMCP         # MCP Client Dashboard
-IncludeFileUpload  # File processing
-IncludeVoice       # Voice interface
-Include2FA         # 2FA auth
-IncludePWA         # PWA support
-IncludeMonitoring  # Full monitoring
-IncludeMCPServer   # MCP Server mode
```

### **Advanced Usage:**
```powershell
# Minimal app with just AI
.\new-fullstack-app.ps1 -AppName "ChatApp" `
  -IncludeAI:$true `
  -IncludeMCP:$false `
  -IncludeMonitoring:$false

# MCP-focused app
.\new-fullstack-app.ps1 -AppName "MCPHub" `
  -IncludeMCP:$true `
  -IncludeMCPServer:$true
```

## 🎯 Use Cases

### **1. SaaS Starter**
Choose: AI + 2FA + Monitoring + PWA
Perfect for: Customer-facing applications

### **2. MCP Service Hub**
Choose: MCP Client + MCP Server + File Upload
Perfect for: Integration platforms

### **3. Internal Tool**
Choose: Minimal + Voice + File Upload
Perfect for: Quick internal tools

### **4. Enterprise Platform**
Choose: Everything!
Perfect for: Production platforms

## 💡 Pro Tips

1. **Start Minimal** - Add features as you need them
2. **Use Interactive Mode** - See all options visually
3. **Read Generated README** - Each app has custom docs
4. **Check mcp-config.json** - Ready for Claude integration
5. **Customize Tools** - Edit `backend/mcp_server.py` to add your own MCP tools

## 🔮 What Makes This Special?

### **DUAL-MODE MCP HUB**
First builder to create apps that are BOTH:
- **MCP Client** - Use other MCP servers
- **MCP Server** - Be an MCP server

### **UNIVERSAL INTEGRATION**
- Connect your app to ANY MCP server
- Expose your app TO any MCP client
- Build MCP service meshes!

### **PRODUCTION-READY**
Not a toy - generates enterprise-grade code:
- Type safety (TypeScript)
- Async/await patterns
- Error handling
- Logging
- Monitoring
- Testing
- CI/CD
- Documentation

## 📊 Statistics

- **5,615 lines** of builder code
- **Generates 100+ files** per app
- **Saves weeks** of setup time
- **Zero config** needed (works out of box)
- **Fully documented**

## 🤝 Support

For issues or questions:
- Check generated `README.md` in your app
- Review `docs/` folder in generated app
- Consult PRD document for architecture details

## 📄 License

MIT License - Use freely for any purpose!

## 🎉 Get Started Now!

```powershell
.\new-fullstack-app.ps1 -AppName "MyFirstApp" -Interactive
```

Choose a bundle, watch the magic happen! ✨

---

**Built with ❤️ by the SOTA Builder Team**

