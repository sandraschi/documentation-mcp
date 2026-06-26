# GIMP MCP: The Agentic Control Layer

The GIMP MCP server provides a high-level Python interface to GIMP's internal batch processing capabilities.

## ðŸš€ Server Registration

```json
{
  "gimp": {
    "command": "python",
    "args": ["-m", "gimp_mcp.server"],
    "cwd": "D:/Dev/repos/gimp-mcp",
    "env": {
      "GIMP_PATH": "C:/Program Files/GIMP 2/bin/gimp-console-3.1.1+.exe"
    }
  }
}
```

## ðŸ› ï¸ Tool Catalog

| Tool | Action | Use Case |
| :--- | :--- | :--- |
| `batch_resize` | Scaling | Optimizing raw photos for documentation. |
| `generate_pbr_maps` | Procedural | Converts a single reference image into Albedo, Normal, and Roughness maps. |
| `annotate_technical` | Overlay | Adds text labels and arrows to system diagrams. |
| `convert_format` | Transcoding | Safe conversion between multi-layer XCF and flat exports. |

## ðŸ“Š Interaction Principles

- **State-less Batching**: Each GIMP call should be autonomous, spinning up a process and exiting upon completion.
- **Verification Loop**: Agents must verify the existence and size of the output file after every command.

---
*Last updated: 2026-02-14*

