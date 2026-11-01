# JSX Patterns & Anti-Patterns

**Common JSX issues and their solutions in MCP webapp development**

## Conditional Rendering Issues

### ❌ Problem: Logical AND in JSX
```tsx
// This causes parsing errors in complex components
{controlMode === 'manual' && <ManualControl />}
{controlMode === 'sensors' && <SensorDashboard />}
{controlMode === 'camera' && <CameraInterface />}
```

**Error:** `Parsing ecmascript source code failed - Unexpected token`

### ✅ Solution: Ternary Operators
```tsx
// Use ternary operators for conditional rendering
{controlMode === 'manual' ? (
  <ManualControl />
) : controlMode === 'sensors' ? (
  <SensorDashboard />
) : (
  <CameraInterface />
)}
```

### ✅ Alternative: Early Returns
```tsx
function ControlPanel({ mode }: { mode: string }) {
  if (mode === 'manual') return <ManualControl />;
  if (mode === 'sensors') return <SensorDashboard />;
  return <CameraInterface />;
}
```

## Component Structure Issues

### ❌ Problem: Missing Container Closures
```tsx
<div className="space-y-6">
  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
    {/* Content */}
  </div>
  {/* Missing closing div for space-y-6 */}
```

### ✅ Solution: Proper Nesting
```tsx
<div className="space-y-6">
  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
    {/* Content */}
  </div>
</div>
```

## Event Handler Issues

### ❌ Problem: Inline Arrow Functions in JSX
```tsx
// Causes unnecessary re-renders
<button onClick={() => handleClick(param)}>
  Click me
</button>
```

### ✅ Solution: useCallback Hooks
```tsx
const handleClick = useCallback((param: string) => {
  // Handle click
}, []); // Memoize to prevent re-renders

<button onClick={() => handleClick(param)}>
  Click me
</button>
```

### ✅ Better: Bind in Render (for simple cases)
```tsx
<button onClick={handleClick.bind(null, param)}>
  Click me
</button>
```

## State Management Issues

### ❌ Problem: State Updates in Render
```tsx
function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      {/* ❌ This causes infinite re-renders */}
      {setCount(count + 1)}
      <p>Count: {count}</p>
    </div>
  );
}
```

### ✅ Solution: Effects for Side Effects
```tsx
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    // Side effects go here
    document.title = `Count: ${count}`;
  }, [count]);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>+</button>
    </div>
  );
}
```

## Props Destructuring Issues

### ❌ Problem: Deep Props Access
```tsx
function RobotCard({ robot }: { robot: Robot }) {
  return (
    <div>
      <h3>{robot.name}</h3>
      <p>{robot.status.battery.level}%</p>
      <p>{robot.status.temperature.value}°C</p>
    </div>
  );
}
```

### ✅ Solution: Destructure Props
```tsx
function RobotCard({ robot }: { robot: Robot }) {
  const { name, status: { battery, temperature } } = robot;

  return (
    <div>
      <h3>{name}</h3>
      <p>{battery.level}%</p>
      <p>{temperature.value}°C</p>
    </div>
  );
}
```

## List Rendering Issues

### ❌ Problem: Missing Keys in Lists
```tsx
function RobotList({ robots }: { robots: Robot[] }) {
  return (
    <div>
      {robots.map(robot => (
        <RobotCard robot={robot} /> {/* Missing key */}
      ))}
    </div>
  );
}
```

### ✅ Solution: Add Unique Keys
```tsx
function RobotList({ robots }: { robots: Robot[] }) {
  return (
    <div>
      {robots.map(robot => (
        <RobotCard key={robot.id} robot={robot} />
      ))}
    </div>
  );
}
```

## Performance Issues

### ❌ Problem: Unnecessary Re-renders
```tsx
function RobotDashboard({ robots }: { robots: Robot[] }) {
  // This recalculates on every render
  const connectedCount = robots.filter(r => r.connected).length;

  return (
    <div>
      <p>Connected: {connectedCount}</p>
      {/* ... */}
    </div>
  );
}
```

### ✅ Solution: useMemo for Expensive Calculations
```tsx
function RobotDashboard({ robots }: { robots: Robot[] }) {
  const connectedCount = useMemo(() => {
    return robots.filter(r => r.connected).length;
  }, [robots]);

  return (
    <div>
      <p>Connected: {connectedCount}</p>
      {/* ... */}
    </div>
  );
}
```

## TypeScript Issues in JSX

### ❌ Problem: Implicit Any in Event Handlers
```tsx
function VelocitySlider({ onChange }: { onChange: (value: number) => void }) {
  return (
    <input
      type="range"
      onChange={(e) => onChange(e.target.value)} {/* e.target.value is string */}
    />
  );
}
```

### ✅ Solution: Proper Type Casting
```tsx
function VelocitySlider({ onChange }: { onChange: (value: number) => void }) {
  return (
    <input
      type="range"
      onChange={(e) => onChange(parseFloat(e.target.value))}
    />
  );
}
```

### ✅ Better: Typed Event Handlers
```tsx
function VelocitySlider({ onChange }: { onChange: (value: number) => void }) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(parseFloat(e.target.value));
  };

  return (
    <input
      type="range"
      onChange={handleChange}
    />
  );
}
```

## Async Operations in JSX

### ❌ Problem: Async Operations in Render
```tsx
function RobotStatus({ robotId }: { robotId: string }) {
  const [status, setStatus] = useState(null);

  // ❌ This is wrong - async in render
  getRobotStatus(robotId).then(setStatus);

  return <div>{status ? 'Connected' : 'Disconnected'}</div>;
}
```

### ✅ Solution: useEffect for Async Operations
```tsx
function RobotStatus({ robotId }: { robotId: string }) {
  const [status, setStatus] = useState(null);

  useEffect(() => {
    getRobotStatus(robotId).then(setStatus);
  }, [robotId]);

  return <div>{status ? 'Connected' : 'Disconnected'}</div>;
}
```

### ✅ Better: Custom Hook
```tsx
function useRobotStatus(robotId: string) {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getRobotStatus(robotId)
      .then(setStatus)
      .finally(() => setLoading(false));
  }, [robotId]);

  return { status, loading };
}

function RobotStatus({ robotId }: { robotId: string }) {
  const { status, loading } = useRobotStatus(robotId);

  if (loading) return <div>Loading...</div>;
  return <div>{status ? 'Connected' : 'Disconnected'}</div>;
}
```

## Form Handling Issues

### ❌ Problem: Uncontrolled Components
```tsx
function RobotConfig({ onSave }: { onSave: (config: Config) => void }) {
  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      const formData = new FormData(e.target);
      onSave(Object.fromEntries(formData)); // Type unsafe
    }}>
      <input name="robotName" type="text" />
      <input name="maxVelocity" type="number" />
      <button type="submit">Save</button>
    </form>
  );
}
```

### ✅ Solution: Controlled Components
```tsx
function RobotConfig({ onSave }: { onSave: (config: Config) => void }) {
  const [config, setConfig] = useState({ robotName: '', maxVelocity: 1 });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(config);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={config.robotName}
        onChange={(e) => setConfig(prev => ({ ...prev, robotName: e.target.value }))}
        type="text"
      />
      <input
        value={config.maxVelocity}
        onChange={(e) => setConfig(prev => ({ ...prev, maxVelocity: parseFloat(e.target.value) }))}
        type="number"
      />
      <button type="submit">Save</button>
    </form>
  );
}
```

## Error Boundary Issues

### ❌ Problem: No Error Boundaries
```tsx
function RobotControl() {
  // If this throws, entire app crashes
  const robot = getRobotData();

  return <RobotDashboard robot={robot} />;
}
```

### ✅ Solution: Error Boundaries
```tsx
class RobotErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Robot control error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <div className="text-red-600 p-4 border border-red-200 rounded">
        Robot control temporarily unavailable. Please refresh.
      </div>;
    }

    return this.props.children;
  }
}

// Usage
<RobotErrorBoundary>
  <RobotControl />
</RobotErrorBoundary>
```

## Testing JSX Components

### ✅ Good: Testing Library Patterns
```tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';

describe('RobotControl', () => {
  it('renders control interface', () => {
    render(<RobotControl robotId="test-robot" />);

    expect(screen.getByText('Manual Control')).toBeInTheDocument();
    expect(screen.getByLabelText('Linear Velocity (m/s)')).toBeInTheDocument();
  });

  it('updates velocity on slider change', async () => {
    render(<RobotControl robotId="test-robot" />);

    const slider = screen.getByLabelText('Linear Velocity (m/s)');
    fireEvent.change(slider, { target: { value: '1.5' } });

    await waitFor(() => {
      expect(screen.getByText('Current: 1.50 m/s')).toBeInTheDocument();
    });
  });

  it('handles emergency stop', () => {
    render(<RobotControl robotId="test-robot" />);

    const stopButton = screen.getByText('Emergency Stop');
    fireEvent.click(stopButton);

    expect(screen.getByText('Reset E-Stop')).toBeInTheDocument();
  });
});
```

## Migration Guide

### Converting from Logical AND to Ternary

**Before:**
```tsx
<div>
  {mode === 'manual' && <ManualPanel />}
  {mode === 'auto' && <AutoPanel />}
</div>
```

**After:**
```tsx
<div>
  {mode === 'manual' ? (
    <ManualPanel />
  ) : mode === 'auto' ? (
    <AutoPanel />
  ) : null}
</div>
```

### Converting from Uncontrolled to Controlled

**Before:**
```tsx
<input name="velocity" defaultValue={1.0} />
```

**After:**
```tsx
const [velocity, setVelocity] = useState(1.0);
<input
  value={velocity}
  onChange={(e) => setVelocity(parseFloat(e.target.value))}
/>
```

Following these patterns prevents common JSX issues and ensures maintainable, performant React components.
