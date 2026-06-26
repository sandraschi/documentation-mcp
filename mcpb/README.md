# documentation-mcp (MCPB Bundle)

Public MCP Documentation Server - Federated RAG for the MCP ecosystem

## Usage

Add to \claude_desktop_config.json\:
\\\json
{
  "mcpServers": {
    "documentation-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "\D:\Dev\repos", "python", "-m", "documentation_mcp"],
      "env": { "PYTHONPATH": "\D:\Dev\repos/src" }
    }
  }
}
\\\

## Tools

- **persistence_store_memory**: persistence_store_memory
- **ask_docs**: ask_docs
- **agentic_doc_workflow**: agentic_doc_workflow

## Requirements

- Python 3.12+
- uv
