# Inkscape MCP: The Agentic Control Layer

The Inkscape MCP server enables the Antigravity agent to programmatically edit and export SVG data structures.

## 🚀 Server Registration

```json
{
  "inkscape": {
    "command": "python",
    "args": ["-m", "inkscape_mcp.server"],
    "cwd": "D:/Dev/repos/inkscape-mcp",
    "env": {
      "INKSCAPE_PATH": "C:/Program Files/Inkscape/bin/inkscape.exe"
    }
  }
}
```

## 🛠️ Tool Catalog

| Tool | Action | Use Case |
| :--- | :--- | :--- |
| `edit_svg_element` | Manipulation | Changes text, colors, or positions of specific SVG IDs. |
| `export_to_bitmap` | Conversion | Renders an SVG into a high-res PNG for documentation. |
| `generate_topology_node` | Construction | Spawns a standardized schematic symbol (e.g., an MCP Server icon). |
| `batch_simplify_vector` | Optimization | Path-reduction for complex SVG files. |

## 📊 Interaction Principles

- **ID-Based Targeting**: Agents should use unique `id` attributes for all SVG elements to ensure precise targeting.
- **Verification**: Post-export validation of resolution and file size is mandatory.

---
*Last updated: 2026-02-14*
