# Build Tools & Configuration Standards

**Standardized build tools, configurations, MCP client integration, and development workflows for MCP ECMAScript projects**

## Project Structure Standards

### ✅ Standard MCP Webapp Structure

```
robotics-webapp/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Home page
│   │   ├── globals.css        # Global styles
│   │   └── docs/              # Documentation pages
│   ├── components/            # Reusable components
│   │   ├── ui/               # UI primitives (Tailwind only)
│   │   └── robotics/         # Domain components
│   └── lib/                  # Utilities and hooks
├── public/                   # Static assets
├── tests/                    # Test files
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── next.config.js
└── eslint.config.mjs
```

### ✅ Standard MCP Server Structure

```
robotics-mcp/
├── src/
│   └── robotics_mcp/
│       ├── server.py          # Main FastMCP server
│       ├── tools/            # Portmanteau tools
│       ├── utils/            # Utilities
│       └── config/           # Configuration
├── tests/                    # Test files
├── pyproject.toml           # Python dependencies
├── mypy.ini                 # Type checking
└── pytest.ini              # Test configuration
```

### ✅ Standard MCP Webapp with Client Integration

```
robotics-webapp/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Home page
│   │   ├── globals.css        # Global styles
│   │   └── docs/              # Documentation pages
│   ├── components/            # Reusable components
│   │   ├── ui/               # UI primitives (Tailwind only)
│   │   └── robotics/         # Domain components
│   ├── lib/                  # Utilities and hooks
│   │   ├── mcp/              # ⭐ MCP client integration
│   │   │   ├── client.ts     # MCP client factory
│   │   │   ├── hooks.ts      # React hooks for MCP
│   │   │   ├── types.ts      # MCP type definitions
│   │   │   └── tools/        # Tool-specific wrappers
│   │   └── utils/            # General utilities
│   └── services/             # Business logic services
├── public/                   # Static assets
├── tests/                    # Test files
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── e2e/                 # End-to-end tests
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── next.config.js
├── eslint.config.mjs
├── mcp-config.json          # ⚠️ Webapp client config (NEVER for MCP servers!)
└── mcp-servers/            # ✅ Standard MCP server configs only
```

## MCP Client Integration Standards

### 🚨 **CRITICAL SAFETY WARNING**

**Non-standard MCP configuration fields will BREAK server startup with strict loaders like Antigravity!**

- ✅ **Allowed**: `command`, `args`, `env`
- ❌ **Forbidden**: `description`, `transport`, `serverUrl`, custom fields
- 🔄 **Required**: Configuration mapping from webapp format to MCP format

**Always separate webapp client config from actual MCP server configs!**

### ✅ MCP Client Architecture

**Best for**: Webapps connecting to MCP servers (stdio or HTTP)

#### Core Client Components

```typescript
// src/lib/mcp/types.ts
export interface MCPConnection {
  transport: 'stdio' | 'http';
  serverUrl?: string;
  command?: string;
  args?: string[];
  env?: Record<string, string>;
}

export interface MCPTool {
  name: string;
  description: string;
  inputSchema: object;
  execute: (params: any) => Promise<any>;
}

export interface MCPResource {
  uri: string;
  name: string;
  description: string;
  mimeType: string;
  read: () => Promise<string | Buffer>;
}
```

#### MCP Client Factory

```typescript
// src/lib/mcp/client.ts
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { HTTPClientTransport } from '@modelcontextprotocol/sdk/client/http.js';

export class MCPClientManager {
  private clients: Map<string, Client> = new Map();
  private connections: Map<string, MCPConnection> = new Map();

  async connect(serverId: string, connection: MCPConnection): Promise<Client> {
    if (this.clients.has(serverId)) {
      return this.clients.get(serverId)!;
    }

    const client = new Client(
      {
        name: 'robotics-webapp',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
          resources: {},
        },
      }
    );

    let transport;
    if (connection.transport === 'stdio') {
      transport = new StdioClientTransport({
        command: connection.command!,
        args: connection.args || [],
        env: { ...process.env, ...connection.env },
      });
    } else if (connection.transport === 'http') {
      transport = new HTTPClientTransport({
        baseUrl: connection.serverUrl!,
      });
    } else {
      throw new Error(`Unsupported transport: ${connection.transport}`);
    }

    await client.connect(transport);
    this.clients.set(serverId, client);
    this.connections.set(serverId, connection);

    return client;
  }

  async disconnect(serverId: string): Promise<void> {
    const client = this.clients.get(serverId);
    if (client) {
      await client.close();
      this.clients.delete(serverId);
      this.connections.delete(serverId);
    }
  }

  getClient(serverId: string): Client | undefined {
    return this.clients.get(serverId);
  }

  async listTools(serverId: string): Promise<MCPTool[]> {
    const client = this.getClient(serverId);
    if (!client) throw new Error(`No connection to ${serverId}`);

    const response = await client.request(
      { method: 'tools/list' },
      { timeout: 10000 }
    );

    return response.tools.map(tool => ({
      name: tool.name,
      description: tool.description,
      inputSchema: tool.inputSchema,
      execute: async (params: any) => {
        const result = await client.request(
          {
            method: 'tools/call',
            params: {
              name: tool.name,
              arguments: params,
            },
          },
          { timeout: 30000 }
        );
        return result;
      },
    }));
  }

  async listResources(serverId: string): Promise<MCPResource[]> {
    const client = this.getClient(serverId);
    if (!client) throw new Error(`No connection to ${serverId}`);

    const response = await client.request(
      { method: 'resources/list' },
      { timeout: 10000 }
    );

    return response.resources.map(resource => ({
      uri: resource.uri,
      name: resource.name,
      description: resource.description,
      mimeType: resource.mimeType,
      read: async () => {
        const result = await client.request(
          {
            method: 'resources/read',
            params: { uri: resource.uri },
          },
          { timeout: 30000 }
        );
        return result.contents[0].text || result.contents[0].blob;
      },
    }));
  }
}

export const mcpClient = new MCPClientManager();
```

#### MCP Configuration

**⚠️ CRITICAL WARNING**: This is a **custom configuration format** for the webapp's MCP client library only. **NEVER** use this format for actual MCP server configurations!

**❌ BREAKS STRICT LOADERS**: Non-standard fields like `"description"`, `"transport"`, `"serverUrl"` will cause strict MCP implementations (Antigravity, etc.) to **refuse to start servers**. Only use standard MCP config fields: `command`, `args`, `env`.

**🔄 SEPARATION REQUIRED**: Keep webapp client config separate from MCP server configs to avoid startup failures.

```json
// src/mcp-config.json - ⚠️ DANGER: Custom webapp client config ONLY
// 🚨 NEVER use this for actual MCP server startup!
// 🚨 Will BREAK strict loaders like Antigravity!
{
  "servers": {
    "robotics-mcp": {
      "transport": "http",      // ❌ NOT in MCP spec - client only
      "serverUrl": "http://localhost:8888"  // ❌ NOT in MCP spec - client only
    },
    "osc-mcp": {
      "transport": "stdio",     // ❌ NOT in MCP spec - client only
      "command": "python",
      "args": ["-m", "osc_mcp.server"],
      "env": {
        "PYTHONPATH": "/path/to/osc/server"  // ✅ Valid in env section
      }
    }
  },
  "defaults": {
    "timeout": 30000,
    "retryAttempts": 3,
    "retryDelay": 1000
  }
}
```

#### Standard MCP Client Configuration (Claude Desktop)

For comparison, here's the **actual MCP client configuration** format used by Claude Desktop:

```json
// %APPDATA%/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "robotics-mcp": {
      "command": "python",
      "args": ["-m", "robotics_mcp.server"],
      "env": {
        "PYTHONPATH": "/path/to/server"
      }
    },
    "unity3d-mcp": {
      "command": "python",
      "args": ["-m", "unity3d_mcp.server"],
      "env": {
        "UNITY_PATH": "C:\\Program Files\\Unity Hub\\Unity Hub.exe"
      }
    }
  }
}
```

**Key Differences:**
- ❌ `"description"` - **Not allowed** (breaks strict loaders)
- ❌ `"transport"`, `"serverUrl"` - **Not part of** standard MCP config
- ✅ `"env": {"PYTHONPATH": "..." }` - **Correct way** to set Python path
- Standard MCP config only supports `command`, `args`, `env`

#### Configuration Separation Pattern

**🚨 NEVER MIX CONFIGS**: Keep webapp client config and MCP server config completely separate!

```typescript
// src/lib/mcp/config-mapper.ts
import { MCPConnection } from './types';

/**
 * Maps webapp client config to standard MCP server configs
 * CRITICAL: Prevents non-standard fields from breaking MCP servers
 */
export function mapToMCPServerConfig(webappConfig: MCPConnection) {
  // Safety check: Reject any config that might have been contaminated
  const configKeys = Object.keys(webappConfig);
  const forbiddenKeys = ['description', 'transport', 'serverUrl'];

  for (const key of forbiddenKeys) {
    if (configKeys.includes(key)) {
      throw new Error(
        `🚨 DANGER: Config contains forbidden MCP field "${key}". ` +
        `This will BREAK strict loaders like Antigravity! ` +
        `Remove non-standard fields before using with MCP servers.`
      );
    }
  }

  if (webappConfig.transport === 'stdio') {
    return {
      command: webappConfig.command!,
      args: webappConfig.args || [],
      env: webappConfig.env || {}
    };
  } else if (webappConfig.transport === 'http') {
    // HTTP transport - server runs separately, client connects via HTTP
    // No MCP server config needed for HTTP connections
    return null;
  }

  throw new Error(`Unsupported transport: ${webappConfig.transport}`);
}

// Usage: Only use mapped config for actual MCP server startup
const serverConfig = mapToMCPServerConfig(webappConnection);
// serverConfig now has ONLY: { command, args, env }
// Safe to pass to MCP server loaders
```

#### File Structure Separation

```
project/
├── mcp-config.json          # ❌ NEVER use for MCP servers
├── mcp-servers/            # ✅ Standard MCP configs only
│   ├── robotics-mcp.json
│   └── osc-mcp.json
└── src/lib/mcp/
    ├── config.ts           # Maps webapp config to MCP format
    └── client.ts           # Uses webapp config internally
```

#### Example MCP Server Configs

```json
// mcp-servers/robotics-mcp.json - ✅ VALID MCP config
{
  "command": "python",
  "args": ["-m", "robotics_mcp.server"],
  "env": {
    "PYTHONPATH": "/path/to/robotics/server"
  }
}
```

```json
// mcp-servers/osc-mcp.json - ✅ VALID MCP config
{
  "command": "python",
  "args": ["-m", "osc_mcp.server"],
  "env": {
    "PYTHONPATH": "/path/to/osc/server"
  }
}
```

**🔥 FAILURE POINT**: Using webapp config directly for MCP servers = startup failures with strict loaders!

#### MCP Configuration Safety Checklist

**🚨 BEFORE deploying or starting MCP servers:**

- [ ] **Separate Configs**: Webapp client config (`mcp-config.json`) is separate from MCP server configs
- [ ] **No Forbidden Fields**: No `description`, `transport`, `serverUrl`, or custom fields in MCP server configs
- [ ] **Valid Fields Only**: MCP server configs contain ONLY: `command`, `args`, `env`
- [ ] **Environment Variables**: PYTHONPATH and others are in `env` object, not top-level
- [ ] **Validation**: Use `mapToMCPServerConfig()` to validate and convert configs
- [ ] **Testing**: Test with strict loaders (Antigravity) before production deployment

**💥 COMMON FAILURE PATTERNS TO AVOID:**

```typescript
// ❌ WRONG: Using webapp config directly
const serverConfig = loadWebappConfig(); // Contains "description", "transport"
await startMCPServer(serverConfig); // 💥 BREAKS with Antigravity!

// ✅ CORRECT: Map to valid MCP format first
const webappConfig = loadWebappConfig();
const serverConfig = mapToMCPServerConfig(webappConfig); // Validates & converts
await startMCPServer(serverConfig); // ✅ Works with all loaders
```

**🔧 QUICK FIX for Existing Projects:**

```bash
# Find configs with forbidden fields
find . -name "*.json" -exec grep -l '"description"\|"transport"\|"serverUrl"' {} \;

# Use the config mapper to validate
# Add validation in your startup code
```

### ✅ React Hooks for MCP Integration

#### MCP Connection Hook

```typescript
// src/lib/mcp/hooks.ts
import { useState, useEffect, useCallback } from 'react';
import { mcpClient } from './client';
import { MCPTool, MCPResource } from './types';

export function useMCPConnection(serverId: string, config: MCPConnection) {
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [tools, setTools] = useState<MCPTool[]>([]);
  const [resources, setResources] = useState<MCPResource[]>([]);

  const connect = useCallback(async () => {
    setIsConnecting(true);
    setError(null);

    try {
      const client = await mcpClient.connect(serverId, config);
      setIsConnected(true);

      // Load available tools and resources
      const [toolsList, resourcesList] = await Promise.all([
        mcpClient.listTools(serverId),
        mcpClient.listResources(serverId),
      ]);

      setTools(toolsList);
      setResources(resourcesList);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Connection failed');
      setIsConnected(false);
    } finally {
      setIsConnecting(false);
    }
  }, [serverId, config]);

  const disconnect = useCallback(async () => {
    try {
      await mcpClient.disconnect(serverId);
      setIsConnected(false);
      setTools([]);
      setResources([]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Disconnection failed');
    }
  }, [serverId]);

  // Auto-connect on mount
  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    isConnected,
    isConnecting,
    error,
    tools,
    resources,
    connect,
    disconnect,
  };
}
```

#### Tool Execution Hook

```typescript
// src/lib/mcp/hooks.ts (continued)
export function useMCPTool(serverId: string, toolName: string) {
  const [isExecuting, setIsExecuting] = useState(false);
  const [lastResult, setLastResult] = useState<any>(null);
  const [lastError, setLastError] = useState<string | null>(null);

  const execute = useCallback(async (params: any) => {
    setIsExecuting(true);
    setLastError(null);

    try {
      const client = mcpClient.getClient(serverId);
      if (!client) {
        throw new Error(`No connection to ${serverId}`);
      }

      const result = await client.request(
        {
          method: 'tools/call',
          params: {
            name: toolName,
            arguments: params,
          },
        },
        { timeout: 30000 }
      );

      setLastResult(result);
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Tool execution failed';
      setLastError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsExecuting(false);
    }
  }, [serverId, toolName]);

  return {
    execute,
    isExecuting,
    lastResult,
    lastError,
  };
}
```

#### Resource Access Hook

```typescript
// src/lib/mcp/hooks.ts (continued)
export function useMCPResource(serverId: string, resourceUri: string) {
  const [content, setContent] = useState<string | Buffer | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const client = mcpClient.getClient(serverId);
      if (!client) {
        throw new Error(`No connection to ${serverId}`);
      }

      const result = await client.request(
        {
          method: 'resources/read',
          params: { uri: resourceUri },
        },
        { timeout: 30000 }
      );

      const resourceContent = result.contents[0].text || result.contents[0].blob;
      setContent(resourceContent);
      return resourceContent;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Resource load failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, [serverId, resourceUri]);

  return {
    content,
    isLoading,
    error,
    load,
  };
}
```

### ✅ MCP Client Dependencies

#### Standard Package.json for MCP Clients

```json
{
  "name": "robotics-webapp",
  "version": "0.1.0-alpha",
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.5.0",
    "next": "^16.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "typescript": "^5.6.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "eslint": "^8.0.0",
    "eslint-config-next": "^16.0.0",
    "@typescript-eslint/eslint-plugin": "^7.0.0",
    "@typescript-eslint/parser": "^7.0.0",
    "prettier": "^3.0.0",
    "jest": "^29.0.0",
    "@testing-library/react": "^16.0.0",
    "@testing-library/jest-dom": "^6.0.0"
  },
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "preview": "next build && next start",
    "lint": "next lint",
    "lint:fix": "next lint --fix",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "mcp:connect": "node scripts/connect-mcp.js",
    "mcp:test": "node scripts/test-mcp-connection.js"
  }
}
```

### ✅ Connection Management Patterns

#### Auto-Reconnection with Circuit Breaker

```typescript
// src/lib/mcp/connection-manager.ts
import { mcpClient } from './client';

export class MCPConnectionManager {
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000; // Start with 1 second
  private maxReconnectDelay = 30000; // Max 30 seconds
  private circuitBreakerOpen = false;
  private circuitBreakerTimeout = 60000; // 1 minute

  async connectWithRetry(serverId: string, config: MCPConnection): Promise<void> {
    if (this.circuitBreakerOpen) {
      throw new Error('Circuit breaker is open - MCP server unavailable');
    }

    try {
      await mcpClient.connect(serverId, config);
      this.reconnectAttempts = 0; // Reset on successful connection
      console.log(`✅ Connected to MCP server: ${serverId}`);
    } catch (error) {
      console.error(`❌ Failed to connect to MCP server: ${serverId}`, error);

      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectAttempts++;
        const delay = Math.min(this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1), this.maxReconnectDelay);

        console.log(`🔄 Retrying connection in ${delay}ms (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

        setTimeout(() => {
          this.connectWithRetry(serverId, config);
        }, delay);
      } else {
        console.error(`💥 Max reconnection attempts reached for ${serverId}`);
        this.openCircuitBreaker();
      }
    }
  }

  private openCircuitBreaker(): void {
    this.circuitBreakerOpen = true;
    console.log('🔌 Circuit breaker opened - pausing MCP connections');

    setTimeout(() => {
      this.circuitBreakerOpen = false;
      this.reconnectAttempts = 0;
      console.log('🔌 Circuit breaker reset - resuming MCP connections');
    }, this.circuitBreakerTimeout);
  }

  async disconnect(serverId: string): Promise<void> {
    try {
      await mcpClient.disconnect(serverId);
      console.log(`🔌 Disconnected from MCP server: ${serverId}`);
    } catch (error) {
      console.error(`❌ Error disconnecting from MCP server: ${serverId}`, error);
    }
  }
}

export const connectionManager = new MCPConnectionManager();
```

### ✅ Component Integration Examples

#### MCP Tool Component

```tsx
// src/components/MCPToolRunner.tsx
'use client';

import { useState } from 'react';
import { useMCPTool } from '@/lib/mcp/hooks';

interface MCPToolRunnerProps {
  serverId: string;
  toolName: string;
  params: Record<string, any>;
  onResult?: (result: any) => void;
  onError?: (error: string) => void;
}

export function MCPToolRunner({
  serverId,
  toolName,
  params,
  onResult,
  onError
}: MCPToolRunnerProps) {
  const { execute, isExecuting, lastResult, lastError } = useMCPTool(serverId, toolName);
  const [executionCount, setExecutionCount] = useState(0);

  const handleExecute = async () => {
    try {
      setExecutionCount(prev => prev + 1);
      const result = await execute(params);
      onResult?.(result);
    } catch (error) {
      onError?.(error instanceof Error ? error.message : 'Unknown error');
    }
  };

  return (
    <div className="p-4 border rounded-lg">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold">{toolName}</h3>
        <button
          onClick={handleExecute}
          disabled={isExecuting}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {isExecuting ? 'Executing...' : 'Execute Tool'}
        </button>
      </div>

      <div className="space-y-2">
        <div>
          <label className="block text-sm font-medium mb-1">Parameters:</label>
          <pre className="bg-gray-100 p-2 rounded text-sm overflow-auto">
            {JSON.stringify(params, null, 2)}
          </pre>
        </div>

        {lastResult && (
          <div>
            <label className="block text-sm font-medium mb-1">Last Result:</label>
            <pre className="bg-green-50 border border-green-200 p-2 rounded text-sm overflow-auto">
              {JSON.stringify(lastResult, null, 2)}
            </pre>
          </div>
        )}

        {lastError && (
          <div>
            <label className="block text-sm font-medium mb-1 text-red-600">Last Error:</label>
            <pre className="bg-red-50 border border-red-200 p-2 rounded text-sm overflow-auto text-red-800">
              {lastError}
            </pre>
          </div>
        )}

        <div className="text-sm text-gray-600">
          Executions: {executionCount}
        </div>
      </div>
    </div>
  );
}
```

#### MCP Server Status Component

```tsx
// src/components/MCPServerStatus.tsx
'use client';

import { useMCPConnection } from '@/lib/mcp/hooks';

interface MCPServerStatusProps {
  serverId: string;
  config: MCPConnection;
}

export function MCPServerStatus({ serverId, config }: MCPServerStatusProps) {
  const { isConnected, isConnecting, error, tools, resources, connect, disconnect } = useMCPConnection(serverId, config);

  return (
    <div className="p-4 border rounded-lg">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <div
            className={`w-3 h-3 rounded-full ${
              isConnected ? 'bg-green-500' : error ? 'bg-red-500' : 'bg-yellow-500'
            }`}
          />
          <h3 className="text-lg font-semibold">{serverId}</h3>
          <span className="text-sm text-gray-500">({config.transport})</span>
        </div>

        <div className="space-x-2">
          {!isConnected && (
            <button
              onClick={connect}
              disabled={isConnecting}
              className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700 disabled:opacity-50"
            >
              {isConnecting ? 'Connecting...' : 'Connect'}
            </button>
          )}
          {isConnected && (
            <button
              onClick={disconnect}
              className="px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700"
            >
              Disconnect
            </button>
          )}
        </div>
      </div>

      {error && (
        <div className="mb-4 p-2 bg-red-50 border border-red-200 rounded text-red-800 text-sm">
          {error}
        </div>
      )}

      <div className="grid grid-cols-2 gap-4 text-sm">
        <div>
          <div className="font-medium mb-2">Tools ({tools.length})</div>
          <div className="max-h-32 overflow-y-auto">
            {tools.slice(0, 5).map(tool => (
              <div key={tool.name} className="text-gray-600 truncate">
                • {tool.name}
              </div>
            ))}
            {tools.length > 5 && (
              <div className="text-gray-400">... and {tools.length - 5} more</div>
            )}
          </div>
        </div>

        <div>
          <div className="font-medium mb-2">Resources ({resources.length})</div>
          <div className="max-h-32 overflow-y-auto">
            {resources.slice(0, 5).map(resource => (
              <div key={resource.uri} className="text-gray-600 truncate">
                • {resource.name}
              </div>
            ))}
            {resources.length > 5 && (
              <div className="text-gray-400">... and {resources.length - 5} more</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
```

### ✅ Testing MCP Client Integrations

#### Unit Tests for MCP Client

```typescript
// tests/unit/mcp-client.test.ts
import { jest } from '@jest/globals';
import { mcpClient } from '@/lib/mcp/client';

// Mock the MCP SDK
jest.mock('@modelcontextprotocol/sdk/client/index.js');
jest.mock('@modelcontextprotocol/sdk/client/stdio.js');
jest.mock('@modelcontextprotocol/sdk/client/http.js');

describe('MCPClient', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('connect', () => {
    it('should connect to stdio server successfully', async () => {
      const connection: MCPConnection = {
        transport: 'stdio',
        command: 'python',
        args: ['-m', 'test_server'],
      };

      const client = await mcpClient.connect('test-server', connection);

      expect(client).toBeDefined();
      expect(mcpClient.getClient('test-server')).toBe(client);
    });

    it('should connect to HTTP server successfully', async () => {
      const connection: MCPConnection = {
        transport: 'http',
        serverUrl: 'http://localhost:8888',
      };

      const client = await mcpClient.connect('test-server', connection);

      expect(client).toBeDefined();
      expect(mcpClient.getClient('test-server')).toBe(client);
    });

    it('should throw error for unsupported transport', async () => {
      const connection: MCPConnection = {
        transport: 'unsupported' as any,
      };

      await expect(mcpClient.connect('test-server', connection))
        .rejects
        .toThrow('Unsupported transport: unsupported');
    });
  });

  describe('listTools', () => {
    it('should list available tools', async () => {
      // Setup mock client
      const mockClient = {
        request: jest.fn().mockResolvedValue({
          tools: [
            {
              name: 'test_tool',
              description: 'A test tool',
              inputSchema: { type: 'object' },
            },
          ],
        }),
      };

      (mcpClient as any).clients.set('test-server', mockClient);

      const tools = await mcpClient.listTools('test-server');

      expect(tools).toHaveLength(1);
      expect(tools[0].name).toBe('test_tool');
      expect(tools[0].description).toBe('A test tool');
    });

    it('should throw error if not connected', async () => {
      await expect(mcpClient.listTools('nonexistent-server'))
        .rejects
        .toThrow('No connection to nonexistent-server');
    });
  });
});
```

#### Integration Tests

```typescript
// tests/integration/mcp-integration.test.ts
import { render, screen, waitFor } from '@testing-library/react';
import { MCPServerStatus } from '@/components/MCPServerStatus';

// Mock the MCP client
jest.mock('@/lib/mcp/client');

describe('MCP Integration', () => {
  it('should connect to MCP server on mount', async () => {
    const mockConfig: MCPConnection = {
      transport: 'http',
      serverUrl: 'http://localhost:8888',
    };

    render(<MCPServerStatus serverId="test-server" config={mockConfig} />);

    await waitFor(() => {
      expect(screen.getByText('test-server')).toBeInTheDocument();
    });

    // Check that connection was attempted
    expect(screen.getByText('(http)')).toBeInTheDocument();
  });

  it('should display tools and resources when connected', async () => {
    // Mock successful connection with tools and resources
    const mockConfig: MCPConnection = {
      transport: 'http',
      serverUrl: 'http://localhost:8888',
    };

    render(<MCPServerStatus serverId="test-server" config={mockConfig} />);

    await waitFor(() => {
      expect(screen.getByText('Tools (2)')).toBeInTheDocument();
      expect(screen.getByText('Resources (1)')).toBeInTheDocument();
    });
  });

  it('should handle connection errors gracefully', async () => {
    // Mock connection failure
    const mockConfig: MCPConnection = {
      transport: 'http',
      serverUrl: 'http://invalid-url',
    };

    render(<MCPServerStatus serverId="test-server" config={mockConfig} />);

    await waitFor(() => {
      expect(screen.getByText('Connection failed')).toBeInTheDocument();
    });
  });
});
```

### ✅ Configuration Management

#### Environment-Based Configuration

**🚨 DANGER**: Never pass webapp client config directly to MCP server loaders! Always map to standard MCP format first.

**Note**: PYTHONPATH and other environment variables should be set in the `env` section of each server config, not as top-level fields.

```typescript
// src/lib/mcp/config.ts
import mcpConfig from '../../../mcp-config.json';

export interface MCPConfig {
  servers: Record<string, MCPConnection>;
  defaults: {
    timeout: number;
    retryAttempts: number;
    retryDelay: number;
  };
}

export function loadMCPConfig(): MCPConfig {
  // Override with environment variables
  const config: MCPConfig = {
    ...mcpConfig,
    servers: { ...mcpConfig.servers },
  };

  // Environment variable overrides
  if (process.env.MCP_ROBOTICS_URL) {
    config.servers['robotics-mcp'].serverUrl = process.env.MCP_ROBOTICS_URL;
  }

  if (process.env.MCP_OSC_COMMAND) {
    config.servers['osc-mcp'].command = process.env.MCP_OSC_COMMAND;
  }

  // Override PYTHONPATH in env section (not as separate field)
  if (process.env.MCP_PYTHONPATH) {
    config.servers['osc-mcp'].env = {
      ...config.servers['osc-mcp'].env,
      PYTHONPATH: process.env.MCP_PYTHONPATH
    };
  }

  return config;
}

export function getMCPConnection(serverId: string): MCPConnection | null {
  const config = loadMCPConfig();
  return config.servers[serverId] || null;
}

export function getMCPDefaults() {
  const config = loadMCPConfig();
  return config.defaults;
}
```

#### Runtime Configuration Updates

```typescript
// src/lib/mcp/config-manager.ts
import { MCPConfig, loadMCPConfig } from './config';

export class MCPConfigManager {
  private config: MCPConfig;
  private listeners: Array<(config: MCPConfig) => void> = [];

  constructor() {
    this.config = loadMCPConfig();
  }

  getConfig(): MCPConfig {
    return { ...this.config };
  }

  updateServerConfig(serverId: string, updates: Partial<MCPConnection>): void {
    if (this.config.servers[serverId]) {
      this.config.servers[serverId] = {
        ...this.config.servers[serverId],
        ...updates,
      };

      this.notifyListeners();
      this.saveConfig();
    }
  }

  addServer(serverId: string, connection: MCPConnection): void {
    this.config.servers[serverId] = connection;
    this.notifyListeners();
    this.saveConfig();
  }

  removeServer(serverId: string): void {
    delete this.config.servers[serverId];
    this.notifyListeners();
    this.saveConfig();
  }

  subscribe(listener: (config: MCPConfig) => void): () => void {
    this.listeners.push(listener);

    // Return unsubscribe function
    return () => {
      const index = this.listeners.indexOf(listener);
      if (index > -1) {
        this.listeners.splice(index, 1);
      }
    };
  }

  private notifyListeners(): void {
    this.listeners.forEach(listener => listener(this.getConfig()));
  }

  private saveConfig(): void {
    // In a real implementation, this would save to a file or database
    console.log('MCP config updated:', this.config);
  }
}

export const configManager = new MCPConfigManager();
```

## Package.json Standards

### ✅ Standard Scripts

```json
{
  "name": "robotics-webapp",
  "version": "0.1.0-alpha",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "preview": "next build && next start",
    "lint": "next lint",
    "lint:fix": "next lint --fix",
    "type-check": "tsc --noEmit",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "clean": "rm -rf .next out node_modules/.cache"
  }
}
```

### ✅ Dependency Management

```json
{
  "dependencies": {
    "next": "^16.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "typescript": "^5.6.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "eslint": "^8.0.0",
    "eslint-config-next": "^16.0.0",
    "@typescript-eslint/eslint-plugin": "^7.0.0",
    "@typescript-eslint/parser": "^7.0.0",
    "prettier": "^3.0.0",
    "jest": "^29.0.0",
    "@testing-library/react": "^16.0.0",
    "@testing-library/jest-dom": "^6.0.0"
  }
}
```

## TypeScript Configuration

### ✅ Strict TypeScript Config

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["DOM", "DOM.Iterable", "ES2022"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/lib/*": ["./src/lib/*"],
      "@/types/*": ["./src/types/*"]
    },
    "forceConsistentCasingInFileNames": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noImplicitReturns": true,
    "noUncheckedIndexedAccess": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  },
  "include": [
    "next-env.d.ts",
    "**/*.ts",
    "**/*.tsx",
    ".next/types/**/*.ts"
  ],
  "exclude": [
    "node_modules",
    ".next",
    "out",
    "build"
  ]
}
```

### ✅ Path Mapping Standards

```json
// tsconfig.paths.json - for complex path mappings
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@/components": ["src/components/index.ts"],
      "@/components/*": ["src/components/*"],
      "@/hooks": ["src/hooks/index.ts"],
      "@/hooks/*": ["src/hooks/*"],
      "@/lib": ["src/lib/index.ts"],
      "@/lib/*": ["src/lib/*"],
      "@/types": ["src/types/index.ts"],
      "@/types/*": ["src/types/*"],
      "@/utils": ["src/utils/index.ts"],
      "@/utils/*": ["src/utils/*"],
      "@/styles/*": ["src/styles/*"],
      "@/assets/*": ["src/assets/*"],
      "@/config/*": ["src/config/*"]
    }
  }
}
```

## ESLint Configuration

### ✅ Next.js + TypeScript ESLint

```javascript
// eslint.config.mjs
import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "next/typescript"),
  {
    rules: {
      // TypeScript strict rules
      "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/prefer-const": "error",
      "@typescript-eslint/no-non-null-assertion": "warn",

      // React rules
      "react-hooks/exhaustive-deps": "error",
      "react-hooks/rules-of-hooks": "error",
      "react/jsx-key": "error",
      "react/jsx-no-useless-fragment": "warn",

      // General code quality
      "no-console": ["warn", { "allow": ["warn", "error"] }],
      "no-debugger": "error",
      "prefer-const": "error",
      "no-var": "error",

      // Import rules
      "import/order": ["error", {
        "groups": ["builtin", "external", "internal", "parent", "sibling", "index"],
        "newlines-between": "always"
      }]
    }
  },
  {
    // Disable rules for generated files
    files: ["**/*.generated.ts", "**/*.generated.tsx"],
    rules: {
      "@typescript-eslint/no-unused-vars": "off",
      "@typescript-eslint/no-explicit-any": "off"
    }
  }
];

export default eslintConfig;
```

## Prettier Configuration

### ✅ Consistent Code Formatting

```javascript
// .prettierrc.js
module.exports = {
  // Basic formatting
  printWidth: 100,
  tabWidth: 2,
  useTabs: false,
  semi: true,
  singleQuote: true,
  quoteProps: 'as-needed',
  trailingComma: 'es5',
  bracketSpacing: true,
  bracketSameLine: false,
  arrowParens: 'always',

  // Language specifics
  jsxSingleQuote: true,
  endOfLine: 'lf',

  // Import sorting
  importOrder: [
    '^@/(.*)$',
    '',
    '^react$',
    '^next/(.*)$',
    '',
    '^@radix-ui/(.*)$',
    '^lucide-react$',
    '',
    '^[./]'
  ],
  importOrderSeparation: true,
  importOrderSortSpecifiers: true,

  // Plugin configurations
  plugins: ['@trivago/prettier-plugin-sort-imports']
};
```

## Next.js Configuration

### ✅ Production-Ready Next.js Config

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // React strict mode for development
  reactStrictMode: true,

  // Enable experimental features safely
  experimental: {
    // App directory is stable in Next.js 16
    appDir: true,
    // Turbopack: ~10x faster development builds
    // See BUNDLERS_COMPARISON.md for Turbopack vs Webpack guide
    turbopack: process.env.NODE_ENV === 'development',
  },

  // TypeScript strict checking
  typescript: {
    // Ensure TypeScript errors break the build
    ignoreBuildErrors: false,
    // Use tsconfig paths
    tsconfigPath: './tsconfig.json',
  },

  // ESLint configuration
  eslint: {
    // Ensure ESLint errors break the build
    ignoreDuringBuilds: false,
  },

  // Image optimization
  images: {
    // Allow images from trusted domains
    domains: ['localhost', 'cdn.example.com'],
    // Enable modern formats
    formats: ['image/avif', 'image/webp'],
  },

  // Headers for security and performance
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'origin-when-cross-origin',
          },
        ],
      },
    ];
  },

  // Webpack configuration for advanced use cases
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Add custom webpack rules here if needed

    // Example: Add support for SVG as React components
    config.module.rules.push({
      test: /\.svg$/,
      use: ['@svgr/webpack'],
    });

    return config;
  },
};

module.exports = nextConfig;
```

## Testing Configuration

### ✅ Jest + Testing Library Setup

```javascript
// jest.config.js
const nextJest = require('next/jest');

const createJestConfig = nextJest({
  // Provide the path to your Next.js app to load next.config.js and .env files
  dir: './',
});

// Add any custom config to be passed to Jest
const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapping: {
    // Handle module aliases (this will be automatically configured for you based on your tsconfig.json paths)
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  testEnvironment: 'jest-environment-jsdom',
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/_*.{js,jsx,ts,tsx}',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};

// createJestConfig is exported this way to ensure that next/jest can load the Next.js config which is async
module.exports = createJestConfig(customJestConfig);
```

### ✅ Test Setup File

```javascript
// jest.setup.js
import '@testing-library/jest-dom';

// Mock Next.js router
jest.mock('next/router', () => ({
  useRouter() {
    return {
      route: '/',
      pathname: '/',
      query: '',
      asPath: '/',
      push: jest.fn(),
      pop: jest.fn(),
      reload: jest.fn(),
      back: jest.fn(),
      prefetch: jest.fn().mockResolvedValue(undefined),
      beforePopState: jest.fn(),
      events: {
        on: jest.fn(),
        off: jest.fn(),
        emit: jest.fn(),
      },
    };
  },
}));

// Mock environment variables
process.env.NEXT_PUBLIC_API_URL = 'http://localhost:3000';

// Global test utilities
global.fetch = jest.fn();

// Cleanup after each test
afterEach(() => {
  jest.clearAllMocks();
});
```

## CI/CD Configuration

### ✅ GitHub Actions Workflow

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
    - uses: actions/checkout@v4

    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Run linter
      run: npm run lint

    - name: Type check
      run: npm run type-check

    - name: Run tests
      run: npm run test:coverage

    - name: Upload coverage reports
      uses: codecov/codecov-action@v4
      with:
        file: ./coverage/lcov.info

  build:
    needs: test
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Use Node.js 20.x
      uses: actions/setup-node@v4
      with:
        node-version: 20.x
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Build application
      run: npm run build

    - name: Upload build artifacts
      uses: actions/upload-artifact@v4
      with:
        name: nextjs-build
        path: .next/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v4

    - name: Deploy to production
      run: |
        echo "Deploy to production"
        # Add your deployment commands here
```

## Performance Optimization

### ✅ Bundle Analysis

```javascript
// next.config.js - Add bundle analyzer
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  // ... other config
});
```

```json
// package.json - Add analyze script
{
  "scripts": {
    "analyze": "ANALYZE=true npm run build"
  }
}
```

### ✅ Lighthouse CI

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI

on:
  pull_request:
    branches: [main]

jobs:
  lighthouse:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Use Node.js 20.x
      uses: actions/setup-node@v4
      with:
        node-version: 20.x
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Build application
      run: npm run build

    - name: Start application
      run: npm run start &
      timeout-minutes: 1

    - name: Run Lighthouse
      uses: treosh/lighthouse-ci-action@v10
      with:
        urls: http://localhost:3000
        configPath: .lighthouserc.json
        uploadArtifacts: true
        temporaryPublicStorage: true
```

```json
// .lighthouserc.json
{
  "ci": {
    "collect": {
      "numberOfRuns": 3,
      "startServerCommand": "npm run start",
      "startServerReadyPattern": "ready on",
      "url": ["http://localhost:3000"]
    },
    "assert": {
      "assertions": {
        "categories:performance": "error",
        "categories:accessibility": "error",
        "categories:best-practices": "error",
        "categories:seo": "warn",
        "categories:pwa": "warn"
      }
    }
  }
}
```

## Docker Configuration

### ✅ Multi-Stage Docker Build

```dockerfile
# Dockerfile
FROM node:20-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./
RUN npm ci --only=production && npm cache clean --force

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build the application
RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy the built application
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["npm", "run", "start"]
```

### ✅ Docker Compose for Development

```yaml
# docker-compose.yml
version: '3.8'

services:
  webapp:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    volumes:
      - .:/app
      - /app/node_modules
    command: npm run dev

  robotics-mcp:
    image: robotics-mcp:latest
    ports:
      - "8888:8888"
    environment:
      - MCP_MODE=dual

  osc-mcp:
    image: osc-mcp:latest
    ports:
      - "8000:8000"
```

## Development Workflow

### ✅ Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.57.0
    hooks:
      - id: eslint
        files: \.(js|ts|tsx)$
        types: [file]

  - repo: local
    hooks:
      - id: type-check
        name: TypeScript Type Check
        entry: npx tsc --noEmit
        language: system
        files: \.(ts|tsx)$
        pass_filenames: false

  - repo: local
    hooks:
      - id: test
        name: Run Tests
        entry: npm run test
        language: system
        files: \.(js|ts|tsx)$
        pass_filenames: false
```

### ✅ VS Code Configuration

```json
// .vscode/settings.json
{
  "typescript.preferences.importModuleSpecifier": "non-relative",
  "typescript.suggest.autoImports": true,
  "typescript.updateImportsOnFileMove.enabled": "always",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "emmet.includeLanguages": {
    "typescript": "html",
    "typescriptreact": "html"
  },
  "files.associations": {
    "*.css": "tailwindcss"
  }
}
```

These standardized configurations ensure consistent, high-quality ECMAScript development across all MCP projects.
