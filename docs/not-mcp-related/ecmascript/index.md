# ECMAScript Standards Index

**Comprehensive ECMAScript development standards for MCP projects**

## Overview

This section contains standardized patterns, best practices, and configurations for JavaScript/TypeScript development in MCP projects. These standards ensure consistency, type safety, and maintainability across all ECMAScript-based MCP components.

## Core Documents

### [📋 ECMAScript Standards](README.md)
Complete JavaScript/TypeScript development standards including:
- TypeScript patterns and best practices
- React component development
- Error handling and performance optimization
- Modern JavaScript (ES2022+) usage
- JSX patterns and anti-patterns

### [⚛️ JSX Patterns & Anti-Patterns](JSX_PATTERNS.md)
Common JSX issues and their solutions:
- Conditional rendering best practices
- Component structure guidelines
- Event handler patterns
- Performance optimization techniques
- Testing patterns for JSX components

### [🔷 TypeScript Patterns](TYPESCRIPT_PATTERNS.md)
Advanced TypeScript patterns for MCP development:
- Interface and type definitions
- Generic constraints and branded types
- React component typing
- MCP server tool definitions
- Error handling with Result types

### [🔧 Build Tools & Configuration](BUILD_TOOLS.md)
Standardized build configurations and tooling:
- Project structure standards (servers, webapps, MCP clients)
- MCP Client Integration Standards (stdio/HTTP connections)
- Package.json and dependency management
- TypeScript and ESLint configurations
- Next.js production setup
- CI/CD pipelines and Docker configurations

### [⚡ Bundlers Comparison](BUNDLERS_COMPARISON.md)
Turbopack vs Webpack comprehensive guide:
- Performance benchmarks and metrics
- When to choose each bundler
- Migration guides and compatibility issues
- Troubleshooting common bundler issues
- MCP-specific recommendations

### [🛡️ App Resilience & Anti-Crash](APP_RESILIENCE.md)
Comprehensive resilience framework:
- File watching (nodemon, chokidar, watchfiles)
- Process management (PM2, systemd, forever)
- Health checks and monitoring
- Crash recovery and auto-restart
- Circuit breakers and graceful shutdown

## Quick Reference

### TypeScript Essentials
```typescript
// Interface definitions
interface RobotState {
  id: string;
  position: Vector3;
  battery: number;
}

// Generic constraints
interface ApiResponse<T extends { id: string }> {
  success: boolean;
  data: T;
}

// Discriminated unions
type RobotCommand =
  | { type: 'move'; linear: number; angular: number }
  | { type: 'stop' }
  | { type: 'emergency_stop'; reason: string };
```

### JSX Patterns
```tsx
// ✅ Good: Ternary conditional rendering
{controlMode === 'manual' ? (
  <ManualControl />
) : controlMode === 'sensors' ? (
  <SensorDashboard />
) : (
  <CameraInterface />
)}

// ✅ Good: Type-safe event handlers
const handleVelocityChange = useCallback((
  axis: 'linear' | 'angular',
  value: number
) => {
  setVelocity(prev => ({ ...prev, [axis]: value }));
}, []);
```

### Component Best Practices
```tsx
// ✅ Good: Props with discriminated unions
type ButtonProps = PrimaryButtonProps | SecondaryButtonProps | DangerButtonProps;

// ✅ Good: Custom hooks for complex logic
function useRobotState(robotId: string) {
  const [state, setState] = useState<RobotState | null>(null);
  // ... hook logic
  return { state, isConnected };
}
```

## Implementation Checklist

### Project Setup
- [ ] TypeScript configuration matches standards
- [ ] ESLint rules configured for React/TypeScript
- [ ] Prettier configuration applied
- [ ] Path mappings configured (`@/components/*`, etc.)
- [ ] Testing framework set up (Jest + Testing Library)

### Code Quality
- [ ] Strict TypeScript mode enabled
- [ ] No `any` types (except in generated code)
- [ ] Comprehensive interface definitions
- [ ] Proper error handling patterns
- [ ] React hooks rules followed

### Component Development
- [ ] Functional components with hooks
- [ ] Type-safe props interfaces
- [ ] Proper conditional rendering (ternary operators)
- [ ] Memoization for expensive computations
- [ ] Error boundaries for fault isolation

### Testing
- [ ] Component tests with Testing Library
- [ ] Custom hook tests with `renderHook`
- [ ] Type-safe test utilities
- [ ] Coverage thresholds configured
- [ ] CI/CD testing pipeline

### Performance
- [ ] Bundle analysis configured
- [ ] Code splitting implemented
- [ ] Image optimization enabled
- [ ] Caching strategies applied
- [ ] Lighthouse CI configured

## Related Standards

- **[MCP Protocol Standards](../mcp-protocol/)** - MCP communication patterns
- **[FastMCP Standards](../fastmcp/)** - FastMCP framework usage
- **[Testing Standards](../testing/)** - Comprehensive testing patterns
- **[CI/CD Standards](../deployment/)** - Deployment and automation

## Contributing

When contributing ECMAScript code to MCP projects:

1. **Follow TypeScript Standards** - Strict typing, no `any` types
2. **Use JSX Patterns** - Ternary conditionals, proper event handling
3. **Write Tests** - Component and hook tests required
4. **Follow Build Standards** - ESLint, Prettier, proper configurations
5. **Document APIs** - Type-safe interfaces with comprehensive docs

## Troubleshooting

### Common Issues

**JSX Parsing Errors:**
- Use ternary operators instead of `&&` for conditionals
- Ensure proper JSX nesting and closing tags
- Check for missing imports

**TypeScript Errors:**
- Enable strict mode in tsconfig.json
- Use proper interface definitions
- Avoid `any` types

**Build Errors:**
- Check ESLint configuration
- Verify import paths and aliases
- Ensure proper dependency versions

**Performance Issues:**
- Use React.memo for expensive components
- Implement useMemo for costly computations
- Enable code splitting

These standards ensure high-quality, maintainable ECMAScript code across all MCP projects.
