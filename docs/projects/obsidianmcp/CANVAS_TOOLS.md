# ObsidianMCP Canvas Tools

## Overview

Canvas tools enable programmatic creation and manipulation of Obsidian Canvas files through MCP.

Canvas files are JSON documents following the [JSON Canvas 1.0](https://jsoncanvas.org) specification.

## Available Tools

| Tool | Description |
|------|-------------|
| `list_canvases` | List all .canvas files in vault |
| `read_canvas` | Read and parse canvas content |
| `create_canvas` | Create new canvas with nodes/edges |
| `add_canvas_node` | Add node to existing canvas |
| `add_canvas_edge` | Add edge connecting nodes |
| `delete_canvas` | Delete canvas (with optional backup) |

## Node Types

| Type | Use Case | Required Fields |
|------|----------|-----------------|
| `text` | Markdown content card | `text` |
| `file` | Link to vault file | `file` |
| `link` | URL/web link | `url` |
| `group` | Container for nodes | `label` |

## Example Usage

### Create a Simple Diagram

```python
# Create canvas with two text nodes
canvas = await create_canvas(
    name="Architecture",
    folder="diagrams",
    nodes=[
        {
            "type": "text", 
            "text": "# Frontend\nReact + TypeScript",
            "x": 0, "y": 0, "width": 200, "height": 100,
            "color": "1"
        },
        {
            "type": "text",
            "text": "# Backend\nPython + FastAPI", 
            "x": 300, "y": 0, "width": 200, "height": 100,
            "color": "2"
        }
    ],
    edges=[
        {"fromNode": "node1", "toNode": "node2", "label": "REST API"}
    ]
)
```

### Add Nodes Dynamically

```python
# Add a new node to existing canvas
node = await add_canvas_node(
    canvas_path="diagrams/Architecture.canvas",
    node_type="text",
    x=150, y=200,
    text="# Database\nPostgreSQL",
    color="3"
)

# Connect it to existing node
edge = await add_canvas_edge(
    canvas_path="diagrams/Architecture.canvas",
    from_node="backend-id",
    to_node=node.id,
    label="SQL"
)
```

### List and Read

```python
# List all canvases
canvases = await list_canvases()
for c in canvases:
    print(f"{c.name}: {c.node_count} nodes, {c.edge_count} edges")

# Read specific canvas
content = await read_canvas("diagrams/Architecture.canvas")
for node in content.nodes:
    print(f"  {node.type}: {node.text or node.file}")
```

## Colors

Obsidian canvas supports these preset colors:
- `"1"` - Red
- `"2"` - Orange
- `"3"` - Yellow
- `"4"` - Green
- `"5"` - Cyan
- `"6"` - Purple

Or use hex codes: `"#FF5733"`

## Auto-Generated IDs

When creating nodes/edges without explicit IDs, 8-character hex IDs are auto-generated:

```python
node = await add_canvas_node(...)
print(node.id)  # e.g., "a1b2c3d4"
```

## Backup Protection

`delete_canvas` creates backups by default:

```python
# Moves to .obsidian-mcp-backups/Architecture_20251128_143022.canvas
await delete_canvas("Architecture.canvas")

# Permanent delete (no backup)
await delete_canvas("temp.canvas", backup=False)
```

## Integration with ADN

ADN can export notes to Obsidian canvas format:

```python
# Export ADN notes as canvas nodes
await adn_export("canvas", 
    folder="/development/mcp",
    export_path="~/Documents/claude-depot/canvases/"
)
```

This creates a visual representation of note relationships.

## Technical Details

- Canvas files are plain JSON with `.canvas` extension
- Positions are in pixels (origin top-left)
- Edges support `fromSide`/`toSide` for precise connection points
- File nodes use vault-relative paths

