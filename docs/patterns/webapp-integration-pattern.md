# Webapp Integration Pattern

**Last Updated:** 2025-12-29

**Pattern for integrating MCP servers with web frontends (React, Vue, etc.)**

---

## Overview

This pattern describes how to build web applications that integrate with MCP servers, providing a user-friendly interface for MCP tools and resources.

**Reference Implementation:** `robotics-webapp` - Full-stack React + FastAPI application integrating 7+ MCP servers.

---

## Architecture

### Three-Layer Architecture

```
┌─────────────────────────────────────┐
│   Frontend (React/Vue/etc.)        │
│   - UI Components                   │
│   - State Management               │
│   - Service Layer                  │
└──────────────┬──────────────────────┘
               │ HTTP API
┌──────────────▼──────────────────────┐
│   Backend API (FastAPI/Express)     │
│   - MCP Client Proxy                │
│   - Business Logic                  │
│   - Error Handling                  │
└──────────────┬──────────────────────┘
               │ HTTP API
┌──────────────▼──────────────────────┐
│   MCP Servers (FastMCP)             │
│   - Tool Execution                  │
│   - Resource Access                 │
│   - State Management                │
└─────────────────────────────────────┘
```

---

## Components

### 1. Frontend Service Layer

Create typed service classes for MCP communication:

```typescript
// src/services/mcpService.ts
class MCPService {
  private baseUrl: string

  constructor(baseUrl: string = 'http://localhost:8354') {
    this.baseUrl = baseUrl
  }

  async checkHealth(serverName: string): Promise<boolean> {
    const response = await fetch(`${this.baseUrl}/api/mcp/servers/${serverName}/health`)
    return response.ok
  }

  async callTool(
    serverName: string,
    toolName: string,
    arguments: Record<string, any>
  ): Promise<MCPToolResponse> {
    const response = await fetch(
      `${this.baseUrl}/api/mcp/servers/${serverName}/tools/${toolName}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ arguments })
      }
    )
    return response.json()
  }
}

export default new MCPService()
```

### 2. Backend MCP Client

Proxy MCP calls from backend:

```python
# backend/mcp_client.py
import aiohttp
from typing import Any

class MCPClient:
    def __init__(self):
        self.servers = {
            'unity3d': {'base_url': 'http://localhost:8001', 'enabled': True},
            'vrchat': {'base_url': 'http://localhost:8002', 'enabled': True},
            # ... more servers
        }
        self.session: aiohttp.ClientSession | None = None

    async def call_tool(
        self,
        server_name: str,
        tool_name: str,
        arguments: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Call an MCP tool on a specific server"""
        if server_name not in self.servers:
            raise ValueError(f"Unknown MCP server: {server_name}")

        server_config = self.servers[server_name]
        if not server_config['enabled']:
            raise ValueError(f"MCP server {server_name} is disabled")

        if not self.session:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)

        url = f"{server_config['base_url']}/api/v1/tools/{tool_name}"
        payload = {'arguments': arguments or {}}

        async with self.session.post(url, json=payload) as resp:
            if resp.status == 200:
                return {
                    'success': True,
                    'data': await resp.json(),
                    'server': server_name,
                    'tool': tool_name
                }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {resp.status}: {await resp.text()}",
                    'server': server_name,
                    'tool': tool_name
                }
```

### 3. Backend API Endpoints

Expose MCP functionality via REST API:

```python
# backend/main.py
from fastapi import FastAPI, HTTPException
from backend.mcp_client import mcp_client

app = FastAPI()

@app.get("/api/mcp/servers/{server_name}/health")
async def check_server_health(server_name: str):
    """Check MCP server health"""
    healthy = await mcp_client.check_health(server_name)
    return {"healthy": healthy, "server": server_name}

@app.post("/api/mcp/servers/{server_name}/tools/{tool_name}")
async def call_mcp_tool(
    server_name: str,
    tool_name: str,
    arguments: dict = None
):
    """Call an MCP tool"""
    try:
        result = await mcp_client.call_tool(server_name, tool_name, arguments)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
```

### 4. Frontend Components

React components with MCP integration:

```typescript
// src/components/MCPStatusBanner.tsx
import { useState, useEffect } from 'react'
import mcpService from '../services/mcpService'

interface Props {
  serverName: string
  serverDisplayName: string
}

export default function MCPStatusBanner({ serverName, serverDisplayName }: Props) {
  const [status, setStatus] = useState<'checking' | 'connected' | 'disconnected'>('checking')

  useEffect(() => {
    const checkHealth = async () => {
      const healthy = await mcpService.checkHealth(serverName)
      setStatus(healthy ? 'connected' : 'disconnected')
    }
    checkHealth()
    const interval = setInterval(checkHealth, 30000) // Check every 30s
    return () => clearInterval(interval)
  }, [serverName])

  if (status === 'checking') {
    return <div className="banner yellow">Checking connection...</div>
  }

  if (status === 'connected') {
    return <div className="banner green">MCP Server Connected - Using real data</div>
  }

  return <div className="banner red">MOCK DATA MODE - MCP Server Not Connected</div>
}
```

---

## Key Features

### 1. Health Checking

- **Backend**: Periodic health checks for all MCP servers
- **Frontend**: Real-time status indicators
- **Fallback**: Graceful degradation to mock data when servers unavailable

### 2. Error Handling

- **Connection Errors**: Fallback to mock data
- **Tool Errors**: Display user-friendly error messages
- **Timeout Handling**: Configurable timeouts per server

### 3. Mock Data Mode

- **Default**: Webapp works without MCP servers (mock data)
- **Visual Indicators**: Clear banners showing connection status
- **Progressive Enhancement**: Real functionality when servers available

### 4. Multi-Server Support

- **Configuration**: Environment variables for server URLs
- **Dynamic Discovery**: List available tools per server
- **Unified Interface**: Single API for all MCP servers

---

## Configuration

### Backend Environment Variables

```env
# MCP Server URLs
UNITY3D_MCP_URL=http://localhost:8001
VRCHAT_MCP_URL=http://localhost:8002
AVATAR_MCP_URL=http://localhost:8003
OSC_MCP_URL=http://localhost:8004
VROID_MCP_URL=http://localhost:8005
RESONITE_MCP_URL=http://localhost:8006
LOCAL_LLM_MCP_URL=http://localhost:8007
```

### Frontend Configuration

```typescript
// vite.config.ts or similar
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8354',
        changeOrigin: true
      }
    }
  }
})
```

---

## Best Practices

### 1. Type Safety

- Use TypeScript for frontend services
- Define interfaces for all MCP responses
- Use Pydantic models in backend

### 2. Error Handling

- Always handle connection failures gracefully
- Provide clear error messages to users
- Log errors for debugging

### 3. Performance

- Cache health check results
- Batch tool calls when possible
- Use WebSockets for real-time updates

### 4. Security

- Validate all inputs
- Sanitize error messages
- Use HTTPS in production
- Implement rate limiting

### 5. User Experience

- Show loading states during tool calls
- Display connection status prominently
- Provide fallback mock data
- Clear error messages

---

## Example: Full Integration

### Backend Service

```python
# backend/llm_service.py
from backend.mcp_client import mcp_client

class LLMService:
    async def list_models(self, provider: str = "all"):
        """List available LLM models"""
        result = await mcp_client.call_tool(
            'local_llm',
            'llm_models',
            {'operation': f'{provider}_list'}
        )
        return result.get('data', [])

    async def load_model(self, model_id: str, provider: str):
        """Load a model for inference"""
        result = await mcp_client.call_tool(
            'local_llm',
            'llm_models',
            {
                'operation': f'{provider}_load',
                'model_id': model_id
            }
        )
        return result
```

### Frontend Service

```typescript
// src/services/llmService.ts
class LLMService {
  async listModels(provider: string = 'all'): Promise<LLMModel[]> {
    const response = await fetch(
      `${this.baseUrl}/api/llm/models?provider=${provider}`
    )
    const data = await response.json()
    return data.models || []
  }

  async loadModel(modelId: string, provider: string): Promise<LoadResult> {
    const response = await fetch(
      `${this.baseUrl}/api/llm/models/${modelId}/load`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ provider })
      }
    )
    return response.json()
  }
}
```

### React Component

```typescript
// src/app/ai-llm/page.tsx
export default function AILLMPage() {
  const [models, setModels] = useState<LLMModel[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadModels()
  }, [])

  const loadModels = async () => {
    setLoading(true)
    try {
      const models = await llmService.listModels()
      setModels(models)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <MCPStatusBanner serverName="local_llm" serverDisplayName="Local LLM" />
      {/* Model list UI */}
    </div>
  )
}
```

---

## Reference Implementation

**Full Example:** `robotics-webapp`
- Repository: `https://github.com/sandraschi/robotics-webapp`
- Architecture: React + FastAPI + 7 MCP servers
- Features: Health checking, mock data fallback, real-time status

**Key Files:**
- `backend/mcp_client.py` - MCP client implementation
- `backend/main.py` - FastAPI endpoints
- `src/services/mcpService.ts` - Frontend MCP service
- `src/components/MCPStatusBanner.tsx` - Status indicator component

---

## start_webapp tool (headless launch)

MCP servers that ship a webapp can expose a `start_webapp` tool so clients (e.g. Claude Desktop) can launch the app without user interaction.

**Behavior:** The tool runs the repo’s start script in an “automated” mode that: (1) starts the backend, (2) waits until it is ready (e.g. HTTP GET to a health or API endpoint), (3) starts the frontend, (4) waits until it is ready, (5) opens the default browser to the frontend URL, (6) exits. Backend and frontend keep running in the background.

**Implementation:**  
- **Start script:** Add a flag (e.g. `-Automated` in PowerShell). When set: start backend in a hidden process, poll for readiness, start frontend in a hidden process, poll for readiness, `Start-Process <frontend_url>`, then exit. When not set, keep the existing interactive behavior (e.g. backend in a visible window, frontend in foreground).  
- **MCP tool:** One tool, e.g. `start_webapp()`, that resolves the path to the start script (from `__file__`), runs it with the automated flag, waits for completion (with a timeout), and returns `{ "success": true, "url": "http://localhost:PORT" }` or an error payload.

**Reference:** Docs MCP in this repo: `start_webapp` in `src/docs_mcp/server.py`; `web_sota/start.ps1 -Automated`. See also [starts/README.md](../starts/README.md).

---

## Related Patterns

- [MCP Server Composition Pattern](./mcp-server-composition.md) - Compose multiple MCP servers
- [Portmanteau Pattern](./MCP_PORTMANTEAU_BEST_PRACTICES.md) - Organize tools into families
- [FastMCP Persistent Storage](../fastmcp/persistent-storage.md) - State management

---

**Last Updated:** 2025-12-29
