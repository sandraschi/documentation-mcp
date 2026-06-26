# [BUG-002] Static Input Constraint (Non-Expanding Textboxes)

- **ID**: `BUG-002`
- **Severity**: `P2`
- **Date**: 2026-03-18
- **Repo/Component**: Generic Webapp / Input Components

## Symptom
Textboxes (Textareas) have a fixed height and do not expand or scroll when content exceeds the initial viewport, cutting off user input.

## Root Cause
Hardcoded `height` in CSS instead of `min-height` or lacks `overflow-y: auto`.

## Resolution
Implemented "Dynamic Scaling" rule in `WEBAPP_STANDARDS.md`.

## SOTA Impact
Updated [WEBAPP_STANDARDS.md](../../standards/WEBAPP_STANDARDS.md).
