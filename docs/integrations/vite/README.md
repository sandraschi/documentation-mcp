# Vite Integration Guide

**Timestamp**: 2026-01-23
**Status**: Frontend Standard

## Overview

Vite is a lightning-fast frontend build tool that has replaced Webpack as the standard for modern React applications. It provides Hot Module Replacement (HMR) that stays fast regardless of project size.

## Role in MyHomeServer

In this project, Vite serves as the development server and build pipeline for the React-based dashboard. It manages the compilation of TypeScript, processing of Tailwind CSS, and bundling of assets.

## Key Features

1.  **Instant Server Start**: Uses native ES modules in the browser to avoid bundling during development.
2.  **HMR**: Changes to your React components (e.g., `Cameras.tsx`) reflect in the browser instantly without losing state.
3.  **Plugin System**: Supports optimized builds for production using Rollup.

## Configuration (`vite.config.ts`)

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:10500' // Bridge to MyHomeServer backend
    }
  }
});
```

## Environment Variables

Vite uses a specific prefix for security:
*   Only variables starting with `VITE_` are exposed to your frontend code.
*   Access them via `import.meta.env.VITE_APP_TITLE`.

## Commands

```powershell
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build locally
npm run preview
```

## Best Practices

*   **Path Aliases**: Use `@/` for `src/` to avoid deeply nested relative imports.
*   **Asset Handling**: Place global assets in `public/` and component-specific assets in `src/assets/`.
*   **Dependencies**: Keep `devDependencies` clean; Vite handles most tree-shaking automatically.
