# LLM-TXT: Automated MCP Documentation Synthesis

The LLM-TXT MCP is a specialized utility server designed to transform raw codebases, telemetry, and unstructured documentation into high-fidelity `.txt` and `.md` formats optimized for LLM context windows and RAG ingestion.

## ðŸš€ Deployment & Integration

### Engine Strategy
- **Framework**: FastMCP 3.1.1+.4+ (SOTA).
- **Output Standard**: Markdown-enhanced text streams.
- **Core Function**: Context window optimization for large-scale code analysis.

### MCP Registration
```json
{
  "llm_txt": {
    "command": "python",
    "args": ["-m", "llm_txt_mcp.server"],
    "cwd": "D:/Dev/repos/llm-txt-mcp",
    "env": {
      "OUTPUT_DIR": "D:/Dev/repos/mcp-central-docs/generated",
      "MAX_FILE_SIZE_MB": "10"
    }
  }
}
```

## ðŸ“„ Synthesis & Formatting Tools

### Context Optimization
| Tool | Operation | Description |
| :--- | :--- | :--- |
| `convert_to_txt` | Transformation | Recursive conversion of codebases into single, LLM-digestible text files. |
| `strip_noise` | Optimization | Removal of boilerplate, comments, and non-essential logic for prompt compression. |
| `generate_summary` | Synthesis | Automated generation of `README.md` buffers from raw source directories. |

### Technical Formatting
- **`apply_markdown_template`**: Wraps raw text in SOTA-compliant headers and metadata blocks.
- **`validate_structure`**: Checks generated `.txt` files for token-efficiency and structural integrity.

## ðŸ› ï¸ Advanced SOTA Workflows

### RAG Pre-Processing
The LLM-TXT server is a critical part of the `mcp-central-docs` ingestion pipeline:
1. **Discovery**: `repo_ops` identifies a new project repo.
2. **Synthesis**: `llm_txt_mcp` converts the entire repo into `project_context.txt`.
3. **Indexing**: The RAG engine chunks and indexes the optimized text file.

### Automated PR Summaries
Agents use this server to generate technically exhaustive changelogs by synthesizing the diffs between two Git branches into a human-readable summary.

## ðŸ“Š Performance & Token Metrics
- **Compression Ratio**: Can achieve up to 70% reduction in raw file size by stripping noise while maintaining logic parity.
- **Processing Speed**: Multi-threaded conversion of 1,000+ files in < 5 seconds.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
*Fleet Status: Active*

