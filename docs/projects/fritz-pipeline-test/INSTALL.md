# INSTALL — fritz-pipeline-test

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (Astral)

## Install

```bash
git clone https://github.com/sandraschi/fritz-pipeline-test.git
cd fritz-pipeline-test
uv sync
```

## Run

```bash
uv run fritz-pipeline-test   # CLI greeter
uv run pytest tests/ -q      # tests
```

## MCP configuration

Add to your MCP client config:

```json
{
  "mcpServers": {
    "fritz-pipeline-test": {
      "command": "uv",
      "args": ["run", "--directory", "PATH\\TO\\fritz-pipeline-test", "fritz-pipeline-test"]
    }
  }
}
```
