# [BUG-003] Malformed Media Scaling (Video UI)

- **ID**: `BUG-003`
- **Severity**: `P2`
- **Date**: 2026-03-18
- **Repo/Component**: Generic Webapp / Media Players

## Symptom
Video UI elements appear either too small (unusable) or too large (breaking layout) due to rigid width/height definitions.

## Root Cause
Lack of `aspect-ratio` control or container-relative sizing (`width: 100%`).

## Resolution
Implemented "Media Container Hygiene" in `WEBAPP_STANDARDS.md`.

## SOTA Impact
Updated [WEBAPP_STANDARDS.md](../../standards/WEBAPP_STANDARDS.md).
