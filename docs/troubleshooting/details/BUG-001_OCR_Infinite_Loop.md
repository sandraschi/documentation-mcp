# [BUG-001] OCR-Scanner Infinite Render Loop

- **ID**: `BUG-001`
- **Severity**: `P1`
- **Date**: 2026-03-18
- **Repo/Component**: `ocr-mcp` / `ScanViewer.tsx`, `scanner.tsx`

## Symptom
The browser tab freezes or becomes unresponsive due to an infinite re-render loop when selecting regions or loading images.

## Root Cause
Unstable callback functions (not wrapped in `useCallback`) being passed as props to child components, combined with `useEffect` hooks that triggered state updates based on those props.

## Resolution
1. Wrapped all store-dispatching handlers in `useCallback`.
2. Refined `useEffect` dependency arrays in `ScanViewer.tsx` to ensure stable references.
3. Implemented guarded state updates in child components.

## SOTA Impact
Informed the creation of [REACT_HARDENING.md](../../standards/REACT_HARDENING.md).
