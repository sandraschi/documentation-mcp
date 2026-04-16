# Inkscape MCP -- Project Status

**Last Updated**: 2026-02-15
**Repo**: `D:\Dev\repos\inkscape-mcp` | [GitHub](https://github.com/sandraschi/inkscape-mcp)
**Version**: v1.0.0
**Python**: 3.10+ | **Build**: Setuptools
**Status**: 🟢 PRODUCTION READY

---

## What It Is

Professional vector graphics and SVG operations for AI agents. Provides a bridge between natural language and the Inkscape vector engine.

**Key Capability**: Conversational SVG generation and complex vector manipulations (path boolean, transformations, filtering).

---

## Architecture

Organized into 6 core categories with 27 specialized vector operations:
- **Generation**: AI-powered natural language to SVG.
- **Paths**: Boolean operations, simplification, and offsets.
- **Objects**: Transform, align, and distribute.
- **Filters**: Professional SVG filter application.
- **Extensions**: Native access to 200+ Inkscape internal extensions.
- **IO**: High-fidelity export to PDF, PNG, and EPS.

---

## Current State

| Feature | Status | Notes |
|---------|--------|-------|
| AI SVG Gen | Working | Stable natural language to vector flow |
| Vector Ops | Working | 27 core operations verified |
| Ext. Access | Working | Bridge to legacy Inkscape extensions |
| CI/CD | Working | Automated GitHub Actions verification |

---

## Port Allocation

| Service | Port | Status |
|---------|------|--------|
| Dashboard | (TBD) | Planned for integration |
