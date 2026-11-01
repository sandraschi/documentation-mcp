# TypeScript Patterns for MCP Development

**Type-safe patterns and best practices for MCP server and webapp development**

## Type Definition Standards

### ✅ Interface vs Type Aliases

```typescript
// ✅ Use interfaces for object shapes (extensible)
interface RobotState {
  id: string;
  position: Vector3;
  velocity: Vector3;
  battery: number;
  status: RobotStatus;
}

// ✅ Use type aliases for unions and primitives
type RobotStatus = 'idle' | 'moving' | 'error' | 'charging';
type Vector3 = [number, number, number];
type RobotId = string & { readonly __brand: 'RobotId' };

// ❌ Don't use classes for data structures
class RobotState {
  constructor(public id: string, public position: Vector3) {}
}
```

### ✅ Generic Constraints

```typescript
// ✅ Constrain generics for type safety
interface ApiResponse<T extends { id: string }> {
  success: boolean;
  data: T;
  error?: string;
}

// ✅ Usage ensures type safety
const response: ApiResponse<Robot> = await api.getRobot('robot-1');
// TypeScript knows response.data has an id property
```

## React Component Patterns

### ✅ Props with Discriminated Unions

```typescript
// ✅ Discriminated union for component variants
type ButtonVariant = 'primary' | 'secondary' | 'danger';
type ButtonSize = 'sm' | 'md' | 'lg';

interface BaseButtonProps {
  children: React.ReactNode;
  onClick: () => void;
  disabled?: boolean;
}

interface PrimaryButtonProps extends BaseButtonProps {
  variant: 'primary';
  size?: ButtonSize;
}

interface SecondaryButtonProps extends BaseButtonProps {
  variant: 'secondary';
  size?: ButtonSize;
  outline?: boolean;
}

interface DangerButtonProps extends BaseButtonProps {
  variant: 'danger';
  confirmText?: string;
}

type ButtonProps = PrimaryButtonProps | SecondaryButtonProps | DangerButtonProps;

// ✅ Type-safe component
function Button(props: ButtonProps) {
  const { variant, children, onClick, disabled, ...rest } = props;

  const className = variant === 'primary'
    ? 'bg-blue-600 hover:bg-blue-700'
    : variant === 'secondary'
    ? 'bg-gray-600 hover:bg-gray-700'
    : 'bg-red-600 hover:bg-red-700';

  return (
    <button
      className={`${className} text-white px-4 py-2 rounded`}
      onClick={onClick}
      disabled={disabled}
      {...rest}
    >
      {children}
    </button>
  );
}
```

### ✅ Custom Hook Patterns

```typescript
// ✅ Generic custom hook with constraints
function useApi<TData, TError = Error>(
  url: string,
  options?: { method?: string; body?: any }
) {
  const [data, setData] = useState<TData | null>(null);
  const [error, setError] = useState<TError | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(url, {
        method: options?.method || 'GET',
        headers: { 'Content-Type': 'application/json' },
        body: options?.body ? JSON.stringify(options.body) : undefined,
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const result: TData = await response.json();
      setData(result);
      setError(null);
    } catch (err) {
      setError(err as TError);
      setData(null);
    } finally {
      setLoading(false);
    }
  }, [url, options]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, error, loading, refetch: fetchData };
}

// ✅ Type-safe usage
interface Robot {
  id: string;
  name: string;
  status: RobotStatus;
}

function RobotDashboard() {
  const { data: robots, error, loading } = useApi<Robot[]>('/api/robots');

  if (loading) return <div>Loading robots...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!robots) return <div>No robots found</div>;

  return (
    <div>
      {robots.map(robot => (
        <div key={robot.id}>
          <h3>{robot.name}</h3>
          <p>Status: {robot.status}</p>
        </div>
      ))}
    </div>
  );
}
```

## MCP Server Patterns

### ✅ FastMCP Tool Definitions

```typescript
import { FastMCP } from 'fastmcp';

// ✅ Strongly typed tool parameters
interface CreateRobotParams {
  robotId: string;
  robotType: 'scout' | 'go2' | 'g1';
  platform: 'unity' | 'vrchat';
  position?: {
    x: number;
    y: number;
    z: number;
  };
}

interface RobotResponse {
  success: boolean;
  robotId: string;
  message: string;
  data?: {
    position: { x: number; y: number; z: number };
    status: RobotStatus;
  };
}

// ✅ Type-safe tool implementation
export function createRobotTool(mcp: FastMCP, robotManager: RobotManager) {
  mcp.tool()(
    'create_robot',
    'Create a new virtual robot instance',
    {
      robotId: {
        type: 'string',
        description: 'Unique identifier for the robot',
        required: true,
      },
      robotType: {
        type: 'string',
        enum: ['scout', 'go2', 'g1'],
        description: 'Type of robot to create',
        required: true,
      },
      platform: {
        type: 'string',
        enum: ['unity', 'vrchat'],
        description: 'Target platform for the robot',
        required: true,
      },
      position: {
        type: 'object',
        description: 'Initial position (optional)',
        properties: {
          x: { type: 'number', default: 0 },
          y: { type: 'number', default: 0 },
          z: { type: 'number', default: 0 },
        },
      },
    }
  )(
    async (params: CreateRobotParams): Promise<RobotResponse> => {
      try {
        const robot = await robotManager.createRobot({
          id: params.robotId,
          type: params.robotType as RobotType,
          platform: params.platform as Platform,
          position: params.position || { x: 0, y: 0, z: 0 },
        });

        return {
          success: true,
          robotId: robot.id,
          message: `Robot ${robot.id} created successfully`,
          data: {
            position: robot.position,
            status: robot.status,
          },
        };
      } catch (error) {
        return {
          success: false,
          robotId: params.robotId,
          message: `Failed to create robot: ${error.message}`,
        };
      }
    }
  );
}
```

## Error Handling Patterns

### ✅ Result Types

```typescript
// ✅ Result type for operations that can fail
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

// ✅ Usage in functions
async function connectToRobot(robotId: string): Promise<Result<RobotConnection, ConnectionError>> {
  try {
    const connection = await robotApi.connect(robotId);
    return { success: true, data: connection };
  } catch (error) {
    return {
      success: false,
      error: new ConnectionError(`Failed to connect to ${robotId}: ${error.message}`)
    };
  }
}

// ✅ Type-safe error handling
const result = await connectToRobot('robot-1');
if (result.success) {
  // TypeScript knows result.data is RobotConnection
  console.log('Connected:', result.data.status);
} else {
  // TypeScript knows result.error is ConnectionError
  console.error('Connection failed:', result.error.message);
}
```

### ✅ Custom Error Classes

```typescript
// ✅ Hierarchical error classes
class RobotError extends Error {
  constructor(
    message: string,
    public readonly robotId: string,
    public readonly operation: string
  ) {
    super(message);
    this.name = 'RobotError';
  }
}

class ConnectionError extends RobotError {
  constructor(robotId: string, cause: string) {
    super(`Connection failed for robot ${robotId}: ${cause}`, robotId, 'connect');
    this.name = 'ConnectionError';
  }
}

class ValidationError extends RobotError {
  constructor(robotId: string, field: string, value: any) {
    super(`Invalid ${field} value: ${value}`, robotId, 'validate');
    this.name = 'ValidationError';
  }
}

// ✅ Type-safe error handling
try {
  await robot.connect();
} catch (error) {
  if (error instanceof ConnectionError) {
    // Handle connection errors specifically
    showConnectionError(error.robotId);
  } else if (error instanceof ValidationError) {
    // Handle validation errors
    showValidationError(error.field, error.value);
  } else {
    // Handle other errors
    showGenericError(error.message);
  }
}
```

## Utility Types

### ✅ Branded Types for Safety

```typescript
// ✅ Branded types prevent mixing incompatible values
type RobotId = string & { readonly __brand: 'RobotId' };
type UserId = string & { readonly __brand: 'UserId' };

// ✅ Factory functions for branded types
function createRobotId(id: string): RobotId {
  if (!id || typeof id !== 'string') {
    throw new Error('Invalid robot ID');
  }
  return id as RobotId;
}

function createUserId(id: string): UserId {
  if (!id || typeof id !== 'string') {
    throw new Error('Invalid user ID');
  }
  return id as UserId;
}

// ✅ Type-safe usage prevents mistakes
const robotId = createRobotId('robot-1');
const userId = createUserId('user-1');

// ❌ This would be a TypeScript error:
// const mixedId: RobotId = userId; // Type 'UserId' is not assignable to type 'RobotId'
```

### ✅ Strict Object Types

```typescript
// ✅ Exact object types (no extra properties)
type RobotConfig = {
  id: RobotId;
  name: string;
  maxVelocity: number;
  sensorTypes: readonly SensorType[];
};

// ✅ Builder pattern for complex objects
class RobotConfigBuilder {
  private config: Partial<RobotConfig> = {};

  id(id: RobotId): this {
    this.config.id = id;
    return this;
  }

  name(name: string): this {
    this.config.name = name;
    return this;
  }

  maxVelocity(velocity: number): this {
    this.config.maxVelocity = velocity;
    return this;
  }

  sensors(...types: SensorType[]): this {
    this.config.sensorTypes = types;
    return this;
  }

  build(): RobotConfig {
    if (!this.config.id || !this.config.name) {
      throw new Error('Robot ID and name are required');
    }

    return {
      id: this.config.id,
      name: this.config.name,
      maxVelocity: this.config.maxVelocity || 2.0,
      sensorTypes: this.config.sensorTypes || [],
    };
  }
}

// ✅ Type-safe fluent API
const config = new RobotConfigBuilder()
  .id(createRobotId('scout-1'))
  .name('Autonomous Scout')
  .maxVelocity(3.0)
  .sensors('lidar', 'camera', 'imu')
  .build();
```

## Testing Patterns

### ✅ Strongly Typed Tests

```typescript
import { describe, it, expect } from '@jest/globals';
import { render, screen, fireEvent } from '@testing-library/react';

// ✅ Type-safe test utilities
function renderRobotCard(robot: Robot) {
  return render(<RobotCard robot={robot} />);
}

// ✅ Strongly typed test data
const mockRobot: Robot = {
  id: 'test-robot' as RobotId,
  name: 'Test Robot',
  position: [0, 0, 0],
  velocity: [0, 0, 0],
  battery: 85,
  status: 'idle',
  sensors: [],
};

describe('RobotCard', () => {
  it('displays robot information correctly', () => {
    renderRobotCard(mockRobot);

    expect(screen.getByText('Test Robot')).toBeInTheDocument();
    expect(screen.getByText('Battery: 85%')).toBeInTheDocument();
    expect(screen.getByText('Status: idle')).toBeInTheDocument();
  });

  it('calls onSelect when clicked', () => {
    const onSelect = jest.fn();
    render(<RobotCard robot={mockRobot} onSelect={onSelect} />);

    fireEvent.click(screen.getByRole('button'));

    expect(onSelect).toHaveBeenCalledWith(mockRobot.id);
  });
});
```

## Configuration Patterns

### ✅ Typed Configuration

```typescript
// ✅ Strongly typed configuration
interface DatabaseConfig {
  host: string;
  port: number;
  database: string;
  username: string;
  password: string;
  ssl: boolean;
  connectionTimeout: number;
}

interface RobotApiConfig {
  baseUrl: string;
  apiKey: string;
  timeout: number;
  retryAttempts: number;
}

interface AppConfig {
  database: DatabaseConfig;
  robotApi: RobotApiConfig;
  logLevel: 'debug' | 'info' | 'warn' | 'error';
  environment: 'development' | 'staging' | 'production';
}

// ✅ Type-safe configuration loading
function loadConfig(): AppConfig {
  const config = {
    database: {
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT || '5432'),
      database: process.env.DB_NAME || 'robotics',
      username: process.env.DB_USER || 'robot',
      password: process.env.DB_PASSWORD || '',
      ssl: process.env.DB_SSL === 'true',
      connectionTimeout: parseInt(process.env.DB_TIMEOUT || '30000'),
    },
    robotApi: {
      baseUrl: process.env.ROBOT_API_URL || 'http://localhost:3000',
      apiKey: process.env.ROBOT_API_KEY || '',
      timeout: parseInt(process.env.ROBOT_API_TIMEOUT || '5000'),
      retryAttempts: parseInt(process.env.ROBOT_API_RETRIES || '3'),
    },
    logLevel: (process.env.LOG_LEVEL as AppConfig['logLevel']) || 'info',
    environment: (process.env.NODE_ENV as AppConfig['environment']) || 'development',
  };

  // Validate configuration
  if (!config.database.password) {
    throw new Error('Database password is required');
  }

  return config;
}
```

## Performance Patterns

### ✅ Memoized Computations

```typescript
// ✅ Type-safe memoization
function useRobotMetrics(robots: readonly Robot[]): RobotMetrics {
  return useMemo(() => {
    const total = robots.length;
    const connected = robots.filter(r => r.status === 'connected').length;
    const averageBattery = robots.reduce((sum, r) => sum + r.battery, 0) / total;
    const errorCount = robots.filter(r => r.status === 'error').length;

    return {
      total,
      connected,
      averageBattery: Math.round(averageBattery * 100) / 100,
      errorCount,
      healthScore: connected / total,
    };
  }, [robots]); // TypeScript ensures robots is readonly
}

// ✅ Strongly typed return value
interface RobotMetrics {
  total: number;
  connected: number;
  averageBattery: number;
  errorCount: number;
  healthScore: number;
}
```

Following these TypeScript patterns ensures type safety, maintainability, and prevents runtime errors in MCP development.
