# 🛡️ React Hardening Standards

Proactive development patterns to prevent common React pitfalls, specifically targeting stability in complex, agent-orchestrated web applications.

## 1. Hook Dependency Stability (MANDATORY)

### 1.1 `useCallback` for Handlers
All functions passed as props to child components or used in `useEffect` dependencies MUST be wrapped in `useCallback`.
- **Why**: Prevents child components from re-rendering unnecessarily and avoids infinite loops in effects.
- **Rule**: If it updates state or is used in an effect, it must be stable.

```tsx
// ✅ CORRECT
const handleSelection = useCallback((selection: Selection) => {
  setSelection(selection);
}, [setSelection]);
```

### 1.2 `useMemo` for Complex Computations
Transformations of data from stores or props used in render or effects must be memoized.
- **Rule**: Guard any object/array creation that is used as a dependency.

## 2. Render Loop Prevention

### 2.1 Guarded State Updates
Avoid direct state updates inside `useEffect` without conditional guards.
- **Pattern**: Check if the value has actually changed before calling `setState`.

### 2.2 `useRef` for "Silent" State
Use `useRef` for values that need to persist between renders but should NOT trigger a re-render.
- **Example**: Tracking the last "processed" value to avoid redundant API calls.

## 3. Component Life-cycle Safety

### 3.1 Cleanup Functions
Every `useEffect` that sets a timer, event listener, or async request MUST return a cleanup function.

### 3.2 Signal-Based Abort (SOTA)
Use `AbortController` for all API calls within effects to prevent state updates on unmounted components.

```tsx
useEffect(() => {
  const controller = new AbortController();
  fetchData(controller.signal);
  return () => controller.abort();
}, [dependencies]);
```

## 4. UI/UX Resilience

### 4.1 Skeleton & Loading States
Components MUST handle `isLoading` and `isProcessing` states gracefully using the SOTA AppLayout pattern.

### 4.2 Error Boundaries
Critical UI components (Viewers, Converters) MUST be wrapped in an Error Boundary to prevent application-wide crashes.
