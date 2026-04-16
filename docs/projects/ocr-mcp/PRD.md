# OCR-MCP – Product Requirements Document

**Version**: 0.2.0-alpha  
**Framework**: FastMCP 3.1  
**Last Updated**: 2026-03-16  

## Product Vision

OCR-MCP is a document understanding MCP server that provides multi-engine OCR, scanner control (Windows WIA), and FastMCP 3.1 features: **sampling**, **agentic workflow tool** (SEP-1577), **prompts**, and **skills** resource for LLM-oriented use.

## Goals

- Expose OCR, preprocessing, analysis, and workflow tools via MCP with a single, discoverable surface.
- Support agentic document workflows via `ctx.sample_step()` and the `agentic_document_workflow` tool.
- Provide prompts and a skills resource so clients and LLMs can use the server without reading code.
- Integrate WIA scanners (Windows) with stable discovery and scan execution.

## Requirements Summary

### Functional

| Area | Requirement | Status |
|------|-------------|--------|
| Framework | FastMCP 3.1 (sampling, prompts, resources) | ✅ |
| Sampling | Sampling handler; tools can use ctx.sample / sample_step | ✅ |
| Agentic workflow | agentic_document_workflow with sample_step + tools loop | ✅ |
| Prompts | process-instructions, quality-assessment-guide, scanner-workflow, batch-processing-guide, agentic-workflow-instructions | ✅ |
| Resources | logs, capabilities, skills (LLM-oriented reference) | ✅ |
| OCR backends | 10+ engines (PaddleOCR-VL-1.5, DeepSeek-OCR-2, olmOCR-2, etc.) with auto-selection | ✅ |
| Scanner | WIA 2.0 (Windows); stable discovery (single-thread executor, no CoUninitialize on release) | ✅ |
| Portmanteau tools | document_processing, image_management, scanner_operations, workflow_management | ✅ |
| Web UI | React frontend + FastAPI backend for upload, scan, batch, pipelines | ✅ |

### Non-Functional

- **Python**: 3.12+
- **Dependencies**: fastmcp>=3.1, no `[server]` extra required
- **Transport**: stdio; optional HTTP/Streamable via transport module
- **Docs**: CHANGELOG, README, PLACEHOLDER_AUDIT, extension.toml, mcpb.json

## Out of Scope (Current)

- TWAIN / SANE scanner backends
- Linux/macOS scanner support
- Cloud-only deployment (server runs locally)

## References

- **Repo**: [ocr-mcp](https://github.com/sandraschi/ocr-mcp)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Status**: [STATUS.md](STATUS.md)
- **Integration**: [integrations/ocr-mcp/OCR_MCP_INTEGRATION_GUIDE.md](../../integrations/ocr-mcp/OCR_MCP_INTEGRATION_GUIDE.md)
- **Master plan**: In-repo `OCR-MCP_MASTER_PLAN.md`
