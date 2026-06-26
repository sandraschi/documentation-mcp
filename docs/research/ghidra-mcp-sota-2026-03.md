# AI-Assisted Reverse Engineering MCP — SOTA Research

**Date:** 2026-03-23  
**Context:** Assessment of Ghidra+MCP ecosystem for `reversing-mcp` project  
**Cloned repos:** `D:\Dev\repos\reversing-mcp\external\`

---

## Landscape Overview

As of March 2026, three significant repos exist for Ghidra+MCP integration. The ecosystem evolved rapidly in 2025 from "GUI plugin with HTTP bridge" to "headless agentic workflows via pyghidra". The shift is driven by the same force as everywhere: agentic AI workflows need automation, not GUI dependency.

---

## Repo 1: LaurieWired/GhidraMCP (7.6k ⭐)

**URL:** https://github.com/LaurieWired/GhidraMCP  
**Clone:** `external\GhidraMCP`  
**License:** Apache-2.0  
**Last release:** v1.4, June 23 2025  

### Architecture
```
[Claude Desktop / MCP Client]
        ↕ stdio MCP
[bridge_mcp_ghidra.py]  ← Python bridge script
        ↕ HTTP :8080
[GhidraMCP Java Plugin]  ← runs inside Ghidra GUI
        ↕ Ghidra Java API
[Ghidra GUI + loaded binary]
```

### What It Does
- Ghidra extension (Java, built with Maven) that starts an HTTP server inside Ghidra
- Python bridge script connects MCP clients to that HTTP server
- ~40 tools: decompile, list functions/classes/imports/exports/strings, rename functions/variables, xrefs, disassemble, comments, prototype setting

### Setup
1. Build or download GhidraMCP.zip from releases
2. Install into Ghidra via File → Install Extensions
3. Enable plugin in File → Configure → Developer → GhidraMCPPlugin
4. Start Ghidra, open project, load binary, run analysis
5. HTTP server starts automatically on :8080
6. Run bridge_mcp_ghidra.py to expose as MCP

### Strengths
- Community standard — most tutorials reference this
- Works reliably with Ghidra 10.x/11.x
- Simple architecture, easy to understand
- Pre-built releases available

### Weaknesses
- GUI-coupled — Ghidra must be running with binary loaded
- Not headless — can't run in CI or docker without display
- Bridge adds no value — is just an HTTP→MCP adapter
- 40 tools — limited compared to headless alternatives
- Last release June 2025 — some stagnation

### Our Use
Our `bridge_mcp_ghidra.py` is functionally identical to LaurieWired's bridge. We added no value here.

---

## Repo 2: mrphrazer/ghidra-headless-mcp (24 ⭐)

**URL:** https://github.com/mrphrazer/ghidra-headless-mcp  
**Clone:** `external\ghidra-headless-mcp`  
**License:** GPL-2.0  
**Author:** Tim Blazytko — well-known RE researcher (@mr_phrazer)  
**Status:** Very new, March 2026, 3 commits  
**Note from README:** "This entire project—code, tests, and documentation—is 100% vibe coded."

### Architecture
```
[MCP Client]
    ↕ stdio or TCP MCP
[ghidra_headless_mcp.py]
    ↕ pyghidra Python API
[Ghidra JVM — headless, no GUI]
```

### What It Does
- **212 tools** across **34 feature groups** — by far the most comprehensive
- Uses `pyghidra` (NSA's official Python bridge to Ghidra JVM)
- No GUI required — purely headless
- Fake backend mode — run without Ghidra for CI/testing

### Feature Groups (34 total)
- Core: analysis, health, task management
- Program lifecycle: open/close/save/export, project management
- Transactions: begin/commit/undo/redo — safe mutation
- Listing: disassemble, code units, data definitions
- Memory: read/write raw bytes, block management
- Patching: assemble, NOP, branch inversion
- Symbols/namespaces/externals/references
- Comments, bookmarks, tags, metadata, source maps, relocations
- Functions: create/delete/rename/body/signature/callers/callees/batch
- Types/structs/enums/unions: full type system access
- Variables/parameters/stack frames
- **Decompiler**: decomp, AST, tokens, type tracing, writeback
- **P-code**: per-instruction, per-function, per-block, varnode uses
- **Graph**: basic blocks, CFG edges, call paths
- **Search**: bytes, constants, strings, instructions, p-code, text
- **Scripting**: `ghidra.eval`, `ghidra.call`, `ghidra.script` — arbitrary

### Unique Capabilities Not in Other Repos
- **P-code access** — Ghidra's intermediate representation, architecture-agnostic semantics
- **Transaction management** — safe agentic mutation with rollback
- **CFG + basic block extraction** — enables control flow analysis
- **Type system full access** — define structs, enums, unions from C declarations
- **`ghidra.eval`** — execute arbitrary Python inside Ghidra's runtime
- **Fake backend** — develop/test without Ghidra installed

### Installation
```powershell
# In powershell, from repo root
python -m venv .venv
.\.venv\Scripts\activate
pip install .

# Run with fake backend (no Ghidra needed)
python ghidra_headless_mcp.py --fake-backend

# Run with real Ghidra
$env:GHIDRA_INSTALL_DIR = "D:\path\to\ghidra"
python ghidra_headless_mcp.py
```

### Limitations
- Very new — 3 commits, 24 stars, no releases
- GPL-2.0 license (more restrictive than Apache)
- Windows untested (likely works, pyghidra is cross-platform)
- Requires Ghidra 11.1+ with pyghidra support (exact version TBD)
- pyghidra Python version must match Ghidra's bundled Jython — can be fiddly

### Assessment
**Architecturally correct for 2026.** The tool count and feature depth are unmatched. The "vibe coded" disclaimer is honest but the test suite and CI enforcement suggest real quality. The main risk is Windows compatibility and pyghidra version alignment.

---

## Repo 3: cyberkaida/reverse-engineering-assistant — ReVa (619 ⭐)

**URL:** https://github.com/cyberkaida/reverse-engineering-assistant  
**Clone:** `external\reverse-engineering-assistant`  
**License:** Apache-2.0  
**Last release:** v7.1.1, January 7 2026 — actively maintained  
**Requires:** Ghidra 12.0+ (for headless mode)

### Architecture — Two Modes

**Assistant Mode (Ghidra GUI running):**
```
[MCP Client — Claude Code / VSCode]
    ↕ Streamable HTTP MCP
[ReVa MCP endpoint :8080/mcp/message]
    ↕ Ghidra Java API (inside running Ghidra)
[Ghidra GUI + loaded binary]
```

**Headless Mode (no GUI):**
```
[MCP Client]
    ↕ stdio MCP
[mcp-reva process]
    ↕ PyGhidra / ReVaHeadlessLauncher
[Ghidra headless JVM]
[Projects stored in .reva/projects/]
```

### What It Does
- Ghidra extension + Python MCP server
- Both interactive (assist ongoing analysis) and automated (headless batch) workflows
- Projects in headless mode are ephemeral and auto-cleaned
- Can work on multiple files in same project

### Design Philosophy (Key Differentiator)
> "ReVa provides smaller, critical fragments with reinforcement and links to other relevant information to reduce context usage and hallucination."

Each tool returns **surrounding context** — namespace, xrefs, related symbols — not just raw data. This is explicitly designed to:
- Reduce LLM hallucination in long RE tasks
- Combat "context rot" (stale/irrelevant context accumulation)
- Encourage human-like binary exploration patterns
- Handle large binaries and entire firmware images

### Claude Code Integration
```bash
# Install
uv tool install reverse-engineering-assistant

# Add to Claude Code
claude mcp add --scope user ReVa -- mcp-reva

# Add with Ghidra path
export GHIDRA_INSTALL_DIR=/path/to/ghidra
claude mcp add --scope user ReVa -- mcp-reva
```

### Claude Code Marketplace Skills
```bash
claude plugin marketplace add cyberkaida/reverse-engineering-assistant
```
Skills included:
- **Binary Triage** — quick initial assessment
- **Deep Analysis** — comprehensive function-level analysis
- **Cryptography Analysis** — find and analyze crypto usage
- **CTF guides** — structured CTF problem solving

### Claude Desktop Config (Assistant Mode)
```json
{
  "mcpServers": {
    "ReVa": {
      "type": "http",
      "url": "http://localhost:8080/mcp/message"
    }
  }
}
```

### Claude Desktop Config (Headless Mode)
```json
{
  "mcpServers": {
    "ReVa": {
      "command": "mcp-reva",
      "env": {
        "GHIDRA_INSTALL_DIR": "D:\\path\\to\\ghidra"
      }
    }
  }
}
```

### Limitations
- **Requires Ghidra 12.0+** — hard requirement for headless
- Java + Python dual stack (Gradle build for extension)
- Less comprehensive tool set than ghidra-headless-mcp (no p-code, no raw transaction control)
- Streamable HTTP transport — not all MCP clients support it yet (VSCode incompatibility fixed in v7.1.1)

### Assessment
**Primary recommendation.** Most mature, actively maintained, best LLM-optimized design. The context-aware tool design is a genuine insight that reduces the classic LLM RE failure mode of asking for too much at once. Apache-2.0 license is clean.

---

## Comparison Table

| Feature | LaurieWired | ghidra-headless-mcp | ReVa |
|---------|-------------|---------------------|------|
| Stars | 7.6k | 24 | 619 |
| Headless | ❌ | ✅ | ✅ (12.0+) |
| Tool count | ~40 | 212 | ~50 |
| P-code | ❌ | ✅ | ❌ |
| Transactions | ❌ | ✅ | ❌ |
| Ghidra scripting | ❌ | ✅ | partial |
| LLM-optimized | ❌ | partial | ✅ |
| Claude marketplace | ❌ | ❌ | ✅ |
| Windows tested | ✅ | ❓ | ✅ |
| License | Apache-2.0 | GPL-2.0 | Apache-2.0 |
| Maintained | stagnating | new | active |
| Min Ghidra | 10.x | 11.1+ | 12.0+ |

---

## pyghidra Notes

pyghidra is NSA's official Python bridge to Ghidra. It allows calling Ghidra's Java API from Python without a GUI.

Key requirements:
- Ghidra 11.1+ for basic pyghidra support
- Ghidra 12.0+ for headless scripting support used by ReVa
- Python version must be compatible with the JVM (usually Python 3.10-3.12)
- `GHIDRA_INSTALL_DIR` environment variable must point to Ghidra installation

Check pyghidra status:
```python
import pyghidra
pyghidra.start()
print("pyghidra works")
```

Common issue on Windows: JVM class path conflicts. Set `JAVA_HOME` to Ghidra's bundled JDK if needed:
```powershell
$env:JAVA_HOME = "D:\path\to\ghidra\support\JDK"
```

---

## Recommended Reading

- Ghidra source: https://github.com/NationalSecurityAgency/ghidra
- pyghidra docs: https://github.com/NationalSecurityAgency/ghidra/tree/master/Ghidra/Features/PyGhidra
- Tim Blazytko's work: https://synthesis.to/ (binary analysis, deobfuscation)
- cyberkaida streams: https://twitch.tv/cyberkaida (RE live coding)
- "The Ghidra Book" — Chris Eagle & Kara Nance (No Starch Press)

## Tags
`[research, ghidra, reverse-engineering, mcp, ai-reversing, sota, 2026, high]`
