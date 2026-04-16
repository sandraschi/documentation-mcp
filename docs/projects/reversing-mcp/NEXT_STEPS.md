# reversing-mcp — Next Steps

**Created:** 2026-03-23  
**Based on:** Assessment session + GHIDRA_SOTA_2026.md (Ghidra/ReVa notes)

---

## Priority 1: Determine Ghidra Version (today)

```powershell
# Find Ghidra on Goliath — check common install paths
Get-ChildItem "D:\", "C:\Program Files\" -Filter "ghidra*" -Directory -Recurse -ErrorAction SilentlyContinue | Select-Object FullName

# Check version once found
Get-Content "D:\path\to\ghidra\Ghidra\application.properties" | Select-String "application.version"
```

**Decision gate:** Is Ghidra 12.0 available?
- Yes → ReVa headless is viable
- No (11.x) → Use ReVa in GUI/assistant mode OR update Ghidra first

---

## Priority 2: Install ReVa (assistant mode, this week)

ReVa in GUI/assistant mode works with Ghidra 11.x and is the least-friction path to a working headless-ish setup.

```powershell
# Download latest ReVa release for your Ghidra version from:
# https://github.com/cyberkaida/reverse-engineering-assistant/releases

# Install into Ghidra:
# 1. Start Ghidra
# 2. File → Install Extensions → + button → select ReVa zip
# 3. Restart Ghidra
# 4. Enable both plugins (Project view AND Code Browser)

# ReVa serves MCP on http://localhost:8080/mcp/message by default
```

**Add to `claude_desktop_config.json`:**
```json
{
  "mcpServers": {
    "ReVa": {
      "command": "python",
      "args": ["-m", "mcp.client.http"],
      "env": {}
    }
  }
}
```
(Claude Code is the preferred client: `claude mcp add --transport http ReVa http://localhost:8080/mcp/message`)

---

## Priority 3: Test mrphrazer headless with fake backend (this week)

```powershell
cd D:\Dev\repos\reversing-mcp\external\ghidra-headless-mcp

# Create venv
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install
pip install -e .

# Test fake backend (no Ghidra needed)
python ghidra_headless_mcp.py --fake-backend
# Should start, list tools via MCP

# List tools
# Connect with MCP inspector or Claude Desktop
```

---

## Priority 4: Decide Architecture (end of week)

After testing both, choose:

### Option A: reversing-mcp as companion server
```
Claude Desktop
├── ReVa (or ghidra-headless-mcp) → Ghidra analysis
└── reversing-mcp (slimmed) → static analysis + Directmedia
```

**reversing-mcp keeps:**
- `analyze_binary` (static tools only)
- `extract_strings`
- `get_hexdump`
- `analyze_entropy`
- `analyze_pe_file`
- `analyze_directmedia_file`
- `decompress_directmedia_library`

**reversing-mcp drops:**
- All `ghidra_*` tools (bridge to LaurieWired)
- `bridge_mcp_ghidra.py`
- `start_ghidra` (launch tool)
- One of the two web frontends

### Option B: Integrate pyghidra directly
Add pyghidra as optional dep to reversing-mcp, pull in mrphrazer's headless approach.
More work, more control, single server.

**Recommendation: Option A** — simpler, leverages best-of-breed tools, maintains focus.

---

## Cleanup Tasks (any time)

- [ ] Delete `reversing-webapp/` or `web_sota/` — pick one, document which
- [ ] Fix Python version mismatch — `.venv` uses 3.10, system has 3.13
- [ ] Update `glama.json` if planning Glama publication
- [ ] Mark `bridge_mcp_ghidra.py` as deprecated once replacement chosen
- [ ] Remove `server.py.bak` and `server.bak` files
- [ ] Add `external/` to `.gitignore` (reference clones, not part of project)

---

## glama.json Status

The `glama.json` exists but the server is not Glama-publication-ready:
- Tool descriptions need review (some are LaurieWired-dependent)
- Transport config needs updating for FastMCP 3.0 patterns
- Consider separating static-analysis tools into standalone Glama-publishable server

---

## Reference Resources

- Ghidra releases: https://github.com/NationalSecurityAgency/ghidra/releases
- pyghidra docs: https://github.com/NationalSecurityAgency/ghidra/tree/master/Ghidra/Features/PyGhidra
- ReVa releases: https://github.com/cyberkaida/reverse-engineering-assistant/releases
- mrphrazer headless: https://github.com/mrphrazer/ghidra-headless-mcp
- LaurieWired GhidraMCP: https://github.com/LaurieWired/GhidraMCP
- Ghidra Book: O'Reilly "The Ghidra Book" (Chris Eagle, Kara Nance)
