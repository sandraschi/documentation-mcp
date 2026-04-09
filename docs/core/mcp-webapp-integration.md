# MCP-WebApp Integration Standards

## Overview
Standards for integrating MCP servers into web application UIs, enabling seamless AI-powered workflows in browser-based interfaces.

## Port Mandate (MANDATORY)

All MCP webapp dashboards MUST use ports from the reserved range **10700-10800**. NEVER use 3000, 5000, 5173, 8000, or 8080. See [Webapp Port Reservoir](../operations/WEBAPP_PORTS.md) for the allocation registry and your assigned port.

## Architecture Patterns

### Backend Integration Layer
```python
# FastAPI backend for MCP-webapp bridge
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from mcp import ClientSession, StdioServerParameters
import asyncio
import json

app = FastAPI()

# MCP server registry
mcp_servers = {
    "blender": {
        "command": "python",
        "args": ["-m", "blender_mcp.server"],
        "env": {}
    },
    "gimp": {
        "command": "python",
        "args": ["-m", "gimp_mcp.server"],
        "env": {}
    }
}

class MCPBridge:
    """Bridge between webapp and MCP servers."""

    def __init__(self):
        self.sessions = {}
        self.connections = {}

    async def connect_server(self, server_name: str) -> str:
        """Connect to MCP server and return session ID."""
        if server_name not in mcp_servers:
            raise ValueError(f"Unknown MCP server: {server_name}")

        config = mcp_servers[server_name]

        # Create MCP client session
        server_params = StdioServerParameters(
            command=config["command"],
            args=config["args"],
            env=config["env"]
        )

        session = await ClientSession.connect(server_params)
        session_id = f"{server_name}_{id(session)}"

        self.sessions[session_id] = session
        return session_id

    async def call_tool(self, session_id: str, tool_name: str, args: dict) -> dict:
        """Call MCP tool and return result."""
        if session_id not in self.sessions:
            raise ValueError(f"Unknown session: {session_id}")

        session = self.sessions[session_id]
        result = await session.call_tool(tool_name, arguments=args)
        return result

    async def list_tools(self, session_id: str) -> list:
        """List available tools for session."""
        if session_id not in self.sessions:
            raise ValueError(f"Unknown session: {session_id}")

        session = self.sessions[session_id]
        tools = await session.list_tools()
        return tools

# Global bridge instance
mcp_bridge = MCPBridge()

@app.post("/api/mcp/connect/{server_name}")
async def connect_mcp_server(server_name: str):
    """Connect to MCP server."""
    try:
        session_id = await mcp_bridge.connect_server(server_name)
        return {"session_id": session_id, "status": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/mcp/{session_id}/call/{tool_name}")
async def call_mcp_tool(session_id: str, tool_name: str, args: dict = None):
    """Call MCP tool."""
    try:
        result = await mcp_bridge.call_tool(session_id, tool_name, args or {})
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/mcp/{session_id}/tools")
async def list_mcp_tools(session_id: str):
    """List MCP tools."""
    try:
        tools = await mcp_bridge.list_tools(session_id)
        return {"tools": tools}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Frontend Integration Service
```typescript
// MCP service for React frontend
class MCPService {
  private baseUrl: string;
  private sessions: Map<string, string> = new Map();

  constructor(baseUrl = '/api') {
    this.baseUrl = baseUrl;
  }

  async connectServer(serverName: string): Promise<string> {
    const response = await fetch(`${this.baseUrl}/mcp/connect/${serverName}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) {
      throw new Error(`Failed to connect to ${serverName}`);
    }

    const data = await response.json();
    const sessionId = data.session_id;
    this.sessions.set(serverName, sessionId);
    return sessionId;
  }

  async callTool(serverName: string, toolName: string, args: any = {}): Promise<any> {
    const sessionId = this.sessions.get(serverName);
    if (!sessionId) {
      throw new Error(`Not connected to ${serverName}`);
    }

    const response = await fetch(
      `${this.baseUrl}/mcp/${sessionId}/call/${toolName}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(args),
      }
    );

    if (!response.ok) {
      throw new Error(`Failed to call ${toolName}`);
    }

    const data = await response.json();
    return data.result;
  }

  async listTools(serverName: string): Promise<any[]> {
    const sessionId = this.sessions.get(serverName);
    if (!sessionId) {
      throw new Error(`Not connected to ${serverName}`);
    }

    const response = await fetch(`${this.baseUrl}/mcp/${sessionId}/tools`);
    if (!response.ok) {
      throw new Error(`Failed to list tools for ${serverName}`);
    }

    const data = await response.json();
    return data.tools;
  }

  async disconnectServer(serverName: string): Promise<void> {
    const sessionId = this.sessions.get(serverName);
    if (sessionId) {
      this.sessions.delete(serverName);
      // Additional cleanup if needed
    }
  }
}

export const mcpService = new MCPService();
```

## React Integration Patterns

### MCP Server Connection Manager
```typescript
// React hook for MCP server management
import { useState, useEffect, useCallback } from 'react';
import { mcpService } from '../services/mcpService';

interface MCPServer {
  name: string;
  status: 'disconnected' | 'connecting' | 'connected' | 'error';
  tools: any[];
  error?: string;
}

export const useMCPServer = (serverName: string) => {
  const [server, setServer] = useState<MCPServer>({
    name: serverName,
    status: 'disconnected',
    tools: [],
  });

  const connect = useCallback(async () => {
    setServer(prev => ({ ...prev, status: 'connecting', error: undefined }));

    try {
      await mcpService.connectServer(serverName);
      const tools = await mcpService.listTools(serverName);

      setServer(prev => ({
        ...prev,
        status: 'connected',
        tools,
      }));
    } catch (error) {
      setServer(prev => ({
        ...prev,
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error',
      }));
    }
  }, [serverName]);

  const disconnect = useCallback(async () => {
    try {
      await mcpService.disconnectServer(serverName);
      setServer(prev => ({
        ...prev,
        status: 'disconnected',
        tools: [],
        error: undefined,
      }));
    } catch (error) {
      console.error('Error disconnecting:', error);
    }
  }, [serverName]);

  return {
    server,
    connect,
    disconnect,
  };
};
```

### Tool Execution Component
```typescript
// Component for executing MCP tools
import React, { useState, useEffect } from 'react';
import { useMCPServer } from '../hooks/useMCPServer';
import { mcpService } from '../services/mcpService';

interface ToolExecutorProps {
  serverName: string;
  toolName: string;
  argsSchema?: any;
  onResult?: (result: any) => void;
}

const ToolExecutor: React.FC<ToolExecutorProps> = ({
  serverName,
  toolName,
  argsSchema,
  onResult,
}) => {
  const { server, connect } = useMCPServer(serverName);
  const [args, setArgs] = useState<any>({});
  const [isExecuting, setIsExecuting] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (server.status === 'disconnected') {
      connect();
    }
  }, [server.status, connect]);

  const executeTool = async () => {
    if (server.status !== 'connected') return;

    setIsExecuting(true);
    setError(null);

    try {
      const toolResult = await mcpService.callTool(serverName, toolName, args);
      setResult(toolResult);
      onResult?.(toolResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsExecuting(false);
    }
  };

  const renderArgsForm = () => {
    if (!argsSchema) return null;

    return (
      <div className="space-y-4">
        {Object.entries(argsSchema.properties || {}).map(([key, prop]: [string, any]) => (
          <div key={key}>
            <label className="block text-sm font-medium mb-1">
              {prop.title || key}
            </label>
            <input
              type={prop.type === 'number' ? 'number' : 'text'}
              value={args[key] || ''}
              onChange={(e) => setArgs(prev => ({
                ...prev,
                [key]: prop.type === 'number' ? Number(e.target.value) : e.target.value
              }))}
              className="w-full px-3 py-2 border rounded-md"
              placeholder={prop.description}
            />
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="p-6 border rounded-lg">
      <h3 className="text-lg font-semibold mb-4">Execute {toolName}</h3>

      <div className="mb-4">
        <span className={`px-2 py-1 rounded text-sm ${
          server.status === 'connected' ? 'bg-green-100 text-green-800' :
          server.status === 'connecting' ? 'bg-yellow-100 text-yellow-800' :
          'bg-red-100 text-red-800'
        }`}>
          {server.status}
        </span>
      </div>

      {renderArgsForm()}

      <button
        onClick={executeTool}
        disabled={server.status !== 'connected' || isExecuting}
        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {isExecuting ? 'Executing...' : 'Execute Tool'}
      </button>

      {error && (
        <div className="mt-4 p-3 bg-red-100 text-red-800 rounded">
          Error: {error}
        </div>
      )}

      {result && (
        <div className="mt-4 p-3 bg-green-100 text-green-800 rounded">
          <pre className="text-sm overflow-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default ToolExecutor;
```

## Real-time Updates with WebSockets

### WebSocket Integration
```python
# WebSocket endpoint for real-time MCP updates
@app.websocket("/ws/mcp/{session_id}")
async def mcp_websocket(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time MCP communication."""
    await websocket.accept()

    if session_id not in mcp_bridge.sessions:
        await websocket.send_json({"error": "Invalid session"})
        await websocket.close()
        return

    session = mcp_bridge.sessions[session_id]
    mcp_bridge.connections[session_id] = websocket

    try:
        while True:
            # Listen for tool execution requests
            data = await websocket.receive_json()

            if data.get("type") == "call_tool":
                try:
                    result = await session.call_tool(
                        data["tool_name"],
                        arguments=data.get("args", {})
                    )
                    await websocket.send_json({
                        "type": "tool_result",
                        "tool_name": data["tool_name"],
                        "result": result
                    })
                except Exception as e:
                    await websocket.send_json({
                        "type": "error",
                        "tool_name": data["tool_name"],
                        "error": str(e)
                    })

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        if session_id in mcp_bridge.connections:
            del mcp_bridge.connections[session_id]
```

### React WebSocket Hook
```typescript
// React hook for WebSocket MCP communication
import { useEffect, useRef, useState, useCallback } from 'react';

interface WebSocketMessage {
  type: string;
  [key: string]: any;
}

export const useMCPWebSocket = (sessionId: string) => {
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<WebSocketMessage[]>([]);
  const wsRef = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    const ws = new WebSocket(`ws://localhost:10702/ws/mcp/${sessionId}`);  // Use port from WEBAPP_PORTS registry

    ws.onopen = () => {
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages(prev => [...prev, message]);
    };

    ws.onclose = () => {
      setIsConnected(false);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };

    wsRef.current = ws;
  }, [sessionId]);

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
  }, []);

  const sendMessage = useCallback((message: WebSocketMessage) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  }, []);

  useEffect(() => {
    return () => {
      disconnect();
    };
  }, [disconnect]);

  return {
    isConnected,
    messages,
    connect,
    disconnect,
    sendMessage,
  };
};
```

## Error Handling and Resilience

### Connection Recovery
```typescript
// Automatic reconnection logic
class MCPConnectionManager {
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  async connectWithRetry(serverName: string): Promise<void> {
    try {
      await mcpService.connectServer(serverName);
      this.reconnectAttempts = 0;
    } catch (error) {
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectAttempts++;
        console.log(`Reconnecting... Attempt ${this.reconnectAttempts}`);

        await new Promise(resolve =>
          setTimeout(resolve, this.reconnectDelay * this.reconnectAttempts)
        );

        return this.connectWithRetry(serverName);
      }
      throw error;
    }
  }
}
```

### Graceful Degradation
```typescript
// Fallback UI when MCP servers are unavailable
const MCPFallback: React.FC<{ serverName: string }> = ({ serverName }) => {
  return (
    <div className="p-6 border-2 border-dashed border-gray-300 rounded-lg">
      <div className="text-center">
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          MCP Server Unavailable
        </h3>
        <p className="text-gray-600 mb-4">
          The {serverName} MCP server is currently unavailable.
          Some features may be limited.
        </p>
        <button
          onClick={() => window.location.reload()}
          className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700"
        >
          Retry Connection
        </button>
      </div>
    </div>
  );
};
```

## Performance Optimization

### Request Batching
```typescript
// Batch multiple tool calls for efficiency
class MCPBatchExecutor {
  private queue: Array<{
    serverName: string;
    toolName: string;
    args: any;
    resolve: (value: any) => void;
    reject: (error: any) => void;
  }> = [];

  private batchSize = 5;
  private isProcessing = false;

  async addToBatch(
    serverName: string,
    toolName: string,
    args: any
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      this.queue.push({
        serverName,
        toolName,
        args,
        resolve,
        reject,
      });

      this.processBatch();
    });
  }

  private async processBatch(): Promise<void> {
    if (this.isProcessing || this.queue.length === 0) return;

    this.isProcessing = true;

    const batch = this.queue.splice(0, this.batchSize);

    try {
      // Execute batch in parallel
      const results = await Promise.allSettled(
        batch.map(item =>
          mcpService.callTool(item.serverName, item.toolName, item.args)
        )
      );

      // Resolve/reject promises
      results.forEach((result, index) => {
        const item = batch[index];
        if (result.status === 'fulfilled') {
          item.resolve(result.value);
        } else {
          item.reject(result.reason);
        }
      });
    } catch (error) {
      // Handle batch-level errors
      batch.forEach(item => item.reject(error));
    } finally {
      this.isProcessing = false;

      // Process remaining items
      if (this.queue.length > 0) {
        setTimeout(() => this.processBatch(), 0);
      }
    }
  }
}
```

## Security Considerations

### Authentication
```python
# MCP server authentication
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token for MCP access."""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/mcp/connect/{server_name}")
async def connect_mcp_server(
    server_name: str,
    token_data = Depends(verify_token)
):
    """Connect to MCP server with authentication."""
    # Verify user has permission for this server
    if server_name not in token_data.get("allowed_servers", []):
        raise HTTPException(status_code=403, detail="Access denied")

    # Proceed with connection...
```

## Testing Integration

### End-to-End Tests
```typescript
// E2E test for MCP-webapp integration
describe('MCP Server Integration', () => {
  beforeEach(async () => {
    // Start test MCP server
    // Setup test database
  });

  afterEach(async () => {
    // Cleanup test server
    // Clear test data
  });

  test('should connect to MCP server', async () => {
    render(<App />);

    // Wait for connection
    await waitFor(() => {
      expect(screen.getByText('Connected to Blender MCP')).toBeInTheDocument();
    });
  });

  test('should execute tool and display result', async () => {
    render(<ToolExecutor serverName="blender" toolName="create_cube" />);

    // Fill form
    fireEvent.change(screen.getByLabelText('Size'), {
      target: { value: '2.0' }
    });

    // Execute tool
    fireEvent.click(screen.getByText('Execute Tool'));

    // Verify result
    await waitFor(() => {
      expect(screen.getByText(/Cube created/)).toBeInTheDocument();
    });
  });
});
```

## Next Steps
After webapp integration, consider:
1. [Real-time Collaboration](./collaboration.md)
2. [Multi-user Sessions](./multi-user.md)
3. [Offline Capabilities](./offline.md)
