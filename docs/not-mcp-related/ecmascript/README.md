# ECMAScript Standards for MCP Projects

**JavaScript/TypeScript Development Standards and Best Practices**

## Overview

This document defines ECMAScript standards for MCP server development, focusing on JavaScript and TypeScript best practices, JSX patterns, and modern development workflows.

## Core Principles

### 1. TypeScript First
- **All new code**: TypeScript mandatory
- **Type safety**: Strict mode enabled
- **Interface definitions**: Comprehensive type coverage
- **Generic patterns**: Type-safe abstractions

### 2. Modern JavaScript
- **ES2022+ features**: Latest stable ECMAScript
- **Async/await patterns**: No Promise chains
- **Destructuring**: Preferred over object access
- **Template literals**: Over string concatenation

### 3. JSX Standards
- **Component patterns**: Functional components with hooks
- **Conditional rendering**: Ternary operators over && patterns
- **Props typing**: Strict interface definitions
- **Event handling**: Type-safe event signatures

## TypeScript Standards

### Interface Definitions
```typescript
// ✅ GOOD: Comprehensive interface
interface RobotControlProps {
  robotId: string;
  linearVelocity: number;
  angularVelocity: number;
  onVelocityChange: (linear: number, angular: number) => void;
  isConnected: boolean;
  emergencyStop?: boolean;
}

// ❌ BAD: Missing types
interface RobotControlProps {
  robotId: any;
  velocity: number; // Too vague
  callback: Function; // Too generic
}
```

### Generic Type Patterns
```typescript
// ✅ GOOD: Generic API response
interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: string;
  timestamp: Date;
}

// Usage
const robotResponse: ApiResponse<RobotState> = await api.getRobot('scout-01');
```

### Union Types for State
```typescript
// ✅ GOOD: Exhaustive state management
type ControlMode = 'manual' | 'autonomous' | 'emergency';

interface ControlState {
  mode: ControlMode;
  velocity: {
    linear: number;
    angular: number;
  };
}

// ✅ GOOD: Discriminated unions
type RobotCommand =
  | { type: 'move'; linear: number; angular: number }
  | { type: 'stop' }
  | { type: 'emergency_stop'; reason: string };
```

## JSX Patterns

### Conditional Rendering
```tsx
// ✅ GOOD: Ternary operator (recommended)
{controlMode === 'manual' ? (
  <ManualControlPanel />
) : controlMode === 'sensors' ? (
  <SensorDashboard />
) : (
  <CameraInterface />
)}

// ❌ BAD: Logical AND (causes parsing issues)
{controlMode === 'manual' && <ManualControlPanel />}

// ❌ BAD: Complex conditions
{controlMode === 'manual' ? <ManualControlPanel /> : null}
{controlMode === 'sensors' ? <SensorDashboard /> : null}
{controlMode === 'camera' ? <CameraInterface /> : null}
```

### Component Props
```tsx
// ✅ GOOD: Interface-based props
interface VelocityControlProps {
  value: number;
  onChange: (value: number) => void;
  min: number;
  max: number;
  step: number;
  disabled?: boolean;
  label: string;
}

function VelocityControl({
  value,
  onChange,
  min,
  max,
  step,
  disabled = false,
  label
}: VelocityControlProps) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium">{label}</label>
      <input
        type="range"
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        min={min}
        max={max}
        step={step}
        disabled={disabled}
        className="w-full"
      />
    </div>
  );
}
```

### Event Handlers
```tsx
// ✅ GOOD: Type-safe event handlers
function RobotControl() {
  const [velocity, setVelocity] = useState({ linear: 0, angular: 0 });

  const handleVelocityChange = useCallback((
    axis: 'linear' | 'angular',
    value: number
  ) => {
    setVelocity(prev => ({ ...prev, [axis]: value }));
  }, []);

  const handleEmergencyStop = useCallback(() => {
    // Emergency stop logic
    setVelocity({ linear: 0, angular: 0 });
  }, []);

  return (
    <div>
      <VelocityControl
        label="Linear Velocity (m/s)"
        value={velocity.linear}
        onChange={(value) => handleVelocityChange('linear', value)}
        min={-2}
        max={2}
        step={0.1}
      />
      <button
        onClick={handleEmergencyStop}
        className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded"
      >
        Emergency Stop
      </button>
    </div>
  );
}
```

## React Hooks Patterns

### Custom Hooks
```tsx
// ✅ GOOD: Custom hook for robot state
function useRobotState(robotId: string) {
  const [state, setState] = useState<RobotState | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const connect = async () => {
      try {
        const connection = await roboticsMcp.connect(robotId);
        setIsConnected(true);

        // Set up real-time updates
        const unsubscribe = connection.onStateChange(setState);
        return unsubscribe;
      } catch (error) {
        console.error('Failed to connect to robot:', error);
        setIsConnected(false);
      }
    };

    connect();
  }, [robotId]);

  return { state, isConnected };
}

// Usage
function RobotDashboard({ robotId }: { robotId: string }) {
  const { state, isConnected } = useRobotState(robotId);

  if (!isConnected) {
    return <div className="text-red-600">Disconnected</div>;
  }

  return (
    <div className="p-4 border rounded">
      <h3 className="font-bold">Robot {robotId}</h3>
      <p>Status: {state?.status || 'Unknown'}</p>
    </div>
  );
}
```

### Effect Dependencies
```tsx
// ✅ GOOD: Proper dependency arrays
useEffect(() => {
  const interval = setInterval(() => {
    updateRobotState(robotId);
  }, 50); // 20Hz updates

  return () => clearInterval(interval);
}, [robotId]); // Include all dependencies

// ✅ GOOD: Empty array for mount-only effects
useEffect(() => {
  console.log('Robot control mounted');
  return () => console.log('Robot control unmounted');
}, []); // Empty array = run once

// ❌ BAD: Missing dependencies
useEffect(() => {
  updateRobotState(robotId); // robotId not in deps
}, []); // Will use stale robotId
```

## Error Handling

### Async Error Boundaries
```tsx
// ✅ GOOD: Error boundary for async operations
function RobotControlErrorBoundary({
  children,
  fallback
}: {
  children: React.ReactNode;
  fallback: (error: Error) => React.ReactNode;
}) {
  const [error, setError] = useState<Error | null>(null);

  if (error) {
    return fallback(error);
  }

  return (
    <ErrorContext.Provider value={{ setError }}>
      {children}
    </ErrorContext.Provider>
  );
}

// Usage
<RobotControlErrorBoundary
  fallback={(error) => (
    <div className="bg-red-50 border border-red-200 p-4 rounded">
      <h3 className="text-red-800 font-bold">Control Error</h3>
      <p className="text-red-700">{error.message}</p>
    </div>
  )}
>
  <RobotControlPanel />
</RobotControlErrorBoundary>
```

### API Error Handling
```tsx
// ✅ GOOD: Structured error responses
interface ApiError {
  code: string;
  message: string;
  details?: Record<string, any>;
}

async function sendRobotCommand(command: RobotCommand): Promise<RobotResponse> {
  try {
    const response = await fetch('/api/robot/command', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(command),
    });

    if (!response.ok) {
      const errorData: ApiError = await response.json();
      throw new Error(`${errorData.code}: ${errorData.message}`);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error('Network error: Unable to connect to robot');
    }
    throw error;
  }
}
```

## Performance Optimization

### Memoization
```tsx
// ✅ GOOD: Memoize expensive computations
const robotStatusSummary = useMemo(() => {
  return {
    totalRobots: robots.length,
    connectedRobots: robots.filter(r => r.connected).length,
    averageBattery: robots.reduce((sum, r) => sum + r.battery, 0) / robots.length,
    alerts: robots.filter(r => r.battery < 20 || r.temperature > 60).length,
  };
}, [robots]);

// ✅ GOOD: Callback memoization
const handleRobotSelect = useCallback((robotId: string) => {
  setSelectedRobot(robotId);
  // Additional logic...
}, []); // Empty deps = stable reference
```

### Component Optimization
```tsx
// ✅ GOOD: Component memoization
const RobotCard = memo<{
  robot: Robot;
  onSelect: (id: string) => void;
}>(({ robot, onSelect }) => {
  return (
    <div
      className="p-4 border rounded cursor-pointer hover:shadow-md"
      onClick={() => onSelect(robot.id)}
    >
      <h3 className="font-bold">{robot.name}</h3>
      <p>Battery: {robot.battery}%</p>
      <p>Status: {robot.connected ? 'Connected' : 'Disconnected'}</p>
    </div>
  );
});

// ✅ GOOD: List optimization
function RobotList({ robots }: { robots: Robot[] }) {
  return (
    <div className="space-y-2">
      {robots.map(robot => (
        <RobotCard
          key={robot.id}
          robot={robot}
          onSelect={handleRobotSelect}
        />
      ))}
    </div>
  );
}
```

## Testing Standards

### Component Testing
```tsx
// ✅ GOOD: Component test with user events
import { render, screen, fireEvent } from '@testing-library/react';
import { RobotControl } from './RobotControl';

describe('RobotControl', () => {
  it('updates velocity on slider change', () => {
    render(<RobotControl robotId="test-robot" />);

    const slider = screen.getByLabelText('Linear Velocity (m/s)');
    fireEvent.change(slider, { target: { value: '1.5' } });

    expect(screen.getByText('Current: 1.50 m/s')).toBeInTheDocument();
  });

  it('disables controls during emergency stop', () => {
    render(<RobotControl robotId="test-robot" />);

    const emergencyButton = screen.getByText('Emergency Stop');
    fireEvent.click(emergencyButton);

    const slider = screen.getByLabelText('Linear Velocity (m/s)');
    expect(slider).toBeDisabled();
  });
});
```

### Hook Testing
```tsx
// ✅ GOOD: Custom hook testing
import { renderHook, act } from '@testing-library/react';
import { useRobotState } from './useRobotState';

describe('useRobotState', () => {
  it('connects to robot on mount', async () => {
    const { result } = renderHook(() => useRobotState('test-robot'));

    // Initially not connected
    expect(result.current.isConnected).toBe(false);

    // Wait for connection
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 100));
    });

    expect(result.current.isConnected).toBe(true);
  });
});
```

## Build Configuration

### Next.js Configuration
```javascript
// ✅ GOOD: next.config.js with proper settings
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  typescript: {
    strict: true,
    noImplicitAny: true,
  },
  eslint: {
    ignoreDuringBuilds: false,
  },
};

module.exports = nextConfig;
```

### TypeScript Configuration
```json
// ✅ GOOD: tsconfig.json for MCP webapps
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
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

## Common Issues & Solutions

### JSX Parsing Errors
```tsx
// ❌ PROBLEM: Logical AND in JSX
{condition && <Component />}

// ✅ SOLUTION: Ternary operator
{condition ? <Component /> : null}
```

### Type Errors
```tsx
// ❌ PROBLEM: Implicit any
function handleChange(value) { // 'value' is any
  // ...
}

// ✅ SOLUTION: Explicit types
function handleChange(value: number) {
  // ...
}
```

### Memory Leaks
```tsx
// ❌ PROBLEM: Missing cleanup
useEffect(() => {
  const interval = setInterval(callback, 1000);
  // No cleanup!
}, []);

// ✅ SOLUTION: Cleanup function
useEffect(() => {
  const interval = setInterval(callback, 1000);
  return () => clearInterval(interval);
}, []);
```

## Tools & Linting

### ESLint Configuration
```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'next/core-web-vitals',
    '@typescript-eslint/recommended',
  ],
  rules: {
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/no-explicit-any': 'warn',
    'react-hooks/exhaustive-deps': 'error',
    'react/jsx-key': 'error',
  },
};
```

### Prettier Configuration
```javascript
// .prettierrc.js
module.exports = {
  semi: true,
  trailingComma: 'es5',
  singleQuote: true,
  printWidth: 100,
  tabWidth: 2,
  useTabs: false,
};
```

## Performance Monitoring

### Bundle Analysis
```bash
# Analyze bundle size
npm run build
npx @next/bundle-analyzer
```

### Runtime Performance
```tsx
// ✅ GOOD: Performance monitoring
import { useEffect } from 'react';

function RobotDashboard() {
  useEffect(() => {
    const startTime = performance.now();

    return () => {
      const endTime = performance.now();
      console.log(`RobotDashboard render time: ${endTime - startTime}ms`);
    };
  });

  return <div>Robot controls...</div>;
}
```

## Security Considerations

### Input Validation
```tsx
// ✅ GOOD: Validate all inputs
interface RobotCommand {
  robotId: string;
  command: 'move' | 'stop' | 'rotate';
  parameters: Record<string, number>;
}

function validateCommand(input: any): RobotCommand {
  if (!input.robotId || typeof input.robotId !== 'string') {
    throw new Error('Invalid robot ID');
  }

  if (!['move', 'stop', 'rotate'].includes(input.command)) {
    throw new Error('Invalid command');
  }

  // Validate parameters...
  return input as RobotCommand;
}
```

### XSS Prevention
```tsx
// ✅ GOOD: Sanitize user inputs
import DOMPurify from 'dompurify';

function RobotStatus({ status }: { status: string }) {
  const sanitizedStatus = DOMPurify.sanitize(status);

  return (
    <div dangerouslySetInnerHTML={{ __html: sanitizedStatus }} />
  );
}
```

## Conclusion

Following these ECMAScript standards ensures:
- **Type Safety**: Comprehensive TypeScript coverage
- **Performance**: Optimized React patterns
- **Maintainability**: Consistent code structure
- **Reliability**: Proper error handling
- **Testability**: Comprehensive test coverage

These standards evolve with ECMAScript specifications and React best practices.
