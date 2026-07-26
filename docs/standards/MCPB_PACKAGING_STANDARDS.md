# MCPB & Glama Packaging Standards (SOTA v2.0)

**Version:** 2.2 (June 2026)  
**Status:** Official Fleet Standard  
**Framework**: FastMCP 3+ (floor: 3.2+, current SOTA: 3.4.x)  

---

## 🛠️ 1. Core Tooling: uv + justfile

Modern fleet Python repos MUST use **Astral uv**. Legacy `pip` or `requirements.txt` are deprecated for internal development.

### 1.1. Universal `justfile` Recipes
Every MCP server repository MUST include a root **`justfile`** with these standard recipes:

```justfile
# Bundle for Claude Desktop (MCPB)
mcpb-pack:
    mcpb pack . dist/{{name}}-v{{version}}.mcpb

# Serve for local testing
serve:
    uv run {{cmd}} --serve

# Standard lint/format
lint:
    uv run ruff check .
    uv run ruff format --check .
```

---

## 📦 2. MCPB (Claude Desktop) Architecture

### 2.1. Required Structure
```
mcp-server/
├── manifest.json          # v0.2 Standard
├── assets/
│   ├── icon.png          # 256x256px identifying icon
│   └── prompts/          # SOTA Prompting (3-4-100 Rule)
│       ├── system.md     # 3,000+ words of core capabilities
│       ├── user.md       # 4,000+ words of tutorials
│       └── examples.json # 100+ structured tool call mappings
├── src/                  # Self-contained source code
└── README.md            # Installation & Usage
```

### 2.2. Manifest.json (v0.2)
```json
{
  "manifest_version": "0.2",
  "name": "your-package-name",
  "version": "1.0.0",
  "description": "FastMCP 3+ server description",
  "author": { "name": "Your Name/Team" },
  "server": {
    "type": "python",
    "entry_point": "src/package_name/server.py",
    "mcp_config": {
      "command": "python",
      "args": ["-m", "package_name.server"],
      "env": {
        "PYTHONPATH": "${PWD}",
        "PYTHONUNBUFFERED": "1"
      }
    }
  },
  "tools": [
    { "name": "tool_name", "description": "High-level summary" }
  ]
}
```

### 2.3. Package Inclusions & Exclusions

To ensure Claude Desktop can successfully interpret and run the bundle, follow these strict rules:

| Category | **IN (Mandatory)** | **OUT (Forbidden)** |
|----------|-------------------|----------------------|
| **Metadata** | `manifest.json` | `glama.json`, `pyproject.toml`, `uv.lock` |
| **Logic** | `src/` (Self-contained) | `.venv/`, `node_modules/`, `__pycache__/` |
| **Assets** | `assets/icon.png`, `assets/prompts/*` | `.git/`, `.github/`, `.vscode/` |
| **Docs** | `README.md`, `CHANGELOG.md` | `llms.txt`, `llms-full.txt` |

> [!CAUTION]
> Including a `.venv` or `node_modules` inside the `.mcpb` will significantly increase package size and may cause Claude Desktop to reject the bundle due to platform-specific binary conflicts.

### 2.4. Exclusion Mechanism (.mcpbignore)

The `mcpb` CLI uses a **`.mcpbignore`** file (syntax identical to `.gitignore`) to filter files during the packing process. Every SOTA repository MUST include this file to prevent environmental leakage.

#### Standard `.mcpbignore` Template:
```text
# Logic/Dev Bloat
.venv/
node_modules/
__pycache__/
.ruff_cache/
.pytest_cache/
tests/

# Discovery & Fleet Metadata
glama.json
llms.txt
llms-full.txt
.git/
.github/
.vscode/

# Build Artifacts
dist/
build/
*.mcpb
```

---

## 🌐 3. Discovery & Registry (glama.json)

The `glama.json` manifest is for **external indexing** (glama.ai) and MUST be excluded from the `.mcpb` bundle.

```json
{
  "mcpServers": {
    "server-id": {
      "command": "python",
      "args": ["-m", "src.package.server"],
      "env": { "PYTHONPATH": "${workspaceFolder}" },
      "capabilities": {
        "tools": { "enabled": true },
        "prompts": { "enabled": true }
      },
      "metadata": {
        "version": "1.0.0",
        "tags": ["category", "tool-type"],
        "homepage": "https://github.com/..."
      }
    }
  }
}
```

---

## 🚀 4. CI/CD (GitHub Actions 2026)

Always use `@v4` or `@v5` for core actions.

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v1
      - name: Build MCPB
        run: |
          bunx @anthropic-ai/mcpb pack . dist/package.mcpb
      - uses: actions/upload-artifact@v4
        with:
          name: release-bundle
          path: dist/
```

---

## 🔧 5. CLI Installation & Usage

The Anthropic `mcpb` CLI is a Node.js-based tool used to bundle and validate your MCP server.

### 5.1. Installation
```powershell
# Use bunx (no global install needed)
bunx @anthropic-ai/mcpb --version

# Or global install if preferred
bun add -g @anthropic-ai/mcpb
mcpb --version
```

### 5.2. Core Commands
| Command | Purpose |
|---------|---------|
| `mcpb pack <dir> <output.mcpb>` | Create a bundle from a SOTA layout. |
| `mcpb validate <file>` | Check a `manifest.json` or `.mcpb` for errors. |
| `mcpb inspect <file.mcpb>` | List the contents and manifest of a bundle. |

> [!WARNING]
> **FORBIDDEN**: Never use `mcpb init` or `mcpb create`. These commands generate legacy/broken manifests that do not comply with v2.0 SOTA standards. Always author your layout manually according to Section 2.
```

---

*Last Updated: June 16, 2026*  
*Standard maintained by the Antigravity SOTA Fleet.*
