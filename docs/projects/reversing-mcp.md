# reversing-mcp — Project Documentation

**Status:** In Progress (incomplete, architectural decision needed)  
**Location:** `D:\Dev\repos\reversing-mcp`  
**GitHub:** `https://github.com/sandraschi/reversing-mcp` (private)  
**Last Updated:** 2026-03-23  

---

## What This Project Is

An MCP server for AI-assisted binary reverse engineering, combining:
1. A bridge to Ghidra (currently via LaurieWired's GhidraMCP HTTP plugin)
2. Standalone binary analysis tools (PE parsing, entropy, hexdump, strings)
3. Directmedia legacy format decoder (.DKI files from 1990s German CD-ROM encyclopedias)
4. A Next.js web UI and a Vite web UI (both exist, both partially functional)

The Ghidra integration is the main gap: it requires a live Ghidra GUI + plugin running on localhost:8080, which is not agentic. Headless/automated analysis is not yet implemented.

---

## Current State (2026-03-23)

### What Works
- `analyze_binary`, `extract_strings`, `get_hexdump`, `analyze_entropy`, `analyze_pe_file` — Python-native, no external tools needed
- `analyze_directmedia_file`, `decompress_directmedia_library` — Directmedia .DKI decoding (proprietary 1990s format)
- GhidraMCP bridge (`bridge_mcp_ghidra.py`) — works IF Ghidra GUI + LaurieWired plugin is running on :8080
- FastAPI + uvicorn HTTP endpoint (`/mcp`, `/health`) — functional
- Two web UIs (reversing-webapp Next.js + web_sota Vite) — exist but are tech demos

### What Doesn't Work / Is Missing
- **No headless Ghidra** — all Ghidra tools require GUI to be running
- **No pyghidra integration** — the correct 2026 approach
- **GhidraMCP bridge is just a pass-through** — no value added over LaurieWired directly
- **glama.json exists but server not publication-ready** — incomplete tool set for gold standard
- **Two competing web UIs** — should pick one (Vite/web_sota is cleaner)
- `server.py` bak files suggest unfinished refactoring
- `debug_proj.gpr` — actual Ghidra project present (some real reversing happened)

### Tech Stack
- Python 3.13, FastMCP 3.x (venv has fastmcp installed)
- FastAPI + uvicorn for HTTP transport
- pyproject.toml with proper packaging
- Tests exist but some fail (pytest cache present)
- ruff for linting
- `.cursor/skills/reversing-expert` — Cursor skill for RE context

---

## Architecture Decision Needed

### Option A: Pivot to pyghidra headless (recommended)
Replace LaurieWired bridge with `ghidra-headless-mcp` (mrphrazer) or ReVa headless.
- Pro: Actually agentic, no GUI required
- Pro: 212 tools vs 40 in LaurieWired
- Con: Requires Ghidra 12.0+ and pyghidra setup on Goliath
- Con: mrphrazer repo is very new (March 2026, 3 commits, 24 stars)

### Option B: Keep LaurieWired bridge, add value elsewhere
Keep GUI-dependent Ghidra, focus on what's unique: static analysis + Directmedia tools.
- Pro: Works today
- Con: Not agentic, not suitable for automation

### Option C: Hybrid — supplement ReVa with our static tools
Run ReVa or ghidra-headless-mcp for Ghidra integration, keep our server for:
- static analysis (entropy, PE, hex)
- Directmedia/legacy format decoding
- Binary prep pipeline
- Pro: Clear scope, plays to our strengths
- **This is the recommended path**

---

## External Repos (Cloned for Analysis)

All cloned to `D:\Dev\repos\reversing-mcp\external\`

### 1. LaurieWired/GhidraMCP
- **Path:** `external\GhidraMCP`
- **Stars:** 7.6k, 645 forks — community standard
- **Architecture:** Java Ghidra plugin (HTTP :8080) + Python bridge
- **Requires:** Ghidra GUI running, binary loaded, plugin started
- **Tools:** ~40 (decompile, rename, xrefs, imports/exports, strings)
- **Limitation:** GUI-coupled, not headless, not agentic
- **Our current use:** `bridge_mcp_ghidra.py` is essentially their bridge.py
- **Assessment:** Superseded by headless approaches for agentic RE, but fine for interactive sessions

### 2. mrphrazer/ghidra-headless-mcp
- **Path:** `external\ghidra-headless-mcp`
- **Stars:** 24 — very new (2026-03)
- **Author:** Tim Blazytko (@mr_phrazer) — respected RE researcher
- **Architecture:** pyghidra backend, pure Python, NO GUI required
- **Tools:** 212 tools across 34 feature groups — most comprehensive available
- **Unique features:**
  - P-code access (intermediate representation, architecture-agnostic)
  - Transaction/undo management for safe agentic mutation
  - `ghidra.eval` / `ghidra.call` / `ghidra.script` — arbitrary scripting
  - CFG edges, basic blocks, type system, struct building
  - Fake backend mode for CI without Ghidra
  - Stdio + TCP transports
- **Limitation:** Very new, Windows untested, pyghidra version compatibility unclear
- **Assessment:** Architecturally correct for 2026, needs Windows validation

### 3. cyberkaida/reverse-engineering-assistant (ReVa)
- **Path:** `external\reverse-engineering-assistant`
- **Stars:** 619, 56 forks
- **Architecture:** Ghidra extension (Java) + MCP server, both assistant and headless modes
- **Requires:** Ghidra 12.0+ for headless mode
- **Transport:** Streamable HTTP MCP transport (port 8080 in assistant mode)
- **Key design philosophy:** Tools designed specifically for LLM consumption
  - Small, focused tools that return xrefs + namespace context alongside results
  - Nudges LLM toward human-like binary exploration patterns
  - Reduces context rot in long analysis tasks
- **Headless mode:** `mcp-reva` via uvx, creates ephemeral projects in `.reva/projects/`
- **Claude Code marketplace:** Skills for Binary Triage, Deep Analysis, Crypto Analysis, CTF
- **Last release:** v7.1.1, January 7 2026 — actively maintained
- **Assessment:** Most mature, best design, actively maintained — **primary recommendation**

---

## 2026 SOTA: AI-Assisted Reverse Engineering

### What's Changed
The field moved from "GUI tool with AI chat" to "headless agentic workflows" in 2025-2026.

### Winning Patterns
1. **Headless-first** — pyghidra is the NSA's official Python bridge to Ghidra internals
2. **LLM-optimized tool design** — tools return context (xrefs, namespaces, related symbols) not just raw data
3. **P-code access** — intermediate representation enables cross-architecture semantic reasoning
4. **Transaction/undo** — safe mutation for multi-step agentic analysis with rollback
5. **Multi-MCP composition** — RE server + GitHub MCP + web search = full research pipeline

### Key Technologies
- **pyghidra** — NSA's Python bridge to Ghidra JVM (requires matching Python/JDK versions)
- **Ghidra 12.0** — required for headless pyghidra support (check your version!)
- **FastMCP 3.x** — our fleet SOTA (already in venv)
- **Streamable HTTP transport** — ReVa uses this, allows multiple clients to same Ghidra instance

### Ghidra Version Check (Critical)
Run in PowerShell to check:
```powershell
# Find ghidraRun.bat
Get-ChildItem "D:\*" -Recurse -Name "ghidraRun.bat" -ErrorAction SilentlyContinue | Select-Object -First 3
```
- Ghidra 11.x → LaurieWired only (no headless pyghidra support)
- Ghidra 12.0+ → ReVa headless + ghidra-headless-mcp possible

---

## Recommended Next Steps

### Immediate (hours)
1. Check Ghidra version installed on Goliath
2. If Ghidra 12.0+: install ReVa via `uvx --from reverse-engineering-assistant mcp-reva`
3. Add ReVa to Claude Desktop config with `GHIDRA_INSTALL_DIR`

### Short Term (days)
4. Test `ghidra-headless-mcp` on Windows — mrphrazer's fake backend mode works without Ghidra
5. Decide: pivot reversing-mcp to static-analysis-only companion server
6. Remove redundant LaurieWired bridge from our server (it adds no value)
7. Clean up: pick one web UI (web_sota Vite is cleaner than Next.js)

### Medium Term (1-2 weeks)
8. Implement proper headless Ghidra integration (via pyghidra or subprocess)
9. Add `.gitignore` for `external/` repos (they shouldn't be committed as subdirs)
10. Consider glama.json publication if server scope is clarified

---

## Claude Desktop Config (ReVa)
```json
{
  "mcpServers": {
    "ReVa": {
      "command": "uvx",
      "args": ["--from", "reverse-engineering-assistant", "mcp-reva"],
      "env": {
        "GHIDRA_INSTALL_DIR": "D:\\path\\to\\ghidra"
      }
    }
  }
}
```

## Claude Desktop Config (ghidra-headless-mcp, fake mode for testing)
```json
{
  "mcpServers": {
    "ghidra-headless": {
      "command": "python",
      "args": [
        "D:\\Dev\\repos\\reversing-mcp\\external\\ghidra-headless-mcp\\ghidra_headless_mcp.py",
        "--fake-backend"
      ]
    }
  }
}
```

---

## Files of Interest

| File | Purpose |
|------|---------|
| `src/reversing_mcp/server.py` | Main MCP server, 1034 lines |
| `src/reversing_mcp/bridge_mcp_ghidra.py` | LaurieWired HTTP bridge |
| `src/reversing_mcp/analyzers.py` | PE, entropy, strings, hexdump |
| `docs/GHIDRA.md` | Ghidra setup notes |
| `ROADMAP.md` | Future direction analysis |
| `ASSESSMENT.md` | Existing self-assessment |
| `debug_proj.gpr` | Actual Ghidra project (real reversing done) |
| `external/GhidraMCP` | LaurieWired cloned |
| `external/ghidra-headless-mcp` | mrphrazer cloned |
| `external/reverse-engineering-assistant` | ReVa/cyberkaida cloned |

---

## Related Projects
- `directmedia-mcp` — Directmedia .DKI decoder (optional import in server.py)
- `mcp-central-docs` — This file lives here

## Tags
`[reversing-mcp, ghidra, python, reverse-engineering, mcp, in-progress, high]`
