# Ghidra MCP — State of the Art, March 2026

**Research date:** 2026-03-23  
**Context:** Assessment of AI-assisted reverse engineering tooling for `reversing-mcp` project

---

## ⚠️ Core Architectural Constraint: LaurieWired Requires a Human at the PC

Before comparing approaches, this must be understood clearly:

**LaurieWired/GhidraMCP is not headless and cannot be made headless.**

It is built around the Ghidra GUI plugin model: the plugin runs *inside* a running
Ghidra instance, exposes a local HTTP server, and assumes a human has already:
1. Opened Ghidra
2. Created a project and imported the binary
3. Run auto-analysis
4. Manually started the plugin HTTP server

An agent or automated pipeline can do none of these steps. The agent can only call
tools against a session a human has already set up. The moment the human closes
Ghidra, all `ghidra_*` tools stop working.

**This is fundamentally a co-pilot architecture** — useful when a human reverse
engineer is actively working in Ghidra and wants AI assistance on the side. It is
not suitable for:
- Batch analysis of multiple binaries
- Overnight / unattended RE runs
- CI/CD pipeline integration
- Any scenario where no human is sitting at the PC

The two headless alternatives (mrphrazer and ReVa) solve this at the architecture
level via `pyghidra` — they can open Ghidra, load a binary, run analysis, and
execute the full RE workflow entirely without a GUI or human present.

---



### 1. LaurieWired/GhidraMCP — Community Standard (aging)

**GitHub:** https://github.com/LaurieWired/GhidraMCP  
**Stars:** 7.6k | **Forks:** 645 | **Last release:** v1.4 (June 2025)  
**Architecture:** Java Ghidra plugin (HTTP server :8080) + Python MCP bridge  
**License:** Apache-2.0

**How it works:**
```
MCP Client → bridge_mcp_ghidra.py → HTTP :8080 → Ghidra GUI plugin → Ghidra DB
```

**Tools:** ~40 tools (decompile, rename, xrefs, imports/exports, strings, segments)

**Setup:**
1. Install GhidraMCP plugin zip into Ghidra (File → Install Extensions)
2. Enable: File → Configure → Developer → GhidraMCPPlugin
3. Start Ghidra, load binary, run analysis
4. Start HTTP server (Edit → Tool Options → GhidraMCP HTTP Server)
5. Run `bridge_mcp_ghidra.py` as MCP server

**Claude Desktop config:**
```json
{
  "mcpServers": {
    "ghidra": {
      "command": "python",
      "args": [
        "D:\\Dev\\repos\\reversing-mcp\\src\\reversing_mcp\\bridge_mcp_ghidra.py",
        "--ghidra-server", "http://127.0.0.1:8080/"
      ]
    }
  }
}
```

**Pros:** Proven, large community, good documentation  
**Cons:** GUI-required (no headless), plugin must be manually started per session, not growing, ~40 tools only

---

### 2. mrphrazer/ghidra-headless-mcp — Newest, Most Comprehensive

**GitHub:** https://github.com/mrphrazer/ghidra-headless-mcp  
**Stars:** 24 | **Commits:** 3 | **No releases yet**  
**Architecture:** Pure Python via `pyghidra` — **no GUI needed**  
**License:** GPL-2.0  
**Author:** Tim Blazytko (@mr_phrazer)

**How it works:**
```
MCP Client → ghidra_headless_mcp.py → pyghidra → Ghidra headless JVM → binary
```

**Tools:** **212 tools across 34 feature groups** — far most comprehensive:
- Program lifecycle (open, save, export, sessions)
- Disassembly + patching (assemble, NOP, branch invert)
- Full type system (structs, enums, unions, C declarations)
- P-code access (basic blocks, CFG edges, varnode tracking)
- Decompiler writeback (commit recovered names/params to DB)
- Cross-references (memory, register, stack, external)
- Transactions + undo/redo for safe mutation
- Raw Ghidra scripting via `ghidra.eval` / `ghidra.call`
- Search (bytes, constants, instructions, p-code, text)
- Graph extraction (call paths, CFG)

**Transports:** stdio (default) + TCP

**Fake backend mode:** Can run without Ghidra for CI/testing:
```
python ghidra_headless_mcp.py --fake-backend
```

**Setup:**
```bash
cd D:\Dev\repos\reversing-mcp\external\ghidra-headless-mcp
python -m venv .venv
.venv\Scripts\activate
pip install .
```

**Claude Desktop config:**
```json
{
  "mcpServers": {
    "ghidra_headless": {
      "command": "python",
      "args": [
        "D:\\Dev\\repos\\reversing-mcp\\external\\ghidra-headless-mcp\\ghidra_headless_mcp.py",
        "--ghidra-install-dir", "D:\\path\\to\\ghidra"
      ]
    }
  }
}
```

**Pros:** Headless (no GUI), most tools, p-code access, transactions/undo, proper agent design  
**Cons:** Very new (3 commits, no releases), Windows compatibility untested, pyghidra JVM startup is slow

**pyghidra note:** Requires Ghidra's bundled Python/JVM environment. Installation can be fiddly on Windows — pyghidra must match Ghidra's Jython version.

---

### 3. cyberkaida/reverse-engineering-assistant (ReVa) — Most Mature Headless

**GitHub:** https://github.com/cyberkaida/reverse-engineering-assistant  
**Stars:** 619 | **Forks:** 56 | **Last release:** v7.1.1 (Jan 7, 2026)  
**Architecture:** Ghidra extension (Java) with optional headless PyGhidra mode  
**License:** Apache-2.0  
**Requires:** **Ghidra 12.0+** (hard requirement for headless mode)

**Two operating modes:**

**Assistant mode** (GUI + HTTP):
```
MCP Client → HTTP :8080/mcp/message → ReVa plugin → Ghidra GUI
```

**Headless mode** (no GUI):
```
MCP Client → mcp-reva (stdio) → pyghidra → Ghidra headless JVM
```

**Design philosophy:** "Tool-driven approach — small tools designed for effective LLM use"
- Each tool returns context (namespace, xrefs) alongside primary data
- Reduces hallucination in long analysis chains
- Tolerates varied LLM inputs, redirects correctable mistakes
- Designed for large binaries and entire firmware images

**Claude Code marketplace integration:**
```bash
claude plugin marketplace add cyberkaida/reverse-engineering-assistant
```
Skills: Binary Triage, Deep Analysis, Cryptography Analysis, CTF guides

**Headless setup:**
```bash
# Set Ghidra install dir
$env:GHIDRA_INSTALL_DIR = "D:\path\to\ghidra"

# Install
pip install reverse-engineering-assistant

# Or via uv
uv tool install reverse-engineering-assistant
```

**Claude Desktop headless config:**
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

**Assistant mode config (GUI running):**
```json
{
  "mcpServers": {
    "ReVa": {
      "command": "npx",
      "args": ["@modelcontextprotocol/client-http", "http://localhost:8080/mcp/message"]
    }
  }
}
```
Or for Claude Code: `claude mcp add --scope user --transport http ReVa -- http://localhost:8080/mcp/message`

**Notable tools/capabilities:**
- Binary triage, deep analysis, crypto analysis workflows
- Can work with multiple files in same project
- Supports combining with GitHub MCP (source lookup) and Kagi MCP (web search)
- Manages project lifecycle in headless mode (ephemeral projects auto-cleaned up)

**Pros:** Most mature, actively maintained, best design philosophy, Claude Code skills, headless works  
**Cons:** Ghidra 12.0+ hard requirement, Java build from source required if building extension yourself

---

## Comparison Matrix

| Feature | LaurieWired | mrphrazer | ReVa (cyberkaida) |
|---------|-------------|-----------|-------------------|
| Stars | 7.6k | 24 | 619 |
| Headless mode | ❌ | ✅ | ✅ |
| GUI mode | ✅ | ❌ | ✅ |
| Tool count | ~40 | 212 | ~30-40 |
| P-code access | ❌ | ✅ | ❌ |
| Transactions/undo | ❌ | ✅ | ❌ |
| Type system tools | basic | full | basic |
| LLM-optimized tool design | ❌ | partial | ✅ |
| Windows tested | ✅ | ❓ | ✅ |
| Ghidra 12+ required | ❌ | ❌ | ✅ (headless) |
| Active maintenance | slowing | new | ✅ |
| Claude Code skills | ❌ | ❌ | ✅ |

---

## Ghidra Version Check

**Critical:** ReVa headless requires Ghidra 12.0+. mrphrazer's headless also benefits from 12.0+.

Check installed version:
```powershell
# Find ghidraRun.bat and check version
Get-ChildItem "D:\path\to\ghidra" -Filter "*.bat" | Select-String "GHIDRA_VERSION"
# Or
& "D:\path\to\ghidra\ghidraRun.bat" --version
```

**Ghidra download:** https://github.com/NationalSecurityAgency/ghidra/releases  
**Current stable:** 11.3 (Jan 2025) — Ghidra 12.0 may still be in development as of March 2026

> ⚠️ Check current Ghidra releases before assuming 12.0 is available!

---

## pyghidra Integration Notes

Both mrphrazer and ReVa headless use `pyghidra` — the NSA's official Python bridge to Ghidra.

**pyghidra install (Windows):**
```powershell
# pyghidra is bundled with Ghidra 11.1+
# Set GHIDRA_INSTALL_DIR, then:
pip install pyghidra

# Or use the bundled install script:
& "$env:GHIDRA_INSTALL_DIR\support\pyghidra_install.py"
```

**Known Windows issues:**
- JVM startup is slow (5-15 seconds first call)
- Path separators in GHIDRA_INSTALL_DIR must be correct
- Python version must be compatible with Ghidra's JVM

---

## 2026 integration patterns

The field has converged on these design principles for AI-assisted RE:

1. **Headless-first** — GUI plugins are useful interactively, but agentic workflows need headless
2. **Tool design for LLM consumption** — return context (xrefs, namespace, related symbols) not just raw data
3. **P-code access** — intermediate representation enables cross-architecture semantic reasoning
4. **Transaction/undo** — safe mutation for multi-step agent analysis with rollback capability
5. **Composition over monolith** — combine with other MCP servers (GitHub, web search) for richer analysis
6. **Fake/mock backends** — enable CI testing and development without full Ghidra install

---

## Recommended Action Plan for reversing-mcp

### Immediate (days)
1. Check Ghidra version installed on Goliath
2. Try ReVa in assistant mode (GUI) first — lowest friction, just install the extension
3. Clone and test mrphrazer's server with `--fake-backend` to understand tool surface

### Short term (1-2 weeks)
1. Test ReVa headless if Ghidra 12.0 is available
2. Test mrphrazer's headless on Windows (pyghidra path issues likely)
3. Decide: keep LaurieWired bridge or migrate to headless approach

### Architecture decision
- **Option A:** Drop Ghidra tools from reversing-mcp, use ReVa as dedicated Ghidra MCP
- **Option B:** Integrate mrphrazer's pyghidra backend into reversing-mcp directly
- **Option C (recommended):** reversing-mcp = static analysis + legacy formats companion; ReVa = Ghidra MCP

### Keep from reversing-mcp
- All static analysis tools (entropy, PE, hexdump, strings) — not in Ghidra servers
- Directmedia decompressor — unique capability
- Drop: LaurieWired HTTP bridge, both web frontends (or pick one)
