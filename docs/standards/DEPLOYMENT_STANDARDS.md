# Deployment & Installation Patterns

## 1. Zero-Install Execution (Preferred)

To maintain friction-less operation, all servers should support:

- **Python**: `uvx <package-name>`
- **Node.js**: `npx -y <package-name>`

## 2. Developer Setup ("Clone & Connect")

1.  **Clone**: `git clone <repo_url> D:/Dev/repos/<server-name>`
2.  **Environment**: Use `uv sync` (Python) or `npm install` (Node). Prefer **`justfile`** recipes for `serve` / `test` / `lint` when present.

**README alignment (fleet):** Root **README.md** install snippets MUST NOT start at **`uv sync`** / **`npm install`** alone — they MUST show **clone (or equivalent source step)** first, then change into the repo root, then sync/install. Mirrors the order above so copy-paste installs work. Norm: **[DOCUMENTATION_STANDARDS.md](./DOCUMENTATION_STANDARDS.md) §1** (README.md bullet).
3.  **Config**: Register the absolute path to the entry point in `mcp_config.json`.
4.  **Packaging**: **`glama.json`** at repo root; **`.mcpb`** via **`mcpb pack`** per **[PACKAGING_STANDARDS.md §5](./PACKAGING_STANDARDS.md#5-python-mcp-repo-uv-justfile-llmstxt-glama-mcpb-pack)** and **[MCPB_PACKAGING_STANDARDS.md](./MCPB_PACKAGING_STANDARDS.md)** when distributing for Claude Desktop.

## 3. Auto-Discovery

- Register with **Glama.ai** using `glama.json`.
- Expose `/.well-known/mcp/manifest.json` for **LobeHub** discovery.

## 4. Production Substrate

- Use **Docker Compose** for deployments requiring persistent DBs (Postgres, Redis).
- Ensure ports fall within the **10700-11500** SOTA range.
