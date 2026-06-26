# audiotool-nexus-mcp

**Status**: Active  
**Version**: 0.1.0  
**Stack**: Node.js, TypeScript, React (Vite), Zustand  
**Port**: 10900 (Webapp)

## Overview
A bridge between the [Model Context Protocol (MCP)](https://modelcontextprotocol.io) and the [Audiotool](https://audiotool.com) cloud DAW. It allows AI agents to manipulate studio projects in real-time through the Nexus SDK.

## Key Features
- **Project Orchestration**: Create devices, tracks, and MIDI regions via MCP tools.
- **Bi-directional Telemetry**: Real-time signal analysis and project state monitoring.
- **SOTA Dashboard**: Professional production views (Mixer, Sampler, Mastering) with high-res meters and spectral analysis.
- **Hyper-Vibecoding**: Pattern-based creative collaboration paradigm.

## Connection Info
The system uses **Stdio transport** for the MCP server and **Direct SDK integration** for the webapp.

### Auth
- **MCP Server**: Requires `AUDIOTOOL_PAT` (Personal Access Token).
- **Webapp**: Standard OAuth flow.

## Roadmap
- [ ] Direct audio streaming to local agents.
- [ ] Multi-user agentic collaboration.
- [ ] VST/Device preset randomization tools.

---
[README](file:///D:/Dev/repos/audiotool-nexus-mcp/README.md) | [Changelog](file:///D:/Dev/repos/audiotool-nexus-mcp/CHANGELOG.md)
