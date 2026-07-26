# AppLayout Template

Fleet-standard sidebar + topbar for every webapp.

## Files

| File | Purpose |
|------|---------|
| `Shell.tsx` | Main layout — sidebar, topbar, health polling, zoom, connection store |
| `use-zoom.ts` | Standalone zoom hook (also embedded inline in Shell for single-file use) |

## Usage

1. Copy `Shell.tsx` into your webapp's components/ directory
2. Copy `use-zoom.ts` into hooks/ (or keep the embedded version in Shell)
3. Customize the `/* CUSTOMIZE */` sections:
   - `NAV` array — your routes
   - `BACKEND_PORT` — your backend port
   - `HEALTH_URL` — backend health endpoint
   - App name / version in sidebar logo area
   - Topbar title
4. Wire into App.tsx:

```tsx
import { Shell } from "./components/Shell";

export default function App() {
  return (
    <Shell>
      <Routes>...</Routes>
    </Shell>
  );
}
```

## Requirements

Add to package.json:

```json
"dependencies": {
  "framer-motion": "^11.0.0",
  "lucide-react": "^0.468.0",
  "zustand": "^5.0.0",
  "clsx": "^2.0.0"
}
```

## Features

- Retractable sidebar (collapse toggle at TOP, per fleet standard)
- Exponential backoff health polling (1s, 2s, 4s, 8s, 16s, 30s)
- Tauri `backend-status` event listener
- Zustand connection store (`useConnection`)
- Ctrl+Scroll Zoom (0.8× – 3.0×, persisted to localStorage)
- Framer Motion page transitions
- Dark theme compatible (uses Zinc palette)
- `data-testid="topbar"` and `data-testid="backend-dot"`
