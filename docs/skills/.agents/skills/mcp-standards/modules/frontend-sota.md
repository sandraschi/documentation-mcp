# Frontend SOTA Standards

## Overview
State-of-the-art standards for frontend development in MCP ecosystem, focusing on React, TypeScript, and modern web technologies.

## Technology Stack (SOTA Requirements)

### Core Technologies
- **React 18+** with modern hooks and concurrent features
- **TypeScript 5.0+** with strict type checking
- **Vite** for build tooling and development server
- **Tailwind CSS** for utility-first styling
- **React Query/TanStack Query** for server state management

### Required Dependencies
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.0.0",
    "@tanstack/react-query": "^5.0.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0"
  },
  "devDependencies": {
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "vite": "^5.0.0",
    "@vitejs/plugin-react": "^4.0.0"
  }
}
```

## Project Structure

### Standard Layout
```
frontend/
├── public/
│   ├── favicon.ico
│   └── assets/
├── src/
│   ├── components/
│   │   ├── ui/              # Reusable UI components
│   │   ├── layout/          # Layout components
│   │   └── forms/           # Form components
│   ├── pages/               # Route-based pages
│   ├── hooks/               # Custom React hooks
│   ├── lib/                 # Utilities and configurations
│   ├── services/            # API and external service integrations
│   ├── types/               # TypeScript type definitions
│   ├── constants/           # Application constants
│   └── styles/              # Global styles and Tailwind config
├── tests/                   # Test files
├── docs/                    # Component documentation
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── vite.config.ts
└── index.html
```

## Component Architecture

### Component Patterns
```typescript
// Component with proper TypeScript and React patterns
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  children
}) => {
  const baseClasses = "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50";

  const variantClasses = {
    primary: "bg-blue-600 text-white hover:bg-blue-700 focus-visible:ring-blue-500",
    secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200 focus-visible:ring-gray-500",
    danger: "bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-500"
  };

  const sizeClasses = {
    sm: "h-8 px-3 text-sm",
    md: "h-10 px-4 text-base",
    lg: "h-12 px-6 text-lg"
  };

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
};

export default Button;
```

### Custom Hooks
```typescript
// Custom hook for MCP server integration
import { useQuery, useMutation } from '@tanstack/react-query';

interface MCPServer {
  id: string;
  name: string;
  status: 'running' | 'stopped' | 'error';
  tools: string[];
}

export const useMCPServers = () => {
  return useQuery({
    queryKey: ['mcp-servers'],
    queryFn: async (): Promise<MCPServer[]> => {
      const response = await fetch('/api/mcp/servers');
      if (!response.ok) throw new Error('Failed to fetch MCP servers');
      return response.json();
    },
    staleTime: 30000, // 30 seconds
  });
};

export const useStartMCPServer = () => {
  return useMutation({
    mutationFn: async (serverId: string) => {
      const response = await fetch(`/api/mcp/servers/${serverId}/start`, {
        method: 'POST',
      });
      if (!response.ok) throw new Error('Failed to start MCP server');
      return response.json();
    },
  });
};
```

## State Management

### Server State with React Query
```typescript
// API service layer
class MCPApiService {
  private baseUrl: string;

  constructor(baseUrl = '/api') {
    this.baseUrl = baseUrl;
  }

  async getServers(): Promise<MCPServer[]> {
    const response = await fetch(`${this.baseUrl}/mcp/servers`);
    return response.json();
  }

  async startServer(serverId: string): Promise<void> {
    await fetch(`${this.baseUrl}/mcp/servers/${serverId}/start`, {
      method: 'POST',
    });
  }

  async stopServer(serverId: string): Promise<void> {
    await fetch(`${this.baseUrl}/mcp/servers/${serverId}/stop`, {
      method: 'POST',
    });
  }
}

// React Query setup
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 3,
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
    },
    mutations: {
      retry: 1,
    },
  },
});

// App.tsx
const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <AppContent />
      </Router>
    </QueryClientProvider>
  );
};
```

## MCP Integration Patterns

### MCP Server Management UI
```typescript
// MCP Server Dashboard Component
import React from 'react';
import { useMCPServers, useStartMCPServer, useStopMCPServer } from '../hooks/useMCPServers';

const MCPServerDashboard: React.FC = () => {
  const { data: servers, isLoading, error } = useMCPServers();
  const startServer = useStartMCPServer();
  const stopServer = useStopMCPServer();

  if (isLoading) return <div>Loading MCP servers...</div>;
  if (error) return <div>Error loading servers: {error.message}</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">MCP Server Management</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {servers?.map((server) => (
          <div key={server.id} className="border rounded-lg p-4 shadow-sm">
            <div className="flex justify-between items-center mb-3">
              <h3 className="font-semibold">{server.name}</h3>
              <StatusBadge status={server.status} />
            </div>

            <div className="mb-3">
              <p className="text-sm text-gray-600">
                {server.tools.length} tools available
              </p>
            </div>

            <div className="flex gap-2">
              {server.status === 'stopped' ? (
                <Button
                  onClick={() => startServer.mutate(server.id)}
                  disabled={startServer.isPending}
                  variant="primary"
                  size="sm"
                >
                  {startServer.isPending ? 'Starting...' : 'Start'}
                </Button>
              ) : (
                <Button
                  onClick={() => stopServer.mutate(server.id)}
                  disabled={stopServer.isPending}
                  variant="danger"
                  size="sm"
                >
                  {stopServer.isPending ? 'Stopping...' : 'Stop'}
                </Button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
```

## Testing Standards

### Component Testing
```typescript
// Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import Button from './Button';

describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('applies correct variant classes', () => {
    render(<Button variant="danger">Danger</Button>);
    const button = screen.getByText('Danger');
    expect(button).toHaveClass('bg-red-600');
  });
});
```

### Integration Testing
```typescript
// MCP Server integration test
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import MCPServerDashboard from './MCPServerDashboard';

// Mock the API
vi.mock('../services/mcpApi', () => ({
  getMCPServers: vi.fn(() => Promise.resolve([
    { id: '1', name: 'Test Server', status: 'running', tools: ['tool1', 'tool2'] }
  ]))
}));

const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: { retry: false },
  },
});

describe('MCPServerDashboard', () => {
  it('displays MCP servers', async () => {
    render(
      <QueryClientProvider client={createTestQueryClient()}>
        <MCPServerDashboard />
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Test Server')).toBeInTheDocument();
    });

    expect(screen.getByText('2 tools available')).toBeInTheDocument();
  });
});
```

## Performance Optimization

### Code Splitting
```typescript
// Lazy loading for route-based code splitting
import { lazy, Suspense } from 'react';

const MCPServerDashboard = lazy(() => import('./pages/MCPServerDashboard'));
const ToolManager = lazy(() => import('./pages/ToolManager'));

const App: React.FC = () => {
  return (
    <Router>
      <Suspense fallback={<div>Loading...</div>}>
        <Routes>
          <Route path="/servers" element={<MCPServerDashboard />} />
          <Route path="/tools" element={<ToolManager />} />
        </Routes>
      </Suspense>
    </Router>
  );
};
```

### Bundle Analysis
```javascript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    react(),
    visualizer({
      filename: 'dist/stats.html',
      open: true,
      gzipSize: true,
      brotliSize: true,
    }),
  ],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
          query: ['@tanstack/react-query'],
        },
      },
    },
  },
});
```

## Accessibility Standards

### ARIA Implementation
```typescript
// Accessible form component
interface TextInputProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  error?: string;
  required?: boolean;
  disabled?: boolean;
}

const TextInput: React.FC<TextInputProps> = ({
  label,
  value,
  onChange,
  error,
  required = false,
  disabled = false,
}) => {
  const inputId = `input-${label.toLowerCase().replace(/\s+/g, '-')}`;

  return (
    <div className="space-y-1">
      <label
        htmlFor={inputId}
        className="block text-sm font-medium text-gray-700"
      >
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>

      <input
        id={inputId}
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        required={required}
        aria-invalid={!!error}
        aria-describedby={error ? `${inputId}-error` : undefined}
        className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
          error ? 'border-red-500' : 'border-gray-300'
        } ${disabled ? 'bg-gray-100 cursor-not-allowed' : ''}`}
      />

      {error && (
        <p
          id={`${inputId}-error`}
          className="text-sm text-red-600"
          role="alert"
        >
          {error}
        </p>
      )}
    </div>
  );
};
```

## Next Steps
After frontend development, proceed to:
1. [MCP Integration Standards](./mcp-integration.md)
2. [Deployment Standards](./deployment.md)
3. [Performance Standards](./performance.md)