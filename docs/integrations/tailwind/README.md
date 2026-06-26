# Tailwind CSS Integration Guide

**Timestamp**: 2026-01-23
**Status**: UI/UX Standard

## Overview

Tailwind CSS is a utility-first CSS framework. Instead of writing custom CSS, you apply pre-defined classes directly to your HTML/React components.

## Role in MyHomeServer

Tailwind provides the **Beautiful Dark UI** of the dashboard. It ensures:
*   **Consistency**: Every spacing, color, and font size follows a strict design system.
*   **Performance**: It purges unused styles, resulting in tiny CSS files.
*   **Responsiveness**: Easy mobile-first design using prefixes like `md:`, `lg:`.

## Core Patterns in this Project

### 1. Utility Classes
```tsx
<div className="p-4 bg-card border border-border rounded-lg shadow-sm">
  <h2 className="text-xl font-bold text-primary">Camera 1</h2>
</div>
```

### 2. Dark Mode Standard
This project is **Dark-Only**. We use:
*   `bg-background`: The main dark background.
*   `text-foreground`: High-contrast text.
*   `text-muted-foreground`: Sub-text and labels.

### 3. Component Reusability
We use `cn` (a utility function in `utils/cn.ts`) to merge Tailwind classes safely.

```typescript
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

## Configuration (`tailwind.config.js`)

Custom colors for MyHomeServer are defined here:
```javascript
module.exports = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#3b82f6", // Smart home blue
        card: "#1e293b",    // Dark card background
      }
    }
  }
}
```

## Troubleshooting

*   **Styles not applying**: Ensure `postcss.config.js` exists. Tailwind requires PostCSS to process the classes.
*   **Class Overrides**: If two classes conflict, the last one in the CSS file usually wins. Use `tailwind-merge` (the `cn` function) to solve this professionally.
