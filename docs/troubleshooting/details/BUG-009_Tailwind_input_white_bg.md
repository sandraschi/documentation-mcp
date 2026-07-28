# BUG-009: Tailwind `input` Class White Background in Dark Theme

- **Severity**: P2
- **Date**: 2026-07-25
- **Component**: Fleet-wide (webapp inputs)

## Symptom

Text inputs (`<input>`, `<select>`) using `className="input"` or `className="input w-full"` render with a white background and light grey text, making them unreadable in dark theme webapps.

## Root Cause

Tailwind's `input` class is auto-generated from the `--input` CSS variable or Tailwind forms base styles. When `--input` is not explicitly set for dark mode (or when Tailwind's default forms styles are used), the background defaults to white with dark text — invisible in a dark-themed app.

**Affected pattern:**
```tsx
<input className="input" ... />
<input className="input w-full" ... />
```

## Resolution

Replace bare `input` class with explicit dark-theme Tailwind classes:

```tsx
// Before
className="input"
className="input w-full"

// After
className="bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-2 text-sm text-white placeholder-zinc-500 outline-none focus:ring-1 focus:ring-amber-500/30"
```

Also add `color-scheme: dark` to the global CSS so native date pickers and form controls render dark:

```css
body { color-scheme: dark; }
input, select, textarea { color-scheme: dark; }
```

## Affected Repos (Fixed)

| Repo | Files | Pattern |
|------|-------|---------|
| advanced-memory-mcp | NoteViewer.tsx, ExportSettings.tsx, ResearchSettings.tsx, LLMProviderSettings.tsx | `input w-full` |
| scraper-mcp | tools.tsx, logs.tsx | `input` |
| toolbench-mcp | ToolsPage.tsx, LogsPage.tsx, SettingsPage.tsx | `input` |

## Fleet Scan Results

19 repos were found with `input` substring in className, but most use `border-input` (border color only, not background) which is harmless. The actual bug pattern is the bare `input` class or `bg-input`.

## Prevention

- **Do not use** `className="input"` bare class in dark-theme apps.
- Always use explicit dark-theme styling on inputs.
- Set `color-scheme: dark` in the root CSS for native form controls.
- Alternatively, define a custom `input` component class with proper dark theme values in main.css.
